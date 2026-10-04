"""Strategy archetypes: hand-set thetas for our own planner.

A single self-play lineage never shows itself the behaviours that beat it
(measured 2026-08-23: the shipped policy never buys a third quadrant, never
fertilizes, and sells melons into the opponent's glut). These thetas put such
opponents in the ladder without any third-party agent: every knob is a bias on
a head output or on one of the value outputs `brain.decide` prices the day
from, so the decode is a constant strategy readable from the dict.

The archetypes are also the **yardstick**: `Trainer.absolute_eval` measures
absolute coins against them on fixed seeds, and that number is what champion
selection and `--promote` now run on. A dead archetype is therefore not a
harmless spare tyre -- it is a quarter of the scale. Measured 2026-08-25, the
old `wheat_farmer` earned exactly **0 coins**: `value_tilt=-3` drove every grow
score to about -15, `_unit_ratio` (a softplus) mapped that to a grow multiplier
of 0, so it valued planting at nothing, spent its purse on land and finished
broke. `Trainer` now probes every archetype at construction -- and again
whenever `--resume` swaps the set for a checkpoint's -- and refuses any that
earns under 10k.

**Every coin figure in this file is that probe** unless it says otherwise:
`PROBE_PAIRS` = 4 episode seeds played in both seats against the zero theta
from the engine's own day 0, mean own coins over the 8 games. It is the number
`MIN_COINS` gates on, so a knob tuned against anything else is tuned against a
scale the run does not use. (`tests/test_archetype_ladder.py` builds a
2-pair `Trainer` and so measures the same rungs on 4 games; its numbers are
not these and are not meant to be.)

**Recalibrated 2026-08-26** for the one-crossing route and the corrected admit
model (`plan.EST_MOVES` 2 -> 1, `plan.EST_LEAD` 5). Those change the plan every
zero-theta archetype walks, so the whole ladder moved -- at `PROBE_PAIRS` = 4:

    expander 12,344   rusher 27,010   rancher 47,994   patient_grower 23,997
    value_farmer 34,524   squeeze_seller 30,345   staple_bulk 15,881
    mixed_ranch 66,308

Every rung clears `MIN_COINS`, and so does every drawn rung over five seeds at
`n_archetypes = len(NAMES) + 4` (lowest 12,079). `mixed_ranch` keeps the top of
the yardstick -- until 2026-08-28, when the two Kaggle-field rungs were added
and `wheat_clone` took it at the same 4-pair probe:

    wheat_clone 111,706   wool_specialist 74,971

A third field rung, `wheat_clone_v4`, was appended on 2026-08-30 and was never
probed at 4 pairs either -- it is `wheat_clone` at `animal_share` -1.0, and
what holds it is the same liveness floor. See its entry for the real-engine
sweep that chose it.

Those two are the **v1** figures, before the crew and herd-mix genes were tuned
into the same two entries later the same day (`hire_bias`, `animal_mix`; see
each entry). Both rungs moved and neither was re-probed at 4 pairs: what holds
them is `tests/test_archetype_ladder.py`'s liveness floor over the whole
`NAMES` list, which is the assertion `MIN_COINS` exists for. The nine rungs
above are unmoved -- the genes are inert at zero and no older entry names them.

That is worth knowing before reading a champion number: the yardstick's
ceiling moved, so an `abs_coins` measured across 11 rungs is not comparable
with one measured across 9. The per-knob figures further down this file were measured before
that recalibration unless they say otherwise: they are the *argument* for a
knob's value, not a live pin, and `tests/test_archetype_ladder.py` is what
holds the ladder itself.

Two knobs exist to make that failure unreachable:

* **`grow_bias`** sets the *mean* grow score across the nine products.
  `archetype_theta` centres the value terms, so the tilt knobs only decide the
  *shape* of the grow vector and `grow_bias` alone decides its level -- and the
  level is the only thing `_unit_ratio` reads. A negative tilt can no longer
  switch growing off. The crop mix is a softmax over grow scores, which is
  shift-invariant, so centring changes no mix.
* **`mid_tilt`** adds a band selector on the same product-value feature: a
  difference of two sharp tanh steps that is ~2 for strawberry, milk and wool
  and ~0 everywhere else. `value_tilt` is monotone in `log1p(base)`, so it can
  only ever crown **melon** -- the product whose price collapses fastest when
  dumped (`above_target` 3.6 against strawberry's and milk's 1.6). `mid_tilt`
  is how an archetype leans on the high-value products that survive being sold.

The one other non-bias knob, `value_tilt`, routes the per-product feature
`log1p(base) / 6` (brain.features, column 2) through encoder unit 0 into the
grow score, so crop choice can lean toward high-value or cheap products.

Two more knobs exist because a *constant* theta could not otherwise say what
the evaluation opponent says:

* **`crowd`** subtracts `crowd * tanh(own / 25)` from every grow score, where
  `own` is this farm's own producing tiles of that product (brain.features
  column 7). It is the only **state-dependent** term an archetype writes, and
  it is the whole difference between a rung with a strategy and a rung with a
  *book*: the crop softmax re-ranks as production accumulates, so one fixed
  theta plants melon until melon is crowded and then strawberry. Zero at
  `own = 0`, so it needs no centring -- the empty board on which `grow_bias`
  sets the level is exactly where it vanishes.

  Its grip on the **herd** loosened on 2026-08-26 and is worth stating
  exactly, because the old claim ("nothing else in this file can produce a
  mixed herd") is now false. `Macro.animal_want` is a proportional split of
  the three animal grow scores rather than one `argmax` over them, so a
  constant theta already *asks* for a mix, and `budget.grant` -- a threshold
  on value per coin -- can fund two kinds out of it on its own. What a
  constant theta still cannot do is *re-rank* the mix as the pasture fills:
  the three scores are constants, so the same kind leads on every board of the
  season. `crowd` is what moves them, and it shows up on the board:
  `mixed_ranch` at `crowd` 0 ends on **0 geese / 4.4 cows / 0.9 sheep**, at
  `crowd` 5 on **3.9 / 5.6 / 0.5**, worth 61,396 against 71,215 coins.
* **`land_cap`** is the number of quadrants the archetype stops at. Past it a
  step on `glob[7] = nquad / 4` takes `head[1]` down by `_CAP_M`; below it the
  term is exactly zero, so `land` and `land_afford` still decide *when*.
  `land` alone cannot express this: it is a bias on `head[1]` and `head[1]`
  reads no quadrant count.

  Since 2026-08-26 `head[1]` is a **coin bias** and not a boolean -- the
  planner prices the quadrant and the gene is `land_price * tanh(head[1] +
  land_afford * afford)`, deliberately bounded so that no gene can refuse an
  arbitrarily valuable quadrant (`core/brain.py`, `LAND_BIAS_STEPS`). So the
  step can no longer be a *decision*: what `_CAP_M` buys is a saturated
  `tanh`, i.e. a demand that the quadrant behind the wall be worth a whole
  extra price on top of its own. That the cap still holds is measured rather
  than argued -- across five rungs (`expander`, `rusher`, `rancher`,
  `staple_bulk`, `mixed_ranch`) and both settings, `land_cap` 2 ends every one
  of 8 games on exactly 2 quadrants and `land_cap` 3 on exactly 3, because
  `plan.land_reach` clamps the valuation to the tiles one day's crew can
  actually walk to and 25 unreachable tiles are never worth 2,000 coins.

A kagg2-shaped rung
-------------------
`mixed_ranch` is the answer to "can this parameterisation express the
evaluation opponent". Decoded from `kagg2`'s 719-step tape and measured in the
real engine against `pass` on seeds 0, 1, 3 and 7, `kagg2` is: three quadrants
(day 6 and day 11; the fourth only on the branch its shop draw unlocks), a
crew of 12 leased fresh every morning, **fourteen to eighteen pasture animals
in a mixed cow/sheep herd**, melon planted once by day 7 and never re-sown,
about 34 strawberry, a wheat treadmill that is both feed and a market drip,
and **no coop, no goose, no egg and no tomato at all**. It ends on 160,982 to
190,365 coins, 179,249 on average.

The answer is "the build-out, not the sell side". The three quadrants needed
`land_cap`; the diversified crop book needed `crowd`; the mixed herd needed
`crowd` too until the planner started buying one (2026-08-26), and still needs
it for the third kind. Measured in the real engine against `pass` over four
seeds in both seats, `mixed_ranch` ends on 3 quadrants (`kagg2`: 3, or 4 on
its high branch) and earns **81,657** coins to `kagg2`'s 179,249 -- **46%**.
The *timing* is its own: this rung takes its second quadrant at dawn on day 0
and its third around day 14, where `kagg2` buys on days 6 and 11.

The herd is the part that went backwards with the land valuation and has not
come back. On 2026-08-25 this rung finished on a 29-33 pasture-and-coop herd
against `kagg2`'s 14-18 -- too many, but the right order. It now finishes on
about **ten** animals, because the day's purse is spread across three animal
lists and a bigger hire bill and closes on fewer of each. That is a planner
result, not a knob: no setting of `animal_share` measured above buys a deeper
herd (0.5 buys none at all), and the knob is at the value that buys the most.

What did *not* cross is the sell side, and that is where the missing half is.
`kagg2` keeps every product's supply under the town's own drain, so it sells
strawberry, wheat, milk and wool *above* base all season: market inventory ends
**below** its opening level on six of the nine products, and its final quotes
are 1.2x to 2.3x base. Reproducing that here means a positive `hold`, and a
positive `hold` on a farm with a herd starves -- the feed bill falls due before
the reservation ever clears (`mixed_ranch` at `hold` +0.5 earns 32,664 in-sim
against 71,215, and its pasture ends empty). So this rung has `kagg2`'s board
and book, a shallower version of its herd, and dumps where `kagg2` drips.
Making the drip reachable is a planner change -- a reservation that reads the
town's drain rather than a fixed multiple of base -- not another knob here.

...and the rung that is only an opening
---------------------------------------
`mixed_ranch` has the right *shape* and about half the size, and half is not
enough: measured across 30 checkpoints, 11 of the 16 working ones beat it 128
games out of 128 and 15 of 16 beat it at least 94% of the time, while `kagg2`
wins 24 of 24. An objective assembled from that ladder has no observation
anywhere near the region it is meant to predict -- it measures the size of a
win it always gets, not the probability of a win it never gets.

`kagg2_proxy` is the same theta played from a **handicapped opening**, and it
is the cheapest way to put a rung the policy loses to on the board without
asking the planner for a capability it does not have. Nothing new is asked of
the simulator either: `rollout.episode` already takes `(nquad, money)` per
seat, and `Trainer.draw_starts` already opens a quarter of all pairs warm. The
only change is that the two seats stop sharing the row -- see
`Trainer.episode_starts` and `place_handicap` for the seat-indexing trap that
hides in that sentence.

What it buys, and what it costs:

* The win bit stops being a constant. Against every cold rung a working
  checkpoint scores 0.99-1.00; against the fitted proxy `p2s0/champion` scores
  **0/128**. And it is a genuinely different ranking rather than the same one
  again -- measured over 30 checkpoints in
  `docs/superpowers/plans/2026-08-26-win-objective.md`, Spearman(`abs_coins`,
  proxy margin) is +0.26 over the top 10 against **+0.90** for `abs_coins`
  against the cold `mixed_ranch`'s margin.
* The handicap is **free capital, not better routing**, so a policy could
  learn "beat a rich opponent" rather than "beat a well-routed one". Three
  mitigations, all in `es/train.py`: `arch_frac` stays 0.5 so half the episodes
  are still self-play, `HOLDOUT_RUNGS` keeps a handicap level and a different
  book out of training entirely, and the liveness probe plays this rung *with*
  its handicap so the number `MIN_COINS` gates on is the game the run plays.

Two decode scales worth knowing before tuning a knob here
---------------------------------------------------------
`hold` is a logit, and `brain.decide` turns it into a reservation of
`0.8 * base * softplus(hold) / softplus(0)` coins per unit. It crosses `base`
at about **+0.32**: a market whose inventory starts at `MARKET_I0` and only
grows never quotes above base for long, so any `hold` past that means "sell
nothing until `plan` forces the terminal liquidation". That is a real strategy
-- `patient_grower` earns 29,325 coins on it, more than `expander` does -- but
it is *hoarding*, not haggling, and it goes badly with livestock, because the
feed bill comes due before any sale does. Re-measured against the land-value
planner on 2026-08-26 that is a slope rather than the cliff it used to be
(`patient_grower` at `animal_share` -1.5 / 0 / +2 / +3: 17,380 / 12,909 /
11,208 / 4,369, and `rancher` at `hold=6` falls to 6,973 from 51,327), so a
herd alone no longer sinks a rung under the floor -- but it still costs one
half its coins or more, and a big enough one still does sink it. Every named
archetype with `hold > 0` therefore keeps `animal_share <= -1.5`.

`press` is the other logit, decoded as `base * max(tanh(press), 0)` coins per
lot of delay, so it saturates fast: +0.5 already prices a lot of delay at 0.46
of base and +2.0 at 0.96. Anything past about +3 is the same strategy as +2.
In practice it saturates harder than that: it only ranks the three lots of one
day against each other, and the whole positive half picks the same lot, so
what it really decides is *whether* delay is priced at all. Measured on
`squeeze_seller`, press 1, 2 and 3 all earn 31,237 -- one number, not three.

Which lot is the better one flipped with the land valuation: press 0 now earns
36,014 on that rung, where before 2026-08-26 it earned 26,105 against the
positive half's 31,476. `squeeze_seller` keeps `press = 2` anyway. The
archetypes are opponents and a yardstick, not champions: `MIN_COINS` is the
only bar they have to clear, and this is the one rung in the ladder that
prices delay at all. Retuning it to `press = 0` for 4.8k of yardstick would
delete a behaviour the trained policy would then never be made to play
against.
"""
from __future__ import annotations

