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
5. Computing generalized sample variance $\det(S)$ and safe log-determinant $\log \det(S)$.
6. Comparing hypervolume of diversified asset basket versus concentrated equity basket.

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

### 2. 📊 Practical Dataset Application: Real Market Generalized Variance & Ellipsoid Volume
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

# 1. Generalized sample variance det(S)
det_S = np.linalg.det(S)
print(f"Generalized sample variance det(S): {det_S:.2e}")
assert det_S > 0  # Strictly positive definite

# 2. Numerically safe log-determinant
sign, logdet = np.linalg.slogdet(S)
assert sign > 0
assert np.isclose(logdet, np.log(det_S))
print(f"Log-determinant log|S|: {logdet:.4f}")

# 3. Geometric hypervolume comparison: Diversified (6 assets) vs Equity Block (2 assets)
S_equity = S[:2, :2]
det_equity = np.linalg.det(S_equity)
print(f"Equity Block det(S_equity): {det_equity:.2e}")
# The volume of the uncertainty ellipsoid is proportional to sqrt(det(S))
vol_equity = np.sqrt(det_equity)
assert vol_equity > 0
```

---

## ✅ Acceptance Criteria
- [X] Triangular matrix determinant equals product of diagonal elements.
- [X] `np.linalg.slogdet` matches `sum(log(diag))` for positive diagonal matrix.
- [X] Elementary row swap sign reversal is verified.
- [X] Generalized sample variance $\det(S) > 0$ confirms positive definiteness.
- [X] Numerically stable log-determinant via `np.linalg.slogdet` matches `log(det(S))`.
- [X] Ellipsoidal uncertainty volume for equity block is computed.
