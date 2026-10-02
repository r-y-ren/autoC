"""OpenAI-ES over the JAX simulator.

    theta_{t+1} = theta_t + (alpha / (N * sigma)) * sum_i A_i * eps_i

with antithetic sampling, rank-normalised returns, and Adam on the resulting
gradient estimate.

The objective is a **blend of an absolute anchor and a shaped margin**
(`shaped_advantage`), and *selection* now runs on the absolute number too
(`_measure_champion`). Both are 2026-08-25 reversals of the previous design,
which had the win bit as the selection rule and a minority absolute term.
What the measurements said:

* `mean_win` saturates in ~100 generations and then decays back to 0.5. It has
  to: the pool is the policy's own lineage, so "beat your past selves" is
  satisfiable at any absolute level, and a round-robin over 12 clone rungs plus
  theta made ~63% of episodes self-play.
* `abs` (coins against the fixed archetypes) plateaued after ~30 minutes of a
  13-hour run, and corr(abs, champ) over the run was **-0.17**. The selection
  rule and the thing worth selecting for were, measurably, unrelated.
* `absolute_eval` fed `best_abs.npy`, which `--promote` then ignored: it wrote
  `tr.theta`, the last iterate.

The objective the run is now judged on is absolute: earn at least twice the
fixed evaluation opponent (kagg2 makes ~150-170k coins a game), i.e. >= 300k,
in a *contested* market. So coins are what the gradient mostly consumes, coins
are what picks the champion, and the win term is kept at minority weight
because a policy that farms well but folds head-to-head still loses the
tournament.

What that measurement could not see, and the flags that answer it
-----------------------------------------------------------------
Measured again on 2026-08-26, over 30 checkpoints x 720 real-engine games
against `kagg2`: **the two fitness terms rank policies identically**
(Spearman +0.973, +0.965 over the 16 non-degenerate ones). They have to. Every
rung is beaten in essentially every game, so the opponent's coins sit at their
floor and the margin is a monotone transform of own coins -- against
`mixed_ranch`, `theirs` spans 16.3k across the checkpoints while `mine` spans
60.4k. The 0.6/0.4 blend is a blend of a number with itself, and re-weighting
the two cannot fix that.

Nor is the ordering broken: `abs_coins` is the **best single predictor** of the
real `kagg2` margin there is (rho +0.926 / +0.924 / +0.733 over the three
subsets). It is the best predictor of a quantity that is 49k from the decision
boundary, and past the point where the market saturates it stops working -- on
the tracker's own rows, own coins correlate +0.32 with the margin and **+0.79
with kagg2's coins**. The two farms scale together.

What the ladder is missing is an opponent it *loses* to. So, in slot-allocation
and selection rather than in `shaped_advantage`:

* `AR.PROXY_NAME` -- a rung played from a handicapped opening, and the only
  measured quantity that adds information about the real margin once
  `abs_coins` is controlled for (partial rho +0.42 on its win rate at the top
  10, against **-0.63** for the ladder's margin against `mixed_ranch`).
* `rung_weight` -- the archetype episode block divided by weight rather than
  round-robin, so the kagg2-shaped rungs can carry more than 6.25% of it.
* `select_metric` / `select_coin_floor` -- selection on the weighted expected
  tournament score, floored on absolute coins so that a policy which buys
  margin by burning the market down cannot be promoted.
* `collapse_floor` -- the second liveness floor. `MIN_COINS` asks whether a
  rung can earn; this asks whether it still earns with a real policy on the
  board.
* `holdout_rungs` -- a holdout on *opponents*. The seed holdout tracks the
  selection half to a mean 1.1% and is answering a question nobody is asking.

Every one of them defaults to the behaviour above, because the evidence grades
the rung "strong" and the weights "not established": land the rung, earn the
weights.

Variance reduction (GOAL.md's priority order)
---------------------------------------------
1. **Common random numbers.** Every candidate in a generation is evaluated on the
   *same* episode seeds against the *same* opponents. ES consumes only the rank
   ordering, and every candidate is a small perturbation of one parent, so
   matched seeds make the returns strongly correlated and
   `Var(X-Y) = Var(X) + Var(Y) - 2Cov(X,Y)` collapses. Costs nothing.
2. The seed set is **resampled between generations**. Holding it fixed would let
   the population overfit those particular episodes and drift off true expected
   win rate.
3. Each episode seed is played **twice, once in each seat**, by the same
   candidate against the same opponent. Seat asymmetry (the first player commits
   first inside a market round, and hired hands spawn on different tiles) then
   cancels out of the score instead of leaking into the ranking.

`eps` is regenerated on device from a per-index PRNG key rather than
materialised as a POP x n_params matrix (Salimans et al.'s seed-sharing trick).

Sharding
--------
ES is embarrassingly parallel, so the population is sharded across every visible
device along the batch axis. The rollout is `jit(vmap(...))` over that axis and
`tables` is replicated, so XLA partitions the work with no cross-device traffic
inside an episode; the only thing that crosses is the per-rollout win score, a
handful of floats. With one device the mesh is 1-wide and this is a no-op.

The real-engine gate (`--real-gate`)
------------------------------------
Everything above selects in the **simulator**, and the simulator is a proxy.
Measured across ~10 runs, the proxy stops tracking the tournament after ~1.5k
generations: flow23's three consecutive in-sim records scored 64.6%, 52.1% and
47.9% against the real `kagg2` while the in-sim margin they were taken on rose
monotonically. `best_abs.npy` is what `--promote` ships, so the deliverable was
getting worse on the only measurement that counts.

Under `--real-gate` the in-sim record stops deciding and starts *nominating*.
Each in-sim record launches an asynchronous `scripts/eval_vs_baselines.py` --
the same script, opponent and seed base the tracker uses, so the numbers are
comparable rather than merely similar -- and `best_abs_theta` moves only if the
real win rate (or margin, under `--real-gate-metric margin`) beats the
incumbent's, whose own numbers come from its own gated eval. The trainer never
blocks: one `Popen.poll()` a generation, one eval in flight, queue depth 1.

In-sim records dry up -- most runs take their last one inside the first
~1.5k generations and then run for thousands more -- so a gate fed by records
alone goes idle exactly when the proxy has drifted furthest, and `best_abs.npy`
stays a theta nothing has been measured against since. `--real-gate-every N`
feeds it anyway: every `N` generations, if no eval is in flight and nothing is
waiting, the **search centre** (`theta`, the ES mean) is nominated and competes
under the same accept rule. An in-sim record on the same generation wins the
slot; the cadence is skipped that generation and comes round again at the next
multiple of `N`. Verdicts say which kind they judged (`real_gate_source`).

A gate fed by many n=48 readings has a winner's curse of its own: the record
is the max over a sequence of noisy draws, so the incumbent's number is
inflated by the largest upward error the run happened to make, and past some
point no honest theta can clear it. flow28b's gate accepted a periodic
candidate at 85.4%/+6,023 on 48 games; the same theta replicated at
74.5%/+4,936 on 192 fresh ones -- an ~11pp bar nothing was going to beat.
`--real-gate-replicate` answers it the way `--best-replicate` answers the
in-sim one: every acceptance is immediately re-measured on a fresh seed base
(`--real-gate-seed-base + 1`), the incumbent's numbers become the **pooled**
win rate and margin over both evals, and the next candidate is compared
against those. The replicate jumps the queue -- it is what the bar means, and
a candidate measured against an un-replicated bar is measured against noise --
but it never moves `best_abs.npy`, because the theta did not change.

And with it on, an acceptance is **provisional**. One n=48 reading against a
pooled n=96 bar is not a fair comparison, and flow27c shows what it costs: a
candidate read 79.2%/+7,022 against an incumbent pooled at 78.1%/+6,135, took
the record, replicated at 60.4% and left the run with a pooled 69.8%/+5,291 --
the record got *worse* and the bar dropped with it. So the previous incumbent
(its theta and its pooled numbers) is kept in `prev_incumbent` until the
replicate lands, and only if the candidate's own **pooled** pair beats it does
the record move: `best_abs.npy`, `best_abs_theta` and the stall clock all wait
for that confirmation. A candidate that fails its replicate is reverted and
the previous incumbent goes back to being the bar. `best_abs.npy` therefore
changes less often and every change is a theta measured twice.

A gate that only filters cannot steer. On flow27c/28c/27d every periodic
centre candidate taken after the record was refused (52-77% against pooled
bars of 62-76%): the ES centre keeps walking away from the theta the real
engine preferred, because the gradient and the selection that produce it are
both in-sim, and the gate can only say no. `--real-gate-recentre K` closes the
loop -- after `K` consecutive *periodic* candidates have been refused (or
reverted) since the last confirmation, the search is put back on the confirmed
record: `theta <- best_abs_theta`, Adam cleared, sigma stepped exactly as a
stall restart does (`_restart_from_record`, shared with `_maybe_restart` so
there is one such move in the trainer and not two).

Fixed seeds make the gate itself a thing to overfit. flow27g's confirmed
record pooled 83.3% on the two bases the gate selects on and 91.7% on one
neighbouring base, but 62.5% on another (n=192); the champion is 76-85% on
every base. A theta that wins on 96 particular games is not a better theta.
`--real-gate-fresh` takes the seeds out of the loop: every nomination draws a
**fresh** base (deterministic from `--seed`), and the incumbent is replayed on
that same base in the same slot cycle, so the decision is a *paired*
comparison on games neither theta has been selected on. The incumbent's
running pooled numbers are kept for the log; they are never what a candidate
is measured against.

The two records are then separate objects, and both are kept: `best_abs` (the
scalar) and `best_sim.npy` are the in-sim record, which keeps moving so that a
gate rejection cannot wedge the nomination stream; `best_abs.npy` and
`best_abs_theta` are the gated one. `_maybe_restart` re-centres on the gated
one, which is the point of the flag -- a run whose proxy is climbing away from
the real objective is sent back to the last theta the real engine preferred.
"""

from __future__ import annotations

import atexit
import copy
import csv
import hashlib
import json
import math
import os
import signal
import subprocess
import sys
from typing import NamedTuple

import jax
import jax.numpy as jnp
import numpy as np

from .. import spec
from ..core import policy as PO
from ..sim import eod, market, rollout
from ..sim.state import build_tables
from . import archetypes as AR
from . import kagg2_flow as K2F
from . import kaggle_flow as KGF
from . import tape_actions as TPA
from . import tape_flow as TPF


class Config(NamedTuple):
    pop: int = 128              # candidates per generation (even; antithetic pairs)
    episodes: int = 64          # episodes per candidate
    sigma: float = 0.02
    lr: float = 0.02
    beta1: float = 0.9
    beta2: float = 0.999
    eps_adam: float = 1e-8
    weight_decay: float = 0.003  # decoupled: theta <- (1 - wd) * theta each gen
    bias_clip: float = 8.0      # head/aux biases are clipped to this, not decayed
    margin_scale: float = 100_000.0  # coins per unit of the shaped relative term
    abs_weight: float = 0.6     # weight on the absolute anchor, vs 1-w on margin
    chunk: int = 1024           # rollouts evaluated per device call
    market_jitter: float = 0.0  # marketParams domain randomisation strength
    pool_every: int = 100       # generations between opponent-pool snapshots
    pool_size: int = 12
    champ_every: int = 10       # generations between champion re-measurements
    arch_frac: float = 0.5      # share of episode slots that face an archetype
    #: How the archetype block's slots are divided between the rungs.
    #: "fixed" is `largest_remainder` -- a pure function of the weights, so the
    #: same rungs take the leftover slots in every generation of the run and a
    #: ladder wider than the block loses its tail outright (127 tapes at 256
    #: episodes never sample the last 12). "carry" runs the same allocation as
    #: a token bucket (`SlotCarry`), so the leftovers rotate and every rung's
    #: cumulative share tracks its weight to within one slot. Rotation is
    #: between generations only: one index row is still drawn per generation
    #: and every candidate plays it, so common random numbers are untouched.
    slot_rotation: str = "carry"
    #: Play every **pinned** rung exactly once per candidate per generation.
    #:
    #: A pinned action tape (`--tape-actions` on a file carrying a `town` key,
    #: cut with `--with-town`) is ONE deterministic board: the recorded town
    #: schedule fixes the shop draws, so the sim reproduces the engine and the
    #: live game to the coin and both seats of a pair return the same numbers
    #: for the same theta. The only per-episode variation left is the
    #: candidate's own perturbation, which the pair does not resolve either --
    #: every candidate plays its own theta on both seats.
    #:
    #: So the slot allocator's whole reason for handing a rung several pairs
    #: (variance reduction over the board draw) is absent here, and measured on
    #: the live 384-episode arms it spent 75% of the pinned budget replaying
    #: identical outcomes: 86 pinned rungs at weight 2 took ~2 pairs = ~4
    #: episodes of the same game each. On, each pinned rung takes exactly one
    #: episode and its `--rung-weight` moves to the fitness aggregation instead
    #: (`shaped_advantage`'s `ep_weight`), where it scales the board's
    #: contribution rather than its replay count. Off -- the default -- the
    #: allocation and the arithmetic are byte-identical to every run before it.
    pinned_once: bool = False
    #: Play every PINNED rung on a FIXED seed word derived from the tape,
    #: instead of the generation's drawn one. Off by default, where a pinned
    #: rung's episodes take the same per-slot CRN word every other episode
    #: takes.
    #:
    #: A `--with-town` tape pins the *shops* (`sim.eod.unlock_shop`), which is
    #: the big lottery and the reason the rung is called pinned at all. It does
    #: not pin the rest of the day generator: `sim.eod.spawn_weeds` still walks
    #: two words per empty tile out of `eod.host_stream(seed, day)`, so the
    #: same (candidate, pinned tape) evaluated under two generations' seeds
    #: plays two different weed histories and returns two different coin
    #: totals. Measured on a 32-member population over 16 pinned rungs, that
    #: residual moved the pinned-only ranking to spearman 0.985 across two CRN
    #: seeds -- noise on 82 % of the fitness weight, on boards whose whole
    #: point is that they are one fixed game.
    #:
    #: On, the word for a pinned slot is `pinned_seed_word(rung name)` -- a
    #: blake2b digest of `tape_act_<episode>`, so it is a property of the tape
    #: and of nothing else: stable across processes, across machines, across
    #: generations and across `--resume`. Every other slot (a drawn tape, an
    #: archetype, self-play) keeps the drawn word, and the draw itself still
    #: happens, so `self.rng`'s stream -- and therefore every warm start, market
    #: jitter and opponent index behind it -- is what it would have been.
    pinned_fixed_seed: bool = False
    warm_frac: float = 0.25     # share of episode pairs that open on a warm start
    warm_money_max: int = 40_000  # warm-start cash is uniform in [STARTING_MONEY, this]
    #: Let a `--tape-actions` rung's pairs take the warm start too. Off,
    #: because an action tape is a *verbatim* recording of a game that opened
    #: on the engine's day 0: replaying those 719 frames from two extra
    #: quadrants and 40,000 coins is not the recorded opponent, it is a
    #: strictly richer one that still plays the poor seat's orders. Measured
    #: on the six band6 tapes with flow102_g280, the warm pairs are won 96.1 %
    #: of the time against 51.3 % on the cold ones, which pulled the rung's
    #: sim win rate 11.6 points above the engine's paired csv on the same
    #: opponents. `--tape-act-warm` restores the old behaviour.
    tape_act_warm: bool = False
    n_archetypes: int = 4       # hand-set strategy opponents kept beside the pool
    abs_every: int = 25         # generations between absolute-strength measurements
    abs_pairs: int = 64         # fixed seed pairs the measurement plays (x2 seats)
    restart_stall: int = 0      # gens without a `best_abs` improvement before an
                                # IPOP-style sigma restart; 0 disables it
    stall_sigma_mult: float = 2.0   # what that restart multiplies sigma by. 2.0
                                # is the IPOP default; 1.0 keeps the step and
                                # makes the restart a pure jump back onto
                                # `best_abs_theta` with Adam cleared, which is
                                # what a ladder that only trains at small sigma
                                # wants -- see `_maybe_restart`.
    # --------------------------------------------------- the win-tracking half
    # Every default below is the behaviour that was there before it existed, so
    # an unflagged run is the run that came before this block.
    rung_weight: tuple = ()     # ((archetype name, weight), ...); () = uniform
    proxy_handicap: tuple = AR.NO_HANDICAP   # (nquad, money) opening for the
                                # `kagg2_proxy` rung's **own seat**; the default
                                # is the engine's day 0, i.e. no handicap
    select_metric: str = "coins"     # "coins", "score", "margin:<rung>" or
                                # "softwin:<rung>:<tau>" -- what `best_abs`, the
                                # champion and `--promote` select on; see
                                # `Trainer.selection_score`
    select_coin_floor: float = 0.0   # a candidate under this many yardstick
                                # coins cannot be selected, whatever it scores
    best_gate: str = "sel"      # "sel" (the record is a max over the selection
                                # half alone) or "both" (the holdout half must
                                # not fall either) -- see `_accept_best`
    best_margin: float = 0.0    # how far a candidate has to clear the record
                                # before it replaces it, in the selected metric
    collapse_floor: float = 0.0      # a rung keeping less than this share of
                                # its zero-theta coins against the incumbent is
                                # dropped from the yardstick mean; 0 = report only
    holdout_rungs: bool = True  # also play `AR.HOLDOUT_RUNGS` -- reported, never
                                # trained on and never selected on
    kagg2_flow: bool = False    # append the `kagg2_flow` rung: an opponent whose
                                # market presence is kagg2's measured one (see
                                # `es.kagg2_flow`) instead of a planner's
    kagg2_flow_scale: tuple = (0.5, 1.5)   # per-episode-pair uniform scale on
                                # every product of the flow table
    kagg2_flow_jitter: int = 2  # per-episode-pair uniform day shift, +- this
                                # many days, of the whole flow calendar
    kagg2_flow_shift: tuple = None   # (LO, HI) inclusive, in days: the range
                                # that same shift is drawn from when the
                                # gradient's flow family is not centred on the
                                # table's own calendar. `None` (the default)
                                # keeps the symmetric `+- kagg2_flow_jitter`
                                # draw, which is every run before 2026-08-28.
    kaggle_flow: bool = False   # append the `kaggle_flow` rung: the same kind
                                # of opponent, with the *Kaggle field's*
                                # measured market presence (see
                                # `es.kaggle_flow`) instead of kagg2's. It is
                                # appended after `kagg2_flow`, so every rung
                                # index and weight a run already has is
                                # unchanged by turning it on.
    kaggle_flow_scale: tuple = None   # (LO, HI): its own per-episode-pair
                                # scale range. `None` shares `kagg2_flow_scale`
                                # -- the two rungs are the same kind of
                                # randomisation and there is no reason to
                                # state it twice unless the field's level is
                                # known to sit elsewhere.
    kaggle_flow_shift: tuple = None   # (LO, HI) inclusive, in days. `None`
                                # shares whatever the kagg2 rung is drawing:
                                # `kagg2_flow_shift` if it is set, else the
                                # symmetric `+- kagg2_flow_jitter`.
    tape_rungs: tuple = ()      # paths to `es.tape_flow` `.npz` tables, one
                                # rung each: the market presence of **one**
                                # Kaggle replay seat rather than a mean over a
                                # field. Appended after `kaggle_flow`, in the
                                # order given, so no existing rung index moves.
    tape_flow_scale: tuple = None    # (LO, HI): their per-episode-pair scale
                                # range. `None` shares `kagg2_flow_scale`.
    tape_flow_shift: tuple = None    # (LO, HI) inclusive, in days. `None`
                                # shares whatever the kagg2 rung is drawing.
    tape_actions: tuple = ()    # paths to `es.tape_actions` `.npz` tables, one
                                # ACTION rung each (`tape_act_<ep>`). Where a
                                # `--tape-rung` replays a recorded seat's daily
                                # market aggregates through a surrogate board,
                                # this replays its per-step actions: seat 1 is
                                # the recording, unit for unit and order for
                                # order, and its farm, shed, hires and land are
                                # simulated. Verified byte-exact against the
                                # engine on 15 of 16 paired boards
                                # (`scripts/check_tape_actions.py`), so these
                                # rungs are scored on the margin like a planner
                                # rung and never on `--tape-score ours`, which
                                # exists for the flow surrogate's phantom coins.
                                # Appended after the `--tape-rung` rungs.
    tape_score: str = "margin"  # how a `tape_` rung's episodes are scored:
                                # "margin" reads them like every other rung
                                # (own coins minus the flow seat's) and is
                                # every run before 2026-09-04; "ours" reads
                                # our coins alone. See `shaped_advantage`.
    # --------------------------------- how faithfully a tape rung is replayed
    # Both off by default: off, `sim.market.apply_flow` and `sim.rollout.run_day`
    # emit the program they always did and every existing run reproduces coin
    # for coin. See `scratchpad/tapegap/report.md` for the measurement that
    # asked for them.
    tape_flow_backed: bool = False   # clamp the flow seat's sell count to what
                                # its shed holds *before* revenue and the
                                # inventory advance, not only on the drain, so
                                # an exogenous table can no longer be paid for
                                # -- or flood the book with -- goods the seat
                                # never grew. The engine caps a SELL at
                                # `shed[item]`; this is that cap.
    #: `--shop-crn`. Off, the sim is byte-identical to the engine and to
    #: every run before this flag. On, the end-of-day shop draw is taken from
    #: a fixed position in the same per-(seed, day) word stream instead of
    #: from just past the weed walk, so it no longer depends on how many EMPTY
    #: tiles the two seats left that day.
    #:
    #: Why: the engine's day generator is consumed one `random()` per empty
    #: tile (ours, then theirs) BEFORE `choice(sorted(SHOPS))`, so a candidate
    #: that plants one tile more re-rolls every later shop unlock. A
    #: YARN_STORE (the only wool sink) is worth ~25k to whichever seat holds
    #: wool, so an ES fitness *difference* between two antithetic candidates
    #: carries a zero-mean +/-25k lottery that has nothing to do with either
    #: perturbation (`scratchpad/coupling`, `scratchpad/glut/verdicts.log`
    #: 2026-09-06 10:50Z). `choice` is uniform over the eight shops from
    #: whatever word it reads, so cutting the coupling leaves the shop
    #: distribution -- and the expectation of fitness -- alone. TRAINING-side
    #: only: it is a common random number for the search, never an eval
    #: semantic. Never turn it on for a fidelity gate.
    shop_crn: bool = False
    tape_flow_spread: bool = False   # spend the day's table across the day's
                                # market turns (`rollout.MARKET_TURNS`, one
                                # `row // n` share each with the remainder on
                                # the last) instead of dumping all of it at
                                # hour 0, so the tape trades at the hours we
                                # trade at rather than always ahead of us.
    # ------------------------------------------ the de-biased flow yardstick
    # Off by default, so an unflagged run measures exactly what it measured
    # before these existed. See `Trainer.absolute_report`.
    abs_flow_draws: int = 0     # K > 0: the yardstick plays the `kagg2_flow`
                                # rung at K *fixed* (scale, shift) draws and
                                # reports their mean, instead of reading the
                                # single centre of the family; 0 = the centre
    abs_flow_scale: tuple = (500, 1500)   # thousandths; the inclusive range
                                # those K draws' scale is uniform on
    abs_flow_shift: tuple = (-2, 2)       # days; the inclusive range those K
                                # draws' calendar shift is uniform on
    abs_select: str = "sel"     # which of the fixed seed pairs the *selected*
                                # statistic and the record are read on: "sel"
                                # (the first half, today), "hold" (the second
                                # half) or "all" (every pair)
    # --------------------------------------- against the winner's curse
    # Both off by default, and both are answers to the same failure: a record
    # taken on a *fixed* measurement is a max over a static target, and ES
    # closes on the target rather than on the thing it stands for. See
    # `Trainer.measurement_draws` and `Trainer._replicate_record`.
    abs_fresh_draws: bool = False    # re-draw the K flow levels for every
                                # measurement, from a stream seeded by the
                                # generation, instead of reusing the one fixed
                                # set of levels for the whole run
    best_replicate: int = 0     # a candidate that beats the record is
                                # re-measured this many times, on draws and
                                # seed pairs it was not screened on, and the
                                # record is taken only if the mean of those
                                # also beats it -- at the replicate mean, not
                                # at the screening reading; 0 = no replication
    train_only: str = "all"     # which theta coordinates the ES may move:
                                # "all" (every live one, i.e. every run before
                                # this field), "biases" (what `bias_mask`
                                # marks), or a comma-separated list of
                                # `PO.SHAPES` block names -- see `train_mask`
    optimizer: str = "adam"     # "adam" or "sgd". Under "sgd" the step is
                                # `lr * m` with `m` the beta1 momentum of the
                                # raw gradient: it *scales with the gradient*,
                                # so a generation whose advantage was noise
                                # takes a small step instead of Adam's full
                                # `lr` per coordinate -- see `apply_gradient`
    # ------------------------------------------- day-10 fitness shaping
    # Both weights default to 0.0, and 0.0 is *exactly* inert: `Trainer.
    # fitness_bonus` returns `None`, and `shaped_advantage` then evaluates the
    # same expression, character for character, that it evaluated before these
    # fields existed. See `shaped_advantage` and `TILE_FILL_DAYS`.
    #
    # Why they exist: a ledger over 88 live losses to the 2000-2200 band read
    # (1) the opponents' lead is set on day 10 -- they plant ~11.5 melon on day
    # 0 and sell 69 units on days 10-11, and in 69 of the 88 games the day-9 ->
    # day-10 coin swing is larger than the final margin; and (2) from day 10 on
    # they hold 56 planted tiles to our 47, with 0.6 idle unlocked tiles to our
    # 9.1. End-of-game coins alone cannot reward the *joint* move (plant more +
    # hire the crew to work it) that closes either gap, because either half
    # alone loses coins.
    d10_cash_weight: float = 0.0   # coins of shaped margin per coin of the
                                # day-D lead, added to the margin before the
                                # sigmoid; 1.0 = day D counts like the finish
    d10_cash_day: int = 10      # which day's end-of-day purse `d10_cash_weight`
                                # reads, 0-based, as `sim.rollout`'s `daily`
                                # indexes it
    tile_fill_weight: float = 0.0  # **coins per net filled tile**: the term is
                                # `w * mean_{d in TILE_FILL_DAYS} (planted -
                                # idle)` for our seat, so `w` carries the whole
                                # unit conversion and the logged raw number
                                # stays in tiles -- see `TILE_FILL_DAYS`
    late_price_weight: float = 0.0  # **coins of margin per coin of realised
                                # unit price**: `w * (our mean coins per unit
                                # sold over LATE_PRICE_DAYS - theirs)`. This
                                # term and `d10_cash_weight` pull in opposite
                                # directions -- the 2100 band wins by being
                                # ahead at day 10, the top ten by being level
                                # there and selling better afterwards -- so an
                                # arm should have a reason before it sets both


def perturbations(key, pop_half, n):
    """eps for one generation, regenerated from a key rather than checkpointed.

    Salimans et al.'s seed-sharing trick exists to avoid materialising a
    POP x n_params matrix across workers. At n ~ 4,200 that matrix is under a
    megabyte, so it is materialised here for clarity; what is kept from the trick
    is that eps is *derived from a key* and never stored, so a checkpoint is just
    theta plus the optimiser moments.
    """
    return jax.random.normal(key, (pop_half, n), dtype=jnp.float32)


def rank_normalise(x):
    """Centred ranks in [-0.5, 0.5], with **tied fitnesses sharing a rank**.

    Win rate over 32 episodes takes only 65 distinct values, so exact ties are
    common -- especially early, when most candidates beat the pool outright.
    Breaking those ties by array index would be actively harmful here: the array
    is [theta + sigma*eps ; theta - sigma*eps], so index order *is* the
    antithetic sign, and index tie-breaking would inject a systematic
    "positive perturbations are better" bias into the gradient. Averaging ranks
    over tied groups leaves tied candidates with identical advantage, which is
    what they deserve.
    """
    n = x.shape[0]
    order = jnp.argsort(x)
    raw = jnp.zeros(n, jnp.float32).at[order].set(jnp.arange(n, dtype=jnp.float32))
    eq = (x[:, None] == x[None, :]).astype(jnp.float32)
    avg = (eq * raw[None, :]).sum(axis=1) / eq.sum(axis=1)
    return avg / (n - 1) - 0.5


def win_scores(mine, theirs):
    """Per-episode {0, 0.5, 1}. The tournament's own scoring rule."""
    return jnp.where(mine > theirs, 1.0, jnp.where(mine == theirs, 0.5, 0.0))


#: `Config.tape_score` / `--tape-score`: how a tape rung's episodes are scored.
TAPE_SCORES = ("margin", "ours")

#: `--slot-rotation`. See `Config.slot_rotation` and `SlotCarry`.
SLOT_ROTATIONS = ("fixed", "carry")

#: The inclusive day window `--tile-fill-weight` averages over, and the number
#: of days in it. Days 10-25: day 10 is where the band's board lead opens (the
#: loss ledger's day-9 -> day-10 swing) and day 25 is the last day a tile
#: planted that morning can still be harvested inside the 30-day season, so
#: past it an empty tile is not a mistake and rewarding a full board would be
#: rewarding waste. Fixed rather than flagged: it is a fact about the game's
#: calendar, not a knob, and `sim.rollout.episode(day_tiles=True)` returns the
#: whole [N_DAYS, 2, 2] stack either way.
TILE_FILL_DAYS = (10, 25)
TILE_FILL_NDAYS = TILE_FILL_DAYS[1] - TILE_FILL_DAYS[0] + 1

#: Episodes in one slot of the opponent index: a pair is played from both
#: seats. Named because `--pinned-once` has to convert between "pairs a rung
#: would have taken" and "episodes it would have contributed", and the 2 in
#: that conversion is this one and not a coincidence.
EPISODES_PER_PAIR = 2

#: The inclusive day window `--late-price-weight` reads realised price over.
#: Days 15-29: a ledger of 30 recorded top-10 games (rating 2820-2940) found
#: those players level or *behind* at day 10 (paired gap -459) and winning the
#: second half on price alone -- income d15-29 +19k paired at flat volume,
#: carrot +28/unit, milk +17, wool +14, strawberry +14, delivered through 2.1x
#: our SELL rows in half-size slices (9.6 rows per selling day against our
#: 4.5). Day 15 is where that divergence starts; 29 is the last day.
LATE_PRICE_DAYS = (15, spec.N_DAYS - 1)


def own_coin_score(mine, cfg, xp=jnp):
    """Our coins alone, on the margin term's own [0, 1] scale.

    `sigmoid(log1p(mine) - log1p(margin_scale))`, which is
    `(1 + mine) / (2 + mine + margin_scale)`: the **absolute** term's `log1p`
    squash of own coins, read through the **relative** term's sigmoid so the
    two are commensurate and a tape rung's episodes can neither dominate an
    archetype's nor go silent beside them in the same mean. It passes 0.5 at
    `margin_scale` and, being scale-relative like `log1p`, keeps slope where
    `sigmoid(mine / margin_scale)` is already flat (0.75 at 300k against 0.95).

    `xp` is the array module: `jnp` in the gradient, `np` in `absolute_report`.
    """
    return 1.0 / (1.0 + xp.exp(math.log1p(cfg.margin_scale)
                               - xp.log1p(xp.maximum(mine, 0.0))))


def fitness_components(mine, theirs, cfg, tape=None, bonus=None,
                       ep_weight=None):
    """Unranked per-candidate own and relative components of ES fitness."""
    if bonus is None:
        rel = jax.nn.sigmoid((mine - theirs) / cfg.margin_scale)
    else:
        rel = jax.nn.sigmoid((mine - theirs + bonus) / cfg.margin_scale)
    if tape is not None:
        ours = mine if bonus is None else mine + bonus
        rel = jnp.where(tape, own_coin_score(ours, cfg), rel)
    own = jnp.log1p(jnp.maximum(mine, 0.0))
    if ep_weight is None:
        rel, own = rel.mean(axis=1), own.mean(axis=1)
    else:
        w = jnp.asarray(ep_weight, jnp.float32)
        w = w / jnp.sum(w)
        rel, own = (rel * w).sum(axis=1), (own * w).sum(axis=1)
    return own, rel


def shaped_advantage(mine, theirs, cfg, tape=None, bonus=None, ep_weight=None):
    """Centred advantage from raw final money: an absolute anchor, plus margin.

    Two components, each rank-normalised separately so the blend weight means
    what it says and neither term's units matter:

    * **absolute** -- `mean_e log1p(own coins)`, at `abs_weight` (0.6). The
      majority term, because the target is stated in coins: >= 300k, twice what
      the fixed evaluation opponent earns. `log1p` rather than the raw mean for
      two reasons. It is the mean *of the log*, so one blow-out episode cannot
      carry a candidate whose other episodes collapsed -- ES ranks on the whole
      seed set or it chases outliers. And it makes the anchor scale-relative:
      the same rank gap separates 20k from 40k as separates 150k from 300k, so
      the term does not go flat once the policy is rich.
    * **relative** -- `mean_e sigmoid(margin / margin_scale)`. Monotone in the
      win bit but with resolution inside a win, which the bit throws away. Kept
      because the tournament is head-to-head; demoted because measured on `fix1`
      at gen 1739 the candidate score correlated -0.90 with the *opponent's*
      coins and only +0.61 with its own, i.e. most of the search direction was
      about suppressing a clone.

    `margin_scale` is 100k, not the old 25k. The sigmoid has useful slope over
    roughly +-2 scales; at 25k that is +-50k, and once a policy is earning
    hundreds of thousands every margin sits in the flat tail and the relative
    term degenerates into the win bit it was introduced to improve on. At 100k
    the term still separates a 100k win from a 300k one (0.73 vs 0.95).

    `tape` is the per-episode mask `--tape-score ours` fills in (`Trainer.
    tape_episodes`); `None` -- every run before 2026-09-04 -- is the arithmetic
    above to the byte. Those episodes are played against a `tape_` rung, whose
    flow seat is an exogenous table: it is *credited* 25-48k a tape for products
    its board never grows, so the rung's margin is offset from the engine's by a
    per-tape 4k-41k. Calibrated against the real engine on 2026-09-04, a tape
    rung ranks small theta changes 5/6 the way the engine does on **our** coins
    and 3/6 -- a coin flip -- on the opponent's. Their relative term is
    therefore `own_coin_score`: the same coins the absolute term reads, on the
    same [0, 1] scale as every other episode's margin. The absolute term is
    untouched, since it already reads our coins alone.

    `bonus` is the day-10 shaping term (`Trainer.fitness_bonus`,
    `--d10-cash-weight` / `--tile-fill-weight`), a per-episode array **in
    coins**, or `None`. `None` -- both weights at their 0.0 default, and every
    run before 2026-09-08 -- takes the branch below verbatim, so an unshaped
    run's ranking input is not "the term times zero", it is the identical
    expression on the identical array.

    It is added to the **margin** and to nothing else. Not to `mine`: the
    absolute anchor is a claim about coins actually banked, and a shaping term
    inside `log1p(mine)` would make a candidate that ends poor but stood tall
    on day 10 look rich, which is the opposite of the anchor's job. On a
    `--tape-score ours` episode the margin is not read at all, so the same
    coins are added inside `own_coin_score` instead -- otherwise the shaping
    would be silent on exactly the tape rungs the loss ledger was built from.
    That is the one place the bonus touches an absolute reading, and it is
    forced: those episodes have no usable opponent purse.

    `ep_weight` is a per-episode weight for the two means, or `None` -- every
    run before `--pinned-once` -- which is the plain `mean` this always took,
    kept as `mean` rather than as a uniform weighted sum so an unflagged run's
    arithmetic is byte-identical and not merely equivalent.

    It exists because `--pinned-once` moves a rung's `--rung-weight` out of the
    slot allocation and into here. A pinned board is deterministic, so the four
    episodes a weight-2 rung used to take were four copies of one number `x`,
    contributing `4x` to a sum over `E` episodes; one episode at weight 4
    contributes the same `4x` to a sum of weights. The weight therefore scales
    the *board's* contribution, exactly as its replay count used to, without
    paying for the replay.
    """
    own, rel = fitness_components(mine, theirs, cfg, tape, bonus, ep_weight)
    return (cfg.abs_weight * rank_normalise(own)
            + (1.0 - cfg.abs_weight) * rank_normalise(rel))


