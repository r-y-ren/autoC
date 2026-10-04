# Calibrating the win-first gate (min-flips / margin-slack)

Data agent, 2026-09-09. Read-only over `S/lossflip/*_live62.csv`; no games played.
Scripts: `S/wfcal/cal.py`, `cal2.py`, `cal3.py`.

Set: the 55 **held-out** live tapes (`S/livewin/live_heldout_ids.txt`), seat-grouped
into boards exactly as `S/live55/flips.py` does. Base = `flow135_g350`.
Base record on the 55: **19 wins / 36 losses (34.5 %)**.

## 1. The statistic is biased upward under noise

The board margins are not symmetric about zero:

| side | n | within 3k of 0 | median abs |
| --- | --- | --- | --- |
| losses (base margin <= 0) | 36 | **11** | 6,958 |
| wins (base margin > 0) | 19 | **1** | 8,110 |

Eleven losses sit inside one noise-width of the win line and only one win does.
So **zero-mean noise flips far more boards than it drops**: `net flips` has a
*positive* null mean, and a `min-flips` threshold set against zero is mis-set.

Null distribution of net board flips on 55 boards (iid Gaussian per-board noise,
20,000 draws; `sigma` = per-board paired margin noise, coins/game):

| sigma | null mean | null **sd** | p95 | P(net>=4) | P(>=6) | P(>=8) | P(>=10) | P(>=12) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1,000 | +1.5 | 1.24 | +4 | .058 | .001 | .000 | .000 | .000 |
| 2,000 | +2.7 | 1.56 | +5 | .303 | .042 | .002 | .000 | .000 |
| 2,700 | +3.3 | 1.74 | +6 | .456 | **.108** | .009 | .000 | .000 |
| 4,000 | +4.2 | 2.05 | +8 | .627 | **.257** | .054 | .006 | .000 |
| 6,000 | +5.2 | 2.49 | +9 | .750 | **.447** | .172 | .039 | .006 |

Two data-driven estimates of the same sd, per the brief:

* **(a) resampling the candidates' own per-board deltas, centred to zero mean.**
  Sign-flip (symmetry) randomisation: sd **1.33 - 1.87** per candidate, pooled
  noise pool (n=220) sd **2.08**; null means +2.5 to +6.0.
  A plain bootstrap of the centred deltas gives sd **1.40 - 2.87** (same means).
* **(b) binomial.** 36 losing boards, 19 winning boards; pooled centred flip rate
  on losses .146, drop rate on wins .053 ->
  `sd = sqrt(36*.146*.854 + 19*.053*.947)` = **2.33**.
  With the raw (uncentred) rates .243 / .039 -> **2.71**.

**Null sd ~ 1.6 - 2.3 boards, with a null MEAN of +2.7 to +5.2**, not 0.
The realistic per-board noise is 2-5k coins/game (the observed candidate spreads
are sd 1.8-5.2k and include real signal; the shop draw is the source).

## 2. The candidates

Paired vs the live base on the 55 held-out boards, seat-grouped:

| candidate | flips | drops | **net boards** | family delta (coins/game) | SE | t |
| --- | --- | --- | --- | --- | --- | --- |
| `flow166_g170` | +11 | -1 | **+10** | +2,767 | 681 | +4.1 |
| `flow167_g150` | +10 | -1 | **+9** | +3,225 | 540 | +6.0 |
| `g170pair` | +11 | -1 | **+10** | +3,682 | 703 | +5.2 |
| `paironly` | +3 | 0 | **+3** | +875 | 247 | +3.6 |
| `flow172_g60` | +14 | -1 | **+13** | +4,592 | 591 | +7.8 |

(The brief quoted +10/+10 and +3.1k/+3.4k for the first two; the held-out read is
+10/+9 and +2.8k/+3.2k. `flow167_g150` is a nine, not a ten.)

## 3. ACCEPT / refuse table

`A` = accept, `r` = refuse. Rule as deployed: `net >= min_flips` and
`family delta >= -slack` (the all-games leg is checked separately, s5).

**Every candidate's family delta is positive**, so the slack column is inert:
the table is identical at slack 0, 400, 800 and 1600.

| candidate | net | family delta | mf=4 | mf=6 | mf=8 | mf=10 |
| --- | --- | --- | --- | --- | --- | --- |
| `flow166_g170` | +10 | +2,767 | A | A | A | A |
| `flow167_g150` | +9 | +3,225 | A | A | A | **r** |
| `g170pair` | +10 | +3,682 | A | A | A | A |
| `paironly` | +3 | +875 | r | r | r | r |
| `flow172_g60` | +13 | +4,592 | A | A | A | A |

(slack in {0, 400, 800, 1600}: no cell changes.)

## 4. Recommendation

**The deployed `6 / 800` does NOT meet (i).** A pure-noise candidate clears
`net >= 6` **10.8 %** of the time at sigma 2.7k, **25.7 %** at 4k and **44.7 %**
at 6k -- because the null mean is already +3 to +5. The 800-coin slack adds
nothing: it only bites at -800, which is 1.2 SE below a zero family delta, and
no candidate on record is near it.

Recommended: **`--real-gate-min-flips 9` with `--real-gate-margin-slack 0` on the
family**, i.e. the family margin may not go negative at all.

* (i) noise: `P(net>=9)` is .002 at sigma 2.7k, ~.02 at 4k, ~.08 at 6k; the
  `family delta >= 0` conjunct roughly halves each (a noise family delta is
  symmetric about 0 with SE ~680) -> **~1 % at 4k, ~4 % at 6k. <= 5 %.**
* (ii) `flow166_g170` (+10), `flow167_g150` (+9), `g170pair` (+10) and
  `flow172_g60` (+13) are all accepted; `paironly` (+3) is refused.

If the slack must stay non-zero for the metric's stated purpose (buying wins with
coins), use **`min_flips 10` + `slack 800`** -- but that loses `flow167_g150`.
The evidence is that real win-first gains have **not** cost margin: all five
candidates are +875 to +4,592 a game at t 3.6 to 7.8. A **positive** family floor
(>= 0) is a much sharper noise filter than any negative slack.

## 5. The all-games leg

Full pinned read for `flow166_g170` vs base: 157 shared boards **+3,786/game**;
the 148 boards outside the live family **+3,773/game with SE 757**.

The all-games mean is over ~3x as many boards but the per-game noise is barely
lower (SE ~750 vs ~680 on the family), so a slack of 800 there is **~1 SE** --
a genuinely neutral candidate fails leg (c) about 14 % of the time on noise
alone. Leg (c) exists only to stop the family being bought off the rest of the
set, so it should be a **looser** slack than the family's: **1,500 (~2 SE)**,
which refuses only real regressions while the tight (>= 0) floor does the work
on the family.
