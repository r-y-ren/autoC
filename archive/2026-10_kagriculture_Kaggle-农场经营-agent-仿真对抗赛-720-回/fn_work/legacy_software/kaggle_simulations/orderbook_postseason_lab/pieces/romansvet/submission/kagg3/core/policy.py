"""Shared per-product encoder + global head (GOAL.md's architecture).

    score_p = f(product_features_p  (+)  global_context)   for each of 9 products
              36 -> 64 -> 2,  weights SHARED across all products
    global    24 -> 32 -> 18

Sharing the encoder is what makes the market randomisation bind: the network has
to *read* base / T / above_target off its inputs rather than memorise the default
market table, which a monolithic net would do.

Deviation from GOAL.md: the encoder emits **two** scores per product, not one --
a grow score and a sell score. One scalar cannot rank both "what is worth
planting" and "what is worth liquidating today"; those genuinely disagree
(a product whose price has collapsed is a bad sell and may still be a fine
grow, and vice versa). That takes the total from 3,827 to 3,892 parameters,
which changes nothing about ES: the perturbation is isotropic and O(n).

A third head block (`g3`/`gb3`, 32 -> 9) once emitted labour-priority weights.
Nothing decodes it since PLANNER_V3_1 1.6 made labour an admit-then-route
decision over coin values; it is kept so the parameter layout is stable, and
`brain.decide` ignores it.

The sell head adds a per-product price gate (`w3`/`b3`, 64 -> 1 off the shared
encoder), which PLANNER_V3_1 1.2 re-typed into the timing pressure `press`, and a
global lot count (`g4`/`gb4`, 32 -> 1). Nothing decodes the lot count since
PLANNER_V3_1 1.2 made the lot split a reservation-value allocation; it is kept
so the parameter layout is stable, and `brain.decide` ignores it.

The unblock genes (`g5`/`gb5`, 32 -> 3) add a small `aux` output block read by
`brain.decide` for decisions that used to be hard-wired. Decodes to zero
(inert) at zero. Column 0 carried `fert_buy` until PLANNER_V3_1 0.11 valued
fertilizer instead; the slot stays in the layout so every checkpoint keeps its
shape, and nothing decodes it.

The residual-drain genes (`dh`, 2 -> 64, and `ds`, 2 -> 2) carry the two
per-product columns `brain.residual_drain` computes -- the town's remaining
appetite for a product minus the supply both seats have already committed to
it. They are a second *input* block, not a second head: widening `prod_feat`
would widen `w1` and move every later block, so no existing checkpoint would
decode. `dh` adds into the shared encoder's pre-activation, so the drain can
interact with price, base and the board through the trained hidden units; `ds`
is a direct linear path onto the grow and sell scores, so product mix can read
it without routing through a tanh an archetype may have saturated.

The development genes (`g6`/`gb6`, 32 -> 2) carry `compact` -- how tightly the
day clusters its new plantings and structures around the shed-access spawn --
and `dev_weight`, a multiplier on what a planting or a placement is worth to
the labour router. Both decode to a no-op at zero (`compact = 0` reproduces
the plain sweep rank bit for bit, `dev_weight = GROW_ONE` is x1), so every
theta trained before them is a prefix that decodes exactly as it did. Total
now 4,584.

The market-saturation gene (`g7`/`gb7`, 32 -> 1) biases the plant mix's
absorption gate (`brain.decide`). It is the one appended block whose zero
decode is **not** a no-op: `tanh(0) == 0` leaves the gate at "plant only into
town appetite nobody has claimed", which is the shipped default and the fix
for melon over-planting (2026-08-26, measured on the real engine). Every
incumbent checkpoint still *unpacks*; it decodes a different plant mix on the
days its market is already oversupplied, deliberately. Total now 4,617.

The crew and herd-mix genes (`g8`/`gb8`, 32 -> 4) are the two things a
constant theta could not say before 2026-08-28, and they are both *biases on a
decision the planner already makes*, not new decisions:

* `crew[0]` is `hire_bias`, coins per hand added to the hire enumeration's
  gain (`plan` section 1.5). The crew size is not a gene -- it is the `h` whose
  admitted task value less `HIRE_BILLS[h]` is largest -- and nothing else in
  the genome reaches it except by making the *work* worth more (`dev`,
  `free_urgency`, `dev_weight`). `head[0]`, the old `n_hire`, is not available
  for this: it is a `DEAD_HEAD` slot, so `g2[:, 0]` holds whatever it held when
  masking began (0.51 in `artifacts/theta.npy`), and a gene placed there would
  decode differently for every incumbent checkpoint.
* `crew[1:4]` is `animal_mix`, a logit added to the herd want's softmax over
  (GOOSE, COW, SHEEP). `brain.decide` read *one* per-product grow score for
  both halves of the herd decision -- the want and the planner's own valuation
  (`_unit_ratio`, clipped at 4x) -- so a want of 2:1 sheep:cow was unreachable:
  at any separation big enough to move the want both scores are still past the
  clip, both animals are worth 4x, and the cheaper cow takes the pasture. This
  block moves the want and leaves the valuation alone.

Both decode to exactly 0 at zero, so every theta trained before them is a
prefix that decodes byte for byte as it did (`tests/test_genome_retype.py`, and
the pinned ladder table in `tests/test_archetype_ladder.py`). 132 params,
4,617 -> 4,749.

The hire-bias day buckets (`g9`/`gb9`, 32 -> 3) let the crew gene read the
calendar. `hire_bias` was one number for the whole season and the Kaggle
field's labour ramp is not -- the modal opponent fields 3-4 hands on day 5 and
14 by day 10 -- and a constant bias big enough for the late crew buys the
*cheap early* hands first (`es/archetypes.py`, the `wheat_clone` v2 note). The
gene is now four biases indexed by the day, `brain.HIRE_BIAS_BUCKETS` naming
the edges (days 0-5, 6-10, 11-20, 21+). Bucket 0 is the old `crew[0]`; this
block carries buckets 1..3.

Appended rather than widened into `g8`: the block is stored row-major, so a
fifth column would move every weight after the first row and no checkpoint on
disk would survive it. Its zero decode is also *not* the compatible one, and
that is the one place this layout does more than pad -- `unpack` **copies**
`g8[:, 0]` into all three columns when it pads a shorter theta, so a genome
trained when `hire_bias` was one number for the season keeps that number on
every day of it. A theta already this long says what it says. 99 params,
4,749 -> 4,848.

The crew-ramp genes (`g10`/`gb10`, 32 -> 4) are the structural answer to the
loss signature the Kaggle replays all share: the opponent reaches ~12 hired
hands and ~9k cash by day 10 while we hold ~6 hands and ~3.3k, because the
early purse went on animals and coops. `hire_bias` cannot re-order that -- it
nudges the hire enumeration's gain by a constant per hand and says nothing
about *when* the crew has to exist or what has to wait for it. This block says
both:

* `ramp[0:3]` is a crew **target** as a function of the day -- a logistic with
  a height (`brain.CREW_TARGET_MAX` hands), a midpoint day and a steepness.
  `plan` 1.5 adds `CREW_TARGET_PUSH` coins to every candidate hand up to that
  target, which is above the dearest marginal fib bill the enumeration can
  reach, so the argmax lands on the target whenever the purse can pay for it.
* `ramp[3]` is the deferral: while the day's crew is *under* the target, the
  animal candidate values and the structure builds are scaled by
  `(DEFER_ONE - defer) / DEFER_ONE`, so the coins the crew needs are not spent
  on a pasture first. Saturated it takes the animal channel to zero until the
  ramp is met; at zero it is exactly x1.

Inert at zero by construction and in integers: `relu(tanh(0)) == 0` makes the
target height exactly 0.0 hands, so `target == 0`, `min(h, 0) == 0` adds `0`
to the enumerated gain, and `crew < 0` is false on every day -- which pins the
deferral scale at `DEFER_ONE` and every scaled quantity at `x * DEFER_ONE //
DEFER_ONE == x`. 132 params, 4,848 -> 4,980.

The production-forecast genes (`fh`, 8 -> 64, and `fs`, 8 -> 2) are the second
*input* block, laid out exactly like `dh`/`ds`. Nothing the network saw carried
production **timing**: `prod_feat` columns 7 and 8 count the tiles producing
each product on either board, so eight strawberry tiles read the same whether
they yield tomorrow or in a week, and a planting date could move without a
single feature moving (2026-09-08 plateau diagnosis, section 4). The block
carries `brain.production_forecast` -- what each board can harvest today and
what it adds over the next 1, 3 and 7 days, ours and the opponent's, from
public tile state only. Inert at zero: the two extra matmul products are
exactly 0.0 and `x + 0.0 == x`, so every theta trained under the 4,980 layout
is a prefix that decodes bit for bit as it did. 528 params, 4,980 -> 5,508.

The global product residual (`gp`, 27 -> 32) is the first block to run the
other way: every block above it feeds the per-product encoder, and the head has
never had a path back *from* it. `gh = tanh(glob_feat @ g1 + gb1)` was all the
land bias, dev_frac, animal_share, the plant-mix sharpness, the saturation
gate, the hire bias and the crew ramp were allowed to know, and `glob_feat`
carries exactly two product aggregates -- the shed total and the *mean* price
ratio -- with nothing product-identified in it at all. So the head could not
tell "melon is glutted and wool is scarce" from its mirror image; both read as
the same mean. Measured over 1,440 real g350 decisions against the band6 tapes,
the best linear map from `glob_feat` leaves 27 % of the grow scores' variance,
55 % of `press`' and 53 % of the animal-versus-crop grow contrast unexplained,
and among decision pairs whose `glob_feat` agrees to four decimals 18 % put the
best grow score on a different product while the head emitted a bit-identical
`animal_share`.

`gp` reads the flattened per-product summary -- (grow, sell, press) x 9,
`PROD_SUMMARY_SCALE` putting the three channels on one scale -- onto the global
hidden width and adds it to that pre-activation. Flattened rather than pooled:
a permutation-invariant pool is the summary the head effectively already has
(the mean over products of the encoder hidden is 96 % linearly predictable from
`glob_feat`), and it is the *identity* of the glutted product that `glob_feat`
cannot say. One matmul off an already-nonzero quantity rather than a zero-init
bottleneck, which ES cannot start: two zero factors make each other's gradient
zero. No bias -- `gb1` is already this pre-activation's. Inert at zero in the
same sense as `fh`/`fs`. 864 params, 5,508 -> 6,372.

The forward-admit gene (`g11`/`gb11`, 32 -> 1) is the *other* half of the same
loss: the ramp says how many hands the day should end with, and this says how
far ahead the hire enumeration is allowed to look when it prices them. 1.5
scores every candidate crew against the task set `_derive` emits **today**, and
a field of one-time crops outside their bonus window emits nothing at all --
`spec.CROP_WINDOW_START[I_MELON]` is 6, so the twelve melon tiles of the
recorded top-tier opening are silent through day 5 and the argmax reads an
empty board. `macro.forward_days` widens the projection the *scan* reads (and
only the scan -- the route, the admission and the market row still walk today's
real work) by that many days.

A horizon rather than a switch, because the measurement says the switch loses:
as a fixed `FORWARD_ADMIT_ON` at three days it is -9,224 coins a game on band6,
since a theta's `hire_bias` and crew ramp are already priced for today-only
admission. What the block buys is the ability to move the horizon *with* the
rest of the head instead of against it.

Inert at zero by construction: the decode is `round(FWD_DAYS_GAIN * z)`
clipped to `[0, FWD_DAYS_MAX]`, which is exactly 0 at `z = 0`, and a zero
horizon makes `age + 0 >= window` the mask that was already there -- so `plan`
skips the projected pass outright and every shipped theta plans byte for byte
as it did. The gain is sized off the ES step and not off the logit: the
logistic the block shipped with (`round(6 * sigmoid(z - 4))`) is inert at zero
*and* inert one sigma away from it -- 0 of 512 members decoded a day at sigma
0.02 -- which is a gene the search cannot select on. See `brain.FWD_DAYS_GAIN`
for the measurement. 33 params, 6,372 -> 6,405.

The forward-value genes (`fv`, 12 -> 32) are `gp`'s twin one input over: a
second path into the global head's pre-activation, carrying what `gh` could
never read. `glob_feat` says how many tiles are planted and how much cash is
in hand; nothing in it says **when the board pays**. The forced-opening
diagnostic is that hole measured -- a twelve-melon day-0 board emits no task
for six days (`spec.CROP_WINDOW_START[I_MELON]` is 6), so the head prices
hands, land and the animal share against an empty task set and hires nobody,
while the same head on a wheat board that pays tomorrow reads an identical
`glob_feat`.

`brain.forward_value` is the feature: per seat and over horizons 1, 3 and 7
days, the units the standing board will produce and what they are worth at
today's quote. Both seats, because the opponent's tiles, clocks and standing
yield are public (`PolicyObs`) and the melon race is a race. Both channels,
because coins are the head's other resource axis and a unit of wheat and a
unit of melon are a factor of ten apart.

Deliberately the *global head* and not the encoder: the per-product half of
this projection already reaches the encoder through `fh`/`fs`, and nothing
there reduces to a board total -- `w2` maps the shared hidden layer to one
grow and one sell score per product and the head never sees either.

No bias, for `gp`'s reason: `gb1` is already this pre-activation's. Appended
and inert at zero in the same sense -- the extra matmul is exactly 0.0 and
`x + 0.0 == x` for every finite float, so a theta trained under the 6,405
layout is a prefix that decodes bit for bit as it did
(`tests/test_forward_value.py`). 384 params, 6,405 -> 6,789.

The market-momentum genes (`mh`, 1 -> 64, and `ms`, 1 -> 2) carry the
previous-to-current dawn market draw for each product. They mirror `dh`/`ds`
without widening the original product input: `mh` adds to the encoder
pre-activation and `ms` to its two scores. Both blocks are appended and zero
initialized, so a 6,789-coordinate theta is an exact prefix and the new input
is inert until these coordinates move. 66 params, 6,789 -> 6,855.

The crop-mix readout (`cm`, 32 -> 5, and `cb`, 5) adds signed log-share
preferences to the crop allocation, after grow-score sharpness and before
maturity and absorption masks. Like the animal-mix readout, it separates
desired proportions from purchase valuations. Both blocks start at zero;
earlier layouts retain their original decode branch and padded zero tails
must preserve it across backends. 165 params, 6,855 -> 7,020.

The crop-day bias (`cd`, 5 x 9) makes that readout day-indexed: one log-share
bias per crop per day bucket, added to the same crop logits behind
`brain.CROP_DAY_ON`. A season-constant mixture cannot hold a *block* crop
programme (pure wheat on day 2, pure strawberry on day 3 -- the ymg_aq
opening), which is what the macro fit measured when it dumped all of the
ymg_aq mass on wheat. Zero initialized and appended, so a 7,020-coordinate
theta is an exact prefix. 45 params, 7,020 -> 7,065.

Of `head`'s 18 outputs five are decoded (`DEAD_HEAD` names the rest):
`head[1]` the land bias in coins, `head[2]` the animal-mix sharpness, `head[5]`
dev_frac, `head[6]` animal_share, `head[7]` the plant-mix sharpness.
`live_mask` turns the dead slots into an ES mask. `head[2]` was masked while
the day bought one animal kind; the mixed herd gives it something to sharpen
again, and it costs no new parameter block.

Deterministic by construction: no sampling anywhere, argmax ties break to the
lowest index, and every quantity is floored to an integer.
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np

from .. import spec

N_PROD_FEAT = 12
N_GLOBAL_FEAT = 24
N_ENC_IN = N_PROD_FEAT + N_GLOBAL_FEAT      # 36
N_ENC_HID = 64
N_ENC_OUT = 2                               # (grow, sell)
N_HEAD_HID = 32
N_HEAD_OUT = 18
N_PRIO_OUT = 9                              # dead (was the labour-priority weights)
N_AUX_OUT = 3            # [0] dead (was fert_buy), land_afford, free_urgency
#: Per-product residual-drain columns: (gap, share). See `brain.residual_drain`.
N_DRAIN_FEAT = 2
#: Development genes: (compact, dev_weight). See `brain.decide`.
N_DEV_OUT = 2
#: Market-saturation gene: one global bias on the plant mix's absorption gate.
#: See `brain.decide`.
N_SAT_OUT = 1
#: Crew and herd-mix genes: `[hire_bias, animal_mix x N_ANIMALS]`. One block
#: rather than two because both are biases the *head* emits from the same
#: hidden layer and neither is worth a 32-wide matmul of its own.
N_CREW_OUT = 1 + spec.N_ANIMALS
#: Day buckets the hire bias is indexed by; `brain.HIRE_BIAS_BUCKETS` holds the
#: edges and `brain.decide` does the selection. Bucket 0 is `crew[0]` -- the
#: gene as it shipped -- and `g9`/`gb9` carries buckets 1..3, which is what
#: makes an older theta a prefix of this layout.
N_HIRE_BUCKETS = 4
N_HIRE_EXTRA = N_HIRE_BUCKETS - 1
#: Day buckets the crop-day log-share bias (`cd`) is indexed by;
#: `brain.CROP_DAY_BUCKETS` holds the edges and `brain.decide` does the
#: selection, exactly as it does for the hire bias. Nine and not the hire
#: bias's four: the block crop programmes the top five run (MACRO-EXTRACT
#: section 3 -- ymg_aq plants pure wheat on day 2 and pure strawberry on day 3)
#: change from one day to the next inside the opening, and any bucket that
#: holds both days can only average them. The hire edges (6, 11, 21) are a
#: subset of these, so the hire scheme is this one with coordinates tied.
N_CROP_DAY_BUCKETS = 9
#: Crew-ramp genes: `[target height, ramp midpoint day, ramp steepness,
#: animal deferral]`. One block rather than two for the same reason `g8` is
#: one: all four are biases the head emits off the same hidden layer, they are
#: read by the same decision (how fast the crew ramps and what waits for it),
#: and neither half is worth a 32-wide matmul of its own.
N_CREW_RAMP_OUT = 4
#: Per-product production-forecast columns. See `brain.production_forecast`:
#: (own ready now, own +1d, own +3d, own +7d, opp ready now, opp +1d, opp +3d,
#: opp +7d). A second *input* block for the same reason `dh`/`ds` is one --
#: widening `prod_feat` would widen `w1` and move every later block.
N_FCAST_FEAT = 8
#: Channels of the product summary the global head reads: the encoder's two
#: scores (grow, sell) and its timing pressure (`press`, the `w3`/`b3` gate).
#: Those three *are* the per-product encoding as anything downstream sees it --
#: `brain.decide` decodes nothing else per product -- so they are the compact,
#: product-identified summary the global head was missing.
N_SUMMARY_CH = N_ENC_OUT + 1
#: The flattened summary, product-major: `[grow_0, sell_0, press_0, grow_1,
#: ...]`. Flattened rather than pooled deliberately -- see `gp` in `SHAPES`.
N_PROD_SUMMARY = spec.N_PRODUCTS * N_SUMMARY_CH
#: Per-channel divisor of that summary, so one isotropic ES step moves each
#: channel's contribution to the global pre-activation by about the same
#: amount. The three channels are trained quantities on very different scales
#: -- measured over 1,440 real g350 decisions against the band6 tapes, rms
#: grow 1.16, sell 4.58, press 0.83 -- and an unscaled path would let `sell`
#: dominate the block's whole perturbation budget. Fixed constants, not a
#: running normalisation: a normaliser that moved with the state would make the
#: block's decode depend on the batch it was in.
PROD_SUMMARY_SCALE = np.array([1.0, 4.0, 1.0], np.float32)
#: Forward-admit horizon gene: one logit the hire scan's projection window is
#: decoded from, `[0, brain.FWD_DAYS_MAX]` days. See `brain.decide` and
#: `plan.FORWARD_ADMIT_ON`. One output, so one column and one bias -- the
#: horizon is a single global number the day states, not a per-product one.
N_FWD_OUT = 1

#: Columns in the switch-gene block: one logit per `plan.SWITCH_GENES` entry,
#: in that tuple's order, which is a layout and may never be reordered or
#: renumbered -- column i belongs to the switch named i for the life of every
#: theta trained under it. Widening the block is an append like any other (a
#: new name at the *end* of the tuple and this count raised), and `plan` asserts
#: the two agree at import.
#: 2026-09-17: widened 10 -> 11 when `plan.ENDROUTE_ON` shipped -- the block is
#: the full catalogue of shipped behaviour switches at launch time, so a
#: from-scratch ES can find the switch vector itself instead of being handed
#: one [USER 2026-09-17].  Widening shifts `g12`, so a theta already written
#: under the 7,428 layout is NOT a prefix of this one and must be remapped;
#: every theta at or below 7,065 (the shipped 6,789 champion included) is.
#: 2026-09-17: widened 11 -> 13 when PUMPCLIP shipped -- `plan.OPEN_PUMP_ON`
#: (True -> False) and `plan.CLIP_CAP_ON` (False -> True) are both a shipped
#: value now, so by the same catalogue rule both are columns.  `g12` shifts
#: again, 7,428 -> 7,494, and the layout 7,461 -> 7,527; the 7,065 prefix rule
#: is unchanged, so the shipped 6,789 champion still pads to it with the whole
#: block zero, which decodes to exactly these new defaults.
#: 2026-09-18: widened 13 -> 15 when PES shipped -- `plan.ENDROUTE2_ON` and
#: `plan.ENDROUTE2_SPLIT_ON` (both False -> True) are shipped values now, so by
#: the same catalogue rule both are columns.  `g12` shifts again, 7,494 ->
#: 7,560, and the layout 7,527 -> 7,593; the 7,065 prefix rule is unchanged, so
#: the shipped 6,789 champion still pads to it with the whole block zero, which
#: decodes to exactly these new defaults.
#: 2026-09-18: widened 15 -> 16 when ESR shipped -- `plan.ENDROUTE_ROW2_ON`
#: (False -> True) is a shipped value now, so by the same catalogue rule it is
#: a column.  The SAME ship moves `plan.OPEN_PUMP_ON` back to True and
#: `plan.CLIP_CAP_ON` back to False; both KEEP their columns (11 and 12), and
#: because a zero gene decodes to the module default whatever that default
#: currently is, the block still decodes to exactly the shipped vector.  `g12`
#: shifts 7,560 -> 7,593 and the layout 7,593 -> 7,626; the 7,065 prefix rule
#: is unchanged, so the shipped 6,789 champion still pads to it with the whole
#: block zero.
#: 2026-09-18: widened 16 -> 17 when WIDEPICK shipped -- `plan.WIDE_PICK_ON`
#: (False -> True) is a shipped value now, so by the same catalogue rule it is
#: a column.  `g12` shifts 7,593 -> 7,626 and the layout 7,626 -> 7,659; the
#: 7,065 prefix rule is unchanged, so the shipped 6,789 champion still pads to
#: it with the whole block zero, which decodes to exactly these new defaults.
#: 2026-09-18: widened 17 -> 18 for `plan.WIDE_PICK_FREE_ON` (WIDEPICK2), the
#: free-first ordering of WIDE_PICK's turn-1 kind -- same catalogue rule, same
#: append-at-the-end.  `g12` shifts 7,626 -> 7,659 and the layout 7,659 ->
#: 7,692; the 7,065 prefix rule is unchanged, so the shipped 6,789 champion
#: still pads to it with the whole block zero.
#: 2026-09-21: widened 18 -> 19 for `plan.MELONVETO_POST_ON`, appended so its
#: zero gene is the default-OFF arm and every preceding switch keeps its index.
#: 2026-09-22: widened 20 -> 21 for shipped `plan.OVERFLOW_GUARD_ON`.
N_SWITCH_GENES = 21
#: Fertilizer-timing look-ahead outputs [g12]: one logit, decoded to a day
#: count by `brain.FERT_DEFER_GAIN`.
N_FT_OUT = 1
#: Forward-value columns the global head reads. `brain.forward_value`:
#: `[own units +1d/+3d/+7d, own coins +1d/+3d/+7d, opp units x3, opp coins
#: x3]`. Two seats x `len(brain.FWDVAL_HORIZONS)` horizons x (units, coins).
N_FWDVAL_SEATS = 2
N_FWDVAL_CH = 2                 # units, coins
N_FWDVAL_FEAT = N_FWDVAL_SEATS * N_FWDVAL_CH * 3
N_MOMENTUM_FEAT = 1

SHAPES = [
    ("w1", (N_ENC_IN, N_ENC_HID)), ("b1", (N_ENC_HID,)),
    ("w2", (N_ENC_HID, N_ENC_OUT)), ("b2", (N_ENC_OUT,)),
    ("g1", (N_GLOBAL_FEAT, N_HEAD_HID)), ("gb1", (N_HEAD_HID,)),
    ("g2", (N_HEAD_HID, N_HEAD_OUT)), ("gb2", (N_HEAD_OUT,)),
    # Appended, not interleaved: every theta trained before this block is a
    # prefix of the layout and unpacks with it zeroed. Keep new blocks at the
    # end for the same reason.
    ("g3", (N_HEAD_HID, N_PRIO_OUT)), ("gb3", (N_PRIO_OUT,)),
    # Sell head: a per-product price gate off the shared encoder's hidden layer
    # and a global lot count off the head's hidden layer.
    ("w3", (N_ENC_HID, 1)), ("b3", (1,)),
    ("g4", (N_HEAD_HID, 1)), ("gb4", (1,)),
    # Unblock genes (2026-08-23). Appended for the same reason as g3/g4: every
    # earlier theta is a prefix and unpacks with this block zeroed. NOT placed
    # in head[13..17] -- those outputs were always live parameters and carry
    # trained noise in every checkpoint.
    ("g5", (N_HEAD_HID, N_AUX_OUT)), ("gb5", (N_AUX_OUT,)),
    # Residual town drain (2026-08-26). Appended for the same reason as every
    # block above it: each earlier theta is a prefix and unpacks with this one
    # zeroed, and a zero block contributes exactly 0.0 to the sums it enters,
    # so every incumbent checkpoint decodes byte for byte as it did.
    #
    # Deliberately NOT named `w4`/`b4`: `docs/superpowers/plans/
    # 2026-08-26-drain-aware-reservation.md` section 3 reserves those names for
    # its (gated) patience head, and two blocks sharing a name in a layout that
    # can only ever be appended to is a checkpoint-shredding class of mistake.
    ("dh", (N_DRAIN_FEAT, N_ENC_HID)), ("ds", (N_DRAIN_FEAT, N_ENC_OUT)),
    # Development locality and weight (2026-08-26). Appended after `dh`/`ds`
    # for the same reason as every block above them, and deliberately NOT
    # placed in a `DEAD_HEAD` slot: a masked coordinate holds whatever it held
    # when masking began, which on a resumed or trunk-warmed run is not zero,
    # so a "dead" slot cannot promise a decode of exactly zero -- and `head[2]`
    # came back for the animal mix anyway. 66 params, 4,518 -> 4,584.
    ("g6", (N_HEAD_HID, N_DEV_OUT)), ("gb6", (N_DEV_OUT,)),
    # Market-saturation bias on the plant mix (2026-08-26). Appended for the
    # same reason as every block above it: each earlier theta is a prefix and
    # unpacks with this one zeroed, and `tanh(0) == 0` makes the decoded bias
    # exactly 0.0, which is the shipped default rather than a no-op -- see
    # `brain.decide`'s `absorb` gate. 33 params, 4,584 -> 4,617.
    ("g7", (N_HEAD_HID, N_SAT_OUT)), ("gb7", (N_SAT_OUT,)),
    # Crew size and herd mix (2026-08-28). Appended for the same reason as
    # every block above it, and -- unlike `g7` -- genuinely inert at zero:
    # `tanh(0) == 0` makes `hire_bias` exactly 0 coins per hand, which the
    # enumeration adds as `0 * h`, and a zero `animal_mix` is added to the
    # want's logits, where `x + 0.0 == x`. 132 params, 4,617 -> 4,749.
    ("g8", (N_HEAD_HID, N_CREW_OUT)), ("gb8", (N_CREW_OUT,)),
    # Hire-bias day buckets 1..3 (2026-08-28). Bucket 0 stays `g8` column 0, so
    # every earlier theta is still a prefix -- but zero here is not what an
    # earlier theta *meant*, so `unpack` and `pad` copy that column into these
    # when they pad one. 99 params, 4,749 -> 4,848.
    ("g9", (N_HEAD_HID, N_HIRE_EXTRA)), ("gb9", (N_HIRE_EXTRA,)),
    # Crew-target ramp and early-spend deferral (2026-08-30). Appended for the
    # same reason as every block above it -- each earlier theta is a prefix and
    # unpacks with this one zeroed -- and, unlike `g7`/`g9`, genuinely inert at
    # zero: the decoded target is 0 hands, which adds `0` to 1.5's gain and
    # leaves the deferral scale at `plan.DEFER_ONE`, i.e. integer x1 on every
    # quantity it touches. 132 params, 4,848 -> 4,980.
    ("g10", (N_HEAD_HID, N_CREW_RAMP_OUT)), ("gb10", (N_CREW_RAMP_OUT,)),
    # Production forecast (2026-09-08). A second per-product *input* block, laid
    # out exactly like `dh`/`ds`: `fh` adds into the shared encoder's
    # pre-activation so timing can interact with price, drain and the board
    # through the trained hidden units, and `fs` is a direct linear path onto
    # the grow and sell scores so the mix can read it without routing through a
    # tanh an archetype may have saturated.
    #
    # Appended, and inert at zero in the strongest sense the layout has: the
    # two extra products are exactly 0.0 and `x + 0.0 == x` for every finite
    # float, so a theta trained under the 4,980 layout is a prefix that decodes
    # bit for bit as it did (`tests/test_forecast_feature.py`). 528 params,
    # 4,980 -> 5,508.
    ("fh", (N_FCAST_FEAT, N_ENC_HID)), ("fs", (N_FCAST_FEAT, N_ENC_OUT)),
    # The global head's product residual (2026-09-08). Every block above this
    # one feeds the *encoder*; the head has never had a path back from it, so
    # `gh = tanh(glob_feat @ g1 + gb1)` is everything dev_frac, animal_share,
    # the plant-mix sharpness, the land bias, the saturation gate, the hire
    # bias and the crew ramp are allowed to know. `glob_feat` carries exactly
    # two product aggregates -- the shed total and the *mean* price ratio --
    # plus the fertilizer and wheat shed counts, and nothing product-identified
    # at all: not the per-product market inventory, not the town's per-product
    # appetite, not the residual drain, not the forecast. Measured on 1,440
    # real g350 decisions the best linear map from `glob_feat` leaves 27 % of
    # the grow scores' variance, 55 % of `press`' and 53 % of the
    # animal-versus-crop grow contrast unexplained -- and among decision pairs
    # whose `glob_feat` agrees to four decimals, 18 % disagree on which product
    # is the best thing to plant while the head emits a bit-identical
    # `animal_share`.
    #
    # `gp` is that path: the flattened product summary onto the global hidden
    # width, added to the pre-activation. **Flattened, not pooled**: a pooled
    # (permutation-invariant) summary is the one the head already effectively
    # has -- the mean over products of the encoder hidden is 96 % linearly
    # predictable from `glob_feat` -- so summing over products would spend
    # 2,048 parameters to add 4 % of one signal. The identity of *which*
    # product is glutted is the part `glob_feat` cannot say, and a flattened
    # 27-wide read is what says it, for 864.
    #
    # One matmul off an already-nonzero quantity, deliberately: a zero-init
    # *bottleneck* (per-product projection then flatten) would be stationary
    # under ES -- both factors zero makes each one's gradient zero and the
    # antithetic pair sees only a sigma^2 term -- so the block would never
    # start learning. No bias of its own either: `gb1` is already the bias on
    # this pre-activation and a second one would be the same coordinate twice.
    #
    # Appended and inert at zero in the same sense as `fh`/`fs`: the extra
    # matmul is exactly 0.0 and `x + 0.0 == x` for every finite float, so a
    # theta trained under the 5,508 layout is a prefix that decodes bit for bit
    # as it did (`tests/test_global_product.py`). 864 params, 5,508 -> 6,372.
    ("gp", (N_PROD_SUMMARY, N_HEAD_HID)),
    # Forward-admit horizon (2026-09-09). Appended for the same reason as every
    # block above it -- each earlier theta is a prefix and unpacks with this one
    # zeroed -- and inert at zero by construction rather than by luck: the
    # decode is `round(FWD_DAYS_GAIN * z)` clipped to `[0, FWD_DAYS_MAX]`,
    # which is exactly 0 days at `z = 0`, and that is
    # `plan.FORWARD_ADMIT` switched off and the enumeration reading today's
    # task set alone. 33 params, 6,372 -> 6,405.
    ("g11", (N_HEAD_HID, N_FWD_OUT)), ("gb11", (N_FWD_OUT,)),
    # Forward value (2026-09-09). `gp`'s twin one input over: a second path
    # into the global head's pre-activation, carrying the one thing
    # `glob_feat` has never said -- *when* the standing board pays. The
    # per-product half of the same projection already reaches the encoder
    # (`fh`/`fs`), and nothing there reduces to a board total, so the head that
    # sizes the crew, the land bias, dev_frac and the animal share reads an
    # identical vector on a twelve-melon opening that emits nothing for six
    # days and on a wheat board that pays tomorrow.
    #
    # No bias, for `gp`'s reason: `gb1` is already this pre-activation's.
    # Appended and inert at zero in the same sense -- the extra matmul is
    # exactly 0.0 and `x + 0.0 == x` for every finite float, so a theta trained
    # under the 6,405 layout is a prefix that decodes bit for bit as it did
    # (`tests/test_forward_value.py`). 384 params, 6,405 -> 6,789.
    ("fv", (N_FWDVAL_FEAT, N_HEAD_HID)),
    # Previous-to-current dawn market draw, one normalized scalar per product.
    # Appended in two zero-initialized blocks so the old 6,789 coordinates keep
    # their offsets and a padded incumbent remains byte-exact.
    ("mh", (N_MOMENTUM_FEAT, N_ENC_HID)),
    ("ms", (N_MOMENTUM_FEAT, N_ENC_OUT)),
    # Crop log-share residual, analogous to g8's animal-mix outputs. This
    # separates desired proportions from the grow scores that also price
    # purchases. The zero tail preserves the incumbent's mixture; training
    # can name cm,cb alone without moving development, herd or valuations.
    ("cm", (N_HEAD_HID, spec.N_CROPS)), ("cb", (spec.N_CROPS,)),
    # Crop-day log-share bias: one number per crop per day bucket, read
    # straight off theta rather than out of the head. `cm`/`cb` is a *static*
    # preference -- one mixture for the whole season -- and MACRO-EXTRACT
    # section 4 item 5 measured what that costs: the least-squares fit of the
    # ymg_aq block programme onto `cb` dumps all mass on wheat, because a
    # day-2 pure-wheat block and a day-3 pure-strawberry block are the same
    # target to a season-constant bias. This block is the day index that fit
    # was missing. Not a matmul off `gh` for the same reason `cb` is not:
    # the quantity is a proportion, not a valuation, and the head already
    # reaches the mix through `cm`. Appended and zero initialized, so every
    # earlier theta is an exact prefix and decodes bit for bit as it did
    # (`tests/test_crop_day.py`). 45 params, 7,020 -> 7,065.
    ("cd", (spec.N_CROPS, N_CROP_DAY_BUCKETS)),
    # The switch-gene block (2026-09-16). `plan` carries ~66 module constants
    # `NAME_ON = True/False` that the lead flipped by hand and judged one at a
    # time; this is the subset the theta states instead. One logit per switch
    # off the global head, decoded in `brain.decide` to a *flip* against the
    # module default (`round(SWITCH_GAIN * z) > 0`), so the zero block is every
    # switch at the value it ships with -- inert in the same sense `g11` is,
    # and an earlier theta is a prefix that decodes bit for bit
    # (`tests/test_geneswitch.py`). Off `gh` rather than straight off theta
    # (`cd`'s pattern) deliberately: a switch that can read the board is a
    # strictly wider object than the constant it replaces -- the same lever the
    # lead could only set for the whole season. 330 params, 7,065 -> 7,395.
    ("sw", (N_HEAD_HID, N_SWITCH_GENES)), ("swb", (N_SWITCH_GENES,)),
    # Fertilizer-timing look-ahead (2026-09-16, FERTENGINE). One logit -> how
    # many days ahead `plan`'s fertilizer site looks before spending a unit
    # today: an application covers `day..day+2`, so the units it buys depend on
    # *when* in the tile's yield window it lands, and the ENG22 engine class
    # lands 92 % of its applications on the best day against our 29 %.
    # Appended for the reason every block above it is -- each earlier theta is
    # a prefix and unpacks with this one zeroed -- and inert at zero by
    # construction rather than by luck: the decode is
    # `round(FERT_DEFER_GAIN * z)` clipped to `[0, FERT_DEFER_MAX]`, exactly 0
    # days at `z = 0`, and a zero look-ahead is `fert_cand` as it always was
    # (`tests/test_fertengine.py`). 33 params, 7,395 -> 7,428.
    ("g12", (N_HEAD_HID, N_FT_OUT)), ("gb12", (N_FT_OUT,)),
]
N_PARAMS = sum(int(np.prod(s)) for _, s in SHAPES)
N_PARAMS_LEGACY = sum(int(np.prod(s)) for _, s in SHAPES[:8])   # 3,892


def offset(name: str) -> int:
    """Start index of parameter block `name` in the flat theta."""
    i = 0
    for n, shape in SHAPES:
        if n == name:
            return i
        i += int(np.prod(shape))
    raise KeyError(name)


#: The layout the hire-bias day buckets append to, 4,749. A theta this long or
#: shorter said one `hire_bias` for the whole season, so `unpack` and `pad`
#: carry that number into the buckets rather than zeroing them; a longer one
#: carries buckets of its own.
N_PARAMS_PRE_BUCKET = offset("g9")


class Params(NamedTuple):
    w1: object
    b1: object
    w2: object
    b2: object
    g1: object
    gb1: object
    g2: object
    gb2: object
    g3: object
    gb3: object
    w3: object
    b3: object
    g4: object
    gb4: object
    g5: object
    gb5: object
    dh: object
    ds: object
    g6: object
    gb6: object
    g7: object
    gb7: object
    g8: object
    gb8: object
    g9: object
    gb9: object
    g10: object
    gb10: object
    fh: object
    fs: object
    gp: object
    g11: object
    gb11: object
    fv: object
    mh: object
    ms: object
    cm: object
    cb: object
    cd: object
    sw: object
    swb: object
    g12: object
    gb12: object


def unpack(xp, theta) -> Params:
    """Flat vector -> weight tensors. Fixed order, so checkpoints are portable.

    A theta shorter than `N_PARAMS` is an older layout; the missing tail is
    zeros, so it behaves exactly as it did when it was trained -- with one
    block where zeros are *not* what it said. `g9`/`gb9` holds hire-bias
    buckets 1..3 and the theta that predates it carries one bias for the whole
    season in `g8` column 0, so the pad copies that column across the buckets
    rather than zeroing them. Every other appended block decodes to its own
    no-op at zero and needs nothing here.

    The copy is exact where it has to be and to a float32 ulp where it does
    not: buckets 1..3 are their own matmul, so a copied *column* is not a
    copied reduction and `gh @ g9` can differ from `gh @ g8[:, :1]` in the last
    bit. Every theta on disk when the buckets landed has a zero `g8` block --
    the gene is a bias there, or absent -- and a bias copies exactly, so the
    ulp is reachable only by a theta trained under the 4,749 layout, and only
    where `HIRE_BIAS_MAX * tanh(z)` sits within 1e-5 of an integer.

    The branch is on `theta.shape[0]`, which is static under `jax.jit`, so this
    traces to one program per layout rather than to a `where`.
    """
    legacy = theta.shape[0] <= N_PARAMS_PRE_BUCKET
    if theta.shape[0] < N_PARAMS:
        theta = xp.concatenate([theta, xp.zeros(N_PARAMS - theta.shape[0], theta.dtype)])
    out, i = [], 0
    for _, shape in SHAPES:
        n = int(np.prod(shape))
        out.append(theta[i:i + n].reshape(shape))
        i += n
    p = Params(*out)
    if legacy:
        p = p._replace(g9=xp.broadcast_to(p.g8[:, :1], p.g9.shape),
                       gb9=xp.broadcast_to(p.gb8[:1], p.gb9.shape))
    return p


def pad(arr: np.ndarray) -> np.ndarray:
    """numpy: an older-layout theta at this layout's length, meaning intact.

    The flat-array twin of `unpack`'s pad, for the callers that store or train
    a theta rather than decode one (`scripts/train.py --resume`,
    `scripts/gene_sweep.py`): they hand the padded vector on, and a vector that
    is already `N_PARAMS` long never reaches `unpack`'s legacy branch again --
    so the hire-bias copy has to happen once, here, or a resumed run silently
    loses its bias on every day past the fifth. It is the copy `unpack` makes
    and only for the layouts `unpack` makes it for: an array that already
    reaches into `g9` carries buckets of its own and is padded with zeros.

    The parameter axis is the trailing one; leading axes (a pool, an Adam
    moment) come through untouched. A longer array is a newer layout and is
    returned as it came -- refusing it is the caller's call to make.
    """
    n = arr.shape[-1]
    if n >= N_PARAMS:
        return arr
    out = np.concatenate(
        [arr, np.zeros(arr.shape[:-1] + (N_PARAMS - n,), arr.dtype)], axis=-1)
    g8, g9 = offset("g8"), offset("g9")
    gb8, gb9 = offset("gb8"), offset("gb9")
    if n > N_PARAMS_PRE_BUCKET:
        # The array already carries part of the bucket block: it is a layout
        # that had the buckets, so the copy would overwrite trained weights
        # with a gene they have already moved away from. Pad it and no more.
        return out
    # `g8` is row-major [N_HEAD_HID, N_CREW_OUT], so column 0 is every
    # `N_CREW_OUT`-th coordinate; `g9` is [N_HEAD_HID, N_HIRE_EXTRA] the same
    # way. Strided rather than reshaped so a batched leading axis needs no case.
    src = out[..., g8:g8 + N_HEAD_HID * N_CREW_OUT:N_CREW_OUT]
    for k in range(N_HIRE_EXTRA):
        out[..., g9 + k:g9 + N_HEAD_HID * N_HIRE_EXTRA:N_HIRE_EXTRA] = src
        out[..., gb9 + k] = out[..., gb8]
    return out


def init_theta(rng: np.random.Generator) -> np.ndarray:
    """He-ish scaling per layer; ES explores from here."""
    parts = []
    for name, shape in SHAPES:
        if name in ("mh", "ms", "cm", "cb", "cd", "sw", "swb", "g12", "gb12"):
            parts.append(np.zeros(shape).ravel())
        elif len(shape) == 2:
            parts.append(rng.normal(0.0, np.sqrt(2.0 / shape[0]), shape).ravel())
        else:
            parts.append(np.zeros(shape))
    return np.concatenate(parts).astype(np.float32)


class Outputs(NamedTuple):
    scores: object      # [9, 2]  (grow, sell) per product
    head: object        # [18]    global decisions
    prio: object        # [9]     dead since 1.6 (was labour-priority weights)
    gate: object        # [9]     per-product timing pressure, pre-activation
    lots: object        # []      dead since 1.2 (was the sell lot count)
    aux: object      # [3]  unblock genes, pre-activation
    dev: object      # [2]  development locality and weight, pre-activation
    sat: object      # []   market-saturation bias on the plant mix, pre-activation
    crew: object     # [4]  hire bias (bucket 0) + per-animal want bias, pre-activation
    hire: object     # [4]  hire bias per day bucket, pre-activation; [0] is crew[0]
    ramp: object     # [4]  crew target height / midpoint / steepness + animal deferral
    fwd: object      # []   forward-admit horizon, pre-activation [g11]
    crop_mix: object  # [5] crop log-share residual, independent of grow value
    switch: object    # [N_SWITCH_GENES] gene-switch flip logits [sw/swb]
    #: [] fertilizer-timing look-ahead, pre-activation [g12]. Defaulted so a
    #: caller written before the block (a few unit tests build `Outputs`
    #: directly) decodes the zero horizon, which is the shipped plan.
    ft: object = 0.0


def forward(xp, p: Params, prod_feat, glob_feat, drain_feat,
            fcast_feat=None, fwdval_feat=None, momentum=None) -> Outputs:
    """prod [9, 12], glob [24], drain [9, 2], fcast [9, 8], fwdval [12] -> Outputs.

    The drain and forecast terms are *added* to two existing sums rather than
    concatenated into either input. Adding is what keeps an older checkpoint
    bit-exact: with `dh`/`ds` (or `fh`/`fs`) zero the extra products are 0.0 and
    `x + 0.0 == x` for every finite float, while a concatenation would change
    the matmul's reduction length and with it the rounding of the terms that
    were already there. Parenthesised explicitly so the pre-existing
    sub-expression is the one that was there before, whatever the backend does
    with the outer add -- and the forecast's add is *outside* the drain's for
    the same reason, so a caller that predates the forecast block gets the
    identical two-term expression.

    `fcast_feat=None` is that caller: the block is simply not applied. It is
    for callers written before the forecast existed (a few unit tests drive
    `forward` directly); `brain.decide` always passes one.

    `gp` is the same add one layer over: the flattened per-product summary
    joins the global head's pre-activation, parenthesised the same way so the
    expression the champion was trained under is still the exact
    sub-expression, and zero there is the identical `x + 0.0 == x` no-op. It is
    the only path in this function that runs *from* the encoder *to* the head;
    everything else flows the other way.

    `fv` joins that same pre-activation from the *outside* -- the forward-value
    vector is an input, not a read-back of the encoder -- and its add is
    parenthesised outside `gp`'s for the reason the forecast's is outside the
    drain's: a caller that predates the block gets the identical two-term
    expression. `fwdval_feat=None` is that caller (a few unit tests drive
    `forward` directly); `brain.decide` always passes one.
    """
    x = xp.concatenate([prod_feat, xp.broadcast_to(glob_feat, (spec.N_PRODUCTS,
                                                              N_GLOBAL_FEAT))], axis=1)
    pre = (x @ p.w1 + p.b1) + drain_feat @ p.dh
    enc_pre = pre if fcast_feat is None else pre + fcast_feat @ p.fh
    h = xp.tanh(enc_pre if momentum is None else enc_pre + momentum @ p.mh)
    scores = (h @ p.w2 + p.b2) + drain_feat @ p.ds
    if fcast_feat is not None:
        scores = scores + fcast_feat @ p.fs
    if momentum is not None:
        scores = scores + momentum @ p.ms
    # `press` is the `gate` output, hoisted so the summary can read it; the
    # expression is the one that was inline in `Outputs` and its slice is
    # unchanged, so `gate` is the same array it always was.
    press = h @ p.w3 + p.b3                                     # [9, 1]
    summary = (xp.concatenate([scores, press], axis=1)
               / xp.asarray(PROD_SUMMARY_SCALE))                # [9, 3]
    gpre = (glob_feat @ p.g1 + p.gb1) + summary.reshape(N_PROD_SUMMARY) @ p.gp
    gh = xp.tanh(gpre if fwdval_feat is None else gpre + fwdval_feat @ p.fv)
    crew = gh @ p.g8 + p.gb8
    return Outputs(scores=scores, head=gh @ p.g2 + p.gb2, prio=gh @ p.g3 + p.gb3,
                   gate=press[:, 0], lots=(gh @ p.g4 + p.gb4)[0],
                   aux=gh @ p.g5 + p.gb5, dev=gh @ p.g6 + p.gb6,
                   sat=(gh @ p.g7 + p.gb7)[0], crew=crew,
                   # Bucket 0 is `crew[0]` itself, not a copy of the matmul:
                   # the gene's first bucket *is* the gene as it shipped.
                   hire=xp.concatenate([crew[:1], gh @ p.g9 + p.gb9]),
                   ramp=gh @ p.g10 + p.gb10,
                   fwd=(gh @ p.g11 + p.gb11)[0],
                   crop_mix=gh @ p.cm + p.cb,
                   switch=gh @ p.sw + p.swb,
                   ft=(gh @ p.g12 + p.gb12)[0])


#: Head outputs nothing decodes any more (PLANNER_V3_1 section 2): 0 was
#: n_hire, 3..4 feed_daily / care_on, 8..12 the budget order, 13..17 were never
#: read. Live: 1 the land coin bias, 2 the animal-mix sharpness, 5 dev_frac, 6
#: animal_share, 7 plant-mix sharpness. (2 was `n_fertilize` before 0.11 priced
#: fertilizer, and dead until the mixed herd gave it a mix to sharpen.)
DEAD_HEAD = (0, 3, 4) + tuple(range(8, N_HEAD_OUT))
#: aux[0] was fert_buy; aux[1] (land afford) and aux[2] (free-tile urgency) live.
DEAD_AUX = (0,)


def live_mask() -> np.ndarray:
    """float32[N_PARAMS]: 1 where a parameter can change a decoded output, 0
    where it only feeds a deleted one. ES perturbs and updates the live
    coordinates only -- hygiene that keeps a dead block at its value *when
    masking began*, for a future reactivation. That is the fresh init only on
    a fresh lineage; on a resumed or trunk-warmed run it is whatever the block
    already held. Not a speed-up either: the dead coordinates' noise never
    reached the live ones (elementwise Adam, decoupled decay, no norm
    coupling)."""
    mask = np.ones(N_PARAMS, np.float32)
    shapes = dict(SHAPES)

    def zero(name, cols=None):
        off = offset(name)
        block = mask[off:off + int(np.prod(shapes[name]))].reshape(shapes[name])
        if cols is None:
            block[...] = 0.0
        else:
            block[..., list(cols)] = 0.0

    zero("g2", DEAD_HEAD)
    zero("gb2", DEAD_HEAD)
    zero("g3")
    zero("gb3")
    zero("g4")
    zero("gb4")
    zero("g5", DEAD_AUX)
    zero("gb5", DEAD_AUX)
    return mask


N_DEAD = int((live_mask() == 0).sum())
