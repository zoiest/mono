# Story 015: Block Inversion & Conditional Gaussian Covariance

## User Story
**As a** Bayesian statistician,
**I want to** invert block matrices using the Banachiewicz formula and compute conditional covariance matrices,
**So that** I can derive precision matrices and conditional Gaussian distributions in multivariate data analysis..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 5: Inverses
* **Sections:** 5.5 (Inverses of Partitioned Matrices, Banachiewicz Inversion)

---

## 🎯 What You Will Learn
1. Banachiewicz block inversion formula.
2. Connection between the Schur complement and conditional variance: Cov(X_2 | X_1).
3. Precision matrix structure in Gaussian graphical models.
4. Inverting partitioned covariance matrices using the Banachiewicz block inversion formula.
5. Extracting partial correlations between equity assets controlling for hedges and commodities.

---

## 🛠️ Step-by-Step Implementation Guide


### 1. Banachiewicz Block Inversion
```python
import numpy as np

A = np.array([[4.0, 1.0], [1.0, 3.0]])
B = np.array([[1.0], [0.5]])
C = B.T
D = np.array([[2.0]])

M = np.block([[A, B], [C, D]])
M_inv_direct = np.linalg.inv(M)

# Block inversion formula
A_inv = np.linalg.inv(A)
S_A = D - C @ A_inv @ B
S_A_inv = np.linalg.inv(S_A)

B11 = A_inv + A_inv @ B @ S_A_inv @ C @ A_inv
B12 = -A_inv @ B @ S_A_inv
B21 = -S_A_inv @ C @ A_inv
B22 = S_A_inv

M_inv_block = np.block([[B11, B12], [B21, B22]])

assert np.allclose(M_inv_direct, M_inv_block)
print("Banachiewicz block inversion verified.")
```

### 2. 📊 Practical Dataset Application: Real Market Banachiewicz Block Inversion & Partial Correlations
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

# Partition S into Equities (A: 2x2) and Non-Equities (D: 4x4)
A = S[:2, :2]
B = S[:2, 2:]
C = S[2:, :2]
D = S[2:, 2:]

inv_A = np.linalg.inv(A)
S_schur = D - C @ inv_A @ B
inv_Schur = np.linalg.inv(S_schur)

# Banachiewicz block inverse blocks
top_left = inv_A + inv_A @ B @ inv_Schur @ C @ inv_A
top_right = -inv_A @ B @ inv_Schur
bot_left = -inv_Schur @ C @ inv_A
bot_right = inv_Schur

Theta_block = np.block([[top_left, top_right], [bot_left, bot_right]])
Theta_full = np.linalg.inv(S)

assert np.allclose(Theta_block, Theta_full)

# Partial Correlation between SPY and QQQ controlling for remaining 4 assets
partial_corr_spy_qqq = -Theta_full[0, 1] / np.sqrt(Theta_full[0, 0] * Theta_full[1, 1])
marginal_corr_spy_qqq = S[0, 1] / np.sqrt(S[0, 0] * S[1, 1])

print(f"Marginal Correlation (SPY, QQQ): {marginal_corr_spy_qqq:.4f}")
print(f"Partial Correlation (SPY, QQQ | Rest): {partial_corr_spy_qqq:.4f}")
assert partial_corr_spy_qqq > 0.50
```

---

## ✅ Acceptance Criteria
- [X] Banachiewicz block inversion matches `np.linalg.inv(M)` within machine precision.
- [X] Conditional covariance `D - C @ A_inv @ B` verified as Schur complement.
- [X] Banachiewicz block inverse is assembled and verified against full matrix inversion.
- [X] Bottom-right block of precision matrix is confirmed equal to inverse Schur complement $(S/A)^{-1}$.
- [X] Partial correlation between SPY and QQQ controlling for other assets is computed from precision matrix entries.
