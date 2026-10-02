# Runtime selection among complete day plans — bounded feasibility review

Date: 2026-09-12. Scope: read-only review of `arms-next` and preserved
development evidence. No policy, simulator, evaluation, corpus, or submission
file was changed or run.

## Verdict

This is a **new decision interface**, not an already-tested name for ISEARCH,
theta soup, forward-admit, or wall imitation. It is implementable cheaply only
as an **observation-only gate over 2–4 plans that the existing NumPy planner has
already made feasible**. An exact short rollout from a live observation is not
currently implementable: the simulator needs opponent-private state that the
observation correctly withholds, and there is no observation-to-`sim.State`
constructor.

The evidence does not refute conditional selection. It does refute treating a
small fixed perturbation as an unconditional improvement. The honest next
measurement is therefore an offline oracle-ceiling plus cross-fitted
observation-only selector on development states, before any runtime code. A
positive oracle without out-of-fold predictability is a refusal.

## What exists, and what does not

At day hour 0, `agent/runtime.py:29-35` does exactly

```
view = parse.parse_view(obs, player)
macro = macro_fn(obs, player, view)
plan = plan.build_day(np, view, macro)
```

and caches the six plan arrays for the other 23 turns. The packaged `macro_fn`
constructs `brain.PolicyObs` from the same observation and calls
`brain.decide(np, theta, po)` (`scripts/package_submission.py:127-153`). The
natural insertion point is between `macro_fn` and the single `build_day` call:
produce candidate `Macro`s, call `build_day(np, ...)` once per candidate, score,
and cache the selected complete tuple. `render.turn_action` already consumes
that tuple without knowing how it was chosen.

`build_day` is the required feasibility boundary. It derives purchases,
enumerates hire counts, admits tasks, routes units, reserves cash, and allocates
sales for one `Macro` (`core/plan.py:5745-5762,5876`). Those internal argmaxes
are search *inside one plan*. The architecture never creates multiple complete
plans and never predicts their resulting next states. `build_day_stats` merely
returns overflow destroyed, purchase shortfall, and dropped task value from the
same planner calculation (`core/plan.py:3418-3430`); it is diagnostic, not an
outcome or opponent-response value function.

The nearby closed experiments answer different questions:

* **ISEARCH** applies one pre-registered integer offset table to B's decoded
  `Macro`, fixed across boards for the named day window. Each variant plays its
  choice unconditionally for the season. It tested local actions, not a gate or
  within-state counterfactual comparison (consensus §76;
  `2026-09-11-integer-search.md`).
* **Theta soup/extrapolation** chooses one fixed theta before the game. Its
  mixed family results establish drift/local-peak evidence along those theta
  directions, not the absence of statewise ranking reversals (consensus §46).
* **Forward-admit** projects a wider future task curve only into the hire scan;
  the executed pass remains today's single plan. Its losses reject that hiring
  rule, not choice among complete feasible plans
  (`2026-09-10-forward-admit.md` and
  `2026-09-10-forward-horizon-feasibility.md`).
* **Wall imitation** replaces observation-dependent integers with a pinned
  per-day plate. It proved the copied plate bad; it contains neither competing
  plans nor an observation-dependent selector (consensus §70;
  `2026-09-11-wall-imitation.md`).

The current policy is already observation-dependent and already sees current
money, shed, seeds, both public farms, public crop clocks/yields, market
inventory/prices, and shops (`core/brain.py:80-125`). Its forward-production
features price both standing boards at current quotes (`brain.py:430-519`). A
new selector must beat that learned state response; merely re-expressing its
features around the same planner score is likely redundant.

## Why an exact live rollout is unavailable

`parse.parse_view` reconstructs the planner's own tile state, shed, seeds,
money, public market and `opp_commit` (`agent/parse.py:23-113`). This is enough
to build feasible plans. It is not a simulator state.

`sim.State` additionally carries both seats' full shed and seed vectors,
per-unit inventories and insertion order, unit positions, hand counts, hires,
plant lifetime clocks, and market/town state (`sim/state.py:40-75`).
`sim.initial_state` is the only constructor; searches find no `from_obs` or
reconstruction path. A current raw observation can recover more of **our**
state than `DayView` keeps, including our unit positions and private
inventories. It cannot recover the opponent's shed, seeds, carried inventories,
inventory insertion order, or future plan. Those fields affect purchases,
shed overflow, drops, and shared-market clearing.

