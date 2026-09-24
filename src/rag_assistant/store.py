"""Lightweight persisted vector index for the portfolio corpus (~154 chunks).

Why numpy + local files:
- Corpus is tiny; brute-force cosine is transparent and fast enough.
- No Pinecone/Qdrant/chroma ops burden for a learning showcase.
- Metadata stays beside vectors so citations remain inspectable.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import numpy as np

from rag_assistant.paths import CHUNKS_JSONL, VECTOR_META, VECTOR_NPZ


@dataclass(frozen=True)
class IndexedChunk:
    chunk_id: str
    document_id: str
    source_type: str
    source_url: str
    document_title: str
    project_name: Optional[str]
    section: str
    parent_section: str
    heading_path: str
    chunk_index: int
    content: str
    token_count: int
    content_sha256: str
    metadata: Dict[str, Any]

    @classmethod
    def from_chunk_row(cls, row: Dict[str, Any]) -> "IndexedChunk":
        return cls(
            chunk_id=row["chunk_id"],
            document_id=row["document_id"],
            source_type=row.get("source_type", ""),
            source_url=row.get("source_url", ""),
            document_title=row.get("document_title", ""),
            project_name=row.get("project_name"),
            section=row.get("section", ""),
            parent_section=row.get("parent_section", ""),
            heading_path=row.get("heading_path", ""),
            chunk_index=int(row.get("chunk_index", 0)),
            content=row.get("content", ""),
            token_count=int(row.get("token_count", 0)),
            content_sha256=row.get("content_sha256", ""),
            metadata=row.get("metadata") or {},
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ScoredChunk:
    chunk: IndexedChunk
    score: float

    def to_dict(self) -> Dict[str, Any]:
        payload = self.chunk.to_dict()
        payload["score"] = round(float(self.score), 6)
        return payload


class NumpyVectorStore:
    """In-memory cosine index loaded from embeddings.npz + meta.json."""

    def __init__(self, vectors: np.ndarray, chunks: List[IndexedChunk], model: str, dim: int):
        if vectors.ndim != 2:
            raise ValueError("vectors must be 2-D")
        if len(chunks) != vectors.shape[0]:
            raise ValueError("chunk/meta count must match embedding rows")
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms = np.maximum(norms, 1e-12)
        self.vectors = (vectors / norms).astype(np.float32)
        self.chunks = chunks
        self.model = model
        self.dim = dim

    @classmethod
    def load(
        cls,
        npz_path: Path = VECTOR_NPZ,
        meta_path: Path = VECTOR_META,
    ) -> "NumpyVectorStore":
        if not npz_path.exists() or not meta_path.exists():
            raise FileNotFoundError(
                f"Vector index missing. Run `python -m rag_assistant.main embed` first.\n"
                f"Expected: {npz_path} and {meta_path}"
            )
        data = np.load(npz_path)
        vectors = data["vectors"]
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        chunks = [IndexedChunk(**row) for row in meta["chunks"]]
        return cls(
            vectors=vectors,
            chunks=chunks,
            model=meta.get("embedding_model", ""),
            dim=int(meta.get("dimensions", vectors.shape[1])),
        )

    def search(
        self,
        query_vector: Sequence[float],
        *,
        top_k: int = 5,
        source_types: Optional[Sequence[str]] = None,
    ) -> List[ScoredChunk]:
        q = np.asarray(query_vector, dtype=np.float32)
        q = q / max(float(np.linalg.norm(q)), 1e-12)
        scores = self.vectors @ q
        order = np.argsort(-scores)
        results: List[ScoredChunk] = []
        allowed = set(source_types) if source_types else None
        for idx in order:
            chunk = self.chunks[int(idx)]
            if allowed is not None and chunk.source_type not in allowed:
                continue
            results.append(ScoredChunk(chunk=chunk, score=float(scores[int(idx)])))
            if len(results) >= top_k:
                break
        return results


def load_chunks_jsonl(path: Path = CHUNKS_JSONL) -> List[IndexedChunk]:
    if not path.exists():
        raise FileNotFoundError(f"Missing chunks corpus: {path}")
    chunks: List[IndexedChunk] = []
    with path.open("r", encoding="utf-8") as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            chunks.append(IndexedChunk.from_chunk_row(json.loads(line)))
    return chunks


def save_index(
    *,
    vectors: np.ndarray,
    chunks: List[IndexedChunk],
    embedding_model: str,
    npz_path: Path = VECTOR_NPZ,
    meta_path: Path = VECTOR_META,
) -> Dict[str, Any]:
    npz_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(npz_path, vectors=vectors.astype(np.float32))
    meta = {
        "embedding_model": embedding_model,
        "dimensions": int(vectors.shape[1]),
        "chunk_count": len(chunks),
        "chunks": [c.to_dict() for c in chunks],
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "npz_path": str(npz_path),
        "meta_path": str(meta_path),
        "chunk_count": len(chunks),
        "dimensions": int(vectors.shape[1]),
        "embedding_model": embedding_model,
    }
