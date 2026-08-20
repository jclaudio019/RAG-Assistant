"""Quality and audit reporting for RAG-Assistant chunking."""

from __future__ import annotations

import json
import statistics
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List

from rag_assistant.chunking.chunker import Chunk
from rag_assistant.chunking.config import ChunkingConfig


@dataclass
class ChunkReport:
    """Comprehensive metrics and evaluation report for generated chunks."""

    documents_processed: int
    total_chunks: int
    total_source_tokens: int
    total_chunk_tokens: int
    duplication_ratio: float
    min_tokens: int
    max_tokens: int
    avg_tokens: float
    median_tokens: float
    p90_tokens: float
    source_word_coverage_pct: float
    token_distribution: Dict[str, int]
    document_summaries: List[Dict[str, Any]]
    validation_checks: Dict[str, bool]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_markdown(self) -> str:
        """Render a clean, human-readable Markdown summary report."""
        lines = [
            "# RAG-Assistant — Chunking Quality & Inspection Report",
            "",
            "## Summary Metrics",
            "",
            f"- **Documents Processed:** {self.documents_processed}",
            f"- **Total Chunks Produced:** {self.total_chunks}",
            f"- **Average Chunk Tokens:** {self.avg_tokens:.1f}",
            f"- **Median Chunk Tokens:** {self.median_tokens:.1f}",
            f"- **Token Range:** {self.min_tokens} – {self.max_tokens} tokens",
            f"- **90th Percentile (p90):** {self.p90_tokens:.1f} tokens",
            f"- **Source Word Coverage:** {self.source_word_coverage_pct:.2f}%",
            f"- **Duplication / Overlap Ratio:** {self.duplication_ratio:.3f}x",
            "",
            "## Token Distribution",
            "",
            "| Token Range | Chunk Count | Percentage |",
            "| :--- | :--- | :--- |",
        ]

        for bucket, count in self.token_distribution.items():
            pct = (count / self.total_chunks * 100) if self.total_chunks else 0.0
            lines.append(f"| {bucket} | {count} | {pct:.1f}% |")

        lines.extend([
            "",
            "## Validation & Integrity Checks",
            "",
            "| Check | Status |",
            "| :--- | :--- |",
        ])

        for check, passed in self.validation_checks.items():
            icon = "PASSED" if passed else "FAILED"
            lines.append(f"| `{check}` | {icon} |")

        lines.extend([
            "",
            "## Per-Document Breakdown",
            "",
            "| Document ID | Chunks | Avg Tokens | Min/Max | Source Type |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ])

        for d in self.document_summaries:
            lines.append(
                f"| `{d['document_id']}` | {d['chunks']} | {d['avg_tokens']:.1f} | "
                f"{d['min_tokens']} / {d['max_tokens']} | {d['source_type']} |"
            )

        lines.append("")
        return "\n".join(lines)


def generate_chunk_report(
    index_path: Path,
    chunks: List[Chunk],
    config: ChunkingConfig,
    output_dir: Path,
) -> ChunkReport:
    """Evaluate chunk metrics, verify source coverage, and generate JSON/Markdown reports."""
    token_fn = config.get_token_counter()
    token_counts = [c.token_count for c in chunks] or [0]

    # Load source documents from index.json
    with index_path.open("r", encoding="utf-8") as fp:
        index_data = json.load(fp)

    documents = index_data.get("documents", [])
    total_source_tokens = 0
    all_source_words: set[str] = set()

    doc_meta_map: Dict[str, dict] = {}
    for doc in documents:
        doc_id = doc["document_id"]
        doc_meta_map[doc_id] = doc
        norm_path = doc.get("normalized_path")
        if norm_path and Path(norm_path).exists():
            text = Path(norm_path).read_text(encoding="utf-8")
            total_source_tokens += token_fn(text)
            words = [w.lower().strip(".,;:!?()[]\"'") for w in text.split() if len(w) > 2]
            all_source_words.update(words)

    # Collect words from chunks
    all_chunk_words: set[str] = set()
    for c in chunks:
        words = [w.lower().strip(".,;:!?()[]\"'") for w in c.content.split() if len(w) > 2]
        all_chunk_words.update(words)

    # Word coverage calculation
    covered_words = all_source_words.intersection(all_chunk_words)
    coverage_pct = (
        (len(covered_words) / len(all_source_words) * 100) if all_source_words else 100.0
    )

    total_chunk_tokens = sum(token_counts)
    duplication_ratio = (
        (total_chunk_tokens / total_source_tokens) if total_source_tokens else 1.0
    )

    # Token Distribution Histogram
    buckets = {
        "< 100 tokens": 0,
        "100 – 300 tokens": 0,
        "300 – 500 tokens": 0,
        "500 – 700 tokens": 0,
        "700 – 850 tokens": 0,
        "> 850 tokens": 0,
    }
    for t in token_counts:
        if t < 100:
            buckets["< 100 tokens"] += 1
        elif t <= 300:
            buckets["100 – 300 tokens"] += 1
        elif t <= 500:
            buckets["300 – 500 tokens"] += 1
        elif t <= 700:
            buckets["500 – 700 tokens"] += 1
        elif t <= 850:
            buckets["700 – 850 tokens"] += 1
        else:
            buckets["> 850 tokens"] += 1

    # Per-document stats
    doc_chunk_map: Dict[str, List[Chunk]] = {}
    for c in chunks:
        doc_chunk_map.setdefault(c.document_id, []).append(c)

    doc_summaries = []
    for doc_id, doc_chunks in sorted(doc_chunk_map.items()):
        d_tokens = [c.token_count for c in doc_chunks]
        meta = doc_meta_map.get(doc_id, {})
        doc_summaries.append(
            {
                "document_id": doc_id,
                "title": meta.get("title", doc_chunks[0].document_title),
                "source_type": meta.get("source_type", doc_chunks[0].source_type),
                "chunks": len(doc_chunks),
                "total_tokens": sum(d_tokens),
                "avg_tokens": sum(d_tokens) / len(d_tokens) if d_tokens else 0,
                "min_tokens": min(d_tokens) if d_tokens else 0,
                "max_tokens": max(d_tokens) if d_tokens else 0,
            }
        )

    # Validation Checks
    validation_checks = {
        "all_chunks_under_max_token_ceiling": all(t <= config.max_tokens + 50 for t in token_counts),
        "no_empty_chunks": all(bool(c.content.strip()) for c in chunks),
        "source_coverage_healthy_ge_98pct": coverage_pct >= 98.0,
        "metadata_provenance_preserved": all(bool(c.document_id and c.heading_path) for c in chunks),
        "all_chunk_ids_unique": len(set(c.chunk_id for c in chunks)) == len(chunks),
    }

    # Percentiles
    sorted_tokens = sorted(token_counts)
    p90_idx = int(len(sorted_tokens) * 0.90)
    p90_val = sorted_tokens[min(p90_idx, len(sorted_tokens) - 1)]

    report = ChunkReport(
        documents_processed=len(doc_chunk_map),
        total_chunks=len(chunks),
        total_source_tokens=total_source_tokens,
        total_chunk_tokens=total_chunk_tokens,
        duplication_ratio=round(duplication_ratio, 3),
        min_tokens=min(token_counts),
        max_tokens=max(token_counts),
        avg_tokens=round(statistics.mean(token_counts), 1),
        median_tokens=round(statistics.median(token_counts), 1),
        p90_tokens=round(p90_val, 1),
        source_word_coverage_pct=round(coverage_pct, 2),
        token_distribution=buckets,
        document_summaries=doc_summaries,
        validation_checks=validation_checks,
    )

    # Write report files
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "chunk_report.json"
    md_path = output_dir / "chunk_report.md"

    with json_path.open("w", encoding="utf-8") as fp:
        json.dump(report.to_dict(), fp, indent=2, ensure_ascii=False)
        fp.write("\n")

    md_path.write_text(report.to_markdown(), encoding="utf-8")
    return report
