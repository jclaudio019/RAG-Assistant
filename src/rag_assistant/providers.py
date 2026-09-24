"""Provider selection for embeddings and generation.

Defaults favor Cloudflare Workers AI for this showcase (existing credentials,
low cost). Set RAG_EMBED_PROVIDER=gemini / RAG_GENERATE_PROVIDER=gemini when
Gemini billing is available.
"""

from __future__ import annotations

import os
from typing import List, Tuple

from rag_assistant import cloudflare_ai, gemini_client


def embed_provider() -> str:
    return (os.environ.get("RAG_EMBED_PROVIDER") or "cloudflare").strip().lower()


def generate_provider() -> str:
    return (os.environ.get("RAG_GENERATE_PROVIDER") or "cloudflare").strip().lower()


def embed_documents(texts: List[str]) -> Tuple[List[List[float]], str]:
    provider = embed_provider()
    if provider == "gemini":
        vectors = gemini_client.embed_texts(texts, task_type="RETRIEVAL_DOCUMENT")
        return vectors, gemini_client.DEFAULT_EMBED_MODEL
    vectors = cloudflare_ai.embed_texts(texts)
    return vectors, cloudflare_ai.DEFAULT_EMBED_MODEL


def embed_query(text: str) -> Tuple[List[float], str]:
    provider = embed_provider()
    if provider == "gemini":
        return gemini_client.embed_query(text), gemini_client.DEFAULT_EMBED_MODEL
    return cloudflare_ai.embed_query(text), cloudflare_ai.DEFAULT_EMBED_MODEL


def generate_answer(*, system: str, user: str) -> Tuple[str, str]:
    provider = generate_provider()
    if provider == "gemini":
        try:
            text = gemini_client.generate_text(system=system, user=user)
            return text, gemini_client.DEFAULT_GENERATE_MODEL
        except gemini_client.GeminiError:
            # Automatic fallback keeps the public demo usable if Gemini credits lapse.
            text = cloudflare_ai.generate_text(system=system, user=user)
            return text, f"{cloudflare_ai.DEFAULT_GENERATE_MODEL} (fallback)"
    text = cloudflare_ai.generate_text(system=system, user=user)
    return text, cloudflare_ai.DEFAULT_GENERATE_MODEL
