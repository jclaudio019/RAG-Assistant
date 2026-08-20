"""Ingestion-only pipeline for website and showcase GitHub project documents."""

from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional


@dataclass(frozen=True)
class DocumentSource:
    document_id: str
    source_type: str
    source_url: str
    raw_path: str
    normalized_path: str
    title: str
    raw_sha256: str
    normalized_sha256: str
    last_checked_at: str
    last_changed_at: str
    status: str = "ingested"
    repo_url: Optional[str] = None
    file_path: Optional[str] = None
    project_name: Optional[str] = None


PROJECT_ROOT = Path(__file__).resolve().parents[3]
KNOWLEDGE_ROOT = PROJECT_ROOT / "knowledge"
RAW_ROOT = KNOWLEDGE_ROOT / "raw"
PROCESSED_ROOT = KNOWLEDGE_ROOT / "processed" / "documents"
INDEX_PATH = PROCESSED_ROOT / "index.json"
WEBSITE_ROOT = "https://joseoclaudio.com"


WEBSITE_PAGE_ORDER: List[dict] = [
    {"path": "/", "slug": "home", "title": "Home"},
    {"path": "/about", "slug": "about", "title": "About"},
    {"path": "/projects", "slug": "projects", "title": "Projects"},
    {"path": "/projects/retail-demand-forecasting", "slug": "projects-retail-demand-forecasting", "title": "Retail demand forecasting"},
    {"path": "/projects/credit-risk-pd-model", "slug": "projects-credit-risk-pd-model", "title": "Credit risk PD model"},
    {"path": "/projects/retail-allocation-simulator", "slug": "projects-retail-allocation-simulator", "title": "Retail allocation simulator"},
    {"path": "/projects/time-series-analysis-r", "slug": "projects-time-series-analysis-r", "title": "Time-series analysis"},
    {"path": "/projects/black-scholes-options-modeling", "slug": "projects-black-scholes-options-modeling", "title": "Black-Scholes modeling"},
    {"path": "/projects/backtesting-system", "slug": "projects-backtesting-system", "title": "Backtesting system"},
    {"path": "/projects/warehouse-club-market-expansion", "slug": "projects-warehouse-club-market-expansion", "title": "Warehouse club expansion"},
    {"path": "/experience", "slug": "experience", "title": "Experience"},
    {"path": "/skills", "slug": "skills", "title": "Skills"},
]


SHOWCASED_PROJECTS: List[dict] = [
    {
        "name": "Retail demand forecasting",
        "repo": "retail-operations",
        "repo_url": "https://github.com/jclaudio019/retail-operations",
        "owner": "jclaudio019",
        "branch": "main",
    },
    {
        "name": "Credit risk PD model",
        "repo": "credit_risk",
        "repo_url": "https://github.com/jclaudio019/credit_risk",
        "owner": "jclaudio019",
        "branch": "main",
    },
    {
        "name": "Retail allocation simulator",
        "repo": "retail-allocation-simulator",
        "repo_url": "https://github.com/jclaudio019/retail-allocation-simulator",
        "owner": "jclaudio019",
        "branch": "main",
    },
    {
        "name": "Time-series analysis",
        "repo": "time_series_analysis",
        "repo_url": "https://github.com/jclaudio019/time_series_analysis",
        "owner": "jclaudio019",
        "branch": "main",
    },
    {
        "name": "Black-Scholes options modeling",
        "repo": "black-scholes-options-modeling",
        "repo_url": "https://github.com/jclaudio019/black-scholes-options-modeling",
        "owner": "jclaudio019",
        "branch": "main",
    },
    {
        "name": "Backtesting system",
        "repo": "backtesting-system",
        "repo_url": "https://github.com/jclaudio019/backtesting-system",
        "owner": "jclaudio019",
        "branch": "main",
    },
    {
        "name": "Warehouse club market expansion",
        "repo": "warehouse-club-market-expansion-strategy",
        "repo_url": "https://github.com/jclaudio019/warehouse-club-market-expansion-strategy",
        "owner": "jclaudio019",
        "branch": "main",
    },
]


