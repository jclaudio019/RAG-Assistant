# Final Report — Retail Demand and POS Forecasting

## Executive summary

Retail teams need a reliable view of expected daily demand before they can plan staffing, inventory reviews, and other downstream operations. Using recent sales alone can miss recurring weekly patterns, changes in demand level, and known calendar disruptions.

This project addresses that forecasting problem for daily point-of-sale unit sales in the `FOODS`, `HOBBIES`, and `HOUSEHOLD` categories. It delivers a leakage-safe category-level demand forecasting process: historical sales are evaluated with expanding-window validation, then pre-specified models are compared once on an untouched 365-day test period.

Every evaluated alternative improved on the Naive benchmark. The best observed test WAPE by category was:

| Category | Best observed test model | Test WAPE | Improvement versus Naive |
|---|---|---:|---:|
| FOODS | XGBoost Faster | 10.22% | 5.88 percentage points |
| HOBBIES | XGBoost Shallow | 8.00% | 9.47 percentage points |
| HOUSEHOLD | Linear Regression (Full) | 7.05% | 12.83 percentage points |

The business takeaway is category-specific: XGBoost achieved the lowest observed error for `FOODS`, but ETS was nearly as accurate with less complexity. For `HOBBIES`, several approaches were effectively tied. For `HOUSEHOLD`, Linear Regression performed best. The project therefore shows that model complexity should be justified by category-level value, not assumed to be better.

## Business questions answered

### Can historical POS demand forecast future category demand accurately?

Yes. The Naive model produced test WAPE values of 16.10% for `FOODS`, 17.47% for `HOBBIES`, and 19.88% for `HOUSEHOLD`. Every non-naive approach reduced those errors. Historical demand therefore provides a useful basis for daily category-level forecasting.

### What demand patterns matter?

- Weekly seasonality is clear across all categories, with stronger demand from Friday through Sunday.
- Christmas Day demand falls to zero or near zero, consistent with store closures. It was retained in the data and treated as a known calendar effect.
- `FOODS` is relatively stable, `HOBBIES` is more variable, and `HOUSEHOLD` shows the clearest upward movement over time.
- These patterns justify weekly seasonal baselines, calendar features, lag features, rolling averages, and holiday-aware models.

### Do statistical and machine-learning models improve on simple baselines?

Yes, but the value depends on the category. ETS was the strongest baseline during rolling validation. Linear Regression, Prophet, and XGBoost were then tested using the same 13 expanding monthly validation windows before final test evaluation.

### Is the extra modelling effort worth it?

| Category | Practical assessment |
|---|---|
| FOODS | Conditionally. XGBoost had the lowest observed test WAPE, but ETS was only 0.47 WAPE points higher. Use XGBoost when that marginal accuracy gain justifies additional maintenance; otherwise ETS is a credible simpler option. |
| HOBBIES | Not clearly. XGBoost was lowest, but Prophet and ETS were within 0.12 WAPE points. The small gain alone does not justify a much more complex workflow. |
| HOUSEHOLD | No. Linear Regression outperformed both Prophet and XGBoost on the test period, so the more complex alternatives did not provide enough value. |

## Method

The M5 Forecasting dataset was aggregated to one daily observation per category:

```text
ds | cat_id | y
```

The chronological split was fixed before model comparison:

| Period | Dates |
|---|---|
| Train | 2011-01-29 to 2014-06-20 |
| Validation | 2014-06-21 to 2015-06-20 |
| Test | 2015-06-21 to 2016-06-19 |

Validation used 13 calendar-aligned, expanding windows. Every model was refitted using only the history available before a window. The test set was held out until the final notebook.

Model families evaluated:

- Baselines: Naive, Seasonal Naive, 7-Day SMA, and ETS.
- Linear Regression: lag, rolling, trend, calendar, and Christmas features; both full and reduced versions were tested using permutation importance.
- Prophet: weekly and yearly seasonality, Christmas as a holiday, and four understandable trend/seasonality settings.
- XGBoost: the shared lag, rolling, calendar, trend, and holiday feature set with four small parameter configurations.

WAPE is the primary business-facing metric because it expresses absolute error relative to total demand. Lower is better. MAE and RMSE were also calculated in the notebooks.

## Final test results

The table below includes every model evaluated in the final fixed test comparison. These scores are reported transparently, but they were not used to tune any settings after the test was opened.

