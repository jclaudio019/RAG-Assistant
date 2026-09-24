"""Export the numpy vector index into a compact JSON payload for Cloudflare Workers."""

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any, Dict

import numpy as np

from rag_assistant.paths import PROJECT_ROOT, VECTOR_META, VECTOR_NPZ


def export_worker_index(
    output_path: Path | None = None,
) -> Dict[str, Any]:
    if not VECTOR_NPZ.exists() or not VECTOR_META.exists():
        raise FileNotFoundError("Run `python -m rag_assistant.main embed` first.")

    vectors = np.load(VECTOR_NPZ)["vectors"].astype(np.float32)
    meta = json.loads(VECTOR_META.read_text(encoding="utf-8"))
    # L2-normalize so the Worker only needs a dot product.
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms = np.maximum(norms, 1e-12)
    unit = vectors / norms

    payload = {
        "embedding_model": meta.get("embedding_model"),
        "dimensions": int(unit.shape[1]),
        "chunk_count": int(unit.shape[0]),
        "vectors_base64": base64.b64encode(unit.tobytes()).decode("ascii"),
        "chunks": meta["chunks"],
    }

    default_out = PROJECT_ROOT / "deploy" / "worker_index.json"
    out = output_path or default_out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return {
        "output_path": str(out),
        "chunk_count": payload["chunk_count"],
        "dimensions": payload["dimensions"],
        "bytes": out.stat().st_size,
    }
