#!/usr/bin/env python3
"""Generates writings/ch04_determinants.org, writings/ch05_inverses.org, and writings/ch06_eigenanalysis.org."""

from pathlib import Path

CH04 = r""":PROPERTIES:
:ID:       0192e4b3-0004-7000-8000-000000000004
:ROAM_ALIASES: "Chapter 4: Determinants" "Schur Complement Determinant" "Weinstein-Aronszajn Identity"
:END:
#+title: Chapter 04: Determinants
#+subtitle: Laplace Expansions, Block Determinants, Schur Complements, and Rank-1 Updates
#+author: Antigravity Notes
#+date: [2026-10-04]
#+filetags: :matrix-algebra:determinants:schur-complement:rank-1-update:slogdet:

[[id:0192e4b3-0003-7000-8000-000000000003][← Previous: Chapter 03 (Rank of Matrices)]] | [[id:0192e4b3-0000-7000-8000-000000000000][Master Index]] | [[id:0192e4b3-0005-7000-8000-000000000005][Next: Chapter 05 (Inverses) →]]

* Definitions & Geometric Meaning

The determinant $\det(A)$ (or $|A|$) is a scalar-valued function defined for square $n \times n$ matrices:
\begin{equation}
\det(A) = \sum_{j=1}^n a_{ij} C_{ij}
\end{equation}
where $C_{ij} = (-1)^{i+j} M_{ij}$ is the *cofactor* of entry $a_{ij}$, and $M_{ij}$ is the determinant of the $(n-1) \times (n-1)$ sub-matrix obtained by deleting row $i$ and column $j$.

** Geometric Interpretation
- In 2D: $\det(A)$ represents the signed area of the parallelogram spanned by the column vectors.
- In 3D: $\det(A)$ represents the signed volume of the parallelepiped.
- In $n$D: $\det(A)$ represents the hypervolume scaling factor under the linear map $x \mapsto Ax$.
- In statistics: $|\Sigma|$ is the *generalized variance* of a multivariate random vector.

* Core Algebraic Properties

1. *Identity:* $\det(I_n) = 1$.
2. *Transpose:* $\det(A^T) = \det(A)$.
3. *Multiplicativity:* $\det(AB) = \det(A) \det(B)$.
4. *Scalar Scaling:* $\det(c A) = c^n \det(A)$ for $A \in \mathbb{R}^{n \times n}$.
5. *Triangular Matrices:* If $T$ is upper or lower triangular, $\det(T) = \prod_{i=1}^n t_{ii}$.
6. *Elementary Row Operations:*
   - Interchanging two rows multiplies the determinant by $-1$.
   - Multiplying a row by scalar $c$ multiplies the determinant by $c$.
   - Adding a scalar multiple of one row to another leaves the determinant unchanged.
7. *Singularity:* $A$ is invertible $\iff \det(A) \ne 0 \iff \text{rank}(A) = n$.
8. *Orthogonal Matrices:* If $Q^T Q = I$, then $\det(Q)^2 = 1 \implies \det(Q) = \pm 1$.

* Determinants of Partitioned Matrices

Let $M$ be partitioned into blocks:
\begin{equation}
M = \begin{pmatrix} A & B \\ C & D \end{pmatrix}
\end{equation}

** Block Triangular Matrices
If $C = 0$ (or $B = 0$):
\begin{equation}
\det \begin{pmatrix} A & B \\ 0 & D \end{pmatrix} = \det(A) \det(D)
\end{equation}

** Schur Complement Determinant Formulas
If $A$ is non-singular, we can factor $M$ via block Gaussian elimination:
\begin{equation}
\begin{pmatrix} A & B \\ C & D \end{pmatrix} = \begin{pmatrix} I & 0 \\ C A^{-1} & I \end{pmatrix} \begin{pmatrix} A & 0 \\ 0 & D - C A^{-1} B \end{pmatrix} \begin{pmatrix} I & A^{-1} B \\ 0 & I \end{pmatrix}
\end{equation}
Taking determinants yields:
\begin{equation}
\det(M) = \det(A) \det(D - C A^{-1} B)
\end{equation}
The matrix $S_A = D - C A^{-1} B$ is called the *Schur complement of $A$ in $M$*.
Similarly, if $D$ is non-singular:
\begin{equation}
\det(M) = \det(D) \det(A - B D^{-1} C)
\end{equation}

* The Fundamental Determinant Identity & Rank-1 Updates

** Weinstein-Aronszajn Identity
For any matrices $A \in \mathbb{R}^{p \times q}$ and $B \in \mathbb{R}^{q \times p}$:
\begin{equation}
\det(I_p + AB) = \det(I_q + BA)
\end{equation}
*Proof:* Consider the block matrix $M = \begin{pmatrix} I_p & -A \\ B & I_q \end{pmatrix}$. Applying the Schur complement with respect to $I_p$ gives $\det(M) = \det(I_p)\det(I_q - B(-I_p)^{-1}(-A)) = \det(I_q + BA)$. Applying Schur complement with respect to $I_q$ gives $\det(M) = \det(I_q)\det(I_p - (-A)(I_q)^{-1}B) = \det(I_p + AB)$. Equating them yields the identity.

** Rank-1 Determinant Update Formula
Let $A \in \mathbb{R}^{n \times n}$ be non-singular, and let $x, y \in \mathbb{R}^n$.
\begin{equation}
\det(A + x y^T) = \det(A(I_n + A^{-1} x y^T)) = \det(A) \det(I_n + (A^{-1} x) y^T)
\end{equation}
Applying the Weinstein-Aronszajn identity where $A^{-1}x$ is $n \times 1$ and $y^T$ is $1 \times n$:
\begin{equation}
\det(I_n + (A^{-1} x) y^T) = \det(I_1 + y^T (A^{-1} x)) = 1 + y^T A^{-1} x
\end{equation}
Therefore:
\begin{equation}
\det(A + x y^T) = \det(A) (1 + y^T A^{-1} x)
\end{equation}

** Special Cases
1. *When $A = I_n$:*
   \begin{equation}
   \det(I_n + x y^T) = 1 + y^T x
   \end{equation}
2. *Equicorrelation Matrix:* Let $E_n = \alpha I_n + \beta \mathbf{1}_n \mathbf{1}_n^T$.
   \begin{equation}
   \det(\alpha I_n + \beta \mathbf{1} \mathbf{1}^T) = \alpha^n \left(1 + \frac{\beta}{\alpha} \mathbf{1}^T \mathbf{1}\right) = \alpha^n \left(1 + \frac{n\beta}{\alpha}\right) = \alpha^{n-1} (\alpha + n\beta)
   \end{equation}

* Numerical Python Implementation & Best Practices

#+begin_src python
import numpy as np

# 1. Standard Determinant
G = np.array([
    [1.0, -2.0,  2.0],
    [2.0,  0.0,  1.0],
    [1.0,  1.0, -2.0]
])
det_G = np.linalg.det(G)
print("det(G):", det_G)  # -7.0

# 2. Critical Statistical Practice: np.linalg.slogdet
# For large sample covariance matrices, det(Sigma) can underflow to 0.0
# slogdet returns (sign, log(abs(det)))
sign, logdet = np.linalg.slogdet(G)
print(f"Sign: {sign}, Log-Determinant: {logdet:.4f}, exp(logdet)*sign = {sign * np.exp(logdet):.2f}")

# 3. Verification of Rank-1 Update: det(A + x y^T) == det(A) * (1 + y^T A^{-1} x)
A = np.array([[3.0, 1.0], [1.0, 2.0]])
x = np.array([[2.0], [1.0]])
y = np.array([[1.0], [3.0]])

det_direct = np.linalg.det(A + x @ y.T)
A_inv = np.linalg.inv(A)
det_formula = np.linalg.det(A) * (1.0 + (y.T @ A_inv @ x)[0, 0])

print("Direct det(A + x y^T):", det_direct)
print("Formula det(A)(1 + y^T A^{-1} x):", det_formula)
assert np.isclose(det_direct, det_formula)

# 4. Equicorrelation Matrix Determinant
alpha, beta, n = 4.0, 2.0, 5
En = alpha * np.eye(n) + beta * np.ones((n, n))
expected_det = (alpha ** (n - 1)) * (alpha + n * beta)
print("Computed det(E_n):", np.linalg.det(En))
print("Expected formula:", expected_det)
assert np.isclose(np.linalg.det(En), expected_det)
#+end_src

* Chapter 04 Exercises

1. *Exercise 4.1:* Compute the determinant of $G = \begin{pmatrix} 1 & 2 & 3 \\ 0 & 4 & 5 \\ 0 & 0 & 6 \end{pmatrix}$ by hand using the triangular property, and verify with NumPy.
2. *Exercise 4.2:* Use the rank-1 determinant formula to evaluate $\det(I_4 + 3 x x^T)$ where $x = (1, 1, 1, 1)^T$.
3. *Exercise 4.3:* Let $M = \begin{pmatrix} A & B \\ B^T & A \end{pmatrix}$ where $A, B$ are $k \times k$ symmetric and commute ($AB = BA$). Show that $\det(M) = \det(A - B)\det(A + B)$.
"""

