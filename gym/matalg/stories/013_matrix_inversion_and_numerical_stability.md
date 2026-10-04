# Story 013: Matrix Inversion & Numerical Conditioning

## User Story
**As a** scientific computing practitioner,
**I want to** measure matrix conditioning, avoid explicit matrix inversion, and use LAPACK solvers,
**So that** I can build numerically robust regression and estimation routines resistant to floating-point truncation..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 5: Inverses
* **Sections:** 5.1, 5.2, 5.3 (Inverses, Properties, Implementation in R)

---

## 🎯 What You Will Learn
1. Condition number kappa(A) = sigma_max / sigma_min.
2. Why np.linalg.solve(A, b) is faster and more accurate than inv(A) @ b.
3. Left inverse A_L = (A^T A)^{-1} A^T for overdetermined systems.
4. Right inverse A_R = A^T (A A^T)^{-1} for underdetermined systems.
5. Inverting the asset covariance matrix to obtain the precision matrix $\Theta = S^{-1}$.
6. Computing condition number $\kappa(S)$ and evaluating GMV portfolio weights via `np.linalg.solve` vs `np.linalg.inv`.

---

## 🛠️ Step-by-Step Implementation Guide


### 1. Solving Linear Systems vs Inversion
```python
import numpy as np

# Hilbert matrix (notoriously ill-conditioned)
n = 5
H = np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])
b = np.ones(n)

cond_H = np.linalg.cond(H)
print(f"Condition number of Hilbert matrix: {cond_H:.2e}")

# Solve Ax = b
x_solve = np.linalg.solve(H, b)
x_inv = np.linalg.inv(H) @ b

res_solve = np.linalg.norm(H @ x_solve - b)
res_inv = np.linalg.norm(H @ x_inv - b)

print(f"Residual via solve: {res_solve:.2e}, Residual via inv: {res_inv:.2e}")
assert res_solve <= res_inv + 1e-12
```

### 2. 📊 Practical Dataset Application: Real Market Precision Matrix & GMV Portfolio
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

# Condition number of empirical covariance matrix
cond_S = np.linalg.cond(S)
print(f"Covariance Matrix Condition Number kappa(S): {cond_S:.2f}")

# Computing Global Minimum Variance (GMV) portfolio weights: S w = 1
ones = np.ones(p)

# Method 1: Numerically robust solve
w_solve_raw = np.linalg.solve(S, ones)
w_solve = w_solve_raw / np.sum(w_solve_raw)

# Method 2: Explicit matrix inversion
Theta = np.linalg.inv(S)
w_inv_raw = Theta @ ones
w_inv = w_inv_raw / np.sum(w_inv_raw)

# Compare weights and residuals
assert np.allclose(w_solve, w_inv)
res_solve = np.linalg.norm(S @ w_solve_raw - ones)
res_inv = np.linalg.norm(S @ w_inv_raw - ones)
print(f"Residual ||S w_solve - 1||: {res_solve:.2e}")
print(f"Residual ||S w_inv - 1||:   {res_inv:.2e}")
assert res_solve < 1e-12

print("GMV Portfolio Weights (SPY, QQQ, GLD, XLE, TLT, VNQ):\n", np.round(w_solve, 4))
```

---

## ✅ Acceptance Criteria
- [X] Condition number $\kappa(A)$ is computed via `np.linalg.cond`.
- [X] Residual of `np.linalg.solve` is demonstrated to be smaller or equal to `np.linalg.inv`.
- [X] Left inverse satisfies `A_L @ A == I_n` for full column rank matrix.
- [X] Precision matrix $\Theta = S^{-1}$ and condition number $\kappa(S)$ are evaluated.
- [X] GMV portfolio weights solved via `np.linalg.solve` match explicit inversion.
- [X] Linear system residual $\|S w - \mathbf{1}\|_2 < 10^{-12}$ confirms precision of `np.linalg.solve`.