import numpy as np

from .. import spec
from ..core import policy as PO

KNOBS = ("land", "dev", "animal_share", "crop_sharp", "value_tilt", "mid_tilt",
         "grow_bias", "hold", "press", "land_afford", "free_urgency",
         "crowd", "land_cap", "animal_sharp", "dev_weight", "sat",
         "prod_bias", "sell_bias", "hire_bias", "animal_mix",
         "crew_target", "crew_mid", "crew_steep", "animal_defer")

_HEAD_INDEX = {"land": 1, "animal_sharp": 2, "dev": 5, "animal_share": 6,
               "crop_sharp": 7}
_AUX_INDEX = {"land_afford": 1, "free_urgency": 2}   # gb5
#: `gb6` column 1: what a planting or a placement is worth to the labour
#: router, decoded `_unit_ratio` and clipped at `GROW_MAX` -- x1 at 0, so a
#: rung that does not name it walks exactly the plan it walked before. It is
#: the only knob in this file that reaches the **crew size**: `plan` hires the
#: `h` whose admitted task value less `HIRE_BILLS[h]` is largest, and this is
#: what a development task contributes to that sum.
_DEV_INDEX = {"dev_weight": 1}                       # gb6
#: `gb7`: the plant mix's absorption gate. Zero is the *shipped default*
#: ("plant only into town appetite nobody has claimed") rather than a no-op --
#: see `brain.decide`. Saturated positive it plants into a market the town
#: cannot absorb anyway, which is the only way a constant theta puts melon on
#: the board at all: melon's `share` is pinned at `-DRAIN_CLIP` from day 1, so
#: at `sat = 0` the gate masks it out of the crop softmax every single day.
_SAT_INDEX = {"sat": 0}                              # gb7
#: `gb8` column 0: the crew gene, decoded `brain.HIRE_BIAS_MAX * tanh(z)` coins
#: per hand and added to `plan` 1.5's enumerated gain. This is the **only** knob
#: in this file that asks for hands directly -- `dev`, `free_urgency` and
#: `dev_weight` move the crew by making the day's work worth more, which is a
#: different lever and a much blunter one. Against the fib bill the decode reads
#: as a crew target (see `brain.HIRE_BIAS_MAX` for the table); at 0 the day
#: hires exactly what the enumeration alone hires.
#: `hire_bias` is four numbers, one per day bucket [brain.HIRE_BIAS_BUCKETS]:
#: bucket 0 lives in `gb8` column 0 and buckets 1..3 in `gb9`. An entry may
#: still write one number for the whole season -- `_hire_vec` fills every
#: bucket with it, which is exactly what the knob meant before the buckets
#: existed, so v1 and v2 entries are byte for byte the thetas they were.
_CREW_INDEX = {"hire_bias": 0}                       # gb8
#: `gb8` columns 1..3: `animal_mix`, a per-kind logit on the herd want's
#: softmax, in the want's own log-share units and keyed by `spec.ANIMALS`
#: ("GOOSE", "COW", "SHEEP") rather than by product. Shift-invariant, so only
#: the differences matter and an entry naming one kind is a complete statement.
_MIX_OFF = 1                                         # gb8
#: `gb10`: the crew-target ramp and the early-spend deferral. `crew_target` is
#: the ramp's *height* in `brain.CREW_TARGET_MAX` hands (`relu(tanh)`, so 0 --
#: and the whole block inert -- when a rung does not name it), `crew_mid` the
#: day it is centred on and `crew_steep` how sharply it rises, both
#: `sigmoid`-scaled. `animal_defer` is how hard the animal channel waits while
#: the crew is under the target. This is the only knob group that can state the
#: Kaggle field's *opening*: a rung that fields 12 hands by day 10 and buys its
#: pasture afterwards is `crew_target` high, `crew_mid` around 8 and
#: `animal_defer` saturated -- which `hire_bias` alone cannot say, because a
#: constant per-hand tilt buys the cheap early hands and the coops too.
_RAMP_INDEX = {"crew_target": 0, "crew_mid": 1, "crew_steep": 2,
               "animal_defer": 3}                    # gb10

_VALUE_FEAT = 2          # brain.features prod column: log1p(base) / 6

#: The value feature's actual per-product values. Constant: `brain._BASE` reads
#: `spec.DEFAULT_MARKET_PARAMS`, so market jitter moves the engine's prices but
#: not the feature the policy sees.
_VALUE = np.log1p(np.array([spec.DEFAULT_MARKET_PARAMS[n]["base"]
                            for n in spec.PRODUCTS], np.float64)) / 6.0

#: Band edges for `mid_tilt`, placed at the midpoints of the gaps that bracket
#: {strawberry, milk, wool} in value-feature space: fertilizer .769 | .799
#: strawberry ... wool .884 | .921 melon. `_BAND_K` is steep enough that the
#: two tanh steps are saturated on both sides of each gap, so the band is ~2 on
#: the three products inside it and under 0.1 on every product outside.
_BAND_LO = float((_VALUE[spec.I_FERT] + _VALUE[spec.I_STRAWBERRY]) / 2.0)
_BAND_HI = float((_VALUE[spec.I_WOOL] + _VALUE[spec.I_MELON]) / 2.0)
_BAND_K = 100.0

#: `brain.features` prod column 7: own producing tiles of this product / 25.
#: The one *state-dependent* per-product feature `crowd` needs -- every other
#: column an archetype reads is a constant of the market table.
_OWN_FEAT = 7
#: `brain.features` glob column 7: nquad / _N_QUAD, what `land_cap` steps on.
_NQUAD_FEAT = 7
_N_QUAD = int(spec.LAND_PRICES.shape[0]) + 1      # brain.features' own divisor
#: Logit `land_cap` subtracts from `head[1]` past the cap. `head[1]` is read
#: through a `tanh` since the land bias became coins, so what this has to do is
#: **saturate** that `tanh` on top of whatever `land + land_afford * afford`
#: contributes: float32 `tanh` returns exactly -1 by |z| = 10, and the named
#: rungs reach `land` 10 with `afford` clipped at 4, so anything past ~24 is
#: equivalent and 60 is comfortably clear of the whole sampled range too. The
#: saturated bias is exactly one quadrant price of demanded margin -- see the
#: `land_cap` bullet in the module docstring for why that holds in a season.
_CAP_M = 60.0

