# An objective that tracks P(win vs kagg2)

**Status: DESIGN + MEASUREMENT. No training code changed here.** Section 1 is a new
experiment (30 checkpoints × in-sim fitness × 720 real-engine games vs `kagg2`);
sections 2–3 are a proposal. `es/archetypes.py`, `core/brain.py` and `core/policy.py`
are being merged by another agent and are not touched by this document.

Reads on: `docs/superpowers/plans/2026-08-26-kagg3-vs-kagg2-diagnosis.md` (the 48-game
gap attribution) and `2026-08-26-work-idle-tiles.md` §6 (the planner-side version of the
same divergence).

---

## 0. The claim

The fitness is `0.6·rank(mean log1p(own coins)) + 0.4·rank(mean sigmoid(margin/100k))`
over a pool of self-play rungs plus 8 archetypes. Measured across 30 checkpoints, **its
two terms rank policies identically** (Spearman **+0.973**, and +0.965 over the 16
non-degenerate ones). They have to: every rung is beaten in essentially every game, so the
opponent's coins sit at their floor and the margin is a monotone transform of own coins.
The hardest rung, `mixed_ranch`, loses **128 of 128** games to 11 of those 16 checkpoints
and at least 94 % to 15 of them, by **+16.5k … +57.0k**. kagg2 wins **24 of 24** by
**−49.0k**. The objective has no observations anywhere near the region it is meant to
predict — it measures the size of a
win it always gets, not the probability of a win it never gets.

Re-weighting the two terms cannot fix that, because they are the same number. Nor is the
problem a broken ranking: measured against the real kagg2 margin, **today's `abs_coins` is
the best single predictor there is** (ρ = +0.93 over 30 checkpoints, +0.73 over the top
10). It is the best predictor *of a quantity that is 49k from the decision boundary*, and
the run has already left the range where it works — over the tracker's seven comparable
rows, own coins correlate **+0.32** with the margin and **+0.79** with *kagg2's* coins.
The two farms scale together.

What the ladder needs is an opponent it *loses* to. `mixed_ranch` played from an opening
of **3 quadrants and 20,000 coins** is one: it holds `p2s0/champion` to **70.0k** while
earning **100.8k** (kagg2: 62.0k / 111.0k) and reproduces **81 %** of kagg2's suppression
against today's rung's 20 %. Controlling for coins, it is the **only** measured sim
quantity that adds information about the real margin — the win rate against it scores a
partial ρ of **+0.42** over the top 10, where the ladder's margin against `mixed_ranch`
scores **−0.63**. Section 3 specifies it; every flag defaults to today's behaviour, and
§3.9 stages the rollout because n = 10 cannot tune a weight.

| | today | proposed (§3) |
|---|---|---|
| gradient | `0.6·rank(mean log1p(own)) + 0.4·rank(mean sigmoid(margin/100k))`; 8 rungs at an equal share, `mixed_ranch` = 6.25 % of episodes | `0.3 / 0.7` at **τ = 25k**; 9 rungs weighted, `kagg2_proxy` **12.5 %**, the kagg2-shaped pair **21.9 %** |
| selection (`best_abs.npy`, `--promote`) | most own coins against the rungs | best weighted score, **subject to** own coins ≥ 80,000 |
| yardstick holdout | seeds only — and it shows nothing (ρ = +0.998 with the selection half) | seeds **and** two held-out opponents |
| tracker (every 2 h) | 16 games; per-game CSV deleted by the `EXIT` trap | 48 games; CSV kept for `paired_ci.py`; margin CI, Wilson win CI, `coins_vs_starter` as the anti-denial gate |

---

## 1. Why in-sim fitness and the real kagg2 margin diverge

### 1.1 What was run

| | |
|---|---|
| Checkpoints | **30** — 20 archived (`p2s0` ×6, `arch1.remote` ×5, `work1/measured` ×5, `run3`/`theta.npy`, `theta_gen30`, `land1`, `shape1`) + 10 in the ES neighbourhood of `p2s0/champion` (8 isotropic perturbations at σ 0.04 / 0.10 on the live mask, 2 midpoints) |
| Layout | every array zero-padded to `PO.N_PARAMS = 4,518` by `train.py::_fit_layout`'s rule (3,892 / 4,287 / 4,386 → 4,518) |
| (a) fitness block | the exact mixture `Trainer.generation` builds: 32 seed pairs × 2 seats = 64 episodes, `opponent_slots(32, pool 4, arch 8, arch_frac 0.5)`, `draw_starts` warm starts, `p2s0/pool.npy` as the self-play pool, the checkpoint itself in the non-archetype rotation. CRN across all 30. |
| (b) yardstick block | `absolute_report`'s own measurement: 8 named archetypes × 64 fixed `abs` seed pairs × 2 seats = 1,024 games each, cold start, default market |
| (c) real engine | `kaggle_environments`, CPU, **12 seeds × 2 seats = 24 games** per checkpoint vs `../kaggriculture2/main.py`, seed base **20260825** (the tracker's), `ProcessPoolExecutor(max_tasks_per_child=1)` |
| (d) proxy block | five candidate kagg2-proxy rungs (§3.3), the same 64 fixed seed pairs × 2 seats = 128 games each |
| Total | 30 × 24 = **720 real-engine games**, 30 × 1,728 = **51,840 in-sim rollouts** |

The set splits cleanly in two, and the split is not a judgement call: **14 checkpoints
earn 4.4k–12.6k** against the archetype yardstick and **16 earn 51k–120k**, with nothing
in between. The 14 are the pre-Phase-2 lineages (`arch1`, `work1`, `run3`, `land1`,
`shape1`, `theta_gen30`) — they decode against a planner they were never trained on, and
the diagnosis's own local survey found the same thing (`arch1.remote/best_abs` 8.3k vs
`starter`). Three of them (`arch1_best_abs`, `arch1_pool3`, `arch1_pool6`) return
**byte-identical** real-engine results — 4,225 own, 163,991 to kagg2 on all 24 games —
which is what "different weights, same collapsed behaviour" looks like.

Every correlation below is reported on all 30, on the 16, and on the top 10,
because the three answer different questions: "does the sim notice a broken policy",
"does it order working policies", and "does it order the policies a run actually chooses
between".

Per-checkpoint numbers for the 16 (sorted by real margin; ±SE is over the 24 games):

