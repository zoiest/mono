# Story 012: The Weinstein-Aronszajn Identity & Rank-1 Updates

## User Story
**As a** machine learning engineer,
**I want to** implement the Weinstein-Aronszajn determinant identity and rank-1 determinant updates,
**So that** I can perform fast $O(n^2)$ determinant evaluations in Gaussian processes and active learning..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 4: Determinants
* **Sections:** 4.6 (A Key Property of Determinants: Weinstein-Aronszajn, Equicorrelation)

---

## 🎯 What You Will Learn
1. Weinstein-Aronszajn Identity: det(I_p + AB) = det(I_q + BA).
2. Rank-1 update formula: det(A + x y^T) = det(A) * (1 + y^T A^{-1} x).
3. Analytical determinant of equicorrelation matrix alpha I + beta 1 1^T.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Rank-1 Determinant Update
```python
import numpy as np

n = 4
A = np.diag([2.0, 3.0, 4.0, 5.0])
x = np.array([[1.0], [2.0], [1.0], [1.0]])
y = np.array([[2.0], [1.0], [3.0], [1.0]])

# Direct calculation
det_direct = np.linalg.det(A + x @ y.T)

# Fast rank-1 update formula: det(A) * (1 + y^T A^{-1} x)
det_A = np.prod(np.diag(A))
y_Ainv_x = (y.T @ (x / np.diag(A)[:, None]))[0, 0]
det_formula = det_A * (1.0 + y_Ainv_x)

print(f"Direct: {det_direct:.4f}, Formula: {det_formula:.4f}")
assert np.isclose(det_direct, det_formula)
```

---

## ✅ Acceptance Criteria
- [X] `det(I_p + AB) == det(I_q + BA)` verified for rectangular `A` and `B`.
- [X] Rank-1 update formula matches `np.linalg.det(A + x @ y.T)`.
- [X] Equicorrelation matrix determinant formula matches numerical calculation.