| Category | Model | Test WAPE | Effort |
|---|---|---:|---|
| FOODS | XGBoost Faster | 10.22% | High |
| FOODS | ETS | 10.69% | Medium |
| FOODS | Linear Regression (Reduced) | 11.06% | Medium |
| FOODS | Prophet Additive | 13.16% | Medium |
| FOODS | 7-Day SMA | 14.17% | Low |
| FOODS | Seasonal Naive | 14.61% | Low |
| FOODS | Naive | 16.10% | Low |
| HOBBIES | XGBoost Shallow | 8.00% | High |
| HOBBIES | Prophet Flexible | 8.04% | Medium |
| HOBBIES | ETS | 8.12% | Medium |
| HOBBIES | Linear Regression (Full) | 8.78% | Medium |
| HOBBIES | Seasonal Naive | 9.38% | Low |
| HOBBIES | 7-Day SMA | 11.60% | Low |
| HOBBIES | Naive | 17.47% | Low |
| HOUSEHOLD | Linear Regression (Full) | 7.05% | Medium |
| HOUSEHOLD | XGBoost Shallow | 7.53% | High |
| HOUSEHOLD | Prophet Flexible | 8.31% | Medium |
| HOUSEHOLD | ETS | 8.44% | Medium |
| HOUSEHOLD | Seasonal Naive | 9.17% | Low |
| HOUSEHOLD | 7-Day SMA | 14.45% | Low |
| HOUSEHOLD | Naive | 19.88% | Low |

## Validation selection versus test performance

The validation winners were frozen before test evaluation. Their test errors were higher than validation errors, which is normal for a new out-of-sample period and reinforces why validation and test data must remain separate.

| Category | Validation-selected model | Validation WAPE | Test WAPE |
|---|---|---:|---:|
| FOODS | XGBoost Faster | 6.99% | 10.22% |
| HOBBIES | Linear Regression (Full) | 6.50% | 8.78% |
| HOUSEHOLD | Prophet Flexible | 6.88% | 8.31% |

The lowest observed test model differs from the validation-selected model for `HOBBIES` and `HOUSEHOLD`. This is an important finding, not a reason to tune again on the test period. Before changing the validated choice for a live use case, these alternatives should be assessed on a new future holdout period.

## Operational and financial interpretation

Forecast accuracy matters because it changes two operational exposures. For each category-day, the forecast residual is `actual − forecast`:

- A positive residual is an under-forecast. If inventory were limited to the forecast, the difference represents demand that could not be filled.
- A negative residual is an over-forecast. It represents inventory that would remain on hand after demand was met.

The table below applies that inventory-constrained scenario to the fixed test forecasts. It values units at the daily sales-weighted M5 `sell_price`. The dollar figures are **retail-value exposure**, not realized lost revenue, cash tied up, or profit: the dataset does not contain unit cost, gross margin, inventory availability, carrying cost, markdowns, substitutions, or backorders.

| Category | Model | Under-forecast units | Under-forecast retail-value exposure | Over-forecast units | Over-forecast retail-value exposure |
|---|---|---:|---:|---:|---:|
| FOODS | Naive | 415,148 | $1.09M | 1,150,579 | $3.01M |
| FOODS | ETS | 830,705 | $2.18M | 209,461 | $0.54M |
| FOODS | XGBoost Faster | 696,729 | $1.82M | 296,956 | $0.78M |
| HOBBIES | Naive | 25,534 | $0.11M | 225,804 | $0.96M |
| HOBBIES | ETS | 96,856 | $0.41M | 20,009 | $0.07M |
| HOBBIES | XGBoost Shallow | 90,863 | $0.38M | 24,192 | $0.10M |
| HOUSEHOLD | Naive | 114,353 | $0.46M | 595,585 | $2.30M |
| HOUSEHOLD | ETS | 241,795 | $0.95M | 59,615 | $0.22M |
| HOUSEHOLD | Linear Regression (Full) | 132,093 | $0.52M | 119,754 | $0.46M |

These figures show why lower aggregate forecast error is not the whole decision. Naive forecasts leave much more over-forecast retail-value exposure in all three categories, while ETS sharply reduces that exposure but can create more under-forecast retail-value exposure. The best observed model can improve the balance further, but its value is category-specific: for `HOBBIES`, the gap between ETS and XGBoost is small; for `HOUSEHOLD`, Linear Regression materially reduces under-forecast retail-value exposure relative to ETS.

### Category priorities

Average selling price helps put forecast error into business context, but it is not a margin measure. The table uses the same sales-weighted M5 `sell_price` values as the exposure analysis; actual margin, unit cost, and holding cost are not available in the dataset.

