# Story 001: Matrix Creation & R-to-Python Translation

## User Story
**As a** data scientist migrating statistical workflows from R to Python,
**I want to** master NumPy array creation, memory layouts (C-order vs Fortran-order), and indexing semantics,
**So that** I can translate matrix textbook examples and R code faithfully without subtle dimension or transposition bugs..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 1: Introduction
* **Sections:** 1.4-1.7 (Guide to R, Summary of Matrix Operators, Examples of Commands)

---

## 🎯 What You Will Learn
1. How NumPy's 0-based indexing contrasts with R's 1-based indexing.
2. How column-major (order='F') reshaping reproduces R's default matrix(byrow=FALSE) behavior.
3. The difference between 1D arrays of shape (n,) and 2D column vectors of shape (n, 1).
4. Basic matrix slicing, row/column extraction, and block sub-matrices in NumPy.
5. Ingesting multivariate financial CSV data (`data/asset_returns.csv`) into 2D NumPy float arrays.
6. Slicing multi-asset time series and ensuring contiguous C-order memory layout.

---

## 🛠️ Step-by-Step Implementation Guide


### 1. Recreate R's Matrix Constructors
In R:
```r
A <- matrix(c(1, 2, 3, 4, 5, 6), nrow=2, ncol=3, byrow=FALSE)
B <- matrix(c(1, 2, 3, 4, 5, 6), nrow=2, ncol=3, byrow=TRUE)
```
In Python:
```python
import numpy as np

# Column-major (R default byrow=FALSE)
A = np.array([1, 2, 3, 4, 5, 6]).reshape((2, 3), order='F')
# Row-major (R byrow=TRUE)
B = np.array([1, 2, 3, 4, 5, 6]).reshape((2, 3), order='C')

print("A (column-major):\n", A)
print("B (row-major):\n", B)
assert A[0, 1] == 3  # Corresponds to A[1, 2] in R
assert B[1, 1] == 5  # Corresponds to B[2, 2] in R
```

### 2. Handle Vector Geometry
```python
# 1D array
x = np.array([10.0, 20.0, 30.0])
print("x shape:", x.shape)  # (3,)

# Explicit 2D column vector
x_col = x[:, None]  # shape (3, 1)
print("x_col shape:", x_col.shape)
assert x_col.shape == (3, 1)
```

### 3. 📊 Practical Dataset Application: Real Market Data Ingestion & Slicing
```python
import csv
import numpy as np

# Ingest 250 days x 6 assets from data/asset_returns.csv
with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)
    assets = headers[1:]  # ['SPY', 'QQQ', 'GLD', 'XLE', 'TLT', 'VNQ']
    data = [[float(v) for v in row[1:]] for row in reader]

X = np.array(data)  # shape (250, 6)
n, p = X.shape
print(f"Ingested market returns matrix X: {n} days x {p} assets ({assets})")
assert X.shape == (250, 6)
assert X.flags['C_CONTIGUOUS']

# Extract sub-matrices: first 5 days of Equities (SPY=col 0, QQQ=col 1)
equity_sub = X[:5, [0, 1]]
print("First 5 days equity returns (SPY, QQQ):\n", equity_sub)
assert equity_sub.shape == (5, 2)

# Extract SPY returns as a 2D column vector vs 1D array
spy_1d = X[:, 0]
spy_col = X[:, 0:1]
assert spy_1d.shape == (250,)
assert spy_col.shape == (250, 1)
```

---

## ✅ Acceptance Criteria
- [X] `A` correctly matches R's column-major matrix layout with shape `(2, 3)`.
- [X] `B` correctly matches R's row-major matrix layout with shape `(2, 3)`.
- [X] Indexing `A[0, 1]` returns `3`.
- [X] Vector conversions between 1D and 2D column vector shapes are verified.
- [X] `data/asset_returns.csv` is loaded into a $(250, 6)$ contiguous NumPy array.
- [X] Multi-asset slicing extracts 5-day equity sub-matrix with shape $(5, 2)$.
- [X] Single-column asset extraction preserves $(250, 1)$ column-vector shape.
