# Story 006: Partitioned Matrices & Block Multiplication

## User Story
**As a** scientific computing engineer,
**I want to** implement block matrix assembly and verify conformable block multiplication rules,
**So that** I can manipulate partitioned matrices and construct composite block systems for ANOVA and linear models..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 2: Vectors and Matrices
* **Sections:** 2.6 (Partitioned Matrices, Sub-matrices, Block Manipulation)

---

## 🎯 What You Will Learn
1. Block matrix slicing and assembly via np.block.
2. Verifying block matrix multiplication rules.
3. Block diagonal matrices and sparse representation.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Block Matrix Multiplication
```python
import numpy as np

A11 = np.array([[1.0, 2.0], [3.0, 4.0]])
A12 = np.array([[5.0], [6.0]])
A21 = np.array([[7.0, 8.0]])
A22 = np.array([[9.0]])

A = np.block([[A11, A12], [A21, A22]])

B11 = np.array([[2.0, 0.0], [1.0, 3.0]])
B12 = np.array([[1.0], [0.0]])
B21 = np.array([[4.0, 2.0]])
B22 = np.array([[5.0]])

B = np.block([[B11, B12], [B21, B22]])

# Block multiplication by parts
C11 = A11 @ B11 + A12 @ B21
C12 = A11 @ B12 + A12 @ B22
C21 = A21 @ B11 + A22 @ B21
C22 = A21 @ B12 + A22 @ B22
C_block = np.block([[C11, C12], [C21, C22]])

# Full matrix product
C_direct = A @ B

print("C via direct multiplication:
", C_direct)
assert np.allclose(C_block, C_direct)
```

---

## ✅ Acceptance Criteria
- [X] Partitioned matrix `A` and `B` assemble correctly with `np.block`.
- [X] Sub-block multiplication matches full matrix multiplication `A @ B` exactly.
