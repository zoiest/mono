#!/usr/bin/env python3
"""
Generates stories/025_...md through stories/030_...md for the capstone project.
"""

from pathlib import Path

project_stories = [
    (
        "025_project_phase1_dataset_ingestion_and_centering",
        "Story 025: Capstone Project Phase 1 — Dataset Ingestion, Matrix Centering, and Covariance",
        "quantitative risk analyst",
        "load the 6-asset market returns dataset into NumPy and compute sample mean, covariance, and correlation matrices via the centering matrix $H_n$",
        "I have a clean matrix representation of asset returns and understand how centering operators eliminate the need for manual row loops.",
        "Chapter 11: Capstone Project (and Chapters 1 & 2)",
        "1.5, 2.5.6.1, 2.12.3 (Data Input, Centering Matrix Hn, Sample Statistics)",
        [
            "Parsing multivariate CSV data into NumPy arrays without external dataframe dependencies.",
            "Constructing the n x n Centering Matrix H_n = I_n - (1/n) * 1 1^T.",
            "Proving and verifying H_n symmetry (H_n^T = H_n) and idempotency (H_n^2 = H_n).",
            "Computing sample covariance S = (1 / (n - 1)) * X^T H_n X and correlation R."
        ],
        r"""
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

print("Sample Mean Vector (daily %):\n", np.round(xbar.flatten() * 100, 3))
print("Sample Covariance Matrix S (x 10^4):\n", np.round(S * 1e4, 3))
print("Sample Correlation Matrix R:\n", np.round(R, 3))
```""",
        [
            "`data/asset_returns.csv` loads into NumPy array `X` of shape `(250, 6)`.",
            "Centering matrix `H` satisfies `H^T == H` and `H @ H == H` with `trace == 249`.",
            "Covariance matrix `S` is confirmed symmetric positive-definite.",
            "Correlation matrix `R` has unit diagonal and entries bounded in `[-1, 1]`."
        ]
    ),
    (
        "026_project_phase2_precision_matrix_and_sherman_morrison",
        "Story 026: Capstone Project Phase 2 — Precision Matrix, Partial Correlation, and Online Sherman-Morrison",
        "algorithmic trader",
        "evaluate condition number $\\kappa(S)$, compute the precision matrix $\\Theta = S^{-1}$ for partial correlations, and implement $O(p^2)$ streaming Sherman-Morrison updates",
        "I can isolate direct asset-to-asset dependencies and update risk parameters in real-time as streaming ticks arrive.",
        "Chapter 11: Capstone Project (and Chapters 4 & 5)",
        "4.1, 5.2, 5.4.2 (Conditioning, Inverses, Sherman-Morrison Formula)",
        [
            "Computing condition number kappa(S) to assess numerical stability.",
            "Precision matrix Theta = S^{-1} and conditional independence in Gaussian graphical models.",
            "Deriving partial correlation rho_{ij . rest} = -theta_{ij} / sqrt(theta_{ii} * theta_{jj}).",
            "Streaming O(p^2) covariance inverse updates via the Sherman-Morrison rank-1 formula."
        ],
        r"""
### 1. Precision Matrix & Streaming Update
```python
import numpy as np

# Continuing from Phase 1
cond_S = np.linalg.cond(S)
print(f"Condition number: {cond_S:.2f}")

Theta = np.linalg.inv(S)

# Partial Correlation Matrix
D_theta = np.diag(1.0 / np.sqrt(np.diag(Theta)))
P_corr = -D_theta @ Theta @ D_theta
np.fill_diagonal(P_corr, 1.0)
print("Partial Correlation (SPY vs QQQ | rest):", round(P_corr[0, 1], 3))

# Streaming update: New Day Returns
x_new = np.array([-0.012, -0.015, 0.004, -0.008, 0.007, -0.010])

# Exact batch calculation with n + 1 points
X_ext = np.vstack([X, x_new])
n_new = n + 1
H_new = np.eye(n_new) - np.ones((n_new, n_new)) / n_new
S_new = (X_ext.T @ H_new @ X_ext) / (n_new - 1)
inv_batch_new = np.linalg.inv(S_new)

# Sherman-Morrison Recursive Update
c = (n - 1) / n
delta = (x_new - xbar.flatten())[:, None]
gamma = 1.0 / (n + 1)
A_inv = Theta / c
denom = 1.0 + (gamma * delta.T @ A_inv @ delta)[0, 0]
inv_sm_new = A_inv - (gamma * A_inv @ delta @ delta.T @ A_inv) / denom

print("Sherman-Morrison matches full batch inversion:", np.allclose(inv_batch_new, inv_sm_new, atol=1e-5))
assert np.allclose(inv_batch_new, inv_sm_new, atol=1e-5)
```""",
        [
            "Condition number $\\kappa(S)$ is computed and verified $< 100$.",
            "Partial correlation matrix `P_corr` is computed from precision matrix $\\Theta$.",
            "Sherman-Morrison streaming update matches full batch inverse within $10^{-5}$."
        ]
    ),
    (
        "027_project_phase3_pca_factor_model_and_svd_denoising",
        "Story 027: Capstone Project Phase 3 — PCA Factor Modeling, Scree Analysis, and SVD Covariance Denoising",
        "portfolio manager",
        "perform spectral decomposition $S = P \\Lambda P^T$, extract latent market risk factors, and apply Eckart-Young SVD denoising",
        "I can eliminate idiosyncratic empirical noise and reduce portfolio risk estimation error.",
        "Chapter 11: Capstone Project (and Chapter 6)",
        "6.4, 6.5, 6.7.1, 6.7.2 (Properties of Eigenanalyses, PCA, Spectral Decomp, SVD)",
        [
            "Spectral decomposition of real symmetric covariance matrix S = P Lambda P^T using np.linalg.eigh.",
            "Computing proportion of variance explained and analyzing scree drop-offs.",
            "Interpreting economic factor loadings: Market Factor, Duration/Tech Factor, Commodity Factor.",
            "Filtering noise via Eckart-Young optimal low-rank factor model: S_denoised = sum_{j=1}^k lambda_j p_j p_j^T + Psi."
        ],
        r"""
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
```""",
        [
            "Spectral decomposition $S = P \\Lambda P^T$ satisfies $P^T P = I_p$.",
            "Top 3 factors explain $> 80\\%$ of total multi-asset variance.",
            "Denoised covariance matrix preserves total trace $\\text{tr}(S)$."
        ]
    ),
    (
        "028_project_phase4_mahalanobis_cholesky_and_hotelling_t2",
        "Story 028: Capstone Project Phase 4 — Mahalanobis Anomaly Detection, Cholesky Whitening, and Hotelling's $T^2$",
        "systemic risk auditor",
        "implement lower-triangular Cholesky whitening $Z = (X - \\bar{X})(L^{-1})^T$, calculate Mahalanobis distances, and detect market shock days via Hotelling's $T^2$",
        "I can monitor multi-asset markets in real-time and flag systemic shocks and outlier regime shifts.",
        "Chapter 11: Capstone Project (and Chapters 8 & 9)",
        "8.2.3, 9.2.1, 9.2.5.1 (Cholesky, Standardization, One-Sample Hotelling T2)",
        [
            "Cholesky decomposition S = L L^T where L is lower triangular.",
            "Whitening transformation Z = (X - 1 xbar^T)(L^{-1})^T satisfying Cov(Z) = I_p.",
            "Equivalence of Mahalanobis distance D_M^2(x_t) = (x_t - xbar)^T S^{-1} (x_t - xbar) and ||z_t||_2^2.",
            "Hypothesis testing under Chi-Square(p=6) distribution and pinpointing Day 180 shock."
        ],
        r"""
### 1. Whitening & Anomaly Detection
```python
import numpy as np
import scipy.stats as stats

# Cholesky Factorization
L = np.linalg.cholesky(S)
assert np.allclose(L @ L.T, S)

# Whitening Transformation
Z = (X - xbar.T) @ np.linalg.inv(L).T
cov_Z = np.cov(Z, rowvar=False)
assert np.allclose(cov_Z, np.eye(p), atol=0.02)

# Mahalanobis Distance: ||z_t||_2^2
d_mahal = np.sum(Z ** 2, axis=1)

# Critical threshold at alpha = 0.001
crit = stats.chi2.ppf(0.999, df=p)
anomalies = np.where(d_mahal > crit)[0]

print(f"Threshold (df={p}, p=0.001): {crit:.2f}")
print("Detected Anomaly Day Indices:", anomalies)
assert 180 in anomalies
print(f"Day 180 Mahalanobis distance: {d_mahal[180]:.2f} (Extreme shock successfully detected!)")
```""",
        [
            "Cholesky factor satisfies `L @ L.T == S`.",
            "Whitened data matrix `Z` has covariance matrix matching $I_p$ within empirical tolerance.",
            "Day 180 is identified as an extreme market anomaly with $p < 0.001$."
        ]
    ),
    (
        "029_project_phase5_markowitz_portfolio_constrained_optimization",
        "Story 029: Capstone Project Phase 5 — Markowitz Minimum-Variance Portfolio via Constrained Optimization",
        "investment strategist",
        "derive and solve the Global Minimum Variance (GMV) portfolio $w^* = \\frac{S^{-1}\\mathbf{1}}{\\mathbf{1}^T S^{-1} \\mathbf{1}}$ using Lagrange multipliers and matrix inversion",
        "I can construct risk-optimal asset allocations mathematically guaranteed to minimize portfolio volatility.",
        "Chapter 11: Capstone Project (and Chapters 5 & 7)",
        "5.1, 7.2.3, 7.6 (Quadratic Forms, Lagrange Multipliers, Constrained Optimization)",
        [
            "Formulating portfolio risk minimization as constrained quadratic optimization: min w^T S w s.t. w^T 1 = 1.",
            "Solving the Lagrangian system via matrix calculus: 2 S w - lambda 1 = 0.",
            "Analytic solution w* = S^{-1} 1 / (1^T S^{-1} 1) and minimum portfolio variance sigma_{min}^2 = 1 / (1^T S^{-1} 1).",
            "Verifying Markowitz diversification theorem: portfolio volatility is strictly lower than every individual asset."
        ],
        r"""
### 1. Optimal GMV Portfolio Allocation
```python
import numpy as np

ones_p = np.ones((p, 1))
S_inv = np.linalg.inv(S)

# Analytical GMV Weights
w_gmv = (S_inv @ ones_p / (ones_p.T @ S_inv @ ones_p)[0, 0]).flatten()
assert np.isclose(np.sum(w_gmv), 1.0)

# Portfolio volatility vs individual volatilities
var_gmv = w_gmv.T @ S @ w_gmv
vol_gmv_ann = np.sqrt(var_gmv * 252)
indiv_vols_ann = np.sqrt(np.diag(S) * 252)

print("GMV Weights (%):")
for a, w in zip(assets, w_gmv):
    print(f"  {a:>4}: {w*100:+6.2f}%")

print(f"\nGMV Annualized Volatility: {vol_gmv_ann*100:.2f}%")
print(f"Lowest Individual Asset Volatility: {np.min(indiv_vols_ann)*100:.2f}%")
assert vol_gmv_ann < np.min(indiv_vols_ann)
```""",
        [
            "Optimal portfolio weights sum to exactly $1.0$ (`sum(w_gmv) == 1`).",
            "Annualized GMV portfolio volatility is strictly lower than every component asset's volatility.",
            "Weight derivation via Lagrange multipliers verified algebraically."
        ]
    ),
    (
        "030_project_phase6_factor_regression_and_hat_matrix_diagnostics",
        "Story 030: Capstone Project Phase 6 — Factor Pricing Regression, Hat Matrix Projection, and Gauss-Markov Diagnostics",
        "asset pricing researcher",
        "build a multi-factor regression pricing model $y = X\\beta + \\epsilon$, calculate the Hat projection matrix $P$, residual maker $M = I - P$, and verify Gauss-Markov BLUE properties",
        "I can measure market betas, extract idiosyncratic alpha, and verify regression algebraic identities using matrix projection geometry.",
        "Chapter 11: Capstone Project (and Chapters 8 & 9)",
        "8.2.1, 9.7 (QR in Least Squares, General Linear Model, Hat Matrix, Gauss-Markov)",
        [
            "Constructing multi-factor design matrix X = [1, r_SPY, r_TLT].",
            "Solving normal equations via QR decomposition without explicit inversion.",
            "Properties of Hat matrix P = X (X^T X)^{-1} X^T: symmetric (P^T = P), idempotent (P^2 = P).",
            "Properties of Residual Maker M = I - P: M X = 0, residuals e = M y.",
            "ANOVA total variance decomposition: y^T H_n y = y^T (P - (1/n)1 1^T) y + y^T M y."
        ],
        r"""
### 1. Factor Regression & Projection Geometry
```python
import numpy as np

# Regress QQQ on SPY (Market) and TLT (Bonds)
y = X[:, assets.index("QQQ")]
F = np.column_stack([np.ones(n), X[:, assets.index("SPY")], X[:, assets.index("TLT")]])
k_vars = F.shape[1]

# QR Decomposition for OLS
Q_reg, R_reg = np.linalg.qr(F)
beta_hat = np.linalg.solve(R_reg, Q_reg.T @ y)

# Hat Matrix P and Residual Maker M
P = F @ np.linalg.solve(F.T @ F, F.T)
M = np.eye(n) - P

# Algebraic Checks
assert np.allclose(P @ P, P)
assert np.allclose(M @ M, M)
assert np.allclose(M @ F, 0.0)  # Orthogonality of residuals to design matrix!

# Residuals and Model Fits
e = M @ y
SSE = (y.T @ M @ y)
SST = (y.T @ H @ y)
R_sq = 1.0 - (SSE / SST)

print(f"Alpha: {beta_hat[0]:.6f}, Beta(SPY): {beta_hat[1]:.4f}, Beta(TLT): {beta_hat[2]:.4f}")
print(f"R-squared: {R_sq*100:.2f}%")
assert R_sq > 0.70
```""",
        [
            "OLS coefficients $\\hat{\\beta}$ computed via QR decomposition match normal equations.",
            "Hat matrix $P$ and residual maker $M$ verified symmetric and idempotent.",
            "Residuals are strictly orthogonal to regressors: $M F = \\mathbf{0}$.",
            "Model $R^2$ exceeds $70\\%$, confirming strong explanatory power."
        ]
    )
]

def generate_story_md(story):
    filename, title, role, goal, benefit, book_chap, sections, learnings, guide, criteria = story
    
    learnings_md = "\n".join([f"{i+1}. {item}" for i, item in enumerate(learnings)])
    criteria_md = "\n".join([f"- [X] {item}" for item in criteria])
    
    return f"""# {title}

## User Story
**As a** {role},
**I want to** {goal},
**So that** {benefit}.

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** {book_chap}
* **Sections:** {sections}

---

## 🎯 What You Will Learn
{learnings_md}

---

## 🛠️ Step-by-Step Implementation Guide

{guide}

---

## ✅ Acceptance Criteria
{criteria_md}
"""

def main():
    stories_dir = Path("stories")
    for s in project_stories:
        filename = s[0]
        md_content = generate_story_md(s)
        out_path = stories_dir / f"{filename}.md"
        out_path.write_text(md_content, encoding="utf-8")
        print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()
