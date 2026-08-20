from __future__ import annotations

import json
import shutil
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rag_assistant.chunking import (
    ChunkingConfig,
    StructureAwareChunker,
    chunk_all_documents,
    generate_chunk_report,
)
from rag_assistant.ingestion.ingest import INDEX_PATH, PROCESSED_ROOT


class TestChunkingPipeline(unittest.TestCase):
    def setUp(self):
        self.config = ChunkingConfig(
            target_tokens=100,
            min_tokens=20,
            max_tokens=150,
            subdivision_overlap_tokens=20,
        )
        self.chunker = StructureAwareChunker(config=self.config)

    def test_structure_aware_chunking_preserves_hierarchy(self):
        doc = """# Main Project

## Architecture

This is the system architecture overview explaining components, data flow, and distributed services across multiple backend layers in detail to ensure reliable operation.

### Backend Pipeline

Detailed explanation of the Python data pipeline and ingestion rules, covering normalization, content hashing, idempotency, and structured validation.
"""
        meta = {
            "document_id": "test::doc1",
            "title": "Main Project",
            "source_type": "project",
            "source_url": "https://example.com/repo",
            "project_name": "Test Project",
        }
        chunks = self.chunker.chunk_document(meta, doc)
        self.assertGreaterEqual(len(chunks), 2)

        # Check provenance and hierarchy
        backend_chunk = next(
            (c for c in chunks if "Backend Pipeline" in c.section), None
        )
        self.assertIsNotNone(backend_chunk)
        self.assertEqual(
            backend_chunk.heading_path, "Main Project > Architecture > Backend Pipeline"
        )
        self.assertEqual(backend_chunk.parent_section, "Main Project")
        self.assertEqual(backend_chunk.document_title, "Main Project")
        self.assertEqual(backend_chunk.source_type, "project")
        self.assertTrue(backend_chunk.chunk_id.startswith("test::doc1::c"))

    def test_tiny_section_merging(self):
        doc = """# Main Project

## Summary
Short intro.

## Details
Short detail.
"""
        meta = {"document_id": "test::tiny", "title": "Main Project"}
        # With min_tokens=20, both tiny sub-10 token sections should merge into 1 chunk
        chunks = self.chunker.chunk_document(meta, doc)
        self.assertEqual(len(chunks), 1)

    def test_chunking_is_deterministic(self):
        doc = """# Case Study

## Executive Summary
Results of the forecasting analysis across 365 test days.

## Methodology
Expanding window validation comparing linear regression, prophet, and xgboost.
"""
        meta = {"document_id": "test::det", "title": "Case Study"}
        first_run = self.chunker.chunk_document(meta, doc)
        second_run = self.chunker.chunk_document(meta, doc)

        self.assertEqual(len(first_run), len(second_run))
        for c1, c2 in zip(first_run, second_run):
            self.assertEqual(c1.chunk_id, c2.chunk_id)
            self.assertEqual(c1.content_sha256, c2.content_sha256)
            self.assertEqual(c1.token_count, c2.token_count)
            self.assertEqual(c1.content, c2.content)

    def test_oversized_section_subdivision(self):
        long_paragraph = (
            "This is a long sentence explaining credit risk analysis in detail. " * 30
        )
        doc = f"# Credit Risk\n\n## Overview\n\n{long_paragraph}"
        meta = {"document_id": "test::oversized", "title": "Credit Risk"}

        chunks = self.chunker.chunk_document(meta, doc)
        self.assertGreater(len(chunks), 1)
        for c in chunks:
            self.assertLessEqual(c.token_count, self.config.max_tokens + 25)
            self.assertEqual(c.heading_path, "Credit Risk > Overview")

    def test_chunk_all_documents_end_to_end(self):
        if not INDEX_PATH.exists():
            self.skipTest("Index manifest not found, skipping full integration test")

        tmp_dir = Path("/tmp/rag_chunk_test")
        if tmp_dir.exists():
            shutil.rmtree(tmp_dir)
        tmp_dir.mkdir(parents=True, exist_ok=True)

        try:
            prod_config = ChunkingConfig()
            chunks, summary = chunk_all_documents(
                index_path=INDEX_PATH,
                output_dir=tmp_dir,
                config=prod_config,
            )
            self.assertGreater(len(chunks), 20)
            self.assertTrue((tmp_dir / "chunks.jsonl").exists())

            report = generate_chunk_report(
                index_path=INDEX_PATH,
                chunks=chunks,
                config=prod_config,
                output_dir=tmp_dir,
            )
            self.assertGreater(report.total_chunks, 0)
            self.assertGreaterEqual(report.source_word_coverage_pct, 98.0)
            self.assertTrue(report.validation_checks["no_empty_chunks"])
            self.assertTrue(report.validation_checks["all_chunk_ids_unique"])
            self.assertTrue((tmp_dir / "chunk_report.json").exists())
            self.assertTrue((tmp_dir / "chunk_report.md").exists())
        finally:
            if tmp_dir.exists():
                shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    unittest.main()
