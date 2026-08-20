# Interactive PD Scorecard Website Handoff Design

## Purpose

Create a small, framework-neutral handoff that lets the portfolio website add
an educational probability-of-default score explorer without importing the
notebooks, Python environment, or unpublished model pickle.

The explorer accepts understandable borrower and historical-loan fields,
maps them into the 17 grouped feature families used by the published model,
and reproduces both outputs already documented in the repository:

- `P(good) = sigmoid(intercept + selected coefficients)`
- `PD = 1 - P(good)`
- illustrative score = intercept points plus one selected point value from
  each feature family

This is a historical model demonstration. It must never present approval,
pricing, underwriting, treatment, regulatory, or production-calibrated advice.

## Scope

### Included

- A browser-safe configuration containing friendly fields, exact grouping
  rules, coefficients, points, reference categories, defaults, explanatory
  copy, and artifact version.
- A dependency-free JavaScript scorer with input validation.
- A standalone accessible demonstration page for visual and functional review.
- Fixed test vectors covering reference, lower-risk, higher-risk, boundary,
  missing-value, and invalid-input behavior.
- A concise website integration guide for the separate website implementation
  chat.

### Excluded

- FastAPI, DuckDB, a database, network requests, persistence, authentication,
  or analytics collection.
- Re-fitting, calibrating, or changing the published model.
- An approval recommendation, pricing decision, or production risk band.
- Raw Lending Club status cleaning or the notebook preprocessing pipeline.
- LGD, EAD, or expected-loss calculations.

## Chosen approach

Use a dual-mode, client-side explorer.

The primary form shows eight understandable fields:

1. Lending Club grade
2. Interest rate
3. Annual income
4. Debt-to-income ratio
5. Loan term
6. Employment length
7. Home ownership
8. Credit inquiries in the last six months

An “Advanced assumptions” disclosure contains the other nine model families:

1. State
2. Income verification status
3. Loan purpose
4. Initial listing status
5. Months since loan issue
6. Months since earliest credit line
7. Accounts currently delinquent
8. Months since last delinquency
9. Months since last public record

Every advanced value remains editable. Defaults are labelled demonstration
assumptions, not average applicants or recommended values. The initial result
must state that all 17 fields contribute even when the advanced section is
collapsed.

## Public handoff structure

Create only these files:

```text
website_handoff/
├── README.md
├── demo.html
├── pd-scorecard-config.json
├── pd-scorecard.mjs
├── pd-scorecard.test.mjs
└── test-vectors.json
```

Responsibilities:

- `pd-scorecard-config.json`: authoritative browser configuration and model
  snapshot derived from `model/pd_model_coefficients.csv`,
  `model/scorecard.csv`, and `model/model_metadata.json`.
- `pd-scorecard.mjs`: validation, raw-to-grouped mapping, calculation, relative
  banding, and contribution ordering. It contains no UI framework code.
- `pd-scorecard.test.mjs`: one small Node built-in test suite covering the
  configuration, mappings, calculations, and invalid inputs.
- `demo.html`: dependency-free reference interface. It demonstrates the
  intended interaction and accessibility but does not impose the final
  portfolio visual styling.
- `test-vectors.json`: stable inputs and expected outputs that the website chat
  can reuse in its own test suite.
- `README.md`: copy-ready implementation contract, embedding steps, result
  wording, accessibility notes, and verification commands.

No build tool, package manifest, generated source, framework adapter, or test
framework is added. Node's built-in test runner validates the module.

## Configuration contract

`pd-scorecard-config.json` contains:

- `artifactVersion`
- `modelDirection` with `modelOutput: "P(good)"` and
  `pdFormula: "1 - P(good)"`
- exact intercept coefficient and intercept score points
- theoretical score minimum `300` and maximum `850`
- display-only relative score bands
- `fields`, ordered for the interface

Each field contains:

- stable `id`
- label, description, primary/advanced placement, input type, and default
- validation bounds or allowed values
- one ordered set of mapping rules
- for every model category: exact category label, coefficient, integer points,
  friendly label, and reference-category marker

Mapping rules must preserve the notebook boundaries exactly:

- Interest rate: `<=9.548`, `(9.548,12.025]`, `(12.025,15.74]`,
  `(15.74,20.281]`, `>20.281`
- Annual income: `<=20,000`, then open-left/closed-right bands through
  `140,000`, then `>140,000`
- DTI: `<=1.4`, then open-left/closed-right bands through `35`, then `>35`
- Employment length: `0`, `1`, `2–4`, `5–6`, `7–9`, `10`
- Loan age: `<38`, `38–39`, `40–41`, `42–48`, `49–52`, `53–64`,
  `65–84`, `>84`
- Earliest credit line age: missing or `<140`, `140–164`, `165–247`,
  `248–270`, `271–352`, `>352`
- Inquiries: `0`, `1–2`, `3–6`, `>6`
- Current delinquencies: `0`, `>=1`
- Months since last delinquency: missing, `0–3`, `4–30`, `31–56`, `>=57`
- Months since last record: missing, `0–2`, `3–20`, `21–31`, `32–80`,
  `81–86`, `>86`

Discrete mappings preserve the published grouping exactly:

- Grades `A` through `G`
- Home ownership: `MORTGAGE`, `OWN`, or the grouped
  `RENT/OTHER/NONE/ANY` reference category
- States: standalone `CA`, `NY`, and `TX`, plus the 11 published state groups
- Verification: `Not Verified`, `Source Verified`, `Verified`
- Purpose: standalone `credit_card` and `debt_consolidation`, plus the three
  published purpose groups
