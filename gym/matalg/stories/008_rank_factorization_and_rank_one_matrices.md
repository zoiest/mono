# Story 008: Rank Factorization & Outer Products of Rank 1

## User Story
**As a** machine learning researcher,
**I want to** compute full rank factorizations $A = BC$ and analyze rank-1 structures $x y^T$,
**So that** I can implement low-rank matrix decompositions and identify rank-1 updates..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 3: Rank of Matrices
* **Sections:** 3.2 (Rank Factorization, Matrices of Rank 1)

---

## 🎯 What You Will Learn
1. Rank Factorization Theorem: A = BC with B full column rank, C full row rank.
2. Structure of rank-1 matrices: A = x y^T.
3. Eigenstructure of rank-1 matrices: non-zero eigenvalue equals y^T x.
4. Constructing rank factorizations from SVD or row echelon form.
5. Performing rank-1 decomposition of centered returns to extract the systematic market factor.
6. Verifying the outer product structure of the leading factor approximation.

---

## 🛠️ Step-by-Step Implementation Guide


### 1. Rank Factorization
```python
import numpy as np

# Rank 1 matrix A = x y^T
x = np.array([[2.0], [3.0], [1.0]])
y = np.array([[4.0], [5.0]])
A = x @ y.T
assert np.linalg.matrix_rank(A) == 1

# Rank factorization A = B @ C
B = x  # (3, 1) full column rank
C = y.T  # (1, 2) full row rank
assert np.allclose(A, B @ C)

# Rank 2 factorization via SVD
M = np.random.randn(4, 2) @ np.random.randn(2, 5)
U, s, Vt = np.linalg.svd(M, full_matrices=False)
r = np.linalg.matrix_rank(M)
B_svd = U[:, :r] @ np.diag(s[:r])
C_svd = Vt[:r, :]
assert np.allclose(M, B_svd @ C_svd)
```

### 2. 📊 Practical Dataset Application: Real Market Systematic Factor Rank-1 Factorization
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

# Rank-1 Market Factor Factorization via SVD
U, Sig, Vt = np.linalg.svd(X_tilde, full_matrices=False)

# Dominant mode: sigma_1 * u_1 * v_1^T
f1 = Sig[0] * U[:, 0]    # Factor scores (250,)
beta1 = Vt[0, :]         # Factor exposures / betas (6,)
M1 = np.outer(f1, beta1) # Rank-1 matrix (250, 6)

print(f"Leading singular value: {Sig[0]:.4f}")
print("Asset exposures to systematic market mode (beta_1):\n", np.round(beta1, 4))
assert np.linalg.matrix_rank(M1) == 1
assert np.allclose(M1, Sig[0] * np.outer(U[:, 0], Vt[0, :]))

# Percentage of total variance captured by the rank-1 market factor
var_explained = (Sig[0] ** 2) / np.sum(Sig ** 2)
print(f"Variance explained by rank-1 systematic factor: {var_explained * 100:.2f}%")
assert var_explained > 0.40  # Dominant market factor captures over 40% of variance
```

---

## ✅ Acceptance Criteria
- [X] Outer product `x @ y.T` is verified to have rank 1.
- [X] Rank factorization `A = B @ C` is verified with full rank factors.
- [X] SVD-based rank factorization produces exact matrix reconstruction.
- [X] Leading SVD mode factorizes centered returns into outer product of factor scores and asset loadings.
- [X] Factor matrix $M_1 = f_1 \beta_1^T$ is confirmed to have matrix rank 1.
- [X] Leading rank-1 systematic factor explains $> 40\%$ of total empirical variance.
