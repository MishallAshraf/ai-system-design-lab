# Course progress

34 of 72 topics learned. Topics 1–33 were learned in course order; the remaining topics are learned in **product order**, each just before the Lampus build phase that uses it (see "Build phases" and "Learning order" in `docs/lampus-product.md`). Labs for topics 1–33 are backfilled inside those phases.

Columns: **Learned** = date I studied it · **Lab** = built in this repo · **Note** = one-page note written.

## 1. Foundations (9/9)

| # | Topic | Learned | Lab | Note |
| --- | --- | --- | --- | --- |
| 1 | Scalability: vertical vs horizontal | 2026-10 | [x] | [ ] |
| 2 | Load balancing | 2026-10 | [x] | [ ] |
| 3 | Caching strategies | 2026-10 | [x] | [ ] |
| 4 | SQL vs NoSQL | 2026-10 | [x] | [ ] |
| 5 | Message queues and pub/sub | 2026-10 | [x] | [ ] |
| 6 | CAP theorem and consistency | 2026-10-07 | [x] | [ ] |
| 7 | Sharding and replication | 2026-10-09 | [ ] | [ ] |
| 8 | Rate limiting | 2026-10-09 | [x] | [ ] |
| 9 | API design: REST, gRPC, streaming | 2026-10-10 | [x] | [ ] |

## 2. ML and LLM fundamentals (7/7)

| # | Topic | Learned | Lab | Note |
| --- | --- | --- | --- | --- |
| 10 | Training vs inference, prefill vs decode | 2026-10-12 | [ ] | [ ] |
| 11 | Embeddings | 2026-10-13 | [ ] | [ ] |
| 12 | Transformer and attention basics | 2026-10-14 | [ ] | [ ] |
| 13 | Tokens, context windows, long context | 2026-10-16 | [ ] | [ ] |
| 14 | Reasoning models and test-time compute | 2026-10-20 | [ ] | [ ] |
| 15 | Model selection: API vs open-weight, small vs large | 2026-10-23 | [ ] | [ ] |
| 16 | Mixture of experts and multimodal models | 2026-10-24 | [ ] | [ ] |

## 3. Data layer (7/7)

| # | Topic | Learned | Lab | Note |
| --- | --- | --- | --- | --- |
| 17 | Batch vs streaming pipelines | 2026-10-25 | [ ] | [ ] |
| 18 | Document ingestion: parsing PDFs, tables, OCR | 2026-10-28 | [ ] | [ ] |
| 19 | Data quality, labeling, curation | 2026-10-29 | [ ] | [ ] |
| 20 | Vector databases and ANN indexes (HNSW, IVF) | 2026-10-30 | [x] | [ ] |
| 21 | Feature stores | 2026-10-31 | [ ] | [ ] |
| 22 | Data versioning and lineage | 2026-11-02 | [x] | [ ] |
| 23 | Synthetic data generation | 2026-11-04 | [ ] | [ ] |

## 4. Training and adaptation (7/7)

| # | Topic | Learned | Lab | Note |
| --- | --- | --- | --- | --- |
| 24 | Experiment tracking and model registry | 2026-11-05 | [ ] | [ ] |
| 25 | GPU memory math and accelerators | 2026-11-06 | [ ] | [ ] |
| 26 | Fine-tuning: SFT, LoRA, QLoRA | 2026-11-08 | [ ] | [ ] |
| 27 | Preference tuning: DPO family | 2026-11-08 | [ ] | [ ] |
| 28 | RL with verifiable rewards (GRPO) | 2026-11-09 | [ ] | [ ] |
| 29 | Distillation into smaller models | 2026-11-10 | [ ] | [ ] |
| 30 | Distributed training: FSDP, tensor, pipeline parallelism | 2026-11-11 | [ ] | [ ] |

## 5. Inference and serving (3/8)

