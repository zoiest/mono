# Story 028: Capstone Project Phase 4 — Mahalanobis Anomaly Detection, Cholesky Whitening, and Hotelling's $T^2$

## User Story
**As a** systemic risk auditor,
**I want to** implement lower-triangular Cholesky whitening $Z = (X - \bar{X})(L^{-1})^T$, calculate Mahalanobis distances, and detect market shock days via Hotelling's $T^2$,
**So that** I can monitor multi-asset markets in real-time and flag systemic shocks and outlier regime shifts..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 11: Capstone Project (and Chapters 8 & 9)
* **Sections:** 8.2.3, 9.2.1, 9.2.5.1 (Cholesky, Standardization, One-Sample Hotelling T2)

---

## 🎯 What You Will Learn
1. Cholesky decomposition S = L L^T where L is lower triangular.
2. Whitening transformation Z = (X - 1 xbar^T)(L^{-1})^T satisfying Cov(Z) = I_p.
3. Equivalence of Mahalanobis distance D_M^2(x_t) = (x_t - xbar)^T S^{-1} (x_t - xbar) and ||z_t||_2^2.
4. Hypothesis testing under Chi-Square(p=6) distribution and pinpointing Day 180 shock.

---

## 🛠️ Step-by-Step Implementation Guide


### 1. Whitening & Anomaly Detection
```python
import numpy as np
import scipy.stats as stats

# Cholesky Factorization
L = np.linalg.cholesky(S)
assert np.allclose(L @ L.T, S)

# Whitening Transformation
Z = (X - xbar.T) @ np.linalg.inv(L).T
cov_Z = np.cov(Z, rowvar=False)
assert np.allclose(cov_Z, np.eye(p), atol=0.02)

# Mahalanobis Distance: ||z_t||_2^2
d_mahal = np.sum(Z ** 2, axis=1)

# Critical threshold at alpha = 0.001
crit = stats.chi2.ppf(0.999, df=p)
anomalies = np.where(d_mahal > crit)[0]

print(f"Threshold (df={p}, p=0.001): {crit:.2f}")
print("Detected Anomaly Day Indices:", anomalies)
assert 180 in anomalies
print(f"Day 180 Mahalanobis distance: {d_mahal[180]:.2f} (Extreme shock successfully detected!)")
```

---

## ✅ Acceptance Criteria
- [X] Cholesky factor satisfies `L @ L.T == S`.
- [X] Whitened data matrix `Z` has covariance matrix matching $I_p$ within empirical tolerance.
- [X] Day 180 is identified as an extreme market anomaly with $p < 0.001$.
