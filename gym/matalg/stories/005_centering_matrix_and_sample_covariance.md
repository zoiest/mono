# Story 005: The Centering Matrix $H_n$ and Sample Covariance Computation

## User Story
**As a** multivariate data analyst,
**I want to** implement the centering matrix $H_n = I_n - \frac{1}{n}\mathbf{1}\mathbf{1}^T$ and calculate sample covariance matrices,
**So that** I can perform mean-centering and compute sample variance-covariance matrices directly via algebraic matrix multiplication..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 2: Vectors and Matrices
* **Sections:** 2.5.6.1, 2.12.3 (The Centering Matrix Hn, Sample Statistics in R)

---

## 🎯 What You Will Learn
1. Properties of H_n: symmetry, idempotency (H_n^2 = H_n), and null space H_n 1 = 0.
2. Rank and trace of H_n: tr(H_n) = n - 1.
3. Mean centering of data matrix X: X_c = H_n X.
4. Calculating sample covariance S = (1 / (n - 1)) * X^T H_n X.
5. Constructing the $250 \times 250$ centering matrix $H_{250}$ and computing de-meaned returns.
6. Computing sample covariance $S = \frac{1}{n-1} X^T H X$ and scaling to correlation matrix $R = D^{-1} S D^{-1}$.

---

## 🛠️ Step-by-Step Implementation Guide


### 1. Centering Matrix Construction & Covariance
```python
import numpy as np

def make_centering_matrix(n: int) -> np.ndarray:
    return np.eye(n) - np.ones((n, n)) / n

n = 5
H = make_centering_matrix(n)
ones = np.ones(n)

# Algebraic verifications
assert np.allclose(H, H.T)              # Symmetric
assert np.allclose(H @ H, H)            # Idempotent
assert np.allclose(H @ ones, 0.0)       # Annihilator
assert np.isclose(np.trace(H), n - 1)   # Rank / Trace

# Covariance calculation
X = np.array([
    [10.0, 2.0],
    [12.0, 4.0],
    [14.0, 5.0],
    [16.0, 9.0],
    [18.0, 10.0]
])

S_matrix = (X.T @ H @ X) / (n - 1)
S_numpy = np.cov(X, rowvar=False)

print("S via Centering Matrix:\n", S_matrix)
assert np.allclose(S_matrix, S_numpy)
```

### 2. 📊 Practical Dataset Application: Real Market Centering, Covariance, and Correlation
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    assets = next(reader)[1:]
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape

# Construct Centering Matrix H_n
ones = np.ones((n, 1))
H = np.eye(n) - (ones @ ones.T) / n

# Verify H properties
assert np.allclose(H, H.T)              # Symmetric
assert np.allclose(H @ H, H)            # Idempotent
assert np.isclose(np.trace(H), n - 1)   # Rank = 249

# Center the asset returns
X_centered = H @ X
col_means = np.mean(X_centered, axis=0)
assert np.allclose(col_means, 0.0, atol=1e-12)

# Sample covariance matrix S
S = (X.T @ H @ X) / (n - 1)
S_np = np.cov(X, rowvar=False)
assert np.allclose(S, S_np)

# Scaling S to correlation matrix R = D^{-1} S D^{-1}
D_inv = np.diag(1.0 / np.sqrt(np.diag(S)))
R = D_inv @ S @ D_inv
assert np.allclose(np.diag(R), np.ones(p))
print("Empirical Correlation Matrix R (SPY, QQQ, GLD, XLE, TLT, VNQ):\n", np.round(R, 3))
```

---

## ✅ Acceptance Criteria
- [X] `H_n` satisfies `H^T == H`, `H @ H == H`, and `H @ 1 == 0`.
- [X] `tr(H_n) == n - 1` is verified.
- [X] `X.T @ H_n @ X / (n - 1)` exactly matches `np.cov(X, rowvar=False)`.
- [X] Centering matrix $H_{250}$ is verified symmetric, idempotent, and rank 249.
- [X] De-meaned matrix $HX$ has zero column means ($\mathbf{1}^T(HX) = \mathbf{0}$).
- [X] Covariance matrix $S = \frac{1}{n-1}X^THX$ matches NumPy's `np.cov`.
- [X] Correlation matrix $R = D^{-1} S D^{-1}$ has unit diagonal.
