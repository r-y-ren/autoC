# ROUTEORDER — the intra-block visiting order, measured and built

2026-09-16 20:54–22:10Z, branch `routeorder` off master `bb695a2` (FT2 +
ROUTEEFF). Follow-up to `2026-09-16-routeeff.md` §6, which closed the
development-order lever and named this as the remaining mechanism. Legs:
ENG22 (22 engine tapes, both seats, 3 seed draws) and V45LEG (30 post-09-15
band tapes). No training, no upload, remote untouched.

## 1. VERDICT

**The walk-minimal visiting order is worth +7,372/board at spot, 90 % of it is
reachable by a static sort key — and 86 % of THAT is forbidden by the one guard
the reorder cannot drop.** `ROUTE_ORDER_ON` (block-local boustrophedon, built
here) moves the term 9 % and reads **ENG22 +433/game, sd 1,815, se 158,
t +2.74, n=132 (3 seeds x 44)**, our purse +498 / theirs +65 — **over the kill
bar (+100, t 2) on the pooled leg, under it on any single seed (+312 t 1.03 /
+429 t 1.44 / +559 t 2.59)**. **V45LEG −175/game, se 97, t −1.80**, board win
70.0 → 70.0 %. The switch ships **OFF**; the lead decides whether a POOLED180
is worth it on a +433/−175 split.

## 2. How a unit's day is ordered today (`plan.py:_routes`, :10063 in the base tree, :10122 here)

1. The day ranks every task tile once, into `order` (`_rank_near`, the
   `compact` gene over the serpentine); the first `n_tasks` ranks carry work.
2. Each unit takes a **contiguous block of ranks** `[s, e]`: it walks from its
   spawn to rank `s`, then works ranks in **rank order**, one after the other.
   The block ends at the largest `e` whose `L(e) = base + cum[e] − cum[s] +
   max(D(s,e), land_lead)` fits the turn budget — so the walk inside a block is
   exactly the sum of consecutive Manhattan hops **in `order`**, and nothing
   anywhere minimises it.
3. The only existing reorder is `HARVEST_FIRST_ON` (OFF): a static-key sort of
   the block expressed as a pairwise count, priced against the wall
   `total ≤ bud − lead` and a **shed-distance gate** (never end farther from a
   shed access than the rank order would). Pickups are the block's **lead**,
   charged before rank `s`, so no permutation can move an op in front of the
   pickup that loads it.

## 3. The reachable ceiling (`S/routeorder/probe.py` + `ceiling.py`)

