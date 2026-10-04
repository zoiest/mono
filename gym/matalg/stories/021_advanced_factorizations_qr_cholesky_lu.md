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
4. Simulating correlated multi-asset returns using the Cholesky factor $S = L L^T$.
5. Demonstrating the QR decomposition relationship $S = \frac{1}{n-1} R^T R$.

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

### 2. 📊 Practical Dataset Application: Real Market Cholesky Simulation & QR Covariance
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape
H = np.eye(n) - np.ones((n, n)) / n
X_tilde = H @ X
S = (X_tilde.T @ X_tilde) / (n - 1)

# 1. Cholesky Factorization: S = L L^T
L = np.linalg.cholesky(S)
assert np.allclose(L @ L.T, S)
print("Cholesky factor L (lower triangular) verified.")

# 2. Correlated Monte Carlo Simulation
np.random.seed(42)
M_sim = 50000
Z_iid = np.random.randn(M_sim, p)
X_sim = Z_iid @ L.T  # Correlated asset returns
S_sim = np.cov(X_sim, rowvar=False)

# Check Monte Carlo convergence
assert np.allclose(S_sim, S, atol=2e-4)
print("Monte Carlo simulated covariance converged to empirical S within 0.02% error.")

# 3. QR Decomposition: X_tilde = Q R => S = (1/(n-1)) R^T R
Q_qr, R_qr = np.linalg.qr(X_tilde)
S_from_qr = (R_qr.T @ R_qr) / (n - 1)
assert np.allclose(S, S_from_qr)
print("QR covariance relationship S == (1/(n-1)) R^T R verified.")
```

---

## ✅ Acceptance Criteria
- [X] QR back-substitution produces identical OLS coefficients to normal equations.
- [X] Cholesky factor `L @ L.T` recovers target covariance.
- [X] Simulated samples have empirical covariance matching target $\Sigma$.
- [X] Cholesky decomposition $S = L L^T$ is computed and verified.
- [X] Correlated Monte Carlo returns generated via $Z L^T$ reproduce empirical covariance $S$.
- [X] QR factorization of centered returns verifies $S = \frac{1}{n-1} R^T R$.