def _load_env() -> None:
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))


_load_env()


class IngestionError(RuntimeError):
    pass


def _read_json(path: Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def _write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=2, sort_keys=True)
        fp.write("\n")


def _write_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _normalize_markdown_content(raw_markdown: str) -> str:
    text = raw_markdown.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()
    return text + "\n"


def _fetch(url: str, timeout: int = 30) -> bytes:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read()
    except Exception as exc:
        raise IngestionError(f"fetch-failed: {url}") from exc


def _fetch_json(url: str, timeout: int = 30) -> object:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "rap-assistant-ingestion/1.0",
    }
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return {"error": "not-found"}
        raise IngestionError(f"api-fetch-failed:{exc.code}:{url}") from exc
    except Exception as exc:
        raise IngestionError(f"api-fetch-failed:{url}") from exc


def _extract_html_title(html: str) -> str:
    match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    return "Untitled"


def _decode_html(html_bytes: bytes) -> str:
    return html_bytes.decode("utf-8", errors="replace")


def _to_markdown_payload_to_text(payload: object) -> str:
    if isinstance(payload, str):
        return payload.strip() + "\n"
    if not isinstance(payload, dict):
        raise IngestionError("invalid-cloudflare-response")

    if "result" in payload:
        res = payload["result"]
        if isinstance(res, str):
            return res.strip() + "\n"
        if isinstance(res, dict):
            for key in ("data", "text", "content", "markdown"):
                if key in res and isinstance(res[key], str):
                    return res[key].strip() + "\n"
        if isinstance(res, list) and res:
            first = res[0]
            if isinstance(first, str):
                return first.strip() + "\n"
            if isinstance(first, dict):
                for key in ("data", "text", "content", "markdown"):
                    if key in first and isinstance(first[key], str):
                        return first[key].strip() + "\n"

    if "data" in payload:
        data = payload["data"]
        if isinstance(data, str):
            return data.strip() + "\n"
        if isinstance(data, dict):
            for key in ("text", "content", "markdown"):
                if key in data and isinstance(data[key], str):
                    return data[key].strip() + "\n"

    raise IngestionError("unsupported-cloudflare-response-shape")


