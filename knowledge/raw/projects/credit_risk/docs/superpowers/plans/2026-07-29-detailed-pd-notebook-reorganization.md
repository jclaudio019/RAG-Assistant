# Detailed PD Notebook Reorganization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the condensed five-notebook PD project with six detailed, executed notebooks that preserve the complete original analysis, update the public documentation, retain private recommendations locally, pass independent source and technical audits, and publish verified notebook outputs to GitHub.

**Architecture:** Three GPT-5.6 Terra medium implementers build non-overlapping notebook pairs in parallel Git worktrees from the same clean base. Their commits merge into an integration worktree, where documentation, sequential execution, independent GPT-5.6 Sol high audits, one coordinated fix wave, final clean execution, and GitHub verification occur.

**Tech Stack:** Jupyter Notebook, Python 3.12, pandas, NumPy, Matplotlib, seaborn, scikit-learn, SciPy, statsmodels, Git worktrees, GitHub CLI.

## Global Constraints

- Authoritative sources are `/Users/joseclaudio/Dev_local/Credit_Risk/PD_Data_Model.ipynb` and `/Users/joseclaudio/Dev_local/Credit_Risk/Credit Risk Modeling - PD Model - With Comments - 6-2.ipynb`.
- Preserve all substantive transformations, investigated features, intermediate evidence, rejected-feature reasoning, model steps, and author conclusions.
- Consolidate only duplicate displays/plots, empty cells, failed scratch work, obsolete path/load shortcuts, and chat-like or copied instructional boilerplate.
- Correct obvious defects transparently without changing the original analytical question.
- Raw data path is `../data/loan_data_2007_2014.csv` from the notebooks directory.
- Analysis reference date is `2017-12-01`.
- Historical bad statuses are `Charged Off`, `Default`, `Does not meet the credit policy. Status:Charged Off`, and `Late (31-120 days)`.
- `good_bad = 0` means historical bad; `good_bad = 1` means all other observed statuses.
- Split is stratified 80/20 with `random_state=42` before learning imputation statistics.
- Generated checkpoints live under `data/processed/` and are never committed.
- No helper `.py` modules, absolute machine paths, raw data, processed data, model artifacts, or public development-process documents.
- Public notebooks are committed with executed outputs and zero error outputs.
- `recommendations.md` remains local, ignored, untracked, and unreferenced by public files.
- Implementation commits use `jclaudio <jclaudio@brainlessqi.com>` with no Codex, OpenAI, AI, or co-author attribution.
- Implementation agents use GPT-5.6 Terra with medium reasoning.
- Independent final auditors use GPT-5.6 Sol with high reasoning.
- The final public branch is pushed only after source coverage, technical correctness, final clean execution, saved-output validation, and remote-tree validation pass.

---

### Task 1: Freeze Boundaries and Create Isolated Worktrees

**Files:**
- Read: `docs/superpowers/specs/2026-07-29-detailed-pd-notebook-reorganization-design.md`
- Create privately: `.superpowers/sdd/2026-07-29-detailed-pd-notebook-reorganization/source-coverage-contract.md`
- Create privately: `.superpowers/sdd/2026-07-29-detailed-pd-notebook-reorganization/progress.md`
- Create worktrees: `.worktrees/pd-data-foundation`, `.worktrees/pd-woe-engineering`, `.worktrees/pd-model-scorecard`, `.worktrees/pd-integration`

**Interfaces:**
- Consumes: clean `main` at the same base commit in every worktree.
- Produces: four isolated branches and an exact source-coverage contract used by all implementers and auditors.

- [ ] **Step 1: Verify the base repository and Git identity**

```bash
git status --short --branch
git rev-parse HEAD
git config user.name
git config user.email
git check-ignore -q .worktrees
```

Expected: clean `main`, user `jclaudio`, email `jclaudio@brainlessqi.com`, and `.worktrees` ignored.

- [ ] **Step 2: Record the private coverage contract**

The contract must assign:

