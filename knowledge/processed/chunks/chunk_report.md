# RAG-Assistant — Chunking Quality & Inspection Report

## Summary Metrics

- **Documents Processed:** 26
- **Total Chunks Produced:** 153
- **Average Chunk Tokens:** 197.2
- **Median Chunk Tokens:** 174.0
- **Token Range:** 30 – 847 tokens
- **90th Percentile (p90):** 340.0 tokens
- **Source Word Coverage:** 100.00%
- **Duplication / Overlap Ratio:** 1.010x

## Token Distribution

| Token Range | Chunk Count | Percentage |
| :--- | :--- | :--- |
| < 100 tokens | 25 | 16.3% |
| 100 – 300 tokens | 105 | 68.6% |
| 300 – 500 tokens | 20 | 13.1% |
| 500 – 700 tokens | 2 | 1.3% |
| 700 – 850 tokens | 1 | 0.7% |
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
| `career::knowledge_base` | 20 | 156.9 | 33 / 482 | career_profile |
| `project::backtesting-system::README.md` | 5 | 277.2 | 30 / 847 | project |
| `project::black-scholes-options-modeling::README.md` | 4 | 148.5 | 37 / 280 | project |
| `project::credit_risk::README.md` | 9 | 204.9 | 87 / 349 | project |
| `project::credit_risk::docs/PORTFOLIO_CASE_STUDY.md` | 3 | 182.0 | 80 / 259 | project |
| `project::credit_risk::reports/FINAL_REPORT.md` | 3 | 321.3 | 107 / 474 | project |
| `project::portfolio-projects::README.md` | 3 | 112.0 | 81 / 163 | project |
| `project::retail-allocation-simulator::README.md` | 4 | 202.2 | 67 / 317 | project |
| `project::retail-allocation-simulator::how-to-use.md` | 3 | 142.3 | 91 / 183 | project |
| `project::retail-allocation-simulator::workflow.md` | 18 | 211.4 | 98 / 533 | project |
| `project::retail-operations::Final_Report.md` | 11 | 199.8 | 102 / 389 | project |
| `project::retail-operations::README.md` | 6 | 173.0 | 96 / 257 | project |
| `project::time_series_analysis::README.md` | 5 | 134.0 | 88 / 176 | project |
| `project::warehouse-club-market-expansion-strategy::README.md` | 4 | 182.5 | 80 / 299 | project |
| `website::about` | 4 | 127.0 | 83 / 171 | website |
| `website::experience` | 4 | 184.0 | 89 / 305 | website |
| `website::home` | 4 | 199.5 | 161 / 281 | website |
| `website::projects` | 5 | 221.4 | 117 / 364 | website |
| `website::projects-backtesting-system` | 1 | 56.0 | 56 / 56 | website |
| `website::projects-black-scholes-options-modeling` | 6 | 258.0 | 108 / 456 | website |
| `website::projects-credit-risk-pd-model` | 6 | 244.8 | 122 / 340 | website |
| `website::projects-retail-allocation-simulator` | 4 | 261.5 | 184 / 368 | website |
| `website::projects-retail-demand-forecasting` | 9 | 227.2 | 93 / 501 | website |
| `website::projects-time-series-analysis-r` | 5 | 213.2 | 130 / 309 | website |
| `website::projects-warehouse-club-market-expansion` | 2 | 102.5 | 67 / 138 | website |
| `website::skills` | 5 | 221.4 | 117 / 364 | website |
