# Credit Risk Notebook Transfer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transfer the completed PD analysis into a simple, standalone, GitHub-ready repository built around five numbered notebooks.

**Architecture:** The new repository remains notebook-led. Each notebook owns one visible stage of the analysis, local data stays under `data/` and is ignored by Git, and documentation summarizes the work without adding an application or Python package layer.

**Tech Stack:** Python, Jupyter, pandas, NumPy, SciPy, scikit-learn, statsmodels, Matplotlib, Seaborn

## Global Constraints

- Target repository: `/Users/joseclaudio/Dev_local/project_potfolio/credit_risk`.
- Source project: `/Users/joseclaudio/Dev_local/Credit_Risk`.
- Do not add FastAPI, DuckDB, Python application modules, or an outputs directory.
- Commit implementation work under the existing `jclaudio` Git identity only; do not add Codex attribution or co-author trailers. Do not push.
- Move only `Data/loan_data_2007_2014.csv` and `Data/LCDataDictionary (1).xlsx`.
- Exclude all datasets, pickles, saved models, caches, and generated artifacts from Git.
- Preserve original source notebooks and their outputs; create cleaned copies in the new repository.

---

### Task 1: Establish Repository Hygiene and Move Canonical Data

**Files:**
- Create: `/Users/joseclaudio/Dev_local/project_potfolio/credit_risk/.gitignore`
- Create: `/Users/joseclaudio/Dev_local/project_potfolio/credit_risk/data/README.md`
- Move: `/Users/joseclaudio/Dev_local/Credit_Risk/Data/loan_data_2007_2014.csv`
- Move: `/Users/joseclaudio/Dev_local/Credit_Risk/Data/LCDataDictionary (1).xlsx`

**Interfaces:**
- Consumes: the two approved canonical source files.
- Produces: local notebook inputs at `data/loan_data_2007_2014.csv` and `data/LCDataDictionary.xlsx`.

- [ ] **Step 1: Write the failing repository-hygiene check**

Create a temporary shell check that asserts the target data files exist and that `git check-ignore` excludes both.

- [ ] **Step 2: Run the check and verify it fails**

Run it from the empty target repository. Expected: failure because `data/` and the ignore rules do not exist yet.

- [ ] **Step 3: Add minimal ignore rules and data documentation**

Ignore local data files, notebook checkpoints, Python caches, environments, macOS metadata, and serialized model artifacts. Explain where the two local source files belong and that they are intentionally absent from GitHub.

- [ ] **Step 4: Move the two approved source files**

Move the 229 MB Lending Club CSV and data dictionary into the target `data/` directory. Rename only the dictionary to `LCDataDictionary.xlsx`.

- [ ] **Step 5: Verify hygiene**

Run `git status --short --ignored`, confirm both data files are present locally, and confirm neither appears as trackable content.

### Task 2: Create the Numbered Notebook Workflow

**Files:**
- Create: `/Users/joseclaudio/Dev_local/project_potfolio/credit_risk/notebooks/00_data_preparation.ipynb`
- Create: `/Users/joseclaudio/Dev_local/project_potfolio/credit_risk/notebooks/01_data_cleaning_and_exploration.ipynb`
- Create: `/Users/joseclaudio/Dev_local/project_potfolio/credit_risk/notebooks/02_feature_engineering_and_woe.ipynb`
- Create: `/Users/joseclaudio/Dev_local/project_potfolio/credit_risk/notebooks/03_pd_logistic_regression.ipynb`
- Create: `/Users/joseclaudio/Dev_local/project_potfolio/credit_risk/notebooks/04_pd_validation_and_scorecard.ipynb`

**Interfaces:**
- Consumes: `data/loan_data_2007_2014.csv`.
- Produces: a sequential PD analysis whose final notebook reports probability of default and scorecard interpretation.

- [ ] **Step 1: Write the failing notebook-contract test**