```text
Worktree A -> notebooks 00-01
  Preparation notebook cells 0-13
  PD_Data_Model.ipynb cells 0-76

Worktree B -> notebooks 02-03
  PD_Data_Model.ipynb cells 77-215

Worktree C -> notebooks 04-05
  Credit Risk Modeling - PD Model - With Comments - 6-2.ipynb cells 0-128
  PD Model.ipynb cells 0-19 as clarification only

Controller/docs -> README.md, Final_Report.md, .gitignore, private recommendations.md
```

For every assigned source cell, the agent report must classify it as preserved, consolidated, corrected, or intentionally omitted under the approved rules.

- [ ] **Step 3: Create all branches from the same base**

```bash
git worktree add .worktrees/pd-data-foundation -b agent/pd-data-foundation main
git worktree add .worktrees/pd-woe-engineering -b agent/pd-woe-engineering main
git worktree add .worktrees/pd-model-scorecard -b agent/pd-model-scorecard main
git worktree add .worktrees/pd-integration -b agent/pd-notebook-integration main
```

- [ ] **Step 4: Provide raw data to isolated worktrees without tracking it**

In each worktree, create `data/` if needed and link:

```text
data/loan_data_2007_2014.csv
  -> /Users/joseclaudio/Dev_local/project_potfolio/credit_risk/data/loan_data_2007_2014.csv
```

Verify each path is ignored with:

```bash
git check-ignore -v data/loan_data_2007_2014.csv
```

- [ ] **Step 5: Record baseline execution evidence**

Use the already-validated current notebooks as the baseline:

```bash
conda run -n portfolio jupyter nbconvert --to notebook --execute notebooks/00_data_preparation.ipynb --output-dir /tmp/pd-baseline --ExecutePreprocessor.kernel_name=python3 --ExecutePreprocessor.timeout=900
```

Expected: exit 0. The remaining current notebooks were previously validated in the same environment; the integration stage revalidates the complete replacement sequence.

---

### Task 2: Build Data Understanding and Cleaning Notebooks

**Files:**
- Create: `notebooks/00_data_understanding_and_preparation.ipynb`
- Create: `notebooks/01_data_cleaning_and_target_definition.ipynb`
- Read only: `/Users/joseclaudio/Dev_local/Credit_Risk/Data/Credit Risk Modeling - Preparation - With Comments - 3-1.ipynb`
- Read only: `/Users/joseclaudio/Dev_local/Credit_Risk/PD_Data_Model.ipynb`
- Report privately: task report and cell-coverage map in the plan workspace.

**Interfaces:**
- Consumes: raw CSV at `../data/loan_data_2007_2014.csv`.
- Produces:
  - `../data/processed/clean_inputs_train.pkl`
  - `../data/processed/clean_inputs_test.pkl`
  - `../data/processed/targets_train.pkl`
  - `../data/processed/targets_test.pkl`

- [ ] **Step 1: Create a failing structural check**

Run before creating the notebooks:

```bash
test -f notebooks/00_data_understanding_and_preparation.ipynb
test -f notebooks/01_data_cleaning_and_target_definition.ipynb
```

Expected: failure because both new files are absent.

- [ ] **Step 2: Build notebook 00 from the assigned source cells**

Create focused markdown and code cells covering:

```text
dataset context -> shape/head/tail/columns/info -> missingness overview
employment length -> term -> earliest credit line -> issue date
future two-digit-year correction -> selected descriptive checks -> conclusions
```

Use `REFERENCE_DATE = pd.Timestamp("2017-12-01")`. For parsed earliest-credit-line dates greater than the reference date, subtract `pd.DateOffset(years=100)` before calculating rounded months since the reference date.

- [ ] **Step 3: Build notebook 01 and its exact data contract**

The notebook must:

```text
load raw data
repeat only deterministic conversions required for reproducibility
define good_bad
split inputs/target with test_size=0.20, random_state=42, stratify=good_bad
fit annual_inc mean on training rows only
apply that mean to training and held-out rows
fill total_rev_hi_lim from funded_amnt row by row
fill emp_length_int and event-count fields with zero
verify selected missingness and dtypes
create data/processed
write the four named pickle checkpoints
```

Event-count fields are `acc_now_delinq`, `total_acc`, `pub_rec`, `open_acc`, `inq_last_6mths`, and `delinq_2yrs`.

