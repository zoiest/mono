#!/usr/bin/env python3
"""Generates bin/ch01_introduction.org, bin/ch02_vectors_and_matrices.org, and bin/ch03_rank_of_matrices.org."""

from pathlib import Path

CH01 = r""":PROPERTIES:
:ID:       0192e4b3-0001-7000-8000-000000000001
:ROAM_ALIASES: "Chapter 1: Introduction" "Matrix Computing Fundamentals in Python" "R to Python Matrix Migration"
:END:
#+title: Chapter 01: Introduction & Computational Matrix Foundations
#+subtitle: Migration from R to Python (NumPy & SciPy) — Basics of Matrix Algebra for Statistics
#+author: Antigravity Notes
#+date: [2026-10-04]
#+filetags: :matrix-algebra:python:numpy:scipy:syntax:data-input:

[[id:0192e4b3-0000-7000-8000-000000000000][← Back to Master Index]] | [[id:0192e4b3-0002-7000-8000-000000000002][Next: Chapter 02 (Vectors and Matrices) →]]

* Core Objectives & Scope

The purpose of this study is to master foundational and advanced matrix algebra required for rigorous modern statistics, especially multivariate data analysis, linear regression models, and multivariate hypothesis testing. While the original text (/Basics of Matrix Algebra for Statistics with R/ by Nick Fieller) is framed around R, this guide provides complete parity in modern Python using ~numpy~ and ~scipy.linalg~.

** Target Topics Across the Curriculum
1. Elementary vector and matrix arithmetic, partitioned matrices, and matrix trace identities.
2. Centering matrices $H_n$, idempotency, and projection operators in linear models.
3. Matrix rank, linear independence, rank factorization, and collinearity in experimental design.
4. Determinants, Schur complements, and the Weinstein-Aronszajn rank-1 update identity.
5. Matrix inversion, ill-conditioning, condition numbers, and the Sherman-Morrison-Woodbury formula.
6. Eigenanalysis of real symmetric matrices, spectral decompositions, matrix powers/exponentials, and Singular Value Decomposition (SVD).
7. Vector and matrix calculus: gradients of linear/quadratic forms, trace derivatives, and log-determinant gradients for Maximum Likelihood Estimation (MLE).
8. Advanced factorizations (QR, LU, Cholesky), generalized inverses ($A^+, A^-$), Hadamard products ($A \circ B$), and Kronecker products ($A \otimes B$).
9. Major statistical applications: Multivariate Normal distribution, Hotelling's $T^2$, MANOVA, Principal Component Analysis (PCA), Fisher's Linear Discriminant Analysis (LDA), Canonical Correlation Analysis (CCA), Classical Metric MDS, and Constrained Ordinary Least Squares (OLS).

* Python Matrix Toolchain Setup & Syntax Fundamentals

In Python, the primary numerical engine is *NumPy* (~numpy~), complemented by *SciPy* (~scipy.linalg~) for specialized LAPACK/BLAS decompositions.

#+begin_src python
import numpy as np
import scipy.linalg as la

# Ensure clean float printing matching R's options(digits=3)
np.set_printoptions(precision=3, suppress=True)
#+end_src

** Critical Paradigm Differences Between R and Python

1. *0-based Indexing:* Python arrays use 0-indexed slicing (~A[0, 0]~ is the top-left element), whereas R uses 1-indexed slicing (~A[1, 1]~).
2. *Memory Order:* R matrices default to column-major (Fortran order, ~order='F'~). NumPy arrays default to row-major (C order, ~order='C'~). When creating arrays from a 1D sequence to match textbook examples, order must be handled explicitly:
   - R: ~matrix(c(1, 2, 3, 4, 5, 6), nrow=2, ncol=3, byrow=FALSE)~
   - Python: ~np.array([1, 2, 3, 4, 5, 6]).reshape((2, 3), order='F')~
3. *1D Vectors vs 2D Matrices:*
   - In R, ~x <- c(1, 2, 3)~ is a dimensionless vector that acts as a $3 \times 1$ column vector or $1 \times 3$ row vector depending on context.
   - In NumPy, ~x = np.array([1, 2, 3])~ has shape ~(3,)~. For matrix multiplication with 2D matrices, NumPy handles 1D arrays cleanly via ~@~, but if explicit $3 \times 1$ column geometry is needed, use ~x[:, None]~ or ~x.reshape(-1, 1)~.

* Inputting and Manipulating Data in Python

** Creating Vectors and Matrices

#+begin_src python
import numpy as np

# 1D vector of length 4
x = np.array([1.37, 1.63, 1.73, 1.36])
print("Vector x:", x, "Shape:", x.shape)

# Column-major matrix creation (R default byrow=FALSE)
# In R: A <- matrix(c(1,2,3,4,5,6), nrow=2, ncol=3, byrow=F)
A = np.array([1, 2, 3, 4, 5, 6]).reshape((2, 3), order='F')
print("Matrix A (column-major):\n", A)
# Result:
# [[1 3 5]
#  [2 4 6]]

# Row-major matrix creation (R byrow=TRUE)
# In R: B <- matrix(c(1,2,3,4,5,6), nrow=2, ncol=3, byrow=T)
B = np.array([1, 2, 3, 4, 5, 6]).reshape((2, 3), order='C')
print("Matrix B (row-major):\n", B)
# Result:
# [[1 2 3]
#  [4 5 6]]
#+end_src

** Subsetting and Slicing

#+begin_src python
# Access single element (row index 0, col index 1) -> corresponds to A[1, 2] in R
print("A[0, 1]:", A[0, 1])  # 3

# Access first row as 1D array
print("A[0, :]:", A[0, :])  # array([1, 3, 5])

# Access second column as 1D array
print("A[:, 1]:", A[:, 1])  # array([3, 4])

# Preserve 2D geometry for a column slice:
print("A[:, 1:2]:\n", A[:, 1:2])
# [[3]
#  [4]]
#+end_src

* Fundamental Matrix Operations in Python

** Addition, Subtraction, and Scalar Multiplication

#+begin_src python
# Addition: A + B
print("A + B:\n", A + B)

# Subtraction: A - B
print("A - B:\n", A - B)

# Scalar multiplication
print("2 * A:\n", 2 * A)
#+end_src

** Matrix Multiplication vs Elementwise Multiplication

#+begin_src python
# Elementwise (Hadamard) product: A * B
print("Elementwise product A * B:\n", A * B)

# Matrix Multiplication (@ operator):
# A is (2, 3), B.T is (3, 2) -> A @ B.T is (2, 2)
ABt = A @ B.T
print("A @ B.T:\n", ABt)
# [[22 49]
#  [28 64]]

# Transpose cross product: A.T @ B (shape (3, 3))
AtB = A.T @ B
print("A.T @ B:\n", AtB)
# [[ 9 12 15]
#  [19 26 33]
#  [29 40 51]]
#+end_src

** Stacking and Joining Matrices

In R, matrices are combined with ~cbind()~ and ~rbind()~. In NumPy, use ~np.hstack()~ and ~np.vstack()~ (or ~np.column_stack~):

#+begin_src python
# Horizontal concatenation (side-by-side) -> R: cbind(A, B)
H = np.hstack([A, B])
print("Horizontal stack (2x6):\n", H)

# Vertical concatenation (stacked on top) -> R: rbind(A, B)
V = np.vstack([A, B])
print("Vertical stack (4x3):\n", V)
#+end_src

** Diagonals and Trace

#+begin_src python
E = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

# Extract diagonal: diag(E)
print("Diagonal elements:", np.diag(E))  # [1 5 9]

# Trace: sum(diag(E))
print("Trace tr(E):", np.trace(E))       # 15

# Construct diagonal matrix from vector: diag(c(1, 5, 9))
D = np.diag([1, 5, 9])
print("Diagonal matrix D:\n", D)

# Cyclic property of trace: tr(E @ F) == tr(F @ E)
F = np.array([[1, 4, 7], [2, 5, 8], [3, 6, 9]])
print("tr(E @ F):", np.trace(E @ F))  # 285
print("tr(F @ E):", np.trace(F @ E))  # 285
#+end_src

** Determinants and Inverses

#+begin_src python
G = np.array([
    [1, -2,  2],
    [2,  0,  1],
    [1,  1, -2]
])

# Determinant: det(G)
det_G = np.linalg.det(G)
print("det(G):", det_G)  # -7.0

# Matrix Inverse: solve(G)
G_inv = np.linalg.inv(G)
print("G^{-1}:\n", G_inv)
print("Verification G @ G_inv:\n", np.round(G @ G_inv, 6))

# Moore-Penrose Pseudoinverse (ginv in MASS):
M = A @ B.T
print("M = A @ B.T:\n", M)
print("pinv(M):\n", np.linalg.pinv(M))
#+end_src

** Eigenanalyses and SVD Quick Tour

#+begin_src python
# Eigenvalues and eigenvectors of symmetric matrix
S = np.array([
    [4.0, 2.0],
    [2.0, 3.0]
])

evals, evecs = np.linalg.eigh(S)
print("Eigenvalues:", evals)
print("Eigenvectors (columns):\n", evecs)

# Singular Value Decomposition (SVD): A = U @ diag(s) @ Vt
U, s, Vt = np.linalg.svd(A, full_matrices=False)
print("Singular values:", s)
print("Reconstructed A:\n", U @ np.diag(s) @ Vt)
#+end_src

* Chapter 01 Exercises

1. *Exercise 1.1:* Install NumPy and SciPy in your Python environment and verify imports and version information.
2. *Exercise 1.2:* Create matrix $X = \begin{pmatrix} 1 & 4 & 7 \\ 2 & 5 & 8 \\ 3 & 6 & 9 \end{pmatrix}$ in Python both via row-major slicing and column-major reshaping. Verify shape and transpose.
3. *Exercise 1.3:* Verify that for rectangular matrix $A \in \mathbb{R}^{2 \times 3}$, $A A^T$ is $2 \times 2$ and $A^T A$ is $3 \times 3$. Calculate the traces $\text{tr}(A A^T)$ and $\text{tr}(A^T A)$ and verify equality.
4. *Exercise 1.4:* Given $u = (1, 2)^T$ and $v = (3, 4)^T$, compute the inner product $u^T v$ and the outer product $u v^T$ in NumPy. What are their shapes and ranks?
"""