The probe records the **ordered op path** of every unit-day, both seats, real
engine (the ROUTEEFF step ledger plus `path`/`sx`/`sy`; the path's Manhattan
length reproduces the engine's MOVE count to the step, 26,170/26,170). Each
unit-day is cut at every shed interaction (PICKUP / DROP / PLACE), which stay
pinned — that is the pickup-before-use constraint — and the distinct tiles of
each segment are re-visited in the cheapest order (exact for k ≤ 7, else
NN + 2-opt + or-opt). Priced like ROUTEEFF: spot on the landing day, our own
impact ON, seed charged on the PLANT share, nothing past d29, our purse only.

| order family (d20-29, ENG22 22 boards / TOPLEG 19) | moves saved /unit-day | 1:1 | at 2.211 steps/op |
|---|---:|---:|---:|
| **FREE** (open TSP path) | **1.39 / 1.32** | **+7,372 / +7,643** (t 15.7 / 14.5) | +3,546 / +3,629 |
| PREC (producers before consumers) | 0.96 / 0.90 | +5,317 / +5,393 | +2,525 / +2,544 |
| **SERP** (best of 4 boustrophedon keys) | **1.25 / 1.18** | **+6,723 / +6,917** | +3,243 / +3,274 |

Two facts decide the build (`S/routeorder/gatevar.py`, `serpvar.py`):

* **The saving is not interior re-ordering.** Pin a unit-day's first and last
  tile and optimise everything between them: **0.047 moves/unit-day**. The
  whole 1.39 is *where the day starts and ends*.
* **A single fixed key is worth nothing** (−0.01: `order` already is a
  serpentine). All four orientations (rows/columns × either end) are what pays,
  so the switch computes all four and takes the cheapest.

## 4. The switch — `ROUTE_ORDER_ON` (default OFF), plan.py:2392 (constants), :10038 (`_ro_block`), :10494 + :10554 (the two passes and the decode hand-off)

**Block-local boustrophedon with an earned extension.** Per unit, per day:

* Four static per-rank keys (sweep rows or columns, from either end, each line
  taken against the one before it) → `_ro_block` turns a key into a permutation
  with **`xp.argsort`** on `key*N_T + idx` (distinct by construction), and into
  the block's own local clock `cum2` — the same five arrays `harvest_first`
  builds by hand, so the existing traced decode is reused unchanged. No Python
  loop over traced values; it traces under `jax.jit`.
* **Pass 1** takes the cheapest of the four, refused unless it is *strictly*
  shorter than the rank order, fits `bud − lead`, and passes the shed gate.
* **Pass 2** spends what pass 1 saved: recut at `bud + sav`, re-sweep the wider
  block, take the extension only if the swept total still fits the REAL window
  — so no admitted rank is ever one the route cannot reach.
* Never on a block an excursion claimed (`ins > 0`); asserts against
  `HARVEST_FIRST_ON` (one mechanism, never both).

`tests/test_routeorder.py` (8 pass): whole-plan sha256 OFF-identity against
`git archive bb695a2 src` via `tests/_pin.py`, the pickup-before-use assertion
on the emitted route, shape/turn-budget, the mutual-exclusion assert, jit.

## 5. Legs

| leg | Δ margin/game | sd | se | t | our | theirs | win | flips |
|---|---:|---:|---:|---:|---:|---:|---|---|
| ENG22 seed 0 (n 44) | +312 | 2,012 | 303 | +1.03 | +433 | +120 | 40.9 → 43.2 % | +1/−0 |
| ENG22 seed 1 (n 44) | +429 | 1,978 | 298 | +1.44 | +482 | +53 | 43.2 → 40.9 % | +0/−1 |
| ENG22 seed 2 (n 44) | +559 | 1,431 | 216 | +2.59 | +579 | +20 | 40.9 → 40.9 % | +0/−0 |
| **ENG22 pooled (n 132)** | **+433** | 1,815 | 158 | **+2.74** | +498 | +65 | 41.7 → 41.7 % | +1/−1 |
| **V45LEG (n 60)** | **−175** | 753 | 97 | **−1.80** | +97 | +272 | 70.0 → 70.0 % | +0/−0 |
| ENG22 **no shed gate** (n 44) | **−1,864** | 3,929 | 592 | **−3.15** | −633 | **+1,231** | 40.9 → 38.6 % | +1/−2 |

**The mechanism fires, and by exactly the amount the gate leaves it**
(`S/routeorder/raw_on`, 22 boards ON vs OFF, d20-29): `mid_move` **8.929 →
8.862**, moves **10.175 → 10.082**, prod ops **10.340 → 10.389**
(+5 ops/game), distinct tiles 5.047 → 5.068, `present` unchanged. That is
**9 % of the ROUTEEFF gap** — and it is what the gate allows: the gated sweep
ceiling is **0.169** moves/unit-day against the ungated **1.250** (50 % of
segments improvable falls to 9 %).

**The gate is load-bearing, re-confirmed at n=44**: without it the switch takes
7× more of the term and loses −1,864, and the loss is **their purse** (+1,231
to them against −633 of ours) — a block that ends far from a shed access
wrecks the tail, the DROP leg and the lot it feeds. This is the 2026-09-03
`HARVEST_FIRST_ON` census (36 % of blocks, +0.41 tiles) priced in coins.

## 6. Standing

* `mid_move` is real and large, and **86 % of it is behind the shed gate**, not
  behind the sort key. The remaining head-room on this term is *not* another
  visiting order: it is a block whose END is chosen with the shed in it — i.e.
  the block **assignment** (`_cut`), not the block's internal sweep.
* `ROUTE_ORDER_ON` ships OFF and is pinned byte-identical to `bb695a2`.
  ENG22 +433 t 2.74 / V45LEG −175 t −1.80 is a split read, not a promotion.

## 7. Repro

```bash
WORKERS=3 bash S/routeorder/run_all.sh instrument        # 52 boards, ~6 min
.venv/bin/python S/routeorder/ceiling.py                 # the priced ceilings
.venv/bin/python S/routeorder/gatevar.py                 # what the gate costs
.venv/bin/python -m pytest -q tests/test_routeorder.py   # 8 tests, OFF identity
FT2="OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True,\
brain.MELON_GENE_ON=True,brain.CROP_DAY_ON=True,LOT4_ON=True,LOT4_TURN=17,\
SELL_SLOT_PRIORITY_ON=True,FERT_TIMING_ON=True,FERT_TIMING_DAYS=2"
WORKERS=3 bash S/judge7065/run_eng22.sh routeorder artifacts/kagg2_games/thetas/\
flow193_g100_hr.npy /mnt/e/_work/kaggriculture3-routeorder "$FT2,ROUTE_ORDER_ON=True"
.venv/bin/python S/nexthigh/pair.py S/lossflip/ft2_eng22.csv S/lossflip/routeorder_eng22.csv
```
