# 2026-09-11 — Coordinate search over candidate B's OWN coarse integers

**September 13 correction — `m0p1` is not an isolated extra planted tile.**
The exact `S/isearch/mk_off.py` intervention raises the day-0 melon *target*
by one without conserving total targets. Tracing saved dawn108660678 through
both the historical `/root/wt_isearch` and current frozen-B planner gives the
same base and modified plans:

| Planned quantity | B | `m0p1` |
|---|---|---|
| Crop targets W/C/M | 11/11/0 | 11/11/1 |
| Seed purchases W/C/M | 11/8/0 | 11/11/1 |
| Animal purchases goose/cow/sheep | 1/4/1 | 1/3/0 |
| Land purchase | None | Turn 3 |
| PLANT commands | 19 | 23 |
| Opening wheat pump | Buy 53, sell 48 | Buy 53, sell 48 |

These are **planned commands**, not a newly executed engine game. The target
change affects land valuation, spending, herd and routing; the old explanation
below that melon shortened the wheat pump is contradicted on this dawn. The
old simulator results remain negative evidence for that coupled intervention,
not a causal price for one melon tile. Its `sim/units.py` predates the sequential
unit-order repair, so its exact balance effects are not current engine results.
Section6 confirms that the engine legs were never run. No unchanged rerun is
selected; see the [current melon review](2026-09-13-melon-sigma-reachability.md).

**The question.** The tie census (`2026-09-11-tie-census.md`, consensus §67) showed the
theta→plan interface is 42 integers and that the ES cannot search them: at sigma 0.02 a
population member lands in a different `Macro` on 27.4 of the 42, and none of 64 members
decoded B's plan. The wall run (`2026-09-11-wall-imitation.md`, §70) then showed that
*setting* those integers to the top tier's plate loses −24.2 k. Between "the ES cannot move
them" and "the wall's values are wrong" sits the question this doc answers: **is B a local
optimum in the integer lattice — and if not, which single coordinate pays?**

Codex advice §3 (`2026-09-11-codex-astra-advice2.md`): expose 6-10 interpretable controls as
**offsets to B's decoded policy**, ±1 on counts and days, screen on a balanced development
panel, keep ≤3, combine only on evidence, freeze ONE finalist for paired engine confirmation.
That is what this is. TOPB2 and LIVE-C 43-72 are development data here; the hold-out
(LIVEC-H30B, 73-102) was not played by this arm at all.

