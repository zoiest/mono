#!/usr/bin/env python3
"""Generates bin/ch07_vector_and_matrix_calculus.org, bin/ch08_further_topics.org, and bin/ch09_key_applications_to_statistics.org."""

from pathlib import Path

CH07 = r""":PROPERTIES:
:ID:       0192e4b3-0007-7000-8000-000000000007
:ROAM_ALIASES: "Chapter 7: Vector and Matrix Calculus" "Matrix Calculus" "Lagrange Multipliers" "Rayleigh Quotient"
:END:
#+title: Chapter 07: Vector and Matrix Calculus
#+subtitle: Gradients of Linear Forms, Quadratic Forms, Matrix Derivatives, and Constrained Optimization
#+author: Antigravity Notes
#+date: [2026-10-04]
#+filetags: :matrix-calculus:derivatives:gradients:lagrange-multipliers:rayleigh-quotient:optimization:

[[id:0192e4b3-0006-7000-8000-000000000006][← Previous: Chapter 06 (Eigenanalysis)]] | [[id:0192e4b3-0000-7000-8000-000000000000][Master Index]] | [[id:0192e4b3-0008-7000-8000-000000000008][Next: Chapter 08 (Further Topics) →]]

* Motivation & Layout Conventions

In multivariate statistics, matrix calculus is essential for:
1. *Maximum Likelihood Estimation (MLE):* Finding parameter vectors $\hat{\beta}$ or covariance matrices $\hat{\Sigma}$ that maximize likelihood functions.
2. *Constructing Likelihood Ratio Tests:* Evaluating curvature via Fisher information matrices $\mathcal{I} = -E\left[\frac{\partial^2 \log L}{\partial \theta \partial \theta^T}\right]$.
3. *Constrained Optimization:* Deriving PCA, LDA, and CCA through Lagrange multipliers.

** Layout Convention
In this guide, we use the standard mathematical convention (denominator layout for vector derivatives):
For scalar $f(x)$ and vector $x = (x_1, \dots, x_p)^T$:
\begin{equation}
\frac{\partial f}{\partial x} = \begin{pmatrix} \frac{\partial f}{\partial x_1} \\ \vdots \\ \frac{\partial f}{\partial x_p} \end{pmatrix} \in \mathbb{R}^p
\end{equation}

* Differentiation of a Scalar with Respect to a Vector

** 1. Derivative of Linear Form $a^T x$
Let $f(x) = a^T x = \sum_{i=1}^p a_i x_i$. Then $\frac{\partial f}{\partial x_k} = a_k$. In vector form:
\begin{equation}
\frac{\partial (a^T x)}{\partial x} = a
\end{equation}
Similarly, $\frac{\partial (x^T a)}{\partial x} = a$.

** 2. Derivative of Sum of Squares $x^T x$
Let $f(x) = x^T x = \sum_{i=1}^p x_i^2$. Then $\frac{\partial f}{\partial x_k} = 2 x_k$. In vector form:
\begin{equation}
\frac{\partial (x^T x)}{\partial x} = 2x
\end{equation}

** 3. Derivative of Quadratic Form $x^T S x$
Let $f(x) = x^T S x = \sum_{i=1}^p \sum_{j=1}^p s_{ij} x_i x_j$.
\begin{equation}
\frac{\partial f}{\partial x_k} = \sum_{j=1}^p s_{kj} x_j + \sum_{i=1}^p s_{ik} x_i = (S x)_k + (S^T x)_k
\end{equation}
Therefore:
\begin{equation}
\frac{\partial (x^T S x)}{\partial x} = (S + S^T) x
\end{equation}
*Key Special Case:* If $S$ is *symmetric* ($S = S^T$), which is standard in statistics:
\begin{equation}
\frac{\partial (x^T S x)}{\partial x} = 2 S x
\end{equation}

* Differentiation of a Scalar with Respect to a Matrix

Let $f(X)$ be a scalar function of matrix $X = (x_{ij}) \in \mathbb{R}^{m \times n}$.
The derivative is the matrix whose $(i, j)$-th entry is $\frac{\partial f}{\partial x_{ij}}$:
\begin{equation}
\frac{\partial f}{\partial X} = \begin{pmatrix} \frac{\partial f}{\partial x_{11}} & \dots & \frac{\partial f}{\partial x_{1n}} \\ \vdots & \ddots & \vdots \\ \frac{\partial f}{\partial x_{m1}} & \dots & \frac{\partial f}{\partial x_{mn}} \end{pmatrix}
\end{equation}

** 1. Derivative of Trace $\text{tr}(X)$
$\text{tr}(X) = \sum_{i=1}^n x_{ii}$.
\begin{equation}
\frac{\partial \text{tr}(X)}{\partial X} = I_n
\end{equation}

** 2. Derivative of Bilinear Form $a^T X b$
$a^T X b = \sum_i \sum_j a_i x_{ij} b_j$.
\begin{equation}
\frac{\partial (a^T X b)}{\partial X} = a b^T
\end{equation}
In particular, $\frac{\partial (a^T X a)}{\partial X} = a a^T$.

** 3. Derivative of Trace of Product $\text{tr}(XA)$
- When $X$ is *unconstrained (non-symmetric):*
  \begin{equation}
  \frac{\partial \text{tr}(XA)}{\partial X} = A^T
  \end{equation}
- When $X$ is *symmetric ($X = X^T$):*
  \begin{equation}
  \frac{\partial \text{tr}(XA)}{\partial X} = A + A^T - \text{diag}(A)
  \end{equation}
  (often written simply as $A + A^T$ when off-diagonal symmetric differentials are handled).

** 4. Derivative of Quadratic Trace $\text{tr}(A^T X A)$
Using the cyclic trace property $\text{tr}(A^T X A) = \text{tr}(X A A^T)$:
\begin{equation}
\frac{\partial \text{tr}(A^T X A)}{\partial X} = A A^T
\end{equation}

** 5. Derivative of Determinant $\det(X)$
Using Jacobi's formula / Laplace cofactor expansion:
\begin{equation}
\frac{\partial \det(X)}{\partial X} = \det(X) (X^{-1})^T
\end{equation}
For symmetric $X$: $\frac{\partial \det(X)}{\partial X} = \det(X) X^{-1}$.

** 6. Derivative of Log-Determinant $\log \det(X)$ (Cornerstone of MLE)
Applying the chain rule:
\begin{equation}
\frac{\partial \log \det(X)}{\partial X} = \frac{1}{\det(X)} \frac{\partial \det(X)}{\partial X} = (X^{-1})^T
\end{equation}
For real symmetric positive-definite covariance matrix $\Sigma$:
\begin{equation}
\frac{\partial \log |\Sigma|}{\partial \Sigma} = \Sigma^{-1}
\end{equation}

* Constrained Optimization & Rayleigh Quotients

Many multivariate statistical methods involve maximizing a quadratic form subject to a normalization constraint.

** Problem Formulation
Maximize $x^T A x$ subject to $x^T B x = 1$, where $A, B$ are real symmetric matrices and $B$ is positive definite.
We set up the Lagrangian:
\begin{equation}
L(x, \lambda) = x^T A x - \lambda (x^T B x - 1)
\end{equation}
Differentiating with respect to $x$ and setting to zero:
\begin{equation}
\frac{\partial L}{\partial x} = 2 A x - 2 \lambda B x = \mathbf{0} \implies A x = \lambda B x
\end{equation}
This is the *generalized eigenvalue problem*!
Multiplying on the left by $x^T$:
\begin{equation}
x^T A x = \lambda x^T B x = \lambda (1) = \lambda
\end{equation}
Hence, the value of the objective function at the optimum is precisely the eigenvalue $\lambda$.
- *Maximum:* $\lambda_{\max}$, achieved at the corresponding eigenvector $x_{\max}$.
- *Minimum:* $\lambda_{\min}$, achieved at the corresponding eigenvector $x_{\min}$.

** Rayleigh Quotient
For $B = I$:
\begin{equation}
R_A(x) = \frac{x^T A x}{x^T x}
\end{equation}
\begin{equation}
\lambda_{\min}(A) \le \frac{x^T A x}{x^T x} \le \lambda_{\max}(A)
\end{equation}

* Numerical Python Verification

#+begin_src python
import numpy as np

# 1. Numerical Verification of Gradient of Quadratic Form: d(x^T S x)/dx == 2 S x
S = np.array([[3.0, 1.0], [1.0, 4.0]])
x = np.array([2.0, -1.0])

# Analytical gradient
grad_analytical = 2 * S @ x

# Numerical gradient via finite differences
eps = 1e-6
grad_numerical = np.zeros_like(x)
for i in range(len(x)):
    x_plus = x.copy()
    x_plus[i] += eps
    x_minus = x.copy()
    x_minus[i] -= eps
    f_plus = x_plus.T @ S @ x_plus
    f_minus = x_minus.T @ S @ x_minus
    grad_numerical[i] = (f_plus - f_minus) / (2 * eps)

print("Analytical gradient 2Sx:", grad_analytical)
print("Numerical gradient:", grad_numerical)
assert np.allclose(grad_analytical, grad_numerical, atol=1e-5)

# 2. Rayleigh Quotient Maximization Verification
evals, evecs = np.linalg.eigh(S)
max_lambda = evals[-1]
max_evec = evecs[:, -1]

# Value of Rayleigh quotient at leading eigenvector
R_max = (max_evec.T @ S @ max_evec) / (max_evec.T @ max_evec)
print(f"Max eigenvalue: {max_lambda:.4f}, Rayleigh quotient at leading eigenvector: {R_max:.4f}")
assert np.isclose(max_lambda, R_max)
#+end_src

* Chapter 07 Exercises

1. *Exercise 7.1:* Let $f(x) = (y - Xx)^T (y - Xx)$. Differentiate $f(x)$ with respect to $x$, set the result to zero, and derive the normal equations $X^T X x = X^T y$.
2. *Exercise 7.2:* For symmetric positive-definite matrix $\Sigma$ and constant matrix $A$, show that $\frac{\partial}{\partial \Sigma} \text{tr}(\Sigma^{-1} A) = -\Sigma^{-1} A \Sigma^{-1}$.
3. *Exercise 7.3:* Given $A = \begin{pmatrix} 5 & 2 \\ 2 & 2 \end{pmatrix}$, compute the maximum and minimum values of the Rayleigh quotient $R(x) = \frac{x^T A x}{x^T x}$, and find the vectors $x$ achieving these extrema.
"""

