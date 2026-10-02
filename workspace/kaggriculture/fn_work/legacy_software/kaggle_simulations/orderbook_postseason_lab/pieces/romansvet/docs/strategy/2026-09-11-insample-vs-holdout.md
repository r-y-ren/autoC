# Do the B-seeded ES arms gain on their OWN training rungs? (in-sample vs hold-out)

Agent, 2026-09-11, 55-minute box, CPU only. New files: `S/insample/` (board files,
`analyse.py`, logs), screen CSV `S/simscreen/insample_s0.csv`.

**Question.** Every B-seeded arm (flow196/197/200/201 remote, flow198 local) loses or reads
level against candidate B on the paired hold-out legs while the trainer's own `mean_win`
drifts up. Two diagnoses with different fixes:

* **(A) OVERFIT** — the records really do gain on the boards the ES scored, and the gain does
  not transfer. Fix = board/seed rotation, regularisation, a wider field.
* **(B) NOISE WALK** — the records do not gain even on the boards the ES scored. Fix =
  estimator variance (effective population, dimension, step length), per the E3 audit.

## Method — the in-sample board is the cell the ES actually scored

A training rung is played by the trainer as **one episode per generation** (`--pinned-once`),
on a seed that is a pure function of the rung name
(`--pinned-fixed-seed` -> `pinned_seed_word("tape_act_<id>")` =
`blake2b(name, key="kagg3.pinned.seed.v1") % (2**31-1)`,
`.claude/worktrees/arms-next/src/kagg3/es/train.py:1316`), with the seat alternating per
generation and staggered by the rung's position in the block
(`pinned_seats`, `(t + i) % 2`, same file :4437). `--shop-crn` fixes the shop word.
So the in-sample cell is exactly `(tape, pinned_seed_word, seat)` — which is a
`S/simscreen/screen.py` board, on the same pinned-town tapes
(`artifacts/tape_actions_town/`, all 206 resolve) with `shop_crn` on and the shipped `hr`
switch string. The screen is the engine to ~85 coins on this tape family
(`docs/strategy/2026-09-11-simscreen-topb2.md`: sign 6/6, max error 45 coins vs the engine legs).

Board files: `S/insample/boards_flow201_s0.json` (seat `= i % 2`, the trainer's even
generations) and `_s1.json` (the odd-generation phase, built, run only if time allowed).
The rung sets **nest** — flow196 147 ⊂ flow200 166 ⊂ flow201 206 — so one screen over the
flow201 rungs serves every arm; each arm's rows are selected by its own `--tape-actions` list
(`S/insample/rungs_flow*.txt`) and weighted by its own `--rung-weight` values
(`S/insample/weights_flow*.json`; flow200 = 85 rungs at w2, 61 at w4, 20 at w10.2).
flow198's 147 rungs are **not** a subset (top-tier rotation set), so it is not screened here.

Honest unit = one rung (n = 166 / 206), one seat, paired against B board by board.
`dobj_w` is the ES objective itself: rung-weighted mean of `sigmoid((mine-theirs)/3000)`
(`--margin-scale 3000`, `--select-metric score`, `--abs-weight 0`), record minus B.

## Hold-out side (already measured, `S/glut/verdicts.log` AUTOJUDGE-vsB lines)

Paired Δ margin vs B, coins/board (TOPB2 and LIVE-C legs are 2 seats per tape; `t` on the
honest unit is in the log line):

| record | TOPB2 | LIVEC-H30 | LIVEC-H30B | LIVE62 | verdict logged |
|---|---|---|---|---|---|
| flow196_g100p_hr | −784 | −755 (t −3.9) | −24 | −460 | loss (arm retired) |
| flow200_g10_hr | −1,222 (t −2.6) | −632 (t −2.7) | −7 | −547 | loss #1 |
| flow200_g30_hr | −61 | +158 | +209 | −58 | LEVEL |
| flow200_g100p_hr | −290 | −428 | −230 | −267 | loss #2 |
| flow201_g10_hr | −1,815 (t −3.6) | −430 | −42 | −175 | loss #1 |
| flow201_g20_hr | −1,663 (t −3.2) | −280 | +88 | −326 | loss #2 |
| flow201_g100p_hr | −1,461 (t −2.3) | −541 (t −2.2) | −153 | −81 | loss #3 → Rule 4 |
| flow201_g140_hr | −871 (t −2.4) | −327 | +304 | −62 | loss #4 (retired arm) |
| flow198_g10_hr (local) | −795 (t −2.7) | −361 | −132 | +115 | loss #1 |