CH05 = r""":PROPERTIES:
:ID:       0192e4b3-0005-7000-8000-000000000005
:ROAM_ALIASES: "Chapter 5: Inverses" "Sherman-Morrison Formula" "Block Matrix Inversion" "Banachiewicz Formula"
:END:
#+title: Chapter 05: Inverses
#+subtitle: Inverses of Regular, Patterned, and Partitioned Matrices
#+author: Antigravity Notes
#+date: [2026-10-04]
#+filetags: :matrix-algebra:inverses:sherman-morrison:block-inversion:condition-number:

[[id:0192e4b3-0004-7000-8000-000000000004][← Previous: Chapter 04 (Determinants)]] | [[id:0192e4b3-0000-7000-8000-000000000000][Master Index]] | [[id:0192e4b3-0006-7000-8000-000000000006][Next: Chapter 06 (Eigenanalysis) →]]

* Definition & Fundamental Properties

A square matrix $A \in \mathbb{R}^{n \times n}$ is invertible (non-singular) if there exists a matrix $A^{-1}$ such that:
\begin{equation}
A A^{-1} = A^{-1} A = I_n
\end{equation}
$A^{-1}$ exists if and only if $\det(A) \ne 0 \iff \text{rank}(A) = n$.

** Key Properties
1. *Uniqueness:* The inverse is unique.
2. *Inverse of Inverse:* $(A^{-1})^{-1} = A$.
3. *Transpose:* $(A^T)^{-1} = (A^{-1})^T$.
4. *Determinant:* $\det(A^{-1}) = \frac{1}{\det(A)}$.
5. *Product Rule:* $(AB)^{-1} = B^{-1} A^{-1}$. For $k$ matrices:
   \begin{equation}
   (A_1 A_2 \dots A_k)^{-1} = A_k^{-1} \dots A_2^{-1} A_1^{-1}
   \end{equation}
6. *Orthogonal Matrix:* If $Q^TQ = I$, then $Q^{-1} = Q^T$.
7. *Rank Preservation:* If $A$ is non-singular, $\text{rank}(AB) = \text{rank}(B)$ and $\text{rank}(CA) = \text{rank}(C)$.

* One-Sided Inverses for Rectangular Matrices

Let $A \in \mathbb{R}^{m \times n}$.
1. *Left Inverse ($m > n$, full column rank):*
   $A^T A \in \mathbb{R}^{n \times n}$ is non-singular. The *left inverse* $A_L \in \mathbb{R}^{n \times m}$ is:
   \begin{equation}
   A_L = (A^T A)^{-1} A^T \implies A_L A = (A^T A)^{-1}(A^T A) = I_n
   \end{equation}
   This is the OLS projection operator in linear models: $\hat{\beta} = A_L y$.
2. *Right Inverse ($m < n$, full row rank):*
   $A A^T \in \mathbb{R}^{m \times m}$ is non-singular. The *right inverse* $A_R \in \mathbb{R}^{n \times m}$ is:
   \begin{equation}
   A_R = A^T (A A^T)^{-1} \implies A A_R = (A A^T)(A A^T)^{-1} = I_m
   \end{equation}

* Numerical Condition Numbers & Linear Solvers

The *condition number* of an invertible matrix $A$ (with respect to the 2-norm) is:
\begin{equation}
\kappa(A) = \|A\|_2 \|A^{-1}\|_2 = \frac{\sigma_{\max}(A)}{\sigma_{\min}(A)}
\end{equation}
- $\kappa(A) \ge 1$.
- If $\kappa(A) \approx 1$, $A$ is *well-conditioned*.
- If $\kappa(A) \gg 10^8$, $A$ is *ill-conditioned*, and numerical inversion loses roughly $\log_{10}(\kappa(A))$ digits of precision.
- *Rule:* Never write ~np.linalg.inv(A) @ b~; always write ~np.linalg.solve(A, b)~.

* Inverses of Patterned Matrices

** 1. Equicorrelation Matrices
Matrices of the form $\alpha I_n + \beta \mathbf{1}_n \mathbf{1}_n^T$ with $\alpha \ne 0$ and $\alpha + n\beta \ne 0$:
\begin{equation}
(\alpha I_n + \beta \mathbf{1}_n \mathbf{1}_n^T)^{-1} = \frac{1}{\alpha} I_n - \frac{\beta}{\alpha(\alpha + n\beta)} \mathbf{1}_n \mathbf{1}_n^T
\end{equation}

** 2. The Sherman-Morrison Formula (Rank-1 Update Inverse)
Let $A \in \mathbb{R}^{n \times n}$ be invertible, and $x, y \in \mathbb{R}^n$. If $1 + y^T A^{-1} x \ne 0$, then:
\begin{equation}
(A + x y^T)^{-1} = A^{-1} - \frac{A^{-1} x y^T A^{-1}}{1 + y^T A^{-1} x}
\end{equation}
This allows $O(n^2)$ updating of matrix inverses upon receiving a new data point, avoiding $O(n^3)$ recomputation.

** 3. The Woodbury Matrix Identity (Rank-$k$ Update)
For matrices $A \in \mathbb{R}^{n \times n}$, $U \in \mathbb{R}^{n \times k}$, $C \in \mathbb{R}^{k \times k}$, and $V \in \mathbb{R}^{k \times n}$:
\begin{equation}
(A + U C V)^{-1} = A^{-1} - A^{-1} U (C^{-1} + V A^{-1} U)^{-1} V A^{-1}
\end{equation}

* Inverses of Partitioned Matrices (Banachiewicz Inversion Formula)

Let $M = \begin{pmatrix} A & B \\ C & D \end{pmatrix}$. If $A$ is non-singular and the Schur complement $S = D - C A^{-1} B$ is non-singular:
\begin{equation}
\begin{pmatrix} A & B \\ C & D \end{pmatrix}^{-1} = \begin{pmatrix} A^{-1} + A^{-1} B S^{-1} C A^{-1} & -A^{-1} B S^{-1} \\ -S^{-1} C A^{-1} & S^{-1} \end{pmatrix}
\end{equation}
Similarly, if $D$ is non-singular with Schur complement $T = A - B D^{-1} C$:
\begin{equation}
\begin{pmatrix} A & B \\ C & D \end{pmatrix}^{-1} = \begin{pmatrix} T^{-1} & -T^{-1} B D^{-1} \\ -D^{-1} C T^{-1} & D^{-1} + D^{-1} C T^{-1} B D^{-1} \end{pmatrix}
\end{equation}

** Statistical Consequence: Conditional Covariance
If $(X_1, X_2)^T \sim N\left(\begin{pmatrix} \mu_1 \\ \mu_2 \end{pmatrix}, \begin{pmatrix} \Sigma_{11} & \Sigma_{12} \\ \Sigma_{21} & \Sigma_{22} \end{pmatrix}\right)$, the precision matrix is $\Sigma^{-1}$. The bottom-right block of $\Sigma^{-1}$ is:
\begin{equation}
(\Sigma_{22} - \Sigma_{21} \Sigma_{11}^{-1} \Sigma_{12})^{-1} = (\text{Cov}(X_2 \mid X_1))^{-1}
\end{equation}
The Schur complement represents the conditional covariance of $X_2$ given $X_1$!

* Numerical Python Implementation

#+begin_src python
import numpy as np

# 1. Solving Ax = b vs Inverting
A = np.array([[3.0, 1.0], [1.0, 2.0]])
b = np.array([9.0, 8.0])

x_solve = np.linalg.solve(A, b)
print("Solution via np.linalg.solve:", x_solve)  # [2. 3.]

# Condition number
cond_A = np.linalg.cond(A)
print("Condition number kappa(A):", cond_A)

# 2. Sherman-Morrison Formula Verification
x = np.array([[1.0], [2.0]])
y = np.array([[3.0], [1.0]])

# Direct inverse
inv_direct = np.linalg.inv(A + x @ y.T)

# Formula inverse
A_inv = np.linalg.inv(A)
denom = 1.0 + (y.T @ A_inv @ x)[0, 0]
inv_formula = A_inv - (A_inv @ x @ y.T @ A_inv) / denom

print("Direct (A + xy^T)^{-1}:\n", inv_direct)
print("Sherman-Morrison formula:\n", inv_formula)
assert np.allclose(inv_direct, inv_formula)

# 3. Equicorrelation Inverse Verification
alpha, beta, n = 5.0, 2.0, 4
En = alpha * np.eye(n) + beta * np.ones((n, n))
inv_En_formula = (1.0 / alpha) * np.eye(n) - (beta / (alpha * (alpha + n * beta))) * np.ones((n, n))
assert np.allclose(np.linalg.inv(En), inv_En_formula)
print("Equicorrelation formula matches np.linalg.inv exactly.")
#+end_src

* Chapter 05 Exercises

1. *Exercise 5.1:* Prove that for non-singular matrices $X, Y$, $(X + Y)^{-1} = X^{-1}(X^{-1} + Y^{-1})^{-1} Y^{-1}$.
2. *Exercise 5.2:* Suppose $A = I_n - 2 x x^T$ where $x^T x = 1$ (Householder reflector matrix). Show algebraically that $A^{-1} = A$. Verify numerically in NumPy.
3. *Exercise 5.3:* For partitioned matrix $M = \begin{pmatrix} 2 & 1 & 0 \\ 1 & 3 & 1 \\ 0 & 1 & 2 \end{pmatrix}$, compute the Schur complement of $A = \begin{pmatrix} 2 & 1 \\ 1 & 3 \end{pmatrix}$ and invert $M$ using the Banachiewicz block formula.
"""

