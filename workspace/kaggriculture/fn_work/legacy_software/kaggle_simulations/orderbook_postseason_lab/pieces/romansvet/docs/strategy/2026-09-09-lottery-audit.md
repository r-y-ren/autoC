# Lottery audit — every decision taken on a statistic, and whether the statistic can carry it

2026-09-09. Code-only audit (no new simulations). Scope: the ES trainer in the remote training tree
`.claude/worktrees/arms-next` at `bdec0e9` (`src/kagg3/es/train.py`, `scripts/train.py`), the main
repo's `scripts/`, and the local measurement harness under
**S** = `/tmp/claude-0/-mnt-e--work-kaggriculture3/8b388b22-9a4b-4bf0-8e3e-dc4aac1d5f04/scratchpad`.

Question asked of every site: *a decision is taken here (accept / reject / record / re-centre /
select / promote / rank / stop / tune). Is the noise of the statistic it reads smaller than the
threshold that decides?* Where it is not, the site is a **LOTTERY**: it emits verdicts at a rate set
by chance, and every downstream conclusion inherits that rate.

## Measured noise constants used throughout

| constant | value | source |
|---|---|---|
| per-game own-coin spread, drawn board | ~20–30k coins | S/spo csvs; loss ledger |
| per-board \|Δ margin\| between near-neighbour thetas, pinned | median 1,734, mean 2,831, pooled sd 4,240 | `docs/strategy/2026-09-09-judge-calibration.md` §1 |
| net flips on the 42-board pinned held-out set, across 24 arms | mean +2.8, **sd 3.1**, range 0…+12 | judge-calibration §TL;DR 2 |
| flips concentrated in | **15 of 42 boards** (30 of 84 games); 100 % of every arm's flips | judge-calibration §1 |
| judge true positives vs 1,808-game drawn legs | **0 of 4 fires** (all 7 arms with both reads lost the legs, −2.7…−9.1 pts) | judge-calibration §TL;DR 3 |
| leg discrimination between close arms | 640–656-game legs ρ 0.83–0.85; band6 (192) and jesse4 (128) ρ **0.07–0.13** | judge-calibration §TL;DR 5 |
| ES centre motion | Adam snr \|m̂\|/√v̂ **0.17–0.19** vs pure-noise expectation **0.23**; drift/√gen flat 0.0033 across flow150–155 | `docs/strategy/2026-09-09-plateau-review-verdicts.md` §0 |
| shop draw | one RNG draw per EMPTY tile at end of day → any tile change re-rolls every later shop, ±25k zero-mean | memory, shop-lottery 2026-09-06 |
| mirrored seats | pinned boards return the *same* outcome in both seats; drawn boards strongly correlated | `pinned_tally` docstring; `paired_stats` docstring |

The live recipe these thresholds are read under (`S/launch_flow137.sh`, and the same flags in 12 of
the launch scripts on disk): `--episodes 256/512 --abs-every 10 --abs-pairs 64 --abs-select all
--best-margin 0.005 --best-replicate 2 --real-gate-every 50 --real-gate-games 24
--real-gate-replicate-games 48 --real-gate-metric win --real-gate-min-gain 0.0
--real-gate-paired-t 1.7 --real-gate-replicate --real-gate-recentre 1 --real-gate-fresh
--real-gate-seed-per-opponent`, 8 gate opponents.

## 1. The ES trainer (`.claude/worktrees/arms-next/src/kagg3/es/train.py`)

### 1.1 In-sim record acceptance — `_accept_best`

`train.py:5514-5822`. The decision: `sel > best_abs + best_margin` (and, under `--best-gate both`,
`hold >= best_hold`).

* **Statistic**: `selection_score(rep)`. Under the live recipe that is `--select-metric score` with
  `--abs-weight 0.0` and `--margin-scale 3000` — i.e. the mean of `sigmoid(margin/3000)` over the
  rung-weighted fixed boards. At scale 3000 the sigmoid is saturated for any |margin| > ~9k, and the
  measured near-neighbour |Δmargin| is median 1,734 / pooled sd 4,240, so the statistic is a *near
  win-bit* mean. Its per-reading sd on `--abs-pairs 64` (64 boards, both seats — and mirrored seats
  are strongly correlated, so the effective n is ≈64) is ≈ 0.5/√64 = **0.0625**; `--best-replicate 2`
  averages three readings → ≈ **0.036**.