- [ ] **Step 4: Validate notebook JSON and source coverage**

```bash
jq -e '.nbformat == 4 and (.cells | length) > 0' notebooks/00_data_understanding_and_preparation.ipynb
jq -e '.nbformat == 4 and (.cells | length) > 0' notebooks/01_data_cleaning_and_target_definition.ipynb
rg -n '/Users/|Would you like|TODO|TBD' notebooks/00_data_understanding_and_preparation.ipynb notebooks/01_data_cleaning_and_target_definition.ipynb
```

Expected: both `jq` checks pass; `rg` returns no matches.

- [ ] **Step 5: Execute both notebooks in order**

```bash
conda run -n portfolio jupyter nbconvert --to notebook --execute notebooks/00_data_understanding_and_preparation.ipynb --output-dir /tmp/pd-task-a --ExecutePreprocessor.kernel_name=python3 --ExecutePreprocessor.timeout=900
conda run -n portfolio jupyter nbconvert --to notebook --execute notebooks/01_data_cleaning_and_target_definition.ipynb --output-dir /tmp/pd-task-a --ExecutePreprocessor.kernel_name=python3 --ExecutePreprocessor.timeout=900
```

Copy the successful executed notebooks back to their tracked paths and verify all code cells executed with zero error outputs.

- [ ] **Step 6: Commit only the assigned notebooks**

```bash
git add notebooks/00_data_understanding_and_preparation.ipynb notebooks/01_data_cleaning_and_target_definition.ipynb
git commit -m "docs: restore detailed PD data preparation"
```

---

### Task 3: Build Discrete and Continuous WoE Notebooks

**Files:**
- Create: `notebooks/02_discrete_feature_engineering_and_woe.ipynb`
- Create: `notebooks/03_continuous_feature_engineering_and_woe.ipynb`
- Read only: `/Users/joseclaudio/Dev_local/Credit_Risk/PD_Data_Model.ipynb`
- Report privately: task report and cell-coverage map in the plan workspace.

**Interfaces:**
- Consumes Task 2 checkpoints.
- Produces:
  - `../data/processed/discrete_inputs_train.pkl`
  - `../data/processed/discrete_inputs_test.pkl`
  - `../data/processed/model_inputs_train.pkl`
  - `../data/processed/model_inputs_test.pkl`
  - unchanged target checkpoints from Task 2.

- [ ] **Step 1: Create a failing structural check**

```bash
test -f notebooks/02_discrete_feature_engineering_and_woe.ipynb
test -f notebooks/03_continuous_feature_engineering_and_woe.ipynb
```

Expected: failure because both new files are absent.

- [ ] **Step 2: Implement the notebook-local WoE interfaces**

Both notebooks use functions with these interfaces:

```python
def woe_discrete(inputs: pd.DataFrame, feature: str, target: pd.Series) -> pd.DataFrame:
    """Return category counts, good/bad distributions, WoE, and feature IV."""

def woe_ordered_continuous(inputs: pd.DataFrame, feature: str, target: pd.Series) -> pd.DataFrame:
    """Return ordered-bin counts, good/bad distributions, WoE, and feature IV."""

def plot_by_woe(table: pd.DataFrame, rotation: int = 0) -> None:
    """Plot WoE in table order with readable labels."""
```

Zero distributions must be clipped to a documented small positive value before taking logarithms.

- [ ] **Step 3: Build notebook 02 with complete discrete coverage**

Preserve the manual grade derivation and analyze:

```text
grade
home_ownership
addr_state
verification_status
purpose
initial_list_status
```

Preserve category grouping and reference reasoning, calculate an IV summary, apply train-derived groups unchanged to held-out rows, and save the two discrete checkpoint files.

- [ ] **Step 4: Build notebook 03 with complete continuous coverage**

Analyze and conclude on:

```text
term_int
emp_length_int
mths_issue_date
int_rate
funded_amnt
mths_earliest_cr_line_date
installment
delinq_2yrs
inq_last_6mths
open_acc
pub_rec
total_acc
acc_now_delinq
total_rev_hi_lim
annual_inc
mths_since_last_delinq
dti
mths_since_last_record
```

