# Detailed PD Notebook Reorganization Design

**Date:** 2026-07-29  
**Status:** Approved in conversation on 2026-07-29  
**Public repository:** `jclaudio019/credit_risk`

## Goal

Rebuild the public Probability of Default project as a detailed, notebook-led
analysis that faithfully preserves the author's original preparation,
feature-engineering, modeling, validation, scorecard work, and analytical
conclusions while removing accidental repetition, failed scratch work, spelling
errors, chat-like text, and obsolete path assumptions.

The result remains an educational portfolio project. It should demonstrate the
actual analytical process without presenting itself as a production lending
system or as work completed by a more experienced data scientist than the
author.

## Authoritative Sources

Both original notebooks are truth sources:

1. `/Users/joseclaudio/Dev_local/Credit_Risk/PD_Data_Model.ipynb`
   - Data preparation and cleaning
   - Missing-value decisions
   - Historical target construction
   - Train/test preparation
   - WoE and IV derivation
   - Fine and coarse classing
   - Discrete and continuous feature analysis

2. `/Users/joseclaudio/Dev_local/Credit_Risk/Credit Risk Modeling - PD Model - With Comments - 6-2.ipynb`
   - Feature and reference-category selection
   - Logistic regression
   - Coefficients and p-values
   - Held-out predictions
   - Confusion matrix and threshold analysis
   - ROC/AUC, Gini, and KS
   - 300–850 scorecard construction
   - Individual account scoring

The smaller preparation notebook and `PD Model.ipynb` may be consulted to
clarify intent, but they do not override the two sources above.

## Preservation Rules

The reorganization preserves analytical intent and coverage, not every
accidental notebook cell.

Preserve:

- Every substantive cleaning and transformation decision.
- Every feature investigated through WoE/IV or fine/coarse classing.
- Features rejected from the final model and the author's reason for rejecting
  them.
- Intermediate tables and plots that support a decision.
- The author's conclusions throughout the workflow, rewritten only for
  spelling, clarity, and professional presentation.
- The model-selection, validation, and scorecard reasoning.
- Honest weak or negative findings, including unsuitable classification
  thresholds or variables with limited predictive value.

Consolidate or remove:

- Repeated dataframe displays that add no new information.
- Duplicate plotting experiments showing the same result.
- Empty cells, undefined scratch variables, and cells preserved only because an
  earlier attempt failed.
- Chat prompts such as "Would you like me to..." and pasted instructional
  boilerplate.
- Absolute local paths and obsolete pickle-loading shortcuts.
- Course explanations copied verbatim. Necessary concepts will be rewritten in
  the author's portfolio voice and tied directly to the analysis.

Correct transparently:

- Typographical errors in labels and prose.
- Obvious category-condition defects, such as a label saying `>=4` while the
  code tests `>=9`.
- Duplicated category operands.
- Undefined intermediate variables.
- Accidental reuse of training data as test data.
- Pandas chained-assignment patterns.
- Date parsing that incorrectly places two-digit historical years in the
  future.
- Leakage-prone preprocessing where a training-only statistic is appropriate.

Corrections must preserve the original analytical question. A short markdown
note should explain any correction that materially changes the original
implementation.

## Public Notebook Structure

### `00_data_understanding_and_preparation.ipynb`

Purpose: establish the dataset, its business meaning, and the raw fields needed
for PD analysis.

Content:

- Dataset origin, observation period, row/column dimensions, and field overview.
- Head, tail, column list, data types, missingness overview, and selected
  descriptive statistics.
- Employment-length string investigation and integer conversion.
- Loan-term conversion.
- Earliest-credit-line parsing and months-since calculation.
- Loan-issue-date parsing and months-since calculation.
- Explanation and correction of future dates caused by two-digit year parsing.
- Analysis reference date fixed at `2017-12-01`, matching the original work.
  Parsed credit-line dates later than that reference are corrected by moving
  them back 100 years before months-since values are calculated.
- Conclusions describing which raw fields are ready for cleaning and why.

### `01_data_cleaning_and_target_definition.ipynb`

Purpose: apply explicit data-quality decisions and create a reproducible
historical PD target and modeling split.

Content:

- Deterministic field conversions and historical target construction.
- Stratified 80/20 train/test split using `random_state=42` before learning any
  imputation statistic.
- Missing-value counts before repair for both partitions.
- `total_rev_hi_lim` imputation from `funded_amnt` with the original reasoning.
- `annual_inc` imputation using the training mean, applied unchanged to held-out
  rows.
- Zero imputation for event-count fields where missing represents no recorded
  event.
- Remaining missingness checks and data-type checks.
- Dummy-variable preparation for the original categorical fields.
- `good_bad = 0` for:
  - `Charged Off`
  - `Default`
  - `Does not meet the credit policy. Status:Charged Off`
  - `Late (31-120 days)`
- `good_bad = 1` for all other observed statuses.
- Class counts and proportions.
- Saved ignored checkpoints under `data/processed/`.
- Conclusions describing what the target represents and does not represent.

