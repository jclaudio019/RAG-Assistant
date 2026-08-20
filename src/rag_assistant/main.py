"""Entry point for RAG-Assistant."""

import json
import sys

from rag_assistant.ingestion import ingest_all_sources
from rag_assistant.ingestion.ingest import preview_ingest_plan


def main() -> None:
    """Run ingestion or print a preview of the ingestion plan."""
    if len(sys.argv) > 1 and sys.argv[1] == "ingest":
        result = ingest_all_sources()
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    if len(sys.argv) > 1 and sys.argv[1] in {"plan", "status"}:
        print(json.dumps(preview_ingest_plan(), indent=2, sort_keys=True))
        return

    print("Usage: python -m rag_assistant.main [ingest|plan]")


if __name__ == "__main__":
    main()
