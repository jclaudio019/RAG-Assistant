from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rag_assistant.citations import enrich_citations, experience_category, explore_url


class TestCitations(unittest.TestCase):
    def test_website_and_project_explore_urls(self):
        self.assertEqual(
            explore_url(
                document_id="website::projects-time-series-analysis-r",
                source_type="website",
                source_url="https://joseoclaudio.com/projects/time-series-analysis-r",
            ),
            "https://joseoclaudio.com/projects/time-series-analysis-r",
        )
        self.assertEqual(
            explore_url(
                document_id="project::time_series_analysis::README.md",
                source_type="project",
                source_url="https://github.com/jclaudio019/time_series_analysis",
            ),
            "https://joseoclaudio.com/projects/time-series-analysis-r",
        )

    def test_career_professional_maps_to_experience(self):
        self.assertEqual(
            experience_category(
                "career_profile",
                "Professional Experience > EssilorLuxottica",
                "career::knowledge_base",
            ),
            "professional",
        )
        self.assertEqual(
            explore_url(
                document_id="career::knowledge_base",
                source_type="career_profile",
                source_url="local::kb",
                heading_path="Professional Experience > EssilorLuxottica",
            ),
            "https://joseoclaudio.com/experience",
        )

    def test_unpublished_backtesting_project_uses_github_and_coursework_scope(self):
        repository = "https://github.com/jclaudio019/backtesting-system"
        document_id = "project::backtesting-system::README.md"

        self.assertEqual(
            explore_url(
                document_id=document_id,
                source_type="project",
                source_url=repository,
                repo_url=repository,
            ),
            repository,
        )
        self.assertEqual(
            experience_category("project", "Backtesting System", document_id),
            "coursework",
        )

    def test_career_h1_portfolio_word_does_not_force_project_category(self):
        self.assertEqual(
            experience_category(
                "career_profile",
                "Jose O. Claudio Vargas — Career & Portfolio Knowledge Base",
                "career::knowledge_base",
            ),
            "career_profile",
        )
        self.assertEqual(
            experience_category(
                "career_profile",
                "Jose O. Claudio Vargas — Career & Portfolio Knowledge Base > Professional Experience > EssilorLuxottica",
                "career::knowledge_base",
            ),
            "professional",
        )
        enriched = enrich_citations(
            [
                {
                    "label": "Time-series analysis",
                    "source_type": "project",
                    "source_url": "https://github.com/jclaudio019/time_series_analysis",
                    "section": "README",
                    "document_id": "project::time_series_analysis::README.md",
                },
                {
                    "label": "Time-series analysis",
                    "source_type": "project",
                    "source_url": "https://github.com/jclaudio019/time_series_analysis",
                    "section": "README",
                    "document_id": "project::time_series_analysis::README.md",
                },
            ]
        )
        self.assertEqual(len(enriched), 1)
        self.assertTrue(enriched[0]["explore_url"].endswith("/projects/time-series-analysis-r"))


if __name__ == "__main__":
    unittest.main()
