"""Stage 4: query embedding → vector search → top-k scored chunks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

from rag_assistant.providers import embed_query
from rag_assistant.store import NumpyVectorStore, ScoredChunk


@dataclass(frozen=True)
class RetrievalResult:
    query: str
    top_k: int
    hits: List[ScoredChunk]
    embedding_model: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "top_k": self.top_k,
            "embedding_model": self.embedding_model,
            "hit_count": len(self.hits),
            "hits": [h.to_dict() for h in self.hits],
        }


class Retriever:
    def __init__(self, store: Optional[NumpyVectorStore] = None):
        self.store = store or NumpyVectorStore.load()

    def retrieve(
        self,
        query: str,
        *,
        top_k: int = 5,
        source_types: Optional[Sequence[str]] = None,
        fetch_k: Optional[int] = None,
    ) -> RetrievalResult:
        query = (query or "").strip()
        if not query:
            raise ValueError("query must be non-empty")

        pool_k = fetch_k or max(top_k * 2, top_k)
        qvec, model = embed_query(query)
        raw = self.store.search(qvec, top_k=pool_k, source_types=source_types)
        hits = _dedupe_hits(raw, top_k=top_k)
        return RetrievalResult(query=query, top_k=top_k, hits=hits, embedding_model=model)


def _dedupe_hits(hits: List[ScoredChunk], *, top_k: int) -> List[ScoredChunk]:
    seen_hash = set()
    seen_doc_section = set()
    out: List[ScoredChunk] = []
    for hit in hits:
        content_hash = hit.chunk.content_sha256
        section_key = (hit.chunk.document_id, hit.chunk.heading_path)
        if content_hash in seen_hash:
            continue
        # Prefer diversity across sections when scores are close; keep first (highest score).
        if section_key in seen_doc_section and len(out) >= max(2, top_k - 1):
            continue
        seen_hash.add(content_hash)
        seen_doc_section.add(section_key)
        out.append(hit)
        if len(out) >= top_k:
            break
    return out
