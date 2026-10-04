# Story 007: Matrix Rank, Linear Independence, and SVD Thresholding

## User Story
**As a** statistical programmer,
**I want to** determine matrix rank, assess linear dependency, and understand numerical SVD tolerance,
**So that** I can detect multicollinearity and rank deficiency in regression design matrices..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 3: Rank of Matrices
* **Sections:** 3.1, 3.4 (Rank Definitions, Rank in Statistics)

---

## 🎯 What You Will Learn
1. Row rank equals column rank for any real matrix.
2. SVD-based numerical rank determination in np.linalg.matrix_rank.
3. Detecting collinearity when a column is a linear combination of others.
4. Gram matrix rank equality: rank(X^T X) == rank(X X^T) == rank(X).
5. Detecting full column rank in multivariate market return series.
6. Diagnosing artificial multicollinearity and near-zero singular values.

---

## 🛠️ Step-by-Step Implementation Guide


### 1. Rank Evaluation & Collinearity
```python
import numpy as np

# Construct matrix where col 3 = col 1 + 2 * col 2
c1 = np.array([1.0, 2.0, 3.0, 4.0])
c2 = np.array([2.0, 0.0, 1.0, -1.0])
c3 = c1 + 2 * c2
X = np.column_stack([c1, c2, c3])

rank_X = np.linalg.matrix_rank(X)
print("Shape of X:", X.shape)
print("Rank of X:", rank_X)
assert rank_X == 2  # Collinear!

# Gram matrix rank preservation
XtX = X.T @ X
assert np.linalg.matrix_rank(XtX) == rank_X
```

### 2. 📊 Practical Dataset Application: Real Market Rank & Multicollinearity Diagnostics
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

# 1. Rank of market returns matrix
rank_X = np.linalg.matrix_rank(X)
print(f"Matrix X shape: {X.shape}, Rank: {rank_X}")
assert rank_X == 6  # Full column rank: assets are linearly independent

# 2. Inject artificial multicollinearity (synthetic derivative ETF)
# synth = 60% SPY + 40% QQQ
spy = X[:, 0]
qqq = X[:, 1]
synth_etf = 0.60 * spy + 0.40 * qqq

# Construct augmented matrix (250 x 7)
X_aug = np.column_stack([X, synth_etf])
rank_aug = np.linalg.matrix_rank(X_aug)
print(f"Augmented Matrix shape: {X_aug.shape}, Rank: {rank_aug}")
assert rank_aug == 6  # Rank does not increase!

# Inspect singular values of X_aug
singular_vals = np.linalg.svd(X_aug, compute_uv=False)
print("Singular values of X_aug:\n", np.round(singular_vals, 6))
assert np.isclose(singular_vals[-1], 0.0, atol=1e-12)
```

---

## ✅ Acceptance Criteria
- [X] Linear dependence between columns is detected via rank deficit.
- [X] `np.linalg.matrix_rank(X) == 2` for a $4 \times 3$ matrix with 2 independent columns.
- [X] Gram matrix `X.T @ X` has identical rank to `X`.
- [X] Empirical returns matrix $X$ is confirmed full rank ($\text{rank}(X) = 6$).
- [X] Appending a collinear synthetic asset does not increase the rank ($\text{rank}(X_{\text{aug}}) = 6$).
- [X] Smallest singular value of the collinear system is verified to be zero ($\approx 10^{-15}$).