#: The nine products in ascending value-feature order, and the midpoints of the
#: eight gaps between them. `prod_bias` / `sell_bias` write a **staircase** on
#: the same feature `value_tilt` and `mid_tilt` ride: eight sharp tanh steps,
#: one per gap, whose coefficients are the successive differences of the wanted
#: bias vector. Summed, step `k` contributes `+c_k` to every product above gap
#: `k` and `-c_k` to every product below it, so with `c_k = (b[k+1] - b[k]) / 2`
#: the sum is the wanted vector up to one constant -- and the constant is
#: exactly what `grow_bias` (resp. `hold`) already centres away.
#:
#: This is the generalisation `value_tilt` and `mid_tilt` are two fixed shapes
#: of, and it exists because the Kaggle field's book cannot be written in
#: either: the modal opponent is **wheat**-heavy with zero carrot and zero
#: tomato, and `value_tilt` is monotone in `log1p(base)`, so it can only ever
#: rank wheat (the cheapest product in the game) against carrot and tomato in
#: the one order the ramp allows.
_STAIR_ORDER = np.argsort(_VALUE)
_STAIR_EDGES = ((_VALUE[_STAIR_ORDER][1:] + _VALUE[_STAIR_ORDER][:-1]) / 2.0)
#: Steepness of one staircase step. The narrowest gap in `_VALUE` is EGG-TOMATO
#: at 0.0298, so a step reaches `tanh(400 * 0.0149) = 1 - 1e-5` at its nearer
#: neighbour and saturates outright at every other product -- the bias vector is
#: therefore reproduced to five decimal places. 400 is also small enough that
#: the pre-activation (`400 * v` against `-400 * edge`, both about 300) keeps
#: ~4 digits of float32 headroom past the cancellation.
_STAIR_K = 400.0
#: First encoder hidden unit the staircase may use: 0 is `value_tilt`, 1 and 2
#: are `mid_tilt`'s two steps, 3 is `crowd`.
_STAIR_H0 = 4
_N_STAIR = int(spec.N_PRODUCTS) - 1


def _bias_vec(bias) -> np.ndarray:
    """float64[9] from a knob given as a per-product mapping or a sequence.

    A mapping is keyed by `spec.PRODUCTS` name and defaults to 0 for anything
    it leaves out, which is how the entries below stay readable: a book is
    three or four products and eight silences.
    """
    if bias is None:
        return np.zeros(spec.N_PRODUCTS, np.float64)
    if isinstance(bias, dict):
        out = np.zeros(spec.N_PRODUCTS, np.float64)
        for k, v in bias.items():
            out[list(spec.PRODUCTS).index(k)] = float(v)
        return out
    out = np.asarray(bias, np.float64)
    if out.shape != (spec.N_PRODUCTS,):
        raise ValueError(f"prod/sell bias must be [{spec.N_PRODUCTS}], got {out.shape}")
    return out


def _mix_vec(bias) -> np.ndarray:
    """float64[3] from `animal_mix` given as a `spec.ANIMALS`-keyed mapping or
    a sequence. Same shape of argument as `_bias_vec`, a different key space:
    the herd want ranks *animals* and the book ranks *products*, and writing
    the mix in animal names is what keeps a herd entry readable next to the
    9-product book above it."""
    if bias is None:
        return np.zeros(spec.N_ANIMALS, np.float64)
    if isinstance(bias, dict):
        out = np.zeros(spec.N_ANIMALS, np.float64)
        for k, v in bias.items():
            out[list(spec.ANIMALS).index(k)] = float(v)
        return out
    out = np.asarray(bias, np.float64)
    if out.shape != (spec.N_ANIMALS,):
        raise ValueError(f"animal_mix must be [{spec.N_ANIMALS}], got {out.shape}")
    return out


def _hire_vec(bias) -> np.ndarray:
    """float64[N_HIRE_BUCKETS] from `hire_bias` given as one number for the
    whole season or as a per-bucket sequence [brain.HIRE_BIAS_BUCKETS].

    A scalar fills every bucket, so it says what it always said: the buckets
    are a refinement of the knob, not a replacement for it, and an entry that
    does not care about the calendar should not have to write four numbers.
    """
    if bias is None:
        return np.zeros(PO.N_HIRE_BUCKETS, np.float64)
    if np.ndim(bias) == 0:
        return np.full(PO.N_HIRE_BUCKETS, float(bias), np.float64)
    out = np.asarray(bias, np.float64)
    if out.shape != (PO.N_HIRE_BUCKETS,):
        raise ValueError(f"hire_bias must be a number or [{PO.N_HIRE_BUCKETS}], "
                         f"got {out.shape}")
    return out


def _stair_coefs(bias: np.ndarray) -> np.ndarray:
    """The eight step coefficients whose staircase reproduces `bias`, [8]."""
    return np.diff(bias[_STAIR_ORDER]) / 2.0


def _stair_terms(bias: np.ndarray) -> np.ndarray:
    """The staircase's actual per-product contribution, [9].

    Exactly what `policy.forward` computes for encoder units `_STAIR_H0 ..`
    given the weights `archetype_theta` writes -- the same standing precondition
    as `_grow_terms`, and the same reason: the centring has to subtract the
    number the network really adds, not the number it was asked for.
    """
    steps = np.tanh(_STAIR_K * (_VALUE[:, None] - _STAIR_EDGES[None, :]))
    return steps @ _stair_coefs(bias)


def _grow_terms(value_tilt: float, mid_tilt: float, prod_bias=None) -> np.ndarray:
    """The per-product grow contribution of the two tilt knobs, [9].

    Exactly what `policy.forward` computes for encoder units 0-2 given the
    weights `archetype_theta` writes, so centring on its mean is exact rather
    than approximate.

    That exactness has one standing precondition, which `archetype_theta`
    keeps by writing nothing outside the blocks the knobs name: the encoder
    pre-activation is `x @ w1 + b1 + drain_feat @ dh` and the scores carry
    `+ drain_feat @ ds`, so a nonzero drain block would add a *state-dependent*
    term this function cannot see and the centring would drift with the board.
    So no rung reads the residual drain, and that is a choice rather than an
    omission: `crowd` and `land_cap` make an archetype react to its *own*
    board, which is what gives a rung a book instead of a list, but a rung
    that also tracked the contested market would stop being a fixed yardstick
    for the policy that is learning to contest it.
    """
    ramp = 10.0 * value_tilt * np.tanh(_VALUE)
    band = (np.tanh(_BAND_K * (_VALUE - _BAND_LO))
            - np.tanh(_BAND_K * (_VALUE - _BAND_HI)))
    stair = _stair_terms(_bias_vec(prod_bias))
    return ramp + 5.0 * mid_tilt * band + stair


def archetype_theta(**knobs) -> np.ndarray:
    unknown = set(knobs) - set(KNOBS)
    if unknown:
        raise KeyError(f"unknown archetype knobs: {sorted(unknown)}")
    theta = np.zeros(PO.N_PARAMS, np.float32)
    gb2 = PO.offset("gb2")
    for name, idx in _HEAD_INDEX.items():
        theta[gb2 + idx] = knobs.get(name, 0.0)
    gb5 = PO.offset("gb5")
    for name, idx in _AUX_INDEX.items():
        theta[gb5 + idx] = knobs.get(name, 0.0)
    gb6 = PO.offset("gb6")
    for name, idx in _DEV_INDEX.items():
        theta[gb6 + idx] = knobs.get(name, 0.0)
    gb7 = PO.offset("gb7")
    for name, idx in _SAT_INDEX.items():
        theta[gb7 + idx] = knobs.get(name, 0.0)
    gb8 = PO.offset("gb8")
    gb9 = PO.offset("gb9")
    hire = _hire_vec(knobs.get("hire_bias"))
    theta[gb8 + _CREW_INDEX["hire_bias"]] = hire[0]
    theta[gb9:gb9 + PO.N_HIRE_EXTRA] = hire[1:]
    theta[gb8 + _MIX_OFF:gb8 + _MIX_OFF + spec.N_ANIMALS] = _mix_vec(
        knobs.get("animal_mix"))
    gb10 = PO.offset("gb10")
    for name, idx in _RAMP_INDEX.items():
        theta[gb10 + idx] = knobs.get(name, 0.0)
    w1 = PO.offset("w1")
    w2 = PO.offset("w2")
    b1 = PO.offset("b1")
    value_tilt = float(knobs.get("value_tilt", 0.0))
    mid_tilt = float(knobs.get("mid_tilt", 0.0))
    # crop value tilt: x[:, 2] -> h[0] -> grow score
    theta[w1 + _VALUE_FEAT * PO.N_ENC_HID + 0] = 1.0          # w1[2, 0]
    theta[w2 + 0 * PO.N_ENC_OUT + 0] = 10.0 * value_tilt      # w2[0, 0]
    # mid-value band: two sharp steps on the same feature, differenced.
    theta[w1 + _VALUE_FEAT * PO.N_ENC_HID + 1] = _BAND_K      # w1[2, 1]
    theta[w1 + _VALUE_FEAT * PO.N_ENC_HID + 2] = _BAND_K      # w1[2, 2]
    theta[b1 + 1] = -_BAND_K * _BAND_LO
    theta[b1 + 2] = -_BAND_K * _BAND_HI
    theta[w2 + 1 * PO.N_ENC_OUT + 0] = 5.0 * mid_tilt         # w2[1, 0]
    theta[w2 + 2 * PO.N_ENC_OUT + 0] = -5.0 * mid_tilt        # w2[2, 0]
    # Per-product staircase on the same value feature: `prod_bias` into the
    # grow score, `sell_bias` into the sell score. Both share the eight hidden
    # units, because the steps themselves are a function of the feature alone --
    # only the output weights differ.
    prod_bias = _bias_vec(knobs.get("prod_bias"))
    sell_bias = _bias_vec(knobs.get("sell_bias"))
    if prod_bias.any() or sell_bias.any():
        cg, cs = _stair_coefs(prod_bias), _stair_coefs(sell_bias)
        for k in range(_N_STAIR):
            h = _STAIR_H0 + k
            theta[w1 + _VALUE_FEAT * PO.N_ENC_HID + h] = _STAIR_K
            theta[b1 + h] = -_STAIR_K * _STAIR_EDGES[k]
            theta[w2 + h * PO.N_ENC_OUT + 0] = cg[k]
            theta[w2 + h * PO.N_ENC_OUT + 1] = cs[k]
    b2 = PO.offset("b2")
    # Centre the tilts so `grow_bias` alone sets the level `_unit_ratio` reads.
    theta[b2 + 0] = (float(knobs.get("grow_bias", 0.0))
                     - float(_grow_terms(value_tilt, mid_tilt, prod_bias).mean()))
    # Same centring on the sell side, and for the same reason: `hold` is the
    # *mean* reservation across the nine products and `sell_bias` only shapes
    # it, so a rung that dumps melon does not thereby hoard everything else.
    theta[b2 + 1] = (float(knobs.get("hold", 0.0))              # reservation-value logit
                     - float(_stair_terms(sell_bias).mean()))
    theta[PO.offset("b3")] = knobs.get("press", 0.0)          # timing-pressure logit
    # Crowding: -crowd * tanh(own / 25) on every grow score. Encoder unit 3,
    # zero at `own = 0`, so it needs no centring -- it *is* centred at the
    # empty board `grow_bias` is measured on.
    crowd = float(knobs.get("crowd", 0.0))
    if crowd:
        theta[w1 + _OWN_FEAT * PO.N_ENC_HID + 3] = 1.0        # w1[7, 3]
        theta[w2 + 3 * PO.N_ENC_OUT + 0] = -crowd
    # Quadrant cap: a step on glob[7] = nquad / _N_QUAD that subtracts `_CAP_M`
    # from `head[1]` once the archetype already owns `land_cap` quadrants, and
    # exactly zero below that -- so `land_cap` is the board it ends the season
    # on, not the last purchase it makes. Head hidden unit 0.
    land_cap = float(knobs.get("land_cap", _N_QUAD))
    if land_cap < _N_QUAD:
        g1, gb1, g2 = PO.offset("g1"), PO.offset("gb1"), PO.offset("g2")
        theta[g1 + _NQUAD_FEAT * PO.N_HEAD_HID + 0] = _BAND_K
        theta[gb1 + 0] = -_BAND_K * (land_cap - 0.5) / _N_QUAD
        theta[g2 + 0 * PO.N_HEAD_OUT + 1] = -_CAP_M / 2.0
        theta[gb2 + 1] -= _CAP_M / 2.0
    return theta


