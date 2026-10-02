"""Fire schedules and coin values, closed-form over the engine's tables.

PLANNER_V3_1 sections 0.2, 0.6 and 0.11 all need the same three questions
answered per tile without a loop: when does this animal or crop produce next,
how many monetizable productions are left, and what is one more input worth.
Everything here is int32 elementwise arithmetic so it vectorises over the 100
tiles and traces shape-static on both backends.

Calendar conventions (see the plan's engine facts):

* A production fire at the end of day `e` is harvestable on `h = e + 1`;
  a harvest on day `h` reaches the shed at eod `h` and sells on `h + 1`, so
  it is monetizable iff `h <= pay_day()`. `pay_day` is `ops.LAST_SHED_DAY`
  until `plan.HORIZON_DROP_ON` is set, and `LAST_SHED_DAY + 1` after -- see
  the switch's own block in `plan.py` for the derivation.
* An animal placed on `t_day` with `first`/`interval` fires on harvest days
  `t_day + first + k * interval`, k >= 0. An ongoing crop does the same but
  fires at most `CROP_MAX_YIELD` times.

Prices are today's hour-0 quotes -- the Phase-1 projection. Opponent impact
and multi-day drift are [LEARNED] and arrive with the Phase-2 genome.
"""

from __future__ import annotations

from .. import spec
from . import ops as O


#: The module that owns the horizon switch. `plan` binds itself here at import
#: time (see `plan.HORIZON_DROP_ON`), because this module cannot import it: the
#: dependency runs the other way. A *lazy* `from . import plan` inside
#: `pay_day` is not the alternative -- it is a bug. The benchmark harness hides
#: this repo's `kagg3` from `sys.modules` and `src` from `sys.path` for the
#: length of every game seated against a packaged agent
#: (`scripts/eval_vs_baselines.py::_vendored_imports`, whose docstring states
#: the invariant: nothing under `kagg3/core` may import lazily), so a runtime
#: import here resolves to the *packaged* planner or raises, and the agent
#: forfeits the game. Measured: 12 games at 3,000 coins, the starting purse.
_PLAN = None


def pay_day():
    """int: the last day whose work still turns into coins [PLANNER_V3_1 0.4].

    Two different facts wear the same number and the DROP module separates
    them. `ops.LAST_SHED_DAY` = 28 is the last day with an **end-of-day**: the
    last night the engine banks a unit's inventory into the shed for free. The
    horizon every terminal rule actually wants is the last day whose **payoff
    can still be sold**, and those coincide only while day 29 is a dead day.

    With `plan.DROP_ON` the day-29 chain closes inside the day --
    HARVEST/COLLECT, walk to a shed-access tile, DROP, and `SELL_TURNS[-1]`
    sells what the DROP banked, because units act before their turn's market.
    So a day-29 harvest monetizes and the horizon is 29. `plan.HORIZON_DROP_ON`
    is the switch that moves it; OFF this returns `ops.LAST_SHED_DAY` and every
    expression below is the integer it always was.

    Reads the switch off `_PLAN`, which `plan` binds at import time; before
    that binding (only possible while `plan` itself is still executing) the
    horizon is the un-switched one.
    """
    return O.LAST_SHED_DAY + (1 if _PLAN is not None and _PLAN.HORIZON_DROP_ON else 0)


