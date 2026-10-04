# Story 011: Schur Complements & Block Partitioned Determinants

## User Story
**As a** probabilistic modeler,
**I want to** compute determinants of partitioned matrices using Schur complements,
**So that** I can evaluate joint and conditional likelihoods in structured Gaussian graphical models..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 4: Determinants
* **Sections:** 4.5 (Determinants of Partitioned Matrices, Schur Complement)

---

## 🎯 What You Will Learn
1. Block Gaussian elimination and factorization.
2. Schur complement formula: det(M) = det(A) * det(D - C A^{-1} B).
3. Block triangular matrices: det([[A, B], [0, D]]) = det(A) det(D).

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Schur Complement Determinant
```python
import numpy as np

A = np.array([[4.0, 1.0], [1.0, 3.0]])
B = np.array([[1.0, 0.0], [0.0, 2.0]])
C = B.T
D = np.array([[5.0, 1.0], [1.0, 4.0]])

M = np.block([[A, B], [C, D]])

det_direct = np.linalg.det(M)
S_A = D - C @ np.linalg.inv(A) @ B
det_schur = np.linalg.det(A) * np.linalg.det(S_A)

print("Direct det(M):", det_direct)
print("Schur formula det(A) * det(D - C A^{-1} B):", det_schur)
assert np.isclose(det_direct, det_schur)
```

---

## ✅ Acceptance Criteria
- [X] Block partitioned matrix `M` determinant is computed directly.
- [X] Schur complement formula matches direct determinant within machine precision.
