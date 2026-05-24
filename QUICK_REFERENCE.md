# Quick Reference: QUBO→Ising λ/4 vs λ/2

**Question:** Is $h_k = -w_k/2 + \lambda \deg(k)/4$ or $\lambda \deg(k)/2$?

**Answer:** **λ/4 is correct.**

---

## One-Minute Explanation

Your student derived: $h_k = -w_k/2 + \lambda \deg(k)/2$ ❌  
You said: $h_k = -w_k/2 + \lambda \deg(k)/4$ ✓

**Why you're right:** The handshake lemma says

$$\sum_{e=(i,j) \in E} (s_i + s_j) = \sum_{k=1}^{N} \deg(k) \cdot s_k$$

is ONE sum, not two. Your student split it into $\sum s_i + \sum s_j$, claimed each equals $\sum \deg(k) s_k$, and got $2\sum \deg(k) s_k$ (the factor-of-2 error).

---

## Numerical Check

| Formula | $h_0$ | $h_1$ | Status |
|---------|-------|-------|--------|
| Student's (λ/2) | 4.0 | 5.0 | ❌ |
| Yours (λ/4) | 1.25 | 2.25 | ✓ |

**Example:** $w = [3, 1, 1, 1, 1, 1]$, edge (0,1), $\lambda = 11$.
- Yours: $h_0 = -3/2 + 11·1/4 = -1.5 + 2.75 = 1.25$ ✓
- Student: $h_0 = -3/2 + 11·1/2 = -1.5 + 5.5 = 4.0$ ❌

---

## Three Proofs

### 1. Symbolic (SymPy)
```bash
python scripts/derive_ising_symbolic.py
```
Expands QUBO on 5 graphs. Every one yields λ/4. ✓

### 2. Empirical (Brute-force)
```bash
python scripts/verify_qubo_ising_equivalence.py --all
```
Results:
```
λ/4: max energy residual = 0.0e+00  ✓
λ/2: max energy residual = 1.8e+01  ❌
```

### 3. Regression Tests
```bash
python -m pytest tests/test_qubo_ising_equivalence.py -v
```
13/13 tests pass (energy equivalence, handshake lemma, argmin agreement). ✓

---

## For Code Review

**File:** `experiments/mrta/ising_map.py:96`
```python
h_field[k] = -utilities[k] / 2.0 + (lambda_penalty * degrees[k]) / 4.0
```
✓ **Already correct.** No changes needed.

---

## Key Documents

1. **`DERIVATION_NOTE.md`** — Full math (10 pages, self-contained)
2. **`VERIFICATION_SUMMARY.md`** — Evidence + talking points (2 pages)
3. **`QUICK_REFERENCE.md`** — This card (1 page)

---

## Where the Student Went Wrong

**PDF, around the degree term:**

Student writes:
$$\lambda \sum_{e=(i,j)} (s_i + s_j) = \lambda \sum_e s_i + \lambda \sum_e s_j = 2\lambda \sum_k \deg(k) s_k$$

✗ **This is wrong.** The handshake lemma tells us the *single* sum (LHS) equals $\sum_k \deg(k) s_k$, not twice that. Splitting it and applying the lemma to each part double-counts.

---

## Confidence Level

- ✅ Algebraically sound (checked by hand and SymPy)
- ✅ Empirically verified (brute-force on 3 instances)
- ✅ Code-verified (OIM parameters match formula)
- ✅ Regression-tested (13 tests, all pass)
- ✅ Repository-ready (no production code changes)

**Confidence: 100%**

---

## Next Steps

1. Share `DERIVATION_NOTE.md` Sections 1–11 with your student.
2. Have them run the three verification scripts.
3. They can present this to their thesis committee with full confidence.

---

**Status:** ✅ Verified. λ/4 is correct. Deploy.