def largest_remainder(k, weights):
    """Split `k` whole slots over `weights` in proportion, exactly. -> int[n].

    Floor every share, then hand the shortfall to the largest fractional parts.
    The alternative -- rounding each share independently -- does not sum to `k`,
    and the difference is not cosmetic: the slots are episode pairs, so a
    rounding that overshoots would index past the batch and one that undershoots
    would leave a candidate unevaluated on a pair the population shares.

    Ties in the remainder are broken by index (a stable sort), so the allocation
    is a pure function of `(k, weights)` and two runs with the same flags divide
    their ladder identically.
    """
    n = len(weights)
    w = np.asarray(weights, float)
    if n == 0 or k <= 0:
        return np.zeros(n, np.int64)
    if not np.isfinite(w).all() or (w < 0).any() or w.sum() <= 0:
        raise ValueError(f"rung weights must be finite, non-negative and not "
                         f"all zero; got {list(w)}")
    share = k * w / w.sum()
    take = np.floor(share).astype(np.int64)
    short = int(k - take.sum())
    if short > 0:
        # `-remainder` ascending == remainder descending, and `kind="stable"`
        # keeps equal remainders in index order -- which is what makes the
        # uniform case give the low-numbered rungs the spare slots, exactly as
        # the round-robin it replaces did.
        take[np.argsort(-(share - take), kind="stable")[:short]] += 1
    return take


def arch_pairs(n_pairs, n_arch, arch_frac):
    """How many of the generation's episode pairs face the archetype ladder.

    Split out of `opponent_slots` so the rotating allocator
    (`SlotCarry.take`) can be handed the same `k` the fixed allocator would
    have used, without either of them owning the rule.
    """
    k = round(arch_frac * n_pairs) if n_arch > 0 else 0
    return int(min(max(k, 0), n_pairs))


class SlotCarry:
    """Rung slot allocation that rotates across generations. -> int[n_arch]

    `largest_remainder` is a pure function of `(k, weights)`, which is exactly
    the defect the 2026-09-08 plateau review (section 2) names: with an
    unchanged configuration the same rungs take the leftover slots every
    single generation. Redrawing the board seeds does not rotate opponent
    coverage, so a pool larger than the archetype block simply loses its tail
    -- 127 equally-weighted tapes at 256 episodes (115 archetype pairs) leave
    the last 12 tapes **never sampled**, in every generation of the run.

    This is the same allocation run as a token bucket instead. Every rung
    accrues `k * w_i / sum(w)` credit per generation; the generation's `k`
    slots go one at a time to whichever rung is owed the most, and each slot
    costs its rung one unit of credit. Two consequences, both wanted:

    * The credit vector sums to zero after every generation (it gains `k` and
      spends `k`), and no rung's credit can fall below -1 -- a rung is only
      ever charged when it holds the maximum, and the maximum is at least the
      mean, which is zero. So each rung's cumulative slots track
      `total * w_i / sum(w)` to within one slot **forever**: the long-run
      proportions are the requested ones, not the ones rounding happened to
      leave.
    * A rung whose per-generation share is below one slot still gets slots,
      just not every generation. That is what makes a 127-tape pool cover all
      127 tapes.

    A zero weight is still zero slots: while any slot is left to hand out the
    running credit sums to a positive number, so the maximum is positive and
    a rung sitting at 0 credit can never hold it.

    The rotation is **between** generations only. `Trainer.generation` draws
    one index row per generation and every candidate in the population plays
    it, so common random numbers are untouched: the whole population still
    faces one opponent list on one seed list.
    """

    def __init__(self, n=0):
        self.credit = np.zeros(int(n), float)

    def resize(self, n):
        """Match a ladder that grew (`--resume` + a new `--tape-rung`)."""
        n = int(n)
        if len(self.credit) != n:
            c = np.zeros(n, float)
            m = min(n, len(self.credit))
            c[:m] = self.credit[:m]
            # Credit is only meaningful as a zero-sum vector; a ladder that
            # changed width re-centres rather than handing the survivors a
            # head start they did not earn against this rung set.
            self.credit = c - (c.mean() if n else 0.0)

    def take(self, k, weights):
        """This generation's slots per rung, and the credit moves with them."""
        w = np.asarray(weights, float)
        n = len(w)
        self.resize(n)
        take = np.zeros(n, np.int64)
        if n == 0 or k <= 0:
            return take
        if not np.isfinite(w).all() or (w < 0).any() or w.sum() <= 0:
            raise ValueError(f"rung weights must be finite, non-negative and "
                             f"not all zero; got {list(w)}")
        self.credit += k * w / w.sum()
        for _ in range(int(k)):
            # `argmax` breaks ties by lowest index, so generation 0 of a
            # uniform ladder hands out exactly the counts the round-robin did.
            j = int(np.argmax(self.credit))
            take[j] += 1
            self.credit[j] -= 1.0
        return take


def opponent_slots(n_pairs, n_pool, n_arch, arch_frac, weights=None,
                   take=None):
    """Opponent index per episode pair, into `pool + archetypes + [theta]`.

    Round-robin over the whole ladder is the right *within-group* rule -- random
    draws leave rungs unfaced, which turns the objective into "beat whoever
    showed up" and lets self-play cycle. What it got wrong was the group split:
    a flat round-robin gives every *candidate* an equal share, and the pool
    outnumbers the archetypes several to one, so ~63% of the measured run's
    episodes were played against the policy's own lineage. `arch_frac` fixes the
    archetype share directly, so the opponent the absolute yardstick is made of
    is also the opponent the gradient mostly sees.

    The archetype slots are the leading block. Position carries no information:
    the seeds are redrawn every generation and the warm-start flags are drawn
    per pair from an independent stream, so no seed or start is systematically
    tied to a group.

    `weights` re-divides *that* block. The 8-rung ladder gives every archetype
    an equal share, so `mixed_ranch` -- the one kagg2-shaped rung, and the only
    one a strong policy does not beat 128 games out of 128 -- carries 6.25% of
    the gradient's episodes while six rungs that are settled by generation 100
    carry 37.5% between them. Weighting is applied **here**, as slot
    allocation, rather than as a coefficient inside `shaped_advantage`, for
    three reasons: it keeps this module's rule intact (the opponent the
    yardstick is made of is the opponent the gradient mostly sees), it weights
    *both* fitness terms by one mixture instead of only the margin, and it buys
    variance reduction on the rung that matters instead of re-weighting a mean
    that stays as noisy as it was.

    `weights=None` is the uniform round-robin this had before, laid out
    interleaved -- so an unflagged run draws the byte-identical opponent row.
    A weight vector lays each rung's pairs out as one contiguous block
    (`np.repeat`), which is only a difference of order.

    `take` overrides the allocation entirely with a caller-supplied count per
    rung -- what `--slot-rotation carry` passes, from `SlotCarry.take`, so
    that the leftover slots move between generations instead of landing on the
    same rungs forever. It must sum to the archetype pair count this
    generation has, which is what `arch_pairs` says.
    """
    n_other = n_pool + 1                       # the pool, plus theta itself
    k = arch_pairs(n_pairs, n_arch, arch_frac)
    idx = np.empty(n_pairs, np.int64)
    if take is not None:
        # A rotating allocation (`SlotCarry.take`) decided the counts; the
        # layout below is the weighted one, so `--slot-rotation carry` differs
        # from `fixed` in *which* rungs get the spare slots and in nothing
        # else.
        take = np.asarray(take, np.int64)
        if len(take) != n_arch:
            raise ValueError(f"opponent_slots: {len(take)} rung counts for "
                             f"{n_arch} archetypes")
        if int(take.sum()) != k:
            raise ValueError(f"opponent_slots: rung counts sum to "
                             f"{int(take.sum())}, not the {k} archetype pairs "
                             f"this generation has")
        idx[:k] = n_pool + np.repeat(np.arange(n_arch), take)
    elif weights is None:
        idx[:k] = n_pool + np.arange(k) % n_arch
    else:
        if len(weights) != n_arch:
            raise ValueError(f"opponent_slots: {len(weights)} weights for "
                             f"{n_arch} archetypes")
        idx[:k] = n_pool + np.repeat(np.arange(n_arch),
                                     largest_remainder(k, weights))
    j = np.arange(n_pairs - k) % n_other
    # The current parameters are always in the non-archetype rotation: against a
    # purely frozen pool the win rate saturates between snapshots and the rank
    # signal vanishes. `n_pool` in `j` addresses theta, which lives past the
    # archetypes in the candidate list.
    idx[k:] = np.where(j == n_pool, n_pool + n_arch, j)
    return idx


def bias_mask():
    """float32[N_PARAMS]: 1 on the head, aux and development **bias**
    coordinates.

    `gb2` (18 head biases), `gb5` (3 unblock biases) and `gb6` (2 development
    biases) are the coordinates an archetype uses to state a decisive discrete
    choice, and they are the ones decoupled weight decay hurts most. Decay pins
    ||theta|| at
    lr*sqrt(n_live/(2*wd)) ~ 15.4, and spread over 3,561 live coordinates that
    leaves a head logit unable to exceed about +-1.2 -- while the hand-set
    archetypes use +-10 to +-30 to drive the land bias on `head[1]` to a
    saturated `tanh` and keep it there. A policy that cannot express a firm
    discrete decision is not being regularised, it is being clamped. These
    coordinates are exempted from decay and bounded by a clip instead.

    `gb6` joins for exactly the reason `gb5` did: `compact` decodes through a
    `relu(tanh(z))` and `dev_weight` through a softplus ratio, so both need a
    logit the decay equilibrium above does not leave room for -- a gene that
    cannot leave its first band is not regularised, it is switched off.
    """
    m = np.zeros(PO.N_PARAMS, np.float32)
    shapes = dict(PO.SHAPES)
    for name in ("gb2", "gb5", "gb6"):
        off = PO.offset(name)
        m[off:off + int(np.prod(shapes[name]))] = 1.0
    return m


def train_mask(spec: str) -> np.ndarray:
    """float32[N_PARAMS]: 1 where `spec` says the ES may move a coordinate.

    A champion-seeded run has a problem the fresh-lineage runs did not: Adam's
    per-coordinate normalisation makes every live coordinate take a step of
    about `lr` whether or not the gradient carried any signal, so a few hundred
    generations of pure noise walk a good theta a distance `lr*sqrt(gens*n)`
    away from itself in every direction at once. Restricting *which* coordinates
    the update is allowed to touch is the cheap half of the answer (`--optimizer
    sgd` is the other half): the rest of the champion is then held exactly as it
    was loaded, byte for byte, and the search happens in the handful of
    coordinates that state a decision.

    Values:

    ``all`` (or ``""``)
        every coordinate -- the behaviour of every run before this flag.
    ``biases``
        exactly what `bias_mask` marks: `gb2`/`gb5`/`gb6`, the head, aux and
        development biases. These are the coordinates an archetype uses to
        state a decisive discrete choice, and the ones a decayed-norm policy
        cannot express on its own. After `live_mask` that is **nine** live
        coordinates (`gb2` loses the 13 `DEAD_HEAD` slots, `gb5` loses
        `DEAD_AUX[0]`) -- a deliberately tiny search space, which is the point,
        but small enough to be worth the startup line that prints the count.
    ``all-biases``
        every bias block in the layout (`b1`, `b2`, `gb1`, `b3`, `gb2`, `gb5`,
        `gb6`, `gb7`, `gb8`, `gb9`, `gb10`, `gb11`), i.e. the above plus the
        head blocks appended after `bias_mask` was written -- the saturation,
        crew/herd, hire-bucket, crew-ramp and forward-admit biases -- and the
        encoder's own biases. `bias_mask` is deliberately not widened to match:
        it also governs *decay exemption*, which is a separate decision from
        what may be trained.
    a comma-separated list of `PO.SHAPES` block names
        e.g. ``g8,gb8`` for the crew/herd-mix head alone, ``gp`` for the
        global head's product residual by itself, or ``g11,gb11`` for the
        forward-admit horizon gene (33 coordinates against 6,405 -- the
        cheapest arm in the layout). Naming one appended block is the cheapest
        way to ask whether a new input path pays: the champion is held byte for
        byte and the search runs in 864 (or 33) coordinates instead of 6,405,
        so the same population buys many times the samples per live
        coordinate. A gene that reads `gh` can be moved *with* the hidden layer
        it reads by naming both, e.g. ``g1,gb1,g11,gb11``. Unknown names are
        refused here rather than silently training nothing.

    The result is AND-ed into `Trainer.mask`, which gates the *perturbation* as
    well as the update (`generation` draws `eps * self.mask`), so an excluded
    coordinate is neither jittered in the population nor moved by the step --
    the same treatment `PO.live_mask`'s dead columns already get. Masking only
    the update would leave the population carrying jitter that the fitness, and
    therefore the gradient on the coordinates that *are* trained, still sees.
    """
    spec = (spec or "all").strip()
    if spec in ("", "all"):
        return np.ones(PO.N_PARAMS, np.float32)
    if spec == "biases":
        return bias_mask()
    shapes = dict(PO.SHAPES)
    if spec == "all-biases":
        m = np.zeros(PO.N_PARAMS, np.float32)
        for name, shape in PO.SHAPES:
            if len(shape) == 1:          # a bias block is the rank-1 one
                off = PO.offset(name)
                m[off:off + int(np.prod(shape))] = 1.0
        return m
    m = np.zeros(PO.N_PARAMS, np.float32)
    names = [n.strip() for n in spec.split(",") if n.strip()]
    if not names:
        raise ValueError(f"{spec!r} names no parameter block.")
    for name in names:
        if name not in shapes:
            raise ValueError(
                f"{name!r} is not a parameter block. Use 'all', 'biases', "
                f"'all-biases', or a comma-separated list of "
                f"{', '.join(n for n, _ in PO.SHAPES)}.")
        off = PO.offset(name)
        m[off:off + int(np.prod(shapes[name]))] = 1.0
    return m


def batch_mesh():
    """One-axis mesh over every visible device, for batch-axis sharding."""
    devices = jax.devices()
    return jax.sharding.Mesh(np.array(devices), ("b",)), len(devices)


def shard_batch(mesh, *arrays):
    """Place batched arrays across the mesh along axis 0."""
    spec_ = jax.sharding.PartitionSpec("b")
    sharding = jax.sharding.NamedSharding(mesh, spec_)
    return [jax.device_put(a, sharding) for a in arrays]


def make_evaluator(hi_t, lo_t, flow_backed=False, flow_spread=False,
                   tape=None, tape_turns=None, shop_crn=False,
                   day_metrics=False, d10_cash_day=10):
    """(tables, theta_cand, theta_opp, words, seat) -> final money [mine, theirs].

    Raw coins rather than the win bit: the shaped fitness and the anchor are
    both functions of the margin and the absolute total, and the bit is
    recoverable from them with `win_scores`. Returning two floats instead of one
    costs nothing -- the episode computed both either way.

    `tables` is an argument rather than a closure so that re-randomising the
    market between generations swaps in a new price table without triggering a
    recompile (the compile is ~40 s; a generation is ~1.6 s).

    `flow_backed` / `flow_spread` are `Config.tape_flow_backed` /
    `.tape_flow_spread`, closed over as Python bools so the choice is made at
    trace time and a run with both off compiles the program it always did. See
    `sim.market.apply_flow`.

    `shop_crn` is `Config.shop_crn` / `--shop-crn`, closed over the same way
    and off by default: see `sim.eod.SHOP_CRN_BASE`.

    `tape` / `tape_turns` are `--tape-actions`' stacked device tables and their
    market-turn schedule (`es.tape_actions`, `sim.rollout.episode`). Closed over
    for the same reason the two bools are: with no action rung they are `None`
    and the replay seat is absent from the device program, not merely switched
    off in it.

    `day_metrics` is another trace-time bool. Off, every row is the 2-wide
    `[mine, theirs]` this returned before the day-10 fitness terms existed --
    which is what keeps the dozen tests that stub `Trainer.evaluate` with a
    2-column array valid. On, the row is **11 int32 columns**:

         0 mine        final coins, our seat
         1 theirs      final coins, the opponent's seat
         2 d10 mine    our coins at the end of day `d10_cash_day`
         3 d10 theirs  theirs at the end of the same day
         4 fill        sum over `TILE_FILL_DAYS` of (planted - idle), our seat
         5 units       units we sold over `LATE_PRICE_DAYS`
         6 coins       what those sales paid us
         7 units opp   units they sold over the same window
         8 coins opp   what those paid them
         9 rows        our SELL slots that moved a unit in the window
        10 sell days   days of the window on which we sold at all
        11 fwd days    our decoded `macro.forward_days` summed over the season
                       -- present only where the layout carries the `g11` gene
                       (`sim.rollout.FWD_GENE`), so a tree without the block
                       emits the eleven columns it always did

    Every column is a **count or a coin total**, never a ratio or a mean, so
    all eleven stay int32 and the array's dtype -- which `win_scores`,
    `absolute_report` and `_probe_archetypes` all read through -- is what it
    always was. The caller takes the two divisions (`TILE_FILL_NDAYS`, and
    coins/units for the realised price); doing them here would have forced the
    whole row to float and bought nothing but a rounding rule. Every reading
    comes off `episode`'s `daily` / `day_tiles` outputs, so this costs one
    wider result per episode and no second rollout.
    """
    d0, d1 = TILE_FILL_DAYS
    p0, p1 = LATE_PRICE_DAYS

    def one(tables, theta_c, theta_o, words, seat, start_nquad, start_money,
            flow, tape_ctl=None):
        a = jnp.where(seat == 0, theta_c, theta_o)
        b = jnp.where(seat == 0, theta_o, theta_c)
        out = rollout.episode(tables, jnp.stack([a, b]), words, hi_t, lo_t,
                              start_nquad, start_money, flow,
                              flow_backed=flow_backed,
                              flow_spread=flow_spread,
                              tape=tape, tape_ctl=tape_ctl,
                              tape_turns=tape_turns,
                              shop_crn=shop_crn,
                              day_tiles=day_metrics)
        money = out[0]
        mine = jnp.where(seat == 0, money[0], money[1])
        theirs = jnp.where(seat == 0, money[1], money[0])
        if not day_metrics:
            return jnp.stack([mine, theirs])
        daily, rows = out[1], out[3]
        # `daily[d]` is the purse at the *end* of day d, the same instant the
        # engine's own day boundary reports -- see `episode`'s scan.
        purse = daily[d10_cash_day]
        net = rows[d0:d1 + 1, :, 0] - rows[d0:d1 + 1, :, 1]     # [days, 2]
        fill = net.sum(axis=0)
        # Columns 2-4 of `rows` are cumulative, so a window is one subtraction:
        # `rows[p1]` is the total through the last day of it and `rows[p0 - 1]`
        # the total through the day before the first.
        win = rows[p1] - rows[p0 - 1]                           # [2, 5]
        # Per-day SELL rows inside the window, to count the days we sold on at
        # all -- "9.6 rows per selling day" is a slicing statistic, and a run
        # that sells on three days would flatter itself on a per-day mean.
        per_day = rows[p0:p1 + 1, :, 4] - rows[p0 - 1:p1, :, 4]  # [days, 2]
        sell_days = (per_day > 0).sum(axis=0).astype(jnp.int32)
        ours = lambda v: jnp.where(seat == 0, v[0], v[1])
        theirs_ = lambda v: jnp.where(seat == 0, v[1], v[0])
        cols = [mine, theirs,
                ours(purse), theirs_(purse),
                ours(fill),
                ours(win[:, 2]), ours(win[:, 3]),
                theirs_(win[:, 2]), theirs_(win[:, 3]),
                ours(win[:, 4]), ours(sell_days)]
        if rollout.FWD_GENE:
            # Column 11: our seat's decoded forward-admit horizon summed over
            # the season's days (`rows`' sixth column, which is per-day, not
            # cumulative). A count like every other column, so the row stays
            # int32; `Trainer.day_metric_means` takes the one division.
            cols.append(ours(rows[:, :, 5].sum(axis=0)))
        return jnp.stack(cols)

    plain = jax.jit(jax.vmap(
        lambda t, c, o, w, s, nq, mo: one(t, c, o, w, s, nq, mo, None),
        in_axes=(None, 0, 0, 0, 0, 0, 0)))
    with_flow = jax.jit(jax.vmap(one, in_axes=(None, 0, 0, 0, 0, 0, 0, 0)))
    with_tape = jax.jit(jax.vmap(
        lambda t, c, o, w, s, nq, mo, tc: one(t, c, o, w, s, nq, mo, None, tc),
        in_axes=(None, 0, 0, 0, 0, 0, 0, 0)))
    with_both = jax.jit(jax.vmap(one, in_axes=(None, 0, 0, 0, 0, 0, 0, 0, 0)))

    def call(tables, theta_c, theta_o, words, seat, start_nquad, start_money,
             flow=None, tape_ctl=None):
        """`flow` is `market.apply_flow`'s control word per episode, int32 [E, 3].

        `tape_ctl` is `rollout`'s `[seat, table]` word per episode, int32
        [E, 2], and is `None` on a run with no action rung. Four arms rather
        than one always-on path, for the reason the two below give: which
        opponent machinery is present has to be a *structural* fact about the
        compiled program, and each arm keeps a stable input signature, so a run
        pays one compile per combination it actually uses and nothing for the
        ones it does not.

        Two compiled programs rather than one always-on path with the flag
        pinned off. The flow code is genuinely absent from `plain`, so "the
        rung is not enabled" is a *structural* guarantee about the device
        program and not a claim about arithmetic on a zeroed table -- which is
        the property `tests/test_kagg2_flow.py::test_zero_diff` is asserting
        and the reason a run without `--kagg2-flow` needs no re-pinning. Each
        arm keeps a stable input signature, so this costs one extra compile in
        a flow run and nothing at all in every other run.
        """
        base = (tables, theta_c, theta_o, words, seat, start_nquad, start_money)
        if tape_ctl is None:
            return (plain(*base) if flow is None else with_flow(*base, flow))
        if flow is None:
            return with_tape(*base, tape_ctl)
        return with_both(*base, flow, tape_ctl)

    return call


def flow_control(seat, scale_milli=1000, shift=0, table=None):
    """`market.apply_flow` control words for a batch. -> int32 [E, 3] or [E, 4].

    `seat` is the **physical** player the measured flow drives in each episode,
    or -1 for an episode that is not playing a flow rung -- the same
    convention, and the same trap, as `place_handicap`: everywhere the rung is
    the *opponent* that is `1 - seat`, and in `_probe_archetypes`, where the
    rung is the candidate, it is `seat`.

    `scale_milli` and `shift` are the per-episode randomisation (thousandths of
    the table's units, and days the calendar slides by). They broadcast, so a
    fixed measurement passes the scalars and a training generation passes a
    drawn vector. An off episode is forced back to `market.FLOW_OFF` so that two
    batches that are off differ in nothing at all.

    `table` picks which measurement is replayed (`market.FLOW_T_KAGG2` /
    `market.FLOW_T_KAGGLE`) and broadcasts the same way. `None` -- the default,
    and what a run with no `kaggle_flow` rung passes -- emits the **3-column**
    word instead, which is a different `apply_flow` program and not a defaulted
    column: it is what keeps such a run byte-identical to the run that came
    before the second table existed.
    """
    seat = np.asarray(seat, np.int32).reshape(-1)
    sm = np.broadcast_to(np.asarray(scale_milli, np.int32), seat.shape)
    sh = np.broadcast_to(np.asarray(shift, np.int32), seat.shape)
    off = seat < 0
    cols = [seat,
            np.where(off, market.FLOW_OFF[1], sm),
            np.where(off, market.FLOW_OFF[2], sh)]
    if table is not None:
        tb = np.broadcast_to(np.asarray(table, np.int32), seat.shape)
        cols.append(np.where(off, market.FLOW_T_KAGG2, tb))
    return np.stack(cols, axis=1).astype(np.int32)


#: The seed every *fixed* thing in this campaign is drawn from: the absolute
#: measurement's seed pairs (`Trainer.__init__`) and the flow ensemble's levels
#: (`flow_ensemble_draws`). One constant, because the whole point of both is
#: that they never move between two checkpoints' numbers.
FIXED_SEED = 20260823

#: The seed the **fresh** yardstick draws come from (`--abs-fresh-draws`), kept
#: apart from `FIXED_SEED` so that "the levels this generation drew" can never
#: collide with "the levels every generation reuses".
FRESH_SEED = 20260828

#: The seed the *replicate* measurement's episode seed pairs come from
#: (`--best-replicate`). A third constant rather than a third position in the
#: fresh stream: the replicate has to differ from the screening measurement in
#: **both** axes at once (which levels, which games), and two axes drawn from
#: one stream are one axis wearing two hats.
REPLICATE_SEED = 20260829


def flow_ensemble_draws(k, scale_milli=(500, 1500), shift=(-2, 2),
                        seed=FIXED_SEED):
    """`k` fixed `(scale_milli, shift)` levels of the flow rung. -> [(int, int)]

    The yardstick's flow rung used to be read at the *centre* of the family the
    gradient trains on (scale 1.0, no day shift), which is one arbitrary member
    of it. Measured over eight archived thetas against the real engine
    (`scripts/fidelity_scoreboard.py`, 2026-08-27), the centre's margin ranks
    them at Spearman 0.738 and inverts the top three, while the **mean over ten
    fixed draws** of the family ranks them at 0.976 (leave-one-out >= 0.96).
    The centre is not merely one sample of a noisy quantity, it is the worst
    level in its own neighbourhood; averaging over the family is what removes
    the bias, not what averages the noise away.

    Fixed forever, so the statistic stays a deterministic function of theta and
    two checkpoints remain comparable -- the same property the fixed seed set
    buys, one level up. `default_rng(seed)` is drawn in exactly the order
    `Trainer.episode_flow` draws a generation's levels (all `k` scales, then
    all `k` shifts), so an ensemble member is a level a training episode could
    actually have been played at rather than a grid someone chose, and the
    numbers line up with the scoreboard's table.

    The two ranges are arguments rather than `cfg.kagg2_flow_scale` /
    `cfg.kagg2_flow_jitter` because the yardstick and the gradient want
    different things from them: the gradient wants breadth, the yardstick wants
    to sit where the real matchup sits, and the real engine's margins matched
    the sim's around scale 1.3 / shift +2 rather than at 1.0 / 0. Passing the
    training ranges reproduces the scoreboard's table exactly, since the
    defaults are those ranges.
    """
    k = int(k)
    if k <= 0:
        return []
    lo, hi = (int(x) for x in scale_milli)
    slo, shi = (int(x) for x in shift)
    if lo <= 0 or hi < lo:
        raise ValueError(f"abs_flow_scale {(lo, hi)}: needs 0 < lo <= hi, in "
                         f"thousandths (1000 is the table's own level).")
    if shi < slo:
        raise ValueError(f"abs_flow_shift {(slo, shi)}: needs lo <= hi, in days.")
    rng = np.random.default_rng(seed)
    # `uniform` on the *float* scale and then `rint(x * 1000)`, not `uniform`
    # on the thousandths directly: it is the arithmetic `episode_flow` does, so
    # the default range reproduces the drawn levels bit for bit.
    scale = np.rint(rng.uniform(lo / 1000.0, hi / 1000.0, k) * 1000).astype(np.int32)
    days = rng.integers(slo, shi + 1, k).astype(np.int32)
    return [(int(s), int(d)) for s, d in zip(scale, days)]


def fresh_flow_draws(k, gen, replicate=0, scale_milli=(500, 1500),
                     shift=(-2, 2)):
    """`k` levels drawn for *this* measurement alone. -> [(int, int)]

    The fixed ensemble (`flow_ensemble_draws`) buys comparability between two
    checkpoints and pays for it with a static target: `best_abs` is a max over
    a sequence of readings of the *same ten games*, so a long enough run stops
    selecting the theta that plays the family well and starts selecting the one
    that plays those ten levels well. Measured on 2026-08-27: over 150
    generations at K=10 the record climbed +12.9k -> +17.8k while the same
    theta's centre margin sat at ~-5k throughout, and the "best" scored -3,255
    against the real engine where the run's starting theta scored +2,465.

    Re-drawing every measurement makes the record a max over readings the
    optimiser could not have aimed at: the level set that produced a lucky
    reading is gone by the next measurement, so a theta can only keep the
    record by being good against the *family*. It gives up the property the
    fixed set was for -- two measurements are no longer of literally the same
    thing -- which is why it is a flag and why the ladder signature carries it.

    Deterministic in `(gen, replicate)`, so a resumed run re-draws the same
    levels it would have drawn, and a rerun of a generation reproduces it.
    `replicate` is 0 for the screening measurement and 1..N for the replicates
    of `--best-replicate`, which is what keeps a replicate's levels independent
    of the screening levels it is checking.
    """
    return flow_ensemble_draws(k, scale_milli, shift,
                               seed=[FRESH_SEED, int(gen), int(replicate)])


def cold_starts(n_pairs):
    """The engine's day 0 for `n_pairs` episode pairs: (nquad, money), int32 [n, 2]."""
    return (np.ones((n_pairs, 2), np.int32),
            np.full((n_pairs, 2), spec.STARTING_MONEY, np.int32))


def place_handicap(nquad, money, side, handicap):
    """Raise one seat's opening in each row. -> (nquad, money), int32 [n, 2].

    `side[e]` is the **physical** player index (0 or 1) the handicap belongs to
    in episode `e`, and `handicap[e]` is its `(nquad, money)`. Both arrays are
    per *episode*, never per seed pair -- which is the whole point, and the one
    place this change is not local.

    `make_evaluator.one` seats the candidate at player 0 only when `seat == 0`,
    so an asymmetric row indexed by pair would hand the opening to the
    *candidate* on one of the pair's two seats: the rung would be handicapped in
    one game and we would be handicapped in the other, and the pair's margin
    would average the two into nothing. `Trainer` therefore builds its starts at
    episode resolution and passes `1 - seat` here.

    `maximum` rather than assignment, so a handicap can only ever add: a warm
    start (`draw_starts`) that already opened the pair on four quadrants and
    40,000 coins is not walked *back* to the rung's three and 20,000.
    """
    nquad, money = np.array(nquad, np.int32), np.array(money, np.int32)
    if nquad.shape[0] == 0:
        return nquad, money
    h = np.asarray(handicap, np.int32).reshape(-1, 2)
    row = np.arange(nquad.shape[0])
    col = np.asarray(side, np.int64)
    nquad[row, col] = np.maximum(nquad[row, col], h[:, 0])
    money[row, col] = np.maximum(money[row, col], h[:, 1])
    return nquad, money


def host_words(seeds):
    """[E, N_DAYS, STREAM_WORDS] uint32 -- the engine's own generator, drained."""
    return np.stack([
        np.stack([eod.host_stream(int(s), d) for d in range(spec.N_DAYS)])
        for s in seeds
    ])


#: Salt for `pinned_seed_word`, so the fixed board a pinned rung plays is not
#: also some other derivation's number. Bumping it re-rolls every pinned
#: board once and for all, which is the only way to ask "was that board's
#: verdict about the theta or about that board".
PINNED_SEED_SALT = b"kagg3.pinned.seed.v1"


def pinned_seed_word(name) -> int:
    """The fixed seed word a pinned rung plays on. -> int in [0, 2**31 - 1)

    `name` is the ladder label (`tape_act_<episode>`), so the word is a
    function of the recorded episode and of nothing else -- not of the rung's
    position on the ladder, not of the generation, not of the process.

    blake2b rather than `hash()`: CPython salts `hash(str)` per process, so a
    resumed run (or a second machine in the same sweep) would put the same
    pinned tape on a different board and the whole point would be lost. This
    digest is the same everywhere forever.

    Why not the engine's seed. The pinned judge
    (`scripts/eval_vs_baselines.py --seed-per-opponent`) draws opponent `i`'s
    seed from `seed_base + SEED_STRIDE * (i + 1)` -- `i` is the tape's POSITION
    in that leg's `--opponents` list, so the same tape is played on
    975191099 in one leg and on something else in the next, and there is no
    "the seed the engine uses for this tape" to match. The engine's weeds are
    a draw like ours; what a pinned board must be is *one* game, not the
    engine's particular one.
    """
    d = hashlib.blake2b(str(name).encode("utf-8"), key=PINNED_SEED_SALT,
                        digest_size=8).digest()
    return int(int.from_bytes(d, "big") % (2 ** 31 - 1))


class AbsReport(NamedTuple):
    """One absolute-strength measurement, split into selection and holdout.

    Every scalar here is a **rung-weighted** mean of the per-rung means, using
    the same weights the gradient's slot allocation uses, so the yardstick and
    the objective describe one mixture. At uniform weights that is the plain
    mean it always was.

    The fields after `holdout_win` are additive: they carry defaults so an
    older positional construction still works, and so nothing that only wants
    coins has to learn about the rest.
    """
    coins: float            # selection seeds: mean own coins over all archetypes
    win: float              # selection seeds: win rate over all archetypes
    mine: tuple             # selection seeds: mean own coins, per archetype
    theirs: tuple           # selection seeds: mean opponent coins, per archetype
    holdout: float          # holdout seeds: mean own coins
    holdout_win: float      # holdout seeds: win rate
    score: float = 0.0      # selection seeds: mean sigmoid(margin / margin_scale)
    holdout_score: float = 0.0        # the same on the holdout seeds
    wins: tuple = ()        # selection seeds: win rate, per archetype
    keep: tuple = ()        # per archetype: its coins here / its zero-theta coins
    live: tuple = ()        # per archetype: did it clear `collapse_floor`
    weights: tuple = ()     # per archetype: the weight it entered the means at
    holdout_rungs: tuple = ()   # per held-out rung: (label, own, theirs, margin, win)


    # The holdout half's twins of `mine`/`theirs`, so a per-rung quantity can be
    # gated on unseen seeds the same way a headline is. Same array, same call,
    # the other mask -- a second evaluator call would be a second input shape
    # and a ~40 s XLA compile (see `absolute_report`). Both are 0.0 for every
    # rung when `abs_pairs` is too small to leave a holdout half at all, which
    # is exactly what `holdout` already reports in that case.
    holdout_mine: tuple = ()    # holdout seeds: mean own coins, per archetype
    holdout_theirs: tuple = ()  # holdout seeds: mean opponent coins, per archetype
    # The de-biased flow yardstick (`--abs-flow-draws`), for the log line and
    # nothing else: every *selected* number above already reads the ensemble
    # when it is on. `flow_draws` is 0 for a run without it, which is what the
    # log gates on -- the other two are then 0.0 and mean nothing.
    flow_draws: int = 0             # K the flow rung was measured over
    flow_ens_margin: float = 0.0    # flow rung margin, mean over the K draws
    flow_centre_margin: float = 0.0  # the same rung at the family's centre
    # *Which* K levels, not just how many. Redundant under the fixed ensemble
    # (the run header prints them once and they never move), and the whole
    # audit trail under `--abs-fresh-draws`, where every measurement is read at
    # levels of its own and "K=10" no longer says what was played.
    flow_levels: tuple = ()         # the (scale_milli, shift) pairs, in order
    # `--select-metric softwin:<rung>:<tau>` reads a *nonlinear* function of
    # each game's margin, and no pair of coin means can reconstruct it: the
    # mean of tanh is not the tanh of the mean. It therefore has to be reduced
    # where the per-game array still exists, which is `absolute_report`, and
    # carried out per rung like `mine`/`theirs`. Empty under every other
    # metric -- a `coins` or `margin:` run builds the report it always built.
    softwin: tuple = ()         # selection seeds: mean tanh(margin/tau), per rung
    holdout_softwin: tuple = ()  # the same on the holdout half


