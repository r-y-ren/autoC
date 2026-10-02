# Judge calibration: does the 42-board pinned held-out flip count predict the drawn legs?

2026-09-09. Data-only study (no new simulations). Inputs: `S/lossflip/*.csv` (28 measured arms + the
live base `flow135_g350.csv`, one row per pinned-town game), `S/judge/*_legs/`, `S/f148pend/`,
`S/f149pend/`, `S/esf1*/`, `S/esg*/` (drawn-leg csvs), `S/ablation/out.txt`.
Scripts: `S/judgecal/{an2,stats,stats2,stats3,legs,legs2}.py`; per-board table `S/judgecal/boards.csv`.

**S** = `/tmp/claude-0/-mnt-e--work-kaggriculture3/8b388b22-9a4b-4bf0-8e3e-dc4aac1d5f04/scratchpad`.

## TL;DR

1. The held-out flip count is decided by **15 of the 42 boards** (30 of 84 games). Across all 24
   near-neighbour arms measured on the pinned set, **every single flip and every single drop lands
   inside that set** — the other 27 boards (54 games: 46 frozen losses, 8 frozen wins) never change
   hands for any arm. 100 % of the "+6" in flow156_g20, flow155_g50 and flow150_g40 comes from it.
2. Net flips has **sd 3.1 across the 24 arms** (mean +2.8, range 0…+12). "+6" is ~1 sd above the
   arm-to-arm mean: it is a draw from the lottery, not a signal.
3. Of the 7 arms that have both a pinned read and drawn legs, **all 7 lost the legs** (−2.7 to −9.1
   win pts pooled over 1,808 games). The current rule (net ≥ +6) fired on 4 of them; all 4 lost.
   The judge has **zero demonstrated true positives**.
4. The best-ordering statistic is *not* on the held-out 42 at all: it is the paired margin delta on
   the **20 pinned games played against the 10 tapes that also appear in the drawn legs**
   (Spearman ρ = 0.64…0.75 vs the leg outcome, against 0.36…0.50 for every held-out statistic).
   It is already in every lossflip csv — it costs nothing to compute.
5. Side finding on the legs themselves: only the **640–656-game legs** (top10, today41) rank close
   arms (ρ 0.83–0.85 vs the pooled read); band6 (192) and jesse4 (128) rank them at ρ 0.07–0.13.
   A "level on band6" read on a near-neighbour arm is worth nothing.
6. n = 7 arms. ρ = 0.75 at n = 7 is p ≈ 0.07. **The calibration is under-powered** and the honest
   recommendation is the cheap power-up in §4, not a hard promotion threshold.

## 1. The near-tie set

Perturbation scale of the margin on a pinned held-out game, measured across the 24 non-melon arms
(1,655 board×arm pairs where the margin actually moved):

| quantity | value |
|---|---|
| median \|Δ margin\| | 1,734 |
| mean \|Δ margin\| | 2,831 |
| p25 / p75 | 618 / 3,439 |
| sd of Δ margin (pooled) | 4,240 |
| median per-board sd | ≈ 2,400 |

A literal near-tie rule (|base margin| < 1,734) catches only 8 games / 4 boards — too narrow. The
operational definition that matters is **outcome-unstable**: boards whose win/loss is not constant
across the 24 arms. There are **15 such boards / 30 games**; the base margin on them runs from −642
to −12,708, i.e. |margin| alone does not identify them (a −6,142 board flips for 5 arms; a −4,102
board never flips).

Volatile games (base margin, share of the 24 arms that win it):

| board | seat 0 margin | seat 1 margin | arm win rate |
|---|---|---|---|
| 106722363 | −642 | −1,542 | 8 % / 4 % |
| 106459205 | +1,034 | +1,034 | 75 % |
| 106479420 | −1,104 | −1,065 | 42 % |
| 106815218 | −1,344 | −1,344 | 46 % |
| 106819049 | −2,137 | −2,137 | 42 % |
| 106558765 | +3,287 | +3,287 | 92 % |
| 106807583 | −4,399 | −4,399 | 4 % |
| 106670138 | +4,412 | +4,997 | 96 % |
| 105268279 | −4,504 | −4,504 | 4 % |
| 106832523 | −4,504 | −4,504 | 8 % |
| 106389749 | −5,187 | −5,187 | 4 % |
| 106606614 | +5,411 | +5,411 | 96 % |
| 106629051 | +5,613 | +5,613 | 96 % |
| 106933649 | −6,142 | −6,008 | 24 % |
| 106800430 | −12,708 | −6,575 | 8 % |

