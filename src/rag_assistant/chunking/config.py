"""Configurable policies and tokenizer utilities for structure-aware chunking."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class ChunkingConfig:
    """Configuration parameters for structure-aware chunking."""

    target_tokens: int = 500
    min_tokens: int = 80
    max_tokens: int = 850
    subdivision_overlap_tokens: int = 80
    encoding_name: str = "cl100k_base"

    def get_token_counter(self) -> Callable[[str], int]:
        """Return a cached, thread-safe token length function."""
        try:
            import tiktoken

            encoding = tiktoken.get_encoding(self.encoding_name)
            return lambda text: len(encoding.encode(text, disallowed_special=()))
        except Exception:
            return lambda text: max(1, len(text.strip().split()))
