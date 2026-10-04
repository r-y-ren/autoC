# E3-pin — the one-step antisymmetric test at B in PINNED mode

Agent run 2026-09-11 (local RTX 3070, 150-minute box). Specified by
`docs/strategy/2026-09-10-consensus.md` §67 and `docs/strategy/2026-09-11-tie-census.md` §7.
Centre: candidate B = `artifacts/kagg2_games/thetas/flow193_g100_hr.npy` (6,789 params).
Nothing under `src/`, `.claude/worktrees/arms-next` or `S/localarm/tree` was touched: the
pin patch is applied to a COPY of the arm tree at `/root/tree_pinned`.

## 0. PRE-REGISTRATION (written before any E3-pin number was read)

**PASS** (ties are the binding constraint; a pinned arm is licensed as a polish):
κ ≥ 0.03 on the rig's hold-out block, AND the antisymmetric `+d` win on **both**
families (LIVE-C hold-out and TOPB2) at α 0.1 or α 0.03, AND `+d` beats ≥ 12 of the
16 signed randoms and **all** of the signed permuted-advantage controls.

**NO-GO**: κ ≤ 0.015, or `+d` loses. That falsifies "the integer ties are what is
blocking the ES at B": the next move is the shop re-roll or a changed seat/objective,
not another σ/pop knob.

Secondary, pre-registered read-out: **how many of the 8 random directions move 100 %
of the screen's boards in pinned mode** (E3b measured 5/8 unpinned at α 0.1). If the
pin removed the cell lottery, that share falls.

## 1. Rig

