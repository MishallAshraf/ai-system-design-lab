# AI System Design Lab

My hands-on record of a 72-topic course on designing production AI systems, built around **Lampus**, a bilingual (English and Urdu) AI tutoring platform for schools and tutors.

Every topic here has three things: working code, a measured result, and a one-page note in my own words.

## Progress

**37 of 72 topics learned.** See [PROGRESS.md](PROGRESS.md) for the full checklist with labs and notes.

| Branch | Topics | Learned |
| --- | --- | --- |
| Foundations | 9 | 9 |
| ML and LLM fundamentals | 7 | 7 |
| Data layer | 7 | 7 |
| Training and adaptation | 7 | 7 |
| Inference and serving | 8 | 3 |
| LLM application patterns | 8 | 0 |
| Evaluation and observability | 7 | 0 |
| Reliability, cost and scale | 6 | 0 |
| Safety, privacy and governance | 6 | 0 |
| Case studies | 7 | 0 |

## Why "Lampus"

In ancient Athens, runners carried a flame from hand to hand in a torch relay, each keeping it alight for the next. They called the torch a *lampas*, and Greek writers used the relay as an image for passing knowledge from one generation to the next. In Homer's *Odyssey*, Lampus is also one of the two horses that pull the chariot of Dawn, bringing the first light of each day.

Lampus is built by Mishal, a tutor whose name means "torch," to keep that relay going: an AI tutor that doesn't do the work for students, but lights the next step so they can find the answer themselves.

*Pass the light.*

## The product

Lampus gives students a tutor grounded in their own textbooks, gives teachers auto-grading and lesson tools, and gives schools private, safe workspaces. See [docs/lampus-product.md](docs/lampus-product.md) for how each course topic maps to a feature.

## Results

Measured numbers from each lab will appear here as they're built.

