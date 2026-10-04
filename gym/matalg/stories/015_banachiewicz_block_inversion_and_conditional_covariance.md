# Story 015: Block Inversion & Conditional Gaussian Covariance

## User Story
**As a** Bayesian statistician,
**I want to** invert block matrices using the Banachiewicz formula and compute conditional covariance matrices,
**So that** I can derive precision matrices and conditional Gaussian distributions in multivariate data analysis..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 5: Inverses
* **Sections:** 5.5 (Inverses of Partitioned Matrices, Banachiewicz Inversion)

---

## 🎯 What You Will Learn
1. Banachiewicz block inversion formula.
2. Connection between the Schur complement and conditional variance: Cov(X_2 | X_1).
3. Precision matrix structure in Gaussian graphical models.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Banachiewicz Block Inversion
```python
import numpy as np

A = np.array([[4.0, 1.0], [1.0, 3.0]])
B = np.array([[1.0], [0.5]])
C = B.T
D = np.array([[2.0]])

M = np.block([[A, B], [C, D]])
M_inv_direct = np.linalg.inv(M)

# Block inversion formula
A_inv = np.linalg.inv(A)
S_A = D - C @ A_inv @ B
S_A_inv = np.linalg.inv(S_A)

B11 = A_inv + A_inv @ B @ S_A_inv @ C @ A_inv
B12 = -A_inv @ B @ S_A_inv
B21 = -S_A_inv @ C @ A_inv
B22 = S_A_inv

M_inv_block = np.block([[B11, B12], [B21, B22]])

assert np.allclose(M_inv_direct, M_inv_block)
print("Banachiewicz block inversion verified.")
```

---

## ✅ Acceptance Criteria
- [X] Banachiewicz block inversion matches `np.linalg.inv(M)` within machine precision.
- [X] Conditional covariance `D - C @ A_inv @ B` verified as Schur complement.
