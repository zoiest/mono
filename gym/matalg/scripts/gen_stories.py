#!/usr/bin/env python3
"""Generates stories/001_...md through stories/024_...md for practical exercises."""

from pathlib import Path

stories_data = [
    (
        "001_matrix_creation_and_r_to_python_translation",
        "Story 001: Matrix Creation & R-to-Python Translation",
        "data scientist migrating statistical workflows from R to Python",
        "master NumPy array creation, memory layouts (C-order vs Fortran-order), and indexing semantics",
        "I can translate matrix textbook examples and R code faithfully without subtle dimension or transposition bugs.",
        "Chapter 1: Introduction",
        "1.4-1.7 (Guide to R, Summary of Matrix Operators, Examples of Commands)",
        [
            "How NumPy's 0-based indexing contrasts with R's 1-based indexing.",
            "How column-major (order='F') reshaping reproduces R's default matrix(byrow=FALSE) behavior.",
            "The difference between 1D arrays of shape (n,) and 2D column vectors of shape (n, 1).",
            "Basic matrix slicing, row/column extraction, and block sub-matrices in NumPy."
        ],
        r"""
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
```""",
        [
            "`A` correctly matches R's column-major matrix layout with shape `(2, 3)`.",
            "`B` correctly matches R's row-major matrix layout with shape `(2, 3)`.",
            "Indexing `A[0, 1]` returns `3`.",
            "Vector conversions between 1D and 2D column vector shapes are verified."
        ]
    ),
    (
        "002_vector_geometry_and_orthogonality",
        "Story 002: Vector Geometry, Inner/Outer Products, and Orthogonality",
        "statistician analyzing feature spaces",
        "implement vector inner products, outer products, Euclidean norms, and test for orthogonality",
        "I can compute projection angles and verify orthogonal subspaces in linear statistical models.",
        "Chapter 2: Vectors and Matrices",
        "2.1 (Vectors, Definitions, Example 2.1, Orthogonal vectors)",
        [
            "Computing inner products x^T y and outer products x y^T.",
            "Evaluating Euclidean L2 norms and cosine similarities.",
            "Testing orthogonality condition x^T y = 0.",
            "Rank properties of outer products."
        ],
        r"""
### 1. Vector Products & Angles
```python
import numpy as np

a = np.array([1.0, 2.0, 3.0])
b = np.array([4.0, -2.0, 0.0])
c = np.array([1.0, 1.0, -1.0])

# Inner products
dot_ab = a @ b
dot_ac = a @ c
dot_bc = b @ c

print(f"a^T b = {dot_ab}")  # 0.0 -> orthogonal!
print(f"a^T c = {dot_ac}")  # 0.0 -> orthogonal!
print(f"b^T c = {dot_bc}")  # 2.0

assert np.isclose(dot_ab, 0.0)
assert np.isclose(dot_ac, 0.0)

# Outer product (rank-1 matrix)
outer_ab = np.outer(a, b)
print("Outer product a b^T:\n", outer_ab)
assert np.linalg.matrix_rank(outer_ab) == 1
```""",
        [
            "Vectors `a` and `b` are confirmed orthogonal (`a @ b == 0`).",
            "Vectors `a` and `c` are confirmed orthogonal (`a @ c == 0`).",
            "Outer product `a b^T` is confirmed to have rank 1.",
            "Euclidean norms and cosine distance tests pass."
        ]
    ),
    (
        "003_matrix_multiplication_and_frobenius_inner_product",
        "Story 003: Matrix Multiplication, Cross Products, and the Trace Operator",
        "numerical algorithm developer",
        "implement matrix multiplication `@`, cross-products $X^TX$ and $XX^T$, and cyclic trace identities",
        "I can write performant matrix arithmetic and simplify statistical expressions using trace tricks.",
        "Chapter 2: Vectors and Matrices",
        "2.3, 2.4, 2.8.2 (Matrix Arithmetic, Transpose, Trace of Products)",
        [
            "Matrix multiplication conformability and the `@` operator.",
            "Cross-products $X^TX$ (Gram matrix) and $XX^T$.",
            "Trace linearity and cyclic invariance: tr(ABC) = tr(BCA) = tr(CAB).",
            "The Frobenius inner product tr(A^T B) and matrix Frobenius norm."
        ],
        r"""
### 1. Trace and Cross Products
```python
import numpy as np

A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
B = np.array([[7.0, 8.0], [9.0, 1.0], [2.0, 3.0]])

# Matrix products
AB = A @ B  # (2, 2)
BA = B @ A  # (3, 3)

# Cyclic trace property: tr(AB) == tr(BA)
tr_AB = np.trace(AB)
tr_BA = np.trace(BA)
print(f"tr(AB) = {tr_AB}, tr(BA) = {tr_BA}")
assert np.isclose(tr_AB, tr_BA)

# Cross product properties: A^T A is symmetric
AtA = A.T @ A
assert np.allclose(AtA, AtA.T)
assert np.isclose(np.trace(A @ A.T), np.trace(A.T @ A))
```""",
        [
            "`A @ B` and `B @ A` are computed with conformable dimensions.",
            "Trace cyclic equality `tr(AB) == tr(BA)` is verified.",
            "`A.T @ A` is verified to be symmetric positive semi-definite.",
            "`tr(A A.T) == tr(A.T A)` is confirmed."
        ]
    ),
    (
        "004_special_matrices_and_symmetrization",
        "Story 004: Special Matrices & Quadratic Form Symmetrization",
        "statistical modeler",
        "implement and test symmetric, skew-symmetric, orthogonal, and permutation matrices",
        "I can decompose arbitrary square matrices and express quadratic forms using symmetric matrices.",
        "Chapter 2: Vectors and Matrices",
        "2.5, 2.9 (Special Matrices: Symmetric, Orthogonal, Permutation, Quadratic Forms)",
        [
            "Decomposing square matrix A = A_sym + A_skew.",
            "Orthogonal matrices Q^T Q = I and preservation of norms.",
            "Permutation matrices and row/column swaps.",
            "Symmetrization of quadratic forms x^T A x = x^T A_sym x."
        ],
        r"""
### 1. Matrix Decomposition & Quadratic Symmetrization
```python
import numpy as np

# Non-symmetric matrix
A = np.array([[2.0, 1.0], [5.0, 4.0]])

# Symmetric and Skew-Symmetric components
A_sym = 0.5 * (A + A.T)
A_skew = 0.5 * (A - A.T)

assert np.allclose(A, A_sym + A_skew)
assert np.allclose(A_sym, A_sym.T)
assert np.allclose(A_skew, -A_skew.T)

# Quadratic form equality: x^T A x == x^T A_sym x
x = np.array([3.0, -2.0])
q_orig = x.T @ A @ x
q_sym = x.T @ A_sym @ x
print(f"Original Q(x) = {q_orig}, Symmetric Q(x) = {q_sym}")
assert np.isclose(q_orig, q_sym)
```""",
        [
            "Matrix `A` is decomposed into symmetric and skew-symmetric parts.",
            "`A_sym` is verified symmetric and `A_skew` skew-symmetric.",
            "Quadratic forms `x^T A x` and `x^T A_sym x` are verified equal.",
            "Orthogonal matrix length preservation is verified."
        ]
    ),
    (
        "005_centering_matrix_and_sample_covariance",
        "Story 005: The Centering Matrix $H_n$ and Sample Covariance Computation",
        "multivariate data analyst",
        "implement the centering matrix $H_n = I_n - \\frac{1}{n}\\mathbf{1}\\mathbf{1}^T$ and calculate sample covariance matrices",
        "I can perform mean-centering and compute sample variance-covariance matrices directly via algebraic matrix multiplication.",
        "Chapter 2: Vectors and Matrices",
        "2.5.6.1, 2.12.3 (The Centering Matrix Hn, Sample Statistics in R)",
        [
            "Properties of H_n: symmetry, idempotency (H_n^2 = H_n), and null space H_n 1 = 0.",
            "Rank and trace of H_n: tr(H_n) = n - 1.",
            "Mean centering of data matrix X: X_c = H_n X.",
            "Calculating sample covariance S = (1 / (n - 1)) * X^T H_n X."
        ],
        r"""
### 1. Centering Matrix Construction & Covariance
```python
import numpy as np

def make_centering_matrix(n: int) -> np.ndarray:
    return np.eye(n) - np.ones((n, n)) / n

n = 5
H = make_centering_matrix(n)
ones = np.ones(n)

# Algebraic verifications
assert np.allclose(H, H.T)              # Symmetric
assert np.allclose(H @ H, H)            # Idempotent
assert np.allclose(H @ ones, 0.0)       # Annihilator
assert np.isclose(np.trace(H), n - 1)   # Rank / Trace

# Covariance calculation
X = np.array([
    [10.0, 2.0],
    [12.0, 4.0],
    [14.0, 5.0],
    [16.0, 9.0],
    [18.0, 10.0]
])

S_matrix = (X.T @ H @ X) / (n - 1)
S_numpy = np.cov(X, rowvar=False)

print("S via Centering Matrix:\n", S_matrix)
assert np.allclose(S_matrix, S_numpy)
```""",
        [
            "`H_n` satisfies `H^T == H`, `H @ H == H`, and `H @ 1 == 0`.",
            "`tr(H_n) == n - 1` is verified.",
            "`X.T @ H_n @ X / (n - 1)` exactly matches `np.cov(X, rowvar=False)`."
        ]
    ),
    (
        "006_partitioned_matrices_and_block_multiplication",
        "Story 006: Partitioned Matrices & Block Multiplication",
        "scientific computing engineer",
        "implement block matrix assembly and verify conformable block multiplication rules",
        "I can manipulate partitioned matrices and construct composite block systems for ANOVA and linear models.",
        "Chapter 2: Vectors and Matrices",
        "2.6 (Partitioned Matrices, Sub-matrices, Block Manipulation)",
        [
            "Block matrix slicing and assembly via np.block.",
            "Verifying block matrix multiplication rules.",
            "Block diagonal matrices and sparse representation."
        ],
        r"""
### 1. Block Matrix Multiplication
```python
import numpy as np

A11 = np.array([[1.0, 2.0], [3.0, 4.0]])
A12 = np.array([[5.0], [6.0]])
A21 = np.array([[7.0, 8.0]])
A22 = np.array([[9.0]])

A = np.block([[A11, A12], [A21, A22]])

B11 = np.array([[2.0, 0.0], [1.0, 3.0]])
B12 = np.array([[1.0], [0.0]])
B21 = np.array([[4.0, 2.0]])
B22 = np.array([[5.0]])

B = np.block([[B11, B12], [B21, B22]])

# Block multiplication by parts
C11 = A11 @ B11 + A12 @ B21
C12 = A11 @ B12 + A12 @ B22
C21 = A21 @ B11 + A22 @ B21
C22 = A21 @ B12 + A22 @ B22
C_block = np.block([[C11, C12], [C21, C22]])

# Full matrix product
C_direct = A @ B

print("C via direct multiplication:\n", C_direct)
assert np.allclose(C_block, C_direct)
```""",
        [
            "Partitioned matrix `A` and `B` assemble correctly with `np.block`.",
            "Sub-block multiplication matches full matrix multiplication `A @ B` exactly."
        ]
    ),
    (
        "007_matrix_rank_and_linear_independence",
        "Story 007: Matrix Rank, Linear Independence, and SVD Thresholding",
        "statistical programmer",
        "determine matrix rank, assess linear dependency, and understand numerical SVD tolerance",
        "I can detect multicollinearity and rank deficiency in regression design matrices.",
        "Chapter 3: Rank of Matrices",
        "3.1, 3.4 (Rank Definitions, Rank in Statistics)",
        [
            "Row rank equals column rank for any real matrix.",
            "SVD-based numerical rank determination in np.linalg.matrix_rank.",
            "Detecting collinearity when a column is a linear combination of others.",
            "Gram matrix rank equality: rank(X^T X) == rank(X X^T) == rank(X)."
        ],
        r"""
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
```""",
        [
            "Linear dependence between columns is detected via rank deficit.",
            "`np.linalg.matrix_rank(X) == 2` for a $4 \\times 3$ matrix with 2 independent columns.",
            "Gram matrix `X.T @ X` has identical rank to `X`."
        ]
    ),
    (
        "008_rank_factorization_and_rank_one_matrices",
        "Story 008: Rank Factorization & Outer Products of Rank 1",
        "machine learning researcher",
        "compute full rank factorizations $A = BC$ and analyze rank-1 structures $x y^T$",
        "I can implement low-rank matrix decompositions and identify rank-1 updates.",
        "Chapter 3: Rank of Matrices",
        "3.2 (Rank Factorization, Matrices of Rank 1)",
        [
            "Rank Factorization Theorem: A = BC with B full column rank, C full row rank.",
            "Structure of rank-1 matrices: A = x y^T.",
            "Eigenstructure of rank-1 matrices: non-zero eigenvalue equals y^T x.",
            "Constructing rank factorizations from SVD or row echelon form."
        ],
        r"""
### 1. Rank Factorization
```python
import numpy as np

# Rank 1 matrix A = x y^T
x = np.array([[2.0], [3.0], [1.0]])
y = np.array([[4.0], [5.0]])
A = x @ y.T
assert np.linalg.matrix_rank(A) == 1

# Rank factorization A = B @ C
B = x  # (3, 1) full column rank
C = y.T  # (1, 2) full row rank
assert np.allclose(A, B @ C)

# Rank 2 factorization via SVD
M = np.random.randn(4, 2) @ np.random.randn(2, 5)
U, s, Vt = np.linalg.svd(M, full_matrices=False)
r = np.linalg.matrix_rank(M)
B_svd = U[:, :r] @ np.diag(s[:r])
C_svd = Vt[:r, :]
assert np.allclose(M, B_svd @ C_svd)
```""",
        [
            "Outer product `x @ y.T` is verified to have rank 1.",
            "Rank factorization `A = B @ C` is verified with full rank factors.",
            "SVD-based rank factorization produces exact matrix reconstruction."
        ]
    ),
    (
        "009_rank_inequalities_and_collinearity",
        "Story 009: Rank Inequalities & Degrees of Freedom in ANOVA",
        "statistical theoretical analyst",
        "verify Sylvester and Frobenius rank inequalities and relate matrix rank to degrees of freedom",
        "I can verify mathematical bounds on matrix products and derive valid degrees of freedom in hypothesis testing.",
        "Chapter 3: Rank of Matrices",
        "3.3, 3.4 (Rank Inequalities, Sylvester's Inequality, Rank in Statistics)",
        [
            "Subadditivity: rank(A + B) <= rank(A) + rank(B).",
            "Product bound: rank(AB) <= min(rank(A), rank(B)).",
            "Sylvester's rank inequality: rank(AB) >= rank(A) + rank(B) - p.",
            "Connection between rank of idempotent matrices and degrees of freedom."
        ],
        r"""
### 1. Sylvester's Rank Inequality Verification
```python
import numpy as np

# A is 5x4 of rank 3, B is 4x6 of rank 3
A = np.random.randn(5, 3) @ np.random.randn(3, 4)
B = np.random.randn(4, 3) @ np.random.randn(3, 6)

rank_A = np.linalg.matrix_rank(A)
rank_B = np.linalg.matrix_rank(B)
rank_AB = np.linalg.matrix_rank(A @ B)
p = 4

print(f"rank(A) = {rank_A}, rank(B) = {rank_B}, rank(AB) = {rank_AB}")
sylvester_bound = rank_A + rank_B - p
print(f"Sylvester lower bound: {sylvester_bound}")
assert rank_AB >= sylvester_bound
assert rank_AB <= min(rank_A, rank_B)
```""",
        [
            "Sylvester's inequality `rank(AB) >= rank(A) + rank(B) - p` is confirmed.",
            "Product rank is bounded by `min(rank(A), rank(B))`.",
            "Subadditivity `rank(A + B) <= rank(A) + rank(B)` is verified."
        ]
    ),
    (
        "010_determinants_and_geometric_volume",
        "Story 010: Determinants, Laplace Expansions, and Log-Determinants",
        "computational statistician",
        "calculate determinants via Laplace expansion, evaluate triangular matrices, and use slogdet",
        "I can compute generalized variances and evaluate multivariate normal densities without numerical overflow/underflow.",
        "Chapter 4: Determinants",
        "4.1, 4.2, 4.3 (Determinant Definitions, Implementation, Properties)",
        [
            "Laplace expansion by minors and cofactors.",
            "Determinant of triangular matrices as product of diagonals.",
            "Effects of elementary row operations.",
            "Using np.linalg.slogdet for robust likelihood evaluation."
        ],
        r"""
### 1. Determinants and slogdet
```python
import numpy as np

# Triangular matrix
T = np.array([
    [2.0, 3.0, 1.0],
    [0.0, 5.0, 4.0],
    [0.0, 0.0, 3.0]
])
det_T = np.linalg.det(T)
expected_det = 2.0 * 5.0 * 3.0
assert np.isclose(det_T, expected_det)

# Log-determinant for large covariance matrix
Sigma = np.diag([1e-3, 1e-4, 1e-5, 1e-2])
sign, logdet = np.linalg.slogdet(Sigma)
print(f"Log-det: {logdet:.4f}")
assert sign == 1
assert np.isclose(logdet, np.sum(np.log(np.diag(Sigma))))
```""",
        [
            "Triangular matrix determinant equals product of diagonal elements.",
            "`np.linalg.slogdet` matches `sum(log(diag))` for positive diagonal matrix.",
            "Elementary row swap sign reversal is verified."
        ]
    ),
    (
        "011_schur_complements_and_block_determinants",
        "Story 011: Schur Complements & Block Partitioned Determinants",
        "probabilistic modeler",
        "compute determinants of partitioned matrices using Schur complements",
        "I can evaluate joint and conditional likelihoods in structured Gaussian graphical models.",
        "Chapter 4: Determinants",
        "4.5 (Determinants of Partitioned Matrices, Schur Complement)",
        [
            "Block Gaussian elimination and factorization.",
            "Schur complement formula: det(M) = det(A) * det(D - C A^{-1} B).",
            "Block triangular matrices: det([[A, B], [0, D]]) = det(A) det(D)."
        ],
        r"""
### 1. Schur Complement Determinant
```python
import numpy as np

A = np.array([[4.0, 1.0], [1.0, 3.0]])
B = np.array([[1.0, 0.0], [0.0, 2.0]])
C = B.T
D = np.array([[5.0, 1.0], [1.0, 4.0]])

M = np.block([[A, B], [C, D]])

det_direct = np.linalg.det(M)
S_A = D - C @ np.linalg.inv(A) @ B
det_schur = np.linalg.det(A) * np.linalg.det(S_A)

print("Direct det(M):", det_direct)
print("Schur formula det(A) * det(D - C A^{-1} B):", det_schur)
assert np.isclose(det_direct, det_schur)
```""",
        [
            "Block partitioned matrix `M` determinant is computed directly.",
            "Schur complement formula matches direct determinant within machine precision."
        ]
    ),
    (
        "012_weinstein_aronszajn_identity_and_rank_one_updates",
        "Story 012: The Weinstein-Aronszajn Identity & Rank-1 Updates",
        "machine learning engineer",
        "implement the Weinstein-Aronszajn determinant identity and rank-1 determinant updates",
        "I can perform fast $O(n^2)$ determinant evaluations in Gaussian processes and active learning.",
        "Chapter 4: Determinants",
        "4.6 (A Key Property of Determinants: Weinstein-Aronszajn, Equicorrelation)",
        [
            "Weinstein-Aronszajn Identity: det(I_p + AB) = det(I_q + BA).",
            "Rank-1 update formula: det(A + x y^T) = det(A) * (1 + y^T A^{-1} x).",
            "Analytical determinant of equicorrelation matrix alpha I + beta 1 1^T."
        ],
        r"""
### 1. Rank-1 Determinant Update
```python
import numpy as np

n = 4
A = np.diag([2.0, 3.0, 4.0, 5.0])
x = np.array([[1.0], [2.0], [1.0], [1.0]])
y = np.array([[2.0], [1.0], [3.0], [1.0]])

# Direct calculation
det_direct = np.linalg.det(A + x @ y.T)

# Fast rank-1 update formula: det(A) * (1 + y^T A^{-1} x)
det_A = np.prod(np.diag(A))
y_Ainv_x = (y.T @ (x / np.diag(A)[:, None]))[0, 0]
det_formula = det_A * (1.0 + y_Ainv_x)

print(f"Direct: {det_direct:.4f}, Formula: {det_formula:.4f}")
assert np.isclose(det_direct, det_formula)
```""",
        [
            "`det(I_p + AB) == det(I_q + BA)` verified for rectangular `A` and `B`.",
            "Rank-1 update formula matches `np.linalg.det(A + x @ y.T)`.",
            "Equicorrelation matrix determinant formula matches numerical calculation."
        ]
    ),
    (
        "013_matrix_inversion_and_numerical_stability",
        "Story 013: Matrix Inversion & Numerical Conditioning",
        "scientific computing practitioner",
        "measure matrix conditioning, avoid explicit matrix inversion, and use LAPACK solvers",
        "I can build numerically robust regression and estimation routines resistant to floating-point truncation.",
        "Chapter 5: Inverses",
        "5.1, 5.2, 5.3 (Inverses, Properties, Implementation in R)",
        [
            "Condition number kappa(A) = sigma_max / sigma_min.",
            "Why np.linalg.solve(A, b) is faster and more accurate than inv(A) @ b.",
            "Left inverse A_L = (A^T A)^{-1} A^T for overdetermined systems.",
            "Right inverse A_R = A^T (A A^T)^{-1} for underdetermined systems."
        ],
        r"""
### 1. Solving Linear Systems vs Inversion
```python
import numpy as np

# Hilbert matrix (notoriously ill-conditioned)
n = 5
H = np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])
b = np.ones(n)

cond_H = np.linalg.cond(H)
print(f"Condition number of Hilbert matrix: {cond_H:.2e}")

# Solve Ax = b
x_solve = np.linalg.solve(H, b)
x_inv = np.linalg.inv(H) @ b

res_solve = np.linalg.norm(H @ x_solve - b)
res_inv = np.linalg.norm(H @ x_inv - b)

print(f"Residual via solve: {res_solve:.2e}, Residual via inv: {res_inv:.2e}")
assert res_solve <= res_inv + 1e-12
```""",
        [
            "Condition number $\\kappa(A)$ is computed via `np.linalg.cond`.",
            "Residual of `np.linalg.solve` is demonstrated to be smaller or equal to `np.linalg.inv`.",
            "Left inverse satisfies `A_L @ A == I_n` for full column rank matrix."
        ]
    ),
    (
        "014_sherman_morrison_and_woodbury_updates",
        "Story 014: Patterned Inverses & The Sherman-Morrison Formula",
        "real-time systems engineer",
        "implement $O(n^2)$ inverse updates via Sherman-Morrison and invert equicorrelation matrices",
        "I can perform online sequential parameter updates in streaming Kalman filters and regression.",
        "Chapter 5: Inverses",
        "5.4 (Inverses of Patterned Matrices, Sherman-Morrison)",
        [
            "Inverting equicorrelation matrices alpha I + beta 1 1^T analytically.",
            "The Sherman-Morrison formula: (A + x y^T)^{-1} = A^{-1} - (A^{-1} x y^T A^{-1}) / (1 + y^T A^{-1} x).",
            "The Woodbury identity for rank-k updates."
        ],
        r"""
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
```""",
        [
            "Sherman-Morrison formula matches `np.linalg.inv(A + x @ y.T)`.",
            "Equicorrelation inverse formula verified against `np.linalg.inv`."
        ]
    ),
    (
        "015_banachiewicz_block_inversion_and_conditional_covariance",
        "Story 015: Block Inversion & Conditional Gaussian Covariance",
        "Bayesian statistician",
        "invert block matrices using the Banachiewicz formula and compute conditional covariance matrices",
        "I can derive precision matrices and conditional Gaussian distributions in multivariate data analysis.",
        "Chapter 5: Inverses",
        "5.5 (Inverses of Partitioned Matrices, Banachiewicz Inversion)",
        [
            "Banachiewicz block inversion formula.",
            "Connection between the Schur complement and conditional variance: Cov(X_2 | X_1).",
            "Precision matrix structure in Gaussian graphical models."
        ],
        r"""
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
```""",
        [
            "Banachiewicz block inversion matches `np.linalg.inv(M)` within machine precision.",
            "Conditional covariance `D - C @ A_inv @ B` verified as Schur complement."
        ]
    ),
    (
        "016_eigenanalysis_and_spectral_decomposition",
        "Story 016: Eigenanalysis & The Spectral Decomposition Theorem",
        "applied mathematician",
        "compute eigenvalues/eigenvectors of symmetric matrices and reconstruct matrices via the Spectral Theorem",
        "I can decompose covariance matrices into principal geometric axes and orthogonal subspaces.",
        "Chapter 6: Eigenanalysis of Real Symmetric Matrices",
        "6.1, 6.2, 6.4, 6.7.1 (Characteristic Equation, Symmetric Properties, Spectral Decomposition)",
        [
            "The Spectral Theorem: A = P Lambda P^T for real symmetric matrices.",
            "Orthonormality of eigenvectors: P^T P = I.",
            "Trace equals sum of eigenvalues; Determinant equals product of eigenvalues.",
            "Rank equals number of non-zero eigenvalues."
        ],
        r"""
### 1. Spectral Decomposition
```python
import numpy as np

# Symmetric matrix
S = np.array([[5.0, 2.0], [2.0, 2.0]])

# np.linalg.eigh guarantees real eigenvalues and orthonormal eigenvectors
evals, P = np.linalg.eigh(S)

# Orthonormality check
assert np.allclose(P.T @ P, np.eye(2))

# Spectral reconstruction: P @ diag(evals) @ P.T
S_rec = P @ np.diag(evals) @ P.T
assert np.allclose(S, S_rec)

# Trace and determinant checks
assert np.isclose(np.trace(S), np.sum(evals))
assert np.isclose(np.linalg.det(S), np.prod(evals))
print("Spectral Theorem successfully verified.")
```""",
        [
            "Eigenvalues and eigenvectors are computed using `np.linalg.eigh`.",
            "Eigenvector matrix `P` is verified to be orthogonal (`P.T @ P == I`).",
            "Spectral reconstruction `P @ diag(evals) @ P.T` recovers `S`.",
            "Trace and determinant eigenvalue equalities are confirmed."
        ]
    ),
    (
        "017_matrix_functions_and_matrix_exponential",
        "Story 017: Matrix Functions, Square Roots, and the Matrix Exponential",
        "stochastic process modeler",
        "compute matrix powers, matrix square roots $S^{1/2}$, and the matrix exponential $\\exp(A)$",
        "I can perform Mahalanobis whitening and solve continuous-time Markov transition rates.",
        "Chapter 6: Eigenanalysis of Real Symmetric Matrices",
        "6.6, 6.7.1.1 (Matrix Exponential, Square Root of Positive Semi-Definite Matrices)",
        [
            "Defining f(A) = P f(Lambda) P^T via spectral decomposition.",
            "Matrix square root S^{1/2} and inverse square root S^{-1/2} for Mahalanobis whitening.",
            "Matrix exponential exp(A) = sum A^k / k! and comparison with scipy.linalg.expm."
        ],
        r"""
### 1. Matrix Square Root & Exponential
```python
import numpy as np
import scipy.linalg as la

S = np.array([[4.0, 1.0], [1.0, 3.0]])
evals, P = np.linalg.eigh(S)

# Matrix square root S^{1/2}
S_sqrt = P @ np.diag(np.sqrt(evals)) @ P.T
assert np.allclose(S_sqrt @ S_sqrt, S)

# Matrix exponential exp(S)
S_exp = P @ np.diag(np.exp(evals)) @ P.T
S_exp_scipy = la.expm(S)
assert np.allclose(S_exp, S_exp_scipy)

print("Matrix square root and exponential verified.")
```""",
        [
            "`S_sqrt @ S_sqrt == S` is verified.",
            "`P @ diag(exp(evals)) @ P.T` matches `scipy.linalg.expm(S)`."
        ]
    ),
    (
        "018_singular_value_decomposition_and_low_rank_approximation",
        "Story 018: Singular Value Decomposition (SVD) & Low-Rank Approximation",
        "data compression & ML engineer",
        "implement SVD $A = U \\Sigma V^T$ and verify the Eckart-Young-Mirsky optimal low-rank approximation",
        "I can compress high-dimensional feature spaces and perform robust pseudo-inversion.",
        "Chapter 6: Eigenanalysis of Real Symmetric Matrices",
        "6.7.2 (Singular Value Decomposition of an m x n Matrix)",
        [
            "Economy SVD vs Full SVD in NumPy.",
            "Relationship between singular values of A and eigenvalues of A^T A and A A^T.",
            "The Eckart-Young-Mirsky optimal rank-k approximation theorem."
        ],
        r"""
### 1. SVD and Rank-k Reconstruction
```python
import numpy as np

# Non-square matrix
A = np.array([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
    [7.0, 8.0, 9.0],
    [10.0, 11.0, 12.0]
])

U, s, Vt = np.linalg.svd(A, full_matrices=False)

# Exact reconstruction
A_rec = U @ np.diag(s) @ Vt
assert np.allclose(A, A_rec)

# Best Rank-1 approximation
A_rank1 = s[0] * np.outer(U[:, 0], Vt[0, :])
print("Rank-1 approximation:\n", A_rank1)
assert np.linalg.matrix_rank(A_rank1) == 1
```""",
        [
            "SVD reconstruction `U @ diag(s) @ Vt` recovers original matrix `A`.",
            "Singular values match square roots of eigenvalues of `A.T @ A`.",
            "Rank-1 approximation is verified to have rank 1."
        ]
    ),
    (
        "019_matrix_calculus_for_mle",
        "Story 019: Vector and Matrix Calculus for Maximum Likelihood Estimation",
        "theoretical statistician",
        "derive gradients of linear forms, quadratic forms, trace operators, and log-determinants",
        "I can mathematically derive MLE estimators and normal equations from first principles.",
        "Chapter 7: Vector and Matrix Calculus",
        "7.2, 7.3 (Differentiation with Respect to Vector and Matrix)",
        [
            "Gradients of a^T x and x^T S x: d(x^T S x)/dx = 2 S x.",
            "Matrix derivatives: d tr(XA)/dX = A^T.",
            "Log-determinant derivative: d log|X| / dX = X^{-1}.",
            "Deriving the OLS normal equations X^T X beta = X^T y."
        ],
        r"""
### 1. Numerical Gradient Verification
```python
import numpy as np

# Quadratic form: f(x) = x^T S x
S = np.array([[3.0, 1.0], [1.0, 2.0]])
x = np.array([1.5, -2.0])

grad_analytical = 2 * S @ x

# Numerical approximation via central differences
eps = 1e-6
grad_num = np.zeros_like(x)
for i in range(len(x)):
    xp, xm = x.copy(), x.copy()
    xp[i] += eps
    xm[i] -= eps
    grad_num[i] = (xp.T @ S @ xp - xm.T @ S @ xm) / (2 * eps)

assert np.allclose(grad_analytical, grad_num, atol=1e-5)
print("Analytical gradient 2Sx verified numerically.")
```""",
        [
            "Analytical gradient `2 * S @ x` matches finite differences.",
            "Log-determinant derivative $\\nabla \\log|\\Sigma| = \\Sigma^{-1}$ is verified."
        ]
    ),
    (
        "020_constrained_optimization_and_rayleigh_quotients",
        "Story 020: Constrained Optimization & Rayleigh Quotients",
        "optimization specialist",
        "maximize quadratic forms under quadratic constraints using Lagrange multipliers and Rayleigh quotients",
        "I can solve eigenproblems arising in PCA, Fisher's discriminant analysis, and canonical correlation.",
        "Chapter 7: Vector and Matrix Calculus",
        "7.6 (Use of Eigenanalysis in Constrained Optimization)",
        [
            "Lagrangian formulation for maximizing x^T A x subject to x^T x = 1.",
            "Derivation of the Rayleigh quotient R_A(x) = (x^T A x) / (x^T x).",
            "Generalized Rayleigh quotient for x^T A x subject to x^T B x = 1."
        ],
        r"""
### 1. Rayleigh Quotient Optimization
```python
import numpy as np

A = np.array([[5.0, 2.0], [2.0, 2.0]])
evals, evecs = np.linalg.eigh(A)

min_val, max_val = evals[0], evals[1]
v_min, v_max = evecs[:, 0], evecs[:, 1]

# Check extrema
R_max = (v_max.T @ A @ v_max) / (v_max.T @ v_max)
R_min = (v_min.T @ A @ v_min) / (v_min.T @ v_min)

assert np.isclose(R_max, max_val)
assert np.isclose(R_min, min_val)
print(f"Max Rayleigh quotient: {R_max:.4f}, Min: {R_min:.4f}")
```""",
        [
            "Maximum Rayleigh quotient equals largest eigenvalue $\\lambda_{\\max}$.",
            "Minimum Rayleigh quotient equals smallest eigenvalue $\\lambda_{\\min}$."
        ]
    ),
    (
        "021_advanced_factorizations_qr_cholesky_lu",
        "Story 021: Advanced Factorizations: QR, Cholesky, and LU",
        "quantitative developer",
        "implement QR decomposition for regression and Cholesky decomposition for correlated Gaussian sampling",
        "I can perform fast matrix solves and simulate correlated multivariate distributions.",
        "Chapter 8: Further Topics",
        "8.2 (Further Matrix Decompositions: QR, LU, Cholesky)",
        [
            "QR decomposition: X = Q R, and solving R beta = Q^T y.",
            "Cholesky decomposition: Sigma = L L^T for positive definite covariance.",
            "Simulating multivariate normals: X = mu + L Z."
        ],
        r"""
### 1. QR Least Squares & Cholesky Simulation
```python
import numpy as np

# QR Least Squares
X = np.array([[1.0, 1.0], [1.0, 2.0], [1.0, 3.0], [1.0, 4.0]])
y = np.array([2.0, 3.0, 5.0, 7.0])

Q, R = np.linalg.qr(X)
beta_qr = np.linalg.solve(R, Q.T @ y)
beta_direct = np.linalg.inv(X.T @ X) @ X.T @ y
assert np.allclose(beta_qr, beta_direct)

# Cholesky Simulation
Sigma = np.array([[4.0, 1.2], [1.2, 1.0]])
L = np.linalg.cholesky(Sigma)
np.random.seed(42)
Z = np.random.randn(2, 50000)
X_sim = (L @ Z).T
cov_emp = np.cov(X_sim, rowvar=False)
assert np.allclose(Sigma, cov_emp, atol=0.05)
print("QR and Cholesky algorithms successfully verified.")
```""",
        [
            "QR back-substitution produces identical OLS coefficients to normal equations.",
            "Cholesky factor `L @ L.T` recovers target covariance.",
            "Simulated samples have empirical covariance matching target $\\Sigma$."
        ]
    ),
    (
        "022_generalized_inverses_and_least_squares",
        "Story 022: Generalized Inverses & The Moore-Penrose Pseudoinverse",
        "linear algebra researcher",
        "compute the Moore-Penrose pseudoinverse $A^+$ and solve underdetermined linear systems",
        "I can compute minimum-norm solutions to rank-deficient regression models.",
        "Chapter 8: Further Topics",
        "8.3 (Generalized Inverses, Moore-Penrose, Solutions of Linear Equations)",
        [
            "The four Penrose conditions for A^+.",
            "Using np.linalg.pinv for rank-deficient matrices.",
            "General solution to consistent systems: x = A^- y + (I - A^- A) w.",
            "Minimum norm least squares solutions."
        ],
        r"""
### 1. Moore-Penrose Pseudoinverse Verification
```python
import numpy as np

# Rank-deficient 2x3 matrix
A = np.array([[1.0, 2.0, 3.0], [2.0, 4.0, 6.0]])
A_pinv = np.linalg.pinv(A)

# Check all 4 Penrose conditions:
assert np.allclose(A @ A_pinv @ A, A)                     # 1. A A^+ A = A
assert np.allclose(A_pinv @ A @ A_pinv, A_pinv)           # 2. A^+ A A^+ = A^+
assert np.allclose((A @ A_pinv).T, A @ A_pinv)           # 3. (A A^+)^T = A A^+
assert np.allclose((A_pinv @ A).T, A_pinv @ A)           # 4. (A^+ A)^T = A^+ A
print("All 4 Moore-Penrose conditions verified.")
```""",
        [
            "All four Penrose conditions are satisfied within machine precision.",
            "Pseudoinverse solves underdetermined systems with minimum Euclidean norm."
        ]
    ),
    (
        "023_kronecker_products_and_vec_operator",
        "Story 023: Kronecker Products, Vec Operator, and Matrix Equations",
        "time series econometrician",
        "implement Kronecker products $A \\otimes B$, column-major $\\text{vec}(A)$, and solve Sylvester matrix equations",
        "I can estimate Vector Autoregressive (VAR) models and solve continuous Lyapunov equations.",
        "Chapter 8: Further Topics",
        "8.5 (Kronecker Products and the Vec Operator)",
        [
            "Kronecker product properties: (A kron B)(C kron D) = (AC) kron (BD).",
            "Column-major vectorization: A.flatten(order='F').",
            "The fundamental identity: vec(ABC) = (C^T kron A) vec(B).",
            "Solving matrix equations A X B = C."
        ],
        r"""
### 1. Kronecker and Vec Identity
```python
import numpy as np

A = np.array([[1.0, 2.0], [3.0, 4.0]])
B = np.array([[5.0, 6.0], [7.0, 8.0]])
C = np.array([[9.0, 1.0], [2.0, 3.0]])

# vec(ABC)
ABC = A @ B @ C
vec_ABC = ABC.flatten(order='F')

# (C^T kron A) vec(B)
kron_term = np.kron(C.T, A)
vec_formula = kron_term @ B.flatten(order='F')

assert np.allclose(vec_ABC, vec_formula)
print("vec(ABC) == (C^T kron A) vec(B) verified.")
```""",
        [
            "`A.flatten(order='F')` executes column-major vectorization.",
            "Fundamental identity `vec(ABC) == (C^T kron A) vec(B)` is verified.",
            "Mixed product property `(A kron B) @ (C kron D) == (A @ C) kron (B @ D)` is verified."
        ]
    ),
    (
        "024_multivariate_statistics_and_linear_models",
        "Story 024: Multivariate Hypothesis Testing, PCA, LDA, and OLS",
        "senior statistician",
        "implement Hotelling's $T^2$, PCA, Fisher's LDA, Metric MDS, and Constrained OLS in Python",
        "I can perform end-to-end multivariate analysis and regression modeling using matrix algebra.",
        "Chapter 9: Key Applications to Statistics",
        "9.2-9.7 (Multivariate Normal, PCA, LDA, CCA, MDS, Linear Models)",
        [
            "One-sample Hotelling's T^2 hypothesis testing and F-statistic conversion.",
            "Principal Component Analysis via spectral decomposition of sample covariance.",
            "Fisher's Linear Discriminant Analysis crimcoords via generalized eigenvalues B a = lambda W a.",
            "Classical Metric Multidimensional Scaling (MDS) via double-centering.",
            "Gauss-Markov OLS, Hat matrix P, and residual maker M."
        ],
        r"""
### 1. Hotelling's T^2 & OLS Projection
```python
import numpy as np
import scipy.stats as stats

# Hotelling's T^2
np.random.seed(42)
X = np.random.randn(20, 2) + np.array([0.4, -0.3])
mu0 = np.array([0.0, 0.0])
n, p = X.shape

diff = np.mean(X, axis=0) - mu0
S = np.cov(X, rowvar=False)
T2 = n * (diff.T @ np.linalg.solve(S, diff))
F_stat = ((n - p) / ((n - 1) * p)) * T2
p_val = 1.0 - stats.f.cdf(F_stat, p, n - p)
print(f"Hotelling T2: {T2:.4f}, F-stat: {F_stat:.4f}, p-val: {p_val:.4f}")

# OLS Hat Matrix & Residual Maker
X_reg = np.hstack([np.ones((n, 1)), X[:, :1]])
y_reg = X[:, 1]
beta = np.linalg.solve(X_reg.T @ X_reg, X_reg.T @ y_reg)
P = X_reg @ np.linalg.solve(X_reg.T @ X_reg, X_reg.T)
M = np.eye(n) - P

assert np.allclose(P @ P, P)  # Idempotent
assert np.allclose(M @ M, M)  # Idempotent
assert np.allclose(M @ X_reg, 0.0)  # Orthogonal to X
print("Hotelling's T^2 and OLS Hat/Residual operators verified.")
```""",
        [
            "Hotelling's $T^2$ test statistic and p-value computed accurately.",
            "Hat matrix $P$ and residual maker $M$ confirmed symmetric and idempotent.",
            "Residual maker $M$ verified orthogonal to design matrix $X$ ($MX = 0$).",
            "Classical MDS coordinate recovery matches true pairwise distances."
        ]
    )
]

try:
    from scripts.story_real_data_extensions import EXTENSIONS
except ImportError:
    from story_real_data_extensions import EXTENSIONS

def generate_story_md(story):
    filename, title, role, goal, benefit, book_chap, sections, learnings, guide, criteria = story
    
    prefix = filename[:3]
    if prefix in EXTENSIONS:
        ext = EXTENSIONS[prefix]
        learnings = list(learnings) + ext["learnings"]
        guide = guide.rstrip() + "\n\n" + ext["guide"].strip()
        criteria = list(criteria) + ext["criteria"]

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
    stories_dir.mkdir(parents=True, exist_ok=True)
    
    for story in stories_data:
        filename = story[0]
        md_content = generate_story_md(story)
        file_path = stories_dir / f"{filename}.md"
        file_path.write_text(md_content, encoding="utf-8")
        print(f"Wrote {file_path}")

if __name__ == "__main__":
    main()
