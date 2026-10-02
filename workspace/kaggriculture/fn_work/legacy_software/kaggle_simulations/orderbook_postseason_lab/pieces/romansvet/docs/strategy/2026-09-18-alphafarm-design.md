# ALPHAFARM — expert iteration (AlphaZero-style) on the shipped theta: design + price

2026-09-18, branch `alphafarm`. Backup path to top 5 if WINRATE stalls. Design only, nothing built.
Read with [[rlprobe]], [[rlprobe2]], [[mpcfeas]], [[p4premise]], [[goalaudit]], [[esfix]].

## 0. The design in four sentences

At each dawn of a training game, sample `K` candidate `plan.Macro`s around the one the current theta
emits, roll each to game end in the JAX sim with the *same* theta playing the continuation and the
*same* tape opponent and shop stream (CRN), score two-purse (`ours − theirs`), commit the best, and
record (dawn state → best macro) as a label. That is **sampled policy improvement at depth 1**, not a
tree: the action is ~40 correlated ints and the chance node is the 3-daily shop draw, so a tree has
nothing to expand — the continuation *is* the policy, which is what makes rounds compound like policy
iteration. Between rounds, fit theta by supervised regression of `brain.decide`'s **pre-quantisation**
outputs onto those labels (`plan.py` is never in the loss — it is the environment). The signal is
genuinely different from ES/WINRATE (30 dense, credit-assigned, CRN-paired action labels per game vs
one scalar per candidate theta per generation), but the **action space is the same `Macro`** ESJUDGE9
closed on every mask and fitness — which is what the falsifier tests, first and cheaply.

## 1. Search at training time

* Shape: `K` candidates = the policy's macro + small integer jitter on `plant_target[5]`,
  `animal_want[3]`, `crew_target`, `hire_bias`, `land_bias`, `grow_mult[9]`, `fert_defer`. Dawns run
  **sequentially**: search day `d`, commit, advance, search `d+1`. Target = argmax (round 1) →
  softmax-weighted later (temperature on the two-purse margin).
* Cost: a rollout from dawn `d` is `(30 − d)/30` of an episode, so a game costs
  `30 · K · S · 0.5 ≈ 15·K·S` episode-equivalents (the naive 30·K·S is the untruncated bound).
  `K=8, S=4` → **480 eq-episodes per training game**.
* Throughput (measured, current recipe): pop 1024 × `--episodes 54` in **180.2 s/gen** = 55,296
  eps/gen = **307 eps/s per arm** with two arms sharing the host (single-arm historical ceiling
  1,476 eps/s at pop 512 × 160 / 55.5 s, 09-10 recipe; first gen pays ~390 s of XLA compile).
  Local CPU is 5.1 eps/s ([[rlprobe]]) → **everything here runs remote, as a script**.
  At 307 eps/s and 480 eq/game: **2,300 training games/h** (1,150/h at the untruncated bound).
* Value net: inputs are the `PolicyObs` scalars (`day, money, opp_money, nquad×2, seeds[5], shed[12],
  mkt_inv[9], price[9], shops[8]` + whole-array reductions of `kind/occ/t_day/t_yield`, since
  `brain.py:83` forbids per-tile indexing), i.e. reuse `brain.features`; target = the final
  `ours − theirs` of rollouts already run (labels are free). **It cannot replace the rollouts**:
  candidate spreads at one dawn are a few hundred coins against a shop-lottery sd of
  1,857/game ([[mpcfeas]]), so ranking needs value RMSE ≲ 200 — implausible. Use it only to *prune*
  (`K=16` → roll out the top 4): a ~4× cut, not 1000×. Not on the critical path.

## 2. Policy update

* `brain.decide(xp, theta, obs)` is `xp`-generic and already runs under `jnp` inside the sim
  (`rollout.py:277`), so it traces under `jax.grad`. Differentiable: `PO.unpack` → `PO.forward` →
  `out.scores / head / aux / crew` → `sig(...)`, `_softmax`, `tanh` — all smooth in theta.
  **Not** differentiable: `_qfloor` (`brain.py:961`, a floor), `.astype(int32)`, `_largest_remainder`
  (two `argsort`s), saturated `clip`, and the switch genes' thresholds.
* So the loss lives on the continuous quantities *just before* each `_qfloor`: `land_frac`,
  `dev_frac`, `animal_share`, the animal softmax `wa`, the crop shares, `hire_bias`/`grow_mult`
  pre-floor. Target transform: label `n` from `floor(f·x)` becomes the **bin** `[n/x, (n+1)/x)` with
  an in-bin Huber (zero inside, distance to the nearest edge outside) — exact, since any `f` in the
  bin reproduces the searched macro. Theta is flat, ~7,626 params, Adam, full batch.
* `plan.py` stays **out of the loss** (it is the environment that consumes the Macro); the sim is
  never differentiated. Output is an ordinary theta → ships and is judged through the existing
  `S/judgekit/judge.sh` / BAND250 path, and can also seed an ES run.

## 3. Opponents

Falsifier and round 1: **100 % tape seat** (`rollout.episode(..., tape=, tape_ctl=)`, seat 1 replays
recorded frames). Campaign: **≈ 85-90 % tapes** — inside that ~60 % BAND250 clone tapes
(`S/carrotflat3/band250_ids.txt`, the 60-75 % of live games), ~40 % engine tapes with the 38 losing
gated boards oversampled ~2× since the loss tail is the target ([[goalaudit]]) — and **≤ 10-15 %
self-play**, never 0.5: `--arch-frac 0.5` plus a win-shaped fitness is the flow222 collapse (−18,661,
[[esfix]]). A tape cannot react, so search will find macros that exploit a frozen seat: every score is
two-purse and any label with `d_theirs > 0` is dropped — the gift channel as a training constraint.