| checkpoint | real own | kagg2 | **real margin** | ±SE | real win | sim `abs` | sim margin vs `mixed_ranch` | sim margin vs the proxy | today's fitness (rank blend) |
|---|---|---|---|---|---|---|---|---|---|
| `p2s0_champion` | 62,046 | 111,035 | **−48,988** | 2,895 | 0.00 | 118,935 | +56,628 | −30,730 | 0.893 |
| `perturb_s04_1` | 58,799 | 110,855 | **−52,056** | 2,191 | 0.00 | 113,728 | +48,979 | −25,323 | 0.747 |
| `p2s0_theta` | 75,207 | 127,783 | **−52,575** | 2,282 | 0.00 | 119,593 | +56,800 | −23,870 | **1.000** |
| `p2s0_pool3` | 73,277 | 126,310 | **−53,032** | 5,135 | 0.04 | 113,278 | +49,585 | −24,150 | 0.560 |
| `mix_champ_theta` | 69,251 | 122,310 | **−53,058** | 2,461 | 0.00 | 116,403 | +54,964 | −29,173 | 0.907 |
| `perturb_s04_3` | 67,572 | 124,838 | **−57,266** | 2,181 | 0.00 | 118,564 | +57,002 | −33,149 | 0.760 |
| `mix_champ_pool3` | 69,990 | 129,984 | **−59,994** | 2,683 | 0.00 | 114,391 | +54,379 | −20,719 | 0.653 |
| `perturb_s04_2` | 71,655 | 133,931 | **−62,276** | 4,078 | 0.00 | 111,469 | +49,666 | −21,473 | 0.493 |
| `perturb_s10_2` | 67,611 | 131,416 | **−63,805** | 2,148 | 0.00 | 108,028 | +38,726 | −51,818 | 0.587 |
| `perturb_s10_0` | 59,124 | 127,390 | **−68,266** | 4,101 | 0.00 | 98,007 | +16,549 | −24,889 | 0.160 |
| `perturb_s10_1` | 51,785 | 120,159 | **−68,374** | 4,673 | 0.00 | 106,614 | +47,031 | −41,637 | 0.400 |
| `perturb_s04_0` | 63,980 | 141,995 | **−78,016** | 3,865 | 0.00 | 97,099 | +33,974 | −19,959 | 0.333 |
| `p2s0_pool2` | 44,205 | 134,229 | **−90,024** | 3,449 | 0.00 | 89,284 | +19,129 | −36,695 | 0.173 |
| `p2s0_best_abs` | 46,454 | 136,512 | **−90,057** | 2,514 | 0.00 | 95,015 | +29,666 | −34,627 | 0.267 |
| `perturb_s10_3` | 45,219 | 135,982 | **−90,762** | 4,196 | 0.00 | 90,769 | +26,506 | −38,251 | 0.067 |
| `p2s0_pool0` | 34,193 | 141,499 | **−107,306** | 3,776 | 0.00 | 51,023 | −14,070 | −74,417 | 0.000 |

Two things are visible before any statistic. **Own coins and the margin disagree at the
top**: `p2s0/theta` earns **75,207** — the most of any checkpoint — and its margin is
3,587 *worse* than `p2s0/champion`'s, because kagg2 took 127,783 against it and 111,035
against the champion. And **the run's own promotion rule picks the wrong one of the two**:
`p2s0/theta` scores 1.000 on today's fitness blend and `p2s0/champion` 0.893, while the
real margin ranks them the other way. `p2s0/best_abs` — what `--promote` and the tracker
actually ship — is fourteenth of sixteen at **−90,057**, because it was frozen at
generation 73 of a 75-generation smoke run; that is a property of this local run, not of
the rule.

Also note **1 of 384 games was a win** (`p2s0/pool3`, 1/24). The real matchup is not near
a decision boundary anywhere in this set.

### 1.2 Rank correlations

Spearman ρ against the **real-engine margin vs kagg2**. Null band at p = 0.05 two-tailed:
|ρ| > 0.362 (n = 30), 0.503 (n = 16), 0.648 (n = 10) — read the columns accordingly, and
read the *pattern* rather than any single cell.

| sim quantity | all (n=30) | non-degenerate (n=16) | top-10 by `abs` (n=10) |
|---|---|---|---|
| **`abs_coins` — today's selection rule** | **+0.926** | **+0.924** | **+0.733** |
| `abs_holdout` | +0.921 | +0.888 | +0.588 |
| fitness anchor, `mean log1p(own)` vs the pool | +0.919 | +0.897 | +0.709 |
| fitness margin term, `mean sigmoid(margin/100k)` | +0.920 | +0.915 | **+0.745** |
| today's 0.6/0.4 rank blend | +0.908 | +0.891 | +0.685 |
| sim margin vs `mixed_ranch` | +0.874 | +0.818 | +0.479 |
| sim win vs `mixed_ranch` (= `abs` win rate) | +0.893 | +0.608 | +0.406 |
| denial: −(opponent coins vs `mixed_ranch`) | +0.768 | +0.482 | +0.042 |
| sim margin vs the calibrated proxy | +0.867 | +0.468 | +0.248 |
| **sim win vs the calibrated proxy** | +0.719 | +0.456 | **+0.554** |
| sim own coins vs the calibrated proxy | +0.878 | +0.529 | +0.430 |

**Which sim quantity best predicts the real kagg2 margin? `abs_coins` — the rule already
in use.** +0.926 over all 30, +0.924 over the 16 working checkpoints, +0.733 over the top
10. The margin term is its equal (+0.745 at the top). That is not a vindication of the
objective; it is a statement about the *range*. Every checkpoint here loses by
49k–107k, so "closer to winning" and "stronger" are the same ordering, and coins measure
strength on 1,024 games where the real margin is measured on 24.

The question that separates them is: **what does a quantity add beyond coins?** Partial
Spearman against the real margin with rank(`abs_coins`) removed from both sides:

| sim quantity | all | non-degenerate | top-10 |
|---|---|---|---|
| sim margin vs `mixed_ranch` | −0.247 | −0.463 | **−0.628** |
| denial: −(opponent coins vs `mixed_ranch`) | −0.041 | −0.563 | −0.556 |
| `abs_holdout` | −0.130 | −0.331 | −0.433 |
| uniform τ = 25k score over the 8 rungs, no proxy | −0.012 | −0.347 | −0.387 |
| today's 0.6/0.4 rank blend | −0.016 | +0.074 | +0.050 |
| sim margin vs the calibrated proxy | +0.377 | +0.152 | +0.087 |
| sim own coins vs the calibrated proxy | +0.441 | +0.242 | +0.239 |
| **sim win vs the calibrated proxy** | +0.267 | +0.294 | **+0.424** |

Three readings, and the third is the one that decides §3:

1. **Every quantity the current objective already contains adds nothing, or subtracts.**
   The ladder's margin against `mixed_ranch` is the worst of them: it is +0.903 collinear
   with `abs_coins` over the top 10 (+0.968 over all 30) and its residual points the
   *wrong way*, −0.628. The 0.4 weight on the margin term is buying noise.
2. **The only quantities with positive residual information are the ones measured against
   a rung that beats us.** `win vs the calibrated proxy` is the best of them, +0.424 at
   the top and +0.554 raw — and it is exactly `GOAL.md`'s `W`. Against the current ladder
   the win bit is a constant 1.00 and carries nothing; against a rung that wins 90–100 %
   of its games it varies again (over the top 10: **0.000, 0.000, 0.000, 0.016, 0.023,
   0.055, 0.086, 0.094, 0.094, 0.102** on 128 games each) and starts predicting.
