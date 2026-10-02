# GOAL — Kaggriculture agent via OpenAI-ES

**Competition:** https://www.kaggle.com/competitions/kaggriculture/overview

## Objective

Reach the **top five on the final leaderboard** in Kaggle's Kaggriculture
simulation competition with an agent whose entire strategy is **learned from game
outcomes alone** — no hand-written strategy, no labelled data — and
whose runtime behaviour is **deterministic and microsecond-scale**.

**Lead decision 2026-09-14 (user delegated the path choice):** top-five action tapes
may be used as **initialisation and macro targets only** (seed thetas, macro-plan
trajectories, executability tests). Promotion stays outcome-only: the seven-family
pinned-tape judge and rule §115 (pooled band ≥ +450 coins, t ≥ 2). Rationale: every
lever near B is closed and the ES cannot climb out of B's basin at training sigma
(crop mix 70 sd, herd 7-14 sd, sale day no gene); the top five play a different
build, so the search must start where that build is expressible.

## Current working rules and existing tools

User direction, updated 2026-09-13: move quickly toward wins using the established
evaluation protocol. Reuse existing tools before writing a helper or reaching for
general web search. Read the applicable tool's arguments and current source first;
older scripts may have fixed inputs or historical defaults.

| Task | Existing tool or entry point | Use |
| --- | --- | --- |
| Kaggle CLI | `.venv/bin/kaggle -W competitions episodes SUBMISSION_ID --format json`; `.venv/bin/kaggle -W competitions replay EPISODE_ID -p OUTPUT_DIR` | Installed commands verified with local `--help`. Also exposes submissions, leaderboard, logs and submission limits. Use existing CLI/API tools for Kaggle data rather than general web search. |
| Current Kaggle episodes and leaderboard | `S/ladder2/capture_snapshot.py OUTPUT_DIR`, `S/ladder2/summarize_snapshot.py SNAPSHOT_DIR` | Paced public API reads for the configured B/hr submissions and competition; use a fresh directory. Do not replace this with web search or overwrite older captures. |
| Public replay download | `S/rotband/download.py`, `S/rotband/rate_limit.py` | Existing downloader uses `S/rotband/epseat.txt` and its replay cache. Inspect its fixed batch before execution; preserve its HTTP403/429 stop behavior. |
| Saved replay and tape handling | `scripts/tape_opponent.py`, `scripts/make_tape_actions.py`, `scripts/check_tape_actions.py` | Extract opponent packages, action tapes and town data from existing replays; match exact episode/seat/artifact identity. Same team or submission does not establish an identical tape. |
| Existing replay summaries | `scripts/replay_profile.py`, `scripts/replay_flow.py`, `scripts/plan_stats.py` | Reuse for a concrete loss question. Summaries are diagnostic and do not replace game outcomes; do not assume the historical profiler proves exact accepted trades. |
| Standard candidate evaluation | `S/unitorder/assemble_judge.py`, `judge_runtime_preflight.py`, `judge_execution.py`, `judge_saved_audit.py` | Reuse the established seven-family protocol, candidate/source custody, exact keys and B baselines, shared CPU lock, and separate family reports. Protocol: `docs/strategy/2026-09-13-unit-order-off-judge-plan.md`; shared integration: `docs/strategy/2026-09-13-momentum-judge-integration.md`. |
| Underlying game evaluator | `scripts/eval_vs_baselines.py` and existing family runners | Use through the standard campaign for candidate decisions. Do not invent another benchmark or substitute an ad hoc baseline run. |
| Training and monitoring | `scripts/train.py`, the active campaign's existing launcher/protocol, `S/unitorder/nvml_monitor.py` | Use recorded commands and original process handles. Both remote GPUs and the local GPU are authorized; do not restart a live run because a status request or SSH connection ended. |
| Package and submit | `scripts/package_submission.py`, `scripts/submit.py` | Reuse the release workflow with the intended candidate/source and required release checks. Do not blindly package a script's default theta or source tree. |