### `02_discrete_feature_engineering_and_woe.ipynb`

Purpose: preserve the complete discrete-variable WoE/IV investigation and
category-grouping reasoning.

Content:

- WoE and IV concepts, formulas, interpretation, and safeguards for zero
  distributions.
- Step-by-step manual WoE construction for `grade`.
- Reusable notebook-local WoE/IV calculation and plotting functions.
- Analysis of:
  - grade
  - home ownership
  - address state
  - verification status
  - purpose
  - initial list status
- Original plots and useful range-focused plots.
- Explicit category-merging decisions and reference-category reasoning.
- IV summary for the investigated discrete variables.
- Train-derived category definitions applied unchanged to held-out rows.
- Saved ignored discrete-feature checkpoints.
- Conclusions for every investigated variable, including weak variables.

### `03_continuous_feature_engineering_and_woe.ipynb`

Purpose: preserve the complete fine/coarse-classing analysis for ordered and
continuous predictors.

Content:

- Ordered/continuous WoE helper and fine-classing procedure.
- Analysis, plots, coarse categories, and conclusions for:
  - term
  - employment length
  - months since issue
  - interest rate
  - funded amount
  - months since earliest credit line
  - installment
  - delinquencies in the last two years
  - inquiries in the last six months
  - open accounts
  - public records
  - total accounts
  - accounts currently delinquent
  - total revolving high credit limit
  - annual income
  - months since last delinquency
  - debt-to-income ratio
  - months since last public record
- Preservation of the original conclusion that funded amount has limited
  useful monotonic discriminatory structure.
- Explicit handling of missing-value categories where absence is informative.
- Train-derived binning/grouping applied unchanged to held-out rows.
- Saved ignored final feature-matrix checkpoints.
- A compact final feature and reference-category inventory.

### `04_pd_logistic_regression_and_validation.ipynb`

Purpose: fit the PD model and preserve the complete statistical and held-out
validation analysis.

Content:

- Selected features and their reference categories.
- The final candidate inventory comes from the original model notebook's full
  selected-feature and reference-category lists, not the reduced five-feature
  version currently published.
- Rationale for dropping a reference level from each dummy-variable family.
- Broader initial logistic specification.
- Coefficients, intercept, and coefficient summary.
- Statistically interpretable logistic specification with p-values.
- Removal of variable families whose categories are consistently
  non-significant, with the original reasoning retained.
- Final model fit.
- Held-out class and probability predictions.
- Confusion matrix in counts and proportions.
- Accuracy at the displayed threshold, with a warning about class imbalance.
- ROC curve and AUC.
- Gini coefficient.
- Cumulative population/good/bad calculations.
- KS statistic and KS plot.
- Conclusions that distinguish rank discrimination from classification
  performance.

The notebook models `P(good)`. PD is always calculated explicitly as
`1 - P(good)`.

### `05_pd_scorecard_and_final_conclusions.ipynb`

Purpose: translate the fitted PD model into an illustrative scorecard and close
the completed public analysis.

Content:

- Reconstructed coefficient table including zero-coefficient reference
  categories.
- Original feature-family names.
- Minimum score 300 and maximum score 850.
- Minimum/maximum coefficient sums.
- Score rescaling, preliminary rounding, and reconciliation of rounding
  differences.
- Final category scores.
- Held-out account score calculation.
- Relationship between score, `P(good)`, and PD.
- Example account-level score interpretation.
- Final conclusions covering data preparation, feature behavior, model
  discrimination, threshold limitations, and the educational status of the
  scorecard.

LGD, EAD, Expected Loss, FastAPI, DuckDB, and interactive delivery are excluded
from this public notebook. They belong only in the private recommendations
document.

## Data and Execution Contract

- Raw input: `data/loan_data_2007_2014.csv`.
- Notebook-relative input path: `../data/loan_data_2007_2014.csv`.
- Generated checkpoints: `data/processed/*.pkl`.
- `data/processed/` is ignored by Git.
- Public notebooks are executed and committed with their outputs.
- Run order is `00` through `05`.
- No helper `.py` modules are added.
- No absolute machine-specific paths appear in public notebooks.
- Notebook-local helper functions are allowed when they make the analysis
  readable and are used within that notebook.
- Later notebooks load the prior stage's checkpoint rather than duplicating the
  earlier stage's transformations.
- The public README tells users to run the notebooks sequentially.

## README Design

The public README will:

- Retain the project introduction and business context.
- Describe the six-notebook workflow.
- Replace `Skills demonstrated` with `Methodology`.
- Explain data understanding, cleaning, target construction, WoE/IV,
  fine/coarse classing, feature and reference-category selection, logistic
  regression, held-out validation, and scorecard construction.
- Report only freshly reproduced final metrics.
- Retain concise limitations specific to the historical data and educational
  scorecard.
