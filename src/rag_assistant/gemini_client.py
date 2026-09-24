"""Minimal Gemini Developer API client (embeddings + generation) via HTTPS.

Kept intentionally thin so the RAG stages stay inspectable without an SDK wrapper.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional


API_ROOT = "https://generativelanguage.googleapis.com/v1beta"
DEFAULT_EMBED_MODEL = "gemini-embedding-001"
DEFAULT_GENERATE_MODEL = "gemini-2.0-flash"
DEFAULT_EMBED_DIM = 768


class GeminiError(RuntimeError):
    pass


def _api_key() -> str:
    # Allow local .env without requiring shell export.
    env_file = Path(__file__).resolve().parents[2] / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise GeminiError("GEMINI_API_KEY (or GOOGLE_API_KEY) is not set")
    return key


def _post(path: str, payload: Dict[str, Any], timeout: int = 60) -> Dict[str, Any]:
    url = f"{API_ROOT}/{path}?key={_api_key()}"
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise GeminiError(f"gemini-http-{exc.code}: {detail[:500]}") from exc
    except Exception as exc:
        raise GeminiError(f"gemini-request-failed: {exc}") from exc


def embed_texts(
    texts: List[str],
    *,
    model: str = DEFAULT_EMBED_MODEL,
    task_type: str = "RETRIEVAL_DOCUMENT",
    output_dimensionality: int = DEFAULT_EMBED_DIM,
    batch_size: int = 16,
    pause_s: float = 0.15,
) -> List[List[float]]:
    """Embed a list of strings. Returns one vector per input text."""
    vectors: List[List[float]] = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        requests = [
            {
                "model": f"models/{model}",
                "content": {"parts": [{"text": text}]},
                "taskType": task_type,
                "outputDimensionality": output_dimensionality,
            }
            for text in batch
        ]
        payload = _post(f"models/{model}:batchEmbedContents", {"requests": requests})
        embeddings = payload.get("embeddings") or []
        if len(embeddings) != len(batch):
            raise GeminiError(
                f"embed-count-mismatch: expected {len(batch)}, got {len(embeddings)}"
            )
        for item in embeddings:
            values = item.get("values")
            if not values:
                raise GeminiError("empty-embedding-returned")
            vectors.append(values)
        if start + batch_size < len(texts) and pause_s:
            time.sleep(pause_s)
    return vectors


def embed_query(
    text: str,
    *,
    model: str = DEFAULT_EMBED_MODEL,
    output_dimensionality: int = DEFAULT_EMBED_DIM,
) -> List[float]:
    """Embed a single retrieval query (RETRIEVAL_QUERY task type)."""
    return embed_texts(
        [text],
        model=model,
        task_type="RETRIEVAL_QUERY",
        output_dimensionality=output_dimensionality,
        batch_size=1,
        pause_s=0,
    )[0]


def generate_text(
    *,
    system: str,
    user: str,
    model: str = DEFAULT_GENERATE_MODEL,
    temperature: float = 0.2,
    max_output_tokens: int = 1024,
) -> str:
    """Generate a grounded answer. Returns plain text."""
    payload = {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_output_tokens,
        },
    }
    result = _post(f"models/{model}:generateContent", payload)
    candidates = result.get("candidates") or []
    if not candidates:
        raise GeminiError(f"no-candidates: {json.dumps(result)[:400]}")
    parts = (((candidates[0] or {}).get("content") or {}).get("parts")) or []
    text = "".join(part.get("text", "") for part in parts if isinstance(part, dict))
    if not text.strip():
        raise GeminiError("empty-generation")
    return text.strip()
