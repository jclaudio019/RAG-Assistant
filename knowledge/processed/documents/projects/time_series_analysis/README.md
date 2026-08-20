# Time-Series Analysis in R

Selected graduate coursework from the **M.S. in Applied Statistics program at Purdue University**, organized to demonstrate practical time-series analysis in R.

The repository contains a final project and six course notebooks covering stationarity, transformations, autocorrelation, ARIMA modeling, residual diagnostics, forecasting, and spectral methods. The notebooks have been renamed and lightly edited for clarity and portfolio presentation while preserving the original statistical work.

## Featured final project

### [Time-Series Analysis and Forecasting in R](final-project/time_series_analysis_and_forecasting_in_r.ipynb)

The final project combines:

- simulations of Gaussian white noise, random walks, Poisson processes, Brownian bridges, AR(1), MA(1), and integrated ARIMA processes;
- an ARIMA-based analysis and 24-month forecast of the U.S. unemployment rate; and
- an ARIMA-based analysis and 24-month forecast of the S&P 500 using the two workbook inputs retained beside the notebook.

The project is educational rather than a production forecasting system. Its fixed model specifications illustrate the full analytical workflow without claiming exhaustive model selection or investment applicability.

## Coursework

1. [Stationarity and Variance-Stabilizing Transformations](coursework/01_stationarity_and_variance_stabilization.ipynb)
2. [Autocorrelation, Partial Autocorrelation, and Model Identification](coursework/02_acf_pacf_and_model_identification.ipynb)
3. [ARIMA Estimation and Model Selection](coursework/03_arima_estimation_and_model_selection.ipynb)
4. [Residual Diagnostics and Forecast Evaluation](coursework/04_residual_diagnostics_and_forecasting.ipynb)
5. [ARIMA Forecasting Applications](coursework/05_arima_forecasting_applications.ipynb)
6. [Spectral Analysis and Fourier Regression](coursework/06_spectral_analysis_and_fourier_methods.ipynb)

## Skills demonstrated

- R and Jupyter notebooks
- Time-series visualization and exploratory analysis
- Stationarity assessment, transformations, and differencing
- ACF/PACF interpretation and tentative model identification
- AR, MA, and ARIMA estimation
- AIC-based model comparison
- Residual diagnostics and Ljung-Box testing
- Point forecasting and forecast interpretation
- Stochastic-process simulation
- Spectral analysis and Fourier regression

## Reproducing the notebooks

The notebooks use R with the `IRkernel`, `TSA`, `astsa`, `readxl`, and `quantmod` packages.

```r
install.packages(c("IRkernel", "TSA", "astsa", "readxl", "quantmod"))
IRkernel::installspec()
```

Launch Jupyter from the repository root and run a notebook from top to bottom. The S&P 500 workbook files must remain beside the final-project notebook because it reads them with relative paths.

## Coursework disclosure

This repository presents my own selected graduate coursework. Course numbering has been retained inside some notebooks to preserve context, while filenames, titles, and explanatory framing have been refined for public portfolio use. The work should be interpreted as evidence of learning and applied statistical practice, not as official course material or an answer key.
