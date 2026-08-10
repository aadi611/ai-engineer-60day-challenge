# Module 3: Programming & Data Stack for Quant

You're already a strong programmer — this module is mostly "new libraries and
new data-handling idioms," not "learn to code." It runs in parallel with the
other modules; dip into it whenever an exercise elsewhere needs a tool you
don't have yet.

---

## 3.1 The core Python quant stack (ongoing reference, not a linear course)

- `pandas` — time series indexing, resampling, rolling windows (the backbone of almost all quant Python code)
  - [pandas docs — Time series / date functionality](https://pandas.pydata.org/docs/user_guide/timeseries.html)
- `numpy` — you likely know this already from AI work; the quant-specific idioms are vectorized returns calculations, rolling stats
- `statsmodels` — regression, time series models (ARIMA, stationarity tests) — used throughout Module 1 and 5
- `scipy.stats` / `scipy.optimize` — distributions, hypothesis tests, portfolio optimization
- `matplotlib` / `plotly` — you know this; quant-specific charts: equity curves, drawdown charts, rolling Sharpe

**Exercise:** if you haven't already, redo the Module 1.2 and 1.4 exercises
using idiomatic pandas (rolling windows, `.pct_change()`, resampling to
weekly/monthly) instead of manual loops — this is the muscle memory you need.

## 3.2 Getting market data (free sources)

- [`yfinance`](https://github.com/ranaroussi/yfinance) — free, unofficial Yahoo Finance wrapper; good enough for learning/backtesting on daily equity data
- [FRED](https://fred.stlouisfed.org/) via `pandas_datareader` or the FRED API — free macro data (rates, inflation, GDP)
- [Alpha Vantage](https://www.alphavantage.co/) — free tier API for stocks/FX/crypto
- Know the limits: free daily-bar equity data is fine for learning; real quant shops pay for tick-level, survivorship-bias-free, point-in-time data. You should understand *why* that distinction matters (see Module 6 — survivorship bias) even while using free data to learn.

**Exercise:** write a small reusable data-loading module — pull daily OHLCV
for a handful of tickers via `yfinance`, cache it to local parquet/CSV, and
expose a clean `get_prices(tickers, start, end)` function. You'll reuse this
in every module from here on, so make it something you actually want to import.

## 3.3 Backtesting frameworks (survey, don't commit yet)

You'll build a simple backtester by hand in Module 6 (you should understand
the mechanics before outsourcing them), but know the landscape:

- [`backtrader`](https://www.backtrader.com/) — popular, mature, good docs
- [`vectorbt`](https://vectorbt.dev/) — vectorized/fast, steeper learning curve
- [`zipline-reloaded`](https://github.com/stefan-jansen/zipline-reloaded) — maintained fork of Quantopian's old engine

## 3.4 Optional but worth knowing exists

- SQL — for querying larger historical datasets (you likely already know this)
- `Jupyter` notebooks — the standard quant research environment for exploration (you likely already use these)
- Basics of a faster language (C++/Rust) — only relevant later if you go toward low-latency execution (Module 7); not needed for research-track work

---

## Done when you can:

- Load, clean, and resample real market data fluently in pandas without looking up basic syntax
- Have a reusable data-fetching utility you'll keep using in later modules
- Explain what a backtesting framework does and name 2-3 options, without necessarily having picked one yet

Next: [04_financial_markets_instruments](../04_financial_markets_instruments/README.md)
