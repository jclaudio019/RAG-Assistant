# RAP-Asistamt

A public portfolio assistant project powered by retrieval-augmented generation (RAG).

## Goal

This project will build an assistant that answers questions about my experience, projects, and technical work using grounded sources:

- Resume
- Personal website
- GitHub repositories

The assistant should always prioritize accuracy and cite where answers come from across these sources.

## Initial Setup

This repository is intentionally minimal to start work quickly:

- `src/rap_assistamt/` contains the project source package.
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
- `/resume` is intentionally skipped because canonical career content is in `knowledge/raw/jose_claudio_career_knowledge_base.md`.

### GitHub repositories ingested (showcase only)

- `https://github.com/jclaudio019/retail-operations`
- `https://github.com/jclaudio019/credit_risk`
- `https://github.com/jclaudio019/retail-allocation-simulator`
- `https://github.com/jclaudio019/time_series_analysis`
- `https://github.com/jclaudio019/black-scholes-options-modeling`
- `https://github.com/jclaudio019/backtesting-system`
- `https://github.com/jclaudio019/warehouse-club-market-expansion-strategy`

## Commands

- `python -m rap_assistamt.main plan` shows the planned ingestion set.
- `python -m rap_assistamt.main ingest` runs website + project ingestion.

## Storage model

- Raw website HTML: `knowledge/raw/website/<slug>/page.html`
- Processed website Markdown: `knowledge/processed/documents/website/<slug>.md`
- Raw project docs: `knowledge/raw/projects/<repo>/<file>`
- Processed project docs: `knowledge/processed/documents/projects/<repo>/<file>`
- Current document states: `knowledge/processed/documents/index.json`

## Notes

- HTML pages are normalized through Cloudflare toMarkdown conversion.
- GitHub Markdown documents are normalized through deterministic cleanup validation.
- Ingestion is idempotent using SHA-256 hashes over raw and normalized content.
