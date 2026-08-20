# Backtesting System Repository Repair Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair and document the two-stage Backtesting System so its public repository is reproducible, internally consistent, and credible to potential employers.

**Architecture:** Preserve the repository's two existing lanes: a historical `backtestlib` package for local historical analysis and a Docker-based paper-trading flow containing QuestDB, FastAPI, one EMA crossover strategy, and an Alpaca trade-update listener. Make the smallest changes needed to fix package imports, Docker service discovery, and the shared strategy-run identifier from run creation through completion and trade-event storage.

**Tech Stack:** Python 3.11, pytest, pandas, FastAPI, Pydantic, requests, Docker Compose, QuestDB, Alpaca paper-trading SDK, Jupyter.

## Global Constraints

- Public wording must say “graduate coursework”; do not add “FM 5151” outside preserved notebook artifacts.
- Describe one EMA crossover strategy only.
- Do not claim profitability, production readiness, live trading, multi-strategy support, or real-money execution.
- Do not place live Alpaca orders or use real credentials during validation.
- Keep `.env` ignored and use empty placeholders or mocks only.
- Do not add dependencies or redesign the repository structure.

---

### Task 1: Repair the historical package imports

**Files:**
- Modify: `backtestlib/tests/test_data.py`
- Modify: `backtestlib/tests/test_backtest.py`
- Modify: `backtestlib/tests/test_portfolio.py`
- Modify: `backtestlib/tests/test_strategy.py`
- Modify: `backtestlib/strategy_testing.ipynb`

**Interfaces:**
- Consumes: the installed package declared as `name = "backtestlib"` in `backtestlib/pyproject.toml`
- Produces: tests and notebook imports that consistently use `import backtestlib` and `import backtestlib.data`

- [ ] **Step 1: Prove the stale import fails in a fresh Python 3.11 environment**

Run:

```bash
python3.11 -m venv /tmp/backtesting-system-backtestlib-venv
/tmp/backtesting-system-backtestlib-venv/bin/pip install -e ./backtestlib pytest
/tmp/backtesting-system-backtestlib-venv/bin/python -c "import backtestlib_; print(backtestlib_.__file__)"
```

Expected: FAIL with `ModuleNotFoundError: No module named 'backtestlib_'`.

- [ ] **Step 2: Replace only the stale package name**

Change executable imports to:

```python
import backtestlib as bt
import backtestlib.data
```

Update the notebook's import cell from `import backtestlib_ as bt` to `import backtestlib as bt`. Remove or correct commented examples containing `backtestlib_` so a repository search has no false instructions.

- [ ] **Step 3: Verify the package resolves inside this repository**

Run:

```bash
cd backtestlib
/tmp/backtesting-system-backtestlib-venv/bin/python -c "from pathlib import Path; import backtestlib; path=Path(backtestlib.__file__).resolve(); root=Path.cwd().resolve(); print(path); assert root in path.parents"
/tmp/backtesting-system-backtestlib-venv/bin/pytest tests -q
cd ..
rg -n "backtestlib_" backtestlib
```

Expected: package path prints under `backtestlib/`, all historical-package tests pass, and `rg` returns no matches.

- [ ] **Step 4: Commit the package repair**

```bash
git add backtestlib/tests backtestlib/strategy_testing.ipynb
git commit -m "Fix historical backtest package imports"
```

### Task 2: Use one strategy-run identifier and the Docker API hostname

**Files:**
- Modify: `paper_trading/test_crossover.py`
- Modify: `paper_trading/crossover.py`
- Modify: `paper_trading/compose.yml`

**Interfaces:**
- Consumes: `create_client_order_id(strategy_id: str, entry_or_exit) -> str`
- Produces: `post_engine_run(strategy_id: str, start_time: datetime, initial_capital: float)`, `run_strategy_for_day(strategy_id: str)`, and `API_URL` derived from `API_HOST`

- [ ] **Step 1: Add failing tests for API discovery and identifier reuse**

Add focused tests to `paper_trading/test_crossover.py`:

```python
def test_api_url_uses_configured_host():
    assert crossover.api_url("api") == "http://api:8000"


def test_post_engine_run_uses_provided_strategy_id(monkeypatch):
    captured = {}

    def fake_post(url, json):
        captured.update(url=url, payload=json)
        return FakeResponse()

    monkeypatch.setattr(crossover.requests, "post", fake_post)
    crossover.post_engine_run("Crossover:run-1", datetime(2024, 12, 10, 9, 30), 1_000_000)

    assert captured["payload"]["strategy_id"] == "Crossover:run-1"
```

Import `datetime` and the `crossover` module, and define the existing minimal `FakeResponse.raise_for_status()` test double in this file.

- [ ] **Step 2: Run the focused tests and confirm the current behavior fails**

Run:

