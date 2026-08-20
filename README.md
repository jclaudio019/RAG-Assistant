# RAG-Assistant

A public portfolio assistant project powered by retrieval-augmented generation (RAG).

## Goal

This project will build an assistant that answers questions about my experience, projects, and technical work using grounded sources:

- Resume / Career Profile
- Personal website
- GitHub repositories

The assistant should always prioritize accuracy and cite where answers come from across these sources.

## Initial Setup

This repository is intentionally minimal to start work quickly:

- `src/rag_assistant/` contains the project source package.
- `README.md` captures the project purpose and scope.
- `pyproject.toml` defines package metadata.

## Status

Initial scaffold created on 2026-08-19.

## Ingestion scope (implemented)

- Website pages ingested from `https://joseoclaudio.com`:
  - `/`
  - `/about`
  - `/projects`
  - `/projects/retail-demand-forecasting`
  - `/projects/credit-risk-pd-model`
  - `/projects/retail-allocation-simulator`
  - `/projects/time-series-analysis-r`
  - `/projects/black-scholes-options-modeling`
  - `/projects/backtesting-system`
  - `/projects/warehouse-club-market-expansion`
  - `/experience`
  - `/skills`
- `/contact` is intentionally excluded.
- Canonical career content is in `knowledge/raw/jose_claudio_career_knowledge_base.md`.

### GitHub repositories ingested (showcase only)

- `https://github.com/jclaudio019/retail-operations`
- `https://github.com/jclaudio019/credit_risk`
- `https://github.com/jclaudio019/retail-allocation-simulator`
- `https://github.com/jclaudio019/time_series_analysis`
- `https://github.com/jclaudio019/black-scholes-options-modeling`
- `https://github.com/jclaudio019/backtesting-system`
- `https://github.com/jclaudio019/warehouse-club-market-expansion-strategy`

## Commands

- `python -m rag_assistant.main plan` shows the planned ingestion set.
- `python -m rag_assistant.main ingest` runs website + project + career profile ingestion.
- `python -m rag_assistant.main chunk` runs structure-aware contextual chunking and generates chunk reports.

## Storage model

- Raw website HTML: `knowledge/raw/website/<slug>/page.html`
- Processed website Markdown: `knowledge/processed/documents/website/<slug>.md`
- Raw project docs: `knowledge/raw/projects/<repo>/<file>`
- Processed project docs: `knowledge/processed/documents/projects/<repo>/<file>`
- Raw career profile: `knowledge/raw/jose_claudio_career_knowledge_base.md`
- Processed career profile: `knowledge/processed/documents/career/jose_claudio_career_knowledge_base.md`
- Current document states: `knowledge/processed/documents/index.json`
- Retrieval-ready chunks: `knowledge/processed/chunks/chunks.jsonl`
- Chunk audit report: `knowledge/processed/chunks/chunk_report.md`

## Notes

- HTML pages are normalized through Cloudflare toMarkdown conversion.
- GitHub Markdown documents are normalized through deterministic cleanup validation.
- Ingestion is idempotent using SHA-256 hashes over raw and normalized content.
- Chunking preserves markdown heading hierarchy (`heading_path`, `section`, `parent_section`), embeds document provenance, and applies forced overlap only when subdividing oversized sections.