Use the original coarse-class boundaries unless an approved correction is required. Correct the mislabeled `delinq_2yrs:>=4` condition to test `>=4`. Preserve the conclusion that funded amount lacks useful monotonic discriminatory structure. Save the two final model-input checkpoint files.

- [ ] **Step 5: Validate structure and assigned coverage**

```bash
jq -e '.nbformat == 4 and (.cells | length) >= 20' notebooks/02_discrete_feature_engineering_and_woe.ipynb
jq -e '.nbformat == 4 and (.cells | length) >= 30' notebooks/03_continuous_feature_engineering_and_woe.ipynb
rg -n '/Users/|Would you like|TODO|TBD' notebooks/02_discrete_feature_engineering_and_woe.ipynb notebooks/03_continuous_feature_engineering_and_woe.ipynb
```

Expected: both `jq` checks pass; `rg` returns no matches.

- [ ] **Step 6: Commit only the assigned notebooks**

Full execution occurs after Task 2 merges. Validate Python syntax in every code cell before committing:

```bash
conda run -n portfolio python -c "import ast, nbformat; [ast.parse(''.join(c.source)) for p in ['notebooks/02_discrete_feature_engineering_and_woe.ipynb','notebooks/03_continuous_feature_engineering_and_woe.ipynb'] for c in nbformat.read(p, as_version=4).cells if c.cell_type == 'code']"
git add notebooks/02_discrete_feature_engineering_and_woe.ipynb notebooks/03_continuous_feature_engineering_and_woe.ipynb
git commit -m "docs: restore detailed PD feature engineering"
```

---

### Task 4: Build Model Validation and Scorecard Notebooks

**Files:**
- Create: `notebooks/04_pd_logistic_regression_and_validation.ipynb`
- Create: `notebooks/05_pd_scorecard_and_final_conclusions.ipynb`
- Read only: `/Users/joseclaudio/Dev_local/Credit_Risk/Credit Risk Modeling - PD Model - With Comments - 6-2.ipynb`
- Read only for clarification: `/Users/joseclaudio/Dev_local/Credit_Risk/PD Model.ipynb`
- Report privately: task report and cell-coverage map in the plan workspace.

**Interfaces:**
- Consumes Task 3 model inputs and Task 2 targets.
- Produces:
  - `../data/processed/pd_model.pkl`
  - `../data/processed/model_feature_names.pkl`
  - `../data/processed/reference_categories.pkl`
  - `../data/processed/validation_predictions.pkl`

- [ ] **Step 1: Create a failing structural check**

```bash
test -f notebooks/04_pd_logistic_regression_and_validation.ipynb
test -f notebooks/05_pd_scorecard_and_final_conclusions.ipynb
```

Expected: failure because both new files are absent.

- [ ] **Step 2: Build notebook 04 from the original full candidate inventory**

The notebook must:

```text
load model matrices and targets
select the original full candidate feature list
drop one explicit reference category per feature family
fit the initial logistic model
report intercept, coefficients, and p-values
remove original non-significant feature families with preserved reasoning
fit the final model
predict held-out P(good) and PD = 1 - P(good)
report confusion matrices, threshold accuracy, ROC/AUC, Gini, cumulative curves, and KS
save model, feature names, references, and validation predictions
```

The reduced five-feature specification currently published must not replace the original candidate inventory.

- [ ] **Step 3: Build notebook 05 with complete scorecard arithmetic**

The notebook must:

```text
load the fitted model contract
add zero-coefficient reference categories
derive original feature-family names
set min_score=300 and max_score=850
calculate min/max coefficient sums
calculate preliminary and final category scores
show rounding reconciliation
score held-out accounts
relate score to P(good) and PD
interpret at least one example account
close with evidence-aligned final conclusions
```

Exclude LGD, EAD, Expected Loss, FastAPI, DuckDB, and interactive delivery.

- [ ] **Step 4: Validate structure and source coverage**

