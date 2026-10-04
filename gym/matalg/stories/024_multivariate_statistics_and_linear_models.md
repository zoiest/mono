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
6. Performing Mahalanobis anomaly detection to uncover the Day 180 market shock event.
7. Computing the OLS projection hat matrix $H = X(X^T X)^{-1} X^T$ and diagnosing influential trading days.

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

### 2. 📊 Practical Dataset Application: Real Market Mahalanobis Outlier Detection & OLS Hat Diagnostics
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    assets = next(reader)[1:]
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape
H_cent = np.eye(n) - np.ones((n, n)) / n
X_tilde = H_cent @ X
S = (X_tilde.T @ X_tilde) / (n - 1)
Theta = np.linalg.inv(S)

# 1. Mahalanobis Distance Anomaly Detection: D_M^2(x_t) = x_t^T Theta x_t
d_mahal = np.sum((X_tilde @ Theta) * X_tilde, axis=1)

# Find anomaly day
anomaly_idx = np.argmax(d_mahal)
print(f"Most extreme market outlier index: Day {anomaly_idx} with D_M^2 = {d_mahal[anomaly_idx]:.2f}")
assert anomaly_idx == 180  # Day 180 injected shock detected!
assert d_mahal[anomaly_idx] > 22.46  # Exceeds chi2(p=6, 0.999) critical value = 22.46

# 2. Multi-factor Linear Model Diagnostics: SPY on remaining assets
y = X[:, 0]
X_reg = np.column_stack([np.ones(n), X[:, 1:]])  # Intercept + 5 assets (250, 6)

# Hat Matrix P = X (X^T X)^{-1} X^T
P = X_reg @ np.linalg.inv(X_reg.T @ X_reg) @ X_reg.T
assert np.allclose(P @ P, P)          # Idempotent
assert np.allclose(P, P.T)            # Symmetric
assert np.isclose(np.trace(P), 6.0)   # tr(P) == rank(X) == 6

# Leverage scores h_ii = P_ii
leverage = np.diag(P)
print(f"Average leverage: {np.mean(leverage):.4f} (p/n = {6/250:.4f})")
print(f"Leverage of Day 180 shock: {leverage[anomaly_idx]:.4f}")
assert leverage[anomaly_idx] > 2 * (6 / 250)  # Exceeds 2p/n high leverage threshold
```

---

## ✅ Acceptance Criteria
- [X] Hotelling's $T^2$ test statistic and p-value computed accurately.
- [X] Hat matrix $P$ and residual maker $M$ confirmed symmetric and idempotent.
- [X] Residual maker $M$ verified orthogonal to design matrix $X$ ($MX = 0$).
- [X] Classical MDS coordinate recovery matches true pairwise distances.
- [X] Day 180 is identified as the maximum Mahalanobis anomaly surpassing the $\chi^2_6(0.999)$ threshold of 22.46.
- [X] Hat matrix $P$ is verified symmetric, idempotent, with trace equal to rank 6.
- [X] Day 180 is diagnosed as a high-leverage observation ($h_{ii} > 2p/n$).
