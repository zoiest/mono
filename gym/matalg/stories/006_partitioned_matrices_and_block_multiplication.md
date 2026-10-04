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
4. Partitioning the 6 assets into Equities/Energy vs Defensive/Income blocks.
5. Computing block covariance sub-matrices and verifying cross-block transpositions.

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

print("C via direct multiplication:\n", C_direct)
assert np.allclose(C_block, C_direct)
```

### 2. 📊 Practical Dataset Application: Real Market Asset Class Partitioning & Block Covariance
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape
H = np.eye(n) - np.ones((n, n)) / n
X_tilde = H @ X

# Partition assets into two economic blocks:
# Block 1: Growth & Cyclicals (SPY, QQQ, XLE -> indices 0, 1, 3)
# Block 2: Defensive & Yield (GLD, TLT, VNQ -> indices 2, 4, 5)
idx1 = [0, 1, 3]
idx2 = [2, 4, 5]
X1 = X_tilde[:, idx1]  # (250, 3)
X2 = X_tilde[:, idx2]  # (250, 3)

# Block covariance computation
S11 = (X1.T @ X1) / (n - 1)  # (3, 3) Equities auto-covariance
S22 = (X2.T @ X2) / (n - 1)  # (3, 3) Defensive auto-covariance
S12 = (X1.T @ X2) / (n - 1)  # (3, 3) Cross-covariance
S21 = (X2.T @ X1) / (n - 1)  # (3, 3) Cross-covariance

assert np.allclose(S12, S21.T)

# Assemble 2x2 block matrix
S_block = np.block([[S11, S12], [S21, S22]])

# Compare with reordered full covariance matrix
S_full = (X_tilde.T @ X_tilde) / (n - 1)
idx_reordered = idx1 + idx2
S_reordered = S_full[np.ix_(idx_reordered, idx_reordered)]
assert np.allclose(S_block, S_reordered)
print("Block Covariance Matrix assembled successfully:\n", np.round(S_block * 1e4, 2))
```

---

## ✅ Acceptance Criteria
- [X] Partitioned matrix `A` and `B` assemble correctly with `np.block`.
- [X] Sub-block multiplication matches full matrix multiplication `A @ B` exactly.
- [X] Assets are partitioned into two $(250, 3)$ economic blocks.
- [X] Cross-covariance symmetry $S_{12} = S_{21}^T$ is verified.
- [X] Full covariance assembled via `np.block` matches indexed slice of $S$.