- Listing status: `f` or `w`
- Term: `36` or `60` months

The JSON stores no applicant records and makes no remote requests.

## Scoring module contract

`pd-scorecard.mjs` exports three named functions:

```js
mapInputs(config, rawInputs)
scoreMappedInputs(config, mappedInputs)
scoreApplicant(config, rawInputs)
```

`mapInputs` validates each field and returns exactly one category per feature
family. Unknown categories, non-finite numbers, values outside the documented
domain, and incomplete input objects produce a descriptive `TypeError` or
`RangeError`; the scorer never silently substitutes a value.

`scoreMappedInputs` requires all 17 mapped categories, rejects duplicates and
unknown category IDs, and returns:

```js
{
  artifactVersion,
  logOdds,
  pGood,
  pd,
  score,
  relativeBand,
  mappedCategories,
  contributions
}
```

Calculations:

```text
logOdds = interceptCoefficient + sum(selected category coefficients)
pGood = 1 / (1 + exp(-logOdds))
pd = 1 - pGood
score = interceptPoints + sum(selected category integer points)
```

The score must land within the published theoretical `300–850` range for all
valid category combinations. `pGood` and `pd` must remain in `[0,1]` and sum
to one within floating-point tolerance.

Contributions are sorted by absolute score points, excluding the intercept.
Each contribution identifies the field, selected category, coefficient,
points, and whether it raised, lowered, or did not change the score relative
to that feature's reference category.

## Relative result bands

The interface may describe location on the theoretical score range, but it
must not imply calibrated default-rate bands. Use these fixed display bands:

| Score | Display label |
| --- | --- |
| 300–409 | Higher relative historical risk |
| 410–519 | Elevated relative historical risk |
| 520–629 | Middle relative historical risk |
| 630–739 | Lower relative historical risk |
| 740–850 | Lowest relative historical risk |

Every result places “relative historical” in visible text. No color or label
may imply approve/decline, safe/unsafe, eligible/ineligible, or good/bad
borrower treatment.

## Reference interface

The reference page contains:

1. Title and one-sentence educational purpose
2. Persistent notice: “Educational historical-model demonstration. Not a
   lending decision, approval recommendation, or calibrated production PD.”
3. Primary form with eight fields
4. Native `<details>` element titled “Advanced assumptions (9)”
5. “Calculate historical estimate” button
6. Result region with:
   - illustrative score
   - estimated `P(good)`
   - estimated PD
   - relative historical band
   - three strongest selected contributions
   - expandable full calculation breakdown
7. Method note linking the score to the published model artifacts

The result updates only after explicit calculation. Changed inputs mark the
existing result as stale until recalculated. Validation errors appear next to
the affected field and in a focusable summary. The page never stores inputs.

Accessibility requirements:

- Real labels and fieldsets; no placeholder-only labels
- Keyboard-operable native controls and disclosure
- Focus moves to the error summary after invalid submission and to the result
  heading after a successful calculation
- Result updates use `aria-live="polite"`
- Meaning is not communicated by color alone
- Percentage values retain enough precision to avoid displaying `0%` for a
  non-zero value

## Defaults

Defaults are a deterministic demonstration scenario, not a historical average.
They must be listed in the configuration and repeated in the README so the
website implementation cannot hide assumptions. Use:

- grade `C`
- interest rate `13.5`
- annual income `60,000`
- DTI `18`
- term `36`
- employment length `5`
- home ownership `MORTGAGE`
- inquiries `1`
- state `CA`
- verification `Source Verified`
- purpose `debt_consolidation`
- initial listing status `f`
- months since issue `50`
- months since earliest credit line `240`
- accounts currently delinquent `0`
- months since last delinquency: missing
- months since last record: missing

## Testing and acceptance

Use Node's built-in `node:test` and `assert` modules. No dependency install is
allowed. The test command imports the scorer and reads the two JSON files.

Acceptance checks:

1. The configuration contains 17 unique feature families and 102 scorecard
   rows when the intercept and all categories are counted.
2. Its 85 coefficients, 102 score rows, intercept, score endpoints, reference
   categories, and artifact version reconcile to the public model bundle.
3. Every allowed discrete input and numeric boundary maps to exactly one
   published category.
4. The reference, minimum-score, maximum-score, default, missing-value, and
   threshold-boundary vectors match fixed expected categories and numerical
   outputs.
5. Invalid, incomplete, non-finite, and out-of-domain inputs fail explicitly.
6. For every valid vector, `PD = 1 - P(good)` and the score remains 300–850.
7. When served locally, the standalone demo loads without external network
   requests or console errors.
8. Public copy contains all required limitations and never makes or recommends
   a lending decision.
9. `git diff --check` passes and no private design, recommendation, raw data,
   processed data, pickle, or temporary output becomes tracked.

## Handoff instructions

The website chat receives the `website_handoff/` directory and should treat
the JSON plus test vectors as the integration contract. It may translate the
reference HTML into the site's existing components and styling, but it must
preserve:

- field IDs and mapping boundaries
- formulas and artifact version
- all 17 inputs and disclosed defaults
- visible educational limitations
- explicit calculate/stale-result behavior
- test-vector outputs

The website implementation must not require this credit-risk repository at
runtime; it copies the versioned handoff files into the website codebase.

## Success condition

The separate website chat can copy the six-file directory, run a no-install
validation command, open the reference page, and reproduce the published model
and scorecard without reading the notebooks or guessing any risk logic.
