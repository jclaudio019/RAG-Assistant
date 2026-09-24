"""Map retrieved chunks to visitor-facing Explore-further links and experience categories."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

SITE = "https://joseoclaudio.com"

# Repo slug → portfolio case-study path (when a public page exists).
PROJECT_PAGE = {
    "retail-operations": "/projects/retail-demand-forecasting",
    "credit_risk": "/projects/credit-risk-pd-model",
    "retail-allocation-simulator": "/projects/retail-allocation-simulator",
    "time_series_analysis": "/projects/time-series-analysis-r",
    "black-scholes-options-modeling": "/projects/black-scholes-options-modeling",
    "backtesting-system": "/projects/backtesting-system",
    "warehouse-club-market-expansion-strategy": "/projects/warehouse-club-market-expansion",
}


def experience_category(source_type: str, heading_path: str = "", document_id: str = "") -> str:
    path = (heading_path or "").lower()
    if source_type == "website":
        if "experience" in document_id or document_id.endswith("::experience"):
            return "professional"
        if "projects-" in document_id or document_id.endswith("::projects"):
            return "portfolio_project"
        if document_id.endswith("::about") or document_id.endswith("::home"):
            return "profile"
        if document_id.endswith("::skills"):
            return "skills"
        return "website"
    if source_type == "project":
        if "coursework" in path or "assignment" in path or "graduate" in path:
            return "coursework"
        return "portfolio_project"
    if source_type == "career_profile":
        if "professional experience" in path:
            return "professional"
        if "education" in path or "graduate financial mathematics" in path:
            return "coursework"
        if "professional development" in path or "> financial risk manager" in path:
            return "professional_development"
        if "ai / genai" in path or "> lumina" in path or "portfolio rag assistant" in path:
            return "exploratory"
        if "technical & analytical skills" in path or path.endswith("skills"):
            return "skills"
        # Avoid matching the H1 phrase "Portfolio Knowledge Base".
        if (
            "portfolio projects" in path
            or "showcased project" in path
            or " > projects" in path
            or path.rstrip().endswith("projects")
        ):
            return "portfolio_project"
        return "career_profile"
    return source_type or "unknown"


def explore_url(
    *,
    document_id: str,
    source_type: str,
    source_url: str,
    heading_path: str = "",
    repo_url: Optional[str] = None,
) -> str:
    """Prefer clickable portfolio pages; fall back to GitHub; last resort source_url."""
    if source_type == "website" and source_url.startswith("http"):
        return source_url

    if document_id.startswith("website::"):
        slug = document_id.split("::", 1)[1]
        if slug == "home":
            return f"{SITE}/"
        if slug == "skills":
            return f"{SITE}/projects"
        if slug.startswith("projects-"):
            return f"{SITE}/projects/{slug[len('projects-'):]}"
        return f"{SITE}/{slug}"

    if document_id.startswith("project::"):
        parts = document_id.split("::")
        repo = parts[1] if len(parts) > 1 else ""
        page = PROJECT_PAGE.get(repo)
        if page:
            return f"{SITE}{page}"
        if repo_url and repo_url.startswith("http"):
            return repo_url
        if source_url.startswith("http"):
            return source_url

    if source_type == "career_profile":
        path = (heading_path or "").lower()
        if "professional experience" in path:
            return f"{SITE}/experience"
        if "education" in path:
            return f"{SITE}/about"
        if "ai / genai" in path or "rag" in path:
            return f"{SITE}/projects/interactive-rag"
        if "technical" in path or "skills" in path:
            return f"{SITE}/projects"
        return f"{SITE}/experience"

    if source_url.startswith("http"):
        return source_url
    return f"{SITE}/projects"


def enrich_citations(citations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    enriched: List[Dict[str, Any]] = []
    seen = set()
    for raw in citations:
        category = experience_category(
            raw.get("source_type", ""),
            raw.get("section") or raw.get("heading_path") or "",
            raw.get("document_id", ""),
        )
        url = explore_url(
            document_id=raw.get("document_id", ""),
            source_type=raw.get("source_type", ""),
            source_url=raw.get("source_url", ""),
            heading_path=raw.get("section") or "",
            repo_url=(raw.get("metadata") or {}).get("repo_url") if isinstance(raw.get("metadata"), dict) else raw.get("repo_url"),
        )
        label = raw.get("label") or raw.get("document_title") or "Source"
        key = (url, label)
        if key in seen:
            continue
        seen.add(key)
        item = dict(raw)
        item["experience_category"] = category
        item["explore_url"] = url
        enriched.append(item)
    return enriched