Structure of the 84-game judge:

| class | games | boards |
|---|---|---|
| frozen losses (no arm ever wins) | 46 | 23 |
| frozen wins (no arm ever loses) | 8 | 4 |
| volatile losses (flippable) | 20 | 10 |
| volatile wins (droppable) | 10 | 5 |

Also: **30 of the 42 boards give byte-identical margins in both seats**, so the "84 games" are
really ≈ 42–50 independent observations, and the decisive part is ~15 boards / ~10 flippable ones.

### Where the recent "+6" came from

| arm | held-out flips | of which volatile | drops | of which volatile | flipped boards |
|---|---|---|---|---|---|
| flow156_g20 | 6 | **6** | 0 | 0 | 106479420, 106815218, 106933649 |
| flow155_g50 | 6 | **6** | 0 | 0 | 106479420, 106722363, 106819049 |
| flow150_g40 | 8 | **8** | 2 | 2 | 106479420, 106722363, 106815218, 106819049, 106933649 |
| flow149_pend_g106 | 12 | **12** | 0 | 0 | 105268279, 106479420, 106807583, 106815218, 106819049, 106933649 |
| flow148_pend_g150 | 8 | **8** | 2 | 2 | 106800430, 106815218, 106819049, 106832523 |
| flow130_g260 | 6 | **6** | 2 | 2 | 106389749, 106479420, 106815218 |
| flow135_g200 | 4 | **4** | 2 | 2 | 106479420, 106815218 |
| cdrop (knob) | 4 | **4** | 0 | 0 | 106815218, 106819049 |

**100 %** of every arm's flips and drops. Nine or ten boards produce the entire signal, and each
board is worth 2 flips because both seats move together. Net flips across the 24 non-melon arms:
values `0×10, 2×4, 4×4, 6×4, 7, 12` — mean +2.8, **sd 3.1**. A "+6" is +1.0 sd.

(The block ablation in `S/ablation/out.txt` is the same story from the other side: both halves of
flow155_g50 give +4, both halves of flow150_g40 give +4/+2 — the halves are indistinguishable
because they are all sampling the same 10 coins.)

## 2. Candidate statistics vs the drawn legs

Seven arms have both a pinned read (`S/lossflip/<arm>.csv`) and drawn legs paired against the g350
refs in `S/esf135c`. Leg outcome = pooled over the five legs common to every era
(band6@777001 192, top10@777001 640, band6@777002 192, jesse4@777001 128, today41@777001 656;
n = 1,808; flood6 excluded, its opponent count changed from 96 to 192 games).
flow156_g20's today41 leg is missing, so its pooled read is over 4 legs / 1,152 games.

Held-out statistics (paired vs g350 on the 76–84 common held-out games):
`net` = flips − drops; `dm` = mean paired Δ margin; `clip5` = same, each game clipped to ±5,000;
`dm_nv` = Δ margin on non-volatile games only; `ew` = expected-win delta, Σ[σ(m_c/s) − σ(m_b/s)] with
s = 8,000; `sign` = mean sign(Δ margin) with |Δ| < 1,734 trimmed to 0.
`LEG_*` = the same statistics computed on the **20 pinned games (10 tapes × 2 seats) whose opponent
tape also appears in a drawn leg**: 105228357, 105232167 (top10), 105268279, 105269242 (jesse4),
105400600, 105441481, 105441843, 105442685, 105443859, 105592028 (band6). `ALL_*` = the full pinned
set (232 common games).

