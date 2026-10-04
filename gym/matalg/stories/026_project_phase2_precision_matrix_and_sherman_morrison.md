# Story 026: Capstone Project Phase 2 — Precision Matrix, Partial Correlation, and Online Sherman-Morrison

## User Story
**As a** algorithmic trader,
**I want to** evaluate condition number $\kappa(S)$, compute the precision matrix $\Theta = S^{-1}$ for partial correlations, and implement $O(p^2)$ streaming Sherman-Morrison updates,
**So that** I can isolate direct asset-to-asset dependencies and update risk parameters in real-time as streaming ticks arrive..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 11: Capstone Project (and Chapters 4 & 5)
* **Sections:** 4.1, 5.2, 5.4.2 (Conditioning, Inverses, Sherman-Morrison Formula)

---

## 🎯 What You Will Learn
1. Computing condition number kappa(S) to assess numerical stability.
2. Precision matrix Theta = S^{-1} and conditional independence in Gaussian graphical models.
3. Deriving partial correlation rho_{ij . rest} = -theta_{ij} / sqrt(theta_{ii} * theta_{jj}).
4. Streaming O(p^2) covariance inverse updates via the Sherman-Morrison rank-1 formula.

---

## 🛠️ Step-by-Step Implementation Guide


### 1. Precision Matrix & Streaming Update
```python
import numpy as np

# Continuing from Phase 1
cond_S = np.linalg.cond(S)
print(f"Condition number: {cond_S:.2f}")

Theta = np.linalg.inv(S)

# Partial Correlation Matrix
D_theta = np.diag(1.0 / np.sqrt(np.diag(Theta)))
P_corr = -D_theta @ Theta @ D_theta
np.fill_diagonal(P_corr, 1.0)
print("Partial Correlation (SPY vs QQQ | rest):", round(P_corr[0, 1], 3))

# Streaming update: New Day Returns
x_new = np.array([-0.012, -0.015, 0.004, -0.008, 0.007, -0.010])

# Exact batch calculation with n + 1 points
X_ext = np.vstack([X, x_new])
n_new = n + 1
H_new = np.eye(n_new) - np.ones((n_new, n_new)) / n_new
S_new = (X_ext.T @ H_new @ X_ext) / (n_new - 1)
inv_batch_new = np.linalg.inv(S_new)

# Sherman-Morrison Recursive Update
c = (n - 1) / n
delta = (x_new - xbar.flatten())[:, None]
gamma = 1.0 / (n + 1)
A_inv = Theta / c
denom = 1.0 + (gamma * delta.T @ A_inv @ delta)[0, 0]
inv_sm_new = A_inv - (gamma * A_inv @ delta @ delta.T @ A_inv) / denom

print("Sherman-Morrison matches full batch inversion:", np.allclose(inv_batch_new, inv_sm_new, atol=1e-5))
assert np.allclose(inv_batch_new, inv_sm_new, atol=1e-5)
```

---

## ✅ Acceptance Criteria
- [X] Condition number $\kappa(S)$ is computed and verified $< 100$.
- [X] Partial correlation matrix `P_corr` is computed from precision matrix $\Theta$.
- [X] Sherman-Morrison streaming update matches full batch inverse within $10^{-5}$.
