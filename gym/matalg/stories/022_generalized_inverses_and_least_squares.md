# Story 022: Generalized Inverses & The Moore-Penrose Pseudoinverse

## User Story
**As a** linear algebra researcher,
**I want to** compute the Moore-Penrose pseudoinverse $A^+$ and solve underdetermined linear systems,
**So that** I can compute minimum-norm solutions to rank-deficient regression models..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 8: Further Topics
* **Sections:** 8.3 (Generalized Inverses, Moore-Penrose, Solutions of Linear Equations)

---

## 🎯 What You Will Learn
1. The four Penrose conditions for A^+.
2. Using np.linalg.pinv for rank-deficient matrices.
3. General solution to consistent systems: x = A^- y + (I - A^- A) w.
4. Minimum norm least squares solutions.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Moore-Penrose Pseudoinverse Verification
```python
import numpy as np

# Rank-deficient 2x3 matrix
A = np.array([[1.0, 2.0, 3.0], [2.0, 4.0, 6.0]])
A_pinv = np.linalg.pinv(A)

# Check all 4 Penrose conditions:
assert np.allclose(A @ A_pinv @ A, A)                     # 1. A A^+ A = A
assert np.allclose(A_pinv @ A @ A_pinv, A_pinv)           # 2. A^+ A A^+ = A^+
assert np.allclose((A @ A_pinv).T, A @ A_pinv)           # 3. (A A^+)^T = A A^+
assert np.allclose((A_pinv @ A).T, A_pinv @ A)           # 4. (A^+ A)^T = A^+ A
print("All 4 Moore-Penrose conditions verified.")
```

---

## ✅ Acceptance Criteria
- [X] All four Penrose conditions are satisfied within machine precision.
- [X] Pseudoinverse solves underdetermined systems with minimum Euclidean norm.
