# RAG-Assistant — Chunking Quality & Inspection Report

## Summary Metrics

- **Documents Processed:** 25
- **Total Chunks Produced:** 267
- **Average Chunk Tokens:** 112.8
- **Median Chunk Tokens:** 80.0
- **Token Range:** 15 – 847 tokens
- **90th Percentile (p90):** 232.0 tokens
- **Source Word Coverage:** 100.00%
- **Duplication / Overlap Ratio:** 1.009x

## Token Distribution

| Token Range | Chunk Count | Percentage |
| :--- | :--- | :--- |
| < 100 tokens | 155 | 58.1% |
| 100 – 300 tokens | 99 | 37.1% |
| 300 – 500 tokens | 10 | 3.7% |
| 500 – 700 tokens | 2 | 0.7% |
| 700 – 850 tokens | 1 | 0.4% |
| > 850 tokens | 0 | 0.0% |

## Validation & Integrity Checks

| Check | Status |
| :--- | :--- |
| `all_chunks_under_max_token_ceiling` | PASSED |
| `no_empty_chunks` | PASSED |
| `source_coverage_healthy_ge_98pct` | PASSED |
| `metadata_provenance_preserved` | PASSED |
| `all_chunk_ids_unique` | PASSED |

## Per-Document Breakdown

| Document ID | Chunks | Avg Tokens | Min/Max | Source Type |
| :--- | :--- | :--- | :--- | :--- |
| `career::knowledge_base` | 34 | 92.3 | 25 / 290 | career_profile |
| `project::backtesting-system::README.md` | 8 | 173.1 | 22 / 847 | project |
| `project::black-scholes-options-modeling::README.md` | 7 | 84.7 | 37 / 165 | project |
| `project::credit_risk::README.md` | 11 | 167.6 | 41 / 349 | project |
| `project::credit_risk::docs/PORTFOLIO_CASE_STUDY.md` | 10 | 54.6 | 17 / 143 | project |
| `project::credit_risk::reports/FINAL_REPORT.md` | 18 | 53.4 | 15 / 144 | project |
| `project::portfolio-projects::README.md` | 4 | 84.0 | 52 / 111 | project |
| `project::retail-allocation-simulator::README.md` | 8 | 101.1 | 39 / 179 | project |
| `project::retail-allocation-simulator::how-to-use.md` | 5 | 85.4 | 48 / 132 | project |
| `project::retail-allocation-simulator::workflow.md` | 23 | 165.4 | 17 / 533 | project |
| `project::retail-operations::Final_Report.md` | 16 | 137.4 | 66 / 326 | project |
| `project::retail-operations::README.md` | 6 | 173.0 | 96 / 257 | project |
| `project::time_series_analysis::README.md` | 6 | 111.7 | 66 / 166 | project |
| `project::warehouse-club-market-expansion-strategy::README.md` | 9 | 80.9 | 40 / 145 | project |
| `website::about` | 5 | 101.4 | 79 / 149 | website |
| `website::experience` | 4 | 184.0 | 89 / 305 | website |
| `website::home` | 10 | 79.3 | 16 / 281 | website |
| `website::projects` | 12 | 92.2 | 19 / 364 | website |
| `website::projects-black-scholes-options-modeling` | 12 | 129.0 | 32 / 456 | website |
| `website::projects-credit-risk-pd-model` | 11 | 133.5 | 40 / 269 | website |
| `website::projects-retail-allocation-simulator` | 11 | 95.1 | 34 / 232 | website |
| `website::projects-retail-demand-forecasting` | 12 | 170.4 | 43 / 501 | website |
| `website::projects-time-series-analysis-r` | 10 | 106.5 | 36 / 217 | website |
| `website::projects-warehouse-club-market-expansion` | 3 | 68.3 | 22 / 138 | website |
| `website::skills` | 12 | 92.2 | 19 / 364 | website |
