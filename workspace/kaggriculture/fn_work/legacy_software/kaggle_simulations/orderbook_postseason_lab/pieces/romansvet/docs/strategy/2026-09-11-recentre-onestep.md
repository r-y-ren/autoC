# Re-centring B's one-step test: is the no-signal result a property of g1000 or of the estimator?

2026-09-11, 22:26-23:30Z. Scripts + raw output: `S/popcurve/B/recentre.py`, `summarise_recentre.py`,
`recentre.json`, `recentre.log`, `recentre_summary.txt`, `grads/g_g400_p512_s9001.npy`,
`grads/g_g940_p512_s9001.npy` (remote copies in `~/popcurve/B/`). The g1000 row is B's
`onestep.json` (docs/strategy/2026-09-10-pop-spearman-B.md §3), untouched.

**Verdict in one line.** The no-signal finding is a property of the **centre**, not of the estimator or
the objective: at `flow172_g940` the same P=512 / sigma 0.02 / margin_scale 3000 ES step, at the arm's
real Adam length `||d|| = 0.2323`, **gains** on the objective one generation later both in-sample
(+0.0067 obj_w, beats 16/16 random steps, antisym z +3.1) and held-out (+0.0043 obj_w, beats 16/16),
where at g1000 the identical step loses (-0.019 / -0.007) and beats 3/16 and 11/16. But g1000 is still
the highest point of the lineage on every metric, in-sample and held-out, by more than one g940-step's
gain — so **keep the arms' init at g1000**; re-centring would retrace the path the lineage already took.

## 1. Design (B's rig, one token changed)

`recentre.py` imports `popcurve.build_trainer / build_batch / one_draw` and `onestep.score_batch /
held_out_argv / report`; the *only* edit to the flow187 launcher argv is the `--init-theta` value.
Both centres verified at setup: theta == the `.npy` (`theta_matches_file True`), md5 576dc458 (g400) /
958f100d (g940), shape (6789,), `n 6789 live 5997 sigma 0.02 margin_scale 3000 abs_weight 0.0
||d|| 0.2323 episodes 159 pinned 147` — identical to B's g1000 setup line. Same 8 random +-
control directions (`default_rng(777)`, live mask), same in-sample batch (the trainer's rng is
independent of theta, so the 159 episodes are the same boards B scored), same held-out = LIVE-C
43-72 played pinned from both seats (60 games). One ES seed (9001) per centre — seed 9002 did not fit
the 75-min box (each centre took 1,364 / 1,376 s on the shared GPU0; two arms untouched throughout).
`||g_9001||`: 39.26 (g400), 41.80 (g940), 40.90 (g1000) — the estimator's scale is centre-independent,
as rank normalisation predicts.

Statistics per B: antisym = F(+d)-F(-d) isolates the linear term; its sd over the 8 random pairs is
`2|gradF| ||d|| / sqrt(n)`, so `z = antisym/sd`, `kappa = z/sqrt(5997)`, and `|gradF| ||d|| = sd
sqrt(n)/2` (an upper bound — the random antisym spread also carries the discrete-outcome roughness).
`ES_sym = (F(+d)+F(-d))/2 - F(c)` is the curvature the ES direction buys, vs the random mean.

## 2. Is g400 genuinely lower than g940 / g1000 on this objective? Yes, monotone.

| centre | ‖θ‖ | F_in obj_w | F_in win_w | F_in margin | F_ho obj_w | F_ho win_w | F_ho margin |
|---|---|---|---|---|---|---|---|
| g400  | 16.626 | 0.5197 | 0.5190 | +2,473 | 0.5415 | 0.5000 | +1,071 |
| g940  | 17.812 | 0.5839 | 0.5737 | +3,505 | 0.6037 | 0.6000 | +2,573 |
| g1000 | 17.964 | 0.5952 | 0.6102 | +3,801 | 0.6164 | 0.6667 | +3,185 |

The lineage climbed the flow187 objective for real, and held-out (never trained on) tracks it: g400→g940
+6.4 pts obj / +10 pts held-out win; g940→g1000 a further +1.1 pts obj / +6.7 pts held-out win (60
games, so the win step is ~1 sd, the coin step +612 is firmer). g1000 is the best point on all six cells.

## 3. The ES step at each centre (seed 9001; g1000 = B's seed 9001)

**IN-SAMPLE (159 episodes)** — `+d` gain = F(+d)-F(c); `rand<+d` = fraction of the 16 random steps the ES step beats.

