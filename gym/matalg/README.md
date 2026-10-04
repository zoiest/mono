# matalg: Basics of Matrix Algebra for Statistics with Python (NumPy & SciPy)

Welcome to the **`matalg`** learning gym! This repository provides an end-to-end mathematical and computational foundation for matrix algebra in modern statistics, translating all concepts and R implementations from **_Basics of Matrix Algebra for Statistics with R_** by Nick Fieller (Chapman & Hall/CRC) into idiomatic Python using **NumPy** and **SciPy**.

---

## 📖 Textbook & Project Overview

- **Source Textbook:** _Basics of Matrix Algebra for Statistics with R_
- **Author:** Nick Fieller (University of Sheffield)
- **Publisher:** Chapman & Hall/CRC The R Series (Taylor & Francis Group, 2016)
- **Reference PDF:** [`downloads/Basics_of_Matrix_Algebra_for_Statistics_with_R.pdf`](file:///home/tofunth/stuffs/mono/gym/matalg/downloads/Basics_of_Matrix_Algebra_for_Statistics_with_R.pdf)
- **Interactive Exercise Board:** [GitHub Projects: @zoiest's matalg](https://github.com/users/zoiest/projects/2)
- **Target Python Stack:** Python 3.12+ / NumPy 2.0+ / SciPy 1.14+

---

## 📁 Repository Structure

```
.
├── BUILD.bazel               # Bazel targets: org2html and Google Drive sync
├── README.md                 # Project architecture, curriculum, and guides
├── bin/                      # Compiled binaries (used for binary generation)
├── writings/                 # Org-mode chapters & compiled HTML files
│   ├── index.org             # Master Org-Roam knowledge base & MOC
│   ├── ch01_introduction.org # Chapter 1: Introduction & Syntax
│   ├── ch02_vectors_and_matrices.org # Chapter 2: Vectors, Centering Matrix H_n, Trace
│   ├── ch03_rank_of_matrices.org # Chapter 3: Rank Factorization & Inequalities
│   ├── ch04_determinants.org # Chapter 4: Determinants, Schur Complements, Rank-1
│   ├── ch05_inverses.org     # Chapter 5: Inverses, Sherman-Morrison, Block Inversion
│   ├── ch06_eigenanalysis.org # Chapter 6: Spectral Decomposition, Matrix Exponentials, SVD
│   ├── ch07_vector_and_matrix_calculus.org # Chapter 7: Vector/Matrix Derivatives, Rayleigh Quotients
│   ├── ch08_further_topics.org # Chapter 8: QR, LU, Cholesky, Pseudoinverse, Kronecker & Vec
│   ├── ch09_key_applications_to_statistics.org # Chapter 9: MVN, Hotelling T^2, MANOVA, PCA, LDA, MDS, OLS
│   └── ch10_outline_solutions.org # Chapter 10: Complete Python Numerical Solutions
├── downloads/                # Local reference materials (gitignored)
│   └── Basics_of_Matrix_Algebra_for_Statistics_with_R.pdf
├── scripts/                  # Automation scripts
│   ├── gen_index.py          # Generator for writings/index.org
│   ├── gen_ch01_to_ch03.py   # Generator for chapters 1, 2, 3
│   ├── gen_ch04_to_ch06.py   # Generator for chapters 4, 5, 6
│   ├── gen_ch07_to_ch09.py   # Generator for chapters 7, 8, 9
│   ├── gen_ch10_solutions.py # Generator for chapter 10 solutions
│   ├── gen_stories.py        # Generator for stories/*.md
│   └── sync_stories_to_gh_project.py # GitHub Project 2 synchronizer
└── stories/                  # 24 Practical Step-by-Step Exercise Stories
    ├── 001_matrix_creation_and_r_to_python_translation.md
    ├── 002_vector_geometry_and_orthogonality.md
    ├── ...
    └── 024_multivariate_statistics_and_linear_models.md
```

---

## 📑 Org-Mode Book Chapters & Knowledge Base

The book's entire mathematical theory, proofs, and numerical examples are converted to Org-mode documents in [`writings/`](file:///home/tofunth/stuffs/mono/gym/matalg/writings/):

| Chapter | Title | Org Reference | Key Focus Areas |
|:-------:|:------|:--------------|:----------------|
| **Index** | Master Knowledge Base | [`writings/index.org`](file:///home/tofunth/stuffs/mono/gym/matalg/writings/index.org) | Complete R-to-Python Rosetta Stone, 10 Cardinal Rules |
| **01** | Introduction & Syntax | [`writings/ch01_introduction.org`](file:///home/tofunth/stuffs/mono/gym/matalg/writings/ch01_introduction.org) | Memory order (F vs C), 0-indexing, 1D vs 2D arrays |
| **02** | Vectors & Matrices | [`writings/ch02_vectors_and_matrices.org`](file:///home/tofunth/stuffs/mono/gym/matalg/writings/ch02_vectors_and_matrices.org) | Centering matrix $H_n$, Idempotency, Trace cyclic properties |
| **03** | Rank of Matrices | [`writings/ch03_rank_of_matrices.org`](file:///home/tofunth/stuffs/mono/gym/matalg/writings/ch03_rank_of_matrices.org) | Rank factorization $A = BC$, Rank-1 $xy^T$, Sylvester inequality |
| **04** | Determinants | [`writings/ch04_determinants.org`](file:///home/tofunth/stuffs/mono/gym/matalg/writings/ch04_determinants.org) | Schur complements, Weinstein-Aronszajn identity $\det(I+AB)=\det(I+BA)$ |
| **05** | Inverses | [`writings/ch05_inverses.org`](file:///home/tofunth/stuffs/mono/gym/matalg/writings/ch05_inverses.org) | Sherman-Morrison rank-1 update, Banachiewicz block inversion |
| **06** | Eigenanalysis | [`writings/ch06_eigenanalysis.org`](file:///home/tofunth/stuffs/mono/gym/matalg/writings/ch06_eigenanalysis.org) | Spectral Theorem $A = P \Lambda P^T$, matrix square root, SVD |
| **07** | Vector & Matrix Calculus | [`writings/ch07_vector_and_matrix_calculus.org`](file:///home/tofunth/stuffs/mono/gym/matalg/writings/ch07_vector_and_matrix_calculus.org) | $\nabla (x^T S x) = 2Sx$, $\nabla \log\det(X) = X^{-1}$, Rayleigh quotient |
| **08** | Further Topics | [`writings/ch08_further_topics.org`](file:///home/tofunth/stuffs/mono/gym/matalg/writings/ch08_further_topics.org) | QR, Cholesky, Moore-Penrose $A^+$, Kronecker product, $\text{vec}(ABC)$ |
| **09** | Applications to Statistics | [`writings/ch09_key_applications_to_statistics.org`](file:///home/tofunth/stuffs/mono/gym/matalg/writings/ch09_key_applications_to_statistics.org) | MVN MLE, Hotelling $T^2$, MANOVA, PCA, Fisher LDA, MDS, OLS |
| **10** | Outline Solutions | [`writings/ch10_outline_solutions.org`](file:///home/tofunth/stuffs/mono/gym/matalg/writings/ch10_outline_solutions.org) | Complete Python numerical code solutions for all 9 chapters |
| **11** | Capstone Project | [`writings/ch11_capstone_project.org`](file:///home/tofunth/stuffs/mono/gym/matalg/writings/ch11_capstone_project.org) | End-to-end Multivariate Financial Risk & Factor Analysis Engine |

---

## 🏃 Practical Exercise Stories (001 - 030)

The practical exercises are organized into 30 progressive stories in [`stories/`](file:///home/tofunth/stuffs/mono/gym/matalg/stories/) and synchronized directly to [GitHub Project 2](https://github.com/users/zoiest/projects/2):

### Foundational Curriculum (Stories 001 - 024)
- **Story 001:** Matrix Creation & R-to-Python Translation
- **Story 002:** Vector Geometry, Inner/Outer Products, and Orthogonality
- **Story 003:** Matrix Multiplication, Cross Products, and the Trace Operator
- **Story 004:** Special Matrices & Quadratic Form Symmetrization
- **Story 005:** The Centering Matrix $H_n$ and Sample Covariance Computation
- **Story 006:** Partitioned Matrices & Block Multiplication
- **Story 007:** Matrix Rank, Linear Independence, and SVD Thresholding
- **Story 008:** Rank Factorization & Outer Products of Rank 1
- **Story 009:** Rank Inequalities & Degrees of Freedom in ANOVA
- **Story 010:** Determinants, Laplace Expansions, and Log-Determinants
- **Story 011:** Schur Complements & Block Partitioned Determinants
- **Story 012:** The Weinstein-Aronszajn Identity & Rank-1 Updates
- **Story 013:** Matrix Inversion & Numerical Conditioning
- **Story 014:** Patterned Inverses & The Sherman-Morrison Formula
- **Story 015:** Block Inversion & Conditional Gaussian Covariance
- **Story 016:** Eigenanalysis & The Spectral Decomposition Theorem
- **Story 017:** Matrix Functions, Square Roots, and the Matrix Exponential
- **Story 018:** Singular Value Decomposition (SVD) & Low-Rank Approximation
- **Story 019:** Vector and Matrix Calculus for Maximum Likelihood Estimation
- **Story 020:** Constrained Optimization & Rayleigh Quotients
- **Story 021:** Advanced Factorizations: QR, Cholesky, and LU
- **Story 022:** Generalized Inverses & The Moore-Penrose Pseudoinverse
- **Story 023:** Kronecker Products, Vec Operator, and Matrix Equations
- **Story 024:** Multivariate Hypothesis Testing, PCA, LDA, and OLS

### Capstone Mini-Project: Multivariate Asset Analytics Engine (Stories 025 - 030)
Dataset: [`data/asset_returns.csv`](file:///home/tofunth/stuffs/mono/gym/matalg/data/asset_returns.csv) ($N=250$ business days $\times$ $p=6$ asset classes: SPY, QQQ, GLD, XLE, TLT, VNQ).
- **Story 025:** Capstone Project Phase 1 — Dataset Ingestion, Matrix Centering, and Covariance Estimation
- **Story 026:** Capstone Project Phase 2 — Precision Matrix, Partial Correlation, and Online Sherman-Morrison Updates
- **Story 027:** Capstone Project Phase 3 — PCA Factor Modeling, Scree Analysis, and SVD Covariance Denoising
- **Story 028:** Capstone Project Phase 4 — Mahalanobis Anomaly Detection, Cholesky Whitening, and Hotelling's $T^2$
- **Story 029:** Capstone Project Phase 5 — Markowitz Minimum-Variance Portfolio via Constrained Optimization
- **Story 030:** Capstone Project Phase 6 — Factor Pricing Regression, Hat Matrix Projection, and Gauss-Markov Diagnostics

---

## 🛠️ Build & Automation Commands

### Compile Org Notes to HTML
```bash
bazel run //gym/matalg:org2html
```
Uses Emacs in batch mode with incremental SHA-256 build avoidance to compile all `.org` files into standalone `.html` files in `writings/`.

### Re-Sync Stories to GitHub Projects
```bash
python3 scripts/sync_stories_to_gh_project.py
```
Synchronizes all 24 markdown stories to [https://github.com/users/zoiest/projects/2](https://github.com/users/zoiest/projects/2) with Status set to `Ready`, Priority `P1`, and Size `M`.

### Sync Notes with Remote Storage (Google Drive)
```bash
bazel run //gym/matalg:sync
```
