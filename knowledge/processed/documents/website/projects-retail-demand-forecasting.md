---
description: Portfolio of Jose Claudio, an analytics professional combining forecasting, statistical modeling, automation, finance, and supply-chain decision support.
---

[Skip to main content](#main-content)

[ All Case Studies](/projects)

01 — Forecasting

# Retail Demand Forecasting

Compared forecasting methods for daily retail demand and translated under- and over-forecast errors into retail-value exposure.

[ View on GitHub](https://github.com/jclaudio019/retail-operations)

![Retail Demand Forecasting project overview](/images/retail-demand-forecasting-hero-v2.png)

Portfolio overview from the project data: headline metrics, category demand over time, and Friday–Sunday seasonality.

7.05%

Best test WAPE

$3.01M

Naive over-forecast retail value\*

365 days

Untouched test period

\*Retail-value exposure for FOODS under a Naive inventory-constrained scenario (sales-weighted sell\_price). Not realized P&L, cash, or profit.

## Business Problem

Retail teams need a reliable view of daily demand to plan staffing and inventory. Recent sales alone can miss weekly patterns, changes in demand, and calendar events such as Christmas closures. Forecast accuracy also needs to be understood through the operational effects of under- and over-forecasting.

## Solution

I forecast daily unit sales for FOODS, HOBBIES, and HOUSEHOLD at the category level. This keeps weekly and holiday patterns visible without adding store-item allocation complexity.

I compared simple baselines, linear regression, Prophet, and XGBoost. Models were selected through expanding-window validation and evaluated once on a separate 365-day test period.

I then valued under- and over-forecasts using the sales-weighted selling price. These values represent potential retail exposure, not realized revenue, cash, or profit because unit cost, margin, and carrying cost were not available.

Allocation, replenishment, safety stock, and purchasing recommendations were outside the project scope.

## Dataset

The M5 Forecasting dataset (Walmart daily unit sales) was aggregated to one daily observation per category (ds | cat\_id | y). Chronological split: train 2011-01-29 to 2014-06-20, validation 2014-06-21 to 2015-06-20, and test 2015-06-21 to 2016-06-19\. Validation used 13 calendar-aligned expanding windows. Christmas Day demand falls to zero or near zero and was retained as a known calendar effect. Unit residuals on the test period were valued using sales-weighted sell\_price to support the exposure analysis.

## Methodology

I compared simple baselines with statistical and machine-learning models across 13 expanding validation windows. The selected models were evaluated once on a separate 365-day test period, and forecast errors were valued at the sales-weighted selling price.

Step-by-step method · 7 steps

* 01Prepared and validated the analytical data, then explored weekly seasonality, category behavior, and calendar effects — including the Friday–Sunday lift and Christmas closures.
* 02Established Naive, Seasonal Naive, 7-day SMA, and ETS baselines before comparing more complex models.
* 03Built Linear Regression with lag, rolling, trend, calendar, and Christmas features (full and reduced versions via permutation importance) to keep an interpretable option in the comparison.
* 04Tested Prophet with weekly/yearly seasonality and Christmas as a holiday, plus XGBoost on the shared feature set with small, pre-specified configurations — not an exhaustive hyperparameter search.
* 05Compared models across 13 expanding monthly validation windows with identical dates, horizons, and metrics (WAPE primary; MAE and RMSE also tracked).
* 06Froze validation-selected models per category, then evaluated every pre-specified model once on the untouched 365-day test year — with no post-test tuning.
* 07Translated test residuals into under-forecast and over-forecast unit counts and retail-value exposure, then ranked categories by volume, average selling price, and where deeper analysis would create the most decision value.

## Findings

Every evaluated alternative improved on the Naive benchmark. The best observed test WAPE was 10.22% for FOODS with XGBoost, 8.00% for HOBBIES with XGBoost, and 7.05% for HOUSEHOLD with linear regression. No model won every category, and simpler models were often close to the best result. Validation winners also changed on the test period for HOBBIES and HOUSEHOLD, showing why test data must remain separate.

![Category daily sales \(7-day rolling\) — purple glow marks Dec 25 demand dropping to near zero.](/images/retail-demand-sales-seasonality.png)

Category daily sales (7-day rolling) — purple glow marks Dec 25 demand dropping to near zero.

![True demand vs best observed model on the untouched test year — shaded gaps show under- and over-forecast.](/images/retail-demand-actual-vs-forecast.png)

True demand vs best observed model on the untouched test year — shaded gaps show under- and over-forecast.

7.05%

Best test WAPE

HOUSEHOLD

$3.01M

Naive excess exposure

FOODS · retail-value

365

Untouched test days

No post-test tuning

FOODSHOBBIESHOUSEHOLD

Category demand (7-day rolling)

Full history (2011–2016). Soft purple glow marks Dec 25 — demand collapses to near zero when stores close.

Dec 25 '11Dec 25 '122014Dec 25 '14Dec 25 '1508.0k16.0k24.0k32.0k

* FOODS
* HOBBIES
* HOUSEHOLD

Model accuracy

Test WAPE by model · FOODS. Lower is better — best observed model highlighted.

0%5%10%18.1%NaiveSeasonal Naive7-Day SMAProphet AdditiveLinear Regression(Reduced)ETSXGBoost Faster

Complexity vs value

Naive → ETS → best observed model. Additional complexity helped selectively, not everywhere.

NaiveETSBest0%5%10%15%20%

* FOODS
* HOBBIES
* HOUSEHOLD

Actual vs forecast

FOODS · XGBoost Faster — the validation-selected model, shown on the first 120 days of the untouched test year (test WAPE 10.22%). Solid area = true demand; dashed line = forecast.

Jun 21Jul 1Jul 9Jul 18Jul 27Aug 5Aug 15Aug 25Sep 4Sep 13Sep 23Oct 2Oct 1809.5k19.0k28.5k38.0k

* True demand
* Forecast

Weekly seasonality

Average daily units by weekday (2011–2016). Demand rises into the weekend across all three categories.

MonTueWedThuFriSatSun07.5k15.0k22.5k30.0k

* FOODS
* HOBBIES
* HOUSEHOLD

Hover charts for values · category tabs filter accuracy and forecast views

## Operations & Finance

Forecast accuracy matters because it changes two operational exposures. For each category-day, a positive residual (actual − forecast) is an under-forecast: demand that could not be filled if inventory were limited to the forecast. A negative residual is an over-forecast: inventory that would remain after demand was met. The table below applies that inventory-constrained scenario to fixed test forecasts and values units at sales-weighted sell\_price.

These figures show retail-value exposure, not realized lost sales, cash, or profit. Margin, unit cost, carrying cost, and service-level policy were not available.

| Category  | Model                    | Under-forecast retail-value exposure | Over-forecast retail-value exposure |
| --------- | ------------------------ | ------------------------------------ | ----------------------------------- |
| FOODS     | Naive                    | $1.09M                               | $3.01M                              |
| FOODS     | XGBoost Faster           | $1.82M                               | $0.78M                              |
| HOBBIES   | Naive                    | $0.11M                               | $0.96M                              |
| HOBBIES   | XGBoost Shallow          | $0.38M                               | $0.10M                              |
| HOUSEHOLD | Naive                    | $0.46M                               | $2.30M                              |
| HOUSEHOLD | Linear Regression (Full) | $0.52M                               | $0.46M                              |

Full exposure detail · all models and unit counts

| Category  | Model                    | Under-forecast units | Under-forecast retail-value exposure | Over-forecast units | Over-forecast retail-value exposure |
| --------- | ------------------------ | -------------------- | ------------------------------------ | ------------------- | ----------------------------------- |
| FOODS     | Naive                    | 415,148              | $1.09M                               | 1,150,579           | $3.01M                              |
| FOODS     | ETS                      | 830,705              | $2.18M                               | 209,461             | $0.54M                              |
| FOODS     | XGBoost Faster           | 696,729              | $1.82M                               | 296,956             | $0.78M                              |
| HOBBIES   | Naive                    | 25,534               | $0.11M                               | 225,804             | $0.96M                              |
| HOBBIES   | ETS                      | 96,856               | $0.41M                               | 20,009              | $0.07M                              |
| HOBBIES   | XGBoost Shallow          | 90,863               | $0.38M                               | 24,192              | $0.10M                              |
| HOUSEHOLD | Naive                    | 114,353              | $0.46M                               | 595,585             | $2.30M                              |
| HOUSEHOLD | ETS                      | 241,795              | $0.95M                               | 59,615              | $0.22M                              |
| HOUSEHOLD | Linear Regression (Full) | 132,093              | $0.52M                               | 119,754             | $0.46M                              |

[Full report and code ](https://github.com/jclaudio019/retail-operations)

Naive forecasts create much more over-forecast retail-value exposure in every category. Better models reduce that amount but can increase under-forecast retail-value exposure, so model comparisons should consider both sides instead of WAPE alone. For HOBBIES, ETS and XGBoost are close. For HOUSEHOLD, linear regression produces a better balance than ETS.

Average selling price helps put error into business context (it is not a margin measure). Categories differ in volume, retail value, and where deeper work is worth the effort:

| Category  | Test units | Retail value | Avg unit price | Recommended focus                                                                                                                                |
| --------- | ---------- | ------------ | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| FOODS     | 9.73M      | $25.49M      | $2.62          | Highest volume and retail-value exposure. ETS is a strong simple baseline; review weekday buffers before adding complexity.                      |
| HOBBIES   | 1.44M      | $6.15M       | $4.27          | Highest average selling price, but ETS≈XGBoost. Dig deeper only if margin, stockout cost, or promotions make the small accuracy gain meaningful. |
| HOUSEHOLD | 3.57M      | $14.05M      | $3.94          | Strongest candidate for deeper analysis — better observed balance than ETS, worth weekday/event/high-value item review.                          |

## Business Implications

Forecast accuracy is only part of the decision. Under-forecasts can mean missed demand, while over-forecasts can leave excess product on the shelf. A production decision should compare those costs by category and use different buffers when running short is more expensive than carrying extra inventory.

## Conclusion

Historical sales can forecast category demand more accurately than simply using recent sales, but the best method depends on the category.

The project compares baseline, statistical, and machine-learning models, evaluates them on separate test data, and translates errors into potential retail exposure so operations and finance can discuss the same result.

The practical next step is to keep simpler models when results are close, review HOUSEHOLD in more detail, and set category buffers based on the cost of stockouts versus excess inventory.

## Worth Digging Deeper

* 01Measure forecast error by weekday and business-critical demand periods, then set category-specific safety buffers from stockout cost versus carrying cost.
* 02Where the data supports it, add prediction intervals or forecast quantiles so buffers are probabilistic rather than ad hoc point-forecast padding.
* 03Drill into high-value item groups within HOUSEHOLD (and price-sensitive pockets of HOBBIES) where average selling price makes residual error more expensive.
* 04If unit cost, margin, and holding-cost inputs become available, replace retail-value exposure with a true expected economic-cost objective for model selection.
* 05Extend beyond category-level demand into allocation / replenishment only after the demand signal and its uncertainty are stable enough to trust.

## Limitations

* Forecasts are at the daily category level, not SKU-store level.
* Price, promotions, substitutions, stockouts, and inventory availability were not modeled as predictive inputs.
* Dollar exposure uses sell\_price retail value — not unit cost, margin, carrying cost, or realized P&L.
* Recursive multi-day forecasts can accumulate error through lag and rolling features.
* The test period is one historical year; demand changes should be monitored on future data.
* Allocation, replenishment, safety stock, and order recommendations were intentionally out of scope.

## Technologies

PythonpandasstatsmodelsProphetXGBoostscikit-learn

[Next case studyCredit Risk Probability of Default](/projects/credit-risk-pd-model)

7.5k