The active tool interface also provides shell execution/process polling, Git,
file edits, and Sol subagents. No dedicated Kaggle connector is exposed in the
current tool catalog; the repository's working API scripts are the Kaggle tools.

**Evolution loop:** one actionable hypothesis, one focused branch/change, only
the relevant correctness checks, then the unchanged standard game evaluation.
Judge progress primarily by wins/losses/ties and the existing per-family report
against B. Do not pool seeds/families or create a new composite acceptance score.
Preserve required release gates; backend parity is not a performance measure.

**Necessary tests:** for weight-only candidates with validated unchanged source,
layout and runtime, reuse existing checkpoint/eligibility checks and the standard
judge. Do not add a suite or repeat history/parity studies for each seed. Run
focused semantic regression tests when code changes; use backend/simulator/
packaging checks when those interfaces change or evidence reveals a mismatch.
Documentation and evidence-only updates need no model or game tests. Reuse valid
evidence until its bound inputs change, and retain the existing release checks
before submission.

**Research:** use Sol tasks with a time budget matched to the question and the
evidence required. Short lookups may take5–10 minutes; substantive replay,
policy or training research may need30–60 minutes or longer when justified.
A timebox is a progress checkpoint, not a reason to give a superficial or
premature answer. Extend a task with a new bounded scope when meaningful work
remains. Require source/replay evidence, explicit uncertainty, and a concrete
implementation decision. A concise report may summarize substantial research;
brevity is not a substitute for doing it. Avoid duplicate studies, new metrics
and extra evaluation tooling that do not help the next decision. Keep current
jobs moving while independent research runs.

Use feature branches and descriptive commits; validate before merging. Record
launch handles, results and decisions in existing records, not repeated new
documents. Preserve historical evidence and untracked replays. The user's current
top-five objective and these directions supersede older experimental plans below.

## Formal objective

Let `θ ∈ R^n` be the weights of a small day-level policy network. The agent is the
deterministic map

```
π_θ : obs_features → macro_action      (argmax over factored heads, no sampling)
```

Maximise expected **win rate** — not profit — because the final Bradley-Terry
tournament scores win/loss/tie only and discards coin margin:

```
J(θ) = E[ W(θ, φ, ω) ]        φ ~ opponent pool P
                              ω ~ episode randomness (weed spawns, shop unlock draws)

W = 1 on win, 0.5 on tie, 0 on loss
```

Optimise with the OpenAI-ES gradient estimator (isotropic Gaussian perturbation,
rank-normalised returns, no backpropagation through the environment):

```
θ_{t+1} = θ_t + (α / (N·σ)) · Σ_{i=1..N} A_i · ε_i

  ε_i ~ N(0, I)
  A_i  = rank-normalised J(θ_t + σ·ε_i)
```

The opponent pool `P` grows by periodically freezing `θ`, producing a self-play
ladder at no extra cost.

## Policy architecture

**Shared per-product encoder + global head — 3,827 trainable params.**

The 9 products (wheat, carrot, tomato, strawberry, melon, egg, milk, wool,
fertilizer) are structurally identical: each carries (inventory offset from I₀,
current price, base, T, own production, opponent production, town demand). A
monolithic MLP would learn nine near-duplicate copies of the same scoring logic.
Share the encoder instead:

```
score_p = f_φ(product_features_p ⊕ global_context)   for each of 9 products
                36 → 64 → 1,  weights SHARED across all 9      = 2,433 params
allocation = top-k / softmax over {score_p}

global head     24 → 32 → 18  (hand count, land buy, fertilizer) = 1,394 params
                                                          total  = 3,827 params
```

Two reasons this beats a wider monolithic net at a fraction of the size:

1. It expresses the true structure of the decision. The optimal allocation is a
   *ranking* of products by marginal value; a shared scorer plus top-k is exactly
   that, so the network is not spending capacity rediscovering the form.
