# Story 021: Advanced Factorizations: QR, Cholesky, and LU

## User Story
**As a** quantitative developer,
**I want to** implement QR decomposition for regression and Cholesky decomposition for correlated Gaussian sampling,
**So that** I can perform fast matrix solves and simulate correlated multivariate distributions..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 8: Further Topics
* **Sections:** 8.2 (Further Matrix Decompositions: QR, LU, Cholesky)

---

## 🎯 What You Will Learn
1. QR decomposition: X = Q R, and solving R beta = Q^T y.
2. Cholesky decomposition: Sigma = L L^T for positive definite covariance.
3. Simulating multivariate normals: X = mu + L Z.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. QR Least Squares & Cholesky Simulation
```python
import numpy as np

# QR Least Squares
X = np.array([[1.0, 1.0], [1.0, 2.0], [1.0, 3.0], [1.0, 4.0]])
y = np.array([2.0, 3.0, 5.0, 7.0])

Q, R = np.linalg.qr(X)
beta_qr = np.linalg.solve(R, Q.T @ y)
beta_direct = np.linalg.inv(X.T @ X) @ X.T @ y
assert np.allclose(beta_qr, beta_direct)

# Cholesky Simulation
Sigma = np.array([[4.0, 1.2], [1.2, 1.0]])
L = np.linalg.cholesky(Sigma)
np.random.seed(42)
Z = np.random.randn(2, 50000)
X_sim = (L @ Z).T
cov_emp = np.cov(X_sim, rowvar=False)
assert np.allclose(Sigma, cov_emp, atol=0.05)
print("QR and Cholesky algorithms successfully verified.")
```

---

## ✅ Acceptance Criteria
- [X] QR back-substitution produces identical OLS coefficients to normal equations.
- [X] Cholesky factor `L @ L.T` recovers target covariance.
- [X] Simulated samples have empirical covariance matching target $\Sigma$.
