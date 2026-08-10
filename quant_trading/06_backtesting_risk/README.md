# Module 6: Backtesting, Overfitting & Risk Management

This is arguably the most important module in the entire curriculum. Most
people who "get into quant" can build a strategy that looks great in a
backtest. Almost none of them can tell you honestly whether that result means
anything. This module is about becoming the person who can.

---

## 6.1 Backtesting methodology and its failure modes (1.5 weeks)

- *Advances in Financial Machine Learning* — López de Prado, Ch. 1-7 (this is the canonical treatment — read it slowly)
- [QuantStart — Successful Backtesting of Algorithmic Trading Strategies (Parts I & II)](https://www.quantstart.com/articles/)
- Know these failure modes by name and be able to spot each one in a strategy write-up:
  - **Look-ahead bias** — using information that wouldn't have been available at decision time
  - **Survivorship bias** — testing only on assets that still exist today (ignoring delisted/bankrupt ones)
  - **Overfitting / data snooping** — tuning parameters until the backtest looks good (directly connects to Module 1.3's multiple comparisons problem)
  - **Transaction cost blindness** — ignoring spread, slippage, and commissions, which can turn a "profitable" strategy negative
  - **Regime dependence** — a strategy that only worked in one historical period (e.g. only in a bull market)

**Exercise:** take one of your strategies from Module 5 and deliberately
audit it for each failure mode above. Then re-run the backtest with realistic
transaction costs (e.g. 5-10 bps per trade) and see how much of the "edge"
survives.

## 6.2 Building a backtester by hand (1 week)

Do this before reaching for `backtrader`/`vectorbt` — you need to understand
the mechanics (position tracking, mark-to-market, cash accounting, avoiding
look-ahead bias in the loop itself) before trusting a framework to do it for you.

- [QuantStart's event-driven backtesting series](https://www.quantstart.com/articles/) (search "event-driven backtesting")

**Exercise:** write a simple vectorized backtester in pandas from scratch:
given a price series and a position signal (e.g. from Module 5.2's momentum
strategy), compute the resulting equity curve, including realistic
transaction costs. Output standard performance stats (see 6.3).

## 6.3 Performance & risk metrics (1 week)

- [QuantStart — Sharpe Ratio, drawdown, and risk-adjusted return articles](https://www.quantstart.com/articles/)
- Know how to compute and interpret: Sharpe ratio, Sortino ratio, maximum drawdown, Calmar ratio, win rate vs. payoff ratio, and *why* Sharpe ratio alone is a dangerously incomplete summary (it says nothing about tail risk / drawdown depth)

**Exercise:** add all of the above metrics as a reusable "tearsheet" function
to your Module 3.2 utilities, and run it on 2-3 strategies from Module 5 to
compare them properly (not just "which had the higher total return").

## 6.4 Portfolio construction & position sizing (1 week)

- Revisit Module 0.3's Lagrange-multiplier portfolio exercise — now implement full Markowitz mean-variance optimization in Python (`scipy.optimize`)
- Read about the **Kelly Criterion** for position sizing — [Investopedia — Kelly Criterion](https://www.investopedia.com/articles/trading/04/091504.asp) — and why full Kelly is almost never used in practice (fractional Kelly, and why)
- Focus: diversification, correlation between strategies/assets, why naive "equal weight everything" often beats a poorly-estimated optimizer (estimation error in the covariance matrix is a real, well-documented problem)

**Exercise:** implement Markowitz optimization on a small basket of assets,
plot the efficient frontier, and compare the "optimal" portfolio's
out-of-sample performance (next year's data) against a simple equal-weight
portfolio. This is a firsthand demonstration of estimation-error risk.

## 6.5 Risk management practices

- Position limits, stop-losses (and their pitfalls), value-at-risk (VaR) and its well-known limitations, stress testing
- [Investopedia — Value at Risk (VaR)](https://www.investopedia.com/terms/v/var.asp)

---

## Done when you can:

- Name and detect all five backtesting failure modes in someone else's strategy write-up
- Build a working vectorized backtester with realistic transaction costs from scratch
- Compute and correctly interpret Sharpe, Sortino, max drawdown, and Calmar
- Explain why Markowitz optimization is fragile in practice and what fractional Kelly is for

Next: [07_market_microstructure](../07_market_microstructure/README.md)
