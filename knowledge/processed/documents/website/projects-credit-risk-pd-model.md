---
description: Built an end-to-end educational credit-risk case study connecting calibrated probability of default to expected loss, portfolio risk, stress, simulation, approval strategy, and monitoring.
---

[Skip to main content](#main-content)

[ All Case Studies](/projects)

03 — Credit Risk Modeling

# Credit Risk Decision & Portfolio Analytics

Built an end-to-end educational credit-risk case study connecting calibrated probability of default to expected loss, portfolio risk, stress, simulation, approval strategy, and monitoring.

[ View on GitHub](https://github.com/jclaudio019/credit%5Frisk)[Launch Dashboard ](/projects/credit-risk-pd-model/dashboard)

Sample inputs

Grade

C

Income

$60K

DTI

18%

Illustrative result

**570**Score

PD 13.7%

Interpretable scorecard

How do borrower inputs shape risk?

The balance between repayment strength and default risk determines the illustrative score.

466,285

Historical accounts

0.669

Out-of-time AUC

$771.6M

Portfolio expected loss\*

\*Educational estimate using documented LGD/EAD assumptions; 11.58% of $6.66B exposure. Not a reserve, pricing rule, or lending decision.

## Business Problem

A borrower-level probability score is only one part of a credit decision. The project asks how to build an interpretable PD model, turn it into expected loss, understand portfolio concentration and tail risk, test transparent downturn sensitivities, evaluate approval thresholds, and monitor stability without presenting an educational model as a lending policy.

## Solution

I organized a notebook-first workflow around time-based train, validation, and out-of-time test vintages. A logistic champion was calibrated on the 2013 validation vintage and evaluated on 2014 loans, keeping development and final evaluation separate.

The calibrated PD feeds a transparent expected-loss calculation (PD × LGD × EAD), segment reporting, independent and correlated-default simulation, sensitivity stress scenarios, and a threshold explorer. Monitoring adds PSI and vintage performance with explicit seasoning warnings.

DuckDB provides the analytical data layer, while deterministic static exports power the public dashboard without introducing a separate backend service. Model scoring remains visible in the analytical workflow and final notebook.

## Dataset

The analysis covers 466,285 historical Lending Club loans issued from 2007 through 2014\. Time-based splits use loans through 2012 for training (95,902), 2013 for validation/calibration (134,755), and 2014 as the out-of-time test book (235,628). The target is a simplified loan-status default proxy.

## Methodology

The workflow moves from reproducible DuckDB preparation through calibrated PD modeling, expected loss, portfolio aggregation, Monte Carlo simulation, sensitivity stress, approval thresholds, and monitoring. Each major notebook retains the underlying educational calculation before helper reuse.

Step-by-step method · 7 steps

* 01Prepared and validated the canonical analytical table in DuckDB, then created chronological train, validation, and out-of-time test cohorts.
* 02Compared an interpretable logistic model with a nonlinear challenger, selected the champion on validation evidence, and calibrated probability levels before final evaluation.
* 03Evaluated out-of-time discrimination, calibration, Brier score, KS, and a bootstrap AUC interval while keeping a classification threshold separate from ranking quality.
* 04Calculated account expected loss as PD × LGD × EAD and reconciled account-level results to portfolio and segment totals.
* 05Simulated independent defaults and a one-factor correlated-default scenario, then summarized loss distributions with VaR and expected shortfall.
* 06Applied transparent PD, LGD, and EAD sensitivity scenarios and explored how candidate PD thresholds change approvals, exposure, expected defaults, and loss.
* 07Measured population shift with PSI and compared predicted versus observed vintage performance, explicitly flagging under-seasoned outcomes.

## Findings

The calibrated logistic model achieved 0.669 ROC-AUC, 0.245 KS, and 0.075 Brier score on the 2014 out-of-time book. Estimated expected loss was $771.6M, or 11.58% of $6.66B exposure, under the documented assumptions. Correlated defaults widened the simulated tail materially, severe sensitivity more than doubled expected loss, and 2014 PSI was low at 0.008—but the vintage is under-seasoned, so its observed default rate is downward-biased.

Interactive scorecard

### Credit risk score explorer

Educational example based on historical data. It is not a lending decision or a production credit score.

GradeABCDEFG

Interest rate (%)

Annual income

DTI (%)

Term (months)3660

Employment length (years)

HomeownershipRENTOTHERNONEANYOWNMORTGAGE

Inquiries in last 6 months

Advanced historical fields

StateNDNEIANVFLHIALNMVANYOKTNMOLAMDNCCAUTKYAZNJARMIPAOHMNRIMADESDINGAWAORWIMTTXILCTKSSCCOVTAKMSWVNHWYDCMEID

Verification statusNot VerifiedSource VerifiedVerified

Loan purposeeducationalsmall\_businessweddingrenewable\_energymovinghouseothermedicalvacationmajor\_purchasecarhome\_improvementdebt\_consolidationcredit\_card

Initial list statusfw

Months since issue

Months since earliest credit line

Accounts currently delinquent

Months since last delinquency

Months since last public record

Calculate

## Business Implications

The analysis shows how model ranking becomes a portfolio decision framework, but it does not select a production cutoff. A real lender would need pricing, operating costs, recoveries, fairness testing, policy constraints, outcome maturity, and governance before using the model for underwriting.

## Conclusion

Historical borrower and loan information contains enough signal to compare relative risk, but model performance alone cannot determine a lending policy.

The remaining business question is which threshold creates an acceptable balance between missed credit losses and rejected good borrowers. The probability, threshold, and illustrative score should remain separate decisions.

## Limitations

* The historical loan-status target is a simplified default proxy rather than a fixed performance-horizon definition.
* LGD and EAD use documented simplifying assumptions; expected loss is not an accounting reserve or realized loss.
* The portfolio-default correlation is assumed rather than empirically calibrated.
* Stress results are transparent sensitivity scenarios, not regulatory macroeconomic stress tests.
* The 2014 test vintage is under-seasoned, which biases observed default outcomes downward.
* Candidate thresholds demonstrate trade-offs; no optimal approval, pricing, or lending policy is claimed.
* Fairness, regulatory suitability, production monitoring controls, and formal model governance require further work.
* Historical Lending Club accounts may not represent a current institution, portfolio, policy, or economic environment.

## Technologies

PythonDuckDBpandasscikit-learnReactRechartsJupyter

[Next case studyRetail Allocation Simulator](/projects/retail-allocation-simulator)

Ask
