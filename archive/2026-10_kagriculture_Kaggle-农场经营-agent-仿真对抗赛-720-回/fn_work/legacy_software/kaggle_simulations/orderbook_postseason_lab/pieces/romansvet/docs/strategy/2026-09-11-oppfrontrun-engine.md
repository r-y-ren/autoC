# OPP_FRONTRUN — screen and paired engine judge vs candidate B

2026-09-11.  Build and judge of `S/oppsell/plan.patch` (design
`docs/strategy/2026-09-11-oppsell-design.md`, plan `S/oppsell/README.md`).
Theta is candidate B (`artifacts/kagg2_games/thetas/flow193_g100_hr.npy`) in every arm —
this is a switch, not a training change.  Base switches
`OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True`.

## 0. Build

`git apply --check` and `git apply` both clean at b906407, `py_compile` clean, in a
PRIVATE copy of the arms-next worktree (`/root/wt_oppsell`).  `git status --porcelain src/`
stays empty in the main worktree and in `.claude/worktrees/arms-next`.
The patch's own helper smoke reproduces `S/oppsell/helper_smoke.txt` to the coin:
lot-3 delta `[4,0,0,18,0,0,3,3,2]` (lot 1 untouched, products they do not hold at 0),
hold cut `{WHEAT 2, STRAWBERRY 23, MILK 40, WOOL 2, FERTILIZER 7}`, inert on d12 and on
the terminal day.

**Arm encoding.**  The switch string is comma-split (`S/drainpin/on2b.py`,
`S/simscreen/screen.py`), so the design's `OPP_FRONTRUN_DAY=(0,...)` form cannot be
passed.  `_FRONTRUN_DAY` / `_FRONTRUN_NIGHT` are the module-level arrays the helpers
actually read, and setting either to the scalar `0` zeroes that half exactly
(`on * hit * 0` broadcasts to int32[9] zeros) — verified in the smoke above.

| arm | switches appended | half |
|---|---|---|
| A0 | `OPP_FRONTRUN_ON=True,OPP_FRONTRUN_SCALE=0` | identity |
| A1 | `OPP_FRONTRUN_ON=True,_FRONTRUN_NIGHT=0` | intraday (inv) alone |
| A2 | `OPP_FRONTRUN_ON=True,_FRONTRUN_DAY=0` | interday (hold) alone |
| A3 | `OPP_FRONTRUN_ON=True` | both |
| A4 | `OPP_FRONTRUN_ON=True,_FRONTRUN_NIGHT=0,OPP_FRONTRUN_SCALE=50` | A1 at half dose |

**Identity check (step 1).**  OFF (`OPP_FRONTRUN_ON=False`) reproduces B's screen rows
**byte for byte** on the first 10 TOPB2 boards (10/10 on mine/theirs/margin/shop_sig), and
A0 (`SCALE=0`) reproduces them on all 40 (40/40).  Both helpers return their argument
object, so OFF allocates nothing.

## 1. Screen (`S/simscreen/screen_opp.py`, the frozen board files, CPU, pinned-town sim)

Paired by board against B's own baselines `S/simscreen/topb2_40.csv` (fit set) and
`full120.csv` (LIVE-C, the honest read).  `d` and `t` are on the board unit.

| arm | TOPB2 d | t | W/L | dours | dtheirs | **LIVE-C d** | **t** | W/L | dours | dtheirs | win% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A0 | 0 | — | — | 0 | 0 | — | — | — | — | — | identical |
| A1 | +191 | +0.60 | 8/12 | −564 | −755 | **+285** | **+2.68** | 37/23 | −434 | −719 | 86→90/120 |
| A2 | −146 | −1.22 | 2/9 | +50 | +196 | **−179** | **−2.81** | 6/30 | −103 | **+76** | 86→86 |
| A3 | +60 | +0.20 | 8/12 | −394 | −454 | +136 | +1.19 | 29/31 | −459 | −595 | 86→90 |
| A4 | −3 | −0.02 | 11/9 | −332 | −329 | +162 | +2.52 | 40/19 | −172 | −334 | 86→88 |

* **A2 refused** on both stated grounds: Δ ≤ 0 on LIVE-C (−179, t −2.81, 6 boards up
  against 30 down) **and** `dours (−103) < dtheirs (+76)` — the interday hold cut takes
  coins off *us* and hands them *theirs*, the exact `OPP_SUPPLY_ON` signature.  The
  README's own risk note ("the hold cut is large on the steep products, MILK 40 → 0") is
  what happened.
* **A3 is A1 diluted by A2** and is inside noise; **A1 is the best surviving arm**, A4 the
  runner-up.  Dose response is monotone and in the right order (0 → +162 → +285), so A1
  is not a half-dose tuning artefact.

## 2. Engine judge, A1 (`S/oppsell/engine.sh`, WORKERS=5, names `of_*`)

`S/bank/paired.py` ALL lines, arm minus B.  No VOID line on any leg.