| arm | leg ΔWin | leg ΔMargin | H_net | H_dm | H_clip5 | H_ew | LEG_net | LEG_dm | LEG_clip5 | ALL_net | ALL_dm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| flow149_pend_g106 | −2.7 | −165 | +12 | +764 | +627 | +2.5 | +2 | **+523** | +581 | +19 | +317 |
| flow156_g20 | −5.7 | −2,716 | +6 | −181 | −363 | −0.2 | 0 | −1,243 | −787 | +2 | −386 |
| flow135_g200 | −6.9 | −884 | +2 | −552 | −701 | −1.6 | 0 | −509 | −305 | −7 | −679 |
| flow155_g50 | −7.0 | −2,176 | +6 | −1,127 | −938 | −2.4 | 0 | −2,405 | −1,172 | +5 | −784 |
| flow148_pend_g150 | −7.9 | −1,148 | +6 | +963 | +190 | +2.5 | 0 | −762 | −396 | +19 | +2,209 |
| flow150_g40 | −8.6 | −2,550 | +6 | −310 | −313 | −0.7 | 0 | −1,712 | −986 | +8 | −296 |
| flow130_g260 | −9.1 | −2,322 | +4 | −815 | −1,149 | −1.9 | 0 | −2,226 | −1,599 | −14 | −1,495 |

Spearman ρ over these 7 arms:

| statistic | ρ vs leg ΔWin | ρ vs leg ΔMargin |
|---|---|---|
| H_net (**the current judge**) | 0.45 | 0.12 |
| H_dm | 0.36 | 0.21 |
| H_dm on non-volatile boards | 0.32 | 0.29 |
| H_dm on volatile boards | 0.43 | 0.36 |
| H_clip5 | 0.46 | 0.36 |
| H_sign (trimmed) | 0.43 | 0.29 |
| H_ew (logistic, s = 2,000 / 4,240 / 8,000) | 0.32 / 0.36 / 0.50 | 0.11 / 0.18 / 0.29 |
| H win rate | 0.04 | 0.33 |
| **LEG_dm (20 games)** | **0.64** | **0.64** |
| **LEG_clip5 / LEG_dm_nv** | **0.75** | **0.68** |
| LEG_net / LEG_dwin | 0.61 | 0.61 |
| LEG_ew | 0.64 | 0.64 |
| ALL_net / ALL_dm / ALL_clip5 | 0.29 / 0.32 / 0.43 | 0.36 / 0.29 / 0.18 |

Readings:

* Every held-out statistic sits at ρ ≈ 0.3–0.5 — indistinguishable from noise at n = 7
  (the 5 % critical value for n = 7 is 0.786).
* Making the held-out statistic *smoother* helps a little (clip5 0.46, logistic-8k 0.50 vs net 0.45)
  and restricting it to non-volatile boards **hurts** (0.32) — because the non-volatile boards carry
  no outcome information at all (net_nonvol is exactly 0 for all 24 arms; only the margin moves).
* Playing more pinned tapes (ALL, 232 games) does **not** help (0.29–0.43): the extra tapes are
  training-rung tapes, and the arms that gain most there (flow148_pend_g150: ALL_dm +2,209,
  ALL_net +19) are among the worst on the drawn legs.
* The one thing that orders the arms is **who they are playing**: 20 pinned games against the exact
  tapes the legs use beat 84 held-out games against tapes the legs never use.

## 3. Recommended judge rule

**Primary gate (new): `LEG_dm > 0`** — the paired Δ margin over the 20 pinned games against the ten
leg-family tapes must not be negative. **Secondary: `H_dm ≥ 0`** (held-out paired Δ margin not down)
and **`H_net ≥ +6`** kept only as a *cheap screen for something to look at*, never as evidence.

Behaviour on the 7 calibration arms (the only arms where both reads exist):

| rule | passes | outcome of the passers |
|---|---|---|
| current: H_net ≥ +6 | 149_pend_g106, 156_g20, 155_g50, 150_g40, 148_pend_g150 | 4 of 5 lost the legs by 5.7–8.6 pts |
| H_net ≥ +6 **and** H_dm ≥ 0 | 149_pend_g106, 148_pend_g150 | 1 of 2 lost by 7.9 pts |
| **LEG_dm > 0** | 149_pend_g106 | the only arm whose legs were level (−2.7 pts, pooled t −0.49) |
| LEG_dm > 0 **and** H_net ≥ +6 | 149_pend_g106 | same |

