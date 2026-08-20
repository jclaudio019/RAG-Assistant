# Black-Scholes Options Modeling

This project began as part of my graduate coursework. I used Python to work through option pricing and hedging under the Black-Scholes assumptions.

## What I worked on

- Black-Scholes prices for European calls and puts
- option Greeks including delta, gamma, theta, and vega
- simulated stock-price paths
- delta and gamma hedging at different rebalancing frequencies

The main analysis is in [`analysis/hedging_final.ipynb`](analysis/hedging_final.ipynb). The notebook keeps the results from my original course work.

## What I learned

The hedging experiment helped me see the trade-off between rebalancing frequency and variability. More frequent rebalancing kept the hedge closer to the model, while less frequent rebalancing produced a wider range of outcomes. In a real market, transaction costs would also matter when deciding how often to rebalance.

## Interactive extension

After the course, I extended the project with an interactive Options Pricing and Hedge Explorer. It retrieves the newest available Yahoo market data when requested and compares option prices and hedge exposure using:

- market-implied volatility; and
- a one-day GARCH(1,1) volatility forecast from two years of daily returns.

The comparison shows how volatility assumptions affect the Black-Scholes price, delta, gamma, and estimated delta-neutral share hedge.

```bash
streamlit run streamlit_app.py
```

> The original graduate coursework notebook and Black-Scholes pricing implementation are preserved unchanged. The previously empty time-series module, market-data integration, GARCH comparison, and interactive interface were developed after the course with AI-assisted coding and were reviewed and tested as a separate portfolio enhancement.

## Project structure

```text
analysis/          hedging notebook
streamlit_app.py    post-course interactive pricing and hedge explorer
src/final/          pricing and simulation functions, including the post-course GARCH estimator
tests/             checks for pricing, paths, and rates
```

## Running the project

This project uses Python 3.11 or newer.

```bash
python -m pip install -e .
python -m pytest -q
jupyter notebook analysis/hedging_final.ipynb
streamlit run streamlit_app.py
```

## Limitations

This is a student modeling project, not a trading recommendation or production pricing library. It assumes the Black-Scholes model conditions and does not include transaction costs or market-impact modeling. A Longstaff-Schwartz American-option extension was part of the original starter material, but I did not complete it, so it is not included here. The interactive extension uses Yahoo data that may be delayed or incomplete, `^IRX` as a rate proxy, and a single normal-residual GARCH(1,1) specification. Hedge quantities are educational estimates and are not connected to a brokerage account.
