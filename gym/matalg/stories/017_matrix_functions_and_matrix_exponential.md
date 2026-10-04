# Story 017: Matrix Functions, Square Roots, and the Matrix Exponential

## User Story
**As a** stochastic process modeler,
**I want to** compute matrix powers, matrix square roots $S^{1/2}$, and the matrix exponential $\exp(A)$,
**So that** I can perform Mahalanobis whitening and solve continuous-time Markov transition rates..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 6: Eigenanalysis of Real Symmetric Matrices
* **Sections:** 6.6, 6.7.1.1 (Matrix Exponential, Square Root of Positive Semi-Definite Matrices)

---

## 🎯 What You Will Learn
1. Defining f(A) = P f(Lambda) P^T via spectral decomposition.
2. Matrix square root S^{1/2} and inverse square root S^{-1/2} for Mahalanobis whitening.
3. Matrix exponential exp(A) = sum A^k / k! and comparison with scipy.linalg.expm.
4. Computing symmetric matrix square root $S^{1/2}$ and inverse square root $S^{-1/2}$.
5. Implementing Mahalanobis whitening transformation $Z = \tilde{X} S^{-1/2}$ to produce spherical uncorrelated returns.

---

## 🛠️ Step-by-Step Implementation Guide


### 1. Matrix Square Root & Exponential
```python
import numpy as np
import scipy.linalg as la

S = np.array([[4.0, 1.0], [1.0, 3.0]])
evals, P = np.linalg.eigh(S)

# Matrix square root S^{1/2}
S_sqrt = P @ np.diag(np.sqrt(evals)) @ P.T
assert np.allclose(S_sqrt @ S_sqrt, S)

# Matrix exponential exp(S)
S_exp = P @ np.diag(np.exp(evals)) @ P.T
S_exp_scipy = la.expm(S)
assert np.allclose(S_exp, S_exp_scipy)

print("Matrix square root and exponential verified.")
```

### 2. 📊 Practical Dataset Application: Real Market Matrix Square Root & Mahalanobis Whitening
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

# Spectral decomposition for matrix functions
lambdas, Q = np.linalg.eigh(S)

# Symmetric matrix square root and inverse square root
S_sqrt = Q @ np.diag(np.sqrt(lambdas)) @ Q.T
S_inv_sqrt = Q @ np.diag(1.0 / np.sqrt(lambdas)) @ Q.T

# Verification
assert np.allclose(S_sqrt @ S_sqrt, S)
assert np.allclose(S_inv_sqrt @ S @ S_inv_sqrt, np.eye(p))

# Mahalanobis Whitening Transformation: Z = X_tilde @ S^{-1/2}
Z = X_tilde @ S_inv_sqrt

# Covariance of whitened data must be identity matrix I_p
S_Z = (Z.T @ Z) / (n - 1)
assert np.allclose(S_Z, np.eye(p))
print("Whitening successful: Covariance of transformed returns equals I_6 exactly!")
```

---

## ✅ Acceptance Criteria
- [X] `S_sqrt @ S_sqrt == S` is verified.
- [X] `P @ diag(exp(evals)) @ P.T` matches `scipy.linalg.expm(S)`.
- [X] Symmetric square root $S^{1/2}$ and inverse square root $S^{-1/2}$ are computed via spectral decomposition.
- [X] Identities $S^{1/2} S^{1/2} = S$ and $S^{-1/2} S S^{-1/2} = I_6$ are confirmed.
- [X] Whitened return series $Z = \tilde{X} S^{-1/2}$ has empirical covariance equal to identity matrix $I_6$.
