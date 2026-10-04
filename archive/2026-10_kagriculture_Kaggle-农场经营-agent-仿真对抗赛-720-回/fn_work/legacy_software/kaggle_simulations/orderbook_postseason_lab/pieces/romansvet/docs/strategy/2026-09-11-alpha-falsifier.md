# The pre-registered alpha falsifier: is the B-seeded ES step a too-long move along a real direction?

Agent, 2026-09-11, 45-minute box, CPU only. New files: `S/alpha/` (build script, runner,
`analyse.py`, logs, 18 scaled thetas, `alpha_summary.json`), screen CSVs
`S/simscreen/alpha_a01.csv`, `alpha_a03.csv`, `alpha_a003.csv`.

## The test, in the words it was registered in

`docs/strategy/2026-09-11-insample-vs-holdout.md` (consensus §59) closed with:

> Take B and its own arm's step direction at a generation boundary ... and screen
> `B + α·(record − B)` for α ∈ {1.0, 0.3, 0.1, 0.03} on `S/insample/boards_flow201_s0.json`
> (the same 166/206 in-sample boards) paired against B. **Prediction of verdict B**: the
> in-sample Δ is monotone in α with its maximum at α ≤ 0.1 and no α gives ≥ +300 at t ≥ 2 —
> the generation step is a too-long move along a noise direction. **Falsified if** any record
> direction at α = 1.0 reads ≥ +300 in-sample at t ≥ 2 (then the walk is real and the loss is
> genuinely out-of-sample = diagnosis A after all).

Six records (the task's set, three per arm) × α ∈ {0.3, 0.1, 0.03} were screened here;
α = 1.0 is the `S/insample` screen's own rows, reused, except `flow200_g200p_hr` (a record that
post-dates that run) which was screened fresh alongside. B = `flow193_g100_hr`.

## Method (identical cell to the in-sample run)

* Thetas: `S/alpha/build_thetas.py` writes `S/alpha/thetas/<record>_a{0.3,0.1,0.03}.npy` =
  `B + α(record − B)`, float32, elementwise. Step lengths: `‖record − B‖` = 0.86 (g10 records)
  to 2.83 (flow201_g140) against `‖B‖` = 18.11; 5,997 of 6,789 coordinates move.
* Boards: `S/insample/boards_flow201_s0.json` — 206 (pinned rung tape,
  `pinned_seed_word`, trainer seat phase s0) triples, unchanged, `--boards 206`.
* Screen: `S/simscreen/screen.py`, shipped `hr` switches, `shop_crn` on, `--chunk 206`,
  three parallel CPU runs (`S/alpha/run.sh`, logs `S/alpha/a0{1,3,03}.log`), 4,120 episodes
  in ~11 min wall. `shopdiff` **0.0 %** on every row: all 24 scaled thetas saw byte-identical
  shop sequences to B's.
* Determinism: B was re-screened inside the α 0.1 run and reproduced the `S/insample` margins
  on **206/206** boards exactly, so the reused α = 1.0 rows are the same instrument.
* Honest unit = one rung. `d206` pairs on all 206 boards; `dOwn` on the arm's own rung list
  (flow200 = 166 ⊂ flow201 = 206), `dOwn_w` weighted by the arm's own `--rung-weight`.

## Result — every cell, all six records × four α

