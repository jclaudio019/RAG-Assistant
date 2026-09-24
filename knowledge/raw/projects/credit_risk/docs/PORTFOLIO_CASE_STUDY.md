# Credit Risk & Portfolio Expected Loss Analytics

## The Problem

Which borrowers might default is only part of credit risk. Lenders also need to know
how much they might lose, where losses concentrate, and how underwriting appetite
changes the book.

## Why Default Prediction Isn't Enough

A 20% PD on a small loan can matter less than a lower PD on a large funded amount.
Portfolio risk needs **PD × LGD × EAD**.

## What I Built

An end-to-end educational analytics case study on Lending Club data: DuckDB/SQL layer,
calibrated PD, empirical LGD, funded-amount EAD, expected loss, segmentation, stress,
Monte Carlo (with a simple correlation illustration), and approval-threshold tradeoffs —
with notebooks for step-by-step explanation.

## Analytical Approach

Temporal validation → leakage-controlled features → logistic PD (+ boosting challenger)
→ isotonic calibration → empirical LGD → EAD proxy → EL aggregation → stress/MC/thresholds.

## Key Challenges Actually Encountered

- Class imbalance and status-based default definition
- Leakage from payment/recovery/seasoning fields
- Raw scores ranking OK but badly calibrated for EL
- High empirical LGD / limited recoveries
- No true default-date balance tape for EAD
- Under-seasoned OOT 2014 vintages
- Interpretability vs small challenger lift

## Key Findings

- Portfolio EL ≈ **$771.6M** on **$6.66B** (**11.6%**)
- OOT AUC **0.669**; Brier **0.24 → 0.08**
- Grade C ≈ **28.1%** of EL; grade A ≈ **15.0%** exposure / **5.3%** EL
- Severe sensitivity stress **+103.3%** EL
- Correlation fattens sample VaR/ES vs independence
- PD≤10% ≈ **41.1%** approval / **5.7%** EL rate (OOT)

## Business Implications

Manage dollars and concentration; treat appetite as a curve; do not equate “highest PD grade”
with “largest portfolio loss contribution.”

## Technical Stack

Python, DuckDB/SQL, pandas, scikit-learn, SciPy, Matplotlib, pytest, Jupyter.

## Limitations

Public-data approximations; not a bank production or regulatory model.

## What I Would Do With Better Data

Fixed default horizons, recovery cashflows with discounting, event-time EAD, macro
drivers, and live performance feedback for monitoring.
