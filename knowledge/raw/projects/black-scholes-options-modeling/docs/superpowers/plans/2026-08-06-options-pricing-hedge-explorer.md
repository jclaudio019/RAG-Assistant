# Options Pricing and Hedge Explorer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Streamlit tool that refreshes Yahoo option data, compares implied and GARCH(1,1) volatility in the existing Black-Scholes model, and explains the resulting delta and gamma hedge exposure.

**Architecture:** Keep the original notebook and `blackscholes.py` unchanged. Add the GARCH estimator to the existing empty `timeseries.py`, put pure position calculations in one small `hedging.py` module, and keep Yahoo retrieval plus presentation in a single `streamlit_app.py`. Deploy the same repository to Streamlit Community Cloud; the separate Cloudflare portfolio will only link to it later.

**Tech Stack:** Python 3.11+, NumPy, Pandas, SciPy, `arch` 8.x, yfinance 1.5.x, Streamlit 1.60.x, pytest

## Global Constraints

- Preserve `analysis/hedging_final.ipynb` and `src/final/blackscholes.py` byte-for-byte.
- Use Yahoo data for an educational demonstration and label it as potentially delayed.
- Use a constant-mean normal-residual GARCH(1,1), two years of daily prices, a one-day forecast, and 252 trading days for annualization.
- Require 252 usable returns; do not expose GARCH order, distribution, or lookback controls.
- Use `^IRX` as a disclosed risk-free-rate proxy and zero as the labeled fallback dividend yield.
- Use a 100-share contract multiplier.
- Measure gamma exposure only; do not construct a second-option gamma hedge.
- Refresh only on button press; do not stream, poll, trade, persist portfolios, or add a database.
- Keep the post-course AI-assistance disclosure from the approved design.

---

## File map

- Modify `pyproject.toml`: add the three runtime dependencies.
- Modify `src/final/timeseries.py`: implement one GARCH volatility estimator.
- Create `src/final/hedging.py`: keep pure position and model-summary calculations out of the UI.
- Modify `src/final/__init__.py`: export the new hedge and time-series functions using the package's existing style.
- Create `tests/test_timeseries.py`: verify GARCH output and input rejection.
- Create `tests/test_hedging.py`: verify contract scaling, hedge direction, and Black-Scholes integration.
- Create `streamlit_app.py`: fetch Yahoo data, manage one-session hedge state, and render the explorer.
- Create `requirements.txt`: make Streamlit Community Cloud install this package from the repository.
- Modify `README.md`: document the extension, local command, hosted link, limitations, and AI disclosure.

---

### Task 1: GARCH(1,1) volatility estimator

**Files:**
- Modify: `pyproject.toml`
- Modify: `src/final/timeseries.py`
- Create: `tests/test_timeseries.py`

**Interfaces:**
- Consumes: `pandas.Series` of positive adjusted daily prices.
- Produces: `garch_annualized_volatility(prices: pd.Series) -> float`, expressed as a decimal annualized volatility such as `0.24`.

- [ ] **Step 1: Add the failing estimator tests**

Create `tests/test_timeseries.py`:

```python
import numpy as np
import pandas as pd
import pytest

from final.timeseries import garch_annualized_volatility


def test_garch_returns_positive_annualized_volatility():
    rng = np.random.default_rng(5151)
    daily_returns = rng.normal(0.0004, 0.012, 600)
    prices = pd.Series(100 * np.exp(np.cumsum(daily_returns)))

    volatility = garch_annualized_volatility(prices)

    assert np.isfinite(volatility)
    assert 0 < volatility < 2


def test_garch_requires_252_returns():
    prices = pd.Series(np.linspace(100, 120, 252))

    with pytest.raises(ValueError, match="252 daily returns"):
        garch_annualized_volatility(prices)


def test_garch_rejects_nonpositive_prices():
    prices = pd.Series(np.linspace(100, 120, 300))
    prices.iloc[-1] = 0

    with pytest.raises(ValueError, match="positive"):
        garch_annualized_volatility(prices)
```

- [ ] **Step 2: Run the tests and verify the expected import failure**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_timeseries.py
```

Expected: collection fails because `garch_annualized_volatility` does not exist.

- [ ] **Step 3: Add the `arch` dependency**

Append this entry to the existing `dependencies` array in `pyproject.toml`:

```toml
    "arch~=8.0",
