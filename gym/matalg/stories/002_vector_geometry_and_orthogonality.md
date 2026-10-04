# Story 002: Vector Geometry, Inner/Outer Products, and Orthogonality

## User Story
**As a** statistician analyzing feature spaces,
**I want to** implement vector inner products, outer products, Euclidean norms, and test for orthogonality,
**So that** I can compute projection angles and verify orthogonal subspaces in linear statistical models..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 2: Vectors and Matrices
* **Sections:** 2.1 (Vectors, Definitions, Example 2.1, Orthogonal vectors)

---

## 🎯 What You Will Learn
1. Computing inner products x^T y and outer products x y^T.
2. Evaluating Euclidean L2 norms and cosine similarities.
3. Testing orthogonality condition x^T y = 0.
4. Rank properties of outer products.
5. Computing inner products and cosine similarity between empirical asset return series.
6. Constructing an orthogonalized Treasury return series via Gram-Schmidt projection.

---

## 🛠️ Step-by-Step Implementation Guide


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
```

### 2. 📊 Practical Dataset Application: Real Market Vector Geometry & Orthogonalization
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
```

---

## ✅ Acceptance Criteria
- [X] Vectors `a` and `b` are confirmed orthogonal (`a @ b == 0`).
- [X] Vectors `a` and `c` are confirmed orthogonal (`a @ c == 0`).
- [X] Outer product `a b^T` is confirmed to have rank 1.
- [X] Euclidean norms and cosine distance tests pass.
- [X] Cosine similarity between SPY and TLT is verified negative on centered returns.
- [X] Treasury returns are successfully orthogonalized against equity returns ($s^T t_\perp = 0$).
- [X] Outer product of the asset mean vector $\bar{x}\bar{x}^T$ is verified to have rank 1.