| piece | value |
|---|---|
| tree | `/root/tree_pinned` = `cp -a S/localarm/tree` + `git apply S/ties/brain.patch` |
| pin | `KAGG3_PIN_INTS=S/ties/pin_B.npz` (B's own theta) for the estimator AND the screen |
| pinned fields | `plant_target, animal_want, crew_target, compact, forward_days, land_bias` |
| free subspace | trainer live mask 5,997 **minus 429 frozen genes = 5,568 free** |
| step length | `R = 0.003·√5997 = 0.232321` — unchanged from E3/E3b, so every α means what it meant there |
| directions | ES `d` (σ 0.02, P 512, eps seed 9001), 4 permuted-advantage controls, 8 randoms `default_rng(777)`, all confined to the free subspace |
| screen | `S/onestep_pin/screen_pin.py` (= `S/simscreen/screen.py`, tree from `KAGG3_SCREEN_TREE`), LIVE-C 120 cells / 60 tapes, TOPB2 40 cells / 20 tapes, paired vs B-pinned |

**The freeze mask.** `S/onestep_pin/mask.py` recomputes census.py's gene attribution
(`alive_coarse & ~alive_fine`, jacobian tolerance 1e-6) and takes the union over a
12-obs panel (days 0/4/9/14/20/27 × both seats): **429 genes, the identical set the
day-0 census reports** — no gene that is coarse-only at day 0 becomes fine-alive
anywhere in the panel (fine-alive grows 3,119 → 3,215; the 429 are untouched). All
429 lie inside the trainer's live mask, so the free subspace is 5,568.

**Masking `d` after the draw is exactly masking ε in the draw.** Under the pin the
frozen genes cannot change any decode, so every fitness in the population is
unchanged by zeroing those coordinates of ε; and
`g_j = Σ_i δ_i ε_ij /(pop·σ)` touches coordinate `j` only through `ε[:, j]`. So
`g[frozen] = 0` (what `sweep_pin.py` does) is byte-equivalent to drawing ε with the
frozen columns zeroed, without touching the trainer. The randoms and the permuted
controls are drawn on the same free mask, so no direction spends length on genes the
pinned objective cannot see.

## 2. SELF-CHECK — the pin is idempotent at its own centre (PASSED)

B screened on the patched tree, TOPB2 first 10 boards, with and without
`KAGG3_PIN_INTS`:

* **10/10 boards byte-identical** (mine, theirs, margin, shop_sig) pinned vs unpinned;
* both reproduce the canonical `S/simscreen/topb2_40.csv` B rows **to the coin**, so the
  patched tree also plays the same agent the judge plays.

Files: `S/onestep_pin/selfcheck_{unpinned,pinned}.csv`.

## 3. THE PIN WORKS: the cell lottery is gone (the headline measurement)

Pre-registered secondary read-out, α 0.1, `+`-side steps of length 0.0232:

| | boards whose margin moves at all | randoms moving 100 % of boards | 16 signed random gains | random antisym A |
|---|---|---|---|---|
| **E3b, UNPINNED** LIVE-C | (not all measured) | **5/8** at 100 % | mean +68, **sd 107** | mean +10, **sd 184** |
| **E3b, UNPINNED** TOPB2 | | | mean −668, **sd 977** | mean +684, **sd 1,527** |
| **E3-pin** LIVE-C 120 | **16.4 %** mean | **0/8** | mean −4, **sd 4** | mean +2, **sd 6** |
| **E3-pin** TOPB2 40 | **13.4 %** mean | **0/8** | mean −37, **sd 44** | mean −13, **sd 84** |

At α 0.03 the pinned steps move 7.3 % (LIVE-C) / 3.4 % (TOPB2) of boards. So the pin
does exactly what §59/§67 said it would: holding the 12 coarse decodes removes the
**cell** lottery. A same-length random step is no longer a ±1,000-coin coin flip on
the top tier; the noise in the paired statistic falls **~25× on LIVE-C and ~20× on
TOPB2**. That is the cleanest confirmation yet that the integer cells, not the
estimator, were producing the ±25 k board swings the ES has been averaging over.

It also shows what is left underneath: in the free (coin-scaled) subspace, an ES-sized
step changes the *outcome* of only one board in six, and by a few coins.

## 4. The rig (GPU, σ 0.02 × P 512, eps seed 9001, 2,708 s)

`S/onestep_pin/sweep_pin.txt` / `.json`; log `S/onestep_pin/run.log`.
`n 6789 live 5997 free 5568 frozen(live) 429`, `R 0.2323`, 159 episodes (147 pinned),
79 scored thetas, draw 665 s, `‖g‖ 47.11`.

**Held-out block (LIVE-C 43-72, both seats) — the pre-registered verdict field:**

| α | metric | F(centre) | +d gain | −d gain | antisym | κ vs randoms | a>r | a>p | rand<+d |
|---|---|---|---|---|---|---|---|---|---|
| 1.0 | obj_w | +0.6486 | **−0.0067** | −0.0137 | +0.0070 | 0.0162 | 7/8 | 3/4 | 2/16 |
| 1.0 | margin | +3,971 | **−81** | −446 | +365 | 0.0483 | 8/8 | 4/4 | 2/16 |
| 0.1 | obj_w | +0.6486 | **−0.00135** | −0.00461 | +0.00326 | **0.0268** | 8/8 | 4/4 | 4/16 |
| 0.1 | margin | +3,971 | **−22** | −72 | +50 | 0.0220 | 8/8 | 4/4 | 4/16 |
| 0.03 | obj_w | +0.6486 | **−0.00040** | −0.00084 | +0.00045 | 0.0074 | 5/8 | 3/4 | 4/16 |
| 0.03 | margin | +3,971 | **−0** | −12 | +12 | 0.0118 | 7/8 | 4/4 | 8/16 |

`+d` **loses at every α on both metrics** on the hold-out. The positive antisym is
carried entirely by `−d` being worse still, which is curvature, not a gradient. In
sample the same cell reads `+d` +0.00015 at α 0.1 (κ 0.042) — the §6 "mixed" case:
the estimator resolves its own batch a little and the hold-out not at all.

**A note on the `[WARN] saved advantages do NOT rebuild the draw's gradient` line.**
It is an artefact of where the freeze is applied, not a defect: the integrity check
compares the *masked* `g` with the *unmasked* rebuild, and the measured discrepancy is
exactly the frozen share — cos 0.9651 vs √(5568/5997) = 0.9636, ratio 1.0362 vs
√(5997/5568) = 1.0378. Independently, `frozen_gnorm/raw_gnorm = 0.2619` against the
isotropic √(429/5997) = 0.2675: **the draw puts precisely a random vector's share of
its length on the frozen genes**, which is what "the pin makes them fitness-blind"
predicts. The permuted controls are built from the same masked vectors and are
comparable; the cell is not void.

## 5. The engine-exact read-out (pinned CPU screen, paired vs B-pinned)

`S/onestep_pin/analysis.txt`, csvs in `S/onestep_pin/csv/`. 4,290 paired board rows,
`shopdiff 0.0 %` throughout. `zA` = (A_cell − mean A_rand)/sd A_rand;
`r<A` = randoms whose A is smaller; `p<A` = permuted controls whose A is smaller;
`r<g+` = signed random steps whose gain is smaller than `gain(+d)`.

| family | α | gain(+d) | t(+) | gain(−d) | A | zA | r<A | p<A | r<g+ | p<g+ |
|---|---|---|---|---|---|---|---|---|---|---|
| LIVE-C (60 tapes) | 0.1 | **−2** | −0.15 | **+72** | −74 | −11.97 | **0/8** | **0/4** | 12/16 | 3/8 |
| LIVE-C | 0.03 | **−4** | −0.40 | −2 | −2 | −0.20 | 5/8 | 1/4 | 1/16 | 0/8 |
| TOPB2 (20 tapes) | 0.1 | **−196** | −1.43 | −17 | −179 | −1.98 | **0/8** | **0/4** | 0/16 | 0/8 |
| TOPB2 | 0.03 | **−79** | −0.91 | −7 | −72 | −1.49 | 1/8 | 1/4 | 3/16 | 1/8 |

The ES direction **loses on both families at both α**, and its antisymmetric statistic
is **negative** on both — i.e. on the judge field the *mirror* step `−d` is the better
one, the opposite sign to the rig's own hold-out block. Screen-side
κ = zA/√5568 is **−0.160** (LIVE-C α 0.1) and **−0.027** (TOPB2 α 0.1). The
`12/16 r<g+` on LIVE-C α 0.1 is not a win: the random null there is −4 ± 4 coins, so
"beats 12 of 16" and "gained −2 coins" are the same statement.

## 5b. REPLICATION at a second eps seed (9002), and the seed-to-seed cosine

The whole rig was re-run at `EPS_SEED=9002` (same σ 0.02, P 512, same freeze, same
tree; `S/onestep_pin/run_s9002.log`, `sweep_pin_s9002.txt`) and its direction screened
on both families.

* **The two draws are orthogonal.** `cos(d_9001, d_9002) = +0.0142`, against
  `1/√5568 = 0.0134` for two *random* vectors in the free subspace. Two independent
  population draws at the same centre share, to measurement precision, **nothing**.
  Whatever each draw points at, it is not a reproducible feature of the objective.
* **Held-out κ falls further**: α 0.1 obj_w κ **0.0123** (α 1.0 margin 0.047), `+d`
  gain −0.00020 (obj_w) and −7 (margin) — losing again. At α 0.03 the seed-9002 cell
  reads a marginal in-field gain (+0.00117 obj_w, +27 margin, rand<+d 13/16) but its
  antisym is +0.00045 with κ 0.0094, and the engine-exact screen kills it (below).
* **Screen, α 0.1**: LIVE-C gain(+d) **−15** (A −96, 0/8 randoms, 0/4 perms);
  TOPB2 gain(+d) **−199** (A −208, 0/8, 0/4). At α 0.03: LIVE-C +4 (A +0, 5/8),
  TOPB2 −63 (A −56, 1/8).

Two independent draws, four family×α read-outs each, and `+d` is negative in seven of
the eight. This is not a one-seed artefact.

## 5c. How flat the pinned objective is

Among the boards a step moves at all (α 0.1, paired |Δmargin|):

| family | direction | boards moved | mean \|Δ\| among moved | median | max |
|---|---|---|---|---|---|
| LIVE-C | 8 randoms ± | 16.1 % | 91 | 42 | 798 |
| LIVE-C | ES ± | 17.9 % | 458 | 71 | 5,951 |
| TOPB2 | 8 randoms ± | 16.1 % | 493 | 289 | 2,203 |
| TOPB2 | ES ± | 25.0 % | 675 | 439 | 2,203 |

Five boards in six do not move at all, and the median mover shifts 42 coins on LIVE-C.
The ES direction moves *more* boards and by more coins than a random one of the same
length — it is not inert, it is simply pointed the wrong way.

## 6. VERDICT — **NO-GO** (pre-registered)

| clause | required | measured | |
|---|---|---|---|
| κ on the rig's hold-out | ≥ 0.03 | **0.0268** (obj_w α 0.1), 0.022 (margin α 0.1), 0.0074 at α 0.03; **0.0123** at eps seed 9002 | FAIL |
| antisym `+d` win on both families at α 0.1 or 0.03 | yes | `+d` **loses on both, at both α**, on **both eps seeds**; A negative on both | FAIL |
| `+d` beats ≥ 12/16 randoms | yes | 0/16 (TOPB2 α 0.1); the LIVE-C 12/16 is a −2-coin "win" | FAIL |
| `+d` beats all signed permuted controls | yes | 0/8 (LIVE-C α 0.1), 0/8 (TOPB2 α 0.1) | FAIL |

The NO-GO branch is reached by its own terms (`+d` loses), and κ never clears 0.03.
**The integer ties are not the binding constraint at B.** Freezing the coarse cells did
exactly what it was designed to do — it removed the lottery, by a factor of ~20-25 in
the paired sd — and with the lottery gone there is still **no decodable gradient at B
in the coin-scaled subspace**: the estimator's direction is if anything anti-aligned
with the judge field, and the permuted-advantage control matches or beats it
everywhere.

Two things follow, and they are the point of the measurement:

1. **B is a peak for this estimator in the fine subspace, and the remaining variance is
   not the cells.** With 429 coarse genes held, an ES-length step changes one board in
   six and a few coins; the ±25 k that the arms average over must therefore come from
   the part the pin cannot touch — the end-of-day **shop re-roll** (one RNG draw per
   empty tile, `shop-lottery` memory) — or from the seat/objective itself.
2. **Do not re-cut an arm in pinned mode.** A pinned arm would be climbing a field in
   which `+d` already loses the hold-out; and §67's own guard (a pinned theta must
   replay unpinned and reproduce B's counts) never even gets tested, because there is
   nothing to promote. Step 5 of the brief was therefore not run.

The constructive next move is the one §7 of the tie census names for a NO-GO: a changed
**objective/seat**, or the shop re-roll — not another σ, pop, lr or freeze set.

## 7. Files

| path | what |
|---|---|
| `/root/tree_pinned` | the patched tree copy (scratch, outside the repo) |
| `S/onestep_pin/sweep_pin.py` | `sweep_c.py` + `--freeze-mask` (masks d, the perms and the randoms) |
| `S/onestep_pin/run_pin.sh` | the one-command GPU runner (sets `KAGG3_PIN_INTS`) |
| `S/onestep_pin/mask.py`, `coarse_mask.npy`, `coarse_mask.json` | the 429-gene freeze set + the 12-obs panel that confirms it |
| `S/onestep_pin/screen_pin.py` | `S/simscreen/screen.py` with the tree from `KAGG3_SCREEN_TREE` |
| `S/onestep_pin/build_rand.py`, `thetas_screen/` | the free-subspace random controls and the α-rescaled step thetas |
| `S/onestep_pin/csv/*.csv`, `analyse.py`, `analysis.txt` | the paired screen rows and the read-out |
| `S/onestep_pin/selfcheck_{unpinned,pinned}.csv` | the idempotence gate |
| `S/onestep_pin/{run_s9002.log,sweep_pin_s9002.{json,txt},thetas_s9002/,grads_s9002/}` | the eps-seed 9002 replication |

Standing: `git diff --stat src/` empty, no judge lock taken, no engine leg, no ssh, GPU left free.
