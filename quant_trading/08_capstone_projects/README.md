# Module 8: Capstone Projects

Everything before this was inputs. This module is where you prove you can
run the full research loop end to end, honestly. Pick at least one project
and take it all the way through — don't stop at "the backtest looks good."

Each project should produce a short **research write-up** (a few pages: 
hypothesis, data, methodology, results, and — critically — an honest section
on why the result might *not* be real, referencing the failure modes from
Module 6.1). That write-up is the actual deliverable, not the code. This is
exactly the format real quant researchers use to present ideas.

---

## Project ideas (pick 1-2, in increasing difficulty)

### A. Factor strategy backtest (easiest — builds on Module 5.1 + 6)

Pick a factor (value, momentum, or a combination), construct it properly on
a reasonably-sized universe (50-100 stocks, free data is fine), backtest it
with realistic transaction costs, and report full performance stats (Module
6.3). Explicitly test for overfitting by splitting into in-sample/out-of-sample
periods.

### B. Pairs trading / stat arb system (Module 5.3 + 6 + 7)

Find a cointegrated pair, build the full signal generation → backtest →
risk-managed position sizing pipeline. Add realistic execution assumptions
(Module 7.3) and show how much the "edge" degrades once you account for
spread and slippage.

### C. Options strategy analysis (Module 4.3 + 5.4)

Pick an options strategy (e.g. covered calls on an index), price it with your
own Black-Scholes implementation, backtest its historical payoff pattern
across various volatility regimes, and analyze the risk profile (max
loss/gain, Greeks exposure over time).

### D. ML-based signal with proper validation (Module 5.5 + 6 — hardest, plays to your strengths)

Build a simple ML model (start with something interpretable like logistic
regression or a small gradient-boosted tree — not a black box) to predict a
short-horizon direction or return, using **walk-forward validation** (not
standard k-fold — this is the López de Prado warning from Module 5.5 made
concrete). Be genuinely skeptical of any positive result; try to break it by
testing on a different time period or asset.

### E. Paper trading (optional, after any of the above)

Take a strategy you backtested and run it forward on a paper-trading account
(Interactive Brokers paper trading is free) for a few weeks. Compare live
paper performance to what the backtest predicted — the gap between the two
is itself a valuable lesson in everything Module 6 and 7 warned you about.

---

## What "done" looks like

A GitHub-able project folder per capstone containing:
- Clean, documented code (data loading → signal → backtest → metrics)
- A written report answering: what's the hypothesis, what did you find, and
  — most importantly — **what would make you doubt this result is real?**
- Equity curve, drawdown chart, and the standard tearsheet metrics from Module 6.3

If you can produce 2-3 of these honestly (including the "here's why this
might not be real" section), you're no longer "starting from scratch" —
you're doing the actual job.
