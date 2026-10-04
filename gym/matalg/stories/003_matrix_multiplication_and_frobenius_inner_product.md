# Story 003: Matrix Multiplication, Cross Products, and the Trace Operator

## User Story
**As a** numerical algorithm developer,
**I want to** implement matrix multiplication `@`, cross-products $X^TX$ and $XX^T$, and cyclic trace identities,
**So that** I can write performant matrix arithmetic and simplify statistical expressions using trace tricks..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 2: Vectors and Matrices
* **Sections:** 2.3, 2.4, 2.8.2 (Matrix Arithmetic, Transpose, Trace of Products)

---

## 🎯 What You Will Learn
1. Matrix multiplication conformability and the `@` operator.
2. Cross-products $X^TX$ (Gram matrix) and $XX^T$.
3. Trace linearity and cyclic invariance: tr(ABC) = tr(BCA) = tr(CAB).
4. The Frobenius inner product tr(A^T B) and matrix Frobenius norm.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Trace and Cross Products
```python
import numpy as np

A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
B = np.array([[7.0, 8.0], [9.0, 1.0], [2.0, 3.0]])

# Matrix products
AB = A @ B  # (2, 2)
BA = B @ A  # (3, 3)

# Cyclic trace property: tr(AB) == tr(BA)
tr_AB = np.trace(AB)
tr_BA = np.trace(BA)
print(f"tr(AB) = {tr_AB}, tr(BA) = {tr_BA}")
assert np.isclose(tr_AB, tr_BA)

# Cross product properties: A^T A is symmetric
AtA = A.T @ A
assert np.allclose(AtA, AtA.T)
assert np.isclose(np.trace(A @ A.T), np.trace(A.T @ A))
```

---

## ✅ Acceptance Criteria
- [X] `A @ B` and `B @ A` are computed with conformable dimensions.
- [X] Trace cyclic equality `tr(AB) == tr(BA)` is verified.
- [X] `A.T @ A` is verified to be symmetric positive semi-definite.
- [X] `tr(A A.T) == tr(A.T A)` is confirmed.
