# Module 5: Quant Strategies

This is "the actual quant playbook" — the recurring families of strategies
that everything before this module was preparation for. The goal isn't to
memorize specific strategies (most published ones are arbitraged away) but to
understand the *categories of edge* and how to reason about new ones.

---

## 5.1 Factor investing (1.5 weeks) - taking more time busy with another project

- [QuantStart — factor investing articles](https://www.quantstart.com/articles/) and search "Fama French"
- Read the original idea: Fama-French three-factor model (market, size, value), later extended (momentum, quality, low-vol)
- Focus: what a "factor" is, how factor exposure is measured (regression — straight from Module 1.3), why factors are believed to persist (risk premia vs. behavioral explanations)

**Exercise:** using free data, construct a simple value factor (e.g. rank
stocks by P/B) and a simple momentum factor (e.g. 12-month return excluding
the most recent month) across a basket of ~20-30 stocks, and check whether
sorting into quintiles by each factor shows any return spread historically.
This is a simplified factor backtest — expect noisy results with this little
data; the point is the methodology, not finding real alpha yet.

## 5.2 Momentum & mean-reversion strategies (1 week)

- [QuantStart — Mean Reversion & Momentum](https://www.quantstart.com/articles/) (filter articles)
- Focus: the intuition for why momentum works over medium horizons (weeks-months) while mean-reversion tends to dominate short horizons (days) and long horizons (years) — and that this isn't a contradiction, it's regime/horizon-dependent

**Exercise:** implement a simple moving-average crossover momentum strategy
and a simple Bollinger-Band mean-reversion strategy on the same asset, and
compare their equity curves. Notice how differently they perform in trending
vs. choppy periods.

## 5.3 Statistical arbitrage / pairs trading (1 week)

- [QuantStart — Pairs Trading with Python](https://www.quantstart.com/articles/) (search "pairs trading" and "cointegration")
- Focus: cointegration (different from correlation — this is where Module 1.4's stationarity concept becomes directly useful), the Engle-Granger test, spread construction, z-score entry/exit rules

**Exercise:** find two historically cointegrated stocks (e.g. same-sector
pair), run the Engle-Granger cointegration test, construct the spread, and
build a simple z-score-based pairs trading signal.

## 5.4 Options strategies (0.5-1 week)

Building on Module 4.3's options pricing foundation:

- Covered calls, protective puts, straddles/strangles, spreads (vertical, calendar) — read Hull's later chapters or [Investopedia's options strategies section](https://www.investopedia.com/options-basics-tutorial-4583012)
- Focus: what market view (direction, volatility) each structure expresses, and how payoff/risk profiles differ

## 5.5 Machine learning in trading (survey — you have an ML head start)

Given your AI engineering background, this is where you'll move fastest —
but the discipline is different from typical ML: non-stationary data,
low signal-to-noise, and severe overfitting risk (this is where Module 6
becomes essential, not optional).

- *Advances in Financial Machine Learning* — Marcos López de Prado (the standard text bridging ML and quant finance — written for exactly your background)
- Focus on his core warnings before the techniques: standard k-fold cross-validation is *wrong* for financial time series (label leakage across time), and most "ML alpha" papers fail to replicate live

---

## Done when you can:

- Explain what a factor is and construct a simple one from real data
- Explain when momentum vs. mean-reversion tends to dominate, and why
- Distinguish correlation from cointegration and explain why it matters for pairs trading
- Explain why standard ML cross-validation is unsafe for financial time series

Next: [06_backtesting_risk](../06_backtesting_risk/README.md)
