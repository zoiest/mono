#!/usr/bin/env python3
"""Generates bin/index.org - Master Index & Map of Content."""

import os
from pathlib import Path

INDEX_CONTENT = r""":PROPERTIES:
:ID:       0192e4b3-0000-7000-8000-000000000000
:ROAM_ALIASES: "Basics of Matrix Algebra for Statistics" "Matrix Algebra in Python MOC" "Fieller Matrix Notes"
:END:
#+title: Basics of Matrix Algebra for Statistics with Python (NumPy & SciPy)
#+subtitle: Comprehensive Chapter Summaries, Code Recipes, and Statistical Matrix Foundations
#+author: Antigravity Notes
#+date: [2026-10-04]
#+filetags: :linear-algebra:statistics:numpy:scipy:matrix-calculus:pca:regression:reference:

* Textbook & Reference Information

- *Book Title:* /Basics of Matrix Algebra for Statistics with R/
- *Author:* Nick Fieller (University of Sheffield)
- *Publisher:* Chapman & Hall/CRC The R Series (Taylor & Francis Group, 2016)
- *Local PDF:* [[file:///home/tofunth/stuffs/mono/gym/matalg/downloads/Basics_of_Matrix_Algebra_for_Statistics_with_R.pdf][downloads/Basics_of_Matrix_Algebra_for_Statistics_with_R.pdf]]
- *Target Computing Stack:* Python 3.12+ / NumPy 2.0+ / SciPy 1.14+ (converted from base R and MASS)
- *Interactive Project Board:* [[https://github.com/users/zoiest/projects/2][GitHub Projects: @zoiest's matalg]]
- *Repository Location:* ~mono/gym/matalg~

* Map of Content (MOC)

#+caption: Structure of Matrix Algebra for Statistics in Python
| Chapter | Title | Org Reference | Topics Covered | Mapped Stories |
|---------+-------+---------------+----------------+----------------|
| *01* | Introduction | [[id:0192e4b3-0001-7000-8000-000000000001][Chapter 01: Introduction]] | Setup, Syntax, Slicing, R-to-Python Translation | Story 001 |
| *02* | Vectors and Matrices | [[id:0192e4b3-0002-7000-8000-000000000002][Chapter 02: Vectors and Matrices]] | Vector Norms, Matrix Arithmetic, Trace, Centering Matrix $H_n$, Idempotency | Story 002, 003, 004, 005 |
| *03* | Rank of Matrices | [[id:0192e4b3-0003-7000-8000-000000000003][Chapter 03: Rank of Matrices]] | Rank Factorization, Rank-1 Matrices, Sylvester/Frobenius Inequalities | Story 006, 007 |
| *04* | Determinants | [[id:0192e4b3-0004-7000-8000-000000000004][Chapter 04: Determinants]] | Laplace Expansions, Schur Complements, Weinstein-Aronszajn Identity | Story 008, 009 |
| *05* | Inverses | [[id:0192e4b3-0005-7000-8000-000000000005][Chapter 05: Inverses]] | Regular & One-Sided Inverses, Sherman-Morrison Formula, Banachiewicz Inversion | Story 010, 011, 012 |
| *06* | Eigenanalysis | [[id:0192e4b3-0006-7000-8000-000000000006][Chapter 06: Eigenanalysis]] | Spectral Decomposition, Matrix Exponential $\exp(A)$, SVD, Rayleigh Quotient | Story 013, 014, 015 |
| *07* | Vector & Matrix Calculus | [[id:0192e4b3-0007-7000-8000-000000000007][Chapter 07: Vector and Matrix Calculus]] | Gradients of Linear/Quadratic Forms, Trace Derivatives, $\nabla \log \det(X)$ | Story 016, 017 |
| *08* | Further Topics | [[id:0192e4b3-0008-7000-8000-000000000008][Chapter 08: Further Topics]] | QR, LU, Cholesky, Schur, Moore-Penrose $A^+$, Kronecker Product $A \otimes B$, $\text{vec}$ | Story 018, 019, 020 |
| *09* | Key Applications to Statistics | [[id:0192e4b3-0009-7000-8000-000000000009][Chapter 09: Applications to Statistics]] | MVN MLE, Hotelling's $T^2$, MANOVA, PCA, LDA, CCA, Metric MDS, Gauss-Markov OLS | Story 021, 022, 023, 024 |
| *10* | Outline Solutions | [[id:0192e4b3-0010-7000-8000-000000000010][Chapter 10: Solutions]] | Complete Python Numerical Solutions for Chapters 1 through 9 | All Exercises |

* Rosetta Stone: R to Python (NumPy / SciPy) Matrix Translation

#+caption: Direct Translation between R and Python Matrix Operations
| Mathematical Operation | R Expression | Python (NumPy / SciPy) Equivalent | Critical Differences & Notes |
|------------------------+--------------+------------------------------------+------------------------------|
| *Vector Creation* | ~c(1, 2, 3)~ | ~np.array([1, 2, 3])~ | R 1-indexed; NumPy 0-indexed |
| *2D Column Vector* | ~matrix(c(1, 2, 3))~ | ~np.array([[1], [2], [3]])~ or ~x[:, None]~ | In NumPy 1D array has shape ~(n,)~ |
| *Matrix Creation (Row-major)* | ~matrix(dat, 2, 3, byrow=T)~ | ~np.array(dat).reshape(2, 3)~ | NumPy is row-major (C-order) by default |
| *Matrix Creation (Col-major)* | ~matrix(dat, 2, 3, byrow=F)~ | ~np.array(dat).reshape((2, 3), order='F')~ | R is column-major by default |
| *Identity Matrix* | ~diag(n)~ | ~np.eye(n)~ | ~np.identity(n)~ also works |
| *Matrix Multiplication* | ~A %*% B~ | ~A @ B~ or ~np.matmul(A, B)~ | ~A * B~ is elementwise in both! |
| *Elementwise (Hadamard)* | ~A * B~ | ~A * B~ or ~np.multiply(A, B)~ | Requires conformable or broadcastable shapes |
| *Matrix Transpose* | ~t(A)~ | ~A.T~ | For 1D array ~x~, ~x.T~ is still 1D! |
| *Cross-Product* $X^TX$ | ~crossprod(X)~ | ~X.T @ X~ | Faster than naive in both |
| *Cross-Product* $XX^T$ | ~tcrossprod(X)~ | ~X @ X.T~ | Essential in kernel methods |
| *Matrix Inversion* $A^{-1}$ | ~solve(A)~ | ~np.linalg.inv(A)~ | Do *not* use to solve $Ax=b$ |
| *Linear System Solve* $Ax=b$ | ~solve(A, b)~ | ~np.linalg.solve(A, b)~ | Uses LU/LAPACK factorization |
| *Determinant* $\det(A)$ | ~det(A)~ | ~np.linalg.det(A)~ | Use ~np.linalg.slogdet(A)~ for log-det |
| *Trace* $\text{tr}(A)$ | ~sum(diag(A))~ | ~np.trace(A)~ | Sum of main diagonal elements |
| *Diagonal Vector Extract* | ~diag(A)~ | ~np.diag(A)~ | Returns 1D array of diagonals |
| *Create Diagonal Matrix* | ~diag(v)~ | ~np.diag(v)~ | When input is 1D array |
| *Column Binding (Horizontal)* | ~cbind(A, B)~ | ~np.hstack([A, B])~ or ~np.column_stack~ | Matrices must have same row count |
| *Row Binding (Vertical)* | ~rbind(A, B)~ | ~np.vstack([A, B])~ or ~np.row_stack~ | Matrices must have same column count |
| *Matrix Rank* | ~qr(A)$rank~ | ~np.linalg.matrix_rank(A)~ | Uses SVD thresholding |
| *Eigenvalues & Eigenvectors* | ~eigen(A)~ | ~np.linalg.eig(A)~ (general) | Returns ~(eigenvalues, eigenvectors)~ |
| *Symmetric Eigenanalysis* | ~eigen(A, symmetric=T)~ | ~np.linalg.eigh(A)~ | Strictly real eigenvalues (ascending) |
| *Singular Value Decomp (SVD)*| ~svd(A)~ | ~np.linalg.svd(A, full_matrices=False)~ | In Python $A = U \Sigma V^T$ ($V$ transposed!) |
| *Cholesky Decomposition* | ~chol(A)~ | ~np.linalg.cholesky(A)~ | *Trap:* R returns upper $U$; NumPy returns lower $L$ ($A = LL^T$) |
| *QR Decomposition* | ~qr(A)~ | ~np.linalg.qr(A)~ | Returns $Q, R$ directly |
| *LU Decomposition* | ~Matrix::lu(A)~ | ~scipy.linalg.lu(A)~ | Returns $P, L, U$ |
| *Schur Decomposition* | ~Matrix::Schur(A)~ | ~scipy.linalg.schur(A)~ | Returns $T, Z$ |
| *Moore-Penrose Inverse* $A^+$ | ~MASS::ginv(A)~ | ~np.linalg.pinv(A)~ | Robust pseudoinverse via SVD |
| *Kronecker Product* $A \otimes B$ | ~A %x% B~ or ~kronecker(A, B)~ | ~np.kron(A, B)~ | Block matrix tensor product |
| *Vec Operator* $\text{vec}(A)$ | ~c(A)~ | ~A.flatten(order='F')~ | *Must specify* ~order='F'~ for column-major! |

* The Ten Cardinal Rules of Matrix Computing in Python for Statisticians

1. *Never invert a matrix to solve a linear system:*
   Always use ~np.linalg.solve(X.T @ X, X.T @ y)~ or ~scipy.linalg.solve~ instead of ~np.linalg.inv(X.T @ X) @ X.T @ y~. Explicit inversion is computationally slower ($O(n^3)$ with larger constant factor) and numerically unstable.
2. *Always use ~np.linalg.eigh~ for symmetric matrices:*
   Covariance, correlation, and scatter matrices are mathematically symmetric. ~np.linalg.eigh~ is $2\times$ faster, guarantees strictly real eigenvalues and orthonormal eigenvectors, and avoids numerical leakage into the complex plane.
3. *Beware of the 1D Array Semantics:*
   In NumPy, ~x = np.array([1, 2, 3])~ has shape ~(3,)~. Its transpose ~x.T~ is still ~(3,)~. If you require explicit column or row vector geometry, use ~x[:, None]~ (shape ~(3, 1)~) or ~x[None, :]~ (shape ~(1, 3)~).
4. *Beware of Cholesky Orientation Differences:*
   R's ~chol(A)~ returns an *upper triangular* matrix $U$ such that $U^T U = A$. NumPy's ~np.linalg.cholesky(A)~ returns a *lower triangular* matrix $L$ such that $L L^T = A$. If you need upper triangular in Python, take ~L.T~ or call ~scipy.linalg.cholesky(A, lower=False)~.
5. *Always use ~slogdet~ for likelihoods and determinants:*
   Determinants of large covariance matrices underflow to ~0.0~ or overflow to ~inf~ rapidly. Always calculate log-likelihoods via ~sign, logdet = np.linalg.slogdet(Sigma)~.
6. *Order matters in Vectorization:*
   Mathematical matrix algebra and R define the $\text{vec}(A)$ operator by stacking columns. Because NumPy is C-order (row-major) by default, you must explicitly pass ~order='F'~: ~A.flatten(order='F')~ to match textbook derivations!
7. *Avoid computing $X^TX$ explicitly in OLS when possible:*
   Forming $X^TX$ squares the condition number: $\kappa(X^TX) = \kappa(X)^2$. For ill-conditioned data, use QR decomposition ($Q, R = \text{qr}(X)$) or ~np.linalg.lstsq(X, y, rcond=None)~.
8. *Exploit the Centering Matrix $H_n$:*
   The centering matrix $H_n = I_n - \frac{1}{n}\mathbf{1}\mathbf{1}^T$ satisfies $H_n^T = H_n$, $H_n^2 = H_n$, $\text{tr}(H_n) = n-1$, and $H_n \mathbf{1} = \mathbf{0}$. The sample covariance is compactly written as $S = \frac{1}{n-1} X^T H_n X$.
9. *Track dimensions religiously:*
   A scalar is a $1 \times 1$ matrix. Therefore, quadratic forms $x^T A x$ are scalars, enabling identities such as $x^T A x = \text{tr}(x^T A x) = \text{tr}(A x x^T)$.
10. *Verify idempotency for degrees of freedom:*
    In linear models, test statistics follow $\chi^2$ distributions under Cochran's theorem if and only if the underlying quadratic form matrix is symmetric and idempotent. The degrees of freedom equal the trace: $\text{rank}(A) = \text{tr}(A)$.
"""

def main():
    out_path = Path("bin/index.org")
    out_path.write_text(INDEX_CONTENT, encoding="utf-8")
    print(f"Generated {out_path} ({len(INDEX_CONTENT)} chars)")

if __name__ == "__main__":
    main()
