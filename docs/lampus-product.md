# Lampus: product plan

Lampus is a bilingual (English and Urdu / Roman Urdu) AI tutoring platform for schools and private tutors. It's the product I build to practice every topic in the course, piloted with my own tutoring students.

## The name

*Lampas* is the ancient Greek word for torch: in Athenian torch relays, runners passed the flame hand to hand, an old image for passing knowledge between generations. In Homer's *Odyssey*, Lampus is one of the two horses that pull the chariot of Dawn. The product's founder, Mishal, has a name that means "torch." Lampus lights the next step for a student instead of doing the work for them. Tagline: *Pass the light.*

## What it does

- **Students:** a tutor that explains step by step from their own textbook (with page citations), gives hints instead of answers, checks photographed homework, picks the next best exercise, and supports voice for young children.
- **Teachers and tutors:** auto-graded assignments with rubric scores, class dashboards, a lesson-plan and question-paper generator, search across the school's materials.
- **Parents:** weekly progress reports.
- **Schools:** separate private workspaces with their own curriculum, limits and billing.

## Topic-to-feature map

| Branch | Where it shows up in Lampus |
| --- | --- |
| Foundations | Autoscaling for exam-season spikes; load balancing; caching common explanations; SQL for users, grades, billing and NoSQL for transcripts and events; a queue for homework grading and pub/sub for "attempt submitted" events; strong consistency for grades and payments, eventual for leaderboards; sharding by school; rate limits per student and school; REST public API, gRPC internally, streamed tutor replies, webhooks to school systems |
| ML and LLM fundamentals | Prefill vs decode planning for textbook context; embeddings for concepts and questions; KV memory sizing; token budgets per session (Urdu costs more tokens); thinking budgets only for hard math; API models for hard problems, a self-hosted small model for children's data; handwritten-homework photos and voice |
| Data layer | Nightly report cards (batch) vs live mastery updates (streaming); ingesting textbooks, past papers and handwriting with OCR; teacher-labeled grading data; vector search filtered by school and grade; a feature store of mastery signals; versioned curricula and records of which model graded what; synthetic practice questions and simulated students |
| Training | Experiment tracking and registry; GPU sizing; LoRA for Socratic tutoring style and Roman Urdu; DPO from teacher preferences (hints over answers); GRPO on math with checkable answers; distilling a big tutor into a small one; distributed training on Kaggle's 2 GPUs plus a design write-up |
| Inference and serving | vLLM or SGLang with one LoRA adapter per subject; live tutoring (streamed) vs overnight grading (batch); continuous batching; prefix caching so a class shares the lesson context; quantization; disaggregation (write-up); speculative decoding; routing and autoscaling |
| LLM application patterns | Context engineering of student profile, lesson and history; structured JSON grading; RAG with textbook citations; GraphRAG over a concept prerequisite graph; tools via MCP (calculator, code runner, Google Classroom); a homework-help agent with safety rails; long-term learning memory; a multi-agent lesson planner |
| Evaluation and observability | Teacher-graded golden datasets; an LLM grader calibrated against teachers; tracing; A/B tests of hint styles; checking whether the tutor gave away the answer; eval gates in CI; drift and hallucination monitoring |
| Reliability, cost and scale | Under-1-second first token; retries and multi-provider fallback; semantic and prompt caching; cost per student per month; quotas per school; graceful degradation on exam day |
| Safety, privacy and governance | Protecting minors' data and class-level access control; age-appropriate guardrails, no answers during tests, distress escalation to a counselor; defending against prompt injection in chat and uploads; agents need teacher approval to contact parents; red teaming; audit logs of grading decisions (education is high-risk under the EU AI Act) |
| Case studies | Parent/teacher help desk; next-best-exercise recommender; school-wide search; programming track with a code-running tutor; the internal model platform; payment fraud, account sharing and cheating detection; project research assistant with citations |

## Build phases

1. **MVP** (Foundations, LLM fundamentals): one school, API-based tutor with RAG over one textbook, login, streaming, rate limits. Pilot with 3–5 of my students.
2. **Grading and data** (Data layer, first evals): ingestion with OCR, rubric grading, a golden set from my own marking.
3. **Personalization:** mastery features, recommender, concept graph.
4. **Own models** (Training, Inference): fine-tune and distill a small tutor, self-host with multi-adapter serving, route between it and API models.
5. **Agents and teacher tools:** lesson planner, research assistant, Classroom integration.
6. **Production hardening:** safety and red teaming, quotas, cost tracking, monitoring, fallbacks, audit trail.

## Backfill milestones for topics 1–33

| Milestone | Build | Topics |
| --- | --- | --- |
| M1 Platform core | FastAPI chat API with streaming, Postgres, Redis cache, token-bucket rate limiter, queue worker, Docker Compose, a load test | 1–9 |
| M2 LLM layer | Token cost calculator, context budget manager, embeddings search, small/large router, thinking-budget switch | 10–16 |
| M3 Knowledge pipeline | PDF and table ingestion with OCR, chunk and embed into pgvector, HNSW vs exact recall benchmark, data quality checks, dataset versioning, simulated students | 17–23 |
| M4 Model lab | MLflow tracking, GPU memory calculator, QLoRA fine-tune, small DPO run, toy GRPO on math, distillation, 2-GPU FSDP on Kaggle | 24–30 |
| M5 Serving | Engine benchmark on a rented GPU, TTFT and throughput measurements, continuous batching experiment | 31–33 |

## Data plan

| Need | Sources |
| --- | --- |
| Textbook content | OpenStax free textbooks; Pakistani textbook board PDFs only after checking terms |
| Math with checkable answers | GSM8K, MATH, MathQA |
| Science | SciQ, ARC, ScienceQA |
| Programming track | MBPP, HumanEval |
| Student practice histories | ASSISTments, EdNet, Junyi Academy |
| Handwriting | IAM, CROHME; my own and consented, anonymized student work |
| Volume and gaps | Synthetic: simulated students, tutoring conversations, Urdu/Roman Urdu versions, DPO pairs (always labeled synthetic) |
| Trusted evaluation | A golden set of 100–300 items I mark myself |

Some datasets are research or non-commercial only: fine for a portfolio, swap before any commercial launch. Record each in `data/SOURCES.md`.

## Where things run

| Work | Where | Cost |
| --- | --- | --- |
| App development | GitHub Codespaces | Free monthly hours |
| Embeddings, vector search | CPU, pgvector | Free |
| Tutor LLM calls | Cheap API models / free tiers | A few dollars a month |
| Fine-tuning, DPO, GRPO, distillation | Colab, Kaggle (small models, QLoRA) | Free |
| Distributed training | Kaggle 2-GPU notebooks | Free |
| Serving benchmarks | Hourly GPU rental, one afternoon per lab | A few dollars per lab |
| Pilot hosting | Small cloud server | About $5–10 a month |
| Too big to run | Design write-up plus small simulation | Free |