3. **The proxy is a genuinely different ranking.** Spearman(`abs_coins`, proxy margin) is
   +0.857 / +0.450 / **+0.261** across the three subsets, against +0.968 / +0.947 /
   **+0.903** for `abs_coins` vs the `mixed_ranch` margin. Today's ladder measures the
   same thing twice; the proxy measures something else.

**And the honest limit of this experiment.** It cannot see the regime the campaign is
actually in. Every checkpoint here is 49k or more from a win. The tracker's real lineages
sit at 59–92k own coins vs kagg2, where coins and margin come apart: over its seven
comparable rows, Spearman(own coins, margin) is **+0.32** while Spearman(own coins,
kagg2's coins) is **+0.79** — the two farms scale together. `esfix1` bought +25.4k of own
coins over ~6,000 generations and gave back 10.1k of margin, because kagg2 gained 35.5k
in the same window. Coins predict the margin *until the market saturates*, and the run is
past that point. That, not a broken rank ordering, is why the objective has to change.

### 1.3 The mechanism — four measurements

**(a) The two fitness terms are one measurement.** Spearman between the absolute anchor
`mean_e log1p(own)` and the relative term `mean_e sigmoid(margin/100k)`, over the same
episode set:

| subset | ρ(anchor, margin term) | ρ(`abs_coins`, `abs_margin`) |
|---|---|---|
| all 30 checkpoints | **+0.973** | +0.995 |
| 16 non-degenerate | **+0.965** | +0.997 |
| top 10 by `abs` | +0.867 | +0.988 |

The 0.6/0.4 blend is a blend of a number with itself. It has to be: for a fixed rung the
opponent's coins barely move across checkpoints while ours move a lot. Against
`mixed_ranch` over the 16 non-degenerate checkpoints, **`theirs` spans 54.1k–70.4k
(a 16.3k range) while `mine` spans 52.4k–112.8k (60.4k)** — so `margin ≈ own − const`,
and the sigmoid is a monotone transform of own coins.

**(b) The win bit is saturated at the top of the ladder.** Of the 16 non-degenerate
checkpoints, 15 have `abs_win_sel` in **0.99–1.00** across all 8 rungs (1,024 games each);
**11 beat `mixed_ranch` — the kagg2-shaped rung, the hardest one — in 128 of 128 games**,
and 15 of 16 beat it at least 94 % of the time. Their margin against it spans
**+16.5k … +57.0k** (the sixteenth, `p2s0/pool0`, is the warm-started init at −14.1k).
The real game is **−49.0k at 0/24**. Nothing in the objective's range overlaps the region
it is supposed to predict.

**(c) The ladder's hardest rung is half of kagg2.** Own and opponent coins for
`p2s0/champion`, in-sim against every rung (128 games each) and in the real engine:

| opponent | its coins | our coins | margin | our win | suppression |
|---|---|---|---|---|---|
| `staple_bulk` | **838** | 126,718 | +125,880 | 1.00 | 0 |
| `rusher` | 10,043 | 117,949 | +107,906 | 1.00 | 8,769 |
| `expander` | 16,306 | 114,819 | +98,513 | 1.00 | 11,899 |
| `patient_grower` | 22,356 | 119,617 | +97,261 | 1.00 | 7,101 |
| `squeeze_seller` | 22,509 | 117,609 | +95,100 | 1.00 | 9,110 |
| `rancher` | 22,527 | 119,828 | +97,301 | 1.00 | 6,890 |
| `value_farmer` | 38,984 | 121,501 | +82,517 | 1.00 | 5,217 |
| **`mixed_ranch`** | **56,078** | 112,706 | **+56,628** | 1.00 | **14,012** |
| **`kagg2`, real engine (24 games)** | **111,035** | **62,046** | **−48,989** | **0.00** | **70,165** |

kagg2 earns **1.98×** the top rung and holds us to **0.55×** what the top rung does.
Suppression is measured against the least-suppressive opponent available on each side
(in-sim `staple_bulk`, 126,718; real `starter`, 132,211 from the diagnosis), so the last
column is comparable across the line: `mixed_ranch` reproduces **14,012 / 70,165 = 20 %**
of what kagg2 does to us.

It is not a collapsibility problem — `mixed_ranch` keeps **0.76** of its unopposed income
when a strong policy is on the board (73,841 → 56,078), against kagg2's **0.65**
(170,553 → 111,035). It is a **level** problem: the rung has the right shape and half the
size.

**(d) It is not seed overfitting.** `abs_holdout` — the half of the fixed seed set nothing
selects on — tracks `abs_coins_sel` to a **mean 1.1 % and worst 4.0 %** across all 30
checkpoints (ρ = +0.998). The existing holdout is working perfectly and is answering a
question nobody is asking. The missing holdout is on *opponents*.

**Side finding, actionable now:** `staple_bulk` earns **17,560 coins against the zero
theta** — comfortably over `AR.MIN_COINS = 10,000` — and **838 against `p2s0/champion`**,
i.e. it keeps **4.8 %**. The liveness probe measures it against an opponent it never
faces. It is currently 1/8 of the yardstick and contributes the single largest own-coin
term in it (126,718). See §3.3 for the second floor this needs.

---

## 2. Candidate objectives

All five are stated as changes to `shaped_advantage` / `absolute_report` / the
`--promote` rule. "Collapse" below means the two failure modes this codebase has
already met: the **liveness floor** (`AR.MIN_COINS = 10,000` — a rung that earns nothing
silently rescales the yardstick) and **archetype exploitation** (a fixed rung is a fixed
supply curve; a policy can learn its book rather than a strategy).

### A. Weight the margin against the hardest rung up

`opponent_slots` gives every archetype an equal share, so `mixed_ranch` — the only
kagg2-shaped rung — carries **2 of 32 seed pairs (4 of 64 episodes, 6.25 %)** in the
gradient and **1/8 of the mean** in the yardstick. Candidate A raises both: a weighted
round-robin over the rungs (`--rung-weight NAME=W`), and `abs_weight` 0.6 → 0.3.

* **Expected effect: small on its own.** Re-weighting inside a set of rungs that every
  non-degenerate checkpoint beats 100 % of the time redistributes weight *among wins*; it
  cannot manufacture a loss to learn from. Spearman(`abs_coins`, `margin_mixed_ranch`)
  is **+0.947** over the 16 non-degenerate checkpoints, so tripling `mixed_ranch`'s share
  moves the ranking by almost nothing. Concretely: the τ = 25k score over the 8 rungs at
  uniform weight is **0.903–0.972** across all 15 strong checkpoints — a 0.07 spread in a
  quantity bounded by 1.
* **Collapse risk: low, exploitation risk: moderate.** Concentrating episodes on one
  fixed theta is exactly the setting archetype exploitation lives in; the rung's supply
  curve is deterministic, and 4 → 12 episodes a generation is 3× more signal to fit it
  with. Mitigation is a *held-out* rung (§3.3), which does not exist today — the current
  holdout is on **seeds**, not on opponents.
* **Promotion: unchanged** (`best_abs` still coins) — which is precisely the problem A
  does not fix.

### B. An explicit denial term

`fitness += w_den · rank(−mean_e log1p(opponent coins))`.

* **Expected effect: redundant, and mis-priced.** The margin term already differentiates
  the opponent's coins with coefficient exactly −1, and that **is** the tournament's rule:
  only the sign of the margin scores. The **1.5 : 1** exchange rate the diagnosis measured
  (S0→S5: +37k of revenue to kagg3, −45k to kagg2) is a fact about which *actions* buy
  margin cheaply, not a reason to re-weight the objective; any `w_den > 0` on top of a
  margin term prices the opponent's ruin above our own win, which is not what a
  Bradley-Terry field pays for. The tracker's own regression
  points the other way for the *current* policy: over `esfix1`'s ~6,000 generations own
  coins vs kagg2 rose **67k → 92.4k** while kagg2's rose **97k → 132.5k** and the margin
  stayed at −30…−40k — a slope of **+1.40 kagg2 coins per kagg3 coin**. Observational,
  and it may straddle the f0a678c / d3a1f8b code syncs the tracker warns about, but it is
  the same co-scaling §1.3 measures: coins and denial are not opposites here, they move
  together, and only the *composition* of the book separates them.
* **Collapse risk: high — this is the mutual-destruction optimum.** The diagnosis's S6
  reaches ratio 1.96 with kagg3 on **72k coins**, *below* the 80k ceiling S3/S5 reach.
  In a Bradley-Terry field of 30+ agents a 72k denial policy loses to every third agent
  that farms 130k in a quiet game. The liveness floor does **not** protect against this:
  it probes the *archetypes* against the zero theta, and the archetypes stay healthy —
  it is the trained policy that burns the market down.
* **Promotion: would have to change**, and to a floor rather than a maximum: promote on
  margin *subject to* own coins ≥ some F.

### C. A kagg2-proxy rung

The ladder's top rung is **half of kagg2** (§1.3). Candidate C adds a rung calibrated so
that a strong kagg3 faces, in sim, the numbers it faces in the real engine: opponent
~111k coins, own ~62k, margin ≈ −49k. Two ways to build it:

1. **Knobs only** (higher `crowd`, `land_cap` 4). Measured below — it does not reach,
   because an archetype runs *this* planner, and this planner's throughput ceiling is
   the unit-turn budget `2026-08-26-work-idle-tiles` measured, not its knobs.
2. **An asymmetric opening.** `draw_starts` already carries per-player `(nquad, money)`;
   `rollout.episode` takes them per seat. Give the proxy rung — and only that rung — an
   opening of 3–4 quadrants and 20–40k coins, and it reaches kagg2's production without
   any new planner capability. Nothing new is being asked of the simulator: `warm_frac`
   already opens a quarter of all pairs on 2–4 quadrants and up to `warm_money_max`
   40,000 coins. The only change is that the two seats stop sharing the row.

* **Expected effect: the only candidate that changes what is being measured.** The
  fitted rung (§3.3, `mixed_ranch` with the opponent seat opening on 3 quadrants and
  20,000 coins) reproduces **81 %** of kagg2's suppression against today's rung's 20 %,
  and it is an **independent** ranking of the policies a run actually chooses between:
  Spearman(`abs_coins`, proxy margin) is +0.857 / +0.450 / **+0.261** across the three
  subsets, against +0.968 / +0.947 / **+0.903** for `abs_coins` vs the `mixed_ranch`
  margin. Controlling for coins it is the only quantity here with *positive* residual
  information about the real margin (win: +0.42 at the top; §1.2). And it un-saturates
  the win bit: the proxy wins 90–100 % of its games, so `W` varies again
  (0.000 … 0.102 over the top 10) where against every current rung it is a constant 1.00.
* **Collapse risk: low. Exploitation risk: the highest of the five**, and the handicap is
  not kagg2's mechanism (free capital, not better routing), so a policy could learn "beat
  a rich opponent" instead of "beat a well-routed one". Mitigations: keep `arch_frac` at
  0.5 so half the episodes are still self-play; hold one handicap level out of training
  and only report it; keep the liveness probe but run it **with the handicap applied**,
  otherwise the probe measures a different game from the one played.
* **Promotion: must change.** Own coins against a handicapped rung are ~40 % lower, so
  `best_abs`'s scale moves the moment the rung is added and old and new runs' `best_abs`
  numbers stop being comparable. Selection has to move to a margin/score quantity that is
  invariant to the rung's strength.

### D. A tournament / Bradley-Terry term

`GOAL.md` is explicit: `J(θ) = E[W]`, `W ∈ {0, 0.5, 1}`, "the final Bradley-Terry
tournament scores win/loss/tie only and discards coin margin", and the Non-goals list
names "coin margin, expected profit, or any shaped proxy as the selection metric". The
current objective is 60 % coins by weight and 100 % coins by selection rule — it is the
opposite of the stated goal, and §1 says the swap did not buy what it was meant to.

Fitting actual BT strengths over the ladder is not worth it at pop 128 (each candidate
plays 64 episodes; a BT fit needs a round-robin the population cannot afford). The
implementable form is **expected tournament score against a weighted ladder** — which is
candidates A + C with the margin term's temperature dropped so it approximates the bit:

```
score(θ) = (1/E) Σ_e w_{o(e)} · sigmoid( (mine_e − theirs_e) / τ )
```

* **Expected effect:** at τ = 25k rather than 100k the sigmoid's slope per coin at the
  −49k margin of the real game is **4.33e-6** against 2.36e-6 — **1.84×** more resolution
  where the games are actually contested — while a +100k blow-out against `expander`
  flattens from 1.97e-6 to 7.07e-7 and `staple_bulk`'s +128k from 1.70e-6 to 2.35e-7. Full
  table in §3.1. It is not that ties need breaking; it is that runaway wins need
  discounting.
* **Collapse risk: the pure bit saturates** — that is the measured failure that got win
  rate demoted in the first place (`mean_win` reaches 0.5 and stays). The sigmoid at a
  finite τ is what keeps a gradient; and the fixed rungs (which the policy beats 100 % of
  the time) plus the proxy rung (which it loses to 97 % of the time) are two saturated
  ends that a τ-shaped term still separates.
* **Promotion: `best_abs` → best score on the same fixed seeds.**

### E. Curriculum — coins first, then margin

`--abs-weight` annealed linearly over `--gens` (0.6 → 0.15 cold, or 0.3 → 0.15 on top
of §3).

* **Expected effect: cheap insurance, not a lever.** The measured problem is not that the
  early run needs coins; it is that the *late* run keeps buying them. An anneal makes the
  late run's objective right without risking the early scale-building. Two lines in
  `generation()`.
* **Collapse risk: low, but it breaks comparability** — `best_abs` measured at gen 500
  and at gen 8,000 are then selected under different objectives, and the pool's rungs were
  frozen under a mixture of them. `_snapshot`'s eviction rule (`_versus_pool`, a win rate)
  is unaffected.
* **Promotion:** must move to the *final* objective from generation 1, or the run spends
  its first half promoting on a rule it will later disown.

### Ranking

| | changes what is measured | fixes selection | measured residual info (top 10) | cost | risk |
|---|---|---|---|---|---|
| **C + D + A** (§3) | **yes** | **yes** | **+0.42** (proxy win) | 1 rung + ~80 lines | exploitation, mitigated by a held-out rung |
| A alone | no | no | −0.63 (the rung it up-weights) | ~20 lines | low |
| B | no — the margin already differentiates it | needs a floor anyway | −0.56 | ~10 lines | **high — mutual destruction** |
| D alone | partly (τ only) | yes | −0.39 (τ = 25k score, no proxy) | ~30 lines | saturation at both ends |
| E | no | no | n/a | ~5 lines | low; take it as a rider on C+D+A |

The residual column is the partial Spearman of §1.2 — what the candidate's own measured
quantity adds to the real kagg2 margin beyond `abs_coins`. **Every candidate that reuses
the existing ladder scores negative there.** C is the only one that does not, and that is
the whole argument.

---

## 3. Spec for the top candidate — weighted expected tournament score on a calibrated ladder

C + D + A, with E as an optional rider. Every flag below **defaults to today's
behaviour**, so an unflagged `scripts/train.py` invocation is byte-for-byte the current
run and every existing checkpoint keeps its meaning.

### 3.1 The objective

The weighting is applied as **slot allocation**, not as a term in `shaped_advantage`.
That keeps the module docstring's rule intact ("the opponent the absolute yardstick is
made of is also the opponent the gradient mostly sees"), automatically weights *both*
fitness terms by the same mixture, and buys variance reduction on the rung that matters
instead of only re-weighting a noisy mean.

```python
# src/kagg3/es/train.py  --  opponent_slots, archetype block only
#
# Today:   idx[:k] = n_pool + np.arange(k) % n_arch          # uniform round-robin
# Becomes: a largest-remainder allocation of the k archetype pairs over the rungs
#          in proportion to `weights`, laid out as contiguous per-rung blocks.
#          Position still carries no information: the seeds are redrawn every
#          generation and the warm-start flags come from an independent stream.
def opponent_slots(n_pairs, n_pool, n_arch, arch_frac, weights=None):
    ...
    w = np.ones(n_arch) if weights is None else np.asarray(weights, float)
    share = k * w / w.sum()
    take = np.floor(share).astype(int)
    take[np.argsort(-(share - take))[:k - take.sum()]] += 1     # largest remainder
    idx[:k] = n_pool + np.repeat(np.arange(n_arch), take)
```

`np.repeat` lays each rung's pairs out as a contiguous block, which is also what makes the
proxy's episodes trivially identifiable for the start override below.

`shaped_advantage` keeps its shape; only `margin_scale` is retuned.

```
adv = abs_weight * rank(mean_e log1p(own)) + (1-abs_weight) * rank(mean_e sigmoid(margin/tau))
```

with `tau = margin_scale`. The tuning argument is the slope `s(1-s)/tau` per coin:

| margin, and where it occurs | τ = 100k (today) | τ = 25k (proposed) | ratio |
|---|---|---|---|
| **−49k** — the real kagg2 game, and the calibrated proxy | 2.36e-6 | **4.33e-6** | **1.84×** |
| +20k — `mixed_ranch` vs the weakest non-degenerate checkpoint | 2.48e-6 | 8.56e-6 | 3.46× |
| +57k — `mixed_ranch` vs the champion | 2.31e-6 | 3.36e-6 | 1.46× |
| +100k — `expander` vs the champion | 1.97e-6 | 7.07e-7 | 0.36× |
| +128k — `staple_bulk` vs the champion | 1.70e-6 | 2.35e-7 | 0.14× |

Today's τ is nearly **flat over the whole range** (1.70–2.48e-6, a factor of 1.5) — the
"relative" term prices a coin of margin against a collapsed rung almost exactly as dearly
as a coin of margin in a game that is actually close. τ = 25k concentrates the resolution
inside ±50k of a tied game (1.8–3.5× today's slope) and discounts the runaway wins by
2.8× and 7.2×. It is not about breaking ties; it is about refusing to pay for them.

**This is a design argument, and §1's data cannot confirm it.** Sweeping τ ∈ {25k, 50k,
100k} against the real margin, the yardstick score's ρ over the 16 working checkpoints is
0.862 / 0.882 / 0.882 and over the top 10 is 0.624 / 0.636 / 0.636 — differences far
inside the n = 10 null band of 0.648. Take τ = 25k for the reason above, not because it
measured better; and treat it as the first thing to re-sweep once a run trained on this
objective produces checkpoints that differ in style rather than in strength.

### 3.2 Flags

| flag | default (= today) | proposed run | what it touches |
|---|---|---|---|
| `--rung-weight NAME=W` (repeatable) | none → all 1 | `kagg2_proxy=3 mixed_ranch=2 value_farmer=1.5` | `opponent_slots`, `absolute_report` |
| `--n-archetypes` | 4 | **9** (`AR.NAMES` + `kagg2_proxy`) | `_build_archetypes` |
| `--proxy-handicap NQUAD:MONEY` | `1:3000` (= cold, off) | **`3:20000`** (fitted, §3.3) | `draw_starts`, `absolute_report`, `_probe_archetypes` |
| `--margin-scale` | 100000 | **25000** | `shaped_advantage` |
| `--abs-weight` | 0.6 | **0.3** | `shaped_advantage` |
| `--abs-weight-final` | = `--abs-weight` | 0.15 (candidate E) | linear anneal over `--gens` |
| `--select-metric` | `coins` | **`score`** | `_measure_champion`, `best_abs`, `--promote`, `_maybe_restart` |
| `--select-coin-floor` | 0 | **80000** | selection guard |

`--select-coin-floor 80000` is 0.75 × the incumbent's weighted selection-half coins under
the proposed ladder (`p2s0/champion`: **106,816**, against 118,843 on today's unweighted
8-rung yardstick). The recipe, not the constant, is what carries across a planner merge:
run `absolute_report` once on the incumbent and take 0.75 of its `coins`.

**One implementation trap.** `Trainer._play` indexes the start arrays by **pair**
(`nq[pair], mo[pair]`), and `make_evaluator.one` puts the candidate at player 0 only on
seat 0 (`a = where(seat == 0, theta_c, theta_o)`). An asymmetric row indexed by pair
would therefore hand the handicap to *us* on one of the two seats. The starts have to be
built at **episode** resolution and the handicap placed at index `1 - seat`. This is one
line in `_play` and it is the only place the change is not local; `absolute_report` and
`_probe_archetypes` already build their starts per episode (`cold_starts(total)`), so the
handicap drops straight in there. `tests/test_warm_start.py` should pin it.

Refusals, in the same place as the existing `--abs-weight` / `--arch-frac` checks (before
the run directory is created): a `--rung-weight` naming a rung not in the archetype list;
a negative weight; `--proxy-handicap` with `--n-archetypes` below the proxy's index;
`--select-coin-floor > 0` with `--select-metric coins` (it would silently do nothing).

### 3.3 The rung, and how it is calibrated

**Who is in the mixture.** `arch_frac` stays at **0.5**, so half the episode pairs face
the ladder and half round-robin the self-play pool plus `theta` — unchanged, and it is
what keeps the ratchet and bounds the exploitation risk. Inside the ladder half, at
`--episodes 64` (32 pairs, k = 16 archetype pairs) and weights
`kagg2_proxy 3, mixed_ranch 2, value_farmer 1.5, the other six 1`:

| rung | weight | share × 16 | pairs | episodes / 64 | today |
|---|---|---|---|---|---|
| `kagg2_proxy` (new) | 3 | 3.84 | **4** | 8 (12.5 %) | — |
| `mixed_ranch` | 2 | 2.56 | 3 | 6 (9.4 %) | 4 (6.25 %) |
| `value_farmer` | 1.5 | 1.92 | 2 | 4 (6.25 %) | 4 (6.25 %) |
| `expander` (first of the remainder tie) | 1 | 1.28 | 2 | 4 | 4 |
| `rusher`, `rancher`, `patient_grower`, `squeeze_seller`, `staple_bulk` | 1 each | 1.28 | 1 each | 2 each | 4 each |
| self-play pool + `theta` | — | — | 16 | 32 (50 %) | 32 (50 %) |

Floors sum to 12 and the four largest remainders (0.92, 0.84, 0.56, then the first 0.28)
take the rest, so the allocation is exact. The two rungs carrying the kagg2 shape go from
**6.25 % → 21.9 %** of the gradient's episodes; the six rungs that are settled by
generation 100 fall from **37.5 % → 21.9 %**.

`kagg2_proxy` is `mixed_ranch`'s knobs played from a handicapped opening. The handicap is
not a free parameter: it is *fitted* so that the in-sim match reproduces the real-engine
kagg2 match for the same theta.

| quantity | real engine, `p2s0/champion` vs `kagg2` | in sim, target |
|---|---|---|
| opponent coins | 111,035 | 105k … 118k |
| own coins | 62,046 | 56k … 68k |
| margin | −48,989 | −44k … −54k |
| win rate | 0/24 | ≤ 0.15 |

Measured, `p2s0/champion`, the 64 fixed `abs` seed pairs × 2 seats = **128 games per
variant**. "suppression" is `own coins against the least-suppressive opponent − own coins
here`; the in-sim reference is `staple_bulk` (126,718) and the real one is `starter`
(132,211), so the last column is comparable across the line:

| variant | its coins | our coins | margin | our win | suppression | % of kagg2's |
|---|---|---|---|---|---|---|
| `mixed_ranch`, cold — **today's rung** | 56,078 | 112,706 | +56,628 | 1.00 | 14,012 | **20 %** |
| `mixed_ranch` `crowd` 6 / `land_cap` 4, cold | 46,383 | 114,203 | +67,820 | 1.00 | 12,515 | 18 % |
| `value_farmer`, opp 3 quad + 20k | 33,226 | 95,539 | +62,313 | 1.00 | 31,179 | 44 % |
| `mixed_ranch`, opp 4 quad + 40k | 96,390 | 75,239 | −21,150 | 0.17 | 51,479 | 73 % |
| **`mixed_ranch`, opp 3 quad + 20k** | **100,778** | **70,048** | **−30,730** | **0.02** | **56,670** | **81 %** |
| `kagg2`, real engine (24 games) | 111,035 | 62,046 | −48,989 | 0.00 | 70,165 | 100 % |

Three things this settles:

* **Knobs alone go the wrong way.** `crowd` 6 / `land_cap` 4 makes the rung *weaker*
  (46,383 vs 56,078), because an archetype runs this planner and the planner is
  unit-turn-bound, not knob-bound. The `2026-08-26-work-idle-tiles` measurement is the
  reason: 48.6 % of unit-turns are moves and the value tail is dropped, so extra land and
  extra crowding buy nothing.
* **More handicap is not better.** 4 quadrants + 40k is *easier* than 3 + 20k (−21.2k vs
  −30.7k) — `land_cap` 3 makes the fourth quadrant dead weight and the extra cash has no
  unit-turns to spend itself through. **`--proxy-handicap 3:20000`** is the fitted point,
  and the fit is a shallow optimum in one direction only.
* **The residual is 18.3k and it splits evenly**: the rung earns 10.3k less than kagg2
  (100.8k vs 111.0k) and we earn 8.0k more than we do against kagg2 (70.0k vs 62.0k) —
  a 13 % sim-vs-engine level offset that the diagnosis's own scenario model carries too
  (±13 %, worst case −29 %). This rung is as calibrated as this simulator gets.

Calibration is a **measurement, not a constant**: `mixed_ranch`'s output moves whenever
the planner does (the module already warns that a planner merge shifts archetype
earnings and `tests/test_archetype_ladder.py` must be re-run). The handicap therefore
gets the same treatment — re-fit it after every planner merge, in the same test.

**Held out — two rungs, testing two different kinds of transfer.** Neither is ever put in
`self.archetypes`; both are played only inside `absolute_report`'s holdout block.

* `mixed_ranch` at `--proxy-handicap 3:30000` — *handicap-level* transfer. If the policy
  is learning "beat a rich opponent" rather than a strategy, its margin here will lag the
  trained rung's as the run progresses.
* `value_farmer` at `3:20000` — *strategy* transfer: the same handicap on a different
  book. Measured today at 33,226 / 95,539 / **+62,313**, 44 % of kagg2's suppression — a
  middle rung, so it is a transfer probe, not a difficulty probe.

Today's holdout is on *seeds* and shows no overfitting at all (`abs_holdout` tracks
`abs_coins_sel` to a **mean 1.1 % and worst 4.0 %** across all 30 checkpoints, ρ = +0.998,
§1.3d) — which is exactly why the missing holdout is the *opponent* one.

