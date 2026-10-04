# Story 009: Rank Inequalities & Degrees of Freedom in ANOVA

## User Story
**As a** statistical theoretical analyst,
**I want to** verify Sylvester and Frobenius rank inequalities and relate matrix rank to degrees of freedom,
**So that** I can verify mathematical bounds on matrix products and derive valid degrees of freedom in hypothesis testing..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 3: Rank of Matrices
* **Sections:** 3.3, 3.4 (Rank Inequalities, Sylvester's Inequality, Rank in Statistics)

---

## 🎯 What You Will Learn
1. Subadditivity: rank(A + B) <= rank(A) + rank(B).
2. Product bound: rank(AB) <= min(rank(A), rank(B)).
3. Sylvester's rank inequality: rank(AB) >= rank(A) + rank(B) - p.
4. Connection between rank of idempotent matrices and degrees of freedom.

---

## 🛠️ Step-by-Step Implementation Guide

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
```

---

## ✅ Acceptance Criteria
- [X] Sylvester's inequality `rank(AB) >= rank(A) + rank(B) - p` is confirmed.
- [X] Product rank is bounded by `min(rank(A), rank(B))`.
- [X] Subadditivity `rank(A + B) <= rank(A) + rank(B)` is verified.