class GenerationField(NamedTuple):
    """The randomness and opponents shared by one population evaluation."""
    noise: object
    key: object
    next_key: object
    seeds: object
    opponent_index: object
    keep: object
    words: object
    opponents: object
    tables: object
    starts: tuple
    flow: object
    tape_ctl: object
    tape: object
    episodes: object
    layout: object
    episode_weight: object
    rung_episodes: dict


class ScopeDiagnostic(NamedTuple):
    """Saved inputs and outputs of the fixed no-update scope comparison."""
    scopes: tuple
    pairs: int
    field: GenerationField
    masks: object
    masked_noise: object
    money: object
    own: object
    relative: object
    own_rank: object
    relative_rank: object
    advantage: object
    gradients: object


#: `--select-metric margin:<rung>`: the prefix, and the separator an operator
#: types. The rung is named, not indexed, because the ladder's indices move
#: (the flow rung and every `--rung-theta` anchor append) while the names do
#: not -- the same reason `--rung-weight` is keyed by name.
MARGIN_PREFIX = "margin:"

#: `--select-metric softwin:<rung>:<tau>`: the same rung, read through a tanh
#: of width `tau` coins instead of raw coins. The rung is named the same way
#: and for the same reason; `tau` rides on the metric string rather than on a
#: flag of its own so that one string still says what the yardstick *is* --
#: which is what `ladder_signature` checkpoints and what a resume compares.
SOFTWIN_PREFIX = "softwin:"


class SelectSpec(NamedTuple):
    """`--select-metric`, parsed. -> (kind, rung, tau)."""
    kind: str               # "coins", "score", "margin" or "softwin"
    rung: str | None        # the rung named, for the two per-rung kinds
    tau: float | None       # tanh width in coins; `softwin` only


def select_spec(metric) -> SelectSpec:
    """Parse a `--select-metric` string. -> SelectSpec. Raises on a typo.

    One parser, because the spec is read in a dozen places -- selection, the
    holdout twin, the ladder check, the record gate, the log header -- and a
    string sliced in a dozen places is a string that means twelve slightly
    different things. Every rejection here is an error rather than a silent
    fallback to coins: an unknown metric that quietly selected on coins is
    exactly the failure `--select-metric` was added to fix.
    """
    m = str(metric)
    if m in ("coins", "score"):
        return SelectSpec(m, None, None)
    if m.startswith(MARGIN_PREFIX):
        name = m[len(MARGIN_PREFIX):]
        if not name:
            raise ValueError(f"select_metric {m!r}: "
                             f"{MARGIN_PREFIX}<rung> needs a rung name.")
        return SelectSpec("margin", name, None)
    if m.startswith(SOFTWIN_PREFIX):
        name, sep, tau = m[len(SOFTWIN_PREFIX):].rpartition(":")
        if not sep or not name:
            raise ValueError(
                f"select_metric {m!r}: {SOFTWIN_PREFIX}<rung>:<tau> needs a "
                f"rung name and a tau in coins, e.g. "
                f"{SOFTWIN_PREFIX}kagg2_flow:3000.")
        try:
            tau = float(tau)
        except ValueError:
            raise ValueError(
                f"select_metric {m!r}: tau {tau!r} is not a number. It is the "
                f"tanh's width in coins, e.g. "
                f"{SOFTWIN_PREFIX}{name}:3000.") from None
        if not (tau > 0) or not math.isfinite(tau):
            raise ValueError(
                f"select_metric {m!r}: tau must be positive and finite -- it "
                f"divides the margin, and {tau} is either a division by zero, "
                f"a sign flip, or a metric that is constant.")
        return SelectSpec("softwin", name, tau)
    raise ValueError(
        f"select_metric {m!r}: expected 'coins', 'score' or "
        f"'{MARGIN_PREFIX}<rung>', or '{SOFTWIN_PREFIX}<rung>:<tau>'")


#: "no record yet", for `best_abs` and `champion_score`.
#:
#: It used to be `-1.0`, which was safe only while every selectable metric was
#: a positive one (yardstick coins, or a sigmoid in [0, 1]). A *margin* is
#: routinely negative -- the thetas measured against kagg2 sit near -5,000 on
#: the `kagg2_flow` rung -- so `-1.0` would have refused every one of them as
#: "worse than no record at all" and the run would never write `best_abs.npy`.
#: `-inf` is the only sentinel nothing legitimate can sit under. It survives
#: `state.npz` (`np.float64(-inf)` round-trips exactly); what it does not
#: survive is `json.dumps`, so `scripts/train.py` logs `None` for it instead.
NO_BEST = -math.inf

#: Rounds of resampling `Trainer` allows a *sampled* archetype that fails the
#: liveness probe before it gives up and raises.
PROBE_TRIES = 8
#: Episode seed pairs the liveness probe plays per archetype (x2 seats).
PROBE_PAIRS = 4

#: The archetype whose planner sits behind the `kaggle_flow` rung. The rung's
#: market presence is the measured table, so this only has to put a board and a
#: hiring schedule of roughly the right shape in front of the policy's opponent
#: features -- and the Kaggle field is a field of tuned wheat clones (137 wheat
#: tiles, 12-14 hands by day 10), not of kagg2s.
KAGGLE_PLANNER = "wheat_clone"

#: The archetype whose planner sits behind a `--tape-rung`. The tapes we cut
#: are class-A Kaggle seats, which is the same field `KAGGLE_PLANNER` stands in
#: for -- and for the same reason: what the rung asserts is the measured market
#: presence, and the planner is only there to put a board of roughly the right
#: shape in front of the policy's opponent features.
TAPE_PLANNER = KAGGLE_PLANNER


def read_eval_csv(path):
    """(win rate, mean margin, games) off an `eval_vs_baselines.py --csv`, or
    `None` if the file is missing, empty or not that CSV.

    The summary the script prints is parsed by nobody: the per-game rows are
    written after the last game and carry the two columns the gate needs, so
    reading them is both cheaper to get right and the same arithmetic
    `scripts/kagg2_track_row.py` does for the tracker -- a tie counts a half.
    """
    try:
        with open(path, newline="") as fh:
            rows = list(csv.DictReader(fh))
    except OSError:
        return None
    wins, margins = [], []
    for r in rows:
        try:
            mine, theirs = float(r["mine"]), float(r["theirs"])
        except (KeyError, TypeError, ValueError):
            return None
        wins.append(1.0 if mine > theirs else (0.5 if mine == theirs else 0.0))
        margins.append(mine - theirs)
    if not wins:
        return None
    return float(np.mean(wins)), float(np.mean(margins)), len(wins)


def read_eval_games(path):
    """`{(seed, opponent, seat): (mine, theirs)}` off the same CSV, or `None`.

    `read_eval_csv` pools the rows into two means and throws the rows away, and
    with them the only thing that makes the gate's two legs *paired*: both legs
    of a `--real-gate-fresh` round play the same seed base against the same
    field, so every game the candidate played has a twin in the incumbent's
    CSV. Differencing those twins removes the board from the comparison
    entirely -- the board lottery is worth +-8 win-rate points between seed
    sets of this size, which is several times the gap the gate is asked to
    resolve -- and leaves a per-game difference whose spread is a *measurable*
    standard error rather than a guessed one (`paired_stats`).

    The key is the evaluator's own `(seed, opponent, seat)`, which is exactly
    what `scripts/paired_ci.py` pairs on, so the gate and the offline
    confidence interval read one definition of "the same game".
    """
    try:
        with open(path, newline="") as fh:
            rows = list(csv.DictReader(fh))
    except OSError:
        return None
    out = {}
    for r in rows:
        try:
            key = (int(r["seed"]), r["opponent"], int(r["seat"]))
            out[key] = (float(r["mine"]), float(r["theirs"]))
        except (KeyError, TypeError, ValueError):
            return None
    return out or None


def pinned_tape_id(path):
    """The tape an `--opponents` path names, for a pinned gate's log.

    `artifacts/panel_opp_town/opponent_tape_105228357/main.py` is the episode
    `105228357` -- the same id the town schedule is keyed by, so a flip in the
    log can be looked up in the schedule and in the live game it replicates.
    Anything else keeps enough of its path to be identified (the directory of a
    bare `main.py`, else the file name).
    """
    parts = str(path).replace("\\", "/").split("/")
    for part in reversed(parts):
        if part.startswith("opponent_tape_"):
            return part[len("opponent_tape_"):]
    if parts and parts[-1] == "main.py" and len(parts) > 1:
        return parts[-2]
    return parts[-1] if parts else str(path)


def pinned_tally(cand, inc):
    """Flips and drops between two legs of a pinned round, or `None`.

    `cand` / `inc` are `read_eval_games` maps of the *same* games -- in pinned
    mode every opponent is played once per seat played (`--real-gate-pinned-
    seats`) under its recorded town, and the town is the only thing the
    outcome depended on, so the two legs are the same live-replica board
    played by two policies. Rows are counted as they come: at two seats a
    board that changes hands is worth two flips, at one seat it is worth one.

    A **flip** is a game the incumbent did not win and the candidate did; a
    **drop** is the reverse. Both are counted on the strict `mine > theirs`
    the leaderboard scores, which is also what
    `scratchpad/lossflip/flips.py` counts, so a gate row and the offline
    ledger of the same pair are the same two numbers.

    `cand_wins - inc_wins == flips - drops` by construction, which is why the
    acceptance rule can be stated in either currency.
    """
    if not cand or not inc:
        return None
    keys = [k for k in cand if k in inc]
    if not keys:
        return None
    flipped, dropped = [], []
    cand_wins = inc_wins = 0
    cw_score = iw_score = 0.0
    cand_margin = inc_margin = 0.0
    for k in sorted(keys, key=lambda k: (str(k[1]), int(k[2]), int(k[0]))):
        cm, ct = cand[k]
        im, it = inc[k]
        c_won, i_won = cm > ct, im > it
        cand_wins += int(c_won)
        inc_wins += int(i_won)
        cw_score += 1.0 if cm > ct else (0.5 if cm == ct else 0.0)
        iw_score += 1.0 if im > it else (0.5 if im == it else 0.0)
        cand_margin += cm - ct
        inc_margin += im - it
        label = f"{pinned_tape_id(k[1])}/{int(k[2])}"
        if c_won and not i_won:
            flipped.append(label)
        elif i_won and not c_won:
            dropped.append(label)
    n = len(keys)
    return {"n": n, "cand_wins": cand_wins, "inc_wins": inc_wins,
            "flips": len(flipped), "drops": len(dropped),
            "flipped": flipped, "dropped": dropped,
            # The tie-counting-a-half rates `read_eval_csv` reports, so the
            # margin metric and `--real-gate-win-floor` compare like with like.
            "cand_win": cw_score / n, "inc_win": iw_score / n,
            "cand_margin": cand_margin / n, "inc_margin": inc_margin / n}


def paired_stats(cand, inc, group_seats=True):
    """Paired candidate-minus-incumbent statistics over the games both played.

    -> `{"n", "boards", "win", "margin", "t_win", "t_margin"}`, or `None` when
    the two legs share no game (a failed leg, a resume that lost the rows, or a
    run whose CSV predates the `seed` column).

    `win`/`margin` are the *mean paired differences*: the candidate's win score
    minus the incumbent's on the same board and seat, and the same for coins.
    `t_win`/`t_margin` are those means over their own standard errors -- a
    one-sample t on the differences, which is the test the comparison has
    always deserved. It is computed here rather than assumed because the
    per-game difference of two policies on one board is far quieter than
    either policy's own game-to-game spread, so the standard error the gate
    needs cannot be read off a win rate's binomial.

    **The two seats of a board are one observation, not two.** The rows are
    keyed `(seed, opponent, seat)` and the evaluator plays every board from
    both sides, so the row count is twice the number of independent boards --
    and the two mirrored games are strongly correlated (frequently the same
    outcome, and always the same market draw). Dividing by `sqrt(2n_boards)`
    when the evidence is `n_boards` inflates the statistic by up to `sqrt(2)`:
    the plateau review's probe (section 3) took ten independent board outcomes
    from t = 3.00 to t = 4.36 purely by duplicating each into a second seat.
    So the differences are **averaged within `(seed, opponent)`** before the
    spread is taken. `n` stays the number of paired *games* (what the operator
    counted) and `boards` is the number the t is computed on.

    The means are untouched by the grouping when the seats are balanced, which
    they are by construction; `group_seats=False` restores the old
    row-independent statistic for a caller that wants to see the difference.

    A pair that never differs (`sd == 0`) is `inf` when the mean is non-zero
    and 0.0 when it is not: two thetas that scored identically on every shared
    game are the same reading, and no threshold should let one displace the
    other.
    """
    keys = [k for k in cand if k in inc]
    if not keys:
        return None
    dw, dm, groups = [], [], []
    for k in keys:
        cm, ct = cand[k]
        im, it = inc[k]
        cw = 1.0 if cm > ct else (0.5 if cm == ct else 0.0)
        iw = 1.0 if im > it else (0.5 if im == it else 0.0)
        dw.append(cw - iw)
        dm.append((cm - ct) - (im - it))
        # The key is `(seed, opponent, seat)`; the board is the first two.
        groups.append(tuple(k[:2]) if isinstance(k, tuple) and len(k) >= 2
                      else k)
    order = {}
    for g in groups:
        order.setdefault(g, len(order))
    gid = np.asarray([order[g] for g in groups], np.int64)
    n_boards = len(order)
    out = {"n": len(keys), "boards": n_boards if group_seats else len(keys)}
    for name, d in (("win", np.asarray(dw, float)),
                    ("margin", np.asarray(dm, float))):
        mean = float(d.mean())
        if group_seats and n_boards < len(keys):
            # One number per board: the mean of that board's seats.
            per = (np.bincount(gid, weights=d, minlength=n_boards)
                   / np.bincount(gid, minlength=n_boards))
        else:
            per = d
        centre = float(per.mean())
        sd = float(per.std(ddof=1)) if per.size > 1 else 0.0
        se = sd / math.sqrt(per.size) if sd > 0 else 0.0
        out[name] = mean
        out["t_" + name] = (centre / se if se > 0 else
                            (math.copysign(math.inf, centre) if centre else 0.0))
    return out


def _write_npy(path, arr):
    """`np.save` to `path` exactly (no `.npy` suffix games), atomically.

    Atomic because the eval subprocess's workers `np.load` the candidate file
    once per game: a half-written one is a crashed worker, and an in-place
    rewrite while an earlier eval still reads it is the bug
    `scripts/remote_eval_kagg2.sh` archives a copy to avoid.
    """
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        np.save(fh, np.asarray(arr))
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


class CandidateKeeper:
    """`--keep-candidates`: every gated theta kept, with the verdict it got.

    The gate reuses one candidate file (`real_gate_cand.npy`, overwritten per
    eval, because the training host's root disk sits near full), so once a run
    is over the thetas it *refused* are gone: `log.jsonl` has their numbers and
    nothing has their weights. With the flag on, every nomination is copied to
    `<run>/cands/g{gen:05d}_{kind}.npy` **before** the eval starts and left
    there, and every verdict appends one line to `<run>/cands/index.jsonl` --
    so a finished run can be mined for its near-misses, not just for the
    record it took.

    Off by default and reached only through `RealGate.keeper`, which is `None`
    unless `scripts/train.py` was given the flag: a run without it writes the
    same files, in the same order, that it wrote before this class existed.
    Nothing here is ever deleted, and nothing here is read back by the gate --
    it is a side-channel for the operator, not state the run depends on.
    """

    #: The nomination kinds that get a file. A replicate re-measures a theta
    #: already saved under its own generation, so it adds a verdict line and
    #: no second copy.
    KINDS = ("record", "periodic")

    def __init__(self, run_dir):
        self.dir = os.path.join(run_dir, "cands")
        os.makedirs(self.dir, exist_ok=True)
        self.index_path = os.path.join(self.dir, "index.jsonl")
        #: gen -> (kind, file, md5), for the verdicts that land later.
        self.saved = {}

    @staticmethod
    def _md5(path):
        with open(path, "rb") as fh:
            return hashlib.md5(fh.read()).hexdigest()

    def save(self, theta, gen, kind):
        """Keep `theta` as the `kind` nomination of generation `gen`."""
        name = f"g{int(gen):05d}_{kind}.npy"
        path = os.path.join(self.dir, name)
        _write_npy(path, np.asarray(theta, np.float32))
        self.saved[int(gen)] = (kind, name, self._md5(path))
        return path

    def _lookup(self, gen):
        """(kind, file, md5) of the theta kept at `gen`, or `(None,)*3`.

        In memory for the run that saved it, off disk for a resumed one --
        whose replicate verdict lands in a process that never saw the
        nomination it belongs to.
        """
        if int(gen) in self.saved:
            return self.saved[int(gen)]
        for kind in self.KINDS:
            name = f"g{int(gen):05d}_{kind}.npy"
            path = os.path.join(self.dir, name)
            if os.path.isfile(path):
                return kind, name, self._md5(path)
        return None, None, None

    @staticmethod
    def verdict_of(res):
        """One word for what the gate did with this theta.

        Confirmation and revert are read before the error flag: a replicate
        whose *eval* crashed still confirms the provisional record
        (`_settle_replicate`), and what happened to the theta is the record
        moving, not the subprocess dying.
        """
        if res.get("confirmed"):
            return "replicate-confirmed"
        if res.get("reverted"):
            return "replicate-failed"
        if res.get("error"):
            return "failed"
        if res.get("provisional"):
            return "provisional"
        return "accepted" if res.get("accepted") else "rejected"

    def record(self, res, gate):
        """Append this verdict's line to `index.jsonl`."""
        def f(x):
            return None if x is None else float(x)

        gen = int(res.get("gen", -1))
        kind, name, md5 = self._lookup(gen)
        bar_win, bar_margin = res.get("incumbent_win"), res.get("incumbent_margin")
        ref = bar_win if gate.metric == "win" else bar_margin
        row = {
            "gen": gen, "kind": kind, "file": name, "md5": md5,
            "verdict": self.verdict_of(res),
            # Which leg produced the line: "record"/"periodic" is the
            # nomination itself, "replicate" its second reading.
            "source": res.get("source"),
            "win": f(res.get("win")), "margin": f(res.get("margin")),
            "games": int(res.get("games") or 0),
            # The incumbent played on the *same* seed base
            # (`--real-gate-fresh`); `None` when the round was not paired.
            "paired_win": f(res.get("paired_win")),
            "paired_margin": f(res.get("paired_margin")),
            # The bar: the incumbent's pooled numbers, and the single number
            # the candidate had to clear in the units of `metric`.
            "bar_win": f(bar_win), "bar_margin": f(bar_margin),
            "bar": None if ref is None else float(ref) + float(gate.min_gain),
            "metric": gate.metric, "min_gain": float(gate.min_gain),
        }
        if res.get("replicate_win") is not None:
            row["replicate_win"] = f(res.get("replicate_win"))
            row["replicate_margin"] = f(res.get("replicate_margin"))
        if res.get("error"):
            row["error"] = str(res["error"])
        with open(self.index_path, "a") as fh:
            fh.write(json.dumps(row) + "\n")
            fh.flush()
        return row