**Liveness:** `_probe_archetypes` must play the proxy **with its handicap applied**,
otherwise the probe measures a different game from the one trained on. Two floors, not
one:

* the existing `MIN_COINS = 10,000` against the zero theta, and
* a new **ceiling-of-collapse** check against the *incumbent* theta: a rung that keeps
  under 25 % of its zero-theta coins when a real policy is on the board is not a rung,
  it is a free win. `staple_bulk` fails this today — 17,560 coins against the zero theta,
  **838** against `p2s0/champion` — 4.8 % (§1.3) — and it is currently 1/8 of the
  yardstick. `mixed_ranch` keeps 0.76 and kagg2 itself 0.65, so a 25 % floor separates a
  live rung from a free win with room.

### 3.4 `absolute_eval`, `best_abs` and promotion

`AbsReport` gains three fields and one weighting:

```python
class AbsReport(NamedTuple):
    coins: float        # selection seeds, weighted mean own coins      (unchanged when w=1)
    score: float        # selection seeds, weighted mean sigmoid(margin / margin_scale)   NEW
    win: float
    mine: tuple; theirs: tuple
    holdout: float; holdout_win: float
    holdout_score: float                                               # NEW
    holdout_rungs: tuple # per held-out rung: (own, theirs, margin, win)  NEW
```