- Remove `Future work`.
- Remove production-governance, monitoring, fairness, and system-validation
  checklists that do not belong in this showcase README.

`Final_Report.md` will be updated after the final executed run so its notebook
names, methodology, metrics, and conclusions do not contradict the rebuilt
analysis. It will not contain future-development recommendations.

## Private Recommendations

Create repository-root `recommendations.md` only after adding
`/recommendations.md` to `.gitignore`.

It remains local and untracked. It will contain:

- LGD scope, target definition, recovery/cost requirements, and candidate
  modeling approaches.
- EAD scope, exposure timing, revolving versus installment considerations, and
  candidate approaches.
- Expected Loss calculation: `EL = PD × LGD × EAD`.
- Suggested order: stabilize PD, define LGD, define EAD, calculate account and
  portfolio expected loss, then consider delivery.
- FastAPI, DuckDB, and interactive portfolio options.
- Required data, unresolved decisions, validation checkpoints, and stopping
  points.

No public document links to this file.

## Parallel Worktree Design

All implementation begins from the same clean `main` commit.

### Worktree A: `agent/pd-data-foundation`

- Owns notebooks `00` and `01`.
- Truth-source range: preparation notebook plus `PD_Data_Model.ipynb` cells
  0–76.
- Must not edit notebooks `02`–`05`, README, `.gitignore`, or recommendations.

### Worktree B: `agent/pd-woe-engineering`

- Owns notebooks `02` and `03`.
- Truth-source range: `PD_Data_Model.ipynb` cells 77–215. Empty tail cells and
  display-only cells still must be classified by the source-coverage audit.
- Must not edit notebooks `00`, `01`, `04`, `05`, README, `.gitignore`, or
  recommendations.

### Worktree C: `agent/pd-model-scorecard`

- Owns notebooks `04` and `05`.
- Truth-source range: both original model notebooks.
- Must not edit notebooks `00`–`03`, README, `.gitignore`, or recommendations.

Implementation agents use GPT-5.6 Terra at medium reasoning. Each agent:

- Reads its private task brief first.
- Uses only its assigned truth-source range.
- Validates notebook JSON and assigned analytical coverage.
- Commits only assigned notebook files.
- Uses the configured `jclaudio` Git identity.
- Adds no Codex or AI co-author attribution.

Parallel work is drafting and notebook construction. Full pipeline execution is
an integration-stage activity because later notebooks depend on earlier
checkpoints.

## Integration and Review

1. Create an integration branch and worktree.
2. Merge worktree A, B, and C commits in notebook order.
3. Dispatch a documentation task for README, `.gitignore`, and the private
   recommendations file.
4. Run notebooks `00`–`05` sequentially using the existing `portfolio` Conda
   environment.
5. Save successful executed copies back to the tracked notebooks.
6. Verify:
   - every code cell has a non-null execution count;
   - no notebook contains an error output;
   - notebook sources contain no absolute local path;
   - generated data/model artifacts are ignored;
   - the repository contains only intended public files.
7. Run an independent source-coverage audit against both truth-source
   notebooks.
8. Run an independent technical audit covering data flow, train/test
   separation, WoE/IV calculations, feature bins, model interpretation,
   metrics, scorecard arithmetic, and reproducibility.
   Final auditors use GPT-5.6 Sol at high reasoning and do not share an
   implementation agent's context.
9. Send all material findings through one coordinated fix wave.
10. Run one independent scoped re-review.
11. Merge to `main` and push only after both audits pass with no unresolved
    material finding.
12. After the final merged commit, run the entire `00`–`05` sequence one last
    time from regenerated ignored checkpoints, replace the tracked notebooks
    with those executed copies, and repeat the zero-error/output checks.
13. Push the final commit to GitHub and verify:
    - local `HEAD` equals `origin/main`;
    - all six notebook paths exist in the remote tree;
    - the remote notebook JSON contains executed code cells and saved outputs;
    - the remote tree excludes private process files, recommendations, data,
      processed checkpoints, and model artifacts.

## Source-Coverage Acceptance Rules

The final source audit must account for every substantive original cell as one
of:

- preserved directly;
- consolidated with named duplicate cells;
- corrected with the defect and replacement identified;
- omitted because it is empty, chat-like boilerplate, an obsolete path/load
  shortcut, or failed scratch work.

The audit fails if:

- an investigated feature disappears without explanation;
- an original analytical conclusion disappears;
- a material transformation or model step is missing;
- a public conclusion is stronger than the executed evidence;
- a corrected implementation silently changes analytical meaning;
- any notebook cannot run in the documented sequence.

## Public Git Boundary

Public commits may include:

- Six executed notebooks.
- README updates.
- `Final_Report.md` updates.
- `.gitignore` updates.
- Data-location documentation if required.

Public commits must not include:

- `recommendations.md`.
- `docs/superpowers/`.
- Worktree, task-brief, ledger, review-package, or audit-process artifacts.
- Raw or processed data.
- Pickled models or generated tables.
- Codex or AI attribution.
