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
5. Resolving multicollinearity in asset replication regressions using the Moore-Penrose pseudoinverse $X^+$.
6. Proving that the pseudoinverse selects the minimum $L_2$-norm coefficient vector.

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

### 2. 📊 Practical Dataset Application: Real Market Asset Replication via Pseudoinverse
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

# Replicating SPY (col 0) using remaining 5 assets
y = X[:, 0]
X_other = X[:, 1:]

# Inject collinearity: duplicate column 0 (QQQ)
X_coll = np.column_stack([X_other, X_other[:, 0]])  # (250, 6), rank 5
assert np.linalg.matrix_rank(X_coll) == 5

# Normal equations matrix X^T X is singular
try:
    np.linalg.inv(X_coll.T @ X_coll)
    assert False
except np.linalg.LinAlgError:
    print("X_coll^T X_coll is singular, as expected.")

# Solve via Moore-Penrose Pseudoinverse
pinv_X = np.linalg.pinv(X_coll)
beta_pinv = pinv_X @ y

# Verify normal equations are satisfied: X^T X beta == X^T y
assert np.allclose(X_coll.T @ X_coll @ beta_pinv, X_coll.T @ y)

# Verify minimum norm property splits weight evenly between duplicated assets
print(f"Weight on QQQ original:  {beta_pinv[0]:.4f}")
print(f"Weight on QQQ duplicate: {beta_pinv[-1]:.4f}")
assert np.isclose(beta_pinv[0], beta_pinv[-1])
print(f"L2 norm of pseudoinverse coefficients: {np.linalg.norm(beta_pinv):.4f}")
```

---

## ✅ Acceptance Criteria
- [X] All four Penrose conditions are satisfied within machine precision.
- [X] Pseudoinverse solves underdetermined systems with minimum Euclidean norm.
- [X] Collinear replication design matrix has $\text{rank}(X_{\text{coll}}) = 5 < 6$.
- [X] Pseudoinverse solution $\hat{\beta} = X_{\text{coll}}^+ y$ satisfies normal equations.
- [X] Coefficients for collinear columns are split equally to achieve minimum $L_2$ norm.
