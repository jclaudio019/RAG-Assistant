"""Stage 8: thin FastAPI surface for the portfolio demo."""

from __future__ import annotations

import os
import time
from collections import defaultdict, deque
from typing import Deque, Dict, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from rag_assistant.ask import ask
from rag_assistant.paths import VECTOR_META, VECTOR_NPZ
from rag_assistant.retrieval import Retriever

MAX_QUERY_CHARS = 500
DEFAULT_TOP_K = 6
MAX_TOP_K = 8
RATE_LIMIT_WINDOW_S = 60
RATE_LIMIT_MAX = int(os.environ.get("RAG_RATE_LIMIT_PER_MINUTE", "8"))

app = FastAPI(title="RAG-Assistant", version="0.2.0")

_origins = [
    o.strip()
    for o in os.environ.get(
        "RAG_CORS_ORIGINS",
        "http://localhost:3000,https://joseoclaudio.com,https://www.joseoclaudio.com",
    ).split(",")
    if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins or ["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

_retriever: Optional[Retriever] = None
_hits: Dict[str, Deque[float]] = defaultdict(deque)


def get_retriever() -> Retriever:
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=MAX_QUERY_CHARS)
    top_k: int = Field(DEFAULT_TOP_K, ge=1, le=MAX_TOP_K)


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


def _rate_limit(ip: str) -> None:
    now = time.time()
    bucket = _hits[ip]
    while bucket and now - bucket[0] > RATE_LIMIT_WINDOW_S:
        bucket.popleft()
    if len(bucket) >= RATE_LIMIT_MAX:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again shortly.")
    bucket.append(now)


@app.get("/health")
def health():
    ready = VECTOR_NPZ.exists() and VECTOR_META.exists()
    return {
        "ok": True,
        "index_ready": ready,
        "rate_limit_per_minute": RATE_LIMIT_MAX,
    }


@app.post("/api/ask")
def api_ask(payload: AskRequest, request: Request):
    _rate_limit(_client_ip(request))
    question = payload.question.strip()
    if len(question) < 3:
        raise HTTPException(status_code=400, detail="Question too short.")
    try:
        result = ask(question, retriever=get_retriever(), top_k=payload.top_k)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Generation failed: {exc}") from exc

    # Public response: answer + citations + inspectable retrieval (no private CoT).
    return {
        "question": result.query,
        "answer": result.answer,
        "abstained": result.abstained,
        "citations": result.citations,
        "explore": [
            {
                "label": c.get("label"),
                "explore_url": c.get("explore_url"),
                "experience_category": c.get("experience_category"),
                "section": c.get("section"),
            }
            for c in result.citations
            if c.get("explore_url")
        ],
        "generator_model": result.generator_model,
        "flow": result.to_dict()["flow"],
        "retrieved": [
            {
                "chunk_id": h.chunk.chunk_id,
                "document_id": h.chunk.document_id,
                "title": h.chunk.project_name or h.chunk.document_title,
                "section": h.chunk.heading_path,
                "source_type": h.chunk.source_type,
                "source_url": h.chunk.source_url,
                "score": round(h.score, 4),
                "excerpt": h.chunk.content[:280],
            }
            for h in result.retrieval.hits
        ],
    }