CH02 = r""":PROPERTIES:
:ID:       0192e4b3-0002-7000-8000-000000000002
:ROAM_ALIASES: "Chapter 2: Vectors and Matrices" "Centering Matrix Hn" "Idempotent Matrices" "Matrix Trace Identities"
:END:
#+title: Chapter 02: Vectors and Matrices
#+subtitle: Algebraic Structures, Special Matrices, Partitioning, and Statistical Forms
#+author: Antigravity Notes
#+date: [2026-10-04]
#+filetags: :matrix-algebra:vectors:trace:centering-matrix:idempotent:quadratic-forms:

[[id:0192e4b3-0001-7000-8000-000000000001][← Previous: Chapter 01 (Introduction)]] | [[id:0192e4b3-0000-7000-8000-000000000000][Master Index]] | [[id:0192e4b3-0003-7000-8000-000000000003][Next: Chapter 03 (Rank of Matrices) →]]

* Vectors: Definitions & Geometry

A vector $x \in \mathbb{R}^p$ is an ordered $p$-tuple of real numbers:
\begin{equation}
x = \begin{pmatrix} x_1 \\ x_2 \\ \vdots \\ x_p \end{pmatrix}
\end{equation}
By mathematical convention, vectors are column vectors unless explicitly transposed.

** Fundamental Vector Products
- *Inner Product (Scalar Product):*
  \begin{equation}
  x^T y = \sum_{i=1}^p x_i y_i \in \mathbb{R}
  \end{equation}
  In NumPy: ~x @ y~ or ~np.dot(x, y)~.
- *Outer Product (Rank-1 Matrix):*
  \begin{equation}
  x y^T = \begin{pmatrix} x_1 y_1 & x_1 y_2 & \dots & x_1 y_q \\ x_2 y_1 & x_2 y_2 & \dots & x_2 y_q \\ \vdots & \vdots & \ddots & \vdots \\ x_p y_1 & x_p y_2 & \dots & x_p y_q \end{pmatrix} \in \mathbb{R}^{p \times q}
  \end{equation}
  In NumPy: ~np.outer(x, y)~ or ~x[:, None] @ y[None, :]~.
- *Euclidean Norm (Length):*
  \begin{equation}
  \|x\|_2 = \sqrt{x^T x} = \sqrt{\sum_{i=1}^p x_i^2}
  \end{equation}
  In NumPy: ~np.linalg.norm(x)~.
- *Orthogonality:*
  Two vectors $x, y \ne \mathbf{0}$ are orthogonal ($x \perp y$) if and only if $x^T y = 0$.

* Matrix Arithmetic & Fundamental Properties

Let $A = (a_{ij}) \in \mathbb{R}^{m \times p}$ and $B = (b_{jk}) \in \mathbb{R}^{p \times n}$.
The product $C = AB \in \mathbb{R}^{m \times n}$ has entries:
\begin{equation}
c_{ik} = \sum_{j=1}^p a_{ij} b_{jk}
\end{equation}

** Core Algebraic Rules
1. *Associativity:* $A(BC) = (AB)C$.
2. *Distributivity:* $A(B + C) = AB + AC$ and $(A + B)C = AC + BC$.
3. *Non-commutativity:* In general, $AB \ne BA$ even when both are square matrices of the same dimension.
4. *Transpose of a Product:* $(AB)^T = B^T A^T$. In general:
   \begin{equation}
   (A_1 A_2 \dots A_k)^T = A_k^T \dots A_2^T A_1^T
   \end{equation}

* Trace Operator & Useful Tricks

The trace of a square $n \times n$ matrix $A$, denoted $\text{tr}(A)$, is the sum of its diagonal elements:
\begin{equation}
\text{tr}(A) = \sum_{i=1}^n a_{ii}
\end{equation}

** Key Trace Properties
1. *Linearity:* $\text{tr}(\alpha A + \beta B) = \alpha \text{tr}(A) + \beta \text{tr}(B)$.
2. *Transpose Invariance:* $\text{tr}(A^T) = \text{tr}(A)$.
3. *Cyclic Property:* For matrices $A \in \mathbb{R}^{m \times p}$ and $B \in \mathbb{R}^{p \times m}$:
   \begin{equation}
   \text{tr}(AB) = \text{tr}(BA) = \sum_{i=1}^m \sum_{j=1}^p a_{ij} b_{ji}
   \end{equation}
   More generally, for any cyclic permutation: $\text{tr}(ABC) = \text{tr}(BCA) = \text{tr}(CAB)$ (provided matrix dimensions allow multiplication).
4. *Trace of Outer Product:*
   \begin{equation}
   \text{tr}(x y^T) = y^T x
   \end{equation}
5. *Frobenius Inner Product:*
   \begin{equation}
   \text{tr}(A^T B) = \sum_{i, j} a_{ij} b_{ij} = \text{vec}(A)^T \text{vec}(B)
   \end{equation}
   And the squared Frobenius norm is $\|A\|_F^2 = \text{tr}(A^T A) = \sum_{i, j} a_{ij}^2$.

* Special Matrices in Statistics

** 1. Symmetric & Skew-Symmetric Matrices
- A matrix $A$ is *symmetric* if $A^T = A$.
- A matrix $A$ is *skew-symmetric* if $A^T = -A$.
- Any square matrix $A$ can be decomposed uniquely into symmetric and skew-symmetric components:
  \begin{equation}
  A = \frac{1}{2}(A + A^T) + \frac{1}{2}(A - A^T)
  \end{equation}

** 2. Products with Transpose: $A^TA$ and $AA^T$
For any real rectangular matrix $A \in \mathbb{R}^{m \times n}$:
- Both $A^T A$ ($n \times n$) and $A A^T$ ($m \times m$) are symmetric.
- Both are *positive semi-definite*: for any vector $z$, $z^T (A^TA) z = (Az)^T (Az) = \|Az\|_2^2 \ge 0$.
- $\text{rank}(A^TA) = \text{rank}(AA^T) = \text{rank}(A)$.

** 3. Orthogonal Matrices
A square matrix $Q \in \mathbb{R}^{n \times n}$ is orthogonal if:
\begin{equation}
Q^T Q = Q Q^T = I_n \implies Q^{-1} = Q^T
\end{equation}
- Orthogonal transformations preserve lengths: $\|Qx\|_2 = \|x\|_2$.
- Preserves inner products and angles: $(Qx)^T (Qy) = x^T Q^T Q y = x^T y$.
- $\det(Q) = \pm 1$.

** 4. Idempotent Matrices
A square matrix $M$ is *idempotent* if:
\begin{equation}
M^2 = M
\end{equation}
- *Fundamental Statistical Theorem:* If $M$ is symmetric and idempotent, then:
  \begin{equation}
  \text{rank}(M) = \text{tr}(M)
  \end{equation}
- In linear models, the projection (hat) matrix $P = X(X^TX)^{-1}X^T$ and residual operator $M = I - P$ are symmetric and idempotent.

** 5. The Centering Matrix $H_n$ (Crucial Statistical Tool)
Let $\mathbf{1}_n = (1, 1, \dots, 1)^T \in \mathbb{R}^n$. The centering matrix is defined as:
\begin{equation}
H_n = I_n - \frac{1}{n} \mathbf{1}_n \mathbf{1}_n^T
\end{equation}
- *Symmetry:* $H_n^T = H_n$.
- *Idempotency:*
  \begin{equation}
  H_n^2 = \left(I - \frac{1}{n}\mathbf{1}\mathbf{1}^T\right)\left(I - \frac{1}{n}\mathbf{1}\mathbf{1}^T\right) = I - \frac{2}{n}\mathbf{1}\mathbf{1}^T + \frac{1}{n^2}\mathbf{1}(\mathbf{1}^T\mathbf{1})\mathbf{1}^T = I - \frac{1}{n}\mathbf{1}\mathbf{1}^T = H_n
  \end{equation}
  since $\mathbf{1}^T \mathbf{1} = n$.
- *Annihilator of Constant Vectors:* $H_n \mathbf{1}_n = \mathbf{1}_n - \frac{1}{n}\mathbf{1}(n) = \mathbf{0}$.
- *Trace & Rank:* $\text{tr}(H_n) = \text{tr}(I_n) - \frac{1}{n}\text{tr}(\mathbf{1}\mathbf{1}^T) = n - \frac{1}{n}(n) = n - 1$.
  Therefore, $\text{rank}(H_n) = n - 1$.
- *Data Centering:* For an $n \times p$ data matrix $X$, $H_n X$ subtracts the column sample means:
  \begin{equation}
  H_n X = X - \mathbf{1}_n \bar{x}^T
  \end{equation}
  where $\bar{x} = \frac{1}{n} X^T \mathbf{1}_n$.
- *Sample Covariance Matrix:*
  \begin{equation}
  S = \frac{1}{n - 1} X^T H_n X
  \end{equation}

** 6. Nilpotent, Unipotent, and Similar Matrices
- *Nilpotent:* $A^k = 0$ for some positive integer $k$. All eigenvalues are 0.
- *Unipotent:* $A - I$ is nilpotent.
- *Similar:* $B = P^{-1} A P$ for non-singular $P$. Similar matrices share the same eigenvalues, trace, and determinant.

* Partitioned Matrices

Matrices partitioned into sub-blocks:
\begin{equation}
M = \begin{pmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{pmatrix}
\end{equation}

** Block Multiplication Rule
Provided sub-matrix dimensions are conformable:
\begin{equation}
\begin{pmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{pmatrix}
\begin{pmatrix} B_{11} & B_{12} \\ B_{21} & B_{22} \end{pmatrix}
= \begin{pmatrix} A_{11}B_{11} + A_{12}B_{21} & A_{11}B_{12} + A_{12}B_{22} \\ A_{21}B_{11} + A_{22}B_{21} & A_{21}B_{12} + A_{22}B_{22} \end{pmatrix}
\end{equation}

* Linear and Quadratic Forms

** Linear Form
A linear combination of variables $x_1, \dots, x_p$:
\begin{equation}
L(x) = a^T x = \sum_{i=1}^p a_i x_i
\end{equation}

** Quadratic Form
A degree-2 homogeneous polynomial in $x$:
\begin{equation}
Q(x) = x^T A x = \sum_{i=1}^p \sum_{j=1}^p a_{ij} x_i x_j
\end{equation}
- *Symmetrization Principle:* Since $x^T A x$ is a scalar ($1 \times 1$), $x^T A x = (x^T A x)^T = x^T A^T x$. Thus:
  \begin{equation}
  x^T A x = x^T \left(\frac{A + A^T}{2}\right) x
  \end{equation}
  We can always assume without loss of generality that the matrix of a quadratic form is *symmetric*.

* Complete Numerical Code Recipes in Python

#+begin_src python
import numpy as np

# 1. Construction of Centering Matrix H_n
def centering_matrix(n: int) -> np.ndarray:
    ones = np.ones((n, 1))
    return np.eye(n) - (ones @ ones.T) / n

H4 = centering_matrix(4)
print("Centering Matrix H_4:\n", H4)
print("H_4 is symmetric:", np.allclose(H4, H4.T))
print("H_4 is idempotent (H^2 == H):", np.allclose(H4 @ H4, H4))
print("Trace of H_4 (rank):", np.trace(H4))  # 3.0

# 2. Sample Statistics via Centering Matrix
# 4 observations on 2 variables
X = np.array([
    [10.0, 2.0],
    [12.0, 4.0],
    [14.0, 5.0],
    [16.0, 9.0]
])
n, p = X.shape
H = centering_matrix(n)

# Mean centered data: H @ X
X_centered = H @ X
print("Mean centered data:\n", X_centered)
print("Column means:", np.mean(X, axis=0))

# Sample covariance matrix S = (1 / (n - 1)) * X.T @ H @ X
S = (X.T @ H @ X) / (n - 1)
print("Sample covariance S:\n", S)
print("NumPy np.cov verification:\n", np.cov(X, rowvar=False))
#+end_src

* Chapter 02 Exercises

1. *Exercise 2.1:* Given $a = (1, 2, 3)^T$, $b = (4, -2, 0)^T$, and $c = (1, 1, -1)^T$, determine which pairs are orthogonal.
2. *Exercise 2.2:* Prove algebraically that $A A^T$ is symmetric for any rectangular matrix $A \in \mathbb{R}^{m \times n}$. Then verify numerically in NumPy for a random $4 \times 3$ matrix.
3. *Exercise 2.3:* For $n = 5$, construct the centering matrix $H_5$. Verify that $H_5 \mathbf{1}_5 = \mathbf{0}$, $\text{tr}(H_5) = 4$, and $H_5^2 = H_5$.
4. *Exercise 2.4:* For matrix $A = \begin{pmatrix} 2 & 1 \\ 5 & 4 \end{pmatrix}$, compute the quadratic form $x^T A x$ where $x = (x_1, x_2)^T$. Write the quadratic form using the symmetric version $A_s = \frac{1}{2}(A + A^T)$.
"""

