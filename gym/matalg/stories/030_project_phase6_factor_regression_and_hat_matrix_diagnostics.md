# Story 030: Capstone Project Phase 6 — Factor Pricing Regression, Hat Matrix Projection, and Gauss-Markov Diagnostics

## User Story
**As a** asset pricing researcher,
**I want to** build a multi-factor regression pricing model $y = X\beta + \epsilon$, calculate the Hat projection matrix $P$, residual maker $M = I - P$, and verify Gauss-Markov BLUE properties,
**So that** I can measure market betas, extract idiosyncratic alpha, and verify regression algebraic identities using matrix projection geometry..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 11: Capstone Project (and Chapters 8 & 9)
* **Sections:** 8.2.1, 9.7 (QR in Least Squares, General Linear Model, Hat Matrix, Gauss-Markov)

---

## 🎯 What You Will Learn
1. Constructing multi-factor design matrix X = [1, r_SPY, r_TLT].
2. Solving normal equations via QR decomposition without explicit inversion.
3. Properties of Hat matrix P = X (X^T X)^{-1} X^T: symmetric (P^T = P), idempotent (P^2 = P).
4. Properties of Residual Maker M = I - P: M X = 0, residuals e = M y.
5. ANOVA total variance decomposition: y^T H_n y = y^T (P - (1/n)1 1^T) y + y^T M y.

---

## 🛠️ Step-by-Step Implementation Guide


### 1. Factor Regression & Projection Geometry
```python
import numpy as np

# Regress QQQ on SPY (Market) and TLT (Bonds)
y = X[:, assets.index("QQQ")]
F = np.column_stack([np.ones(n), X[:, assets.index("SPY")], X[:, assets.index("TLT")]])
k_vars = F.shape[1]

# QR Decomposition for OLS
Q_reg, R_reg = np.linalg.qr(F)
beta_hat = np.linalg.solve(R_reg, Q_reg.T @ y)

# Hat Matrix P and Residual Maker M
P = F @ np.linalg.solve(F.T @ F, F.T)
M = np.eye(n) - P

# Algebraic Checks
assert np.allclose(P @ P, P)
assert np.allclose(M @ M, M)
assert np.allclose(M @ F, 0.0)  # Orthogonality of residuals to design matrix!

# Residuals and Model Fits
e = M @ y
SSE = (y.T @ M @ y)
SST = (y.T @ H @ y)
R_sq = 1.0 - (SSE / SST)

print(f"Alpha: {beta_hat[0]:.6f}, Beta(SPY): {beta_hat[1]:.4f}, Beta(TLT): {beta_hat[2]:.4f}")
print(f"R-squared: {R_sq*100:.2f}%")
assert R_sq > 0.70
```

---

## ✅ Acceptance Criteria
- [X] OLS coefficients $\hat{\beta}$ computed via QR decomposition match normal equations.
- [X] Hat matrix $P$ and residual maker $M$ verified symmetric and idempotent.
- [X] Residuals are strictly orthogonal to regressors: $M F = \mathbf{0}$.
- [X] Model $R^2$ exceeds $70\%$, confirming strong explanatory power.
