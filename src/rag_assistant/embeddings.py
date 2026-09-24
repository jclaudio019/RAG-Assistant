"""Stage 3: embed chunks.jsonl into the local numpy vector store."""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from rag_assistant.providers import embed_documents
from rag_assistant.store import load_chunks_jsonl, save_index


def build_embeddings() -> Dict[str, Any]:
    chunks = load_chunks_jsonl()
    texts = [
        f"Title: {c.document_title}\nSection: {c.heading_path}\n\n{c.content}"
        for c in chunks
    ]
    vectors, model = embed_documents(texts)
    matrix = np.asarray(vectors, dtype=np.float32)
    result = save_index(vectors=matrix, chunks=chunks, embedding_model=model)
    result["provider"] = model
    return result
