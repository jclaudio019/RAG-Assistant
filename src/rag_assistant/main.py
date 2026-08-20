"""Entry point for RAG-Assistant."""

import json
import sys
from pathlib import Path

from rag_assistant.chunking import (
    ChunkingConfig,
    chunk_all_documents,
    generate_chunk_report,
)
from rag_assistant.ingestion import ingest_all_sources
from rag_assistant.ingestion.ingest import (
    INDEX_PATH,
    PROCESSED_ROOT,
    preview_ingest_plan,
)


def main() -> None:
    """Run ingestion, chunking, or print a preview of the plan."""
    if len(sys.argv) > 1 and sys.argv[1] == "ingest":
        result = ingest_all_sources()
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    if len(sys.argv) > 1 and sys.argv[1] == "chunk":
        output_dir = PROCESSED_ROOT.parent / "chunks"
        config = ChunkingConfig()
        chunks, summary = chunk_all_documents(
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

    if len(sys.argv) > 1 and sys.argv[1] in {"plan", "status"}:
        print(json.dumps(preview_ingest_plan(), indent=2, sort_keys=True))
        return

    print("Usage: python -m rag_assistant.main [ingest|chunk|plan]")


if __name__ == "__main__":
    main()
