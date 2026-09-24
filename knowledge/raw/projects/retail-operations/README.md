# Retail Demand Forecasting

This portfolio project forecasts daily point-of-sale demand for the M5
`FOODS`, `HOBBIES`, and `HOUSEHOLD` categories. It then uses forecast errors in
a limited extension that illustrates inventory sensitivity under controlled,
hypothetical assumptions.

Forecasting is the core of the project. The inventory notebooks do not recreate
Walmart's replenishment system, recommend a production policy, or optimize true
business costs.

## Workflow

| Notebook | Purpose |
| --- | --- |
| `00_data_preparation.ipynb` | Join, validate, and save the daily M5 data. |
| `01_data_exploration.ipynb` | Explore trend, seasonality, events, and outliers. |
| `02_baseline_forecasting.ipynb` | Compare Naive, Seasonal Naive, 7-Day SMA, and ETS. |
| `03_forecast_validation.ipynb` | Run 13 expanding, calendar-aligned validation windows. |
| `04_linear_regression.ipynb` | Evaluate recursive linear-regression forecasts. |
| `05_prophet_model.ipynb` | Evaluate Prophet configurations. |
| `06_xgboost_model.ipynb` | Evaluate recursive XGBoost configurations. |
| `07_model_comparison.ipynb` | Select by validation and evaluate once on test data. |
| `08_inventory_risk_analysis.ipynb` | Analyze errors and calibrate historical buffers. |
| `09_inventory_policy_simulation.ipynb` | Evaluate controlled inventory scenarios on test data. |
| `10_monte_carlo_uncertainty_analysis.ipynb` | Test uncertainty, policy tradeoffs, and tail risk. |

## Data and Validation

Modeling uses one row per category and date:

```text
ds | cat_id | y
```

The chronological split is fixed:

- Train: 2011-01-29 through 2014-06-20
- Validation: 2014-06-21 through 2015-06-20
- Test: 2015-06-21 through 2016-06-19

Models are selected using validation WAPE only. The selected model is then
refitted on train plus validation and evaluated once on the untouched test
period. MAE and RMSE are also reported.

The inventory extension follows the same separation:

- validation residuals calibrate p90, p95, and p98 historical buffers
- final-test demand evaluates the controlled policy scenarios
- validation residual blocks generate Monte Carlo demand paths

No test result is used to select a forecasting model or buffer level.

## Headline Forecast Results

| Category | Validation-selected model | Validation WAPE | Test WAPE |
| --- | --- | ---: | ---: |
| FOODS | XGBoost Faster | 6.99% | 10.22% |
| HOBBIES | Linear Regression (Full) | 6.50% | 8.78% |
| HOUSEHOLD | Prophet Flexible | 6.88% | 8.31% |

More complexity was not always more useful. ETS remained close to XGBoost for
`FOODS`, several models were close for `HOBBIES`, and Linear Regression produced
the lowest observed test WAPE for `HOUSEHOLD`.

## Forecast Risk Extension

The extension uses a simple daily order-up-to simulation with lost sales and
hypothetical 7-, 14-, 21-, and 28-day lead times. At the 14-day setting, the
validation-calibrated p95 buffer produced these final-test results:

| Category | Fill rate | Stockout days | Average on-hand inventory |
| --- | ---: | ---: | ---: |
| FOODS | 99.07% | 25 | 38,622 |
| HOBBIES | 97.55% | 94 | 2,183 |
| HOUSEHOLD | 100.00% | 0 | 17,614 |

Monte Carlo analysis uses 2,000 seven-day block-bootstrap paths. Larger buffers
generally improve service and reduce severe lost-unit outcomes, but they also
increase inventory. The analysis reports this tradeoff rather than declaring an
optimal policy.

## Limitations

- M5 contains sales demand, not complete inventory records.
- Lead times, starting inventory, lost sales, and ordering rules are hypothetical.
- Results are aggregated to category level and may hide store-item behavior.
- No unit cost, margin, holding cost, stockout cost, supplier constraint, or service target is available.
- Historical residuals may not represent future structural changes.

Run notebooks in numerical order. Source data is stored under
`data/m5/datasets/`; derived parquet files are written to `data/processed/` and
are excluded from Git.

See `Final_Report.md` for the detailed analysis and
`PORTFOLIO_PROJECT_SUMMARY.md` for concise portfolio-page content.