```bash
jq -e '.nbformat == 4 and (.cells | length) >= 20' notebooks/04_pd_logistic_regression_and_validation.ipynb
jq -e '.nbformat == 4 and (.cells | length) >= 15' notebooks/05_pd_scorecard_and_final_conclusions.ipynb
rg -n '/Users/|Would you like|TODO|TBD|LGD|EAD|Expected Loss|FastAPI|DuckDB' notebooks/04_pd_logistic_regression_and_validation.ipynb notebooks/05_pd_scorecard_and_final_conclusions.ipynb
```

Expected: both `jq` checks pass; `rg` returns no matches.

- [ ] **Step 5: Commit only the assigned notebooks**

```bash
conda run -n portfolio python -c "import ast, nbformat; [ast.parse(''.join(c.source)) for p in ['notebooks/04_pd_logistic_regression_and_validation.ipynb','notebooks/05_pd_scorecard_and_final_conclusions.ipynb'] for c in nbformat.read(p, as_version=4).cells if c.cell_type == 'code']"
git add notebooks/04_pd_logistic_regression_and_validation.ipynb notebooks/05_pd_scorecard_and_final_conclusions.ipynb
git commit -m "docs: restore detailed PD model and scorecard"
```

---

### Task 5: Merge Notebook Branches and Update Documentation

**Files:**
- Delete:
  - `notebooks/00_data_preparation.ipynb`
  - `notebooks/01_data_cleaning_and_exploration.ipynb`
  - `notebooks/02_feature_engineering_and_woe.ipynb`
  - `notebooks/03_pd_logistic_regression.ipynb`
  - `notebooks/04_pd_validation_and_scorecard.ipynb`
- Modify: `.gitignore`
- Modify: `README.md`
- Modify: `Final_Report.md`
- Create locally only: `recommendations.md`

**Interfaces:**
- Consumes: three reviewed notebook-pair commits.
- Produces: one six-notebook integration branch, current public documentation, and a private recommendations document.

- [ ] **Step 1: Merge notebook commits in dependency order**

```bash
git merge --no-ff agent/pd-data-foundation
git merge --no-ff agent/pd-woe-engineering
git merge --no-ff agent/pd-model-scorecard
```

Expected: no file conflicts because notebook scopes do not overlap.

- [ ] **Step 2: Remove the five superseded notebooks**

Delete exactly the five old paths listed above. Keep all six new notebook paths.

- [ ] **Step 3: Update `.gitignore` before creating private recommendations**

Add exactly:

```gitignore
data/processed/
/recommendations.md
```

Verify both rules with `git check-ignore`.

- [ ] **Step 4: Rewrite README methodology and workflow**

The README must contain:

```text
project introduction
scope and business context
six-notebook workflow table
methodology
fresh results after Task 6
reproducibility
concise project-specific limitations
```

Remove `Skills demonstrated` and `Future work`. Do not mention the private recommendations file.

- [ ] **Step 5: Create the private recommendations document**

Cover:

```text
LGD definition, target, recovery/cost data, candidate methods
EAD definition, timing, exposure data, installment/revolving distinctions
EL = PD x LGD x EAD
recommended implementation order and stopping points
FastAPI, DuckDB, and interactive options
data requirements, decisions, and validation gates
```

Confirm `git status --ignored --short recommendations.md` reports it ignored.

- [ ] **Step 6: Align `Final_Report.md`**

Update notebook names, methodology, and narrative. Retain the existing metric
values unchanged on the private integration branch; Task 6 must replace them
with the newly executed values before the documentation commit is accepted.

- [ ] **Step 7: Commit only public documentation changes**

```bash
git add .gitignore README.md Final_Report.md notebooks/00_data_preparation.ipynb notebooks/01_data_cleaning_and_exploration.ipynb notebooks/02_feature_engineering_and_woe.ipynb notebooks/03_pd_logistic_regression.ipynb notebooks/04_pd_validation_and_scorecard.ipynb
git commit -m "docs: reorganize detailed PD notebook workflow"
```

Do not stage `recommendations.md`.

---

### Task 6: Execute the Integrated Pipeline and Freeze Reproduced Results

**Files:**
- Modify with executed outputs: all six new notebooks.
- Modify with reproduced metrics: `README.md`
- Modify with reproduced metrics: `Final_Report.md`
- Generate ignored: `data/processed/*`

