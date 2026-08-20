# Credit Risk Portfolio Business Case and Model Artifacts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a business-first credit-risk case study and a lightweight, inspectable representation of the final PD model without committing the 513 MB Statsmodels pickle.

**Architecture:** Notebook 05 remains the reproducible export boundary because it already reconstructs the fitted coefficient table and scorecard from the final model contract. It will write deterministic CSV/JSON artifacts to a tracked `model/` directory. `Final_Report.md` becomes the canonical portfolio-case source, `README.md` remains the concise repository entry point, and `recommendations.md` remains an ignored private roadmap.

**Tech Stack:** Jupyter Notebook, Python 3.12, pandas, NumPy, Statsmodels Logit, scikit-learn metrics, CSV, JSON, Markdown, Git.

## Global Constraints

- Keep the public work educational and portfolio-oriented; do not present it as an underwriting policy, regulatory model, or production decision system.
- Describe WoE as the method used to examine risk ordering and guide grouping/coarse classing.
- Describe IV as a descriptive feature-level diagnostic, not an automatic feature-selection rule.
- State that the logistic regression uses one-hot grouped categories, not numerical WoE-transformed values.
- State that consistently non-significant feature families were removed after the initial full-rank Logit review.
- Preserve `PD = 1 - P(good)` throughout.
- Do not commit the approximately 513 MB `pd_model.pkl`, raw data, processed checkpoints, private recommendations, or `docs/superpowers`.
- Do not add FastAPI, DuckDB, LGD, EAD, expected loss, a website implementation, or raw-loan production scoring.
- Preserve executed notebook outputs; regenerate only through a complete ordered run when required for a correct export.
- Use only `jclaudio <jclaudio@brainlessqi.com>` for any authorized commit; never add Codex, AI, or co-author attribution.

---

## File map

- Modify `notebooks/05_pd_scorecard_and_final_conclusions.ipynb`
  - Export the final model coefficients, scorecard, and metadata from the same in-memory objects used for scoring.
- Create `model/pd_model_coefficients.csv`
  - Public estimated parameter table, including the intercept and p-values.
- Create `model/scorecard.csv`
  - Public scorecard table, including zero-coefficient reference categories and final integer points.
- Create `model/model_metadata.json`
  - Public model direction, population, metrics, references, score range, versions, and limitations.
- Create `model/README.md`
  - Explain the model bundle and its raw-input scoring limitation.
- Modify `Final_Report.md`
  - Canonical business-first portfolio case study.
- Modify `README.md`
  - Concise repository entry point with headline evidence and links.
- Modify ignored `recommendations.md`
  - Preserve LGD/EAD/EL and delivery guidance while adding the immediate portfolio and PD-strengthening sequence.

---

### Task 1: Export the lightweight model bundle from Notebook 05

**Files:**
- Modify: `notebooks/05_pd_scorecard_and_final_conclusions.ipynb`
- Create: `model/pd_model_coefficients.csv`
- Create: `model/scorecard.csv`
- Create: `model/model_metadata.json`
- Create: `model/README.md`

**Interfaces:**
- Consumes: `model`, `model_feature_names`, `reference_categories`, `validation_predictions`, `scorecard`, `final_min`, `final_max`, and `scored_accounts` created by existing Notebook 05 cells.
- Produces:
  - `model/pd_model_coefficients.csv` with columns `feature`, `coefficient`, `p_value`;
  - `model/scorecard.csv` with columns `feature`, `original_feature`, `coefficient`, `score_final`;
  - `model/model_metadata.json` with the exact schema specified below;
  - a freshly executed Notebook 05 with the export confirmation saved in its output.

- [ ] **Step 1: Read the notebook-editing instructions and establish the failing artifact check**

Use the `jupyter-notebook` skill before editing the notebook.

Run:

```bash
test ! -e model/pd_model_coefficients.csv
test ! -e model/scorecard.csv
test ! -e model/model_metadata.json
```

Expected: all three checks pass because the public model bundle does not yet exist.

- [ ] **Step 2: Add deterministic export imports to Notebook 05**

Extend the first code cell imports with:

```python
import json
import platform
import sklearn
import statsmodels
from sklearn.metrics import roc_auc_score
```

Do not remove or reorder the existing model-loading logic.

- [ ] **Step 3: Add the public artifact export cell after scorecard validation and held-out scoring**

Insert one markdown cell titled `## Export the lightweight public model bundle`
after the held-out scoring and score/PD validation cells. Explain that the
bundle is inspectable but does not accept raw loan applications.

Insert one code cell with this logic:

```python
public_model_dir = Path("../model")
public_model_dir.mkdir(exist_ok=True)

coefficients = pd.DataFrame(
    {
        "feature": model.params.index,
        "coefficient": model.params.to_numpy(),
        "p_value": model.pvalues.to_numpy(),
    }
)

scorecard_export = scorecard[
    ["feature", "original_feature", "coefficient", "score_final"]
].copy()

auc = roc_auc_score(
    validation_predictions["actual_good"],
    validation_predictions["p_good"],
)
gini = 2 * auc - 1

ks_frame = validation_predictions.sort_values("p_good").reset_index(drop=True).copy()
ks_frame["cumulative_good"] = (
    ks_frame["actual_good"].cumsum() / ks_frame["actual_good"].sum()
)
ks_frame["cumulative_bad"] = (
    (1 - ks_frame["actual_good"]).cumsum()
    / (1 - ks_frame["actual_good"]).sum()
)
ks = (ks_frame["cumulative_bad"] - ks_frame["cumulative_good"]).max()

predicted_good = (validation_predictions["p_good"] >= 0.5).astype(int)
bad_mask = validation_predictions["actual_good"].eq(0)
bad_detected = int((predicted_good[bad_mask] == 0).sum())
bad_total = int(bad_mask.sum())

metadata = {
    "artifact_version": "1.0.0",
    "model_type": "Unpenalized binary logistic regression (Statsmodels Logit)",
    "target": {
        "name": "good_bad",
        "good_label": 1,
        "bad_label": 0,
        "model_output": "P(good)",
        "pd_definition": "1 - P(good)",
    },
    "population": {
        "training_rows": int(model.nobs),
        "held_out_rows": int(len(validation_predictions)),
        "total_rows": int(model.nobs + len(validation_predictions)),
    },
    "model_contract": {
        "estimated_feature_count_excluding_intercept": len(model_feature_names),
        "estimated_parameter_count_including_intercept": len(model.params),
        "reference_categories": reference_categories,
    },
    "held_out_metrics": {
        "auc": float(auc),
        "gini": float(gini),
        "ks": float(ks),
        "displayed_p_good_threshold": 0.5,
        "bad_detected": bad_detected,
        "bad_total": bad_total,
        "bad_recall": bad_detected / bad_total,
    },
    "scorecard": {
        "minimum": int(final_min),
        "maximum": int(final_max),
        "basis": "Theoretical per-family coefficient extrema including the intercept",
    },
    "library_versions": {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "scikit_learn": sklearn.__version__,
        "statsmodels": statsmodels.__version__,
    },
    "source_notebook": "notebooks/05_pd_scorecard_and_final_conclusions.ipynb",
    "limitations": [
        "Historical educational PD proxy without a fixed performance horizon",
        "Random holdout rather than time-based validation",
        "Not calibrated as a production probability or scorecard",
        "Requires the engineered feature schema and does not score raw applications",
        "Not an underwriting, pricing, approval, or regulatory model",
    ],
}

coefficients.to_csv(
    public_model_dir / "pd_model_coefficients.csv",
    index=False,
    float_format="%.12g",
)
scorecard_export.to_csv(
    public_model_dir / "scorecard.csv",
    index=False,
    float_format="%.12g",
)
with (public_model_dir / "model_metadata.json").open("w", encoding="utf-8") as file:
    json.dump(metadata, file, indent=2, sort_keys=True)
    file.write("\n")

print("Exported public model bundle:", sorted(path.name for path in public_model_dir.iterdir()))
```

- [ ] **Step 4: Create the model bundle README**

Create `model/README.md` with these sections and facts:

```markdown
# Lightweight PD model artifacts

This directory contains an inspectable representation of the fitted historical
probability-of-default model.

## Files

- `pd_model_coefficients.csv`: the fitted intercept and feature coefficients,
  with Statsmodels p-values.
- `scorecard.csv`: all scorecard categories, including zero-coefficient
  reference categories and final integer points.
- `model_metadata.json`: the model direction, population, held-out metrics,
  reference categories, score range, library versions, and limitations.

## Intended use

These files make the fitted model and scorecard reviewable without committing
the approximately 513 MB Statsmodels results pickle. They support inspection
and reconstruction of calculations that already use the engineered feature
schema.

They are not a raw-loan scoring package. Raw inputs still require the cleaning,
category grouping, and coarse-classing workflow in notebooks 00 through 03.
The model is an educational historical analysis, not an underwriting,
approval, pricing, or regulatory system.
```

- [ ] **Step 5: Rebuild ignored checkpoints and execute Notebook 05**