def fires_between(xp, t_day, first, interval, lo_day, hi_day):
    """Number of harvest days `h = t_day + first + k*interval` (k >= 0) with
    `lo_day <= h <= hi_day`."""
    base = t_day + first
    lo = xp.maximum(lo_day, base)
    k0 = (lo - base + interval - 1) // interval                # lo >= base: non-negative
    k1 = xp.where(hi_day >= base, (hi_day - base) // interval, -1)
    return xp.maximum(k1 - k0 + 1, 0)


def fires_on(xp, t_day, first, interval, h):
    """Whether a fire lands on harvest day `h`."""
    d = h - (t_day + first)
    return (d >= 0) & (d % interval == 0)


def next_fire_after(xp, t_day, first, interval, day):
    """Harvest day of the first fire whose end-of-day is strictly after
    today's -- the fire a CARE emitted today pays on (a fire-day care banks
    toward the *next* fire; so does a care on a quiet day)."""
    base = t_day + first
    lo = xp.maximum(day + 2, base)
    k = (lo - base + interval - 1) // interval
    return base + k * interval


def crop_fires_on(xp, t_day, crop, h):
    """`fires_on` for an ongoing crop, which fires at most CROP_MAX_YIELD times."""
    first = xp.asarray(spec.CROP_FIRST_YIELD_DAY)[crop]
    interval = xp.maximum(xp.asarray(spec.CROP_INTERVAL)[crop], 1)
    mxy = xp.asarray(spec.CROP_MAX_YIELD)[crop]
    d = h - (t_day + first)
    return (d >= 0) & (d % interval == 0) & (d // interval <= mxy - 1)


def animal_value(xp, price, t_day, t_yield, t_favail, a, day):
    """Remaining sellable production of a standing animal of kind `a`, in
    coins at today's prices: the units it holds plus every fire still
    harvestable by `pay_day`, times its product's price, plus one
    fertilizer per remaining day (today's if already available), times the
    fertilizer price. Assumes it is fed and harvested; that is the caller's
    rationing question, not this function's.

    Prices are today's hour-0 quotes -- the Phase-1 projection. Opponent
    impact and multi-day drift are [LEARNED] and arrive with the Phase-2
    genome.
    """
    first = xp.asarray(spec.ANIMAL_FIRST_YIELD_DAY)[a]
    interval = xp.asarray(spec.ANIMAL_INTERVAL)[a]
    prod = xp.asarray(spec.ANIMAL_PRODUCT)[a]
    # Today's stock sells if today can still be sold; a fire on harvest day
    # `h` sells if `h` can. Both read the same horizon [0.4].
    hi = pay_day()
    sellable_today = (day <= hi).astype(xp.int32)
    units = t_yield * sellable_today + fires_between(xp, t_day, first, interval, day + 1, hi)
    # One fertilizer per remaining day: `refresh_animals` re-arms `t_favail` at
    # every end-of-day, so the collections left are days `day + 1 .. hi`.
    fert = xp.maximum(hi - day, 0) + t_favail * sellable_today
    return units * price[prod] + fert * price[spec.I_FERT]


def fert_marginal_value(xp, price, t_day, t_yield, crop, day, harvest_age):
    """Coins one fertilizer application today adds on this tile [0.11].

    Fertilizer is active on day, day+1, day+2. Ongoing crop: +1 unit per fire
    in that window that is watered at its eod (the planner waters fertilized
    crops on fire days) and still monetizable, capped at the crop's last
    fire. One-time crop: each in-window watering in the fertilized days adds
    +2 instead of +1, clipped at CROP_MAX_YIELD against the yield the
    remaining unfertilized waterings would reach anyway -- so a crop that
    saturates without fertilizer (melon watered daily) is worth 0, and the
    day-28 same-day FERTILIZE->WATER->HARVEST chain is worth at most +1.

    Ongoing crops ignore `t_yield`: the planner harvests a crop whenever it
    holds units, so a fire is never clipped by CROP_MAX_YIELD in practice.

    Two preconditions the caller must enforce -- the arithmetic does not
    check them and a violation over-values the tile:

    * `t_fert < day`: no application is already active. Fertilizing a tile
      covered through `day + 1` or later extends coverage by at most one
      day, but `n_ong` and `n_fert` price the whole three-day window, so a
      redundant application is over-valued by up to 2 units. `plan.py`'s
      `want_fert` mask already carries this condition.
    * one-time branch only, `t_water == 0` today: `w_lo` counts today as an
      available watering, and the engine allows one watering per day, so an
      already-watered tile cannot buy today's +2. Always true at hour 0 --
      the end of day resets `watered_today`.

    Prices are today's hour-0 quotes -- the Phase-1 projection. Opponent
    impact and multi-day drift are [LEARNED] and arrive with the Phase-2
    genome.
    """
    ongoing = xp.asarray(spec.CROP_ONGOING)[crop]
    first = xp.asarray(spec.CROP_FIRST_YIELD_DAY)[crop]
    interval = xp.maximum(xp.asarray(spec.CROP_INTERVAL)[crop], 1)
    mxy = xp.asarray(spec.CROP_MAX_YIELD)[crop]
    ws = xp.asarray(spec.CROP_WINDOW_START)[crop]

    base = t_day + first
    last_h = base + (mxy - 1) * interval
    hi = xp.minimum(xp.minimum(day + 3, pay_day()), last_h)
    n_ong = fires_between(xp, t_day, first, interval, day + 1, hi)

    d_h = t_day + harvest_age
    w_lo = xp.maximum(day, t_day + ws)
    n_water = xp.maximum(d_h - w_lo + 1, 0)                             # in-window waterings left
    n_fert = xp.maximum(xp.minimum(day + 2, d_h) - w_lo + 1, 0)         # ... of which fertilized
    gain_one = xp.minimum(mxy, t_yield + n_water + n_fert) - xp.minimum(mxy, t_yield + n_water)
    gain_one = xp.where(d_h <= pay_day(), gain_one, 0)

    units = xp.where(ongoing == 1, n_ong, gain_one)
    return units * price[crop]


def new_plant_units(xp, crop, day):
    """int: units a crop planted today yields by `pay_day`, unfertilized
    and watered on every in-window day; 0 if it cannot mature in time.

    The `t_day == day` case of `remaining_plant_units`, which it delegates to
    rather than restating: two copies of one recurrence drift."""
    return remaining_plant_units(xp, crop, day, day)


def remaining_plant_units(xp, crop, t_day, day):
    """int: units a tile planted on `t_day` still delivers to the shed after
    `day` -- a one-time crop keeps everything until its (clamped) harvest, an
    ongoing crop only its fires after today. `new_plant_units(c, d)` is the
    `t_day == day` case."""
    ongoing = xp.asarray(spec.CROP_ONGOING)[crop]
    first = xp.asarray(spec.CROP_FIRST_YIELD_DAY)[crop]
    interval = xp.maximum(xp.asarray(spec.CROP_INTERVAL)[crop], 1)
    mxy = xp.asarray(spec.CROP_MAX_YIELD)[crop]
    sat = xp.asarray(spec.CROP_SATURATE_AGE)[crop]
    ws = xp.asarray(spec.CROP_WINDOW_START)[crop]
    hi = pay_day()
    can = t_day + first <= hi
    # `plan._derive`'s harvest clamp, restated on a tile that may not exist
    # yet. Melon is the only crop whose saturation age differs from its
    # max-yield day, and its `one` is CROP_MAX_YIELD either way -- this line
    # keeps the two schedules agreeing rather than changing a value.
    harvest_age = xp.clip(hi - t_day, first, sat)
    one = xp.minimum(mxy, 1 + xp.maximum(harvest_age - ws + 1, 0))
    last_h = t_day + first + (mxy - 1) * interval
    ong = fires_between(xp, t_day, first, interval, day + 1, xp.minimum(hi, last_h))
    return xp.where(can, xp.where(ongoing == 1, ong, one), 0)


def crop_remaining_value(xp, price, t_day, t_yield, crop, day, harvest_age):
    """Coins a standing crop will still sell if kept alive and watered: a
    one-time crop's clipped units at its harvest day (0 past the horizon), an
    ongoing crop's held units plus the fires left before its last."""
    ongoing = xp.asarray(spec.CROP_ONGOING)[crop]
    first = xp.asarray(spec.CROP_FIRST_YIELD_DAY)[crop]
    interval = xp.maximum(xp.asarray(spec.CROP_INTERVAL)[crop], 1)
    mxy = xp.asarray(spec.CROP_MAX_YIELD)[crop]
    ws = xp.asarray(spec.CROP_WINDOW_START)[crop]
    d_h = t_day + harvest_age
    w_lo = xp.maximum(day, t_day + ws)
    n_water = xp.maximum(d_h - w_lo + 1, 0)
    hi = pay_day()
    one = xp.where(d_h <= hi, xp.minimum(mxy, t_yield + n_water), 0)
    last_h = t_day + first + (mxy - 1) * interval
    ong = t_yield + fires_between(xp, t_day, first, interval, day + 1, xp.minimum(hi, last_h))
    return xp.where(ongoing == 1, ong, one) * price[crop]
