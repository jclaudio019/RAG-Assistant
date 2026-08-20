# Credit Risk Notebook Transfer Design

## Goal

Create a standalone, GitHub-ready `credit_risk` portfolio repository that presents the completed Probability of Default (PD) work as a simple, numbered notebook workflow.

## Scope

- Keep the project notebook-led; do not add Python application modules, FastAPI, DuckDB, or an outputs directory.
- Move the canonical Lending Club source files into `data/`:
  - `loan_data_2007_2014.csv`
  - `LCDataDictionary (1).xlsx`
- Keep the data local and excluded from Git.
- Build a five-notebook progression from data preparation through PD logistic regression and scorecard interpretation.
- Add concise GitHub-facing documentation and a final project report.

## Repository Layout

```text
credit_risk/
├── .gitignore
├── README.md
├── Final_Report.md
├── requirements.txt
├── data/
│   ├── .gitkeep
│   └── README.md
├── notebooks/
│   ├── 00_data_preparation.ipynb
│   ├── 01_data_cleaning_and_exploration.ipynb
│   ├── 02_feature_engineering_and_woe.ipynb
│   ├── 03_pd_logistic_regression.ipynb
│   └── 04_pd_validation_and_scorecard.ipynb
└── docs/superpowers/specs/
```

## Notebook Contract

The notebooks run in numerical order and communicate through local, ignored data artifacts where necessary. They make the analysis visible rather than hiding it behind a software layer:

1. Load and document the canonical Lending Club data.
2. Clean the data, define the `good_bad` target, and inspect class balance and key variables.
3. Build grouped and binned scorecard features, then demonstrate WoE and IV.
4. Fit and interpret the final logistic-regression model.
5. Convert predicted probability of good standing to PD, validate discrimination, and show the scorecard interpretation.

## GitHub and Portfolio Contract

- The repository includes code/notebooks and documentation, not the Lending Club data, trained model artifacts, intermediate pickles, or generated exports.
- README content is concise: business question, notebook workflow, data setup, results, limitations, and skills demonstrated.
- Portfolio material uses approximately four evidence-led visuals, with claims limited to rerun validation results.
- The project is educational and historical; it is not a production lending decision system.

## Deferred Work

- FastAPI becomes a later phase after the final scoring workflow can be rerun reproducibly.
- DuckDB becomes a later phase only if SQL exploration or repeatable local querying adds value.
- LGD, EAD, and expected-loss calculation are outside this PD transfer.

## Transfer Boundaries

The new repository receives the two approved canonical data files and selected notebook/documentation content. Legacy root notebooks, saved model files, large intermediate CSVs, and pickle artifacts remain in the original `Credit_Risk` directory until separately reviewed.