Create a temporary validation script that checks the five exact filenames, valid notebook JSON, ordered stage headings, local data path usage, and the presence of the `good_bad`, WoE/IV, logistic-regression, PD, AUC/Gini, and scorecard stages.

- [ ] **Step 2: Run the contract test and verify it fails**

Expected: failure because the target notebooks do not exist.

- [ ] **Step 3: Create notebook 00**

Adapt the existing preparation work into a short notebook that imports dependencies, resolves `../data/loan_data_2007_2014.csv`, loads the data, documents shape/types, checks required columns, and explains the next stage.

- [ ] **Step 4: Create notebook 01**

Adapt the existing cleaned portfolio notebook to show target definition, missing-value handling, date and employment conversions, selected distributions, class balance, and concise conclusions.

- [ ] **Step 5: Create notebook 02**

Adapt the existing feature work to show dummy grouping, coarse classing, WoE/IV calculations, reference categories, and the final selected feature list. Keep the important reasoning visible in cells.

- [ ] **Step 6: Create notebook 03**

Adapt the existing modeling notebook to split data, fit the broader and refined logistic models, show coefficients and p-values, and state clearly that the target models probability of good standing.

- [ ] **Step 7: Create notebook 04**

Adapt the final notebook to calculate `PD = 1 - P(good)`, show AUC/Gini and the confusion matrix, build the 300–850 scorecard, and state the historical/educational limitations.

- [ ] **Step 8: Run the notebook-contract test**

Expected: all structural and terminology checks pass.

### Task 3: Add GitHub and Portfolio Documentation

**Files:**
- Create: `/Users/joseclaudio/Dev_local/project_potfolio/credit_risk/README.md`
- Create: `/Users/joseclaudio/Dev_local/project_potfolio/credit_risk/Final_Report.md`
- Create: `/Users/joseclaudio/Dev_local/project_potfolio/credit_risk/requirements.txt`

**Interfaces:**
- Consumes: the final notebook workflow and validated results.
- Produces: a concise GitHub landing page and a deeper interview-ready report.

- [ ] **Step 1: Write the failing documentation check**

Check that the README names all five notebooks, explains local data setup, distinguishes probability of good standing from PD, and includes limitations and future work without claiming FastAPI, DuckDB, LGD, EAD, or expected loss are already implemented.

- [ ] **Step 2: Run the check and verify it fails**

Expected: failure because the documentation files do not exist.

- [ ] **Step 3: Write the README**

Use the retail-operation style: project objective, business context, notebook table, methodology, results, reproducibility, limitations, skills demonstrated, and future extensions.

- [ ] **Step 4: Write the final report**

Summarize the dataset, target definition, feature-engineering approach, model interpretation, validation evidence, scorecard, limitations, and next phases.

- [ ] **Step 5: Add minimal dependencies**

List only packages actually imported by the final notebooks.

- [ ] **Step 6: Run the documentation check**

Expected: all documentation-contract checks pass.

### Task 4: Execute and Verify the Shareable Project

**Files:**
- Modify only notebook outputs and execution metadata produced by the approved top-to-bottom run.

**Interfaces:**
- Consumes: the completed repository.
- Produces: reproducible notebooks with current, internally consistent evidence.

- [ ] **Step 1: Validate notebook JSON**

Use the shared portfolio Python environment to load and validate every notebook.

- [ ] **Step 2: Execute notebooks sequentially**

Run `00` through `04` in order. Stop on the first substantive failure rather than weakening the analysis.

- [ ] **Step 3: Re-run structural checks**

Confirm notebook names, data paths, target semantics, PD inversion, documentation claims, and ignored-data behavior.

- [ ] **Step 4: Inspect Git scope**

Run `git status --short --ignored` before committing and verify that only the five approved notebooks contain execution changes. After committing, confirm the commit uses the `jclaudio` author/committer identity with no Codex attribution or trailers.

- [ ] **Step 5: Report completion**

Commit the verified notebook outputs, then report exact files created, the two moved data files, notebook execution results, validation results, assumptions, and blockers.
