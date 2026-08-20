# Credit Risk Portfolio Website Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the credit-risk PD case study and a validated client-side score explorer as the existing portfolio's second project.

**Architecture:** Reuse the data-driven project route and lazy project-specific component boundary. Keep model math in a pure tested JavaScript module, configuration in JSON, and UI state in one React component.

**Tech Stack:** React 18, Create React App, Tailwind CSS 3, existing Lucide icons, Jest through react-scripts, static Cloudflare Pages deployment.

## Global Constraints

- Preserve the existing retail project and global visual system byte-for-byte unless a shared integration line must change.
- Add no dependency, API, database, persistence, or hosting configuration.
- Use the public credit-risk artifacts as the only numerical source.
- Describe results as educational relative historical risk, never approval or calibrated production output.
- No new visible copy may contain an em dash.
- Work in an isolated Git worktree and commit only as `jclaudio <jclaudio@brainlessqi.com>`.

---

### Task 1: Exact browser scoring contract

**Files:**
- Create: `src/data/creditRiskScorecard.json`
- Create: `src/lib/creditRiskScoring.test.js`
- Create: `src/lib/creditRiskScoring.js`

**Interfaces:**
- Consumes: published coefficient, scorecard, metadata, and notebook grouping rules.
- Produces: `mapInputs(config, rawInputs)`, `scoreMappedInputs(config, mappedInputs)`, and `scoreApplicant(config, rawInputs)`.

- [ ] Write literal Jest tests for the default scenario, theoretical minimum and maximum, numeric boundaries, missing values, incomplete inputs, and invalid values. The default result literals must be independently calculated from the published coefficients and points.
- [ ] Run `CI=true npm test -- --runInBand src/lib/creditRiskScoring.test.js` and confirm failure because the module does not exist.
- [ ] Create the JSON with 17 ordered field families, 102 scorecard rows including the intercept, exact boundaries, and disclosed defaults.
- [ ] Implement the three pure functions. Reject incomplete, unknown, non-finite, negative count, and unmapped values. Require exactly one category per family.
- [ ] Run the focused test and confirm all cases pass.
- [ ] Reconcile JSON coefficients, points, references, and endpoints against the credit-risk CSV/JSON artifacts with a one-time validation command.
- [ ] Commit `test: define credit risk scoring contract`.

### Task 2: Employer-facing case study content

**Files:**
- Modify: `src/data/content.js:109-230`
- Create: `public/images/credit-risk-pd-model-hero.png`

**Interfaces:**
- Consumes: `Final_Report.md` and validated metrics.
- Produces: one `projects` entry with slug `credit-risk-pd-model` that satisfies the existing `ProjectCard` and `ProjectDetail` fields.

- [ ] Add the second project record after retail with the exact metrics, concise business problem, solution paragraphs, dataset, methodology summary, method steps, findings, implications, conclusion, limitations, technologies, public GitHub URL, and no private roadmap.
- [ ] Create a 4:3 dark dashboard hero asset using the existing near-black, off-white, and purple visual language; it must communicate PD, AUC, Gini, KS, and the illustrative scorecard without implying approval.
- [ ] Scan only the new content for forbidden production claims, private roadmap terms, and em dashes.
- [ ] Run `npm run build` and confirm the new content schema does not break generic project rendering.
- [ ] Commit `feat: add credit risk portfolio case study`.

### Task 3: Interactive score explorer

**Files:**
- Create: `src/components/CreditRiskScoreExplorer.jsx`
- Modify: `src/pages/ProjectDetail.jsx:1-8,165-198`

**Interfaces:**
- Consumes: `creditRiskScorecard.json` and `scoreApplicant`.
- Produces: one accessible primary/advanced form, stale-state behavior, and score result section rendered only for `credit-risk-pd-model`.

- [ ] Add a browser-level failing check expectation: the direct credit-risk route must contain eight primary controls, a closed advanced disclosure with nine controls, no result before calculation, and the required educational notice.
- [ ] Implement the explorer with native inputs, local `useState`, one explicit Calculate action, inline validation, stale-result notice, `aria-live`, result focus, top-three contributions, and full breakdown disclosure.
- [ ] Lazy-import the component in `ProjectDetail.jsx` and render it in a `Section` labelled `Explore the Scorecard` only for the credit-risk slug.
- [ ] Run the scoring Jest suite and `npm run build`.
- [ ] Start the local build, repeat the browser check, calculate the default scenario, change one input, confirm stale state, recalculate, and verify the result changes.
- [ ] Commit `feat: add interactive PD score explorer`.

### Task 4: Full preservation and deployment validation

**Files:**
- Modify: `.gitignore`
- Verify: all tracked changes from the feature branch

**Interfaces:**
- Consumes: completed feature branch.
- Produces: reviewed, merged, pushed, and live-verified second project.

- [ ] Run `CI=true npm test -- --runInBand` and `npm run build` from a clean worktree.
- [ ] Run `git diff --check` and inspect the complete diff against `main`; confirm the retail object, retail chart component/data/images, theme, navigation, footer, routes, contact form, and deployment workflow are unchanged except the intentional generic project-detail hook.
- [ ] Inspect `/`, `/projects`, `/projects/retail-demand-forecasting`, and `/projects/credit-risk-pd-model` at desktop and mobile widths; verify console errors are zero.
- [ ] Run the frontend pre-flight: preserve mode, exact existing tokens, no new dependency, no em dash in new visible copy, keyboard labels and disclosures, responsive single-column collapse, and educational limitations.
- [ ] Request one independent final review of the branch and address only material findings.
- [ ] Merge the reviewed branch to `main`, rerun tests and build on merged `main`, then push `origin/main`.
- [ ] Poll the live Cloudflare route until the credit-risk page appears or a clear external deployment blocker is observed.
