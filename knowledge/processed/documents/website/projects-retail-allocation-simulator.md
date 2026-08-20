---
description: Portfolio of Jose Claudio, an analytics professional combining forecasting, statistical modeling, automation, finance, and supply-chain decision support.
---

[Skip to main content](#main-content)

[ All Case Studies](/projects)

03 — Retail Operations

# Retail Allocation Simulator

Automates weekly store-item allocation so limited inventory follows consistent business rules and every recommendation can be reviewed in Excel.

[ View on GitHub](https://github.com/jclaudio019/retail-allocation-simulator)

![Retail Allocation Simulator project overview](/images/retail-allocation-simulator-hero.png)

A distribution-center-to-store flow represents the allocation decision itself—not a forecast or an optimization claim.

325K

Store-item rows

1,800

Fictional stores

13

Audit tabs

The included large example is independently generated fictional data; it does not reproduce employer records, identifiers, or proprietary materials.

## Business Problem

When available inventory cannot satisfy every suggested store order, a retailer needs a repeatable way to decide which locations receive product. Manual reductions or additions can become inconsistent, difficult to review, and disconnected from store need, recent sales, shipment minimums, and inventory constraints.

## Solution

The simulator evaluates one weekly allocation snapshot and classifies each item as balanced, short, or available for an increase. It then applies explicit rank, inventory, sales, capacity, line-limit, shipment, and optional dollar-target rules to produce a final recommendation.

The result is an Excel workbook with the final allocation, inventory checks, approval flags, and supporting tabs. Reviewers can see why units were added, reduced, retained, or excluded without relying on an unexplained score.

The project intentionally stops at allocation. It does not forecast demand, determine purchasing quantities, optimize transportation, or represent a production deployment.

## Dataset

The included large weekly example contains 325,000 unique store-item rows across 1,800 fictional stores and 380 fictional items in two retail categories. Recent Item Sales is an illustrative year-to-date measure, and store ranks run from A1 through E. All values are independently generated for the portfolio.

## Methodology

The simulator validates weekly inputs, classifies item availability, applies reduction or increase rules, checks operating limits, and records each decision in a 13-tab Excel workbook.

Step-by-step method · 5 steps

* 01Validate the control panel and store-item input for required fields, unique keys, numeric values, and supported operating modes.
* 02Compare suggested orders with distribution-center availability to identify balanced items, shortages, and inventory that may be allocated.
* 03Reduce short items using current inventory, store rank, and recent sales-based priority rather than arbitrary cuts.
* 04Add eligible units only while store capacity, item availability, line limits, minimum-shipment requirements, and target controls permit them.
* 05Write the final recommendation, availability checks, approval flags, and allocation summaries to an ordered 13-tab workbook for review.

## AI-Assisted Development

I defined the business problem, allocation logic, requirements, decision rules, validation criteria, and weekly scenarios. I used generative AI through Codex, Claude Code, Antigravity IDE, and CLI-based workflows to help translate those specifications into code, tests, and documentation.

The simulator remains a rule-based analytical workflow, not a generative-AI product or AI model. I reviewed and validated the implementation, business rules, and outputs.

## Findings

The simulator shows that weekly allocation can be handled with visible business rules and checked from input to final recommendation. The examples cover shortages, extra availability, capacity limits, shipment minimums, targets, validation, and approval flags. They demonstrate how the process works rather than claiming a measured sales or inventory improvement.

## Business Implications

Operations teams receive a consistent recommendation and a clear review trail before approval. Each allocation remains tied to defined inputs and limits, while exceptions stay visible.

## Conclusion

Limited inventory does not require an unexplained model. Clear priority rules, validation checks, and reviewable outputs can make weekly allocation more consistent.

Production use would require live-system integration, monitoring, controls, and measured outcomes. Forecasting, replenishment, purchasing, and transportation remain separate problems.

## Limitations

* This is a portfolio-scale rule-based simulator, not a production optimization system.
* The example data is fictional and does not establish real-world sales, service-level, or inventory improvements.
* Demand forecasting, purchasing, transportation, routing, and distribution-center operations are outside scope.
* Manual business validation remains necessary even when automated implementation tests pass.

## Technologies

PythonpandasExcelXlsxWriterpytest

[Next case studyTime-Series Analysis & Forecasting in R](/projects/time-series-analysis-r)
