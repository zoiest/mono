# Story 029: Capstone Project Phase 5 — Markowitz Minimum-Variance Portfolio via Constrained Optimization

## User Story
**As a** investment strategist,
**I want to** derive and solve the Global Minimum Variance (GMV) portfolio $w^* = \frac{S^{-1}\mathbf{1}}{\mathbf{1}^T S^{-1} \mathbf{1}}$ using Lagrange multipliers and matrix inversion,
**So that** I can construct risk-optimal asset allocations mathematically guaranteed to minimize portfolio volatility..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 11: Capstone Project (and Chapters 5 & 7)
* **Sections:** 5.1, 7.2.3, 7.6 (Quadratic Forms, Lagrange Multipliers, Constrained Optimization)

---

## 🎯 What You Will Learn
1. Formulating portfolio risk minimization as constrained quadratic optimization: min w^T S w s.t. w^T 1 = 1.
2. Solving the Lagrangian system via matrix calculus: 2 S w - lambda 1 = 0.
3. Analytic solution w* = S^{-1} 1 / (1^T S^{-1} 1) and minimum portfolio variance sigma_{min}^2 = 1 / (1^T S^{-1} 1).
4. Verifying Markowitz diversification theorem: portfolio volatility is strictly lower than every individual asset.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Optimal GMV Portfolio Allocation
```python
import numpy as np

ones_p = np.ones((p, 1))
S_inv = np.linalg.inv(S)

# Analytical GMV Weights
w_gmv = (S_inv @ ones_p / (ones_p.T @ S_inv @ ones_p)[0, 0]).flatten()
assert np.isclose(np.sum(w_gmv), 1.0)

# Portfolio volatility vs individual volatilities
var_gmv = w_gmv.T @ S @ w_gmv
vol_gmv_ann = np.sqrt(var_gmv * 252)
indiv_vols_ann = np.sqrt(np.diag(S) * 252)

print("GMV Weights (%):")
for a, w in zip(assets, w_gmv):
    print(f"  {a:>4}: {w*100:+6.2f}%")

print(f"
GMV Annualized Volatility: {vol_gmv_ann*100:.2f}%")
print(f"Lowest Individual Asset Volatility: {np.min(indiv_vols_ann)*100:.2f}%")
assert vol_gmv_ann < np.min(indiv_vols_ann)
```

---

## ✅ Acceptance Criteria
- [X] Optimal portfolio weights sum to exactly $1.0$ (`sum(w_gmv) == 1`).
- [X] Annualized GMV portfolio volatility is strictly lower than every component asset's volatility.
- [X] Weight derivation via Lagrange multipliers verified algebraically.
