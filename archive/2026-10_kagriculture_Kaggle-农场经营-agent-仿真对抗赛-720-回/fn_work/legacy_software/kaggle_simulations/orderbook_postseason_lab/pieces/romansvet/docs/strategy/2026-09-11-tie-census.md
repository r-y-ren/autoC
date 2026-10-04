# The tie census at candidate B — how wide is the cell the ES is sampling?

2026-09-11. Tools: `S/ties/census.py`, `S/ties/pinned_check.py`, `S/ties/brain.patch`
(**unapplied**), `S/ties/pin_B.npz`, raw table `S/ties/census.json`.
Instrument: the xp-shim of `S/switch0/tie.py` — `brain.decide(xp, theta, obs)` takes its
array module, so a wrapper that delegates to `jax.numpy` and records every `floor` and
`argsort` argument sees every quantised decode, in order, with tracers intact so
`jax.jacrev` runs straight through it. **Nothing under `src/` was touched**
(`git diff --stat src/` empty); the tree read is `.claude/worktrees/arms-next`, the one
candidate B was trained in.

Centre: **B = `artifacts/kagg2_games/thetas/flow193_g100_hr.npy`**, padded to 6,789 params,
‖B‖ = 18.112, `hr` switches on, day-0 board (`sim.state.initial_state`), seat 0, one
decision.

---

## 1. What was enumerated

68 discretisations in one `decide`:

| group | n | what |
|---|---|---|
| `xp.floor` arguments | 55 (16 calls) | every `_qfloor` decode + both floors of each `_largest_remainder` |
| `absorb` thresholds | 5 | `drain[:,1] + DRAIN_CLIP·tanh(sat) > −DRAIN_CLIP`, one per crop |
| `argsort` rank keys | 8 | the leftover-allocation order inside the two `_largest_remainder`s |

Plus one boolean the shim cannot see because it is a Python comparison, priced analytically:
**`land_ok`** (`land_bias > −land_price`, i.e. `land_frac > −256`) — gap 3.378 steps,
‖∇land_frac‖ 62.2, **radius 0.054**. (`w_sum > 0` is inert: `w_sum` ≈ 1.)

For each: the decoded continuous value, the nearest boundary, the gap, ‖∇θ(value)‖ from
`jax.jacrev` over the full 6,789-vector, and the perpendicular radius `gap / ‖∇‖` — the
distance from B, in theta norm, to the nearest wall of its own cell.

## 2. The census

Radii (full table in `S/ties/census.json`, sorted):

| radius ≤ | ties | of 68 |
|---|---|---|
| 0.003 | **33** | 49 % |
| 0.005 | 38 | 56 % |
| 0.01 | **41** | 60 % |
| 0.02 | **46** | 68 % |
| 0.1 | **56** | 82 % |
| 1.5 | **62** | 91 % |

The 6 that are not in any band are not far — they have **exactly zero gradient**:
`press[WHEAT, TOMATO, STRAWBERRY, MILK, WOOL]` and `animal_defer` sit at
`_qfloor(0.0) = 1e-4` behind a `maximum(tanh(z), 0)` that is switched off, so the gene
behind them is dead at this obs, not merely distant.

The tightest ties are the **coin-scaled fixed points**, because their gradients are
100–2,000× larger (they are multiplied by `GROW_ONE` 256, `HIRE_BIAS_MAX` 400, or the
market `base` prices):

| tie | value | gap | ‖∇‖ | radius |
|---|---|---|---|---|
| `plant_rankkey[MELON]` | −0.77829 | 0.00095 | 28.1 | 3.4e−5 |
| `grow_mult[MELON]` | 168.063 | 0.063 | 1196.6 | 5.3e−5 |
| `grow_mult[STRAWBERRY]` | 199.106 | 0.106 | 1510.0 | 7.0e−5 |
| `press[MELON]` | 49.201 | 0.201 | 1803.0 | 1.1e−4 |
| `all_bias[bucket 2]` | −2.203 | 0.203 | 1618.9 | 1.3e−4 |
| **`animal_count`** | **6.99129** | **0.0087** | 31.9 | **2.7e−4** |
| `hold[MILK]` | 132.201 | 0.201 | 913.4 | 2.2e−4 |
| `forward_days` | 2.920 | 0.080 | 55.7 | 1.4e−3 |
| **`n_dev`** | **28.68582** | **0.314** | 91.6 | **3.4e−3** |
| `plant_lr[WHEAT]` | 10.760 | 0.240 | 53.1 | 4.5e−3 |
| `land_frac` | −252.622 | 0.378 | 62.2 | 6.1e−3 |
| `animal_lr[COW]` | 4.124 | 0.124 | 11.2 | 1.1e−2 |
| `plant_lr[STRAWBERRY]` | 0.1789 | 0.179 | 6.84 | 2.6e−2 |
| `crew_target` | 0.00021 | 0.0002 | 0.0035 | 5.9e−2 (saturated at day 0) |
| `compact` | 7.836 | 0.164 | 2.18 | 7.5e−2 |
| `absorb_margin[*]` | 6.07–6.10 | 6.07–6.10 | 20.0 | 0.30 |

