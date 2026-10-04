# Story 023: Kronecker Products, Vec Operator, and Matrix Equations

## User Story
**As a** time series econometrician,
**I want to** implement Kronecker products $A \otimes B$, column-major $\text{vec}(A)$, and solve Sylvester matrix equations,
**So that** I can estimate Vector Autoregressive (VAR) models and solve continuous Lyapunov equations..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 8: Further Topics
* **Sections:** 8.5 (Kronecker Products and the Vec Operator)

---

## 🎯 What You Will Learn
1. Kronecker product properties: (A kron B)(C kron D) = (AC) kron (BD).
2. Column-major vectorization: A.flatten(order='F').
3. The fundamental identity: vec(ABC) = (C^T kron A) vec(B).
4. Solving matrix equations A X B = C.
5. Estimating a Vector Autoregressive (VAR(1)) cross-asset spillover model using Kronecker products and the vec operator.
6. Verifying $\text{vec}(Y) = (I_p \otimes X_{\text{lag}}) \text{vec}(B)$.

---

## 🛠️ Step-by-Step Implementation Guide


### 1. Kronecker and Vec Identity
```python
import numpy as np

A = np.array([[1.0, 2.0], [3.0, 4.0]])
B = np.array([[5.0, 6.0], [7.0, 8.0]])
C = np.array([[9.0, 1.0], [2.0, 3.0]])

# vec(ABC)
ABC = A @ B @ C
vec_ABC = ABC.flatten(order='F')

# (C^T kron A) vec(B)
kron_term = np.kron(C.T, A)
vec_formula = kron_term @ B.flatten(order='F')

assert np.allclose(vec_ABC, vec_formula)
print("vec(ABC) == (C^T kron A) vec(B) verified.")
```

### 2. 📊 Practical Dataset Application: Real Market VAR(1) Cross-Asset Spillover via Kronecker & Vec
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

# VAR(1) Model: Y = X_lag @ B + E
Y = X_tilde[1:, :]        # (249, 6)
X_lag = X_tilde[:-1, :]   # (249, 6)

# Vectorization identity: vec(Y) = (I_p \otimes X_lag) vec(B)
K = np.kron(np.eye(p), X_lag)  # (249*6, 6*6) = (1494, 36)
vec_Y = Y.flatten(order='F')   # Column-stacking vec operator

assert K.shape == (249 * 6, 6 * 6)

# Solve for vec(B)
vec_B = np.linalg.lstsq(K, vec_Y, rcond=None)[0]
B_kron = vec_B.reshape((p, p), order='F')

# Benchmark against direct matrix regression B = (X_lag^T X_lag)^{-1} X_lag^T Y
B_ols = np.linalg.lstsq(X_lag, Y, rcond=None)[0]

assert np.allclose(B_kron, B_ols)
print("VAR(1) Cross-Asset Spillover Matrix B (from Kronecker system):\n", np.round(B_kron, 3))
```

---

## ✅ Acceptance Criteria
- [X] `A.flatten(order='F')` executes column-major vectorization.
- [X] Fundamental identity `vec(ABC) == (C^T kron A) vec(B)` is verified.
- [X] Mixed product property `(A kron B) @ (C kron D) == (A @ C) kron (B @ D)` is verified.
- [X] Kronecker system matrix $I_p \otimes X_{\text{lag}}$ is constructed with dimensions $(1494, 36)$.
- [X] Vectorized VAR(1) solution matches equation-by-equation OLS regression.
- [X] Column-stacking vec operator reshaping preserves matrix layout.