| record | α | n(206) | Δ206 | t206 | win % | n own | Δ own | t own | Δ own_w | flips +/− | Δobj_w |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| flow200_g10_hr | 1.0 | 206 | −544 | −3.40 | 71.4 | 166 | −646 | −3.78 | −425 | 8/12 | −0.0165 |
| flow200_g10_hr | 0.3 | 206 | −537 | −3.83 | 69.9 | 166 | −548 | −3.79 | −412 | 6/13 | −0.0121 |
| flow200_g10_hr | 0.1 | 206 | −631 | −4.59 | 69.9 | 166 | −619 | −4.14 | −494 | 6/13 | −0.0182 |
| flow200_g10_hr | 0.03 | 206 | −40 | −0.67 | 73.3 | 166 | −30 | −0.48 | +2 | 1/1 | −0.0029 |
| flow200_g100p_hr | 1.0 | 206 | −281 | −1.92 | 73.8 | 166 | −318 | −1.95 | −188 | 7/6 | +0.0013 |
| flow200_g100p_hr | 0.3 | 206 | −485 | −3.69 | 70.4 | 166 | −503 | −3.41 | −329 | 5/11 | −0.0089 |
| flow200_g100p_hr | 0.1 | 206 | −518 | −3.82 | 68.9 | 166 | −518 | −3.55 | −394 | 5/14 | −0.0168 |
| flow200_g100p_hr | 0.03 | 206 | +9 | +0.14 | 72.3 | 166 | +19 | +0.29 | +45 | 0/2 | +0.0010 |
| flow200_g200p_hr | 1.0 | 206 | −466 | −3.11 | 70.9 | 166 | −494 | −3.16 | −399 | 6/11 | −0.0095 |
| flow200_g200p_hr | 0.3 | 206 | −92 | −0.90 | 72.3 | 166 | −83 | −0.75 | +26 | 4/6 | −0.0023 |
| flow200_g200p_hr | 0.1 | 206 | −97 | −1.30 | 72.8 | 166 | −60 | −0.75 | −29 | 3/4 | −0.0029 |
| flow200_g200p_hr | 0.03 | 206 | −45 | −0.82 | 73.3 | 166 | −0 | −0.01 | +38 | 1/1 | +0.0006 |
| flow201_g10_hr | 1.0 | 206 | −511 | −3.41 | 70.4 | 206 | −511 | −3.41 | −545 | 5/11 | −0.0203 |
| flow201_g10_hr | 0.3 | 206 | −418 | −3.36 | 72.3 | 206 | −418 | −3.36 | −292 | 5/7 | −0.0113 |
| flow201_g10_hr | 0.1 | 206 | −565 | −4.12 | 68.9 | 206 | −565 | −4.12 | −453 | 5/14 | −0.0172 |
| flow201_g10_hr | 0.03 | 206 | −6 | −0.13 | 72.8 | 206 | −6 | −0.13 | +79 | 0/1 | +0.0020 |
| flow201_g100p_hr | 1.0 | 206 | −38 | −0.08 | 71.4 | 206 | −38 | −0.08 | −171 | 4/8 | −0.0106 |
| flow201_g100p_hr | 0.3 | 206 | +35 | +0.30 | 73.3 | 206 | +35 | +0.30 | +9 | 3/3 | +0.0025 |
| flow201_g100p_hr | 0.1 | 206 | −71 | −0.69 | 72.8 | 206 | −71 | −0.69 | −60 | 2/3 | −0.0045 |
| flow201_g100p_hr | 0.03 | 206 | −63 | −0.89 | 72.3 | 206 | −63 | −0.89 | −41 | 0/2 | −0.0035 |
| flow201_g140_hr | 1.0 | 206 | +107 | +0.61 | 74.3 | 206 | +107 | +0.61 | +207 | 7/5 | +0.0069 |
| flow201_g140_hr | 0.3 | 206 | +46 | +0.36 | 73.8 | 206 | +46 | +0.36 | +137 | 6/5 | +0.0019 |
| flow201_g140_hr | 0.1 | 206 | −38 | −0.41 | 73.3 | 206 | −38 | −0.41 | −36 | 2/2 | +0.0034 |
| flow201_g140_hr | 0.03 | 206 | +47 | +0.79 | 73.8 | 206 | +47 | +0.79 | +148 | 2/1 | +0.0045 |

B's own read on these boards: win 73.3 %, mean margin +6,755.
(`flow201_g100p_hr` α 1.0 carries the known +85k outlier board 106825802; trimmed it reads
−289, t −2.01 — see the in-sample doc. The scaled rows do not have it.)

### Where the maximum over α sits (arm-own-rung Δ)

| record | α 1.0 | α 0.3 | α 0.1 | α 0.03 | argmax |
|---|---:|---:|---:|---:|---|
| flow200_g10_hr | −646 | −548 | −619 | −30 | α 0.03 |
| flow200_g100p_hr | −318 | −503 | −518 | +19 | α 0.03 |
| flow200_g200p_hr | −494 | −83 | −60 | −0 | α 0.03 |
| flow201_g10_hr | −511 | −418 | −565 | −6 | α 0.03 |
| flow201_g100p_hr | −38 | +35 | −71 | −63 | α 0.3 |
| flow201_g140_hr | +107 | +46 | −38 | +47 | α 1.0 |

