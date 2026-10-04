# Story 016: Eigenanalysis & The Spectral Decomposition Theorem

## User Story
**As a** applied mathematician,
**I want to** compute eigenvalues/eigenvectors of symmetric matrices and reconstruct matrices via the Spectral Theorem,
**So that** I can decompose covariance matrices into principal geometric axes and orthogonal subspaces..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 6: Eigenanalysis of Real Symmetric Matrices
* **Sections:** 6.1, 6.2, 6.4, 6.7.1 (Characteristic Equation, Symmetric Properties, Spectral Decomposition)

---

## 🎯 What You Will Learn
1. The Spectral Theorem: A = P Lambda P^T for real symmetric matrices.
2. Orthonormality of eigenvectors: P^T P = I.
3. Trace equals sum of eigenvalues; Determinant equals product of eigenvalues.
4. Rank equals number of non-zero eigenvalues.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Spectral Decomposition
```python
import numpy as np

# Symmetric matrix
S = np.array([[5.0, 2.0], [2.0, 2.0]])

# np.linalg.eigh guarantees real eigenvalues and orthonormal eigenvectors
evals, P = np.linalg.eigh(S)

# Orthonormality check
assert np.allclose(P.T @ P, np.eye(2))

# Spectral reconstruction: P @ diag(evals) @ P.T
S_rec = P @ np.diag(evals) @ P.T
assert np.allclose(S, S_rec)

# Trace and determinant checks
assert np.isclose(np.trace(S), np.sum(evals))
assert np.isclose(np.linalg.det(S), np.prod(evals))
print("Spectral Theorem successfully verified.")
```

---

## ✅ Acceptance Criteria
- [X] Eigenvalues and eigenvectors are computed using `np.linalg.eigh`.
- [X] Eigenvector matrix `P` is verified to be orthogonal (`P.T @ P == I`).
- [X] Spectral reconstruction `P @ diag(evals) @ P.T` recovers `S`.
- [X] Trace and determinant eigenvalue equalities are confirmed.