Therefore `sim.rollout.run_day` (`sim/rollout.py:207`) cannot be called
exactly at runtime from the observation. Filling hidden opponent fields with
zero, a prior, or sampled beliefs is permitted, but it is an approximate model
whose ranking must survive across those assumptions. Reading the opponent's
actual hidden shed/inventories, replaying its future tape as a runtime input, or
importing the true saved simulator state would be privileged-state selection.
Future weed/shop RNG words are likewise unavailable and may only be sampled.
Public opponent tiles, their clocks and standing yield are allowed because the
current observation contains them.

JAX is also the wrong live backend: the submission is deliberately pure NumPy
and never imports JAX (`GOAL.md:159-179`). The archive calls the NumPy planner
microsecond-scale but gives no measured 2–4-plan latency. Thus runtime cost is
currently **unmeasured**; it should be timed on recorded dawn observations.
Two to four `build_day(np, ...)` calls multiply the only expensive hour-0 path,
while all later turns remain cached. A JAX branch rollout would add compilation
and package dependencies and is not a faithful solution to missing state.

## Cheapest discriminating measurement

Do this on development data only, with candidate generation and features frozen
before reading outcomes:

1. Define 2–4 deterministic candidate `Macro` transforms. Include B. Each arm
   must pass through the unchanged NumPy `build_day`, and byte-identical B must
   remain one candidate. Reject duplicate six-array plans before scoring.
2. In an **offline diagnostic**, branch saved simulator dawn states for one day
   under common randomness and the same opponent process. Full state and future
   opponent actions may be used only to create counterfactual target labels or
   an explicitly named oracle ceiling; they must not be selector inputs.
3. Train or specify a tiny gate using only fields constructible from the current
   `PolicyObs`/`DayView`, then report leave-tape-out predictions. Keep families
   separate. Do not key on tape id, seed, future shop/weed draws, future market
   inventory, opponent action rows, or opponent-private state.
4. Compare three values: always-B, the unattainable oracle max, and the
   out-of-fold gate. Also time 1/2/4 NumPy `build_day` calls. Continue only if
   the oracle is material **and** the permitted-observation gate captures a
   stable fraction on each development family.

There is already a cheap warning and a reason to measure. On the preserved
ISEARCH development CSVs, `S/isearch/t2.csv` and `S/isearch/lc.csv`, a
descriptive oracle choosing B or the best of all 24 full-season variants
separately per board would add **+2,049.9 coins/board on TOPB2 dev (18/20
boards positive; 40 seat-games)** and **+1,131.8 on LIVE-C dev (27/30 boards
positive; 60 seat-games)**. As in `S/isearch/pair_multi.py`, the two seat-games
for each `(tape, seed)` are averaged before comparison. The calculation is:

```bash
JAX_PLATFORMS=cpu .venv/bin/python - <<'PY'
import collections, csv, numpy as np
for path in ("S/isearch/t2.csv", "S/isearch/lc.csv"):
    d = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in csv.DictReader(open(path)):
        d[r["theta"]][r["tape"], r["seed"]].append(float(r["margin"]))
    g = {n: {k: np.mean(v) for k, v in z.items()} for n, z in d.items()}
    keys, names = sorted(g["base"]), [n for n in g if n != "base"]
    gain = np.array([[g[n][k] - g["base"][k] for k in keys] for n in names])
    envelope = np.maximum(0, gain.max(axis=0))
    print(path, len(keys), envelope.mean(), int((envelope > 0).sum()))
PY
```

This is an optimistically biased maximum over 24 outcomes, uses season-level
variants rather than day choices, and is not a selector result. It only proves
that the negative variant means conceal ranking reversals. Independently,
consensus §63 measured about **+530/board** for an outcome-oracle side of one
day-0 switch on LIVE-C while the same switch was bad unconditionally. Neither
number supplies an observation-only predictor.

So material upside remains possible but unproved. B's coarse decode has very
little within-day board variation, and the local offsets, wall, soup, and
forward-admit families all failed as fixed choices. That makes a naive plan
score a low-probability route. The proposal remains open precisely at the one
untested link: whether current public state predicts which of a few *complete,
feasible* plans wins often enough out of fold. The measurement above answers
that before taking on a partial-observability model or changing production.
