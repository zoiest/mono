# Story 018: Singular Value Decomposition (SVD) & Low-Rank Approximation

## User Story
**As a** data compression & ML engineer,
**I want to** implement SVD $A = U \Sigma V^T$ and verify the Eckart-Young-Mirsky optimal low-rank approximation,
**So that** I can compress high-dimensional feature spaces and perform robust pseudo-inversion..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 6: Eigenanalysis of Real Symmetric Matrices
* **Sections:** 6.7.2 (Singular Value Decomposition of an m x n Matrix)

---

## 🎯 What You Will Learn
1. Economy SVD vs Full SVD in NumPy.
2. Relationship between singular values of A and eigenvalues of A^T A and A A^T.
3. The Eckart-Young-Mirsky optimal rank-k approximation theorem.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. SVD and Rank-k Reconstruction
```python
import numpy as np

# Non-square matrix
A = np.array([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
    [7.0, 8.0, 9.0],
    [10.0, 11.0, 12.0]
])

U, s, Vt = np.linalg.svd(A, full_matrices=False)

# Exact reconstruction
A_rec = U @ np.diag(s) @ Vt
assert np.allclose(A, A_rec)

# Best Rank-1 approximation
A_rank1 = s[0] * np.outer(U[:, 0], Vt[0, :])
print("Rank-1 approximation:
", A_rank1)
assert np.linalg.matrix_rank(A_rank1) == 1
```

---

## ✅ Acceptance Criteria
- [X] SVD reconstruction `U @ diag(s) @ Vt` recovers original matrix `A`.
- [X] Singular values match square roots of eigenvalues of `A.T @ A`.
- [X] Rank-1 approximation is verified to have rank 1.
