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

## Fresh-environment validation

Run the historical-package checks in a fresh Python 3.11 environment:

```bash
python3.11 -m venv /tmp/backtesting-system-backtestlib-venv
/tmp/backtesting-system-backtestlib-venv/bin/pip install -e ./backtestlib pytest
/tmp/backtesting-system-backtestlib-venv/bin/pytest backtestlib/tests -q
```

Run the paper-trading checks separately. They use mocks and require neither credentials nor a running database:

```bash
python3.11 -m venv /tmp/backtesting-system-paper-venv
/tmp/backtesting-system-paper-venv/bin/pip install -r paper_trading/requirements.txt
cd paper_trading
/tmp/backtesting-system-paper-venv/bin/pytest -q
cd ..
```

## Docker API validation

For the API/database smoke check, create `paper_trading/.env` from `.env.example` with your own Alpaca paper credentials only when running the paper-trading workers. The following validation starts only QuestDB and the API; it does not start `crossover` or `listener`.

If you have a pre-change `hw5_data` volume, this educational project has no migration system. From `paper_trading`, run `docker compose down -v` before the smoke check and then recreate the services with `docker compose up -d questdb api`. The `-v` command permanently deletes all local QuestDB data in that volume, so use it only when that data can be discarded.

```bash
set -euo pipefail
cd paper_trading
trap 'docker compose down' EXIT
docker compose up -d questdb api
python3.11 - <<'PY'
import json
import secrets
import time
import uuid
from datetime import datetime, timedelta, timezone
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

base_url = "http://localhost:8000"


def call(method, path, payload=None):
    body = json.dumps(payload).encode() if payload is not None else None
    request = Request(
        base_url + path,
        data=body,
        headers={"Content-Type": "application/json"},
        method=method,
    )
    with urlopen(request, timeout=5) as response:
        response_body = response.read()
    return json.loads(response_body) if response_body else None


for attempt in range(30):
    try:
        call("GET", "/engine_runs")
        break
    except URLError:
        if attempt == 29:
            raise
        time.sleep(1)

strategy_id = f"Crossover:{secrets.token_hex(6)}"
client_order_id = f"{strategy_id}@{secrets.token_hex(6)}@ENTRY"
execution_id = str(uuid.uuid4())
start = datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0)
end = start + timedelta(minutes=1)
event_time = start + timedelta(seconds=30)
run_payload = {
    "strategy_id": strategy_id,
    "start_time": start.isoformat(),
    "initial_capital": 1000000,
}
completion_payload = {"end_time": end.isoformat()}
trade_payload = {
    "strategy_id": strategy_id,
    "timestamp": event_time.isoformat(),
    "event_type": "FILL",
    "broker": "ALPACA",
    "client_order_id": client_order_id,
    "entry_exit": "ENTRY",
    "direction": "BUY",
    "execution_id": execution_id,
    "last_execution_time": event_time.isoformat(),
    "quantity": 1,
    "average_fill_price": 142.5,
    "total_price": 142.5,
}

call("POST", "/engine_run", run_payload)
call("PATCH", f"/engine_run/{strategy_id}", completion_payload)
call("POST", "/trade_event", trade_payload)
encoded_strategy_id = quote(strategy_id, safe="")
runs = call("GET", f"/engine_runs?strategy_id={encoded_strategy_id}")
events = call("GET", f"/trade_events?strategy_id={encoded_strategy_id}")


def parsed_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)


def assert_fields(actual, expected):
    for field, expected_value in expected.items():
        if field in {"start_time", "end_time", "timestamp", "last_execution_time"}:
            assert actual[field] is not None
            assert parsed_time(actual[field]) == parsed_time(expected_value)
        else:
            assert actual[field] == expected_value


matching_runs = [run for run in runs if run["strategy_id"] == strategy_id]
matching_events = [
    event for event in events if event["client_order_id"] == client_order_id
]
assert len(matching_runs) == 1
assert len(matching_events) == 1
assert_fields(matching_runs[0], run_payload | completion_payload)
assert_fields(matching_events[0], trade_payload)
PY
```

## AI-assisted cleanup

After the coursework, I used AI-assisted development tools to repair package imports, align service configuration, make the run identifier consistent across the paper-trading flow, add focused tests, and rewrite the public documentation. I reviewed and validated the resulting changes.

## Limitations

- This is an educational graduate-coursework project, not a production trading platform or investment recommendation.
- The broker-connected flow uses Alpaca paper trading only.
- It demonstrates one EMA crossover strategy.
- The project provides no evidence of profitability.
- Historical evaluation does not model transaction costs, slippage, or market impact.
- The strategy has no out-of-sample validation or production execution controls.
- The database and API are not publicly deployed.
- No real credentials are tracked in this repository; paper-trading workers require the user's own Alpaca paper credentials.
- Public validation uses mocks and local database/API checks and places no live or paper orders.
- Historical notebook results are illustrative rather than investment evidence.
- QuestDB and FastAPI are intended for local Docker use only.