CH08 = r""":PROPERTIES:
:ID:       0192e4b3-0008-7000-8000-000000000008
:ROAM_ALIASES: "Chapter 8: Further Topics" "QR and Cholesky Decompositions" "Generalized Inverses" "Kronecker and Vec"
:END:
#+title: Chapter 08: Further Matrix Decompositions & Algebraic Operators
#+subtitle: QR, LU, Cholesky, Schur, Generalized Inverses, Hadamard, and Kronecker Products
#+author: Antigravity Notes
#+date: [2026-10-04]
#+filetags: :matrix-algebra:qr:cholesky:schur:pseudoinverse:kronecker:vec-operator:

[[id:0192e4b3-0007-7000-8000-000000000007][← Previous: Chapter 07 (Vector and Matrix Calculus)]] | [[id:0192e4b3-0000-7000-8000-000000000000][Master Index]] | [[id:0192e4b3-0009-7000-8000-000000000009][Next: Chapter 09 (Key Applications to Statistics) →]]

* Further Matrix Decompositions

** 1. QR Decomposition
Any real matrix $X \in \mathbb{R}^{n \times p}$ ($n \ge p$) can be factored as:
\begin{equation}
X = Q R
\end{equation}
- $Q \in \mathbb{R}^{n \times p}$ has orthonormal columns ($Q^T Q = I_p$).
- $R \in \mathbb{R}^{p \times p}$ is upper triangular.
- *Application to Ordinary Least Squares (OLS):*
  \begin{equation}
  X^T X = (QR)^T (QR) = R^T Q^T Q R = R^T R
  \end{equation}
  The normal equations $X^TX \beta = X^T y$ become:
  \begin{equation}
  R^T R \beta = R^T Q^T y \implies R \beta = Q^T y
  \end{equation}
  Since $R$ is upper triangular, $\hat{\beta}$ is solved via fast back-substitution without computing $X^TX$, preserving numerical stability ($\kappa(R) = \kappa(X) \ll \kappa(X^TX)$).

** 2. LU and LDU Decompositions
For square matrix $A \in \mathbb{R}^{n \times n}$:
\begin{equation}
P A = L U
\end{equation}
where $P$ is a permutation matrix, $L$ is unit lower triangular, and $U$ is upper triangular.

** 3. Cholesky Decomposition
For any real *symmetric positive-definite* matrix $A \in \mathbb{R}^{n \times n}$:
\begin{equation}
A = L L^T \quad (\text{NumPy convention: lower triangular } L)
\end{equation}
\begin{equation}
A = U^T U \quad (\text{R convention: upper triangular } U = L^T)
\end{equation}
- $L$ has strictly positive diagonal entries: $l_{ii} > 0$.
- Computing cost is $\frac{1}{3} n^3$ flops (half the cost of LU factorization).
- *Application to Multivariate Simulation:* To generate random vector $X \sim N_p(\mu, \Sigma)$:
  1. Compute Cholesky factor $\Sigma = L L^T$.
  2. Sample standard normal vector $Z \sim N_p(\mathbf{0}, I_p)$.
  3. Set $X = \mu + L Z$. Then $\text{Cov}(X) = L \text{Cov}(Z) L^T = L I L^T = \Sigma$.

** 4. Schur Decomposition
For any square matrix $A \in \mathbb{R}^{n \times n}$:
\begin{equation}
A = Q T Q^T
\end{equation}
where $Q$ is orthogonal and $T$ is upper quasi-triangular. The eigenvalues of $A$ appear on the diagonal blocks of $T$.

* Generalized Inverses

When a matrix $A \in \mathbb{R}^{m \times n}$ is singular or rectangular, the standard inverse does not exist.

** 1. Moore–Penrose Pseudoinverse $A^+$
The unique matrix $A^+ \in \mathbb{R}^{n \times m}$ satisfying all four Penrose conditions:
1. $A A^+ A = A$
2. $A^+ A A^+ = A^+$
3. $(A A^+)^T = A A^+$ (symmetric projector onto column space of $A$)
4. $(A^+ A)^T = A^+ A$ (symmetric projector onto row space of $A$)
- Computed via SVD: If $A = U \Sigma V^T$, then $A^+ = V \Sigma^+ U^T$ where $\Sigma^+$ reciprocates non-zero singular values.
- In NumPy: ~np.linalg.pinv(A)~.

** 2. Generalized Inverse $A^-$
Any matrix $A^-$ satisfying only the first condition:
\begin{equation}
A A^- A = A
\end{equation}
$A^-$ is not unique.
- *Solving Consistent Linear Systems $Ax = y$:*
  $Ax = y$ is consistent if and only if $A A^- y = y$.
  The general solution is:
  \begin{equation}
  x = A^- y + (I - A^- A) w
  \end{equation}
  for any arbitrary vector $w$.

* Hadamard Products (Elementwise Multiplication)

The Hadamard product of matrices $A, B \in \mathbb{R}^{m \times n}$ is:
\begin{equation}
(A \circ B)_{ij} = a_{ij} b_{ij}
\end{equation}
- *Schur Product Theorem:* If $A$ and $B$ are positive semi-definite, then their Hadamard product $A \circ B$ is also positive semi-definite.
- In NumPy: ~A * B~.

* Kronecker Products and the Vec Operator

** 1. Kronecker Product $A \otimes B$
For $A \in \mathbb{R}^{m \times n}$ and $B \in \mathbb{R}^{p \times q}$, the Kronecker product is the $(m p) \times (n q)$ block matrix:
\begin{equation}
A \otimes B = \begin{pmatrix} a_{11} B & \dots & a_{1n} B \\ \vdots & \ddots & \vdots \\ a_{m1} B & \dots & a_{mn} B \end{pmatrix}
\end{equation}
In NumPy: ~np.kron(A, B)~.

** Core Kronecker Properties
1. *Transpose:* $(A \otimes B)^T = A^T \otimes B^T$.
2. *Mixed Product Rule:* $(A \otimes B)(C \otimes D) = (AC) \otimes (BD)$ (provided dimensions conform).
3. *Inverse:* $(A \otimes B)^{-1} = A^{-1} \otimes B^{-1}$.
4. *Trace:* $\text{tr}(A \otimes B) = \text{tr}(A) \text{tr}(B)$.
5. *Determinant:* For $A_{m \times m}$ and $B_{n \times n}$:
   \begin{equation}
   \det(A \otimes B) = (\det A)^n (\det B)^m
   \end{equation}
6. *Eigenvalues:* If $\lambda_i$ are eigenvalues of $A$ and $\mu_j$ are eigenvalues of $B$, the $mn$ eigenvalues of $A \otimes B$ are $\lambda_i \mu_j$.

** 2. The Vec Operator $\text{vec}(A)$
The $\text{vec}$ operator stacks the columns of matrix $A \in \mathbb{R}^{m \times n}$ into an $(mn) \times 1$ column vector:
\begin{equation}
\text{vec}(A) = \begin{pmatrix} a_{*1} \\ a_{*2} \\ \vdots \\ a_{*n} \end{pmatrix}
\end{equation}
*NumPy Warning:* Since NumPy defaults to row-major, you must use ~A.flatten(order='F')~ to match column-major vectorization!

** 3. The Fundamental Kronecker-Vec Identity
For conformable matrices $A, B, C$:
\begin{equation}
\text{vec}(A B C) = (C^T \otimes A) \text{vec}(B)
\end{equation}
- *Special Case:* $\text{vec}(A B) = (I \otimes A) \text{vec}(B) = (B^T \otimes I) \text{vec}(A)$.
- *Trace-Vec Identity:* $\text{tr}(A^T B) = \text{vec}(A)^T \text{vec}(B)$.
- *Solving Matrix Equations:* The linear matrix equation $A X B = C$ transforms into standard linear system:
  \begin{equation}
  (B^T \otimes A) \text{vec}(X) = \text{vec}(C)
  \end{equation}

* Numerical Python Implementation

#+begin_src python
import numpy as np
import scipy.linalg as la

# 1. QR Decomposition in Least Squares
X = np.array([[1.0, 1.0], [1.0, 2.0], [1.0, 3.0], [1.0, 4.0]])
y = np.array([2.0, 3.0, 5.0, 7.0])

Q, R = np.linalg.qr(X)
# Solve R beta = Q.T @ y
beta_qr = np.linalg.solve(R, Q.T @ y)
beta_direct = np.linalg.inv(X.T @ X) @ X.T @ y
print("Beta via QR:", beta_qr)
assert np.allclose(beta_qr, beta_direct)

# 2. Cholesky Sampling for Correlated Gaussian Data
Sigma = np.array([[4.0, 1.2], [1.2, 1.0]])
L = np.linalg.cholesky(Sigma)  # Sigma = L @ L.T
np.random.seed(42)
Z = np.random.randn(2, 50000)
X_sim = (L @ Z).T  # Shape (50000, 2)
emp_cov = np.cov(X_sim, rowvar=False)
print("Empirical simulated covariance:\n", emp_cov)
assert np.allclose(Sigma, emp_cov, atol=0.05)

# 3. Kronecker Product and Vec Identity: vec(ABC) == (C.T kron A) @ vec(B)
A = np.array([[1.0, 2.0], [3.0, 4.0]])
B = np.array([[5.0, 6.0], [7.0, 8.0]])
C = np.array([[9.0, 1.0], [2.0, 3.0]])

ABC = A @ B @ C
vec_ABC = ABC.flatten(order='F')
kron_term = np.kron(C.T, A)
vec_formula = kron_term @ B.flatten(order='F')

print("vec(ABC):\n", vec_ABC)
print("(C.T kron A) @ vec(B):\n", vec_formula)
assert np.allclose(vec_ABC, vec_formula)
#+end_src

* Chapter 08 Exercises

1. *Exercise 8.1:* Compute the QR decomposition of $A = \begin{pmatrix} 1 & 2 \\ 2 & 1 \\ 1 & 1 \end{pmatrix}$. Verify that $Q^T Q = I_2$ and $Q R = A$.
2. *Exercise 8.2:* Find the Cholesky factor $L$ for $V = \begin{pmatrix} 4 & 2 \\ 2 & 10 \end{pmatrix}$ by hand. Verify that $L L^T = V$.
3. *Exercise 8.3:* For $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$ and $B = \begin{pmatrix} 2 & 0 \\ 1 & 3 \end{pmatrix}$, compute $\det(A \otimes B)$ using the formula $(\det A)^2 (\det B)^2$ and verify in NumPy.
"""

