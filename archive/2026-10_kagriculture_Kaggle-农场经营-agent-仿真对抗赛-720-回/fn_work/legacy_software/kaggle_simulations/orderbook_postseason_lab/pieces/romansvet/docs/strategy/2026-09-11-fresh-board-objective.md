# Fresh-board objective: 30 new LIVE-C boards (73-102) as weight-4 pinned rungs at flow172_g1000

2026-09-11, 01:06-01:52Z. Rig + raw output: `S/popcurve/B/fresh.py`, `fresh_ids.txt`, `fresh.json`, `fresh.log`,
`fresh_{A,B}_margins.npz`, `fresh_holdout_margins.npz`, `grads/g_fresh_p512_s9001.npy`, remote `rollouts/p512_s9001_fresh.npz`
(all in `~/popcurve/B/` too). Remote GPU1 next to flow191 (14.8 GB free), `~/stage_hr`, `--chunk 4096`, 2,273 s; both arms untouched.

**Verdict in one line.** The 30 fresh boards are a real change of field (the centre loses 9/30 in the sim — the same nine
it loses in the engine base read) — but adding them at weight 4 (18 % of the mass) turns the gradient by only 11°
(cos(g_A, g_B) 0.983) and the B step still **loses held-out** (LIVE-C 43-72: obj −0.0116, margin −186 coins, win −6.7 pt;
10/16 obj, 12/16 margin randoms beaten), like the A step (−0.0066 / −232 / −3.3 pt). The fresh slice shows the strongest
linear signal any rig has measured at g1000 (antisym z +2.0…+3.5, +d gain +628…+868 coins, 14-16/16) — for BOTH
directions, so it is the g1000 direction generalising to new boards, not the new rungs teaching anything. Decision rule
(held-out net gain > 0 on obj AND margin) fails → **flow192 NOT staged.**

## 1. Design

The seat-swap and lost-board docs: a changed field must change the OPPONENT or the BOARD. This is the first field that does:
the 30 pinned-town boards cut 00:25Z from sub 56140532 (LIVE-C 73-102, opponents 2512-2685, live 20 W / 10 L, g1000 hr base
21/30) appended as pinned rungs exactly as LIVE-C 1-42 were (`--tape-actions artifacts/tape_actions_town/<id>.npz`,
`--rung-weight tape_act_<id>=4`).

* **Field A** = the arm's objective, `~/launch_flow190.sh` via `popcurve.launcher_argv` (rung weights byte-identical to
  flow187's): 147 pinned + 12 carried = 159 episodes, mass 1,096 (pinned 1,084).
* **Field B** = A + 30 fresh rungs at w4 = 177 pinned. The trainer never refuses pinned > `--episodes` (`n_pairs =
  max((E − len(pin)) // 2, 1)`), but at E = 160 the carried block would shrink 12 → 2, so **B uses `--episodes 190`**
  (177 + 12 = 189 episodes). Fresh mass 240 of 1,336 = **18.0 %**.
* Centre g1000, P 512, σ 0.02, margin_scale 3000, ‖d‖ 0.2323 (lr 0.003·√5997), eps seed 9001, B's 8 random ± controls
  (rng 777). g_A from B's saved rollout `p512_s9001.npz` (cos vs B's saved gradient 0.99994); g_B from a fresh P = 512
  rollout on the B batch (same eps, 716 s). Centre + es_A± + es_B± + rand{0..7}± = 21 thetas scored on the A batch, the B
  batch (per rung → fresh-30 slice, old-147 slice, displacement) and HELD-OUT LIVE-C 43-72 both seats (60 games, uniform;
  43-72 ∩ 73-102 = ∅ asserted). antisym = F(+d) − F(−d), z vs the 8 random antisyms, κ = z/√5997, `beats` = of 16 randoms.
* **Seed 9002 not run**: the 9001 pass took 38 min (rollout 12 + XLA recompiles ~18); a second could not finish in the box.

## 2. Remote setup (additive only, verified)

* `rsync --ignore-existing`: `artifacts/tape_actions_town/<id>.npz` ×30 and `artifacts/panel_opp_town/opponent_tape_<id>/`
  ×30 into `~/stage_hr/artifacts/` — 352 → 382 in both dirs, 794,806 bytes, nothing else transferred.
* `~/stage_hr/artifacts/town_schedules.json` 352 → 382 rows: backup `town_schedules.json.bak_20260911T010929Z` (98,251 B
  = old file); rows from `S/band2100p/town_schedules.json` (same dict / `indent=1` format); no duplicate ids; old file minus
  its closing brace verified a **byte-prefix** of the new one, all 352 old values and their order re-checked after reload
  (`~/popcurve/B/append_town.py`). The arms read this file only at gate time, by id.