So the proposed rule turns 4 false promotions into 0 on the arms we have, at the cost of also
rejecting nothing we know to have been good (there is nothing known to have been good).

### Honest power statement

* **7 arms.** All 7 lost the drawn legs; the calibration therefore contains **no positive control**.
  Everything above is discrimination *within losers*, which is the harder half of the problem but
  not the half that promotion actually needs.
* ρ = 0.75 at n = 7 has p ≈ 0.07 two-sided. Three arms swapping rank would erase it.
* LEG_dm rests on **20 games / 10 tapes / 1 board each**. Its per-arm noise is not measured. It is
  plausible that it works because it is literally the leg opponents, and plausible that it is a
  10-coin lottery of its own. Treat it as the best available ordering, not as a validated gate.
* Nothing here says the drawn legs are the right target either — they are drawn-board, open-loop
  tapes, which the tape-fidelity note (2026-09-11 memory) says overstate us against the 2100 band.

### Cheapest way to power it (recommended, in order)

1. **Re-use the 13 existing full leg sets that have no pinned read.** These arms already have all
   five legs on disk paired against the same g350 refs — the expensive half (1,808 games each) is
   already paid for. Their leg outcomes vs g350 span **−18.8 to −1.2 win pts**, i.e. 17 points of
   spread versus the 6.4 points the current 7 arms span, and two of them are *positive on margin*
   (the closest thing to a positive control available):

   | arm (theta on disk) | leg ΔWin | leg ΔMargin | t |
   |---|---|---|---|
   | esg100/best_sim_now | −18.8 | −5,859 | −15.8 |
   | esf130/cand_g40 | −18.7 | −5,297 | −13.1 |
   | esg100/cand_g100 | −17.4 | −5,342 | −13.2 |
   | esg180/cand_g180 | −16.5 | −5,007 | −14.3 |
   | esf130b/cand_g130 | −12.4 | −3,298 | −8.5 |
   | esf134/cand_g40 | −8.1 | −2,279 | −6.1 |
   | esf135/cand_g40 | −7.9 | −1,619 | −3.9 |
   | esf133/cand_g100 | −7.2 | −1,799 | −4.6 |
   | esf138/cand_g10 | −4.4 | −247 | −0.7 |
   | esf137/cand_g10 | −3.7 | −436 | −1.4 |
   | esf141/cand_g40 | −3.3 | −352 | −1.2 |
   | esf138b/cand_g100 | −1.5 | **+553** | +1.8 |
   | esf138c/cand_g200 | −1.2 | **+458** | +1.5 |

   Cost: one `S/lossflip/run.sh`-style pinned run per arm (1 seed × ~160 tapes × 2 seats ≈ 320
   games, ~15–20 min, parallelisable), pointing `--theta` at the npy already sitting in each dir.
   That takes the calibration from **7 arms to 20** and gives it a real dynamic range. This is the
   single highest-value action in this note.
2. **Only then** re-fit the rule. With 20 arms, ρ = 0.45 (n = 20) is significant at p < 0.05, so the
   held-out statistics get a fair test too, and the LEG_dm threshold can be set on a real curve
   instead of on one passing arm.
3. If only ONE leg can be afforded per candidate, it must be a **big** one: `today41@777001`
   (656 games) or `top10@777001` (640 games). Measured against the 1,808-game pooled read:

   | single leg | games | ρ vs pooled, 7 near arms | ρ vs pooled, 20 arms |
   |---|---|---|---|
   | today41@777001 | 656 | **0.83** | **0.95** |
   | top10@777001 | 640 | **0.85** | 0.88 |
   | band6@777002 | 192 | 0.57 | 0.82 |
   | band6@777001 | 192 | 0.13 | 0.78 |
   | jesse4@777001 | 128 | 0.07 | 0.78 |
   | band6@777001 + jesse4@777001 | 320 | 0.07 | 0.84 |

   The small legs are a ±5-pt lottery of their own: per-arm spread across the five legs is 4.2–13.1
   win pts (flow148_pend_g150: band6 −13.5, band6@777002 −5.7, jesse4 −18.8, top10 −5.6). Any
   "level on band6" or "level on jesse4" claim on a near-neighbour arm is worth nothing; only the
   640–656-game legs (or the pooled read) rank close arms. jesse4 remains useful as a *veto*
   (largest |t| on 6 of 7 losing arms) but not as a ranking.
