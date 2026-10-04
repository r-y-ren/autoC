# Record selection and gate calibration (log-based, 2026-09-10)

Read-only from remote `train.log` / `log.jsonl` / `real_gate.log` (flow172/183/184/184b/185b/185c in
`~/stage_leg20`; 187/188 in `~/stage_hr`) and the local judge (`S/glut/verdicts.log`,
`docs/strategy/2026-09-10-verdicts.txt`). Data: `S/gatecal/records.csv` (53 rows) + `q*.txt`. No
engine runs. `~/stage_slope/artifacts/flow184*` is byte-identical to the `stage_leg20` copies.

## Mechanism in the logs (correcting the brief)

`train.log`'s `abs <value>` is the probe's **coin** read (~100k). The **selector** is
`log.jsonl:abs_score` (= `abs_screen`, a 0-1 score on the 64 fixed seed pairs): a record fires when
`abs_score > bar + best_margin(0.005)`, the candidate is re-measured 2x (`abs_replicate`) and that
mean becomes the new bar (verified on every record of every arm). `best_abs` in log.jsonl is that
bar rounded to 1 dp - not a value. Coins and score decouple (flow172 g850: 99,716 coins = a record;
g840: 100,373 = not), so Delta-abs below uses `abs_score`, with the coin Delta alongside.

## Q1 - does the in-sim probe select real records?

**(a) Correlation with the gate.** 45 gate decisions, 37 with a computable Delta-abs.

| pairing | n | Pearson | Spearman |
|---|---|---|---|
| Delta abs_score vs gate net flips, **records only** | 25 | **-0.016** | **-0.365** |
| Delta abs_score vs net, all decisions (records+periodic) | 37 | +0.286 | +0.103 |
| Delta abs_score vs net, min_flips arms only (183-188) | 9 | +0.080 | +0.043 |
| Delta abs **coins** vs net | 37 | +0.025 | +0.092 |
| abs_score **level** vs net | 45 | -0.301 | -0.134 |

The +0.286 on "all decisions" is an artefact of the periodic rows (negative Delta-abs *and* negative
net); among records the magnitude of the in-sim gain carries **no** information about the size of
the real gate move. The level correlation is negative: the further an arm has trained, the worse a
record does on the pinned field.

*vs the local judge* - only 4 records ever had a LIVE-C leg (n=4, no correlation computable):

| record | gate net | judge TOPB2 | judge LIVE-C | judge LIVE62 | verdict |
|---|---|---|---|---|---|
| flow184 g10 | +4 ACCEPT | 25.0->25.0 (-69) | C22 63.6->59.1 (+133) | 88.7->88.7 (+20) | LEVEL/NEG |
| flow185c g10 | +3 ACCEPT | 25.0->30.0 (-1,090 t-2.0) | C63 68.3->68.3 (-560) | 88.7->**82.3** (-781) | NEGATIVE |
| flow185b g160 | +3 ACCEPT | 25.0->25.0 (-198) | C72 68.1->**59.7** (-302) | 88.7->85.5 (+83) | NEGATIVE |
| flow187 g70 | +2 refuse | 25.0->30.0 (+740 t1.5) | h30 63.3->60.0 (-325) | 88.7->87.1 (+231) | LEVEL |
| flow172 g940 | +0 ACCEPT | TOPB 25->35 (+5,578) | (set did not exist) | LIVE55 34.5->83.6 | POSITIVE |
| flow172 g1000 | +4 ACCEPT | TOPB 25->40 (+5,758) | C8 50->75 (hr comp) | LIVE55 34.5->89.1 | POSITIVE |

Sign of Delta-abs is uninformative here too: g940 (+0.0089) and g1000 (-0.0048, a periodic pick) are
the genuine wins; the false accepts sit at +0.008..+0.015 or are first-records.

**(b) How often a higher-abs record reads >= 0** - of 25 records with Delta abs_score > 0 and a gate
read (null probabilities from the bootstrap in Q2):