From `notebooks/`, execute notebooks 00 through 04 into a temporary directory
from an empty `data/processed/` directory, then execute the modified Notebook
05 and save its executed copy back to the tracked notebook path.

Run each notebook with:

```bash
MPLCONFIGDIR=/tmp conda run -n portfolio jupyter nbconvert \
  --to notebook \
  --execute NOTEBOOK_NAME.ipynb \
  --output-dir EXECUTION_DIRECTORY \
  --ExecutePreprocessor.kernel_name=python3 \
  --ExecutePreprocessor.timeout=900
```

Expected: six sequential `PASS` results and the three public artifact files
plus `model/README.md`.

- [ ] **Step 6: Validate the artifact contract against the fitted checkpoints**

Run:

```bash
/Users/joseclaudio/opt/anaconda3/envs/portfolio/bin/python - <<'PY'
import json
import pickle
from pathlib import Path

import pandas as pd

root = Path(".")
processed = root / "data" / "processed"

with (processed / "pd_model.pkl").open("rb") as file:
    model = pickle.load(file)
with (processed / "model_feature_names.pkl").open("rb") as file:
    features = pickle.load(file)
with (processed / "reference_categories.pkl").open("rb") as file:
    references = pickle.load(file)

coefficients = pd.read_csv(root / "model" / "pd_model_coefficients.csv")
scorecard = pd.read_csv(root / "model" / "scorecard.csv")
metadata = json.loads((root / "model" / "model_metadata.json").read_text())

assert len(coefficients) == 85
assert coefficients["feature"].tolist() == list(model.params.index)
assert coefficients["coefficient"].round(10).tolist() == model.params.round(10).tolist()
assert coefficients["p_value"].round(10).tolist() == model.pvalues.round(10).tolist()
assert len(features) == 84
assert len(references) == 17
assert len(scorecard) == 102
assert set(references).issubset(set(scorecard["feature"]))
assert metadata["population"] == {
    "training_rows": 373028,
    "held_out_rows": 93257,
    "total_rows": 466285,
}
assert abs(metadata["held_out_metrics"]["auc"] - 0.699482203847858) < 1e-12
assert abs(metadata["held_out_metrics"]["gini"] - 0.398964407695716) < 1e-12
assert abs(metadata["held_out_metrics"]["ks"] - 0.2916524985747112) < 1e-12
assert metadata["held_out_metrics"]["bad_detected"] == 10
assert metadata["held_out_metrics"]["bad_total"] == 10194
assert metadata["scorecard"]["minimum"] == 300
assert metadata["scorecard"]["maximum"] == 850
assert not list((root / "model").glob("*.pkl"))
print("PASS: lightweight model bundle reconciles to the fitted model")
PY
```

Expected: `PASS: lightweight model bundle reconciles to the fitted model`.

- [ ] **Step 7: Commit the independently reviewable model bundle**

After task review approval:

```bash
git add notebooks/05_pd_scorecard_and_final_conclusions.ipynb \
  model/README.md \
  model/pd_model_coefficients.csv \
  model/scorecard.csv \
  model/model_metadata.json
git commit -m "feat: publish lightweight PD model artifacts"
```

---

### Task 2: Rewrite the public report as a portfolio business case

**Files:**
- Modify: `Final_Report.md`

**Interfaces:**
- Consumes: executed notebook evidence and `model/model_metadata.json`.
- Produces: a self-contained Markdown case study suitable as the copy source for a portfolio page modeled on the Retail Demand Forecasting presentation.

- [ ] **Step 1: Record the required report-evidence checks before rewriting**

Run:

```bash
rg -n "^## (Project summary|Business problem|Solution|Dataset and target|Methodology|Findings|Business implications|Conclusion|Limitations|Technologies|Notebook map)$" Final_Report.md
```

Expected: the command does not find the complete approved section set in the
current report.

- [ ] **Step 2: Rewrite `Final_Report.md` with the approved business-first structure**

Use these exact headings:

```markdown
# Credit Risk Probability-of-Default Case Study

## Project summary
## Headline evidence
## Business problem
## Solution
## Dataset and target
## Methodology
## Findings
## Business implications
## Conclusion
## Limitations
## Technologies
## Notebook map
```

The report must include:

- the decision question: whether historical borrower and loan characteristics
  can rank observed credit risk and translate model output into an
  interpretable score;
- 466,285 total rows, 373,028 training rows, and 93,257 held-out rows;
- `P(good)` as the model output and `PD = 1 - P(good)`;
- AUC `0.699482`, Gini `0.398964`, and KS `0.291652`;
- 10 detected bad loans out of 10,194 at the displayed 0.5 `P(good)` threshold;
- the illustrative 300–850 scorecard;
- the exact WoE/IV/model-selection distinction from the global constraints;
- grade IV `0.292145` as the strongest reviewed discrete diagnostic, without
  implying that IV selected the final features;
