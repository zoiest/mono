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

print("A (column-major):
", A)
print("B (row-major):
", B)
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

---

## ✅ Acceptance Criteria
- [X] `A` correctly matches R's column-major matrix layout with shape `(2, 3)`.
- [X] `B` correctly matches R's row-major matrix layout with shape `(2, 3)`.
- [X] Indexing `A[0, 1]` returns `3`.
- [X] Vector conversions between 1D and 2D column vector shapes are verified.
