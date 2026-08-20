"""Structure-aware contextual chunking implementation for RAG-Assistant."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from rag_assistant.chunking.config import ChunkingConfig


@dataclass(frozen=True)
class Chunk:
    """A retrieval-ready, structure-aware chunk of text."""

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
    char_count: int
    content_sha256: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class StructureAwareChunker:
    """Parses Markdown documents by heading hierarchy and creates context-rich chunks."""

    def __init__(self, config: Optional[ChunkingConfig] = None) -> None:
        self.config = config or ChunkingConfig()
        self.token_counter = self.config.get_token_counter()
        self.header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "h1"),
                ("##", "h2"),
                ("###", "h3"),
            ],
            strip_headers=False,
        )
        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.target_tokens,
            chunk_overlap=self.config.subdivision_overlap_tokens,
            length_function=self.token_counter,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def _extract_heading_context(self, meta: Dict[str, str], default_title: str) -> tuple[str, str, str]:
        """Extract (section, parent_section, heading_path) from header metadata."""
        h1 = meta.get("h1", "").strip()
        h2 = meta.get("h2", "").strip()
        h3 = meta.get("h3", "").strip()

        path_parts = [p for p in [h1, h2, h3] if p]
        if not path_parts:
            return default_title, default_title, default_title

        heading_path = " > ".join(path_parts)
        section = h3 or h2 or h1 or default_title
        parent_section = h1 if (h2 or h3) else default_title
        return section, parent_section, heading_path

    def _subdivide_if_needed(self, content: str) -> List[str]:
        """Subdivide oversized content using recursive character splitting."""
        token_len = self.token_counter(content)
        if token_len <= self.config.max_tokens:
            return [content]

        sub_chunks = self.recursive_splitter.split_text(content)
        return [sc for sc in sub_chunks if sc.strip()]

    def chunk_document(self, doc_meta: Dict[str, Any], markdown_text: str) -> List[Chunk]:
        """Convert a normalized Markdown document into structure-aware Chunk objects."""
        document_id = doc_meta.get("document_id", "unknown")
        document_title = doc_meta.get("title", "Untitled")
        source_type = doc_meta.get("source_type", "unknown")
        source_url = doc_meta.get("source_url", "")
        project_name = doc_meta.get("project_name")

        cleaned_text = markdown_text.strip()
        if not cleaned_text:
            return []

        # Extract structural sections via MarkdownHeaderTextSplitter
        raw_sections = self.header_splitter.split_text(cleaned_text)
        if not raw_sections:
            raw_sections = [
                type("DocSection", (), {"page_content": cleaned_text, "metadata": {}})()
            ]

        # Stage 1: Merge tiny orphan leading sections (like standalone frontmatter) with next section
        normalized_sections: List[tuple[str, str, str, str]] = []
        pending_prefix = ""

        for s in raw_sections:
            content = s.page_content.strip()
            if not content:
                continue

            section, parent_sec, heading_path = self._extract_heading_context(
                getattr(s, "metadata", {}), document_title
            )

            # If section is empty or pure frontmatter without headers, buffer to prepend
            if not getattr(s, "metadata", {}) and content.startswith("---"):
                pending_prefix = content + "\n\n"
                continue

            if pending_prefix:
                content = pending_prefix + content
                pending_prefix = ""

            normalized_sections.append((section, parent_sec, heading_path, content))

        # If only prefix remained
        if pending_prefix and not normalized_sections:
            normalized_sections.append(
                (document_title, document_title, document_title, pending_prefix.strip())
            )

        # Stage 2: Merge adjacent tiny sections sharing the exact same parent section if < min_tokens
        merged_sections: List[tuple[str, str, str, str]] = []
        for section, parent_sec, heading_path, content in normalized_sections:
            if not merged_sections:
                merged_sections.append((section, parent_sec, heading_path, content))
                continue

            prev_sec, prev_parent, prev_path, prev_content = merged_sections[-1]
            prev_tokens = self.token_counter(prev_content)
            curr_tokens = self.token_counter(content)

            # Merge if both are small, share parent, and together don't exceed target tokens
            if (
                prev_parent == parent_sec
                and (prev_tokens < self.config.min_tokens or curr_tokens < self.config.min_tokens)
                and (prev_tokens + curr_tokens <= self.config.target_tokens)
            ):
                combined_content = f"{prev_content}\n\n{content}"
                merged_sections[-1] = (section, parent_sec, heading_path, combined_content)
            else:
                merged_sections.append((section, parent_sec, heading_path, content))

        # Stage 3: Subdivide oversized sections and construct final Chunk objects
        chunks: List[Chunk] = []
        chunk_idx = 0

        for section, parent_sec, heading_path, content in merged_sections:
            sub_texts = self._subdivide_if_needed(content)

            for sub_text in sub_texts:
                clean_sub = sub_text.strip()
                if not clean_sub:
                    continue

                chunk_id = f"{document_id}::c{chunk_idx:04d}"
                tok_count = self.token_counter(clean_sub)
                char_count = len(clean_sub)
                sha256_hash = hashlib.sha256(clean_sub.encode("utf-8")).hexdigest()

                chunks.append(
                    Chunk(
                        chunk_id=chunk_id,
                        document_id=document_id,
                        source_type=source_type,
                        source_url=source_url,
                        document_title=document_title,
                        project_name=project_name,
                        section=section,
                        parent_section=parent_sec,
                        heading_path=heading_path,
                        chunk_index=chunk_idx,
                        content=clean_sub,
                        token_count=tok_count,
                        char_count=char_count,
                        content_sha256=sha256_hash,
                        metadata={
                            "file_path": doc_meta.get("file_path"),
                            "repo_url": doc_meta.get("repo_url"),
                            "raw_path": doc_meta.get("raw_path"),
                            "normalized_path": doc_meta.get("normalized_path"),
                        },
                    )
                )
                chunk_idx += 1

        return chunks


def chunk_all_documents(
    index_path: Path,
    output_dir: Path,
    config: Optional[ChunkingConfig] = None,
) -> tuple[List[Chunk], dict]:
    """Load all processed documents from index.json and chunk them into chunks.jsonl."""
    if not index_path.exists():
        raise FileNotFoundError(f"Index manifest not found at: {index_path}")

    with index_path.open("r", encoding="utf-8") as fp:
        index_data = json.load(fp)

    documents = index_data.get("documents", [])
    chunker = StructureAwareChunker(config=config)
    all_chunks: List[Chunk] = []
    doc_chunk_counts: Dict[str, int] = {}

    for doc_meta in documents:
        norm_path_str = doc_meta.get("normalized_path")
        if not norm_path_str:
            continue

        norm_path = Path(norm_path_str)
        if not norm_path.exists():
            continue

        content = norm_path.read_text(encoding="utf-8")
        doc_chunks = chunker.chunk_document(doc_meta, content)
        all_chunks.extend(doc_chunks)
        doc_chunk_counts[doc_meta["document_id"]] = len(doc_chunks)

    # Write output chunks.jsonl
    output_dir.mkdir(parents=True, exist_ok=True)
    chunks_jsonl_path = output_dir / "chunks.jsonl"

    with chunks_jsonl_path.open("w", encoding="utf-8") as fp:
        for c in all_chunks:
            fp.write(json.dumps(c.to_dict(), ensure_ascii=False) + "\n")

    summary = {
        "documents_processed": len(doc_chunk_counts),
        "total_chunks": len(all_chunks),
        "chunks_jsonl_path": str(chunks_jsonl_path),
        "chunks_per_document": doc_chunk_counts,
    }

    return all_chunks, summary
