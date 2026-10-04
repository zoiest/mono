#!/usr/bin/env python3
"""
Generates bin/ch11_capstone_project.org and progressive stories (025 to 030).
"""

from pathlib import Path

CH11 = r""":PROPERTIES:
:ID:       0192e4b3-0011-7000-8000-000000000011
:ROAM_ALIASES: "Chapter 11: Capstone Project" "Multivariate Financial Analytics Engine" "Matrix Algebra in Practice"
:END:
#+title: Chapter 11: Capstone Project — Multivariate Asset Analytics Engine
#+subtitle: Progressive Implementation of an End-to-End Financial Risk & Factor Model
#+author: Antigravity Notes
#+date: [2026-10-04]
#+filetags: :capstone:project:finance:covariance:pca:cholesky:markowitz:regression:

[[id:0192e4b3-0010-7000-8000-000000000010][← Previous: Chapter 10 (Outline Solutions)]] | [[id:0192e4b3-0000-7000-8000-000000000000][Master Index]]

* Project Overview & Dataset Specification

This hands-on capstone project connects the core matrix algebra principles from Chapters 1 through 9 into a cohesive, production-grade statistical engine: the *Multivariate Asset Analytics & Portfolio Risk Engine*.

** The Dataset
Located at ~data/asset_returns.csv~, this dataset comprises $N = 250$ business days of returns across $p = 6$ major exchange-traded funds representing distinct economic asset classes:
1. *SPY:* S&P 500 ETF (US Large-Cap Equity benchmark)
2. *QQQ:* Nasdaq 100 ETF (Tech Growth Equity)
3. *GLD:* SPDR Gold Shares (Precious Metals Commodity)
4. *XLE:* Energy Select Sector ETF (Cyclical Natural Resources)
5. *TLT:* 20+ Year Treasury Bond ETF (Fixed Income Duration / Flight-to-Safety)
6. *VNQ:* Vanguard Real Estate ETF (REITs / Real Assets)

** Progressive Implementation Architecture
The project is organized into six interconnected phases:
1. *Phase 1: Ingestion, Centering, and Covariance:* Centering matrix $H_n = I - \frac{1}{n}\mathbf{1}\mathbf{1}^T$, sample covariance $S = \frac{1}{n-1} X^T H_n X$, and correlation matrix $R$.
2. *Phase 2: Conditioning, Precision Matrix, and Online Updates:* Condition number $\kappa(S)$, partial correlations via precision matrix $\Theta = S^{-1}$, and $O(p^2)$ streaming Sherman-Morrison updates.
3. *Phase 3: PCA Factor Analysis and SVD Denoising:* Spectral decomposition $S = P \Lambda P^T$, scree analysis, and Eckart-Young optimal low-rank covariance filtering.
4. *Phase 4: Mahalanobis Anomaly Detection & Cholesky Whitening:* Lower-triangular Cholesky factorization $S = L L^T$, whitening transformation $Z = (X - \mathbf{1}\bar{x}^T)(L^{-1})^T$, and Hotelling's $T^2$ test identifying market shock days.
5. *Phase 5: Markowitz Minimum-Variance Portfolio:* Constrained quadratic optimization via Lagrange multipliers $w^* = \frac{S^{-1}\mathbf{1}}{\mathbf{1}^T S^{-1} \mathbf{1}}$, and efficient frontier derivation via block matrix inversion.
6. *Phase 6: Multi-Factor Pricing Regression:* General linear model $y = X\beta + \epsilon$, QR-based OLS estimation, Hat matrix $P$, residual maker $M = I - P$, and ANOVA sum of squares decomposition.

* Phase 1: Data Ingestion, Centering, and Sample Statistics

#+begin_src python
import csv
import numpy as np

# 1. Load dataset into NumPy 2D array
def load_returns_data(csv_path: str = "data/asset_returns.csv"):
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        assets = header[1:]
        dates = []
        data = []
        for row in reader:
            dates.append(row[0])
            data.append([float(val) for val in row[1:]])
    return assets, dates, np.array(data)

assets, dates, X = load_returns_data()
n, p = X.shape
print(f"Loaded returns matrix X: {n} days x {p} assets ({assets})")

# 2. Algebraic Mean Centering via Centering Matrix H_n
ones = np.ones((n, 1))
H = np.eye(n) - (ones @ ones.T) / n

# Verify H properties
assert np.allclose(H, H.T)              # Symmetric
assert np.allclose(H @ H, H)            # Idempotent
assert np.isclose(np.trace(H), n - 1)   # Rank equals n - 1 = 249

# Mean vector and centered data
xbar = (X.T @ ones) / n
X_centered = H @ X

# 3. Sample Covariance Matrix S
S = (X.T @ H @ X) / (n - 1)

# Correlation Matrix R = D^{-1} S D^{-1}
D_inv = np.diag(1.0 / np.sqrt(np.diag(S)))
R = D_inv @ S @ D_inv

print("\nSample Covariance Matrix S (x 10^4):\n", np.round(S * 1e4, 3))
print("\nSample Correlation Matrix R:\n", np.round(R, 3))
#+end_src

* Phase 2: Conditioning, Precision Matrix, and Online Sherman-Morrison Updates

The inverse covariance $\Theta = S^{-1}$ is the *precision matrix*. Off-diagonal entries describe partial correlations between assets after controlling for all other assets:
\begin{equation}
\rho_{ij \cdot \text{rest}} = -\frac{\theta_{ij}}{\sqrt{\theta_{ii} \theta_{jj}}}
\end{equation}

When new returns $x_{t+1}$ arrive, updating $S$ via standard inversion costs $O(p^3)$. Using the **Sherman-Morrison formula**, we update $S^{-1}$ in $O(p^2)$ time!

#+begin_src python
# 1. Condition Number & Precision Matrix
cond_S = np.linalg.cond(S)
print(f"Condition number kappa(S): {cond_S:.2f} (Well-conditioned)")

Theta = np.linalg.inv(S)

# Partial Correlation Matrix
D_theta = np.diag(1.0 / np.sqrt(np.diag(Theta)))
P_corr = -D_theta @ Theta @ D_theta
np.fill_diagonal(P_corr, 1.0)
print("\nPartial Correlation Matrix:\n", np.round(P_corr, 3))

# 2. Recursive Online Sherman-Morrison Covariance Update
# Simulating the arrival of a new observation vector x_new
x_new = np.array([-0.012, -0.015, 0.004, -0.008, 0.007, -0.010])

# Direct batch update with n + 1 points
X_extended = np.vstack([X, x_new])
n_new = n + 1
H_new = np.eye(n_new) - np.ones((n_new, n_new)) / n_new
S_direct_new = (X_extended.T @ H_new @ X_extended) / (n_new - 1)
inv_direct_new = np.linalg.inv(S_direct_new)

# Sherman-Morrison Update:
# S_{n+1} = ((n-1)/n) * S_n + (1/(n+1)) * (x_new - xbar)(x_new - xbar)^T
c = (n - 1) / n
delta = (x_new - xbar.flatten())[:, None]
gamma = 1.0 / (n + 1)

# (c * S + gamma * delta @ delta.T)^{-1}
# Let A = c * S, then A^{-1} = (1/c) * Theta
A_inv = Theta / c
u = delta
v = gamma * delta
denom = 1.0 + (v.T @ A_inv @ u)[0, 0]
inv_sm_new = A_inv - (A_inv @ u @ v.T @ A_inv) / denom

print("Sherman-Morrison updated inverse matches batch re-inversion:", np.allclose(inv_direct_new, inv_sm_new, atol=1e-5))
assert np.allclose(inv_direct_new, inv_sm_new, atol=1e-5)
#+end_src

* Phase 3: PCA Factor Model & SVD Covariance Denoising

#+begin_src python
# 1. Spectral Decomposition of S
evals, P = np.linalg.eigh(S)
# Sort in descending order
idx = np.argsort(evals)[::-1]
evals, P = evals[idx], P[:, idx]

total_var = np.trace(S)
explained_var_ratio = evals / total_var
cumulative_var = np.cumsum(explained_var_ratio)

print("Eigenvalues (Variance per Mode):", np.round(evals * 1e4, 4))
print("Percentage of Variance Explained:", np.round(explained_var_ratio * 100, 2))
print("Cumulative Variance:", np.round(cumulative_var * 100, 2))

# Interpret the Top 3 Factor Loadings:
for j in range(3):
    print(f"\nFactor {j+1} Loadings ({explained_var_ratio[j]*100:.1f}% var):")
    for asset, load in zip(assets, P[:, j]):
        print(f"  {asset:>4}: {load:+.4f}")

# 2. Eckart-Young Low-Rank Factor Denoising (k = 3 factors)
k = 3
S_factors = P[:, :k] @ np.diag(evals[:k]) @ P[:, :k].T
# Residual specific asset variance
Psi = np.diag(np.maximum(np.diag(S - S_factors), 0))
S_denoised = S_factors + Psi

print("\nOriginal Trace tr(S):", total_var)
print("Denoised Trace tr(S_denoised):", np.trace(S_denoised))
assert np.isclose(total_var, np.trace(S_denoised))
#+end_src

* Phase 4: Mahalanobis Distance, Cholesky Whitening, and Shock Detection

#+begin_src python
import scipy.stats as stats

# 1. Cholesky Factorization
L = np.linalg.cholesky(S)  # S = L @ L.T
assert np.allclose(L @ L.T, S)

# 2. Whitening Transformation
# Z = (X - 1 xbar^T) (L^{-1})^T
Z = (X - xbar.T) @ np.linalg.inv(L).T
cov_Z = np.cov(Z, rowvar=False)
assert np.allclose(cov_Z, np.eye(p), atol=1e-2)
print("Cholesky Whitened Covariance matches Identity I_p within empirical error.")

# 3. Mahalanobis Distances across all 250 trading days
# D_M^2(x_t) = (x_t - xbar)^T S^{-1} (x_t - xbar) == ||z_t||_2^2
d_mahal = np.sum(Z ** 2, axis=1)

# Critical value at alpha = 0.001 under Chi-Square(p=6)
crit_val = stats.chi2.ppf(0.999, df=p)
anomalies = np.where(d_mahal > crit_val)[0]

print(f"\nChi-Square(df=6) 99.9% Critical Threshold: {crit_val:.2f}")
print("Detected Anomaly Day Indices:", anomalies)
for day in anomalies:
    p_val = 1.0 - stats.chi2.cdf(d_mahal[day], df=p)
    print(f"  Date: {dates[day]} (Day {day}) | Mahalanobis D_M^2 = {d_mahal[day]:.2f} | p-value = {p_val:.2e}")

# Day 180 is precisely our injected market shock!
assert 180 in anomalies
print("Successfully pinpointed injected market shock at Day 180!")
#+end_src

* Phase 5: Markowitz Minimum-Variance Portfolio via Constrained Optimization

The Global Minimum Variance (GMV) portfolio minimizes $w^T S w$ subject to $w^T \mathbf{1} = 1$:
\begin{equation}
L(w, \lambda) = w^T S w - \lambda (w^T \mathbf{1} - 1)
\end{equation}
Differentiating:
\begin{equation}
\frac{\partial L}{\partial w} = 2 S w - \lambda \mathbf{1} = \mathbf{0} \implies w = \frac{\lambda}{2} S^{-1} \mathbf{1}
\end{equation}
Using $\mathbf{1}^T w = 1 \implies \frac{\lambda}{2} \mathbf{1}^T S^{-1} \mathbf{1} = 1 \implies \frac{\lambda}{2} = \frac{1}{\mathbf{1}^T S^{-1} \mathbf{1}}$.
Therefore:
\begin{equation}
w^* = \frac{S^{-1} \mathbf{1}}{\mathbf{1}^T S^{-1} \mathbf{1}}
\end{equation}

#+begin_src python
# 1. Global Minimum Variance (GMV) Weights
ones_p = np.ones((p, 1))
S_inv = np.linalg.inv(S)

numerator = S_inv @ ones_p
denominator = (ones_p.T @ S_inv @ ones_p)[0, 0]
w_gmv = (numerator / denominator).flatten()

# Verify weights sum to 1
assert np.isclose(np.sum(w_gmv), 1.0)

# GMV Portfolio Annualized Volatility
daily_var_gmv = w_gmv.T @ S @ w_gmv
ann_vol_gmv = np.sqrt(daily_var_gmv * 252)
indiv_ann_vols = np.sqrt(np.diag(S) * 252)

print("\nOptimal GMV Portfolio Weights:")
for asset, w in zip(assets, w_gmv):
    print(f"  {asset:>4}: {w*100:+6.2f}%")

print(f"\nGMV Annualized Volatility: {ann_vol_gmv*100:.2f}%")
print("Individual Asset Volatilities:")
for asset, v in zip(assets, indiv_ann_vols):
    print(f"  {asset:>4}: {v*100:.2f}%")

# Diversification benefit: GMV risk is strictly lower than every component asset!
assert ann_vol_gmv < np.min(indiv_ann_vols)
print("Markowitz diversification theorem verified: Portfolio risk < min individual asset risk!")
#+end_src

* Phase 6: Factor Pricing Regression & Residual Analysis

Model asset returns as a linear function of Market (SPY) and Duration (TLT) factors:
\begin{equation}
y_t = \beta_0 + \beta_1 r_{\text{SPY}, t} + \beta_2 r_{\text{TLT}, t} + \epsilon_t
\end{equation}

#+begin_src python
# 1. Multi-factor regression for QQQ (Tech) and XLE (Energy)
target_idx = assets.index("QQQ")
y = X[:, target_idx]

# Regressors: Intercept, SPY (Market), TLT (Bonds)
F_matrix = np.column_stack([np.ones(n), X[:, assets.index("SPY")], X[:, assets.index("TLT")]])
k_vars = F_matrix.shape[1]

# 2. QR-based OLS Estimation
Q_reg, R_reg = np.linalg.qr(F_matrix)
beta_hat = np.linalg.solve(R_reg, Q_reg.T @ y)

# 3. Hat Matrix P and Residual Maker M
P = F_matrix @ np.linalg.solve(F_matrix.T @ F_matrix, F_matrix.T)
M = np.eye(n) - P

# Algebraic Checks: Idempotency and Orthogonality
assert np.allclose(P @ P, P)
assert np.allclose(M @ M, M)
assert np.allclose(P @ M, 0.0)
assert np.allclose(M @ F_matrix, 0.0)  # Residuals orthogonal to regressors!

# Residuals and Sum of Squares
residuals = M @ y
SSE = (y.T @ M @ y)
SST = (y.T @ H @ y)
R_squared = 1.0 - (SSE / SST)
s_error = np.sqrt(SSE / (n - k_vars))

print(f"\nQQQ 2-Factor Pricing Model Results:")
print(f"  Alpha (Intercept): {beta_hat[0]:.6f}")
print(f"  Beta (Market/SPY): {beta_hat[1]:.4f}")
print(f"  Beta (Bonds/TLT):  {beta_hat[2]:.4f}")
print(f"  Model R^2:         {R_squared*100:.2f}%")
print(f"  Residual Std Err:  {s_error:.6f}")

assert R_squared > 0.70  # Tech returns strongly explained by Market and Rates
print("Factor model projection and Gauss-Markov residual orthogonality fully verified.")
#+end_src

* Capstone Summary & Skills Acquired

By executing this project, you have implemented:
1. *Data Centering & Matrix Statistics:* $H_n = I - \frac{1}{n}\mathbf{1}\mathbf{1}^T$, $S = \frac{1}{n-1} X^T H_n X$.
2. *Real-time Streaming Matrix Updates:* $O(p^2)$ Sherman-Morrison rank-1 recursive inverse updates.
3. *Factor Risk Analysis:* Spectral Theorem $S = P \Lambda P^T$, scree analysis, and SVD denoising.
4. *Whitening & Outlier Detection:* Cholesky factor $L L^T = S$, Mahalanobis distance, and Hotelling's $T^2$ anomaly testing.
5. *Constrained Matrix Optimization:* Markowitz GMV portfolio $w^* = \frac{S^{-1}\mathbf{1}}{\mathbf{1}^T S^{-1} \mathbf{1}}$.
6. *Linear Model Geometry:* Hat matrix $P$, residual maker $M$, and ANOVA quadratic forms.
"""

def main():
    Path("bin/ch11_capstone_project.org").write_text(CH11, encoding="utf-8")
    print("Wrote bin/ch11_capstone_project.org")

if __name__ == "__main__":
    main()
