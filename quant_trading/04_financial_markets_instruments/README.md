# Module 4: Financial Markets & Instruments

Now that you have math, stats, and finance vocabulary, learn the actual
instruments and market mechanics you'll be modeling and trading.

---

## 4.1 Equities & how exchanges work (1 week)

- [Investopedia — Stock Market Basics](https://www.investopedia.com/investing/investing-101/) 
- Focus: order types (market/limit/stop), bid-ask spread, exchanges vs. dark pools, market makers, how an order actually gets filled

**Exercise:** open a broker's paper-trading account (e.g. Interactive
Brokers paper trading, or any free simulator) and place a few limit and
market orders. Watch how the bid-ask spread moves. This is worth doing
hands-on even briefly — it makes order-book concepts in Module 7 concrete
instead of abstract.

## 4.2 Fixed income (bonds) (1 week)

- [Investopedia — Bonds Basics](https://www.investopedia.com/investing/bonds-fixed-income/)
- Khan Academy has a bonds section under macro/finance too
- Focus: yield, duration, convexity (this connects directly back to Module 0's Taylor series — duration/convexity are first/second-order price sensitivity to yield, exactly like Delta/Gamma for options), the yield curve (you touched this in Module 2.3 — now go deeper on *why* it's shaped the way it is)

## 4.3 Derivatives: options and futures (2 weeks — the most important sub-module here)

- **Options, Futures, and Other Derivatives — John Hull** (the standard textbook; read Ch. 1-13 for now, covering forwards/futures, options mechanics, and Black-Scholes — save exotic derivatives for later if ever)
- [Khan Academy — Options, swaps, futures, MBSs, CDOs, and other derivatives](https://www.khanacademy.org/economics-finance-domain/core-finance/derivative-securities) (free, good supplement/primer before or alongside Hull)
- Focus: what a call/put option is, payoff diagrams, put-call parity, the Greeks (Delta/Gamma/Theta/Vega — and now you'll recognize these as Taylor series terms from Module 0.1), Black-Scholes assumptions and where they break

**Exercise:** implement Black-Scholes pricing from scratch in Python (not
just call a library) for a call and put option. Then compute the Greeks
numerically (via finite differences) and verify they roughly match the
closed-form Greek formulas. Plot a payoff diagram for a simple options
strategy (e.g. a covered call or a straddle).

## 4.4 FX and commodities (0.5 week — survey level)

- [Investopedia — Forex Trading basics](https://www.investopedia.com/forex/forex-basics-setting-up-account/)
- Just get fluent in the vocabulary (pips, carry trade, spot vs. forward) — go deeper later only if you specialize in this asset class

## 4.5 Market participants & structure

- Read about the different players: retail, market makers, hedge funds, prop trading firms, HFT firms — and how their incentives differ (this matters when you get to Module 7 microstructure and start reasoning about *who* is on the other side of your trade)

---

## Done when you can:

- Explain the difference between a market order and a limit order and why the distinction matters for execution
- Explain duration/convexity for bonds and connect it explicitly to Taylor series
- Price a European option with Black-Scholes from scratch and explain what each Greek measures
- Name the major categories of market participants and how their incentives differ

Next: [05_quant_strategies](../05_quant_strategies/README.md)