* **Threshold**: `--best-margin 0.005` = **0.14 standard errors**.
* **Compounding**: `best_abs` is a max over the whole run's sequence of readings. At `--abs-every 10`
  and `--gens 30000` that is up to 3,000 readings; E[max of 3,000 standard normals] ≈ 3.5 σ ≈
  **+0.13 in score** of pure luck — 26× the bar. The code's own docstring at `train.py:5518-5528`
  states the defect ("`best_abs` is a **max over a noisy sequence**… biased upward by however far the
  luckiest reading of the run happened to land") and measures it at ~3k coins on flow2.
* **VERDICT: LOTTERY.** `--best-replicate 2` (`train.py:5081-5140`) is the correct fix and is on in
  the live recipe, but it only removes the *screening* luck; the bar `best_abs` itself is still a
  running max, so the ratchet still climbs on noise, just more slowly.
* **Smallest fix**: set `--best-margin` to ≥ 2 standard errors of the replicate mean (≈0.07 at these
  settings, i.e. **14× the current value**), or drop the running max entirely and select the record
  by a paired t against the standing record on shared boards (`paired_stats` already exists and is
  correct — it is simply not wired into the in-sim path).

### 1.2 `--abs-select` / holdout ratchet

`train.py:5548-5552`, `_check_abs_select` `train.py:3708-3735`. The live recipe uses
`--abs-select all`, which **selects on every fixed pair and leaves no holdout**; `_check_abs_select`
then refuses `--best-gate both`, so the one guard against a lucky selection-half draw is unavailable
by construction. The docstring's own defence ("on 64 pairs instead of 32 the reading is about √2 less
lucky") buys 1.41× against a 26× shortfall.
**VERDICT: LOTTERY** (as configured). **Fix**: `--abs-select sel` + `--best-gate both`, which costs
nothing and restores the holdout veto; or raise `--abs-pairs` to 256 (2× the SE reduction) — both
cheaper than any of the above.

### 1.3 Champion tracking — `_measure_champion`

`train.py:5563-5592`, accept on `sel >= self.champion_score`. Same max-over-noisy-sequence, with a
**non-strict** comparison and **no margin at all**. It is deliberately the same rule as `best_abs`
(the docstring calls the agreement "the fix"), which means it inherits the same bias rather than
providing an independent read. **VERDICT: LOTTERY.** **Fix**: none needed if `--promote` ships
`best_abs_theta` (it does) — but stop citing `champion.npy` as corroboration; it is the same draw.

### 1.4 Stall / restart-sigma

`_maybe_restart` `train.py:5232-5279`, `_restart_from_record` `train.py:5280-5308`,
`_gate_restart_check` `train.py:5203-5231`. The trigger is `t - last_improve >= restart_stall`
(live: 1500 generations without a record). Because §1.1 makes records a lottery, the stall clock is
a clock on *when the noise last pointed up*, not on convergence. At `--stall-sigma-mult 1.0` (the
live setting) the consequence is bounded — theta jumps back onto `best_abs_theta` and Adam is
cleared — but that jump **discards 1,500 generations of search** on the strength of a lottery record.
**VERDICT: MARGINAL** (bounded harm, wrong trigger). **Fix**: trigger the restart on a *measured*
statistic (e.g. the gate's paired margin against the record) rather than on the absence of a
lottery win, or accept the jump as a periodic reset and stop calling it a stall diagnosis.

### 1.5 `--real-gate-recentre 1` — the noise moves the optimizer

`recentre_due` `train.py:2310-2323`, `_recentre_on_record` `train.py:5160-5202`, called from
`train.py:5024-5027`. The decision: **one** consecutive periodic refusal puts the search centre back
onto the gated record. A periodic refusal is a single 24-game gate round (§2.1) whose false-refusal
rate under a null is ≈50 %. So a centre that is *exactly as good as* the record is thrown away with
probability ~½ every `--real-gate-every 50` generations.
**This is the single most consequential lottery in the trainer**, because it is the only one that
feeds noise back into θ itself: everything else mis-labels a checkpoint, this one steers the search.
It also explains the stepdyn finding directly — a centre that is repeatedly reset to a
noise-selected record cannot show directed drift, and measured drift/√gen is flat at 0.0033 with
Adam snr 0.17–0.19 *below* the 0.23 pure-noise expectation
(`docs/strategy/2026-09-09-plateau-review-verdicts.md` §0).
**VERDICT: LOTTERY.** **Fix**: `--real-gate-recentre 3` at minimum (three consecutive refusals is
p≈0.12 under the null instead of 0.5), and require the refusals to be *significant* refusals
(paired t ≤ −1.7), not merely `not accepted`.

### 1.6 The gradient estimate itself

`generation` `train.py:4915-4935` (antithetic pairs, CRN board seeds shared across the population),
`rank_normalise` `train.py:509-526` (ties share a rank — correct, and specifically guards against
the antithetic-sign bias), `shaped_advantage` `train.py:584-670`, `step` `train.py:4742-4790`.

The **construction** is sound: antithetic sampling, common random numbers, rank transform, decoupled
weight decay with bias exemption, Adam bias correction counted from the last moment clear.
The **magnitude** is not. Measured (`plateau-review` §0, `S/stepdyn`): per-block Adam
snr |m̂|/√v̂ = **0.17–0.19** against a pure-noise expectation of **0.23**, |step| = 0.22·lr, and
drift/√gen flat at 0.0033 across flow150–155 — i.e. at `--episodes 160–512` the centre is an
**Adam-floor random walk with no directed block**. Every per-generation ranking decision downstream
of this is a decision on noise.
**VERDICT: LOTTERY** (the estimator, at the episode counts actually used).
**Fix**: the only lever with the right sign is episodes per candidate — the noise falls as 1/√E, so
recovering a 2:1 snr from 0.18 needs ~E×100, which is not affordable. The affordable fix is to
**change the fitness to one with a smaller per-episode variance**: pinned boards (deterministic,
`--pinned-once`) instead of drawn ones remove the board and shop lotteries outright, which is why
`--shop-crn` (§1.8) was worth ±25k and why the pinned rungs are the right direction.

### 1.7 Fitness terms

* `--abs-weight` (default 0.6, live **0.0**): with the absolute anchor switched off the fitness is
  the margin sigmoid alone. `shaped_advantage`'s own docstring (`train.py:598-602`) records that the
  relative term measured −0.90 correlation with the *opponent's* coins and only +0.61 with its own —
  i.e. at `--abs-weight 0.0` the search direction is mostly "suppress the clone". **MARGINAL**: a
  live design choice, but it maximises the term with the worst measured alignment to the objective.
* `--margin-scale` (default 100000, live **3000**): the docstring argues *against* small scales
  ("at 25k … every margin sits in the flat tail and the relative term degenerates into the win bit").
  The live setting is 3000, i.e. 8× more degenerate than the value the docstring rejects. The term is
  effectively a win bit, so the fitness resolution per episode is 1 bit and the per-candidate SE at
  E=256 is 0.5/√256 = 0.031 — against antithetic fitness *differences* that the gradient needs to
  resolve at ~σ·‖∇‖ scale. **VERDICT: LOTTERY** (the configured value, not the code).
  **Fix**: `--margin-scale` at or above 25,000 restores resolution inside a win; or select on
  `softwin:<rung>:<tau>` which is the same idea with a bounded tail.
* `--d10-cash-weight` / `--tile-fill-weight` / `--late-price-weight`: all **0.0** in every launch
  script on disk, so inert. **SOUND** (not decided on).

### 1.8 `--shop-crn`

`Config.shop_crn` `train.py:396-414`. This is the *correct* class of fix and the model for the rest
of this audit: it identifies a ±25k zero-mean term in the antithetic fitness *difference* that has
nothing to do with either perturbation, and removes it from the training seat only while leaving the
shop distribution (and therefore the expectation of fitness) untouched. It is on in the live recipe.
**VERDICT: SOUND.** Note the docstring's own warning — never enable it for a fidelity gate.

### 1.9 Opponent / board sampling

* `largest_remainder` `train.py:685-702` and `SlotCarry` `train.py:714-786`: the token bucket fixes
  the real defect (a pure function of `(k, weights)` starved the tail of a 127-tape pool forever).
  Cumulative slots track the requested proportion to within one slot. **VERDICT: SOUND.**
* `opponent_slots` `train.py:787-860`: round-robin within group, `arch_frac` sets the group split.
  Deterministic, no draw. **SOUND.**
* **But**: the *residual* noise it leaves is the objective's non-stationarity. At `--arch-frac 0.9`
  with 47 tape rungs and 256 episodes (115 archetype pairs), each rung contributes ~2 episodes per
  generation, and `SlotCarry` deliberately **rotates which rungs get slots between generations**.
  CRN holds *within* a generation (the whole population plays one opponent list on one seed list,
  `SlotCarry` docstring `train.py:745-748`) but not *across* generations, so consecutive gradients
  estimate slightly different objectives. Per-rung fitness at 2 episodes has an SE of ~15–20k coins.
  **VERDICT: MARGINAL** — correct for coverage, but it means no single generation's gradient is an
  estimate of the run's objective. **Fix**: nothing to change in the allocator; the fix is to stop
  reading any single-generation number (`mean_win`, `best_win`) as evidence.
* `--arch-frac`: silently gave the tape block **zero** slots at 0.0 for flow123–127 (memory,
  `S/esdrift`), voiding those runs' verdicts. `_arch_frac_warning` `train.py:4619-4622` now warns.
  **SOUND after the fix**, and a standing reminder that a configuration bug is indistinguishable from
  a null result at this noise level.
* Board seeds: `seeds = self.rng.integers(...)` `train.py:4928`, one per slot, **shared across the
  whole population** — proper CRN. **SOUND.**

### 1.10 `mean_win` / `best_win` per generation

`train.py:5006-5008`, logged every generation over `--episodes` games against a rotating opponent
list. Rotation (§1.9) means successive values are not comparable, and the module docstring
(`train.py:14`) already records that `mean_win` "saturates in ~100 generations and then decays back
to 0.5". It is used by hand in the verdict log to kill runs ("flow128 killed at gen ~165", "the g130
re-centre … dropped mean_win 0.35→0.19"). **VERDICT: LOTTERY** as a kill criterion.
**Fix**: kill runs on the gate's paired record, never on `mean_win`.

## 2. The real gate (`RealGate`, `train.py:1833-3250`)

### 2.1 `beats` — the raw accept rule

`train.py:3003-3040`. With `--real-gate-min-gain 0.0` (the default *and* the live setting) the rule
is `win > ref_win or (win == ref_win and margin > ref_margin)` — **accept on any excess whatsoever**,
on `--real-gate-games 24`. Its own docstring at `accepts_result` (`train.py:3126-3137`) states the
problem out loud: "48 games resolve the win rate in steps of 1/96 and two records a step apart are
routinely the same policy measured twice" — and then resolves the tie on the *margin*, which is a
continuous statistic with a ~25k per-game spread and therefore never ties, so the tie-break decides
by coin flip whenever the win rates match.
Under a null candidate the accept probability of `beats` alone is ≈**0.5**.
**VERDICT: LOTTERY** in isolation. It is rescued in the live recipe only because
`--real-gate-paired-t 1.7` is `and`-ed onto it (`train.py:2705`).
**Fix**: never run the gate without `--real-gate-paired-t`; and set `--real-gate-min-gain` to a
non-zero value so the rule states a real effect size rather than "any excess".

### 2.2 `paired_stats` — the statistic

`train.py:1625-1699`. This is the **best-engineered statistic in the tree** and should not be
re-audited. It computes a one-sample t on per-game *differences* rather than on a win rate's
binomial, and it correctly treats **the two seats of a board as one observation**, averaging within
`(seed, opponent)` before taking the spread — the docstring cites the plateau review's probe that
took ten board outcomes from t=3.00 to t=4.36 purely by duplicating each into a second seat. It
returns `inf` only when the mean is non-zero and `0.0` when two thetas scored identically.
**VERDICT: SOUND.**

### 2.3 The gate's power, and its false-accept rate over a run

`--real-gate-games 24` over 8 opponents, both seats → **12 boards** for the provisional t.
`--real-gate-replicate-games 48` pooled with the provisional round → **36 boards** for
`_confirm_paired` (`train.py:2875-2909`), which additionally requires ≥2 paired rounds and a positive
pooled paired win difference. That two-stage design is correct and is not the problem.

The problem is arithmetic:

* **Size.** One-sided `t ≥ 1.7` at 11 df is p≈0.058; at 35 df, p≈0.049. Two independent stages ≈
  **0.003 per nomination**. But `--real-gate-every 50` over `--gens 30000` offers ≈**600
  nominations per run**, so a run makes ≈**2 confirmed false accepts** from pure noise, plus ~35
  provisional ones — and each provisional false accept is enough to trigger
  `--real-gate-recentre 1`'s counterpart, reset `periodic_rejects`, and move the bar.
* **Power.** At 36 boards, `t ≥ 1.7` detects a paired win-rate delta of `1.7·sd/√36`. With per-board
  paired win deltas in {−1, −0.5, 0, +0.5, +1} and the measured ~15/42 outcome-unstable share, sd≈0.35
  → minimum detectable effect ≈ **+10 win points on the 8 gate opponents**. Improvements smaller than
  that are invisible to the gate, and the campaign has been chasing 2–4 point moves.
* Consequently, at the plateau, an accept is **more likely to be a noise draw than a true +10-point
  policy** — the base rate of true +10-point moves is near zero while noise gets 600 tries.
* This is exactly what was measured: "gate-confirmed thetas (flow138 g10/g100/g200, flow141 g40)
  lose 2–4 pts on top10/jesse4 legs the 8-tape gate never plays" (memory, es-noise-floor).

**VERDICT: LOTTERY** (as a promotion oracle at the plateau; sound as a crash detector).
**Fix, in order of cost**: (a) reduce the number of tries — `--real-gate-every 250` cuts nominations
5× for free; (b) raise `--real-gate-paired-t` to 2.5 (size 0.009 → 0.0004 per stage); (c) the only
way to buy power is boards: 36 → 150 boards to see a 5-point move, which means
`--real-gate-replicate-games 300`. Do (a) and (b) now; (c) is the real answer.

### 2.4 Gate-opponent set vs. the legs

The gate plays 8 tape opponents (`--real-gate-opponent`, live: 6 loss tapes + 2 fixed). The judge
legs play different opponents, and the top-ten band appears in *neither* the training rungs nor the
gate. Memory records the consequence twice: gate-confirmed thetas lost 2–4 pts on legs the gate never
plays, and remote gate reads were a ±5–10 pt seed-set lottery (flow138 g10: gate +6.5, local −4.0,
hard tapes −6.3). A statistic measured on a set that does not contain the population you are
selecting for has an *unbounded* bias, not a noise level.
**VERDICT: LOTTERY** — and this one cannot be fixed by more games.
**Fix**: the gate opponent list must be a random draw from the same population the legs sample, or
the gate's verdict must never be reported as a strength claim. `launch_flow158`'s move (top-ten tapes
into training, 42 held-out as gate) is the right shape.

### 2.5 The pinned gate — `_decide_pinned` / `pinned_tally`

`_decide_pinned` `train.py:2740-2807` (rule at `train.py:2791-2793`), `pinned_tally`
`train.py:1572-1622`. The decision: `(flips - drops) >= min_flips and cand_wins > inc_wins`.

* **Statistic**: net flips on the pinned set. **Measured sd across 24 near-neighbour arms: 3.1**
  (mean +2.8, range 0…+12), and **every flip and every drop lands in the same 15 of 42 boards**
  (judge-calibration §TL;DR 1–2).
* **Threshold**: `--real-gate-min-flips`, **default 1** (`scripts/train.py:2136`), live launches use
  **3**. A bar of 1 is 0.3 σ below the arm-to-arm mean — it accepts essentially every candidate. A
  bar of 3 is *at* the arm-to-arm mean — it accepts ≈50 % of null candidates. The offline judge's
  `+6` bar is ~1 sd above the mean and still produced **0 true positives in 4 fires**.
* **Seat doubling**: at the default `--real-gate-pinned-seats 2` a pinned board that changes hands is
  worth **two** flips (`pinned_tally` docstring `train.py:1578-1581`), so `min_flips` is silently
  halved relative to `seats 1`. The live launches set `1`; the default does not.
* **VERDICT: LOTTERY**, at every bar tested.
* **Fix**: do not decide on net flips at all. The calibration already names the replacement: the
  paired **margin delta** on the 20 pinned games shared with the legs ranks arms at ρ 0.64–0.75
  against 0.36–0.50 for every held-out flip statistic, and it is already in every lossflip csv.

### 2.6 `--real-gate-fresh` and `--real-gate-seed-per-opponent`

`_fresh_base` `train.py:2545-2551`; the flags are on in every live launch. Fresh base seeds per round
stop a candidate from being selected on the base it was screened on; per-opponent seeds fix the
±9-pt board lottery that 16 shared boards produced. Both are correct variance-control moves that
cost nothing. **VERDICT: SOUND** — do not re-audit.

### 2.7 `_significant` refuses on a missing statistic

`train.py:3040-3075`: `stats is None` → **refused**, not waved through. Correct failure direction.
**VERDICT: SOUND.**

## 3. Decisions taken by hand in the verdict log

`S/glut/verdicts.log` (1,086 lines). `docs/strategy/2026-09-04-verdicts.txt` and
`2026-09-09-verdicts.txt` are byte-subsets of it (0 unique lines under `comm`), so all references
below are to the scratchpad log.

| # | line | decision | statistic as reported | noise | verdict |
|---|---|---|---|---|---|
| 3.1 | `:1028`, `:1007`, and the 09-09 07:20–09:02Z block | **ES arms killed on a 3-strike rule where each strike is a 42–62-board flip count** — flow152, flow155 (killed at gen 105 on a 12/42 vs 12/42 *tie*), flow156, flow158/159 strikes at ±0/+1 boards | net flips, bar ±1 board | net-flip sd **3.1**; a ±1-board strike is **0.3 sd** | **LOTTERY** — the arm-termination policy is a random killer. `:970` even kills flow149 in the same line that records the gate ACCEPTED it ("seed-set lottery") |
| 3.2 | `:73` indicting `:35,:45,:46,:56,:57,:64` | **six flow88–94 gate acceptances** at +2.1…+7.6 pts on n=144–192 | gate win-rate delta | the *identical* theta read **49.3 % vs 55.6 %** on two n=144 draws → same-theta seed sd ≈4.5 pts | **LOTTERY ×6**, retro-confirmed: all six later contradicted (`:43,:52,:58,:62,:65,:67`) |
| 3.3 | `:127` | the 16-shared-board leg: flow99_g250 **+289 t 0.2 / +2.1 pts** vs **+9.4 pts on the same base with 16 shared boards** | leg win delta | 16 effective boards | **LOTTERY, retro-invalidating** every leg verdict before `--seed-per-opponent` (~130 log lines of decisions up to 2026-09-05 02:00Z) |
| 3.4 | `:87` → `:100` | **flow93_g10 promoted then withdrawn in 70 minutes** | promotion pooled n=2,240 +1,906 t 3.9; withdrawal one band6 leg W16/L29, margin +262 **t 0.2**, −6.8 pts | McNemar se on 45 discordant = 3.5 pt → −6.8 is **1.9 se**; the three band win-deltas span **14.6 pts** | **LOTTERY** — the *withdrawal* was the weaker statistic and it won |
| 3.5 | `:446` | **shop-adaptive herd family CLOSED** | band6@777001 −2.3k **t −3.6**; @777002 +1.7k **t +2.1**; pooled ≈ −0.3k | pooled n≈512, se ≈575 → CI ±1,130 | **LOTTERY** — the log itself writes "opposite signs by base = lottery" and closes the family anyway |
| 3.6 | `:985` | **same-day-sale family closed, COLLECT_DROP turned off** | pinned +16/−5 (+1,010), held-out **+4/−0**; drawn band6 **−1,441 t −1.2** (CI ±2,350) | both sides inside noise; the +16/−5 is exactly the 15-board near-tie set | **LOTTERY both ways** |
| 3.7 | `:644`, `:660`, `:682` | three ES candidates **"LEVEL — not promoted"**, and the architectural conclusion "the ceiling is at the theta/search level, not the rung" | flow133_g100 +259 t 0.9 (McNemar z **1.04**); flow135_g40 +595 t 2.0 (z 0.88); flow134_g40 **+4 coins t 0.0** (z 0.62) | on 1,904 boards these nulls exclude only effects **> ±2.1 win pts** | **MARGINAL as verdicts, LOTTERY as an architectural conclusion** |
| 3.8 | `:70`, reused in plateau-review §5 | **HIRE_ROW_ON null used as a positive claim** ("execution waste caps at ≈2k and does not convert") | −378/game **t −0.75**, n=768 | se 504 → 95 % CI **[−1,366, +610]** | **LOTTERY** — a null that cannot exclude +610/game is not evidence of no effect |
| 3.9 | `:493` | **ADMIT7 "LEVEL, NOT PROMOTED"** | 1,904 boards, +188, sd 8,080, **t 1.0** → CI **[−175, +551]** | the CRN-sim prediction was **+427 — inside the CI** | **MARGINAL**: the engine did not refute the sim, it failed to resolve it |
| 3.10 | `:528`, `:513` | herd-latency **PARKED** at +261 (t 4.7 in the CRN sim); tomato-abstention **DEAD** at −135 (t −4.1 in the sim) | sim t's are real (sim paired sd ≈5,820) | to resolve +261 in the **engine** at 80 % power needs n ≈ **7,500–39,800 games**; −135 needs **28,000–139,000** | **SOUND in the sim, UNMEASURABLE in the engine** — correct to park, wrong to quote as engine facts |
| 3.11 | `:440` | **carrot family closed** | ALL n=384 −947 **t −3.19**; ≥3 sinks n=84 −3,469 **t −3.04** | the two "level" sub-cells (n=111 CI ±3.4k, n=189 CI ±2.6k) are unmeasured | **family closure SOUND; the per-sink-bucket sub-claims LOTTERY** |
| 3.12 | `:384`, `:835` | **hand ramp / crew ramp DEAD** | band6 **n=40** (55.0→52.5 % = one board) + top10 n=72 −4.3k t −3.0; later g350 −2,153 t −2.1 on 33 flips | n=40 → win CI ±15 pts | **MARGINAL** — carried by the t−3.0 leg; the band leg is decorative |
| 3.13 | `:12–:23` | SAME_DAY_FERT: intermediate "the ramp fix is real" on **n=32–36** (+6.3 / +6.2 win pts, margin t −0.3/−0.07) | later replicates −5,511 **t −3.4**, −5,339 **t −2.9** | n=32 → win CI ±17 pts | closure **SOUND**; the intermediate claims were **LOTTERY** |
| 3.14 | `:599` | CARROT_LATE_SEED **parked** | +247 **t 6.1** on the LIVE base, **−234 t −6.6** on the gen-130 base | two 6-σ results of opposite sign = base-conditional, not noise | **MARGINAL** — a measured +247 left unshipped |
| 3.15 | `:1068`, `:1082` | flow156_g20 **not promoted** despite held-out +6/−0 | six drawn legs down: band6 t −2.1, top10 **t −4.1**, flood6 t −2.5, jesse4 −11.0 pts **t −5.7** | refuting statistic far stronger than the supporting one | **SOUND** — the only recent non-promotion where the right statistic won |
| 3.16 | `:4,:268,:376,:386,:980,:1069` (melon), `:463` (JOINT_PLATE t −27), `:477` (CREW_FROM_TASKS t −28), `:553` (straw-first t −17/−19), `:311`, `:328`, `:399`, `:429`, `:394`; promotions `:190,:515,:540,:589,:615` (t 3.1–16.8 on 1,280–1,904 boards) | closures and promotions at |t| 4–28 | magnitudes far outside any noise | **SOUND — do not re-audit** |

Two structural notes from the same pass:

* **Null controls exist and work.** `sellcad_off` reproduces the base exactly (Δmargin 0 on all 84
  games), which is what proves the flip lottery is *board selection*, not run noise. And `em8`,
  `em10`, `emherd` return byte-identical reads (Δmargin −1,684 each) — three "arms" that are one arm.
  Any arm count quoted from the lossflip family must be de-duplicated first.
* **"LEVEL" almost never means "no effect".** On the harness's own sizes it means: n=192 band6 →
  cannot exclude ±2.4k/game; n=1,904 knob leg (sd 8,080) → cannot exclude ±360/game and ±2.1 win pts;
  n=384 CRN sim (sd 5,820) → cannot exclude ±580. Every "LEVEL" in the log should be read as
  "not measured below X", with X stated.

## 4. The local harness

### 4.1 `S/bank/paired.py:26-28` — **every published t is inflated by 1.40×**

The trainer fixed this in `paired_stats(group_seats=True)` (`train.py:1625`, §2.2). The local harness
never did: `paired.py` computes `sd` and `t` over **rows**, and rows are `(seed, opponent, seat)`
with the two seats of a board near-duplicates. Measured seat-identical rates on the judge legs:
72/96, 205/320, 45/64, 215/328.

| leg | rows | reported t | boards | board-level t | inflation |
|---|---|---|---|---|---|
| flow150_g40 band6@777001 | 192 | −2.14 | 96 | −1.51 | 1.41 |
| flow150_g40 top10@777001 | 640 | −4.52 | 320 | −3.23 | 1.40 |
| flow150_g40 jesse4@777001 | 128 | −4.28 | 64 | −3.03 | 1.41 |
| flow156_g20 today41@777001 | 656 | −2.09 | 328 | −1.50 | 1.39 |

Every t in `S/spo/*.out`, `S/judge/*.txt`, `S/legs/summary.txt`, `S/fert2/report.txt` and every
verdict-log line quoting them carries this factor. A "t 2.14, significant" read is really t ≈ 1.51,
p ≈ 0.13. **VERDICT: LOTTERY** (it converts non-results into results at the exact bar people use).
**Fix**: average the two seats into one observation before `stats()` (`paired.py:22-37`) — 3 lines,
and the trainer already has the reference implementation.

### 4.2 `S/spo/measure.sh:11,15,19` and `S/legs/legs.sh:11-16` — the drawn legs

`--games 16 --seed-per-opponent` (pairing is **on** — good). Sizes: band6 192 rows / 96 boards,
top10 640/320, flood6 192/96, wall6 192/96, jesse4 128/64, today41 656/328. Per-board paired sd
14,000–22,400 coins, consistent with the ±25k shop draw. Measured MDE at board-level t=2:
**band6 4,041–4,565**, top10 **2,159**, wall6 **2,862**.

* "band pooled +1.1k" is **0.27× the band6 MDE**. "band6 LEVEL" is unfalsifiable: anything from
  −4.0k to +4.0k reads level.
* Direct lottery evidence, one theta on three seed bases (`S/spo/f106g300.out:3-5`): band6
  **+736 (t +0.55)**, **−4,509 (t −3.67)**, **−338 (t −0.26)**. Between-seed sd of the leg mean is
  **2,870** against a within-leg SE of 1,342 — the printed error bar understates the real uncertainty
  of a "band6 verdict" by ~2.1×, **and the sign flips**.
* Two arms were killed on it: `S/spo/f112g10.out:6` ("cut: rejected on band") and
  `S/spo/f106g90.out:5` ("cut at 13:30Z: g90 rejected on the band") — while their **top10 legs read
  +3,572 (t 4.62) and +3,324 (t 4.35)**. A 96-board leg overruled a 320-board leg.
* Independently confirmed: band6@777001 ρ **0.13** and jesse4 ρ **0.07** against the pooled read,
  vs today41 0.83 / top10 0.85 (judge-calibration §5).

**VERDICT: band6 and jesse4 as accept/reject legs = LOTTERY; top10 / today41 = MARGINAL (sound for
effects ≥ 2k).** **Fix (free)**: decide on **top10 + today41 pooled** (648 boards, MDE ≈ 1.2k) at
board level; keep jesse4 only as a catastrophe veto; stop reading band6 as a verdict.

### 4.3 `S/lossflip/flips.py:16-17,31` + `S/judge/judge.sh:15-16,19` — the flip count

Held-out 42 ids = 76–84 games from ~160 pinned tapes (`lossflip/run.sh:10`, `--games 1`). Pinned
boards are deterministic, so pairing is exact and run noise is zero — **the noise is board
selection**. Structure: 46 frozen losses + 6 frozen wins + 20 volatile losses + 12 volatile wins;
only **16 boards ever move**, and 30/42 boards give byte-identical margins in both seats, so each
moving board is worth exactly ±2. H_net across 27 non-melon arms: **mean +2.0, sd 3.7** (24-arm
figure: mean +2.8, sd 3.1). An independent Poisson-binomial check from the per-board flip
probabilities predicts sd = 2×1.27 = **2.5**, matching.

The bar was **≥ +3** (`judgecal/judge.sh.bak:12`) and then **≥ +6** — i.e. at, then one sd above, the
mean of a pure-noise process; **25 % of arms clear +6 by chance**. Median |base margin| on games that
actually changed hands: flow156_g20 **1,084**, flow150_g40 **1,604**, flow130_g260 **1,768**,
flow155_g50 **1,973**; and 24/26, 29/34, 28/30, 25/31 of moved games sit under 5k. **Every flip is
decided inside 10–20 % of one shop draw.**

**VERDICT: LOTTERY.** Already demoted to a printed screen in `flips.py:32-39` / `judge.sh:19-21` —
correct. The honest statement is "H_net is uninformative", not "H_net ≥ 6 is weak evidence".

### 4.4 `S/judge/judge.sh:21` — the replacement gate is better, unvalidated, and has two live bugs

Accept iff `LEG20 d-margin > 0 AND H_dm >= 0`. LEG20 is the paired Δmargin over **20 pinned games**
(10 tapes × 2 seats). Its ordering evidence is ρ 0.64–0.75 at **n = 7 arms, p ≈ 0.07**, with **no
positive control** (all 7 arms are losers), and the 5 % critical value at n=7 is **0.786** — nothing
clears it. Its own per-arm noise is unmeasured: 10 boards at ~4,240 perturbation sd → SE ≈ **1,340
coins**, so a `> 0` threshold is a coin flip for any near-neighbour arm, and the observed LEG20
values (−181 … −1,243) all sit inside 1 SE of zero.

* **BUG A** (`judge.sh:17-18` with `lossflip/run.sh:11`): `run.sh` **appends** to `$name.summary` and
  never truncates, while `judge.sh` greps `-m1` — the **oldest** line. A re-run makes the gate read a
  stale LEG20/H_dm. `S/judge/flow156_g20.txt:15-23` shows it happening: two stacked summary blocks,
  `LEG20 d-margin NA`, `LEGS SKIPPED`.
* **BUG B** (`judge.sh:21`): a regex miss yields `NA`, which the gate treats as **reject**. A
  formatting change silently rejects every candidate without saying so.

**VERDICT: MARGINAL / UNVALIDATED.** **Fix**: truncate the summary (or `tail -1` the grep); make `NA`
an error rather than a rejection; do not treat `LEG20 > 0` as a promotion gate until the 13-arm
power-up (`judgecal/chain_now.sh`) lands.

### 4.5 `S/fert2/` — the knob probe

`run.sh:10` has **no `--seed-per-opponent`**: four opponents share one seed set (384 rows, 192
boards, 122/192 seat-identical). Gate (`report.txt:9-14`): promote iff **ALL ≥ +1,500 AND t ≥ 2 AND
kagg2 ≥ −1,000**. Measured board-level MDE at t=2 is **1,356** (base) / **1,059** (marginal), so the
**+1,500 ALL bar is correctly set at ~1× MDE — this is the best-calibrated bar in the harness**, and
both arms correctly failed. But the **per-opponent `kagg2 >= −1,000` guard** is read off 96 rows /
48 boards with MDE ≈ **2,900**: its threshold is **one third of its own MDE**, a pure coin flip, and
it is what tripped "fails hard on kagg2" and skipped replication (`report.txt:18-19`).
`agg3.py:19,44-48` reports every ledger metric as a bare `mean` with **no sd and no n** — the
counterfactual-ledger family already killed six times.
**VERDICT: ALL-row gate SOUND; the per-opponent guard LOTTERY; `agg3.py` ledger means LOTTERY.**
**Fix**: drop the per-opponent guard or raise it to −3,000; add `--seed-per-opponent`; never print
`agg3.py` means without an interval.

### 4.6 The two-purse rule (`d ours` / `d theirs`)

Rule text at `S/carrotfloor/results.md:212-216`, `S/strawfirst/results.md:89`,
`docs/strategy/2026-09-09-verdicts.txt:228`. The statistic is `paired.py:31-32`'s `d_ours` /
`d_theirs` columns — and **`paired.py` prints no sd and no t for either purse**; only the margin gets
an error bar. Whole knob families are routed to "denial" or "displacement" on numbers with **zero
uncertainty attached**. Worked example: `verdicts.txt:228` sell-cadence, "n 322 … d-ours +33
d-theirs +321" — n=322 rows ≈ 161 boards, SE(d_theirs) ≈ 20,000/√161 ≈ **1,576**, so **+321 is
0.20 SE**. The 576-board CRN-sim reads (`carrotfloor/results.md:113-114`, +109 / +224 against a
margin sd of 1,083–1,402, SE 45–58) are real *in the sim*, but the sim is 4.6× quieter than the
engine, so they do not transfer.
**VERDICT: LOTTERY on engine legs; MARGINAL on the CRN sim.** **Fix**: add sd/t columns for
`d_ours`/`d_theirs` to `paired.py:58-61` and require |t| ≥ 2 on the purse before naming a signature.

### 4.7 The packaging smoke test

`scripts/eval_vs_baselines.py:389,403`; outputs in `S/smoke_f*/smoke.log`. n = **8 games**: 4 vs one
tape + 4 vs `starter`, and each 4 is 2 seeds × 2 seats → **2 boards per opponent** (seat rows are
byte-identical, `S/smoke_f130g260/smoke.csv:4-5`).
`docs/strategy/2026-09-08-how-we-built-the-agent.md:250` cites "**4/4** versus tape 105443859
(+8,732)" as upload evidence. The counter-example is on disk: `S/smoke_f135g200/smoke.log:2` reads
**win 50.0 %, worst −2,505** on the same tape for a sibling theta. Two boards carries ≈2 bits.
The `starter` half is different: margins +117k…+158k, ~15σ.
**VERDICT: "4/4 vs the tape" = LOTTERY as a quality claim; "0 nulls / DONE / beats starter" = SOUND
as a plumbing check.** **Fix**: report the smoke as pass/fail on plumbing only and drop the tape
win-rate line — the legs already answer the quality question.

## 5. Items that are SOUND — do not re-audit

`paired_stats(group_seats=True)` (`train.py:1625`); `rank_normalise` tie handling
(`train.py:509`); antithetic + shared-CRN board seeds (`train.py:4917-4928`); `--shop-crn`
(`train.py:396-414`); `largest_remainder` (`train.py:685`) and `SlotCarry` (`train.py:714`);
`_significant`'s refuse-on-missing-statistic (`train.py:3040`); `--real-gate-fresh` and
`--real-gate-seed-per-opponent` (`train.py:2545`); `_confirm_paired`'s three conditions
(`train.py:2875`); `_replicate_record` (`train.py:5081`); decoupled weight decay with the bias
exemption and the `adam_t` bias correction (`train.py:4742-4790`); the `--seed-per-opponent` leg
harness (`S/spo/measure.sh:11`); the `S/fert2` ALL-row `+1,500 / t≥2` bar; the smoke test's
plumbing half; and every verdict-log closure or promotion at |t| ≥ 4 on ≥ 1,280 boards
(`:190, :463, :477, :515, :540, :553, :589, :615, :980, :1069` and the melon lines).

## 6. Ranked lottery table

| rank | site | statistic | threshold | noise | why it is worst |
|---|---|---|---|---|---|
| 1 | `train.py:2310-2323` + `:5024` — `--real-gate-recentre 1` | one periodic gate refusal | K = 1 | a single 24-game round refuses a null candidate ~50 % of the time | the only site where noise **steers θ**; it manufactures the measured Adam-floor random walk (snr 0.17–0.19 < 0.23) |
| 2 | `S/bank/paired.py:26-28` | paired t over **rows** | \|t\| ≥ 2 | seats are near-duplicates → **t inflated 1.40×** | silently converts every p≈0.13 into a "significant" result across the whole harness and verdict log |
| 3 | `train.py:2791-2793` / `S/judge/judge.sh:15-19` — net flips | flips − drops | `min_flips` 1 (default) / 3 (live) / +6 (offline) | **sd 3.1**, all flips in 15 of 42 boards, flips decided by <2k coins | **0 true positives in 4 fires**; 25 % of arms clear +6 by chance |
| 4 | `train.py:5514-5522` — `_accept_best` | max over a noisy sequence | `--best-margin 0.005` = **0.14 SE** | E[max of 3,000 readings] ≈ 3.5 σ ≈ +0.13 | the record `--promote` ships is the run's luckiest reading |
| 5 | `train.py:3003-3040` — `beats` | any excess on 24 games | `min_gain 0.0` | accept prob ≈ 0.5 under the null | only survivable because `--real-gate-paired-t 1.7` is and-ed on; never run without it |
| 6 | gate power (`train.py:2705`, `:2875`) | paired t on 12 → 36 boards | t ≥ 1.7 | MDE ≈ **+10 win pts**; ~600 nominations/run → ≈2 confirmed false accepts | at the plateau an accept is more likely noise than signal |
| 7 | `S/spo` band6 / jesse4 legs | leg Δmargin | "level"/"rejected on the band" | MDE **4.0–4.6k**; same theta reads +736 / −4,509 / −338 | killed two arms whose 320-board top10 legs read t +4.4 to +4.6 |
| 8 | verdict-log 3-strike arm kill (`:1007`, `:1028`) | net flips per strike | ±1 board | 0.3 sd | a random arm killer running continuously |
| 9 | `train.py:5006` — `mean_win`/`best_win` per generation | one generation on a rotating rung mixture | used by hand to kill runs | non-stationary objective; docstring says it decays to 0.5 anyway | |
| 10 | `--margin-scale 3000` (`train.py:598-609`) | fitness resolution | — | degenerates the relative term to a win bit, 8× worse than the value the docstring rejects | halves the information per episode at the noise floor |
| 11 | `S/fert2` per-opponent `kagg2 >= −1000` guard | 48-board mean | −1,000 | MDE **2,900** | threshold is ⅓ of its own MDE |
| 12 | two-purse `d_ours`/`d_theirs` | no sd, no t printed | sign | ~0.2 SE on engine legs | routes whole knob families on unquantified numbers |
| 13 | `S/judge/judge.sh:21` — `LEG20 > 0` | 10-board Δmargin | 0 | SE ≈ **1,340**; fitted at n=7, p≈0.07, no positive control | the replacement judge is a zero-threshold sign test |
| 14 | packaging smoke "4/4 vs the tape" | 2 boards | 4/4 | ~2 bits; a sibling theta reads 50 % | cited as upload evidence |

## 7. The three fixes worth doing first

1. **Average the seats in `S/bank/paired.py:22-37`** (3 lines; `train.py:1625` is the reference).
   Every t in the harness and the verdict log is currently 1.40× too large, right at the bar people
   act on. Nothing else in this audit can be trusted until this is done.
2. **`--real-gate-recentre 3` with a significance condition, and `--real-gate-every 250`.** Recentre
   is the only path from gate noise into θ, and 600 nominations per run is 600 lottery tickets.
   Together these cut the false-accept exposure ~30× at zero compute cost.
3. **Retire net flips and band6/jesse4 as accept/reject statistics.** Decide candidates on
   **top10 + today41 pooled at board level** (648 boards, MDE ≈ 1.2k, ρ 0.83–0.85 with the pooled
   read) and use the pinned set only for the LEG20 margin diagnostic — never as a gate until the
   13-arm calibration lands.