#: `grow_bias` 8.0 pins the grow multiplier at its `GROW_MAX` clip for every
#: product. `expander` and `rusher` already sat there before centring existed
#: (their tilts alone put every grow score past the clip), so they are byte-for
#: -byte the same strategy; `rancher` tilts by nothing at all and keeps
#: `grow_bias=0`, which is the multiplier of exactly 1.0 it had.
_GROW_MAXED = 8.0

_NAMED = {
    # buys land whenever it can and fills it
    "expander": dict(land=10.0, dev=3.0, animal_share=-1.5,
                     crop_sharp=0.0, value_tilt=1.0, mid_tilt=0.0,
                     grow_bias=_GROW_MAXED, hold=0.0, press=0.0,
                     land_afford=1.0, free_urgency=3.0,
                     crowd=0.0, land_cap=_N_QUAD),
    # melon/strawberry heavy, dumps at any price, on the two quadrants a
    # season's crew can actually walk. `land_cap` 2 is the 2026-08-26
    # recalibration and the only thing that moved: at the whole board this rung
    # earned **9,092** coins, under `MIN_COINS`, and a rung under the floor is
    # not an opponent, it is a hole in the yardstick. Land is what was eating
    # it and `dev` was not -- `dev` 3, 6 and 8 all measure 9,704 against 10's
    # 9,092, every one of them under the floor, while at `dev` 10 the
    # `land_cap` 4 / 3 / 2 row measures 9,092 / 19,126 / 26,987 -- so the
    # third quadrant costs it as much as the fourth. It dumps melon into a
    # curve whose `above_target` is 3.60, so every tile added past the crew's
    # reach is 2,000-4,000 coins spent on a crop whose own volume has already
    # taken the price down. Crop book, reservation and delay price -- the
    # identity -- are untouched.
    "rusher": dict(land=2.0, dev=10.0, animal_share=-10.0,
                   crop_sharp=3.0, value_tilt=3.0, mid_tilt=0.0,
                   grow_bias=_GROW_MAXED, hold=-6.0, press=0.0,
                   land_afford=0.5, free_urgency=3.0,
                   crowd=0.0, land_cap=2.0),
    # animals first, sells wool/milk/fertilizer
    "rancher": dict(land=1.0, dev=3.0, animal_share=2.0,
                    crop_sharp=0.0, value_tilt=0.0, mid_tilt=0.0,
                    grow_bias=0.0, hold=-1.0, press=0.0,
                    land_afford=0.5, free_urgency=2.0,
                    crowd=0.0, land_cap=_N_QUAD),
    # market timing: strawberry/milk/wool, and a reservation above the market
    # (0.8 * base * softplus(1)/softplus(0) = 1.52x base) that the season only
    # clears on the terminal day, so it hoards its stock and lands it in one
    # block instead of feeding the crash daily. Measured 29,325 coins.
    "patient_grower": dict(land=3.0, dev=6.0, animal_share=-2.0,
                           crop_sharp=2.0, value_tilt=1.0, mid_tilt=3.0,
                           grow_bias=_GROW_MAXED, hold=1.0, press=1.0,
                           land_afford=1.0, free_urgency=3.0,
                           crowd=0.0, land_cap=_N_QUAD),
    # the same crop mix selling normally: 40,146 coins, and the rung that makes
    # the market contested rather than merely occupied. It led the yardstick
    # until `mixed_ranch` arrived; since the land valuation it sits third,
    # behind `mixed_ranch` and `rancher`, because it is one of the five rungs
    # that still take the whole board.
    "value_farmer": dict(land=3.0, dev=6.0, animal_share=-2.0,
                         crop_sharp=2.0, value_tilt=1.0, mid_tilt=3.0,
                         grow_bias=_GROW_MAXED, hold=-1.0, press=0.0,
                         land_afford=1.0, free_urgency=3.0,
                         crowd=0.0, land_cap=_N_QUAD),
    # market timing: a reservation of 1.12x base, which only a market the town
    # has drained below its opening inventory ever clears, plus a delay price
    # that puts the whole day's sale into the first lot. Measured 31,237 coins.
    #
    # Until 2026-08-25 this was `hold=1.0`, and at that reservation the rung
    # was a byte-for-byte duplicate of `patient_grower`: traced side by side
    # the two hold the same money on every one of the thirty days, keep the
    # same nine cows, and finish on exactly 21,200 coins each. At 1.52x base
    # nothing is ever sold on timing grounds, so `press` -- the knob that was
    # meant to separate them -- only chose which lot the forced shed overflow
    # landed in, and on that it saturates: 1 and 2 pick the same lot. The
    # other differences decode to the same day anyway. `land` 2 with
    # `land_afford` 0.5 and `land` 3 with 1.0 both keep
    # `land + land_afford * afford` positive at every affordability a season
    # reaches, so both buy every quadrant; and both tilt vectors put the whole
    # crop softmax on strawberry and pick milk as the animal. Dropping `hold`
    # to where the market does clear is what makes the delay price bite again.
    #
    # The duplication argument no longer holds either way, which is worth
    # recording rather than quietly relying on: under the land valuation this
    # rung at `hold=1.0` earns 31,237 against `patient_grower`'s 29,325, so the
    # two are separated by `land`/`dev`/the tilts alone now. `hold=0.5` stays
    # because the reservation the ladder needs is one a season actually
    # *clears* -- a second hoarder is what the 2026-08-25 split removed.
    "squeeze_seller": dict(land=2.0, dev=8.0, animal_share=-2.0,
                           crop_sharp=2.0, value_tilt=1.5, mid_tilt=2.0,
                           grow_bias=_GROW_MAXED, hold=0.5, press=2.0,
                           land_afford=0.5, free_urgency=3.0,
                           crowd=0.0, land_cap=_N_QUAD),
    # cheap stable crop in bulk -- the repaired `wheat_farmer`. `grow_bias`
    # keeps the grow multiplier alive under the negative tilt that used to
    # zero it. Retuned 2026-08-25 against the 16-hand planner, which had put
    # it on 7,439 coins; `dev` and `hold` both had to move, and neither was
    # worth anything alone (dev alone 5,400, hold alone 8,378, both 17,610).
    #
    # * `dev` 10 -> 6. `n_dev` is `floor(sigmoid(dev + free_urgency * n_free /
    #   25) * n_free + QUANT_EPS)`, and this far into the sigmoid's saturation
    #   all the knob still decides is whether that product rounds up to
    #   `n_free` itself -- "develop the *last* free tile too". On the opening
    #   25-tile board only 10 rounds up; on a 49- or 50-tile board 8 and 9 do
    #   as well, which is where the safe plateau stops. Developing that last
    #   tile is what starts the spiral: the hire enumeration buys the crew
    #   that reaches every queued tile, which cost 143 coins when `MAX_HANDS`
    #   was 10 and costs 2,583 now that it is 16, and `plan.cash_reserve`
    #   holds back `HIRE_BILLS[h + 1]` on top -- so a ~2,500-coin purse is
    #   handed exactly 0 coins to buy seed with. The tiles it hired the crew
    #   for stay empty, which makes tomorrow's free-slot count larger and
    #   tomorrow's crew bigger again: traced, it hires 15-16 hands a day from
    #   day 13 and finishes the season on 100 empty tiles and 7 coins.
    #   Everything in 3..7 measures the same 17,610; 6 is mid-plateau.
    # * `hold` 1.0 -> -1.0. Wheat is the cheapest product in the game, so a
    #   reservation of 1.52x base is one its price never reaches: traced, the
    #   shed sat pinned at 100 wheat from day 5 to the end and the only coins
    #   coming in were `plan`'s shed-overflow forced sale. Selling volume is
    #   this archetype's whole identity, and wheat has the shallowest dump
    #   curve of any crop (`above_target` 0.20 against melon's 3.60), so a
    #   reservation has nothing here to protect.
    #
    # Retuned again 2026-08-26, against the land valuation, and only
    # `land_cap` moved: 11,006 coins at the whole board against 16,566 at
    # three quadrants and 16,304 at two. It clears `MIN_COINS` either way, but
    # 1.1x the floor is not a margin -- one planner change and the rung is a
    # hole in the yardstick again -- and nothing else in the entry was worth a
    # coin. Measured at the uncapped board, `dev` 4, `hold` -3 and
    # `crop_sharp` 6 each land on the identical 11,006 and `press` 0 on
    # 10,302, so the knob that moves this rung is the one about land.
    # `land` stays 6: it still buys every quadrant it is allowed, and it is
    # now allowed three.
    "staple_bulk": dict(land=6.0, dev=6.0, animal_share=-10.0,
                        crop_sharp=3.0, value_tilt=-3.0, mid_tilt=0.0,
                        grow_bias=_GROW_MAXED, hold=-1.0, press=0.5,
                        land_afford=1.0, free_urgency=3.0,
                        crowd=0.0, land_cap=3.0),
    # The shape of `kagg2`, the immutable evaluation opponent, expressed in
    # this planner's own knobs. See the "A kagg2-shaped rung" section of the
    # module docstring for what was measured off its tape and what of it this
    # theta does and does not reach. Strongest rung on the yardstick at
    # **71,215 coins** in-sim (4 seeds x 2 seats vs the zero theta), against
    # `rancher`'s 51,327 and `value_farmer`'s 40,146.
    #
    # Re-measured 2026-08-26 against the land valuation and the mixed herd,
    # and `animal_share` is the one knob that had to move: 0.5 / 1 / 2 / 3 / 4
    # -> 29,485 / 71,215 / 57,951 / 57,936 / 35,088. At 0.5 the rung finished
    # every one of the 8 probe games with an **empty pasture** -- a
    # kagg2-shaped rung with no herd is not the rung -- because the day asked
    # for 46 animals beside 29 plantings and `budget.grant` could fund neither
    # half of that against the day's hire bill. 1.0 asks for a herd the purse
    # can actually close on, and ends the season on ~10 animals of two or
    # three kinds against `kagg2`'s 14-18.
    #
    # Every other knob is load-bearing at the new share; each was measured
    # against the rest held fixed, 4 seeds x 2 seats vs the zero theta:
    #
    # * `crowd` 5. 0 / 3 / 5 / 7 -> 61,396 / 64,992 / 71,215 / 68,865. It is
    #   no longer "the whole rung" -- `Macro.animal_want` splits the herd
    #   across kinds by itself now -- but it is still what spreads the crop
    #   book and what puts a third kind in the pasture: at `crowd` 0 the herd
    #   ends 0.0 geese / 4.4 cows / 0.9 sheep, at 5 it ends 3.9 / 5.6 / 0.5.
    # * `land_cap` 3. `kagg2` ends the season on 75 tiles. 2 / 3 / 4 ->
    #   82,754 / 71,215 / 57,967. The fourth quadrant is 4,000 coins and 25
    #   tiles a 16-hand crew cannot reach, which is the same arithmetic that
    #   stops `kagg2` buying it on its low route -- so 3 beats 4 on coins as
    #   well as on shape. Two quadrants beat both, and this rung does not take
    #   that trade: `kagg2`'s board is the thing it exists to express, and
    #   `rusher` already carries a 2-quadrant rung into the ladder.
    # * `land` -4 with `land_afford` 3 is *not* a delay. The land bias is
    #   `land_price * tanh(land + land_afford * clip(money / price - 1, -1,
    #   4))`, and the opening purse of 3,000 against a 1,000-coin quadrant
    #   already turns it positive, so this rung takes its second quadrant on
    #   day 0 rather than `kagg2`'s day 6 -- `land` 6 with `land_afford` 1
    #   plays the same season to the coin (71,215 either way). What is not
    #   free is waiting: `land_afford` 1 under `land` -4 holds out for five
    #   times the price and earns 65,941.
    # * `mid_tilt` 0 and `value_tilt` 1. The band that crowns strawberry and
    #   milk is what the *other* rungs use; here `crowd` does the spreading and
    #   the band only re-concentrates it -- 0 / 0.5 -> 71,215 / 38,919.
    #   `value_tilt` 1 is a sharp optimum (0.9 / 1.0 / 1.1 -> 56,060 / 71,215
    #   / 53,974): it is what puts melon at the head of the book on day 0 and
    #   keeps the goose behind the cow until the herd is deep.
    # * `hold` -1 and `press` 0. `kagg2` sells *above* base all season by
    #   keeping its supply under the town's drain, and that is the one thing
    #   here that does not survive the crossing: a reservation and a herd do
    #   not mix in this planner (`hold` -1 / -0.3 / +0.5 -> 71,215 / 62,351 /
    #   32,664, and at +0.5 the pasture is empty again), because the feed bill
    #   falls due before the reservation ever clears. This rung dumps instead.
    "mixed_ranch": dict(land=-4.0, dev=10.0, animal_share=1.0,
                        crop_sharp=-1.0, value_tilt=1.0, mid_tilt=0.0,
                        grow_bias=_GROW_MAXED, hold=-1.0, press=0.0,
                        land_afford=3.0, free_urgency=3.0,
                        crowd=5.0, land_cap=3.0),
    # `mixed_ranch`'s knobs again, byte for byte. What makes this a *different*
    # rung is not its theta but its **opening**: `Trainer` gives this slot --
    # and only this slot -- the `--proxy-handicap` start on the opponent seat,
    # so it plays the season from extra quadrants and extra cash. See
    # PROXY_HANDICAP below for why the level is a measurement rather than a
    # constant, and the "A kagg2-shaped rung" section of the docstring for what
    # the knobs themselves reach.
    #
    # It is a separate entry rather than a flag on `mixed_ranch` because the
    # ladder wants both: the cold rung is a difficulty the policy has already
    # passed and still has to keep passing, and the handicapped one is the
    # difficulty it has not. Aliased below rather than copied, so the two can
    # never drift apart under a retune.
}
_NAMED["kagg2_proxy"] = dict(_NAMED["mixed_ranch"])