| leg | n | winOFF | winON | dmargin | sd | t | dours | dtheirs | W | L |
|---|---|---|---|---|---|---|---|---|---|---|
| TOPB2 (fit) | 40 | 32.5 % | 30.0 % | **+223** | 1424 | 0.69 | −562 | −785 | 0 | 1 |
| LIVEC-H30 (held out) | 60 | 63.3 % | 66.7 % | **+247** | 846 | 1.58 | −545 | −792 | 2 | 0 |
| LIVEC-H30B (held out) | 60 | 83.3 % | 80.0 % | **+250** | 795 | 1.71 | −355 | −604 | 0 | 2 |
| LIVE62 (tripwire) | 124 | 85.5 % | 87.1 % | **−365** | 870 | **−3.35** | **−633** | **−268** | 4 | 2 |
| LIVE-C pooled (`S/fertcow/pool_livec.py`) | 60 boards | 44/60 | **44/60** | +248 | 821 | 2.34 | | | | |

**Flipped-board census.**  H30 `107498954` both seats → WIN (+1,046 each).  H30B
`107632627` both seats → LOSS (−1,207 each).  TOPB2 `107460230` seat 1 → LOSS (−2,182).
LIVE62 `107090008`, `107160628` → WIN, `107140814` → LOSS (both seats each).
**Net game flips on the pooled LIVE-C legs = 0** (+2 / −2).
Moves are flat everywhere (H30 2867→2872, H30B 2896→2894, TOPB2 2887→2882,
LIVE62 2878→2880): the allocation shifts, it does not shrink — the design's own first
falsifier is NOT tripped.

## 3. The ledger check — their late c/u (`S/topledger/ledger_opp.py`, TOPB2 40 boards)

B = `topb2_B.npz`, arm = `topb2_ofa1.npz`, same boards, same sim.  d0-14 is identical to
the coin on every board (the d15 gate holds).

| board set | our d15-21 c/u | their d15-21 c/u | our d22-29 c/u | their d22-29 c/u | d_ours d15-29 | d_theirs d15-29 |
|---|---|---|---|---|---|---|
| all 40 | 118.2 → 118.0 | 99.0 → **98.5** | 79.0 → 78.1 | 61.1 → **60.3** | −598 | −756 → PASS |
| **B-LOSS boards (27)** | 126.4 → 126.3 | 106.8 → **106.3** | 76.4 → 75.4 | 64.3 → **63.6** | **−806** | **−699** → **FALSIFIED** |
| B-WIN boards (13) | 102.2 → 101.9 | 83.1 → 82.7 | 84.5 → 83.7 | 54.0 → **53.0** | −164 | −874 → PASS |

**The mechanism is real and it is mis-targeted.**  Their realised late c/u does fall, at
exactly flat units (their units move +0.0 in every band — they are a tape).  But the fall
is 0.5-0.8 c/u where the README's target is 16 c/u, i.e. ~4 % of what the boards need; and
the split is backwards: on the boards B already **wins** we take 874 off them for 164 of
ours, while on the boards B **loses** — the ones the whole design exists to flip — we give
up 806 to take 699, which is the two-purse falsifier the README wrote in advance.
Our own late c/u never rises on any board set.

## 4. Verdict

**A1 (intraday half, full dose) — LEVEL on margin, REFUSED for promotion.**
The four-leg PASS rule fails on three counts: `dmargin > 0` is false on LIVE62
(−365, t −3.35); net game flips on the pooled LIVE-C legs are **0**, not ≥ +2, and Kaggle
scores wins; and the two-purse split is falsified where it matters — on LIVE62
(`dours −633 < dtheirs −268`) and on the TOPB2 boards B loses (−806 vs −699).  The three
promotion legs are each positive but none reaches |t| 2 on its own, the pooled LIVE-C
t 2.34 buys no extra board, and both purses fall on every leg: this is the displacement
signature, with the margin coming from their purse falling slightly faster on the boards
we did not need.

**A2 (interday half) — LOSS, refused at the screen** (LIVE-C −179, t −2.81, 6/30, and it
*raises* their purse).

**A3 (both halves) — LEVEL at the screen**, not judged: it is A1 plus a refused half.

**A4 (A1 at half dose) — LEVEL, and it confirms the dose is not the problem.**
Engine legs: TOPB2 n 40, winOFF 32.5 % → winON 32.5 %, dmargin **+38**, sd 699, t 0.24,
dours −338, dtheirs −375, 0 flips; LIVEC-H30 n 60, 63.3 % → 63.3 %, dmargin **+181**,
sd 394, **t 2.50**, dours −153, dtheirs −333, **0 flips**.  The engine dose response is
monotone (H30 +181 at half dose, +247 at full), both purses still fall, and half the dose
flips no board at all — so A1's margin is the lever, not a tuning artefact, and the lever
is simply too small to move a game.

The family reading: the patch does what it says — it is byte-exact OFF, it is gated, it
shifts rather than shrinks, and it measurably depresses the other seat's realised late
price at flat volume.  It is simply an order of magnitude too small, and the ordering it
buys lands on boards that were already won.  Phase 2 (`mkt_inv_prev`, per-board inference
instead of a 30-tape mean) is the only version of this worth another engine slot, and only
if it can be made to fire on the loss boards.
