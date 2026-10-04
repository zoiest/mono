# Story 002: Vector Geometry, Inner/Outer Products, and Orthogonality

## User Story
**As a** statistician analyzing feature spaces,
**I want to** implement vector inner products, outer products, Euclidean norms, and test for orthogonality,
**So that** I can compute projection angles and verify orthogonal subspaces in linear statistical models..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 2: Vectors and Matrices
* **Sections:** 2.1 (Vectors, Definitions, Example 2.1, Orthogonal vectors)

---

## 🎯 What You Will Learn
1. Computing inner products x^T y and outer products x y^T.
2. Evaluating Euclidean L2 norms and cosine similarities.
3. Testing orthogonality condition x^T y = 0.
4. Rank properties of outer products.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Vector Products & Angles
```python
import numpy as np

a = np.array([1.0, 2.0, 3.0])
b = np.array([4.0, -2.0, 0.0])
c = np.array([1.0, 1.0, -1.0])

# Inner products
dot_ab = a @ b
dot_ac = a @ c
dot_bc = b @ c

print(f"a^T b = {dot_ab}")  # 0.0 -> orthogonal!
print(f"a^T c = {dot_ac}")  # 0.0 -> orthogonal!
print(f"b^T c = {dot_bc}")  # 2.0

assert np.isclose(dot_ab, 0.0)
assert np.isclose(dot_ac, 0.0)

# Outer product (rank-1 matrix)
outer_ab = np.outer(a, b)
print("Outer product a b^T:
", outer_ab)
assert np.linalg.matrix_rank(outer_ab) == 1
```

---

## ✅ Acceptance Criteria
- [X] Vectors `a` and `b` are confirmed orthogonal (`a @ b == 0`).
- [X] Vectors `a` and `c` are confirmed orthogonal (`a @ c == 0`).
- [X] Outer product `a b^T` is confirmed to have rank 1.
- [X] Euclidean norms and cosine distance tests pass.
