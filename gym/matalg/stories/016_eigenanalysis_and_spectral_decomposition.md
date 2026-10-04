# Story 016: Eigenanalysis & The Spectral Decomposition Theorem

## User Story
**As a** applied mathematician,
**I want to** compute eigenvalues/eigenvectors of symmetric matrices and reconstruct matrices via the Spectral Theorem,
**So that** I can decompose covariance matrices into principal geometric axes and orthogonal subspaces..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 6: Eigenanalysis of Real Symmetric Matrices
* **Sections:** 6.1, 6.2, 6.4, 6.7.1 (Characteristic Equation, Symmetric Properties, Spectral Decomposition)

---

## 🎯 What You Will Learn
1. The Spectral Theorem: A = P Lambda P^T for real symmetric matrices.
2. Orthonormality of eigenvectors: P^T P = I.
3. Trace equals sum of eigenvalues; Determinant equals product of eigenvalues.
4. Rank equals number of non-zero eigenvalues.
5. Decomposing market covariance into eigenvalues and eigenvectors using `np.linalg.eigh`.
6. Identifying the dominant eigenvector as the systematic market risk factor.

---

## 🛠️ Step-by-Step Implementation Guide


### 1. Spectral Decomposition
```python
import numpy as np

# Symmetric matrix
S = np.array([[5.0, 2.0], [2.0, 2.0]])

# np.linalg.eigh guarantees real eigenvalues and orthonormal eigenvectors
evals, P = np.linalg.eigh(S)

# Orthonormality check
assert np.allclose(P.T @ P, np.eye(2))

# Spectral reconstruction: P @ diag(evals) @ P.T
S_rec = P @ np.diag(evals) @ P.T
assert np.allclose(S, S_rec)

# Trace and determinant checks
assert np.isclose(np.trace(S), np.sum(evals))
assert np.isclose(np.linalg.det(S), np.prod(evals))
print("Spectral Theorem successfully verified.")
```

### 2. 📊 Practical Dataset Application: Real Market Covariance Spectral Decomposition & Risk Modes
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    assets = next(reader)[1:]
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape
H = np.eye(n) - np.ones((n, n)) / n
S = (X.T @ H @ X) / (n - 1)

# Spectral decomposition of symmetric covariance S
lambdas, Q = np.linalg.eigh(S)
# Sort in descending order
idx = np.argsort(lambdas)[::-1]
lambdas, Q = lambdas[idx], Q[:, idx]

# Verify spectral reconstruction: S == sum(lambda_i * q_i * q_i^T)
S_reconstructed = Q @ np.diag(lambdas) @ Q.T
assert np.allclose(S, S_reconstructed)
assert np.allclose(Q.T @ Q, np.eye(p))
assert np.isclose(np.sum(lambdas), np.trace(S))

# Variance explained
pct_var = lambdas / np.sum(lambdas)
print("Eigenvalues (sorted):", np.round(lambdas * 1e4, 3))
print("Variance Explained (%):", np.round(pct_var * 100, 2))

# Eigenvector 1 (Market Mode) loadings
print("PC1 Eigenvector Loadings across assets:")
for asset, weight in zip(assets, Q[:, 0]):
    print(f"  {asset:>4}: {weight:+.4f}")
```

---

## ✅ Acceptance Criteria
- [X] Eigenvalues and eigenvectors are computed using `np.linalg.eigh`.
- [X] Eigenvector matrix `P` is verified to be orthogonal (`P.T @ P == I`).
- [X] Spectral reconstruction `P @ diag(evals) @ P.T` recovers `S`.
- [X] Trace and determinant eigenvalue equalities are confirmed.
- [X] Spectral decomposition $S = Q \Lambda Q^T$ accurately reconstructs empirical covariance.
- [X] Eigenvector matrix $Q$ is verified orthonormal ($Q^T Q = I_6$).
- [X] Sum of eigenvalues equals total variance $\text{tr}(S)$.
- [X] Proportion of variance explained by each principal component is quantified.
