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

---

## ✅ Acceptance Criteria
- [X] Linear dependence between columns is detected via rank deficit.
- [X] `np.linalg.matrix_rank(X) == 2` for a $4 \times 3$ matrix with 2 independent columns.
- [X] Gram matrix `X.T @ X` has identical rank to `X`.
