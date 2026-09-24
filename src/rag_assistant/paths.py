"""Shared filesystem paths for the RAG-Assistant knowledge pipeline."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_ROOT = PROJECT_ROOT / "knowledge"
PROCESSED_ROOT = KNOWLEDGE_ROOT / "processed"
CHUNKS_JSONL = PROCESSED_ROOT / "chunks" / "chunks.jsonl"
DOC_INDEX_PATH = PROCESSED_ROOT / "documents" / "index.json"
VECTOR_DIR = PROCESSED_ROOT / "vectors"
VECTOR_NPZ = VECTOR_DIR / "embeddings.npz"
VECTOR_META = VECTOR_DIR / "meta.json"
EVAL_DIR = PROJECT_ROOT / "evaluation"
EVAL_QUESTIONS = EVAL_DIR / "questions.json"
EVAL_RESULTS = EVAL_DIR / "results.json"
