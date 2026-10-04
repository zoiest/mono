# Story 014: Patterned Inverses & The Sherman-Morrison Formula

## User Story
**As a** real-time systems engineer,
**I want to** implement $O(n^2)$ inverse updates via Sherman-Morrison and invert equicorrelation matrices,
**So that** I can perform online sequential parameter updates in streaming Kalman filters and regression..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 5: Inverses
* **Sections:** 5.4 (Inverses of Patterned Matrices, Sherman-Morrison)

---

## 🎯 What You Will Learn
1. Inverting equicorrelation matrices alpha I + beta 1 1^T analytically.
2. The Sherman-Morrison formula: (A + x y^T)^{-1} = A^{-1} - (A^{-1} x y^T A^{-1}) / (1 + y^T A^{-1} x).
3. The Woodbury identity for rank-k updates.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Sherman-Morrison Update
```python
import numpy as np

A = np.array([[4.0, 1.0], [1.0, 3.0]])
A_inv = np.linalg.inv(A)

x = np.array([[1.0], [2.0]])
y = np.array([[2.0], [-1.0]])

# Direct inverse of update
inv_direct = np.linalg.inv(A + x @ y.T)

# Fast Sherman-Morrison formula
denom = 1.0 + (y.T @ A_inv @ x)[0, 0]
inv_sm = A_inv - (A_inv @ x @ y.T @ A_inv) / denom

print("Direct inverse:
", inv_direct)
print("Sherman-Morrison formula:
", inv_sm)
assert np.allclose(inv_direct, inv_sm)
```

---

## ✅ Acceptance Criteria
- [X] Sherman-Morrison formula matches `np.linalg.inv(A + x @ y.T)`.
- [X] Equicorrelation inverse formula verified against `np.linalg.inv`.