def _cloudflare_to_markdown(
    html: str,
    source_url: str,
    account_id: Optional[str],
    api_token: Optional[str],
) -> str:
    endpoint = os.environ.get(
        "CLOUDFLARE_TO_MARKDOWN_ENDPOINT",
        f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/tomarkdown" if account_id else "",
    )
    if not endpoint or not api_token:
        raise IngestionError("cloudflare-credentials-not-configured")

    import uuid
    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    filename = Path(urllib.parse.urlparse(source_url).path).name or "index"
    if not filename.endswith(".html"):
        filename = f"{filename}.html"

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="files"; filename="{filename}"\r\n'
        f"Content-Type: text/html\r\n\r\n"
        f"{html}\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")

    request = urllib.request.Request(
        endpoint,
        data=body,
        headers={
            "Authorization": f"Bearer {api_token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
            return _to_markdown_payload_to_text(payload)
    except Exception as exc:
        raise IngestionError(f"cloudflare-tomarkdown-failed:{source_url}") from exc


def _render_website_pages(pages: List[dict]) -> Dict[str, tuple[str, str]]:
    """Render pages using Playwright headless browser for SPA apps, returning {path: (html, title)}."""
    rendered: Dict[str, tuple[str, str]] = {}
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            for p_info in pages:
                path = p_info["path"]
                url = f"{WEBSITE_ROOT}{path}"
                try:
                    page.goto(url, wait_until="networkidle", timeout=30000)
                    rendered[path] = (page.content(), page.title())
                except Exception:
                    pass
            browser.close()
    except Exception:
        pass
    return rendered


def _load_state() -> dict:
    raw = _read_json(INDEX_PATH, default={"documents": []})
    docs = raw.get("documents", [])
    index = {}
    for item in docs:
        if isinstance(item, dict) and "document_id" in item:
            index[item["document_id"]] = item
    return index


def _save_state(index: dict):
    _write_json(INDEX_PATH, {"documents": [index[k] for k in sorted(index)]})


def _sanitize_state_field(value: Optional[str]) -> str:
    if not value:
        return ""
    return str(value)


def _upsert_document(index: dict, doc: DocumentSource) -> None:
    existing = index.get(doc.document_id)
    if existing is None:
        index[doc.document_id] = asdict(doc)
        return

    unchanged = (
        bool(existing.get("normalized_sha256"))
        and existing.get("normalized_sha256") == doc.normalized_sha256
    )

    now = _now_utc()
    existing["last_checked_at"] = now
    if unchanged:
        existing["status"] = "skipped_no_change"
        return

    existing.update({
        "status": doc.status,
        "source_type": doc.source_type,
        "source_url": _sanitize_state_field(doc.source_url),
        "raw_path": _sanitize_state_field(doc.raw_path),
        "normalized_path": _sanitize_state_field(doc.normalized_path),
        "title": _sanitize_state_field(doc.title),
        "raw_sha256": _sanitize_state_field(doc.raw_sha256),
        "normalized_sha256": _sanitize_state_field(doc.normalized_sha256),
        "last_changed_at": _now_utc(),
        "repo_url": _sanitize_state_field(doc.repo_url),
        "file_path": _sanitize_state_field(doc.file_path),
        "project_name": _sanitize_state_field(doc.project_name),
    })


def _upsert_failed(index: dict, doc_id: str, source_type: str, source_url: str, title: str, details: str, repo_url: Optional[str] = None) -> None:
    now = _now_utc()
    existing = index.get(doc_id, {
        "document_id": doc_id,
        "source_type": source_type,
        "source_url": source_url,
        "raw_path": "",
        "normalized_path": "",
        "title": title,
        "raw_sha256": "",
        "normalized_sha256": "",
        "last_changed_at": now,
    })
    existing["last_checked_at"] = now
    existing["status"] = f"failed: {details}"
    if repo_url:
        existing["repo_url"] = repo_url
    index[doc_id] = existing


def _github_api_contents(owner: str, repo: str, path: str = "", branch: str = "main") -> list:
    query = urllib.parse.urlencode({"ref": branch}) if branch else ""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    if query:
        url = f"{url}?{query}"
    payload = _fetch_json(url)
    if isinstance(payload, dict) and payload.get("error") == "not-found":
        return []
    return payload if isinstance(payload, list) else []


def _github_markdown_file_paths(owner: str, repo: str, path: str, branch: str = "main") -> List[str]:
    markdown_files: List[str] = []
    for item in _github_api_contents(owner, repo, path=path, branch=branch):
        if not isinstance(item, dict):
            continue
        item_type = item.get("type")
        item_path = item.get("path", "")
        if item_type == "file" and str(item_path).lower().endswith(".md"):
            markdown_files.append(item_path)
        elif item_type == "dir":
            markdown_files.extend(_github_markdown_file_paths(owner, repo, item_path, branch=branch))
    return markdown_files


def _fetch_markdown_from_github(owner: str, repo: str, branch: str, file_path: str) -> str:
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"
    return _decode_html(_fetch(raw_url))


def _resolve_local_repo_path(repo_slug: str) -> Optional[Path]:
    local_aliases = {
        "retail-operations": "retail-operation",
    }
    candidate_slug = local_aliases.get(repo_slug, repo_slug)
    fallback_dirs = [
        PROJECT_ROOT.parent / "project_potfolio",
        PROJECT_ROOT.parent / "project_portfolio-git-backup",
    ]
    for directory in fallback_dirs:
        repo_path = directory / candidate_slug
        if repo_path.exists():
            return repo_path
    return None


def _github_local_fallback(repo_slug: str, file_path: str) -> Optional[str]:
    # Controlled fallback from local portfolio copies for non-public/private repos.
    repo_path = _resolve_local_repo_path(repo_slug)
    if repo_path is None:
        return None

    candidate_path = repo_path / file_path
    if candidate_path.exists():
        return candidate_path.read_text(encoding="utf-8")
    return None


def _github_local_markdown_files(repo_slug: str) -> List[str]:
    repo_path = _resolve_local_repo_path(repo_slug)
    if repo_path is None:
        return []

    local_docs = [repo_path / "README.md"]
    docs_dir = repo_path / "docs"
    markdown_paths: List[str] = []
    if docs_dir.exists():
        for path in docs_dir.rglob("*.md"):
            if path.is_file():
                markdown_paths.append(str(path.relative_to(repo_path)).replace("\\", "/"))

    for file_path in local_docs:
        if file_path.exists():
            markdown_paths.append(str(file_path.relative_to(repo_path)).replace("\\", "/"))
    return sorted(set(markdown_paths))


def _ingest_website(
    index: dict,
    normalize_html: Callable[[str, str], str],
) -> List[str]:
    results = []
    rendered_pages = _render_website_pages(WEBSITE_PAGE_ORDER)

    for page in WEBSITE_PAGE_ORDER:
        slug = page["slug"]
        path = page["path"]
        source_url = f"{WEBSITE_ROOT}{path}"
        raw_path = RAW_ROOT / "website" / slug / "page.html"
        normalized_path = PROCESSED_ROOT / "website" / f"{slug}.md"
        doc_id = f"website::{slug}"
        try:
            if path in rendered_pages:
                html, page_title = rendered_pages[path]
            else:
                html_bytes = _fetch(source_url)
                html = _decode_html(html_bytes)
                page_title = _extract_html_title(html)

            title = page["title"] if page.get("title") else page_title
            normalized = normalize_html(html, source_url)
            raw_sha = _sha256_hex(html.encode("utf-8"))
            normalized_sha = _sha256_hex(normalized.encode("utf-8"))
            _write_text(raw_path, html)
            _write_text(normalized_path, normalized)
            _upsert_document(
                index,
                DocumentSource(
                    document_id=doc_id,
                    source_type="website",
                    source_url=source_url,
                    raw_path=str(raw_path),
                    normalized_path=str(normalized_path),
                    title=title,
                    raw_sha256=raw_sha,
                    normalized_sha256=normalized_sha,
                    last_checked_at=_now_utc(),
                    last_changed_at=_now_utc(),
                    project_name=None,
                    repo_url=None,
                    file_path=path,
                    status="ingested",
                ),
            )
            results.append(doc_id)
        except Exception as exc:
            _upsert_failed(index, doc_id=doc_id, source_type="website", source_url=source_url, title=page["title"], details=str(exc))
            continue
    return results


def _ingest_project_docs(
    index: dict,
    markdown_normalizer: Callable[[str], str] = _normalize_markdown_content,
) -> List[str]:
    results = []
    for project in SHOWCASED_PROJECTS:
        owner = project["owner"]
        repo = project["repo"]
        repo_url = project["repo_url"]
        project_slug = repo
        project_name = project["name"]

        try:
            local_markdown_paths = _github_local_markdown_files(repo)
            if local_markdown_paths:
                markdown_paths = list(local_markdown_paths)
            else:
                discovered_docs = _github_markdown_file_paths(owner, repo, "docs", branch=project["branch"])
                markdown_paths = ["README.md"]
                markdown_paths.extend(discovered_docs)
            for file_path in markdown_paths:
                raw_content = _github_local_fallback(repo, file_path)
                try:
                    if raw_content is None:
                        raw_content = _fetch_markdown_from_github(owner, repo, project["branch"], file_path)
                except IngestionError:
                    fallback_raw = _github_local_fallback(repo, file_path)
                    if fallback_raw is not None:
                        raw_content = fallback_raw
                if raw_content is None:
                    continue

                doc_id = f"project::{project_slug}::{file_path}"
                normalized = markdown_normalizer(raw_content)
                raw_sha = _sha256_hex(raw_content.encode("utf-8"))
                normalized_sha = _sha256_hex(normalized.encode("utf-8"))
                raw_path = RAW_ROOT / "projects" / project_slug / file_path
                normalized_path = PROCESSED_ROOT / "projects" / project_slug / f"{Path(file_path).with_suffix('.md')}"
                _write_text(raw_path, raw_content.strip() + "\n")
                _write_text(normalized_path, normalized)
                _upsert_document(
                    index,
                    DocumentSource(
                        document_id=doc_id,
                        source_type="project",
                        source_url=repo_url,
                        raw_path=str(raw_path),
                        normalized_path=str(normalized_path),
                        title=project_name,
                        raw_sha256=raw_sha,
                        normalized_sha256=normalized_sha,
                        last_checked_at=_now_utc(),
                        last_changed_at=_now_utc(),
                        repo_url=repo_url,
                        file_path=file_path,
                        project_name=project_name,
                        status="ingested",
                    ),
                )
                results.append(doc_id)
        except Exception as exc:
            _upsert_failed(
                index,
                doc_id=f"project::{project_slug}::README.md",
                source_type="project",
                source_url=repo_url,
                title=project_name,
                details=str(exc),
                repo_url=repo_url,
            )
            continue
    return results


def _ingest_career_profile(
    index: dict,
    markdown_normalizer: Callable[[str], str] = _normalize_markdown_content,
) -> Optional[str]:
    career_file = RAW_ROOT / "jose_claudio_career_knowledge_base.md"
    if not career_file.exists():
        return None

    raw_content = career_file.read_text(encoding="utf-8")
    doc_id = "career::knowledge_base"
    normalized = markdown_normalizer(raw_content)
    raw_sha = _sha256_hex(raw_content.encode("utf-8"))
    normalized_sha = _sha256_hex(normalized.encode("utf-8"))
    normalized_path = PROCESSED_ROOT / "career" / "jose_claudio_career_knowledge_base.md"
    _write_text(normalized_path, normalized)
    _upsert_document(
        index,
        DocumentSource(
            document_id=doc_id,
            source_type="career_profile",
            source_url="local::knowledge/raw/jose_claudio_career_knowledge_base.md",
            raw_path=str(career_file),
            normalized_path=str(normalized_path),
            title="Jose Claudio — Career & Portfolio Knowledge Base",
            raw_sha256=raw_sha,
            normalized_sha256=normalized_sha,
            last_checked_at=_now_utc(),
            last_changed_at=_now_utc(),
            status="ingested",
        ),
    )
    return doc_id


def ingest_all_sources() -> dict:
    """Run ingestion for accepted website pages, showcased project docs, and career knowledge base."""
    index = _load_state()
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    api_token = os.environ.get("CLOUDFLARE_AI_API_TOKEN")

    def _normalize_html(html: str, source_url: str) -> str:
        return _cloudflare_to_markdown(html, source_url, account_id=account_id, api_token=api_token)

    website_ingested = _ingest_website(index, normalize_html=_normalize_html)
    project_ingested = _ingest_project_docs(index)
    career_ingested = _ingest_career_profile(index)

    _save_state(index)
    return {
        "website_count": len(website_ingested),
        "project_count": len(project_ingested),
        "career_count": 1 if career_ingested else 0,
        "document_count": len(index),
    }


def preview_ingest_plan() -> dict:
    return {
        "website_pages": [
            {
                "path": page["path"],
                "slug": page["slug"],
                "title": page["title"],
            }
            for page in WEBSITE_PAGE_ORDER
        ],
        "project_repos": [
            {
                "name": project["name"],
                "repo": project["repo_url"],
            }
            for project in SHOWCASED_PROJECTS
        ],
        "normalized_schema_fields": [
            "source_type",
            "source_url",
            "title",
            "raw_path",
            "normalized_path",
            "raw_sha256",
            "normalized_sha256",
            "last_checked_at",
            "last_changed_at",
            "repo_url",
            "file_path",
            "project_name",
            "status",
        ],
        "idempotent": True,
        "hash_over": ["normalized_content"],
    }