```bash
cd paper_trading
pytest test_crossover.py -q
```

Expected: FAIL because `api_url` does not exist and `post_engine_run` does not accept a strategy identifier.

- [ ] **Step 3: Implement the minimum shared-identifier flow**

In `paper_trading/crossover.py`, use:

```python
def api_url(host=None):
    return f"http://{host or os.environ.get('API_HOST', 'localhost')}:8000"


API_URL = api_url()


def post_engine_run(strategy_id: str, start_time: datetime, initial_capital: float):
    data = {
        "strategy_id": strategy_id,
        "start_time": start_time.isoformat(),
        "initial_capital": initial_capital,
    }
    response = requests.post(f"{API_URL}/engine_run", json=data)
    response.raise_for_status()
```

Change the daily runner and entry point to pass the same value:

```python
def run_strategy_for_day(strategy_id: str):
    ...


def main():
    strategy_id = f"{STRATEGY_NAME}:{uuid4()}"
    start_time = datetime.now()
    post_engine_run(strategy_id, start_time, CAPITAL)
    ...
    run_strategy_for_day(strategy_id)
    ...
    update_engine_run_end_time(strategy_id, datetime.now())
```

Do not generate another identifier inside `run_strategy_for_day`.

- [ ] **Step 4: Give the crossover container the existing API service hostname**

Add this one environment entry to `paper_trading/compose.yml` under `crossover`:

```yaml
      - API_HOST=api
```

- [ ] **Step 5: Run the paper-trading tests**

Run:

```bash
cd paper_trading
pytest test_crossover.py test_listener.py -q
cd ..
```

Expected: all focused tests pass; listener behavior continues to derive `Crossover:run-1` from `Crossover:run-1@ENTRY`.

- [ ] **Step 6: Commit the run-identity repair**

```bash
git add paper_trading/crossover.py paper_trading/compose.yml paper_trading/test_crossover.py
git commit -m "Use one identifier across paper trading runs"
```

### Task 3: Complete an engine run without inserting a second record

**Files:**
- Modify: `paper_trading/models.py`
- Modify: `paper_trading/api.py`
- Modify: `paper_trading/crossover.py`
- Modify: `paper_trading/test_models.py`
- Modify: `paper_trading/test_api.py`
- Modify: `paper_trading/test_crossover.py`

**Interfaces:**
- Consumes: the shared `strategy_id` from Task 2
- Produces: `EngineRunCompletion(end_time: datetime)` and `PATCH /engine_run/{strategy_id}`

- [ ] **Step 1: Add failing completion tests**

Add to `paper_trading/test_models.py`:

```python
def test_engine_run_completion_contains_only_end_time():
    completion = EngineRunCompletion(end_time=datetime(2024, 12, 10, 16, 0))
    assert completion.model_dump(mode="json") == {"end_time": "2024-12-10T16:00:00"}
```

Replace the old completed-insert assertion in `paper_trading/test_api.py` with:

```python
def test_patch_engine_run_updates_matching_strategy(monkeypatch):
    captured = {}

    def fake_get(url, params):
        captured["query"] = params["query"]
        return FakeResponse()

    monkeypatch.setattr(api.requests, "get", fake_get)
    api.patch_engine_run(
        "Crossover:run-1",
        EngineRunCompletion(end_time=datetime(2024, 12, 10, 16, 0)),
    )

    assert "UPDATE engine_runs SET end_time = '2024-12-10T16:00:00'" in captured["query"]
    assert "WHERE strategy_id = 'Crossover:run-1'" in captured["query"]
    assert "INSERT INTO" not in captured["query"]
```

Add to `paper_trading/test_crossover.py`:

```python
def test_completion_patches_same_strategy_id(monkeypatch):
    captured = {}

    def fake_patch(url, json):
        captured.update(url=url, payload=json)
        return FakeResponse()

    monkeypatch.setattr(crossover.requests, "patch", fake_patch)
    crossover.update_engine_run_end_time("Crossover:run-1", datetime(2024, 12, 10, 16, 0))

    assert captured["url"].endswith("/engine_run/Crossover:run-1")
    assert captured["payload"] == {"end_time": "2024-12-10T16:00:00"}
```

- [ ] **Step 2: Run the focused tests and confirm they fail**

Run:

```bash
cd paper_trading
pytest test_models.py test_api.py test_crossover.py -q
```

Expected: FAIL because the completion model and PATCH route do not exist and the client still POSTs.

- [ ] **Step 3: Add the completion model and PATCH route**

In `paper_trading/models.py` add:

```python
class EngineRunCompletion(BaseModel):
    end_time: datetime
```

In `paper_trading/api.py` add:

