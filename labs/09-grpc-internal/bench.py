"""REST/JSON vs gRPC/protobuf for one internal hop (course topic 9).

    python bench.py          # generates the gRPC code, starts both servers, runs the benchmark

The hop: Lampus's API asks a search service for the passages that answer a
question. The answer is 5 passages (about 120 words each) and the question's
embedding (384 floats). Both servers return the same synthetic answer:

  rest       FastAPI + uvicorn, JSON, HTTP/1.1 keep-alive (httpx client)
  rest_raw   the same server, but the JSON is encoded once at start and sent
             as bytes: what's left is HTTP and JSON parsing, not FastAPI's
             per-response encoding
  grpc   grpcio, protobuf (search.proto), one reused channel

Measured, from the client: the size of the answer's body, and the time of a
full call (send, server builds the answer, receive, parse), sequentially.
Writes results.json next to itself.
"""

import json
import random
import statistics
import subprocess
import sys
import time
from concurrent import futures
from pathlib import Path

HERE = Path(__file__).parent
GEN = HERE / "gen"
REST_PORT, GRPC_PORT = 8971, 8972
WARMUP, CALLS, ROUNDS = 200, 2000, 3
QUERY = {"bot_id": "biology-101", "query": "What does the mitochondria do in a cell?", "top_k": 5}


def answer() -> dict:
    """Synthetic: 5 passages of made-up words and a unit-length 384-float vector."""
    rng = random.Random(9)
    words = [w for w in "cell energy membrane protein the of a in and to is that mitochondria "
             "respiration glucose oxygen nucleus enzyme molecule produce release store".split()]
    passages = [{"chunk_id": f"chunk_{rng.getrandbits(40):010x}", "source": f"textbook/chapter-{i + 3}.pdf",
                 "text": " ".join(rng.choice(words) for _ in range(120)), "score": round(0.9 - i * 0.05, 4)}
                for i in range(5)]
    v = [rng.gauss(0, 1) for _ in range(384)]
    norm = sum(x * x for x in v) ** 0.5
    return {"passages": passages, "query_vector": [x / norm for x in v]}


def generate():
    from grpc_tools import protoc
    GEN.mkdir(exist_ok=True)
    rc = protoc.main(["protoc", f"-I{HERE}", f"--python_out={GEN}", f"--grpc_python_out={GEN}", str(HERE / "search.proto")])
    assert rc == 0, "protoc failed"


def stubs():
    sys.path.insert(0, str(GEN))
    import search_pb2
    import search_pb2_grpc
    return search_pb2, search_pb2_grpc


def serve_rest():
    import uvicorn
    from fastapi import FastAPI, Response

    app, body = FastAPI(), answer()
    raw = json.dumps(body, separators=(",", ":")).encode()

    @app.post("/search")
    def search(req: dict):
        return body

    @app.post("/search-raw")
    def search_raw(req: dict):
        return Response(raw, media_type="application/json")

    uvicorn.run(app, host="127.0.0.1", port=REST_PORT, log_level="warning")


def serve_grpc():
    import grpc
    pb, pb_grpc = stubs()
    a = answer()
    reply = pb.SearchResponse(passages=[pb.Passage(**p) for p in a["passages"]], query_vector=a["query_vector"])

    class Search(pb_grpc.SearchServicer):
        def Find(self, request, context):
            return reply

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    pb_grpc.add_SearchServicer_to_server(Search(), server)
    server.add_insecure_port(f"127.0.0.1:{GRPC_PORT}")
    server.start()
    server.wait_for_termination()


def timed(call, n):
    out = []
    for _ in range(n):
        t = time.perf_counter()
        call()
        out.append((time.perf_counter() - t) * 1000)
    return out


def pct(ms, p):
    return round(statistics.quantiles(ms, n=100)[p - 1], 3)


def run():
    import grpc
    import httpx

    generate()
    pb, pb_grpc = stubs()
    procs = [subprocess.Popen([sys.executable, __file__, mode]) for mode in ("rest", "grpc")]
    try:
        client = httpx.Client(base_url=f"http://127.0.0.1:{REST_PORT}")
        channel = grpc.insecure_channel(f"127.0.0.1:{GRPC_PORT}")
        stub = pb_grpc.SearchStub(channel)
        for _ in range(100):  # wait for both servers
            try:
                client.post("/search", json=QUERY)
                stub.Find(pb.SearchRequest(**QUERY), timeout=1)
                break
            except Exception:
                time.sleep(0.2)

        def rest_call():
            r = client.post("/search", json=QUERY)
            r.raise_for_status()
            return r.json()

        def rest_raw_call():
            r = client.post("/search-raw", json=QUERY)
            r.raise_for_status()
            return r.json()

        def grpc_call():
            return stub.Find(pb.SearchRequest(**QUERY))

        a = answer()
        rest_bytes = len(client.post("/search", json=QUERY).content)
        grpc_bytes = grpc_call().ByteSize()
        json_6dp = len(json.dumps({**a, "query_vector": [round(x, 6) for x in a["query_vector"]]},
                                  separators=(",", ":")).encode())
        text_bytes = sum(len(p["text"].encode()) for p in a["passages"])

        times = {"rest": [], "rest_raw": [], "grpc": []}
        for _ in range(ROUNDS):  # alternate, so neither gets a quieter moment of the machine
            for name, call in (("rest", rest_call), ("rest_raw", rest_raw_call), ("grpc", grpc_call)):
                timed(call, WARMUP)
                times[name] += timed(call, CALLS)

        results = {
            "calls_each": CALLS * ROUNDS,
            "body_bytes": {"rest_json": rest_bytes, "rest_json_vector_rounded_6dp": json_6dp,
                           "grpc_protobuf": grpc_bytes, "of_which_passage_text": text_bytes},
            "vector_bytes": {"json": len(json.dumps(a["query_vector"], separators=(",", ":"))),
                             "protobuf": 384 * 4},
            "latency_ms": {name: {"p50": pct(ms, 50), "p95": pct(ms, 95), "p99": pct(ms, 99),
                                  "calls_per_s": round(1000 / statistics.mean(ms))}
                           for name, ms in times.items()},
        }
        print(json.dumps(results, indent=2))
        (HERE / "results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    finally:
        for p in procs:
            p.terminate()


if __name__ == "__main__":
    {"rest": serve_rest, "grpc": serve_grpc}.get(sys.argv[1] if len(sys.argv) > 1 else "", run)()
