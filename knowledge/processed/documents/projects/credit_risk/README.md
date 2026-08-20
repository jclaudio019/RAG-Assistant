# Credit Risk Probability-of-Default Analysis

Can historical borrower and loan characteristics rank observed credit risk,
and can that model output be translated into an interpretable score? This
educational, notebook-led analysis answers that question with an illustrative
probability-of-default (PD) workflow, not a lending decision system or
production credit model.

## Headline evidence

- 466,285 historical loan records across the train/test population.
- Held-out AUC: **0.699482**; Gini: **0.398964**; KS: **0.291652**.
- An illustrative **300–850** scorecard communicates relative model risk.

Read the full [portfolio case](Final_Report.md) and inspect the lightweight
[model artifacts](model/README.md).

The historical target is `good_bad`: `0` for the listed bad loan statuses
(`Charged Off`, `Default`, policy charged-off, and late 31–120 day loans), and
`1` for all other observed statuses. The model estimates probability of good standing, `P(good)`. PD is calculated only afterwards as `1 - P(good)`; the two should not be treated as the same quantity.

## Workflow

Run the notebooks in order.

| Notebook | Purpose |
| --- | --- |
| `00_data_understanding_and_preparation.ipynb` | Establishes the source fields, data quality context, and deterministic date conversions. |
| `01_data_cleaning_and_target_definition.ipynb` | Defines the historical target, applies partition-aware repairs, and creates the train/test split. |
| `02_discrete_feature_engineering_and_woe.ipynb` | Investigates discrete variables with train-derived WoE/IV and category groupings. |
| `03_continuous_feature_engineering_and_woe.ipynb` | Performs fine/coarse classing for ordered and continuous predictors. |
| `04_pd_logistic_regression_and_validation.ipynb` | Fits logistic specifications for `P(good)` and evaluates held-out discrimination and thresholds. |
| `05_pd_scorecard_and_final_conclusions.ipynb` | Builds the illustrative 300–850 scorecard and interprets held-out account scores. |

## Methodology

The workflow begins with data understanding, deterministic cleaning, and the
historical target definition. It then uses a stratified 80/20 train/test split,
with imputation statistics, category definitions, and feature bins learned
from training rows and applied unchanged to held-out rows.

Weight of Evidence (WoE) examined risk ordering and similarity across
categories and intervals, informing category grouping and coarse classing.
Information Value (IV) summarized feature separation strength as a descriptive
diagnostic, not an automatic feature-selection rule. The logistic regression
used one-hot grouped categories, not numeric WoE values; after the initial
full-rank model, consistently non-significant feature families were removed,
with explicit reference categories preserving interpretability. The notebooks
report coefficients, probability interpretation, held-out threshold behavior,
ROC/AUC, Gini, KS, and an illustrative 300–850 scorecard. The model estimates
`P(good)` and calculates PD explicitly as `1 - P(good)`.

The illustrative score scale is derived from the theoretical per-family
minimum and maximum model coefficients, including the intercept, rather than
from the observed training-score distribution.

## Reproducibility

1. Obtain the historical Lending Club CSV and place it at
   `data/loan_data_2007_2014.csv`.
2. Create an environment and install `pip install -r requirements.txt`.
3. Run the six notebooks above in numerical order from the `notebooks/`
   directory so their relative data path resolves.

The source dataset is local and is not included in this repository. See
[`data/README.md`](data/README.md) for the expected location.

## Limitations

- `good_bad` is a simplified historical bad-status proxy, not a fixed
  performance-horizon default definition or current underwriting rule.
- The random holdout is useful for this exercise but does not establish
  time-based stability, calibration, fairness, or regulatory suitability.
- The 300–850 scale is illustrative, not a production scorecard calibration or
  lending policy.
- Historical Lending Club data may not represent a current portfolio or lending
  environment.
