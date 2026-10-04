# Story 008: Rank Factorization & Outer Products of Rank 1

## User Story
**As a** machine learning researcher,
**I want to** compute full rank factorizations $A = BC$ and analyze rank-1 structures $x y^T$,
**So that** I can implement low-rank matrix decompositions and identify rank-1 updates..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 3: Rank of Matrices
* **Sections:** 3.2 (Rank Factorization, Matrices of Rank 1)

---

## 🎯 What You Will Learn
1. Rank Factorization Theorem: A = BC with B full column rank, C full row rank.
2. Structure of rank-1 matrices: A = x y^T.
3. Eigenstructure of rank-1 matrices: non-zero eigenvalue equals y^T x.
4. Constructing rank factorizations from SVD or row echelon form.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Rank Factorization
```python
import numpy as np

# Rank 1 matrix A = x y^T
x = np.array([[2.0], [3.0], [1.0]])
y = np.array([[4.0], [5.0]])
A = x @ y.T
assert np.linalg.matrix_rank(A) == 1

# Rank factorization A = B @ C
B = x  # (3, 1) full column rank
C = y.T  # (1, 2) full row rank
assert np.allclose(A, B @ C)

# Rank 2 factorization via SVD
M = np.random.randn(4, 2) @ np.random.randn(2, 5)
U, s, Vt = np.linalg.svd(M, full_matrices=False)
r = np.linalg.matrix_rank(M)
B_svd = U[:, :r] @ np.diag(s[:r])
C_svd = Vt[:r, :]
assert np.allclose(M, B_svd @ C_svd)
```

---

## ✅ Acceptance Criteria
- [X] Outer product `x @ y.T` is verified to have rank 1.
- [X] Rank factorization `A = B @ C` is verified with full rank factors.
- [X] SVD-based rank factorization produces exact matrix reconstruction.
