# Lampus: product plan

Lampus is a bilingual (English and Urdu / Roman Urdu) AI tutoring platform for schools and private tutors. It's the product I build to practice every topic in the course, piloted with my own tutoring students, and the goal is to take it to production.

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

## Where the code lives

Lampus is built on my bot-builder engine, [agentic-rag-langgraph](https://github.com/MishallAshraf/agentic-rag-langgraph) (agents, RAG, guardrails, sign-in, quotas, evals, API, frontend). The engine stays a general bot builder; Lampus is its first real product. Both live in that repo in two folders (planned):

- `engine/`: the bot builder
- `lampus/`: tutoring features the builder can't make (hint-not-answer checks, grading, mastery, dashboards, reports, Urdu) and the tutor bots

This repo (`ai-system-design-lab`) stays the course record: progress, notes, and labs for topics that don't belong in a product (for example GRPO or FSDP). Every topic links to the product PR where it was applied, with a number measured before and after the change.

## Build phases (product order)

Lampus is built in the order a real product needs things, not in course order. Each remaining topic is learned just before the phase that uses it. Topics in **bold** are not learned yet.

| Phase | What gets built | Topics |
| --- | --- | --- |
| 1. Solid foundations | Engine runs on Linux and in Codespaces; Postgres + pgvector instead of Chroma/SQLite; Redis cache; queue worker; Docker Compose; CI; a load test | 1–9, 20, 22 |
| 2. Tutor MVP | A tutor bot over one OpenStax textbook with page citations, Urdu-aware token budgets, thinking only for hard math, hints instead of answers | 10, 11, 13, 14, 15, 18, **39, 40, 41, 61** |
| 3. Safe to pilot | Golden set I mark myself, LLM grader calibrated against my marks, tracing, eval gate in CI, parental consent, data deletion, no personal data in logs | **47, 48, 49, 52, 60** |
| Pilot | 3–5 of my tutoring students | |
| 4. Grading and personalization | Photographed homework grading, mastery tracking, next-exercise recommender, A/B tests of hint styles, drift monitoring | 16, 17, 19, 21, 23, **50, 53, 67** |
| 5. Own models | Fine-tune and distill a small tutor, self-host it with one adapter per subject, route between it and API models | 12, 24–33, **34, 35, 36, 37, 38, 70** |
| 6. Agents and teacher tools | Lesson planner, MCP tools and Google Classroom, learning memory, research assistant, parent/teacher help desk, school-wide search, programming track | **42, 43, 44, 45, 46, 51, 66, 68, 69, 72** |
| 7. Scale and hardening | Latency budgets, fallbacks, caching, cost per student, quotas per school, graceful degradation, injection defense, agent permissions, red teaming, audit trail, cheating detection | **54–59, 62–65, 71** |

Topics 1–33 were learned in course order before this plan; they are backfilled inside the phase that uses them. Parts that can't run in the product (2-GPU FSDP, disaggregation, serving benchmarks on a rented GPU) become labs or design write-ups in this repo, labeled honestly.

## Learning order for the remaining topics

39 → 40 → 41 → 61 → 47 → 48 → 49 → 52 → 60 → 50 → 53 → 67 → 34 → 35 → 36 → 37 → 38 → 70 → 43 → 44 → 42 → 45 → 46 → 51 → 66 → 68 → 69 → 72 → 54 → 55 → 56 → 57 → 58 → 59 → 62 → 63 → 64 → 65 → 71

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