```

Install the project in the active Python environment:

```bash
python -m pip install -e .
```

Expected: installation succeeds and `python -c "import arch"` exits zero.

- [ ] **Step 4: Implement the minimum estimator**

Replace the placeholder in `src/final/timeseries.py` with:

```python
"""Time-series volatility estimates used by the portfolio extension."""

import numpy as np
import pandas as pd
from arch import arch_model


def garch_annualized_volatility(prices: pd.Series) -> float:
    """Estimate one-day GARCH(1,1) volatility and annualize it."""
    clean_prices = pd.Series(prices, dtype=float).dropna()
    if clean_prices.empty or (clean_prices <= 0).any():
        raise ValueError("prices must contain positive values")

    returns = 100 * np.log(clean_prices / clean_prices.shift(1)).dropna()
    if len(returns) < 252:
        raise ValueError("GARCH estimation requires at least 252 daily returns")

    model = arch_model(
        returns,
        mean="Constant",
        vol="GARCH",
        p=1,
        q=1,
        dist="normal",
        rescale=False,
    )
    result = model.fit(disp="off")
    daily_variance = float(result.forecast(horizon=1).variance.iloc[-1, 0])
    volatility = np.sqrt(daily_variance * 252) / 100
    if not np.isfinite(volatility) or volatility <= 0:
        raise ValueError("GARCH produced an invalid volatility forecast")
    return float(volatility)
```

- [ ] **Step 5: Run the focused and existing tests**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m pytest -q -p no:cacheprovider tests/test_timeseries.py tests/test_blackscholes.py tests/test_random.py tests/test_risk_free_rate.py
```

Expected: all tests pass. Optimization warnings are acceptable only if the returned forecast remains finite; failures are not.

- [ ] **Step 6: Commit the estimator**

```bash
git add pyproject.toml src/final/timeseries.py tests/test_timeseries.py
git commit -m "Add GARCH volatility estimate"
```

---

### Task 2: Position and hedge calculations

**Files:**
- Create: `src/final/hedging.py`
- Modify: `src/final/__init__.py`
- Create: `tests/test_hedging.py`

**Interfaces:**
- Consumes: option delta/gamma, signed contracts, previous stock target, and the existing Black-Scholes arguments.
- Produces: `position_hedge(delta: float, gamma: float, contracts: int, previous_target: float | None = None) -> dict[str, float | None]`.
- Produces: `model_hedge_summary(s: float, k: float, r: float, q: float, v: float, t: float, is_call: bool, contracts: int, previous_target: float | None = None) -> dict[str, float | None]`.

- [ ] **Step 1: Add failing hedge tests**

Create `tests/test_hedging.py`:

```python
import pytest

from final.hedging import model_hedge_summary, position_hedge


def test_position_hedge_scales_one_long_contract():
    result = position_hedge(delta=0.60, gamma=0.05, contracts=1)

    assert result == {
        "position_delta": pytest.approx(60),
        "target_stock_hedge": pytest.approx(-60),
        "hedge_adjustment": None,
        "position_gamma": pytest.approx(5),
    }


def test_position_hedge_reports_refresh_adjustment():
    result = position_hedge(
        delta=0.68,
        gamma=0.04,
        contracts=1,
        previous_target=-60,
    )

    assert result["target_stock_hedge"] == pytest.approx(-68)
    assert result["hedge_adjustment"] == pytest.approx(-8)


def test_short_contract_reverses_delta_and_gamma():
    result = position_hedge(delta=-0.35, gamma=0.03, contracts=-2)

    assert result["position_delta"] == pytest.approx(70)
    assert result["target_stock_hedge"] == pytest.approx(-70)
    assert result["position_gamma"] == pytest.approx(-6)


def test_model_summary_uses_existing_black_scholes_functions():
    result = model_hedge_summary(
        s=100,
        k=100,
        r=0.04,
        q=0.0,
        v=0.25,
        t=0.5,
        is_call=True,
        contracts=1,
    )

    assert result["model_price"] > 0
    assert 0 < result["delta"] < 1
    assert result["gamma"] > 0
    assert result["target_stock_hedge"] < 0
```

