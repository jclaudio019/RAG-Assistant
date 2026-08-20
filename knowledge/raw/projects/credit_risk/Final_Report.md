# Credit Risk Probability-of-Default Case Study

## Project summary

This educational analysis asks whether historical borrower and loan
characteristics can rank observed credit risk and translate model output into
an interpretable score. Using historical Lending Club loan records, it builds
an interpretable logistic-regression view of `P(good)` and derives probability
of default as `PD = 1 - P(good)`.

The result is a historical portfolio analysis: a transparent way to examine
relative risk and communicate it through an illustrative scorecard, not a
lending decision system.

## Headline evidence

- **466,285** historical loan records were reviewed: **373,028** training rows
  and **93,257** held-out rows.
- Held-out ranking metrics were **AUC 0.699482**, **Gini 0.398964**, and
  **KS 0.291652**.
- The model output is `P(good)`; default risk is expressed as
  `PD = 1 - P(good)`.
- The model is translated into an illustrative **300–850** scorecard.
- At the displayed 0.5 `P(good)` threshold, it detected **10 of 10,194**
  held-out bad loans.

## Business problem

Credit-risk teams need a consistent way to summarize how borrower and loan
characteristics relate to observed repayment outcomes. The decision question
was whether those historical characteristics can rank observed credit risk and
turn that ranking into an interpretable score for discussion.

The challenge is not only to estimate risk, but to avoid treating a model
probability or a single threshold as a complete lending decision. A useful
analysis must distinguish relative ranking, the choice of an operating
threshold, and the business consequences of each.

## Solution

The project delivers a six-notebook, train/test workflow that cleans the
historical data, engineers grouped predictors, fits an interpretable logistic
model for `P(good)`, evaluates it on held-out accounts, and translates the
fitted log-odds into an illustrative 300–850 scorecard.

The supporting [public model bundle](model/) provides an inspectable
view of the final model artifacts. The notebooks remain the source for the
historical preprocessing and analysis.

## Dataset and target

The analysis uses 466,285 historical Lending Club loan records. A stratified
80/20 split produced 373,028 training rows and 93,257 held-out rows. The target
is `good_bad`: specified historical charge-off, default, and late-status
outcomes are labelled bad (`0`), while the remaining observed statuses are
labelled good standing (`1`).

The fitted model estimates `P(good)`, the probability of target class 1.
Probability of default is calculated explicitly as `PD = 1 - P(good)`; it is
not a separately trained target.

## Methodology

Cleaning and feature definitions were learned from training data and applied
unchanged to held-out rows. The workflow repaired known data issues,
partitioned the data, and prepared employment, term, date, income, and
credit-line fields before model fitting.

Weight of Evidence (WoE) was used to inspect risk ordering and similarity
across categories and numeric intervals. Those patterns guided category
grouping and coarse classing. Information Value (IV) summarized each feature's
overall separation strength, but was descriptive rather than a feature-
selection cutoff. For example, grade had the strongest reviewed discrete IV
at **0.292145**, without that value selecting the final features.

The logistic regression used one-hot grouped categories, not numeric
WoE-transformed values. After an initial full-rank model, families whose dummy
levels were consistently non-significant were removed: delinquencies, open
accounts, public records, total accounts, and revolving-limit bands. Explicit
reference categories retained an interpretable final specification.

## Findings

On held-out data, the model achieved AUC **0.699482**, Gini **0.398964**, and
KS **0.291652**. Together, these measures indicate limited-to-moderate
historical ranking ability: the model separates risk to a useful degree, while
material overlap between good and bad outcomes remains.

At the displayed 0.5 `P(good)` threshold, only 10 of 10,194 held-out bad loans
were detected. This does not contradict the ranking metrics. AUC, Gini, and KS
evaluate how well the model orders accounts across thresholds; a fixed 0.5
cutoff turns that ordering into one particular classification rule. With an
imbalanced historical target, that displayed rule can have poor bad-loan recall
even when the model provides moderate rank ordering.

The illustrative 300–850 scorecard is a linear translation of fitted
log-odds. Higher scores correspond to higher `P(good)` and lower PD, making
relative historical risk easier to communicate.

## Business implications

The model can support a discussion of relative historical risk, but a business
threshold would require an explicit tradeoff: a higher threshold may reject
more good borrowers, while a lower threshold may miss more defaults. Neither
cost is represented by the displayed 0.5 `P(good)` threshold.

The scorecard offers an interpretable common scale for that conversation. It
does not supply approval, pricing, or treatment rules. Any operating use would
need threshold decisions tied to the cost of missed defaults and rejected good
borrowers, supported by calibration and time-based validation.

## Conclusion

Historical borrower and loan characteristics provided limited-to-moderate
held-out ranking of observed credit risk. The workflow makes the model's
direction explicit—`P(good)` first, then `PD = 1 - P(good)`—and translates the
result into an illustrative 300–850 scorecard. Its value is transparency about
historical relationships and the tradeoffs that a real decision policy would
need to resolve.

## Limitations

- The source data and `good_bad` target are historical and simplified; they do
  not define a fixed performance-horizon default measure or a current policy.
- The scorecard is illustrative and has not been calibrated as a lending rule.
- A single random holdout does not establish temporal stability; time-based
  validation is required before relying on performance across periods.
- Fairness has not been assessed, and the analysis is not a regulatory model.
- The work is a notebook-led historical analysis, not a production raw-loan
  scoring service.

## Technologies

- Python, pandas, NumPy, and Jupyter notebooks for preparation and analysis
- statsmodels for interpretable logistic regression and statistical inference
- scikit-learn for held-out discrimination metrics and validation utilities
- Matplotlib for exploratory and model-evaluation visuals

## Notebook map

| Notebook | Contribution |
| --- | --- |
| [`00_data_understanding_and_preparation.ipynb`](notebooks/00_data_understanding_and_preparation.ipynb) | Establishes source fields, data-quality context, and date preparation. |
| [`01_data_cleaning_and_target_definition.ipynb`](notebooks/01_data_cleaning_and_target_definition.ipynb) | Defines `good_bad`, applies partition-aware cleaning, and creates the split. |
| [`02_discrete_feature_engineering_and_woe.ipynb`](notebooks/02_discrete_feature_engineering_and_woe.ipynb) | Reviews discrete predictors with WoE/IV and category grouping. |
| [`03_continuous_feature_engineering_and_woe.ipynb`](notebooks/03_continuous_feature_engineering_and_woe.ipynb) | Applies fine and coarse classing to ordered and continuous predictors. |
| [`04_pd_logistic_regression_and_validation.ipynb`](notebooks/04_pd_logistic_regression_and_validation.ipynb) | Fits `P(good)` and evaluates held-out ranking and threshold behavior. |
| [`05_pd_scorecard_and_final_conclusions.ipynb`](notebooks/05_pd_scorecard_and_final_conclusions.ipynb) | Builds and interprets the illustrative 300–850 scorecard. |
