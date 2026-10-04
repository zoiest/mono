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
4. Partitioning covariance into Equities ($A$) and Non-Equities ($D$).
5. Computing the Schur complement conditional covariance $D - C A^{-1} B$ and verifying the block determinant identity.

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

### 2. 📊 Practical Dataset Application: Real Market Schur Complement & Information Reduction
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape
H = np.eye(n) - np.ones((n, n)) / n
S = (X.T @ H @ X) / (n - 1)

# Partition S into Equities (A: SPY, QQQ) and Hedges/Commodities (D: GLD, XLE, TLT, VNQ)
A = S[:2, :2]
B = S[:2, 2:]
C = S[2:, :2]
D = S[2:, 2:]

# Schur complement: conditional covariance of Non-Equities given Equities
S_schur = D - C @ np.linalg.inv(A) @ B
print("Schur Complement (Conditional Covariance D|A) shape:", S_schur.shape)

# Verify Block Determinant Identity: det(S) == det(A) * det(S_schur)
det_S = np.linalg.det(S)
det_A = np.linalg.det(A)
det_schur = np.linalg.det(S_schur)

print(f"det(S): {det_S:.2e}")
print(f"det(A) * det(S_schur): {det_A * det_schur:.2e}")
assert np.isclose(det_S, det_A * det_schur)

# Information reduction: conditioning reduces generalized variance
assert det_schur < np.linalg.det(D)
print("Information reduction verified: det(D|A) < det(D)")
```

---

## ✅ Acceptance Criteria
- [X] Block partitioned matrix `M` determinant is computed directly.
- [X] Schur complement formula matches direct determinant within machine precision.
- [X] Schur complement conditional covariance $S / A = D - C A^{-1} B$ is computed.
- [X] Block determinant identity $\det(S) = \det(A) \det(D - C A^{-1} B)$ is confirmed.
- [X] Conditioning reduces generalized variance: $\det(D - C A^{-1} B) < \det(D)$.
