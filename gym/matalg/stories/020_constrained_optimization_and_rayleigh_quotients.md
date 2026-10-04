# Story 020: Constrained Optimization & Rayleigh Quotients

## User Story
**As a** optimization specialist,
**I want to** maximize quadratic forms under quadratic constraints using Lagrange multipliers and Rayleigh quotients,
**So that** I can solve eigenproblems arising in PCA, Fisher's discriminant analysis, and canonical correlation..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 7: Vector and Matrix Calculus
* **Sections:** 7.6 (Use of Eigenanalysis in Constrained Optimization)

---

## 🎯 What You Will Learn
1. Lagrangian formulation for maximizing x^T A x subject to x^T x = 1.
2. Derivation of the Rayleigh quotient R_A(x) = (x^T A x) / (x^T x).
3. Generalized Rayleigh quotient for x^T A x subject to x^T B x = 1.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Rayleigh Quotient Optimization
```python
import numpy as np

A = np.array([[5.0, 2.0], [2.0, 2.0]])
evals, evecs = np.linalg.eigh(A)

min_val, max_val = evals[0], evals[1]
v_min, v_max = evecs[:, 0], evecs[:, 1]

# Check extrema
R_max = (v_max.T @ A @ v_max) / (v_max.T @ v_max)
R_min = (v_min.T @ A @ v_min) / (v_min.T @ v_min)

assert np.isclose(R_max, max_val)
assert np.isclose(R_min, min_val)
print(f"Max Rayleigh quotient: {R_max:.4f}, Min: {R_min:.4f}")
```

---

## ✅ Acceptance Criteria
- [X] Maximum Rayleigh quotient equals largest eigenvalue $\lambda_{\max}$.
- [X] Minimum Rayleigh quotient equals smallest eigenvalue $\lambda_{\min}$.
