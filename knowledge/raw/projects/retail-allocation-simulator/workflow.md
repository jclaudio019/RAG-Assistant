# Retail Inventory Distribution Simulator Workflow

## Purpose

This document explains how the allocation model works in simple, non-technical language.

The model starts with suggested store orders and a limited number of units available at a distribution center. It decides whether orders need to be reduced, whether extra units can be added, and whether complete store allocations need to be removed to stay within a dollar target.

Every stage creates an Excel tab so a reviewer can follow what happened and why.

All examples in this document are fictional and use independently generated demonstration values.

## Weekly snapshot and demonstration data

The large example contains exactly 325,000 unique store-item rows. It is one weekly snapshot for an allocation decision, not a month or year of transaction rows. The large configuration has 1,800 fictional stores and 380 fictional items.

`Recent Item Sales` is an illustrative year-to-date (YTD) measure available at that weekly decision point. Category B has a fictional seasonal demand profile represented through sales, inventory, suggested orders, and distribution-center availability. Items appear in different subsets of stores, so coverage is intentionally uneven rather than a complete store-item grid.

The public ranks are A1, A2, A3, B, C, D, and E. A1 is the strongest public rank and E is the weakest. The engine maps the seven labels to internal priority positions 1 through 7.

The generator uses independent fictional values and broad behavioral patterns only. It does not open, copy, resample, perturb, anonymize, or reproduce employer rows, source rows, or identifiers. The allocation logic and public 12-column input schema remain unchanged.

## The business problem

A retailer has:

- A list of stores.
- A list of items that those stores may need.
- A suggested order for every store-item combination.
- A limited number of units available at the distribution center.
- Inventory and capacity information for every store.
- Store and item performance information.
- Optional dollar targets for Category A, Category B, or both categories combined.

The model answers three main questions:

1. Do suggested orders exceed the available units?
2. If units remain, where should they be distributed?
3. If the total shipment value is too high, which complete store allocations should be removed?

## Input workbook

The input workbook contains two tabs.

### Control Panel

The Control Panel contains the rules for the allocation run.

| Control | Meaning |
|---|---|
| Reduction Only | Reduce orders to available units and stop after the reduction stage. |
| Reduce and Generate Final Order | Reduce orders, skip increases and store pruning, and continue through minimum-shipment and reporting steps. |
| Category A Target Value | Desired qualifying shipment value for Category A. |
| Category B Target Value | Desired qualifying shipment value for Category B. |
| Combined Target Value | Optional target for Category A and Category B together. |
| Minimum Shipment Value | Minimum total shipment value a store must reach before its dollars count toward the target. |
| Capacity Flex Limit | Additional percentage allowed above a store's normal item capacity. |
| Target Tolerance | Acceptable dollar range above or below a target. |
| Max Units per Store-Item | Maximum units allowed for one store-item combination. |
| Skip Duplicate Store-Item Rows? | Determines whether duplicate store-item rows are skipped or treated as an error. |

`Reduction Only` and `Reduce and Generate Final Order` cannot both be active.

### Input Data

The Input Data tab contains one row for every store-item combination.

| Column | Meaning |
|---|---|
| Store ID | Fictional store identifier. |
| Category A Rank | Store priority rank for Category A, using the public labels A1 through E. |
| Category B Rank | Store priority rank for Category B, using the public labels A1 through E. |
| Item ID | Fictional item identifier. |
| Item Description | Plain-language item description. |
| Category | Category A or Category B. |
| Unit Value | Dollar value of one shipped unit. |
| Item Capacity | Normal store capacity for the item. |
| Current Inventory | Units currently available at the store. |
| Distribution Center Availability | Total units available for the item across all stores. |
| Suggested Order | Starting order recommendation for the store-item row. |
| Recent Item Sales | Recent sales activity used as part of allocation priority. |

## How the workflow operates

### Step 1: Setup calculations

The model prepares the data for allocation.

It:

- Creates a Store-Item Key from Store ID and Item ID.
- Selects the correct category rank for each row.
- Rounds distribution-center availability down to whole units.
- Calculates store capacity separately for Category A and Category B.
- Preserves the original Suggested Order.
- Creates the Initial Recommended Allocation.

The initial allocation is the smaller of:

- Suggested Order.
- Distribution Center Availability.

If availability is zero, the initial allocation is zero.

If availability is missing, the initial allocation is also zero, but the model records a separate missing-data action so it can be reviewed later.

### Step 2: Remaining availability

The model totals the initial allocations for each item across all stores.

It then calculates:

```text
Remaining Availability = Available Units - Total Initial Recommended Allocation
```

Each item receives one of three results:

| Result | Meaning |
|---|---|
| Balanced | Suggested allocations exactly match availability. |
| Needs Reduction | Suggested allocations are greater than availability. |
| Can Increase | Availability remains after the initial allocations. |

### Step 3: Reduction pass