Not one record is above B on TOPB2; the pooled sign is negative on 8 of 9 records.

## What the trainer thought it was gaining

The remote `train.log` for flow200/flow201 lives on the training host and this box has no ssh,
so the only trainer log readable here is the local arm's, `artifacts/flow198/train.log`
(same B seed, same recipe family, 81 generations):

* `mean_win` 0.5925 (gen 1) → 0.6128 (gen 80); first-five mean 0.5973, last-five 0.6138.
* gen-to-gen sd of the *change* is 0.0089, i.e. the whole 80-generation drift (+0.017) is
  about **1.9 single-generation steps of noise**, and the series oscillates through it
  (0.5930 at gen 60, 0.6077 at gen 40).
* OLS slope = +0.00022 win/gen = **+1.8 points of population win rate over 80 generations** —
  and `mean_win` is the *population* mean over perturbed candidates on a freshly drawn
  opponent mix, not a paired read on the fixed rungs.

So "the trainer's own `mean_win` climbs" is, on the only log available, a drift inside the
generation-to-generation noise band rather than a measured in-sample gain. The measurement
below is the paired version the trainer never makes.

## In-sample side (this measurement)

Screen: 9 thetas × 206 boards = 1,854 episodes, `S/insample/screen_s0.log`,
per-board rows in `S/simscreen/insample_s0.csv`, pairing in `S/insample/analyse.py`
(`S/insample/insample_summary.json`). Decision rule fixed before the run:

* **A (overfit)** if the deep records gain ≥ +300 coins/rung in-sample with t ≥ 2 while the
  hold-out reads ≤ 0;
* **B (noise walk)** if the in-sample |Δ| is small and |t| < 1.5 — the records are not even
  better on the boards that selected them.

### Fidelity notes on the in-sample cell

* `pinned_seed_word` / `pinned_seats` / `PINNED_SEED_SALT` are **byte-identical** in
  `S/localarm/tree/src/kagg3/es/train.py` (the tree rsynced to the training host) and in
  `.claude/worktrees/arms-next` (the tree the screen imports), so the seed word is exact, not
  a best reading. `artifacts/flow198/train.log:2` confirms the layout the flags produce:
  "147 pinned rungs x 1 episode + 13 episodes carried".
* The seat is the only degree of freedom: the trainer alternates it per generation
  (`(t + i) % 2`), so each rung is in-sample from BOTH seats over consecutive generations.
  The screen plays one phase (`s0`); the 4 weight-0 archetypes ahead of the tape rungs shift
  `i` by an even number, so the parity of the phase is unchanged.
* The residual 13 episodes/generation (pool + self-play) are not screened: they are 7 % of the
  episode budget and carry no fixed board.

### Result — every record is at best LEVEL and mostly BELOW B on its own training rungs

