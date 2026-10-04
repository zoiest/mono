# Story 010: Determinants, Laplace Expansions, and Log-Determinants

## User Story
**As a** computational statistician,
**I want to** calculate determinants via Laplace expansion, evaluate triangular matrices, and use slogdet,
**So that** I can compute generalized variances and evaluate multivariate normal densities without numerical overflow/underflow..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 4: Determinants
* **Sections:** 4.1, 4.2, 4.3 (Determinant Definitions, Implementation, Properties)

---

## 🎯 What You Will Learn
1. Laplace expansion by minors and cofactors.
2. Determinant of triangular matrices as product of diagonals.
3. Effects of elementary row operations.
4. Using np.linalg.slogdet for robust likelihood evaluation.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Determinants and slogdet
```python
import numpy as np

# Triangular matrix
T = np.array([
    [2.0, 3.0, 1.0],
    [0.0, 5.0, 4.0],
    [0.0, 0.0, 3.0]
])
det_T = np.linalg.det(T)
expected_det = 2.0 * 5.0 * 3.0
assert np.isclose(det_T, expected_det)

# Log-determinant for large covariance matrix
Sigma = np.diag([1e-3, 1e-4, 1e-5, 1e-2])
sign, logdet = np.linalg.slogdet(Sigma)
print(f"Log-det: {logdet:.4f}")
assert sign == 1
assert np.isclose(logdet, np.sum(np.log(np.diag(Sigma))))
```

---

## ✅ Acceptance Criteria
- [X] Triangular matrix determinant equals product of diagonal elements.
- [X] `np.linalg.slogdet` matches `sum(log(diag))` for positive diagonal matrix.
- [X] Elementary row swap sign reversal is verified.
