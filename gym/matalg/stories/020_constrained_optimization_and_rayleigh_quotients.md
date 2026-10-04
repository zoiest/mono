# Story 020: Constrained Optimization & Rayleigh Quotients

## User Story
**As a** optimization specialist,
**I want to** maximize quadratic forms under quadratic constraints using Lagrange multipliers and Rayleigh quotients,
**So that** I can solve eigenproblems arising in PCA, Fisher's discriminant analysis, and canonical correlation..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 7: Vector and Matrix Calculus
* **Sections:** 7.6 (Use of Eigenanalysis in Constrained Optimization)

---

## 🎯 What You Will Learn
1. Lagrangian formulation for maximizing x^T A x subject to x^T x = 1.
2. Derivation of the Rayleigh quotient R_A(x) = (x^T A x) / (x^T x).
3. Generalized Rayleigh quotient for x^T A x subject to x^T B x = 1.
4. Finding portfolio allocations that maximize and minimize volatility on the unit sphere $\|w\|_2 = 1$.
5. Validating the Rayleigh quotient bounds $\lambda_{\min}(S) \le w^T S w \le \lambda_{\max}(S)$.

---

## 🛠️ Step-by-Step Implementation Guide


### 1. Rayleigh Quotient Optimization
```python
import numpy as np

A = np.array([[5.0, 2.0], [2.0, 2.0]])
evals, evecs = np.linalg.eigh(A)

min_val, max_val = evals[0], evals[1]
v_min, v_max = evecs[:, 0], evecs[:, 1]

# Check extrema
R_max = (v_max.T @ A @ v_max) / (v_max.T @ v_max)
R_min = (v_min.T @ A @ v_min) / (v_min.T @ v_min)

assert np.isclose(R_max, max_val)
assert np.isclose(R_min, min_val)
print(f"Max Rayleigh quotient: {R_max:.4f}, Min: {R_min:.4f}")
```

### 2. 📊 Practical Dataset Application: Real Market Extremal Portfolios & Rayleigh Quotients
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape
H = np.eye(n) - np.ones((n, n)) / n
S = (X.T @ H @ X) / (n - 1)

# Spectral decomposition
lambdas, Q = np.linalg.eigh(S)
idx = np.argsort(lambdas)[::-1]
lambdas, Q = lambdas[idx], Q[:, idx]

# Extremal risk portfolios on unit sphere ||w||_2 = 1
w_max_risk = Q[:, 0]   # Eigenvector for lambda_max
w_min_risk = Q[:, -1]  # Eigenvector for lambda_min

var_max = w_max_risk.T @ S @ w_max_risk
var_min = w_min_risk.T @ S @ w_min_risk

assert np.isclose(var_max, lambdas[0])
assert np.isclose(var_min, lambdas[-1])
print(f"Max Annualized Volatility: {np.sqrt(var_max * 252) * 100:.2f}%")
print(f"Min Annualized Volatility: {np.sqrt(var_min * 252) * 100:.2f}%")

# Monte Carlo test of Rayleigh bounds: 10,000 random portfolios on unit sphere
np.random.seed(42)
W_rand = np.random.randn(10000, p)
W_rand /= np.linalg.norm(W_rand, axis=1, keepdims=True)
rand_vars = np.sum((W_rand @ S) * W_rand, axis=1)

assert np.all(rand_vars >= lambdas[-1] - 1e-10)
assert np.all(rand_vars <= lambdas[0] + 1e-10)
print("Rayleigh quotient bounds confirmed: lambda_min <= w^T S w <= lambda_max across all 10,000 portfolios!")
```

---

## ✅ Acceptance Criteria
- [X] Maximum Rayleigh quotient equals largest eigenvalue $\lambda_{\max}$.
- [X] Minimum Rayleigh quotient equals smallest eigenvalue $\lambda_{\min}$.
- [X] Maximum and minimum risk portfolios on unit sphere correspond to extremal eigenvectors of $S$.
- [X] Portfolio variances achieve theoretical Rayleigh bounds $\lambda_{\max}$ and $\lambda_{\min}$.
- [X] 10,000 random unit-norm allocations all obey $\lambda_{\min} \le w^T S w \le \lambda_{\max}$.
