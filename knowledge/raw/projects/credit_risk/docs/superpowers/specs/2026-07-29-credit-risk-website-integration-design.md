# Credit Risk Portfolio Website Integration Design

## Goal

Add the probability-of-default case study as the second project in
`/Users/joseclaudio/Dev_local/project_potfolio/website_replica`, including a
client-side interactive score explorer, while preserving the current retail
project, routing, typography, colors, spacing, motion, and deployment flow.

## Design read

This is a preserve-mode data-science portfolio for employers. The existing
dark editorial dashboard language is authoritative: Cabinet Grotesk, Satoshi,
JetBrains Mono, near-black surfaces, off-white text, one purple accent, square
borders, restrained reveal motion, and progressive disclosure.

Design dials remain `variance 6`, `motion 5`, and `density 4`.

## Integration architecture

The existing generic `/projects/:slug` route and `projects` collection remain
unchanged in structure. Add one project record with slug
`credit-risk-pd-model`, then lazy-load one credit-risk component from
`ProjectDetail.jsx`, matching the existing retail chart boundary.

The score explorer runs entirely in the browser:

`friendly historical inputs -> 17 model categories -> log-odds -> P(good) -> PD -> score`

No API, database, persistence, FastAPI, DuckDB, LGD, EAD, expected loss,
authentication, analytics event, or new dependency is added.

## Source-of-truth hierarchy

1. `credit_risk/model/pd_model_coefficients.csv`
2. `credit_risk/model/scorecard.csv`
3. `credit_risk/model/model_metadata.json`
4. `credit_risk/Final_Report.md`
5. The grouping rules in credit-risk notebooks 02 and 03

The untracked `website_replica-preview.html` is not a source. Its statements
about calibrated scores and lending decisions are inaccurate and must remain
untouched unless separately authorized.

## Files

Create:

- `src/data/creditRiskScorecard.json`: exact browser model configuration,
  defaults, fields, mappings, coefficients, points, and display-only bands.
- `src/lib/creditRiskScoring.js`: pure validation, category mapping, scoring,
  and contribution ordering.
- `src/lib/creditRiskScoring.test.js`: literal behavior and boundary tests.
- `src/components/CreditRiskScoreExplorer.jsx`: accessible React interface.
- `public/images/credit-risk-pd-model-hero.png`: project-card and detail hero
  asset in the existing dark dashboard style.

Modify:

- `src/data/content.js`: add the second employer-facing project record.
- `src/pages/ProjectDetail.jsx`: lazy-load and render the explorer only for the
  credit-risk slug.
- `.gitignore`: retain `graphify-out/` and ignore `.worktrees/`.

Do not modify the retail project object, `RetailForecastCharts.jsx`, its data,
its three images, global theme tokens, navigation, footer, route paths, contact
form, static compiled bundle, or deployment workflow.

## Case-study content

Use the validated public evidence:

- 466,285 historical loan records
- 373,028 training rows and 93,257 held-out rows
- AUC 0.699482
- Gini 0.398964
- KS 0.291652
- illustrative 300-850 scorecard
- `PD = 1 - P(good)`
- 10 of 10,194 held-out bad loans detected at displayed `P(good)=0.5`

Methodology language must say that WoE guided category grouping and risk
ordering, IV was descriptive rather than an automatic selection cutoff, and
the final Logit used grouped one-hot categories rather than numeric WoE values.

The public project object omits private future-work recommendations. It may
describe limitations but must not expose the private LGD/EAD/API roadmap.

No new visible copy may contain an em dash. Existing site copy remains
unchanged.

## Score explorer

Primary fields:

- grade
- interest rate
- annual income
- debt-to-income ratio
- loan term
- employment length
- home ownership
- inquiries in the last six months

Advanced assumptions:

- state
- verification status
- purpose
- initial listing status
- months since issue
- months since earliest credit line
- accounts currently delinquent
- months since last delinquency
- months since last public record

All 17 fields always contribute. Collapsed advanced controls use visible,
documented demonstration defaults and remain editable.

Scoring formulas:

```text
logOdds = interceptCoefficient + sum(selected coefficients)
pGood = 1 / (1 + exp(-logOdds))
pd = 1 - pGood
score = interceptPoints + sum(selected integer points)
```

The interface shows the illustrative score, `P(good)`, PD, relative historical
band, three strongest selected contributions, and an expandable full
breakdown. Bands are display-only positions on the theoretical score range,
not calibrated default-rate bands.

The visible notice is:

> Educational historical-model demonstration. Not a lending decision,
> approval recommendation, or calibrated production PD.

The result updates only after the visitor selects Calculate. Any subsequent
input change marks the result stale until recalculated. No inputs are stored.

## Visual behavior

- Reuse `navy`, `cream`, `teal`, `teal-hover`, and `surface` Tailwind tokens.
- Reuse the current square border system and no new shadow or radius language.
- Use existing `font-display`, body, and `font-mono` hierarchy.
- Use native fields, `<details>`, and the existing `Reveal` wrapper.
- Responsive layout is one column below `md` and two columns at `md` or above.
- No new global CSS is required.
- Use existing Lucide icons only because the project already standardizes on
  that family.

## Accessibility

- Every control has a real label and description where needed.
- Numeric inputs declare meaningful minimums and steps.
- Validation errors are visible and associated with their fields.
- Successful results use `aria-live="polite"` and receive programmatic focus.
- Meaning is not communicated by color alone.
- Advanced controls use native keyboard-operable disclosure.
- Buttons retain the existing high-contrast and focus-visible behavior.

## Validation and deployment

Use CRA's existing Jest runner with `CI=true npm test -- --runInBand` for the
pure scoring tests. Run `npm run build`, inspect both project routes locally,
test the calculator at desktop and mobile widths, verify direct URLs, and scan
browser console errors.

The implementation is committed under `jclaudio <jclaudio@brainlessqi.com>`,
merged into local `main`, and pushed to the existing GitHub origin. The current
Cloudflare Pages Git connection is expected to redeploy from that push. Verify
the live `pages.dev` route after deployment; if Cloudflare no longer watches
the repository, report that external connection as the only deployment
blocker rather than changing hosting configuration.