- [ ] **Step 2: Run the tests and verify the expected import failure**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_hedging.py
```

Expected: collection fails because `final.hedging` does not exist.

- [ ] **Step 3: Implement the pure calculations**

Create `src/final/hedging.py`:

```python
"""Small position calculations for the interactive hedge explorer."""

from final import blackscholes

CONTRACT_MULTIPLIER = 100


def position_hedge(
    delta: float,
    gamma: float,
    contracts: int,
    previous_target: float | None = None,
) -> dict[str, float | None]:
    position_delta = delta * CONTRACT_MULTIPLIER * contracts
    target_stock_hedge = -position_delta
    hedge_adjustment = (
        None
        if previous_target is None
        else target_stock_hedge - previous_target
    )
    return {
        "position_delta": position_delta,
        "target_stock_hedge": target_stock_hedge,
        "hedge_adjustment": hedge_adjustment,
        "position_gamma": gamma * CONTRACT_MULTIPLIER * contracts,
    }


def model_hedge_summary(
    s: float,
    k: float,
    r: float,
    q: float,
    v: float,
    t: float,
    is_call: bool,
    contracts: int,
    previous_target: float | None = None,
) -> dict[str, float | None]:
    delta = float(blackscholes.delta(s, k, r, q, v, t, is_call))
    gamma = float(blackscholes.gamma(s, k, r, q, v, t))
    result = position_hedge(delta, gamma, contracts, previous_target)
    return {
        "model_price": float(blackscholes.price(s, k, r, q, v, t, is_call)),
        "delta": delta,
        "gamma": gamma,
        **result,
    }
```

Add this package export to `src/final/__init__.py` without changing the existing exports, which already include `timeseries`:

```python
from .hedging import *
```

- [ ] **Step 4: Run the focused tests**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m pytest -q -p no:cacheprovider tests/test_hedging.py
```

Expected: 4 tests pass.

- [ ] **Step 5: Commit the hedge calculations**

```bash
git add src/final/hedging.py src/final/__init__.py tests/test_hedging.py
git commit -m "Add option hedge calculations"
```

---

### Task 3: Yahoo-backed Streamlit explorer

**Files:**
- Modify: `pyproject.toml`
- Create: `requirements.txt`
- Create: `streamlit_app.py`

**Interfaces:**
- Consumes: `garch_annualized_volatility()` and `model_hedge_summary()` from Tasks 1 and 2.
- Consumes: Yahoo ticker, option-chain, historical-price, dividend, and `^IRX` responses through yfinance.
- Produces: one button-driven Streamlit page; it exposes no reusable API.

- [ ] **Step 1: Add Streamlit and yfinance dependencies**

Append to the existing `dependencies` array in `pyproject.toml`:

```toml
    "streamlit~=1.60",
    "yfinance~=1.5",
```

Create `requirements.txt`:

```text
-e .
```

Install the updated project:

```bash
python -m pip install -e .
```

Expected: installation succeeds and both `import streamlit` and `import yfinance` exit zero.

- [ ] **Step 2: Create the market-data helpers in `streamlit_app.py`**

Start `streamlit_app.py` with the imports, cached selector data, and uncached refresh function below:

```python
from datetime import date, datetime, timezone

import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

from final.hedging import model_hedge_summary
from final.timeseries import garch_annualized_volatility


@st.cache_data(ttl=900, show_spinner=False)
def available_expirations(ticker_symbol: str) -> tuple[str, ...]:
    expirations = tuple(yf.Ticker(ticker_symbol).options)
    if not expirations:
        raise ValueError(f"No listed options found for {ticker_symbol}")
    return expirations


@st.cache_data(ttl=900, show_spinner=False)
def available_strikes(
    ticker_symbol: str, expiration: str, option_type: str
) -> tuple[float, ...]:
    chain = yf.Ticker(ticker_symbol).option_chain(expiration)
    contracts = chain.calls if option_type == "Call" else chain.puts
    strikes = tuple(float(value) for value in contracts["strike"].dropna().unique())
    if not strikes:
        raise ValueError("No strikes found for that expiration")
    return strikes


def fetch_market_inputs(
    ticker_symbol: str,
    expiration: str,
    strike: float,
    option_type: str,
) -> dict[str, object]:
    ticker = yf.Ticker(ticker_symbol)
    history = ticker.history(period="2y", auto_adjust=True)
    prices = history["Close"].dropna()
    if prices.empty:
        raise ValueError(f"No price history returned for {ticker_symbol}")

    chain = ticker.option_chain(expiration)
    contracts = chain.calls if option_type == "Call" else chain.puts
    matching = contracts[np.isclose(contracts["strike"], strike)]
    if matching.empty:
        raise ValueError("The selected option contract is unavailable")
    contract = matching.iloc[0]

    implied_volatility = float(contract["impliedVolatility"])
    if not np.isfinite(implied_volatility) or implied_volatility <= 0:
        raise ValueError("The selected contract has no usable implied volatility")

    bid = float(contract["bid"])
    ask = float(contract["ask"])
    if bid > 0 and ask > 0:
        market_price = (bid + ask) / 2
        market_price_source = "bid/ask midpoint"
    else:
        market_price = float(contract["lastPrice"])
        market_price_source = "last trade"

    rate_history = yf.Ticker("^IRX").history(period="5d", auto_adjust=False)
    rate_values = rate_history["Close"].dropna()
    if rate_values.empty:
        raise ValueError("The ^IRX rate proxy is unavailable")

    dividend_yield = ticker.info.get("dividendYield")
    dividend_fallback = dividend_yield is None
    dividend_yield = float(dividend_yield or 0.0)
    days_to_expiration = (date.fromisoformat(expiration) - datetime.now(timezone.utc).date()).days
    if days_to_expiration <= 0:
        raise ValueError("The selected option has expired")

    return {
        "ticker": ticker_symbol,
        "stock_price": float(prices.iloc[-1]),
        "strike": float(strike),
        "time_to_expiration": days_to_expiration / 365,
        "risk_free_rate": float(rate_values.iloc[-1]) / 100,
        "dividend_yield": dividend_yield,
        "dividend_fallback": dividend_fallback,
        "is_call": option_type == "Call",
        "bid": bid,
        "ask": ask,
        "market_price": market_price,
        "market_price_source": market_price_source,
        "implied_volatility": implied_volatility,
        "garch_volatility": garch_annualized_volatility(prices),
        "last_trade": contract.get("lastTradeDate"),
        "retrieved_at": datetime.now(timezone.utc),
    }
```

- [ ] **Step 3: Add the controls and refresh boundary**

Below the helpers, add:

```python
st.set_page_config(page_title="Options Pricing & Hedge Explorer", layout="wide")
st.title("Options Pricing & Hedge Explorer")
st.caption("Graduate coursework extension · educational use only")

ticker_symbol = st.text_input("Ticker", value="AAPL").strip().upper()
option_type = st.radio("Option type", ["Call", "Put"], horizontal=True)

try:
    expirations = available_expirations(ticker_symbol)
    expiration = st.selectbox("Expiration", expirations)
    strikes = available_strikes(ticker_symbol, expiration, option_type)
    strike = st.selectbox("Strike", strikes, index=len(strikes) // 2)
except Exception as error:
    st.error(f"Unable to load option choices: {error}")
    st.stop()

position_side = st.radio("Position", ["Long", "Short"], horizontal=True)
contracts = st.number_input("Contracts", min_value=1, value=1, step=1)

if "hedge_targets" not in st.session_state:
    st.session_state.hedge_targets = {}

refresh = st.button("Refresh and calculate", type="primary")
if not refresh:
    st.info("Choose a contract, then press Refresh and calculate.")
    st.stop()

available_expirations.clear()
available_strikes.clear()

try:
    market = fetch_market_inputs(ticker_symbol, expiration, strike, option_type)
except Exception as error:
    st.error(f"Refresh failed: {error}")
    st.stop()
```

Do not write any session result before `fetch_market_inputs()` completes; this prevents new selections from being displayed with stale values.

- [ ] **Step 4: Add the comparison and hedge output**

Complete `streamlit_app.py` with:

```python
signed_contracts = int(contracts) if position_side == "Long" else -int(contracts)
position_key = (
    ticker_symbol,
    expiration,
    float(strike),
    option_type,
    position_side,
    int(contracts),
)
if st.session_state.get("position_key") != position_key:
    st.session_state.position_key = position_key
    st.session_state.hedge_targets = {}

rows = []
for label, volatility in (
    ("Market implied", market["implied_volatility"]),
    ("GARCH forecast", market["garch_volatility"]),
):
    summary = model_hedge_summary(
        s=market["stock_price"],
        k=market["strike"],
        r=market["risk_free_rate"],
        q=market["dividend_yield"],
        v=volatility,
        t=market["time_to_expiration"],
        is_call=market["is_call"],
        contracts=signed_contracts,
        previous_target=st.session_state.hedge_targets.get(label),
    )
    st.session_state.hedge_targets[label] = summary["target_stock_hedge"]
    rows.append(
        {
            "Estimate": label,
            "Volatility": volatility,
            "Model price": summary["model_price"],
            "Delta": summary["delta"],
            "Gamma": summary["gamma"],
            "Position delta": summary["position_delta"],
            "Target hedge shares": summary["target_stock_hedge"],
            "Hedge adjustment": summary["hedge_adjustment"],
            "Position gamma": summary["position_gamma"],
        }
    )

st.subheader(f"{ticker_symbol} {expiration} {option_type.lower()} ${strike:g}")
metric_columns = st.columns(4)
metric_columns[0].metric("Stock price", f"${market['stock_price']:.2f}")
metric_columns[1].metric("Market option price", f"${market['market_price']:.2f}")
metric_columns[2].metric("Risk-free proxy", f"{market['risk_free_rate']:.2%}")
metric_columns[3].metric("Days to expiration", round(market["time_to_expiration"] * 365))

comparison = pd.DataFrame(rows).set_index("Estimate")
st.dataframe(
    comparison.style.format(
        {
            "Volatility": "{:.2%}",
            "Model price": "${:.2f}",
            "Delta": "{:.4f}",
            "Gamma": "{:.4f}",
            "Position delta": "{:.2f}",
            "Target hedge shares": "{:.2f}",
            "Hedge adjustment": lambda value: "First refresh" if pd.isna(value) else f"{value:.2f}",
            "Position gamma": "{:.2f}",
        }
    ),
    use_container_width=True,
)

st.markdown(
    "**Delta** estimates immediate directional exposure. The target hedge offsets "
    "that exposure with shares. **Gamma** estimates how much position delta changes "
    "for an approximately $1 move in the stock, so larger absolute gamma means the "
    "share hedge can become outdated faster."
)
st.caption(
    f"Retrieved {market['retrieved_at']:%Y-%m-%d %H:%M UTC}. "
    f"Market comparison uses {market['market_price_source']}. "
    "Yahoo data is for educational use and may be delayed."
)
if market["dividend_fallback"]:
    st.warning("Yahoo did not provide a dividend yield; the model used 0%.")

st.divider()
st.caption(
    "The original graduate coursework notebook and Black-Scholes implementation are preserved. "
    "This market-data, GARCH, and interactive extension was developed after the course "
    "with AI-assisted coding and reviewed and tested separately."
)
```

Before accepting this step, replace the `Hedge adjustment` styling lambda with a preformatted display column if the installed Pandas Styler rejects callables in a format dictionary. Do not add a new formatting dependency.

- [ ] **Step 5: Run static and local smoke checks**

Run:

```bash
python -m py_compile streamlit_app.py src/final/timeseries.py src/final/hedging.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m pytest -q -p no:cacheprovider
streamlit run streamlit_app.py --server.headless true
```

Expected: all tests pass and Streamlit prints a local URL without an import or startup error. Stop the server after checking the initial page.

- [ ] **Step 6: Commit the application**

```bash
git add pyproject.toml requirements.txt streamlit_app.py
git commit -m "Add interactive options hedge explorer"
```

---

### Task 4: Portfolio documentation and disclosure

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: the completed app and its deployment requirements.
- Produces: clear separation between original coursework and the post-course extension, plus local run instructions.

- [ ] **Step 1: Add the extension section to the README**

After the original “What I learned” section, add:

```markdown
## Interactive extension

After the course, I extended the project with an interactive Options Pricing and Hedge Explorer. It retrieves the newest available Yahoo market data when requested and compares option prices and hedge exposure using:

- market-implied volatility; and
- a one-day GARCH(1,1) volatility forecast from two years of daily returns.

The comparison shows how volatility assumptions affect the Black-Scholes price, delta, gamma, and estimated delta-neutral share hedge.

```bash
streamlit run streamlit_app.py
```

> The original graduate coursework notebook and Black-Scholes pricing implementation are preserved unchanged. The previously empty time-series module, market-data integration, GARCH comparison, and interactive interface were developed after the course with AI-assisted coding and were reviewed and tested as a separate portfolio enhancement.
```

Update the project structure block to include `streamlit_app.py` and describe `src/final/timeseries.py` as the post-course GARCH estimator. Add `streamlit run streamlit_app.py` to the running instructions.

- [ ] **Step 2: Update limitations without overstating the tool**

Append these points to the existing limitations paragraph:

```markdown
The interactive extension uses Yahoo data that may be delayed or incomplete, `^IRX` as a rate proxy, and a single normal-residual GARCH(1,1) specification. Hedge quantities are educational estimates and are not connected to a brokerage account.
```

- [ ] **Step 3: Verify documentation and preserved originals**

Run:

```bash
git diff --check
cmp analysis/hedging_final.ipynb /Users/joseclaudio/Dev_local/starter/analysis/hedging_final.ipynb
cmp src/final/blackscholes.py /Users/joseclaudio/Dev_local/starter/pkg/src/final/blackscholes.py
```

Expected: `git diff --check` is silent and both `cmp` commands exit zero.

- [ ] **Step 4: Commit documentation**

```bash
git add README.md
git commit -m "Document interactive modeling extension"
```

---

### Task 5: Final verification, publication, and deployment

**Files:**
- Modify after deployment: `README.md` with the actual Streamlit URL.

**Interfaces:**
- Consumes: all earlier tasks on `main`.
- Produces: a pushed public repository and a shareable Streamlit application.

- [ ] **Step 1: Run the complete local verification**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m pytest -q -p no:cacheprovider
python -m py_compile streamlit_app.py src/final/*.py
git diff --check
git status -sb
```

Expected: every test passes, compilation and diff checks are silent, and the worktree is clean.

- [ ] **Step 2: Run one live-data smoke check without placing orders**

Start the app:

```bash
streamlit run streamlit_app.py
```

In the browser, select one listed AAPL call and press **Refresh and calculate**. Verify:

- the retrieved timestamp is visible;
- implied and GARCH volatility are finite and positive;
- both model prices, deltas, and gammas render;
- both target hedge quantities render;
- a second refresh for the same position shows a hedge adjustment; and
- no brokerage or order action is present.

Stop the local server.

- [ ] **Step 3: Push the verified commits**

```bash
git push origin main
```

Expected: `origin/main` advances to the verified local `main` commit.

- [ ] **Step 4: Deploy from the public repository**

In Streamlit Community Cloud:

1. Select repository `jclaudio019/black-scholes-options-modeling`.
2. Select branch `main`.
3. Select entrypoint `streamlit_app.py`.
4. Select Python 3.11.
5. Request subdomain `black-scholes-hedge-explorer`; if unavailable, accept the generated public subdomain and record the exact URL.
6. Deploy and wait for the app to reach its running state.

Expected: the public URL loads the same explorer without dependency or startup errors.

- [ ] **Step 5: Add the actual app URL and republish**

If the requested subdomain was accepted, add this exact line below the README interactive-extension heading:

```markdown
**[Open the interactive Options Pricing and Hedge Explorer](https://black-scholes-hedge-explorer.streamlit.app/)**
```

If Streamlit assigned a different subdomain, use the exact URL shown in the successful deployment instead.

Then run:

```bash
git add README.md
git commit -m "Add hosted options explorer link"
git push origin main
```

Expected: the README link opens the deployed app.

- [ ] **Step 6: Final remote checks**

Run:

```bash
git status -sb
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
gh repo view jclaudio019/black-scholes-options-modeling --json url,visibility,defaultBranchRef
```

Expected: clean `main` tracking `origin/main`, identical local and remote commits, public visibility, and `main` as the default branch.