class RealGate:
    """A real-engine veto on the in-sim record (`--real-gate`).

    The in-sim selector is a **proxy** for the tournament, and the proxy stops
    tracking it: across ~10 runs the record thetas taken after ~1.5k
    generations score progressively *worse* against the real `kagg2` while the
    in-sim margin they were selected on keeps rising (flow23: 64.6% -> 52.1%
    -> 47.9% real win rate over three consecutive records). Every one of those
    records was written to `best_abs.npy`, which is the file `--promote`
    ships, so the run's deliverable got worse while its log got better.

    The real engine is the only arbiter that cannot drift, and it is cheap:
    48 games against a packaged opponent is ~3 CPU-minutes, on a host whose
    12 cores the GPU trainer barely touches. So under this flag the in-sim
    record only *nominates* -- `scripts/eval_vs_baselines.py` plays the
    nomination in the real engine, and `best_abs.npy` moves only if the real
    number improved.

    Three properties the implementation is built around:

    * **The trainer never blocks.** The eval is a `Popen` in its own session,
      polled once per generation (`poll`); a generation costs seconds and an
      eval minutes, so waiting on it would spend most of the run idle.
    * **Queue depth 1.** Only one eval is in flight; a candidate nominated
      while one runs replaces any earlier waiting one. Measuring a stale
      candidate is worth less than measuring the newest, and an unbounded
      queue would fall further behind the run forever.
    * **The two records are separate objects.** The in-sim threshold
      (`Trainer.best_abs`) keeps moving on in-sim acceptances, exactly as
      before, so a gate rejection cannot wedge the nomination stream; the
      gated theta (`Trainer.best_abs_theta`, `best_abs.npy`) moves only here.
      The in-sim record's theta is kept beside it as `best_sim.npy`.

    `--real-gate-every N` adds a second source of nominations: the search
    centre, offered on a cadence whenever the gate is idle, so that the record
    keeps being contested in the long stretches where the in-sim selector
    produces nothing (`due`).

    `--real-gate-replicate` re-measures every acceptance on a fresh seed base
    and keeps the incumbent's numbers as the pooled reading over both evals,
    which is what stops the bar from drifting up to the luckiest n=48 draw the
    run ever made (`_pool`). With it on the acceptance is **provisional** --
    the previous incumbent is held in `prev_incumbent` and the record moves
    only when the candidate's pooled pair beats it (`_confirm`), or goes back
    to it when it does not (`_revert`).

    `--real-gate-opponent` takes a comma-separated **field** rather than a
    single agent. One packaged opponent is one thing to overfit; the evaluator
    plays `--real-gate-games` seeds x 2 seats against *each* member and writes
    them into the one CSV, which `read_eval_csv` pools -- so the bar becomes a
    reading over the field (4 opponents x 24 games = 192 games a leg).

    `--real-gate-fresh` replaces the two fixed seed bases with a fresh one per
    nomination and plays the incumbent on it too, one leg after the other in
    the single slot, so that what decides is a paired reading on games neither
    theta was selected on (`_fresh_leg`, `_decide_round`).

    `--real-gate-min-gain` is the size of the improvement the gate insists on
    (`beats`). A win rate over 128-256 games has a standard deviation of 3-4
    points, and the old rule accepted on *any* excess -- so one extra win of
    128 moved the record, and with `--real-gate-recentre` it moved the search
    centre too. flow59 accepted gen 200 on a paired 47.7% vs 46.9% (one game)
    and confirmed it pooled at 46.1%/-230 against an incumbent that had read
    53.5%/+3,080. A threshold is not a significance test, but it is the cheap
    half of one: with it the record only moves on a gap the noise does not
    routinely produce. 0 (the default) is the strict rule this build has
    always had, tie-break and all.
    """

    #: The evaluator, relative to the repo root. A plain
    #: `scripts/eval_vs_baselines.py` invocation, so the gate measures what
    #: `scripts/remote_eval_kagg2.sh` measures and the two numbers are
    #: comparable rather than merely similar.
    SCRIPT = os.path.join("scripts", "eval_vs_baselines.py")

    @staticmethod
    def as_field(opponent):
        """A field of packaged agents as a tuple, from whatever says it.

        A plain string is one opponent unless it carries commas, which is how
        `--real-gate-opponent` spells a field on one command line; a list (a
        `real_gate.json` written by this build) is already the field. The tuple
        is what `_start` splats into separate `--opponents` argv entries --
        handing the evaluator one comma-joined string instead would seat a
        single opponent whose `main.py` does not exist.
        """
        if opponent is None:
            return ()
        if isinstance(opponent, str):
            parts = opponent.split(",")
        else:
            parts = [p for one in opponent for p in str(one).split(",")]
        return tuple(p.strip() for p in parts if p.strip())

    @property
    def opponent(self):
        """The field as one string, for logs and for the JSON of older
        builds. `opponents` is the tuple everything else works on."""
        return ",".join(self.opponents)

    @staticmethod
    def field_of(state):
        """The opponent field a saved `real_gate.json` records, as a tuple.

        Handles both shapes: this build writes a list, and every gate state
        written before the field existed holds a single string.
        """
        return RealGate.as_field(state.get("opponent"))

    @staticmethod
    def min_gain_of(state):
        """The acceptance threshold a saved `real_gate.json` records.

        A state written before the flag existed carries no key, which is 0.0 --
        the strict rule those runs were gated by. Unlike the opponent field
        this is not a property of the *measurement*, so a resume that changes
        it is legal (see `load`); it is read only so the change can be said
        out loud.
        """
        try:
            return float(state.get("min_gain") or 0.0)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def paired_t_of(state):
        """The paired-t threshold a saved `real_gate.json` records.

        A state written before the flag existed carries no key, which is 0.0 --
        the test switched off, which is how every gated run before it decided.
        Like `min_gain` it is read only so a resume that changes it can say so.
        """
        try:
            return float(state.get("paired_t") or 0.0)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def win_floor_of(state):
        """The win-rate floor a saved `real_gate.json` records, or `None`.

        `None` -- which is what a state written before the flag existed
        carries, and what an explicit `null` means -- is the floor switched
        off: the margin metric ranks on the margin alone, the rule this build
        had. 0.0 is a floor that happens to allow no drop at all, so the two
        are *not* the same thing and this must not collapse them. Like
        `min_gain` it is a threshold rather than a measurement, so it is read
        only to say out loud that a resume changed it (see `load`).
        """
        v = state.get("win_floor")
        if v is None:
            return None
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def seed_per_opponent_of(state):
        """Whether a saved `real_gate.json` drew a seed list per opponent.

        A state written before the flag existed carries no key, which is
        False -- the one shared list those legs were measured on. Like
        `min_gain` this is read only so a resume that changes it can say so.
        """
        return bool(state.get("seed_per_opponent"))

    #: Games per opponent in pinned mode. One: the schedule pins the town,
    #: the board carries no other seed randomness, and a second seed would
    #: replay the same game under another name.
    PINNED_GAMES = 1

    def __init__(self, run_dir, opponent, games=24, workers=4,
                 seed_base=20260825, metric="win", every=0, replicate=False,
                 recentre=0, fresh=False, fresh_seed=0, min_gain=0.0,
                 win_floor=None, seed_per_opponent=False, paired_t=0.0,
                 replicate_games=None, pinned=None, min_flips=1,
                 pinned_seats=2, script=None, python=None, cwd=None,
                 residual=None, residual_head_py=None):
        if metric not in ("win", "margin"):
            raise ValueError(f"real_gate_metric {metric!r}: expected "
                             f"'win' or 'margin'")
        if float(min_gain) < 0:
            raise ValueError(f"real_gate_min_gain {min_gain!r}: expected >= 0 "
                             f"(0 = the strict rule)")
        if float(paired_t) < 0:
            raise ValueError(f"real_gate_paired_t {paired_t!r}: expected >= 0 "
                             f"(0 = no significance test)")
        if win_floor is not None and float(win_floor) < 0:
            raise ValueError(f"real_gate_win_floor {win_floor!r}: expected "
                             f">= 0 (0 = the win rate may not drop at all); "
                             f"None = no floor")
        if win_floor is not None and metric != "margin":
            raise ValueError(f"real_gate_win_floor {win_floor!r}: only the "
                             f"margin metric ranks without the win rate, so "
                             f"only it has a win rate to floor")
        if int(every) < 0:
            raise ValueError(f"real_gate_every {every!r}: expected >= 0")
        if int(recentre) < 0:
            raise ValueError(f"real_gate_recentre {recentre!r}: expected >= 0")
        if int(min_flips) < 0:
            raise ValueError(f"real_gate_min_flips {min_flips!r}: expected "
                             f">= 0 (a gate that may accept a candidate which "
                             f"flips nothing)")
        if int(pinned_seats) not in (1, 2):
            raise ValueError(f"real_gate_pinned_seats {pinned_seats!r}: "
                             f"expected 1 or 2")
        # src/kagg3/es/train.py -> the repo root, which is the cwd
        # `eval_vs_baselines.py` needs (it does `sys.path.insert(0, "src")`).
        root = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))))
        self.cwd = cwd or root
        self.script = script or os.path.join(self.cwd, self.SCRIPT)
        self.python = python or sys.executable
        self.run_dir = run_dir
        # The gate measures against a *field*: one packaged agent, or several.
        # `eval_vs_baselines.py` plays `--games` seeds x 2 seats against every
        # opponent it is handed and writes them all into the one CSV, which
        # `read_eval_csv` already pools regardless of the `opponent` column --
        # so a field costs proportionally more wall clock and nothing else.
        self.opponents = self.as_field(opponent)
        self.games, self.workers = int(games), int(workers)
        # `--real-gate-replicate-games`: the confirmation is the reading that
        # actually decides -- the provisional verdict only buys the right to be
        # re-measured -- so it is the one worth spending more games on. `None`
        # is `--real-gate-games`, which is what every run before the flag
        # played on both rounds.
        if replicate_games is not None and int(replicate_games) < 1:
            raise ValueError(f"real_gate_replicate_games {replicate_games!r}: "
                             f"expected >= 1 (omit for --real-gate-games)")
        self.replicate_games = (self.games if replicate_games is None
                                else int(replicate_games))
        # Written once per process, the first time a pinned eval starts.
        self._pinned_noted = False
        # `--real-gate-pinned SCHEDULE`: judge on the PINNED LIVE-REPLICA set
        # instead of a seed draw. A `--with-town` opponent package replays a
        # real Kaggle game move for move, and the only thing the engine still
        # draws for itself is the end-of-day shop -- which the schedule pins
        # (`scripts/town_inject.py`, off unless `KAGG3_TOWN_SCHEDULE` names
        # the file, which `_start` sets for the eval it launches). With the
        # town pinned the engine replays the live game: measured 2026-09-09 on
        # four tapes, the outcome is the live one in both seats and on every
        # seed base tried, and the coins reproduce the recorded ledger to the
        # coin on most rows (the weeds are still keyed on the seed, so a board
        # can move by a fraction of a percent without changing hands -- which
        # is why both legs play ONE fixed base and are therefore the identical
        # board). So the whole set is one deterministic question -- which of
        # the games we actually lost would this candidate have flipped -- and
        # a seed count, a replicate and a significance test are all answers to
        # a lottery that is no longer being run (see `_decide_pinned` and the
        # note `_start` writes once).
        self.pinned = (None if pinned is None or not str(pinned).strip()
                       else os.path.abspath(str(pinned)))
        # `--real-gate-min-flips`: how many net live games (flips minus drops)
        # a candidate has to turn round before the record moves. 1 -- the
        # default -- is the weakest rule that still says something: the
        # candidate wins a game the incumbent lost and gives none back.
        self.min_flips = int(min_flips)
        # `--real-gate-pinned-seats`: how many seats of each pinned board a
        # leg plays. 2 -- the default -- is the gate that shipped before the
        # flag, byte for byte. 1 plays seat 0 only, which is the honest count
        # once the town is pinned: measured 2026-09-09, both seats of a pinned
        # tape return the SAME coins for our agent, so the second seat is a
        # re-measurement of the first. It halves the wall clock and, more to
        # the point, makes every count below -- games, wins, flips, drops, and
        # therefore `--real-gate-min-flips` -- one per BOARD instead of two.
        # Read only under `self.pinned`; an unpinned draw is a lottery whose
        # seat bias the pairing is there to cancel.
        self.pinned_seats = int(pinned_seats)
        # `--residual`: the frozen action head the candidate theta flies
        # [ACTIONRL8/ESHEAD]. The gate's whole job is to measure the agent that
        # will be uploaded, and `package_submission.py --residual` puts the
        # head inside the tarball's `main.py` -- so a run training theta under
        # a head has to hand the head to the evaluator too, or the veto is
        # cast on a different agent than the one the run is building. Passed
        # straight through to `eval_vs_baselines.py --residual`, which arms it
        # on the `--theta` seat only.
        self.residual = (None if not residual else os.path.abspath(str(residual)))
        self.residual_head_py = (None if not residual_head_py
                                 else os.path.abspath(str(residual_head_py)))
        if self.residual and not os.path.isfile(self.residual):
            raise ValueError(f"real_gate residual {self.residual!r}: no such "
                             f"head .npz")
        # What pinned mode makes meaningless, kept so the banner and the log
        # can say which flags on the command line are inert.
        self.pinned_ignored = ()
        if self.pinned:
            self.pinned_ignored = tuple(
                name for name, on in (
                    ("--real-gate-games", int(games) != self.PINNED_GAMES),
                    ("--real-gate-replicate", bool(replicate)),
                    ("--real-gate-replicate-games",
                     replicate_games is not None),
                    ("--real-gate-fresh", bool(fresh)),
                    ("--real-gate-seed-per-opponent",
                     bool(seed_per_opponent)),
                    ("--real-gate-paired-t", float(paired_t) > 0))
                if on)
            # Replication of a deterministic game measures the same number
            # twice, and a fresh seed base draws the same games again: both
            # rounds are dropped rather than run. The fixed seed stays
            # `--real-gate-seed-base`, and it is a formality -- the schedule,
            # not the seed, is what the outcome depends on.
            replicate, fresh, seed_per_opponent, paired_t = (
                False, False, False, 0.0)
            # `self.games` is already set above from the flag, so both the
            # local and the attribute are put back to the one game a pinned
            # leg plays.
            games = replicate_games = self.PINNED_GAMES
            self.games = self.replicate_games = self.PINNED_GAMES
        self.seed_base, self.metric = int(seed_base), metric
        # `--real-gate-min-gain`: how much better than the incumbent a
        # candidate has to read before the record moves, in the units of
        # `metric` (win-rate points as a fraction, or coins). 0 keeps the
        # strict-improvement rule with its margin tie-break, byte for byte.
        self.min_gain = float(min_gain)
        # `--real-gate-win-floor`: under `--real-gate-metric margin` the win
        # rate has no say at all, and a candidate that trades the head-to-head
        # bit for coins is accepted on the strength of the margin alone. The
        # floor keeps the margin as the primary (better-powered, continuous)
        # statistic while refusing a candidate whose win rate has fallen more
        # than SLACK below the incumbent's. `None` = off, the rule this build
        # had; 0.0 = the win rate may not drop at all. Not a `float(... or 0)`
        # anywhere: 0.0 and `None` are different settings.
        self.win_floor = None if win_floor is None else float(win_floor)
        # `--real-gate-seed-per-opponent`: hand the evaluator its own seed
        # list per member of the field, so a leg of k opponents samples
        # `games * k` distinct seeds instead of the same `games` seeds k
        # times. The games and the wall clock are the same; only the seed
        # noise of the leg changes (see `eval_vs_baselines.seed_lists`).
        self.seed_per_opponent = bool(seed_per_opponent)
        # `--real-gate-paired-t`: the significance test `min_gain` is only the
        # cheap half of. Both legs of a fresh round play the same seed base, so
        # the CSVs pair game by game; the candidate has to clear the incumbent
        # by T standard errors of the *per-game difference*, not merely by
        # `min_gain` points of a mean whose error nobody measured. 0.0 -- the
        # default -- reads no per-game rows and decides exactly what this build
        # decided before the flag. See `paired_stats`.
        self.paired_t = float(paired_t)
        # Every (candidate, incumbent) game map the current round pair has
        # produced, so the confirmation can run the same test over both bases.
        # Memory only: a resume mid-round loses them and falls back to the
        # unpaired rule for that one round, which is what it did anyway.
        self.round_games = []
        # `--real-gate-every N`: nominate the search centre every N
        # generations even when the in-sim selector has produced no record.
        # 0 = off, and the gate is fed by records alone (see `due`).
        self.every = int(every)
        # `--real-gate-replicate`: re-measure every acceptance on
        # `seed_base + 1` and pool the two readings (see `_pool`).
        self.replicate = bool(replicate)
        # `--real-gate-recentre K`: consecutive *periodic* candidates refused
        # since the last confirmation, and the K that ends the run of them by
        # putting the search back on the record (`recentre_due`). Only the
        # periodic ones count: they are readings of the search centre itself,
        # so a run of them is evidence about where the centre *is*, which is
        # the thing the re-centre acts on. An in-sim record being refused says
        # something about that record, not about the centre.
        self.recentre = int(recentre)
        self.periodic_rejects = 0
        # `--real-gate-fresh`: a new seed base per nomination, the incumbent
        # replayed on it, and a paired decision. `base_seq` is the draw
        # counter (the bases are a function of it and `--seed`, so a resume
        # continues the sequence rather than replaying it); `base_results`
        # caches what the *current* incumbent scored on the bases it has been
        # played on, so the second leg is skipped when it is already known.
        self.fresh = bool(fresh)
        self.fresh_seed = int(fresh_seed)
        self.base_seq = 0
        self.base_results = {}
        self.round = None       # the paired round in flight
        self.leg = None         # "candidate" | "incumbent" within it
        self.inc_leg = None     # (theta, gen, base) owed for the open round
        # Which kind of candidate the in-flight replicate belongs to, so that
        # a revert can be counted against the centre when it was the centre
        # that was provisionally accepted.
        self.replicate_source = None
        # The incumbent's real numbers, from its own gated eval. `None` is
        # "never measured": the first result to land takes the record whatever
        # it says, which is what makes a start-of-run baseline a baseline.
        self.win = None
        self.margin = None
        self.record_gen = None
        # The theta those numbers belong to, and -- while a provisional
        # acceptance waits for its replicate -- the incumbent it displaced.
        # `prev_incumbent` is what `_revert` puts back; `None` is "the record
        # is settled".
        self.record_theta = None
        self.prev_incumbent = None
        # Where `record_theta` came from, for the resume banner: the gate's
        # own state file, `best_abs.npy` beside it, or nowhere at all.
        self.theta_source = "unknown"
        # Games behind `win`/`margin`. It is `games * 2` for a single eval and
        # twice that once a replicate has been pooled in, and it is the weight
        # the pooling uses -- so it has to be state, not a constant.
        self.n = 0
        # Does `best_abs_theta` hold a *gate-accepted* theta? A cold gated run
        # holds none until the first result lands, and `best_abs.npy` must not
        # be written before then -- it would ship the untrained init under the
        # name of a record.
        self.have_record = False
        self.pending = None         # (theta, gen, source) waiting for the slot
        self.running = None         # (theta, gen, source) being measured
        # The re-measurement an acceptance owes, `(theta, gen)`. It jumps the
        # queue: until it lands the incumbent's numbers are a single noisy
        # reading, and every candidate compared against them is compared
        # against that noise.
        self.replicate_due = None
        self.proc = None
        self.log_fh = None
        self.evals = self.accepts = self.rejects = self.failures = 0
        self.replicates = self.reverts = 0
        # `--keep-candidates`, off unless `setup_real_gate` attaches one.
        # Nothing in the gate reads it back; see `CandidateKeeper`.
        self.keeper = None
        # A killed trainer must not leave a `--workers`-wide pool of engine
        # processes behind; `close` is idempotent, so the explicit call at the
        # end of a run and this one cannot double-kill.
        atexit.register(self.close)

    # ------------------------------------------------------------- the files
    @property
    def seats(self):
        """Seats per seed a leg of this gate plays: 2, or 1 when pinned mode
        was told to.

        `eval_vs_baselines.py` plays both seats of every seed so that seat
        bias cancels inside the pair, and on a drawn board that is not
        optional. A pinned board is not drawn: the schedule fixes the only
        thing the engine still rolls, both seats come back with the same
        coins, and the second one buys no information -- so
        `--real-gate-pinned-seats 1` makes a game a BOARD, which is the unit
        flips and drops were always meant to be counted in.
        """
        return self.pinned_seats if self.pinned else 2

    @property
    def csv_path(self):
        """Overwritten per eval: one file, not one per record, on a host whose
        root disk sits at 97% full. The verdicts themselves are in
        `log.jsonl`."""
        return os.path.join(self.run_dir, "real_gate.csv")

    @property
    def theta_path(self):
        return os.path.join(self.run_dir, "real_gate_cand.npy")

    @property
    def json_path(self):
        return os.path.join(self.run_dir, "real_gate.json")

    @property
    def pending_path(self):
        return os.path.join(self.run_dir, "real_gate_pending.npy")

    @property
    def replicate_path(self):
        return os.path.join(self.run_dir, "real_gate_replicate.npy")

    @property
    def prev_path(self):
        return os.path.join(self.run_dir, "real_gate_prev.npy")

    # ------------------------------------------------------------- the queue
    def propose(self, theta, gen, source="record"):
        """Nominate a theta. Queue depth 1: the newest nomination wins.

        `source` is carried through to the verdict (`real_gate_source` in
        `log.jsonl`) so that a gate row can be read back as what it was:
        `"record"` is an in-sim record nominating itself, `"periodic"` is the
        `--real-gate-every` cadence offering the search centre.
        """
        if self.keeper is not None:
            # Before the queue, so a nomination the next one displaces is on
            # disk too -- it was still a theta this run thought worth playing.
            self.keeper.save(theta, gen, source)
        self.pending = (np.asarray(theta, np.float32), int(gen), source)
        self._launch()

    def due(self, gen):
        """Should the `--real-gate-every` cadence nominate at `gen`?

        Only when the gate is otherwise **idle**: an eval in flight or a
        candidate already waiting means the cadence has nothing to add, and
        replacing a waiting in-sim record with the live centre would throw
        away the nomination the selector actually asked for. Generation 0 is
        never due -- it is the untrained init on a cold run.
        """
        return (self.every > 0 and int(gen) > 0 and int(gen) % self.every == 0
                and self.proc is None and self.pending is None
                and self.replicate_due is None)

    def recentre_due(self):
        """Has the centre drifted far enough to be put back (`--real-gate-
        recentre`)?

        `K` consecutive periodic refusals is the evidence: the gate has said
        no to the search centre `K` times running while the record stood, so
        the centre is somewhere the real engine likes less than a theta the
        run already has. Never mid-replicate -- the record it would jump onto
        is provisional until the second reading lands, and jumping onto a
        theta that is about to be reverted is the drift with extra steps.
        """
        return (self.recentre > 0 and self.have_record
                and self.periodic_rejects >= self.recentre
                and self._replicate_waiting() is None)

    def _launch(self):
        """Start the waiting work if the single slot is free.

        A replicate goes first. It is not a candidate competing for the
        record; it is the *bar* the next candidate will be judged against, and
        measuring another candidate before it is measuring against a number
        the gate already knows is half-formed. Ahead of even that comes the
        second leg of an open `--real-gate-fresh` round: the round has already
        spent an eval and decides nothing until the incumbent has been played
        on the same base.
        """
        if self.proc is not None:
            return
        if self.inc_leg is not None:
            theta, gen, base, games = self.inc_leg
            self.inc_leg = None
            self.leg = "incumbent"
            # The same game count as the leg it is being paired with: a round
            # whose two legs played different numbers of games is not a pair.
            self._start(theta, gen, base, "incumbent", games)
            return
        if self.replicate_due is not None:
            theta, gen = self.replicate_due
            self.replicate_due = None
            self.running = (theta, gen, "replicate")
        elif self.pending is not None:
            self.running, self.pending = self.pending, None
        else:
            return
        theta, gen, source = self.running
        base = self.seed_base + (1 if source == "replicate" else 0)
        games = (self.replicate_games if source == "replicate" else self.games)
        if self.pinned:
            # The pinned set is not a draw: one game per opponent per seat
            # played (`--real-gate-pinned-seats`, both by default), on
            # the fixed `--real-gate-seed-base`, under the recorded town. The
            # round is paired like a fresh one -- the incumbent replays the
            # same set -- but there is no base to draw and no second round to
            # confirm on.
            base, games = self.seed_base, self.PINNED_GAMES
        if self.pinned or self.fresh:
            if not self.pinned:
                base = self._next_base()
            self.round = {"gen": gen, "source": source, "theta": theta,
                          "base": base, "cand": None, "inc": None,
                          "games": games}
            self.leg = "candidate"
        self._start(theta, gen, base, source, games)

    def _start(self, theta, gen, base, leg, games=None):
        """Run one eval: this theta, on this seed base, into `csv_path`.

        `games` is the round's own count (`--real-gate-replicate-games` lets a
        replicate round be larger than a screening one); `None` is
        `--real-gate-games`, the count every leg played before that flag.
        """
        _write_npy(self.theta_path, theta)
        # A previous eval's CSV must never be read back as this one's result;
        # dropping it first is what makes "the file exists" mean "this eval
        # wrote it" (the script writes it once, after the last game).
        try:
            os.remove(self.csv_path)
        except OSError:
            pass
        # One `--opponents` flag, one argv entry per member of the field: the
        # evaluator's `nargs="*"` takes them all, and it plays `--games` seeds
        # x `self.seats` seats against each.
        cmd = [self.python, self.script, "--theta", self.theta_path,
               "--opponents", *self.opponents,
               "--games", str(int(games or self.games)),
               "--workers", str(self.workers),
               "--seed-base", str(int(base)), "--csv", self.csv_path]
        # Appended, not inserted: with the flag off the argv is byte-identical
        # to the one every gated run before it launched.
        if self.seed_per_opponent:
            cmd.append("--seed-per-opponent")
        # Likewise: `--real-gate-pinned-seats 2` (the default) adds nothing,
        # so the pinned argv that shipped before this flag is unchanged.
        if self.seats != 2:
            cmd += ["--seats", str(int(self.seats))]
        # The head the candidate flies, on the same terms: absent, the argv is
        # the one an un-headed run launches.
        if self.residual:
            cmd += ["--residual", self.residual]
            if self.residual_head_py:
                cmd += ["--residual-head-py", self.residual_head_py]
        # Not a context manager: the handle is the child's stdout and has to
        # outlive this call, until `poll` or `close` reaps the process.
        self.log_fh = open(os.path.join(self.run_dir, "real_gate.log"), "a")  # noqa: SIM115
        if self.pinned and not self._pinned_noted:
            # Said once, not once a leg: which flags this mode makes inert is
            # a property of the run, and the operator reads it at the top of
            # the log rather than between every pair of legs.
            self._pinned_noted = True
            inert = ", ".join(self.pinned_ignored) or "none on this command line"
            seats = ("2 seats; a board is 2 games" if self.seats == 2 else
                     "seat 0 only; a board is 1 game, and every count below "
                     "-- games, wins, flips, drops -- is per BOARD")
            self.log_fh.write(
                f"=== pinned mode: {self.pinned}\n"
                f"=== pinned mode seats: {self.seats} ({seats})\n"
                f"=== pinned mode plays every opponent once per seat "
                f"({self.PINNED_GAMES} game x {self.seats} seat"
                f"{'' if self.seats == 1 else 's'}) on the fixed seed base "
                f"{self.seed_base}; the schedule pins the town, so the game is "
                f"deterministic and the seed decides nothing.\n"
                f"=== pinned mode IGNORES --real-gate-games, "
                f"--real-gate-replicate-games, --real-gate-fresh, "
                f"--real-gate-seed-per-opponent and --real-gate-paired-t, and "
                f"--real-gate-replicate is a no-op (replicating a "
                f"deterministic game re-measures the same number). Inert "
                f"here: {inert}.\n")
        self.log_fh.write(f"=== gen {gen} ({leg}): {' '.join(cmd)}\n")
        self.log_fh.flush()
        # Its own session: the child then does not receive the terminal's
        # SIGINT (an operator's Ctrl-C would otherwise kill the eval and the
        # trainer would read a truncated CSV), and `close` can reap the whole
        # worker pool with one `killpg`.
        # `None` = inherit, which is what every gated run before pinned mode
        # launched with. Under `--real-gate-pinned` the evaluator's workers
        # read the schedule off this variable (`scripts/town_inject.py`,
        # called per game by `eval_vs_baselines._play` with the opponent path
        # as the key) -- that env var IS how the town reaches the engine.
        env = (None if not self.pinned
               else dict(os.environ, KAGG3_TOWN_SCHEDULE=self.pinned))
        self.proc = subprocess.Popen(
            cmd, cwd=self.cwd, stdout=self.log_fh, stderr=subprocess.STDOUT,
            env=env, start_new_session=True)

    def poll(self):
        """One non-blocking check. The finished eval's verdict, or `None`.

        Called once per generation. `Popen.poll()` is a `waitpid(WNOHANG)`;
        nothing here waits, sleeps or reads the child's output.
        """
        if self.proc is None:
            self._launch()
            return None
        rc = self.proc.poll()
        if rc is None:
            return None
        theta, gen, source = self.running
        self.proc = None
        if self.log_fh is not None:
            self.log_fh.close()
            self.log_fh = None
        res = {"gen": gen, "rc": int(rc), "source": source, "win": None,
               "margin": None,
               "games": 0, "accepted": False, "baseline": self.win is None,
               "incumbent_win": self.win, "incumbent_margin": self.margin,
               "theta": theta}
        read = read_eval_csv(self.csv_path) if rc == 0 else None
        # Read before `_start` deletes the file for the next leg. Only under
        # the flag: with it off nothing downstream looks at them.
        games = (read_eval_games(self.csv_path)
                 if rc == 0 and (self.paired_t > 0 or self.pinned) else None)
        self.evals += 1
        if self.fresh or self.pinned:
            out = self._fresh_leg(res, read, rc, gen, source, games)
            if out is not None and self.keeper is not None:
                self.keeper.record(out, self)
            self._launch()
            return out
        self.running = None
        if source == "replicate":
            self._settle_replicate(res, read, rc)
        elif read is None:
            # A failed eval decides nothing: the candidate is dropped and the
            # incumbent stands. The next in-sim record nominates again, so a
            # transient failure costs one measurement, not the run.
            self.failures += 1
            res["error"] = (f"eval exited {rc}" if rc != 0
                            else f"no readable {self.csv_path}")
        else:
            win, margin, n = read
            res.update(win=win, margin=margin, games=n)
            res["accepted"] = self.accepts_result(win, margin)
            if not res["accepted"] and source == "periodic":
                self.periodic_rejects += 1
            if res["accepted"] and self.replicate:
                # Provisional. The incumbent is held aside, the candidate's
                # single reading becomes the working bar so the replicate can
                # pool into it, and nothing outside the gate moves until the
                # replicate has confirmed it (`_settle_replicate`).
                if self.win is not None:
                    # Whatever there is a *bar* for. This used to require
                    # `have_record` and a known `record_theta`, which is a
                    # statement about `best_abs.npy` rather than about the
                    # number a candidate has to beat -- and the two come
                    # apart on exactly the resume this matters on: a retired
                    # in-sim record (`--reset-best`, a ladder change) clears
                    # `have_record` in `setup_real_gate` while the gate's
                    # real-engine numbers stand. flow28e confirmed a
                    # candidate whose pooled 68.8% was 11pp *below* the
                    # 80.2% bar it was measured against, because nothing was
                    # stashed for it to fail. The theta is optional: it is
                    # what a revert would put back in `best_abs.npy`, and if
                    # it is unknown the numbers still have to be defended.
                    self.prev_incumbent = {
                        "theta": (None if self.record_theta is None else
                                  np.asarray(self.record_theta, np.float32)),
                        "win": self.win, "margin": self.margin,
                        "n": int(self.n), "record_gen": self.record_gen}
                res["accepted"], res["provisional"] = False, True
                self.win, self.margin, self.record_gen = win, margin, gen
                self.n, self.record_theta = n, theta
                self.replicate_due = (theta, gen)
                self.replicate_source = source
            elif res["accepted"]:
                self.win, self.margin, self.record_gen = win, margin, gen
                self.n, self.record_theta = n, theta
                self.have_record = True
                self.accepts += 1
                self.periodic_rejects = 0
            else:
                self.rejects += 1
        if self.keeper is not None:
            self.keeper.record(res, self)
        self._launch()
        return res

    # ------------------------------------------------------ the fresh pairing
    def _next_base(self):
        """The next seed base (`--real-gate-fresh`).

        A function of the run's `--seed` and a counter, so the sequence is
        reproducible and a resume continues it rather than replaying it --
        replaying would hand the run the same "fresh" games it has already
        selected on, which is the thing the flag exists to prevent.
        """
        self.base_seq += 1
        rng = np.random.default_rng([self.fresh_seed, self.base_seq])
        return int(rng.integers(1_000_000, 9_000_000))

    def _incumbent_ref(self):
        """(theta, per-base readings) of the theta a candidate must beat.

        While a provisional record is awaiting its replicate the theta to beat
        is the one it *displaced*, not the provisional record itself -- and if
        it displaced nothing (the first record of a run) there is nothing to
        pair with, so the round is the candidate's leg alone.
        """
        if self.replicate_source is not None or self.prev_incumbent is not None:
            p = self.prev_incumbent
            if p is None:
                return None, {}
            return p.get("theta"), p.setdefault("base_results", {})
        return self.record_theta, self.base_results

    @staticmethod
    def _pooled(readings):
        """Games-weighted (win, margin, n) over `{base: [win, margin, n]}`."""
        tot = sum(r[2] for r in readings.values())
        if tot <= 0:
            return None, None, 0
        return (sum(r[0] * r[2] for r in readings.values()) / tot,
                sum(r[1] * r[2] for r in readings.values()) / tot, tot)

    def _remember(self, cache, base, read, cap=8):
        """Cache one reading, keeping the last `cap` bases."""
        cache[str(int(base))] = [read[0], read[1], read[2]]
        while len(cache) > cap:
            cache.pop(next(iter(cache)))

    def _fresh_leg(self, res, read, rc, gen, source, games=None):
        """One leg of a paired round: the verdict, or `None` mid-round."""
        rnd = self.round
        base = rnd["base"]
        res["base"] = base
        leg, self.leg = self.leg, None
        if leg == "incumbent":
            rnd["inc_games"] = games
            if read is not None:
                self._note_incumbent(base, read)
            else:
                # The bar's own eval failed. The round falls back to the
                # incumbent's pooled numbers rather than being thrown away.
                self.failures += 1
            rnd["inc"] = self._incumbent_ref()[1].get(str(int(base)))
            self.running = None
            return self._decide_round(res, rnd, rc)
        rnd["cand"] = read
        rnd["cand_games"] = games
        if read is None:
            # The candidate's own eval failed: nothing to compare, and the
            # incumbent leg would only spend a second one.
            self.failures += 1
            res["error"] = (f"eval exited {rc}" if rc != 0
                            else f"no readable {self.csv_path}")
            self.running, self.round = None, None
            if source == "replicate":
                self._confirm(res)
            return res
        inc_theta, cache = self._incumbent_ref()
        # In pinned mode the base never changes, so a cache hit would answer
        # every round with an earlier round's reading -- and the decision
        # needs the incumbent's own per-game rows on these games, which a
        # cached pair of pooled numbers does not carry. The bar replays.
        cached = (not self.pinned) and str(int(base)) in cache
        if source == "replicate" and self.paired_t > 0:
            # flow112: the replicate re-played the CANDIDATE alone, so the
            # confirmation pooled its two bases against the incumbent's
            # earlier, different ones -- the unpaired comparison this flag
            # exists to abolish, wearing a paired verdict's name. A cached
            # reading is a number without per-game rows behind it, so it
            # cannot stand in for the leg either.
            cached = False
        if inc_theta is not None and not cached:
            # The second leg: the same games, the other theta.
            self.inc_leg = (inc_theta, gen, base, rnd.get("games", self.games))
            return None
        rnd["inc"] = cache.get(str(int(base)))
        self.running = None
        return self._decide_round(res, rnd, rc)

    def _note_incumbent(self, base, read):
        """Record what the incumbent scored on `base`, and pool it in.

        The pooled numbers are the incumbent's running record over every base
        it has been played on. They are what the log reports and what an
        unpaired comparison falls back to; they are never what a paired
        decision uses.
        """
        _, cache = self._incumbent_ref()
        self._remember(cache, base, read)
        who = self.prev_incumbent if self.prev_incumbent is not None else self
        win, margin, n = read
        if self.pinned:
            # A deterministic re-measurement of the same games. Pooling it
            # would grow `n` by the size of the set every round while the
            # numbers never moved, and report a confidence the one game per
            # tape does not carry; the reading simply stands.
            self.win, self.margin, self.n = win, margin, n
            return
        if isinstance(who, dict):
            tot = int(who["n"]) + n
            who["win"] = (who["win"] * who["n"] + win * n) / tot
            who["margin"] = (who["margin"] * who["n"] + margin * n) / tot
            who["n"] = tot
        elif self.win is not None and self.n > 0:
            tot = self.n + n
            self.win = (self.win * self.n + win * n) / tot
            self.margin = (self.margin * self.n + margin * n) / tot
            self.n = tot

    def _decide_round(self, res, rnd, rc):
        """The paired verdict for a finished round."""
        if self.pinned:
            return self._decide_pinned(res, rnd)
        cw, cm, cn = rnd["cand"]
        gen, source, theta, base = (rnd["gen"], rnd["source"], rnd["theta"],
                                    rnd["base"])
        self.round = None
        res.update(win=cw, margin=cm, games=cn)
        prev = self.prev_incumbent
        bar_w, bar_m = ((prev["win"], prev["margin"]) if prev is not None
                        else (self.win, self.margin))
        res["incumbent_win"], res["incumbent_margin"] = bar_w, bar_m
        inc = rnd["inc"]
        if inc is not None:
            res["paired_win"], res["paired_margin"] = inc[0], inc[1]
            iw, im = inc[0], inc[1]
        else:
            # No paired reading (no incumbent, or its theta is unknown -- a
            # retired in-sim record takes `best_abs_theta` with it). The bar
            # still stands: an unpaired comparison is worse than a paired one,
            # and far better than none.
            iw, im = bar_w, bar_m
        # The two legs' per-game rows, kept whichever branch decides below:
        # the provisional verdict tests one base, the confirmation both.
        pair = (rnd.get("cand_games"), rnd.get("inc_games"))
        if source == "replicate":
            # The provisional record's second base joins its own record; the
            # confirmation pools over both.
            self._remember(self.base_results, base, rnd["cand"])
            self.round_games.append(pair)
            return self._confirm_fresh(res, iw, im)
        ps = (paired_stats(*pair) if self.paired_t > 0
              and pair[0] and pair[1] else None)
        # A baseline has nothing to be significantly better than: with no bar
        # measured yet the first reading takes the record unopposed, exactly as
        # `beats` lets it, and the test starts at the round after. Bound before
        # the `and` rather than short-circuited by it, so the log row carries
        # the paired statistic whichever half of the rule refused the
        # candidate -- the two rules disagreeing is the interesting row.
        sig = self.win is None or self._significant(ps, res)
        res["accepted"] = self.beats(cw, cm, iw, im) and sig
        if not res["accepted"] and source == "periodic":
            self.periodic_rejects += 1
        if res["accepted"] and self.replicate:
            if self.win is not None:
                self.prev_incumbent = {
                    "theta": (None if self.record_theta is None else
                              np.asarray(self.record_theta, np.float32)),
                    "win": self.win, "margin": self.margin,
                    "n": int(self.n), "record_gen": self.record_gen,
                    "base_results": self.base_results}
            res["accepted"], res["provisional"] = False, True
            self.base_results = {}
            self.round_games = [pair]
            self._remember(self.base_results, base, rnd["cand"])
            self.win, self.margin, self.record_gen = cw, cm, gen
            self.n, self.record_theta = cn, theta
            self.replicate_due = (theta, gen)
            self.replicate_source = source
        elif res["accepted"]:
            self.base_results = {}
            self.round_games = []
            self._remember(self.base_results, base, rnd["cand"])
            self.win, self.margin, self.record_gen = cw, cm, gen
            self.n, self.record_theta = cn, theta
            self.have_record = True
            self.accepts += 1
            self.periodic_rejects = 0
        else:
            self.rejects += 1
        return res

    def _decide_pinned(self, res, rnd):
        """The verdict for a round on the pinned live-replica set.

        The set is not a sample. Every opponent is a `--with-town` recording
        of a real Kaggle game, the schedule pins the only draw the engine
        still makes for itself, and both seats of a pinned tape come back with
        the same outcome -- so the games are the live games themselves,
        replayed, and the question the gate is asked stops being "is this
        candidate better on average" and becomes "which of these games would
        it have flipped". Because the two seats agree, N boards read as 2N
        identical games under the default `--real-gate-pinned-seats 2` and as
        N under `1`; the rule below is the same arithmetic either way, but
        only under `1` is a flip counted once.

        That is why the rule is counted rather than averaged. Under
        `--real-gate-metric win` a candidate is accepted when its net flips
        (games the incumbent did not win and it did, minus the reverse) reach
        `--real-gate-min-flips` AND it wins strictly more of the set: the two
        conditions are the same arithmetic at `min_flips >= 1`, and the second
        is what keeps `min_flips 0` from accepting a candidate that changed
        nothing. `margin` keeps the mean-coins rule (`beats`, with
        `--real-gate-min-gain` and `--real-gate-win-floor`), measured on the
        incumbent's own reading of these same games rather than on a pooled
        bar from another set.

        A round with no incumbent leg -- the first candidate of a run has
        nothing to be judged against -- falls back to `beats`, which takes a
        first reading unopposed and refuses anything that cannot clear an
        existing bar.
        """
        cw, cm, cn = rnd["cand"]
        gen, source, theta = rnd["gen"], rnd["source"], rnd["theta"]
        self.round = None
        res.update(win=cw, margin=cm, games=cn)
        res["incumbent_win"], res["incumbent_margin"] = self.win, self.margin
        tally = pinned_tally(rnd.get("cand_games"), rnd.get("inc_games"))
        res["pinned"] = True
        if tally is None:
            res["accepted"] = self.beats(cw, cm, self.win, self.margin)
        else:
            res.update(paired_win=tally["inc_win"],
                       paired_margin=tally["inc_margin"],
                       pinned_n=tally["n"], pinned_flips=tally["flips"],
                       pinned_drops=tally["drops"],
                       pinned_wins=tally["cand_wins"],
                       pinned_incumbent_wins=tally["inc_wins"],
                       pinned_flipped=list(tally["flipped"]),
                       pinned_dropped=list(tally["dropped"]))
            if self.metric == "margin":
                res["accepted"] = self.beats(tally["cand_win"],
                                             tally["cand_margin"],
                                             tally["inc_win"],
                                             tally["inc_margin"])
            else:
                res["accepted"] = (
                    (tally["flips"] - tally["drops"]) >= self.min_flips
                    and tally["cand_wins"] > tally["inc_wins"])
        self._log_pinned(res, tally, gen, source)
        if not res["accepted"] and source == "periodic":
            self.periodic_rejects += 1
        if res["accepted"]:
            self.base_results = {}
            self._remember(self.base_results, rnd["base"], rnd["cand"])
            self.win, self.margin, self.record_gen = cw, cm, gen
            self.n, self.record_theta = cn, theta
            self.have_record = True
            self.accepts += 1
            self.periodic_rejects = 0
        else:
            self.rejects += 1
        return res

    def _log_pinned(self, res, tally, gen, source):
        """The round's flips and drops, by tape id, into `real_gate.log`.

        The log is the operator's ledger of what the gate did, and on a pinned
        set "accepted, 71.4% -> 72.1%" is the least informative thing that
        could be written: the interesting fact is *which live games* moved,
        because each one is an episode that can be pulled up and read. So the
        ids go in, flipped and dropped, on their own lines.
        """
        verdict = "ACCEPT" if res.get("accepted") else "refuse"
        try:
            with open(os.path.join(self.run_dir, "real_gate.log"), "a") as fh:
                if tally is None:
                    fh.write(f"--- gen {gen} ({source}) pinned: no paired "
                             f"incumbent leg -> {verdict}\n")
                    return
                unit = "games" if self.seats == 2 else "boards"
                fh.write(
                    f"--- gen {gen} ({source}) pinned: {tally['n']} {unit}  "
                    f"wins {tally['inc_wins']} -> {tally['cand_wins']}  "
                    f"FLIPS +{tally['flips']} DROPS -{tally['drops']}  "
                    f"net {tally['flips'] - tally['drops']:+d} "
                    f"(min_flips {self.min_flips})  "
                    f"margin {tally['inc_margin']:+.0f} -> "
                    f"{tally['cand_margin']:+.0f}  -> {verdict}\n")
                fh.write("---   flipped: "
                         + (" ".join(tally["flipped"]) or "-") + "\n")
                fh.write("---   dropped: "
                         + (" ".join(tally["dropped"]) or "-") + "\n")
        except OSError:
            # The verdict is not worth losing to a full disk.
            pass

    def _confirm_fresh(self, res, iw, im):
        """The replicate round of a paired candidate: confirm, or revert.

        Both thetas have now been played on two independent bases, so the
        confirmation is the pooled comparison of the two -- like with like,
        on games neither was selected on.
        """
        self.replicates += 1
        cand = self._pooled(self.base_results)
        prev = self.prev_incumbent
        if prev is None:
            ok = True
        else:
            shared = {b: r for b, r in prev.get("base_results", {}).items()
                      if b in self.base_results}
            pw, pm, pn = self._pooled(shared)
            ok = (self.beats(cand[0], cand[1], pw, pm) if pn
                  else self.beats(cand[0], cand[1], iw, im))
        if prev is not None and self.paired_t > 0:
            # `prev is None` is the first record of a run: there is nothing to
            # be significantly better than, and the baseline is taken
            # unopposed as before. Evaluated before the `and`, not
            # short-circuited by it, so the log row carries the pooled
            # statistic whichever half of the rule refused the candidate.
            ok = self._confirm_paired(res) and ok
        self.round_games = []
        self.win, self.margin, self.n = cand[0], cand[1], cand[2]
        res["replicate_win"], res["replicate_margin"] = cand[0], cand[1]
        if ok:
            self._confirm(res)
        else:
            self._revert(res)
        return res

    def _confirm_paired(self, res):
        """The confirmation's own paired test, over every round of the pair.

        Three conditions, and flow112 needed all three. It promoted a theta
        that scored 44.4% against a paired 39.2% on one 240-board provisional
        round -- the incumbent reads 49-54% on every other base -- and then
        "confirmed" it by pooling the candidate's two bases against the
        incumbent's earlier, different ones.

        * **Both rounds, both legs.** Fewer than two rounds, or any round
          missing either theta's per-game rows, is a revert. An unpaired
          confirmation is not a weaker confirmation; it is a different and
          much noisier measurement wearing a paired one's name.
        * **The pooled t clears the threshold.** One lucky base is exactly
          what pooling two of them is for, and the t is computed over the
          union of both rounds' games rather than per round.
        * **The pooled paired win difference is positive.** Under
          `--real-gate-metric margin` the t is a margin test, and a candidate
          can clear it while losing the head-to-head bit the leaderboard
          scores. This is a floor, not a second threshold: it can only reject.
        """
        if len(self.round_games) < 2:
            # The provisional round and the replicate round. Fewer means a
            # resume lost a round's rows, or the replicate never paired.
            res["paired_t"], res["paired_rounds"] = None, len(self.round_games)
            return False
        res["paired_rounds"] = len(self.round_games)
        cg, ig = self._merge_games(self.round_games)
        stats = paired_stats(cg, ig) if cg and ig else None
        if not self._significant(stats, res):
            return False
        # `_significant` has already put the pooled numbers on `res`.
        return stats["win"] > 0

    def _settle_replicate(self, res, read, rc):
        """The provisional record's second reading: confirm it, or revert.

        A candidate takes the record on one n=48 draw against a bar that is
        pooled over n=96, so the comparison is between a noisy number and a
        quiet one and the noisy one wins too often: flow27c's 79.2% candidate
        replicated at 60.4% and left the run pooled at 69.8%, below the
        78.1% it displaced. Confirmation compares like with like -- the
        candidate's *pooled* pair against the incumbent's -- and a candidate
        that cannot clear it never becomes the record at all.
        """
        if read is None:
            # The eval failed, not the candidate. Reverting on a crashed
            # subprocess would let an infrastructure fault retire a policy,
            # so the provisional record stands on its single reading.
            self.failures += 1
            res["error"] = (f"eval exited {rc}" if rc != 0
                            else f"no readable {self.csv_path}")
            self._confirm(res)
            return
        self.replicates += 1
        self._pool(res, *read)
        prev = self.prev_incumbent
        if prev is None or self.beats(self.win, self.margin,
                                      prev.get("win"), prev.get("margin")):
            self._confirm(res)
        else:
            self._revert(res)

    def _confirm(self, res):
        """The provisional record is the record. This is where it moves."""
        res["accepted"], res["confirmed"] = True, True
        self.have_record = True
        self.accepts += 1
        self.prev_incumbent = None
        # The centre is not lost after all: whatever the run of refusals was
        # about, a confirmed record ends it.
        self.periodic_rejects = 0
        self.replicate_source = None

    def _revert(self, res):
        """Put the incumbent back: its numbers, its theta, its generation.

        `best_abs_theta` never moved (that is what "provisional" means), so
        `restore_theta` is normally the theta the trainer already holds and
        the record file does not change. It is carried anyway because the
        gate, not the trainer, is the thing that knows which theta the bar
        belongs to.
        """
        prev = self.prev_incumbent
        self.win, self.margin = prev["win"], prev["margin"]
        self.n, self.record_gen = prev["n"], prev["record_gen"]
        self.record_theta = prev.get("theta")
        self.base_results = prev.get("base_results") or {}
        self.prev_incumbent = None
        self.reverts += 1
        if self.replicate_source == "periodic":
            # Provisionally accepted and then taken back: for the centre that
            # is a refusal like any other, and the one that costs the most.
            self.periodic_rejects += 1
        self.replicate_source = None
        res["reverted"] = True
        # `None` when the bar's theta is not known (a retired in-sim record
        # took `best_abs_theta` with it). Nothing to put back then -- and
        # nothing was taken, since a provisional record never moved it.
        res["restore_theta"] = prev.get("theta")
        res["restored_gen"] = prev["record_gen"]
        res["restored_win"] = prev["win"]
        res["restored_margin"] = prev["margin"]

    def _pool(self, res, win, margin, n):
        """Fold a replicate's reading into the incumbent's numbers.

        The record itself does not move -- it is the same theta, and
        `best_abs.npy` already holds it. What moves is the *bar*: the
        incumbent's win rate and margin become the games-weighted mean over
        both evals, so the number the next candidate has to beat is an
        estimate of the theta rather than the best draw taken of it.
        """
        res.update(win=win, margin=margin, games=n)
        if self.win is None or self.n <= 0 or res["gen"] != self.record_gen:
            # The record moved out from under this replicate. It cannot
            # happen while the replicate holds the single slot, but pooling a
            # reading of one theta into another theta's numbers would be
            # worse than dropping it.
            res["replicate_win"] = res["replicate_margin"] = None
            return
        tot = self.n + n
        self.win = (self.win * self.n + win * n) / tot
        self.margin = (self.margin * self.n + margin * n) / tot
        self.n = tot
        res["replicate_win"], res["replicate_margin"] = self.win, self.margin

    def beats(self, win, margin, ref_win, ref_margin):
        """Does `(win, margin)` improve on `(ref_win, ref_margin)`?

        Split out of `accepts_result` because confirmation asks the same
        question of a different pair: the candidate's pooled numbers against
        the *previous* incumbent's, rather than against the working bar (which
        by then is the candidate's own provisional reading). Both the
        provisional verdict (`_decide_round`, `accepts_result`) and every
        confirmation (`_confirm_fresh`, `_settle_replicate`) come through
        here, so `min_gain` applies to all of them and a candidate cannot be
        let in by the leg that does not enforce it.

        `--real-gate-min-gain` raises the bar from "any excess" to "this much
        excess", in the units of `metric`. It also retires the tie-break: a
        margin cannot make up a win-rate gap the threshold says is too small,
        and an exact tie is a gap of zero. At 0 -- the default -- the rule is
        the strict one this build has always had, tie-break included.

        `--real-gate-win-floor` adds a second, *veto* condition to the margin
        metric only: the margin still decides, but a candidate whose win rate
        has dropped more than the slack below the incumbent's is refused
        however many coins it brought. It is a floor, not a threshold -- it
        can only reject, never accept -- so the baseline (`ref_win is None`,
        nothing measured yet) is still taken unopposed.
        """
        if ref_win is None:
            return True         # nothing measured yet: the first reading wins
        if self.metric == "margin":
            if self.win_floor is not None and win < ref_win - self.win_floor:
                return False    # the win rate fell further than the slack
            if self.min_gain > 0:
                return margin >= ref_margin + self.min_gain
            return margin > ref_margin
        if self.min_gain > 0:
            return win >= ref_win + self.min_gain
        return win > ref_win or (win == ref_win and margin > ref_margin)

    def _significant(self, stats, res=None):
        """Does a paired reading clear `--real-gate-paired-t`?

        `True` with the flag off, always -- the whole test is skipped and
        nothing reads the per-game rows. With it on, the candidate has to be
        `paired_t` standard errors above the incumbent on the *metric being
        selected on*, measured on the games both played.

        `stats is None` -- no shared game, because a leg failed, a resume lost
        the rows, or the evaluator wrote a CSV without a `seed` column -- is
        **refused**, not waved through. A gate asked for a significance test
        and unable to run one has not measured an improvement, and the
        alternative (falling back to the raw comparison) is the rule the flag
        exists to replace.
        """
        if self.paired_t <= 0:
            return True
        if res is not None and stats is not None:
            res["paired_n"] = stats["n"]
            # The number the t was actually computed on: half of `paired_n`
            # once both seats of every board are in, because the two mirrored
            # games are one observation. See `paired_stats`.
            res["paired_boards"] = stats.get("boards", stats["n"])
            res["paired_dwin"], res["paired_dmargin"] = (stats["win"],
                                                         stats["margin"])
            res["paired_t"] = stats["t_" + self.metric]
        if stats is None:
            if res is not None:
                res["paired_t"] = None
            return False
        return stats["t_" + self.metric] >= self.paired_t

    @staticmethod
    def _merge_games(pairs):
        """Every (candidate, incumbent) game map of a round pair, as one pair.

        The bases differ between rounds, so the seeds do and the keys cannot
        collide; pooling them is what lets the confirmation run one test over
        both bases instead of two under-powered ones.
        """
        cand, inc = {}, {}
        for c, i in pairs:
            if c is None or i is None:
                return None, None
            cand.update(c)
            inc.update(i)
        return (cand or None), (inc or None)

    def accepts_result(self, win, margin):
        """Does this real-engine reading replace the gated record?

        Ties on the win rate are broken by the margin, because 48 games
        resolve the win rate in steps of 1/96 and two records a step apart are
        routinely the same policy measured twice; the margin is continuous and
        is the tie-break the tracker's own rows are read with.

        `--real-gate-metric margin` selects on the margin alone, for a run
        whose objective is the coin gap rather than the head-to-head bit.
        """
        return self.beats(win, margin, self.win, self.margin)

    # ------------------------------------------------------------- lifecycle
    def _saved_candidate(self):
        """The waiting nomination a checkpoint carries, or `None`.

        A *periodic* one is deliberately dropped rather than saved. It is the
        search centre of a generation the resumed run has already left, the
        cadence offers a fresh centre within `--real-gate-every` generations
        anyway, and keeping it would mean persisting which kind it was -- a
        new field in `real_gate.json`, which a build without this flag would
        then have to know about. So the resume state is exactly what it was
        before the cadence existed.
        """
        waiting = self.pending or self.running
        if waiting is None or waiting[2] != "record":
            return None
        return waiting

    def _replicate_waiting(self):
        """The re-measurement the gate still owes, `(theta, gen)` or `None`.

        In flight counts as owed: a resume killed the subprocess, so what the
        acceptance bought has not been measured yet.
        """
        if self.replicate_due is not None:
            return self.replicate_due
        if self.running is not None and self.running[2] == "replicate":
            return self.running[0], self.running[1]
        return None

    def state(self):
        """The gate's resumable state, JSON-shaped."""
        waiting = self._saved_candidate()
        return {"win": self.win, "margin": self.margin, "n": int(self.n),
                "record_gen": self.record_gen,
                # A replicate owed across the resume. Its theta is the record
                # theta, saved beside this file; `record_gen` is its
                # generation, so the flag is all this needs to be.
                "replicate_due": self._replicate_waiting() is not None,
                "replicates": self.replicates, "reverts": self.reverts,
                "periodic_rejects": self.periodic_rejects,
                "replicate_source": self.replicate_source,
                # `--real-gate-fresh`: where the base sequence is up to, and
                # what the incumbent has already scored on the recent ones (a
                # cached base is a leg the next round does not have to spend).
                "base_seq": self.base_seq,
                "base_results": self.base_results,
                # The incumbent a provisional record displaced, without its
                # theta (that is `real_gate_prev.npy`). A resume that lands
                # mid-replicate has to be able to revert, or the crash itself
                # would confirm the candidate.
                "prev_incumbent": (None if self.prev_incumbent is None else
                                   {k: v for k, v
                                    in self.prev_incumbent.items()
                                    if k != "theta"}),
                "have_record": bool(self.have_record),
                # The field, as a list. A state written before the field
                # existed holds a bare string here, which `field_of` still
                # reads (a resume compares the two).
                "metric": self.metric, "min_gain": float(self.min_gain),
                # Like `min_gain`: a threshold, written so a resume can say it
                # changed, and owned by the command line rather than restored.
                "paired_t": float(self.paired_t),
                # Like `min_gain`, written so a resume can say they changed;
                # not restored, because the command line owns them. `null` is
                # the floor switched off, which is not the same as 0.0.
                "win_floor": (None if self.win_floor is None
                              else float(self.win_floor)),
                "seed_per_opponent": bool(self.seed_per_opponent),
                # `--real-gate-pinned`: part of what the bar IS (the set the
                # numbers were taken on), so a resume that changes it is
                # comparing two different measurements -- `setup_real_gate`
                # says so out loud. `min_flips` beside it is a threshold, like
                # `min_gain`, and the command line owns it.
                "pinned": self.pinned, "min_flips": int(self.min_flips),
                # How many seats of each pinned board the bar was taken on --
                # part of what the numbers ARE (a count of 2N games or of N
                # boards), so a resume that changes it says so.
                "pinned_seats": int(self.pinned_seats),
                "opponent": list(self.opponents),
                "games": self.games,
                "replicate_games": int(self.replicate_games),
                "workers": self.workers,
                "seed_base": self.seed_base, "evals": self.evals,
                "accepts": self.accepts, "rejects": self.rejects,
                "failures": self.failures,
                "pending_gen": None if waiting is None else int(waiting[1])}

    def save(self, run_dir=None):
        """Write `real_gate.json` (+ the waiting candidate) beside the run.

        A separate file rather than a `state.npz` key, so that a run without
        `--real-gate` writes the checkpoint it wrote before the flag existed.
        The in-flight candidate is saved as *pending*: a resume killed its
        subprocess, so what it holds is a nomination that was never measured
        -- unless it came from the `--real-gate-every` cadence, which is
        dropped instead (`_saved_candidate`).
        """
        d = run_dir or self.run_dir
        waiting = self._saved_candidate()
        if waiting is not None:
            _write_npy(os.path.join(d, "real_gate_pending.npy"), waiting[0])
        else:
            # Nothing is waiting, so a file here is the *decided* nomination of
            # some earlier checkpoint. `load` ignores it -- it reads the file
            # only when `pending_gen` names a generation, and the two are
            # written together -- but an operator reading the run directory
            # cannot tell a live nomination from a fossil, and on flow150 this
            # fossil was mistaken for the record having moved. Same rule, and
            # the same reason, as `real_gate_prev.npy` below.
            try:
                os.remove(os.path.join(d, "real_gate_pending.npy"))
            except OSError:
                pass
        owed = self._replicate_waiting()
        if owed is not None:
            _write_npy(os.path.join(d, "real_gate_replicate.npy"), owed[0])
        prev_theta = (None if self.prev_incumbent is None
                      else self.prev_incumbent.get("theta"))
        if prev_theta is not None:
            _write_npy(os.path.join(d, "real_gate_prev.npy"), prev_theta)
        else:
            # A stale one belongs to an older incumbent, and `load` would
            # attach it to this one.
            try:
                os.remove(os.path.join(d, "real_gate_prev.npy"))
            except OSError:
                pass
        tmp = os.path.join(d, "real_gate.json.tmp")
        with open(tmp, "w") as fh:
            json.dump(self.state(), fh, indent=1)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, os.path.join(d, "real_gate.json"))

    def load(self, run_dir, fit=None):
        """Restore from `real_gate.json`; the parsed state, or `None`.

        `fit` is the caller's layout adapter for every theta restored here --
        the pending candidate, the displaced incumbent, the owed replicate and
        the record itself (`scripts/train.py:_fit_layout`) -- so a checkpoint
        written under an older parameter layout resumes rather than nominating
        a theta this build cannot decode.

        `min_gain` is deliberately *not* restored: it is a threshold, not a
        measurement, so the value on this command line wins over the saved one
        and a segment can tighten or loosen the gate without a reset. The
        saved number is left in the returned state, which is where
        `scripts/train.py:setup_real_gate` notes a change.
        `seed_per_opponent` and `win_floor` are handled the same way -- the
        first changes which seeds the next leg draws and the second how much
        of a win-rate drop this segment will tolerate, neither of which is
        what the saved bar means.
        """
        p = os.path.join(run_dir, "real_gate.json")
        if not os.path.isfile(p):
            return None
        with open(p) as fh:
            state = json.load(fh)
        self.win, self.margin = state.get("win"), state.get("margin")
        self.record_gen = state.get("record_gen")
        self.have_record = bool(state.get("have_record"))
        for k in ("evals", "accepts", "rejects", "failures", "replicates",
                  "reverts", "periodic_rejects"):
            setattr(self, k, int(state.get(k, 0) or 0))
        # `n` predates nothing but the pooling; a state written before it has
        # numbers from exactly one eval.
        self.n = int(state.get("n") or 0)
        if self.win is not None and self.n <= 0:
            self.n = self.games * self.seats
        self.replicate_source = state.get("replicate_source")
        self.base_seq = int(state.get("base_seq") or 0)
        self.base_results = dict(state.get("base_results") or {})
        # The confirmed record's theta. Under `--real-gate` the gate is the
        # only writer of `best_abs.npy` -- it moves that file on confirmation
        # and on nothing else -- so the file beside this state *is* the theta
        # the saved bar was measured on. Without it `_incumbent_ref` has no
        # theta to hand back, `_fresh_leg` skips the incumbent's leg, and
        # every verdict after the resume compares the candidate's fresh base
        # against the incumbent's *pooled* level from other bases: an
        # unpaired reading whose noise is the seed draw. flow61 "accepted"
        # gen 50 at 58.3% against a 44.4% pooled level and flow62 refused gen
        # 40 at 42.1% against 50.3%, neither on a single shared game, where
        # every verdict before the resume had said "against X% paired".
        # Restored here rather than in `scripts/train.py` so that a loaded
        # gate is whole whoever loaded it.
        best = os.path.join(run_dir, "best_abs.npy")
        if self.have_record and os.path.isfile(best):
            arr = np.load(best).astype(np.float32)
            self.record_theta = arr if fit is None else np.asarray(fit(arr))
            self.theta_source = "best_abs.npy"
        prev = state.get("prev_incumbent")
        prev_theta = os.path.join(run_dir, "real_gate_prev.npy")
        if prev:
            # The theta is optional (`save`); the numbers are the half that
            # decides whether the provisional record survives its replicate.
            theta = None
            if os.path.isfile(prev_theta):
                arr = np.load(prev_theta).astype(np.float32)
                theta = arr if fit is None else np.asarray(fit(arr))
            self.prev_incumbent = dict(prev, theta=theta)
        rep = os.path.join(run_dir, "real_gate_replicate.npy")
        if state.get("replicate_due") and os.path.isfile(rep):
            arr = np.load(rep).astype(np.float32)
            self.replicate_due = (
                (arr if fit is None else np.asarray(fit(arr))),
                int(state.get("record_gen") or 0))
            if self.record_theta is None:
                # A resume *between* a provisional acceptance and its
                # replicate. `_decide_round` put this theta in `record_theta`
                # when it took the bar provisionally, and `best_abs.npy` is
                # emphatically not it -- the file waits for the confirmation,
                # which is why `have_record` is still False and the block
                # above found nothing. So the owed replicate's theta is the
                # record theta, exactly as memory had it: it holds the bar
                # (`win`/`margin` are its reading), the incumbent it displaced
                # is in `prev_incumbent`, and `_confirm` only flips the flag
                # -- it never assigns the theta back. Without this the gate
                # came out of the resume owning a bar with nothing to play for
                # it, and every candidate after the confirmation was decided
                # unpaired. This was flow61's and flow62's actual state.
                self.record_theta = self.replicate_due[0]
                self.theta_source = "real_gate_replicate.npy"
        gen = state.get("pending_gen")
        cand = os.path.join(run_dir, "real_gate_pending.npy")
        if gen is not None and os.path.isfile(cand):
            arr = np.load(cand).astype(np.float32)
            self.pending = ((arr if fit is None else np.asarray(fit(arr))),
                            int(gen), "record")
        return state

    def forget_incumbent(self):
        """Drop the incumbent's real numbers, keep its theta
        (`--real-gate-reset`).

        The bar is a measurement, and a measurement can go stale: the opponent
        was repackaged, `--real-gate-games` changed, or the number was simply
        a lucky draw that nothing has beaten since. Forgetting it makes the
        next reading a *baseline* again -- the record theta is re-nominated by
        `scripts/train.py:setup_real_gate` and whatever it scores now becomes
        the bar. `best_abs_theta` is untouched; what goes is the claim that
        its numbers are known.
        """
        self.win = self.margin = self.record_gen = None
        self.n = 0
        self.have_record = False
        self.pending = self.replicate_due = None
        self.prev_incumbent = self.record_theta = None
        self.theta_source = "unknown"
        self.periodic_rejects = 0
        self.base_results = {}

    @staticmethod
    def record_in(run_dir, default=True):
        """Did the gated run in `run_dir` ever accept a record? `default` when
        the directory carries no gate state at all -- a run trained without the
        flag, whose `best_abs_theta` is an in-sim record the gate will
        baseline."""
        p = os.path.join(run_dir, "real_gate.json")
        if not os.path.isfile(p):
            return default
        try:
            with open(p) as fh:
                return bool(json.load(fh).get("have_record"))
        except (OSError, ValueError):
            return default

    def close(self):
        """Kill any in-flight eval and reap its workers. Idempotent.

        The child is its own session leader, so one `killpg` takes the
        `ProcessPoolExecutor` down with it -- without this a killed trainer
        leaves `--real-gate-workers` engine processes running on a host whose
        cores the next run wants.
        """
        proc, self.proc = self.proc, None
        if proc is not None and proc.poll() is None:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except (OSError, AttributeError):
                proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except (OSError, AttributeError):
                    proc.kill()
        if self.log_fh is not None:
            try:
                self.log_fh.close()
            except OSError:
                pass
            self.log_fh = None
        if self.running is not None:
            # Never measured, so it goes back to the queue rather than being
            # lost; a resume picks it up from `real_gate_pending.npy` (or
            # `real_gate_replicate.npy`, for the re-measurement an acceptance
            # still owes).
            # A paired round in flight is abandoned whole: its legs are
            # halves of one reading, and half of one decides nothing. The
            # candidate goes back to the queue and is re-measured on the next
            # fresh base.
            self.round, self.inc_leg, self.leg = None, None, None
            theta, gen, source = self.running
            if source == "replicate":
                if self.replicate_due is None:
                    self.replicate_due = (theta, gen)
            elif self.pending is None:
                self.pending = self.running
            self.running = None