CH06 = r""":PROPERTIES:
:ID:       0192e4b3-0006-7000-8000-000000000006
:ROAM_ALIASES: "Chapter 6: Eigenanalysis" "Spectral Theorem" "Singular Value Decomposition" "PCA Foundations"
:END:
#+title: Chapter 06: Eigenanalysis of Real Symmetric Matrices
#+subtitle: Eigendecompositions, Spectral Theorem, Matrix Functions, SVD, and PCA
#+author: Antigravity Notes
#+date: [2026-10-04]
#+filetags: :matrix-algebra:eigenanalysis:spectral-decomposition:svd:matrix-exponential:pca:

[[id:0192e4b3-0005-7000-8000-000000000005][← Previous: Chapter 05 (Inverses)]] | [[id:0192e4b3-0000-7000-8000-000000000000][Master Index]] | [[id:0192e4b3-0007-7000-8000-000000000007][Next: Chapter 07 (Vector and Matrix Calculus) →]]

* Definitions & Characteristic Equation

Let $A \in \mathbb{R}^{n \times n}$. A non-zero vector $x \in \mathbb{C}^n$ is an *eigenvector* of $A$ with associated *eigenvalue* $\lambda \in \mathbb{C}$ if:
\begin{equation}
A x = \lambda x \iff (A - \lambda I_n) x = \mathbf{0}
\end{equation}
Since $x \ne \mathbf{0}$, the matrix $(A - \lambda I_n)$ must be singular, leading to the *characteristic equation*:
\begin{equation}
p(\lambda) = \det(A - \lambda I_n) = 0
\end{equation}
This is an $n$-th degree polynomial with $n$ roots $\lambda_1, \dots, \lambda_n$ (counted with algebraic multiplicity).

* Eigenanalysis of Real Symmetric Matrices

In statistics, most matrices of interest (covariance matrices $\Sigma$, correlation matrices $R$, scatter matrices $S$, hat matrices $P$) are real and symmetric ($A = A^T$).

** The Spectral Theorem
Let $A \in \mathbb{R}^{n \times n}$ be a real symmetric matrix.
1. *Real Roots:* All eigenvalues $\lambda_1, \dots, \lambda_n$ are strictly real.
2. *Orthogonality:* Eigenvectors corresponding to distinct eigenvalues are mutually orthogonal:
   \begin{equation}
   \lambda_i \ne \lambda_j \implies x_i^T x_j = 0
   \end{equation}
3. *Orthonormal Basis:* There exists an orthogonal matrix $P \in \mathbb{R}^{n \times n}$ ($P^T P = P P^T = I$) whose columns $p_1, \dots, p_n$ are orthonormal eigenvectors:
   \begin{equation}
   P = (p_1, p_2, \dots, p_n), \quad \Lambda = \text{diag}(\lambda_1, \lambda_2, \dots, \lambda_n)
   \end{equation}
4. *Spectral Decomposition:*
   \begin{equation}
   A = P \Lambda P^T = \sum_{i=1}^n \lambda_i p_i p_i^T
   \end{equation}
   Each $p_i p_i^T$ is a symmetric idempotent rank-1 projection matrix onto the $i$-th eigenspace.

* Trace, Determinant, and Rank Relations

From the spectral decomposition $A = P \Lambda P^T$:
1. *Trace:* $\text{tr}(A) = \text{tr}(P \Lambda P^T) = \text{tr}(\Lambda P^T P) = \text{tr}(\Lambda) = \sum_{i=1}^n \lambda_i$.
2. *Determinant:* $\det(A) = \det(P) \det(\Lambda) \det(P^T) = \det(\Lambda) = \prod_{i=1}^n \lambda_i$.
3. *Rank:* For symmetric matrices, $\text{rank}(A)$ equals the number of non-zero eigenvalues.

* Matrix Functions via Spectral Decomposition

Let $f: \mathbb{R} \to \mathbb{R}$ be any analytic function. For symmetric $A = P \Lambda P^T$:
\begin{equation}
f(A) = P f(\Lambda) P^T = P \begin{pmatrix} f(\lambda_1) & & 0 \\ & \ddots & \\ 0 & & f(\lambda_n) \end{pmatrix} P^T = \sum_{i=1}^n f(\lambda_i) p_i p_i^T
\end{equation}

** Examples
1. *Powers:* $A^k = P \Lambda^k P^T$.
2. *Inverse:* $A^{-1} = P \Lambda^{-1} P^T$ (valid when all $\lambda_i \ne 0$).
3. *Matrix Square Root:* For positive semi-definite $A$ ($\lambda_i \ge 0$):
   \begin{equation}
   A^{1/2} = P \Lambda^{1/2} P^T = P \text{diag}(\sqrt{\lambda_1}, \dots, \sqrt{\lambda_n}) P^T
   \end{equation}
   Satisfies $A^{1/2} A^{1/2} = A$. Essential for Mahalanobis whitening: $Z = \Sigma^{-1/2}(X - \mu)$.
4. *Matrix Exponential:*
   \begin{equation}
   \exp(A) = \sum_{k=0}^\infty \frac{A^k}{k!} = P \text{diag}(e^{\lambda_1}, \dots, e^{\lambda_n}) P^T
   \end{equation}

* Singular Value Decomposition (SVD)

For *any* real rectangular matrix $A \in \mathbb{R}^{m \times n}$:
\begin{equation}
A = U \Sigma V^T
\end{equation}
- $U \in \mathbb{R}^{m \times m}$ is orthogonal ($U^T U = I_m$), columns are eigenvectors of $A A^T$.
- $V \in \mathbb{R}^{n \times n}$ is orthogonal ($V^T V = I_n$), columns are eigenvectors of $A^T A$.
- $\Sigma \in \mathbb{R}^{m \times n}$ is diagonal with non-negative entries $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_r > 0$ (the *singular values*).
- $\sigma_i = \sqrt{\lambda_i(A^T A)} = \sqrt{\lambda_i(A A^T)}$.
- *Eckart-Young Theorem:* The optimal rank-$k$ approximation of $A$ under the Frobenius norm is:
  \begin{equation}
  A_k = \sum_{i=1}^k \sigma_i u_i v_i^T
  \end{equation}

* Eigenanalysis of Special Patterned Structures

1. *The Rank-1 Matrix $x x^T$:*
   - Let $x \in \mathbb{R}^n$ with $\|x\|_2^2 = x^T x$.
   - $x x^T (x) = x (x^T x) = (x^T x) x$.
   - Eigenvalues: $\lambda_1 = x^T x = \|x\|_2^2$ (with eigenvector $x$), and $\lambda_2 = \dots = \lambda_n = 0$.
2. *The Matrix $S x x^T$:*
   - Non-zero eigenvalue is $x^T S x$.
3. *The Matrix $a I_n + b x y^T$:*
   - Eigenvalues: $a + b y^T x$ (multiplicity 1) and $a$ (multiplicity $n-1$).

* Statistical Cornerstone: Principal Component Analysis (PCA)

Given sample covariance matrix $S \in \mathbb{R}^{p \times p}$ (symmetric positive semi-definite):
1. We seek linear combination $y_1 = a_1^T x$ that maximizes $\text{Var}(y_1) = a_1^T S a_1$ subject to $a_1^T a_1 = 1$.
2. Rayleigh quotient optimization yields:
   \begin{equation}
   S a_1 = \lambda_1 a_1
   \end{equation}
3. The loadings $a_1, \dots, a_p$ are precisely the orthonormal eigenvectors of $S$, ordered by $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_p \ge 0$.
4. Total variance explained is $\sum_{i=1}^p \lambda_i = \text{tr}(S)$.
5. Proportion of variance explained by $k$ components is $\frac{\sum_{i=1}^k \lambda_i}{\text{tr}(S)}$.

* Numerical Python Implementation

#+begin_src python
import numpy as np
import scipy.linalg as la

# 1. Symmetric Eigenanalysis with np.linalg.eigh
S = np.array([
    [4.0, 2.0],
    [2.0, 3.0]
])

evals, evecs = np.linalg.eigh(S)
print("Eigenvalues (ascending):", evals)
print("Eigenvectors (columns):\n", evecs)

# Verify spectral reconstruction: P @ diag(evals) @ P.T == S
S_rec = evecs @ np.diag(evals) @ evecs.T
assert np.allclose(S, S_rec)
print("Spectral decomposition verified.")

# 2. Matrix Square Root: S^{1/2}
S_sqrt = evecs @ np.diag(np.sqrt(evals)) @ evecs.T
print("Matrix square root S^{1/2}:\n", S_sqrt)
assert np.allclose(S_sqrt @ S_sqrt, S)

# 3. Matrix Exponential: expm(S)
S_exp_formula = evecs @ np.diag(np.exp(evals)) @ evecs.T
S_exp_scipy = la.expm(S)
assert np.allclose(S_exp_formula, S_exp_scipy)
print("Matrix exponential verified against scipy.linalg.expm.")

# 4. Singular Value Decomposition (SVD)
A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
U, s, Vt = np.linalg.svd(A, full_matrices=False)
print("Singular values of A:", s)
# Verify singular values match sqrt of eigenvalues of A @ A.T
evals_AAt = np.linalg.eigvalsh(A @ A.T)
print("sqrt(evals(A @ A.T)):", np.sqrt(np.sort(evals_AAt)[::-1]))
assert np.allclose(s, np.sqrt(np.sort(evals_AAt)[::-1]))
#+end_src

* Chapter 06 Exercises

1. *Exercise 6.1:* Compute eigenvalues and eigenvectors of $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ by hand using the characteristic polynomial. Verify with NumPy ~np.linalg.eigh~.
2. *Exercise 6.2:* For $x = (1, 2, 3)^T$, construct $A = x x^T$. Predict its eigenvalues analytically and verify numerically.
3. *Exercise 6.3:* For covariance matrix $S = \begin{pmatrix} 25 & -2 \\ -2 & 4 \end{pmatrix}$, compute the principal component loadings and the percentage of total variance explained by the first component.
"""

def main():
    Path("writings").mkdir(parents=True, exist_ok=True)
    Path("writings/ch04_determinants.org").write_text(CH04, encoding="utf-8")
    print("Wrote writings/ch04_determinants.org")
    Path("writings/ch05_inverses.org").write_text(CH05, encoding="utf-8")
    print("Wrote writings/ch05_inverses.org")
    Path("writings/ch06_eigenanalysis.org").write_text(CH06, encoding="utf-8")
    print("Wrote writings/ch06_eigenanalysis.org")

if __name__ == "__main__":
    main()
