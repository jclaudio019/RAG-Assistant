# Credit Risk & Portfolio Expected Loss Analytics

## Why I Built This

I started this project to understand how lenders estimate borrower default risk.
That quickly exposed a more interesting question: even if a model can rank who is
more likely to default, how does that become a useful view of financial risk across
an entire loan portfolio?

To explore that question, I expanded the analysis from probability of default (PD)
into loss given default (LGD), exposure at default (EAD), expected loss (EL),
portfolio concentration, stress sensitivities, Monte Carlo loss distributions, and
risk-appetite tradeoffs:

**PD → LGD → EAD → Expected Loss → portfolio behavior → stress → loss distribution
→ risk appetite**

This is an **educational portfolio project**. It is not a production underwriting
system, regulatory capital model, accounting ECL implementation, or live credit
decision engine.

## What I Wanted to Learn

- How should default probabilities be evaluated when they feed loss calculations?
- Why are discrimination and calibration different?
- How do PD, LGD, and EAD interact at account and portfolio level?
- Where does expected loss concentrate relative to exposure?
- What happens when risk assumptions deteriorate?
- How variable can realized portfolio losses become?
- How does a PD cutoff change approved exposure and expected loss?

## What I Found

All headline values below come from
[`reports/final_metrics.json`](reports/final_metrics.json).

- **PD performance:** the selected logistic model achieved **0.669 OOT ROC AUC**
  (95% bootstrap CI **0.665–0.672**) and **0.245 KS** on the 2014 vintage.
- **Calibration:** OOT Brier score improved from **0.242** for the raw probabilities
  to **0.075** after isotonic calibration.
- **Portfolio expected loss:** **$771.6M** on **$6.66B** of exposure, an EL rate of
  **11.6%**, across **466,285** historical loans.
- **Concentration:** grade **C** contributed about **28.1%** of EL versus **26.7%**
  of exposure. Grade **A** represented about **15.0%** of exposure but **5.3%** of EL.
- **Stress sensitivity:** mild assumptions increased EL by **39.3%**; severe
  assumptions increased it by **103.3%**.
- **Loss simulation:** the independent Monte Carlo mean reconciled to analytical EL
  within **0.002%**. On a matched subsample, assumed default correlation of 0.12
  roughly doubled VaR95 relative to independence.
- **Risk appetite:** on the OOT sample, PD ≤ 10% produced **41.1%** approval and a
  **5.7%** approved-book EL rate; PD ≤ 20% produced **87.6%** approval and a
  **9.9%** EL rate.

## What I Learned

- AUC measures ranking, not whether predicted probabilities are numerically reliable.
- Calibration matters when PD is multiplied into a financial loss calculation.
- Borrower risk alone does not determine portfolio loss; exposure, severity, and
  segment size can change the portfolio interpretation.
- Random train/test splits can look more representative than a temporal out-of-time
  test. The older scorecard path and the newer OOT pipeline are kept separate for
  that reason.
- Stress scenarios are explicit sensitivities, not forecasts.
- A risk-appetite threshold is a business tradeoff. Without credible pricing and
  cost data, there is no honest single “optimal” cutoff.

## How I Approached It

1. Ingest the Lending Club extract once into DuckDB and validate the raw data.
2. Preserve the original hands-on PD/WoE/scorecard notebook sequence.
3. Build a leakage-controlled temporal PD pipeline and compare logistic regression
   with a boosting challenger.
4. Calibrate the selected model on the validation vintage and evaluate it OOT.
5. Estimate empirical LGD, define a decision-time EAD proxy, and calculate
   account-level `EL = PD × LGD × EAD`.
6. Aggregate expected loss by grade, purpose, geography, risk band, and vintage.
7. Explore stress sensitivities, independent and correlated-default simulations,
   monitoring concepts, and approval-threshold tradeoffs.