CH03 = r""":PROPERTIES:
:ID:       0192e4b3-0003-7000-8000-000000000003
:ROAM_ALIASES: "Chapter 3: Rank of Matrices" "Matrix Rank" "Rank Factorization" "Collinearity"
:END:
#+title: Chapter 03: Rank of Matrices
#+subtitle: Linear Independence, Rank Factorization, Rank Inequalities, and Statistical Degrees of Freedom
#+author: Antigravity Notes
#+date: [2026-10-04]
#+filetags: :matrix-algebra:rank:linear-independence:factorization:collinearity:statistics:

[[id:0192e4b3-0002-7000-8000-000000000002][← Previous: Chapter 02 (Vectors and Matrices)]] | [[id:0192e4b3-0000-7000-8000-000000000000][Master Index]] | [[id:0192e4b3-0004-7000-8000-000000000004][Next: Chapter 04 (Determinants) →]]

* Definitions & Fundamental Rank Theorem

Let $A \in \mathbb{R}^{m \times n}$.
- The *row rank* of $A$ is the maximum number of linearly independent row vectors in $A$.
- The *column rank* of $A$ is the maximum number of linearly independent column vectors in $A$.

** Fundamental Theorem of Linear Algebra
For any real matrix $A$:
\begin{equation}
\text{row rank}(A) = \text{column rank}(A) = \text{rank}(A) \le \min(m, n)
\end{equation}
- If $\text{rank}(A) = \min(m, n)$, $A$ has *full rank*.
  - Full row rank if $\text{rank}(A) = m$.
  - Full column rank if $\text{rank}(A) = n$.
- If $\text{rank}(A) < \min(m, n)$, $A$ is *rank-deficient* (singular if $m = n$).

* Rank Factorization

** Theorem (Rank Factorization)
If $A \in \mathbb{R}^{m \times n}$ has $\text{rank}(A) = r > 0$, then there exist matrices $B \in \mathbb{R}^{m \times r}$ and $C \in \mathbb{R}^{r \times n}$ both of rank $r$ such that:
\begin{equation}
A = BC
\end{equation}
- $B$ has full column rank $r$.
- $C$ has full row rank $r$.

** Matrices of Rank 1
A non-zero matrix $A \in \mathbb{R}^{m \times n}$ has $\text{rank}(A) = 1$ if and only if there exist non-zero vectors $x \in \mathbb{R}^m$ and $y \in \mathbb{R}^n$ such that:
\begin{equation}
A = x y^T
\end{equation}
All rows of $A$ are scalar multiples of $y^T$, and all columns are scalar multiples of $x$.

* Rank Inequalities

** 1. Subadditivity (Sum and Difference)
\begin{equation}
\text{rank}(A + B) \le \text{rank}(A) + \text{rank}(B)
\end{equation}
\begin{equation}
\text{rank}(A - B) \ge |\text{rank}(A) - \text{rank}(B)|
\end{equation}

** 2. Products of Matrices
For $A \in \mathbb{R}^{m \times p}$ and $B \in \mathbb{R}^{p \times n}$:
\begin{equation}
\text{rank}(AB) \le \min(\text{rank}(A), \text{rank}(B))
\end{equation}

** 3. Sylvester's Rank Inequality
\begin{equation}
\text{rank}(AB) \ge \text{rank}(A) + \text{rank}(B) - p
\end{equation}

** 4. Frobenius Rank Inequality
For conformable matrices $A, B, C$:
\begin{equation}
\text{rank}(ABC) \ge \text{rank}(AB) + \text{rank}(BC) - \text{rank}(B)
\end{equation}

** 5. Invariance Under Multiplication by Non-Singular Matrices
If $P$ is an $m \times m$ non-singular matrix and $Q$ is an $n \times n$ non-singular matrix:
\begin{equation}
\text{rank}(PAQ) = \text{rank}(A)
\end{equation}
In particular, multiplying by orthogonal matrices preserves rank: $\text{rank}(A Q) = \text{rank}(A)$.

** 6. Gram Matrix Rank Equality
\begin{equation}
\text{rank}(A^T A) = \text{rank}(A A^T) = \text{rank}(A)
\end{equation}
*Proof Sketch:* $A^T A x = \mathbf{0} \implies x^T A^T A x = 0 \implies \|Ax\|_2^2 = 0 \implies Ax = \mathbf{0}$.
Thus, the null space of $A^T A$ equals the null space of $A$, meaning their column ranks are identical.

* Statistical Relevance of Rank

1. *Invertibility of Cross-Product in OLS:*
   In the multiple linear regression model $y = X\beta + \epsilon$ with design matrix $X \in \mathbb{R}^{n \times p}$ ($n \ge p$):
   \begin{equation}
   (X^T X)^{-1} \text{ exists} \iff \text{rank}(X^T X) = p \iff \text{rank}(X) = p
   \end{equation}
   If $\text{rank}(X) < p$, multicollinearity exists, parameter estimates $\hat{\beta}$ are non-unique, and generalized inverses must be used.
2. *Degrees of Freedom in ANOVA:*
   In analysis of variance, degrees of freedom correspond precisely to the ranks of idempotent quadratic forms:
   \begin{equation}
   \text{df} = \text{rank}(H_n) = n - 1
   \end{equation}
   Under Cochran's Theorem, if $y \sim N(\mathbf{0}, \sigma^2 I)$ and $y^T A y / \sigma^2 \sim \chi^2_r$, then $r = \text{rank}(A) = \text{tr}(A)$.

* Numerical Computation in Python

In R, matrix rank is computed via ~qr(A)$rank~.
In NumPy, rank is computed via Singular Value Decomposition thresholding using ~np.linalg.matrix_rank(A)~:

#+begin_src python
import numpy as np

# Create a rank-deficient 3x3 matrix (row 3 is row 1 + row 2)
X = np.array([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
    [5.0, 7.0, 9.0]
])

rank_X = np.linalg.matrix_rank(X)
print("Rank of X:", rank_X)  # 2

# Rank-1 matrix verification
u = np.array([[1.0], [2.0], [3.0]])
v = np.array([[4.0], [5.0]])
R1 = u @ v.T  # (3, 2)
print("Outer product R1:\n", R1)
print("Rank of R1:", np.linalg.matrix_rank(R1))  # 1

# Sylvester Inequality Verification
A = np.random.randn(4, 3)
B = np.random.randn(3, 5)
rank_A = np.linalg.matrix_rank(A)
rank_B = np.linalg.matrix_rank(B)
rank_AB = np.linalg.matrix_rank(A @ B)
p = 3
print(f"rank(AB)={rank_AB} >= rank(A)={rank_A} + rank(B)={rank_B} - {p} = {rank_A + rank_B - p}")
assert rank_AB >= rank_A + rank_B - p
#+end_src

* Chapter 03 Exercises

1. *Exercise 3.1:* Construct matrix $X_3 = \begin{pmatrix} 1 & 3 & 4 \\ 2 & 5 & 7 \\ 3 & 8 & 11 \end{pmatrix}$. Find its rank in Python. Express the third column as a linear combination of the first two.
2. *Exercise 3.2:* Find the rank factorization $A = BC$ for $A = \begin{pmatrix} 1 & 2 & 3 \\ 2 & 4 & 6 \end{pmatrix}$.
3. *Exercise 3.3:* Given $X \in \mathbb{R}^{10 \times 3}$ with full column rank, verify numerically that $\text{rank}(X^T X) = 3$ and $\text{rank}(X X^T) = 3$.
"""

def main():
    Path("bin/ch01_introduction.org").write_text(CH01, encoding="utf-8")
    print("Wrote bin/ch01_introduction.org")
    Path("bin/ch02_vectors_and_matrices.org").write_text(CH02, encoding="utf-8")
    print("Wrote bin/ch02_vectors_and_matrices.org")
    Path("bin/ch03_rank_of_matrices.org").write_text(CH03, encoding="utf-8")
    print("Wrote bin/ch03_rank_of_matrices.org")

if __name__ == "__main__":
    main()