- removal of the delinquencies, open-account, public-record, total-account,
  and revolving-limit families because their dummy levels were all or almost
  all non-significant in the initial model;
- an explanation that moderate ranking ability and a poor displayed threshold
  can coexist;
- the business tradeoff between missed defaults and rejected good borrowers;
- clear historical, calibration, temporal-validation, fairness, and
  non-production limitations;
- a link to the public model bundle and the six executed notebooks.

Do not include private future-development steps, FastAPI, DuckDB, LGD, EAD, or
expected loss.

- [ ] **Step 3: Run a report accuracy and prohibited-copy check**

Run:

```bash
rg -n "WoE|Weight of Evidence|Information Value|one-hot|non-significant|0\\.699482|0\\.398964|0\\.291652|10 of 10,194|300–850|PD = 1 - P\\(good\\)|466,285" Final_Report.md
! rg -ni "IV selected|trained on WoE|production-ready|deployment-ready|FastAPI|DuckDB|LGD|EAD|expected loss|recommendations\\.md" Final_Report.md
```

Expected: every required concept is found and no prohibited wording is found.

- [ ] **Step 4: Cross-check every numeric claim against metadata**

Run:

```bash
/Users/joseclaudio/opt/anaconda3/envs/portfolio/bin/python - <<'PY'
import json
from pathlib import Path

report = Path("Final_Report.md").read_text()
metadata = json.loads(Path("model/model_metadata.json").read_text())

required = {
    "466,285": metadata["population"]["total_rows"],
    "373,028": metadata["population"]["training_rows"],
    "93,257": metadata["population"]["held_out_rows"],
    "0.699482": metadata["held_out_metrics"]["auc"],
    "0.398964": metadata["held_out_metrics"]["gini"],
    "0.291652": metadata["held_out_metrics"]["ks"],
    "10 of 10,194": (
        metadata["held_out_metrics"]["bad_detected"],
        metadata["held_out_metrics"]["bad_total"],
    ),
    "300–850": (
        metadata["scorecard"]["minimum"],
        metadata["scorecard"]["maximum"],
    ),
}
for text, source in required.items():
    assert text in report, (text, source)
print("PASS: report evidence matches model metadata")
PY
```

Expected: `PASS: report evidence matches model metadata`.

- [ ] **Step 5: Commit the portfolio case study**

After task review approval:

```bash
git add Final_Report.md
git commit -m "docs: frame PD analysis as a business case"
```

---

### Task 3: Align the repository entry point and private roadmap

**Files:**
- Modify: `README.md`
- Modify ignored: `recommendations.md`

**Interfaces:**
- Consumes: `Final_Report.md`, the six-notebook workflow, and `model/README.md`.
- Produces: a concise public repository entry point and a private next-step roadmap that is never tracked.

- [ ] **Step 1: Update the public README**

Keep the README compact and add:

- the business decision question;
- headline evidence: 466,285 rows, AUC 0.699482, Gini 0.398964, KS 0.291652,
  and the illustrative 300–850 scorecard;
- a direct link to `Final_Report.md`;
- a direct link to `model/README.md`;
- the corrected WoE/IV/model-selection distinction;
- the existing six-notebook map and reproducibility instructions;
- the existing limitations.

Do not duplicate the full findings or business-implications discussion.

- [ ] **Step 2: Organize the ignored private recommendations into sequenced horizons**

Preserve the existing LGD, EAD, expected-loss, FastAPI, DuckDB, and interactive
delivery guidance. Add this sequence near the top:

```markdown
## Recommended development sequence

### 1. Publish the portfolio case

- Use `Final_Report.md` as the copy source for a credit-risk project page that
  follows the Retail Demand Forecasting case-study structure.
- Use the public CSV/JSON model bundle for tables and downloadable evidence.
- Keep the current case static; do not imply that raw applications can be
  scored from the website.

### 2. Strengthen PD

- Define a fixed performance horizon and observation date.
- Add time-based validation and calibration analysis.
- Choose operating thresholds only after defining the relative cost of missed
  defaults and rejected good borrowers.
- Package raw-input preprocessing only after these checks are stable.

### 3. Expand the loss framework

Proceed to LGD, EAD, and expected loss only after the PD definition and
validation gates are stable.

### 4. Add delivery

Add FastAPI, DuckDB, and an interactive view only after the analytical
contracts and lightweight scoring bundle are reproducible.
```

