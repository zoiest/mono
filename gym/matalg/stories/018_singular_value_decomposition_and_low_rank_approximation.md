# Story 018: Singular Value Decomposition (SVD) & Low-Rank Approximation

## User Story
**As a** data compression & ML engineer,
**I want to** implement SVD $A = U \Sigma V^T$ and verify the Eckart-Young-Mirsky optimal low-rank approximation,
**So that** I can compress high-dimensional feature spaces and perform robust pseudo-inversion..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 6: Eigenanalysis of Real Symmetric Matrices
* **Sections:** 6.7.2 (Singular Value Decomposition of an m x n Matrix)

---

## 🎯 What You Will Learn
1. Economy SVD vs Full SVD in NumPy.
2. Relationship between singular values of A and eigenvalues of A^T A and A A^T.
3. The Eckart-Young-Mirsky optimal rank-k approximation theorem.
4. Performing thin SVD on centered returns matrix $\tilde{X} = U \Sigma V^T$.
5. Denoising empirical return data using Eckart-Young-Mirsky rank-2 optimal truncation.

---

## 🛠️ Step-by-Step Implementation Guide


### 1. SVD and Rank-k Reconstruction
```python
import numpy as np

# Non-square matrix
A = np.array([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
    [7.0, 8.0, 9.0],
    [10.0, 11.0, 12.0]
])

U, s, Vt = np.linalg.svd(A, full_matrices=False)

# Exact reconstruction
A_rec = U @ np.diag(s) @ Vt
assert np.allclose(A, A_rec)

# Best Rank-1 approximation
A_rank1 = s[0] * np.outer(U[:, 0], Vt[0, :])
print("Rank-1 approximation:\n", A_rank1)
assert np.linalg.matrix_rank(A_rank1) == 1
```

### 2. 📊 Practical Dataset Application: Real Market SVD Factorization & Eckart-Young Denoising
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

# Thin SVD
U, Sig, Vt = np.linalg.svd(X_tilde, full_matrices=False)

# Verify singular values match sqrt((n-1) * eigenvalues(S))
lambdas = np.sort(np.linalg.eigvalsh(np.cov(X, rowvar=False)))[::-1]
assert np.allclose(Sig, np.sqrt((n - 1) * lambdas))

# Eckart-Young Rank-2 Optimal Low-Rank Approximation
X_k2 = Sig[0] * np.outer(U[:, 0], Vt[0, :]) + Sig[1] * np.outer(U[:, 1], Vt[1, :])
assert np.linalg.matrix_rank(X_k2) == 2

# Low-rank covariance matrix
S_k2 = (X_k2.T @ X_k2) / (n - 1)
assert np.linalg.matrix_rank(S_k2) == 2

# Reconstruction error ||X - X_k2||_F == sqrt(sum_{i=3}^p sigma_i^2)
frob_residual = np.linalg.norm(X_tilde - X_k2, "fro")
expected_residual = np.sqrt(np.sum(Sig[2:] ** 2))
assert np.isclose(frob_residual, expected_residual)
print(f"Rank-2 SVD Denoising captures {((Sig[0]**2 + Sig[1]**2) / np.sum(Sig**2)) * 100:.2f}% of total variance")
```

---

## ✅ Acceptance Criteria
- [X] SVD reconstruction `U @ diag(s) @ Vt` recovers original matrix `A`.
- [X] Singular values match square roots of eigenvalues of `A.T @ A`.
- [X] Rank-1 approximation is verified to have rank 1.
- [X] Singular values $\sigma_i$ are confirmed equal to $\sqrt{(n-1)\lambda_i}$.
- [X] Rank-2 Eckart-Young approximation has rank 2 for both returns and reconstructed covariance.
- [X] Residual Frobenius norm matches theoretical sum of truncated singular values.
