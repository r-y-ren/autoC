---
name: promotion-rule-hr-slot
description: Which judge legs predict the rating a file reaches in the hr slot (sub 56143250), and the promotion rule that follows — 2026-09-12
metadata:
  type: analysis
---

# A promotion rule for the HR SLOT — 2026-09-12

Data-only. No engine games, no sim, no counterfactuals. Tooling and full tables:
`S/promo/{promo.py,files.csv,promo.md}`. Sources: `S/kaggle/watch_56143250.out` +
`S/calib2/games_56143250.csv` (hr's 205 rated ladder games), `S/calib2/fit.json`,
`S/bandgrad/rows.csv` (every judge board with its opponent rating and 20 records of paired
margins), `S/nextband/{boards.csv,teams.csv}` (NEXT30/NEXT14), `S/hladder/rows.json`,
`S/bladder/rows.json`, `docs/strategy/2026-09-11-ladder-projection.md`,
`docs/strategy/2026-09-12-transfer-mechanism.md`.

---

## 1. The hr slot's opponent distribution

hr = sub 56143250, 205 rated games recovered (142W-63L = 69.3 %), rating 2630 at the last read.
Matchmaking pins the opponent to our own rating: **opp − me = +4.0 ± 43.8** (post-30 games,
`S/calib2/games_56143250.csv`). So "the hr slot's pool" is *itself* ± 44, and it moves with us.

| window | n | mean | sd | min | p10 | median | p90 | max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all games | 205 | 2377 | 395 | 489 | 2111 | 2488 | 2655 | 2721 |
| last 100 | 100 | 2595 | 70 | 2437 | 2491 | 2611 | 2679 | 2721 |
| last 60 | 60 | 2630 | 47 | 2525 | 2556 | 2632 | 2696 | 2721 |
| **last 40** | 40 | **2637** | 48 | 2526 | **2568** | 2643 | **2705** | 2721 |

**The slot's live band is 2568-2705 (10/90 of the last 40), mean 2637.** hr has never met an
opponent rated ≥ 2800 (max 2721); only 5 of 205 games were ≥ 2700.

hr's own form in that band (last 100 games): < 2500 **73 %** (15), 2500-2599 **60 %** (30),
2600-2699 **52 %** (50), 2700+ 80 % (5). The 2600-2699 read on 50 games is the binding one and
it says hr is a ~2650-2720 file, consistent with the ladder-projection equilibrium **c = 2720
[2623, 2820]**.

### Which legs cover it

| leg | boards | min | p10 | median | p90 | max | share of hr's last-100 opponents inside the leg's range | exclusive weight (nearest leg by median), last 100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| LIVE62 | 62 | 1827 | 1939 | 1986 | 2061 | 2070 | **0 %** | **0 %** |
| LOSS10 | 10 | 2175 | 2188 | 2274 | 2381 | 2381 | **0 %** | **0 %** |
| LIVEC-H30 | 30 | 2440 | 2476 | 2536 | 2608 | 2615 | 52 % | 34 % |
| LIVEC-H30B | 30 | 2519 | 2535 | 2597 | 2648 | 2682 | **75 %** | 29 % |
| NEXT30 | 30 | 2567 | 2581 | 2653 | 2730 | 2750 | **66 %** | **37 %** |
| TOPB2 | 20 | 2953 | 2956 | 2976 | 3081 | 3081 | **0 %** | **0 %** |

**Answer (i): the hr slot lives at 2568-2705. LIVEC-H30B and NEXT30 cover it; LIVEC-H30 covers its
lower half; LIVE62, LOSS10 and TOPB2 cover none of it.** LIVE62 (1827-2070) and LOSS10 (2175-2381)
are 500-800 points below anything hr now plays; TOPB2 (2953-3081) is 250-350 points above.

---

## 2. Do the legs predict the rating? (what the upload history can and cannot support)

`S/promo/files.csv` lists every submission with a rating trajectory. Only **four** have both a
usable equilibrium rating and a paired leg margin against a common reference (hr):

| sub | file | rating obs | equilibrium c | LIVE62 | LIVEC-H30 | LIVEC-H30B | TOPB2 |
|---|---|---:|---:|---:|---:|---:|---:|
| 56143250 | hr = flow172_g1000_pair_hr | 2630 | **2720** [2623, 2820] | 0 | 0 | 0 | 0 |
| 56161192 | B = flow193_g100_hr | 2548 | **2565** [2397, 2740] | +644 | +772 | +1031 | +903 |
| 56140532 | flow172_g940_pair | 2509 | **2704** [2612, 2807] | −644 | −1131† | na | −635† |
| 56098262 | flow135_g350 | 1916 | ~1868 (est.) | −9734 | na | na | na |

† derived through `flow187_g160_hr` as a bridge (it was judged against both hr and g940_pair).
Every other upload (55957863 flow58_g450 1574, 55966718 split 1681, 55981305 earlysell 1680,
56006782 pump ~1996, 56013041 slot0 1983, 55887090/55890731 flow38 ~1780, 56139820 g60_pair 1764)
predates the paired judge and has **no leg read against any surviving reference** — they contribute a
rating and nothing to regress it on.

| leg | n | Pearson r | Spearman rho | one-variable slope (rating pts per +1,000 coins) |
|---|---:|---:|---:|---:|
| LIVE62 | 4 | +0.96 | +0.40 | +79 |
| LIVEC-H30 | 3 | −0.75 | −0.50 | −67 |
| LIVEC-H30B | 2 | — | — | −150 (two points are a line) |
| TOPB2 | 3 | −0.87 | −0.50 | −96 |

**Answer (ii), honestly: this regression is not identifiable and must not be used.** Three reasons:

1. **n = 3-4, and the leverage is one point.** LIVE62's +0.96 is entirely `flow135_g350`
   (−9,734 coins, 1916 rating) — drop it and r collapses. The three modern files span 156 rating
   points with 95 % CIs 200-340 points wide; the ladder-projection doc states outright that hr and
   g940_pair are **level** (implied strengths 2697/2705, overlapping CIs) and that **B − hr =
   −0.41 ± 0.47 logit on common support = indistinguishable**.
2. **The negative signs on LIVEC-H30/TOPB2 are an artefact of one file's ramp.** B has the best leg
   margins of any candidate ever judged (+903 TOPB2, +1031 H30B) and the lowest observed rating —
   but B has played 150 games *entirely inside the 2200-2400 pool*, where the LOSS10 counter class
   lives (44 % on its 2200-2300 slice vs 79 % at 2300-2400). B's low rating is a pool artefact,
   not a refutation of the legs.
3. **Rating is a lagging, low-K instrument.** From ~g80 the Kaggle K is 8.9
   (`S/calib2/kschedule.json`), so the rating drifts 8.9·(p − 0.5) ≈ +0.9 pts/game at hr's edge; a
   true +50 takes 70-140 games *after* the strength change. Ratings read before that are ramp
   lottery (±100 pts at fixed strength).

**What the data does support** is a direct, paired, same-boards test of whether a leg's verdict
transfers to the slot's own ladder pool. That is `S/hladder` (hr's own 60 ladder boards, opponents
2440-2682 — exactly the slot's band) and `S/bladder` (B's own 50, < 2100-2499):

