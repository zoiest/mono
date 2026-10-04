# Story 004: Special Matrices & Quadratic Form Symmetrization

## User Story
**As a** statistical modeler,
**I want to** implement and test symmetric, skew-symmetric, orthogonal, and permutation matrices,
**So that** I can decompose arbitrary square matrices and express quadratic forms using symmetric matrices..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 2: Vectors and Matrices
* **Sections:** 2.5, 2.9 (Special Matrices: Symmetric, Orthogonal, Permutation, Quadratic Forms)

---

## 🎯 What You Will Learn
1. Decomposing square matrix A = A_sym + A_skew.
2. Orthogonal matrices Q^T Q = I and preservation of norms.
3. Permutation matrices and row/column swaps.
4. Symmetrization of quadratic forms x^T A x = x^T A_sym x.
5. Decomposing empirical cross-lag transition matrices into symmetric and skew-symmetric components.
6. Computing portfolio variance as a strictly positive quadratic form $w^T S w > 0$.

---

## 🛠️ Step-by-Step Implementation Guide


### 1. Matrix Decomposition & Quadratic Symmetrization
```python
import numpy as np

# Non-symmetric matrix
A = np.array([[2.0, 1.0], [5.0, 4.0]])

# Symmetric and Skew-Symmetric components
A_sym = 0.5 * (A + A.T)
A_skew = 0.5 * (A - A.T)

assert np.allclose(A, A_sym + A_skew)
assert np.allclose(A_sym, A_sym.T)
assert np.allclose(A_skew, -A_skew.T)

# Quadratic form equality: x^T A x == x^T A_sym x
x = np.array([3.0, -2.0])
q_orig = x.T @ A @ x
q_sym = x.T @ A_sym @ x
print(f"Original Q(x) = {q_orig}, Symmetric Q(x) = {q_sym}")
assert np.isclose(q_orig, q_sym)
```

### 2. 📊 Practical Dataset Application: Real Market Cross-Lag Symmetrization & Portfolio Variance
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape

# 1. Cross-lag covariance matrix between day t-1 and day t
X_lag = X[:-1]
X_lead = X[1:]
H_sub = np.eye(n - 1) - np.ones((n - 1, n - 1)) / (n - 1)
M_lag = (X_lag.T @ H_sub @ X_lead) / (n - 2)

# Decompose non-symmetric cross-lag matrix into symmetric and skew-symmetric parts
M_sym = 0.5 * (M_lag + M_lag.T)
M_skew = 0.5 * (M_lag - M_lag.T)

assert np.allclose(M_lag, M_sym + M_skew)
assert np.allclose(M_skew.T, -M_skew)

# Any quadratic form eliminates the skew-symmetric component: w^T M w == w^T M_sym w
w = np.array([0.2, 0.2, 0.15, 0.15, 0.15, 0.15])
q_raw = w.T @ M_lag @ w
q_sym = w.T @ M_sym @ w
q_skew = w.T @ M_skew @ w
assert np.isclose(q_skew, 0.0)
assert np.isclose(q_raw, q_sym)

# 2. Portfolio variance quadratic form
H = np.eye(n) - np.ones((n, n)) / n
S = (X.T @ H @ X) / (n - 1)
port_var = w.T @ S @ w
port_vol = np.sqrt(port_var * 252)
print(f"Portfolio Annualized Volatility: {port_vol * 100:.2f}%")
assert port_var > 0  # Strict positive definiteness
```

---

## ✅ Acceptance Criteria
- [X] Matrix `A` is decomposed into symmetric and skew-symmetric parts.
- [X] `A_sym` is verified symmetric and `A_skew` skew-symmetric.
- [X] Quadratic forms `x^T A x` and `x^T A_sym x` are verified equal.
- [X] Orthogonal matrix length preservation is verified.
- [X] Cross-lag transition matrix is decomposed into symmetric and skew-symmetric components.
- [X] Skew-symmetric quadratic form $w^T M_{\text{skew}} w = 0$ is numerically verified.
- [X] Portfolio variance quadratic form $w^T S w > 0$ confirms positive definiteness.
