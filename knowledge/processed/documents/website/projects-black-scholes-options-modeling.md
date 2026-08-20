---
description: Portfolio of Jose Claudio, an analytics professional combining forecasting, statistical modeling, automation, finance, and supply-chain decision support.
---

[Skip to main content](#main-content)

[ All Case Studies](/projects)

05 — Financial Modeling

# Black-Scholes Options Modeling

Extended a graduate Black-Scholes options-modeling project with live market inputs, GARCH volatility, and an interactive Delta-hedge comparison.

[ View on GitHub](https://github.com/jclaudio019/black-scholes-options-modeling)

![Black-Scholes Options Modeling project overview](/images/black-scholes-options-modeling-hero.png)

Option value and hedge exposure respond to the underlying price, time to expiration, and volatility assumption.

3

Supported underlyings

2

Volatility estimates

100

Shares per contract

Educational scope: AAPL, MSFT, and SPY. Live values depend on the selected listed option and Yahoo data availability.

## Business Problem

An option price and its hedge depend on assumptions that change with the market. A useful learning tool should show how the same contract looks under different volatility estimates, connect Delta and Gamma to position exposure, and make the hedge calculation visible without presenting it as a trade recommendation.

## Solution

The original graduate final project established the foundation: European call and put pricing, option Greeks, simulated price paths, and Delta- and Gamma-hedging experiments under the Black-Scholes assumptions.

After the course, I added a portfolio extension that retrieves current contract inputs for AAPL, MSFT, and SPY, compares market-implied volatility with a one-day GARCH(1,1) forecast, and translates both model views into position Delta, Gamma, and a theoretical share hedge.

The interface refreshes only when requested, identifies stale results when inputs change, and keeps the prior hedge target only for the current browser session so a second refresh can show the estimated hedge adjustment.

## Dataset

The preserved coursework uses simulated paths and the inputs retained in the original notebook. The post-course explorer requests current Yahoo option chains, two years of adjusted daily price history, dividend information, and the ^IRX Treasury-bill yield proxy. Market data may be delayed, incomplete, or temporarily unavailable.

## Methodology

The project combines the retained Black-Scholes formulas with a button-driven market-data request, a one-day GARCH(1,1) volatility estimate, and position-level Delta and Gamma scaling for standard 100-share option contracts.

Step-by-step method · 6 steps

* 01Preserved the original executed coursework notebook and Black-Scholes pricing implementation unchanged.
* 02Validated the selected listed option and normalized its bid, ask, last price, implied volatility, expiration, dividend yield, and risk-free-rate proxy.
* 03Estimated a one-day GARCH(1,1) variance forecast from at least 252 adjusted daily returns and annualized the result using 252 trading days.
* 04Calculated Black-Scholes price, Delta, and Gamma separately under market-implied and GARCH volatility.
* 05Scaled Delta and Gamma by 100 shares and the signed contract count, then calculated the theoretical Delta-neutral stock target.
* 06Compared the new target with the preceding successful refresh for the same position while keeping all state inside the current browser session.

## AI-Assisted Development

The original coursework notebook and Black-Scholes pricing implementation are preserved unchanged. The previously empty time-series module, market-data integration, GARCH comparison, and interactive interface were developed after the course with AI-assisted coding and were reviewed and tested as a separate portfolio enhancement.

## Findings

The explorer makes the model sensitivity visible: changing the volatility estimate changes the theoretical option price, Delta, Gamma, and the share hedge derived from them. The implied and GARCH views answer different questions, so the comparison is more useful than treating either estimate as a guaranteed future value.

Interactive extension

### Options pricing & hedge explorer

Compare the same listed option under market-implied and one-day GARCH volatility. Data refreshes only when requested.

SymbolAAPLMSFTSPYOption typeCallPutExpiration2026-08-212026-08-242026-08-262026-08-282026-09-042026-09-112026-09-182026-09-252026-10-022026-10-162026-11-202026-12-182027-01-152027-02-192027-03-192027-06-172027-09-172027-12-172028-01-212028-03-172028-12-15Strike$110$115$120$125$130$135$140$145$150$155$160$165$170$175$180$185$190$195$200$205$210$215$220$225$230$235$240$245$250$255$257.5$260$265$270$275$277.5$280$282.5$285$287.5$290$292.5$295$297.5$300$302.5$305$307.5$310$312.5$315$317.5$320$322.5$325$327.5$330$332.5$335$337.5$340$342.5$345$347.5$350$352.5$355$357.5$360$365$370$375$380$385$390$395$400$405$410$415$420$430$440$450$460$470$480$490$500$510$520$530$540$550$560$570$580$590$600PositionLongShortContract count

Refresh and calculate

**Delta** estimates immediate directional exposure. **Gamma** shows how quickly Delta—and the share hedge—changes for an approximately $1 stock move.

**Educational modeling tool.** Yahoo data may be delayed or incomplete. This is not a trading recommendation, production pricing system, or brokerage connection.

The market-data, GARCH, and interactive extension was developed after the course with AI-assisted coding and reviewed and tested separately.

## Business Implications

Delta provides a current estimate of directional exposure, while Gamma helps explain how quickly that exposure—and the associated share hedge—can change when the stock moves. In practice, transaction costs, liquidity, discrete rebalancing, and model limitations would also affect a hedging decision.

## Conclusion

The completed project connects financial-modeling coursework with a small analytical product that makes assumptions, market inputs, and hedge arithmetic inspectable.

It is an educational comparison, not a production pricing system, risk platform, or trading recommendation.

## Limitations

* Black-Scholes assumes European exercise, continuous trading, stable volatility and rates, and frictionless markets.
* Yahoo data may be delayed, incomplete, or temporarily unavailable; ^IRX is used only as a disclosed rate proxy.
* The GARCH comparison uses one normal-residual GARCH(1,1) specification rather than multiple tuned volatility models.
* The share hedge excludes transaction costs, market impact, discrete execution, and brokerage constraints.
* This is an educational modeling tool and not a trading recommendation or production risk-management system.

## Technologies

JavaScriptPythonCloudflare WorkersGARCH

[Next case studyBacktesting System](/projects/backtesting-system)