| set | opponent bin | boards | B − hr margin | SE | t |
|---|---|---:|---:|---:|---:|
| hladder (hr's ladder pool) | 2400-2500 | 11 | +1,180 | 519 | +2.27 |
| hladder | 2500-2600 | 40 | +1,736 | 636 | +2.73 |
| hladder | 2600+ | 9 | +1,369 | 531 | +2.58 |
| **hladder all** | 2440-2682 | 60 | **+1,579** | 443 | **+3.56** |
| bladder (B's ladder pool) | < 2200 | 21 | +2,336 | 525 | +4.45 |
| bladder | 2200-2400 | 29 | +616 | 444 | +1.39 |
| **bladder all** | < 2500 | 50 | **+1,339** | 360 | **+3.72** |

The judge legs said B beats hr by +772 (H30) / +1,031 (H30B). On hr's own 60 ladder boards, in the
slot's own band, B beats hr by **+1,579 (t 3.6, flips +10/−2, sign p 0.039)**. **The band legs
reproduce the slot's own pool, same sign and same order of magnitude.** That is the strongest
leg→slot evidence available, and it is a within-contrast test, not a cross-file regression.

---

## 3. The Elo arithmetic

Calibration: P(win) = σ((c − opp)/**298**) (`docs/strategy/2026-09-10-rating-calibration-C.md`,
slope 298 pts/logit, CI 182-686); K = **8.9** from ~g80; matching band opp = me + 4.0 ± 43.8.
Because the band is centred on our own rating, the equilibrium rating **is** c (r* = c to within
3 pts), so *rating points and strength points are the same currency*.

| target | Δc | WR on hr's real last-100 pool | ΔWR | Δ per game at K = 8.9 |
|---|---:|---:|---:|---:|
| 2720 (hr today) | +0 | 60.2 % | — | +0.91 |
| 2770 | **+50** | 64.1 % | **+3.9 pp** | +1.25 |
| 2820 | **+100** | 67.8 % | **+7.6 pp** | +1.58 |
| 2920 | **+200** | 74.6 % | **+14.4 pp** | +2.19 |
| 2970 (top-10) | +250 | 77.6 % | +17.4 pp | +2.46 |

Sensitivity (against a rating-matched pool, where the +50/+100/+200 step is +4.2 / +8.3 / +16.2 pp
at s = 298): at s = 208 it is **+6.0 / +11.8 / +22.3 pp**, at s = 534 **+2.3 / +4.7 / +9.3 pp**.

### Margin → win rate → rating, measured per leg

Measured on `S/bandgrad/rows.csv` (20 records × every board, OLS of per-board Δwin-rate on
Δmargin). dp/dc at the matched pool = 0.25/298 = **0.0839 win-rate pp per rating point**.

| leg | boards | base-margin SD | Δmargin SD | pp per +1,000 coins | Δmargin for +50 rating | for +100 | SE of the leg mean | Δmargin at t = 2 | that in rating pts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| LIVE62 | 62 | 11,902 | 2,733 | 3.49 | 1,174 | 2,347 | 347 | 694 | +30 |
| LOSS10 | 10 | 2,019 | 1,735 | 4.05 | 1,013 | 2,026 | 549 | 1,097 | +54 |
| LIVEC-H30 | 30 | 8,130 | 1,874 | 3.59 | 1,143 | 2,286 | 342 | 684 | +30 |
| LIVEC-H30B | 30 | 7,899 | 2,227 | 5.26 | 780 | 1,560 | 407 | 813 | +52 |
| TOPB2 | 20 | 13,197 | 3,106 | 2.98 | 1,375 | 2,750 | 695 | 1,389 | +51 |

**Answer (iii): +50 rating = +3.9 pp win rate on the slot's own pool ≈ +1,000-1,200 coins of paired
margin on a band leg; +100 = +7.6 pp ≈ +2,000-2,300 coins; +200 = +14.4 pp ≈ +4,000-4,600 coins.**
Pooling the three band legs (LIVEC-H30 + LIVEC-H30B + NEXT30 = 90 boards) gives Δmargin SD ≈ 2,066,
SE ≈ 218, so **t = 2 lands at ±436 coins ≈ ±27 rating points**. That is the finest promotion step
the slot's own band can certify, and it is about half a "+50".

### What each leg is worth in rating points

A leg pays into the rating only in proportion to how often the slot meets that tier
(share computed from the measured band, opp = r + 4.0 ± 43.8):

| leg | tier | share of games at r = 2630 | at 2700 | at 2750 | at 2820 | rating pts per +1,000 coins at 2630 | at 2750 | at 2820 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| LIVE62 | 1827-2070 | 0 % | 0 % | 0 % | 0 % | +0 | +0 | +0 |
| LOSS10 | 2175-2381 | 0 % | 0 % | 0 % | 0 % | +0 | +0 | +0 |
| LIVEC-H30 | 2440-2615 | 33 % | 2 % | 0 % | 0 % | +14 | +0 | +0 |
| LIVEC-H30B | 2519-2682 | 86 % | 31 % | 5 % | 0 % | **+54** | +3 | +0 |
| NEXT30* | 2567-2750 | 93 % | 85 % | 46 % | 5 % | **+58** | **+29** | +3 |
| TOPB2 | 2953-3081 | 0.00 % | 0.00 % | 0.0 % | 0.2 % | +0 | +0 | +0 |

`*` NEXT30 has no `S/bandgrad` rows yet; its slope is borrowed from LIVEC-H30B (2519-2682).

**A −1,400-coin loss (the t = −2 resolution of a 20-board leg) costs the slot** −75 rating on
LIVEC-H30B and −82 on NEXT30 *today*, and **−0 on TOPB2 at any rating the slot will reach in the
next 200 games** (−7 only once we are at 2900). That asymmetry is the whole argument for the rule
below.

---

## 4. Recommended rule

> **HR-SLOT PROMOTION RULE.** A candidate replaces the hr file (sub 56143250) when, judged
> paired on real-engine boards against candidate B at both seats, it wins the **slot band** —
> LIVEC-H30 + LIVEC-H30B + NEXT30 pooled as one 90-board leg — with **pooled Δmargin ≥ +450 coins
> and pooled board-t ≥ +2.0**, with **net flips ≥ 0** on those 90 boards and **no single band leg
> worse than −400 coins**; and when neither **TOPB2** (20 top-ten boards, 2953-3081) nor
> **LIVE62** (62 boards, 1827-2070) is *significantly* worse — vetoed only at Δmargin ≤ −1,400
> (TOPB2) or ≤ −700 (LIVE62), i.e. t ≤ −2 on that leg, or at net flips ≤ −4 of 20 (TOPB2) /
> ≤ −8 of 62 (LIVE62). **LOSS10 and NEXT14 stay informational** (falsifiers, never selectors).
> TOPB2 and LIVE62 are **vetoes, not required wins**: a leg the slot never plays cannot be asked to
> improve, only to not collapse. The band bar rises with the claim — a candidate advertised as
> +100 rating must show **≥ +2,000 pooled coins**, not merely clear +450 — and any candidate whose
> pooled band gain comes with a TOPB2 loss between −700 and −1,400 (below veto, above noise) is
> promoted **only if** its pooled band Δmargin is ≥ +1,200, because it is buying the next 100
> rating points at the cost of the 100 after that.

### Why each number

| clause | number | justification |
|---|---|---|
| slot band = H30 + H30B + NEXT30 | 2440-2750 | covers 100 % of the slot's games at r = 2630 and 46 % at 2750; TOPB2/LIVE62/LOSS10 cover 0 % |
| pooled, not per-leg | 90 boards | per-leg t = 2 costs 684-813 coins (≈ +30-52 rating); pooled it costs 436 (≈ +27) — pooling is the only way to certify a step smaller than +50 |
| Δmargin ≥ +450, t ≥ +2 | ≈ +27 rating | the finest step the slot's own band resolves; anything smaller is not distinguishable from the board lottery |
| net flips ≥ 0, not > 0 | sign check only | the 42-board flip-count judge produced **zero true positives on 7 arms** (`docs/strategy/2026-09-09-judge-calibration.md`); flips are a no-regression check, margin is the instrument |
| no single band leg worse than −400 | −400 ≈ t −1 per leg | stops a pooled pass that is one leg winning and two losing (the §107/§114 tier-split failure mode) |
| TOPB2 veto at −1,400 | t = −2 at n = 20, SE 695 | the smallest TOPB2 loss that is not noise; costs the slot ≈ 0 rating today and −7 at 2900, so it is a *future* guard, not a price |
| LIVE62 veto at −700 | t = −2 at n = 62, SE 347 | LIVE62 is 550 pts below the slot; a real collapse there means a broken plan, not a tier trade |
| LOSS10/NEXT14 informational | 10/14 boards | LOSS10's t = 2 needs 1,097 coins (≈ +54 rating) on 10 boards; too coarse to select, fine to falsify |

### The risk this creates, quantified

The rule lets a band specialist through. How exposed is it?

| our rating | P(opp ≥ 2700) | P(opp ≥ 2800) | P(opp ≥ 2900) | P(opp ≥ 2953 = TOPB2) |
|---|---:|---:|---:|---:|
| 2628 (hr now) | 6.0 % | **0.0 %** | 0.00 % | 0.00 % |
| 2700 | 53.6 % | 1.4 % | 0.00 % | 0.00 % |
| **2750** | 89.1 % | **14.7 %** | 0.04 % | 0.00 % |
| 2800 | 99.1 % | 53.6 % | 1.4 % | 0.02 % |
| 2820 (= hr + 100) | 99.8 % | 71 % | 4 % | 0.2 % |
| 2850 | 100 % | 89.1 % | 14.7 % | 1.4 % |

Observed: **0 of hr's 205 games** were against ≥ 2800 (max 2721); by own-rating slice, hr met
≥ 2700 in 0 % of games below 2600 and 7.5 % of the 67 games at 2600-2700 — the fitted band
reproduces the data.

So the exposure is **zero now, 15 % at 2750, and 71 % at 2820**. A candidate promoted on the band
that is genuinely +100 will spend most of its games against 2800+ opponents *at its own
equilibrium* — which is exactly when a top-tier collapse starts costing rating. Hence: the veto
must hold, and it must tighten as the slot climbs. Concretely, **re-read this rule at r = 2750**:
above that, TOPB2 stops being a veto and becomes a required leg.

---

## 5. Caveats

1. **No leg covers 2750-2950.** NEXT30 tops out at 2750; TOPB2 starts at 2953. That gap is the
   entire remaining climb from the slot's current 2630 to a top-10 2967. At r = 2820 the slot's
   pool is 2824 ± 44 — a tier **no judge set contains**. The single highest-value judge build
   available is a **NEXT30-style pinned-town leg at 2800-2950** (same `S/nextband` pipeline,
   `pick.py` with the rating window moved); until it exists, every promotion above 2750 is
   extrapolating.
2. **NEXT30's margin-to-win slope is borrowed** from LIVEC-H30B. It has no `S/bandgrad` rows yet;
   the first candidate judged on it should be added to `S/bandgrad/rows.csv` so the slope is
   measured, not assumed.
3. **298 pts/logit has a wide CI (182-686).** Every "coins → rating" number above scales as 1/s:
   at s = 686 a +450 pooled gain is worth ~12 rating points, at s = 182 it is worth ~44. The
   *ranking* of the legs is insensitive to s (it is driven by the pool shares), the *absolute*
   rating translations are not.
4. **The cross-file regression is reported and rejected**, not used. Four points, one of them
   carrying all the leverage, CIs 200-340 pts wide, and the two best-measured files are formally
   level. The rule rests on (a) pool coverage, which is measured exactly, and (b) the
   `S/hladder`/`S/bladder` paired transfer test, which is a within-contrast measurement on the
   slot's own boards.
5. **§107/§114 remains live.** The flow209 step bought TOPTEN (+506) and LOSS10 (+597) and sold
   LIVEC42 (−344) and W2 (−216); the transfer doc shows the sign is decided by *which product the
   opponent liquidates through* and that **no observable covariate predicts it** (best of 40
   opponent-play features, Spearman +0.128, p 0.07 uncorrected). So a tier-split candidate cannot
   be reasoned about — only measured — and the veto is the only defence.
6. hr's per-game opponent ratings for games 135-205 come from the watcher's `opp~` field (rounded
   to integers); games 1-134 are exact from `S/calib2/games_56143250.csv`. 59 of hr's 264 episodes
   have no rating line in either source and are excluded.
