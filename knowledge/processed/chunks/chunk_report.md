# RAG-Assistant — Chunking Quality & Inspection Report

## Summary Metrics

- **Documents Processed:** 25
- **Total Chunks Produced:** 154
- **Average Chunk Tokens:** 198.6
- **Median Chunk Tokens:** 168.5
- **Token Range:** 23 – 847 tokens
- **90th Percentile (p90):** 348.0 tokens
- **Source Word Coverage:** 100.00%
- **Duplication / Overlap Ratio:** 1.014x

## Token Distribution

| Token Range | Chunk Count | Percentage |
| :--- | :--- | :--- |
| < 100 tokens | 27 | 17.5% |
| 100 – 300 tokens | 105 | 68.2% |
| 300 – 500 tokens | 17 | 11.0% |
| 500 – 700 tokens | 4 | 2.6% |
| 700 – 850 tokens | 1 | 0.6% |
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
| `career::knowledge_base` | 19 | 149.9 | 33 / 369 | career_profile |
| `project::backtesting-system::README.md` | 5 | 277.2 | 30 / 847 | project |
| `project::black-scholes-options-modeling::README.md` | 4 | 148.5 | 37 / 280 | project |
| `project::credit_risk::Final_Report.md` | 11 | 154.9 | 93 / 277 | project |
| `project::credit_risk::README.md` | 6 | 151.0 | 68 / 242 | project |
| `project::portfolio-projects::README.md` | 3 | 112.0 | 81 / 163 | project |
| `project::retail-allocation-simulator::README.md` | 5 | 159.6 | 67 / 218 | project |
| `project::retail-allocation-simulator::how-to-use.md` | 3 | 121.0 | 91 / 143 | project |
| `project::retail-allocation-simulator::workflow.md` | 18 | 204.5 | 98 / 533 | project |
| `project::retail-operations::Final_Report.md` | 13 | 258.5 | 85 / 591 | project |
| `project::retail-operations::README.md` | 5 | 167.6 | 45 / 241 | project |
| `project::time_series_analysis::README.md` | 5 | 134.0 | 88 / 176 | project |
| `project::warehouse-club-market-expansion-strategy::README.md` | 4 | 182.5 | 80 / 299 | project |
| `website::about` | 4 | 125.8 | 83 / 171 | website |
| `website::experience` | 4 | 185.5 | 97 / 304 | website |
| `website::home` | 3 | 256.3 | 23 / 495 | website |
| `website::projects` | 1 | 557.0 | 557 / 557 | website |
| `website::projects-backtesting-system` | 4 | 264.5 | 183 / 425 | website |
| `website::projects-black-scholes-options-modeling` | 6 | 256.3 | 108 / 481 | website |
| `website::projects-credit-risk-pd-model` | 6 | 236.7 | 101 / 337 | website |
| `website::projects-retail-allocation-simulator` | 4 | 242.8 | 175 / 359 | website |
| `website::projects-retail-demand-forecasting` | 11 | 287.5 | 137 / 665 | website |
| `website::projects-time-series-analysis-r` | 5 | 214.2 | 128 / 309 | website |
| `website::projects-warehouse-club-market-expansion` | 2 | 105.0 | 65 / 145 | website |
| `website::skills` | 3 | 121.0 | 98 / 144 | website |
