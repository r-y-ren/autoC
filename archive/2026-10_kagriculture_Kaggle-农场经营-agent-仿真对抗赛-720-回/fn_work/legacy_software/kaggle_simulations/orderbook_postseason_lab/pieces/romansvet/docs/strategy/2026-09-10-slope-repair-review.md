# Review: `slope-repair` (62c571f..6486bac) before a GPU arm — 2026-09-10

Read-only, vs `arms-next` 45f8217. Numbers are my own re-measurement.

## 1. Padding / identity — PASS

`_qfloor(8·0 + 0.5) = floor(0.5 + QUANT_EPS) = 0` exactly, so a zero `g12` gives
`floor = 0.0` and `w = 0.0 + 1.0*w` is bit-exact in float32. Neither tie-perturbing path
fires: `can_mature*absorb` multiplies a zero vector, `floor/max(sum,1.0)` is `0/1`.
`w_sum == 0` is safe — `floor` carries the same mask and `plant_total` is already 0.
Verified: zero-gene floor logits all zero, `sum(plant_target)` conserved 300/300 ON.

`pytest test_plant_floor test_forward_gene test_genome_retype` → **49 passed** (22/19/8).

## 2. ES plumbing — PASS, with one gap

* `--train-only g12,gb12`: `train_mask` (es/train.py:947-968) validates names against
  `dict(PO.SHAPES)`; accepted, 165 coordinates, all live in `live_mask`.
* `--init-theta` auto-pads at **scripts/train.py:2618-2620** — `if init.shape[0] < tr.n:
  init = PO.pad(init)`; `PO.pad` (policy.py:564) zero-extends. 6,789 → 6,954 clean.
* Packager: `N_PARAMS` derives from `SHAPES`, so a 6,954 theta unpacks. **Gap:**
  `package_submission.py:228` copies `theta.npy` with no length assertion, and lines
  44-49 vendor `core/{brain,plan,policy}.py` from whatever tree it runs in — the
  vendored switch, not the theta, decides which program ships.

## 3. Gene slope — credible, reproduced

Move condition `z ≥ 0.5/FLOOR_GAIN = 1/16`, `z ~ N(0, 0.02·√(‖gh‖²+1))`. `‖gh‖` measured
off `PO.forward` itself (32 one-hot probes, flow172_g1000, 300 boards): mean 3.43 → sd
0.0714 → 0.875σ → **predicted 18.8 %** per crop, 64.1 % any-of-5. Empirical (48
antithetic pairs): **melon 19.2 %, any 61.6 %**, largest single-step floor 2/16.
Builder's 19.1 / 62.6 confirmed.

Tiles move: `plant_total` mean 11.4, median 12, p90 20; a 1/16 melon floor gains a tile
on **108 of 280** planting days, 4/16 gives +510. Incumbent plants 0 melon on all 300.

## 4. Corner risk — acceptable

One step reaches 2/16; the whole-day corner needs `gb12 ≈ 2.0`, hundreds of sgd steps at
lr 0.003 — selection, not noise. `2026-09-09-launch_flow172.sh` carries 147 pinned tape
rungs, 20 fresh top-ten tapes at `--rung-weight 3`, `--arch-frac 0.9`; the 12-tape leg
family stays w0. Top tier is in the fitness at the highest weight, so the corner is
priced where it might pay.

## 5. Verdict — launch the floor arm; do not bundle `compact`


**`COMPACT_SOFT_ON = True` is a behaviour change, not a slope repair.** At an unchanged
flow172_g1000 `compact` is 7 on 300/300 boards OFF and 6/7/8 ON — **differs on 202/300
(67.3 %)**. `dev[0]` is `g6`, which `--train-only g12,gb12` never touches, so that arm
moves the champion's plan with zero trainable slope on the change. Own arm (`g6,gb6`),
own paired gate.

**The one thing that would make a launched arm uninterpretable:** the switches are
source globals that nothing prints, checkpoints or asserts — `--fitness-manifest`
(scripts/train.py:2719) logs fitness weights only. rsync the wrong staged tree and the
arm trains 165 coordinates no decode reads (a silent flow151), with no log line saying
so. **Fix first:** print `PLANT_FLOOR_ON` / `COMPACT_SOFT_ON` in the startup banner.
Minor: `test_plant_floor.py` skipifs on absolute `/mnt/e/...` paths, so its identity and
slope tests silently skip on the remote.
