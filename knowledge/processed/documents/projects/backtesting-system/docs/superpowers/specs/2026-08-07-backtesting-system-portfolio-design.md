# Backtesting System Portfolio Design

## Objective

Present Backtesting System to potential employers as a completed, educational systems project. The case study will emphasize historical strategy evaluation, event handling, broker API integration, FastAPI, QuestDB, Docker Compose, and testable service-to-service data flow. It will not use investment returns as evidence of quality.

## Public Positioning

- Approved name: **Backtesting System**.
- Describe the source as two related graduate coursework assignments; omit the course number from the README and portfolio.
- Historical stage: an event-driven Python backtester with data providers, events, strategy callbacks, orders, positions, cash, market value, and a backtest loop.
- Broker-connected stage: one EMA crossover strategy using Alpaca paper trading, trade-update events, FastAPI, QuestDB, and four local Docker Compose services.
- The stages demonstrate related parts of a trading-system workflow but are not one integrated production engine.
- Public validation will use mocks and local database/API checks only. It will not connect to Alpaca or submit orders.

## Repository Repairs

### Historical Backtesting Package

Replace `backtestlib_` imports in `backtestlib/tests/` and `backtestlib/strategy_testing.ipynb` with the public package name `backtestlib`. Do not rename or restructure the package.

Validation must run in a fresh Python 3.11 environment and prove that `backtestlib.__file__` resolves inside this repository at `backtestlib/src/backtestlib` before reporting the expected 10 passing tests.

### Paper-Trading API Address

`paper_trading/crossover.py` will build its API URL from `API_HOST`, defaulting to `localhost` for direct execution. `paper_trading/compose.yml` will set `API_HOST=api` for the crossover service, matching the listener service.

A focused test will verify both the default URL and the environment-derived Docker URL without making a network request.

### Shared Strategy-Run Identifier

Create one identifier at the start of `main()` using `Crossover:<uuid>`. Pass that identifier through:

- the engine-run start request;
- `run_strategy_for_day()`;
- Alpaca client order IDs;
- listener-derived trade events; and
- the engine-run completion request.

The listener will continue deriving `strategy_id` from the portion of `client_order_id` before `@`, so no new database abstraction is required.

### Engine-Run Completion

Add `PATCH /engine_run/{strategy_id}` to the FastAPI service. Its request body contains only `end_time`. The endpoint will execute:

```sql
UPDATE engine_runs
SET end_time = '<ISO timestamp>'
WHERE strategy_id = '<strategy identifier>';
```

`update_engine_run_end_time()` will call this endpoint. A focused test will prove that the same identifier is used, the SQL updates `end_time`, and no second incomplete engine-run insert is made.

### Repository Documentation

The README will explain the two stages, local setup, validated test commands, architecture, AI-assisted post-course cleanup, and limitations. It will state that no real credentials are tracked and that public validation does not place live or paper orders.

## Portfolio Presentation

### Project Order

1. Retail Demand Forecasting
2. Credit Risk Probability of Default
3. Retail Allocation Simulator
4. Time-Series Analysis & Forecasting in R
5. Black-Scholes Options Modeling
6. Backtesting System
7. Warehouse Club Market Expansion — In progress

Warehouse remains last. Existing route slugs and case studies remain unchanged.

### Case-Study Content

The project record will use architecture facts as evidence:

- 1 paper-trading strategy;
- 4 local Docker Compose services;
- 2 QuestDB tables; and
- 2 related graduate coursework assignments.

The case study will include the approved business problem, a two-stage solution, repository data sources, implementation method, findings about system flow rather than performance, business implications, conclusion, limitations, technology tags, GitHub link, and post-course AI-assisted-development disclosure.

### Architecture Component

Add one responsive React/Tailwind component with two labeled lanes and no new dependency:

```text
Historical price provider
  -> Backtest event loop
  -> Strategy callback
  -> Portfolio order
  -> Position and cash update

EMA crossover signal
  -> Alpaca paper order
  -> Alpaca trade-update listener
  -> FastAPI endpoint
  -> QuestDB trade_events table
```

The component will use semantic ordered lists, visible arrows as decoration, high-contrast text, and a mobile layout that stacks each lane vertically without horizontal scrolling.

### Cover Image

Create one dark, purple-accented cover consistent with the existing portfolio. It will visualize two connected lanes: historical market prices moving through an event loop and a paper order moving through an API into a database. It will avoid profit charts, currency gains, trading claims, brokerage logos, and credential-like text.

## Security and Validation

- Keep `.env` ignored and `.env.example` values empty.
- Search tracked files and diffs for Alpaca key or secret material before committing.
- Tests must use explicit placeholders and mocks.
- Backtesting validation: 10 tests in a fresh Python 3.11 environment.
- Paper-trading validation: 5 or more focused tests in a fresh Python 3.11 environment.
- If Docker is available, start only QuestDB and API, insert one sample engine run and trade event, verify both, then stop the services.
- Do not start crossover or listener during public validation.
- Portfolio validation: focused content/order/component tests, full test suite, production build, desktop/mobile browser check, and clean browser console.

## Limitations to Publish

- Educational graduate coursework project.
- Alpaca paper trading only.
- One EMA crossover strategy in the broker-connected flow.
- No evidence of profitability.
- No transaction-cost, slippage, or market-impact model.
- No out-of-sample strategy validation or production execution controls.
- No public database or API deployment.
- No real credentials in the repository.
- No live or paper orders used during public validation.
- Historical notebook results are illustrative rather than investment evidence.
- QuestDB and FastAPI are intended for local Docker use.

## Out of Scope

- Rewriting strategy classes, portfolio accounting, or data-provider architecture.
- Adding strategies to the paper-trading flow.
- Replacing QuestDB, FastAPI, Docker Compose, or the requests-based workflow.
- Building a live portfolio simulator or broker connection on the website.
- Presenting the system as production-ready, profitable, live, or multi-strategy.
