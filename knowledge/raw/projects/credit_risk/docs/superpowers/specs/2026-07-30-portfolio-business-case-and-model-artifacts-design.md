# Credit Risk Portfolio Business Case and Model Artifacts — Design

## Objective

Reframe the public credit-risk project as a business-first portfolio case study
for potential employers and collaborators, following the presentation pattern
of the existing Retail Demand Forecasting project while preserving the
technical evidence in the executed notebooks.

The work will also publish a lightweight, inspectable representation of the
fitted PD model. The current Statsmodels pickle will remain excluded because it
is approximately 513 MB and contains training-design state that is unnecessary
for a portfolio artifact.

## Audience and positioning

The primary audience is hiring managers, analytics leaders, data scientists,
and prospective collaborators. The public story should demonstrate:

- how a credit-risk question was translated into an analytical workflow;
- how data and target decisions were made;
- how Weight of Evidence informed feature engineering;
- how the final model was selected and evaluated;
- how model output was translated into an interpretable scorecard;
- where the analysis is useful and where its limitations prevent deployment.

The tone should be confident but accurate. This is an educational historical
PD analysis, not an underwriting policy, regulatory model, or production
decision system.

## Public business-case structure

`Final_Report.md` will become the canonical source for the future portfolio
page. It will use this structure:

1. Project summary and decision question
2. Headline evidence
3. Business problem
4. Solution
5. Dataset and target
6. Methodology
7. Findings
8. Business implications
9. Conclusion
10. Limitations
11. Technologies
12. Notebook map

The report will lead with the business question:

> Can historical borrower and loan characteristics rank observed credit risk,
> and can that model output be translated into an interpretable score?

Headline evidence will include:

- 466,285 historical loan records across the train/test population;
- held-out AUC of 0.699482;
- Gini of 0.398964;
- KS of 0.291652;
- an illustrative 300–850 scorecard;
- approximately 0.10% bad-class recall at the displayed 0.5 `P(good)`
  threshold, clearly presented as evidence that ranking and classification
  thresholds are different decisions.

## Methodology framing

The report must distinguish Weight of Evidence, Information Value, and model
selection precisely.

Weight of Evidence was used to examine risk ordering and similarity across
categories and numeric intervals. Those patterns informed category grouping
and coarse classing.

Information Value summarized the overall separation strength of each feature.
It was a descriptive diagnostic, not an automatic feature-selection rule.
Variables were not included or excluded solely because they crossed an IV
threshold.

The logistic regression used the resulting one-hot grouped categories, not
numeric WoE-transformed values. After the initial full-rank model, feature
families whose levels were consistently non-significant were removed from the
final specification. Explicit reference categories preserved interpretability.

The report will describe the model direction explicitly:

`PD = 1 - P(good)`

## Findings and business interpretation

The public case should explain, rather than merely list, the metrics:

- Grade was the strongest reviewed discrete feature by IV, but IV was not used
  as a selection cutoff.
- The held-out AUC is just below 0.70, indicating limited-to-moderate historical
  ranking ability rather than strong deployment-ready discrimination.
- Gini and KS support the same conclusion: the model separates risk to a useful
  degree, but material overlap remains.
- The 0.5 `P(good)` threshold identifies only 10 of 10,194 held-out bad loans.
  The model can rank borrowers better than that threshold can classify them.
- A real operating threshold would need explicit costs for missed defaults and
  rejected good borrowers, plus calibration and time-based validation.
- The 300–850 scorecard improves communication of relative model risk but is
  illustrative rather than a lending policy.

## Lightweight public model artifacts

Create a tracked `model/` directory containing:

- `pd_model_coefficients.csv` — intercept and final model coefficients;
- `scorecard.csv` — scorecard points by feature category;
- `model_metadata.json` — target direction, metrics, model type, feature count,
  reference categories, score range, package versions, training population,
  and limitations;
- `README.md` — explains what the artifacts contain and what they cannot do.

Do not commit the 513 MB Statsmodels results pickle.

The lightweight bundle is an inspectable representation of the trained model,
not a raw-application scoring package. It accepts the model’s engineered
feature schema conceptually; raw-loan preprocessing remains notebook-led until
a later delivery phase is approved.

The artifact values must be exported from the final clean notebook execution,
not copied manually. The coefficient names, reference categories, scorecard
endpoints, metrics, and documentation must be cross-checked against saved
notebook outputs and processed checkpoints.

## README alignment

The repository README should remain a concise entry point. It will:

- introduce the business question and delivered solution;
- show the headline model evidence;
- link to `Final_Report.md`;
- explain the six-notebook workflow;
- link to the lightweight model artifact directory;
- retain the data and deployment limitations.

It will not duplicate the full case study or expose private development plans.

## Private recommendations

`recommendations.md` remains local and ignored. It will continue to hold the
development roadmap for:

- stabilizing PD through calibration and time-based validation;
- defining LGD and EAD;
- calculating expected loss;
- packaging raw-input preprocessing;
- FastAPI delivery;
- DuckDB analytical storage;
- an interactive portfolio demonstration.

The private roadmap is not referenced from public repository content.

## Validation and acceptance

The change is complete when:

1. `Final_Report.md` follows the approved business-case structure and accurately
   reflects the executed notebooks.
2. WoE, IV, grouped indicator variables, and significance-based model refinement
   are described correctly.
3. All headline numbers reconcile with the saved notebook outputs.
4. The public model artifacts reproduce the final coefficients, references, and
   300–850 scorecard.
5. The 513 MB pickle, processed checkpoints, raw data, private recommendations,
   and development documentation remain untracked.
6. Notebook execution outputs remain untouched unless regeneration is required
   to export a correct artifact.
7. Structural notebook checks, artifact reconciliation checks, documentation
   checks, and Git hygiene checks pass.

## Scope exclusions

This change will not add:

- FastAPI;
- DuckDB;
- a website implementation;
- an interactive scoring application;
- LGD, EAD, or expected-loss calculations;
- raw-loan production scoring;
- calibration or time-based validation.

Those remain potential follow-up projects in the private recommendations file.
