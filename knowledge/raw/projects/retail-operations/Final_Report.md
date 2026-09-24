# Final Report — Retail Demand Forecasting

## Executive Summary

This project forecasts daily point-of-sale demand for the M5 `FOODS`,
`HOBBIES`, and `HOUSEHOLD` categories. Models are compared with expanding,
calendar-aligned validation and then evaluated once on an untouched test year.

Every evaluated alternative improved on the Naive benchmark. The
validation-selected models produced test WAPE between 8.31% and 10.22%, but the
results also showed that additional model complexity was not consistently more
valuable.

The project then extends forecasting into controlled risk analysis. Validation
forecast errors calibrate historical safety buffers, the final test period
evaluates those buffers, and Monte Carlo paths examine uncertainty. This
extension illustrates inventory and service tradeoffs; it does not reproduce
Walmart's operations or recommend a production policy.

## Business Questions

1. How accurately can historical sales forecast future category demand?
2. Do statistical and machine-learning models improve on simple baselines?
3. Do forecast errors show consistent direction or timing?
4. How do historical buffers change service and inventory exposure?
5. Do those tradeoffs remain similar across alternative demand paths?

## Data and Method

The analysis uses M5 item-store-day sales, calendar events, and selling prices.
Forecasting data is aggregated to one row per category and date:

```text
ds | cat_id | y
```

Only `FOODS`, `HOBBIES`, and `HOUSEHOLD` are modeled.

### Chronological Split

| Period | Dates |
| --- | --- |
| Train | 2011-01-29 to 2014-06-20 |
| Validation | 2014-06-21 to 2015-06-20 |
| Test | 2015-06-21 to 2016-06-19 |

Validation uses 13 expanding windows. Every model is refitted using only the
history available before its forecast window. Lag and rolling features use
prior observations, and multi-step feature-based forecasts are recursive.

WAPE is the primary business-facing metric. MAE and RMSE provide supporting
error measures.

### Models

- Naive
- Seasonal Naive
- 7-Day Simple Moving Average
- Exponential Smoothing
- Linear Regression
- Prophet
- XGBoost

Models are selected by validation performance only. The selected model for each
category is refitted on train plus validation and evaluated once on test data.

## Forecasting Results

### Validation Selection

| Category | Selected model | Validation WAPE | Test WAPE |
| --- | --- | ---: | ---: |
| FOODS | XGBoost Faster | 6.99% | 10.22% |
| HOBBIES | Linear Regression (Full) | 6.50% | 8.78% |
| HOUSEHOLD | Prophet Flexible | 6.88% | 8.31% |

Test errors were higher than validation errors, which reinforces the need for a
separate final period. The lowest observed test model differed from the selected
model for `HOBBIES` and `HOUSEHOLD`; those observations were not used to revise
the earlier selection.

### Practical Interpretation

| Category | Interpretation |
| --- | --- |
| FOODS | XGBoost was strongest, but ETS remained close enough to be a credible simpler option. |
| HOBBIES | Several models were close, so additional complexity offered limited value. |
| HOUSEHOLD | Linear Regression had the lowest observed test WAPE, showing that complexity was not automatically better. |

The main forecasting conclusion is category-specific: choose complexity only
when its incremental accuracy justifies the maintenance cost.

## Forecast Error and Risk

For each day:

```text
residual = actual - forecast
```

A positive residual is an under-forecast; a negative residual is an
over-forecast. These are forecast-error exposures, not observed stockouts or
inventory positions.

Final-test residuals showed that `FOODS` and `HOBBIES` under-forecast more often,
while `HOUSEHOLD` tended to over-forecast. Weekend under-forecast rates were
also elevated. This means one uniform risk adjustment would not fit all three
categories.

## Buffer Calibration

Historical buffers are calculated only from the out-of-sample validation
residuals. Positive cumulative errors are measured across hypothetical 7-, 14-,
21-, and 28-day lead times, and p90, p95, and p98 quantiles are retained.

Validation-calibrated 14-day buffers were:

| Category | p90 | p95 | p98 |
| --- | ---: | ---: | ---: |
| FOODS | 33,496 | 43,550 | 49,009 |
| HOBBIES | 2,798 | 3,278 | 3,738 |
| HOUSEHOLD | 8,378 | 10,087 | 12,881 |

The buffers are sample estimates. They are not guaranteed service levels or
Walmart operating parameters.

## Controlled Inventory Sensitivity

