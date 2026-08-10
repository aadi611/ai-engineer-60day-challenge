# Module 1: Probability & Statistics

This is the actual toolkit of quant work. Strategy design, backtesting, and
risk management are all applied statistics. If Module 0 was "the language,"
this is "the grammar you'll use in every sentence you write from here on."

---

## 1.1 Probability fundamentals (1 week)

- [Khan Academy — Probability](https://www.khanacademy.org/math/statistics-probability/probability-library) (free)
- Focus: random variables, conditional probability, Bayes' theorem, expectation, variance, covariance/correlation

**Exercise:** compute conditional probabilities and Bayes' theorem by hand on
2-3 toy problems (e.g. "given a strategy backtest showed a win, what's the
probability it's a real edge vs. a false positive given a prior"). This
Bayesian framing is exactly how you should think about backtest results later.

## 1.2 Distributions (1 week)

- [Khan Academy — Random variables & probability distributions](https://www.khanacademy.org/math/statistics-probability/random-variables-stats-library)
- Focus: normal distribution, log-normal distribution (stock prices are often modeled log-normal), fat tails / kurtosis, skewness

**Why this matters:** financial returns are famously *not* normally
distributed (fat tails, "Black Swans") — you need to know what the "normal
assumption" gets wrong before you rely on any model that uses it (which is
most of them, including Black-Scholes).

**Exercise:** pull a real stock's daily returns (e.g. via `yfinance` in
Python), plot a histogram against a fitted normal distribution, and compute
skewness/kurtosis. Confirm empirically that real returns have fatter tails
than a normal distribution predicts.

## 1.3 Statistical inference (1.5 weeks)

- [Khan Academy — Inferential statistics](https://www.khanacademy.org/math/statistics-probability/inference-categorical-data-chi-square-tests)
- [StatQuest (YouTube)](https://www.youtube.com/c/joshstarmer) — excellent for hypothesis testing, p-values, confidence intervals, regression — search his playlists for these terms
- Focus: hypothesis testing, p-values (and their abuse), confidence intervals, linear regression, R², multiple testing / the multiple comparisons problem

**Why the multiple comparisons problem matters most of all:** if you test 100
strategies and pick the best backtest result, you will find a "significant"
result by pure chance even if none of the 100 have real edge. This single
idea is the difference between a quant and someone who curve-fits a backtest
and blows up an account. Take it seriously — you'll apply it directly in
Module 6.

**Exercise:** run a linear regression of one stock's returns against a market
index (e.g. SPY) in Python using `statsmodels`, interpret the beta
coefficient, R², and p-value. Then deliberately demonstrate the multiple
comparisons problem: generate 100 random walk series, "backtest" a random
rule against each, and show that several look "significant" by chance alone.

## 1.4 Time series analysis (2 weeks)

This is the statistics sub-field most specific to quant work — financial
data is fundamentally time series data with properties (autocorrelation,
non-stationarity, volatility clustering) that ordinary statistics doesn't
handle well.

- [QuantStart — Time Series Analysis articles](https://www.quantstart.com/articles/) (free, filter by "time series")
- Focus: stationarity (and the Augmented Dickey-Fuller test), autocorrelation, random walks, ARIMA models, volatility clustering, GARCH (conceptually — you'll implement basics, not become a GARCH specialist)

**Exercise:** in Python (`statsmodels`), test a real price series for
stationarity (ADF test), difference it to make it stationary, plot the
autocorrelation function, and fit a simple ARIMA model. Separately, plot
rolling volatility of a stock and observe volatility clustering (calm periods
followed by turbulent periods) — this observation is *why* GARCH-family
models exist.

---

## Done when you can:

- Explain why financial returns violate the normal-distribution assumption, with evidence
- Run and correctly interpret a linear regression (not just get a number out)
- Explain the multiple comparisons problem and demonstrate it with a simulation
- Test a time series for stationarity and explain why it matters for modeling

Next: [02_finance_economics](../02_finance_economics/README.md)