An item needs reduction when its suggested allocations exceed the units available at the distribution center.

The model reduces one unit at a time in this order:

1. Stores that already have current inventory.
2. Weaker category ranks.
3. Lower recent item sales.
4. Zero-inventory stores only when the shortage cannot be solved elsewhere.

When possible, the model protects one unit at a zero-inventory store.

The reduction stops when total allocations for the item equal its available units.

### Step 4: Increase loop

The increase loop runs when an item has units remaining and a dollar target still needs to be reached.

The model distributes one unit at a time. This prevents all remaining units from being concentrated on one store-item row.

Increase priority is:

1. Zero-inventory stores first.
2. Stronger category rank.
3. Higher recent item sales.
4. Store ID as the final tie-breaker.

Before adding each unit, the model checks:

- The item still has available units.
- The store has remaining capacity for the category.
- The store-item row has not reached its maximum unit limit.
- The applicable category or combined dollar target has not been reached.

After every added unit, the model recalculates shipment value and target progress.

The increase loop stops when:

- The target range is reached.
- No units remain.
- Store capacity blocks all candidates.
- The maximum store-item units block all candidates.
- No valid candidate remains.

If all target fields are blank, the model operates as a reduction template and skips the increase and pruning stages.

### Step 5: Store pruning

Pruning is used when qualifying shipment value is above the allowed target range.

The model does not remove one item at a time during this stage. It removes a complete store allocation.

Only stores meeting the Minimum Shipment Value are considered because only those stores count toward target dollars.

Stores are considered for removal in this order:

1. Lowest Shipment Value.
2. Weaker category rank when shipment values are tied.
3. Lower recent item sales when the earlier values are tied.
4. Store ID as the final tie-breaker.

After removing a store, the model recalculates qualifying shipment value. It stops when the total is within the target range.

### Step 6: Minimum shipment summary

The model calculates total Shipment Value for each store.

```text
Shipment Value = Final Recommended Allocation x Unit Value
```

If a store reaches the Minimum Shipment Value:

- Meets Minimum Shipment is true.
- Counts Toward Target is true.

If a store does not reach the minimum:

- The store remains visible in the final output.
- Meets Minimum Shipment is false.
- Counts Toward Target is false.
- Its dollars do not count toward the category or combined target.

### Step 7: Category summary

The model calculates qualifying shipment values for:

- Category A.
- Category B.
- Both categories combined.

Each configured target is evaluated using Target Tolerance.

For example, a target of $1,000 with a tolerance of $50 has an acceptable range from $950 to $1,050.

Possible target results include:

- Within Target.
- Below Target.
- Above Target.
- No Target Configured.
- Not Applicable for a reduction-template run.
- No Valid Candidates Remaining.

### Step 8: Final allocation

The Final Allocation tab presents the store-item result in one place.

It includes:

- Original suggested units.
- Final recommended units.
- Inventory and capacity information.
- Shipment value.
- Minimum-shipment status.
- Target-counting status.
- Allocation action.
- Validation status.

Common allocation actions include:

- Kept Initial Allocation.
- Reduced Due To Availability.
- Increased Allocation.
- Reduced Due To Pruning.
- Set To Zero Due To No Availability.
- Set To Zero Due To Missing Distribution Center Availability.

### Step 9: Availability validation

The model totals final allocations by item and compares them with available units.

Validation passes when:

```text
Total Final Recommended Allocation <= Available Units
```

The model also identifies missing or inconsistent availability values.

### Step 10: Approval flags

Approval flags identify situations that may need human review.

Examples include:

- Missing distribution-center availability.
- Missing category rank.
- Failed availability validation.
- Capacity preventing additional allocation.
- Maximum store-item units reached.
- Target below range with no valid candidates remaining.

### Step 11: Allocation summaries

The final summary tabs organize qualifying allocations by:

- Account group.
- Category.
- Item.
- Store.

The summaries show units, shipment value, and store count where applicable.

## Output workbook tabs

| Tab | Purpose |
|---|---|
| 01 Setup Calculations | Shows the starting data and calculated capacity fields. |
| 02 Remaining Availability | Shows whether every item is balanced, short, or available for increase. |
| 03 Reduction Pass | Shows units removed because suggested demand exceeded availability. |
| 04 Increase Loop | Shows every unit added and the reason the loop stopped. |
| 05 Pruning Pass | Shows complete store allocations removed to meet the dollar target. |
| 06 Minimum Shipment Summary | Shows store shipment values and minimum-shipment results. |
| 07 Category Summary | Shows Category A, Category B, and combined target results. |
| 08 Final Allocation | Shows the final store-item allocation and action for every row. |
| 09 Availability Validation | Confirms final item allocations do not exceed availability. |
| 10 Approval Flags | Lists conditions requiring review. |
| 11 Allocation Summary | Summarizes qualifying units and value by account group and category. |
| 12 Allocation by Item | Summarizes qualifying units and value by item. |
| 13 Allocation by Store | Summarizes qualifying units and value by store. |