- [ ] **Step 3: Verify public/private boundaries and link integrity**

Run:

```bash
rg -n "Final_Report\\.md|model/README\\.md|0\\.699482|0\\.398964|0\\.291652|300–850|Weight of Evidence|Information Value" README.md
git check-ignore -q recommendations.md
! git ls-files --error-unmatch recommendations.md
! rg -ni "FastAPI|DuckDB|LGD|EAD|expected loss|recommendations\\.md" README.md Final_Report.md model/README.md
```

Expected: public links and evidence are present, the recommendations file is
ignored and untracked, and private roadmap topics are absent from public copy.

- [ ] **Step 4: Commit only the public README**

After task review approval:

```bash
git add README.md
git commit -m "docs: align credit risk portfolio entry point"
```

Do not stage or commit `recommendations.md`.

---

### Task 4: Run the final portfolio publication audit

**Files:**
- Validate: `README.md`
- Validate: `Final_Report.md`
- Validate: `model/README.md`
- Validate: `model/pd_model_coefficients.csv`
- Validate: `model/scorecard.csv`
- Validate: `model/model_metadata.json`
- Validate: `notebooks/*.ipynb`
- Validate ignored: `recommendations.md`

**Interfaces:**
- Consumes: all outputs from Tasks 1 through 3.
- Produces: evidence that the public repository is internally consistent, reproducible, and ready for a portfolio-site implementation.

- [ ] **Step 1: Validate every saved notebook**

Run:

```bash
/Users/joseclaudio/opt/anaconda3/envs/portfolio/bin/python - <<'PY'
from pathlib import Path
import nbformat

total_code = 0
total_outputs = 0
for path in sorted(Path("notebooks").glob("*.ipynb")):
    notebook = nbformat.read(path, 4)
    nbformat.validate(notebook)
    code = [cell for cell in notebook.cells if cell.cell_type == "code"]
    for cell in code:
        compile(cell.source, f"{path.name}:{cell.id}", "exec")
    counts = [cell.execution_count for cell in code]
    assert counts == list(range(1, len(code) + 1)), (path.name, counts)
    errors = [
        output
        for cell in code
        for output in cell.get("outputs", [])
        if output.output_type == "error"
    ]
    assert not errors, (path.name, errors)
    outputs = sum(len(cell.get("outputs", [])) for cell in code)
    total_code += len(code)
    total_outputs += outputs
    print(f"PASS {path.name}: code={len(code)} outputs={outputs} errors=0")
assert total_code >= 76
assert total_outputs >= 116
print(f"PASS notebook totals: code={total_code} outputs={total_outputs}")
PY
```

Expected: all six notebooks validate, Notebook 05 includes the executed export
cell, and no saved error output exists.

- [ ] **Step 2: Re-run artifact and documentation reconciliation**

Repeat Task 1 Step 6, Task 2 Steps 3–4, and Task 3 Step 3.

Expected: all checks pass without modifying files.

- [ ] **Step 3: Verify Git hygiene and authorship**

Run:

```bash
git diff --check
git status --short
git check-ignore -q recommendations.md
git check-ignore -q data/processed/pd_model.pkl
git check-ignore -q docs/superpowers/plans/2026-07-30-portfolio-business-case-and-model-artifacts.md
! git ls-files | rg '(^|/)(recommendations\\.md|docs/superpowers|data/processed|loan_data_2007_2014\\.csv|pd_model\\.pkl)$'
git log --format='%an <%ae>' | sort -u
```

Expected:

- the only uncommitted file is ignored `recommendations.md`, which does not
  appear in `git status`;
- no private or large binary artifact is tracked;
- public commits use only `jclaudio <jclaudio@brainlessqi.com>`.

- [ ] **Step 4: Independent final review**

Dispatch two read-only reviews:

1. Business-case reviewer:
   - compare `Final_Report.md` with the approved design and the live Retail
     Demand Forecasting case-study structure;
   - verify employer-facing clarity and credible business interpretation.
2. Technical evidence reviewer:
   - reconcile notebook outputs, CSV/JSON artifacts, metrics, target direction,
     WoE/IV framing, references, scorecard endpoints, and public/private
     boundaries.

Expected: both reviewers return `APPROVE` with zero Critical or Important
findings. Address any material findings with one coordinated fix and re-review.

- [ ] **Step 5: Publish only after authorization**

Confirm the branch is clean and the authorized commits contain only the public
files. Push only if the user has explicitly authorized publication for this
implementation:

```bash
git push origin main
git fetch origin main
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
```

Expected: local and remote `main` resolve to the same commit.