The final methodology and assumptions are documented in
[`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) and
[`docs/ASSUMPTIONS_AND_LIMITATIONS.md`](docs/ASSUMPTIONS_AND_LIMITATIONS.md).

## Explore the Analysis

The notebooks are the main learning product. Their full sequence and calculation
lineage are in [`docs/NOTEBOOK_GUIDE.md`](docs/NOTEBOOK_GUIDE.md).

- Start with [`15_executive_summary.ipynb`](notebooks/15_executive_summary.ipynb)
  for the complete case-study walkthrough.
- Read notebooks `00`–`05` for the original PD, WoE, logistic-regression, and
  scorecard development path.
- Read notebooks `06`–`14` for temporal validation, calibration, LGD, EAD,
  expected loss, portfolio analysis, stress, simulation, thresholds, and monitoring.
- See [`reports/FINAL_REPORT.md`](reports/FINAL_REPORT.md) for the detailed report.
- See [`docs/PORTFOLIO_CASE_STUDY.md`](docs/PORTFOLIO_CASE_STUDY.md) for the concise
  public case study.
- View the [live portfolio presentation](https://joseoclaudio.com/projects/credit-risk-pd-model).
- Open the [interactive credit-risk dashboard](https://joseoclaudio.com/projects/credit-risk-pd-model/dashboard)
  for the calibrated PD, out-of-time model performance, expected loss, portfolio
  concentration, Monte Carlo loss distribution, stress sensitivity, approval
  thresholds, PSI, and vintage-monitoring views.

## Technical Implementation

The repository uses DuckDB as the durable analytical store. The raw CSV is read only
during ingestion; active notebooks and pipeline stages use DuckDB tables rather than
CSV or pickle intermediates. Reusable Python code supports reproducibility, while the
notebooks retain the explanations and visible calculations needed to understand the
methods.

| Path | Purpose |
| --- | --- |
| `notebooks/` | Step-by-step analytical narrative and final walkthrough |
| `src/credit_risk/` | Reusable modeling, portfolio, monitoring, and scoring code |
| `sql/` | DuckDB quality, cleaning, feature, and portfolio transformations |
| `data/` | Local raw input and gitignored canonical DuckDB store |
| `reports/` | Canonical metrics, figures, and detailed report |
| `docs/` | Methodology, assumptions, notebook guide, data dictionary, and traceability |
| `tests/` | Material analytical, pipeline, scoring, and export checks |
| `portfolio_export/` | Deterministic JSON used by the separate portfolio website |

### Reproduce the analysis

Use Python 3.11 or newer, place `loan_data_2007_2014.csv` under `data/`, then run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make end-to-end
```

`make end-to-end` ingests the raw data, executes notebooks `00`–`05`, runs the
reusable pipeline, rebuilds the reported metrics, executes notebooks `06`–`15`, and
runs the test suite. Individual commands remain available in the `Makefile`.

### Model scoring

The final notebook shows how a borrower record is transformed and scored with the
frozen feature builder, calibrated model, and transparent expected-loss identity.
The scoring calculation remains part of the analysis without adding an unused web
service or presenting the project as a backend platform.

### Portfolio presentation export

```bash
make portfolio-export
```

This produces deterministic, chart-ready JSON for the separate portfolio website.
The export is a downstream presentation artifact and is never an analytical input.

## Limitations

- The target is a status-based default proxy rather than a fixed performance horizon.
- The 2014 OOT vintage is under-seasoned in the historical snapshot.
- LGD uses incomplete, undiscounted public recovery fields.
- EAD is approximated by funded amount at decision time.
- Stress scenarios are sensitivities rather than macroeconomic forecasts.
- Correlated-default simulation uses a simplified one-factor assumption on a sample.
- The threshold analysis lacks full revenue, funding-cost, and operational-cost data.

With better data, I would add horizon-aligned outcomes, recovery cash-flow timing,
event-time balances, macroeconomic drivers, pricing economics, and live outcome
feedback for monitoring and recalibration.