* `~/popcurve/B/{fresh.py,fresh_ids.txt,fresh_town_rows.json,append_town.py}` copied (mirrors in `S/popcurve/B/`).

## 3. F(centre) by field (one play of the 21-theta stack; A reproduces B/lostw to 4 dp)

| field | episodes | pinned won | obj_w | win_w | margin_w |
|---|---|---|---|---|---|
| A (current, 147 rungs) | 159 | 106/147 = 72.1 % | 0.5953 | 0.6102 | +2,650 |
| B (+30 fresh at w4) | 189 | 127/177 = 71.8 % | 0.6148 | 0.6264 | +3,209 |
| fresh-30 slice (uniform) | 30 | **21/30 = 70.0 %** | 0.7027 | 0.7000 | +5,747 |
| HELD-OUT LIVE-C 43-72, 2 seats | 60 | 40/60 = 66.7 % | 0.6164 | 0.6667 | +3,185 |

Fresh-30 sim losses: 107573857 −3.5k · 107584581 −8.0k · 107588978 −7.9k · 107600681 −0.3k · 107616563 −5.9k · 107620742 −5.7k ·
107623247 −3.9k · 107630176 −4.9k · 107632627 −1.0k = **the 9 boards the engine base read loses** (extension table 74, 78, 80,
84, 92, 93, 94, 96, 97), margins within ~0.5k. The P = 512 population wins 64.7 % of fresh episodes (centre 70 %).

## 4. One-step test (seed 9001, ‖d‖ 0.2323; `+d` = F(+d) − F(c); `sym` = (F(+d)+F(−d))/2 − F(c) = curvature cost)

**IN-SAMPLE A field** — random step −0.0107 obj (15/16 lose), −2.1 pt, −170 coins; rand antisym sd 0.0136 / 1.1 pt / 420