**§66 is confirmed to the digit**: `n_dev` = 28.68582 against the boundary at 29, and
`animal_count` = `_qfloor(animal_share · n_dev)` = 6.99129 against 7 — a gap of 0.0087,
which one gene of the head crosses at 2.7e−4 of theta norm.

Split by what the integer *means*: of the 46 ties inside 0.02, **18 are coarse**
(tile/hand/day counts and allocation ranks, where one unit is a different strategy) and
28 are coin-scaled fixed point (where one unit is 0.2–1 % of a value in the hundreds).

## 3. The scale that matters is σ, not ‖σε‖

A member's perturbation has norm ‖σε‖ = 1.65 at σ 0.02 (0.41 at σ 0.005), but ε is
isotropic in 6,789 dimensions, so the *decoded value* moves by
∇·σε ~ N(0, σ²‖∇‖²): the displacement along any one tie's normal is **σ‖∇‖**, i.e. the
tie flips with probability ≳ 0.32 whenever its **radius ≲ σ**. So the readable line of the
table is `radius ≤ 0.02` (46/68) and `radius ≤ 0.005` (38/68) — not the 1.5 band.

Measured, 64 draws of ε (`S/ties/census.py`, seed 20260911):

| σ | ‖σε‖ | floor cells crossed / 55 | `Macro` integers changed / 42 | members decoding B's plan |
|---|---|---|---|---|
| 0.02 | 1.649 | **33.9** (sd 2.3) | **27.4** | **0 / 64** |
| 0.005 | 0.412 | **25.0** (sd 3.1) | **21.2** | **0 / 64** |

The prediction from the radius table (46 and 38 ties inside one σ) and the measurement
(33.9 and 25.0 crossings) agree. Per `Macro` field, P(field differs from B's) at σ 0.02 /
σ 0.005:

`hold` 1.00/1.00 · `press` 1.00/1.00 · `grow_mult` 1.00/1.00 · `hire_bias` 0.97/0.94 ·
`dev_weight` 0.97/0.75 · **`plant_target` 0.95/0.52** · `forward_days` 0.66/0.36 ·
`land_bias` 0.64/0.14 · **`animal_want` 0.61/0.48** · `compact`, `crew_target`,
`animal_defer` 0.00/0.00 (all three saturated on a day-0 board).

**Cells per member ≫ 1, on one decision.** A game is ~30 days × 2 seats, so the number of
independent cell draws behind one fitness number is of order 10³. **§59–§63 is the
mechanism**: the ES is not estimating a gradient through a rough surface, it is drawing a
fresh integer plan per member and reading its score.

## 4. The structural fact underneath it

**Every one of `Macro`'s 12 fields is an integer** (`plant_target` int[5], `animal_want`
int[3], `land_bias`, `hold` int[9], `press` int[9], `grow_mult` int[9], `compact`,
`dev_weight`, `hire_bias`, `crew_target`, `animal_defer`, `forward_days` — 42 integers).
`Macro` is the whole interface between theta and the planner. So the theta→plan map is
piecewise constant **by construction**, with no continuous component at all, and
"smooth the decode" cannot mean "pin every integer": pinning all 42 makes the policy
*exactly independent of theta* and the gene count zero.

What separates the two halves is the integer's **range**, not the floor:

* **coarse** — `plant_target`, `animal_want`, `crew_target`, `compact`, `forward_days`,
  and the land decision: counts of tiles, hands and days in the single digits. One unit is
  a different strategy. 12 integers.
* **fine** — `hold`, `press`, `grow_mult`, `dev_weight`, `hire_bias`, `animal_defer`:
  coin- or fixed-point-scaled (`GROW_ONE` = 256, `HIRE_BIAS_MAX` = 400, `_BASE` prices),
  values in the tens to hundreds. One unit is 0.2–1 % — a grid fine enough to read as a
  surface at σ 0.02. 30 integers.

