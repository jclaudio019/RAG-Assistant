"""Stage 6: assemble grounded context for Gemini from retrieved chunks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from rag_assistant.store import ScoredChunk
from rag_assistant.citations import enrich_citations, experience_category, explore_url


@dataclass(frozen=True)
class AssembledContext:
    evidence_block: str
    citations: List[Dict[str, Any]]
    used_chunks: List[ScoredChunk]
    approx_chars: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence_block": self.evidence_block,
            "citations": self.citations,
            "used_chunk_ids": [c.chunk.chunk_id for c in self.used_chunks],
            "approx_chars": self.approx_chars,
        }


def assemble_context(
    hits: List[ScoredChunk],
    *,
    max_chars: int = 9000,
) -> AssembledContext:
    """Format retrieved evidence with provenance labels for the generator."""
    blocks: List[str] = []
    citations: List[Dict[str, Any]] = []
    used: List[ScoredChunk] = []
    total = 0
    seen_urls = set()

    for i, hit in enumerate(hits, start=1):
        c = hit.chunk
        label = c.project_name or c.document_title or c.document_id
        category = experience_category(c.source_type, c.heading_path, c.document_id)
        visit = explore_url(
            document_id=c.document_id,
            source_type=c.source_type,
            source_url=c.source_url,
            heading_path=c.heading_path,
            repo_url=(c.metadata or {}).get("repo_url"),
        )
        header = (
            f"[Source {i}] {label}\n"
            f"experience_category={category} | type={c.source_type} | section={c.heading_path}\n"
            f"url={c.source_url}\n"
            f"explore={visit}"
        )
        body = c.content.strip()
        piece = f"{header}\n{body}\n"
        if total + len(piece) > max_chars and used:
            break
        blocks.append(piece)
        used.append(hit)
        total += len(piece)

        cite_key = (c.source_url, label)
        if cite_key not in seen_urls:
            seen_urls.add(cite_key)
            citations.append(
                {
                    "label": label,
                    "source_type": c.source_type,
                    "source_url": c.source_url,
                    "section": c.heading_path,
                    "document_id": c.document_id,
                    "chunk_id": c.chunk_id,
                    "score": round(float(hit.score), 4),
                    "repo_url": (c.metadata or {}).get("repo_url"),
                    "experience_category": category,
                    "explore_url": visit,
                }
            )

    evidence = "\n---\n".join(blocks) if blocks else "(no evidence retrieved)"
    return AssembledContext(
        evidence_block=evidence,
        citations=enrich_citations(citations),
        used_chunks=used,
        approx_chars=len(evidence),
    )
