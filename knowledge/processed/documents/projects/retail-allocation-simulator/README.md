# Retail Allocation Simulator

How can limited available inventory be allocated across stores to help reduce stockouts while prioritizing locations with the strongest sales opportunity?

This project automates a weekly store-item allocation process. It applies defined business rules to direct available inventory to the stores where it is needed most, rather than adding or removing inventory randomly.

## Business question

When inventory cannot satisfy every suggested store order, how can a retailer make consistent allocation decisions that protect stores with the greatest need, support likely sales, and remain within operational constraints?

## Scope

The simulator evaluates one weekly allocation snapshot across two retail categories. It works with suggested store-item orders and considers distribution-center availability, current store inventory, store rank, recent sales activity, item capacity, minimum shipment value, and optional dollar targets.

The included large weekly example contains 325,000 unique store-item rows in one weekly snapshot. `Recent Item Sales` is an illustrative year-to-date measure. The public ranks are A1, A2, A3, B, C, D, and E, where A1 is the strongest rank and E is the weakest. The generator uses independently created fictional values; it does not open or resample employer rows, source rows, or identifiers.

It is designed to produce an auditable allocation recommendation and supporting Excel review tabs. Demand forecasting, purchasing, transportation optimization, and production deployment are outside this repository’s scope.

## Methodology

The allocation process first prepares and validates the weekly inputs. It then identifies whether each item is balanced, short, or has inventory available to increase orders. Short items are reduced using inventory, rank, and sales-based priority. Available inventory can be added one unit at a time only when store capacity, item availability, line limits, shipment requirements, and target rules allow it. When a target requires a further reduction, the simulator can remove complete qualifying store allocations using defined business logic.

The completed workbook preserves the process in audit tabs so a reviewer can see the final recommendation, availability checks, and approval conditions. See [workflow.md](workflow.md) for the complete plain-language methodology and worked scenarios.

## Validation

I manually reviewed and validated the simulator outputs against the weekly synthetic scenarios. The automated test suite translates selected requested scenarios into repeatable code checks for cases such as shortages, surplus availability, capacity limits, minimum shipment, target accounting, validation, and approval flags. Those implementation tests support, but do not replace, manual business validation.

## AI-assisted development

I defined the business problem, allocation logic, requirements, decision rules, validation criteria, and weekly scenarios. I used generative AI through Codex, Claude Code, Antigravity IDE, and CLI-based workflows to help translate those specifications into code, tests, and documentation.

The simulator remains a rule-based analytical workflow, not a generative-AI product or AI model. I reviewed and validated the implementation, business rules, and outputs.

## Reproducibility

Start with [how-to-use.md](how-to-use.md) for the practical Excel workflow and execution steps. Use [workflow.md](workflow.md) when you need the detailed allocation logic and scenario explanations.

To generate the large weekly input workbook:

```text
python synthetic_data.py --stores 1800 --items 380 --rows 325000 --output examples/synthetic_weekly_input_325k.xlsx
```

Included example workbooks:

- [Small input workbook](examples/synthetic_input.xlsx)
- [Small processed output workbook](examples/synthetic_processed_output.xlsx)
- [Large weekly input workbook](examples/synthetic_weekly_input_325k.xlsx)

## Limitations

- This is a portfolio-scale allocation solution, not a production optimization system.
- It does not forecast future demand or determine purchasing quantities.
- It does not optimize transportation, routing, or distribution-center operations.
- It does not reproduce source data, identifiers, or proprietary business materials.
