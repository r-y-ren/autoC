# E3 prepared, not launched: the one-step test at candidate B's centre (σ × P)

2026-09-11, prep agent, time-boxed, **read-only on the campaign**: no training step, no sim
batch, no ssh, no judge lock, nothing under `src/`. Everything below is staged in `S/onestep/`
and dry-run; the first GPU second is spent only when a human runs one command.

## 1. What was prepared

E3 of `docs/strategy/2026-09-11-lever-ranking.md` (line 95): re-run the validated one-step
antisymmetric gradient test **at candidate B's centre** (`artifacts/kagg2_games/thetas/
flow193_g100_hr.npy`, 6,789 params, md5 `7fcf3948`, LIVE sub 56161192) over
σ ∈ {0.01, 0.02, 0.04} × P ∈ {512, 2048}, because consensus §20 says the σ/pop/margin-scale
A/Bs were all run at flow172_g1000 — the one centre where the estimator had nothing to find
(κ ≤ 0.014), while at g940 the same rig read κ 0.040 and its step beat 16/16 randoms held-out.

The rig survived the 07:17Z /tmp wipe: `S/popcurve/popcurve.py` (trainer/batch/draw, driven
from the arm's own CLI) and `S/popcurve/B/onestep.py` (scoring, hold-out argv, report) are in
the repo, so **nothing was reconstructed** — E3 is a new driver over the existing rig, changing
exactly two tokens of the flow193 launcher argv (`--init-theta` → B, `--sigma` → the cell).

| file | role |
|---|---|
| `S/onestep/sweep_b.py` | the σ×P driver (3 blocks × 2 pops; saves json/txt, grads, and a `.npy` per direction) |
| `S/onestep/run_local.sh` | the ONE command for the local 3070, with a card guard |
| `S/onestep/run_remote.sh` | the same on `~/stage_hr` (staging rsync in its header; the agent never ssh'd) |
| `S/onestep/judge.sh` | real-engine half: TOPB2 + LIVEC-H30 legs for +d, −d, randoms, paired vs B |
| `S/onestep/kappa.py` | engine-side κ from the leg csvs (CPU, no jax) |
| `S/onestep/heldout_ids.txt` | LIVE-C 43-72, identical to the rig's held-out list |
| `S/onestep/README.md` | design, commands, runtimes, memory, decision rule |

## 2. Design decisions worth recording

* **Step length is held fixed across cells**: `R = lr·√n_live = 0.003·√5997 = 0.2323`, the
  arm's real per-generation Adam displacement. σ and P change *which direction* the estimator
  picks, never how far the step walks — otherwise the cells would confound alignment with
  distance and the κ column would be unreadable.
* **The random controls are shared**: they depend only on (θ, mask, R, rng 777), so they are
  byte-identical in every σ block and identical to the ones in the g400/g940/g1000 tables. The
  driver asserts their scores reproduce across blocks (`[control check]`), which doubles as a
  proof that the CRN batch never moved between cells.
* **The objective field is B's own** (the flow193 launcher: 147 pinned rungs, top-ten at 10.2,
  LIVE-C 1-42 at 4, `--margin-scale 3000`, `--abs-weight 0.0`, `--pinned-once
  --pinned-fixed-seed --shop-crn`), not flow198's rotated field — E3 asks about the centre the
  campaign shipped, under the objective that produced it.
* **Hold-out = LIVE-C 43-72** played pinned from both seats: verified 0 overlap with the 147
  flow193 training rungs, and all 30 tapes plus all 147 rungs exist in the local tree
  (`S/localarm/tree`, whose `artifacts/` is a symlink to the repo's).
* **Two judges, not one.** The trainer-block κ (fast, 19 directions per cell) decides which
  cell to believe; `judge.sh` then re-measures the same antisymmetric statistic **in the real
  engine** on the promotion legs. `kappa.py`'s board pairing was validated against the
  auto-judge log: it reproduces `AUTOJUDGE-vsB flow196_g100p_hr` to the coin (TOPB2 −784 /
  −2.5 pp on 20 boards, LIVEC-H30 −755 / −3.3 pp on 30).
* **No shared lock.** `judge.sh` uses `S/onestep/judge.lock`; `/root/kagg3_judge.lock` stays
  the auto-judge's alone. The cost is CPU contention, which is why the default is WORKERS=8
  and the README says to run it when the queue is quiet.

## 3. Cost (measured, not guessed)

From `S/popcurve/results.csv` (3090, chunk 4096) and `S/popcurve/B/recentre.json`: draw 163 s
at P 512, 652 s at P 2048; trainer build ~220 s; hold-out block 575-790 s. The local 3070 runs
this workload at **1.85×** the 3090 (`launch_flow189.sh` header: 101.5 vs 55 s/gen).

* whole sweep, hold-out included: **~2.7 h local**, ~1.5 h remote (~55 / ~29 min per σ block)
* `HOLDOUT=0`: ~1.6 h local, ~50 min remote
* engine judge: ~3 min per direction (100 games); randoms ~25 min, each cell ~6 min, all ~1 h
* GPU memory: chunk-bound, not pop-bound. Default `--chunk 4096` ⇒ ~3.5-4.5 GB + ~0.1 GB of
  θ/eps arrays on the 8 GB card (the pop-512/chunk-8192 local measurement was 6,059 MiB peak);
  no generation and no abs probe is ever run, which is what OOM'd the card before.

## 4. The decision rule, fixed in advance

Read the **hold-out** block.

* **PASS**: held-out `κ(obj_w) > 0.03` **and** `+d` beats ≥ 6 of the 8 signed random steps
  (≥ 14/16 at the default `--nrand 8`) **and** net `+d` gain > 0 on `obj_w` and `margin`
  → continue the ES **from B** at that σ/P (prefer a passing P 512 cell: P 2048 is 4× the wall
  per generation). Confirm in the engine (`judge.sh`: κ(margin) > 0.03, positive paired margin
  vs B) and repeat at `EPS_SEED=9002` before an arm is re-cut — one seed can overstate κ by
  ~1 sd (0.013).
* **FAIL**: every cell flat (κ ≤ 0.015, net gain ≤ 0) → **B is a peak for this estimator**; stop
  turning σ/P/lr/margin_scale at this centre and change the field instead (E9 `W_lost` at B's
  centre, the seat-swap objective, fresh top-tier rungs — recentre-onestep §5's conclusion).
* **Mixed** (in-sample resolves, hold-out flat — the g400 signature): treat as FAIL for the
  knobs and as an argument for widening the field before the next arm.

## 5. Launch

```bash
nohup setsid bash /mnt/e/_work/kaggriculture3/S/onestep/run_local.sh >/dev/null 2>&1 &
```

It refuses while an ES arm holds the 3070 (flow198 at the time of writing, 5.8 GB in use), so
it is safe to arm now and let a human fire it the moment the card frees; `FORCE=1` overrides,
`DRYRUN=1` prints. The remote variant is `S/onestep/run_remote.sh` with the rsync line in its
header (this agent never ssh'd; the classifier blocks remote launches anyway —
`remote-launch-blocked` memory).
