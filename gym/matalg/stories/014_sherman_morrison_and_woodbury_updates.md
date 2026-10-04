# Story 014: Patterned Inverses & The Sherman-Morrison Formula

## User Story
**As a** real-time systems engineer,
**I want to** implement $O(n^2)$ inverse updates via Sherman-Morrison and invert equicorrelation matrices,
**So that** I can perform online sequential parameter updates in streaming Kalman filters and regression..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 5: Inverses
* **Sections:** 5.4 (Inverses of Patterned Matrices, Sherman-Morrison)

---

## 🎯 What You Will Learn
1. Inverting equicorrelation matrices alpha I + beta 1 1^T analytically.
2. The Sherman-Morrison formula: (A + x y^T)^{-1} = A^{-1} - (A^{-1} x y^T A^{-1}) / (1 + y^T A^{-1} x).
3. The Woodbury identity for rank-k updates.
4. Updating the precision matrix $\Theta = S^{-1}$ in $O(p^2)$ when streaming daily return shocks arrive.
5. Verifying the Sherman-Morrison update against full $O(p^3)$ re-inversion.

---

## 🛠️ Step-by-Step Implementation Guide


### 1. Sherman-Morrison Update
```python
import numpy as np

A = np.array([[4.0, 1.0], [1.0, 3.0]])
A_inv = np.linalg.inv(A)

x = np.array([[1.0], [2.0]])
y = np.array([[2.0], [-1.0]])

# Direct inverse of update
inv_direct = np.linalg.inv(A + x @ y.T)

# Fast Sherman-Morrison formula
denom = 1.0 + (y.T @ A_inv @ x)[0, 0]
inv_sm = A_inv - (A_inv @ x @ y.T @ A_inv) / denom

print("Direct inverse:\n", inv_direct)
print("Sherman-Morrison formula:\n", inv_sm)
assert np.allclose(inv_direct, inv_sm)
```

### 2. 📊 Practical Dataset Application: Real Market Precision Matrix Online Sherman-Morrison Update
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape
H = np.eye(n) - np.ones((n, n)) / n
S = (X.T @ H @ X) / (n - 1)
Theta = np.linalg.inv(S)
x_mean = np.mean(X, axis=0)

# Incoming market shock vector (Day 180)
u = (X[180, :] - x_mean)[:, None]  # (6, 1)
c = 0.01

# Sherman-Morrison rank-1 update of precision matrix:
# (S + c u u^T)^{-1} = Theta - (c Theta u u^T Theta) / (1 + c u^T Theta u)
denom = 1.0 + c * (u.T @ Theta @ u)[0, 0]
Theta_sm = Theta - (c * (Theta @ u @ u.T @ Theta)) / denom

# Benchmark with full re-inversion
Theta_direct = np.linalg.inv(S + c * (u @ u.T))

assert np.allclose(Theta_sm, Theta_direct)
assert np.allclose(Theta_sm, Theta_sm.T)  # Preserves symmetry
print("Sherman-Morrison precision matrix update matches full inversion exactly!")
```

---

## ✅ Acceptance Criteria
- [X] Sherman-Morrison formula matches `np.linalg.inv(A + x @ y.T)`.
- [X] Equicorrelation inverse formula verified against `np.linalg.inv`.
- [X] Precision matrix update under rank-1 shock is implemented via Sherman-Morrison formula.
- [X] Sherman-Morrison result matches full $O(p^3)$ matrix inversion within float precision.
- [X] Symmetry of updated precision matrix is preserved.
