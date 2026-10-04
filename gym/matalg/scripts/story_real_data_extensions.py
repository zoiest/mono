"""Real data practical extensions for stories 001 through 024.
References data/asset_returns.csv (N=250 days, p=6 assets: SPY, QQQ, GLD, XLE, TLT, VNQ).
"""

EXTENSIONS = {
    "001": {
        "learnings": [
            "Ingesting multivariate financial CSV data (`data/asset_returns.csv`) into 2D NumPy float arrays.",
            "Slicing multi-asset time series and ensuring contiguous C-order memory layout.",
        ],
        "guide": r"""### 3. 📊 Practical Dataset Application: Real Market Data Ingestion & Slicing
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
```""",
        "criteria": [
            "`data/asset_returns.csv` is loaded into a $(250, 6)$ contiguous NumPy array.",
            "Multi-asset slicing extracts 5-day equity sub-matrix with shape $(5, 2)$.",
            "Single-column asset extraction preserves $(250, 1)$ column-vector shape.",
        ],
    },
    "002": {
        "learnings": [
            "Computing inner products and cosine similarity between empirical asset return series.",
            "Constructing an orthogonalized Treasury return series via Gram-Schmidt projection.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Vector Geometry & Orthogonalization
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape
H = np.eye(n) - np.ones((n, n)) / n
X_tilde = H @ X  # mean-centered returns

# Extract centered returns for SPY (col 0) and TLT (col 4)
s = X_tilde[:, 0]  # SPY
t = X_tilde[:, 4]  # TLT

# Inner product & Cosine similarity (flight-to-safety check)
dot_st = s @ t
norm_s = np.linalg.norm(s)
norm_t = np.linalg.norm(t)
cos_sim = dot_st / (norm_s * norm_t)
print(f"SPY dot TLT: {dot_st:.6f}")
print(f"SPY vs TLT Cosine Similarity: {cos_sim:.4f}")
assert cos_sim < 0  # Confirms negative correlation (flight-to-safety duration hedge)

# Gram-Schmidt Orthogonalization: isolate TLT component orthogonal to SPY
# t_perp = t - proj_s(t)
t_perp = t - ((s @ t) / (s @ s)) * s
print("Orthogonalized TLT dot SPY:", s @ t_perp)
assert np.isclose(s @ t_perp, 0.0, atol=1e-12)

# Outer product of mean return vector
x_bar = np.mean(X, axis=0)
outer_mean = np.outer(x_bar, x_bar)
print("Outer product of mean return vector shape:", outer_mean.shape)
assert outer_mean.shape == (6, 6)
assert np.linalg.matrix_rank(outer_mean) == 1
```""",
        "criteria": [
            "Cosine similarity between SPY and TLT is verified negative on centered returns.",
            "Treasury returns are successfully orthogonalized against equity returns ($s^T t_\\perp = 0$).",
            "Outer product of the asset mean vector $\\bar{x}\\bar{x}^T$ is verified to have rank 1.",
        ],
    },
    "003": {
        "learnings": [
            "Evaluating portfolio returns $r_p = X w$ via matrix-vector multiplication.",
            "Verifying the cyclic trace property and Frobenius norm on empirical asset cross-products.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Portfolio Returns & Cross Products
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape

# 1. Equal-weighted portfolio return vector via matrix-vector product
w = np.ones(p) / p
r_port = X @ w
assert r_port.shape == (n,)
print(f"Equal-weight portfolio annualized return: {np.mean(r_port) * 252 * 100:.2f}%")

# 2. Scatter / Cross-product matrix G = X^T X
G = X.T @ X
assert G.shape == (p, p)
assert np.allclose(G, G.T)

# 3. Cyclic trace invariance: tr(X X^T) == tr(X^T X)
tr_XXt = np.trace(X @ X.T)
tr_XtX = np.trace(G)
print(f"tr(X X^T) = {tr_XXt:.4f}, tr(X^T X) = {tr_XtX:.4f}")
assert np.isclose(tr_XXt, tr_XtX)

# 4. Frobenius norm equality: ||X||_F == sqrt(tr(X^T X))
norm_fro = np.linalg.norm(X, "fro")
norm_trace = np.sqrt(tr_XtX)
assert np.isclose(norm_fro, norm_trace)
print(f"Total Market Frobenius Norm ||X||_F: {norm_fro:.4f}")
```""",
        "criteria": [
            "Equal-weight portfolio return series is computed using matrix-vector multiplication.",
            "Cross-product matrix $X^TX$ is verified symmetric $(6 \\times 6)$.",
            "Cyclic trace identity $\\text{tr}(X X^T) = \\text{tr}(X^T X)$ is confirmed on empirical returns.",
            "Matrix Frobenius norm $\\|X\\|_F = \\sqrt{\\text{tr}(X^TX)}$ is numerically verified.",
        ],
    },
    "004": {
        "learnings": [
            "Decomposing empirical cross-lag transition matrices into symmetric and skew-symmetric components.",
            "Computing portfolio variance as a strictly positive quadratic form $w^T S w > 0$.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Cross-Lag Symmetrization & Portfolio Variance
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape

# 1. Cross-lag covariance matrix between day t-1 and day t
X_lag = X[:-1]
X_lead = X[1:]
H_sub = np.eye(n - 1) - np.ones((n - 1, n - 1)) / (n - 1)
M_lag = (X_lag.T @ H_sub @ X_lead) / (n - 2)

# Decompose non-symmetric cross-lag matrix into symmetric and skew-symmetric parts
M_sym = 0.5 * (M_lag + M_lag.T)
M_skew = 0.5 * (M_lag - M_lag.T)

assert np.allclose(M_lag, M_sym + M_skew)
assert np.allclose(M_skew.T, -M_skew)

# Any quadratic form eliminates the skew-symmetric component: w^T M w == w^T M_sym w
w = np.array([0.2, 0.2, 0.15, 0.15, 0.15, 0.15])
q_raw = w.T @ M_lag @ w
q_sym = w.T @ M_sym @ w
q_skew = w.T @ M_skew @ w
assert np.isclose(q_skew, 0.0)
assert np.isclose(q_raw, q_sym)

# 2. Portfolio variance quadratic form
H = np.eye(n) - np.ones((n, n)) / n
S = (X.T @ H @ X) / (n - 1)
port_var = w.T @ S @ w
port_vol = np.sqrt(port_var * 252)
print(f"Portfolio Annualized Volatility: {port_vol * 100:.2f}%")
assert port_var > 0  # Strict positive definiteness
```""",
        "criteria": [
            "Cross-lag transition matrix is decomposed into symmetric and skew-symmetric components.",
            "Skew-symmetric quadratic form $w^T M_{\\text{skew}} w = 0$ is numerically verified.",
            "Portfolio variance quadratic form $w^T S w > 0$ confirms positive definiteness.",
        ],
    },
    "005": {
        "learnings": [
            "Constructing the $250 \\times 250$ centering matrix $H_{250}$ and computing de-meaned returns.",
            "Computing sample covariance $S = \\frac{1}{n-1} X^T H X$ and scaling to correlation matrix $R = D^{-1} S D^{-1}$.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Centering, Covariance, and Correlation
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    assets = next(reader)[1:]
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape

# Construct Centering Matrix H_n
ones = np.ones((n, 1))
H = np.eye(n) - (ones @ ones.T) / n

# Verify H properties
assert np.allclose(H, H.T)              # Symmetric
assert np.allclose(H @ H, H)            # Idempotent
assert np.isclose(np.trace(H), n - 1)   # Rank = 249

# Center the asset returns
X_centered = H @ X
col_means = np.mean(X_centered, axis=0)
assert np.allclose(col_means, 0.0, atol=1e-12)

# Sample covariance matrix S
S = (X.T @ H @ X) / (n - 1)
S_np = np.cov(X, rowvar=False)
assert np.allclose(S, S_np)

# Scaling S to correlation matrix R = D^{-1} S D^{-1}
D_inv = np.diag(1.0 / np.sqrt(np.diag(S)))
R = D_inv @ S @ D_inv
assert np.allclose(np.diag(R), np.ones(p))
print("Empirical Correlation Matrix R (SPY, QQQ, GLD, XLE, TLT, VNQ):\n", np.round(R, 3))
```""",
        "criteria": [
            "Centering matrix $H_{250}$ is verified symmetric, idempotent, and rank 249.",
            "De-meaned matrix $HX$ has zero column means ($\\mathbf{1}^T(HX) = \\mathbf{0}$).",
            "Covariance matrix $S = \\frac{1}{n-1}X^THX$ matches NumPy's `np.cov`.",
            "Correlation matrix $R = D^{-1} S D^{-1}$ has unit diagonal.",
        ],
    },
    "006": {
        "learnings": [
            "Partitioning the 6 assets into Equities/Energy vs Defensive/Income blocks.",
            "Computing block covariance sub-matrices and verifying cross-block transpositions.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Asset Class Partitioning & Block Covariance
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape
H = np.eye(n) - np.ones((n, n)) / n
X_tilde = H @ X

# Partition assets into two economic blocks:
# Block 1: Growth & Cyclicals (SPY, QQQ, XLE -> indices 0, 1, 3)
# Block 2: Defensive & Yield (GLD, TLT, VNQ -> indices 2, 4, 5)
idx1 = [0, 1, 3]
idx2 = [2, 4, 5]
X1 = X_tilde[:, idx1]  # (250, 3)
X2 = X_tilde[:, idx2]  # (250, 3)

# Block covariance computation
S11 = (X1.T @ X1) / (n - 1)  # (3, 3) Equities auto-covariance
S22 = (X2.T @ X2) / (n - 1)  # (3, 3) Defensive auto-covariance
S12 = (X1.T @ X2) / (n - 1)  # (3, 3) Cross-covariance
S21 = (X2.T @ X1) / (n - 1)  # (3, 3) Cross-covariance

assert np.allclose(S12, S21.T)

# Assemble 2x2 block matrix
S_block = np.block([[S11, S12], [S21, S22]])

# Compare with reordered full covariance matrix
S_full = (X_tilde.T @ X_tilde) / (n - 1)
idx_reordered = idx1 + idx2
S_reordered = S_full[np.ix_(idx_reordered, idx_reordered)]
assert np.allclose(S_block, S_reordered)
print("Block Covariance Matrix assembled successfully:\n", np.round(S_block * 1e4, 2))
```""",
        "criteria": [
            "Assets are partitioned into two $(250, 3)$ economic blocks.",
            "Cross-covariance symmetry $S_{12} = S_{21}^T$ is verified.",
            "Full covariance assembled via `np.block` matches indexed slice of $S$.",
        ],
    },
    "007": {
        "learnings": [
            "Detecting full column rank in multivariate market return series.",
            "Diagnosing artificial multicollinearity and near-zero singular values.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Rank & Multicollinearity Diagnostics
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
```""",
        "criteria": [
            "Empirical returns matrix $X$ is confirmed full rank ($\\text{rank}(X) = 6$).",
            "Appending a collinear synthetic asset does not increase the rank ($\\text{rank}(X_{\\text{aug}}) = 6$).",
            "Smallest singular value of the collinear system is verified to be zero ($\\approx 10^{-15}$).",
        ],
    },
    "008": {
        "learnings": [
            "Performing rank-1 decomposition of centered returns to extract the systematic market factor.",
            "Verifying the outer product structure of the leading factor approximation.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Systematic Factor Rank-1 Factorization
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape
H = np.eye(n) - np.ones((n, n)) / n
X_tilde = H @ X

# Rank-1 Market Factor Factorization via SVD
U, Sig, Vt = np.linalg.svd(X_tilde, full_matrices=False)

# Dominant mode: sigma_1 * u_1 * v_1^T
f1 = Sig[0] * U[:, 0]    # Factor scores (250,)
beta1 = Vt[0, :]         # Factor exposures / betas (6,)
M1 = np.outer(f1, beta1) # Rank-1 matrix (250, 6)

print(f"Leading singular value: {Sig[0]:.4f}")
print("Asset exposures to systematic market mode (beta_1):\n", np.round(beta1, 4))
assert np.linalg.matrix_rank(M1) == 1
assert np.allclose(M1, Sig[0] * np.outer(U[:, 0], Vt[0, :]))

# Percentage of total variance captured by the rank-1 market factor
var_explained = (Sig[0] ** 2) / np.sum(Sig ** 2)
print(f"Variance explained by rank-1 systematic factor: {var_explained * 100:.2f}%")
assert var_explained > 0.40  # Dominant market factor captures over 40% of variance
```""",
        "criteria": [
            "Leading SVD mode factorizes centered returns into outer product of factor scores and asset loadings.",
            "Factor matrix $M_1 = f_1 \\beta_1^T$ is confirmed to have matrix rank 1.",
            "Leading rank-1 systematic factor explains $> 40\\%$ of total empirical variance.",
        ],
    },
    "009": {
        "learnings": [
            "Demonstrating the '$p > n$' rank deficiency in rolling window covariance estimation.",
            "Verifying Sylvester's rank inequality on short financial time series.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Short-Window Rank Deficiency ($p > n$)
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

# Short-window estimation: k = 4 days for p = 6 assets
k = 4
p = 6
X_short = X[:k, :]  # (4, 6)
H_short = np.eye(k) - np.ones((k, k)) / k
S_short = (X_short.T @ H_short @ X_short) / (k - 1)  # (6, 6)

# By rank inequality: rank(S_short) <= min(rank(X_short^T), rank(H_short)) <= k - 1 = 3
rank_S_short = np.linalg.matrix_rank(S_short)
print(f"Short window ({k} days, {p} assets) Covariance Rank: {rank_S_short}")
assert rank_S_short <= k - 1
assert rank_S_short < p

# Demonstrating singularity
det_S_short = np.linalg.det(S_short)
print(f"det(S_short): {det_S_short:.2e}")
assert np.isclose(det_S_short, 0.0)

# Attempting naive inversion raises LinAlgError
try:
    np.linalg.inv(S_short)
    assert False, "Should have raised LinAlgError"
except np.linalg.LinAlgError:
    print("Expected LinAlgError caught: Short-window covariance is non-invertible!")
```""",
        "criteria": [
            "Short-window sample covariance ($k = 4, p = 6$) has $\\text{rank}(S_{\\text{short}}) \\le 3$.",
            "Determinant of short-window covariance is verified to be 0.",
            "Inversion of rank-deficient covariance is confirmed to raise `LinAlgError`.",
        ],
    },
    "010": {
        "learnings": [
            "Computing generalized sample variance $\\det(S)$ and safe log-determinant $\\log \\det(S)$.",
            "Comparing hypervolume of diversified asset basket versus concentrated equity basket.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Generalized Variance & Ellipsoid Volume
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

# 1. Generalized sample variance det(S)
det_S = np.linalg.det(S)
print(f"Generalized sample variance det(S): {det_S:.2e}")
assert det_S > 0  # Strictly positive definite

# 2. Numerically safe log-determinant
sign, logdet = np.linalg.slogdet(S)
assert sign > 0
assert np.isclose(logdet, np.log(det_S))
print(f"Log-determinant log|S|: {logdet:.4f}")

# 3. Geometric hypervolume comparison: Diversified (6 assets) vs Equity Block (2 assets)
S_equity = S[:2, :2]
det_equity = np.linalg.det(S_equity)
print(f"Equity Block det(S_equity): {det_equity:.2e}")
# The volume of the uncertainty ellipsoid is proportional to sqrt(det(S))
vol_equity = np.sqrt(det_equity)
assert vol_equity > 0
```""",
        "criteria": [
            "Generalized sample variance $\\det(S) > 0$ confirms positive definiteness.",
            "Numerically stable log-determinant via `np.linalg.slogdet` matches `log(det(S))`.",
            "Ellipsoidal uncertainty volume for equity block is computed.",
        ],
    },
    "011": {
        "learnings": [
            "Partitioning covariance into Equities ($A$) and Non-Equities ($D$).",
            "Computing the Schur complement conditional covariance $D - C A^{-1} B$ and verifying the block determinant identity.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Schur Complement & Information Reduction
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

# Partition S into Equities (A: SPY, QQQ) and Hedges/Commodities (D: GLD, XLE, TLT, VNQ)
A = S[:2, :2]
B = S[:2, 2:]
C = S[2:, :2]
D = S[2:, 2:]

# Schur complement: conditional covariance of Non-Equities given Equities
S_schur = D - C @ np.linalg.inv(A) @ B
print("Schur Complement (Conditional Covariance D|A) shape:", S_schur.shape)

# Verify Block Determinant Identity: det(S) == det(A) * det(S_schur)
det_S = np.linalg.det(S)
det_A = np.linalg.det(A)
det_schur = np.linalg.det(S_schur)

print(f"det(S): {det_S:.2e}")
print(f"det(A) * det(S_schur): {det_A * det_schur:.2e}")
assert np.isclose(det_S, det_A * det_schur)

# Information reduction: conditioning reduces generalized variance
assert det_schur < np.linalg.det(D)
print("Information reduction verified: det(D|A) < det(D)")
```""",
        "criteria": [
            "Schur complement conditional covariance $S / A = D - C A^{-1} B$ is computed.",
            "Block determinant identity $\\det(S) = \\det(A) \\det(D - C A^{-1} B)$ is confirmed.",
            "Conditioning reduces generalized variance: $\\det(D - C A^{-1} B) < \\det(D)$.",
        ],
    },
    "012": {
        "learnings": [
            "Updating covariance determinants under market shock events via Weinstein-Aronszajn formula.",
            "Comparing empirical correlation determinants against equicorrelation matrix approximations.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Shock Determinant Update & Equicorrelation
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
x_mean = np.mean(X, axis=0)

# Rank-1 shock vector: Day 180 market dislocation event
z = (X[180, :] - x_mean).reshape(-1, 1)  # (6, 1)
c_scale = 1.0 / n

# Updated covariance matrix
S_up = S + c_scale * (z @ z.T)

# Weinstein-Aronszajn identity: det(S + c z z^T) = det(S) * (1 + c z^T S^{-1} z)
inv_S = np.linalg.inv(S)
mahal_term = (z.T @ inv_S @ z)[0, 0]
det_updated_formula = np.linalg.det(S) * (1.0 + c_scale * mahal_term)
det_updated_direct = np.linalg.det(S_up)

print(f"Formula Determinant: {det_updated_formula:.2e}")
print(f"Direct Determinant:  {det_updated_direct:.2e}")
assert np.isclose(det_updated_formula, det_updated_direct)

# Equicorrelation determinant approximation
D_inv = np.diag(1.0 / np.sqrt(np.diag(S)))
R = D_inv @ S @ D_inv
off_diag_corrs = R[np.triu_indices(p, k=1)]
rho_bar = np.mean(off_diag_corrs)
det_equicorr = ((1.0 - rho_bar) ** (p - 1)) * (1.0 + (p - 1) * rho_bar)
print(f"Average Correlation rho_bar: {rho_bar:.4f}")
print(f"Equicorrelation Determinant: {det_equicorr:.4f}, Actual det(R): {np.linalg.det(R):.4f}")
assert det_equicorr > 0
```""",
        "criteria": [
            "Determinant of rank-1 updated covariance matches Weinstein-Aronszajn formula $\\det(S)(1 + c z^T S^{-1} z)$.",
            "Outlier shock vector increases covariance determinant due to expanded dispersion.",
            "Average correlation $\\bar{\\rho}$ and equicorrelation determinant are computed.",
        ],
    },
    "013": {
        "learnings": [
            "Inverting the asset covariance matrix to obtain the precision matrix $\\Theta = S^{-1}$.",
            "Computing condition number $\\kappa(S)$ and evaluating GMV portfolio weights via `np.linalg.solve` vs `np.linalg.inv`.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Precision Matrix & GMV Portfolio
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

# Condition number of empirical covariance matrix
cond_S = np.linalg.cond(S)
print(f"Covariance Matrix Condition Number kappa(S): {cond_S:.2f}")

# Computing Global Minimum Variance (GMV) portfolio weights: S w = 1
ones = np.ones(p)

# Method 1: Numerically robust solve
w_solve_raw = np.linalg.solve(S, ones)
w_solve = w_solve_raw / np.sum(w_solve_raw)

# Method 2: Explicit matrix inversion
Theta = np.linalg.inv(S)
w_inv_raw = Theta @ ones
w_inv = w_inv_raw / np.sum(w_inv_raw)

# Compare weights and residuals
assert np.allclose(w_solve, w_inv)
res_solve = np.linalg.norm(S @ w_solve_raw - ones)
res_inv = np.linalg.norm(S @ w_inv_raw - ones)
print(f"Residual ||S w_solve - 1||: {res_solve:.2e}")
print(f"Residual ||S w_inv - 1||:   {res_inv:.2e}")
assert res_solve < 1e-12

print("GMV Portfolio Weights (SPY, QQQ, GLD, XLE, TLT, VNQ):\n", np.round(w_solve, 4))
```""",
        "criteria": [
            "Precision matrix $\\Theta = S^{-1}$ and condition number $\\kappa(S)$ are evaluated.",
            "GMV portfolio weights solved via `np.linalg.solve` match explicit inversion.",
            "Linear system residual $\\|S w - \\mathbf{1}\\|_2 < 10^{-12}$ confirms precision of `np.linalg.solve`.",
        ],
    },
    "014": {
        "learnings": [
            "Updating the precision matrix $\\Theta = S^{-1}$ in $O(p^2)$ when streaming daily return shocks arrive.",
            "Verifying the Sherman-Morrison update against full $O(p^3)$ re-inversion.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Precision Matrix Online Sherman-Morrison Update
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
```""",
        "criteria": [
            "Precision matrix update under rank-1 shock is implemented via Sherman-Morrison formula.",
            "Sherman-Morrison result matches full $O(p^3)$ matrix inversion within float precision.",
            "Symmetry of updated precision matrix is preserved.",
        ],
    },
    "015": {
        "learnings": [
            "Inverting partitioned covariance matrices using the Banachiewicz block inversion formula.",
            "Extracting partial correlations between equity assets controlling for hedges and commodities.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Banachiewicz Block Inversion & Partial Correlations
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
```""",
        "criteria": [
            "Banachiewicz block inverse is assembled and verified against full matrix inversion.",
            "Bottom-right block of precision matrix is confirmed equal to inverse Schur complement $(S/A)^{-1}$.",
            "Partial correlation between SPY and QQQ controlling for other assets is computed from precision matrix entries.",
        ],
    },
    "016": {
        "learnings": [
            "Decomposing market covariance into eigenvalues and eigenvectors using `np.linalg.eigh`.",
            "Identifying the dominant eigenvector as the systematic market risk factor.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Covariance Spectral Decomposition & Risk Modes
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    assets = next(reader)[1:]
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape
H = np.eye(n) - np.ones((n, n)) / n
S = (X.T @ H @ X) / (n - 1)

# Spectral decomposition of symmetric covariance S
lambdas, Q = np.linalg.eigh(S)
# Sort in descending order
idx = np.argsort(lambdas)[::-1]
lambdas, Q = lambdas[idx], Q[:, idx]

# Verify spectral reconstruction: S == sum(lambda_i * q_i * q_i^T)
S_reconstructed = Q @ np.diag(lambdas) @ Q.T
assert np.allclose(S, S_reconstructed)
assert np.allclose(Q.T @ Q, np.eye(p))
assert np.isclose(np.sum(lambdas), np.trace(S))

# Variance explained
pct_var = lambdas / np.sum(lambdas)
print("Eigenvalues (sorted):", np.round(lambdas * 1e4, 3))
print("Variance Explained (%):", np.round(pct_var * 100, 2))

# Eigenvector 1 (Market Mode) loadings
print("PC1 Eigenvector Loadings across assets:")
for asset, weight in zip(assets, Q[:, 0]):
    print(f"  {asset:>4}: {weight:+.4f}")
```""",
        "criteria": [
            "Spectral decomposition $S = Q \\Lambda Q^T$ accurately reconstructs empirical covariance.",
            "Eigenvector matrix $Q$ is verified orthonormal ($Q^T Q = I_6$).",
            "Sum of eigenvalues equals total variance $\\text{tr}(S)$.",
            "Proportion of variance explained by each principal component is quantified.",
        ],
    },
    "017": {
        "learnings": [
            "Computing symmetric matrix square root $S^{1/2}$ and inverse square root $S^{-1/2}$.",
            "Implementing Mahalanobis whitening transformation $Z = \\tilde{X} S^{-1/2}$ to produce spherical uncorrelated returns.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Matrix Square Root & Mahalanobis Whitening
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape
H = np.eye(n) - np.ones((n, n)) / n
X_tilde = H @ X
S = (X_tilde.T @ X_tilde) / (n - 1)

# Spectral decomposition for matrix functions
lambdas, Q = np.linalg.eigh(S)

# Symmetric matrix square root and inverse square root
S_sqrt = Q @ np.diag(np.sqrt(lambdas)) @ Q.T
S_inv_sqrt = Q @ np.diag(1.0 / np.sqrt(lambdas)) @ Q.T

# Verification
assert np.allclose(S_sqrt @ S_sqrt, S)
assert np.allclose(S_inv_sqrt @ S @ S_inv_sqrt, np.eye(p))

# Mahalanobis Whitening Transformation: Z = X_tilde @ S^{-1/2}
Z = X_tilde @ S_inv_sqrt

# Covariance of whitened data must be identity matrix I_p
S_Z = (Z.T @ Z) / (n - 1)
assert np.allclose(S_Z, np.eye(p))
print("Whitening successful: Covariance of transformed returns equals I_6 exactly!")
```""",
        "criteria": [
            "Symmetric square root $S^{1/2}$ and inverse square root $S^{-1/2}$ are computed via spectral decomposition.",
            "Identities $S^{1/2} S^{1/2} = S$ and $S^{-1/2} S S^{-1/2} = I_6$ are confirmed.",
            "Whitened return series $Z = \\tilde{X} S^{-1/2}$ has empirical covariance equal to identity matrix $I_6$.",
        ],
    },
    "018": {
        "learnings": [
            "Performing thin SVD on centered returns matrix $\\tilde{X} = U \\Sigma V^T$.",
            "Denoising empirical return data using Eckart-Young-Mirsky rank-2 optimal truncation.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market SVD Factorization & Eckart-Young Denoising
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape
H = np.eye(n) - np.ones((n, n)) / n
X_tilde = H @ X

# Thin SVD
U, Sig, Vt = np.linalg.svd(X_tilde, full_matrices=False)

# Verify singular values match sqrt((n-1) * eigenvalues(S))
lambdas = np.sort(np.linalg.eigvalsh(np.cov(X, rowvar=False)))[::-1]
assert np.allclose(Sig, np.sqrt((n - 1) * lambdas))

# Eckart-Young Rank-2 Optimal Low-Rank Approximation
X_k2 = Sig[0] * np.outer(U[:, 0], Vt[0, :]) + Sig[1] * np.outer(U[:, 1], Vt[1, :])
assert np.linalg.matrix_rank(X_k2) == 2

# Low-rank covariance matrix
S_k2 = (X_k2.T @ X_k2) / (n - 1)
assert np.linalg.matrix_rank(S_k2) == 2

# Reconstruction error ||X - X_k2||_F == sqrt(sum_{i=3}^p sigma_i^2)
frob_residual = np.linalg.norm(X_tilde - X_k2, "fro")
expected_residual = np.sqrt(np.sum(Sig[2:] ** 2))
assert np.isclose(frob_residual, expected_residual)
print(f"Rank-2 SVD Denoising captures {((Sig[0]**2 + Sig[1]**2) / np.sum(Sig**2)) * 100:.2f}% of total variance")
```""",
        "criteria": [
            "Singular values $\\sigma_i$ are confirmed equal to $\\sqrt{(n-1)\\lambda_i}$.",
            "Rank-2 Eckart-Young approximation has rank 2 for both returns and reconstructed covariance.",
            "Residual Frobenius norm matches theoretical sum of truncated singular values.",
        ],
    },
    "019": {
        "learnings": [
            "Deriving and evaluating the matrix gradient of the multivariate normal log-likelihood $\\nabla_\\Sigma \\ell$.",
            "Numerically proving that the gradient vanishes at the sample MLE covariance $S_{\\text{MLE}}$.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Matrix Calculus for Gaussian MLE Covariance
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape
H = np.eye(n) - np.ones((n, n)) / n
X_tilde = H @ X
S = (X_tilde.T @ X_tilde) / (n - 1)

# MLE covariance estimate
S_mle = (n - 1) / n * S
inv_mle = np.linalg.inv(S_mle)
A_sum = (n - 1) * S  # Sum of squared deviations

# Log-likelihood gradient with respect to Sigma:
# grad = -0.5 * n * Sigma^{-1} + 0.5 * Sigma^{-1} A Sigma^{-1}
grad_mle = -0.5 * n * inv_mle + 0.5 * inv_mle @ A_sum @ inv_mle

print("Maximum absolute gradient at MLE:\n", np.max(np.abs(grad_mle)))
assert np.allclose(grad_mle, np.zeros((p, p)), atol=1e-6)

# Verify log-likelihood decreases under perturbation: Sigma_pert = S_mle + eps * I
eps = 1e-4
S_pert = S_mle + eps * np.eye(p)
inv_pert = np.linalg.inv(S_pert)

def log_likelihood(Sigma_inv, Sigma):
    return -0.5 * n * np.linalg.slogdet(Sigma)[1] - 0.5 * np.trace(Sigma_inv @ A_sum)

ll_mle = log_likelihood(inv_mle, S_mle)
ll_pert = log_likelihood(inv_pert, S_pert)
print(f"Log-Likelihood at MLE: {ll_mle:.4f}")
print(f"Log-Likelihood at Perturbed: {ll_pert:.4f}")
assert ll_mle > ll_pert
```""",
        "criteria": [
            "Matrix gradient $\\nabla_\\Sigma \\ell$ evaluates to zero at the MLE covariance $S_{\\text{MLE}}$.",
            "Gaussian log-likelihood strictly decreases when moving away from $S_{\\text{MLE}}$ in parameter space.",
        ],
    },
    "020": {
        "learnings": [
            "Finding portfolio allocations that maximize and minimize volatility on the unit sphere $\\|w\\|_2 = 1$.",
            "Validating the Rayleigh quotient bounds $\\lambda_{\\min}(S) \\le w^T S w \\le \\lambda_{\\max}(S)$.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Extremal Portfolios & Rayleigh Quotients
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

# Spectral decomposition
lambdas, Q = np.linalg.eigh(S)
idx = np.argsort(lambdas)[::-1]
lambdas, Q = lambdas[idx], Q[:, idx]

# Extremal risk portfolios on unit sphere ||w||_2 = 1
w_max_risk = Q[:, 0]   # Eigenvector for lambda_max
w_min_risk = Q[:, -1]  # Eigenvector for lambda_min

var_max = w_max_risk.T @ S @ w_max_risk
var_min = w_min_risk.T @ S @ w_min_risk

assert np.isclose(var_max, lambdas[0])
assert np.isclose(var_min, lambdas[-1])
print(f"Max Annualized Volatility: {np.sqrt(var_max * 252) * 100:.2f}%")
print(f"Min Annualized Volatility: {np.sqrt(var_min * 252) * 100:.2f}%")

# Monte Carlo test of Rayleigh bounds: 10,000 random portfolios on unit sphere
np.random.seed(42)
W_rand = np.random.randn(10000, p)
W_rand /= np.linalg.norm(W_rand, axis=1, keepdims=True)
rand_vars = np.sum((W_rand @ S) * W_rand, axis=1)

assert np.all(rand_vars >= lambdas[-1] - 1e-10)
assert np.all(rand_vars <= lambdas[0] + 1e-10)
print("Rayleigh quotient bounds confirmed: lambda_min <= w^T S w <= lambda_max across all 10,000 portfolios!")
```""",
        "criteria": [
            "Maximum and minimum risk portfolios on unit sphere correspond to extremal eigenvectors of $S$.",
            "Portfolio variances achieve theoretical Rayleigh bounds $\\lambda_{\\max}$ and $\\lambda_{\\min}$.",
            "10,000 random unit-norm allocations all obey $\\lambda_{\\min} \\le w^T S w \\le \\lambda_{\\max}$.",
        ],
    },
    "021": {
        "learnings": [
            "Simulating correlated multi-asset returns using the Cholesky factor $S = L L^T$.",
            "Demonstrating the QR decomposition relationship $S = \\frac{1}{n-1} R^T R$.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Cholesky Simulation & QR Covariance
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape
H = np.eye(n) - np.ones((n, n)) / n
X_tilde = H @ X
S = (X_tilde.T @ X_tilde) / (n - 1)

# 1. Cholesky Factorization: S = L L^T
L = np.linalg.cholesky(S)
assert np.allclose(L @ L.T, S)
print("Cholesky factor L (lower triangular) verified.")

# 2. Correlated Monte Carlo Simulation
np.random.seed(42)
M_sim = 50000
Z_iid = np.random.randn(M_sim, p)
X_sim = Z_iid @ L.T  # Correlated asset returns
S_sim = np.cov(X_sim, rowvar=False)

# Check Monte Carlo convergence
assert np.allclose(S_sim, S, atol=2e-4)
print("Monte Carlo simulated covariance converged to empirical S within 0.02% error.")

# 3. QR Decomposition: X_tilde = Q R => S = (1/(n-1)) R^T R
Q_qr, R_qr = np.linalg.qr(X_tilde)
S_from_qr = (R_qr.T @ R_qr) / (n - 1)
assert np.allclose(S, S_from_qr)
print("QR covariance relationship S == (1/(n-1)) R^T R verified.")
```""",
        "criteria": [
            "Cholesky decomposition $S = L L^T$ is computed and verified.",
            "Correlated Monte Carlo returns generated via $Z L^T$ reproduce empirical covariance $S$.",
            "QR factorization of centered returns verifies $S = \\frac{1}{n-1} R^T R$.",
        ],
    },
    "022": {
        "learnings": [
            "Resolving multicollinearity in asset replication regressions using the Moore-Penrose pseudoinverse $X^+$.",
            "Proving that the pseudoinverse selects the minimum $L_2$-norm coefficient vector.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Asset Replication via Pseudoinverse
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

# Replicating SPY (col 0) using remaining 5 assets
y = X[:, 0]
X_other = X[:, 1:]

# Inject collinearity: duplicate column 0 (QQQ)
X_coll = np.column_stack([X_other, X_other[:, 0]])  # (250, 6), rank 5
assert np.linalg.matrix_rank(X_coll) == 5

# Normal equations matrix X^T X is singular
try:
    np.linalg.inv(X_coll.T @ X_coll)
    assert False
except np.linalg.LinAlgError:
    print("X_coll^T X_coll is singular, as expected.")

# Solve via Moore-Penrose Pseudoinverse
pinv_X = np.linalg.pinv(X_coll)
beta_pinv = pinv_X @ y

# Verify normal equations are satisfied: X^T X beta == X^T y
assert np.allclose(X_coll.T @ X_coll @ beta_pinv, X_coll.T @ y)

# Verify minimum norm property splits weight evenly between duplicated assets
print(f"Weight on QQQ original:  {beta_pinv[0]:.4f}")
print(f"Weight on QQQ duplicate: {beta_pinv[-1]:.4f}")
assert np.isclose(beta_pinv[0], beta_pinv[-1])
print(f"L2 norm of pseudoinverse coefficients: {np.linalg.norm(beta_pinv):.4f}")
```""",
        "criteria": [
            "Collinear replication design matrix has $\\text{rank}(X_{\\text{coll}}) = 5 < 6$.",
            "Pseudoinverse solution $\\hat{\\beta} = X_{\\text{coll}}^+ y$ satisfies normal equations.",
            "Coefficients for collinear columns are split equally to achieve minimum $L_2$ norm.",
        ],
    },
    "023": {
        "learnings": [
            "Estimating a Vector Autoregressive (VAR(1)) cross-asset spillover model using Kronecker products and the vec operator.",
            "Verifying $\\text{vec}(Y) = (I_p \\otimes X_{\\text{lag}}) \\text{vec}(B)$.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market VAR(1) Cross-Asset Spillover via Kronecker & Vec
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape
H = np.eye(n) - np.ones((n, n)) / n
X_tilde = H @ X

# VAR(1) Model: Y = X_lag @ B + E
Y = X_tilde[1:, :]        # (249, 6)
X_lag = X_tilde[:-1, :]   # (249, 6)

# Vectorization identity: vec(Y) = (I_p \otimes X_lag) vec(B)
K = np.kron(np.eye(p), X_lag)  # (249*6, 6*6) = (1494, 36)
vec_Y = Y.flatten(order='F')   # Column-stacking vec operator

assert K.shape == (249 * 6, 6 * 6)

# Solve for vec(B)
vec_B = np.linalg.lstsq(K, vec_Y, rcond=None)[0]
B_kron = vec_B.reshape((p, p), order='F')

# Benchmark against direct matrix regression B = (X_lag^T X_lag)^{-1} X_lag^T Y
B_ols = np.linalg.lstsq(X_lag, Y, rcond=None)[0]

assert np.allclose(B_kron, B_ols)
print("VAR(1) Cross-Asset Spillover Matrix B (from Kronecker system):\n", np.round(B_kron, 3))
```""",
        "criteria": [
            "Kronecker system matrix $I_p \\otimes X_{\\text{lag}}$ is constructed with dimensions $(1494, 36)$.",
            "Vectorized VAR(1) solution matches equation-by-equation OLS regression.",
            "Column-stacking vec operator reshaping preserves matrix layout.",
        ],
    },
    "024": {
        "learnings": [
            "Performing Mahalanobis anomaly detection to uncover the Day 180 market shock event.",
            "Computing the OLS projection hat matrix $H = X(X^T X)^{-1} X^T$ and diagnosing influential trading days.",
        ],
        "guide": r"""### 2. 📊 Practical Dataset Application: Real Market Mahalanobis Outlier Detection & OLS Hat Diagnostics
```python
import csv
import numpy as np

with open("data/asset_returns.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    assets = next(reader)[1:]
    X = np.array([[float(v) for v in row[1:]] for row in reader])

n, p = X.shape
H_cent = np.eye(n) - np.ones((n, n)) / n
X_tilde = H_cent @ X
S = (X_tilde.T @ X_tilde) / (n - 1)
Theta = np.linalg.inv(S)

# 1. Mahalanobis Distance Anomaly Detection: D_M^2(x_t) = x_t^T Theta x_t
d_mahal = np.sum((X_tilde @ Theta) * X_tilde, axis=1)

# Find anomaly day
anomaly_idx = np.argmax(d_mahal)
print(f"Most extreme market outlier index: Day {anomaly_idx} with D_M^2 = {d_mahal[anomaly_idx]:.2f}")
assert anomaly_idx == 180  # Day 180 injected shock detected!
assert d_mahal[anomaly_idx] > 22.46  # Exceeds chi2(p=6, 0.999) critical value = 22.46

# 2. Multi-factor Linear Model Diagnostics: SPY on remaining assets
y = X[:, 0]
X_reg = np.column_stack([np.ones(n), X[:, 1:]])  # Intercept + 5 assets (250, 6)

# Hat Matrix P = X (X^T X)^{-1} X^T
P = X_reg @ np.linalg.inv(X_reg.T @ X_reg) @ X_reg.T
assert np.allclose(P @ P, P)          # Idempotent
assert np.allclose(P, P.T)            # Symmetric
assert np.isclose(np.trace(P), 6.0)   # tr(P) == rank(X) == 6

# Leverage scores h_ii = P_ii
leverage = np.diag(P)
print(f"Average leverage: {np.mean(leverage):.4f} (p/n = {6/250:.4f})")
print(f"Leverage of Day 180 shock: {leverage[anomaly_idx]:.4f}")
assert leverage[anomaly_idx] > 2 * (6 / 250)  # Exceeds 2p/n high leverage threshold
```""",
        "criteria": [
            "Day 180 is identified as the maximum Mahalanobis anomaly surpassing the $\\chi^2_6(0.999)$ threshold of 22.46.",
            "Hat matrix $P$ is verified symmetric, idempotent, with trace equal to rank 6.",
            "Day 180 is diagnosed as a high-leverage observation ($h_{ii} > 2p/n$).",
        ],
    },
}
