---
description: Built a leakage-aware demand forecasting workflow, then tested how forecast uncertainty changes service and inventory exposure under controlled policy scenarios.
---

[Skip to main content](#main-content)

[ All Case Studies](/projects)

02 — Forecasting

# Retail Demand Forecasting

Built a leakage-aware demand forecasting workflow, then tested how forecast uncertainty changes service and inventory exposure under controlled policy scenarios.

[ View on GitHub](https://github.com/jclaudio019/retail-operations)

Validation-selected test WAPELower is better

FOODS10.22%

HOBBIES8.78%

HOUSEHOLD8.31%

Forecast risk & inventory sensitivity

From demand forecast to decision tradeoff

Validation-selected forecast accuracy for FOODS, HOBBIES, and HOUSEHOLD, kept separate from post-test model comparisons.

10.22%

FOODS test WAPE\*

94.30 → 99.07%

FOODS fill rate\*\*

2,000

Monte Carlo paths

\*Validation-selected XGBoost model on the untouched test year. \*\*Controlled 14-day simulation comparing no buffer with a validation-calibrated p95 buffer; not a production recommendation.

## Business Problem

Retail teams need reliable daily demand forecasts, but point accuracy alone does not show what happens when demand exceeds the forecast or when a buffer is too conservative. The project asks both which models generalize and how forecast uncertainty changes service and inventory exposure under controlled assumptions.

## Solution

I forecast daily unit sales for FOODS, HOBBIES, and HOUSEHOLD at the category level. This keeps weekly and holiday patterns visible without adding store-item allocation complexity.

I compared simple baselines, linear regression, Prophet, and XGBoost. Models were selected through expanding-window validation and evaluated once on a separate 365-day test period.

I analyzed out-of-sample residuals, calibrated historical buffers from validation only, and evaluated simple order-up-to policies once on the untouched test period.

A block-bootstrap Monte Carlo extension then compared service, average inventory, and tail lost-unit risk across p90, p95, and p98 buffers. These are controlled sensitivity scenarios, not a reconstruction of Walmart's replenishment system.

## Dataset

The M5 Forecasting dataset (Walmart daily unit sales) was aggregated to one daily observation per category (ds | cat\_id | y). Chronological split: train 2011-01-29 to 2014-06-20, validation 2014-06-21 to 2015-06-20, and test 2015-06-21 to 2016-06-19\. Validation used 13 calendar-aligned expanding windows. Christmas Day demand falls to zero or near zero and was retained as a known calendar effect. Inventory buffers were calibrated from validation residuals; final policy comparisons used the untouched test period.

## Methodology

I compared baselines, statistical models, and machine-learning models across 13 expanding validation windows; evaluated the selected model once on a 365-day test period; then connected residual risk to controlled inventory-policy and Monte Carlo sensitivity analyses.

Step-by-step method · 9 steps

* 01Prepared and validated the analytical data, then explored weekly seasonality, category behavior, and calendar effects — including the Friday–Sunday lift and Christmas closures.
* 02Established Naive, Seasonal Naive, 7-day SMA, and ETS baselines before comparing more complex models.
* 03Built Linear Regression with lag, rolling, trend, calendar, and Christmas features (full and reduced versions via permutation importance) to keep an interpretable option in the comparison.
* 04Tested Prophet with weekly/yearly seasonality and Christmas as a holiday, plus XGBoost on the shared feature set with small, pre-specified configurations — not an exhaustive hyperparameter search.
* 05Compared models across 13 expanding monthly validation windows with identical dates, horizons, and metrics (WAPE primary; MAE and RMSE also tracked).
* 06Froze validation-selected models per category, then evaluated every pre-specified model once on the untouched 365-day test year — with no post-test tuning.
* 07Measured the direction and timing of forecast errors, then calibrated p90, p95, and p98 buffers from out-of-sample validation residuals only.
* 08Evaluated no-buffer and buffered 14-day order-up-to scenarios on the untouched test year using fill rate, average inventory, lost units, and excess units.
* 09Ran 2,000 block-bootstrap Monte Carlo paths per category and policy to quantify service, inventory, and tail lost-unit tradeoffs under serially dependent forecast error.

## Findings

Validation selected XGBoost Faster for FOODS, Linear Regression for HOBBIES, and Prophet Flexible for HOUSEHOLD; their untouched-test WAPE was 10.22%, 8.78%, and 8.31%. The policy extension shows the operational tradeoff clearly: for FOODS, a validation-calibrated p95 buffer raised test fill rate from 94.30% to 99.07% while average inventory increased from 12,256 to 38,622 units. Monte Carlo results preserve the same pattern across uncertainty paths: higher buffers improve service and reduce tail lost units, but require more inventory.

10.22%

FOODS test WAPE

Validation-selected model

94.30 → 99.07%

FOODS fill rate

No buffer → p95 buffer

2,000

Monte Carlo paths

Per category and policy

FOODSHOBBIESHOUSEHOLD

Selected model vs baseline

FOODS · XGBoost Faster was selected on validation (6.99% WAPE), then scored once on the untouched test year. Lower is better.

0%5%10%15%20%NaiveXGBoost Faster

When the model under-forecast

FOODS · share of test days with actual demand above the forecast, grouped by weekday. This is diagnostic evidence, not a service target.

SunMonTueWedThuFriSat0%25%50%75%100%

Controlled policy comparison

FOODS · 14-day order-up-to simulation on the untouched test period. Buffers were calibrated only from validation residuals.

No bufferp95 buffer90%93%96%100%010,00020,00030,00040,000

* Average inventory
* Fill rate (%)

Uncertainty tradeoff

FOODS · 2,000 block-bootstrap paths per policy. Higher buffers improve service and reduce tail lost units while increasing inventory.

p90p95p98015,00030,00045,00060,00099%99.25%99.5%99.75%100%

* Average inventory
* Tail lost units (CVaR95)
* Mean fill rate (%)

The inventory analysis is a controlled sensitivity study using hypothetical lead times, buffers, and lost-sales behavior. It illustrates decision tradeoffs; it does not reproduce Walmart's replenishment system or make production inventory recommendations.

## Forecast Risk & Inventory Sensitivity

The extension connects forecast quality to a decision without pretending the available data supports a production replenishment recommendation.

* Model choice remains validation-driven: the lowest observed test score is reported separately and never used to choose the winner.
* Buffers are calibrated from validation residuals, then evaluated once on final test data.
* The Monte Carlo layer preserves forecast-error blocks so uncertainty paths retain short-run dependence instead of treating every day as independent.
* Service gains are shown beside the inventory required to obtain them; no single buffer is presented as universally optimal.

## Business Implications

The project demonstrates a complete analytical chain: validate the demand model, diagnose residual risk, test a transparent policy under fixed assumptions, and quantify uncertainty. The result is decision support rather than a false claim of optimization: stakeholders can see what service improvement costs in additional inventory and where tail risk remains.

## Conclusion

Historical sales can forecast category demand more accurately than simply using recent sales, but the best method depends on the category.

The project compares baseline, statistical, and machine-learning models, evaluates validation-selected models on separate test data, and carries their residual uncertainty into controlled inventory scenarios.

The strongest portfolio lesson is not that one buffer wins. It is that model governance, error diagnosis, policy assumptions, and uncertainty must remain visible from forecast to decision.

## Worth Digging Deeper

* 01Compare historical residual buffers with conformal intervals or forecast quantiles using the same validation-only calibration rule.
* 02Stress-test alternative lead times and review periods instead of treating the illustrative 14-day setting as fixed.
* 03Drill into high-value item groups within HOUSEHOLD (and price-sensitive pockets of HOBBIES) where average selling price makes residual error more expensive.
* 04If unit cost, margin, and holding-cost inputs become available, replace retail-value exposure with a true expected economic-cost objective for model selection.
* 05Extend to SKU-store allocation only when inventory positions, unit economics, substitutions, and operational constraints are available.

## Limitations

* Forecasts are at the daily category level, not SKU-store level.
* Price, promotions, substitutions, stockouts, and inventory availability were not modeled as predictive inputs.
* Lead times, safety buffers, lost-sales behavior, and order-up-to logic are hypothetical analytical assumptions.
* Recursive multi-day forecasts can accumulate error through lag and rolling features.
* The test period is one historical year; demand changes should be monitored on future data.
* The project does not reproduce Walmart's replenishment system or make production purchasing, allocation, or inventory recommendations.

## Technologies

PythonpandasstatsmodelsProphetXGBoostscikit-learn

[Next case studyCredit Risk Decision & Portfolio Analytics](/projects/credit-risk-pd-model)

Ask

99%
