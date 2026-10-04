# Story 005: The Centering Matrix $H_n$ and Sample Covariance Computation

## User Story
**As a** multivariate data analyst,
**I want to** implement the centering matrix $H_n = I_n - \frac{1}{n}\mathbf{1}\mathbf{1}^T$ and calculate sample covariance matrices,
**So that** I can perform mean-centering and compute sample variance-covariance matrices directly via algebraic matrix multiplication..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 2: Vectors and Matrices
* **Sections:** 2.5.6.1, 2.12.3 (The Centering Matrix Hn, Sample Statistics in R)

---

## 🎯 What You Will Learn
1. Properties of H_n: symmetry, idempotency (H_n^2 = H_n), and null space H_n 1 = 0.
2. Rank and trace of H_n: tr(H_n) = n - 1.
3. Mean centering of data matrix X: X_c = H_n X.
4. Calculating sample covariance S = (1 / (n - 1)) * X^T H_n X.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Centering Matrix Construction & Covariance
```python
import numpy as np

def make_centering_matrix(n: int) -> np.ndarray:
    return np.eye(n) - np.ones((n, n)) / n

n = 5
H = make_centering_matrix(n)
ones = np.ones(n)

# Algebraic verifications
assert np.allclose(H, H.T)              # Symmetric
assert np.allclose(H @ H, H)            # Idempotent
assert np.allclose(H @ ones, 0.0)       # Annihilator
assert np.isclose(np.trace(H), n - 1)   # Rank / Trace

# Covariance calculation
X = np.array([
    [10.0, 2.0],
    [12.0, 4.0],
    [14.0, 5.0],
    [16.0, 9.0],
    [18.0, 10.0]
])

S_matrix = (X.T @ H @ X) / (n - 1)
S_numpy = np.cov(X, rowvar=False)

print("S via Centering Matrix:
", S_matrix)
assert np.allclose(S_matrix, S_numpy)
```

---

## ✅ Acceptance Criteria
- [X] `H_n` satisfies `H^T == H`, `H @ H == H`, and `H @ 1 == 0`.
- [X] `tr(H_n) == n - 1` is verified.
- [X] `X.T @ H_n @ X / (n - 1)` exactly matches `np.cov(X, rowvar=False)`.
