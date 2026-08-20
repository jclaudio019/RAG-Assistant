# Options Pricing and Hedge Explorer Design

## Purpose

Extend the graduate coursework Black-Scholes project with a small interactive tool that demonstrates market-data API usage, volatility estimation, option pricing, and hedge interpretation. The original executed hedging notebook and Black-Scholes pricing implementation remain unchanged. The previously empty `timeseries.py` extension point will receive the new GARCH functionality.

The extension is educational. It will not place trades, connect to brokerage accounts, or present hedge quantities as recommendations.

## User experience

The Streamlit app will let a visitor choose:

- an equity ticker;
- an available expiration, strike, and call or put;
- a long or short position; and
- a number of contracts.

Pressing **Refresh and calculate** will fetch the newest available market snapshot and historical prices, then display:

- the market-data timestamp and freshness label;
- stock price, strike, time to expiration, rate proxy, and dividend yield;
- the option bid, ask, midpoint or last-price fallback, and implied volatility;
- a one-day GARCH(1,1) volatility forecast;
- Black-Scholes price, delta, and gamma using implied volatility;
- Black-Scholes price, delta, and gamma using GARCH volatility; and
- the position delta, target delta-neutral share hedge, hedge adjustment since the previous refresh, and position gamma under each volatility estimate.

A short explanation will state that delta measures immediate directional exposure, while gamma estimates how quickly delta and its stock hedge change as the underlying moves. The first version will measure gamma exposure but will not construct a second-option gamma-neutral hedge.

## Data and calculations

`yfinance` will provide the educational market-data connection:

- latest underlying price;
- available option expirations and contract rows;
- bid, ask, last price, and implied volatility;
- historical adjusted daily prices; and
- dividend information.

The 13-week Treasury bill yield available through Yahoo symbol `^IRX` will be used as a disclosed risk-free-rate proxy. Missing dividend yield will fall back to zero and be labeled. The option market comparison will use the bid/ask midpoint when both are positive; otherwise it will use the last traded price and identify that fallback.

Time to expiration will use calendar time divided by 365. Option contracts will use the standard 100-share multiplier.

## GARCH extension

`src/final/timeseries.py` will add one focused GARCH(1,1) volatility estimator using the Python `arch` package.

The estimator will:

1. accept a series of adjusted daily prices;
2. calculate percentage log returns and remove missing values;
3. require at least 252 usable daily observations;
4. fit a constant-mean GARCH(1,1) model with normally distributed residuals;
5. produce a one-day-ahead conditional variance forecast; and
6. convert the forecast to decimal annualized volatility using 252 trading days.

The lookback will be fixed at two years in the first version. GARCH order, residual distribution, and lookback controls are intentionally excluded to keep the tool understandable and reproducible.

## Hedge calculations

For a selected position:

```text
position delta = option delta * 100 * signed contract count
target stock hedge = -position delta
hedge adjustment = new target stock hedge - previous target stock hedge
position gamma = option gamma * 100 * signed contract count
```

Positive contract count represents a long option and negative contract count represents a short option. The app will show fractional theoretical shares but round the highlighted hedge quantity to the nearest whole share. Previous hedge state will live only in the current Streamlit session; no database is required.

## Architecture

All code will remain in the `black-scholes-options-modeling` repository:

```text
analysis/                 original executed coursework notebook
src/final/blackscholes.py original pricing and Greek functions
src/final/timeseries.py   post-course GARCH estimator
tests/                    existing and focused extension tests
streamlit_app.py          interactive pricing and hedge explorer
```

Streamlit Community Cloud will run the Python application directly from the public GitHub repository. The main Cloudflare portfolio website will later receive only a project card and links to the hosted app and repository.

## Error handling

The app will show a concise user-facing error when:

- a ticker or contract cannot be found;
- Yahoo returns incomplete market data;
- historical data has fewer than 252 usable observations;
- GARCH fitting fails or returns a non-finite forecast; or
- an option has expired or has invalid pricing inputs.

Failed refreshes will not combine new inputs with stale results. The page will identify Yahoo data as educational and potentially delayed.

## Verification

Implementation will preserve the existing test suite and add focused checks for:

- a finite, positive GARCH annualized volatility estimate from deterministic sample prices;
- rejection of insufficient price history;
- position delta, target hedge, hedge adjustment, and position gamma arithmetic; and
- implied-volatility and GARCH-volatility results flowing through the existing Black-Scholes functions.

The deployed app will also receive one manual smoke check using a liquid US equity option. No live order or brokerage validation is in scope.

## Portfolio disclosure

The repository README and app will distinguish the course submission from the later extension using this wording:

> The original graduate coursework notebook and Black-Scholes pricing implementation are preserved unchanged. The previously empty time-series module, market-data integration, GARCH comparison, and interactive interface were developed after the course with AI-assisted coding and were reviewed and tested as a separate portfolio enhancement.

## Non-goals

- live streaming or automatic polling;
- trading or brokerage connectivity;
- user accounts or persistent portfolios;
- a database;
- multiple GARCH specifications or parameter tuning controls;
- automated second-option gamma hedging;
- production-grade pricing, execution, or risk management; and
- embedding the application code inside the main portfolio website repository.
