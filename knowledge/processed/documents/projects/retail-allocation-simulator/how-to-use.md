# How to Use the Retail Allocation Simulator

## Purpose

Use this guide to prepare a weekly allocation workbook, run the model, and review the completed allocation. For the explanation behind each allocation decision, see [workflow.md](workflow.md).

## Prepare the input workbook

The input workbook must contain exactly two tabs:

1. `Control Panel`
2. `Input Data`

Use the public input schema and controls described in [workflow.md](workflow.md). The model reads the workbook without changing the original suggested order values.

You can review the included [small input workbook](examples/synthetic_input.xlsx) for the expected layout.

## Run the model

Install the required Python packages once:

```text
python -m pip install -r requirements.txt
```

Run the model by providing an input workbook and the name for the completed workbook:

```text
python main.py --input examples/synthetic_input.xlsx --output examples/synthetic_processed_output.xlsx
```

Replace those example paths with your own workbook paths when you are ready to process a different weekly allocation.

## Review the completed workbook

Start with these tabs:

1. `08 Final Allocation` for the recommended store-item orders and allocation actions.
2. `09 Availability Validation` to confirm item allocations do not exceed available inventory.
3. `10 Approval Flags` to identify conditions that require review.

Then use the remaining audit tabs to trace how the recommendation was created. [workflow.md](workflow.md) explains each tab and the three common allocation scenarios.

## Example files

- [Small input workbook](examples/synthetic_input.xlsx)
- [Small processed output workbook](examples/synthetic_processed_output.xlsx)
- [Large weekly input workbook](examples/synthetic_weekly_input_325k.xlsx)
