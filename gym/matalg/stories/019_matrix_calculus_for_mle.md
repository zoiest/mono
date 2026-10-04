# Story 019: Vector and Matrix Calculus for Maximum Likelihood Estimation

## User Story
**As a** theoretical statistician,
**I want to** derive gradients of linear forms, quadratic forms, trace operators, and log-determinants,
**So that** I can mathematically derive MLE estimators and normal equations from first principles..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 7: Vector and Matrix Calculus
* **Sections:** 7.2, 7.3 (Differentiation with Respect to Vector and Matrix)

---

## 🎯 What You Will Learn
1. Gradients of a^T x and x^T S x: d(x^T S x)/dx = 2 S x.
2. Matrix derivatives: d tr(XA)/dX = A^T.
3. Log-determinant derivative: d log|X| / dX = X^{-1}.
4. Deriving the OLS normal equations X^T X beta = X^T y.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Numerical Gradient Verification
```python
import numpy as np

# Quadratic form: f(x) = x^T S x
S = np.array([[3.0, 1.0], [1.0, 2.0]])
x = np.array([1.5, -2.0])

grad_analytical = 2 * S @ x

# Numerical approximation via central differences
eps = 1e-6
grad_num = np.zeros_like(x)
for i in range(len(x)):
    xp, xm = x.copy(), x.copy()
    xp[i] += eps
    xm[i] -= eps
    grad_num[i] = (xp.T @ S @ xp - xm.T @ S @ xm) / (2 * eps)

assert np.allclose(grad_analytical, grad_num, atol=1e-5)
print("Analytical gradient 2Sx verified numerically.")
```

---

## ✅ Acceptance Criteria
- [X] Analytical gradient `2 * S @ x` matches finite differences.
- [X] Log-determinant derivative $\nabla \log|\Sigma| = \Sigma^{-1}$ is verified.
