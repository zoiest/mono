# Story 013: Matrix Inversion & Numerical Conditioning

## User Story
**As a** scientific computing practitioner,
**I want to** measure matrix conditioning, avoid explicit matrix inversion, and use LAPACK solvers,
**So that** I can build numerically robust regression and estimation routines resistant to floating-point truncation..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 5: Inverses
* **Sections:** 5.1, 5.2, 5.3 (Inverses, Properties, Implementation in R)

---

## 🎯 What You Will Learn
1. Condition number kappa(A) = sigma_max / sigma_min.
2. Why np.linalg.solve(A, b) is faster and more accurate than inv(A) @ b.
3. Left inverse A_L = (A^T A)^{-1} A^T for overdetermined systems.
4. Right inverse A_R = A^T (A A^T)^{-1} for underdetermined systems.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Solving Linear Systems vs Inversion
```python
import numpy as np

# Hilbert matrix (notoriously ill-conditioned)
n = 5
H = np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])
b = np.ones(n)

cond_H = np.linalg.cond(H)
print(f"Condition number of Hilbert matrix: {cond_H:.2e}")

# Solve Ax = b
x_solve = np.linalg.solve(H, b)
x_inv = np.linalg.inv(H) @ b

res_solve = np.linalg.norm(H @ x_solve - b)
res_inv = np.linalg.norm(H @ x_inv - b)

print(f"Residual via solve: {res_solve:.2e}, Residual via inv: {res_inv:.2e}")
assert res_solve <= res_inv + 1e-12
```

---

## ✅ Acceptance Criteria
- [X] Condition number $\kappa(A)$ is computed via `np.linalg.cond`.
- [X] Residual of `np.linalg.solve` is demonstrated to be smaller or equal to `np.linalg.inv`.
- [X] Left inverse satisfies `A_L @ A == I_n` for full column rank matrix.
