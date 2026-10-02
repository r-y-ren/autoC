# E3b — is there a decodable gradient at B at SMALL steps? (random-control re-read)

E3b agent, 2026-09-11, 90-minute box, CPU only (the 3070 runs the E3 sweep being re-read).
Inputs (read-only): `S/onestep/thetas/*.npy` (the sweep's full-R step thetas), `S/onestep/grads/`,
`S/onestep/run_local.log`. New files: `S/onestep_b/` (thetas, runner, analysis, csvs).
Predecessors: `docs/strategy/2026-09-11-e3-step-audit.md` (the α-ladder that found the cliff is
curvature) and consensus §56.

## 0. The question

The audit established that the sweep's own step `R = lr·√n_live = 0.2323` is a cliff for the
σ 0.01 direction (−16.6 k on LIVE-C) and that at α = 0.1 of it the *same* direction reads uphill
(+140 / +286, antisym +396 LIVE-C, +915 TOPB2). But it had **no same-length random controls at
small α**: every random control in the sweep sits at α 1.0, where the cliff dominates and the
comparison is meaningless. And the gradient draws themselves look like pure sampling noise
(‖g₅₁₂‖/‖g₂₀₄₈‖ = 1.998 ≈ √4, cos = 0.53 ≈ √¼). So the audit's "+d gains at α 0.1" could be
(a) a real, tiny gradient, or (b) a number that ANY direction of length 0.1 R would produce
about as often — the sd of the small-α paired statistic was never measured.

E3b measures it: every cell, and eight signed random directions, **at the same small α**, on the
engine-exact screen, paired board by board against B.

## 1. PRE-REGISTRATION (written 2026-09-11 15:38Z, before any E3b number was read)

### Thetas
`θ(cell, sign, α) = B + α·(θ_sweep[cell, sign] − B)` in float64, saved float32, where
`B = artifacts/kagg2_games/thetas/flow193_g100_hr.npy` (6789 params, `_hr` layout).
Verified before screening: every source step has `‖θ_sweep − B‖ = 0.232321` (= R), exactly 5,997
non-zero coordinates (the live mask), **792 off-mask coordinates bit-identical to B**, `plus` and
`minus` exactly antipodal (cos = −1.000000), and α = 1 round-trips to the sweep's own file
bit-for-bit. Cells: `s0p01_p512`, `s0p01_p2048`, `s0p02_p512`, `s0p02_p2048`
(+ `s0p04_*` if the sweep emits them inside the box); controls `rand0…rand7`.

*(The audit's own `S/onestep_audit/thetas/*.npy` were built from the unit gradient rather than
from the saved step file and differ from these by 1 float32 ULP — `np.array_equal` False,
max |Δ| 1.19e-07 — so its csvs are NOT reused; s0p01 is re-screened here. The two readings of the
same α-0.1 cell are then an independent reproducibility check.)*

### Screen
`S/simscreen/screen.py`, shipped `hr` switches, pinned-town action tapes, `shop_crn=True`,
identical (tape, seed, seat) boards for every theta, cold start, both seats.
Two frozen board lists: **LIVE-C hold-out** (`boards.json`, 120 cells = 60 held-out tapes × 2
seats; **honest unit = 60 tapes**) and **TOPB2 top tier** (`boards_topb2.json`, 40 cells = 20
pinned tapes × 2 seats; **honest unit = 20 tapes**). `--chunk 40` on both so the compile cache is
shared. Pairing is per board against B's row in the same csv (`S/fertcow/pair.py` recipe); the
per-tape mean of the two seats is the honest unit and `t` is quoted on it.

### Statistics, per cell and per α ∈ {0.1, 0.03}, per family
* `gain(+αd)` = mean paired Δmargin vs B over the boards, and the same for `gain(−αd)`;
* antisymmetric statistic **`A = gain(+αd) − gain(−αd)`** (the curvature-free part: the symmetric
  part cancels, so A is the only term a first-order gradient can produce);
* `t` on the honest unit (60 tapes / 20 tapes) for `gain(+αd)`, and for A;
* the same A for each of the 8 random directions at the same α;
* **`z = (A_cell − mean A_rand) / sd A_rand`** and **`rand<A`** = how many of the 8 randoms have a
  smaller A than the cell.
Random controls at α 0.1 for both families are computed first; α 0.03 randoms only if time allows.

### PASS rule (pre-registered, fixed before the numbers)
A cell **PASSES E3b** when, at α = 0.1, ALL THREE hold:
1. `gain(+αd) > 0` on **both** families (LIVE-C and TOPB2);
2. `A_cell` beats **≥ 6 of 8** randoms on **both** families;
3. the LIVE-C 60-tape `t` of `gain(+αd)` is **≥ 2**.
Anything else is FAIL. A cell that meets (1) and (2) but not (3) is recorded as FAIL and flagged
as "directionally positive, underpowered".

### The independent evidence line
`p512` and `p2048` are two draws of the same σ from different population sizes. Their agreement —
`cos(d₅₁₂, d₂₀₄₈)` and whether their `+αd` gains agree in sign and rough size — is the real
evidence against noise, because two *independent* noise draws agree only by luck. Measured before
screening: **cos(d₅₁₂, d₂₀₄₈) = +0.5323 (σ 0.01), +0.5268 (σ 0.02)** — both ≈ √(256/1024) = 0.5,
i.e. exactly the shared-prefix value expected when the population mean gradient is ZERO. The
cross-σ cosine `cos(s0p01_p2048, s0p02_p2048) = +0.2273`. So the pre-registered expectation from
the geometry alone is that the cells FAIL; a PASS would mean the engine sees a signal the ε-space
norm test cannot.

## 2. RESULTS

All numbers below are **paired Δmargin vs B in coins per board**, on the identical
(tape, seed, seat) cells, `shopdiff 0.0 %` on every theta in every run (the screen's
byte-identical-shop guarantee held throughout, 4,290 paired board rows).
`t` is on the **honest unit** (60 LIVE-C tapes, 20 TOPB2 tapes); `gain` is the board mean
(identical to the tape mean — every tape carries exactly its two seats).

### 2.0 Reproducibility check against the audit (five overlapping α-0.1/0.03 cells)

The audit's thetas and mine differ by 1 float32 ULP. **Every overlapping cell reproduces to the
coin**: LIVE-C `p2048_a0p1` +140/+140, `p512_a0p1` +286/+286, `p2048_m0p1` −256/−256,
`p2048_a0p03` +111/+111, `p2048_m0p03` −178/−178; TOPB2 `p2048_a0p1` −521/−521,
`p512_a0p1` −703/−703, `p2048_m0p1` −1,436/−1,436, `p2048_a0p03` −647/−647. The screen is stable
to a 1-ULP change in θ, and the audit's §3 table is confirmed independently.

### 2.1 The random controls are the whole story

**LIVE-C, α 0.1, the 8 signed random directions at the same length 0.02323:**

| rand | gain(+) | t(+) | gain(−) | A = gain(+) − gain(−) | t(A) |
|---|---|---|---|---|---|
| rand0 | +201 | +1.85 | −24 | **+224** | +0.95 |
| rand1 | +119 | +1.39 | +181 | −62 | −0.49 |
| rand2 | −4 | −0.06 | +20 | −24 | −0.11 |
| rand3 | +99 | +1.55 | −8 | +107 | +0.49 |
| rand4 | +68 | +0.66 | +112 | −44 | −0.33 |
| rand5 | +203 | +1.52 | −89 | **+292** | +1.28 |
| rand6 | +42 | +0.63 | +227 | −185 | −1.38 |
| rand7 | −143 | −0.65 | +84 | −227 | −1.04 |
| **null** | 16 steps: **mean +68, sd 107** | | | **A: mean +10, sd 184** | |

**TOPB2, α 0.1:**

| rand | gain(+) | t(+) | gain(−) | A | t(A) |
|---|---|---|---|---|---|
| rand0 | +289 | +1.99 | −2,089 | **+2,378** | +3.17 |
| rand1 | +170 | +1.06 | −144 | +314 | +0.94 |
| rand2 | −167 | −1.39 | −2,109 | **+1,942** | +2.31 |
| rand3 | −41 | −0.30 | −1,912 | **+1,872** | +2.36 |
| rand4 | +21 | +0.47 | +27 | −6 | −0.04 |
| rand5 | −511 | −1.12 | −1,945 | **+1,434** | +2.71 |
| rand6 | −194 | −0.51 | +48 | −242 | −0.58 |
| rand7 | −2,172 | −2.93 | +48 | −2,220 | −3.02 |
| **null** | 16 steps: **mean −668, sd 977** | | | **A: mean +684, sd 1,527** | |

Two facts kill the previous reading before any cell is looked at.

1. **A 0.1 R step is not neutral even when it is random.** On LIVE-C a random step of this length
   *gains* +68 ± 107 on average (both signs), so "the +d cell gained +140" is a below-average
   random step. On TOPB2 a random step of this length *costs* −668 ± 977, so "the +d cell lost
   −521" is a better-than-average random step. B is not a stationary point in either direction:
   it is on a slope on LIVE-C (any perturbation helps) and on a ridge on TOPB2 (any perturbation
   hurts), and both of those are *symmetric* effects that no gradient produces.
2. **The antisymmetric statistic A is enormous for random directions on TOPB2.** Four of eight
   random directions have A between +1,434 and +2,378, with t(A) up to +3.17 — and a random
   direction has, by construction, *zero* gradient component. The audit's headline TOPB2 number,
   "antisym +915, of the two mirror steps the trainer's own direction is the better one", is
   **smaller than four of eight coin flips**. On 20 tapes, `A` is simply not a measurement.

### 2.2 The cells, at α 0.1 (the pre-registered scale)

`zA` = (A_cell − mean A_rand)/sd A_rand; `rand<A` = how many of the 8 randoms have smaller A;
`zgain` = (gain(+) − mean gain of the 16 random steps)/sd.

**LIVE-C hold-out (120 cells / 60 tapes):**

| cell | gain(+) | t(+) | gain(−) | t(−) | A | t(A) | zA | rand<A | zgain |
|---|---|---|---|---|---|---|---|---|---|
| s0p01_p512 | **+286** | +1.70 | −29 | −0.13 | **+314** | +1.44 | +1.65 | **8/8** | **+2.04** |
| s0p01_p2048 | +140 | +0.76 | −256 | −1.15 | **+396** | +1.78 | +2.09 | **8/8** | +0.68 |
| s0p02_p512 | +104 | +1.18 | +158 | +1.36 | −54 | −0.37 | −0.35 | 3/8 | +0.34 |
| s0p02_p2048 | +101 | +1.17 | −26 | −0.21 | +127 | +0.86 | +0.63 | 6/8 | +0.31 |

**TOPB2 top tier (40 cells / 20 tapes):**

| cell | gain(+) | t(+) | gain(−) | t(−) | A | t(A) | zA | rand<A | zgain |
|---|---|---|---|---|---|---|---|---|---|
| s0p01_p512 | −703 | −1.58 | −1,402 | −2.52 | +700 | +1.26 | +0.01 | 4/8 | −0.04 |
| s0p01_p2048 | −521 | −1.06 | −1,436 | −2.42 | +915 | +2.01 | +0.15 | 4/8 | +0.15 |
| s0p02_p512 | −454 | −1.34 | +29 | +0.18 | −484 | −1.28 | −0.76 | 1/8 | +0.22 |
| s0p02_p2048 | −475 | −1.33 | −5 | −0.03 | −470 | −1.28 | −0.76 | 1/8 | +0.20 |

### 2.3 The cells, at α 0.03

| family | cell | gain(+) | t(+) | gain(−) | t(−) | A | t(A) |
|---|---|---|---|---|---|---|---|
| LIVE-C | s0p01_p512 | +122 | +1.17 | −100 | −0.42 | +222 | +0.96 |
| LIVE-C | s0p01_p2048 | +111 | +1.04 | −178 | −0.80 | +289 | +1.30 |
| LIVE-C | s0p02_p512 | +73 | +1.28 | −84 | −1.36 | +156 | +1.91 |
| LIVE-C | s0p02_p2048 | +39 | +0.66 | +46 | +0.53 | −7 | −0.07 |
| TOPB2 | s0p01_p512 | −312 | −0.89 | −2,077 | −2.80 | +1,765 | +3.10 |
| TOPB2 | s0p01_p2048 | −647 | −1.42 | −2,017 | −2.66 | +1,370 | +2.69 |
| TOPB2 | s0p02_p512 | +17 | +1.35 | +86 | +0.59 | −69 | −0.48 |
| TOPB2 | s0p02_p2048 | −138 | −1.32 | +74 | +0.51 | −212 | −1.27 |

Note the shape of the α-0.03 column: shrinking the step by 3.3× shrinks `gain(+)` on LIVE-C by
about 2.3× (+286 → +122, +140 → +111, +104 → +73, +101 → +39), which is what a *linear* term does,
but it does the same to the random controls (§2.5), so the shrinkage carries no information about
whether the linear term is the gradient or the draw.

### 2.4 PASS / FAIL against the pre-registered rule

| cell | (1) gain(+) > 0 both families | (2) A beats ≥6/8 randoms both families | (3) LIVE-C t(+) ≥ 2 | **verdict** |
|---|---|---|---|---|
| s0p01_p512 | NO (TOPB2 −703) | NO (TOPB2 4/8) | NO (+1.70) | **FAIL** |
| s0p01_p2048 | NO (TOPB2 −521) | NO (TOPB2 4/8) | NO (+0.76) | **FAIL** |
| s0p02_p512 | NO (TOPB2 −454) | NO (3/8, 1/8) | NO (+1.18) | **FAIL** |
| s0p02_p2048 | NO (TOPB2 −475) | NO (TOPB2 1/8) | NO (+1.17) | **FAIL** |

**No cell passes any of the three clauses.** The two σ 0.01 cells are recorded as
"directionally positive, underpowered" on LIVE-C only: both beat 8/8 randoms on A there, which is
the strongest thing in this document — but with 8 controls the best attainable one-sided rank
p is 1/9 = 0.11, the two cells share a 256-pair ε prefix so they are not two tests, and clause (3)
(t ≥ 2) is missed by both. σ 0.02 shows nothing on either family at either α, consistent with the
sweep's own σ 0.02 block reading flat at full R (`|κ| ≤ 0.027`, `rand<+d` 3-15/16).

### 2.5 p512 vs p2048 agreement — the evidence that was supposed to be decisive

The brief's real test was whether two draws agree. They do agree, and the agreement is **fully
accounted for by the ε prefix they share**, so it is not evidence.

| σ | cos(d₅₁₂, d₂₀₄₈) | ‖g₅₁₂‖/‖g₂₀₄₈‖ | corr of per-tape A fingerprints, LIVE-C α 0.1 | same, α 0.03 |
|---|---|---|---|---|
| 0.01 | **+0.532** | 105.90/52.99 = 1.998 | **+0.717** | +0.510 |
| 0.02 | **+0.527** | 34.24/16.89 = 2.027 | **+0.575** | +0.426 |

Both norm ratios are √4 and both cosines are √(256/1024) = 0.5 to two decimals: this is exactly
what two antithetic draws sharing a 256-pair prefix give **when the population mean gradient is
zero**, and it leaves no room for a signal floor at P 2048. The board-level fingerprints then
correlate at +0.72 / +0.58 against a null of 28 random direction pairs at **−0.02 ± 0.42** — but a
random *pair* has cos ≈ 0, whereas these two directions have cos 0.53, and the boards respond
close to linearly at this step length, so the predicted correlation under pure noise is ≈ 0.53.
Observed 0.575 (σ 0.02) and 0.717 (σ 0.01) against a predicted 0.53. **The two pops agree because
they are half the same draw, not because they found the same hill.** Their `gain(+αd)` on LIVE-C
agrees in sign (+286 vs +140; +104 vs +101) and disagrees by 2× in size; on TOPB2 both are
negative (−703 vs −521; −454 vs −475) and both sit at the random-step mean of −668.

### 2.6 Round 2: σ 0.04, and the α-0.03 random controls

σ 0.04 landed at 16:16Z with the same ε-space signature as its siblings: ‖g₅₁₂‖/‖g₂₀₄₈‖ =
23.18/11.63 = **1.993** (√4 again), `cos(d₅₁₂, d₂₀₄₈)` = **+0.512**. It reads *downhill*:

| family | α | cell | gain(+) | t(+) | gain(−) | A | zA | rand<A | zgain |
|---|---|---|---|---|---|---|---|---|---|
| LIVE-C | 0.1 | s0p04_p512 | −30 | −0.13 | +161 | −191 | −1.09 | 1/8 | −0.92 |
| LIVE-C | 0.1 | s0p04_p2048 | −222 | −1.05 | −21 | −201 | −1.15 | 1/8 | −2.71 |
| TOPB2 | 0.1 | s0p04_p512 | −1,738 | −2.89 | −377 | −1,361 | −1.34 | 1/8 | −1.10 |
| TOPB2 | 0.1 | s0p04_p2048 | −1,400 | −2.44 | −447 | −952 | −1.07 | 1/8 | −0.75 |
| TOPB2 | 0.03 | s0p04_p512 | −1,989 | −2.58 | +118 | −2,107 | −8.46 | 0/8 | −12.49 |
| TOPB2 | 0.03 | s0p04_p2048 | −2,108 | −2.67 | −305 | −1,802 | −7.29 | 0/8 | −13.24 |

`s0p04` is the only cell whose sign is decided at t < −2, and it is **negative** — and note the
scaling: **TOPB2 `gain(+)` is −1,738 at α 0.1 and −1,989 at α 0.03**, i.e. shrinking the step by
3.3× made it *worse*. No smooth function of α does that. The same non-scaling shows up in the
α-0.03 LIVE-C column (§2.3) where `A` shrank by only ~1.3× for a 3.3× smaller step while the
random controls' `A` sd shrank cleanly from 184 to 59. §2.7 says why.

α-0.03 random controls: LIVE-C A mean −35 sd 59 (gain of the 16 steps +31 ± 43);
TOPB2 A mean +83 sd 259 (gain −28 ± 157). Against these, LIVE-C `s0p01_p512` A +222 (zA +4.37,
8/8), `s0p01_p2048` +289 (+5.51, 8/8), `s0p02_p512` +156 (+3.25, 8/8) — and TOPB2 `s0p01_p512`
+1,765 (+6.50, 8/8), `s0p01_p2048` +1,370 (+4.97, 8/8). Read naively that is a strong PASS-shaped
signal at α 0.03. It is not one, and §2.7 is the reason: in every one of those cells the whole
statistic comes from the **`minus` theta crossing a board-independent switch**, and `gain(+)`
itself is still **negative** on TOPB2 (−312, −647; `zgain` −1.81, −3.94 — i.e. *worse* than the
average random step of the same length). Clause (1) of the pre-registered rule fails there too.

### 2.7 WHY every one of these statistics is a single Bernoulli trial

Count, for each of the 56 step thetas, how many boards change margin **at all**:

* the distribution of "boards moved" is 0-89 % for 41 thetas, **exactly one** theta in 90-99 %,
  and **exactly 100.0 % for 14 thetas** — a hole and then a spike, not a continuum;
* **the same 14 thetas move 100.0 % of the boards on BOTH families** — all 120 LIVE-C cells *and*
  all 40 TOPB2 cells, two disjoint tape sets, 100 different games. Set equality is exact
  (`livec-only: []`, `topb2-only: []`).

A perturbation that changes the outcome of *every* game in two unrelated tape families has flipped
a **board-independent decision** — an opening/day-0 choice the planner makes before any board
information is used (the pumped opening; `dominant-strategy-2026-09-03`). The objective at B is
therefore not a smooth surface with a gradient on it: along any ray it is **piecewise constant**,
with one dominating discontinuity, and `gain(α)` is a step function of α.

The 14 are:

| group | thetas crossing the switch |
|---|---|
| randoms (α 0.1) | `rand0−`, `rand2−`, `rand3−`, `rand5−`, `rand7+` |
| σ 0.01 | `s0p01_p512−` and `s0p01_p2048−`, at **both** α 0.1 and α 0.03 |
| σ 0.04 | `s0p04_p512+` and `s0p04_p2048+` at both α; `s0p04_p2048−` at α 0.1 |
| σ 0.02 | **none, at either α** |

Now re-read every headline number in this document:

* the four huge random A's on TOPB2 (+2,378, +1,942, +1,872, +1,434) are exactly `rand0−`,
  `rand2−`, `rand3−`, `rand5−` — the four randoms whose minus side crosses the switch — and the
  one huge negative (−2,220) is `rand7+`, the one whose plus side crosses;
* σ 0.01's celebrated positive A (LIVE-C +314/+396, TOPB2 +700/+915, and +1,765/+1,370 at α 0.03)
  is produced **entirely by its `minus` side crossing the switch and losing**. Its `plus` side
  never crosses. A "the trainer's own direction beats its mirror" reading of that is a statement
  about which side of one binary opening decision the mirror lands on;
* σ 0.04's large negative gains are its `plus` side crossing;
* σ 0.02 crosses on neither side at either α — and σ 0.02 is precisely the cell with **no** signal
  anywhere (A −54, +127, +156, −7; `rand<A` 1-8/8 with no pattern; sweep's own full-R block flat).

So the antisymmetric statistic A — and the sweep's κ, which is the same quantity — is not an
average over 60 or 20 independent boards. It is **one coin flip** ("does the minus side cross?")
read out 120 times. Its honest n is 1, its honest sd is the ±1,500-coin size of the switch, and
every `t` in §2.2-2.6 built on A is overstated by roughly √60 or √20. That is also why the α
scaling is broken: whether a ray crosses a threshold is monotone in α but the *damage* once
crossed is fixed, so `gain` does not shrink toward 0 as α → 0 (σ 0.04 TOPB2: −1,738 at α 0.1,
−1,989 at α 0.03) — it stays at full size until the crossing point, then vanishes.

## 3. VERDICT

> **NO. There is no decodable gradient at B at small steps, on either family, at either α, in any
> cell — and E3b additionally shows the measurement the E3 rig makes cannot decode one.**
>
> All six cells (σ 0.01/0.02/0.04 × P 512/P 2048) **FAIL** the pre-registered rule, and they fail
> every one of its three clauses, not just the strict one: no cell has `gain(+αd) > 0` on both
> families (TOPB2 is negative for all six at α 0.1); no cell beats ≥ 6/8 randoms on A on both
> families; no cell reaches LIVE-C `t ≥ 2` on `gain(+αd)` (best = `s0p01_p512` at **+1.70**).
> The closest cell is **σ 0.01 / P 512**, which on LIVE-C alone gains +286 (`zgain` +2.04) and
> beats 8/8 randoms on A — but its TOPB2 `gain(+)` is −703, its own `t` is 1.70, the best
> attainable one-sided rank p against 8 controls is 0.11, and §2.7 shows its A is one coin flip.
>
> **The p512/p2048 agreement is not evidence.** Their cosines (+0.532, +0.527, +0.512 at
> σ 0.01/0.02/0.04) and norm ratios (1.998, 2.027, 1.993) are the shared-256-pair-prefix values
> for a **zero** mean gradient, to three decimals, at every σ. Their board fingerprints correlate
> at +0.72 / +0.58, which is what cos 0.53 predicts on its own. Two halves of one draw.
>
> **And the rig's statistic is structurally broken at B, independently of the answer.** 14 of 56
> step thetas move 100.0 % of the boards in two disjoint tape families; every large A in the
> experiment — random and ES alike — is one of those crossings. κ and the antisymmetric gain at B
> are a Bernoulli readout of a single board-independent opening switch, with honest n = 1.

**Consequence for the campaign.** The audit's §5 reading ("B is not a peak, the estimator is
correctly signed but tiny, use a smaller step") is **withdrawn**: the positive α-0.1 antisym it
rested on is the σ 0.01 minus-side switch crossing, and it is reproduced by 4 of 8 random
directions. B's centre is neither confirmed nor condemned by this rig — **the rig cannot measure
it**, at any σ, at any step length, because the objective near B is dominated by one discontinuity
and the ES draws are pure sampling noise at P 2048 by their own norm test. Do not re-cut an arm on
a κ, do not lower `lr` on the strength of E3, and do not record "B is a peak". The measurable
thing here is the switch itself: which day-0 decision 14 of 56 small perturbations flip, and which
side of it B sits on, is a one-board-independent-lever question the engine judge *can* answer,
and it is worth more than another σ of this sweep.

### Files
`S/onestep_b/` — `build_thetas.py` (α rescaling, with the norm/mask/round-trip assertions),
`run_main.sh`, `run_rand003.sh`, `run_s0p04.sh`, `analyse.py` (pre-registered statistics),
`agree.py` (fingerprint correlations), `flips.py` (the boards-moved census),
`csv/e3b_{main,r003,s4}_{livec,topb2}.csv` (4,290 paired board rows, `shopdiff 0.0 %` throughout),
`analysis_final.txt`. Nothing under `S/onestep/` or `S/simscreen/` was written;
`git diff --stat src/` is empty; the judge lock was never taken.