class Trainer:
    #: Class-level fallbacks for the ladder's bookkeeping: an empty ladder with
    #: no weights, no handicaps and no held-out rungs. `__init__` shadows every
    #: one of them with an instance attribute; they exist so that the parts of
    #: this class that are pure update rules stay reachable from a
    #: `Trainer.__new__` with three fields set, which is how they are tested.
    #: Nothing here is ever mutated in place -- `place_handicap` copies.
    archetype_names = ()
    archetype_coins = ()
    rung_weights = np.ones(0)
    arch_handicap = np.zeros((0, 2), np.int32)
    holdout_thetas = ()
    #: Index into `self.archetypes` of the `kagg2_flow` rung, or -1 when this
    #: run has none. It is an index rather than a flag because every batch that
    #: faces the ladder has to turn "which rung is this episode playing" into
    #: "does this episode carry the flow", and that is a lookup.
    flow_rung = -1
    #: Index into `self.archetypes` of the `kaggle_flow` rung, or -1. Separate
    #: from `flow_rung` rather than a set of them: the two carry different
    #: tables and (optionally) different randomisation ranges, and the
    #: yardstick's flow ensemble is defined on `kagg2_flow` alone.
    kaggle_rung = -1
    #: `(name, FLOW_TABLE id)` for each `--tape-rung` this run loaded, in the
    #: order the ladder appends them. A tuple rather than two ints because the
    #: count is an operator's choice, and a name rather than an index because
    #: that is what survives a `--resume` (the ladder comes from the
    #: checkpoint, the flags from this invocation).
    tapes = ()
    #: `(rung index, FLOW_TABLE id)` for the tape rungs actually on the ladder,
    #: derived from `tapes` and `archetype_names` by `_bind_rungs`. Empty on a
    #: run with no tape rung, which is what keeps every flow decision below on
    #: the exact expression it had before tape rungs existed.
    tape_slots = ()
    #: `--slot-rotation carry`'s running credit (`SlotCarry`), or `None` under
    #: `fixed`. Run state, not config: it is where in the rotation the ladder
    #: is, and `scripts/train.py` round-trips it through `state.npz` so a
    #: resume does not hand the low-numbered rungs the leftovers all over
    #: again.
    slot_carry = None
    #: {rung name: episodes} for the generation just played, `log.jsonl`'s
    #: `rung_episodes`. Empty until `generation` has run once.
    last_rung_episodes = {}
    #: `--tape-actions` the same way: (ladder index, row of the stacked table)
    #: per action rung, derived by `_bind_rungs`. Empty on a run without one.
    tape_act_slots = ()
    #: Ladder labels of the action rungs, in `--tape-actions` order.
    tape_act_names = ()
    #: Of those, the ones whose `.npz` carried a `town` key: pinned
    #: boards, the set `--pinned-once` plays once. Empty on every run
    #: whose tapes were cut without `--with-town`.
    pinned_act_names = frozenset()
    #: Ladder indices of the pinned rungs, derived by `_bind_rungs`.
    pinned_slots = ()
    #: The `kagg2_flow` levels `absolute_report` averages over, or `()` for the
    #: centre-only yardstick every run before 2026-08-27 used. A class-level
    #: default because the tests that drive the report through a `__new__` stub
    #: predate it, and "no ensemble" is what they mean.
    abs_draws = ()
    #: How many restarts have multiplied sigma (see `__init__`). A class-level
    #: default for the same reason `abs_draws` has one: the stubs that drive
    #: `_maybe_restart` through `__new__` predate it, and 0 is what a run that
    #: has not restarted holds.
    sigma_steps = 0
    #: What the last record gate's replication decided (`--best-replicate`), or
    #: `None` on a measurement that never reached it. Log-only, like
    #: `last_best_gate`, and a class default for the same reason `abs_draws`
    #: has one: the `__new__` stubs that drive the rule directly predate it.
    last_replicate = None
    #: How many candidates the replication refused. Run state, so it is
    #: checkpointed: it is the count of times this run's screening measurement
    #: was a lucky reading, which is the number that says whether the flag is
    #: earning its rollouts.
    replicate_rejects = 0
    #: Rung names this run will append *after* construction, i.e. the
    #: `--rung-theta` anchors. They exist so that `--select-metric
    #: margin:<anchor>` can be validated at construction without refusing the
    #: one ladder shape that is not final yet -- `scripts/train.py` builds the
    #: Trainer first and only then loads the anchor thetas. Nothing else reads
    #: this; the check runs again once the anchors are really in.
    pending_rungs = ()
    #: The generation's re-centre on the gated record
    #: (`--real-gate-recentre`), or `None`. Read by `scripts/train.py` for the
    #: log row, and reset every generation like `last_real_gate`.
    last_recentre = None

    #: The real-engine record gate (`--real-gate`), or `None` -- which is
    #: every run before it existed, and every `__new__` stub in the tests.
    #: `scripts/train.py` attaches it after the ladder is final.
    real_gate = None
    #: The verdict the gate returned *this* generation, for `log.jsonl`, or
    #: `None` on the generations (almost all of them) where none landed.
    last_real_gate = None

    def __init__(self, cfg: Config, seed: int = 0, pending_rungs=()):
        self.cfg = cfg
        self.pending_rungs = tuple(pending_rungs)
        self.tables = build_tables(jnp)
        hi_t, lo_t = eod.weed_threshold()
        self.hi_t, self.lo_t = jnp.int32(hi_t), jnp.int32(lo_t)
        # `--tape-actions` before the evaluator, because the tables and their
        # market-turn schedule are *closed over* by it: which hours resolve a
        # market row is read at trace time, so it has to be known before the
        # first trace. Loading here also refuses a bad path seconds into the
        # run rather than after the liveness probe, exactly as `--tape-rung`'s
        # tables are loaded below.
        acts = TPA.load_many(cfg.tape_actions)
        self.tape_act_names = tuple(TPA.rung_name(a.episode) for a in acts)
        # A tape cut with `--with-town` carries the recorded town schedule, and
        # that is what makes its rung ONE deterministic board -- the property
        # `--pinned-once` trades replays for. Read off the loaded tape rather
        # than off the filename, because the key is the fact.
        self.pinned_act_names = frozenset(
            nm for nm, a in zip(self.tape_act_names, acts) if a.town is not None)
        self.tape_act, self.tape_act_turns = None, None
        if acts:
            stacked = TPA.stack(acts)
            self.tape_act = TPA.device(jnp, stacked)
            self.tape_act_turns = tuple(sorted(
                set(rollout.MARKET_TURNS) | set(stacked.hours)))
        if not 0 <= int(cfg.d10_cash_day) < spec.N_DAYS:
            raise ValueError(
                f"d10_cash_day {cfg.d10_cash_day}: the season is days "
                f"0..{spec.N_DAYS - 1}.")
        # Always on, at every weight including the 0.0 default: the two raw
        # quantities are logged every generation so that an arm running at
        # weight 0 still shows what the shaped arm is being paid for, and a
        # baseline log is the only thing a shaped log can be read against.
        # It buys three more int32 columns per episode and no second rollout;
        # what it must not do is change the *ranking*, and that is
        # `fitness_bonus`'s `None` (see `shaped_advantage`).
        self.evaluate = make_evaluator(self.hi_t, self.lo_t,
                                       bool(cfg.tape_flow_backed),
                                       bool(cfg.tape_flow_spread),
                                       tape=self.tape_act,
                                       tape_turns=self.tape_act_turns,
                                       shop_crn=bool(cfg.shop_crn),
                                       day_metrics=True,
                                       d10_cash_day=int(cfg.d10_cash_day))
        #: Last generation's population means of the two raw shaping
        #: quantities, `(day-D coin lead, net filled tiles)`, or `None` when
        #: the evaluator is a stub that emits only `[mine, theirs]`.
        self.last_day_metrics = None
        #: The **centre** theta's mean decoded `macro.forward_days` on the
        #: fixed measurement boards, or `None` on a generation that took no
        #: absolute reading (and on a tree with no `g11`). The population's own
        #: `fwd` above is a mean over perturbed members; this is the horizon
        #: the theta that gets checkpointed actually plans with, and it comes
        #: off the measurement `absolute_report` was making anyway.
        self.last_centre_fwd = None
        self.mesh, self.n_devices = batch_mesh()
        rng = np.random.default_rng(seed)
        self.theta = jnp.asarray(PO.init_theta(rng))
        self.n = self.theta.shape[0]
        # Dead parameter columns are neither perturbed nor updated (section 2).
        # `--train-only` narrows that further: it is the same kind of mask, so
        # it is AND-ed in here and everything downstream -- the perturbation,
        # the step, the decay -- inherits it with no further change. A
        # coordinate outside the subset is left exactly as it was initialised.
        live = PO.live_mask()
        try:
            self.train_only = train_mask(cfg.train_only)
        except ValueError as exc:
            raise ValueError(f"train_only {cfg.train_only!r}: {exc}") from None
        self.mask = jnp.asarray(live * self.train_only)
        self.n_live = int((np.asarray(live) * self.train_only > 0).sum())
        if self.n_live == 0:
            raise ValueError(f"--train-only {cfg.train_only!r}: leaves no live "
                             f"coordinate -- every one it names is already "
                             f"masked dead by `PO.live_mask`.")
        if str(cfg.optimizer) not in ("adam", "sgd"):
            raise ValueError(f"optimizer {cfg.optimizer!r}: expected "
                             f"'adam' or 'sgd'.")
        # Head/aux biases: clipped after the step instead of decayed.
        self.no_decay = jnp.asarray(bias_mask())
        self.m = jnp.zeros(self.n)
        self.v = jnp.zeros(self.n)
        self.t = 0
        # Adam's bias-correction counter, deliberately *not* `self.t`. It counts
        # steps taken on the current `m`/`v`, so clearing the moments has to
        # reset it too -- see `step`.
        self.adam_t = 0
        self.sigma = float(cfg.sigma)
        self.sigma_restarts = 0
        # How many of those restarts actually *multiplied* sigma. It is the
        # same number as `sigma_restarts` at any `--stall-sigma-mult` above
        # 1.0, and 0 at 1.0 however often the jump fires -- which is the whole
        # difference, because `load_resume` rebuilds sigma as
        # `cfg.sigma * mult ** steps` under *this* invocation's multiplier. A
        # run that took five pure jumps and is then resumed with `--stall-sigma
        # -mult 2.0` must come back at its own sigma, not at 32x it.
        self.sigma_steps = 0
        self.last_improve = 0
        self.pool = [self.theta]
        self.champion = self.theta
        self.champion_score = NO_BEST
        self.history = []
        self.key = jax.random.PRNGKey(seed)
        self.rng = rng
        # Fixed seeds for the absolute measurement: the same games every time,
        # so two checkpoints' numbers are comparable. The first half selects,
        # the second half is only ever reported -- see `absolute_report`.
        abs_seeds = np.random.default_rng(FIXED_SEED).integers(0, 2 ** 31 - 1, cfg.abs_pairs)
        self.abs_words = jnp.asarray(host_words(abs_seeds))
        self.n_abs_sel = max(int(cfg.abs_pairs) // 2, 1)
        # The yardstick's shape, refused here rather than at the first
        # measurement: both of these are minutes into a multi-hour run.
        self._check_abs_select()
        self.abs_draws = tuple(flow_ensemble_draws(
            cfg.abs_flow_draws, cfg.abs_flow_scale, cfg.abs_flow_shift))
        self.best_abs = NO_BEST
        self.best_abs_theta = self.theta
        # The theta the *in-sim* record belongs to. Without `--real-gate` it is
        # `best_abs_theta` at every instant; under the flag the two come apart,
        # because the in-sim record keeps moving (it is the nomination
        # threshold) while `best_abs_theta` waits for the real engine. Kept so
        # that a gated run loses nothing: it is written as `best_sim.npy`.
        self.best_sim_theta = self.theta
        # The real-engine gate and its last verdict; `scripts/train.py` sets
        # the gate once the ladder is final. See `RealGate`.
        self.real_gate = None
        self.last_real_gate = None
        self.last_recentre = None
        # The holdout half's number for the theta `best_abs` currently holds,
        # so `--best-gate both` can ask whether a new record also generalises.
        # `-inf` rather than `-1.0`: the holdout is a mean, and under
        # `--select-metric score` or `margin:<rung>` a legitimate one can sit
        # below any finite sentinel, so the sentinel has to be the one nothing
        # can be under. `best_abs` uses the same one now, for the same reason.
        self.best_hold = NO_BEST
        # The last measurement's gate decision, for `log.jsonl`. `None` until
        # the first measurement, which is exactly when there is nothing to log.
        self.last_best_gate = None
        # The replication's two log fields (see `_replicate_record`). The
        # counter is checkpointed; the dict is this measurement's only.
        self.last_replicate = None
        self.replicate_rejects = 0
        self.abs_history = []
        # Strategy archetypes: never evicted, never snapshotted, faced every
        # generation like a rung. A single lineage never shows itself the
        # behaviours that beat it; these do. `AR.NAMES` fills the first slots,
        # the rest are sampled from the same seed as everything else.
        self.archetype_names, self.archetypes = [], []
        self.archetype_coins = []
        self.rung_weights = np.ones(0)
        self.arch_handicap = np.zeros((0, 2), np.int32)
        if cfg.slot_rotation not in SLOT_ROTATIONS:
            raise ValueError(f"slot_rotation {cfg.slot_rotation!r}: expected "
                             f"one of {', '.join(SLOT_ROTATIONS)}")
        # `None` under "fixed", so an unflagged run calls `opponent_slots`
        # with exactly the arguments it always took.
        self.slot_carry = (SlotCarry() if cfg.slot_rotation == "carry"
                           else None)
        #: {rung name: episodes} for the generation just played -- what
        #: `log.jsonl` carries as `rung_episodes`. Empty until the first one.
        self.last_rung_episodes = {}
        self.flow_rung = -1
        if cfg.tape_score not in TAPE_SCORES:
            raise ValueError(f"tape_score {cfg.tape_score!r}: expected one of "
                             f"{', '.join(TAPE_SCORES)}")
        # The tape rungs' tables go into `sim.market`'s stack *before* anything
        # is traced: from `apply_flow`'s point of view they are constants like
        # the two measured means, and the control word's table column is what
        # selects between them. Loading here rather than in `_build_archetypes`
        # also means a bad path or a mislabelled table is refused seconds into
        # the run instead of after the liveness probe.
        tapes = TPF.load_many(cfg.tape_rungs)
        # `--tape-flow-backed` clamps the flow seat's sells to its shed and
        # credits that shed with the table's `grow` row. A table cut before
        # `grow` existed has no such row, and the clamp without it does not
        # shrink the opponent, it deletes it (`sim.market.apply_flow`) -- so
        # the run is refused here, naming the file, rather than training for a
        # day against a rung that banks four figures.
        if cfg.tape_flow_backed:
            missing = [t.path for t in tapes if t.grow is None]
            if missing:
                raise ValueError(
                    "--tape-flow-backed needs every --tape-rung table to carry "
                    "a `grow` row (what the recorded seat produced); these do "
                    "not: " + ", ".join(missing) + ". Re-cut them with "
                    "scripts/make_tape_rung.py.")
        self.tapes = tuple(
            (t.name, market.register_flow_table(t.sell, t.buy, t.grow))
            for t in tapes)
        if cfg.n_archetypes > 0:
            self._build_archetypes(rng)
        # Rungs the gradient never sees and selection never reads: they are the
        # *opponent* holdout, the one this run did not have. See
        # `AR.HOLDOUT_RUNGS`.
        self.holdout_thetas = []
        if cfg.holdout_rungs and cfg.n_archetypes > 0:
            self.holdout_thetas = [
                (label, jnp.asarray(AR.archetype_theta(**AR.named(name))),
                 tuple(int(x) for x in start))
                for label, name, start in AR.HOLDOUT_RUNGS]

    def _check_abs_select(self):
        """Refuse an `--abs-select` that cannot mean what it says.

        `all` selects on every fixed seed pair, so the holdout half is no
        longer held out -- it is a *subset* of what was selected on. Under
        `--best-gate both` the gate would then be asking whether a statistic
        beat a part of itself, which is not a generalisation check but an
        arithmetic identity dressed as one. Mutually exclusive rather than
        silently a no-op: an operator who passed both asked for a guard, and a
        guard that is quietly absent is worse than one that is refused.

        `hold` swaps the two halves, so it needs a second half to swap to.
        """
        cfg = self.cfg
        if cfg.abs_select not in ("sel", "hold", "all"):
            raise ValueError(f"abs_select {cfg.abs_select!r}: expected 'sel', "
                             f"'hold' or 'all'")
        if cfg.abs_select == "all" and cfg.best_gate == "both":
            raise ValueError(
                "abs_select 'all' with best_gate 'both': `all` selects on every "
                "fixed seed pair, so the holdout half the gate reads is part of "
                "the selected set and the gate cannot ask its question. Pick "
                "one -- `--abs-select all` (a lower-variance statistic on 64 "
                "pairs) or `--best-gate both` (a held-out ratchet on 32).")
        if cfg.abs_select == "hold" and int(cfg.abs_pairs) - self.n_abs_sel < 1:
            raise ValueError(
                f"abs_select 'hold' with abs_pairs {cfg.abs_pairs}: the second "
                f"half is empty, so there is nothing to select on.")

    # ---------------------------------------------------------------- archetypes

    def _bind_rungs(self):
        """Resolve the per-rung weight and opening handicap from names + cfg.

        Both are keyed by *name*, because that is how an operator states them
        (`--rung-weight mixed_ranch=2`) and because a resumed run restores its
        archetype thetas from the checkpoint while taking its flags from this
        invocation. Names therefore round-trip through `state.npz`; the two
        arrays here are derived, so they never need to.
        """
        names = list(self.archetype_names)
        n = len(names)
        # Which ladder slot each loaded tape took. Derived here, with the
        # weights and the handicap, because it is the same kind of fact and
        # has the same failure mode: on `--resume` the ladder comes from the
        # checkpoint while `--tape-rung` comes from this invocation, so the
        # index a tape's table belongs to can only be read off the names.
        pos = {name: i for i, name in enumerate(names)}
        self.tape_slots = tuple((pos[nm], tid) for nm, tid in self.tapes
                                if nm in pos)
        # The same map for `--tape-actions`, whose "table id" is just the row
        # this tape took in the stacked device array (`tape_actions.stack`).
        self.tape_act_slots = tuple((pos[nm], i)
                                    for i, nm in enumerate(self.tape_act_names)
                                    if nm in pos)
        # Ladder order, not tape order: `--pinned-once` builds an episode block
        # from this and the block's seat rotation is keyed by position in it.
        self.pinned_slots = tuple(sorted(
            pos[nm] for nm in self.pinned_act_names if nm in pos))
        w = dict(self.cfg.rung_weight)
        unknown = [k for k in w if k not in names]
        if unknown:
            raise ValueError(
                f"--rung-weight names no such rung: {', '.join(sorted(unknown))}. "
                f"This run's ladder is {', '.join(names) or '(empty)'}.")
        self.rung_weights = np.array([float(w.get(name, 1.0)) for name in names])
        if n and (self.rung_weights < 0).any():
            raise ValueError(f"--rung-weight must be non-negative; got "
                             f"{dict(zip(names, self.rung_weights))}")
        if n and self.rung_weights.sum() <= 0:
            raise ValueError("--rung-weight zeroes every rung; the ladder would "
                             "have no archetype slots at all. Use --arch-frac 0.")
        self._check_select_rung(names)
        handicap = tuple(int(x) for x in self.cfg.proxy_handicap)
        if n and handicap != AR.NO_HANDICAP and AR.PROXY_NAME not in names:
            # A handicap with nowhere to land is the silent failure this whole
            # binding exists to prevent, and `--resume` is where it hides: the
            # archetype set comes from the checkpoint, not from
            # `--n-archetypes`, so an 8-rung run resumed with `--n-archetypes 9
            # --proxy-handicap` keeps its eight cold rungs and trains against
            # no proxy at all -- while the operator watches a log that says
            # otherwise.
            raise ValueError(
                f"--proxy-handicap {handicap[0]}:{handicap[1]} but this "
                f"ladder has no `{AR.PROXY_NAME}` rung: it is "
                f"{', '.join(names)}. On --resume the archetypes come from the "
                f"checkpoint rather than from --n-archetypes, so a run that "
                f"was started without the proxy cannot pick it up by resuming; "
                f"cold-start the ladder the handicap is meant for.")
        hcap = np.tile(np.asarray(AR.NO_HANDICAP, np.int32), (n, 1))
        for i, name in enumerate(names):
            if name == AR.PROXY_NAME:
                hcap[i] = np.asarray(handicap, np.int32)
        self.arch_handicap = hcap

    def weighted_slots(self):
        """The `weights` argument for `opponent_slots`, or None for uniform.

        `None` rather than a vector of ones on purpose: it is what keeps an
        unflagged run on the interleaved round-robin it drew before, so the
        opponent row is byte-identical and not merely equivalent.
        """
        if not len(self.rung_weights) or (self.rung_weights == 1.0).all():
            return None
        return self.rung_weights

    def _build_archetypes(self, rng):
        """Fill the archetype slots, then refuse to train against a dead one.

        The archetypes are the yardstick `absolute_eval` and champion selection
        both read, so a rung that earns nothing is not a spare tyre -- it is a
        1/n_archetypes slice of the scale, silently pulling the mean down and
        handing every candidate the same free win. The old `wheat_farmer` was
        exactly that: measured 2026-08-25 it finished on **0 coins**.

        Every archetype therefore plays `PROBE_PAIRS` seeds in both seats
        against the zero theta before training starts. Nothing under
        `AR.MIN_COINS` gets into `self.archetypes`: a *named* archetype below it
        is a bug in the table and raises immediately, while a *sampled* one is
        redrawn (the sampling ranges are deliberately wide, and about a quarter
        of the draws combine a reservation above the market with an animal herd,
        which starves for want of a sale). Persistent failure still raises.
        """
        names = AR.NAMES[:self.cfg.n_archetypes]
        knobs = [AR.named(n) for n in names]
        n_named = len(knobs)
        for _ in range(self.cfg.n_archetypes - n_named):
            knobs.append(AR.sample_archetype(rng))
        labels = list(names) + [f"sampled{i}" for i in range(len(knobs) - n_named)]
        # The flow rung is an *extra* slot, past `--n-archetypes`, and it plays
        # the `kagg2_proxy` knobs. Its planner is only there to put a
        # kagg2-shaped board and a kagg2-shaped hiring schedule in front of the
        # policy's opponent features; its market presence -- the part that sets
        # the quotes, and the part the proxy gets wrong -- comes from the
        # measured table instead. It takes no handicap: `PROXY_HANDICAP` is a
        # fitted stand-in for suppression the proxy could not produce, and this
        # rung produces the real thing.
        self.flow_rung = -1
        if self.cfg.kagg2_flow:
            knobs.append(AR.named(AR.PROXY_NAME))
            labels.append(K2F.RUNG_NAME)
            self.flow_rung = len(knobs) - 1
        # The Kaggle rung is appended *after* it, so every index and every
        # `--rung-weight` a run already has keeps its meaning when the flag is
        # turned on. Its planner is `wheat_clone` rather than `kagg2_proxy`
        # because that is what the field is (137 wheat tiles, 12-14 hands);
        # like the kagg2 rung it is only there to put a board in front of the
        # policy's opponent features, and its market presence comes from the
        # measured table.
        self.kaggle_rung = -1
        if self.cfg.kaggle_flow:
            knobs.append(AR.named(KAGGLE_PLANNER))
            labels.append(KGF.RUNG_NAME)
            self.kaggle_rung = len(knobs) - 1
        # The tape rungs come last, in the order they were named, so that
        # turning one on moves no index either. Same construction as the
        # `kaggle_flow` rung and for the same reason: the planner
        # (`TAPE_PLANNER`) is a board, the measured table is the opponent.
        for name, _table in self.tapes:
            knobs.append(AR.named(TAPE_PLANNER))
            labels.append(name)
        # The action rungs come after those, so that turning one on moves no
        # index either. Their `TAPE_PLANNER` theta is never played: seat 1's
        # whole day is the recording. It is here because the ladder is a list
        # of thetas and every slot needs one -- and because it is what the
        # liveness probe seats when the tape is in the *candidate* chair.
        for name in self.tape_act_names:
            knobs.append(AR.named(TAPE_PLANNER))
            labels.append(name)
        # Bound before the probe, not after: the probe has to play the proxy
        # **with its handicap applied**, or it measures a different game from
        # the one the run then trains on -- and the handicap is what makes that
        # rung clear `MIN_COINS` by a different margin than its cold twin.
        self.archetype_names = labels
        self._bind_rungs()

        for attempt in range(PROBE_TRIES + 1):
            thetas = [jnp.asarray(AR.archetype_theta(**k)) for k in knobs]
            coins = self._probe_archetypes(thetas, self.arch_handicap)
            bad = [i for i, c in enumerate(coins)
                   if c < self._liveness_floor(i)]
            if not bad:
                break
            # The flow rung is not a draw, so a failure there is a broken table
            # rather than an unlucky sample: raise with the named rungs instead
            # of resampling it into some other archetype.
            fixed = {self.flow_rung, self.kaggle_rung}
            fixed.update(i for i, _t in self.tape_slots)
            named_bad = [i for i in bad if i < n_named or i in fixed]
            if named_bad or attempt == PROBE_TRIES:
                detail = ", ".join(f"{labels[i]}={coins[i]:,.0f}" for i in bad)
                raise ValueError(
                    f"archetype liveness probe failed after {attempt + 1} "
                    f"attempt(s): {detail} coins against the zero theta, floor "
                    f"{AR.MIN_COINS:,.0f}. The archetypes are the absolute "
                    f"yardstick; a dead rung silently rescales it.")
            for i in bad:
                knobs[i] = AR.sample_archetype(rng)
        self.archetypes = thetas
        self.archetype_names = labels
        self.archetype_coins = coins

    def reprobe_archetypes(self):
        """Re-run the liveness probe on whatever archetypes are held right now.

        `--resume` swaps the archetype set for the checkpoint's *after*
        `__init__` has probed the freshly built one, so without this the numbers
        on record describe a set the run is not going to use. Worse, a
        checkpoint written before 2026-08-25 carries the dead `wheat_farmer`,
        and resuming it would put a 0-coin rung back into the yardstick
        silently -- exactly what the probe exists to prevent.

        It now also catches a rung the *planner* killed rather than the table:
        the land valuation (2026-08-26) put the old `rusher` on 9,092 coins,
        so every checkpoint written before the recalibration holds a sub-floor
        rung and is refused here. That is the intended
        answer -- the archetype thetas are frozen in the checkpoint while the
        planner they are measured through is not, so a resumed yardstick is
        only as valid as its last measurement.

        Nothing is redrawn here: a restored set is not a sample, so a failure is
        reported rather than replaced. The one thing that *is* added is the
        `kagg2_flow` rung -- see `_extend_with_flow_rung`.
        """
        if len(self.archetype_names) != len(self.archetypes):
            self.archetype_names = [f"rung{i}" for i in range(len(self.archetypes))]
        if self.cfg.kagg2_flow and K2F.RUNG_NAME not in self.archetype_names:
            self._extend_with_flow_rung()
        if self.cfg.kaggle_flow and KGF.RUNG_NAME not in self.archetype_names:
            self._extend_with_kaggle_rung()
        for name, _table in self.tapes:
            if name not in self.archetype_names:
                self._extend_with_tape_rung(name)
        for name in self.tape_act_names:
            if name not in self.archetype_names:
                self._extend_with_tape_rung(name)
        if not self.archetypes:
            self.archetype_coins, self.archetype_names = [], []
            self.flow_rung = self.kaggle_rung = -1
            self._bind_rungs()
            return []
        # The flags of *this* invocation, against the names of the checkpoint's
        # ladder -- the same rule `--sigma` follows on resume.
        self._bind_rungs()
        names = list(self.archetype_names)
        self.flow_rung = names.index(K2F.RUNG_NAME) if K2F.RUNG_NAME in names else -1
        self.kaggle_rung = (names.index(KGF.RUNG_NAME)
                            if KGF.RUNG_NAME in names else -1)
        coins = self._probe_archetypes(self.archetypes, self.arch_handicap)
        bad = [i for i, c in enumerate(coins) if c < self._liveness_floor(i)]
        if bad:
            detail = ", ".join(f"{self.archetype_names[i]}={coins[i]:,.0f}" for i in bad)
            raise ValueError(
                f"restored archetypes fail the liveness probe: {detail} coins "
                f"against the zero theta, floor {AR.MIN_COINS:,.0f}. Checkpoints "
                f"written before 2026-08-25 carry the dead `wheat_farmer`, and "
                f"ones written before 2026-08-26 carry a `rusher` the land "
                f"valuation put on 9,092; cold-start rather than resume the "
                f"yardstick they were measured on.")
        self.archetype_coins = coins
        return coins

    def _extend_with_flow_rung(self):
        """Grow a restored ladder by the `kagg2_flow` rung. -> None.

        `--kagg2-flow --resume` into a checkpoint written before the rung
        existed is the normal way this run starts: every long run on this
        machine predates the flow, and discarding a 12-rung pool and a few
        thousand generations of theta to pick up one rung would be an absurd
        price. So the flag *extends* the ladder rather than being refused by
        it.

        What this touches is only the ladder. Theta, sigma and its restart
        count, the Adam moments, the generation counter, the PRNG key, the host
        RNG, the cumulative elapsed, `best_abs` and the opponent pool are all
        restored by `scripts/train.py:load_resume` and none of them is indexed
        by rung, so a resumed run continues from exactly where it stopped with
        one more opponent in the mixture.

        Everything that *is* indexed by rung is rebuilt from the names, the
        same way a cold start builds it and in the same call order: the
        `_bind_rungs` that follows derives this rung's weight (1.0 unless
        `--rung-weight kagg2_flow=N` says otherwise) and its opening (no
        handicap -- `PROXY_HANDICAP` stands in for suppression the proxy could
        not produce, and this rung produces the real thing), and the liveness
        probe that follows measures its coins into `archetype_coins`, which is
        the denominator `collapse_floor` reads. A rung appended here is
        therefore indistinguishable from the same rung on a cold ladder.

        The theta is `kagg2_proxy`'s, as on a cold start: the planner is only
        there to put a kagg2-shaped board in front of the policy's opponent
        features, and the market presence -- the part that matters -- is the
        measured table.
        """
        self.archetypes = list(self.archetypes) + [
            jnp.asarray(AR.archetype_theta(**AR.named(AR.PROXY_NAME)))]
        self.archetype_names = list(self.archetype_names) + [K2F.RUNG_NAME]
        # Stale by exactly one entry now; the probe below refills the lot.
        self.archetype_coins = []

    def _extend_with_kaggle_rung(self):
        """Grow a restored ladder by the `kaggle_flow` rung. -> None.

        `_extend_with_flow_rung`'s argument, one table over: every checkpoint
        on this machine predates this rung, and the alternative to extending is
        throwing away the run to pick up one opponent. It is appended last, so
        a ladder that already carries `kagg2_flow` keeps that rung's index.

        The theta is `wheat_clone`'s -- the field's own shape -- and, like the
        kagg2 rung, it takes no handicap.
        """
        self.archetypes = list(self.archetypes) + [
            jnp.asarray(AR.archetype_theta(**AR.named(KAGGLE_PLANNER)))]
        self.archetype_names = list(self.archetype_names) + [KGF.RUNG_NAME]
        self.archetype_coins = []

    def _extend_with_tape_rung(self, name):
        """Grow a restored ladder by one `--tape-rung`. -> None.

        The two arguments above, once more: every checkpoint on this machine
        predates the tape rungs, and the alternative to extending is throwing
        away the run to pick up one opponent. Appended in `--tape-rung` order
        after whatever the ladder already carries, so no existing rung index
        moves and `--rung-weight` keeps every meaning it had.

        The theta is `TAPE_PLANNER`'s and the rung takes no handicap, exactly
        as the two measured-mean flow rungs do; `_bind_rungs` then maps the
        name back to the slot its table belongs to.
        """
        self.archetypes = list(self.archetypes) + [
            jnp.asarray(AR.archetype_theta(**AR.named(TAPE_PLANNER)))]
        self.archetype_names = list(self.archetype_names) + [str(name)]
        self.archetype_coins = []

    def _liveness_floor(self, i):
        """`AR.MIN_COINS` for rung `i`, or 0 where the floor does not apply.

        The floor asks "can this rung earn at all". Under
        `--tape-flow-backed` a flow rung's coins are no longer that question:
        the seat's market presence is an exogenous table clamped to a
        `TAPE_PLANNER` shed that cannot hold most of what the recorded seat
        sold, so it banks a few thousand coins whatever its board does -- the
        very phantom revenue the switch exists to remove. Measured on flow57's
        ladder, `--tape-flow-backed` puts `tape_103254816` on 7,011 and
        `tape_103210032` on 3,949 against a floor of 10,000, and the run would
        refuse to start. The floor is therefore lifted for the flow rungs, and
        only for them, and only with the switch on; every other rung, and every
        run without the switch, is gated exactly as before.
        """
        if not self.cfg.tape_flow_backed:
            return AR.MIN_COINS
        flow_rungs = {self.flow_rung, self.kaggle_rung}
        flow_rungs.update(idx for idx, _t in self.tape_slots)
        return 0.0 if i in flow_rungs else AR.MIN_COINS

    def _probe_archetypes(self, thetas, handicaps=None):
        """Mean own coins for each theta vs the zero theta, both seats, [k].

        `handicaps` is `(nquad, money)` per theta. Note the seat: here the
        *archetype* is the candidate argument (`theta_c`), so it sits at
        physical player `seat`, not `1 - seat` as it does everywhere the
        archetype is the opponent. Getting that backwards would probe the zero
        theta's opening instead of the rung's -- and, since 2026-08-27, would
        point the kagg2 flow at the wrong farm.

        The flow rungs are probed at the **centre** of their randomisation
        (scale 1.0, no day shift), like every other fixed measurement in this
        class, each off its own measured table.
        """
        k = len(thetas)
        n_probe = min(PROBE_PAIRS, int(self.abs_words.shape[0]))
        words = self.abs_words[:n_probe]
        per = n_probe * 2
        total = k * per
        ix = np.arange(total)
        who = ix // per
        seat = (ix % 2).astype(np.int32)
        widx = (ix % per) // 2
        nq, mo = cold_starts(total)
        if handicaps is not None and k:
            nq, mo = place_handicap(nq, mo, seat.astype(np.int64),
                                    np.asarray(handicaps, np.int32)[who])
        zero = jnp.zeros((total, self.n), jnp.float32)
        is_flow, table = self.flow_rung_tables(who)
        # Note the seat again: here the *archetype* is the candidate, so an
        # action rung's tape plays `seat` and not `1 - seat`. The probe then
        # measures the recording itself, which is the honest liveness number
        # for a rung whose opponent is the recording.
        is_ta, ta_table = self.tape_act_tables(who)
        money = np.asarray(self._eval(
            self.tables, jnp.stack([thetas[i] for i in who]), zero,
            words[jnp.asarray(widx)], jnp.asarray(seat),
            jnp.asarray(nq), jnp.asarray(mo),
            flow=self.flow_words(is_flow, seat, table=table),
            tape_ctl=self.tape_act_words(is_ta, seat, ta_table)))
        return [float(x) for x in money[:, 0].reshape(k, per).mean(axis=1)]

    def _eval(self, *args, flow=None, tape_ctl=None):
        """`self.evaluate(*args)`, with the flow and action words appended only
        if there are any. A run with neither rung therefore calls the evaluator
        with exactly the arguments it always took -- which matters because half
        the tests in this repo replace `tr.evaluate` with a stub of that arity.
        The action word goes last and `flow` keeps its slot even when it is
        `None`, so the two are independent."""
        if tape_ctl is not None:
            return self.evaluate(*args, flow, tape_ctl)
        return self.evaluate(*args) if flow is None else self.evaluate(*args, flow)

    def flow_words(self, is_flow, seat, scale_milli=1000, shift=0, table=None):
        """`flow_control` for a batch, or None when this run has no flow rung.

        `None` is what selects `make_evaluator`'s flow-free program, so a run
        without `--kagg2-flow` and without `--kaggle-flow` never compiles the
        flow path at all. A run *with* one passes an array from every call site,
        including the ones no flow episode is in, so the whole run stays on one
        compiled program.

        `scale_milli`, `shift` and `table` broadcast (see `flow_control`): a
        scalar is one level for the whole batch, and a per-episode array is what
        `absolute_report` passes once its ensemble puts two levels of the same
        rung in one call.

        A run with neither the `kaggle_flow` rung nor a `--tape-rung` emits the
        **3-column** word, with no table column at all, whatever `table` says.
        That is the byte-identity promise: such a run compiles and runs exactly
        the `apply_flow` it did before the second table was written.
        """
        if self.flow_rung < 0 and self.kaggle_rung < 0 and not self.tape_slots:
            return None
        seat = np.asarray(seat, np.int32)
        if self.kaggle_rung < 0 and not self.tape_slots:
            table = None
        elif table is None:
            table = market.FLOW_T_KAGG2
        return jnp.asarray(flow_control(
            np.where(np.asarray(is_flow, bool), seat, np.int32(-1)),
            scale_milli, shift, table))

    def flow_rung_tables(self, rung_idx):
        """Which episodes carry a flow, and off which table. -> (bool[], int32[])

        `rung_idx` is a rung index per episode (negative for a pool opponent,
        which is why the `< 0` guards are here rather than a bare `==`: a run
        without the rung holds -1, and -1 is also a pool row).

        A `--tape-rung` is one more (index, table id) pair on the same
        arithmetic; the loop runs zero times on a run without one, so the array
        such a run builds is the one it built before tape rungs existed.
        """
        r = np.asarray(rung_idx)
        z = np.zeros(r.shape, bool)
        is_k2 = (r == self.flow_rung) if self.flow_rung >= 0 else z
        is_kg = (r == self.kaggle_rung) if self.kaggle_rung >= 0 else z
        table = np.where(is_kg, market.FLOW_T_KAGGLE,
                         market.FLOW_T_KAGG2).astype(np.int32)
        is_flow = is_k2 | is_kg
        for idx, tid in self.tape_slots:
            hit = r == idx
            is_flow = is_flow | hit
            table = np.where(hit, np.int32(tid), table).astype(np.int32)
        return is_flow, table

    def tape_act_tables(self, rung_idx):
        """`flow_rung_tables` for `--tape-actions`. -> (bool[], int32[])

        Same arithmetic and the same `< 0` care: the loop runs zero times on a
        run without an action rung, so such a run builds the all-false mask
        that keeps `tape_act_words` returning `None`.
        """
        r = np.asarray(rung_idx)
        on = np.zeros(r.shape, bool)
        table = np.zeros(r.shape, np.int32)
        for idx, row in self.tape_act_slots:
            hit = r == idx
            on = on | hit
            table = np.where(hit, np.int32(row), table).astype(np.int32)
        return on, table

    def tape_act_words(self, is_tape, seat, table=None):
        """`rollout`'s `[seat, table]` word per episode, or None. -> int32 [E, 2]

        `seat` is the **physical** player the recording drives, exactly as
        `flow_words`' is: at every call site where the rung is the opponent
        that is `1 - seat`, and in the liveness probe -- where the rung is the
        candidate -- it is `seat`. A non-tape episode gets seat -1, which
        `rollout.run_day` reads as "this episode plays no tape", so a run with
        an action rung stays on **one** compiled program for every call site
        rather than paying a second trace for the batches no action episode is
        in.
        """
        if not self.tape_act_slots:
            return None
        on = np.asarray(is_tape, bool)
        t = np.zeros(on.shape, np.int32) if table is None else np.asarray(table, np.int32)
        return jnp.asarray(np.stack(
            [np.where(on, np.asarray(seat, np.int32), -1), t], axis=-1).astype(np.int32))

    # ---------------------------------------------------------------- episodes

    def draw_starts(self, n_pairs):
        """Opening state per episode pair: (nquad, money), int32 [n_pairs, 2].

        A `warm_frac` share of pairs open **warm** -- 2-4 quadrants already
        owned and cash uniform in [STARTING_MONEY, warm_money_max] -- the rest
        on the engine's day 0. Along its own trajectory the policy reaches a
        second quadrant on 0/30 days (`land1`, gen 6,627), so without this no
        training episode ever exercises multi-quadrant play and that whole
        region of behaviour gets no gradient. Both seats share one start, so
        the margin stays a fair comparison and the opponent is made to play
        the same off-distribution state rather than handed an edge.
        """
        cfg = self.cfg
        nquad, money = cold_starts(n_pairs)
        warm = self.rng.random(n_pairs) < cfg.warm_frac
        wq = self.rng.integers(2, 5, n_pairs).astype(np.int32)
        wm = self.rng.integers(spec.STARTING_MONEY, cfg.warm_money_max + 1,
                               n_pairs).astype(np.int32)
        nquad[warm] = wq[warm, None]
        money[warm] = wm[warm, None]
        return nquad, money

    def episode_starts(self, n_pairs, idx):
        """`draw_starts` at **episode** resolution, plus each rung's handicap.

        -> (nquad, money), int32 [2 * n_pairs, 2], indexed by episode.

        Two seats of a pair share the pair's drawn start (that is what keeps a
        warm start a fair comparison), and then the opponent's seat alone is
        raised to that rung's opening. Only `kagg2_proxy` has one, so at the
        default `--proxy-handicap` this returns `draw_starts` repeated and
        nothing else.

        Episode resolution is not an optimisation, it is the correctness
        condition -- `place_handicap`'s docstring has the trap. `idx` is
        `opponent_slots`' output, so a pair facing the self-play pool or theta
        gets no handicap at all: the handicap belongs to the rung, not to the
        seat.
        """
        nquad, money = self.draw_starts(n_pairs)
        nquad = np.repeat(nquad, 2, axis=0)
        money = np.repeat(money, 2, axis=0)
        # An action rung opens **cold**, whatever `--warm-frac` says. The
        # tape is 719 recorded frames of a game that started on the engine's
        # day 0; handing that seat two extra quadrants and up to 40,000 coins
        # does not make it play a warm game, it makes it a richer opponent
        # running a poor opponent's orders -- and our seat, which does adapt,
        # collects the difference. This is drawn *after* `draw_starts` rather
        # than instead of it so that `self.rng` sees the identical stream: a
        # run whose action rungs are absent (`tape_act_slots` empty) takes the
        # byte-identical path it always took.
        if self.tape_act_slots and not self.cfg.tape_act_warm:
            on, _ = self.tape_act_tables(np.asarray(idx) - len(self.pool))
            on = np.repeat(on, 2)[:, None]
            nquad = np.where(on, np.int32(1), nquad).astype(np.int32)
            money = np.where(on, np.int32(spec.STARTING_MONEY), money).astype(np.int32)
        if not len(self.arch_handicap):
            return nquad, money
        # With no rung handicapped this still runs, and it is still the
        # identity: `place_handicap` takes a `maximum` against `NO_HANDICAP`,
        # which is the engine's day 0 and therefore a floor no draw can fall
        # below. Keeping one path rather than two costs, measured at
        # `n_pairs=32` over 2,000 repetitions, **68 microseconds a generation**
        # on top of `draw_starts`' 36 -- against a generation of seconds. The
        # device program is untouched either way: same shapes, same batch, and
        # a rollout whose trip counts are all fixed, so only the *values* in
        # the start arrays differ. Measured: toggling the handicap between
        # generations leaves `evaluate._cache_size()` at 2, and 20 interleaved
        # generations each way land on a median ratio of 1.013 and a minimum
        # ratio of 0.980 -- the two arms straddle each other.
        e = np.arange(2 * n_pairs)
        seat = e % 2
        rung = np.asarray(idx)[e // 2] - len(self.pool)
        faces = (rung >= 0) & (rung < len(self.arch_handicap))
        if not faces.any():
            return nquad, money
        hcap = np.tile(np.asarray(AR.NO_HANDICAP, np.int32), (2 * n_pairs, 1))
        hcap[faces] = self.arch_handicap[rung[faces]]
        # `1 - seat` is the physical player the *opponent* occupies; see
        # `make_evaluator.one`.
        return place_handicap(nquad, money, 1 - seat, hcap)

    def episode_flow(self, n_pairs, idx):
        """This generation's measured flow, per episode. -> int32 [2*n_pairs, C].

        `C` is 3 without the `kaggle_flow` rung and 4 with it (the extra column
        is which table). `None` when the run has no flow rung at all, which is
        what keeps such a run on `make_evaluator`'s flow-free program *and* off
        this method's RNG draws: nothing here touches `self.rng` unless a rung
        exists, so an unflagged run's episode seeds and warm starts are the
        byte-identical stream they were before the rung was written.

        The scale and the day shift are drawn once per **pair** and shared by
        its two seats, exactly as `draw_starts` shares a pair's opening. A pair
        is one paired comparison; giving its two games different opponents would
        put the variance the pairing exists to cancel straight back into the
        margin. `1 - seat` is the physical player the opponent occupies.

        The day shift is drawn from `--kagg2-flow-shift` when that is set and
        from `+- --kagg2-flow-jitter` when it is not. A jitter is symmetric
        about the table's own calendar, which asserts that the real matchup
        sits at shift 0; the calibration sweep says it sits near **+2 days**
        (and scale ~1.3), so a jitter cannot put the *gradient* where the
        opponent actually is -- it can only widen the band around a centre
        that is wrong. The range is inclusive on both ends and is drawn with
        the same one `integers(lo, hi + 1, n_pairs)` call the jitter path
        makes, so an unset range is that path down to the RNG stream: same
        bounds, same number of draws, same generator state after.

        The `kaggle_flow` rung draws its own scale and shift, from
        `--kaggle-flow-scale` / `--kaggle-flow-shift` when those are set and
        from the kagg2 rung's ranges when they are not, and they are drawn
        **after** the kagg2 pair so that a run without the second rung sees the
        RNG stream it always saw. An episode plays one rung, so the two draws
        are selected between rather than combined.

        The `--tape-rung` rungs draw last, for the third time and for the same
        reason, and share **one** draw between them: a pair plays one rung, so
        a draw per tape would be a draw per rung the pair is not playing --
        more RNG for the same episodes, and a stream that moves when a tape is
        added rather than only when one is *used*. Randomising these at all
        matters more than it does for the two means: a tape table is n=1, the
        most overfittable rung in the ladder.
        """
        if self.flow_rung < 0 and self.kaggle_rung < 0 and not self.tape_slots:
            return None
        e = np.arange(2 * n_pairs)
        seat = e % 2
        pair_rung = np.asarray(idx) - len(self.pool)
        rung = pair_rung[e // 2]
        lo, hi = self.cfg.kagg2_flow_scale
        span = self.cfg.kagg2_flow_shift
        if span is None:
            j = int(self.cfg.kagg2_flow_jitter)
            span = (-j, j)
        slo, shi = (int(x) for x in span)
        scale = np.rint(self.rng.uniform(lo, hi, n_pairs) * 1000).astype(np.int32)
        shift = self.rng.integers(slo, shi + 1, n_pairs).astype(np.int32)
        if self.kaggle_rung >= 0:
            klo, khi = self.cfg.kaggle_flow_scale or (lo, hi)
            kspan = self.cfg.kaggle_flow_shift or (slo, shi)
            kslo, kshi = (int(x) for x in kspan)
            k_scale = np.rint(
                self.rng.uniform(klo, khi, n_pairs) * 1000).astype(np.int32)
            k_shift = self.rng.integers(kslo, kshi + 1, n_pairs).astype(np.int32)
            is_kg = pair_rung == self.kaggle_rung
            scale = np.where(is_kg, k_scale, scale)
            shift = np.where(is_kg, k_shift, shift)
        if self.tape_slots:
            tlo, thi = self.cfg.tape_flow_scale or (lo, hi)
            tspan = self.cfg.tape_flow_shift or (slo, shi)
            tslo, tshi = (int(x) for x in tspan)
            t_scale = np.rint(
                self.rng.uniform(tlo, thi, n_pairs) * 1000).astype(np.int32)
            t_shift = self.rng.integers(tslo, tshi + 1, n_pairs).astype(np.int32)
            is_tape = np.isin(pair_rung, [i for i, _t in self.tape_slots])
            scale = np.where(is_tape, t_scale, scale)
            shift = np.where(is_tape, t_shift, shift)
        is_flow, table = self.flow_rung_tables(rung)
        wide = self.kaggle_rung >= 0 or bool(self.tape_slots)
        return jnp.asarray(flow_control(
            np.where(is_flow, 1 - seat, -1),
            np.repeat(scale, 2), np.repeat(shift, 2),
            table if wide else None))

    def episode_tape_ctl(self, n_pairs, idx):
        """`episode_flow` for `--tape-actions`. -> int32 [2*n_pairs, 2] or None

        The same decomposition (`idx` per pair, an episode is `(pair, seat)`)
        and the same seat rule: the recording drives `1 - seat`, the opponent's
        physical player, so a pair's two games put it on opposite sides of the
        board and our theta plays both seats against it.

        Nothing here touches `self.rng`. An action tape has no scale and no day
        shift to draw -- it is played verbatim, which is the whole point -- so
        adding the flag moves neither the episode seeds nor the warm starts of
        a run that also has flow rungs.
        """
        if not self.tape_act_slots:
            return None
        e = np.arange(2 * n_pairs)
        seat = e % 2
        pair_rung = np.asarray(idx) - len(self.pool)
        on, table = self.tape_act_tables(pair_rung[e // 2])
        return self.tape_act_words(on, 1 - seat, table)

    def tape_episodes(self, n_pairs, idx):
        """Which episodes are played against a tape rung, or `None`. -> [2p]

        `None` unless `--tape-score ours` has tape rungs to apply it to, so an
        unflagged run hands `shaped_advantage` the argument it defaults to and
        computes the fitness it always computed.

        The decomposition is `episode_flow`'s: `idx` is per episode *pair*, an
        episode is `(pair, seat)`, and a pair's two seats face one opponent.
        """
        if self.cfg.tape_score != "ours" or not self.tape_slots:
            return None
        pair_rung = np.asarray(idx) - len(self.pool)
        rung = pair_rung[np.arange(2 * n_pairs) // 2]
        return jnp.asarray(np.isin(rung, [i for i, _t in self.tape_slots]))

    def candidates(self):
        """Every opponent faced this generation, in `opponent_slots` order."""
        return self.pool + self.archetypes + [self.theta]

    def pinned_block(self):
        """The rungs `--pinned-once` plays once this generation, or `None`.

        `None`, not an empty tuple, so that "no pinned block" is one test at
        every call site and a run without the flag (or without a `--with-town`
        tape) takes the pair-only path it always took.

        Every pinned rung is in the block, including one at `--rung-weight 0`:
        the flag's promise is one episode per pinned board, and the weight is
        applied in the aggregation (`pinned_weights`), where a zero still means
        "not in the objective". The alternative -- dropping weight-0 rungs to
        save an episode -- would make the block's size depend on the weights,
        which is exactly the coupling the flag removes.
        """
        if not self.cfg.pinned_once:
            return None
        pin = tuple(self.pinned_slots)
        return pin or None

    def pinned_keep(self, pin, n_pairs):
        """Which episodes of the `len(pin) + n_pairs` pair layout are played.

        -> int[len(pin) + 2 * n_pairs]

        The pinned block leads and contributes **one** episode per rung; the
        residual pairs contribute both of theirs.
        """
        n = len(pin)
        return np.concatenate([
            2 * np.arange(n) + self.pinned_seats(n),
            2 * n + np.arange(2 * n_pairs)]).astype(np.int64)

    def pinned_seats(self, n):
        """Which seat each pinned rung is played from this generation. -> [n]

        `(t + i) % 2`: the seat **alternates per generation**, staggered by the
        rung's position in the block.

        Fixing seat 0 was the alternative and is wrong here. A pinned board is
        one fixed board, so a fixed seat would make it one fixed *half* of that
        board forever -- our theta always the same physical player, always
        against the same recorded orders from the same side. Whatever seat
        asymmetry that board has (tile layout, who resolves a market row first,
        which side the recording's denial lands on) would then be a permanent
        component of the gradient rather than something the mirror cancels.
        The pair mirroring is what used to cancel it; playing once gives that
        up *within* a generation, so it is recovered *across* generations
        instead -- every pinned board is seen from both sides on consecutive
        steps, at no extra episode.

        The `+ i` stagger is why the alternation is not a bulk oscillation:
        without it every pinned board would swap seats together and each
        generation's whole pinned block would carry one seat's bias. With it
        half the block sits on each seat in every generation, so the bias is
        averaged inside the generation as well as across them.

        `self.t` is the count of *completed* generations at the moment
        `generation` builds its batch (it is incremented after the rollout), so
        gen 0 puts the even-indexed rungs on seat 0 and gen 1 swaps them. It is
        read off the instance rather than passed in so that a `--resume` picks
        the rotation up where the checkpoint left it instead of restarting the
        phase.
        """
        return (int(getattr(self, "t", 0)) + np.arange(int(n))) % 2

    def pinned_weights(self, pin, n_episodes):
        """Per-episode weight for `shaped_advantage`. -> float32[n_episodes]

        `EPISODES_PER_PAIR * --rung-weight` on the pinned block, 1.0 on every
        other episode. A weight-2 pinned rung used to take about two pairs, so
        four episodes of one deterministic board contributed `4x` to a mean
        over `E`; at weight 4 in a weighted mean one episode contributes the
        same `4x`. The weight scales the board's contribution, which is what it
        was always meant to do -- the replay count was only ever the mechanism.
        """
        w = np.ones(int(n_episodes), np.float32)
        rw = np.asarray(self.rung_weights, float)
        w[:len(pin)] = EPISODES_PER_PAIR * rw[list(pin)]
        return w

    def pinned_seeds(self, seeds, idx):
        """Put every PINNED slot on its tape's fixed word. -> int64[n_slots]

        `--pinned-fixed-seed`. `seeds` is the generation's drawn list and `idx`
        is its opponent per slot, both in slot order; a slot is pinned when its
        opponent is a ladder rung (`idx >= len(self.pool)`) whose position is in
        `self.pinned_slots`. Everything else -- a drawn tape, an archetype,
        self-play out of the pool -- keeps the drawn word, which is what keeps
        the flag's promise narrow: only the boards that are already fixed in
        their shops become fixed in their weeds too.

        The override is applied to the *drawn* array rather than replacing the
        draw, so `self.rng` has advanced exactly as far as it would have and
        every later consumer of it (warm starts, market jitter, the next
        generation's opponents) is untouched. Off, it hands back the drawn
        array unchanged, so the words are the ones the run always built.
        """
        seeds = np.array(seeds, np.int64, copy=True)
        if not self.cfg.pinned_fixed_seed or not self.pinned_slots:
            return seeds
        pin = set(self.pinned_slots)
        names = self.archetype_names
        base = len(self.pool)
        for s, o in enumerate(np.asarray(idx, np.int64)):
            r = int(o) - base
            if 0 <= r < len(names) and r in pin:
                seeds[s] = pinned_seed_word(names[r])
        return seeds

    def opponent_index(self, n_pairs, drop=()):
        """This generation's opponent per episode pair. -> int[n_pairs]

        Drawn **once** per generation and played by every candidate in the
        population, which is what keeps the common random numbers intact:
        `--slot-rotation carry` moves the leftover slots between generations,
        never between candidates within one.

        `drop` is a set of rung indices to give no pairs at all -- what
        `--pinned-once` passes for the pinned rungs, which are served by their
        own one-episode block instead. It is applied as a zero weight rather
        than as a post-hoc filter so that the *whole* residual budget is
        divided among the rungs that are left (a zero weight takes no slot,
        `SlotCarry.take`'s docstring says why), and so the carry credit of a
        pinned rung stays at zero instead of accruing a debt it can never
        spend. `drop=()` -- every run before the flag -- takes the byte-
        identical path below.
        """
        cfg = self.cfg
        n_pool, n_arch = len(self.pool), len(self.archetypes)
        w = self.weighted_slots()
        if drop:
            wv = np.ones(n_arch) if w is None else np.asarray(w, float).copy()
            wv[list(drop)] = 0.0
            if wv.sum() <= 0:
                # Every rung on the ladder is pinned. The residual budget then
                # has no archetype to spend itself on, so it is self-play --
                # said here rather than left to `largest_remainder`'s
                # "all-zero weights" refusal, which would be a crash.
                return opponent_slots(n_pairs, n_pool, n_arch, 0.0, None)
            w = wv
        if self.slot_carry is None:
            return opponent_slots(n_pairs, n_pool, n_arch, cfg.arch_frac, w)
        # `weighted_slots` says `None` for an all-ones ladder, which under the
        # fixed rule is the interleaved round-robin. The rotating rule needs
        # the vector: a uniform 127-rung ladder is exactly the case the fixed
        # rule truncates.
        wv = np.ones(n_arch) if w is None else np.asarray(w, float)
        k = arch_pairs(n_pairs, n_arch, cfg.arch_frac)
        take = self.slot_carry.take(k, wv) if k > 0 else np.zeros(n_arch, np.int64)
        return opponent_slots(n_pairs, n_pool, n_arch, cfg.arch_frac, w,
                              take=take)

    def rung_episodes(self, n_pairs, idx, keep=None):
        """{rung name: episodes} for this generation's index row. -> dict

        Episodes, not pairs: a pair is played from both seats, so a rung that
        took three pairs was faced six times. Named because the number an
        operator has to be able to read off the log is "how often did the
        gradient actually see *this tape*" -- the coverage defect section 2 of
        the plateau review found is invisible in any aggregate.

        The self-play half is folded into two entries (`_pool` and `_theta`)
        rather than one per snapshot: the pool is evicted and refilled, so its
        slot numbers are not stable names.

        `keep` is the episode index array `--pinned-once` builds -- the
        episodes actually played, out of the `2 * n_pairs` the pair layout
        describes. With it the count is per episode rather than "pairs times
        two", which is the whole point of the flag: a pinned rung reads 1 and
        the operator can see it. `None` is the doubling every earlier run
        logged.
        """
        idx = np.asarray(idx)
        n_pool = len(self.pool)
        n_arch = len(self.archetypes)
        counts = (np.bincount(idx, minlength=n_pool + n_arch + 1) * 2
                  if keep is None else
                  np.bincount(idx[np.asarray(keep) // 2],
                              minlength=n_pool + n_arch + 1))
        out = {name: int(counts[n_pool + i])
               for i, name in enumerate(self.archetype_names[:n_arch])}
        out["_pool"] = int(counts[:n_pool].sum())
        out["_theta"] = int(counts[n_pool + n_arch])
        return out

    def tape_slot_complaint(self):
        """Why this configuration trains against no tape at all, or `None`.

        The `--arch-frac 0` trap, made loud. Between flow123 and flow127 five
        runs were launched with tape rungs loaded, tape tables registered and
        `--arch-frac 0.0`: every episode went to the self-play pool, the runs
        were pure self-play, and their tape verdicts were void. Nothing in the
        run said so -- the rungs were listed at startup exactly as a run that
        faced them would list them.

        Returns one sentence naming the flag that did it, so
        `scripts/train.py` can warn (or, under
        `--require-tape-slots`, refuse).
        """
        tapes = [self.archetype_names[i]
                 for i, _t in tuple(self.tape_slots) + tuple(self.tape_act_slots)
                 if i < len(self.archetype_names)]
        if not tapes:
            return None
        names = sorted(set(tapes))
        n_arch = len(self.archetypes)
        k = arch_pairs(1024, n_arch, self.cfg.arch_frac)
        if k <= 0:
            return (f"--arch-frac {self.cfg.arch_frac:g} gives the archetype "
                    f"block no episode slots, so the {len(names)} tape rung(s) "
                    f"loaded ({', '.join(names[:6])}"
                    f"{', ...' if len(names) > 6 else ''}) are never played: "
                    f"this run is self-play with the tapes loaded but unused.")
        w = self.weighted_slots()
        if w is None:
            return None
        w = np.asarray(w, float)
        zero = [n for n in names
                if w[self.archetype_names.index(n)] <= 0]
        if len(zero) == len(names):
            return (f"--rung-weight puts every tape rung on weight 0 "
                    f"({', '.join(zero[:6])}"
                    f"{', ...' if len(zero) > 6 else ''}), so none of them "
                    f"takes an episode slot and the gradient never sees a "
                    f"tape.")
        return None

    def _play(self, thetas, words, opp, tables, starts=None, flow=None,
              tape_ctl=None, *, episodes=None, layout=None):
        """Every candidate over the shared episode set -> [pop, episodes, ...].

        Episode index `e` decomposes as (seed `e // 2`, seat `e % 2`), so every
        seed is played once from each side of the board against the same
        opponent. Results are returned per episode, not averaged: which summary
        to take is the caller's business now that fitness is shaped.

        `starts` is `(nquad, money)` per **episode** (see `episode_starts`);
        omitted, every episode opens on the engine's day 0. It used to be per
        seed pair, and that was the bug `place_handicap` documents: an
        asymmetric row indexed by pair lands on our seat in one of the pair's
        two games.

        `flow` is `market.apply_flow`'s control word per **episode** (see
        `flow_control`), or None for a run with no flow rung. Episode
        resolution for the same reason the starts are: the flow belongs to the
        opponent's physical seat, which is `1 - seat` and therefore differs
        between a pair's two games.

        `tape_ctl` is `--tape-actions`' `[seat, table]` word per episode (see
        `episode_tape_ctl`), or None. Independent of `flow`: each is appended
        to the evaluator call only when it exists.

        `episodes` overrides `cfg.episodes` as the batch length, and `layout`
        overrides the `(pair, seat) = (e // 2, e % 2)` decomposition with an
        explicit `(pair_of_episode, seat_of_episode)` pair of int arrays of
        that length. Both are `None` on every call but `--pinned-once`'s, and
        `None` reconstructs exactly the two expressions above -- a pinned rung
        is the one case where an episode is *not* half of a mirrored pair, so
        the batch needs to be able to say which pair and which seat each
        episode is rather than derive it from its position.
        """
        cfg = self.cfg
        pop = thetas.shape[0]
        E = int(cfg.episodes if episodes is None else episodes)
        ci, ei = jnp.meshgrid(jnp.arange(pop), jnp.arange(E), indexing="ij")
        ci, ei = ci.ravel(), ei.ravel()
        total = ci.shape[0]
        nq, mo = starts if starts is not None else cold_starts(E)
        nq, mo = jnp.asarray(nq), jnp.asarray(mo)

        # Chunks are rounded down to a multiple of the device count so every
        # device gets an equal share. The final chunk is padded back up to a
        # full `step` rather than left ragged: a short trailing shape would
        # compile a second program, and an odd one cannot be split evenly across
        # the mesh at all. The padding repeats already-scheduled episodes and is
        # discarded, so it changes cost, never results.
        step = max(self.n_devices, (cfg.chunk // self.n_devices) * self.n_devices)
        pad = (-total) % step
        if pad:
            ci = jnp.concatenate([ci, ci[-1:].repeat(pad)])
            ei = jnp.concatenate([ei, ei[-1:].repeat(pad)])
        if layout is None:
            seat = (ei % 2).astype(jnp.int32)
            pair = ei // 2
        else:
            ep_pair, ep_seat = layout
            seat = jnp.asarray(ep_seat, jnp.int32)[ei]
            pair = jnp.asarray(ep_pair, jnp.int32)[ei]
        outs = []
        for s in range(0, total + pad, step):
            sl = slice(s, s + step)
            rows = [thetas[ci[sl]], opp[pair[sl]], words[pair[sl]], seat[sl],
                    nq[ei[sl]], mo[ei[sl]]]
            # The two optional words ride the same shard so every array in the
            # batch is laid out across the mesh the same way; they are pulled
            # back off by name because they are independent -- a run may have
            # either, both or neither.
            opt = [a if a is None else a[ei[sl]] for a in (flow, tape_ctl)]
            batch = list(shard_batch(self.mesh, *rows,
                                     *[a for a in opt if a is not None]))
            fixed, rest = batch[:len(rows)], batch[len(rows):]
            f = rest.pop(0) if opt[0] is not None else None
            t = rest.pop(0) if opt[1] is not None else None
            outs.append(self._eval(tables, *fixed, flow=f, tape_ctl=t))
        return jnp.concatenate(outs)[:total].reshape(pop, E, *outs[0].shape[1:])

    # ---------------------------------------------------------------- one step

    def apply_gradient(self, grad):
        """One optimiser step on `grad`, in place on `self.theta`.

        Split out of `generation` so the two step rules -- and the flags that
        pick between them -- can be exercised on a synthetic gradient without
        an episode. `generation` calls it with the ES gradient and nothing
        else; the arithmetic below is byte for byte the arithmetic that was
        inline there, on the `adam` default.

        `--optimizer sgd` swaps only the numerator. Adam divides by
        `sqrt(vhat)`, which is a per-coordinate normaliser: a coordinate whose
        gradient is pure noise still has `|mhat| ~ sqrt(vhat)`, so it still
        takes a step of about `lr`. Over G generations that is a random walk of
        `lr*sqrt(G)` per coordinate away from wherever the run started, which
        is exactly what a champion-seeded run must not do. Plain momentum SGD
        (`m = beta1*m + (1-beta1)*grad; theta += lr*m`) has no such floor: the
        step is proportional to the gradient, so a generation that measured
        nothing moves theta by nothing much. It costs the scale invariance --
        `lr` now has units, and has to be retuned against the gradient
        magnitude the fitness shaping actually produces.
        """
        cfg = self.cfg
        # `adam_t`, not `t`. The bias correction exists to undo the zero-init of
        # `m` and `v`, so it has to count from the last time they *were* zeroed
        # -- and `_maybe_restart` and `--from-best` zero them thousands of
        # generations in. Correcting a freshly cleared `m`/`v` by
        # `1 - beta**t` with t in the thousands divides by 1, which leaves
        # `mhat/sqrt(vhat)` at `(1-b1)/sqrt(1-b2) = 3.16` per coordinate instead
        # of 1: a first step 3.16x the intended `lr`, decaying over ~2,000
        # generations. That inflated ||theta|| 17.6 -> 46 on flow2 (the
        # weight-decay equilibrium is 15.8) and collapsed the policy in five
        # generations, twice.
        self.adam_t += 1
        self.m = cfg.beta1 * self.m + (1 - cfg.beta1) * grad
        if cfg.optimizer == "sgd":
            # `v` is left exactly as it was -- untouched, not cleared. A run
            # resumed out of an adam checkpoint into sgd carries the moment it
            # saved and simply stops reading it, and a run resumed the other
            # way finds it stale but valid; neither has to special-case a
            # missing array.
            delta = cfg.lr * self.m
        else:
            self.v = cfg.beta2 * self.v + (1 - cfg.beta2) * grad ** 2
            mhat = self.m / (1 - cfg.beta1 ** self.adam_t)
            vhat = self.v / (1 - cfg.beta2 ** self.adam_t)
            delta = cfg.lr * mhat / (jnp.sqrt(vhat) + cfg.eps_adam)
        # Decay is **decoupled** -- applied to theta, not folded into the
        # gradient. Folded in it is invisible: |wd*theta| measured 1.0% of
        # |grad| per coordinate on fix1, and Adam normalises the sum anyway, so
        # the norm random-walked 15.2 -> 41.0 over 1,739 generations on step
        # noise alone (lr*sqrt(gens*n) = 52). Every point of that inflation
        # pushes the macro heads deeper into saturation, where a sigma-scale
        # perturbation cannot change the decoded action at all. Decoupled, the
        # norm has an equilibrium: ||theta|| = lr*sqrt(n / (2*wd)) ~ 17 at these
        # defaults (lr 0.02, wd 0.003), which is the responsive band an
        # untrained policy starts in. `n` there is the number of *live*
        # coordinates (masking drops 825 of 4,584, so the equilibrium is
        # 0.02*sqrt(3759/0.006) ~ 15.8), and the masked ones are left alone
        # entirely -- decay applied to a coordinate that never receives a
        # gradient would just walk it to zero and destroy its init.
        #
        # The head and aux biases are exempt (see `bias_mask`) and bounded by a
        # +-`bias_clip` box instead: a shared norm budget cannot both hold the
        # weights in the responsive band and let a discrete head commit.
        step = self.theta + delta
        upd = jnp.where(self.no_decay > 0,
                        jnp.clip(step, -cfg.bias_clip, cfg.bias_clip),
                        (1.0 - cfg.weight_decay) * step)
        self.theta = jnp.where(self.mask > 0, upd, self.theta)

    @staticmethod
    def realised_price(money):
        """Coins per unit sold over `LATE_PRICE_DAYS`, per episode. -> (mine, theirs)

        A seat that sold nothing in the window is given a price of 0 rather
        than a NaN. That is a deliberate floor and not merely safe arithmetic:
        under `--late-price-weight` it scores "sold nothing late" as the worst
        possible price, which is the right sign -- a policy that dodges the
        term by not selling has not realised a good price, it has realised
        none. It also keeps the ranking finite, and ES ranks or it does
        nothing.
        """
        def per_unit(units, coins):
            u = units.astype(jnp.float32)
            return jnp.where(units > 0, coins.astype(jnp.float32)
                             / jnp.maximum(u, 1.0), 0.0)
        return (per_unit(money[..., 5], money[..., 6]),
                per_unit(money[..., 7], money[..., 8]))

    @staticmethod
    def day_metric_means(money):
        """Population means of the raw shaping quantities. -> 4- or 6-tuple, or None

        `(mean day-D coin lead, mean net filled tiles, mean realised-price
        lead over days 15-29, mean SELL rows per selling day for our seat)`
        over every candidate and every episode of the generation, or `None`
        when `money` is only two columns wide -- which is what a test stubbing
        `Trainer.evaluate` returns, and what a run whose evaluator predates
        `day_metrics` would.

        On a tree carrying the forward-admit gene (`sim.rollout.FWD_GENE`,
        column 11) two more follow:

        * `fwd`, the mean decoded `macro.forward_days` over (member, episode,
          day) -- the horizon the population actually planned with, in days;
        * `fwd>0`, the fraction of *members* whose mean horizon over their own
          episodes is above zero -- how much of the population the gene is
          alive in at all, which a mean alone cannot say (one member at six
          days and 63 at zero reads the same as everyone at 0.09).

        Both come off `money`, so they cost one column and no rollout. On a
        tree without the block the tuple is the 4 it always was.

        Diagnostics only: these are the numbers the plateau review asked to see
        on the gen line **at weight 0**, so that a shaped arm's log has an
        unshaped one to be read against. Nothing here reaches the gradient.
        """
        if money.shape[-1] < 11:
            return None
        ours, theirs = Trainer.realised_price(money)
        days = money[..., 10]
        rows_per_day = jnp.where(days > 0,
                                 money[..., 9].astype(jnp.float32)
                                 / jnp.maximum(days.astype(jnp.float32), 1.0),
                                 0.0)
        out = (float((money[..., 2] - money[..., 3]).mean()),
               float(money[..., 4].mean()) / TILE_FILL_NDAYS,
               float((ours - theirs).mean()),
               float(rows_per_day.mean()))
        if money.shape[-1] < 12:
            return out
        per = money[..., 11].astype(jnp.float32) / spec.N_DAYS   # [pop, E]
        return out + (float(per.mean()), float((per.mean(axis=-1) > 0).mean()))

    def fitness_bonus(self, money):
        """The day-10 shaping term for `shaped_advantage`, in coins. -> [pop, E] or None

        `None` -- both weights at 0.0, which is the default -- is the whole
        inertness guarantee: `shaped_advantage` then evaluates the expression
        it evaluated before this method existed, on the same array, rather
        than adding a zeroed one to it. The two weights are compared to 0.0
        exactly, because "inert" has to be a decision about the flag the user
        typed and not about whether a product underflowed.

        * `--d10-cash-weight w` adds `w * (our day-D purse - theirs)`. The
          quantity is already coins, so `w` is a pure exchange rate between a
          coin held on day D and a coin held at the finish; `w = 1.0` says
          they are worth the same, and the loss ledger's finding -- that in 69
          of 88 losses the day-9 -> day-10 swing exceeded the final margin --
          is the argument that it is not far below 1.
        * `--tile-fill-weight w` adds `w * mean_{d=10..25}(planted - idle)`
          for our seat. That mean is in **tiles**, so `w` is coins per net
          filled tile and the conversion is entirely in the flag: nothing is
          hidden in a constant here, and the number the gen line logs times
          the number the launcher passes is exactly the coins added.
        * `--late-price-weight w` adds `w * (our coins per unit sold over days
          15-29 - theirs)`. Same rule again: the quantity is coins per unit,
          so `w` is the exchange rate into margin coins and the flag carries
          it. The 30-game top-10 ledger prices that rate: a ~20 coin/unit
          advantage came with +19k of late income, so ~950 is where the term
          would be worth what it measures and anything near it makes the
          shaping the objective.

        The first term and the third pull **against** each other. The 2100
        band wins by being ahead on day 10; the top ten are level or behind
        there (paired gap -459) and win the second half on price. Setting both
        in one arm asks for a policy that is ahead early *and* patient late,
        which may exist but is not what either ledger observed -- so an arm
        that does it should say why.
        """
        cfg = self.cfg
        d10_w, fill_w = float(cfg.d10_cash_weight), float(cfg.tile_fill_weight)
        price_w = float(cfg.late_price_weight)
        if d10_w == 0.0 and fill_w == 0.0 and price_w == 0.0:
            return None
        if money.shape[-1] < 11:
            raise ValueError(
                "--d10-cash-weight / --tile-fill-weight / --late-price-weight "
                "need the evaluator's day metrics, and this one returns only "
                "[mine, theirs]. A test that stubs `Trainer.evaluate` must "
                "either widen the stub to 11 columns or leave the weights at 0.")
        bonus = jnp.zeros(money.shape[:-1], jnp.float32)
        if d10_w != 0.0:
            bonus = bonus + d10_w * (money[..., 2] - money[..., 3]).astype(jnp.float32)
        if fill_w != 0.0:
            bonus = bonus + (fill_w / TILE_FILL_NDAYS) * money[..., 4].astype(jnp.float32)
        if price_w != 0.0:
            ours, theirs = self.realised_price(money)
            bonus = bonus + price_w * (ours - theirs)
        return bonus

    def prepare_generation_field(self):
        """Build the exact random field consumed by one ordinary generation."""
        cfg = self.cfg
        half = cfg.pop // 2
        key = self.key
        self.key, k = jax.random.split(self.key)
        noise = perturbations(k, half, self.n)

        # Fresh episode seeds each generation, shared across the whole
        # population. Half as many seeds as episodes: each is played twice, once
        # per seat.
        pin, n_pairs = self.pinned_block(), max(cfg.episodes // 2, 1)
        if pin is not None:
            n_pairs = max((cfg.episodes - len(pin)) // 2, 1)
        n_slots = n_pairs if pin is None else len(pin) + n_pairs
        seeds = self.rng.integers(0, 2 ** 31 - 1, n_slots)
        candidates = self.candidates()
        if pin is None:
            idx, keep = self.opponent_index(n_pairs), None
        else:
            # The pinned block leads, one slot per pinned rung, and the
            # residual budget is allocated behind it exactly as it always was
            # -- `drop` keeps the pinned rungs out of that allocation so the
            # freed pairs go to the drawn tapes, the archetypes and self-play
            # through the carry logic rather than back to the boards they came
            # from.
            idx = np.concatenate([len(self.pool) + np.asarray(pin, np.int64),
                                  self.opponent_index(n_pairs, drop=pin)])
            keep = self.pinned_keep(pin, n_pairs)
        # After `idx`, because which slots are pinned is a fact about the
        # opponent each slot drew; the draw above is unmoved so the rng stream
        # is the one it always was.
        words = jnp.asarray(host_words(self.pinned_seeds(seeds, idx)))
        rung_episodes = self.rung_episodes(n_slots, idx, keep)
        self.last_rung_episodes = rung_episodes
        opp = jnp.stack([candidates[i] for i in idx])

        # One market draw per generation: common random numbers still hold
        # across the population (every candidate faces the same market), while
        # the market itself moves between generations.
        tables = (self.tables if cfg.market_jitter <= 0 else
                  build_tables(jnp, spec.sample_market_params(self.rng, cfg.market_jitter)))
        # Warm starts are drawn once per generation, like the seeds: shared by
        # every candidate, so they stay inside the common-random-numbers scheme.
        # Episode resolution, because a handicapped rung's opening belongs to
        # one seat of the pair -- see `episode_starts`.
        # Drawn in this order because both take from `self.rng` and the starts
        # drew first before the flow rung existed. Passed positionally only when
        # there is a flow, so a run without the rung calls `_play` with exactly
        # the arguments it always took -- same reason as `_eval`.
        starts = self.episode_starts(n_slots, idx)
        flow = self.episode_flow(n_slots, idx)
        tape_ctl = self.episode_tape_ctl(n_slots, idx)
        tape = self.tape_episodes(n_slots, idx)
        episodes, layout, ep_weight = None, None, None
        if keep is not None:
            # Every per-episode array above was built on the full `2 * n_slots`
            # pair layout, which is what keeps `episode_starts`,
            # `episode_flow`, `episode_tape_ctl` and `tape_episodes` on the one
            # decomposition they document. The pinned block then drops one of
            # its two seats here, and only here.
            nq, mo = starts
            starts = (np.asarray(nq)[keep], np.asarray(mo)[keep])
            flow = None if flow is None else flow[keep]
            tape_ctl = None if tape_ctl is None else tape_ctl[keep]
            tape = None if tape is None else tape[keep]
            episodes, layout = len(keep), (keep // 2, keep % 2)
            ep_weight = self.pinned_weights(pin, len(keep))
        return GenerationField(noise, key, self.key, seeds, idx, keep, words,
                               opp, tables, starts, flow, tape_ctl, tape,
                               episodes, layout, ep_weight, rung_episodes)

    def play_generation_field(self, thetas, field):
        """Evaluate candidate thetas on one prepared common-random field."""
        if field.flow is None and field.tape_ctl is None:
            return self._play(thetas, field.words, field.opponents,
                              field.tables, field.starts,
                              episodes=field.episodes, layout=field.layout)
        return self._play(thetas, field.words, field.opponents, field.tables,
                          field.starts, field.flow, field.tape_ctl,
                          episodes=field.episodes, layout=field.layout)

    def antithetic_scope_diagnostic(self, pairs=32):
        """Compare fixed M/H/J scopes on generation zero without an update."""
        if int(self.t) != 0:
            raise ValueError("scope diagnostic requires generation zero")
        if float(self.sigma) != 0.01:
            raise ValueError("scope diagnostic is fixed at sigma 0.01")
        if int(pairs) != 32 or self.cfg.pop // 2 < int(pairs):
            raise ValueError("scope diagnostic requires first 32 pairs")
        scopes = (("M", "mh,ms"), ("H", "w2,b2"),
                  ("J", "mh,ms,w2,b2"))
        key_before = self.key
        rng_before = copy.deepcopy(self.rng.bit_generator.state)
        credit_before = (None if self.slot_carry is None else
                         self.slot_carry.credit.copy())
        rungs_before = copy.deepcopy(self.last_rung_episodes)
        try:
            field = self.prepare_generation_field()
            noise = field.noise[:pairs]
            live = PO.live_mask()
            masks = jnp.stack([jnp.asarray(live * train_mask(names))
                               for _label, names in scopes])
            masked = noise[None, :, :] * masks[:, None, :]
            candidates = []
            for block in masked:
                candidates.extend((self.theta + self.sigma * block,
                                   self.theta - self.sigma * block))
            money = self.play_generation_field(jnp.concatenate(candidates), field)
            money = jax.block_until_ready(money).reshape(
                len(scopes), 2 * pairs, *money.shape[1:])
            own, relative, own_rank, relative_rank, advantage = [], [], [], [], []
            for block in money:
                mine, theirs = block[..., 0], block[..., 1]
                bonus = self.fitness_bonus(block)
                o, r = fitness_components(mine, theirs, self.cfg, field.tape,
                                          bonus, field.episode_weight)
                ro, rr = rank_normalise(o), rank_normalise(r)
                own.append(o); relative.append(r)
                own_rank.append(ro); relative_rank.append(rr)
                advantage.append(self.cfg.abs_weight * ro
                                 + (1.0 - self.cfg.abs_weight) * rr)
            own, relative = jnp.stack(own), jnp.stack(relative)
            own_rank, relative_rank = jnp.stack(own_rank), jnp.stack(relative_rank)
            advantage = jnp.stack(advantage)
            deltas = jnp.stack((own_rank[:, :pairs] - own_rank[:, pairs:],
                                relative_rank[:, :pairs] - relative_rank[:, pairs:],
                                advantage[:, :pairs] - advantage[:, pairs:]), axis=1)
            gradients = jnp.einsum("scp,spn->scn", deltas, masked) \
                        / (2 * pairs * self.sigma)
            return ScopeDiagnostic(tuple(label for label, _ in scopes), pairs,
                                   field, masks, masked, money,
                                   own, relative, own_rank, relative_rank,
                                   advantage, gradients)
        finally:
            self.key = key_before
            self.rng.bit_generator.state = rng_before
            if self.slot_carry is not None:
                self.slot_carry.credit = credit_before
            self.last_rung_episodes = rungs_before

    def generation(self):
        """One ES step. -> (mean win, best win, abs coins or None, AbsReport or None)."""
        cfg = self.cfg
        half = cfg.pop // 2
        field = self.prepare_generation_field()
        eps = field.noise * self.mask
        thetas = jnp.concatenate([self.theta + self.sigma * eps,
                                  self.theta - self.sigma * eps])
        money = self.play_generation_field(thetas, field)
        mine, theirs = money[..., 0], money[..., 1]
        # Read before the gradient and unconditionally, so the gen line carries
        # both raw quantities on a weight-0 arm too; `fitness_bonus` is what
        # decides whether either of them reaches the ranking.
        self.last_day_metrics = self.day_metric_means(money)
        # Cleared here so the gen line carries a centre reading only on the
        # generations that actually measured one (`abs_every`/`champ_every`),
        # rather than repeating the last one for ten lines.
        self.last_centre_fwd = None
        adv = shaped_advantage(mine, theirs, cfg, field.tape,
                               self.fitness_bonus(money), field.episode_weight)
        grad = (adv[:half] - adv[half:]) @ eps / (cfg.pop * self.sigma)

        self.t += 1
        self.apply_gradient(grad)

        if self.t % cfg.pool_every == 0:
            # The eviction batch is `2 * len(words)`, so it is sliced back to
            # the pair count an unflagged run has: `--pinned-once` must not
            # give the jitted evaluator a second input shape to compile for.
            self._snapshot(field.words[:max(cfg.episodes // 2, 1)],
                           field.tables)

        # Logged in win-rate units regardless of what the gradient consumed, so
        # `mean_win` stays comparable against every earlier run's curve.
        win = win_scores(mine, theirs).mean(axis=1)

        # The real-engine gate (`--real-gate`), polled once a generation and
        # never waited on. Before the measurement block, so a verdict that
        # landed while the last generation ran is already the incumbent by the
        # time this generation nominates -- and so that a nomination made below
        # finds the slot free rather than waiting a whole measurement period.
        self.last_real_gate = None
        self.last_recentre = None
        if self.real_gate is not None:
            self.last_real_gate = self._poll_real_gate()
        # Did an in-sim record nominate this generation? It owns the slot if
        # it did: the cadence below is the fallback for the generations the
        # selector says nothing about.
        nominated = False
        if self.real_gate is not None and self.real_gate.recentre_due():
            self._recentre_on_record()
            # The centre *is* the record now, so offering it to the gate this
            # generation would spend an eval re-measuring the incumbent.
            nominated = True

        # One absolute measurement serves both schedules: the yardstick is fixed
        # (fixed seeds, fixed archetypes, default market), so the same numbers
        # answer "is this the best theta so far" and "is this the champion".
        rep = None
        if self.t % cfg.abs_every == 0 or self.t % cfg.champ_every == 0:
            rep = self.absolute_report(self.theta,
                                       draws=self.measurement_draws())
            self.abs_history.append((self.t, rep.coins, rep.win))
            sel = self.selection_score(rep)
            hold = self.holdout_selection_score(rep)
            accepted = self._accept_best(sel, hold)
            # Beating the record only buys the right to be *re-measured*
            # (`--best-replicate`); what takes it is the replicate mean, which
            # is why `sel`/`hold` are rebound here and the screening reading is
            # carried out on `last_replicate` instead.
            self.last_replicate = None
            if accepted and int(cfg.best_replicate) > 0:
                sel, hold, accepted = self._replicate_record(sel, hold)
            self.last_best_gate = {"sel": sel, "hold": hold,
                                   "accepted": accepted}
            if accepted:
                self.best_abs = sel
                # Tracked in both gate modes, so that a run switched to `both`
                # on a resume compares against the record's own holdout rather
                # than against a sentinel that would wave the next one through.
                self.best_hold = hold
                self.best_sim_theta = self.theta
                if self.real_gate is None:
                    self.best_abs_theta = self.theta
                    self.last_improve = self.t
                else:
                    # Under `--real-gate` an in-sim record only *nominates*.
                    # `best_abs_theta`, the record file and the stall clock all
                    # move in `_poll_real_gate`, when the real engine has
                    # spoken -- while `best_abs` above keeps moving here, so a
                    # rejected nomination cannot wedge the stream behind it.
                    self.real_gate.propose(self.theta, self.t)
                    nominated = True
            elif self.real_gate is None:
                self._maybe_restart()
            if self.real_gate is not None:
                self._gate_restart_check()
            if self.t % cfg.champ_every == 0:
                self._measure_champion(rep)
        # After the record block, so that a record and the cadence landing on
        # the same generation is decided in the record's favour.
        if self.real_gate is not None and not nominated:
            self._nominate_centre()
        abs_coins = rep.coins if (rep is not None and self.t % cfg.abs_every == 0) else None
        return float(win.mean()), float(win.max()), abs_coins, rep

    def _replicate_record(self, screen_sel, screen_hold):
        """Re-measure a candidate record on games it was not screened on.

        -> (sel, hold, accepted), where `sel` is the **replicate mean** and is
        what the record is taken at if it is taken at all.

        `best_abs` is a max over a sequence of noisy readings, so the reading
        that takes the record is the one whose noise pointed up: the record is
        biased upward by the largest upward error the run happened to make, and
        `best_abs.npy` -- the file `--promote` ships -- is whichever theta made
        it. `--best-margin` raises the bar the noise has to clear; it does not
        stop the selected reading from being the lucky one, because the same
        max is still taken over the same fixed measurement.

        Replication does. A candidate that clears the bar is re-measured `N`
        times on levels and seed pairs it has never been read on
        (`measurement_draws`, `replicate_words`), and the record is taken only
        if the **mean of those** clears the same bar -- at that mean, not at the
        screening reading. Both halves matter:

        * measuring again on fresh games is what makes the second reading an
          unbiased estimate of the theta rather than a re-reading of the luck;
        * *recording* the fresh mean is what stops the bar itself from
          drifting upward, since a record kept at the screening value would
          hand the next candidate a target no honest measurement can reach.

        The gate is the same `_accept_best`, so `--best-margin` and
        `--best-gate both` apply to the replicate exactly as they applied to
        the screen. A replicate the coin floor blocks (`selection_score` gives
        `None`) is a refusal outright: the candidate failed the floor on games
        it had not been tuned on, which is the floor doing its job.

        The rollout cost is `N` extra measurements per *accepted candidate*,
        not per generation -- a run that has stopped improving pays nothing.
        """
        cfg = self.cfg
        n = int(cfg.best_replicate)
        sels, holds = [], []
        for i in range(1, n + 1):
            rep = self.absolute_report(self.theta,
                                       draws=self.measurement_draws(i),
                                       words=self.replicate_words(i))
            s = self.selection_score(rep)
            if s is None:
                sels = None
                break
            sels.append(s)
            holds.append(self.holdout_selection_score(rep))
        if sels is None:
            sel, hold, accepted = None, screen_hold, False
        else:
            sel = float(np.mean(sels))
            hold = float(np.mean(holds))
            accepted = self._accept_best(sel, hold)
        self.last_replicate = {"screen": screen_sel, "replicate": sel,
                               "n": n, "rejected": not accepted}
        if not accepted:
            self.replicate_rejects += 1
        return sel, hold, accepted

    def _nominate_centre(self):
        """The `--real-gate-every` cadence: offer the search centre.

        In-sim records are the gate's only other source of candidates, and
        they stop coming -- a run takes a handful in its first thousand
        generations and then none for thousands more, while the centre keeps
        moving. The gate then idles on an incumbent whose theta is older than
        everything the run has learned since, which is the opposite of what
        the flag is for.

        So every `N` generations the centre itself is nominated. It is the
        same `propose` and the same accept rule -- the real engine still has
        to prefer it -- and it is skipped whenever the gate is busy
        (`RealGate.due`), so the cadence can never displace a record's
        nomination or queue more real-engine work than the gate drains.
        """
        if self.real_gate.due(self.t):
            self.real_gate.propose(self.theta, self.t, source="periodic")

    def _recentre_on_record(self):
        """Put the search back on the gated record (`--real-gate-recentre`).

        The gate filters; it does not steer. Every candidate it refuses leaves
        the centre exactly where it was, and on flow27c/28c/27d that centre
        walked away from the record and never came back -- every periodic
        candidate after the record scored below the bar, because the gradient
        that moves the centre is in-sim and the bar is not. A run of `K`
        refusals is the run admitting that, and the answer is the one
        `_maybe_restart` already implements for the in-sim version of the same
        problem: jump back onto the best theta on record and clear the moments
        that describe the basin just left.

        It is deliberately the *same* move. A second, subtly different restart
        would mean two answers to "where does the search resume from", and the
        one a resume rebuilds sigma from (`sigma_steps`) has to be the one
        that ran.
        """
        gate = self.real_gate
        self.last_recentre = {"record_gen": gate.record_gen,
                              "count": int(gate.periodic_rejects)}
        gate.periodic_rejects = 0
        self._restart_from_record()

    def _poll_real_gate(self):
        """One non-blocking look at the gate, and the record move it earns.

        Under `--real-gate-replicate` the verdict that moves it is the
        *replicate's* -- an acceptance is provisional until the second
        reading confirms it -- so `best_abs.npy` changes less often and every
        theta it holds has been measured twice.

        This is the only place `best_abs_theta` changes under `--real-gate`,
        which is what makes `best_abs.npy`, `--promote`, `--from-best` and
        `_maybe_restart` all read a theta the *real engine* preferred rather
        than one the proxy did.
        """
        res = self.real_gate.poll()
        if res is not None and res.get("restore_theta") is not None:
            # A provisional record that failed its replicate. Normally a
            # no-op -- nothing moved `best_abs_theta` while the record was
            # provisional, which is the whole point -- but the gate owns the
            # question of which theta the bar belongs to, so it is the gate's
            # answer that gets written. Not an improvement: the stall clock
            # stays where it was.
            self.best_abs_theta = jnp.asarray(res["restore_theta"])
        if res is not None and res["accepted"]:
            self.best_abs_theta = jnp.asarray(res["theta"])
            # The stall clock runs on the real record too: a run whose in-sim
            # number climbs while the real one does not is exactly the run
            # that should be sent back to the real record, and letting the
            # nominations reset the clock would make the restart unreachable.
            self.last_improve = self.t
        return res

    def _gate_restart_check(self):
        """`_maybe_restart`, under the gate's clock.

        Two differences from the ungated call, both forced by the record being
        the real one:

        * nothing to jump back to until the gate has accepted something, so a
          run with no real record yet never restarts (the ungated rule would
          send it back to the untrained init);
        * a generation whose verdict just *took* the record has improved, so
          it is not a stall however long the in-sim number has been flat.
        """
        if not self.real_gate.have_record:
            return
        if self.last_real_gate is not None and self.last_real_gate["accepted"]:
            return
        self._maybe_restart()

    def _maybe_restart(self):
        """IPOP-style restart: one sigma step-up from the best theta on record.

        ES with a fixed sigma has one failure mode that looks exactly like
        convergence -- the population sits inside a basin whose walls are
        further than `sigma` away, so every perturbation is worse and the mean
        stops moving. Growing the step from the best theta is the cheapest
        escape that does not throw the run away. Once only *while it grows the
        step*: a second doubling is indistinguishable from admitting the run is
        over, and the operator can start a fresh one with a larger `--sigma`.

        At `--stall-sigma-mult 1.0` there is no step-up to run out of and the
        restart is only "jump back onto `best_abs_theta`, clear Adam" -- which
        is exactly as sound the fifth time as the first, and which an operator
        would otherwise have to supply by hand (stop, resume `--from-best`)
        every time the run wandered below its own record. So the once-only rule
        is attached to the thing it is actually about, the sigma. A repeat
        still has to earn a full `--restart-sigma-on-stall` stall, since the
        previous one reset `last_improve`; and `load_resume` rebuilds sigma as
        `sigma * mult ** restarts`, which at 1.0 is sigma however often it
        fired.

        How far it grows is `--stall-sigma-mult`, because the premise is not
        universal. On this ladder sigma 0.04 is not an escape but a collapse --
        flow2 fell 133k -> 98-118k abs and 0.88 -> 0.0x anchor win inside 300
        generations of it, and flow1 never improved in 2,900 -- while 0.02
        keeps producing. A multiplier of 1.0 keeps the productive step and
        leaves the restart as what still helps: the jump back onto the best
        theta with the moments cleared.

        The Adam moments are cleared either way. They describe the curvature of
        the basin just left; carried across the jump they would spend the first
        generations undoing it. `adam_t` goes with them: it is what makes the
        bias correction correct for the zeros they now hold, and leaving it at
        `t` turns the first step after the clear into 3.16x `lr` per
        coordinate -- see `step`.
        """
        cfg = self.cfg
        once_only = float(cfg.stall_sigma_mult) != 1.0
        if (cfg.restart_stall <= 0
                or (once_only and self.sigma_restarts > 0)
                or self.t - self.last_improve < cfg.restart_stall):
            return
        self._restart_from_record()

    def _restart_from_record(self):
        """The restart itself: theta back onto the record, moments cleared.

        Split out of `_maybe_restart` so that `--real-gate-recentre` performs
        the *same* move rather than a second one that drifts from it. The
        callers differ only in what convinced them: a stall in the in-sim
        number, or a run of real-engine refusals of the centre.

        The sigma step-up is the one part that is not unconditional. It is
        once-only at any `--stall-sigma-mult` above 1.0 (a second doubling is
        indistinguishable from admitting the run is over), so a later restart
        is the jump alone -- which is worth doing on its own, and is what
        `_maybe_restart`'s guard already refuses to do a second time.
        """
        cfg = self.cfg
        once_only = float(cfg.stall_sigma_mult) != 1.0
        bump = not (once_only and self.sigma_restarts > 0)
        self.theta = self.best_abs_theta
        if bump:
            self.sigma *= float(cfg.stall_sigma_mult)
            self.sigma_restarts += 1
            # Only a restart that moved sigma is one a resume has to rebuild
            # sigma from; see `sigma_steps` in `__init__`.
            self.sigma_steps += int(once_only)
        self.m = jnp.zeros(self.n)
        self.v = jnp.zeros(self.n)
        self.adam_t = 0
        self.last_improve = self.t

    # ---------------------------------------------------------------- measuring

    def _versus_pool(self, theta, words, tables):
        """Win rate of one theta against every ladder rung, both seats.

        The batch is a fixed `2 * n_pairs` regardless of how many rungs the pool
        currently holds. Sizing it per pool length instead would give the jitted
        evaluator a new input shape every time the ladder grows, and each of
        those costs a ~45 s recompile against a ~3 s generation.

        Only `_snapshot` reads this now: it is how the ladder decides which rung
        to evict, which is genuinely a head-to-head question. Champion selection
        left it on 2026-08-25 -- over a 13 h run `corr(abs, champ)` was -0.17.
        """
        pool = self.pool
        n_pairs = int(words.shape[0])
        p = len(pool)
        total = 2 * n_pairs
        k = np.arange(total)
        rung = k % p
        seat = ((k // p) % 2).astype(np.int32)
        widx = (k // (2 * p)) % n_pairs

        # Ladder measurements stay cold-start so `champ` / `mean_win` remain
        # comparable with every earlier run's curve.
        nq, mo = cold_starts(total)
        money = np.asarray(self._eval(
            tables,
            jnp.broadcast_to(theta, (total, theta.shape[0])),
            jnp.stack([pool[i] for i in rung]),
            words[jnp.asarray(widx)],
            jnp.asarray(seat), jnp.asarray(nq), jnp.asarray(mo),
            # Pool rungs only, so no episode here carries the flow -- but a run
            # that has the rung still passes the array, so it stays on one
            # compiled program instead of paying a second ~40 s compile. Same
            # for the action word.
            flow=self.flow_words(np.zeros(total, bool), seat),
            tape_ctl=self.tape_act_words(np.zeros(total, bool), seat)))
        out = np.asarray(win_scores(money[:, 0], money[:, 1]))
        counts = np.bincount(rung, minlength=p)
        return np.bincount(rung, weights=out, minlength=p) / np.maximum(counts, 1)

    def measurement_draws(self, replicate=0):
        """The flow levels this measurement reads the rung at. -> ((int, int), ...)

        The run's one fixed set by default -- so a run without
        `--abs-fresh-draws` passes `absolute_report` exactly the tuple it read
        off `self.abs_draws` before this existed -- and a set drawn for this
        `(generation, replicate)` alone when the flag is on.

        A replicate is *always* freshened, whatever the flag says: replicating
        a screening reading on the very levels that produced it re-measures the
        seed luck rather than the theta, which is the opposite of the point.
        At `--abs-flow-draws 0` there is no family to draw from and this is
        empty either way; the replicate then differs from the screen in its
        seed pairs alone, which is still an independent sample of the games.
        """
        cfg = self.cfg
        if int(replicate) == 0 and not cfg.abs_fresh_draws:
            return tuple(self.abs_draws)
        return tuple(fresh_flow_draws(cfg.abs_flow_draws, self.t, replicate,
                                      cfg.abs_flow_scale, cfg.abs_flow_shift))

    def replicate_words(self, replicate):
        """Episode seed pairs for replicate `replicate`. -> words, as `abs_words`.

        A different *stream* from the fixed set (`REPLICATE_SEED`, not
        `FIXED_SEED`), so the replicate's games are new games and not a
        reshuffle of the screened ones -- the screening reading is biased
        upward by whatever those particular pairs were worth to this theta, and
        only pairs it has never been read on can measure that away. As many
        pairs as `abs_pairs`, so the sel/hold split (`n_abs_sel`) means the same
        thing in a replicate as in a screen.
        """
        seeds = np.random.default_rng(
            [REPLICATE_SEED, int(self.t), int(replicate)]
        ).integers(0, 2 ** 31 - 1, int(self.cfg.abs_pairs))
        return jnp.asarray(host_words(seeds))

    def absolute_report(self, theta, draws=None, words=None) -> AbsReport:
        """Coins against the archetypes on the fixed seeds, both seats.

        Cold start, default market: the number means the same thing in every
        run. Without archetypes there is nothing fixed to measure against.

        The fixed seed set is **split**. The first half selects (it is what
        `best_abs`, `--promote` and the champion read); the second half is only
        ever reported, as `abs_holdout`. Selection on a fixed 64-seed set is an
        invitation to fit those 64 games, and without a held-out half there is
        no way to see it happening: the two numbers tracking together is the
        evidence that the gain is real, and them diverging is the evidence it
        is not.

        The per-archetype decomposition comes back with it -- *both* sides. A
        mean alone cannot distinguish "earned more" from "the opponent
        collapsed", which is the exact confusion that let the previous
        objective drift scale-free.

        Three things joined it on 2026-08-26, and all three are inert at the
        defaults:

        * every headline is a **rung-weighted** mean of the per-rung means, at
          the same weights `opponent_slots` divides the gradient by;
        * `score` -- `mean_e sigmoid(margin / margin_scale)` -- rides along, so
          `--select-metric score` costs no extra rollout;
        * `keep` is each rung's coins here over its coins against the zero
          theta. A rung under `collapse_floor` is not an opponent, it is a free
          win, and it leaves the weighted means (`live` records which).

        The **opponent** holdout rides in the same batch (see `holdout_thetas`
        and `AbsReport.holdout_rungs`) rather than in a call of its own. One
        call is one input shape, and a second shape costs a ~40 s XLA compile
        against a ~3 s generation; the rungs also then share the seeds with the
        trained ones, so the comparison between them is paired.

        Two things joined it on 2026-08-27, and both are off by default:

        * `--abs-flow-draws K` replaces the flow rung's single reading at the
          **centre** of its randomisation with the mean over `K` fixed draws of
          it (`flow_ensemble_draws`). The centre is one arbitrary member of the
          family the gradient trains on, and measured against the real engine
          it is a *biased* member -- it ranks eight archived thetas at Spearman
          0.738 and inverts the top three, where the ten-draw mean ranks them
          at 0.976. The K blocks ride in this same batch, for the same reason
          the opponent holdout does; every other rung keeps its centre reading,
          so a run's coin headline still means what it meant. The centre's own
          flow margin is measured too and carried out on `flow_centre_margin`,
          so a log line can show the two side by side.
        * `--abs-select` moves which fixed seed pairs the *selected* half of
          this report is read on -- `sel` is the first half and today's rule,
          `hold` swaps the two, `all` reads every pair (which halves the
          statistic's variance and gives up the held-out ratchet;
          `_check_abs_select` refuses the combination that would pretend to
          keep both).

        `draws` and `words` override the two things a *replicated* or
        *freshened* measurement has to move (`--abs-fresh-draws`,
        `--best-replicate`): which levels of the flow family are played, and
        which episode seed pairs they are played on. Both default to the run's
        fixed ones, so every caller that does not pass them -- and every
        measurement of a run with neither flag -- builds the batch it always
        built, down to the byte.
        """
        if not self.archetypes:
            return AbsReport(0.0, 0.0, (), (), 0.0, 0.0)
        arch = list(self.archetypes)
        a = len(arch)
        held = list(self.holdout_thetas)
        rungs = arch + [h[1] for h in held]
        starts = np.concatenate([
            np.asarray(self.arch_handicap, np.int32).reshape(-1, 2),
            np.asarray([h[2] for h in held], np.int32).reshape(-1, 2)])
        r = len(rungs)
        words = self.abs_words if words is None else words
        n_pairs = int(words.shape[0])
        total = 2 * n_pairs * r
        k = np.arange(total)
        a_idx = k % r
        seat = ((k // r) % 2).astype(np.int32)
        widx = k // (2 * r)
        # The flow rung's level per episode. The base block is the centre --
        # scale 1.0, no day shift -- for the same reason the seeds are fixed:
        # two checkpoints' numbers have to be comparable, and a rung whose
        # level moved between them is not a yardstick. Every other rung ignores
        # these two columns entirely (`flow_control` forces an off episode back
        # to `market.FLOW_OFF`).
        scale = np.full(total, 1000, np.int32)
        shift = np.zeros(total, np.int32)
        draws = tuple(self.abs_draws if draws is None else draws) \
            if self.flow_rung >= 0 else ()
        if draws:
            # One more block of the flow rung's *own* episodes per draw, laid
            # out exactly as the base block lays that rung out -- both seats of
            # every fixed pair, the rung as the opponent, its handicap on
            # `1 - seat` (`starts[a_idx]` below, since `a_idx` is the rung).
            j = np.arange(2 * n_pairs)
            add = len(draws) * 2 * n_pairs
            a_idx = np.concatenate([a_idx, np.full(add, self.flow_rung, a_idx.dtype)])
            seat = np.concatenate([seat, np.tile((j % 2).astype(np.int32), len(draws))])
            widx = np.concatenate([widx, np.tile(j // 2, len(draws))])
            scale = np.concatenate(
                [scale] + [np.full(2 * n_pairs, s, np.int32) for s, _ in draws])
            shift = np.concatenate(
                [shift] + [np.full(2 * n_pairs, d, np.int32) for _, d in draws])
        # Which episodes carry a measured flow and off which table. The
        # `kaggle_flow` rung, when the run has one, is read at the **centre**
        # here -- the ensemble above is `kagg2_flow`'s alone, because that is
        # the reading every checkpoint on record was taken at and a yardstick
        # whose definition moved is not a yardstick.
        is_flow, f_table = self.flow_rung_tables(a_idx)
        is_ta, ta_table = self.tape_act_tables(a_idx)
        n_all = int(a_idx.shape[0])
        nq, mo = cold_starts(n_all)
        # The rung is the *opponent* here, so its opening goes at `1 - seat`.
        nq, mo = place_handicap(nq, mo, 1 - seat.astype(np.int64), starts[a_idx])
        # One call while the batch is the size it always was, so a run without
        # the ensemble issues the byte-identical evaluator call it always did.
        # The ensemble grows the batch by K blocks of the flow rung -- ~1.9x on
        # the live 11-rung ladder at K=10 -- so it is split once it outgrows
        # `--chunk`. The shard boundaries are a pure function of the flags, so
        # this costs at most two more XLA compiles for the whole run (a full
        # shard and a remainder), not one per generation. At the live
        # `--chunk 8192` nothing splits at all.
        limit = max(int(self.cfg.chunk), total)
        parts = []
        for lo in range(0, n_all, limit):
            s = slice(lo, min(lo + limit, n_all))
            parts.append(np.asarray(self._eval(
                self.tables,
                jnp.broadcast_to(theta, (s.stop - s.start, theta.shape[0])),
                jnp.stack([rungs[i] for i in a_idx[s]]),
                words[jnp.asarray(widx[s])],
                jnp.asarray(seat[s]), jnp.asarray(nq[s]), jnp.asarray(mo[s]),
                flow=self.flow_words(is_flow[s], 1 - seat[s],
                                     scale[s], shift[s], f_table[s]),
                tape_ctl=self.tape_act_words(is_ta[s], 1 - seat[s],
                                             ta_table[s]))))
        money = parts[0] if len(parts) == 1 else np.concatenate(parts)
        # The centre's own horizon, read off the measurement rather than from a
        # rollout of its own: column 11 is the season's sum of decoded
        # `macro.forward_days` for the seat `theta` played (see
        # `make_evaluator`), so the mean over the fixed boards divided by the
        # season is one number in days.
        self.last_centre_fwd = (float(money[:, 11].mean()) / spec.N_DAYS
                                if money.shape[-1] >= 12 else None)
        win = np.asarray(win_scores(money[:, 0], money[:, 1]))
        score = 1.0 / (1.0 + np.exp(-(money[:, 0] - money[:, 1])
                                    / self.cfg.margin_scale))
        if self.cfg.tape_score == "ours" and self.tape_slots:
            # Selection reads a tape rung the way the gradient does: our coins
            # alone, because the flow seat's are 25-48k of revenue its board
            # never grew (see `shaped_advantage`). The `mine` / `theirs`
            # columns below stay as measured -- they are the diagnostic, and
            # `--select-metric margin:<tape>` / `softwin:<tape>` name a margin
            # explicitly.
            is_tape = np.isin(a_idx, [i for i, _t in self.tape_slots])
            score = np.where(is_tape,
                             own_coin_score(money[:, 0], self.cfg, np), score)
        first = widx < self.n_abs_sel
        # Which pairs the *selected* numbers are read on, and which the
        # reported-only ones are. `sel` is the rule every checkpoint on disk
        # was written under; `hold` swaps the halves; `all` selects on every
        # pair and leaves the second half as a (no longer held-out) diagnostic.
        sel = {"sel": first, "hold": ~first,
               "all": np.ones(n_all, bool)}[self.cfg.abs_select]
        rest = first if self.cfg.abs_select == "hold" else ~first
        # The ensemble blocks are the flow rung's reading; the base block is
        # the centre's. A rung takes its numbers from one or the other, never
        # from both mixed together -- and since every draw contributes the same
        # number of episodes, the mean over the union *is* the mean of the K
        # draws' means, which is the statistic the fidelity table measured.
        ens = np.zeros(n_all, bool)
        ens[total:] = True
        base = ~ens
        block = lambda i: (ens if (draws and i == self.flow_rung) else base)
        per = [block(i) & sel & (a_idx == i) for i in range(a)]
        hold = [block(i) & rest & (a_idx == i) for i in range(a)]
        # Held-out rungs use the whole fixed seed set: nothing selects on them,
        # so there is no half to hold back, and the extra games are free once
        # they are in this batch anyway.
        holdout_rungs = tuple(
            (label, float(money[m, 0].mean()), float(money[m, 1].mean()),
             float((money[m, 0] - money[m, 1]).mean()), float(win[m].mean()))
            for (label, _, _), m in
            ((h, a_idx == a + i) for i, h in enumerate(held)))
        mine = [float(money[m, 0].mean()) for m in per]
        theirs = [float(money[m, 1].mean()) for m in per]
        # Per-rung, on the half nothing selects on. `--select-metric
        # margin:<rung>` gates on one rung's margin, so `--best-gate both` has
        # to be able to ask that rung the same question on unseen seeds; the
        # weighted headlines below cannot answer it.
        hmine = [float(money[m, 0].mean()) if m.any() else 0.0 for m in hold]
        htheirs = [float(money[m, 1].mean()) if m.any() else 0.0 for m in hold]
        wins = [float(win[m].mean()) for m in per]
        scores = [float(score[m].mean()) for m in per]

        # Zero-theta coins are the denominator of the collapse check. They come
        # from the same probe `MIN_COINS` gates on -- with the same handicaps --
        # so the ratio compares one rung's two games, not two rungs.
        zero = (list(self.archetype_coins)
                if len(self.archetype_coins) == a else [0.0] * a)
        keep = [float(t / z) if z > 0 else 0.0 for t, z in zip(theirs, zero)]
        floor = float(self.cfg.collapse_floor)
        live = [k_ >= floor for k_ in keep] if floor > 0 else [True] * a
        flat = np.array(self.rung_weights if len(self.rung_weights) == a
                        else np.ones(a), float)
        w = flat * np.array(live, float)
        if w.sum() <= 0:
            # Every rung collapsed. Excluding the lot would leave nothing to
            # measure, and a yardstick of zero rungs is worse than a soft one:
            # fall back to the unfiltered mixture and let `live` report it.
            live, w = [True] * a, flat
        wm = lambda v: float(np.average(np.asarray(v, float), weights=w))

        # The two readings of the flow rung side by side, on whichever pairs
        # this run selects on. Only the ensemble is selected *by* -- it is
        # already in `mine`/`theirs` above -- but the centre is the number
        # every earlier run reported, so the log can show the gap between the
        # de-biased statistic and the one it replaced without a second call.
        margin = lambda m: (float((money[m, 0] - money[m, 1]).mean())
                            if m.any() else 0.0)
        is_flow = sel & (a_idx == self.flow_rung)
        f_ens = margin(ens & is_flow) if draws and self.flow_rung < a else 0.0
        f_ctr = margin(base & is_flow) if draws and self.flow_rung < a else 0.0

        # The soft win rate, on the same masks and the same games the coin
        # means above are read on. Computed only when something selects on it,
        # so a run under any other metric issues the arithmetic it always did.
        tau = select_spec(self.cfg.select_metric).tau
        if tau:
            gap = money[:, 0] - money[:, 1]
            soft = lambda m: (float(np.tanh(gap[m] / tau).mean())
                              if m.any() else 0.0)
            softwin = tuple(soft(m) for m in per)
            holdout_softwin = tuple(soft(m) for m in hold)
        else:
            softwin = holdout_softwin = ()

        has_hold = all(m.any() for m in hold)
        return AbsReport(
            coins=wm(mine), win=wm(wins),
            mine=tuple(mine), theirs=tuple(theirs),
            holdout=wm([float(money[m, 0].mean()) for m in hold]) if has_hold else 0.0,
            holdout_win=wm([float(win[m].mean()) for m in hold]) if has_hold else 0.0,
            score=wm(scores),
            holdout_score=wm([float(score[m].mean()) for m in hold]) if has_hold else 0.0,
            wins=tuple(wins), keep=tuple(keep), live=tuple(live),
            weights=tuple(float(x) for x in w),
            holdout_rungs=holdout_rungs,
            holdout_mine=tuple(hmine), holdout_theirs=tuple(htheirs),
            flow_draws=len(draws), flow_ens_margin=f_ens,
            flow_centre_margin=f_ctr, flow_levels=tuple(draws),
            softwin=softwin, holdout_softwin=holdout_softwin)

    def _select_rung_name(self):
        """The rung the metric names, or None. -> str|None.

        Both per-rung metrics (`margin:<rung>`, `softwin:<rung>:<tau>`) name
        one; the two whole-ladder ones come back as `None` and the callers
        below turn that into "read a headline". A prefix with nothing usable
        after it is a typo, not a metric, and `select_spec` says so.
        """
        return select_spec(self.cfg.select_metric).rung

    def _check_select_rung(self, names):
        """Refuse at startup a metric that names a rung this ladder lacks.

        Called from `_bind_rungs`, i.e. everywhere the ladder is (re)bound: at
        construction, after `--resume` restores an archetype set, and after
        `--rung-theta` appends its anchors. A metric pointing at a missing rung
        would otherwise raise at the *first measurement*, `--abs-every`
        generations in, which on this machine is minutes of a multi-hour run
        spent to learn about a typo. Same rule, same phrasing, as the
        `--rung-weight` check just above.

        `pending_rungs` is the one exception, and it is a construction-order
        artefact rather than a loophole: `scripts/train.py` has to build the
        Trainer before it can load an anchor's theta into the ladder, so an
        anchor named here is absent from `names` at construction and present at
        every later call.
        """
        name = self._select_rung_name()
        if name is None or name in names or name in tuple(self.pending_rungs):
            return
        raise ValueError(
            f"--select-metric {self.cfg.select_metric} names no such rung "
            f"({name}). This "
            f"run's ladder is {', '.join(names) or '(empty)'}. The rung has to "
            f"be one this run actually plays -- `{K2F.RUNG_NAME}` needs "
            f"--kagg2-flow, `{KGF.RUNG_NAME}` needs --kaggle-flow, a "
            f"`{TPF.RUNG_PREFIX}*` needs its --tape-rung, an anchor "
            f"needs its --rung-theta.")

    def select_rung_index(self):
        """Index into the per-rung tuples of `AbsReport` for the metric's rung."""
        name = self._select_rung_name()
        names = list(self.archetype_names)
        self._check_select_rung(names)
        if name is None or name not in names:
            # Only reachable for a `pending_rungs` anchor that never arrived;
            # the ladder is final by the time anything scores.
            raise ValueError(
                f"--select-metric {self.cfg.select_metric}: the rung is not in "
                f"the ladder ({', '.join(names) or '(empty)'}).")
        return names.index(name)

    def selection_score(self, rep: AbsReport):
        """The one scalar `best_abs`, the champion and `_maybe_restart` read.

        `None` means "not selectable": the candidate is under
        `select_coin_floor` and cannot be promoted whatever it scores. The
        floor is the guard against the mutual-destruction optimum -- a policy
        that buys margin by burning the market down reaches a *high* score on a
        *low* absolute, and in a Bradley-Terry field of thirty agents a 72k
        denial policy loses to every third one that farms 130k in a quiet game.
        It is a floor rather than a term because the failure is a region, not a
        slope. It reads `rep.coins` under every metric, because what it guards
        against is a *coin* collapse however the candidate was ranked.

        `coins` is the default and is what every checkpoint on disk was
        selected by. `score` is the weighted expected tournament score, which
        is what `GOAL.md` actually asks for -- and which only starts to vary
        once the ladder holds a rung the policy loses to.

        `softwin:<rung>:<tau>` is the same rung read through a tanh: the mean
        over games of `tanh((own - theirs) / tau)`, a smooth win rate in
        [-1, +1]. It selects for *winning more games* rather than for winning
        by more the ones already won -- a margin is unbounded, so one blowout
        pair can carry a reading that lost the other fifteen, which is the
        shape a Bradley-Terry field scores as a loss. `tau` is the width in
        coins over which it interpolates between the two: at tau = 3000 a 3k
        margin reads 0.76 and a 30k one reads 1.00, so the second 27k buys
        almost nothing. It is a tanh rather than a hard win rate because a
        step function has no gradient for the record to climb.

        `margin:<rung>` is one rung's mean (own - theirs), and it exists
        because the rung-weighted coin total does not measure what the run is
        for. Across the five thetas ever scored against kagg2 on the real
        engine, the coin total this used to promote on has **zero** rank
        correlation with the real margin (Spearman 0.00), while the in-sim
        margin on the `kagg2_flow` rung alone ranks the same five perfectly
        (Spearman +1.00, level bias under ~1.1k, slope ~0.6-0.8). Every record
        both flow lineages promoted earned more coins in-sim and lost by more
        on the real engine: the yardstick was rewarding the wrong half of the
        game. A margin can be negative, which is why `NO_BEST` is `-inf`.
        """
        cfg = self.cfg
        spec = select_spec(cfg.select_metric)
        if cfg.select_coin_floor > 0 and rep.coins < cfg.select_coin_floor:
            return None
        if spec.kind == "score":
            return rep.score
        if spec.kind == "coins":
            return rep.coins
        i = self.select_rung_index()
        if spec.kind == "softwin":
            if i >= len(rep.softwin):
                # A report measured under a different metric: `softwin` is
                # only filled when something selects on it. Falling back to
                # the margin would silently select on the other quantity.
                raise ValueError(
                    f"select_metric {cfg.select_metric!r}: this report carries "
                    f"no softwin column -- it was measured under another "
                    f"metric.")
            return rep.softwin[i]
        return rep.mine[i] - rep.theirs[i]

    def holdout_selection_score(self, rep: AbsReport):
        """`selection_score`'s number, on the half of the seeds nothing selects on.

        It mirrors `--select-metric` rather than always reading coins, because
        the question `--best-gate both` asks is "did *this* improvement survive
        unseen games" -- and an improvement measured in one rung's margin is
        not answered by a coin count over eleven. There is no
        `select_coin_floor` here: the floor is a rule about which candidates may
        be promoted at all, and `selection_score` has already applied it by the
        time this is compared to anything.
        """
        cfg = self.cfg
        spec = select_spec(cfg.select_metric)
        if spec.kind == "score":
            return rep.holdout_score
        if spec.kind == "coins":
            return rep.holdout
        i = self.select_rung_index()
        if spec.kind == "softwin":
            # 0.0 for a report with no holdout half, by the same rule the
            # margin twin below applies.
            return (rep.holdout_softwin[i]
                    if i < len(rep.holdout_softwin) else 0.0)
        if i >= len(rep.holdout_mine):
            # A report from an `abs_pairs` too small to leave a holdout half,
            # or one built before the per-rung holdout existed. 0.0 is what
            # `holdout` itself reports there.
            return 0.0
        return rep.holdout_mine[i] - rep.holdout_theirs[i]

    def _accept_best(self, sel, hold) -> bool:
        """Does this measurement replace the `best_abs` record?

        `best_abs` is a **max over a noisy sequence** on 32 fixed seeds, so the
        record is biased upward by however far the luckiest reading of the run
        happened to land: flow2's record at gen 2230 read 133,162 on the
        selection half against 129,222 on the holdout (-3,940), where an
        ordinary reading nearby was -1,033. The ~3k difference between those
        two gaps is the seed luck the max selected for, and `best_abs.npy` --
        the file `--promote` ships -- is the theta that got it.

        Two knobs against that, both inert at their defaults so an unflagged
        run is the run that came before them:

        * `--best-margin` makes the record cost something to take, so a reading
          that only beat it by noise does not;
        * `--best-gate both` additionally requires the holdout half not to fall.
          A lucky selection-half draw says nothing about the holdout seeds, so
          a candidate whose sel is up while its hold is down is the signature
          of exactly the reading this is here to refuse.

        `sel is None` is a candidate `select_coin_floor` blocked outright; it
        can never take the record, whatever the holdout says.

        Under `--abs-select all` there is no holdout ratchet at all: `sel` is
        then read on every fixed pair, `hold` is a subset of it, and
        `_check_abs_select` has already refused `--best-gate both` rather than
        let the gate ask a question it cannot answer. `--best-margin` still
        applies, and is the knob that remains against a lucky reading -- on 64
        pairs instead of 32 the reading is about sqrt(2) less lucky to begin
        with.
        """
        cfg = self.cfg
        if cfg.best_gate not in ("sel", "both"):
            raise ValueError(f"best_gate {cfg.best_gate!r}: "
                             f"expected 'sel' or 'both'")
        if sel is None or sel <= self.best_abs + float(cfg.best_margin):
            return False
        return cfg.best_gate != "both" or hold >= self.best_hold

    def absolute_eval(self, theta):
        """(mean own coins, win rate) on the selection seeds. See `absolute_report`."""
        rep = self.absolute_report(theta)
        return rep.coins, rep.win

    def _snapshot(self, words, tables):
        """Freeze the current theta into the ladder.

        On overflow, drop the rung the current policy beats most easily rather
        than the oldest one. Recency-only eviction discards exactly the
        opponents that still pose a problem, which is what lets self-play go in
        circles; keeping the hard ones turns the ladder into a ratchet.
        """
        self.pool.append(self.theta)
        if len(self.pool) > self.cfg.pool_size:
            wins = self._versus_pool(self.theta, words, tables)
            # Never evict the original anchor: it is the one rung guaranteed not
            # to have drifted along with the population.
            wins[0] = -1.0
            self.pool.pop(int(np.argmax(wins)))

    def _measure_champion(self, rep: AbsReport):
        """Track the best parent seen, by `selection_score` (coins by default).

        ES on a self-play objective is not monotone, so the last iterate is not
        reliably the best one.

        The rule used to be mean win rate over the ladder, and both the
        incumbent and the challenger had to be re-scored every time because the
        ladder kept changing underneath them. That rule is gone: measured over a
        13 h run it correlated -0.17 with absolute strength, i.e. it was
        selecting against the thing worth having. The yardstick is now fixed --
        the same archetypes on the same seeds, in the same market -- so an
        incumbent's score stays valid and only the challenger needs playing.

        This deliberately makes `champion` and `best_abs_theta` the *same*
        selection rule, differing only in schedule (`champ_every` against every
        measurement taken). The agreement is the fix, not a redundancy: the two
        used to be selected on rules that correlated -0.17, so which of
        `champion.npy` and `best_abs.npy` an operator pointed an eval script at
        decided what they measured. `--promote` ships `best_abs_theta`.

        Which *number* that is now follows `--select-metric`, through the same
        `selection_score` `best_abs` uses -- so the two still cannot come apart,
        which was the whole point of making them agree.
        """
        sel = self.selection_score(rep)
        if sel is not None and sel >= self.champion_score:
            self.champion, self.champion_score = self.theta, sel
        self.history.append((self.t, rep.coins, self.champion_score))
        return self.champion_score
