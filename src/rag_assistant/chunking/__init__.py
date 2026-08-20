"""Chunking subsystem for RAG-Assistant."""

from rag_assistant.chunking.chunker import (
    Chunk,
    StructureAwareChunker,
    chunk_all_documents,
)
from rag_assistant.chunking.config import ChunkingConfig
from rag_assistant.chunking.reporter import ChunkReport, generate_chunk_report

__all__ = [
    "Chunk",
    "ChunkingConfig",
    "StructureAwareChunker",
    "ChunkReport",
    "chunk_all_documents",
    "generate_chunk_report",
]
