#!/usr/bin/env python3
"""Generates bin/ch10_outline_solutions.org - Complete Python Numerical Solutions."""

from pathlib import Path

CH10 = r""":PROPERTIES:
:ID:       0192e4b3-0010-7000-8000-000000000010
:ROAM_ALIASES: "Chapter 10: Outline Solutions" "Matrix Algebra Exercise Solutions" "Python Solutions"
:END:
#+title: Chapter 10: Outline Solutions to Exercises
#+subtitle: Complete Step-by-Step Mathematical Solutions and Verified Python (NumPy/SciPy) Code
#+author: Antigravity Notes
#+date: [2026-10-04]
#+filetags: :solutions:exercises:numpy:scipy:verification:

[[id:0192e4b3-0009-7000-8000-000000000009][← Previous: Chapter 09 (Key Applications to Statistics)]] | [[id:0192e4b3-0000-7000-8000-000000000000][Master Index]]

* Overview

This document provides complete, verified Python numerical implementations and algebraic derivations for the end-of-chapter exercises from Nick Fieller's /Basics of Matrix Algebra for Statistics with R/, converted to ~numpy~ and ~scipy.linalg~.

#+begin_src python
import numpy as np
import scipy.linalg as la
import scipy.stats as stats

np.set_printoptions(precision=4, suppress=True)
#+end_src

* Chapter 1 Solutions: Introduction

#+begin_src python
# Verification of basic operations and array reshaping
# Exercise 1.2: Matrix creation
X_c = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]).reshape((3, 3), order='C')
X_f = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]).reshape((3, 3), order='F')
print("Row-major (C):\n", X_c)
print("Col-major (F):\n", X_f)

# Exercise 1.3: Rectangular traces
A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print("tr(A @ A.T):", np.trace(A @ A.T))  # 91.0
print("tr(A.T @ A):", np.trace(A.T @ A))  # 91.0
assert np.isclose(np.trace(A @ A.T), np.trace(A.T @ A))

# Exercise 1.4: Inner and Outer products
u = np.array([1.0, 2.0])
v = np.array([3.0, 4.0])
inner_prod = u @ v
outer_prod = np.outer(u, v)
print("Inner product u^T v:", inner_prod)       # 11.0
print("Outer product u v^T:\n", outer_prod)     # [[3. 4.], [6. 8.]]
print("Rank of outer product:", np.linalg.matrix_rank(outer_prod))  # 1
#+end_src

* Chapter 2 Solutions: Vectors and Matrices

#+begin_src python
# (1) Orthogonality of Vectors
a = np.array([1.0, 2.0, 3.0])
b = np.array([4.0, -2.0, 0.0])
c = np.array([1.0, 1.0, -1.0])

print("a^T b:", a @ b)  # 0.0 -> a and b are orthogonal!
print("a^T c:", a @ c)  # 0.0 -> a and c are orthogonal!
print("b^T c:", b @ c)  # 2.0 -> b and c are not orthogonal

# (2) Symmetry of AA^T and A^T A
A = np.random.randn(4, 3)
AAt = A @ A.T
AtA = A.T @ A
assert np.allclose(AAt, AAt.T)
assert np.allclose(AtA, AtA.T)
print("AA^T and A^T A symmetry verified.")

# (3) Centering Matrix H_5 properties
n = 5
H5 = np.eye(n) - np.ones((n, n)) / n
ones = np.ones(n)
assert np.allclose(H5 @ ones, 0.0)
assert np.allclose(H5 @ H5, H5)
assert np.isclose(np.trace(H5), n - 1)
print("Centering matrix H_5: H 1 = 0, H^2 = H, tr(H) = 4 verified.")

# (4) Quadratic Form Symmetrization
# A = [[2, 1], [5, 4]]
A = np.array([[2.0, 1.0], [5.0, 4.0]])
A_sym = 0.5 * (A + A.T)  # [[2, 3], [3, 4]]
x = np.array([3.0, -2.0])
q_orig = x.T @ A @ x
q_sym = x.T @ A_sym @ x
print(f"Original Q(x)={q_orig:.2f}, Symmetric Q(x)={q_sym:.2f}")
assert np.isclose(q_orig, q_sym)
#+end_src

* Chapter 3 Solutions: Rank of Matrices

#+begin_src python
# (1) Rank of X1 and X2
X1 = np.array([
    [1.3, 9.1],
    [1.2, 8.4]
])
# 9.1 / 1.3 = 7.0, 8.4 / 1.2 = 7.0 -> col 2 is 7 * col 1
print("Rank of X1:", np.linalg.matrix_rank(X1))  # 1

X3 = np.array([
    [1.0, 3.0, 4.0],
    [2.0, 5.0, 7.0],
    [3.0, 8.0, 11.0]
])
# Col 3 = Col 1 + Col 2, Row 3 = Row 1 + Row 2
print("Rank of X3:", np.linalg.matrix_rank(X3))  # 2

# (2) Rank Factorization A = BC for 2x3 matrix of rank 1
A = np.array([
    [1.0, 2.0, 3.0],
    [2.0, 4.0, 6.0]
])
# B is (2, 1), C is (1, 3)
B = np.array([[1.0], [2.0]])
C = np.array([[1.0, 2.0, 3.0]])
assert np.allclose(A, B @ C)
print("Rank factorization A = B @ C verified:\n", B @ C)

# (3) Sylvester Inequality Verification
A = np.random.randn(5, 3)
B = np.random.randn(3, 4)
rank_A = np.linalg.matrix_rank(A)
rank_B = np.linalg.matrix_rank(B)
rank_AB = np.linalg.matrix_rank(A @ B)
p = 3
assert rank_AB >= rank_A + rank_B - p
print(f"Sylvester inequality holds: {rank_AB} >= {rank_A + rank_B - p}")
#+end_src

* Chapter 4 Solutions: Determinants

#+begin_src python
# (1) Determinants of 2x2 and Triangular Matrices
A = np.array([[2.0, 3.0], [2.0, 4.0]])
print("det(A):", np.linalg.det(A))  # 2 * 4 - 3 * 2 = 2.0

T = np.array([
    [1.0, 2.0, 3.0],
    [0.0, 4.0, 5.0],
    [0.0, 0.0, 6.0]
])
print("det(T) via product of diagonals:", np.prod(np.diag(T)))  # 24.0
assert np.isclose(np.linalg.det(T), 24.0)

# (2) Rank-1 Update Formula: det(I_4 + 3 x x^T) with x = (1, 1, 1, 1)^T
x = np.ones((4, 1))
det_formula = 1.0 + 3.0 * (x.T @ x)[0, 0]  # 1 + 3 * 4 = 13.0
det_numerical = np.linalg.det(np.eye(4) + 3.0 * (x @ x.T))
print(f"Rank-1 Update Det: Formula={det_formula}, NumPy={det_numerical:.2f}")
assert np.isclose(det_formula, det_numerical)

# (3) Block Determinant with Commuting Blocks: det([[A, B], [B, A]]) == det(A - B) * det(A + B)
A = np.array([[3.0, 1.0], [1.0, 3.0]])
B = np.array([[1.0, 0.0], [0.0, 1.0]])
M = np.block([[A, B], [B, A]])
det_M = np.linalg.det(M)
det_factor = np.linalg.det(A - B) * np.linalg.det(A + B)
print(f"det(M)={det_M:.2f}, det(A-B)*det(A+B)={det_factor:.2f}")
assert np.isclose(det_M, det_factor)
#+end_src

* Chapter 5 Solutions: Inverses

#+begin_src python
# (1) Inverse of 2x2 matrix
A1 = np.array([[12.0, 7.0], [-4.0, 6.0]])
inv_A1 = np.linalg.inv(A1)
print("A1^{-1}:\n", inv_A1)
assert np.allclose(A1 @ inv_A1, np.eye(2))

# (2) Householder Reflector: A = I - 2 x x^T with x^T x = 1
x = np.array([[0.6], [0.8]])  # x^T x = 0.36 + 0.64 = 1
A_house = np.eye(2) - 2 * (x @ x.T)
print("Householder matrix A:\n", A_house)
print("A @ A:\n", A_house @ A_house)
assert np.allclose(A_house @ A_house, np.eye(2))  # A is symmetric orthogonal -> A^{-1} = A

# (3) Equicorrelation Inverse Formula
alpha, beta, n = 3.0, 1.5, 4
E = alpha * np.eye(n) + beta * np.ones((n, n))
E_inv_formula = (1.0 / alpha) * np.eye(n) - (beta / (alpha * (alpha + n * beta))) * np.ones((n, n))
assert np.allclose(np.linalg.inv(E), E_inv_formula)
print("Equicorrelation matrix inverse verified.")
#+end_src

* Chapter 6 Solutions: Eigenanalysis

#+begin_src python
# (1) Eigendecomposition of [[2, 1], [1, 2]]
A = np.array([[2.0, 1.0], [1.0, 2.0]])
# Characteristic eq: (2 - lambda)^2 - 1 = 0 -> lambda^2 - 4 lambda + 3 = 0 -> (lambda - 3)(lambda - 1) = 0
evals, evecs = np.linalg.eigh(A)
print("Eigenvalues:", evals)  # [1., 3.]
print("Eigenvectors:\n", evecs)

# (2) Rank-1 Matrix xx^T Eigenvalues
x = np.array([1.0, 2.0, 3.0])
R1 = np.outer(x, x)
evals_R1 = np.linalg.eigvalsh(R1)
print("Eigenvalues of xx^T:", evals_R1)  # [0., 0., 14.]
assert np.isclose(evals_R1[-1], x @ x)

# (3) PCA on Covariance Matrix S = [[25, -2], [-2, 4]]
S = np.array([[25.0, -2.0], [-2.0, 4.0]])
evals_S, evecs_S = np.linalg.eigh(S)
# Order descending
idx = np.argsort(evals_S)[::-1]
evals_S, evecs_S = evals_S[idx], evecs_S[:, idx]

total_var = np.trace(S)
var_pc1 = evals_S[0] / total_var
print("PCA Eigenvalues:", evals_S)
print(f"PC1 explains {var_pc1 * 100:.2f}% of total variance")
print("PC1 Loadings:", evecs_S[:, 0])
#+end_src

* Chapter 7 Solutions: Vector and Matrix Calculus

#+begin_src python
# (1) Normal Equations Derivation Verification
# f(x) = (y - Xx)^T (y - Xx)
# df/dx = -2 X^T (y - Xx) = 0 => X^T X x = X^T y
X = np.array([[1.0, 1.0], [1.0, 2.0], [1.0, 3.0]])
y = np.array([2.0, 4.0, 5.0])
beta_hat = np.linalg.solve(X.T @ X, X.T @ y)
print("OLS solution beta_hat:", beta_hat)

# (2) Rayleigh Quotient Extrema
A = np.array([[5.0, 2.0], [2.0, 2.0]])
evals, evecs = np.linalg.eigh(A)
print(f"Min Rayleigh quotient: {evals[0]:.4f} at {evecs[:, 0]}")
print(f"Max Rayleigh quotient: {evals[1]:.4f} at {evecs[:, 1]}")
#+end_src

* Chapter 8 Solutions: Further Topics

#+begin_src python
# (1) QR Decomposition Verification
A = np.array([[1.0, 2.0], [2.0, 1.0], [1.0, 1.0]])
Q, R = np.linalg.qr(A)
print("Q^T Q:\n", np.round(Q.T @ Q, 6))
assert np.allclose(Q.T @ Q, np.eye(2))
assert np.allclose(Q @ R, A)
print("QR verified.")

# (2) Cholesky Factorization: V = L @ L.T
V = np.array([[4.0, 2.0], [2.0, 10.0]])
L = np.linalg.cholesky(V)
print("Cholesky factor L:\n", L)
assert np.allclose(L @ L.T, V)

# (3) Kronecker Determinant Identity: det(A kron B) == (det A)^q * (det B)^p
A = np.array([[1.0, 2.0], [3.0, 4.0]])
B = np.array([[2.0, 0.0], [1.0, 3.0]])
kron_AB = np.kron(A, B)
det_direct = np.linalg.det(kron_AB)
det_formula = (np.linalg.det(A) ** 2) * (np.linalg.det(B) ** 2)
print(f"Direct det(A kron B): {det_direct:.2f}, Formula: {det_formula:.2f}")
assert np.isclose(det_direct, det_formula)
#+end_src

* Chapter 9 Solutions: Key Applications to Statistics

#+begin_src python
# (1) One-Sample Hotelling's T^2 Test
n = 20
p = 2
xbar = np.array([1.5, 2.0])
mu0 = np.array([1.0, 1.0])
S = np.array([[2.0, 0.5], [0.5, 1.0]])

diff = xbar - mu0
T2 = n * (diff.T @ np.linalg.solve(S, diff))
F_stat = ((n - p) / ((n - 1) * p)) * T2
p_value = 1.0 - stats.f.cdf(F_stat, p, n - p)

print(f"Hotelling T2: {T2:.4f}, F-stat: {F_stat:.4f}, p-value: {p_value:.6f}")
print("Reject H0 at alpha=0.05?", p_value < 0.05)

# (2) Classical MDS Coordinate Recovery
D = np.array([
    [0.0, 1.0, 2.0],
    [1.0, 0.0, 1.0],
    [2.0, 1.0, 0.0]
])
n = 3
H = np.eye(n) - np.ones((n, n)) / n
B = -0.5 * H @ (D ** 2) @ H
evals, evecs = np.linalg.eigh(B)
idx = np.argsort(evals)[::-1]
evals, evecs = evals[idx], evecs[:, idx]
coords_1d = evecs[:, :1] * np.sqrt(evals[0])
print("Recovered 1D Coordinates from MDS:\n", coords_1d - coords_1d[0])
# Distance between points is 1.0 and 2.0 as expected!
#+end_src
"""

def main():
    Path("bin/ch10_outline_solutions.org").write_text(CH10, encoding="utf-8")
    print("Wrote bin/ch10_outline_solutions.org")

if __name__ == "__main__":
    main()