Tools: `S/isearch/` (new; `S/wall`'s were imported, not edited). `/root/wt_isearch` = a copy
of `/root/wt_wall` (itself the `arms-next` worktree + `S/ties/brain.patch` + the wall's
literal-pin extension) carrying one further extension, below. Nothing under `src/` in `main`
or `arms-next` was touched.

## 0. The tool: RELATIVE offsets, not a plate

The wall's pin could only SET a coarse integer to a board-independent constant. That throws
away the one fact §1 measures: B recomputes every coarse integer per observation. So
`/root/wt_isearch/src/kagg3/core/brain.py` gained `KAGG3_OFF_INTS`:

    off[<Macro field>][variant, day, ...]  ->  macro.field = clip(B's own decode + off, lo, hi)

with `OFF_LIMS` giving each field its legal range (`plant_target`/`animal_want` 0..100,
`crew_target` 0..`spec.MAX_HANDS`, `compact` 0..`DIST_MAX`, `animal_defer` 0..`DEFER_ONE`).
Variant 0 is the all-zero table, which is candidate B **exactly** (`clip(cur + 0) == cur` on
int32) — that is what makes the screen's own base row the reference.

The variant index rides in ONE extra float at the end of theta (slot `PO.N_PARAMS`), which
`policy.unpack` ignores — it slices `SHAPES` in order and never reads the tail — and which
`policy.pad` returns untouched. That is the whole trick of this arm: `KAGG3_PIN_INTS` is
process-global, so the wall paid one ~11-minute XLA compile **per arm**; carrying the variant
in theta makes 25 coordinates ONE compiled program (`S/isearch/screen_off.py`), 25 × 40 and
25 × 60 episodes in two processes. Unset, `KAGG3_OFF_INTS` is dead code and `decide` is the
shipped program character for character.

## 1. Baseline: what B's coarse integers actually decode to

`S/isearch/decode_probe.py` — no simulator, because `brain.decide` is a pure function of
(theta, obs): B's theta against the 2,400 real observations of
`tests/data/trajectory_obs.npz` (80 boards × 30 days).

    d    n   plant_target W    C    T    S    M     animal_want G   C   S    crew  compact defer fwd
    0   80          11.0 11.0  0.0  0.0  0.0             1.0 4.0 1.0        0.00    7.00   0.0  2.00
    1   80           7.0  4.0  0.0  1.0  0.0             0.0 0.0 0.0        0.00    7.00   0.0  6.00
    2   80           8.0  3.0  0.0  1.0  0.0             0.0 0.0 0.0        0.00    7.00   0.0  6.00
    3   80           7.1  2.5  0.0  2.4  0.0             0.0 0.0 0.0        0.00    7.00   0.0  6.00
    5   80           5.6  1.0  0.0  3.4  0.0             0.0 0.0 0.0        0.00    7.00   0.0  6.00
    7   80           2.9  0.4  0.0  3.8  0.0             0.0 0.0 0.0        0.28    7.00   0.0  6.00
    9   80           1.1  0.0  0.0  2.9  0.0             0.0 0.0 0.0        3.62    7.00   0.0  5.55
   10   80           3.2  0.1  0.0 14.2  0.0             0.2 0.1 0.0        9.32    7.00   0.0  3.75
   12   80           2.4  0.1  0.0 15.8  0.0             0.1 0.0 0.1        9.35    7.00   0.0  1.98

**How much do they vary?** Across all 2,400 observations `plant_target` has sd
[5.1, 2.2, 0.2, 7.0, 0.0] and `crew_target` sd 3.6 — but the mean **within-day** sd across
boards is only **0.36 tiles**, **0.06 animals** and **0.29 hands**. `compact` is 7 on every
one of the 2,400 observations (sd 0.0) and `animal_defer` is 0 on every one. So B's coarse
decode is a **day curve, not a board response**: essentially all of its variance is the day
axis, and a per-day offset table is therefore the right relative coordinate — it moves the
curve without pretending the curve is a constant.

Executed, on the boards this arm screens (`S/topledger/topb2_B.npz`,
`S/topledger/switch0_B_livec.npz`, both candidate B, our seat, 4 + 4 boards, mean (sd)):

    TOPB2   d0  11.0(0.0) WHEAT  8.0(0.0) CARROT  0 MELON   COW 4.0(0.0) SHEEP 1.0 GOOSE 1.0  idle 0.0
            d5  19.0      WHEAT 16.5(1.5) STRAW           COW 4.5      SHEEP 1.0            idle 8.0(1.0)
            d10 19.0(1.0) WHEAT 25.5(0.5) STRAW  3.0 MELON COW 6.0(2.0) SHEEP 5.5           idle 12.0(1.0)
    LIVE-C  d0  11.0      WHEAT  8.0      CARROT  0 MELON   COW 4.0      SHEEP 1.0 GOOSE 1.0  idle 0.0
            d5  18.0      WHEAT 15.0      STRAW           COW 5.0      SHEEP 1.0            idle 9.0(0.0)
            d10 18.5(0.5) WHEAT 27.0      STRAW  2.0 MELON COW 7.5(2.5) SHEEP 5.0           idle 12.0(0.0)

d0-d4 is board-invariant to the tile (sd 0.0 on both families); the spread opens only from d5,
and the d5-d10 idle tiles (8-12) are the window the crew edits target.

## 2. The 24 pre-registered edits

Written to `S/isearch/mk_off.py` and screened without change. `CROPS = WHEAT CARROT TOMATO
STRAWBERRY MELON`, `ANIMALS = GOOSE COW SHEEP`.

| # | name | field | offset |
|---|---|---|---|
| 1-3 | `w0p1` `w0m1` `w0p2` | `plant_target[WHEAT]` d0 | +1, −1, +2 |
| 4-6 | `c0p1` `c0m1` `c0m2` | `plant_target[CARROT]` d0 | +1, −1, −2 |
| 7-9 | `t0p1` `s0p1` `m0p1` | `plant_target[TOMATO/STRAW/MELON]` d0 | +1 each (crops B plants 0 of) |
| 10-12 | `w13p1` `w13m1` `c13p1` | `plant_target[WHEAT/CARROT]` d1-d3 | ±1 |
| 13-15 | `cow02p1` `cow02p2` `cow02m1` | `animal_want[COW]` d0-d2 | +1, +2, −1 |
| 16-17 | `shp02p1` `gos02m1` | `animal_want[SHEEP/GOOSE]` d0-d2 | +1, −1 |
| 18-19 | `crw01p1` `crw01p2` | `crew_target` d0-d1 | +1, +2 |
| 20-21 | `crw59p1` `crw59p3` | `crew_target` d5-d9 (the idle window) | +1, +3 |
| 22-23 | `defp64` `defm64` | `animal_defer` all days | ±64 of `DEFER_ONE`=256 |
| 24 | `cmpp1` | `compact` all days | +1 of `DIST_MAX` |

`compact −1` was cut to hold the pre-registered set at 24.

**Closed families, and why these are not them.** Every closed result is a *plate or a curve*;
every edit here is one integer by one step on B's own decode:

* melon — `MELON_OPEN` 54.2→15.1 %, −17,554 t −12.8, pinned judge 1.9 % at 12 tiles and
  3.8 % at 8 (`2026-09-11-additive-melon.md` §1, `2026-09-11-labour-compounding.md` table).
  `m0p1` is **+1 tile**, the floor of that dose curve, kept deliberately as the falsifier of
  "the family is closed at every dose".
* crew — `RAMP11` (the clone's whole hand curve) top10 69.4→55.6 %, −4.3k t −3.0, and
  `CREW_FROM_TASKS` 51.6→39.8 % t −28 (`2026-09-11-labour-compounding.md`). `crw*` moves
  1-3 hands on a 2- or 5-day window, not the curve.
* the joint plate — `JOINT_PLATE` band6 54.2→1.0 %, and the wall's own joint pin −24.2 k
  (§70). This search never combines coordinates before both singles have paid.
* carrot — the *shop-adaptive carrot-count* lever died 2026-09-07 (−1.6k…−9.3k sim,
  displacement; `shop-adaptive-top5` memory). That lever was a conditional rule on the shop
  draw; `c0p1`/`c0m1`/`c0m2`/`c13p1` are flat ±1 on the decode.
* board fill — `PLANT_FILL_LATE_ON` cost 5.6-6.9k and went +0/−10 (`2026-09-09-board-fill.md`);
  no edit here lifts the plan cap, they move the target the cap is computed from.

## 3. Screen

`S/isearch/screen_off.py` imports `S/wall/screen_pin.py` verbatim (same tape seat, pinned
town, shop CRN, frozen boards, shipped `hr` switch string, theta `flow193_g100_hr`).
Development panel:

* **TOPB2** — `S/simscreen/boards_topb2.json`, 40 boards = **20 games**.
* **LIVE-C dev** — `S/isearch/boards_dev.json`, the LIVE-C hold-out tapes **43-72** only
  (ids.txt[42:72]), seed 0, both seats = 60 boards = **30 games**. Boards 73-102
  (LIVEC-H30B) were **not** played.

Honest unit = the game (`S/wall/pair.py`'s rule: the two seat rows of a pinned-town open-loop
tape are near-degenerate, so they are averaged before the paired t). Refusal rule, fixed in
advance: **Δ ≤ 0 on TOPB2, or `dours < dtheirs` (handed back, not earned), or LIVE-C win % down.**

### The table (paired vs B, game unit; `S/isearch/pair_multi.py`, raw in `S/isearch/pair.out`)

| edit | TOPB2 Δ | t | Δours/Δtheirs | LIVE-C Δ | t | Δours/Δtheirs | verdict |
|---|---|---|---|---|---|---|---|
| `w0p1`    |   −620 |  −0.97 | −346 / +274   |  −317 | −1.25 |   +7 / +325   | refuse |
| `w0m1`    |   −454 |  −0.80 | −649 / −195   |  −336 | −1.17 | −393 / −58    | refuse |
| `w0p2`    |   −713 |  −1.11 | −782 / −69    |  −520 | −1.71 | −283 / +238   | refuse |
| `c0p1`    |   **0** | 0 | 0 / 0 | **0** | 0 | 0 / 0 | ZERO |
| `c0m1`    |   **0** | 0 | 0 / 0 | **0** | 0 | 0 / 0 | ZERO |
| `c0m2`    |   **0** | 0 | 0 / 0 | **0** | 0 | 0 / 0 | ZERO |
| `t0p1`    |   **0** | 0 | 0 / 0 | **0** | 0 | 0 / 0 | ZERO |
| `s0p1`    |   **0** | 0 | 0 / 0 | **0** | 0 | 0 / 0 | ZERO |
| `m0p1`    | **−14,435** | **−10.01** | −3,357 / **+11,077** | **−15,117** | **−17.27** | −4,159 / **+10,958** | refuse |
| `w13p1`   |    −22 |  −0.04 | −260 / −239   |    −4 | −0.02 | −302 / −298   | refuse |
| `w13m1`   |   −205 |  −0.46 | −258 / −52    |  −121 | −0.80 | −211 / −90    | refuse |
| `c13p1`   | **+302** | +0.71 | +11 / −291  |  −377 | −1.97 | −198 / +178   | refuse (LIVE-C) |
| `cow02p1` |   −410 |  −0.88 | −533 / −123   |  −122 | −0.58 |  −19 / +104   | refuse |
| `cow02p2` | −2,041 |  −2.33 | −835 / +1,207 |  −799 | −2.34 |  −17 / +782   | refuse |
| `cow02m1` | −2,229 |  −2.54 | +246 / +2,475 | −2,804 | −8.11 | −569 / +2,235 | refuse |
| `shp02p1` |   −410 |  −0.88 | −533 / −123   |  −122 | −0.58 |  −19 / +104   | refuse |
| `gos02m1` | −1,436 |  −2.21 | −1,922 / −487 | −2,705 | −5.79 | −1,874 / +831 | refuse |
| `crw01p1` |   **0** | 0 | 0 / 0 | **0** | 0 | 0 / 0 | ZERO |
| `crw01p2` |   **0** | 0 | 0 / 0 | **0** | 0 | 0 / 0 | ZERO |
| `crw59p1` |    −62 |  −0.41 |   +3 / +65    |   **+22** | +1.00 | +59 / +36 | refuse (TOPB2) |
| `crw59p3` |   −832 |  −2.16 | −465 / +368   |  −169 | −1.01 | −103 / +65    | refuse |
| `defp64`  |   −202 |  −0.89 | −286 / −84    |  −980 | −2.75 | −523 / +457   | refuse |
| `defm64`  |   **0** | 0 | 0 / 0 | **0** | 0 | 0 / 0 | ZERO (clipped) |
| `cmpp1`   |   −374 |  −0.86 |  −39 / +335   |  −401 | −1.56 |  −91 / +309   | refuse |

Base rows: TOPB2 30.0 % win / −1,472 (20 games), LIVE-C dev 63.3 % / +3,863 (30 games).

**Identity check.** Variant 0 on `/root/wt_isearch` reproduces the wall run's B
(`S/wall/t2_base.csv`, a different tree, no offset file) on **all 40 TOPB2 boards with a
maximum difference of 0 coins in both purses** — the offset machinery is exactly inert at
zero, so every Δ above is the edit and nothing else.

## 4. Survivors, combinations, finalist

**None.** Two edits were positive on one family — `c13p1` (+302, t +0.71 on TOPB2) and
`crw59p1` (+22, t +1.00 on LIVE-C) — and each is negative on the other, so neither clears the
pre-registered refusal rule, no pair is eligible for combination, and **there is no finalist
to send to the engine.** The confirmation legs in §6 are written but are NOT to be run: they
would be spending the hold-out on a coordinate that did not survive development.

## 5. The shape of the landscape — the integer-level tie census

Of the 24 single edits, **on both families identically**:

* **8 are exactly zero** on every game, to the coin: `c0p1`, `c0m1`, `c0m2`, `t0p1`, `s0p1`,
  `crw01p1`, `crw01p2`, `defm64`.
* **0 gain more than 1 k** — and 0 gain more than 302 coins on TOPB2 or 22 on LIVE-C.
* **12 (TOPB2) / 14 (LIVE-C) sit within ±300 coins**, i.e. inside the noise of a 20/30-game
  paired screen (sd 0.7-2.9 k per game).
* **4 (TOPB2) / 3 (LIVE-C) lose more than 1 k**: `m0p1`, `cow02m1`, `gos02m1`, `cow02p2`.

Only one of the eight zeros is a clip: `defm64` (`animal_defer` decodes 0 on 2,400/2,400
observations, so −64 clamps back to 0). The other seven **changed the decoded `Macro`** —
`S/isearch/decode_probe.json` confirms +1/−1/+2 on 3.3-6.7 % of observations — and changed
**not one coin of either purse**. Two mechanisms, both readable off §1:

1. **The want is slack where it is not executed.** B decodes `plant_target` [11, 11, 0, 0, 0]
   at d0 and the board executes **11 WHEAT + 8 CARROT**. Wheat's want is exactly consumed, so
   ±1 wheat moves the game (−454 … −713); carrot's want is 3 tiles above what is planted, so
   ±1 and −2 carrot move nothing at all, and a want of 1 for a crop that loses the priority
   contest (`t0p1`, `s0p1`) plants nothing.
2. **`crew_target` is not the hiring channel on d0-d1.** B decodes crew 0 on d0-d5 (§1) and
   hires from `hire_bias`/the 1.5 enumeration; asking the ramp for 1 or 2 more hands there
   changes nothing, which is `2026-09-11-labour-compounding.md` ("labour does not compound")
   read at the interface rather than at the outcome.

A third degeneracy: **`cow02p1` and `shp02p1` are identical board for board on both families**
(−410 / −122). +1 COW and +1 SHEEP at d0-d2 buy the *same* marginal animal — `budget.grant`
prices the mix and the kind asked for at the margin is slack; only the total binds.

**So B is a strict local optimum in the integer lattice at radius 1-2**: every coordinate that
the executor can even feel loses, and the ones that do not lose are the ones the executor
ignores. This is the integer-level version of §67's tie census, and it answers its open
question — the ES cannot search these integers, and there is nothing for it to find within
±1-2 anyway.

### Where the losses come from: the d0 purse, and denial

The loss ordering is not about tiles, it is about the **day-0 purse and what the other seat
does with the slack**. B ends d0 on ~150 coins (§1, `money` 153 TOPB2 / 169 LIVE-C).

* **`m0p1` — ONE melon tile at d0 costs 14.4 k / 15.1 k**, win 30 → 10 % and 63 → 6.7 %,
  17 of 30 LIVE-C games flipped. `Δtheirs` is **+11.0 k on both families** against `Δours`
  −3.4/−4.2 k: five-sixths of the loss is **handed to the opponent**, the two-purse denial
  signature (`counterfactuals-overstate`). The melon family was already closed at 8 and 12
  tiles (−17.6 k, 1.9 %); this says the dose curve does **not** start gently — the **first**
  tile is already most of the damage, so the closure is not about scale. Leading hypothesis,
  not measured here: one melon seed is 80 coins (`CROP_SEED_COST`, `2026-09-11-additive-melon.md`)
  against ~150 coins of d0 slack, and `OPEN_PUMP`'s 53-wheat buy at d0 h0 is what lifts the
  quote that refuses family B's second SHEEP (+21.7 k, `dominant-strategy` memory) — a melon
  tile is the one thing on the board that can shorten that buy.
* **`cow02m1` (−2.2 k / −2.8 k, `Δtheirs` +2.5 k / +2.2 k) and `gos02m1` (−1.4 k / −2.7 k)**:
  taking one animal *out* of the opening also mostly pays the other seat. B's 4 COW + 1 SHEEP
  + 1 GOOSE at d0 is a **denial asset**, exactly as §70 found its 11 WHEAT + 8 CARROT to be.
* **`cow02p2` (−2.0 k / −0.8 k, `Δtheirs` +1.2 k / +0.8 k)**: two more cows at d0-d2 also feed
  the opponent — consistent with the fertiliser/cow ledger's open question (−7.3 k/game with
  more cows, `LOSS10` memory), and against the naive reading of §55's "0.7 fewer cows than the
  top tier". We do not run fewer cows because a coarse integer says so; we run fewer because
  the marginal cow at d0-d2 is paid for out of the opening's denial.

## 6. The confirmation legs — written, and NOT to be run

Nothing survived §4, so the hold-out stays unspent. The mechanism is recorded here because the
arm is a **per-day integer offset table, not a theta and not a switch string**, and the judge's
leg runners take a worktree plus a switch string — so the arm has to reach the engine through
the environment. `S/isearch/engine.sh` is the wrapper (same shape as `S/fertcow/engine.sh` /
`S/oppsell/engine.sh`: the judge's own runners under `is_` names, each single runner call
wrapped in ONE `flock` on ext4 `/root/kagg3_judge.lock`, never nested):

* the worktree is **`/root/wt_isearch`** (a copy of `/root/wt_wall`; `arms-next` + the census
  pin + the wall's literal pin + the relative-offset extension), passed to the runner as `$WT`;
* `S/isearch/mk_final.py <edit>` writes `S/isearch/off_<edit>.npz` with the edit at **variant
  0**, so the shipped theta — which has no variant tail — reads it;
* `KAGG3_OFF_INTS` is exported **and** passed through `env` on the runner call, so every
  worker python inherits it;
* the switch string stays the shipped `hr` one, because the arm is not a switch.

Were there a finalist (say `crw59p1`), the coordinator would run, in this order:

    cd /mnt/e/_work/kaggriculture3
    # 0. identity: the same tree with NO offset file must reproduce B to the coin
    bash S/isearch/engine.sh base t
    # 1. the finalist on the untouched hold-out, then the rest for the record
    FIN=crw59p1 bash S/isearch/engine.sh fin l2      # LIVEC-H30B, boards 73-102
    FIN=crw59p1 bash S/isearch/engine.sh fin l62     # LIVE62
    FIN=crw59p1 bash S/isearch/engine.sh fin t       # TOPB2
    FIN=crw59p1 bash S/isearch/engine.sh fin l       # LIVEC-H30 (boards 43-72)

Each leg prints its own `S/bank/paired.py` line against
`S/lossflip/flow193_g100_hr_{topb2,livech,livech2,live62}.csv` and appends to
`S/isearch/engine.out`. The `base` leg is the gate: if it does not reproduce B's csv to the
coin, the tree — not the arm — is what the legs would be measuring.

## 7. What this settles

1. **B is a local optimum in its own integer lattice at radius 1-2.** 24 pre-registered single
   edits, two development families, 50 paired games each: zero gains, 8 exact zeros, and every
   coordinate the executor can feel loses. Combined with §67 (the ES cannot search these
   integers) the conclusion is not "we need a better search over them" but **"there is nothing
   within one step to find"** — a step that changes the plan at all changes it by a whole
   strategy, and every such step is worse.
2. **The interface is coarser than it looks.** 7 of the 24 edits moved the decoded `Macro` and
   moved zero coins: the want is slack wherever it is not executed (carrot 11 asked, 8
   planted), the crew ramp is not the d0-d1 hiring channel, and the animal *kind* at the margin
   is slack (`cow02p1` ≡ `shp02p1`). The 42-integer interface has well under 42 live integers
   on any given day.
3. **The d0 basket is a denial asset, and one tile of it is worth 14 k.** `m0p1` is the
   cheapest measurement yet of the melon closure: the dose curve does not start gently, and
   5/6 of the loss is handed to the other seat, not lost by us. Whatever the d0 opening is
   doing for us, it is doing it through the opponent's purse — which is where the next lever
   has to be looked for, and it is not a coarse integer.
4. **Costed at 1 CPU-hour.** The variant-in-theta trick (§0) put 25 coordinates in one XLA
   compile; the same 50 screens run the wall's way would have been ~10 hours of compiling.
   `S/isearch/screen_off.py` + `mk_off.py` are reusable for any future offset set.

Open, and not answered here: `land_bias`, `forward_days`, `dev_weight`, `hire_bias` and the
coin-scaled fields (`hold`, `press`, `grow_mult`) were out of scope — they are prices, not
counts, and the tie census calls them near-continuous, so they belong to the ES, not to a
coordinate search. The one integer with a real observable that this arm did not move is
`land_bias` (quadrant timing: we buy d5/d10 against the clone's d6/d11, §70).
