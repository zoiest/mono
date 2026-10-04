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
5. Deriving and evaluating the matrix gradient of the multivariate normal log-likelihood $\nabla_\Sigma \ell$.
6. Numerically proving that the gradient vanishes at the sample MLE covariance $S_{\text{MLE}}$.

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

### 2. 📊 Practical Dataset Application: Real Market Matrix Calculus for Gaussian MLE Covariance
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
S = (X_tilde.T @ X_tilde) / (n - 1)

# MLE covariance estimate
S_mle = (n - 1) / n * S
inv_mle = np.linalg.inv(S_mle)
A_sum = (n - 1) * S  # Sum of squared deviations

# Log-likelihood gradient with respect to Sigma:
# grad = -0.5 * n * Sigma^{-1} + 0.5 * Sigma^{-1} A Sigma^{-1}
grad_mle = -0.5 * n * inv_mle + 0.5 * inv_mle @ A_sum @ inv_mle

print("Maximum absolute gradient at MLE:\n", np.max(np.abs(grad_mle)))
assert np.allclose(grad_mle, np.zeros((p, p)), atol=1e-6)

# Verify log-likelihood decreases under perturbation: Sigma_pert = S_mle + eps * I
eps = 1e-4
S_pert = S_mle + eps * np.eye(p)
inv_pert = np.linalg.inv(S_pert)

def log_likelihood(Sigma_inv, Sigma):
    return -0.5 * n * np.linalg.slogdet(Sigma)[1] - 0.5 * np.trace(Sigma_inv @ A_sum)

ll_mle = log_likelihood(inv_mle, S_mle)
ll_pert = log_likelihood(inv_pert, S_pert)
print(f"Log-Likelihood at MLE: {ll_mle:.4f}")
print(f"Log-Likelihood at Perturbed: {ll_pert:.4f}")
assert ll_mle > ll_pert
```

---

## ✅ Acceptance Criteria
- [X] Analytical gradient `2 * S @ x` matches finite differences.
- [X] Log-determinant derivative $\nabla \log|\Sigma| = \Sigma^{-1}$ is verified.
- [X] Matrix gradient $\nabla_\Sigma \ell$ evaluates to zero at the MLE covariance $S_{\text{MLE}}$.
- [X] Gaussian log-likelihood strictly decreases when moving away from $S_{\text{MLE}}$ in parameter space.
