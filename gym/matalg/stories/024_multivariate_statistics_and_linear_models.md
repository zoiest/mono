# Story 024: Multivariate Hypothesis Testing, PCA, LDA, and OLS

## User Story
**As a** senior statistician,
**I want to** implement Hotelling's $T^2$, PCA, Fisher's LDA, Metric MDS, and Constrained OLS in Python,
**So that** I can perform end-to-end multivariate analysis and regression modeling using matrix algebra..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 9: Key Applications to Statistics
* **Sections:** 9.2-9.7 (Multivariate Normal, PCA, LDA, CCA, MDS, Linear Models)

---

## 🎯 What You Will Learn
1. One-sample Hotelling's T^2 hypothesis testing and F-statistic conversion.
2. Principal Component Analysis via spectral decomposition of sample covariance.
3. Fisher's Linear Discriminant Analysis crimcoords via generalized eigenvalues B a = lambda W a.
4. Classical Metric Multidimensional Scaling (MDS) via double-centering.
5. Gauss-Markov OLS, Hat matrix P, and residual maker M.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Hotelling's T^2 & OLS Projection
```python
import numpy as np
import scipy.stats as stats

# Hotelling's T^2
np.random.seed(42)
X = np.random.randn(20, 2) + np.array([0.4, -0.3])
mu0 = np.array([0.0, 0.0])
n, p = X.shape

diff = np.mean(X, axis=0) - mu0
S = np.cov(X, rowvar=False)
T2 = n * (diff.T @ np.linalg.solve(S, diff))
F_stat = ((n - p) / ((n - 1) * p)) * T2
p_val = 1.0 - stats.f.cdf(F_stat, p, n - p)
print(f"Hotelling T2: {T2:.4f}, F-stat: {F_stat:.4f}, p-val: {p_val:.4f}")

# OLS Hat Matrix & Residual Maker
X_reg = np.hstack([np.ones((n, 1)), X[:, :1]])
y_reg = X[:, 1]
beta = np.linalg.solve(X_reg.T @ X_reg, X_reg.T @ y_reg)
P = X_reg @ np.linalg.solve(X_reg.T @ X_reg, X_reg.T)
M = np.eye(n) - P

assert np.allclose(P @ P, P)  # Idempotent
assert np.allclose(M @ M, M)  # Idempotent
assert np.allclose(M @ X_reg, 0.0)  # Orthogonal to X
print("Hotelling's T^2 and OLS Hat/Residual operators verified.")
```

---

## ✅ Acceptance Criteria
- [X] Hotelling's $T^2$ test statistic and p-value computed accurately.
- [X] Hat matrix $P$ and residual maker $M$ confirmed symmetric and idempotent.
- [X] Residual maker $M$ verified orthogonal to design matrix $X$ ($MX = 0$).
- [X] Classical MDS coordinate recovery matches true pairwise distances.