| step | obj +d | −d | antisym | z | κ | sym | beats | win +d (z, beats) | margin +d / antisym (z, beats) |
|---|---|---|---|---|---|---|---|---|---|
| es_A (= B's) | −0.0205 | −0.0284 | +0.0079 | +0.58 | +0.008 | −0.0244 | 3/16 | −3.9 pt (+0.65, 1/16) | −453 / +139 (+0.33, 3/16) |
| es_B | −0.0164 | −0.0275 | +0.0112 | +0.82 | +0.011 | −0.0220 | 6/16 | −4.2 pt (−0.81, 1/16) | −281 / +414 (+0.99, 8/16) |

**IN-SAMPLE B field (177 rungs, B weights)** — random −0.0104 obj (13/16 lose), −1.9 pt, −169 coins; antisym sd 0.0147 / 2.0 pt / 411

| step | obj +d | −d | antisym | z | κ | sym | beats | win +d (z, beats) | margin +d / antisym (z, beats) |
|---|---|---|---|---|---|---|---|---|---|
| es_A | −0.0130 | −0.0296 | +0.0166 | +1.13 | +0.015 | −0.0213 | 6/16 | −3.5 pt (+0.82, 1/16) | −194 / +418 (+1.02, 8/16) |
| es_B | −0.0110 | −0.0297 | +0.0188 | +1.28 | +0.017 | −0.0203 | 6/16 | −3.6 pt (+0.15, 1/16) | −149 / +625 (+1.52, 8/16) |

**FRESH-30 slice (uniform; in-sample for B only)** — random −0.0038 obj (9/16 lose), −0.8 pt, −52 coins; antisym sd 0.0218 / 4.6 pt / 459

| step | obj +d | −d | antisym | z | κ | sym | beats | win +d (z, beats) | margin +d / antisym (z, beats) |
|---|---|---|---|---|---|---|---|---|---|
| es_A | **+0.0149** | −0.0329 | +0.0478 | **+2.19** | +0.028 | −0.0090 | 14/16 | −3.3 pt (+0.72, 0/16) | **+868** / +1,586 (**+3.46**, 16/16) |
| es_B | **+0.0185** | −0.0254 | +0.0439 | **+2.01** | +0.026 | −0.0034 | 14/16 | 0.0 pt (+0.72, 7/16) | **+628** / +1,528 (**+3.33**, 15/16) |

**HELD-OUT LIVE-C 43-72 (60 games)** — random −0.0171 obj (13/16 lose), −6.9 pt (15/16), −484 coins (14/16); antisym sd 0.0298 / 6.6 pt / 688

| step | obj +d | −d | antisym | z | κ | sym | beats | win +d (z, beats) | margin +d / antisym (z, beats) | flips −/+ |
|---|---|---|---|---|---|---|---|---|---|---|
| es_A | −0.0066 | −0.0424 | +0.0359 | +1.21 | +0.016 | −0.0245 | 11/16 | −3.3 pt (+0.76, 11/16) | −232 / +811 (+1.18, 12/16) | 2/0 |
| es_B | **−0.0116** | −0.0551 | +0.0434 | +1.46 | +0.019 | −0.0333 | **10/16** | **−6.7 pt** (0.00, 7/16) | **−186** / +1,185 (+1.72, **12/16**) | 4/0 |

## 5. Displacement (per pinned rung; a random step of this length flips 7.2 won→lost / 2.4 lost→won on A, 7.6 / 2.7 on B)

es_A+: A batch −10/+2 (mass 52/12), B batch −11/+2 = old-147 −10/+2, fresh **−1/+0**. es_B+: A batch −11/+2 (60/16), B batch
−11/+2 = old-147 −11/+2, fresh **−0/+0**. The B step is not cheaper on the boards g1000 already wins (11 old rungs down, 5.5 %
of the old mass, 2 bought back — the A-step and random signature), and on the fresh 30 it flips nothing: its +628 coins there
are margin on boards already won (18/30 boards up), not new wins. Held-out it flips 4 wins down, 0 losses up (A: 2 / 0).

## 6. Reading

1. **The field changed and the estimator sees it** — F(c) 21/30 on the fresh slice, the nine engine losses reproduced to the
   board, 18 % of B's mass. Yet cos(g_A, g_B) = 0.983: 30 boards at w4 rotate the 6k-dim direction by 11°; both gradients are
   the 147-rung / 1,084-mass block's.
2. **The fresh boards carry the largest linear signal measured at g1000 — for both directions.** antisym z +2.0…+3.5, +d
   +0.015…+0.019 obj / +628…+868 coins, 14-16/16. g_A never saw those boards: this is the current step generalising to
   more boards of the same band, and it is margin on won boards (win +d 0.0 / −3.3 pt) — the same mechanism as the held-out
   margin antisym B/lostw already saw (+811 / +818), now on a slice the centre is not at a peak on.
3. **Held-out it still loses and is no better than A**: obj −0.0116 vs −0.0066, win −6.7 vs −3.3 pt, margin −186 vs −232.
   Antisym is positive (z +1.5 / +1.7, like A's +1.2) but sym −0.033 / −779 is larger: the curvature cost of a ‖d‖ 0.2323
   step at g1000 (13-15/16 randoms lose everywhere) is the binding constraint and more boards in the objective do not lower it.
   Rule: held-out net gain > 0 on obj AND margin — FAIL (obj −0.0116, 10/16; margin −186 although 12/16 randoms beaten).
4. **Is B's higher κ / antisym real alignment or noise?** Noise-sized. Same eps, same 21-theta plays, so the A−B difference
   is paired: held-out margin antisym +1,185 vs +811 = 0.54 random-antisym sd; obj +0.0434 vs +0.0359 = 0.25 sd; A-field obj
   +0.0112 vs +0.0079 = 0.24 sd; the two directions differ by 11° and B's +d gains are worse on obj/win, better on margin —
   no consistent sign. A two-seed follow-up on THIS design is not worth 40 min of the card; the B/lostw 9001-vs-9002 spread
   (their κ swung 0.007 → 0.000 on the same centre) is larger than every A−B gap here.
5. **What the sign pattern does say**: first-order gain real (held-out antisym +0.036…+0.043, fresh +0.044…+0.048), second-order
   dominated (sym −0.025…−0.033). The parabola optimum h*/H = antisym/(4·|sym|) ≈ 0.33-0.38 → net ≈ +0.005 obj / +110 coins
   per step, i.e. the arm's lr 0.001 (‖d‖ 0.077, which no rig has measured) sits where the step first nets positive — at
   seed-lottery size. That is a measurement to run (one play of θ ± d/3 on the saved thetas), not a result.

## 7. Verdict / staging

**Negative under the rule → flow192 NOT staged** (no `~/launch_flow192.sh`, no `S/flow192/`). Generator ready and tested
(`bash -n` clean; 177 tape paths / 177 rung weights; `--episodes 190 --run flow192 --seed 295`):
`python S/popcurve/B/make_flow192_fresh.py S/flow190/launch_flow190.sh S/popcurve/B/fresh_ids.txt <dst> <header>`. The remote
tree already holds every fresh-board file and town row an arm needs, so staging later is a one-second step.

## 8. Dead ends / caveats

* One seed (9001); B/lostw/recentre saw 9001 vs 9002 disagree by the size of these effects. Plays recompile for each new
  episode count (A play 457 s, held-out 640 s, B 9 s) — a second seed costs ~30 min on the shared card.
* `--episodes 190` for B, not 160 (else 2 carried self-play episodes instead of 12); a flow192 must carry the same flag.
* Not tried: fresh weight 8-10 (mass 30 %+); the fresh-rung-only gradient (does it point anywhere the 147-block does not?);
  the lr 0.001 step (θ ± d/3) on the saved plays; a second seed.