| metric | centre | +d gain | -d gain | antisym | rand asym sd | z | κ | ES_sym | rand sym mean (sd) | ‖∇F‖‖d‖ | rand lose | rand<+d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| obj_w | g400 | **+0.0050** | -0.0165 | +0.0215 | 0.0145 | +1.49 | +0.019 | -0.0058 | +0.0042 (0.0041) | 0.56 | 44 % | 44 % |
| obj_w | g940 | **+0.0067** | -0.0244 | +0.0311 | 0.0100 | **+3.11** | **+0.040** | -0.0089 | -0.0102 (0.0042) | 0.39 | 94 % | **100 %** |
| obj_w | g1000 | -0.0194 | -0.0284 | +0.0091 | 0.0137 | +0.66 | +0.009 | **-0.0239** | -0.0111 (0.0043) | 0.53 | 100 % | 19 % |
| win_w | g400 | -0.0037 | -0.0351 | +0.0314 | 0.0107 | +2.92 | +0.038 | -0.0193 | -0.0003 (0.0131) | 0.42 | 62 % | 31 % |
| win_w | g940 | **+0.0247** | -0.0255 | +0.0502 | 0.0233 | +2.15 | +0.028 | -0.0005 | +0.0013 (0.0105) | 0.90 | 50 % | 94 % |
| win_w | g1000 | -0.0392 | -0.0511 | +0.0119 | 0.0139 | +0.85 | +0.011 | **-0.0452** | -0.0228 (0.0090) | 0.54 | 100 % | 6 % |
| margin | g400 | -102 | -357 | +255 | 341 | +0.75 | +0.010 | -229 | -8 (101) | 13.2k | 50 % | 50 % |
| margin | g940 | **+306** | -812 | +1,118 | 182 | **+6.15** | +0.079 | -254 | -87 (132) | 7.0k | 81 % | 94 % |
| margin | g1000 | -290 | -710 | +420 | 352 | +1.19 | +0.015 | -500 | -131 (167) | 13.6k | 69 % | 25 % |

**HELD-OUT (LIVE-C 43-72, 30 boards x 2 seats)**

| metric | centre | +d gain | -d gain | antisym | rand asym sd | z | κ | ES_sym | rand sym mean (sd) | ‖∇F‖‖d‖ | rand lose | rand<+d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| obj_w | g400 | -0.0081 | -0.0275 | +0.0194 | 0.0139 | +1.39 | +0.018 | -0.0178 | -0.0221 (0.0067) | 0.54 | 100 % | 94 % |
| obj_w | g940 | **+0.0043** | -0.0208 | +0.0251 | 0.0148 | +1.70 | +0.022 | -0.0082 | -0.0173 (0.0054) | 0.57 | 100 % | **100 %** |
| obj_w | g1000 | -0.0069 | -0.0449 | +0.0381 | 0.0300 | +1.27 | +0.016 | -0.0259 | -0.0173 (0.0072) | 1.16 | 81 % | 69 % |
| win_w | g400 | 0.0000 | +0.0167 | -0.0167 | 0.0576 | -0.29 | -0.004 | +0.0083 | +0.0208 (0.0161) | 2.23 | 19 % | 19 % |
| win_w | g940 | +0.0167 | 0.0000 | +0.0167 | 0.0350 | +0.48 | +0.006 | +0.0083 | +0.0010 (0.0169) | 1.36 | 25 % | 69 % |
| win_w | g1000 | -0.0333 | -0.0833 | +0.0500 | 0.0609 | +0.82 | +0.011 | **-0.0583** | **-0.0708** (0.0189) | 2.36 | 94 % | 75 % |
| margin | g400 | +104 | -266 | +370 | 388 | +0.95 | +0.012 | -80 | -358 (175) | 15.0k | 88 % | 94 % |
| margin | g940 | **+617** | -13 | +630 | 440 | +1.43 | +0.019 | +302 | -121 (237) | 17.0k | 69 % | 100 % |
| margin | g1000 | -196 | -1,113 | +918 | 690 | +1.33 | +0.017 | -655 | -488 (205) | 26.7k | 88 % | 75 % |

## 4. Reading

1. **Alignment/gain exists at g940 and (weaker) g400, not at g1000.** In-sample κ on the objective is
   0.040 at g940 vs 0.009 at g1000 (4.5x; z +3.11 vs +0.66 on 7 dof); the coin antisym at g940 is
   z +6.15, the largest signal any of these rigs has produced. Held-out κ is flatter (0.018 / 0.022 /
   0.016) but the *net* step differs in sign: g940 +d gains held-out obj (+0.0043, +617 coins, +1.7 pt
   win) and beats every one of the 16 random steps; g1000 +d loses (-0.0069, -196, -3.3 pt).