* `score` and `coins` are averaged over the **same rung weights** as the gradient, so the
  yardstick and the objective describe one mixture.
* `_measure_champion` and the `best_abs` update read `sel = rep.score if
  cfg.select_metric == "score" else rep.coins`, **subject to** `rep.coins >=
  cfg.select_coin_floor`. That floor is the whole guard against candidate B's
  mutual-destruction optimum, and it is a floor rather than a term because the failure is
  a *region*, not a slope.
* `_maybe_restart` reads the same `sel`; the field keeps the name `best_abs` in
  `state.npz` so `--resume` stays compatible, and the log gains `sel_metric`,
  `abs_score`, `abs_holdout_score`, `best_sel`.
* **`best_abs.npy` keeps its filename.** Only `scripts/remote_eval_kagg2.sh` reads it, and
  the tracker should keep pointing at the same path; what changes is the rule that fills
  it. `config.json` and the first `log.jsonl` record carry `select_metric`, so a tracker
  row can always be attributed to the rule that produced it.
* `--promote` is unchanged in mechanism (ship `best_abs_theta`) and changed in meaning.

**Cost.** The yardstick goes from 8 rungs to 9 trained + 2 held out = 11, i.e.
11 × 64 × 2 = **1,408 rollouts** per measurement against today's 1,024. A generation at
`--pop 128 --episodes 64` is 8,192 rollouts and the measurement runs every
`min(abs_every, champ_every) = 10` generations, so the yardstick goes from 1.25 % to
**1.7 %** of training throughput. There is no reason to be stingy with rungs.

