---
description: Portfolio of Jose Claudio, an analytics professional combining forecasting, statistical modeling, automation, finance, and supply-chain decision support.
---

[Skip to main content](#main-content)

[ All Case Studies](/projects)

04 — Applied Statistics

# Time-Series Analysis & Forecasting in R

Used R to simulate time-series behavior and build 24-month forecasts for U.S. unemployment and the S&P 500.

[ View on GitHub](https://github.com/jclaudio019/time%5Fseries%5Fanalysis)

![Time-Series Analysis & Forecasting in R project overview](/images/time-series-analysis-r-hero.png)

Historical patterns lead into several possible future paths, showing seasonality, dependence over time, and forecast uncertainty.

6

Time-series behaviors simulated

2

Real-world series forecasted

24 months

Forecast horizon

Graduate final project completed in R as part of the M.S. in Applied Statistics program at Purdue University. Educational analysis; not an economic or investment recommendation.

## Business Problem

Economic and financial observations change over time, so trend, persistence, and shocks can make methods built for independent data misleading. This project uses simulation, correlation, differencing, and ARIMA models to study those patterns and forecast two real-world series.

## Solution

The first section simulates Gaussian noise, a random walk, a Poisson process, a two-dimensional Brownian bridge, AR(1), MA(1), and integrated ARIMA behavior. The paths and correlation patterns show how each process behaves differently.

The applied sections fit ARIMA(1,1,1) models to monthly U.S. unemployment and S&P 500 data and produce 24-month forecasts. The charts show how uncertainty grows beyond the observed data.

## Dataset

The applied analysis uses the monthly U.S. unemployment-rate series provided by the R astsa package and two S&P 500 workbook inputs retained with the final project. Simulated series use a fixed seed for reproducibility, with 500 observations in the core stochastic-process exercises.

## Methodology

The project moves from controlled simulations to applied forecasting: generate known processes, examine their ACF/PACF structure, difference integrated behavior, fit ARIMA models, and compare observed histories with 24-month forecast paths.

Step-by-step method · 6 steps

* 01Simulated Gaussian, Poisson, Brownian-bridge, autoregressive, moving-average, and integrated time-series behavior in R.
* 02Compared ACF and PACF patterns to identify persistence, moving-average cutoff, and the effect of differencing.
* 03Visualized the monthly U.S. unemployment series and summarized its historical level and variance.
* 04Fit an ARIMA(1,1,1) model and generated a 24-month unemployment forecast.
* 05Loaded and inspected the retained S&P 500 level and percentage-change workbooks, including a regenerated cumulative index.
* 06Fit a second ARIMA(1,1,1) model and generated a 24-month S&P 500 forecast.

## Findings

The simulations make the distinction between stationary and integrated behavior visible: white noise fluctuates around a stable level, a random walk accumulates shocks, the AR(1) ACF decays, and the MA(1) ACF cuts off quickly. In the applied models, both point forecasts remain close to the latest observed level while their uncertainty widens over the 24-month horizon—a useful reminder that the forecast range is as important as the center line.

Brownian bridge simulation

A two-dimensional Brownian bridge wanders unpredictably, yet is constrained to return to its origin.

Step 0 / 500

x **0.00**y **0.00**

PlayPath progress

Forecast explorer

Observed history, the 24-month ARIMA forecast, and its widening 95% uncertainty interval.

U.S. UnemploymentS&P 500

U.S. Unemployment

Month

6193348637791106121136151166181196211227\-404812

Unemployment rate · dashed line marks the forecast boundary

## Business Implications

The project connects time-series theory with practical forecasting in R. It also shows why forecasts should be presented as uncertain model-based ranges rather than guaranteed future values.

## Conclusion

This final project brings simulation, model identification, differencing, ARIMA estimation, and forecast interpretation into one reproducible R analysis.

The GitHub repository also includes six coursework notebooks covering stationarity, autocorrelation, model diagnostics, forecasting, and spectral analysis.

## Limitations

* The applied sections use fixed ARIMA(1,1,1) specifications rather than an exhaustive model-selection process.
* The project does not include rolling-origin validation or comparison against multiple forecasting benchmarks.
* The retained S&P 500 inputs do not include a complete external data-provenance pipeline or calendar-date field.
* The forecasts are educational and should not be used for economic-policy, employment, trading, or investment decisions.

## Technologies

RJupyterastsaARIMAForecasting

[Next case studyBlack-Scholes Options Modeling](/projects/black-scholes-options-modeling)

\-4