4. Do **not** spend on more pinned tapes for the held-out judge: the ALL-set statistics are no better
   than the 42-board ones (ρ 0.29–0.43), because the added tapes are training rungs.

## 4. Secondary observations

* `sellcad_off` reproduces the base exactly (Δ margin 0 on all 84 games) — a useful null control
  showing the pinned harness is deterministic; the "lottery" here is board selection, not run noise.
* `em8`, `em10`, `emherd` give byte-identical held-out reads (Δ margin −1,684 each) — the three knobs
  are the same change on this board set; don't count them as three arms.
* The melon family (melon4/6/8/12) is the only family that moves the frozen boards
  (net_nonvol −2 to −7, Δ margin −10.6k to −21.7k) — confirming the frozen set is not literally
  immovable, only immovable under near-neighbour thetas. It is a valid catastrophe detector and
  should stay in the judge as a floor check.

## 5. Wired into the local judge (2026-09-09)

* **`S/lossflip/leg_family.py`** (new) — the ten pinned tapes that the drawn legs also play, listed
  explicitly with their provenance (band6 6, top10 2, jesse4 2; no today41/flood6 tape is pinned).
  All ten verified present in `artifacts/panel_opp_town/`.
* **`S/lossflip/flips.py`** — unchanged outputs plus one appended line per arm:
  `LEG20: d-margin <x> (n=20 games vs leg-family tapes) | H_dm <y> | H_net <+f/-d>`.
  Verified against this document's numbers:

  ```
  flow156_g20        LEG20: d-margin -1243 (n=20 games vs leg-family tapes) | H_dm  -181 | H_net  +6
  flow149_pend_g106  LEG20: d-margin  +523 (n=20 games vs leg-family tapes) | H_dm  +764 | H_net +12
  flow155_g50        LEG20: d-margin -2404 ... | H_dm -1127 | H_net  +6
  flow150_g40        LEG20: d-margin -1712 ... | H_dm  -310 | H_net  +6
  flow148_pend_g150  LEG20: d-margin  -762 ... | H_dm  +963 | H_net  +6
  flow135_g200       LEG20: d-margin  -508 ... | H_dm  -552 | H_net  +2
  flow130_g260       LEG20: d-margin -2226 ... | H_dm  -815 | H_net  +4
  ```
* **`S/judge/judge.sh`** — the drawn legs now run iff `LEG20 d-margin > 0` **and** `H_dm >= 0`.
  `held-out net flips: N` is still printed (old monitors keep parsing it) and a new
  `gate: ...` line records all three numbers, but H_net no longer gates anything. The skip line
  keeps its `LEGS SKIPPED (...)` prefix. Dry-run: flow156_g20 -> LEGS SKIPPED,
  flow149_pend_g106 -> LEGS RUN.
* **`S/lossflip/run.sh`** — gained an optional third argument (explicit theta path) so calibration
  thetas that do not live in `artifacts/kagg2_games/thetas/` can be replayed without writing into
  the repo. Default behaviour unchanged.
* **`S/judgecal/chain.sh`** (launched detached, PID 36785) — waits for `PLANTFILLDONE`, then runs
  the pinned read serially (`--workers 10`) for the 13 arms in §3, appending each arm's LEG20 and
  HELD-OUT lines to `S/judgecal/chain_summary.txt`, then re-runs `S/judgecal/spear_all.py` (the
  n≈20 Spearman table + the gate check) and appends `JUDGECALDONE`. All 13 thetas are 4980 params
  -> worktree `agent-a85c50163fb5dcbb7`.