### 3.5 Real-engine validation protocol

`scripts/remote_eval_kagg2.sh` already records margin and kagg2's coins. Four changes,
in cost order:

1. **Keep the per-game CSV.** It is written into a `mktemp -d` that the `EXIT` trap
   deletes, so no two tracker rows can ever be compared *paired* — and `scripts/paired_ci.py`
   exists precisely to do that. Write it to `artifacts/kagg2_games/<run>_<gen>.csv`
   instead (≈ 4 kB a row). Zero extra compute. Comparing two 16-game rows *unpaired*
   costs 1.96·√2·3,546 = **±9.8k**; the paired intervals `2026-08-26-work-idle-tiles` §6
   reports on the same 16 games run **±3.5k–8.8k** — and 5–14k is exactly the size of the
   effects being chased.
2. **8 seeds → 24 seeds (16 → 48 games).** Margin SE falls 14,182/√16 = 3,546 → 2,047.
   At `nice -19` with 3 workers that is ≈ 4.5 min per row against a 2 h cadence — a 3.8 %
   duty cycle on a host whose GPUs are the bottleneck.
3. **Four new columns**, all free:
   * `margin_ci95` = 1.96 · sd(margin)/√n;
   * `win_lo` / `win_hi`, Wilson 95 %. Quote them so nobody over-reads the win column:
     **0/16 → [0.0 %, 14.5 %]**, 0/48 → [0.0 %, 7.4 %], 8/16 → [28.0 %, 72.0 %],
     24/48 → [36.4 %, 63.6 %]. Win rate cannot resolve anything until the margin is near
     zero. **Record it; gate on margin.**
   * `joint_coins` = own + kagg2 coins, as a diagnostic only. Measured baseline
     62,046 + 111,035 = **173,081**; the diagnosis's frontier scenarios run S3 189k,
     S5 145k, S8 131k and the S6 collapse 109k — so it falls *as the margin closes*, in
     the good scenarios too. It reads the market's temperature; it is **not** a gate.
   * `sel_metric` and `best_sel`, read off `log.jsonl`, so a row identifies its rule.

   **The gate against mutual destruction is the column the tracker already has:
   `coins_vs_starter`.** A denial collapse buys margin against kagg2 by burning the
   market, and against `starter` there is no market worth burning — so it shows up there
   and nowhere else. The work-idle measurements calibrate the axis: `R3 alone` costs
   **−7,217** vs `starter` and `R4 alone` −3,006, while `R1+R3` gains **+8,391 vs
   `starter` and +14,062 of margin** — the changes that buy margin without the routing fix
   pay for it in own coins, and `starter` is where that is visible. Gate on *both*: a
   paired margin gain against kagg2 whose paired `coins_vs_starter` loss exceeds 10 % is
   the objective eating the market rather than winning the game.