# ------------------------------------------------------------- the Kaggle field
#
# The two rungs below are not inventions: they are the two behavioural classes a
# replay autopsy of 64 leaderboard games found (2026-08-27, `scripts/
# replay_profile.py` over the 64 non-mirror replays, 128 seats, 228 columns).
# The field is a **monoculture** -- 36 of 64 opponents are near-identical forks
# of one public template, identical plant counts to within +-3 -- so an opponent
# ladder made only of this planner's own self-play shapes has never seen the
# strategy that actually beats us 42% of the time.
#
# Class A, "the 140-wheat clone" (36/64, beats us 42%), per-seat medians:
#
#     14 hands by day 10 (3-4 by day 5)   quadrants NE d6, SW d10, never SE
#     plant 140 WHEAT / 36 STRAWBERRY / 18 MELON / 0 CARROT / 0 TOMATO
#     9 COW + 4 SHEEP on pasture, no coop, no goose, no egg
#     sell 431 WHEAT (median day 26)   277 STRAWBERRY (d20)   105 MELON (d10)
#     220 MILK (d17)   132 WOOL (d13)   235 FERTILIZER (d13), fertilises ~70x
#     buys ~250 WHEAT as feed;  final money ~94,000
#
# Class C, "the wool specialist" (6/64, the highest raw scores in the field,
# 110-130k): the same board with 12 SHEEP / 6 COW, 254 WOOL sold at a median
# day 13, and only ~215 WHEAT / ~184 STRAWBERRY units. It is the rung that
# crashes WOOL to 1 by day 20, which is the specific pressure our own
# sheep-heavy wins are not robust to.
#
# **What these two are for is what they do *not* do.** Neither plants a carrot
# or a tomato, neither ever places a goose, and no opponent in 64 games sold a
# single egg -- three markets the town drains all season and nobody contests.
# A ladder without them teaches the policy that every market is contested.
#
# What the knobs reach and what they do not is measured under each entry. Two of
# the three things the 2026-08-27 autopsy could not say became knobs on
# 2026-08-28 (`hire_bias` and `animal_mix`, `policy` block `g8`/`gb8`); the
# third is still not one, and the shape of all three is worth stating once:
#
# * **The labour ramp is now a bias, not a count.** `plan` still picks the crew
#   whose admitted task value less `HIRE_BILLS[h]` is largest -- `hire_bias`
#   adds coins per hand to that gain, which against a fib bill reads as a crew
#   target (`brain.HIRE_BIAS_MAX`). What it still cannot express is the field's
#   *shape*: one number for the season buys the cheap early hands first, so a
#   bias big enough for 12-14 hands on day 20 also puts 7 on day 5 against the
#   field's 3-4, and a bias big enough for the field's day-10 crew of 14 is
#   ruinous (measured below). A ramp would need the bias to read the day.
# * **The herd ratio is now expressible**, and it needed a gene that is not the
#   grow score: `animal_mix` biases the want's softmax alone, leaving
#   `_unit_ratio(grow)` -- what `budget.grant` prices the animal at -- exactly
#   where the book put it. The want is a per-kind *cap* on the day's grant, so
#   biasing it toward the dearer animal is what stops the cheaper one taking
#   the whole pasture. `wool_specialist` lands class C's 12 SHEEP / 6 COW on it.
# * **A per-crop tile *count* is still not a knob.** The mix is a softmax over
#   grow scores and `plant_target` is its largest-remainder split of whatever
#   the day has room and money for, so `prod_bias` sets the *shares* (140 : 36 :
#   18 = 0.72 : 0.19 : 0.09) and the season's totals follow the board.
#: Class A's book, written as the **grow score vector itself**. Paired with
#: `grow_bias = mean(book)` the centring in `archetype_theta` is exactly
#: undone, so `score_p == book[p]` and both decodes can be read off one table:
#:
#: * the crop *shares* are `softmax(book[:5])` -- at `crop_sharp = -10` the mix
#:   multiplier is 1.0002, so a difference of 0.61 is the 0.55 : 0.30 ratio it
#:   looks like -- and the animal shares are `softmax(book[EGG, MILK, WOOL])`;
#: * the planner's own *valuation* of a tile is `min(softplus(score) /
#:   softplus(0), 4)`, which saturates at 2.71. That is why the herd's two
#:   entries are not just a ratio: `budget.grant` funds animals by value per
#:   coin and a SHEEP costs 500 against a COW's 400, so two saturated scores
#:   buy an all-cow pasture whatever the want says (measured round 1: want
#:   0.69/0.31, placed 23 COW / 2 SHEEP). `wool_specialist` separates them by
#:   dropping MILK *below* saturation instead.
#:
#: -12 is the value of the three channels the whole field leaves open: a
#: softmax weight of 2e-9 against wheat's 0.55, so `_largest_remainder` can
#: never hand one of them a leftover unit, and a grow multiplier of 0, so the
#: planner does not value the tile either.
_CLONE_BOOK = {
    # 0.55 : 0.30 : 0.15 of the day's plantings. Not the 0.72 : 0.19 : 0.09 of
    # the season's *totals*: wheat is a one-time crop replanted every four days
    # while strawberry holds its tile, and `brain.decide`'s `can_mature` mask
    # takes strawberry and melon out of the mix from day 19 on, so the late
    # season is all wheat and the daily share has to run ahead of the target.
    "WHEAT": 8.0, "STRAWBERRY": 7.67, "MELON": 6.39,
    "CARROT": -12.0, "TOMATO": -12.0, "EGG": -12.0,
    "MILK": 8.0, "WOOL": 8.0, "FERTILIZER": 8.0,
}
#: The v3 labour ramp: `hire_bias` per day bucket [brain.HIRE_BIAS_BUCKETS], in
#: knob units, decoding to **39 / 385 / 184 / -201 coins** a hand on days 0-5,
#: 6-10, 11-20, 21+.
#:
#: The rung's v2 note below ends on the finding this ramp answers: one number
#: for the season buys the *cheap early* hands first, so the setting that
#: lands the board (0.10) leaves day 20 at 10 hands against the field's 14
#: (11-12 in the real engine, where the v2 table below was measured),
#: and the settings that reach 14 spend the purse before there is anything to
#: harvest. Four numbers separate the two ends. Measured in the simulator
#: against the zero theta (seed 11, one season, hands as `plan` 1.5 hires
#: them):
#:
#:     ramp (coins)          d5  d10  d15  d20   final money
#:     v2  39/39/39/39        7    9    9   10       112,867
#:     385/385/0/-201         9    8    2    6        20,720
#:     v3  39/385/184/-201    7    9   12   14        78,684
#:     39/241/116/-201        7    9   11   13        96,861
#:     184/385/304/-201       7    9   13   14        55,733
#:
#: Two things the table says and the entry is written from:
#:
#: * **Day 10 is not reachable through this gene.** The field fields 14 hands
#:   on day 10; the ramp that demands them from day 0 (385 coins in bucket 0)
#:   hires 14 on day 0 and *8* on day 10 -- it spends the purse, `cash_reserve`
#:   then holds `HIRE_BILLS[h + 1]` of what is left, and the rung plants
#:   nothing that could pay for a crew later (final money 20,720 against
#:   112,867). Bucket 1 saturated reaches 13 hands on day 6 and decays to 9 by
#:   day 10 for the same reason: on this planner's day-10 purse (~2,500 coins
#:   against the field's 8,294) the binding constraint is money, not the gene.
#:   Closing that gap is a *board* problem, and this rung's board is v2's.
#: * **Day 15 and day 20 are.** By then the season has sold something, and
#:   184 coins in bucket 2 buys the mid-season crew the field runs: 9 -> 12 on
#:   day 15 and 10 -> 14 on day 20, which is the class-A ramp this rung was
#:   built to imitate, for 34,000 coins of its own final purse.
#:
#: Bucket 3 is negative (-201) on purpose and costs nothing: past day 21 a hand
#: has fewer days left to pay itself back, and past `ops.LAST_SHED_DAY` the
#: enumeration hires nobody at all whatever the bucket says.
_CLONE_HIRE_V3 = (0.10, 2.0, 0.5, -0.55)