2. It **cannot memorise the default market table.** The encoder must *read*
   `base`/`T`/`above_target` from its inputs, which is what makes the
   `marketParams` domain randomisation actually bind. A monolithic net can memorise
   and will.

Sizing reference for the monolithic alternative, if swept: 150→32→50 = 6,482 params
(too narrow — a 32-unit trunk feeding 8 heads is the bottleneck); 150→128→50 =
25,778; 150→256→50 = 51,506.

Parameter count is **not** an ES constraint at this scale. Full-covariance CMA-ES is
limited to ~10²–10³ params by its O(n²) covariance and O(n³) eigendecomposition, but
OpenAI-ES uses an isotropic perturbation with a single scalar σ — O(n) state, no
matrix — and Salimans et al. (2017) trained ~1.7M-parameter Atari networks with it.
The real cost of dimension is sample complexity: ES gradient variance scales O(n).

## Compute environment

**Training host: remote server, 2× NVIDIA RTX 3090 (24 GB VRAM each, 48 GB total).**

This is not incidental — it dictates the simulator design. The following are
requirements, not optimisations:

1. **The simulator must be JAX: `jit`-compiled, `vmap`-ed, fully on-device.**
   ES throughput is bottlenecked by the environment, never by the ~4k-parameter
   net. A Python-loop simulator leaves both GPUs idle. State must be flat
   int32/float32 arrays — no dicts, no objects, no per-environment Python.
2. **Shard the ES population across both GPUs** with `pmap`/`shard_map`. ES is
   embarrassingly parallel; the only cross-device traffic is one all-reduce of a
   ~4k-float vector per generation. Communication cost is negligible.
3. **Antithetic sampling** — evaluate `θ ± σε`. Halves gradient variance and maps
   cleanly onto the two-device split, one sign per device.
