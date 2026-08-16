# Module 0: Math Foundations

You don't need a pure-math degree. You need enough calculus, linear algebra,
and optimization to read a quant paper without flinching at the notation, and
to implement the models yourself instead of treating them as black boxes.

**Skip nothing here even if it looks "too basic"** — the goal is fluency, not
recognition. You should be able to derive things on paper, not just remember
that they exists.

---

## 0.1 Calculus (1.5-2 weeks)

What you need: derivatives, partial derivatives, chain rule, Taylor series,
integrals (conceptually — you'll rarely hand-integrate in practice), and
*why* these matter for finance (e.g. Taylor expansion is the entire basis of
option "Greeks").

- [3Blue1Brown — Essence of Calculus](https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr) (YouTube, free) — do this first, it builds intuition nothing else does
- [Khan Academy — Calculus 1 & 2](https://www.khanacademy.org/math/calculus-1) (free, with exercises — actually do the problem sets)
- Focus areas: derivatives/gradients, Taylor series expansion, basic optimization (finding minima/maxima)

**Exercise:** derive the Taylor expansion of a function by hand for 2-3
examples, then explain in your own words (a short note, not code) why Delta,
Gamma, and Theta in options pricing are just first/second-order Taylor terms.
You'll revisit this concretely in Module 5.

## 0.2 Linear Algebra (1.5-2 weeks)

What you need: vectors, matrices, matrix multiplication, eigenvalues/eigenvectors,
covariance matrices, matrix decomposition (PCA). This is the backbone of
portfolio theory (covariance matrices) and factor models (PCA/regression).

- [3Blue1Brown — Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) (YouTube, free) — same reasoning as above, build the geometric intuition first
- [Khan Academy — Linear Algebra](https://www.khanacademy.org/math/linear-algebra) (free)
- Focus areas: matrix operations, eigendecomposition, covariance matrices, PCA (you'll use PCA for yield curves and factor models later)

**Exercise:** in Python (NumPy), build a covariance matrix from a small set of
made-up stock return series, compute its eigenvalues/eigenvectors, and explain
what the top eigenvector represents (this is literally PCA — the seed of
factor investing in Module 5).

## 0.3 Optimization (1 week)

What you need: unconstrained optimization (gradient descent — you already
know this from ML), constrained optimization (Lagrange multipliers), and
convexity. This is the machinery behind portfolio optimization (Markowitz).

- [Khan Academy — Lagrange multipliers](https://www.khanacademy.org/math/multivariable-calculus/applications-of-multivariable-derivatives/constrained-optimization/a/lagrange-multipliers-single-constraint) (free)
- [Convex Optimization — Boyd & Vandenberghe](https://web.stanford.edu/~boyd/cvxbook/) (free PDF from Stanford) — skim Ch. 1-4 only, don't try to absorb the whole book

**Exercise:** solve a simple 2-asset portfolio allocation problem by hand
using Lagrange multipliers (minimize variance subject to a target return
constraint) — this is literally the core of Markowitz mean-variance
optimization you'll implement in Module 5/6.

## 0.4 (Optional but valuable) Stochastic calculus primer

Full stochastic calculus is graduate-level and not required to get started,
but if you plan to go toward options/derivatives pricing seriously, get the
vocabulary now so it's not alien later.

- [Stochastic Calculus for Finance video series — YouTube (search "Brownian motion finance intro")] or just read the intro chapter of Hull's derivatives book (see main README)
- Just aim to recognize terms: Brownian motion, Itô's lemma, stochastic differential equations — you do NOT need to derive these yet

---

## Done when you can:

- Explain a derivative and gradient in plain English and compute one by hand
- Build and interpret a covariance matrix and its eigendecomposition in NumPy
- Solve a constrained optimization problem with Lagrange multipliers
- Recognize (not yet master) stochastic calculus vocabulary

Next: [01_probability_statistics](../01_probability_statistics/README.md)
