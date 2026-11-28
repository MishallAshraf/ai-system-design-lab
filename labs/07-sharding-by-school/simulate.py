"""Sharding Lampus by school: a simulation (course topic 7).

    python labs/07-sharding-by-school/simulate.py

Lampus's data belongs to schools: students, conversations, usage, documents.
One Postgres holds it all today. When it can't, the data is split over several
servers (shards), with every row of one school on the same shard, so a
school's queries never need two servers.

The question is how to decide which school goes where. Three ways:

  hash mod N     shard = hash(school_id) % N
  consistent     each shard owns arcs of a hash ring (100 points per shard);
                 a school goes to the next point after hash(school_id)
  directory      a lookup table (school -> shard), filled by placing each new
                 school on the emptiest shard; to add a shard, move just enough
                 schools onto it

Two numbers for each, on synthetic school sizes (few large schools, many small):

  - how uneven the shards are: the fullest shard's rows over the average
  - how much data moves when a 5th shard is added to 4

Standard library only; finishes in a second. Writes results.json next to it.
"""

import bisect
import hashlib
import json
import random
from pathlib import Path

SCHOOLS = 1000
SEED = 7


def school_sizes() -> dict[str, int]:
    """Synthetic: students per school, heavy-tailed (rank r has about 4000 / r^0.9, at least 30)."""
    rng = random.Random(SEED)
    sizes = {}
    for rank in range(1, SCHOOLS + 1):
        base = max(30, int(4000 / rank ** 0.9))
        sizes[f"school_{rng.getrandbits(48):012x}"] = int(base * rng.uniform(0.8, 1.2))
    return sizes


def h(text: str) -> int:
    return int.from_bytes(hashlib.sha256(text.encode()).digest()[:8], "big")


def hash_mod(sizes, n):
    return {s: h(s) % n for s in sizes}


def consistent(sizes, n, points=100):
    ring = sorted((h(f"shard{k}#{p}"), k) for k in range(n) for p in range(points))
    keys = [r[0] for r in ring]
    return {s: ring[bisect.bisect(keys, h(s)) % len(ring)][1] for s in sizes}


def directory(sizes, n):
    """Largest school first, each onto the emptiest shard."""
    load, where = [0] * n, {}
    for s in sorted(sizes, key=sizes.get, reverse=True):
        k = load.index(min(load))
        where[s] = k
        load[k] += sizes[s]
    return where


def directory_add_shard(sizes, where, n):
    """Add shard n: move schools from the fullest shards until the new one holds its share."""
    where = dict(where)
    target = sum(sizes.values()) / (n + 1)
    load = [0] * (n + 1)
    for s, k in where.items():
        load[k] += sizes[s]
    # Smallest schools first: many small moves fill the new shard closest to its share.
    for s in sorted(where, key=sizes.get):
        k = where[s]
        if load[n] + sizes[s] > target:
            continue
        if load[k] - sizes[s] >= target:  # never empty a shard below its own share
            where[s] = n
            load[k] -= sizes[s]
            load[n] += sizes[s]
    return where


def imbalance(sizes, where, n) -> float:
    load = [0] * n
    for s, k in where.items():
        load[k] += sizes[s]
    return max(load) / (sum(load) / n)


def moved(sizes, before, after) -> float:
    return sum(sizes[s] for s in sizes if before[s] != after[s]) / sum(sizes.values())


def main():
    sizes = school_sizes()
    total, biggest = sum(sizes.values()), max(sizes.values())
    results = {"schools": SCHOOLS, "students": total, "biggest_school": biggest,
               "biggest_school_share": round(biggest / total, 3), "strategies": {}}
    for name, place in (("hash mod N", hash_mod), ("consistent hashing", consistent), ("directory", directory)):
        row = {f"imbalance_{n}_shards": round(imbalance(sizes, place(sizes, n), n), 2) for n in (4, 8, 16)}
        four = place(sizes, 4)
        five = directory_add_shard(sizes, four, 4) if name == "directory" else place(sizes, 5)
        row["moved_4_to_5"] = round(moved(sizes, four, five), 3)
        row["imbalance_after_adding_5th"] = round(imbalance(sizes, five, 5), 2)
        results["strategies"][name] = row
    # When does one school no longer fit on one shard? Its students over a shard's average.
    results["biggest_school_vs_average_shard"] = {n: round(biggest / (total / n), 2) for n in (4, 8, 16, 32, 64)}
    print(json.dumps(results, indent=2))
    (Path(__file__).parent / "results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