| Category | Test-period units | Test-period retail value | Sales-weighted average unit price | Recommended focus |
|---|---:|---:|---:|---|
| FOODS | 9.73M | $25.49M | $2.62 | Highest volume and retail-value exposure. ETS is a credible simpler baseline, but its under-forecast and over-forecast trade-off should be optimized with weekday-level buffers before adding more model complexity. |
| HOBBIES | 1.44M | $6.15M | $4.27 | Highest average selling price, but the observed ETS-to-XGBoost gap is small. Start with ETS and investigate further only if margin, stockout cost, promotions, or seasonal events make the small accuracy gain economically meaningful. |
| HOUSEHOLD | 3.57M | $14.05M | $3.94 | Strongest candidate for deeper analysis. Linear Regression produces a better observed under-/over-forecast balance than ETS, so this category is worth examining by weekday, event, and high-value item group. |

This suggests a practical next analysis: measure forecast error by weekday and business-critical demand periods, then set category-specific safety buffers from the cost of a stockout relative to the cost of carrying inventory. Where the data supports it, prediction intervals or forecast quantiles can set those buffers more directly than a single point forecast.

In a production setting, the model should be chosen by minimizing total expected economic cost rather than forecast error alone:

```text
total forecast economic cost
= under-forecast units × selling price × lost-sales rate × gross-margin rate
+ over-forecast units × unit cost × carrying-cost rate × expected holding period
+ expected markdown or obsolescence cost
```

This framework turns forecast improvement into an operational decision. It supports category-specific forecast adjustments or safety buffers when the cost of running short is higher than the cost of carrying extra inventory, while keeping those adjustments transparent and measurable.

## What each model contributed

| Model | What it added | Main limitation |
|---|---|---|
| Naive | A simple minimum benchmark. | Ignores weekly patterns, trend, and calendar effects. |
| Seasonal Naive | Repeats the previous week's day-of-week pattern. | Repeats unusual weeks directly. |
| 7-Day SMA | A smooth, easy-to-explain demand estimate. | Smooths away important day-of-week variation. |
| ETS | Level, damped trend, and weekly seasonality with moderate effort. | Does not use explicit calendar or lag features. |
| Linear Regression | Clear feature effects and an interpretable reduced-feature option. | Assumes linear relationships; recursive forecasts can compound error. |
| Prophet | Trend, weekly/yearly seasonality, holidays, and uncertainty intervals. | Its additional structure did not consistently improve category-level accuracy. |
| XGBoost | Non-linear relationships among lag, rolling, and calendar features. | Higher complexity and lower interpretability; marginal gains were category-specific. |

## Limitations

- Forecasts are at the daily category level, not at SKU-store level.
- The analysis does not model price, promotions, product substitutions, stockouts, or inventory availability as predictive inputs.
- Recursive multi-day forecasts use earlier predictions to construct later lag and rolling features, so errors can accumulate.
- The test period is one historical year. Demand changes should be monitored and models should be re-evaluated on future data.
- This project forecasts demand only. Allocation, replenishment, safety stock, and order recommendations are intentionally out of scope.

## Assumptions

- Daily sales can be summed across all items and stores within each category to create a meaningful category-level demand target.
- Future calendar dates, day of week, month, and Christmas are known when a forecast is made.
- The 13 expanding validation windows are representative enough to choose model configurations before the final test period.
- Demand cannot be negative, so negative model predictions were clipped to zero.
- The four small Prophet and XGBoost configuration sets are sufficient for a portfolio comparison; this is not an exhaustive hyperparameter search.
- Final test scores are a fixed report of the pre-specified models. They are not used to tune model settings or retroactively change the validation selection rule.

## Notebook map

| Notebook | Contribution |
|---|---|
| `00_data_preparation.ipynb` | Joined and validated the M5 analytical data. |
| `01_data_exploration.ipynb` | Identified category behavior, weekly patterns, and calendar effects. |
| `02_baseline_forecasting.ipynb` | Established initial benchmark performance. |
| `03_forecast_validation.ipynb` | Performed expanding-window baseline validation. |
| `04_linear_regression.ipynb` | Tested interpretable feature-based forecasting and feature reduction. |
| `05_prophet_model.ipynb` | Tested holiday-aware trend and seasonality forecasting. |
| `06_xgboost_model.ipynb` | Tested non-linear feature-based forecasting. |
| `07_model_comparison.ipynb` | Performed the final untouched test evaluation. |