| Topic | What I measured | Result |
| --- | --- | --- |
| 4 SQL vs NoSQL, 6 Consistency | Sign-in failures with 10 students at once, after moving users, quotas and the audit log from one shared SQLite connection to Postgres with a connection pool and atomic quota/audit writes ([Lampus Phase 1, Step 3](https://github.com/MishallAshraf/agentic-rag-langgraph/blob/phase-1/docs/adr/0025-postgres-for-users-quotas-and-audit.md)) | 90% → 0%; 50 students: 150 of 150 turns completed |
| 4 SQL vs NoSQL | Saving conversation state with 50 conversations at once, after moving LangGraph checkpoints from SQLite (one locked connection) to Postgres with a pool ([Lampus Phase 1, Step 4](https://github.com/MishallAshraf/agentic-rag-langgraph/blob/phase-1/docs/adr/0026-conversations-in-postgres.md)) | One turn's saving 550 ms → 367 ms (p50); 467 → 692 operations/s |
| 20 Vector databases and ANN indexes | Vector search on the real bots after moving chunks from Chroma to Postgres with pgvector; then HNSW vs exact search on 50,000 synthetic chunks over 50 bots ([Lampus Phase 1, Step 5](https://github.com/MishallAshraf/agentic-rag-langgraph/blob/phase-1/docs/adr/0027-pgvector-as-vector-store.md)) | 2.81 ms → 2.15 ms (p50), same top 10; HNSW filtered to one bot returned 0.7 of 10 results, so search stays exact per bot |
| 22 Data versioning and lineage | Chunks embedded when re-indexing a bot (28 ADRs, 224 chunks) after one file is edited, once each chunk records its file hash, ingest run, settings and code version ([Lampus Phase 1, Step 6](https://github.com/MishallAshraf/agentic-rag-langgraph/blob/phase-1/docs/adr/0028-data-lineage-and-incremental-ingestion.md)) | 225 → 1 (130 s → 0.4 s); nothing changed: 224 → 0 |
| 8 Rate limiting, 3 Caching | One student's 30-message burst over two API copies with a limit of 10 a minute, after moving the limiter (token buckets per student and per bot), conversation locks and the search cache from each copy's memory into Redis ([Lampus Phase 1, Step 7](https://github.com/MishallAshraf/agentic-rag-langgraph/blob/phase-1/docs/adr/0029-redis-for-shared-limits-locks-and-cache.md)) | 20 → 10 messages started; two turns at once in one conversation: 2 → 1 |
| 5 Message queues and pub/sub | Whether a bot build survives a crash with two API copies, after moving builds from the API's memory to Postgres plus a Redis Streams queue run by a separate worker, with pub/sub to wake progress pages and announce new bots ([Lampus Phase 1, Step 8](https://github.com/MishallAshraf/agentic-rag-langgraph/blob/phase-1/docs/adr/0030-build-queue-and-worker.md)) | API copy killed mid-build: build lost → finished 11 s later; the worker killed: a second worker took it over and finished it 17 s later |
| 1 Scaling, 2 Load balancing, 7 Replication | Students answered again after one API copy is killed under load, after putting three copies behind nginx (least connections), adding a Postgres read replica for searches and making conversation locks 15 s with renewal; measuring first found and fixed a hang that stopped one copy for good ([Lampus Phase 1, Step 9](https://github.com/MishallAshraf/agentic-rag-langgraph/blob/phase-1/docs/adr/0031-scale-out-nginx-and-read-replica.md)) | 0 of 20 → 20 of 20 within 20 s; median turn 15.4 s → 7.4 s, throughput unchanged on 2 cores (CPU-bound); searches on the primary 100% → 9% |
| 9 API design | Duplicate turns when 10 students each resend a message whose reply they lost, and forged or replayed webhooks a school's server accepts, after versioning the API under /v1, adding idempotency keys and signing webhooks (Standard Webhooks, HMAC-SHA256) ([Lampus Phase 1, Step 10](https://github.com/MishallAshraf/agentic-rag-langgraph/blob/phase-1/docs/adr/0032-api-v1-idempotency-and-signed-webhooks.md)) | 10 → 0 duplicate turns (20 → 10 charged); 200 → 0 of 200 attack messages accepted, 50 of 50 genuine delivered through a 3 s outage |
| 18 Document ingestion, 41 Chunking and reranking | Student questions (30, chapters 4–6 of OpenStax Prealgebra 2e) whose answering printed page is in the top 5, after taking text and math from the book's web pages (the PDF draws all math as vector shapes), printed page numbers from the PDF footers, and cutting chunks by the book's structure with the answer key never searched ([Lampus Phase 2, Step 11](https://github.com/MishallAshraf/agentic-rag-langgraph/blob/phase-2/docs/adr/0033-textbook-ingestion-printed-pages-and-structure.md)) | 0 → 24 of 30 (default rerank), 27 with vector search; 21 with only the page number fixed; answer key in results 5 → 0 of 5 |
| 7 Sharding | Placing 1,000 synthetic schools (52,658 students) on shards by `school_id`: how uneven the shards are, and how much data moves when a 5th shard joins 4 ([labs/07-sharding-by-school](labs/07-sharding-by-school), design write-up and simulation) | Data moved: hash mod N 75.5%, consistent hashing 25.1%, directory 19.8%; fullest shard at 8 shards 1.62×, 1.43×, 1.00× the average; from 16 shards the biggest school needs splitting |
| 9 API design | REST/JSON vs gRPC/protobuf for an internal search call returning 5 passages and a 384-float vector, on one laptop ([labs/09-grpc-internal](labs/09-grpc-internal), benchmark and design decision) | 12,382 → 5,679 bytes; p50 3.9 ms → 1.0 ms; 2.9 ms is 0.04% of a 7.4 s turn, so public API stays REST, gRPC waits for a hop that matters |

## Repo layout

- `labs/` labs that don't fit in the product: [07-sharding-by-school](labs/07-sharding-by-school) (design and simulation), [09-grpc-internal](labs/09-grpc-internal) (benchmark)
- `notes/` one-page notes per topic
- `data/SOURCES.md` every dataset used, with its license
- `docs/` product plan and design write-ups