## 5. Which genes are alive, and where

`jacrev` over the whole 6,789-vector at this obs:

| | params |
|---|---|
| non-zero gradient onto **some** tie | 3,548 |
| onto at least one **fine** tie | 3,119 |
| onto **coarse ties only** | **429** |
| zero gradient at this obs | 3,241 |

The 429 coarse-only genes are exactly the heads that size the strategy and nothing else:
`g2`/`gb2` columns 2, 5, 6, 7 (animal-mix sharpness, `dev_frac`, `animal_share`,
plant-mix sharpness) 132 · `g5`/`gb5` (`aux[2]` → `dev_frac`) 33 · `g6`/`gb6`
(`dev[0]` → `compact`) 33 · `g8`/`gb8` (animal mix) 99 · `g10`/`gb10` (crew ramp
top/mid/steep) 99 · `g11`/`gb11` (forward days) 33.

The 3,241 dead ones at this obs are the forecast blocks on an empty day-0 board
(`g3`/`gb3`, `g4`/`gb4`, `fh`, `fs`, `fv` = 1,242 entirely, plus half of `w1` and `g1`);
they wake on a planted board, so this column is a property of the obs, not of B.

## 6. PIN-THE-INTEGERS — the proposed mode (`S/ties/brain.patch`, unapplied)

**Option 1 (chosen).** `KAGG3_PIN_INTS=<file.npz>` (key `theta`) holds the *coarse* fields
at whatever a **reference theta decodes on the same obs** — not at a captured constant,
because the counts track the board (`n_dev` is a share of `n_free`, `crew_target` is a
sigmoid in the day, `plant_target` sums to `n_dev − Σanimal_want`). The patch renames the
existing body to `_decide` and adds a 10-line wrapper:

```python
def decide(xp, theta, obs):
    macro = _decide(xp, theta, obs)
    ref, fields = _pin_ref()                 # cached from the env
    if ref is None:
        return macro
    pinned = _decide(xp, xp.asarray(ref), obs)
    return macro._replace(**{f: getattr(pinned, f) for f in fields})
```

`PIN_FIELDS_DEFAULT = (plant_target, animal_want, crew_target, compact, forward_days,
land_bias)`; `KAGG3_PIN_FIELDS` overrides it for ablations. Cost: two forward passes of
the (small) head per decision.

**Gene count in pinned mode: 6,360 free, 429 frozen.** The 429 coarse-only genes must be
frozen as well as pinned — otherwise they random-walk under a fitness that cannot see
them, and the trained theta's *unpinned* play would decode different counts from B's,
making the pinned fitness not the shipped fitness. (429 is the count at this one obs;
the mask has to be re-measured over a day × board panel before a launch — see §7 step 0.)
Of the 6,360, 3,119 have a live path at the day-0 obs.

**Option 2 (soft / straight-through decode) — rejected.** Three reasons, in order of
weight:

1. **ES is gradient-free.** A straight-through estimator exists to carry a *backward* pass
   through a floor; the ES never differentiates the decode, it only samples fitness. A
   soft decode helps only if **the soft decode is what plays** — and then it is not an
   estimator trick, it is a different policy.
2. **It cannot play.** The engine takes integer tiles, hands, animals and lots. A
   temperature-softened `floor` produces 10.76 tiles of wheat, which nothing downstream
   accepts, so the soft value would have to be re-rounded at the planner boundary — i.e.
   the same floor, one function later.
3. **sim-equals-engine.** Training on a soft decode and shipping a hard one means the
   optimised policy and the shipped policy differ by up to one integer on every one of the
   42 fields — which *is* the §59 gap, moved rather than closed. The 99.5 % sim/engine
   agreement and `tests/test_backend_agreement.py` rest on `decide` being one arithmetic
   program; the pinned patch keeps it (unset env = the identical graph, the pin is a
   `Macro._replace`, never a different arithmetic path), a soft decode would not.

So pinned mode is both the safer one for the package (the env is never set by
`scripts/package_submission.py`, never by a judge leg, never by the engine) and the only
one ES can use at all.

**No existing flag to reuse**: `grep -n "decode|hard|soft|pin|quant"` over
`scripts/train.py` and `src/kagg3/es/train.py` finds only prose and `--pin-theta` (which
pins a *frozen opponent* into the ladder, an unrelated meaning). `KAGG3_PIN_INTS` follows
the `KAGG3_OPENING` convention already in `core/plan.py`.