4. **Regenerate `ε` on-device from PRNG keys** instead of materialising a
   `POP × n_params` matrix. (This is Salimans et al.'s seed-sharing trick.)
5. **No host↔device sync inside the generation loop.** Episode returns reduce
   on-device; only the updated `θ` crosses back to the host.
6. **Tabulate the price curve.** `price(inv)` is a pure function — precompute it
   into a lookup table indexed by inventory offset so the hot loop performs a
   gather rather than `sqrt`/`log`/`sq` per product per environment per step.

VRAM is not the binding constraint. Environment state is ~4 KB, so 32,768 parallel
environments cost ~128 MiB; SM occupancy is the real limit.

### Variance reduction — higher leverage than capacity

The dominant error source is **evaluation noise, not policy capacity**. At 32
episodes per candidate the standard error on win rate is 0.5/√32 ≈ **8.8 percentage
points**, larger than the true fitness gap between neighbouring ES candidates.
Selection would be picking luck. Two fixes, in priority order:

1. **Common random numbers — implement this first.** Evaluate every candidate in a
   generation against an *identical* set of episode seeds and identical opponents.
   ES consumes only the rank ordering within a population, and every candidate is a
   small perturbation of a shared parent, so returns under matched seeds are
   strongly correlated; `Var(X−Y) = Var(X) + Var(Y) − 2·Cov(X,Y)` then collapses the
   variance of the comparison. Cost: zero.
   - **Resample the seed set across generations.** Common *within* a generation,
     fresh *between* them. A globally fixed seed set lets the population overfit
     those specific episodes and drift off true expected win rate.
   - Requires the simulator to be deterministic given an explicit seed — fold this
     assertion into the bit-exactness harness.
2. **More episodes per candidate**, only if CRN proves insufficient. 128 episodes
   halves SE to ≈4.4 pp but costs 4× wall-clock.

(Note: 0.5 is the max-variance Bernoulli sd, so these SEs are upper bounds — ties
pull the true value below them.)

### Throughput budget

| | 16-core CPU | 2× RTX 3090 (target) |
|---|---|---|
| Environment throughput | ~1.6e6 steps/s | ~1e7 steps/s |
| Generation @ POP 256 × 8 episodes | 1,474,560 steps → ~0.92 s | — |

Operating points at POP 1024 (antithetic: 512 pairs, 512 per GPU):

| Episodes/candidate | Steps/generation | s/gen @ 1e7 | 10,000 generations |
|---|---|---|---|
| **32 — baseline, with CRN** | 23,592,960 | 2.36 | **~6.6 h** |
| 64 | 47,185,920 | 4.72 | ~13.1 h |
| 128 — fallback if CRN insufficient | 94,371,840 | 9.44 | ~26.2 h |

These count environment stepping only; optimiser, parameter broadcast and device
sync add overhead, so budget **~7–8 h** for the baseline row in practice. That is
still an overnight run, giving roughly **30 independent runs before the deadline** —
iteration count, not any single run, is what reaches the top band.

### Operational notes

- Run training under `tmux`/`nohup`; the connection will drop on a multi-hour job.
- Checkpoint `θ` and the opponent pool every N generations; rsync back to build and
  submit with the kaggle CLI.
- **Release gate — cross-backend equivalence.** Training is JAX float32 on GPU; the
  submission is numpy on 1.6 CPU cores. A test must confirm the numpy forward pass
  reproduces the JAX policy's argmax on a held-out state set before any submission.
  Divergence here is silent and would invalidate every offline result.

## Success criteria

| Tier | Criterion |
|---|---|
| Minimum | Valid submission on the ladder; >90% win rate vs. the built-in `starter` baseline |
| **Target** | **Top five on the final leaderboard** |
| Stretch | Top-3 |

Interim measurable: win rate against the frozen opponent pool, and live ladder
skill rating.

## Hard constraints

- **Determinism.** Identical observation ⇒ identical action. Zero RNG at inference,
  no wall-clock-dependent branching, all tie-breaks by fixed ordering.
- **Speed.** Pure-numpy forward pass; never import torch or jax in the submission.
  Policy evaluated once per in-game day (30×/episode), not per turn (720×).
- **Runtime budget.** 1.6 vCPU, 6.5 GiB RAM, 8 GiB disk, ≤100 MiB submission.
- **Packaging.** `main.py` at archive root; imports resolve under
  `/kaggle_simulations/agent/`.
- **Deadlines.** Entry + team merger 2026-09-23; final submission 2026-09-30;
  leaderboard finalises ~2026-10-15. 5 submissions/day, latest 2 tracked.

## Non-goals

- No behaviour cloning or warm start from a hand-written planner — that would make
  the approach supervised.
- No inference-time search (MCTS, rollouts, replanning).
- No learned micro-executor. Watering/feeding/harvest routing is fixed actuator
  logic (~30 lines of "don't let things die"), not strategy.
- Not optimising coin margin, expected profit, or any shaped proxy as the selection
  metric.
- No differentiable relaxation of the simulator. Writing it functionally in JAX
  keeps that option open at no cost, but ES needs only forward rollouts.

## Approach summary

Four components:

1. Vectorised bit-exact JAX simulator (validated against `kaggle_environments`)
2. Shared per-product encoder + global head, 3,827 params
3. OpenAI-ES loop with CRN, population sharded across 2× RTX 3090, self-play pool
4. Fixed micro-executor

`θ` is shipped directly. There is no distillation step.


## Known risk

ES plateaus in local optima more readily than policy-gradient methods. Mitigation:
IPOP-style restart with doubled `σ` from the current best on stagnation; escalate to
keeping top-K behaviourally diverse elites in the pool if that proves insufficient.
The GPU budget makes several restarts cheap, which substantially blunts this risk.

Secondary risk: the ~1e7 steps/s GPU figure is an estimate from state size and step
complexity, not a measurement. If the Aug 25 benchmark lands nearer 1e6, drop to
POP 512 × 16 episodes and the plan holds with a longer per-run wall-clock.