| threshold | observed | null | one-sided binomial p |
|---|---|---|---|
| net >= 0 | 17/25 (68 %) | 56 % | 0.157 |
| net > 0 | 16/25 (64 %) | 44 % | 0.035 |
| net >= 3 | 11/25 (44 %) | 27 % | 0.050 |
| net >= 5 | 7/25 (28 %) | 15 % | 0.070 |

Restricted to flow172 - the only arm whose accept rule (leg20 Delta-margin) never used net flips, so
net is unselected - 14/18 records land net > 0 (78 % vs 44 %, p = 0.0038) and 10/18 net >= 3
(p = 0.0097). **The probe selects better-than-chance thetas in sign but not in size; the effect is
~+1.3 net games per record above chance.** On the local judge the 2026-09-10 arms are 0 for 4.

**(c) Trajectory / overfit signature** - flow172, 128 abs samples over 1,280 gens:

| gens | abs_score | slope /100 gens | gate paired margin at the last decision |
|---|---|---|---|
| 0-199 | .4349 -> .5163 | +0.0421 | +99 |
| 200-399 | .5318 -> .5554 | +0.0159 | +1,008 |
| 400-599 | .5592 -> .5752 | +0.0107 | +2,556 |
| 600-799 | .5931 -> .6223 | +0.0090 | +2,796 |
| 800-999 | .6021 -> .6196 | +0.0107 | +3,865 |
| **1000-1199** | .6387 -> .6344 | +0.0018 | +4,082 (down from 4,294) |
| **1200-1399** | .6400 -> .6523 | +0.0133 | **+3,718** |

The curves track each other to **gen ~1000**, then separate: abs_score keeps climbing (+0.013/100
gens in 1200-1399, coins 100,365 -> 100,643) while the pinned-gate margin falls 4,294 -> 4,142 ->
4,082 -> 3,718 and every candidate is refused - the same gen at which the local judge flattened
(es-rate A/B: "ZERO after g1000, 4 arms, 482 gens, 0 accepts"). flow187 (+0.0162/100 gens) and
flow188 (+0.0103) show the same shape over 150 gens with 7 gate reads whose best net is **+2**.
**Divergence gen ~1000 for flow172; from gen 0 for flow187/188 (gate field disjoint from the rungs).**

## Q2 - gate calibration

Per-field empirical change rate `p_hat = (FLIPS+DROPS)/games`, averaged over decisions:

| field | games | boards | decisions | mean FLIPS | mean DROPS | p_hat |
|---|---|---|---|---|---|---|
| flow187/188 | 124 | 62 | 7 | 5.57 | 6.57 | 0.0979 |
| flow185b | 166 | 83 | 3 | 8.33 | 7.00 | 0.0924 |
| flow185c | 84 | 42 | 3 | 4.67 | 5.67 | 0.1230 |
| flow172/183/184/184b | 120 | 60 | 32 | 5.72 | 3.53 | 0.0771 |

**Independence, measured not assumed.** Across 45 consecutive eval pairs, 67 boards changed: **60
(89.6 %) moved BOTH seats, 7 (10.4 %) moved one seat** (within one eval only 0.9 % of boards are
seat-split, yet 19/45 decisions have an odd FLIPS or DROPS count). The null below uses that measured
mixture, which inflates sd **1.39x** over a naive per-game model: state both n - 124 games but **~62
effectively independent boards**.

**(a) False-positive tail observed.** Every candidate the judge read LEVEL or NEGATIVE had net in
**{+2, +3, +3, +4}**; the two genuine positives had net **{0, +4}**. At n = 6 net flips do not
separate positives from negatives at all.

**(b) Bootstrap null** - 400k trials; each board changes with p_b, 89.6 % of changed boards move
both seats +/-2, 10.4 % one seat +/-1, direction a coin flip:

| gate | sd(net) | P(net>=3) | P(net>=5) | P(net>=7) | P(net>=10) | net for 5 % FA | for 1 % FA |
|---|---|---|---|---|---|---|---|
| 124 games / 62 boards | 4.86 | 0.290 | **0.167** | 0.085 | 0.027 | **>= 9** | >= 13 |
| 166 games / 83 boards | 5.45 | **0.314** | 0.198 | 0.111 | 0.042 | >= 10 | >= 14 |
| 84 games / 42 boards | 4.48 | **0.273** | 0.146 | 0.068 | 0.019 | >= 9 | >= 11 |
| 120 games / 60 boards | 4.23 | 0.259 | 0.131 | 0.057 | 0.015 | >= 8 | >= 11 |

If the 124 games were fully independent, P(net>=5) = 0.096 and the 5 % bar is net >= 7 - still above
the shipped min_flips 5. **min_flips 5 on the 124-game gate is a ~17 % false accept per nomination;
min_flips 3 on the 83- and 42-board gates is 31 % and 27 %** - reproducing the independent
gate-design A/B estimate (~20 %) and the day's tally of 3 false accepts.

**(c) Power** - true effect = k boards genuinely converted (both seats), plus the same flip noise:

| gate | min_flips | 50 % power | 80 % power |
|---|---|---|---|
| 124 games / 62 boards | 5 | 3 boards = 6 games = **4.8 win pts** | 5 boards = 10 games = **8.1 pts** |
| 166 games / 83 boards | 3 | 2 boards = 4 games = 2.4 pts | 4 boards = 8 games = 4.8 pts |
| 84 games / 42 boards | 3 | 2 boards = 4 games = 4.8 pts | 4 boards = 8 games = 9.5 pts |

min_flips 5 at 124 games needs ~+8 win points to fire reliably, while the whole g60->g1000 lineage
bought ~+2 win pts per 100 gens on the local judge. Raising the bar to net >= 9 (5 % FA) would cost
essentially all remaining sensitivity at this field size - **the fix is more boards, not a higher
threshold** (at 240 boards/480 games, p_hat 0.10, sd(net) ~9.6, the 5 % bar is net >= 17 = 3.5 win
pts: the same false-accept rate at half the detectable effect).

## Cross-check of the day's four known decisions

- **flow185c g10** (net +3/84 ACCEPT, judge REFUSED, LIVE62 88.7->82.3) and **flow185b g160**
  (net +3/166 ACCEPT, judge REFUSED, LIVE-C 68.1->59.7): null P(net>=3) = 0.27 and 0.31 - both
  accepts were *inside* the noise, nothing further to explain.
- **flow187 g70** - net +2 refuse; judged LEVEL (LIVE-C h30 -3.3 pts, LIVE62 -1.6, TOPB2 +740 on 40
  games). A **correct refusal**; false-refuse tally 0/1.
- **flow172 g940** - net **+0**, ACCEPTED by the leg20 Delta-margin rule, and it is the shipped theta
  (+9,130/game on LIVE55, TOPB 25->35 %). A net-flips gate at any min_flips >= 1 would have
  **rejected the best candidate of the campaign**: the margin moved +3,314 -> +3,865 while the win
  count stayed 76/120 - the information was in the margin, not the flip count.

## Dead ends / gaps

- No gen has a missing `abs` where a record fired; abs is sampled every 10 gens (gens 1-9 and
  non-multiples of 10 have none - expected). flow185c has no `real_gate.csv` left on disk, and
  flow183/184/184b produced no judged record other than flow184 g10.
- LIVE-C reads exist for only 4 records ever, against three different cuts (22/63/72 boards) plus
  one hold-out cut (30) - the Delta-win column is not comparable across those rows.
- flow172's gate used metric `leg20`, so its ACCEPT/refuse column must not be pooled with the
  min_flips arms when scoring the *gate*; its net flips are unselected and the cleanest data here.
