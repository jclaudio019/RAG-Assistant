from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rag_assistant.context import assemble_context
from rag_assistant.retrieval import Retriever, _dedupe_hits
from rag_assistant.store import IndexedChunk, NumpyVectorStore, ScoredChunk, save_index


def _fake_chunk(i: int, document_id: str, content: str, section: str = "Sec") -> IndexedChunk:
    return IndexedChunk(
        chunk_id=f"{document_id}::c{i:04d}",
        document_id=document_id,
        source_type="career_profile",
        source_url="https://example.com",
        document_title="Test Doc",
        project_name=None,
        section=section,
        parent_section="Root",
        heading_path=f"Root > {section}",
        chunk_index=i,
        content=content,
        token_count=10,
        content_sha256=f"hash-{i}-{document_id}",
        metadata={},
    )


class TestRetrievalOffline(unittest.TestCase):
    def test_vector_search_returns_nearest_neighbor_and_metadata(self):
        chunks = [
            _fake_chunk(0, "career::knowledge_base", "EssilorLuxottica Supply Chain Analyst forecasting"),
            _fake_chunk(1, "project::credit_risk::README.md", "credit risk logistic regression scorecard"),
            _fake_chunk(2, "website::about", "Purdue University Applied Statistics"),
        ]
        # Hand-built orthonormal-ish vectors so search is deterministic without Gemini.
        vectors = np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=np.float32,
        )
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            npz = tmp_path / "embeddings.npz"
            meta = tmp_path / "meta.json"
            save_index(
                vectors=vectors,
                chunks=chunks,
                embedding_model="test",
                npz_path=npz,
                meta_path=meta,
            )
            store = NumpyVectorStore.load(npz, meta)
            hits = store.search([0.9, 0.1, 0.0], top_k=2)
            self.assertEqual(hits[0].chunk.document_id, "career::knowledge_base")
            self.assertEqual(hits[0].chunk.source_url, "https://example.com")
            self.assertGreater(hits[0].score, hits[1].score)

    def test_dedupe_keeps_unique_content_hashes(self):
        a = _fake_chunk(0, "doc", "same", section="A")
        b = IndexedChunk(**{**a.to_dict(), "chunk_id": "doc::c0001", "chunk_index": 1})
        c = _fake_chunk(2, "doc", "other", section="B")
        hits = [
            ScoredChunk(chunk=a, score=0.9),
            ScoredChunk(chunk=b, score=0.8),
            ScoredChunk(chunk=c, score=0.7),
        ]
        # Force identical hash on a/b
        b_dict = b.to_dict()
        b_dict["content_sha256"] = a.content_sha256
        b2 = IndexedChunk(**b_dict)
        hits[1] = ScoredChunk(chunk=b2, score=0.8)
        out = _dedupe_hits(hits, top_k=5)
        self.assertEqual(len(out), 2)
        self.assertEqual(out[0].chunk.chunk_id, "doc::c0000")

    def test_assemble_context_preserves_provenance_and_budget(self):
        career = _fake_chunk(0, "career::knowledge_base", "Professional experience at EssilorLuxottica.")
        website = IndexedChunk(
            **{
                **_fake_chunk(1, "website::experience", "Supply Chain Analyst role details.").to_dict(),
                "document_title": "Experience",
                "source_url": "https://joseoclaudio.com/experience",
            }
        )
        hits = [
            ScoredChunk(chunk=career, score=0.91),
            ScoredChunk(chunk=website, score=0.88),
        ]
        ctx = assemble_context(hits, max_chars=5000)
        self.assertIn("EssilorLuxottica", ctx.evidence_block)
        self.assertEqual(len(ctx.citations), 2)
        self.assertTrue(ctx.citations[0]["source_url"])
        self.assertGreater(ctx.approx_chars, 0)


if __name__ == "__main__":
    unittest.main()
