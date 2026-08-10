# Module 7: Market Microstructure

Everything so far assumed you can trade at the price you see. In reality,
your own order moves the price, other participants react faster than you,
and the order book has structure that determines whether a strategy that
looks great on daily bars survives when you actually try to execute it. This
module is what separates "backtest quant" from someone who understands what
happens when a strategy meets a real market.

---

## 7.1 The order book (1 week)

- [Investopedia — Order Book basics](https://www.investopedia.com/terms/o/order-book.asp)
- [QuantStart — Market Microstructure articles](https://www.quantstart.com/articles/)
- Focus: bid/ask, depth, the limit order book as a queue, market orders vs. limit orders and their tradeoffs, how the bid-ask spread compensates market makers for adverse selection risk

**Exercise:** if your data source allows it (some free crypto exchange APIs
expose live order books, e.g. Binance's public API), pull a live order book
snapshot and visualize the depth on each side. If not, read through a
detailed order book walkthrough and diagram one by hand from a real example.

## 7.2 Market making (0.5-1 week)

- [QuantStart — intro to market making](https://www.quantstart.com/articles/)
- Focus: how a market maker profits from the spread, inventory risk, adverse selection, why market making isn't "free money" (you're providing insurance against informed traders)

## 7.3 Execution algorithms (0.5 week)

- Read about TWAP, VWAP, and implementation shortfall — the standard algos used to execute large orders without moving the market against yourself
- [Investopedia — VWAP](https://www.investopedia.com/terms/v/vwap.asp)

**Why this matters even for a small retail-scale strategy:** it builds the
right instinct — a backtest that assumes you always get filled at the closing
price is implicitly assuming infinite liquidity and zero market impact. Real
execution costs are why many "profitable" strategies from Module 5/6 don't
survive live trading at any meaningful size.

## 7.4 Latency & HFT (survey only, unless you specialize here)

- Read enough to understand what HFT firms actually do (mostly market
  making and cross-venue arbitrage at microsecond scale) and why this is a
  fundamentally different business than the strategy research you've been
  doing in Modules 5-6 — different skills (systems/networking engineering),
  different capital requirements, different edge sources
- Not a priority to go deep here unless you specifically want the quant-dev/HFT track later

---

## Done when you can:

- Read and explain a limit order book snapshot
- Explain why market making isn't risk-free and where its profit actually comes from
- Explain TWAP/VWAP and why execution algorithms exist
- Articulate why backtested returns often don't survive contact with real execution costs and market impact

Next: [08_capstone_projects](../08_capstone_projects/README.md)