2. **g1000 is a sharper peak.** Random steps lose 100 % in-sample at g1000 (mean -0.0111) vs 94 % at
   g940 (-0.0102) vs 44 % at g400 (+0.0042 — the landscape at g400 is not yet a hilltop). Held-out win:
   a random step costs -7.1 pts at g1000 vs +0.1 / +2.1 at g940 / g400. And the ES direction's own
   curvature term at g1000 (-0.0239 in / -0.0259 ho obj) is 2.7x / 3.2x the g940 value (-0.0089 /
   -0.0082): at g1000 the estimator loads on brittle directions, at g940 it does not.
3. **|∇F|·||d|| is the same everywhere** (0.39-0.56 in-sample, 0.54-1.16 held-out): the objective is not
   flatter at g1000; the estimate simply stops pointing along it. Consistent with a centre that the
   sigma-0.02-smoothed objective's gradient no longer resolves, i.e. a local maximum reached.
4. **The estimator is not broken and the objective is not exhausted in general** — the flow172 recipe
   made real, held-out-verified progress from g400 to g1000 (§2) and this rig sees the mechanism at g940.
   The pop/margin_scale/sigma A/Bs were all run at the one centre where there is nothing to find.

## 5. Recommendation

**Keep the arms' init at g1000.** g1000 leads g940 by +0.011 obj / +6.7 pt win held-out; one g940
step recovers +0.004 / +1.7 pt, and the g940→g1000 segment *is* sixty of those steps under the same
recipe. Re-centring flow191+ at g940 (or g400) would retrace to the same hilltop — it buys nothing
except a controlled demonstration that the arm climbs (which §3 already gives). The constructive
implication is different: further gain from g1000 needs a **changed objective field** (opponents /
boards on which g1000 is not already a peak — e.g. the flow190-style widened gate rungs *inside* the
fitness, not only in the gate), not a changed estimator; B's `lr 0.003 -> 0.001` remains the only
per-step lever with evidence, and its case is strongest exactly at g1000 (curvature 2.7x). If a
re-centred control arm is wanted anyway, g940 is the centre (κ 0.04, step gains held-out), never g400.

## 6. Caveats / dead ends

* One ES seed per centre (9001). B's seed 9002 at g1000 gave antisym ≈ 0 in-sample; a single seed can
  overstate κ by ~1 sd (0.013). The g940 obj_w z +3.11 / margin z +6.15 exceed that, the held-out
  z +1.7 does not on its own — it is the *sign* of the net step (gain vs loss, 16/16 vs 3/16) that
  separates the centres. A seed-9002 repeat at g940 (~23 min) is the next check if anyone needs it.
* Held-out win_w is quantised at 1/60; use obj_w/margin for the held-out comparison.
* `|∇F|·||d||` from the random spread is an upper bound (discrete-outcome roughness counts as spread).
* Not tried: intermediate centres (g600-g800) to locate where alignment dies; two-step compounding.

## Seed-9002 replication at g940
2026-09-11 23:47-00:17Z, GPU1, same `recentre.py` (md5 f8b4606b local=remote), `--centres g940 --seeds 9002`; theta md5 958f100d, `theta_matches_file True`, setup line identical to 9001's; ‖g_9002‖ 40.23 (9001 41.80); same 8 random ± controls (rng 777). Files `S/popcurve/B/recentre_s9002.{json,log}`, `grads/g_g940_p512_s9002.npy`, `summarise_pooled.py` → `pooled_summary.txt`.
Centre + random rows agree across the two g940 runs to 4.9e-4 obj_w (in) / 1.3e-3 (ho); each seed is scored against its own run's centre. Pooled = 2-seed mean ± half-difference; κ null sd for a 2-seed mean = 1/√5997/√2 = 0.0091; z_pooled = Σz/√2.
| block | metric | seed | F(c) | F(+d) | F(−d) | antisym | rand asym sd | z | κ | net +d gain | rand<+d |
|---|---|---|---|---|---|---|---|---|---|---|---|
| in | obj_w | 9001 | 0.5839 | 0.5906 | 0.5595 | +0.0311 | 0.0100 | +3.11 | +0.040 | **+0.0067** | 16/16 |
| in | obj_w | 9002 | 0.5839 | 0.5907 | 0.5619 | +0.0288 | 0.0100 | +2.88 | +0.037 | **+0.0069** | 16/16 |
| in | win_w | 9001 | 0.5737 | 0.5984 | 0.5482 | +0.0502 | 0.0233 | +2.15 | +0.028 | +0.0246 | 15/16 |
| in | win_w | 9002 | 0.5810 | 0.5774 | 0.5518 | +0.0255 | 0.0233 | +1.10 | +0.014 | −0.0036 | 9/16 |
| in | margin | 9001 | +3,505 | +3,811 | +2,693 | +1,118 | 182 | +6.15 | +0.079 | **+305** | 15/16 |
| in | margin | 9002 | +3,503 | +3,691 | +3,114 | +577 | 183 | +3.16 | +0.041 | **+189** | 15/16 |
| ho | obj_w | 9001 | 0.6037 | 0.6080 | 0.5829 | +0.0251 | 0.0148 | +1.70 | +0.022 | **+0.0043** | 16/16 |
| ho | obj_w | 9002 | 0.6043 | 0.6145 | 0.5734 | +0.0411 | 0.0151 | +2.72 | +0.035 | **+0.0102** | 16/16 |
| ho | win_w | 9001 | 0.6000 | 0.6167 | 0.6000 | +0.0167 | 0.0350 | +0.48 | +0.006 | +0.0167 | 11/16 |
| ho | win_w | 9002 | 0.6000 | 0.6167 | 0.5667 | +0.0500 | 0.0350 | +1.43 | +0.018 | +0.0167 | 11/16 |
| ho | margin | 9001 | +2,573 | +3,190 | +2,560 | +630 | 440 | +1.43 | +0.019 | **+617** | 16/16 |
| ho | margin | 9002 | +2,580 | +3,046 | +2,562 | +485 | 446 | +1.09 | +0.014 | **+466** | 16/16 |

