"""Cloudflare Workers AI client for embeddings + grounded generation.

Used as the low-cost default for this portfolio showcase because Gemini prepaid
credits may be unavailable, while Cloudflare credentials already exist for
HTML→Markdown ingestion.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_EMBED_MODEL = "@cf/baai/bge-base-en-v1.5"
DEFAULT_GENERATE_MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
EMBED_DIM = 768


class CloudflareAIError(RuntimeError):
    pass


def _load_dotenv() -> None:
    env_file = Path(__file__).resolve().parents[2] / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip("'\""))


_load_dotenv()


def _credentials() -> tuple[str, str]:
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    token = os.environ.get("CLOUDFLARE_AI_API_TOKEN")
    if not account_id or not token:
        raise CloudflareAIError("CLOUDFLARE_ACCOUNT_ID / CLOUDFLARE_AI_API_TOKEN not configured")
    return account_id, token


def _run(model: str, payload: Dict[str, Any], timeout: int = 90) -> Dict[str, Any]:
    account_id, token = _credentials()
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise CloudflareAIError(f"cloudflare-ai-http-{exc.code}: {detail[:500]}") from exc
    except Exception as exc:
        raise CloudflareAIError(f"cloudflare-ai-failed: {exc}") from exc

    if body.get("success") is False:
        raise CloudflareAIError(f"cloudflare-ai-error: {body.get('errors')}")
    return body.get("result") or {}


def embed_texts(
    texts: List[str],
    *,
    model: str = DEFAULT_EMBED_MODEL,
    batch_size: int = 16,
    pause_s: float = 0.05,
) -> List[List[float]]:
    vectors: List[List[float]] = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        result = _run(model, {"text": batch})
        data = result.get("data") if isinstance(result, dict) else result
        if not isinstance(data, list) or len(data) != len(batch):
            raise CloudflareAIError(
                f"embed-count-mismatch: expected {len(batch)}, got {type(data)}/{getattr(data, '__len__', lambda: '?')()}"
            )
        for row in data:
            if not row:
                raise CloudflareAIError("empty-embedding-returned")
            vectors.append(row)
        if start + batch_size < len(texts) and pause_s:
            time.sleep(pause_s)
    return vectors


def embed_query(text: str, *, model: str = DEFAULT_EMBED_MODEL) -> List[float]:
    return embed_texts([text], model=model, batch_size=1, pause_s=0)[0]


def generate_text(
    *,
    system: str,
    user: str,
    model: str = DEFAULT_GENERATE_MODEL,
    max_tokens: int = 1024,
) -> str:
    result = _run(
        model,
        {
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "max_tokens": max_tokens,
        },
    )
    # OpenAI-compatible shape from Workers AI
    choices = result.get("choices") if isinstance(result, dict) else None
    if choices:
        message = (choices[0] or {}).get("message") or {}
        content = message.get("content")
        if content:
            return str(content).strip()
    # Older/alternate shapes
    for key in ("response", "result"):
        if isinstance(result, dict) and isinstance(result.get(key), str) and result[key].strip():
            return result[key].strip()
    raise CloudflareAIError(f"empty-generation: {json.dumps(result)[:400]}")
