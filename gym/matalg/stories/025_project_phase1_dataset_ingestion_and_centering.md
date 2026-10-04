# Story 025: Capstone Project Phase 1 — Dataset Ingestion, Matrix Centering, and Covariance

## User Story
**As a** quantitative risk analyst,
**I want to** load the 6-asset market returns dataset into NumPy and compute sample mean, covariance, and correlation matrices via the centering matrix $H_n$,
**So that** I have a clean matrix representation of asset returns and understand how centering operators eliminate the need for manual row loops..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 11: Capstone Project (and Chapters 1 & 2)
* **Sections:** 1.5, 2.5.6.1, 2.12.3 (Data Input, Centering Matrix Hn, Sample Statistics)

---

## 🎯 What You Will Learn
1. Parsing multivariate CSV data into NumPy arrays without external dataframe dependencies.
2. Constructing the n x n Centering Matrix H_n = I_n - (1/n) * 1 1^T.
3. Proving and verifying H_n symmetry (H_n^T = H_n) and idempotency (H_n^2 = H_n).
4. Computing sample covariance S = (1 / (n - 1)) * X^T H_n X and correlation R.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Ingestion & Matrix Statistics Implementation
```python
import csv
import numpy as np

# Load CSV
with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    assets = next(reader)[1:]
    data = [[float(v) for v in row[1:]] for row in reader]

X = np.array(data)
n, p = X.shape
print(f"Loaded returns matrix X: {n} days x {p} assets ({assets})")

# Construct Centering Matrix H_n
ones = np.ones((n, 1))
H = np.eye(n) - (ones @ ones.T) / n

# Verify H properties
assert np.allclose(H, H.T)              # Symmetry
assert np.allclose(H @ H, H)            # Idempotency
assert np.isclose(np.trace(H), n - 1)   # Rank / Degrees of Freedom = 249

# Mean vector and covariance
xbar = (X.T @ ones) / n
S = (X.T @ H @ X) / (n - 1)

# Correlation Matrix R = D^{-1} S D^{-1}
D_inv = np.diag(1.0 / np.sqrt(np.diag(S)))
R = D_inv @ S @ D_inv

print("Sample Mean Vector (daily %):
", np.round(xbar.flatten() * 100, 3))
print("Sample Covariance Matrix S (x 10^4):
", np.round(S * 1e4, 3))
print("Sample Correlation Matrix R:
", np.round(R, 3))
```

---

## ✅ Acceptance Criteria
- [X] `data/asset_returns.csv` loads into NumPy array `X` of shape `(250, 6)`.
- [X] Centering matrix `H` satisfies `H^T == H` and `H @ H == H` with `trace == 249`.
- [X] Covariance matrix `S` is confirmed symmetric positive-definite.
- [X] Correlation matrix `R` has unit diagonal and entries bounded in `[-1, 1]`.