Notebook 09 evaluates the validation-calibrated buffers on the separate test
period. The deliberately simple policy assumes:

- daily inventory review
- deterministic hypothetical lead time
- lost sales when demand exceeds available inventory
- order-up-to future point forecasts plus safety stock
- no supplier, case-pack, capacity, cost, or backorder constraints

### Final-Test Results at 14 Days

| Category | Policy | Fill rate | Stockout days | Lost units | Average inventory |
| --- | --- | ---: | ---: | ---: | ---: |
| FOODS | none | 94.30% | 166 | 554,257 | 12,256 |
| FOODS | p95 | 99.07% | 25 | 90,889 | 38,622 |
| HOBBIES | none | 93.36% | 214 | 95,605 | 1,190 |
| HOBBIES | p95 | 97.55% | 94 | 35,218 | 2,183 |
| HOUSEHOLD | none | 99.56% | 32 | 15,626 | 8,126 |
| HOUSEHOLD | p95 | 100.00% | 0 | 0 | 17,614 |

The validation-calibrated p95 buffer improved test-period service for all three
categories, but higher service required more average inventory. The improvement
was largest for `FOODS`; `HOBBIES` remained more exposed than the other
categories after buffering.

Longer lead times generally required more inventory protection. Demand stress
also had a large effect: at +20% demand, p95 fill rates fell to 89.05% for
`FOODS`, 83.13% for `HOBBIES`, and 92.50% for `HOUSEHOLD`.

## Monte Carlo Uncertainty

Validation residuals showed meaningful serial dependence. ACF and Ljung-Box
diagnostics therefore supported sampling seven-day blocks instead of individual
days.

Two thousand block-bootstrap residual paths were added to the fixed final-test
forecast. The same simulated demand path was used for every policy, allowing
paired comparisons.

### Forecast-Bias Uncertainty

| Category | Validation mean residual | 95% block-bootstrap interval |
| --- | ---: | --- |
| FOODS | 564 | [181, 941] |
| HOBBIES | 40 | [4, 81] |
| HOUSEHOLD | 261 | [164, 376] |

All three intervals were above zero during validation, although their magnitude
differed. This describes the historical validation period and does not guarantee
future bias.

### Simulated Policy Results

| Category | Policy | Mean fill rate | Mean inventory | CVaR95 lost units |
| --- | --- | ---: | ---: | ---: |
| FOODS | p90 | 99.81% | 32,570 | 57,421 |
| FOODS | p95 | 99.95% | 42,089 | 25,839 |
| FOODS | p98 | 99.98% | 47,449 | 16,186 |
| HOBBIES | p90 | 99.82% | 3,256 | 5,961 |
| HOBBIES | p95 | 99.92% | 3,685 | 3,467 |
| HOBBIES | p98 | 99.97% | 4,119 | 1,946 |
| HOUSEHOLD | p90 | 99.64% | 7,618 | 27,870 |
| HOUSEHOLD | p95 | 99.84% | 9,038 | 15,859 |
| HOUSEHOLD | p98 | 99.97% | 11,642 | 5,655 |

Moving from p90 to p95 improved mean fill rate more than moving from p95 to p98
for every category. The p95-to-p98 step still reduced tail exposure, showing why
average service and downside risk can support different decisions.

No buffer is labeled optimal. The project does not have the cost or service
information required for that conclusion.

## Conclusions

1. Historical demand supports useful daily category forecasts.
2. More complex models were not consistently better than simpler alternatives.
3. Validation and test separation prevented model selection from being revised after test results were visible.
4. Validation residuals could also calibrate historical buffers without using test outcomes.
5. Those buffers improved service on the independent test period, with a clear inventory tradeoff.
6. Monte Carlo analysis showed that larger buffers reduced average and tail shortfalls, but with diminishing average-service gains.

## Limitations

- The analysis covers only three aggregate categories.
- The test period is one historical year.
- M5 does not include complete inventory positions or replenishment records.
- Lead times, starting inventory, ordering mechanics, and lost sales are hypothetical.
- No margin, holding cost, stockout cost, supplier constraint, or service target is available.
- Block-bootstrap paths preserve local dependence but do not model structural regime change.
- Results do not establish causal effects or provide Walmart inventory recommendations.

The project is best interpreted as a forecasting portfolio with a controlled
decision-sensitivity extension: rigorous enough to show how forecast errors
matter, but intentionally modest about what the available data can prove.
