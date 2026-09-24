"""Entry point for RAG-Assistant."""

from __future__ import annotations

import json
import sys

from rag_assistant.ask import ask
from rag_assistant.chunking import ChunkingConfig, chunk_all_documents, generate_chunk_report
from rag_assistant.embeddings import build_embeddings
from rag_assistant.eval_runner import run_evaluation
from rag_assistant.ingestion import ingest_all_sources
from rag_assistant.ingestion.ingest import INDEX_PATH, PROCESSED_ROOT, preview_ingest_plan
from rag_assistant.paths import EVAL_RESULTS, VECTOR_META, VECTOR_NPZ
from rag_assistant.retrieval import Retriever


USAGE = """Usage: python -m rag_assistant.main <command>

Commands:
  plan              Preview ingestion sources
  ingest            Ingest website + project docs + career KB
  chunk             Structure-aware chunking → chunks.jsonl
  embed             Embed chunks → local numpy vector index
  retrieve "q"      Retrieve top-k chunks for a question
  ask "q"           Retrieve + grounded answer
  eval              Run retrieval evaluation set
  export-worker     Export index JSON for Cloudflare Worker
  serve [port]      Start the thin FastAPI demo server
"""


def main() -> None:
    if len(sys.argv) < 2:
        print(USAGE)
        return

    cmd = sys.argv[1]

    if cmd == "ingest":
        print(json.dumps(ingest_all_sources(), indent=2, sort_keys=True))
        return

    if cmd == "chunk":
        output_dir = PROCESSED_ROOT.parent / "chunks"
        config = ChunkingConfig()
        chunks, _summary = chunk_all_documents(
            index_path=INDEX_PATH,
            output_dir=output_dir,
            config=config,
        )
        report = generate_chunk_report(
            index_path=INDEX_PATH,
            chunks=chunks,
            config=config,
            output_dir=output_dir,
        )
        print(
            json.dumps(
                {
                    "documents_processed": report.documents_processed,
                    "total_chunks": report.total_chunks,
                    "avg_tokens": report.avg_tokens,
                    "min_tokens": report.min_tokens,
                    "max_tokens": report.max_tokens,
                    "source_word_coverage_pct": report.source_word_coverage_pct,
                    "duplication_ratio": report.duplication_ratio,
                    "chunks_jsonl": str(output_dir / "chunks.jsonl"),
                    "report_md": str(output_dir / "chunk_report.md"),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    if cmd in {"plan", "status"}:
        print(json.dumps(preview_ingest_plan(), indent=2, sort_keys=True))
        return

    if cmd == "embed":
        result = build_embeddings()
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    if cmd == "retrieve":
        if len(sys.argv) < 3:
            print('Usage: python -m rag_assistant.main retrieve "your question"')
            sys.exit(2)
        query = " ".join(sys.argv[2:])
        result = Retriever().retrieve(query, top_k=5)
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        return

    if cmd == "ask":
        if len(sys.argv) < 3:
            print('Usage: python -m rag_assistant.main ask "your question"')
            sys.exit(2)
        query = " ".join(sys.argv[2:])
        result = ask(query)
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        return

    if cmd == "eval":
        report = run_evaluation()
        print(
            json.dumps(
                {
                    "question_count": report["question_count"],
                    "source_hit_rate": report["source_hit_rate"],
                    "fact_hit_rate": report["fact_hit_rate"],
                    "both_hit_rate": report["both_hit_rate"],
                    "failure_count": len(report["failures"]),
                    "results_path": str(EVAL_RESULTS),
                    "index_paths": {"npz": str(VECTOR_NPZ), "meta": str(VECTOR_META)},
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    if cmd == "export-worker":
        from rag_assistant.export_worker import export_worker_index

        print(json.dumps(export_worker_index(), indent=2, sort_keys=True))
        return

    if cmd == "serve":
        import uvicorn

        host = "0.0.0.0"
        port = 8080
        if len(sys.argv) > 2:
            port = int(sys.argv[2])
        uvicorn.run("rag_assistant.api:app", host=host, port=port, reload=False)
        return

    print(USAGE)
    sys.exit(2)


if __name__ == "__main__":
    main()