_NAMED["wheat_clone"] = dict(
    land=-4.0, dev=10.0, animal_share=-2.0,
    # `crop_sharp` and `animal_sharp` are pushed into the flat end of their own
    # sigmoids on purpose: `brain.decide` scales both softmaxes by
    # `1 + sig(head) * 4`, so at -10 the multiplier is 1.0002 and the book
    # above is a table of log-shares rather than a puzzle.
    crop_sharp=-10.0, animal_sharp=-10.0,
    value_tilt=0.0, mid_tilt=0.0,
    grow_bias=float(_bias_vec(_CLONE_BOOK).mean()),
    hold=-1.0, press=0.0, land_afford=1.0, free_urgency=4.0,
    crowd=0.0, land_cap=3.0, dev_weight=2.5, sat=3.0,
    prod_bias=_CLONE_BOOK,
    # The two 2026-08-28 genes, both measured in the real engine against the
    # champion (`artifacts/theta_flow9_g15975_champion.npy`, 4 seeds x 2 seats,
    # medians; the v2 table below is the 8-seed re-measurement):
    #
    # * `hire_bias` 0.10 -> 39 coins a hand, which against the fib bill pays
    #   for the ninth. It is a tenth of what the field's day-10 crew of 14
    #   would need and that is the *measurement*: 0.25 / 0.5 / 1.0 (98 / 190 /
    #   304 coins, crews of 11 / 13 / 13) earn 49,543 / 7,159 / 6,689 against
    #   this setting's 63,327, because `cash_reserve` holds `HIRE_BILLS[h + 1]`
    #   of every day's purse back for tomorrow's crew and a rung that hires 13
    #   hands from day 5 has nothing left to buy seed with -- at 0.5 it plants
    #   half a strawberry tile a game. What 0.10 does buy is real: hands on day
    #   20 go 10 -> 11.5 and the champion's own coins fall 146,907 -> 136,226.
    # * `animal_mix` +0.25 on SHEEP. The want is a per-kind cap on the day's
    #   grant, so a quarter of a log-share is enough to stop the cheaper cow
    #   closing the pasture on its own: 10.5 COW / 2.0 SHEEP becomes 6.5 / 5.0
    #   and wool sold goes 31 -> 73 units. Class A's own 9 / 4 sits between
    #   this and `hire_bias` alone (8.0 / 3.0), and the two settings are worth
    #   68,462 and 63,328 coins -- the mix is the better of the two and this
    #   rung takes it.
    # **v3** (2026-08-28, the day buckets): `hire_bias` is four numbers now, and
    # this rung is the reason the block exists -- see `_CLONE_HIRE_V3`.
    # **v3 measured** (2026-08-28, real engine, n=96, seed base 20260829): with
    # `_CLONE_HIRE_V3` the champion takes 153,084 / +105,874 off this rung
    # against 136,801 / +72,256 on v2 -- the ramp spends the rung's purse and
    # makes it *softer*.  The rung stays on the season-constant bias (a scalar
    # fills every bucket, byte-identical to v2); the buckets are for the
    # trained agent, which has the purse to use them.
    hire_bias=0.10, animal_mix={"SHEEP": 0.25},
)
#: What this rung actually plays, measured 2026-08-28 in the **real engine**
#: against `artifacts/theta_flow9_g15975_champion.npy`, 8 seeds x 2 seats,
#: profiled by `scripts/replay_profile.py`'s own columns. Kaggle class-A median
#: | **v1** (before the crew and herd-mix genes) | **v2** (this entry):
#:
#:     plant WHEAT      140 | 144 |  137    hands d5     3-4 |     3 |     7
#:     plant STRAWBERRY  36 |  46 |   47    hands d10     14 |     8 |     8
#:     plant MELON       18 |  20 |   18    hands d20     14 |    11 |    12
#:     plant CARROT       0 |   0 |    0    WATER ops  1,004 | 1,083 | 1,043
#:     plant TOMATO       0 |   0 |    0    sell WHEAT   431 |   454 |   443
#:     place GOOSE        0 |   0 |    0    sell STRAW   277 |   242 |   247
#:     place COW          9 |  10 |    7    sell MELON   105 |   115 |    79
#:     place SHEEP        4 |   2 |    5    sell MILK    220 |   118 |    76
#:     COOP built         0 |   0 |    0    sell WOOL    132 |    30 |    60
#:     quadrants 3 (d6,d10) | 3 |    3      sell FERT    235 |    39 |    41
#:     CARROT/TOMATO/EGG sold 0 | 0 | 0
#:     final money   94,162 | 65,975 | 67,513
#:     the champion's own coins in the same games: 135,435 | 137,047
#:
#: The board and the crop book cross; the **herd's output** still does not, and
#: the labour ramp crosses in the wrong direction. What the two genes bought
#: here is the herd's *shape* -- 10 : 2 against class A's 9 : 4 becomes 7 : 5,
#: and wool sold doubles -- and one more hand from day 20. What they did not buy
#: is class A's ramp, because `hire_bias` is one number for the season and the
#: cheap early hands are the ones it can afford: day 5 goes 3 -> 7 where the
#: field sits at 3-4, and day 10 does not move at all, because by then the
#: rung's *purse* and not the gene is the binding constraint (the field holds
#: 8,294 coins on day 10 to this planner's ~2,500). A ramp needs a bias that
#: reads the day; see the note above `_CLONE_BOOK`.
#:
#: `animal_share` is still one number for the whole season, so a rung that ends
#: on class A's 13 animals asks for that few every day and never gets the deep
#: early pasture that pays for 220 milk and 235 fertilizer (fertilizer is an
#: animal by-product here, so it follows the herd); a rung that asks for more
#: ends on 20+ animals and 5,000 coins of pasture it does not need.
#: `animal_share` -1.0 measures the other end of that trade: 19.5 COW / 3.5
#: SHEEP, milk 204, fertilizer 120, wheat 160 tiles, 80,566 coins. -2.0 is the
#: setting that lands the *board*, which is what the rung is for.
#: Class C is class A with the herd inverted, and inverting it takes more than
#: the want: MILK is dropped to 2.0, which is *under* the grow multiplier's
#: saturation (2.45x against WOOL's clipped 4x), so a sheep is worth 1.63 times
#: a cow per animal against 1.25 times the coins and `budget.grant` funds sheep
#: first until the wool curve flattens. Everything else is class A's -- the
#: replay says so: the class differs from A in its pasture and in the wheat and
#: strawberry it gives up to pay for it, and giving that up is what the deeper
#: `animal_share` does here.
#:
#: **The 12 : 6 ratio was the gene this file was missing**, and it is worth
#: recording what it cost to find that out, because the failure looked like a
#: tuning problem and was not one. `brain.decide` read *one* per-product grow
#: score for both halves of the herd decision: the want (`softmax` over the
#: three) and the planner's valuation (`_unit_ratio`, clipped at 4x). A 2 : 1
#: sheep-to-cow herd needs a want near 0.67 : 0.33, i.e. MILK about 0.7 under
#: WOOL -- but at that separation both scores are still past saturation, both
#: animals are worth 4x, and the cow's cheaper 400 coins take the whole pasture
#: (measured: 21 COW / 0 SHEEP). The only place the two effects balanced was
#: MILK under 2.71, where the want is already 99.5% sheep, so the v1 rung played
#: class C's *product* with an all-sheep herd rather than 12 : 6.
#:
#: `animal_mix` (2026-08-28, `policy` block `g8`) is that second gene: a bias on
#: the want alone, leaving the valuation the book wrote. It runs the balance the
#: other way round -- MILK stays *below* saturation so a sheep is worth 1.63
#: times a cow per animal against 1.25 times the coins, and `animal_mix` then
#: buys the cow's want back with +4.5 log-shares. That is a big number because
#: the two decisions genuinely pull apart: the book has to say "a cow is worth
#: less" for `budget.grant` to fund sheep first, and the want has to say "buy
#: some anyway" for the pasture not to end monotone. Measured in the real engine
#: against the champion, 4 seeds x 2 seats, `animal_mix` COW 0 / +4.0 / +4.5 /
#: +5.3 places 0.0 / 4.0 / **6.0** / 8.5 cows beside 9.5 / 14.0 / **12.0** / 9.0
#: sheep -- +4.5 is class C's herd to the animal -- and the champion's own coins
#: fall 155,573 / 122,252 / **112,426** / 128,186 across the same row. `+4.5`
#: costs this rung coins (52,238 -> 43,364) and buys the deepest suppression of
#: the champion anywhere in the ladder, which is the trade a rung is *for*.
#:
#: `hire_bias` stays 0 here, and that is measured too: at 0.10 the rung earns
#: more itself (63,502) and stops being the pressure -- the herd goes back to
#: 5.5 COW / 7.5 SHEEP and the champion recovers to 134,970.
#:
#: Measured the same way as `wheat_clone` above (8 seeds x 2 seats in the real
#: engine against the champion), class-C median | **v1** | **v2**:
#:
#:     place SHEEP     12 |  10 |  12      sell WOOL   254 |  56 | 117
#:     place COW        6 |   0 |   5      sell WHEAT  215 | 474 | 439
#:     place GOOSE      0 |   0 |   0      sell STRAW  184 | 174 | 198
#:     hands d10       14 |   3 |   7      sell MILK     - |   0 |  72
#:     hands d20       14 |  10 |  12      sell FERT     - |  13 |  76
#:     CARROT/TOMATO/EGG sold 0 | 0 | 0
#:     final money 109,979 | 49,000 | 62,732
#:     the champion's own coins in the same games: 154,057 | 124,529
#:
#: The herd is class C's to the animal, and it is the *rung* that got better for
#: it: +13,732 of its own coins and 29,528 off the champion's, out of one gene
#: and no other change. `hands d10` moving 3 -> 7 at `hire_bias` 0 is the same
#: point from the other side -- the crew is a consequence of the day's work, and
#: a pasture of 17 animals is work.
_WOOL_BOOK = dict(_CLONE_BOOK, MILK=2.0)
_NAMED["wool_specialist"] = dict(
    _NAMED["wheat_clone"],
    grow_bias=float(_bias_vec(_WOOL_BOOK).mean()),
    prod_bias=_WOOL_BOOK,
    animal_share=-0.7,
    hire_bias=0.0,
    animal_mix={"COW": 4.5},
)

