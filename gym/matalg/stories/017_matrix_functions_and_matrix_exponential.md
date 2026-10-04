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

---

## ✅ Acceptance Criteria
- [X] `S_sqrt @ S_sqrt == S` is verified.
- [X] `P @ diag(exp(evals)) @ P.T` matches `scipy.linalg.expm(S)`.