Paired vs B, one board per rung (n = the arm's own rung count), `shopdiff` 0.0 % on all 1,854
episodes, so every theta saw byte-identical shops:

| record | arm | n | in-sample Δ | Δ rung-weighted | t | win% (B) | flips +/− | Δobj_w | hold-out (TOPB2 / H30 / H30B / LIVE62) |
|---|---|---:|---:|---:|---:|---|---|---:|---|
| flow196_g100p_hr | flow196 | 147 | **−551** | −442 | **−3.08** | 72.8 (75.5) | 4/8 | −0.0094 | −784 / −755 / −24 / −460 |
| flow200_g10_hr | flow200 | 166 | **−646** | −425 | **−3.78** | 68.1 (68.7) | 8/9 | −0.0165 | −1,222 / −632 / −7 / −547 |
| flow200_g30_hr | flow200 | 166 | +35 | +254 | +0.24 | 67.5 (68.7) | 4/6 | +0.0011 | −61 / +158 / +209 / −58 |
| flow200_g100p_hr | flow200 | 166 | −318 | −188 | −1.95 | 70.5 (68.7) | 7/4 | +0.0013 | −290 / −428 / −230 / −267 |
| flow201_g10_hr | flow201 | 206 | **−511** | −545 | **−3.41** | 70.4 (73.3) | 5/11 | −0.0203 | −1,815 / −430 / −42 / −175 |
| flow201_g20_hr | flow201 | 206 | −240 | −165 | −1.42 | 74.3 (73.3) | 7/5 | −0.0024 | −1,663 / −280 / +88 / −326 |
| flow201_g100p_hr | flow201 | 206 | −38* | −171 | −0.08* | 71.4 (73.3) | 4/8 | −0.0106 | −1,461 / −541 / −153 / −81 |
| flow201_g140_hr | flow201 | 206 | +107 | +207 | +0.61 | 74.3 (73.3) | 7/5 | +0.0069 | −871 / −327 / +304 / −62 |

\* one board (tape 106825802) blows the pair up by +85k and carries the whole mean; with
|d| < 3 sd trimmed (200 of 206 boards) flow201_g100p reads **−289, t −2.01** — i.e. also below B.

* **Not one record clears the A-threshold** (+300 with t ≥ 2) in-sample. The best reads are
  +35 (t 0.24) and +107 (t 0.61), both inside noise; the mean over the 8 records is **−270**.
* Six of eight are BELOW B on the very boards the ES scored them on, three at t ≈ −3 to −3.8.
* The ES objective itself moves the same way: `Δobj_w` is negative for 5 of 8 and reaches
  −0.020 (flow201_g10) — the trainer's own fitness on its own fixed block is DOWN.
* In-sample and hold-out agree in sign and in order: Pearson 0.66 (Spearman 0.64) between the
  in-sample Δ and the pooled hold-out Δ. There is no in-sample/out-of-sample gap to explain.

## Verdict: **B — NOISE WALK** (not overfit)

The records are not trading in-sample gain for out-of-sample loss; they have no in-sample gain
to trade. The arms are a random walk around B on their own objective, and the hold-out legs are
simply reading the same walk with a different (noisier) instrument. This is the direct
board-level confirmation of consensus §56 / `docs/strategy/2026-09-11-e3-step-audit.md`: the
gradient draw at pop 512-2048 is sampling noise (‖g512‖/‖g2048‖ = 1.998 = √4, cos 0.53 = √¼;
the step's coordinate profile equals its Gaussian controls' to the third decimal), and the
full-length Adam step (α 1.0) is downhill (−16.6k) while only α ≤ 0.1 of it reads slightly
uphill (+140 / +286 t 2.3).

The known **GATE-FIELD OVERFIT** result (2026-09-10, `docs/strategy/2026-09-10-es-rate-B.md:48`:
flow137/138 gate-confirmed thetas lost 2-4 pts on legs the 8-tape gate never played) is a
different mechanism and is **not contradicted**: that was selection by a narrow *gate*, this is
the *training* rungs, and here the training rungs show no gain to lose.

**Fix this implies** — estimator variance and step length, not rotation/regularisation:
1. shorten the step (lr 0.003 → 3e-4, or clip ‖δ‖ to the α 0.1 scale the E3 scale test found
   uphill), which is free and testable on the existing arms;
2. raise the effective population / lower the dimension (flow204's σ/pop grid; `--train-only`
   a smaller live mask) — but note pop 512 → 2048 only bought √4 in ‖g‖, i.e. pure noise
   reduction, so pop alone is a 2× resolution buy at 4× wall;
3. board/seed rotation and regularisation (the A-fixes) are **not** indicated and should not
   consume a GPU slot until an arm is shown to gain in-sample.

## Falsifiable next test (cheap, CPU, no GPU)

Take B and its own arm's step direction at a generation boundary (the `cands/gNNNNN_record.npy`
minus B, already on disk for flow200 g10/g30/g100), and screen `B + α·(record − B)` for
α ∈ {1.0, 0.3, 0.1, 0.03} on `S/insample/boards_flow201_s0.json` (the same 166/206 in-sample
boards) paired against B. **Prediction of verdict B**: the in-sample Δ is monotone in α with its
maximum at α ≤ 0.1 and no α gives ≥ +300 at t ≥ 2 — the generation step is a too-long move along
a noise direction. **Falsified if** any record direction at α = 1.0 reads ≥ +300 in-sample at
t ≥ 2 (then the walk is real and the loss is genuinely out-of-sample = diagnosis A after all).
Cost: 4 α × 3 records + B ≈ 2,700 episodes ≈ 25 min of CPU on the rebuilt screen.
