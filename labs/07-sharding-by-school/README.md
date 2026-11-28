# Lab 07: sharding Lampus by school

Course topic 7 (sharding and partitioning). **A design write-up plus a small simulation.** Lampus runs on one Postgres and doesn't need shards yet. Running real shards would mean several database servers, which is outside this course's budget. So this lab decides *how* Lampus would be split when the time comes, and uses a simulation to choose the way schools are placed on shards. The school sizes are **synthetic**.

```bash
python labs/07-sharding-by-school/simulate.py   # standard library only, about a second
```

## Why shard, and when

Step 9 already spread the *reading* of searches over a replica. Writes all still go to one primary: messages, usage, audit rows, builds. Sharding splits the data itself over several primaries, so each one holds and writes only part of it.

Lampus doesn't need this yet. Signs that it would:

- writes on the primary keep it busy even after the slow queries are fixed;
- the data, mostly chunks and their vectors, no longer fits one server's memory and disk at a sensible price;
- one big school's exam week slows every other school.

Until then a single primary with replicas is simpler, and every query keeps working.

## The shard key: `school_id`

Almost everything in Lampus belongs to one school: its students, their conversations and usage, the school's bots, documents and chunks. A school's queries never need another school's data. So `school_id` is the shard key: every row of a school lives on the same shard, and a request touches one shard only.

The schema has no `school_id` yet. Schools become tenants in a later phase, and this column comes with them.

| Table (today) | Where it goes | Note |
| --- | --- | --- |
| `users`, `sessions`, `grants` | the school's shard | add `school_id`; a login looks up the school first (below) |
| `threads`, conversation checkpoints | the school's shard | |
| `usage`, `idempotency_keys` | the school's shard | quotas and keys are per student, so they stay local |
| `audit` | the school's shard | one hash chain **per school** instead of one global chain |
| `chunks`, `source_files`, `ingest_runs` | the school's shard | a school's searches stay on its shard; vectors are most of the data |
| `builds`, `build_events` | the school's shard | |
| **schools directory** (new) | a small global database, cached | `school_id → shard`, plus the login domain or code |
| shared bots and public course material | copied to every shard | read-only, small: a "reference table" |

### What gets harder

- **Finding the shard.** Every request must know its school before it can query. A student's login or token carries `school_id`; the API looks up the shard in the directory (cached in Redis and in memory, so not a database trip per request).
- **Questions across schools,** such as "turns per day for all schools": run on every shard and add up the results (scatter-gather). That's for admin reports, which can be slow, or for an analytics copy fed from all shards.
- **Uniqueness across schools.** A username is unique *within* a school; the primary keys become `(school_id, username)`.
- **Moving a school** from one shard to another: copy its rows, catch up on new writes, switch the directory entry, delete the old rows. While the switch happens, its writes must pause for a moment or be redirected.

## Placing schools on shards: the simulation

`simulate.py` makes 1,000 synthetic schools, with sizes like real ones: a few large, many small (rank *r* has about 4000 / *r*^0.9 students, at least 30, ±20%). That gives 52,658 students, and the biggest school has 3,718 of them (7.1%). It then compares three ways to place schools:

- **hash mod N:** `shard = hash(school_id) % N`. No lookup table.
- **Consistent hashing:** a hash ring with 100 points per shard. Adding a shard takes over only the arcs next to its points.
- **Directory:** a table `school → shard`. Schools are placed largest first on the emptiest shard. To add a shard, schools are moved onto it, smallest first, until it holds its share.

Two numbers: **imbalance**, the fullest shard's students over the average shard (1.00 is perfect), and **moved**, the share of students whose data changes server when a 5th shard joins 4.

| Placement | Imbalance, 4 shards | 8 shards | 16 shards | Moved, 4 → 5 shards | Imbalance after the 5th |
| --- | --- | --- | --- | --- | --- |
| hash mod N | 1.24 | 1.62 | 2.02 | **75.5%** | 1.24 |
| Consistent hashing | 1.33 | 1.43 | 2.54 | 25.1% | 1.25 |
| Directory | **1.00** | **1.00** | 1.13 | **19.8%** | **1.00** |

What this shows:

- **hash mod N moves three quarters of the data** to add one server. Changing N changes almost every school's shard. It's fine only if N never changes.
- **Consistent hashing moves about 1/5 of the data, close to the minimum, but stays lopsided.** With uneven school sizes, whichever shard happens to get two of the large schools is a quarter fuller than average. At 16 shards one shard is 2.5 times the average. Hashing spreads *schools* evenly, not *students*.
- **A directory is even and moves the least,** because it can look at sizes. Its costs are a lookup on every request (cached), and one more small database that must stay up.
- **The biggest school sets a limit.** It has 0.28 of an average shard's students at 4 shards, 0.56 at 8 and 1.13 at 16. From 16 shards on, the biggest school is more than one shard's share by itself, so no placement can balance it (that's the 1.13 at 16 shards). A school that size must be split, for example by `(school_id, student)`. This is the "hot tenant" problem.

### Decision

- Shard by `school_id`, with a **directory**: even shards, the fewest moves, and a school can be moved deliberately (say, a big school onto its own shard before exam week).
- Very large schools get a shard of their own, and if one outgrows that, it is split by student.
- Start with one shard (today's database) and the directory in place, so going to two shards is a data move, not a code change.

## Doing it with Citus

Citus is an extension that turns Postgres into a sharded cluster. Its latest release is v14.3.0 (October 2026), licensed AGPL-3.0, and its v14 releases support up to PostgreSQL 18 ([releases](https://github.com/citusdata/citus/releases)). From its docs ([docs.citusdata.com](https://docs.citusdata.com/)):

- `create_distributed_table('threads', 'school_id')` splits a table by a column; tables distributed by the same column with `colocate_with` keep each school's rows together on one node, so joins inside a school stay local.
- Reference tables are copied to every node: the place for shared bots and public material.
- Schema-based sharding (since Citus 12.0, `citus_schema_distribute`) puts a whole schema on one node: one schema per school would also work, without adding `school_id` to every table.
- `citus_add_node` and then `rebalance_table_shards()` add a node and spread shards onto it. `create_distributed_table_concurrently` distributes a table while reads and writes continue.

Citus places rows by hash ranges, not by a directory, so the simulation's "hash" rows are closer to how it splits a table; the rebalancer then evens out nodes. Whether a single big school can be moved or isolated without a pause wasn't confirmed for this write-up and would need testing. Running a Citus cluster is outside the budget, so this stays a design.

## Honest limits

- School sizes are synthetic. The real shape comes from real schools.
- The simulation counts students, not bytes or queries per second; a school with heavy usage weighs more than its head count.
- Moves are counted, not timed. How long a school takes to move, and how short its write pause can be, would need a real cluster.