#: **wheat_clone v4** (2026-08-30): the class-A rung retuned on its *herd*.
#:
#: The v2/v3 rung above is an honest imitation of class A's **board** and a
#: poor one of its **purse**: measured against the current champion
#: (`artifacts/theta.npy`, flow38_g25 + DROP + HORIZON_DROP) it ends on 62k
#: where the real leaderboard clones end on 95-130k, so a yardstick built on it
#: reads "the champion wins by 90k" against a field that takes 45% of its games.
#: v4 moves **one gene** -- `animal_share` -2.0 -> -1.0 -- and that is not
#: minimalism, it is what the sweep left standing.
#:
#: Measured in the real engine, `scripts/eval_vs_baselines.py --theta
#: artifacts/theta.npy --seed-base 20260830`, both seats, the rung's own mean
#: coins (= the champion's mean coins less the mean margin). n=48 for the two
#: finalists and the incumbent, n=16 for the screen:
#:
#:     rung                                 its coins  champion  margin    n
#:     wheat_clone (the entry above, hire .10) 61,927   151,701  +89,774   48
#:     dist/opponent_wheat_clone_v3 (v3 ramp)  46,114   151,054 +104,940   16
#:     **v4** animal_share -1.0                63,139   146,298  +83,159   48
#:     v4 + land_cap 2 + free_urgency 8        69,772   150,066  +80,294   48
#:
#: v4 is +1.2k of its own coins on the incumbent and **-6.6k of margin**: what
#: the deeper pasture mostly buys is the *champion's* coins, not the rung's.
#: The `land_cap` 2 row is the stronger rung by 6.6k and is **not** what ships:
#: it finishes on two quadrants, 114 wheat tiles and a nine-hand plateau from
#: day 10, which is a better opponent and a worse class A, and this entry is a
#: yardstick before it is an opponent.
#:
#: and the screen that chose it, every row on top of `wheat_clone` (n=16):
#:
#:     animal_share  -2.0 / -1.3 / **-1.0** / -0.5 /  0.0
#:                 59,177 / 61,902 / **70,090** / 51,448 / 54,376
#:     hold        -1.0 / 0.0 / +0.3      70,090 / 70,589 / 62,577
#:     land        -4.0 / -8.0 / -12.0    70,090 / 27,260 / 27,260
#:     land_afford  1.0 / 2.5            70,090 / 63,281
#:     land_cap     3 / 2                70,090 / 72,880
#:     free_urgency 4 / 8                70,090 / 70,938
#:     dev_weight   2.5 / 4.0            70,090 / 70,090   (already at the clip)
#:     crowd        0 / 3.0              70,090 / 45,391
#:     animal_mix   SHEEP+0.25 / none    70,090 / 72,373
#:     book         v2 / no MELON / STRAWBERRY 8.2
#:                                       70,090 / 60,694 / 49,937
#:     sell_bias    none / MELON+2, WHEAT-1, FERT-1
#:                                       70,090 / 48,866
#:     hire_bias    0.10 flat / (.10,.65,.5,-.55) / (0,.3,.3,0)
#:                                       70,090 / 43,827 / 47,046
#:
#: Three findings the table is worth keeping for:
#:
#: * **`animal_share` is single-peaked at -1.0 and the peak is the herd's
#:   *output*, not its size.** -2.0 and -1.0 both end on 12-17 animals; what
#:   changes is when they are placed, and therefore how many days they produce.
#: * **Every hire ramp still costs the rung 20-27k**, exactly as the v3 note
#:   below `_CLONE_BOOK` predicted, and for the reason it gives: `hire_bias`
#:   adds a *fake* gain to `plan` 1.5's enumeration, so it buys hands the day's
#:   work does not pay for out of a purse that is already empty. The deeper
#:   pasture buys the crew for free instead -- hands on day 20 go 12 -> 14 at
#:   `hire_bias` 0.10 unchanged, because a 17-animal pasture is work.
#: * **`land` cannot delay a purchase, only cancel it.** `head[1]` is read
#:   through a `tanh`, so -8 and -12 are the same saturated refusal and both
#:   rungs finish the season on their opening quadrant, earning 27k. Delaying
#:   the day-0 second quadrant to free early cash is not in this gene space;
#:   `land_afford` 2.5, the closest thing to it, only makes the rung poorer.
#:
#: What v4 actually plays, real engine against the champion, 8 seeds x 2 seats,
#: `scripts/replay_profile.py` medians. Kaggle class-A median | **v4** | (v2):
#:
#:     plant WHEAT      140 |  149 | (137)   hands d5      3-4 |    7 | ( 7)
#:     plant STRAWBERRY  36 |   40 | ( 47)   hands d10      12 |    9 | ( 8)
#:     plant MELON       18 |   17 | ( 18)   hands d20      14 |   14 | (12)
#:     plant CARROT       0 |    0 | (  0)   sell WHEAT    431 |  402 | (443)
#:     plant TOMATO       0 |    0 | (  0)   sell STRAW    277 |  191 | (247)
#:     place COW          9 | 10.5 | (  7)   sell MELON    105 |  100 | ( 79)
#:     place SHEEP        4 |    6 | (  5)   sell MILK     220 |  134 | ( 76)
#:     place GOOSE        0 |    0 | (  0)   sell WOOL     132 |   61 | ( 60)
#:     COOP built         0 |    0 | (  0)   sell FERT     235 |   72 | ( 41)
#:     quadrants  3 (d6,d10) | 3 (d0,d12)    CARROT/TOMATO/EGG sold 0 | 0
#:     money d10      8,294 |  233           final money 94,162 | 67,766
#:     the champion's own coins in the same games: 146,298 (n=48)
#:
#: **The board crosses and the purse does not, and the purse is one number:
#: `money_d10` = 233 coins.** Class A fields 12 hands on day 10 holding 8,294
#: coins; this rung holds two hundred and can afford nine. That is not
#: `hire_bias` -- 12 hands is a 376-coin bill plus a 609-coin `cash_reserve`,
#: which the rung could pay if it had a thousand coins on the day. It is the
#: whole build-out arriving on credit the season has not earned yet: the second
#: quadrant at dawn on day 0 (`LAND_PRICES` 1,000), the third on day 12
#: (2,000), and sixteen or seventeen animals at 400-500 each, against 2,585
#: coins of revenue in the first eight days.
#: Every animal placed late is an animal that produces for half a season, which
#: is why milk, wool and fertilizer come in at 60% / 46% / 31% of class A's on a
#: herd that is the *right size*. Closing it needs revenue before day 8 -- a
#: sell side that drips rather than dumps (see the `mixed_ranch` note above) or
#: a planner that stages the build-out -- and neither is a knob in this file.
_NAMED["wheat_clone_v4"] = dict(
    _NAMED["wheat_clone"],
    animal_share=-1.0,
)

#: The value of every knob added on 2026-08-28 at which it decodes to exactly
#: what the file decoded before it existed: `animal_sharp` 0 is the head[2] the
#: eight older rungs already carried, `dev_weight` 0 is the router's x1, `sat` 0
#: is `brain.decide`'s shipped absorption gate, and an empty book writes no
#: staircase weights at all. Filled in below rather than typed into eight
#: entries, so "every rung names every knob" (`tests/test_archetypes.py`) stays
#: true without eight chances to typo an inert value into a live one.
#:
#: The 2026-08-30 crew-ramp knobs join it on the same terms: `crew_target` 0 is
#: `relu(tanh(0)) == 0` hands, which makes the whole block inert whatever
#: `crew_mid` and `crew_steep` decode to, and `animal_defer` 0 leaves the
#: deferral scale at `plan.DEFER_ONE` (x1). So every rung and every drawn
#: ladder is byte for byte the one it was, and `sample_archetype` draws no new
#: numbers -- a seed's ladder does not move.
_INERT = dict(animal_sharp=0.0, dev_weight=0.0, sat=0.0,
              prod_bias={}, sell_bias={}, hire_bias=0.0, animal_mix={},
              crew_target=0.0, crew_mid=0.0, crew_steep=0.0, animal_defer=0.0)
for _entry in _NAMED.values():
    for _knob, _value in _INERT.items():
        _entry.setdefault(_knob, _value)

#: The order `Trainer` fills its archetype slots in. Beyond the last name the
#: slots are drawn from `sample_archetype`.
#:
#: `wheat_clone`, `wool_specialist` and `wheat_clone_v4` are **appended**, so
#: every existing `--n-archetypes` selects exactly the ladder it selected before
#: (and `kagg2_proxy` keeps slot 8, which `PROXY_NAME` and the handicap row
#: index by name but the tests pin by position).
NAMES = ("expander", "rusher", "rancher", "patient_grower", "value_farmer",
         "squeeze_seller", "staple_bulk", "mixed_ranch", "kagg2_proxy",
         "wheat_clone", "wool_specialist", "wheat_clone_v4")

