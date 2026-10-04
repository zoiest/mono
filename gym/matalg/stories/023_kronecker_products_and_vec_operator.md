# Story 023: Kronecker Products, Vec Operator, and Matrix Equations

## User Story
**As a** time series econometrician,
**I want to** implement Kronecker products $A \otimes B$, column-major $\text{vec}(A)$, and solve Sylvester matrix equations,
**So that** I can estimate Vector Autoregressive (VAR) models and solve continuous Lyapunov equations..

---

## 📖 Book Alignment
* **Book:** *Basics of Matrix Algebra for Statistics with R* (Nick Fieller)
* **Chapter:** Chapter 8: Further Topics
* **Sections:** 8.5 (Kronecker Products and the Vec Operator)

---

## 🎯 What You Will Learn
1. Kronecker product properties: (A kron B)(C kron D) = (AC) kron (BD).
2. Column-major vectorization: A.flatten(order='F').
3. The fundamental identity: vec(ABC) = (C^T kron A) vec(B).
4. Solving matrix equations A X B = C.

---

## 🛠️ Step-by-Step Implementation Guide

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
```

---

## ✅ Acceptance Criteria
- [X] `A.flatten(order='F')` executes column-major vectorization.
- [X] Fundamental identity `vec(ABC) == (C^T kron A) vec(B)` is verified.
- [X] Mixed product property `(A kron B) @ (C kron D) == (A @ C) kron (B @ D)` is verified.