## Worked allocation scenarios

### Scenario 1: One item is short while another item can increase toward the target

#### Situation

Category A has a target of $80 with no tolerance. The Minimum Shipment Value is set to zero for this small example so every shipment dollar counts.

Two Category A items have a Unit Value of $10.

#### Item A1 requires reduction

| Store | Current Inventory | Rank | Recent Sales | Suggested Order | Item Availability |
|---|---:|---:|---:|---:|---:|
| STORE-001 | 1 | 2 | 4 | 2 | 3 |
| STORE-002 | 0 | 1 | 10 | 3 | 3 |

The suggested total is 5 units, but only 3 units are available. Two units must be removed.

STORE-001 is reduced first because it already has current inventory. Its allocation falls from 2 units to 0 units.

STORE-002 keeps 3 units.

Item A1 now uses all 3 available units and contributes:

```text
3 units x $10 = $30
```

#### Item A2 can increase

| Store | Current Inventory | Rank | Recent Sales | Initial Allocation | Item Availability |
|---|---:|---:|---:|---:|---:|
| STORE-001 | 0 | 2 | 5 | 1 | 6 |
| STORE-002 | 1 | 1 | 15 | 1 | 6 |

The initial Item A2 allocation is 2 units, worth $20. Category A therefore starts at:

```text
Item A1 value $30 + Item A2 value $20 = $50
```

The category still needs $30 to reach its $80 target. Because each Item A2 unit is worth $10, the model needs to add 3 units.

The round-robin increase sequence is:

1. Add one unit to STORE-001 because it has zero inventory.
2. Add one unit to STORE-002 because it is the next eligible candidate.
3. Begin the next pass and add one unit to STORE-001.

Final Item A2 allocations are:

- STORE-001: 3 units.
- STORE-002: 2 units.

Item A2 contributes $50. The final Category A value is:

```text
$30 + $50 = $80
```

The model performed reductions for one item and increases for another item during the same run.

### Scenario 2: The order only needs reduction

#### Situation

Reduction Only is active. One item has 4 available units, but three stores request 2 units each.

| Store | Current Inventory | Rank | Recent Sales | Suggested Order |
|---|---:|---:|---:|---:|
| STORE-001 | 2 | 3 | 2 | 2 |
| STORE-002 | 0 | 2 | 5 | 2 |
| STORE-003 | 0 | 1 | 12 | 2 |

Total suggested order:

```text
2 + 2 + 2 = 6 units
```

Available units:

```text
4 units
```

The model must remove 2 units.

STORE-001 is reduced first because:

- It already has current inventory.
- It has the weakest rank.
- It has the lowest recent sales.

Final allocation:

| Store | Final Units |
|---|---:|
| STORE-001 | 0 |
| STORE-002 | 2 |
| STORE-003 | 2 |

The final total is 4 units, which matches availability.

Because Reduction Only is active:

- No units are increased.
- No stores are pruned.
- The increase and pruning audit tabs remain blank.

If the Unit Value is $15, the final allocation value is:

```text
4 units x $15 = $60
```

### Scenario 3: Availability exists, but stores must be cut to meet the dollar target

#### Situation

An item has 12 available units. The current allocation uses 9 units, so availability is not the problem.

The dollar target is $100 with a tolerance of $5. The acceptable range is $95 to $105.

All three stores meet the Minimum Shipment Value.

| Store | Units | Unit Value | Shipment Value |
|---|---:|---:|---:|
| STORE-001 | 2 | $15 | $30 |
| STORE-002 | 3 | $15 | $45 |
| STORE-003 | 4 | $15 | $60 |

Total allocation value:

```text
$30 + $45 + $60 = $135
```

The total is $30 above the upper target limit of $105.

The model considers complete stores in ascending Shipment Value order.

STORE-001 has the lowest qualifying Shipment Value at $30, so its complete allocation is removed.

New total:

```text
$135 - $30 = $105
```

$105 is within the target range, so pruning stops.

Final result:

| Store | Final Units | Final Shipment Value |
|---|---:|---:|
| STORE-001 | 0 | $0 |
| STORE-002 | 3 | $45 |
| STORE-003 | 4 | $60 |
| Total | 7 | $105 |

This scenario shows that the model can remove stores even when distribution-center availability is sufficient. The reason for removal is the dollar target, not an item shortage.

## Summary

The model follows a consistent sequence:

1. Prepare and validate the input.
2. Reduce allocations that exceed item availability.
3. Add available units when valid candidates and target need remain.
4. Remove complete store allocations when qualifying value is above the target range.
5. Apply the minimum-shipment rule.
6. Validate the final allocation.
7. Produce detailed audit and summary tabs.

This structure makes the allocation traceable from the original suggested order to the final recommended allocation.
