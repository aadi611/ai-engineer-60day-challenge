# Quantitative Trading — From Scratch

A self-contained curriculum to go from "strong programmer, weak on markets/math"
to being able to reason like a quant researcher: read a strategy paper, know
which statistical tools apply, build and honestly backtest it, and understand
the market structure that determines whether it survives contact with real
order books.

This is **not** tied to the 60-day AI Engineer clock — it's a parallel,
self-paced track. Treat it as roughly **12-16 weeks at ~1-1.5 hrs/day**, but
the point is depth, not the calendar. Don't move to the next module until you
can do the exercises without looking things up.

**Why this order:** most people jump straight to "build a trading bot" and
hit a wall because they don't have the statistics to know if their backtest
result is signal or noise, or the finance vocabulary to understand what
they're even modeling. This curriculum front-loads math and finance literacy
*specifically the slices a quant needs*, not a full degree's worth, then
builds strategy/backtesting/microstructure knowledge on top of that
foundation.

---

## How to use this

Each module folder has its own `README.md` with:
- What you're learning and why it matters for quant work specifically
- Free/low-cost resources (course, book, paper) — in the order to consume them
- A concrete exercise or build to prove you actually absorbed it (you're a
  programmer — build things, don't just read)

Work through modules **0 → 7 roughly in order** (math and stats are load-bearing
for everything after). Module 8 (capstone) is where it all comes together.

---

## Module map

| Module | Topic | Why it matters |
|---|---|---|
| [00_math_foundations](00_math_foundations/README.md) | Calculus, linear algebra, optimization | The language every model below is written in |
| [01_probability_statistics](01_probability_statistics/README.md) | Probability, distributions, statistical inference, time series | The actual toolkit for "is this edge real or noise" |
| [02_finance_economics](02_finance_economics/README.md) | Financial accounting, macro/micro economics, corporate finance basics | What the numbers you're modeling *mean* |
| [03_programming_data](03_programming_data/README.md) | Python quant stack, data wrangling, numerical computing | Turning theory into working code (you're already strong here — this is mostly new libraries) |
| [04_financial_markets_instruments](04_financial_markets_instruments/README.md) | Equities, fixed income, derivatives, FX, how markets/exchanges work | The instruments and mechanics you'll actually trade or model |
| [05_quant_strategies](05_quant_strategies/README.md) | Factor investing, momentum/mean-reversion, stat arb, options strategies | The actual "quant" playbook |
| [06_backtesting_risk](06_backtesting_risk/README.md) | Backtesting methodology, overfitting/data snooping, portfolio risk, position sizing | Why 90% of backtested strategies are lies, and how not to write one |
| [07_market_microstructure](07_market_microstructure/README.md) | Order books, market making, execution algos, latency | What happens when your strategy meets the real market |
| [08_capstone_projects](08_capstone_projects/README.md) | End-to-end strategy research → backtest → paper trade | Prove it end to end |

---

## Suggested pace (adjust freely)

- **Weeks 1-3** — Module 0 (math) + Module 1 start (probability)
- **Weeks 4-6** — Module 1 finish (statistics, time series) + Module 2 (finance/econ)
- **Weeks 7-8** — Module 3 (programming/data stack) — runs in parallel with everything, really
- **Weeks 9-10** — Module 4 (markets & instruments)
- **Weeks 11-13** — Module 5 (strategies) + Module 6 (backtesting/risk)
- **Week 14** — Module 7 (microstructure)
- **Weeks 15-16+** — Module 8 (capstone)

## Core reference library (the "always open" books)

You'll see these referenced repeatedly across modules — worth owning/bookmarking:

- *Options, Futures, and Other Derivatives* — John Hull (the standard derivatives reference)
- *Advances in Financial Machine Learning* — Marcos López de Prado (backtesting/overfitting, written for people exactly like you: programmers entering quant)
- *Quantitative Trading* — Ernest Chan (practical, approachable, good second book after this curriculum)
- [QuantStart](https://www.quantstart.com/articles/) — free article series, roughly matches this curriculum's structure
- [Investopedia](https://www.investopedia.com/) — your go-to for "wait, what does this term mean" lookups throughout

## Tracking progress

Log what you did each session the same way the AI-engineer track does — see
[../daily_logs/](../daily_logs/) for the format. You can either reuse that folder
with a `quant-` prefix on entries, or keep a `progress_log.md` inside this folder;
your call, just be consistent.