**Verification of the patch** (`S/ties/pinned_check.py`, scratch copy of the tree with the
patch applied — never `src/`):

| mode | coarse ints changed / 12 | fine ints changed / 30 |
|---|---|---|
| env unset, σ 0.02 | 3.62 (0 % identical) | 23.73 |
| env unset, σ 0.005 | 1.55 (20 % identical) | 19.62 |
| **pinned at B**, σ 0.02 | **0.00 (100 % identical)** | 23.73 |
| **pinned at B**, σ 0.005 | **0.00 (100 % identical)** | 19.62 |

Unset, the patched tree reproduces B's Macro exactly (`plant_target [11,11,0,0,0]`,
`animal_want [1,4,1]`, `land_bias −989`, `compact 7`, `forward_days 2`) — the patch is
inert. Pinned, the coarse half is constant and the fine half still moves, which is the
objective the ES would see.

## 7. The pinned-mode one-step test (what would falsify "no gradient")

The rig exists: `S/onestep` (the GPU driver `sweep_b.py` — the arm's own antithetic,
rank-normalised estimator at B, R = lr·√n_live = 0.2323, 8 random ± controls, eps seed
9001, engine κ from `S/onestep/kappa.py`) and `S/onestep_b` (the CPU screen version —
`S/simscreen/screen.py --ref B`, α-rescaled step thetas, paired on LIVE-C 120 +
TOPB2 40). Pinned mode changes **two** things and nothing else.

0. **Measure the freeze mask** over a panel (≈200 obs: 30 days × 6 boards, both seats) —
   the union of genes whose jacobian is non-zero on coarse rows only. 429 is the day-0
   figure; the panel figure is the one to freeze.
1. Stage the patch: `rsync` the tree to a stage dir, `git apply S/ties/brain.patch`
   there. **Never `src/`.**
2. `export KAGG3_PIN_INTS=<stage>/S/ties/pin_B.npz` for the estimator *and* for the screen,
   so the reference and the arms are pinned alike.
3. Build the directions **inside the free subspace**: the live mask that `sweep_b.py`
   already applies, minus the frozen coarse-only genes — otherwise the random controls
   spend their length on genes the pinned objective cannot see and the comparison is
   rigged in the gradient's favour.
4. Score exactly as `S/onestep_b/run_main.sh` does (α ∈ {0.03, 0.1, 1.0}, LIVE-C 120 +
   TOPB2 40, paired vs B), then `S/onestep/kappa.py` for
   `antisym = F(+d) − F(−d)`, `z = antisym/sd(randoms)`, `κ = z/√n_live`.

**Self-check before anything is read** (free, and it fails loudly): B pinned at B must
reproduce B's own csv to the coin on both legs. The pin is idempotent at its own centre;
if that leg moves, the patch is wrong and nothing below means anything.

**GO** — relaunch an ES arm in pinned mode — requires all three:
* **κ ≥ 0.03** at some (σ, P), i.e. ≥ 3× the 0.004–0.011 the unpinned E3 sweep measured at
  this same centre (`S/onestep` README §1, `S/es-noise-floor` memory);
* the **+d arm beats B on both legs at both α**, with Δ(+d) ≈ −Δ(−d) (antisymmetry — a
  one-sided gain is curvature or a lottery, not a gradient);
* **+d beats ≥ 12 of the 16 random ± controls**, the same bar the g940 positive control
  cleared (16/16 there).

**NO-GO** — κ ≤ 0.015 or +d still loses. That **falsifies the tie hypothesis as the
binding constraint**: either the coin-scaled genes carry no fitness at B (B is a peak in
the fine subspace and every remaining gain is a cell *jump*, which no local method finds),
or the variance is the end-of-day shop re-roll rather than the cells (±25k zero-mean per
tile change — `shop-lottery` memory), which the pin cannot touch. Either result is worth
having: it is the first measurement that separates "rough objective" from "wrong seat",
and the next move after a NO-GO is a changed objective, not a changed σ.

**A pinned arm is a polish, never a promotion path on its own.** Its coarse genes are
frozen, so before any judge leg the trained theta must be replayed **unpinned** on a board
panel and shown to decode B's counts exactly; if it does not, the fitness it was selected
on is not the fitness it will be judged on, and the run is void.

## 8. Standing

* `git diff --stat src/` is empty. `S/ties/brain.patch` is **unapplied**; it dry-run
  applies clean to both `.claude/worktrees/arms-next/src` and the repo `src/`.
* Nothing was launched, no judge lock taken, no engine leg run, no ssh.