**Pooled two seeds** (mean ± half-difference; κ null sd for a 2-seed mean = 1/√5997/√2 = 0.0091; z_pooled = Σz/√2):

| centre | block | metric | κ ± SE | z_pooled | net +d gain ± SE (random-step sd) | rand<+d |
|---|---|---|---|---|---|---|
| **g940** | in | obj_w | **+0.039 ± 0.002** | +4.24 | **+0.0068 ± 0.0001** (0.0064) | 32/32 |
| g940 | in | win_w | +0.021 ± 0.007 | +2.30 | +0.0105 ± 0.0141 (0.0152) | 24/32 |
| g940 | in | margin | +0.060 ± 0.019 | +6.58 | **+247 ± 58** (155) | 30/32 |
| **g940** | ho | obj_w | **+0.029 ± 0.007** | +3.13 | **+0.0073 ± 0.0029** (0.0092) | 32/32 |
| g940 | ho | win_w | +0.012 ± 0.006 | +1.35 | +0.0167 ± 0.0000 (0.0247) | 22/32 |
| g940 | ho | margin | +0.016 ± 0.002 | +1.78 | **+541 ± 75** (313) | 32/32 |
| g1000 | in | obj_w | +0.004 ± 0.004 | +0.47 | −0.0176 ± 0.0018 (0.0078) | 9/32 |
| g1000 | in | win_w | +0.004 ± 0.007 | +0.42 | −0.0406 ± 0.0014 (0.0110) | 1/32 |
| g1000 | in | margin | +0.014 ± 0.002 | +1.51 | −150 ± 141 (235) | 15/32 |
| g1000 | ho | obj_w | +0.011 ± 0.006 | +1.17 | −0.0091 ± 0.0022 (0.0163) | 21/32 |
| g1000 | ho | win_w | +0.005 ± 0.005 | +0.58 | −0.0500 ± 0.0167 (0.0352) | 19/32 |
| g1000 | ho | margin | +0.012 ± 0.005 | +1.34 | −308 ± 112 (394) | 22/32 |

**Cross-seed cosine**  cos(g_9001, g_9002): g940 **+0.0098**, g1000 −0.0001 (B's `cos_g1_g2`); null sd 0.0129. g940 does not clear the null, but two estimates each aligned κ ≈ 0.038 predict cos ≈ κ² ≈ 0.0015 ± 0.0129 — the cosine test has no power at this κ; the antisym / net-step rows are the evidence.
**Verdict: g940's ES signal replicates; seed 9001 was not a draw.** Seed 9002 reproduces κ > 0 on every metric (obj_w in 0.037 vs 0.040, ho 0.035 vs 0.022), +d beats 16/16 randoms held-out on obj_w and margin for both seeds (11/16 on quantised ho win_w, both), and pooled net gain > 0 with SE clear of zero on obj_w in (+0.0068 ± 0.0001), obj_w ho (+0.0073 ± 0.0029), margin ho (+541 ± 75). The one non-replicating cell is in-sample win_w (9002 −0.004, 9/16), the noisiest metric.
g1000 pooled stays flat (κ ≤ 0.014, net gain negative in all six cells). flow191's g940 init now rests on two seeds; §5's point that g1000 still leads g940 by more than one step's gain is unchanged.
