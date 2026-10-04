# BOARDSELECT — can a K-plan selector key on OUR OWN day-0 draw?

2026-09-17 10:24-10:35Z, worktree `boardselect` off `5baa0e8`, tools/tables `S/boardselect/`.
PLANSELECT (2026-09-17-planselect.md) closed rival-conditioned selection and left one
survivor: the oracle is a BOARD property keyed to the seed, and the seed's *own-seat* half
(our tiles, quadrant, money, shop timing at day 0) was never in the feature set. This box
reads that half out of the engine and prices the selector.

## 1 The day-0 draw does not exist (`day0_features.csv`, `tools/day0.py`)
Every PLANSELECT board-seat instantiated exactly as its leg runner does
(`scripts/eval_vs_baselines.py::_play`: `make("kaggriculture", {"seed": seed})` +
`town_inject.install_from_env(opponent)` + the seat order), **reset state read only, no game
played**: 224 board-seats, **2 distinct step-0 observations** — one per seat, the only
differing byte `observation.player`. Columns varying ACROSS BOARDS: **NONE**.

On every one of the 112 boards, both seats: money 3000; 10x10 tiles, 25 open (NW), 75
LOCKED, 0 other; `unlocked_quadrants ["NW"]`, farmer spawn (4,4), 0 hands; 0 seeds, 0 shed;
`town.unlocked_shops []`; market at the constant `MARKET_PARAMS` base/I0; RIVAL farm
byte-identical to ours.
Structural, not a sampling accident: `kaggriculture.py::_initialize` (l.244-275) builds
`_new_farm`/`_new_private`/`_new_market`/`_new_town` from the configuration alone. The
episode seed is resolved and **stored** (`env.info["seed"]`); it is first *consumed* in
`_end_of_day` (l.869-871, `random.Random((seed*1_000_003) ^ day)`) for the weed spawn and —
only at `day % 3 == 0` — the shop draw. Our seat's first seed-dependent observation is thus
a ~0.005/tile weed at the start of day 1 and the first shop at day 3.

Corollary: the seed's only *visible* half is the town unlock schedule, which PLANSELECT §2
already fed to the selector (`town-only d5` +531 t 0.94, `town FULL d5` +202 t 0.37, negative
at K=4/8) — the survivor had already been tested under another name.

## 2 Selector = control, exactly (`tables/select.csv`, `tools/select.py`)
Depth-3 tree and nearest-centroid over the day-0 vector, K = 2/4/8/all, against the
no-observation control (best training-mean plan), three evaluations. The feature vector is
constant, so the fitted selector is a constant function: per-board **max|selector − control|
= 0** in all 24 cells and the SELECTION increment is **+0 (se 0)**, in and out of sample, at
every K. K never moves the control either (its pick is the training argmax, always in K=2).

Control value vs FT2, both purses (pair = ours − theirs), per board:
| universe | eval | pair | t | Δours | Δtheirs |
|---|---|---:|---:|---:|---:|
| 4 plans banked on all legs | in sample | +441 | 0.83 | +954 | +513 |
| " | leave-one-LEG-out | +441 | 0.83 | +954 | +513 |
| " | **5-fold by seed** | **−35** | −0.13 | +642 | +677 |
| PLANSELECT per-leg (40/14/7/5) | in sample | +734 | 1.48 | +868 | +134 |
| " | **5-fold by seed** | **−448** | −1.56 | +349 | +797 |

Per leg, held-out by seed, rich universe: eng22 −209, v45 +168, topleg2 −867, topleg3 −818.
The shrinkage +734 → −448 is a two-purse story: the candidate plans keep ours up (+349) but
hand theirs more (+797), the MELONGIFT signature.

## 3 Verdict
(a) Our day-0 draw carries **zero bits**: 112 boards, one observation. (b) Selection
increment over the no-observation control: **exactly +0** at K=2/4/8/all, by construction,
not by noise. (c) Best realisable pair Δ/board out of sample for the whole fixed-plan family:
**−448 t −1.56** (rich universe) / −35 t −0.13 (cross-leg universe) vs the §115b bar
+450 t ≥ 3 — negative, on plans already HARD-REJECTED held-out (ESJUDGE3/CLIPTOP/PUMPCLIP).
(d) No `BOARD_SELECT_ON` spec: there is no day-0 branch to write, and no engine leg was
spent. **BOARD-ADAPTIVE PLAN SELECTION CLOSED** — with PLANSELECT that closes plan selection
on every observable axis (rival d0/2/5, town, own day-0 draw); the oracle's +1,739…+3,455
stays unrealisable.