| # | Topic | Learned | Lab | Note |
| --- | --- | --- | --- | --- |
| 31 | Serving engines: vLLM, SGLang, TensorRT-LLM | 2026-11-18 | [ ] | [ ] |
| 32 | Online, batch and streaming inference, TTFT | 2026-11-21 | [ ] | [ ] |
| 33 | Continuous batching | 2026-11-23 | [ ] | [ ] |
| 34 | KV cache, PagedAttention, prefix caching | | [ ] | [ ] |
| 35 | Quantization: FP8, INT4, AWQ | | [ ] | [ ] |
| 36 | Prefill/decode disaggregation | | [ ] | [ ] |
| 37 | Speculative decoding | | [ ] | [ ] |
| 38 | Model routing, cascades, GPU autoscaling | | [ ] | [ ] |

## 6. LLM application patterns (1/8)

| # | Topic | Learned | Lab | Note |
| --- | --- | --- | --- | --- |
| 39 | Context engineering | 2026-11-25 | [ ] | [ ] |
| 40 | Structured outputs and JSON schemas | **next** | [ ] | [ ] |
| 41 | RAG: chunking, hybrid search, reranking | | [ ] | [ ] |
| 42 | Agentic RAG and GraphRAG | | [ ] | [ ] |
| 43 | Tool use and MCP | | [ ] | [ ] |
| 44 | Agent architectures and harnesses | | [ ] | [ ] |
| 45 | Memory and long-session compaction | | [ ] | [ ] |
| 46 | Multi-agent orchestration and A2A | | [ ] | [ ] |

## 7. Evaluation and observability (0/7)

| # | Topic | Learned | Lab | Note |
| --- | --- | --- | --- | --- |
| 47 | Golden datasets and offline evals | | [ ] | [ ] |
| 48 | LLM-as-judge, calibrated against humans | | [ ] | [ ] |
| 49 | Tracing with OpenTelemetry | | [ ] | [ ] |
| 50 | Online evals and A/B tests on live traces | | [ ] | [ ] |
| 51 | Agent trajectory evaluation | | [ ] | [ ] |
| 52 | Evals in CI and regression gates | | [ ] | [ ] |
| 53 | Drift, hallucination and feedback loops | | [ ] | [ ] |

## 8. Reliability, cost and scale (0/6)

| # | Topic | Learned | Lab | Note |
| --- | --- | --- | --- | --- |
| 54 | Latency budgets: TTFT, p50, p99 | | [ ] | [ ] |
| 55 | Timeouts, retries, multi-provider fallbacks | | [ ] | [ ] |
| 56 | Semantic and prompt caching | | [ ] | [ ] |
| 57 | Token and GPU cost modeling | | [ ] | [ ] |
| 58 | Per-tenant token quotas and rate limits | | [ ] | [ ] |
| 59 | Multi-region and graceful degradation | | [ ] | [ ] |

## 9. Safety, privacy and governance (0/6)

| # | Topic | Learned | Lab | Note |
| --- | --- | --- | --- | --- |
| 60 | Data privacy: PII redaction, retrieval access control | | [ ] | [ ] |
| 61 | Guardrails: deterministic and model-based | | [ ] | [ ] |
| 62 | Prompt injection and tool/MCP security | | [ ] | [ ] |
| 63 | Agent permissions, sandboxing, human approval | | [ ] | [ ] |
| 64 | Red teaming | | [ ] | [ ] |
| 65 | Regulation (EU AI Act) and audit logging | | [ ] | [ ] |

## 10. Case studies (0/7)

| # | Topic | Learned | Lab | Note |
| --- | --- | --- | --- | --- |
| 66 | Customer support agent with RAG | | [ ] | [ ] |
| 67 | Recommendation system | | [ ] | [ ] |
| 68 | Enterprise semantic search | | [ ] | [ ] |
| 69 | Coding agent | | [ ] | [ ] |
| 70 | LLM inference platform | | [ ] | [ ] |
| 71 | Fraud detection system | | [ ] | [ ] |
| 72 | Deep research multi-agent system | | [ ] | [ ] |
