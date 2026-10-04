# Story 027: Capstone Project Phase 3 — PCA Factor Modeling, Scree Analysis, and SVD Covariance Denoising

## User Story
**As a** portfolio manager,
**I want to** perform spectral decomposition $S = P \Lambda P^T$, extract latent market risk factors, and apply Eckart-Young SVD denoising,
**So that** I can eliminate idiosyncratic empirical noise and reduce portfolio risk estimation error..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 11: Capstone Project (and Chapter 6)
* **Sections:** 6.4, 6.5, 6.7.1, 6.7.2 (Properties of Eigenanalyses, PCA, Spectral Decomp, SVD)

---

## 🎯 What You Will Learn
1. Spectral decomposition of real symmetric covariance matrix S = P Lambda P^T using np.linalg.eigh.
2. Computing proportion of variance explained and analyzing scree drop-offs.
3. Interpreting economic factor loadings: Market Factor, Duration/Tech Factor, Commodity Factor.
4. Filtering noise via Eckart-Young optimal low-rank factor model: S_denoised = sum_{j=1}^k lambda_j p_j p_j^T + Psi.

---

## 🛠️ Step-by-Step Implementation Guide


### 1. PCA Factor Model & Denoising
```python
import numpy as np

# Spectral Decomposition
evals, P = np.linalg.eigh(S)
# Order descending
idx = np.argsort(evals)[::-1]
evals, P = evals[idx], P[:, idx]

total_var = np.trace(S)
pct_var = evals / total_var

print("Eigenvalues (Variance per Factor):", np.round(evals * 1e4, 4))
print("Percentage Explained (%):", np.round(pct_var * 100, 2))
print("Cumulative Explained (%):", np.round(np.cumsum(pct_var) * 100, 2))

# Top 3 factor model reconstruction
k = 3
S_factors = P[:, :k] @ np.diag(evals[:k]) @ P[:, :k].T
# Preserve specific asset idiosyncratic variances
Psi = np.diag(np.maximum(np.diag(S - S_factors), 0))
S_denoised = S_factors + Psi

assert np.isclose(np.trace(S), np.trace(S_denoised))
print("Total variance preserved in denoised matrix.")
```

---

## ✅ Acceptance Criteria
- [X] Spectral decomposition $S = P \Lambda P^T$ satisfies $P^T P = I_p$.
- [X] Top 3 factors explain $> 80\%$ of total multi-asset variance.
- [X] Denoised covariance matrix preserves total trace $\text{tr}(S)$.