4. **A gate run before any promotion decision**: 32 seeds (64 games) for both the
   challenger and the incumbent on the same `--seed-base`, then

   ```
   .venv/bin/python scripts/paired_ci.py CHALLENGER.csv INCUMBENT.csv \
       --opponent ../kaggriculture2/main.py --metric margin
   ```

   Promote only on a paired interval that excludes 0.

### 3.6 Tests

| file | change |
|---|---|
| `test_fitness_shaping.py` | `test_defaults_are_the_coin_objective` must still pass **unchanged** — that is the no-op guarantee. New: the largest-remainder allocation sums to `k` and matches the uniform case at `w = 1`; the τ slope table of §3.1. **`test_the_absolute_anchor_outweighs_the_relative_term` deliberately flips** under the proposed settings — its case (own 90k losing by 5k vs own 40k winning by 30k) scores −0.20 / +0.20 at `abs_weight` 0.3 and τ 25k, against +0.10 / −0.10 at today's. Restate it as a conditional on `abs_weight`, with both branches asserted; do not delete it. |
| `test_absolute_eval.py` | `score` is the weighted mean of the per-rung sigmoids; `select_coin_floor` blocks a high-score/low-coin candidate; the held-out proxy never appears in `candidates()`. |
| `test_archetype_ladder.py` | the liveness probe applies the handicap; `kagg2_proxy` clears `MIN_COINS`; the new collapse ceiling fails `staple_bulk` (expected — fix or drop that rung in the same change). |
| `test_warm_start.py` | an asymmetric opening reaches only the proxy rung's episodes; every other rung still shares its seat's start. |
| `test_resume_roundtrip.py` | `select_metric`, `select_coin_floor` and the rung weights round-trip through `state.npz`. |