#: The rung that opens on a handicap. `Trainer` looks this name up in its own
#: archetype labels; a run whose `--n-archetypes` stops short of it simply has
#: no handicapped rung.
PROXY_NAME = "kagg2_proxy"

#: `(nquad, money)` meaning "no handicap at all" -- the engine's own day 0, and
#: the default for every rung including the proxy, so an unflagged run is the
#: run that was there before this file grew a ninth entry.
NO_HANDICAP = (1, spec.STARTING_MONEY)

#: The fitted handicap: the opening `kagg2_proxy` is *meant* to be played from.
#:
#: It is a **measurement, not a constant**. The rung runs this planner, so what
#: it earns -- and therefore how much of `kagg2`'s suppression it reproduces --
#: moves whenever the planner does, exactly as the coin figures above do. The
#: recipe is in `docs/superpowers/plans/2026-08-26-win-objective.md` §3.3:
#: play the incumbent against candidate handicaps on the fixed `abs` seeds,
#: play the same incumbent against `kagg2` in the real engine, and take the
#: handicap whose in-sim **suppression** -- own coins against the least
#: suppressive rung minus own coins here -- is ~80% of the real one. Re-fit it
#: after every planner merge, in the same pass that re-tunes the rungs above.
#:
#: **Fitted 2026-08-26** on the land-valuation / mixed-herd / drain-feature
#: planner, incumbent `artifacts/p2s0/champion.npy`, 128 in-sim games per point
#: (the 64 fixed `abs` seed pairs x 2 seats) against 48 real-engine games
#: (12 seeds x 2 seats x 2 opponents, `--seed-base 20260825`).
#:
#: Real engine, the thing being reproduced:
#:
#:     vs kagg2    mine 53,905  theirs 144,536  margin -90,631 +-3,287  win 0/24
#:     vs starter  mine 85,056                                          win 24/24
#:     real suppression = 85,056 - 53,905 = 31,151 coins
#:
#: In sim the least-suppressive rung is `value_farmer` cold at 90,510 own
#: coins, so suppression is `90,510 - ours`:
#:
#:     money      its coins   our coins    margin   % of kagg2's
#:     cold 3,000    67,857      76,222    +8,365       46
#:     70,000       108,749      70,656   -38,092       64
#:     80,000       117,613      68,335   -49,278       71
#:     85,000       124,540      67,880   -56,660       73
#:     87,000       126,910      64,981   -61,928       82   <- fitted
#:     90,000       131,349      62,149   -69,200       91
#:     100,000      143,252      52,986   -90,266      120
#:
#: Three things this settles, and none of them is what the plan predicted:
#:
#: * **Free land is not a handicap on this planner, it is a tax.** The plan's
#:   fitted point was `3:20000` and it now measures 27% -- *weaker* than the
#:   cold rung's 46%, because `land_cap` 3 means the rung would have bought
#:   those quadrants anyway and being handed them on day 0 spreads a crew of
#:   one over 75 tiles. At an equal purse, one quadrant beats two: `1:100000`
#:   holds us to 52,986 against `2:100000`'s 49,162 while earning more itself.
#:   The handicap is therefore money only, and the rung buys its own board.
#: * **The response is steep and the shelf is flat.** 85k -> 90k moves the
#:   suppression 73% -> 91%, and 86k / 87k / 88k measure 82.3 / 81.9 / 82.6 --
#:   inside each other's noise (own-coin SE is ~1,150 over 128 games, so a
#:   suppression point is worth ~0.4%). 87,000 is the middle of that shelf, and
#:   nothing finer than ~2,000 coins is measurable.
#: * **The residual is on the margin, not the level.** At 87,000 the rung takes
#:   126,910 against kagg2's 144,536 (0.88) and holds us to 64,981 against
#:   53,905 (1.21), for a margin of -61,928 against -90,631 (0.68) at the same
#:   0/128 win rate. That is the same sim-vs-engine level offset the diagnosis
#:   carries; calibrating the margin to 1.00 would take ~100,000 and 120% of
#:   the suppression, which is a harder game than the one being played.
PROXY_HANDICAP = (1, 87_000)

#: Coins an archetype must earn against the zero theta to be allowed into the
#: ladder. `Trainer` enforces it -- see its `_probe_archetypes`.
MIN_COINS = 10_000.0

#: The **second** liveness floor, and the one that catches the opposite
#: failure. `MIN_COINS` asks "can this rung earn at all"; a rung can clear it
#: and still be a free win, because it collapses the moment a real policy is on
#: the board. Measured 2026-08-25, `staple_bulk` earned 17,560 coins against
#: the zero theta and **838** against the then-incumbent -- it kept 4.8% --
#: while being 1/8 of the yardstick and contributing its single largest
#: own-coin term.
#:
#: **It does not fire today, and that is the measurement, not an omission.**
#: Re-measured 2026-08-26 on this planner, `p2s0/champion` against all nine
#: rungs (probe coins vs the zero theta, then opponent coins on the 128-game
#: yardstick):
#:
#:     expander 1.28   rusher 0.95   rancher 1.01   patient_grower 0.73
#:     value_farmer 0.96   squeeze_seller 0.74   staple_bulk 1.01
#:     mixed_ranch 0.95   kagg2_proxy 1.01
#:
#: Nothing is under 0.73. The rung that used to fold does not: the land
#: valuation put `staple_bulk` on three quadrants and 16,566 coins, and it now
#: keeps all of them with a policy on the board. What changed is the
#: *incumbent* -- this one earns 85k against `starter` where the pre-merge one
#: earned 132k -- so the floor is a guard against a failure this ladder can
#: still reach and currently does not. 0.25 keeps the separation the 2026-08-25
#: measurement showed (a free win at 0.05 against a live rung at 0.76) with
#: room under every number above.
#:
#: `Config.collapse_floor` defaults to 0 (off, i.e. today's behaviour); this is
#: the value to set it to. The keep fraction is reported either way -- see
#: `AbsReport.keep`.
COLLAPSE_KEEP = 0.25

#: Rungs the yardstick plays and the gradient never sees: `(label, name,
#: (nquad, money))`. They test two different kinds of transfer, and neither is
#: ever in `Trainer.candidates()` or in any number selection reads.
#:
#: * `mixed_ranch` one handicap level above the trained proxy -- **handicap**
#:   transfer. If the policy is learning "beat a rich opponent" rather than a
#:   strategy, its margin here lags the trained rung's as the run progresses.
#:   Measured 2026-08-26 against `p2s0/champion`: 152,101 / 48,456 / -103,645,
#:   0/128 -- a clear step past the trained rung's -61,928.
#: * `value_farmer` at the trained proxy's own handicap -- **strategy**
#:   transfer: the same opening on a different book. Measured 98,268 / 65,836 /
#:   -32,431 at 2/128 wins, i.e. it beats us too, but through a crop book
#:   rather than a herd.
#:
#: Today's holdout is on *seeds* and shows no overfitting at all (`abs_holdout`
#: tracks `abs_coins` to a mean 1.1% across 30 checkpoints), which is exactly
#: why the missing holdout is the opponent one.
#:
#: Both levels are functions of `PROXY_HANDICAP` and move with it.
HOLDOUT_RUNGS = (
    ("mixed_ranch@1:110000", "mixed_ranch", (1, 110_000)),
    (f"value_farmer@1:{PROXY_HANDICAP[1]}", "value_farmer", PROXY_HANDICAP),
)


def named(name: str) -> dict:
    return dict(_NAMED[name])


def sample_archetype(rng: np.random.Generator) -> dict:
    """A random strategy: every knob uniform over a range wide enough that
    each binary decision lands on both sides across a handful of draws."""
    # `land` and `land_afford` are sized together: the affordability ratio is
    # clipped to [-1, 4] in brain.decide, so land + 4 * land_afford must be
    # able to go negative often enough that the sampled ladder contains
    # non-expanders too. Since the bias became coins that means "demands
    # margin before it buys" rather than "refuses"; `land_cap` is the knob
    # that refuses, and the two are drawn independently on purpose.
    #
    # `hold` and `press` reach well into the positive half now. Before
    # 2026-08-25 every named archetype and almost every draw held at or below
    # zero, i.e. sold at any price at all, so the trained policy never met an
    # opponent that competed with it for a *good* price -- only for a sale.
    # `grow_bias` never goes below zero: it is the level of the grow
    # multiplier, and a draw that switched growing off would be a dead rung.
    #
    # `crowd` never goes below zero either, for a different reason: a negative
    # crowding term is *positive* feedback -- the more of a product the board
    # already makes, the more the softmax wants -- which collapses onto one
    # crop and one animal kind, the very behaviour the knob exists to break.
    # `land_cap` is drawn over the boards a season can end on, so two thirds
    # of the sampled rungs stop short of the whole 10x10 board the way `kagg2`
    # does -- and, since the land valuation, the way the profitable ones do:
    # of the five rungs measured both ways on 2026-08-26 (`expander`,
    # `rusher`, `rancher`, `staple_bulk`, `mixed_ranch`), every one earned
    # more capped at 2 or 3 quadrants than at the whole board.
    u = lambda lo, hi: float(rng.uniform(lo, hi))
    return dict(
        land=u(-6.0, 6.0), dev=u(-1.0, 6.0),
        animal_share=u(-6.0, 3.0), crop_sharp=u(-2.0, 4.0),
        value_tilt=u(-3.0, 3.0), mid_tilt=u(-2.0, 4.0),
        grow_bias=u(2.0, 8.0), hold=u(-6.0, 6.0), press=u(-1.0, 3.0),
        land_afford=u(0.0, 1.0), free_urgency=u(0.0, 4.0),
        crowd=u(0.0, 6.0), land_cap=float(rng.integers(2, _N_QUAD + 1)),
        # The 2026-08-28 knobs (both batches: the book/staircase knobs and the
        # crew/herd-mix pair) are named but **not drawn**, and that is the
        # whole point of `_INERT`: they are handed their inert values, so every
        # rung a seed drew before they existed is still the rung it draws now,
        # byte for byte. Widening the sampler into a space whose liveness has
        # never been probed would put unmeasured rungs in the yardstick and
        # change every existing run's drawn ladder in the same commit -- two
        # changes, one flag, and no way to tell which moved a curve.
        **_INERT)