**Interfaces:**
- Consumes: merged notebook sources and raw CSV.
- Produces: executed notebooks, consistent metrics, and reproducible checkpoints.

- [ ] **Step 1: Start from an empty processed-data directory**

If `data/processed/` exists, move it to a uniquely named directory under `/tmp`; then recreate an empty `data/processed/`.

- [ ] **Step 2: Execute all six notebooks fail-fast**

From `notebooks/`, run in this exact order:

```text
00_data_understanding_and_preparation.ipynb
01_data_cleaning_and_target_definition.ipynb
02_discrete_feature_engineering_and_woe.ipynb
03_continuous_feature_engineering_and_woe.ipynb
04_pd_logistic_regression_and_validation.ipynb
05_pd_scorecard_and_final_conclusions.ipynb
```

For each file:

```bash
conda run -n portfolio jupyter nbconvert --to notebook --execute NOTEBOOK --output-dir EXECUTED_DIR --ExecutePreprocessor.kernel_name=python3 --ExecutePreprocessor.timeout=900
```

Stop immediately on the first non-zero exit. Copy back only after all six complete.

- [ ] **Step 3: Validate saved execution state**

For each tracked notebook, assert:

```jq
([.cells[] | select(.cell_type == "code" and .execution_count == null)] | length) == 0
and
([.cells[].outputs[]? | select(.output_type == "error")] | length) == 0
```

- [ ] **Step 4: Extract reproduced model metrics**

Read the named AUC, Gini, KS, threshold, confusion-matrix, and score-range outputs from notebook 04/05. Replace every stale metric in README and `Final_Report.md`, and remove `RESULTS_FROM_EXECUTED_NOTEBOOK_04`.

- [ ] **Step 5: Verify public/private boundaries**

```bash
git status --short --ignored
git check-ignore -v recommendations.md data/processed/
rg -n '/Users/|recommendations.md|RESULTS_FROM_EXECUTED_NOTEBOOK_04' README.md Final_Report.md notebooks/*.ipynb
```

Expected: private paths ignored; no forbidden public matches. Confirm the
existing metrics are replaced by comparing README and `Final_Report.md` with
the named outputs from executed notebooks 04 and 05.

- [ ] **Step 6: Commit executed notebooks and reproduced documentation**

```bash
git add notebooks/00_data_understanding_and_preparation.ipynb notebooks/01_data_cleaning_and_target_definition.ipynb notebooks/02_discrete_feature_engineering_and_woe.ipynb notebooks/03_continuous_feature_engineering_and_woe.ipynb notebooks/04_pd_logistic_regression_and_validation.ipynb notebooks/05_pd_scorecard_and_final_conclusions.ipynb README.md Final_Report.md
git commit -m "docs: publish complete executed PD analysis"
```

---

### Task 7: Run Independent Source and Technical Audits

**Files:**
- Read: both authoritative source notebooks.
- Read: all six rebuilt notebooks.
- Create privately: source audit report.
- Create privately: technical audit report.

**Interfaces:**
- Consumes: complete integrated branch.
- Produces: two independent verdicts with exact findings and evidence.

- [ ] **Step 1: Dispatch the source-coverage auditor**

Use GPT-5.6 Sol high with no implementation-agent history. Require:

```text
cell-by-cell classification for both truth sources
feature-by-feature coverage
conclusion preservation
consolidation/correction justification
PASS or FAIL
```

- [ ] **Step 2: Dispatch the technical auditor independently**

Use GPT-5.6 Sol high with no implementation-agent history. Require checks for:

```text
sequential execution contract
train/test separation and preprocessing leakage
WoE/IV formulas and zero handling
coarse-class completeness and exclusivity
model target direction
reference categories and p-values
AUC/Gini/KS/confusion calculations
scorecard arithmetic
README/report consistency
public/private Git boundary
PASS or FAIL
```

- [ ] **Step 3: Gate acceptance**

Both reports must say PASS with no unresolved material finding. Minor wording findings may be included in the single fix wave; none are silently discarded.

---