CH09 = r""":PROPERTIES:
:ID:       0192e4b3-0009-7000-8000-000000000009
:ROAM_ALIASES: "Chapter 9: Applications to Statistics" "Multivariate Normal MLE" "Hotelling T2" "MANOVA" "PCA and LDA" "Gauss-Markov OLS"
:END:
#+title: Chapter 09: Key Applications to Statistics
#+subtitle: Multivariate Normal, Hypothesis Testing, PCA, LDA, CCA, Metric MDS, and Linear Models
#+author: Antigravity Notes
#+date: [2026-10-04]
#+filetags: :statistics:multivariate-normal:mle:hotelling:manova:pca:lda:cca:mds:linear-models:

[[id:0192e4b3-0008-7000-8000-000000000008][← Previous: Chapter 08 (Further Topics)]] | [[id:0192e4b3-0000-7000-8000-000000000000][Master Index]] | [[id:0192e4b3-0010-7000-8000-000000000010][Next: Chapter 10 (Outline Solutions) →]]

* The Multivariate Normal Distribution & MLE

A $p$-dimensional random vector $X \sim N_p(\mu, \Sigma)$ with positive-definite covariance matrix $\Sigma$ has probability density function:
\begin{equation}
f(x; \mu, \Sigma) = (2\pi)^{-p/2} |\Sigma|^{-1/2} \exp\left(-\frac{1}{2} (x - \mu)^T \Sigma^{-1} (x - \mu)\right)
\end{equation}

** Standardization (Whitening)
Since $\Sigma$ is symmetric positive-definite, $\Sigma^{-1/2}$ exists. The transformed vector:
\begin{equation}
Z = \Sigma^{-1/2} (X - \mu) \sim N_p(\mathbf{0}, I_p)
\end{equation}

** Maximum Likelihood Estimation via Matrix Calculus
Given an i.i.d. sample of $n$ observations stored in data matrix $X \in \mathbb{R}^{n \times p}$:
The log-likelihood function is:
\begin{equation}
\ell(\mu, \Sigma) = -\frac{np}{2} \log(2\pi) - \frac{n}{2} \log|\Sigma| - \frac{1}{2} \sum_{i=1}^n (x_i - \mu)^T \Sigma^{-1} (x_i - \mu)
\end{equation}
Using the trace trick $\sum_{i=1}^n (x_i - \mu)^T \Sigma^{-1} (x_i - \mu) = \text{tr}\left(\Sigma^{-1} \sum_{i=1}^n (x_i - \mu)(x_i - \mu)^T\right)$:
1. Differentiating with respect to $\mu$:
   \begin{equation}
   \frac{\partial \ell}{\partial \mu} = \Sigma^{-1} \sum_{i=1}^n (x_i - \mu) = \mathbf{0} \implies \hat{\mu} = \bar{x} = \frac{1}{n} X^T \mathbf{1}_n
   \end{equation}
2. Differentiating with respect to $\Sigma^{-1}$ (using $\log|\Sigma| = -\log|\Sigma^{-1}|$):
   \begin{equation}
   \frac{\partial \ell}{\partial \Sigma^{-1}} = \frac{n}{2} \Sigma - \frac{1}{2} A = \mathbf{0} \implies \hat{\Sigma} = \frac{1}{n} A = \frac{1}{n} X^T H_n X
   \end{equation}
   where $H_n = I_n - \frac{1}{n} \mathbf{1}\mathbf{1}^T$ is the centering matrix.
3. *Maximized Log-Likelihood:*
   Substituting $\hat{\mu}$ and $\hat{\Sigma}$ back:
   \begin{equation}
   \ell(\hat{\mu}, \hat{\Sigma}) = -\frac{np}{2} \log(2\pi) - \frac{n}{2} \log|\hat{\Sigma}| - \frac{np}{2}
   \end{equation}

* Multivariate Hypothesis Testing

** 1. One-Sample Hotelling's $T^2$ Test
Test $H_0: \mu = \mu_0$ against $H_1: \mu \ne \mu_0$ with unknown $\Sigma$:
\begin{equation}
T^2 = n (\bar{x} - \mu_0)^T S^{-1} (\bar{x} - \mu_0)
\end{equation}
where $S = \frac{1}{n-1} X^T H_n X$. Under $H_0$:
\begin{equation}
F = \frac{n - p}{(n - 1)p} T^2 \sim F_{p, n - p}
\end{equation}

** 2. Two-Sample Hotelling's $T^2$ Test
Testing equality of mean vectors $H_0: \mu_1 = \mu_2$:
\begin{equation}
T^2 = \frac{n_1 n_2}{n_1 + n_2} (\bar{x}_1 - \bar{x}_2)^T S_{\text{pooled}}^{-1} (\bar{x}_1 - \bar{x}_2)
\end{equation}
\begin{equation}
F = \frac{n_1 + n_2 - p - 1}{(n_1 + n_2 - 2)p} T^2 \sim F_{p, n_1 + n_2 - p - 1}
\end{equation}

** 3. Multivariate Analysis of Variance (MANOVA)
Partition total sum of squares and cross-products $T = W + B$:
- $W$: Within-group SSCP matrix.
- $B$: Between-group SSCP matrix.
- *Wilks' Lambda Statistic:*
  \begin{equation}
  \Lambda = \frac{\det(W)}{\det(W + B)} = \frac{\det(W)}{\det(T)}
  \end{equation}
- *Roy's Largest Root:* Largest eigenvalue of $W^{-1} B$.

* Multivariate Reduction & Scaling Methods

** 1. Principal Component Analysis (PCA)
- Spectral decomposition of sample covariance matrix $S$:
  \begin{equation}
  S = P \Lambda P^T, \quad \lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_p \ge 0
  \end{equation}
- $j$-th principal component score for observation $x$: $y_j = p_j^T (x - \bar{x})$.
- Proportion of variance explained by first $k$ components: $\frac{\sum_{j=1}^k \lambda_j}{\text{tr}(S)}$.

** 2. Fisher's Linear Discriminant Analysis (LDA)
Seeks linear combination $y = a^T x$ maximizing ratio of between-class variance to within-class variance:
\begin{equation}
\max_a \frac{a^T B a}{a^T W a} \implies B a = \lambda W a \iff W^{-1} B a = \lambda a
\end{equation}
The discriminant coefficients (crimcoords) are eigenvectors of $W^{-1} B$.

** 3. Canonical Correlation Analysis (CCA)
Given partitioned variables $X_1 \in \mathbb{R}^p$ and $X_2 \in \mathbb{R}^q$ with covariance $\Sigma = \begin{pmatrix} \Sigma_{11} & \Sigma_{12} \\ \Sigma_{21} & \Sigma_{22} \end{pmatrix}$:
Find $u = a^T X_1$ and $v = b^T X_2$ maximizing correlation $\text{corr}(u, v)$.
Leads to the eigenequation:
\begin{equation}
\Sigma_{11}^{-1} \Sigma_{12} \Sigma_{22}^{-1} \Sigma_{21} a = \rho^2 a
\end{equation}

** 4. Classical Metric Multidimensional Scaling (MDS)
Given pairwise distance matrix $D \in \mathbb{R}^{n \times n}$ with squared entries $D^{(2)} = (d_{ij}^2)$:
1. Apply double centering using $H_n$:
   \begin{equation}
   B = -\frac{1}{2} H_n D^{(2)} H_n
   \end{equation}
2. Spectral decomposition: $B = V \Lambda V^T$.
3. Retain $k$ positive eigenvalues $\Lambda_k = \text{diag}(\lambda_1, \dots, \lambda_k)$ and corresponding eigenvectors $V_k$.
4. Reconstructed coordinates in $\mathbb{R}^k$:
   \begin{equation}
   X = V_k \Lambda_k^{1/2}
   \end{equation}

* The General Linear Model & OLS

The general linear regression model:
\begin{equation}
y = X \beta + \epsilon, \quad E(\epsilon) = \mathbf{0}, \quad \text{Cov}(\epsilon) = \sigma^2 I_n
\end{equation}

** 1. Ordinary Least Squares (OLS) Estimator
Minimizing $\|y - X\beta\|_2^2 = (y - X\beta)^T (y - X\beta)$:
\begin{equation}
\hat{\beta} = (X^T X)^{-1} X^T y
\end{equation}

** 2. Gauss–Markov Theorem
*Theorem:* The OLS estimator $\hat{\beta}$ is the Best Linear Unbiased Estimator (BLUE) — it has minimum variance among all linear unbiased estimators.
*Matrix Proof:*
Let $\tilde{\beta} = C y$ be another unbiased linear estimator. Unbiasedness requires $E(Cy) = C X \beta = \beta \implies CX = I_p$.
Write $C = (X^T X)^{-1} X^T + D$. Then $CX = I_p + DX = I_p \implies DX = \mathbf{0}$.
\begin{equation}
\text{Cov}(\tilde{\beta}) = \sigma^2 C C^T = \sigma^2 \left(((X^TX)^{-1}X^T + D)((X^TX)^{-1}X^T + D)^T\right)
\end{equation}
\begin{equation}
= \sigma^2 (X^T X)^{-1} + \sigma^2 D D^T \ge \sigma^2 (X^T X)^{-1} = \text{Cov}(\hat{\beta})
\end{equation}
since $D D^T$ is positive semi-definite. Hence $\text{Var}(c^T \tilde{\beta}) \ge \text{Var}(c^T \hat{\beta})$ for any vector $c$.

** 3. Projection (Hat) Matrix & Residual Maker
- *Hat Matrix:* $P = X(X^TX)^{-1} X^T$.
  - Symmetric: $P^T = P$.
  - Idempotent: $P^2 = P$.
  - Fits: $\hat{y} = P y$.
- *Residual Maker Matrix:* $M = I_n - P$.
  - Symmetric: $M^T = M$.
  - Idempotent: $M^2 = M$.
  - Orthogonal to $X$: $M X = (I - P)X = X - X = \mathbf{0}$.
  - Residuals: $e = y - \hat{y} = M y$.
- *Residual Sum of Squares (RSS):*
  \begin{equation}
  RSS = e^T e = y^T M^T M y = y^T M y
  \end{equation}
  $\text{df} = \text{tr}(M) = \text{tr}(I_n) - \text{tr}(X(X^TX)^{-1}X^T) = n - p$.
  Unbiased estimator of error variance:
  \begin{equation}
  s^2 = \frac{e^T e}{n - p}
  \end{equation}

** 4. Constrained Least Squares
Minimize $(y - X\beta)^T(y - X\beta)$ subject to linear constraint $R \beta = r$:
Lagrangian $L(\beta, \lambda) = (y - X\beta)^T(y - X\beta) + 2 \lambda^T (R\beta - r)$.
Solution:
\begin{equation}
\hat{\beta}_c = \hat{\beta} - (X^TX)^{-1} R^T [R(X^TX)^{-1}R^T]^{-1} (R\hat{\beta} - r)
\end{equation}

* Complete Python Implementations

#+begin_src python
import numpy as np
import scipy.stats as stats

# 1. Hotelling's T^2 One-Sample Test
# Sample of 10 observations on 2 variables
np.random.seed(42)
X = np.random.randn(10, 2) + np.array([0.5, -0.2])
mu0 = np.array([0.0, 0.0])
n, p = X.shape

xbar = np.mean(X, axis=0)
S = np.cov(X, rowvar=False)
diff = xbar - mu0
T2 = n * (diff.T @ np.linalg.solve(S, diff))
F_stat = ((n - p) / ((n - 1) * p)) * T2
p_val = 1.0 - stats.f.cdf(F_stat, p, n - p)

print(f"Hotelling T2: {T2:.4f}, F-stat: {F_stat:.4f}, p-value: {p_val:.4f}")

# 2. Classical Multidimensional Scaling (MDS)
# Distance matrix between 4 cities
D = np.array([
    [0.0, 3.0, 4.0, 5.0],
    [3.0, 0.0, 5.0, 4.0],
    [4.0, 5.0, 0.0, 3.0],
    [5.0, 4.0, 3.0, 0.0]
])
n = D.shape[0]
H = np.eye(n) - np.ones((n, n)) / n
B = -0.5 * H @ (D ** 2) @ H
evals, evecs = np.linalg.eigh(B)
idx = np.argsort(evals)[::-1]
evals, evecs = evals[idx], evecs[:, idx]

# 2D Configuration
coords = evecs[:, :2] @ np.diag(np.sqrt(np.maximum(evals[:2], 0)))
print("Recovered 2D MDS Coordinates:\n", coords)

# 3. OLS and Hat Matrix Verification
X_reg = np.hstack([np.ones((n, 1)), coords])
y_reg = np.array([10.0, 15.0, 12.0, 20.0])
beta_hat = np.linalg.solve(X_reg.T @ X_reg, X_reg.T @ y_reg)
P = X_reg @ np.linalg.solve(X_reg.T @ X_reg, X_reg.T)
M = np.eye(n) - P
residuals = M @ y_reg

print("Beta hat:", beta_hat)
print("P is idempotent:", np.allclose(P @ P, P))
print("M is orthogonal to X (M @ X == 0):", np.allclose(M @ X_reg, 0))
print("RSS:", residuals.T @ residuals)
#+end_src

* Chapter 09 Exercises

1. *Exercise 9.1:* For bivariate normal sample with $n = 20$, $\bar{x} = (1.5, 2.0)^T$, and $S = \begin{pmatrix} 2.0 & 0.5 \\ 0.5 & 1.0 \end{pmatrix}$, test $H_0: \mu = (1.0, 1.0)^T$ using Hotelling's $T^2$ at $\alpha = 0.05$.
2. *Exercise 9.2:* For data matrix $X = \begin{pmatrix} 1 & 2 \\ 2 & 1 \\ 3 & 4 \\ 4 & 3 \end{pmatrix}$, compute the sample covariance matrix $S$, eigenvalues/eigenvectors, and the first principal component scores.
3. *Exercise 9.3:* Given linear regression model with $X = \begin{pmatrix} 1 & 1 \\ 1 & 2 \\ 1 & 3 \end{pmatrix}$ and $y = \begin{pmatrix} 2 \\ 3 \\ 5 \end{pmatrix}$, compute $\hat{\beta}$, hat matrix $P$, residual maker $M$, and $s^2$.
"""

def main():
    Path("bin/ch07_vector_and_matrix_calculus.org").write_text(CH07, encoding="utf-8")
    print("Wrote bin/ch07_vector_and_matrix_calculus.org")
    Path("bin/ch08_further_topics.org").write_text(CH08, encoding="utf-8")
    print("Wrote bin/ch08_further_topics.org")
    Path("bin/ch09_key_applications_to_statistics.org").write_text(CH09, encoding="utf-8")
    print("Wrote bin/ch09_key_applications_to_statistics.org")

if __name__ == "__main__":
    main()
