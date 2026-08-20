---
description: Portfolio of Jose Claudio, an analytics professional combining forecasting, statistical modeling, automation, finance, and supply-chain decision support.
---

[Skip to main content](#main-content)

[ All Case Studies](/projects)

02 — Credit Risk Modeling

# Credit Risk Probability of Default

Built an interpretable historical risk-ranking model and illustrative scorecard using Lending Club loan outcomes.

[ View on GitHub](https://github.com/jclaudio019/credit%5Frisk)

![Credit Risk Probability of Default project overview](/images/credit-risk-pd-model-hero-v2.png)

The balance between repayment strength and default risk determines the illustrative score.

466,285

Historical records

0.699

Held-out AUC

300-850

Illustrative score

Educational historical analysis only. The score is illustrative and is not a lending decision or production credit score.

## Business Problem

Lenders need a consistent way to compare repayment risk, but a model score should not become an automatic approval decision. The business problem is to identify useful risk differences in borrower and loan information, explain what drives the score, and show how different decision thresholds change the result.

## Solution

I built an interpretable historical risk-ranking model. Data preparation and category groupings were learned from the training data and then applied unchanged to the test data.

Weight of Evidence and Information Value were used to study risk patterns. The final logistic regression uses grouped categories so the direction and contribution of each input remain explainable.

The model estimates P(good) under a simplified historical loan-status target and derives probability of default as 1 − P(good). AUC, Gini, and KS measure how well the model ranks risk, while an illustrative 300–850 score makes the relationship easier to understand. The score is not an approval or pricing rule.

## Dataset

The analysis reviewed 466,285 historical Lending Club loan records. A stratified 80/20 split produced 373,028 training rows and 93,257 held-out rows. The historical good\_bad target labels specified charge-off, default, and late-status outcomes as bad (0), with the remaining observed statuses labelled good standing (1).

## Methodology

Training and test data were kept separate, grouped inputs were used in an interpretable logistic regression, and AUC, Gini, and KS measured risk ranking. Model output was then translated into an illustrative score.

Step-by-step method · 7 steps

* 01Prepared historical loan data, defined the good\_bad proxy, and created a stratified 80/20 train/test split so model development and evaluation remained separate.
* 02Learned cleaning rules, imputation statistics, category definitions, and numeric intervals from training rows, then applied them unchanged to held-out rows to prevent leakage.
* 03Used Weight of Evidence to inspect risk ordering and similarity across categories and intervals, creating groups that stakeholders can challenge and interpret.
* 04Used Information Value as a descriptive separation diagnostic, not an automatic feature-selection cutoff, so grouping and coarse classing remained grounded in observed risk ordering and similarity.
* 05Fit logistic regression with one-hot encoded grouped categories rather than numeric WoE values, retaining explicit reference categories and feature direction for interpretation.
* 06Evaluated held-out ranking with ROC/AUC, Gini, and KS across thresholds, then showed how the displayed 0.5 P(good) threshold turns ranking into one classification rule.
* 07Translated fitted log-odds into an illustrative 300-850 scorecard so relative historical risk could be discussed on a familiar scale without implying a decision rule.

## Findings

The model achieved an AUC of 0.699, Gini of 0.399, and KS of 0.292 on the test data. This supports relative risk ranking, but it does not cleanly separate good and bad outcomes. At the displayed 0.5 P(good) threshold, the model detected only 10 of 10,194 bad loans. The main lesson is that useful risk ranking does not automatically create a useful decision cutoff.

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

The model can support risk segmentation and threshold analysis, but it cannot set approval or pricing rules by itself. A real credit policy would need to compare the costs of missed defaults and rejected good borrowers and add calibration, monitoring, fairness review, and governance.

## Conclusion

Historical borrower and loan information contains enough signal to compare relative risk, but model performance alone cannot determine a lending policy.

The remaining business question is which threshold creates an acceptable balance between missed credit losses and rejected good borrowers. The probability, threshold, and illustrative score should remain separate decisions.

## Limitations

* The historical good\_bad proxy has no fixed performance-horizon default definition.
* A random holdout does not establish temporal stability, population stability, or performance through changing economic conditions.
* The probabilities and illustrative 300-850 score are not calibrated for production use.
* The displayed 0.5 P(good) threshold has extremely weak bad-loan recall and is not a business policy.
* Fairness, monitoring, regulatory suitability, and model governance have not been assessed.
* Advanced models may improve discrimination, but complexity must be justified against interpretability, stability, calibration, validation, auditability, implementation cost, and stakeholder explainability.
* This is not an IFRS 9 model and does not estimate expected credit loss, LGD, EAD, staging, or forward-looking economic scenarios.
* Historical Lending Club accounts may not represent a current institution, portfolio, policy, or economic environment.

## Technologies

PythonpandasNumPystatsmodelsscikit-learnJupyter

[Next case studyRetail Allocation Simulator](/projects/retail-allocation-simulator)