### Task 8: Apply One Coordinated Fix Wave and Re-review

**Files:**
- Modify only paths named by audit findings.
- Create privately: fix report and scoped re-review report.

**Interfaces:**
- Consumes: complete findings list from both audits.
- Produces: one reviewed correction commit.

- [ ] **Step 1: Dispatch one GPT-5.6 Terra medium fixer**

Give the fixer both audit reports, the design spec, and exact integration worktree path. Require a single fix commit and fresh covering execution/check evidence.

- [ ] **Step 2: Run one independent scoped re-review**

Use GPT-5.6 Sol high. Every original finding must be marked `ADDRESSED` or `NOT ADDRESSED`; new material breakage fails the gate.

- [ ] **Step 3: Stop on unresolved material findings**

Do not merge or push if re-review leaves a substantive source-coverage, correctness, execution, or public/private-boundary issue.

---

### Task 9: Final Clean Validation, Merge, Push, and Remote Proof

**Files:**
- Potentially modify executed outputs in all six notebooks.
- Copy locally only: `recommendations.md` into the surviving main checkout.

**Interfaces:**
- Consumes: audit-approved integration branch.
- Produces: final `main`, public GitHub notebooks with outputs, and a retained private recommendations file.

- [ ] **Step 1: Perform the final clean full execution**

Move current `data/processed/` to `/tmp`, recreate it empty, execute notebooks `00`–`05` fail-fast into a new temporary execution directory, and copy all six successful executed copies back.

- [ ] **Step 2: Run final output and content assertions**

Verify for all six:

```text
valid nbformat 4 JSON
every code cell executed
zero error outputs
at least one saved output where the notebook contains display/plot code
no absolute local paths
no private roadmap content
```

Verify README and `Final_Report.md` metrics exactly match notebook outputs.

- [ ] **Step 3: Commit only if final execution changed tracked outputs**

```bash
git add notebooks/00_data_understanding_and_preparation.ipynb notebooks/01_data_cleaning_and_target_definition.ipynb notebooks/02_discrete_feature_engineering_and_woe.ipynb notebooks/03_continuous_feature_engineering_and_woe.ipynb notebooks/04_pd_logistic_regression_and_validation.ipynb notebooks/05_pd_scorecard_and_final_conclusions.ipynb README.md Final_Report.md
git commit -m "docs: refresh final validated notebook outputs"
```

Skip this commit if the staged diff is empty.

- [ ] **Step 4: Verify authorship and tracked scope**

```bash
git status --short --branch
git diff --check main...HEAD
git log main..HEAD --format='%H%x09%an%x09%ae%x09%s%n%b'
git ls-files | rg 'recommendations.md|docs/superpowers|data/processed|\\.pkl$|loan_data_2007_2014\\.csv$'
```

Expected: clean integration branch, no whitespace errors, only `jclaudio` authorship, and no private/generated matches.

- [ ] **Step 5: Merge the approved integration branch to main**

Merge without adding AI attribution. Copy the ignored `recommendations.md` into the surviving main checkout after the merge and confirm it remains ignored.

- [ ] **Step 6: Push main to GitHub**

```bash
git push origin main
```

- [ ] **Step 7: Prove the remote upload and outputs**

```bash
git fetch origin main
git rev-parse HEAD
git rev-parse origin/main
git ls-remote origin refs/heads/main
```

For every notebook path, inspect the remote object:

```bash
git show origin/main:notebooks/NOTEBOOK.ipynb | jq -e '
  ([.cells[] | select(.cell_type == "code" and .execution_count == null)] | length) == 0
  and
  ([.cells[].outputs[]? | select(.output_type == "error")] | length) == 0
  and
  ([.cells[].outputs[]?] | length) > 0
'
```

Also verify the remote tree excludes:

```text
recommendations.md
docs/superpowers/
data/processed/
raw CSV/XLSX data
pickle/joblib model artifacts
```

- [ ] **Step 8: Report final evidence**

Report:

```text
final commit SHA
GitHub repository URL
six notebook PASS lines
source audit verdict
technical audit verdict
remote output verification
private recommendations retained locally
Blockers: none
```
