# Retail Demand and POS Forecasting

A portfolio project that forecasts daily point-of-sale demand from the M5
Forecasting dataset. The work is intentionally focused on clear, reproducible,
category-level forecasting—not inventory optimization.

## Scope

The project models daily unit sales (`y`) by calendar date (`ds`) for:

- `FOODS`
- `HOBBIES`
- `HOUSEHOLD`

It covers data preparation, exploratory analysis, baseline and feature-based
forecasting, rolling validation, model comparison, and one final evaluation on
an untouched test period.

Inventory allocation, replenishment recommendations, safety-stock decisions,
purchasing decisions, and distribution optimization are outside this
repository. A future, separate allocation template may consume these forecasts,
but it is not part of this project.

## Business question

> How accurately can historical point-of-sale demand forecast future daily
> category-level unit sales?

The analysis examines trend, weekly seasonality, holidays, events, and the
relative accuracy and stability of several forecasting approaches.

## Dataset

The project uses the M5 Forecasting dataset, which provides Walmart daily sales
history, product and store hierarchy, calendar events, SNAP indicators, and
selling prices. Modeling data is aggregated to one row per category and date:

```text
ds | cat_id | y
```

## Workflow

| Notebook | Purpose |
| --- | --- |
| `00_data_preparation.ipynb` | Load and validate the joined M5 source data. |
| `01_data_exploration.ipynb` | Create category-day views and examine distributions, seasonality, and events. |
| `02_baseline_forecasting.ipynb` | Compare Naive, Seasonal Naive, 7-Day SMA, and ETS on an initial holdout. |
| `03_forecast_validation.ipynb` | Compare baselines with expanding-window, calendar-month validation. |
| `04_linear_regression.ipynb` | Evaluate recursive Linear Regression with time-series and calendar features. |
| `05_prophet_model.ipynb` | Evaluate Prophet with seasonality, holidays, and limited tuning. |
| `06_xgboost_model.ipynb` | Evaluate recursive XGBoost with the shared feature structure. |
| `07_model_comparison.ipynb` | Compare all pre-specified models and evaluate them once on the untouched test set. |
| `Final_Report.md` | Summarize business findings, final test results, trade-offs, and limitations. |

## Validation approach

The data uses a strict chronological split:

```text
Train:      2011-01-29 through 2014-06-20
Validation: 2014-06-21 through 2015-06-20
Test:       2015-06-21 through 2016-06-19
```

Validation uses 13 calendar-aligned, expanding windows across 365 days. Each
model is refitted using only data available before a window and forecasts that
window without using future actuals. Models are selected by validation results,
then evaluated once on the untouched test period.

## Evaluation metrics

- MAE
- RMSE
- WAPE (%)

Models are compared on mean error and stability across validation windows.

## Current status

All notebooks are complete. The final report shows that XGBoost produced the
lowest observed test WAPE for `FOODS`, XGBoost was narrowly lowest for
`HOBBIES`, and Linear Regression was lowest for `HOUSEHOLD`. Model selection
was frozen during validation; the final test table is reported as a transparent,
one-time comparison on the untouched test period.

## Reproducibility

Run the notebooks in numerical order. The M5 source data is stored under
`data/m5/datasets/`, and derived files are written under `data/processed/`.
Those data files are local and intentionally excluded from Git.

## Limitations

- Results are at the category level, not the SKU-store level.
- Forecasting demand does not prescribe inventory or allocation actions.
