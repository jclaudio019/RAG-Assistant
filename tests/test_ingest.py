from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rag_assistant.ingestion.ingest import _prune_unconfigured_sources


class TestIngestionState(unittest.TestCase):
    def test_prunes_sources_removed_from_configuration(self):
        current_website = "website::home"
        current_project = "project::backtesting-system::README.md"
        stale_website = "website::projects-backtesting-system"
        stale_project = "project::removed-project::README.md"
        career_profile = "career::knowledge_base"
        index = {
            document_id: {"document_id": document_id}
            for document_id in (
                current_website,
                current_project,
                stale_website,
                stale_project,
                career_profile,
            )
        }

        _prune_unconfigured_sources(index)

        self.assertIn(current_website, index)
        self.assertIn(current_project, index)
        self.assertIn(career_profile, index)
        self.assertNotIn(stale_website, index)
        self.assertNotIn(stale_project, index)


if __name__ == "__main__":
    unittest.main()