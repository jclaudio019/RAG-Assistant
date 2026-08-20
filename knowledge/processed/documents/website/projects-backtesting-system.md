---
description: Portfolio of Jose Claudio, an analytics professional combining forecasting, statistical modeling, automation, finance, and supply-chain decision support.
---

[Skip to main content](#main-content)

[ All Case Studies](/projects)

06 — Financial Systems

# Backtesting System

Connected two graduate coursework assignments into a documented workflow spanning historical backtesting and a small paper-trading event pipeline.

[ View on GitHub](https://github.com/jclaudio019/backtesting-system)

![Backtesting System project overview](/images/backtesting-system-hero.png)

Two analytical lanes connect historical strategy evaluation with a paper-trading event workflow.

1

Strategy demonstrated

4

Docker services

2

QuestDB tables

2

Related coursework assignments

Educational system using one EMA crossover strategy and Alpaca's paper-trading interface; no profitability or live-trading claim.

## Business Problem

A strategy notebook can show historical behavior, but it does not explain how signals, orders, broker updates, and stored events connect in an operating workflow. This project examines both stages while keeping their purposes and limitations clear.

## Solution

The first graduate coursework assignment produced a reusable Python package for loading market data, defining strategies, running historical tests, and reviewing portfolio behavior.

The second assignment extended that learning into a small paper-trading architecture: one EMA crossover strategy sends paper orders through Alpaca, a listener receives broker updates, FastAPI provides a narrow data interface, and QuestDB stores engine runs and trade events.

After the coursework, I used AI-assisted development to repair package imports, align Docker service configuration, make the run identifier consistent across the event flow, add focused tests, and prepare the repository for public review.

## Dataset

The historical notebook requests Yahoo Finance data for AAPL and MSFT for dates from December 1, 2020, through December 1, 2023 via YahooDataProvider; no fixed market-data snapshot is tracked. Retained notebook outputs are illustrative artifacts, not an immutable reproducible dataset. Paper-trading validation uses mocks and sample API records, not orders or credentials.

## Methodology

The case study follows a strategy from historical evaluation into an event-driven paper-trading workflow, with one shared identifier connecting the engine run, client order IDs, broker updates, and stored trade events.

Step-by-step method · 6 steps

* 01Used the local backtestlib package to separate market data, strategy logic, backtest execution, and portfolio evaluation.
* 02Applied one short- and long-period EMA crossover rule in the broker-connected coursework flow.
* 03Separated QuestDB, FastAPI, crossover, and listener responsibilities into four Docker Compose services.
* 04Encoded the strategy-run identifier in client order IDs so listener events can be traced to the matching engine run.
* 05Stored run metadata and trade updates in two QuestDB tables through focused API endpoints.
* 06Validated the repaired paths with isolated unit tests and static Docker Compose/configuration checks. The documented local QuestDB/API smoke procedure remains unverified because Docker was unavailable during final validation.

## Findings

The main result is architectural rather than financial. Historical testing and broker-connected execution answer different questions, and a shared run identifier makes the relationship between strategy activity, order updates, and stored records inspectable.

System architecture

### Historical backtesting

1. Historical price provider
2. Backtest event loop
3. Strategy callback
4. Portfolio order
5. Position and cash update

### Paper-trading event flow

1. EMA crossover
2. Alpaca paper order
3. Trade-update listener
4. FastAPI
5. QuestDB trade\_events table

## Business Implications

The project demonstrates how analytical code can be organized into clearer service boundaries and validation points. That structure makes assumptions and event flow easier to explain, test, and review before considering broader strategy or infrastructure work.

## Conclusion

The completed case study connects two pieces of graduate coursework into one documented view of historical testing and paper-trading system design.

It is an educational architecture demonstration, not evidence of strategy profitability, a production trading platform, or a recommendation to trade.

## Limitations

* This is an educational graduate-coursework project, not a production trading platform or investment recommendation.
* The broker-connected flow uses Alpaca paper trading only.
* It demonstrates one EMA crossover strategy.
* The project provides no evidence of profitability.
* Historical evaluation does not model transaction costs, slippage, or market impact.
* The strategy has no out-of-sample validation or production execution controls.
* The database and API are not publicly deployed.
* No real credentials are tracked; the paper-trading workers require the user's own Alpaca paper credentials.
* Public validation used mocks and sample API records and placed no live or paper orders.
* Historical notebook outputs are illustrative artifacts rather than investment or reproducibility evidence.
* QuestDB and FastAPI are intended for local Docker use only.

## Technologies

PythonFastAPIDockerQuestDBAlpaca

[Next case studyWarehouse Club Market Expansion](/projects/warehouse-club-market-expansion)
