# Lab 09: gRPC for Lampus's internal hops?

Course topic 9 (API design: REST, gRPC, versioning). Lampus's public API work (`/v1`, idempotency keys, signed webhooks) went into the product in Step 10 ([ADR 0032](https://github.com/MishallAshraf/agentic-rag-langgraph/blob/phase-1/docs/adr/0032-api-v1-idempotency-and-signed-webhooks.md)). This lab covers the question left over: should the calls *between Lampus's own services* use gRPC instead of REST? **A design decision plus a small benchmark,** on synthetic data, on a laptop.

```bash
cd labs/09-grpc-internal
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt   # .venv/bin/python on Linux or a Codespace
.venv/Scripts/python bench.py
```

## REST and gRPC in one paragraph

REST, as Lampus uses it, is HTTP requests with JSON bodies: readable, easy to try with `curl`, and understood by every language and browser. gRPC is a remote-call framework: the service and its messages are described in a `.proto` file, code is generated from it for each language, and by default the messages travel as Protocol Buffers, a compact binary format ([gRPC docs](https://grpc.io/docs/what-is-grpc/introduction/)). It has four kinds of call: one request and one reply, a stream of replies, a stream of requests, or both streaming ([core concepts](https://grpc.io/docs/what-is-grpc/core-concepts/)). The trade: smaller, typed messages and a fixed contract, against a binary format you can't read by eye and an extra build step.

## The hop measured

Today Lampus's search runs inside the API process: there is no internal network hop yet. The first one comes when search, or the embedding model, moves into its own service. So the benchmark imitates that call: the API asks the search service for the passages answering a question, and gets back 5 passages (about 120 words each) plus the question's embedding, 384 floats.

The same synthetic answer is served three ways ([search.proto](search.proto), [bench.py](bench.py)):

- **REST:** FastAPI 0.165 and uvicorn, returning the answer as a Python dict, the usual FastAPI way. The client is httpx with a kept-alive connection.
- **REST, pre-encoded:** the same server, but the JSON is encoded once at start-up and sent as bytes. This separates the cost of HTTP and JSON from FastAPI's work on each response.
- **gRPC:** grpcio 1.85.4 with protobuf, one reused channel.

Each was called 6,000 times, one call at a time, alternating in rounds after a warm-up. The time is the whole call from the client: send, server answers, receive, parse.

Windows 10 laptop, 4 cores, everything on one machine (loopback), Python 3.11, 2026-11-26:

| | REST (FastAPI dict) | REST (pre-encoded) | gRPC (protobuf) |
| --- | --- | --- | --- |
| Answer body | 12,382 bytes | 12,382 bytes | **5,679 bytes** |
| p50 call | 3.9 ms | 2.6 ms | **1.0 ms** |
| p95 call | 5.3 ms | 4.3 ms | **1.4 ms** |
| p99 call | 6.5 ms | 4.9 ms | **1.6 ms** |
| Calls per second, one at a time | 246 | 348 | **971** |

Where the bytes go:

- The passage text is 3,875 bytes either way: text is text.
- The 384-float vector is 8,035 bytes as JSON (each float written out as about 20 characters) and 1,536 bytes as protobuf (4 bytes each). That's most of the difference.
- Rounding the vector to 6 decimals brings JSON to 7,957 bytes, still 40% more than protobuf. Protobuf's floats are 32-bit, so it also carries less precision than full JSON; 32-bit is what embeddings are stored as anyway.

## What this means for Lampus

- **gRPC is 2.4× smaller and about 4× faster per call here.** About a third of REST's extra time is FastAPI encoding the response (3.9 ms → 2.6 ms pre-encoded); the rest is HTTP/1.1 and JSON parsing.
- **But the hop is tiny next to a turn.** A turn took a median 7.4 s under load in Step 9, mostly the model. Saving 2.9 ms is 0.04% of that. Search is called once or twice per turn, so the protocol can't make students' answers noticeably faster.
- **Where it would matter:** a hop called many times per request, or with big payloads. For example, embedding hundreds of chunks during a build, or a vector-heavy service answering thousands of calls a second. There, 2.4× fewer bytes and a quarter of the time per call add up.

### Decision

- **Public API and the web app stay REST + JSON, with SSE for streaming replies.** Schools' systems and browsers speak HTTP and JSON. Errors are readable, and `curl` is enough to try it. The `/v1` versioning, idempotency keys and webhooks are all built on it.
- **Internal hops: REST until one is measured to matter, then gRPC.** The first candidate is the embedding or model server in the serving phases, where builds send many chunks per call and streaming replies fit gRPC's server-streaming calls.
- **Before switching, check the cheap fix:** returning pre-encoded or faster-encoded JSON already took a third off REST's time here.

## Honest limits

- One machine and loopback: no real network, so the byte difference costs almost nothing in time here. Across machines, smaller messages matter more.
- Calls one at a time; no test with many calls at once.
- A synthetic answer, built once and returned every time: the search itself isn't measured, only the protocol around it.
- Python on both sides. Other languages' JSON and gRPC libraries perform differently.
