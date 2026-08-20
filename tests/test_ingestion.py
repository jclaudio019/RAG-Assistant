from __future__ import annotations

import unittest
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rap_assistamt.ingestion import ingest


class TestIngestionHelpers(unittest.TestCase):
    def test_markdown_normalization_is_deterministic(self):
        raw = "Line 1  \n\n\n\nLine 2\r\nLine 3  \r\n"
        normalized = ingest._normalize_markdown_content(raw)
        self.assertEqual(normalized, "Line 1\n\nLine 2\nLine 3\n")


    def test_idempotent_manifest_keeps_content_state_when_unchanged(self):
        tmp = Path("/tmp/rap_ingest_test")
        if tmp.exists():
            for item in tmp.rglob("*"):
                if item.is_file():
                    item.unlink()
            for item in sorted(tmp.rglob("*"), reverse=True):
                if item.is_dir():
                    item.rmdir()
        tmp.mkdir(parents=True, exist_ok=True)
        original_index_path = ingest.INDEX_PATH
        ingest.INDEX_PATH = tmp / "index.json"

        try:
            index = {}
            doc = ingest.DocumentSource(
                document_id="website::home",
                source_type="website",
                source_url="https://example.com",
                raw_path="/tmp/raw/index.html",
                normalized_path="/tmp/processed/index.md",
                title="Home",
                raw_sha256="same",
                normalized_sha256="same",
                last_checked_at="2020-01-01T00:00:00+00:00",
                last_changed_at="2020-01-01T00:00:00+00:00",
                status="ingested",
            )
            ingest._upsert_document(index, doc)
            self.assertIn("website::home", index)
            first = dict(index["website::home"])

            time.sleep(1)
            ingest._upsert_document(index, doc)
            second = index["website::home"]

            self.assertEqual(second["raw_sha256"], first["raw_sha256"])
            self.assertEqual(second["normalized_sha256"], first["normalized_sha256"])
            self.assertNotEqual(second["last_checked_at"], first["last_checked_at"])
            self.assertEqual(second["last_changed_at"], first["last_changed_at"])
            self.assertEqual(second["status"], "skipped_no_change")
        finally:
            ingest.INDEX_PATH = original_index_path
            if tmp.exists():
                for item in sorted(tmp.rglob("*"), reverse=True):
                    if item.is_file() or item.is_symlink():
                        item.unlink()
                    else:
                        item.rmdir()