```python
@app.patch("/engine_run/{strategy_id}")
def patch_engine_run(strategy_id: str, completion: EngineRunCompletion):
    sql = f"""UPDATE engine_runs
    SET end_time = '{completion.end_time.isoformat()}'
    WHERE strategy_id = '{strategy_id}';"""
    try:
        result = requests.get(QUESTDB_SQL, params={"query": sql.replace("\n", "")})
        result.raise_for_status()
    except Exception as exc:
        logger.error(exc)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exc))
```

In `paper_trading/crossover.py`, replace the completion POST with:

```python
data = {"end_time": end_time.isoformat()}
response = requests.patch(f"{API_URL}/engine_run/{strategy_id}", json=data)
```

- [ ] **Step 4: Run the full paper-trading test group**

Run:

```bash
cd paper_trading
pytest -q
cd ..
```

Expected: all paper-trading tests pass without network access or credentials.

- [ ] **Step 5: Commit the completion repair**

```bash
git add paper_trading/models.py paper_trading/api.py paper_trading/crossover.py paper_trading/test_models.py paper_trading/test_api.py paper_trading/test_crossover.py
git commit -m "Update paper trading run completion"
```

### Task 4: Rewrite the public README and verify the repository

**Files:**
- Modify: `README.md`
- Verify: `.gitignore`
- Verify: `.env.example` if present

**Interfaces:**
- Consumes: the repaired historical and paper-trading flows from Tasks 1–3
- Produces: a recruiter-facing README with exact commands, architecture, scope, limitations, and AI-assisted cleanup disclosure

- [ ] **Step 1: Replace the README with the verified two-stage explanation**

Use these sections and facts:

```markdown
# Backtesting System

Two related graduate-coursework assignments that explore how a trading idea moves from historical testing to a small paper-trading event pipeline.

## What the repository demonstrates
- Historical analysis through the local `backtestlib` Python package.
- One EMA crossover strategy connected to Alpaca's paper-trading interface.
- A FastAPI service that writes engine runs and trade events to two QuestDB tables.
- Docker Compose service boundaries and identifier-based event traceability.

## Architecture
### Historical backtesting lane
Notebook → `backtestlib` → strategy and portfolio evaluation

### Paper-trading lane
EMA crossover → Alpaca paper account → trade-update listener → FastAPI → QuestDB

## AI-assisted cleanup
After the coursework, I used AI-assisted development tools to repair package imports, align service configuration, make the run identifier consistent across the paper-trading flow, add focused tests, and rewrite the public documentation. I reviewed and validated the resulting changes.

## Limitations
- Educational system, not a production trading platform or investment recommendation.
- Demonstrates one EMA crossover strategy; it does not establish profitability.
- Paper-trading integration requires the user's own Alpaca paper credentials.
- Automated tests use mocks and do not place orders.
```

Add the exact fresh-environment commands used in Tasks 1 and 3 and a Docker section that starts only QuestDB and the API for validation.

- [ ] **Step 2: Run secret-safe and wording checks**

Run:

```bash
git check-ignore .env
rg -n "FM 5151|profitab|production-ready|live trading|real money" README.md
git grep -nE "AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9_-]{20,}|ALPACA_API_(KEY|SECRET)=.+"
```

Expected: `.env` is ignored; README has no class code or unsupported claims; credential scan returns no matches.

- [ ] **Step 3: Run both test suites in fresh Python 3.11 environments**

Run:

```bash
/tmp/backtesting-system-backtestlib-venv/bin/pytest backtestlib/tests -q
python3.11 -m venv /tmp/backtesting-system-paper-venv
/tmp/backtesting-system-paper-venv/bin/pip install -r paper_trading/requirements.txt
cd paper_trading
/tmp/backtesting-system-paper-venv/bin/pytest -q
cd ..
```

Expected: both suites pass.

- [ ] **Step 4: Smoke-test only QuestDB and FastAPI when Docker is available**

Run:

```bash
cd paper_trading
docker compose up -d questdb api
curl --fail http://localhost:8000/engine_runs
curl --fail -X POST http://localhost:8000/engine_run -H 'Content-Type: application/json' -d '{"strategy_id":"Crossover:smoke-test","start_time":"2024-12-10T09:30:00","initial_capital":1000000}'
curl --fail -X PATCH http://localhost:8000/engine_run/Crossover:smoke-test -H 'Content-Type: application/json' -d '{"end_time":"2024-12-10T16:00:00"}'
curl --fail 'http://localhost:8000/engine_runs?strategy_id=Crossover%3Asmoke-test'
docker compose down
cd ..
```

Expected: the API returns the inserted run with its completion time. Do not start `crossover` or `listener`.

- [ ] **Step 5: Commit the documentation**

```bash
git add README.md
git commit -m "Document Backtesting System architecture"
```

- [ ] **Step 6: Final repository review**

Run:

```bash
git status --short
git log --oneline -5
```

Expected: only intentional files are committed and no credential or environment file is tracked.