## Verdict: **NOT FALSIFIED**

No record at α = 1.0 reads ≥ +300 at t ≥ 2 in-sample. The largest α = 1.0 read over the six is
**+107 (flow201_g140_hr, t +0.61)**; the largest over all 24 cells is the same +107. Four of the
six are at −466…−646 with t −3.1 to −3.8. Verdict **B (noise walk)** of consensus §59 stands, and
diagnosis A (overfit) is not resurrected: the records still have no in-sample gain to trade away.

### But the prediction's *shape* is wrong, and that matters for the fix

The registered prediction had two clauses. The operative one — no α reaches +300 at t ≥ 2 —
holds **24/24**. The other — "Δ is monotone in α with its maximum at α ≤ 0.1" — is **false**:

* Not one record is monotone. The profile is a **cliff, not a slope**: at α 0.03 every record
  reads Δ ≈ 0 (−30…+47, |t| ≤ 0.9, 0-2 board flips) because a 0.03-scaled step is
  behaviourally B (‖Δθ‖ 0.026-0.085 on ‖B‖ 18.1, below the decode granularity of most genes);
  by α 0.1 the loss is **already full size** (−518, −565, −619 at t −3.5 to −4.6) and shrinking
  the step further from 1.0 to 0.1 does **not** recover it — for 3 of 6 records α 0.1 is the
  *worst* cell of the four.
* So the loss is not proportional to step length. There is no linear regime in which these
  directions gain: the first behaviourally distinguishable amount of them is already downhill.

This is a direct constraint on fix #1 of the in-sample doc ("shorten the step — lr 0.003 → 3e-4,
or clip ‖δ‖ to the α 0.1 scale the E3 scale test found uphill"). The E3 α-scale result was
measured on a *single Adam step built from a fresh 512-2048 gradient draw*; here, on six real
*generation-boundary* records, α 0.1 of the record is as bad as the record. **Shortening the
step does not rescue a record direction.** A shorter lr can only help by changing which
directions get drawn at all, not by taking less of these — if it is tested, it must be judged on
fresh arms, not by rescaling existing records.

## Extra: does the scaled in-sample read pre-rank the hold-out?

Pooled AUTOJUDGE-vsB hold-out Δ (board-count weighted over TOPB2 40 / LIVEC-H30 60 /
LIVEC-H30B 60 / LIVE62 124, from `S/glut/verdicts.log`): flow200_g10 −546, flow200_g100p −296,
flow200_g200p −528, flow201_g10 −432, flow201_g100p −388, flow201_g140 −155.

| in-sample read | Pearson vs pooled hold-out | Spearman | n |
|---|---:|---:|---:|
| α 1.0 (the record itself) | **+0.85** | **+0.89** | 6 |
| α 0.3 | +0.38 | +0.60 | 6 |
| α 0.1 | +0.33 | +0.60 | 6 |

**The scaled read does not pre-rank records; the unscaled one does.** The α 0.1 in-sample Δ is
the weaker predictor of hold-out on all six, and it is weaker precisely because the cliff
destroys the ordering (α 0.1 collapses flow200_g100p and flow201_g10 onto the same −520/−565
while their hold-out Δ differ by 136). Use the plain α = 1.0 in-sample screen (the `S/insample`
run, 206 episodes per record, ~2 min CPU) to pre-rank a record before spending an engine leg;
there is no reason to screen scaled versions. n = 6 and all six hold-out Δ are negative, so this
is an ordering read inside a narrow band, not a calibration.

## Files

`S/alpha/build_thetas.py` (md5s of the 18 thetas in its stdout), `S/alpha/run.sh`,
`S/alpha/analyse.py`, `S/alpha/alpha_summary.json`, logs `S/alpha/a01.log` (1,648 eps, 675 s),
`a03.log`, `a003.log` (1,236 eps each), rows in `S/simscreen/alpha_a{01,03,003}.csv`.
