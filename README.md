# AI System Design Lab

My hands-on record of a 72-topic course on designing production AI systems, built around **Lampus**, a bilingual (English and Urdu) AI tutoring platform for schools and tutors.

Every topic here has three things: working code, a measured result, and a one-page note in my own words.

## Progress

**33 of 72 topics learned.** See [PROGRESS.md](PROGRESS.md) for the full checklist with labs and notes.

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

## Repo layout

- `labs/` code for each lab
- `notes/` one-page notes per topic
- `data/SOURCES.md` every dataset used, with its license
- `docs/` product plan and design write-ups