### 3.7 Sequencing

This lands **after** the land/herd + drain-feature + work-idle-tiles merges, not beside
them. Three reasons, all measured:

1. `es/archetypes.py` is being edited by the merge agent right now, and `kagg2_proxy`
   is a new entry in `_NAMED` / `NAMES` — a guaranteed conflict.
2. Every number in §3.3 is a function of the planner. R1+R3 alone moves the margin vs
   kagg2 by +14,062 and the occupied-tile count from 72.6 to 80.9; the handicap that
   fits *today's* planner will not fit that one.
3. The 8-rung ladder is being recalibrated in the same merge
   (`tests/test_archetype_ladder.py`, `MIN_COINS` against the zero theta). The proxy's
   calibration and the collapse ceiling of §3.3 belong in that same pass.

The parts that do **not** depend on the planner and can land immediately are §3.5's four
tracker changes — keeping the per-game CSV especially, since every comparison made
between now and then is unpaired without it.

### 3.8 What would falsify this

The proxy is calibrated on *levels* — its margin is 0.62 of the real one for the
incumbent (−30.7k against −49.0k). Nothing here measures the **slope**, and the slope is
what a training run consumes. The prediction to check, and the reason to check it early:
over the next 2,000 generations,
`Δ(real margin vs kagg2) ≈ 0.5 · Δ(sim margin vs kagg2_proxy)`. If the tracker's paired
margin moves less than **0.2 ×** the sim proxy margin over that window, the policy is
fitting the handicap rather than the strategy, and the held-out proxy rung (§3.3) will
show it first — its margin will lag the trained one.

### 3.9 Evidence grade, and the staged rollout that follows from it

Being explicit about what §1 does and does not license, because the numbers cut both ways:

| claim | evidence | grade |
|---|---|---|
| The two fitness terms are one measurement | ρ = +0.973 / +0.965 / +0.867, n = 30/16/10 | **strong** |
| The ladder is beaten in ~every game and the win bit carries nothing | 15/16 at `abs_win` ≥ 0.99 over 1,024 games each | **strong** |
| The top rung is half of kagg2 | 56,078 vs 111,035; 20 % of the suppression | **strong** |
| A 3-quadrant / 20k handicap reproduces the kagg2 matchup | 100,778 / 70,048 / −30,730 against 111,035 / 62,046 / −48,989 | **strong on levels** |
| The proxy adds information beyond coins | partial ρ +0.42 (win) / +0.24 (own coins) at the top 10 | **suggestive** — n = 10, null band 0.648 |
| The ladder's margin *subtracts* information | partial ρ −0.628 (top 10), −0.463 (n = 16) | **suggestive**, consistent in sign across subsets |
| Proxy weight 3 is right | sweeping w ∈ {0,1,2,3,5,8}: raw ρ at the top 10 falls (0.64 → 0.25) while the partial rises (−0.35 → +0.28) | **not established** |
| τ = 25k beats τ = 100k | indistinguishable (§3.1) | **not established** |

So: land the **rung** on the evidence, and earn the **weights**.

**Stage 1 — measure only (no gradient change).** Add `kagg2_proxy` and the two held-out
rungs to `absolute_report`; log `proxy_margin`, `proxy_win` and `score` every measurement.
`--rung-weight` stays unset, `--select-metric coins`, `--margin-scale 100000`: the run is
byte-identical to today and the tracker rows stay comparable. Cost: 1.7 % of throughput.
**Exit test:** over ≥ 6 tracker rows, does the logged `proxy_margin` move with the
tracker's paired real margin? A rank correlation over 6 points is weak, but a *sign*
disagreement is decisive and cheap to see.

**Stage 2 — selection.** `--select-metric score --select-coin-floor 80000`, weights still
flat. This changes which theta `--promote` ships without changing the search direction, so
one gate run (§3.5.4) measures it directly against the incumbent.

**Stage 3 — gradient.** `--rung-weight kagg2_proxy=3 mixed_ranch=2 value_farmer=1.5
--abs-weight 0.3 --margin-scale 25000`, on one GPU, against an unchanged run on the other
— the campaign already runs two lineages side by side for exactly this comparison
(`esfix1` / `comb1`). Compare on the tracker's paired real margin, not on `best_sel`,
which is no longer the same number between the two.

---

## 4. Reproduction

Harness in this session's scratchpad — `build_set.py` / `build_set2.py` (assemble and
zero-pad the 30 thetas), `sim_eval.py` (blocks (a)/(b)), `sim_proxy.py` (block (d)),
`real_eval.py` (block (c), the real engine), `analyse.py` / `md.py` / `collapse.py` / `calib.py`
(joins and tables). Nothing was added to `scripts/` and nothing under `src/` was
modified. The real-engine runner is
`scripts/eval_vs_baselines.py::_play` driven from a
`ProcessPoolExecutor(max_tasks_per_child=1)` — one fresh worker per game, because a
packaged file agent rewrites `sys.modules` and a reused worker carries that across
(`2026-08-26-work-idle-tiles` §2 hit the same thing with monkeypatched counterfactuals).

```
IN_NPZ=thetas_all.npz OUT_JSON=sim_all.json  .venv/bin/python sim_eval.py     # blocks A,B
IN_NPZ=thetas_all.npz OUT_JSON=proxy.json N_PAIRS=64 .venv/bin/python sim_proxy.py  # block (d)
IN_NPZ=thetas_all.npz OUT_CSV=real.csv       .venv/bin/python real_eval.py 12 8
SIM=sim_all.json PX=proxy.json REAL=real.csv .venv/bin/python md.py
```

**Harness check:** `p2s0/champion`'s row here — 62,046 own, 111,035 to kagg2,
**−48,988** margin, 0/24 — reproduces the diagnosis's independently-written 24-game
measurement to the coin, on the same seed base. The two harnesses share only
`eval_vs_baselines._play`.

Caveats a reader should carry:

* The archived checkpoints span four lineages and three of them **predate the Phase-2
  planner**; they decode to 4.4–12.6k coins under the current one. They are kept because
  a correlation needs range, but every conclusion is also reported on the 16
  non-degenerate checkpoints alone, and the two differ (§1.2).
* `p2s0` here is the *local* 75-generation smoke run, not the remote 7,830-generation
  one. Its champion is the strongest theta on this machine (116.2k vs `starter` per the
  diagnosis) but sits ~12–15 % below the tracker's best lineage, so the ratios transfer
  and the levels do not.
* 24 games per checkpoint gives a margin SE of ≈ 2.9k; differences under ~8k between two
  adjacent checkpoints are inside the noise. Rank correlations over 16–30 checkpoints are
  robust to that; individual orderings near the top are not.
