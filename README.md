# RAG-Assistant

I built this project to understand how RAG works beyond simply calling an LLM with extra context. Starting with public information from my portfolio, I created an ingestion and structure-aware chunking pipeline, then added embeddings, semantic retrieval, grounding, citations, and evaluation. The goal was to understand where retrieval quality comes from, what fails, and how the system behaves when the available evidence is incomplete.

This is a **portfolio learning showcase**, not an enterprise platform.

## Live surfaces

- Portfolio discovery assistant: [joseoclaudio.com/ask](https://joseoclaudio.com/ask)
- Technical RAG case study: [Interactive RAG showcase](https://joseoclaudio.com/projects/interactive-rag)
- Credit-risk project: [Credit Risk & Portfolio Expected Loss](https://joseoclaudio.com/projects/credit-risk-pd-model)
- Interactive credit-risk dashboard: [Expected loss, portfolio risk, simulation, stress, thresholds, and monitoring](https://joseoclaudio.com/projects/credit-risk-pd-model/dashboard)

The assistant synthesizes grounded answers across skills, experience, projects, and methods, then returns clickable Explore-further links. The case-study page documents retrieval, chunking, evaluation, and grounding.

## Included project evidence

The corpus includes the **Credit Risk & Portfolio Expected Loss Analytics** project, not only the earlier probability-of-default work. Its sources cover out-of-time PD evaluation and calibration, LGD and EAD assumptions, account- and portfolio-level expected loss, concentration, stress sensitivities, Monte Carlo loss distributions, approval-threshold tradeoffs, and monitoring. The linked dashboard provides an interactive presentation of those results.

## Architecture

```
Website + GitHub docs + Career KB
        ↓  ingest / normalize / SHA-256 idempotency
StructureAwareChunker → knowledge/processed/chunks/chunks.jsonl
        ↓  embed (@cf/baai/bge-base-en-v1.5 by default)
Local numpy index (embeddings.npz + meta.json)
        ↓  query embed → cosine top-k → light dedupe
Context assembly (provenance + budget)
        ↓  grounded generation
Cited answer  or  explicit abstention
```

### Why this stack

| Choice | Reason |
| --- | --- |
| Reuse existing Stage 1–2 ingest/chunk | Already solid; no rewrite without eval evidence |
| Cloudflare BGE embeddings | Low cost, existing Cloudflare credentials, 768-d, fine for 154 chunks |
| Numpy / Worker cosine index | Tiny corpus; transparent; no Pinecone/Qdrant ops |
| No reranking (yet) | Baseline eval hit **100%** source + fact rates |
| Cloudflare Llama generation (default) | Gemini prepaid credits were depleted; Gemini still supported via env. Live model: `@cf/meta/llama-3.3-70b-instruct-fp8-fast` |
| Thin Worker + FastAPI | Demo surface only; keys stay server-side |

## Corpus

- 26 documents (12 website, 13 project, 1 career knowledge base)
- 153 structure-aware chunks
- Artifact: `knowledge/processed/chunks/chunks.jsonl`

## Commands

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env   # add CLOUDFLARE_* (and optional GEMINI_API_KEY)

python -m rag_assistant.main plan
python -m rag_assistant.main ingest
python -m rag_assistant.main chunk
python -m rag_assistant.main embed
python -m rag_assistant.main retrieve "Where does Jose work?"
python -m rag_assistant.main ask "Where does Jose work?"
python -m rag_assistant.main eval
python -m rag_assistant.main export-worker
python -m rag_assistant.main serve 8080
```

Optional SPA ingest browser: `pip install -e ".[ingest-spa]"` then install Chromium for Playwright.

### Provider switches

```bash
RAG_EMBED_PROVIDER=cloudflare|gemini
RAG_GENERATE_PROVIDER=cloudflare|gemini
```

Defaults are `cloudflare`. If `RAG_GENERATE_PROVIDER=gemini` and Gemini fails (e.g. credits), generation falls back to Cloudflare.

## Evaluation

26 questions in `evaluation/questions.json`.

Latest baseline (`evaluation/results.json`):

- Answerable source hit rate: **1.0**
- Required-fact hit rate: **1.0**
- Both: **1.0**
- Reranking: **not added** (no ranking failures observed)

## API

Local FastAPI:

- `GET /health`
- `POST /api/ask` `{ "question": "...", "top_k": 5 }`

Deployed Worker (portfolio):

- `GET /api/rag/health`
- `POST /api/rag/ask`

Rate limit: ~8 requests / IP / minute (demo protection).

## Tests

Focused suite only:

```bash
python -m unittest tests.test_ingestion tests.test_chunking tests.test_retrieval -v
```

The evaluation dataset is the main quality signal for retrieval.

## Deployment notes

1. Build embeddings + export Worker index from this repo.
2. Copy `deploy/worker_index.json` → portfolio `worker/src/worker_index.json`.
3. Deploy portfolio Worker with Workers AI binding (`wrangler.jsonc` → `ai.binding = "AI"`).
4. Portfolio UI calls `/api/rag/ask`.

Optional container API: see `Dockerfile` (expects prebuilt `knowledge/processed/vectors`).

## Repository layout

```
src/rag_assistant/
  ingestion/     # Stage 1 (existing)
  chunking/      # Stage 2 (existing)
  embeddings.py  # Stage 3
  store.py       # numpy vector store
  retrieval.py   # Stage 4
  eval_runner.py # Stage 5
  context.py     # Stage 6
  ask.py         # Stage 7
  api.py         # Stage 8
knowledge/processed/
evaluation/
deploy/
```

## Limitations

- Allowlisted public sources only
- Vanilla vector retrieval (no hybrid search yet)
- Public demo is rate-limited
- Not a production support bot

## Next experiments

- Hybrid search
- Metadata filters
- Query rewriting
- Alternative embeddings / chunk budgets
- Gemini generation when billing credits are available