## 4. Chance

`--shop-crn` (`rollout.episode(shop_crn=True)`) moves the 3-daily `choice(SHOPS)` off the weed walk's
moving cursor, so candidates that plant differently still draw the same shops — CRN is valid and the
paired difference loses most of the 1,857 sd. Rule: pick `S` for a per-candidate SE < 300 coins; with
CRN expect **S = 4-8**, without it `1857/√S < 300` → S ≥ 38, unaffordable. The falsifier reports the
realised paired sd, so S is set from data, not from this estimate.

## 5. Throughput, calendar, and the first falsifier

* One round, `K=8, S=4`, 64 games = **30,720 eq-episodes ≈ 100 s of GPU** (+ ~390 s compile, once),
  yielding 1,920 labelled dawns; a 100-round campaign = 3.1 M eps ≈ **2.8 h on one GPU**. A fatter
  recipe (`K=16, S=8`, 256 games/round = 492k eps) is 27 min/round → 30 rounds in 13 h. Search is
  *not* the bottleneck; label quality and distillation transfer are.
* Measurable change after 3-5 rounds (5,760-9,600 labels), a shippable theta after 20-50. Calendar:
  falsifier today, tasks 3-4 one day, campaign ≤ 1 day of GPU → judged candidate 09-21/22, eight days
  before the 09-30 final submission.
* **FIRST FALSIFIER (run before anything else is written).** `S/alphafarm/search_probe.py`: 24 boards
  (12 gated engine tapes drawn from the loss tail + 12 BAND250), `K=8`, select on `S=4` seeds,
  **evaluate the committed trajectory on a held-out seed**, paired against the pure-policy trajectory
  on that same seed. **BAR: mean Δmargin ≥ +1,000/board, Δtheirs ≤ 0, t ≥ 3.** Also report the
  *oracle* (select seed = eval seed) as the upper bound: a big oracle with a zero held-out read is the
  MPCFEAS lottery (argmax agreement 0.20 vs chance 0.25) and kills the path exactly as PLANSELECT
  died. Haircut for pricing: distillation returns 30-60 % of the search gain, so a gain under +2,000
  cannot fund a +1,000 ship.

## 6. Implementation plan (5 tasks, ≤ 3 h each)

1. **`S/alphafarm/search_probe.py` (3 h) — the falsifier.** Copy the harness of
   `S/simscreen/screen.py:165-240`: `tape_ids` / `tape_path` / `TA.load|stack|device`,
   `build_tables(jnp)`, `eod.weed_threshold()`, `eod.host_stream(seed, day)`, board = (tape, seed, seat).
   Step the season with `rollout.run_day(tables, st, d, w[d], hi_t, lo_t, th, shop_crn=True, tape=dev,
   tape_ctl=c, tape_turns=turns)` in a `lax.scan` — carrying `st` **is** the resume-from-dawn
   primitive, so no new sim code and no `episode()` change. Macro injection: monkeypatch
   `kagg3.core.brain.decide` with a wrapper that calls the original and then
   `macro._replace(field=jnp.where((obs.day == d_inject) & (seat == 0), cand, base))`; the candidate
   reaches the wrapper as a closure over the vmapped argument of `one(th, w, c, cand)` (correctly
   batched, since vmap traces `one` with batched tracers). Fallback channel if that is awkward:
   pad `theta` past `N_PARAMS` and read the tail (`PO.unpack` slices fixed offsets). Output CSV:
   board, seed, chosen index per dawn, `d_ours`, `d_theirs`, `Δmargin`, paired sd.
2. **Run + read (2 h).** Hand the script to the remote GPU (it is ~2-5 min of GPU, it can share a
   card with a WINRATE arm). Apply the §5 bar. NO-GO here ends the path at a cost of one day.
3. **`S/alphafarm/soft_decide.py` (3 h).** `decide_soft` = `decide` up to each `_qfloor`, plus the
   bin-target transform and in-bin Huber. Test: re-quantising it reproduces `decide` on the 2,400
   fixture decisions of `tests/test_backend_agreement.py` (that file only, never the full suite).
4. **`S/alphafarm/ei_train.py` (3 h).** Round loop: generate (task 1 machinery, 64 games) → labels →
   Adam on theta (~200 steps) → paired judge of `theta_{k+1}` vs `theta_k` on 60 held-out pinned
   boards; stop after two rounds that fail to improve that pair.
5. **Ship path (2 h).** `S/judgekit/judge.sh LEGS=abce` + BAND250 (≥ 250 band boards per sign), §115b
   bar (POOLED ≥ +450, t ≥ 3, `d_theirs ≤ 0`), then `scripts/package_submission.py` + smoke.

## 7. Verdict — **GO on tasks 1-2 only.**

 The trainer is cheap (2.8 h of GPU for 100 rounds) and its learning signal
is genuinely different from ES, so it is a legitimate backup — but it searches the Macro space
ESJUDGE9 closed and inherits the lottery that killed PLANSELECT and MPCFEAS. One day buys the answer;
do not write tasks 3-5 until the search gain clears +1,000 on held-out seeds.
