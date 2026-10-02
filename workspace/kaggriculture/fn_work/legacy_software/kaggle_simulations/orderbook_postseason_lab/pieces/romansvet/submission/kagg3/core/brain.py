"""Features in, Macro out. Array-agnostic, so the JAX sim and the numpy
submission run literally the same code path.

Feature scaling is fixed and hand-chosen (divide by a plausible maximum) rather
than learned or normalised online -- an online normaliser would be extra state
to ship and another chance for train/serve divergence, and ES does not need
whitened inputs the way SGD does.
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np

from .. import spec
from . import ops as O
from . import plan as P
from . import policy as PO
from . import valuation as VAL

NP_ = spec.N_PRODUCTS

# Static per-product columns, precomputed once.
_BASE = np.array([spec.DEFAULT_MARKET_PARAMS[n]["base"] for n in spec.PRODUCTS], np.float32)
_T = np.array([spec.DEFAULT_MARKET_PARAMS[n]["T"] for n in spec.PRODUCTS], np.float32)
_BT = np.array([spec.DEFAULT_MARKET_PARAMS[n]["below_target"] for n in spec.PRODUCTS], np.float32)
_AT = np.array([spec.DEFAULT_MARKET_PARAMS[n]["above_target"] for n in spec.PRODUCTS], np.float32)

# Days from planting/placing to the first yield, and steady-state units per tile
# per day, for each of the nine market products (fertilizer comes from animals).
_FIRST = np.zeros(NP_, np.float32)
_RATE = np.zeros(NP_, np.float32)
for _c in range(spec.N_CROPS):
    _FIRST[_c] = spec.CROP_FIRST_YIELD_DAY[_c]
    _den = max(int(spec.CROP_MAX_YIELD_DAY[_c]), 1)
    _RATE[_c] = float(spec.CROP_MAX_YIELD[_c]) / _den
for _a in range(spec.N_ANIMALS):
    _pi = int(spec.ANIMAL_PRODUCT[_a])
    _FIRST[_pi] = spec.ANIMAL_FIRST_YIELD_DAY[_a]
    _RATE[_pi] = 1.0 / float(spec.ANIMAL_INTERVAL[_a])
_FIRST[spec.I_FERT] = 1.0
_RATE[spec.I_FERT] = 1.0

# Units of each product the town removes per day once every shop is counted:
# each shop instance ticks 6 times a day (24 turns / interval 4), the town centre
# once.
_SHOP_DAILY = (spec.SHOP_CONSUME.astype(np.float32)
               * (spec.TURNS_PER_DAY // spec.SHOP_SELL_INTERVAL))
_CENTER_DAILY = spec.TOWN_CENTER_CONSUME.astype(np.float32)

#: Units one *undrawn* shop removes per day, averaged over the eight kinds.
#: `sim/eod.unlock_shop` picks the kind uniformly, so a shop the calendar will
#: unlock but the town has not drawn yet is worth the mean row of
#: `SHOP_CONSUME` and not any particular one.
_MEAN_SHOP_DAILY = _SHOP_DAILY.mean(axis=0)

#: Shops standing at the start of day d: one every `SHOP_UNLOCK_INTERVAL` days
#: from zero, capped at `MAX_SHOP_INSTANCES`. `sim/eod.unlock_shop` fires at the
#: end of day d-1 when `d % SHOP_UNLOCK_INTERVAL == 0`, so the count is a
#: constant of the calendar -- which is what lets the drain horizon be priced on
#: days whose shops do not exist yet. That is most of the days a planting
#: decision is made for: the board is committed by day 10 and the eighth shop
#: only opens on day 24.
_SHOPS_ON_DAY = np.minimum(np.arange(spec.N_DAYS) // spec.SHOP_UNLOCK_INTERVAL,
                           spec.MAX_SHOP_INSTANCES).astype(np.float32)


#: Tiles one quadrant holds. A quadrant is unlocked whole (`_do_buy_land`
#: rewrites every LOCKED tile of it at once) and the board starts with exactly
#: NW unlocked, so "locked tiles, capped at a quadrant" is the next quadrant's
#: tile count without ever naming which tiles they are -- see `n_free_slots`.
LAND_TILES = spec.N_TILES // 4

#: Default for `PolicyObs`' opponent-clock fields -- see the note on them.
#: Module-level and read-only: nothing in this file writes a `PolicyObs` array.
_NO_TILES = np.zeros(spec.N_TILES, np.int32)


class PolicyObs(NamedTuple):
    """Everything the network is allowed to see, for one seat.

    **The tile arrays carry no canonical tile order** [LAW]: the simulator
    passes raw board order (`sim/rollout.py::policy_obs`) and the submission
    passes the serpentine `DayView` order it already has to hand
    (`scripts/package_submission.py`). Every use of `kind`, `occ`, `t_day` and
    `t_yield` below is therefore a whole-array reduction and must stay one --
    anything that indexes a per-tile table (`spec.TILE_QUAD`, `plan.SERP_QUAD`)
    against them reads a different board in training than in the submission,
    which is a silent train/serve divergence rather than an error.
    """
    day: object
    money: object
    opp_money: object
    kind: object          # int[100]
    occ: object
    opp_kind: object
    opp_occ: object
    t_day: object
    t_yield: object
    shed: object          # int[12]
    seeds: object         # int[5]
    nquad: object
    opp_nquad: object
    mkt_inv: object       # int[9]
    price: object         # int[9]
    shops: object         # int[8]
    # The opponent's planting / placement dates and standing yield. Public
    # board state, exactly as `kind`/`occ` are -- `observation["farms"][q]
    # ["tiles"]` carries `planted_day`, `placed_day` and `yield_units` for both
    # seats and only `observation["private"]` (shed, seeds) is withheld. Read
    # by `production_forecast` / `forward_value` and by nothing else.
    #
    # Appended with a default so every construction site that predates them
    # still builds: a caller that does not know the opponent's clock gets a
    # board of zeros, which `production_forecast` reads as "placed on day 0"
    # rather than crashing or silently reindexing an existing field. The two
    # seats that matter both pass the real thing (`sim/rollout.policy_obs`,
    # `scripts/package_submission.py`); a fixture or unit test that does not is
    # measuring our own board's forecast, which is the half it exercises.
    opp_t_day: object = _NO_TILES      # int[100]
    opp_t_yield: object = _NO_TILES
    # Previous dawn's shared market inventory. Runtime/simulator glue supplies
    # int32[9]; None is the legacy/day-0 convention and decodes to zero draw.
    prev_mkt_inv: object = None


def market_momentum(xp, obs: PolicyObs):
    """float32[9, 1]: normalized previous-to-current dawn market draw."""
    if obs.prev_mkt_inv is None:
        return xp.zeros((spec.N_PRODUCTS, 1), dtype=xp.float32)
    previous = xp.asarray(obs.prev_mkt_inv).astype(xp.float32)
    current = obs.mkt_inv.astype(xp.float32)
    return ((previous - current) / xp.asarray(_T))[:, None]


def _producing(xp, kind, occ):
    """Tiles currently producing each of the nine products."""
    is_pl = kind == spec.KIND_PLANT
    is_an = ((kind == spec.KIND_COOP) | (kind == spec.KIND_PASTURE)) & (occ >= 0)
    cols = []
    for c in range(spec.N_CROPS):
        cols.append(xp.sum((is_pl & (occ == c)).astype(xp.float32)))
    per_animal = [xp.sum((is_an & (occ == a)).astype(xp.float32))
                  for a in range(spec.N_ANIMALS)]
    for a in range(spec.N_ANIMALS):                       # EGG, MILK, WOOL
        cols.append(per_animal[a])
    cols.append(sum(per_animal))                          # FERTILIZER
    return xp.stack(cols)


def n_free_slots(xp, obs: PolicyObs, land=None):
    """Tiles the planner will treat as developable today.

    With `land` (an int 0/1, not None) the next quadrant's still-LOCKED tiles
    count too [M1]: the engine unlocks a bought quadrant inside the market
    phase of the purchase turn, so `plan._derive` develops it the same day, and
    the head has to size development against the enlarged board or
    `plant_target` can never reach the new tiles. `land=None` returns today's
    answer bit for bit, which is what `features` below wants -- the *feature*
    vector must not move.

    The prospective tiles are counted, never located: quadrants unlock whole,
    so the locked tiles capped at one quadrant's worth are exactly the next
    quadrant's, and no per-tile quadrant table is read. That is a requirement
    and not a simplification -- `PolicyObs`'s tile arrays are in raw order for
    the simulator and serpentine order for the submission, so masking them with
    `spec.TILE_QUAD` would open the two seats' training and serving decisions
    onto different quadrants.

    NOTE: a one-time-harvest crop past its yield window (the `harvest_one`
    branch below) counts as a free slot here. This has tripped two test
    fixtures already -- test fixtures should plant an ongoing crop on filler
    tiles that are meant to stay occupied.
    """
    is_pl = obs.kind == spec.KIND_PLANT
    c = xp.clip(obs.occ, 0, spec.N_CROPS - 1)
    ong = xp.asarray(spec.CROP_ONGOING)[c]
    sat = xp.asarray(spec.CROP_SATURATE_AGE)[c]
    first = xp.asarray(spec.CROP_FIRST_YIELD_DAY)[c]
    age = obs.day - obs.t_day
    # Same clamp as `plan._derive`'s `harvest_one`, and it has to stay the same
    # one: this counts the tiles that harvest frees today. `VAL.pay_day()` is
    # the horizon both read (`plan.HORIZON_DROP_ON`).
    harvest_age = xp.clip(VAL.pay_day() - obs.t_day, first, sat)
    harvest_one = is_pl & (ong == 0) & (age >= harvest_age)
    free = (obs.kind == spec.KIND_EMPTY) | (obs.kind == spec.KIND_WEED) | harvest_one
    if P.EXPIRY_SLOT_ON:
        free = free | P._expiry_slots(xp, obs)
    if P.LATE_EXEC_ON:
        free = free | P._final_slots(xp, obs)
    n = xp.sum(free.astype(xp.int32))
    if land is None:
        return n
    locked = xp.sum((obs.kind == spec.KIND_LOCKED).astype(xp.int32))
    return n + land.astype(xp.int32) * xp.minimum(locked, LAND_TILES)


def daily_town_demand(xp, obs: PolicyObs):
    """float32[9]: units the town removes per whole day at *today's* shop set.

    Six shop ticks (24 turns / interval 4) plus the town centre's one of
    everything but fertilizer -- `core/projector.daily_town_units` in floats.
    """
    return obs.shops.astype(xp.float32) @ xp.asarray(_SHOP_DAILY) + xp.asarray(_CENTER_DAILY)


def expected_drain(xp, obs: PolicyObs, demand):
    """float32[9]: units the town will consume from today to the last day.

    Today's shops drain `demand` every remaining day; on top of that the
    calendar unlocks one more shop every `SHOP_UNLOCK_INTERVAL` days up to
    eight, and each of those has not been drawn yet, so it is priced at
    `_MEAN_SHOP_DAILY`. At day 0 this reproduces the measured season drain of
    the reimplementation exactly -- wheat 525, carrot 327, tomato 228,
    strawberry 426, melon 30, egg 228, milk 327, wool 228, **fertilizer 0**
    (`docs/superpowers/plans/2026-08-26-drain-aware-reservation.md` section 1.1).
    """
    f32 = xp.float32
    day = obs.day.astype(f32)
    days = xp.arange(spec.N_DAYS, dtype=f32)
    ahead = (days >= day).astype(f32)                 # today and every later day
    horizon = xp.sum(ahead)
    n_now = xp.sum(obs.shops.astype(f32))
    unlocks = xp.sum(ahead * xp.maximum(xp.asarray(_SHOPS_ON_DAY) - n_now, 0.0))
    return horizon * demand + unlocks * xp.asarray(_MEAN_SHOP_DAILY)


#: Both residual columns are clipped here. `share` diverges outright on a
#: product the town does not consume -- fertilizer's whole-season drain is
#: exactly zero, so its `share` is minus the entire supply -- and `gap` runs to
#: -7 on a fertilizer-heavy herd. Unclipped, one sigma step on a drain weight
#: would be a double-digit logit swing; the land-affordability ratio in
#: `decide` is clipped for the same reason.
#:
#: The bound bites in exactly one benign place: strawberry's T is 100 against a
#: 426-unit season drain, so its `gap` saturates on an empty board for the first
#: two or three days. `share` is unclipped there (0.998), which is half the
#: reason there are two columns rather than one.
DRAIN_CLIP = 4.0


def residual_drain(xp, obs: PolicyObs, own, opp, demand):
    """float32[9, `policy.N_DRAIN_FEAT`]: the town appetite nobody has claimed.

    Per product, over the rest of the season,

        residual = expected remaining town drain
                 - supply both seats have already committed to this market

    where the committed supply is what already sits in the market above its
    opening inventory, what waits in our own shed for a lot, and what every
    producing tile on *either* board will bank between now and
    `ops.LAST_SHED_DAY`, at that product's steady-state rate.

    This is the scalar that separates "tomato pays +93 coins a unit" from "milk
    pays -55" (2026-08-26 diagnosis, section 4: the four markets that go over
    the drain are exactly the four that lose money, and tomato, egg and carrot
    have 679 units of drain nobody supplies). Nothing else the network sees
    expresses it. `features` carries own tiles, opponent tiles and the market's
    inventory as separate columns, but the residual is a *product* of a tile
    count with the days left and a function of shop unlocks that have not
    happened -- neither is linear in any column, and no combination of the
    existing knobs reaches it.

    Two normalisations, because neither alone covers the nine products:

    * `gap = residual / T` puts the headroom in the units the price curve is
      written in (`spec.market_price` shapes its response on `T`), so it is
      directly commensurate with product column 0's `(inv - I0) / T`.
    * `share = residual / (drain + 1)` is scale-free -- the fraction of the
      town's remaining appetite still unclaimed -- which is what makes wool
      (season drain 282 against a joint supply of 243) comparable with wheat
      (492 against 196). It saturates on melon and fertilizer, whose drains are
      30 a season and exactly zero, and saturating is the correct reading:
      every unit of those two is oversupply by construction.

    Deliberately opponent-inclusive, deliberately horizon-scaled, and
    deliberately an expectation -- producing tiles are priced at the
    steady-state rate whether or not they have reached their first yield.
    """
    f32 = xp.float32
    day = obs.day.astype(f32)
    drain = expected_drain(xp, obs, demand)
    grow_days = xp.maximum(float(O.LAST_SHED_DAY) + 1.0 - day, 0.0)
    supply = ((obs.mkt_inv.astype(f32) - spec.MARKET_I0)
              + obs.shed[:NP_].astype(f32)
              + (own + opp) * xp.asarray(_RATE) * grow_days)
    resid = drain - supply
    gap = xp.clip(resid / xp.asarray(_T), -DRAIN_CLIP, DRAIN_CLIP)
    share = xp.clip(resid / (drain + 1.0), -DRAIN_CLIP, DRAIN_CLIP)
    return xp.stack([gap, share], axis=1)


#: Days ahead the forecast is taken out to. One day is "does this land before
#: the next shop tick", three is the planting/harvest decision's own horizon,
#: seven is the melon/strawberry race. Column 0 of each half is the *standing*
#: quantity, i.e. horizon zero.
FCAST_HORIZONS = (1, 3, 7)
#: Divisors for (ready now, +1d, +3d, +7d), hand-chosen like every other scale
#: in this file: a plausible maximum per column, so each lands near 1.0 on a
#: full board rather than at four different magnitudes.
#:
#: **Powers of two, and they have to be** [LAW]. Everything above is an exact
#: integer count in float32, so dividing by a dyadic scale is an exponent
#: adjustment: exactly representable, and identical on both backends. A round
#: decimal is not -- measured 2026-09-08, seven animals over seven days came to
#: `49 / 100` = 0.49 in numpy and 0.48999998 under `jax.jit`, one ulp apart, on
#: an input both agreed was 49.0. Every quantity `decide` derives is a `floor`,
#: so one ulp is a different move (`tests/test_backend_agreement.py`), and the
#: fix belongs in the feature rather than in another epsilon.
_FCAST_SCALE = np.array([64.0, 32.0, 64.0, 128.0], np.float32)

#: Horizons the *forward-value* block reads. The same three `FCAST_HORIZONS`
#: takes out, deliberately: one projection of the board, two readings of it --
#: `production_forecast` hands the per-product timing to the shared encoder,
#: and `forward_value` hands the board total to the global head, which has
#: never had either.
FWDVAL_HORIZONS = FCAST_HORIZONS
#: Divisors for the units channel, one per horizon, and for the coin channel.
#: Both are **powers of two** for the reason `_FCAST_SCALE` is [LAW]: the
#: quantities above are exact integers in float32 (a unit count, and a count
#: times an integer quote), so a dyadic divisor is an exponent adjustment --
#: exact, and identical in numpy and under `jax.jit`. A round decimal is not,
#: and every quantity `decide` derives is a `floor` away from a different move.
#:
#: One divisor per horizon rather than one for the block: production is roughly
#: linear in the days you wait for it, so a single scale would put the +1d
#: channel a factor of six under the +7d one and spend most of an isotropic ES
#: step's budget on the far horizon. Sized off `tests/data/trajectory_obs.npz`
#: (2,400 recorded observations, our board): rms units 23.7 / 66.4 / 143.0 and
#: rms coins 2,136 / 6,074 / 13,240, each taken to the nearest power of two, so
#: every one of the six channels lands within 30 % of 1.0 (0.74 / 1.04 / 1.12
#: units, 1.04 / 0.74 / 0.81 coins) instead of at six magnitudes.
#:
#: The units row comes out at `_FCAST_SCALE`'s own horizon columns, which is
#: not a coincidence: the per-product forecast is scaled by what one *product*
#: contributes on a full board, and at any moment a board is carrying roughly
#: one product's worth of imminent harvest spread over several crops.
_FWDVAL_UNIT_SCALE = np.array([32.0, 64.0, 128.0], np.float32)
_FWDVAL_COIN_SCALE = np.array([2048.0, 8192.0, 16384.0], np.float32)


def _fires_by(xp, age, first, interval, cap=None):
    """Production events an EOD-firing tile has had by age `age`, capped.

    `sim/eod.refresh_plants` / `refresh_animals` fire at the end of day `d`
    when `(d + 1) - t_day - first` is a non-negative multiple of `interval`, so
    the count at age `a` is `floor((a - first) / interval) + 1` clamped below at
    zero. Integer floor division rounds toward minus infinity in numpy and JAX
    alike, which is what makes the pre-first-yield case fall out rather than
    needing a branch. The difference of this at two ages is the number of
    events between them -- one expression for both backends and every horizon.

    `cap` is the lifetime count an ongoing crop is allowed (`refresh_plants`'
    `pcount <= mxy`). `None` is the animals, which have no lifetime cap at all:
    a number picked to be "big enough" would silently clip a goose read seven
    days past the last day of the season, so there is no number here.
    """
    n = (age - first) // interval + 1
    return xp.maximum(n, 0) if cap is None else xp.clip(n, 0, cap)


def _board_forecast(xp, day, kind, occ, t_day, t_yield):
    """float32[9, 4]: (harvestable now, +1d, +3d, +7d) units, for one board.

    Public tile state only -- crop or animal, its planting/placement date and
    its standing `yield_units`. Nothing private (shed, seeds, cash) enters, so
    the identical function reads our board and the opponent's.

    Three production laws, all from `spec` and `sim/eod`:

    * An **ongoing** crop (tomato, strawberry) and every **animal** bank a unit
      at the end of each day the interval fires. The crop's lifetime count is
      capped at `CROP_MAX_YIELD` (`refresh_plants`' `pcount <= mxy`); an animal
      has no lifetime cap, only a standing one.
    * A **one-time** crop (wheat, carrot, melon) banks nothing at end of day.
      It is seeded with one unit and gains one per *watered* day inside
      `[CROP_WINDOW_START, CROP_MAX_YIELD_DAY]`, capped at `CROP_MAX_YIELD`
      (`sim/units`' WATER op), so its forecast is the in-window days left,
      bounded by the units it can still take.
    * **Fertilizer** is one per living animal per day (`t_favail` is re-armed
      every end of day). Its standing quantity is not observable -- `t_favail`
      is not in `PolicyObs` for either seat -- so column 0 is 0 for it and only
      the horizons carry it.

    Deliberately an *upper* bound in one respect and an expectation in another:
    every tile is assumed watered or fed (an unwatered plant dies in two days
    and the forecast would be wrong about a board that is losing anyway), and
    an ongoing tile is assumed harvested often enough that the standing cap
    never bites, so what is reported is units *produced* rather than units that
    will fit. Both are properties of the feature, not of the engine, and the
    network learns what to do with them.

    Whole-array reductions only [LAW]: `occ` selects the per-crop and
    per-animal constants, which is content-addressed, and no per-tile position
    table is read -- so this reads the same board in the raw-order simulator
    and the serpentine-order submission.
    """
    f32 = xp.float32
    i32 = xp.int32
    is_pl = kind == spec.KIND_PLANT
    is_an = ((kind == spec.KIND_COOP) | (kind == spec.KIND_PASTURE)) & (occ >= 0)
    c = xp.clip(occ, 0, spec.N_CROPS - 1)
    a = xp.clip(occ, 0, spec.N_ANIMALS - 1)
    age = (day - t_day).astype(i32)
    yld = t_yield.astype(i32)

    c_ong = xp.asarray(spec.CROP_ONGOING)[c]
    c_first = xp.asarray(spec.CROP_FIRST_YIELD_DAY)[c]
    c_iv = xp.maximum(xp.asarray(spec.CROP_INTERVAL)[c], 1)
    c_mxy = xp.asarray(spec.CROP_MAX_YIELD)[c]
    c_ws = xp.asarray(spec.CROP_WINDOW_START)[c]
    c_mxd = xp.asarray(spec.CROP_MAX_YIELD_DAY)[c]
    a_first = xp.asarray(spec.ANIMAL_FIRST_YIELD_DAY)[a]
    a_iv = xp.maximum(xp.asarray(spec.ANIMAL_INTERVAL)[a], 1)

    ong_now = _fires_by(xp, age, c_first, c_iv, c_mxy)
    an_now = _fires_by(xp, age, a_first, a_iv)
    n_animals = xp.sum(is_an.astype(f32))

    def by_product(pl_val, an_val, fert_val):
        cols = [xp.sum(xp.where(is_pl & (occ == k), pl_val, 0).astype(f32))
                for k in range(spec.N_CROPS)]
        cols += [xp.sum(xp.where(is_an & (occ == k), an_val, 0).astype(f32))
                 for k in range(spec.N_ANIMALS)]     # EGG, MILK, WOOL in order
        cols.append(fert_val)
        return xp.stack(cols)

    # Column 0: what a HARVEST / COLLECT this turn would take off the board.
    # `sim/units` needs `yield_units > 0` and, for a plant, `age >= first`.
    cols = [by_product(xp.where(age >= c_first, yld, 0), yld, xp.zeros((), f32))]

    for h in FCAST_HORIZONS:
        ahead = age + np.int32(h)
        ong_gain = _fires_by(xp, ahead, c_first, c_iv, c_mxy) - ong_now
        # A one-time crop's water window, intersected with (age, age + h].
        win = xp.maximum(xp.minimum(c_mxd, ahead) - xp.maximum(c_ws - 1, age), 0)
        one_gain = xp.minimum(win, xp.maximum(c_mxy - yld, 0))
        cols.append(by_product(xp.where(c_ong == 1, ong_gain, one_gain),
                               _fires_by(xp, ahead, a_first, a_iv) - an_now,
                               n_animals * f32(h)))
    return xp.stack(cols, axis=1)


def board_forecasts(xp, obs: PolicyObs):
    """`(own, opp)`, each the raw float32[9, 4] `_board_forecast` of one seat.

    Hoisted out of `production_forecast` so `forward_value` can read the same
    two boards rather than project them a second time: the two blocks are two
    *readings* of one projection -- the per-product timing the shared encoder
    gets, and the board total the global head gets -- and computing it twice
    would be two identical traces in the jitted rollout for nothing.
    """
    return (_board_forecast(xp, obs.day, obs.kind, obs.occ, obs.t_day, obs.t_yield),
            _board_forecast(xp, obs.day, obs.opp_kind, obs.opp_occ,
                            xp.asarray(obs.opp_t_day), xp.asarray(obs.opp_t_yield)))


def forward_value(xp, obs: PolicyObs, boards=None):
    """float32[`policy.N_FWDVAL_FEAT`]: what each board is about to be worth.

    Twelve numbers, the global head's half of the 2026-09-08 plateau
    diagnosis' section 4: for our seat and the opponent's, over horizons
    `FWDVAL_HORIZONS`, the **units** the standing board will produce and what
    those units are **worth at today's quote**. Laid out
    `[own units x3, own coins x3, opp units x3, opp coins x3]`.

    `production_forecast` says the same thing per product, and only the shared
    encoder reads it: nine 8-vectors reach `w1` through `fh`/`fs` and are
    reduced to a grow and a sell score apiece. The global head reads
    `glob_feat`, which carries exactly two product aggregates -- the shed total
    and the mean price ratio -- and nothing at all about *when* the board pays.
    So the head that sizes the crew, the land bias, dev_frac and the animal
    share had to give the same answer on a twelve-melon board that emits
    nothing for six days as on a wheat board that pays tomorrow. The
    forced-opening diagnostic is exactly that failure measured: the day-0 melon
    opening prices its hands against an empty task set.

    Coins, not just units, because the head's other resource axis is coins
    (`money / 20000`, the cash gap): a unit of wheat and a unit of melon are a
    factor of ten apart and only the coin channel says so. The quote is
    `obs.price`, today's, not a projection of it -- the market model that would
    project it is the encoder's job and the point here is a comparable number,
    not a forecast of the price curve.

    Public state only, so the identical expression reads both seats -- the
    opponent's tiles, clocks and standing yield are in `PolicyObs` for the same
    reason `production_forecast`'s opponent half is.

    Whole-array reductions only [LAW]: everything here is a sum over
    `_board_forecast`'s output, which is itself content-addressed by `occ`.
    """
    own, opp = board_forecasts(xp, obs) if boards is None else boards
    price = obs.price.astype(xp.float32)
    us = xp.asarray(_FWDVAL_UNIT_SCALE)
    cs = xp.asarray(_FWDVAL_COIN_SCALE)
    cols = []
    for b in (own, opp):
        # Column 0 is the *standing* quantity (horizon zero); the horizons are
        # columns 1.. in `FCAST_HORIZONS` order.
        ahead = b[:, 1:]
        cols.append(xp.sum(ahead, axis=0) / us)
        cols.append(xp.sum(ahead * price[:, None], axis=0) / cs)
    return xp.concatenate(cols)


def production_forecast(xp, obs: PolicyObs, boards=None):
    """float32[9, `policy.N_FCAST_FEAT`]: when each board's supply arrives.

    Eight columns per product: our board's harvestable-now, +1d, +3d and +7d,
    then the opponent's four. `_board_forecast` computes one board; this scales
    and joins them.

    This is the block the 2026-09-08 plateau diagnosis (section 4) asked for.
    `features`' `prod_feat` columns 7 and 8 count the tiles *producing* each
    product on either board, and a count cannot say **when**: eight strawberry
    tiles read identically whether the first yield is tomorrow or a week out,
    and the probe found planting dates and standing yield moving without a
    single feature moving with them. `residual_drain` needs the same distinction
    and cannot make it either -- it prices every producing tile at the
    steady-state rate whether or not it has reached its first yield, which is
    the right call for a season-long residual and the wrong one for "should
    today's lot wait for tomorrow's harvest".

    Returned separately from `features` rather than appended to `prod_feat`,
    for the reason `residual_drain` is: widening `prod_feat` would widen `w1`,
    move every later parameter block and stop every checkpoint on disk
    decoding. It gets its own appended weights instead -- `policy.SHAPES`' `fh`
    and `fs`.
    """
    own, opp = board_forecasts(xp, obs) if boards is None else boards
    scale = xp.asarray(_FCAST_SCALE)
    return xp.concatenate([own / scale, opp / scale], axis=1)


def features(xp, obs: PolicyObs):
    """(prod_feat [9, 12], glob_feat [24], drain_feat [9, 2]).

    The drain block is returned separately rather than appended to `prod_feat`
    because widening `prod_feat` would widen `w1`, move every later parameter
    block and stop every existing checkpoint decoding. It gets its own appended
    weights instead -- `policy.SHAPES`' `dh` and `ds`.
    """
    f32 = xp.float32
    inv = obs.mkt_inv.astype(f32)
    price = obs.price.astype(f32)
    base = xp.asarray(_BASE)
    T = xp.asarray(_T)

    own = _producing(xp, obs.kind, obs.occ)
    opp = _producing(xp, obs.opp_kind, obs.opp_occ)
    demand = daily_town_demand(xp, obs)

    prod = xp.stack([
        (inv - spec.MARKET_I0) / T,
        price / base,
        xp.log1p(base) / 6.0,
        T / 450.0,
        xp.asarray(_BT),
        xp.asarray(_AT),
        demand / 20.0,
        own / 25.0,
        opp / 25.0,
        obs.shed[:NP_].astype(f32) / 100.0,
        xp.asarray(_FIRST) / 12.0,
        xp.asarray(_RATE),
    ], axis=1)

    n_free = n_free_slots(xp, obs).astype(f32)
    unlocked = xp.sum((obs.kind != spec.KIND_LOCKED).astype(f32))
    opp_unlocked = xp.sum((obs.opp_kind != spec.KIND_LOCKED).astype(f32))
    n_plant = xp.sum((obs.kind == spec.KIND_PLANT).astype(f32))
    n_animal = xp.sum((((obs.kind == spec.KIND_COOP) | (obs.kind == spec.KIND_PASTURE))
                       & (obs.occ >= 0)).astype(f32))
    n_weed = xp.sum((obs.kind == spec.KIND_WEED).astype(f32))
    n_struct = xp.sum((((obs.kind == spec.KIND_COOP) | (obs.kind == spec.KIND_PASTURE))
                       & (obs.occ < 0)).astype(f32))
    opp_plant = xp.sum((obs.opp_kind == spec.KIND_PLANT).astype(f32))
    opp_animal = xp.sum((((obs.opp_kind == spec.KIND_COOP) |
                          (obs.opp_kind == spec.KIND_PASTURE))
                         & (obs.opp_occ >= 0)).astype(f32))
    money = obs.money.astype(f32)
    opp_money = obs.opp_money.astype(f32)
    land_next = xp.asarray(spec.LAND_PRICES.astype(np.float32))[xp.clip(obs.nquad - 1, 0, 2)]

    glob = xp.stack([
        obs.day.astype(f32) / 30.0,
        (30.0 - obs.day.astype(f32)) / 30.0,
        money / 20000.0,
        opp_money / 20000.0,
        (money - opp_money) / 20000.0,
        n_free / 100.0,
        unlocked / 100.0,
        obs.nquad.astype(f32) / 4.0,
        opp_unlocked / 100.0,
        opp_plant / 100.0,
        xp.sum(obs.shed.astype(f32)) / 100.0,
        n_plant / 100.0,
        n_animal / 100.0,
        n_weed / 100.0,
        n_struct / 100.0,
        xp.sum(obs.seeds.astype(f32)) / 50.0,
        obs.shed[spec.I_FERT].astype(f32) / 50.0,
        obs.shed[spec.I_WHEAT].astype(f32) / 100.0,
        xp.sum(obs.shops.astype(f32)) / 8.0,
        xp.mean(price / base),
        opp_animal / 100.0,
        obs.opp_nquad.astype(f32) / 4.0,
        land_next / 4000.0,
        xp.ones((), f32),
    ])
    return prod, glob, residual_drain(xp, obs, own, opp, demand)


# --- cross-backend integer quantisation ----------------------------------
#
# Every quantity the head decodes is `floor(continuous * integer_count)`, so it
# sits one ULP from a decision cliff whenever the product lands near an integer.
# numpy (submission) and JAX (training) do not produce bit-identical float32, so
# a product that is mathematically exactly N can fall either side of the floor
# and the two backends emit different actions from the same weights.
#
# Two things are needed to close that, and only together:
#
#   * `kagg3.precision` pins JAX to true float32 matmuls. TF32 tensor cores were
#     the dominant source, worth ~3.5e-3; without them the gap is ~2e-6. This is
#     the half that makes disagreement *unlikely* -- an epsilon cannot, because
#     widening it relocates the cliff without making a landing on one rarer.
#   * This epsilon is the half that makes an exactly-integer product land on the
#     correct side. It has to comfortably exceed residual float32 rounding
#     (~2e-6) while staying far below the 0.5 that would change a genuine
#     decision.
QUANT_EPS = 1e-4

#: The relative half of the guard. float32 agreement between numpy and XLA is
#: *relative* -- a few ULPs of `exp`/`log1p`/matmul, ~1e-7 of the value -- so
#: an absolute epsilon only covers products up to ~QUANT_EPS / 1e-7 = 1,000.
#: `hold` is decoded in coins up to `spec.COIN_CAP` and landed on it first
#: (measured 2026-08-27: `0.8 * 80 * _unit_ratio` = 484 exactly, numpy
#: 483.99990 against XLA 483.99982, decision 1656 of the trajectory fixture,
#: gate 2), but `press` (base * tanh, ~1,300) and the `GROW_ONE`-scaled
#: multipliers (~1,000) carry the same exposure. 1e-6 is ~8 ULPs: 5e-4 coins at
#: 484, one coin at the cap, and it moves a decode only when the product sits
#: within that of an integer -- exactly the landing the backends already
#: disagree on -- so every trained theta decodes as before everywhere else.
QUANT_REL = 1e-6

#: Fixed-point steps of the land bias' `tanh`, quantized before it is scaled to
#: coins rather than after [LAW]. float32 agreement between numpy and XLA is
#: *relative*, so a product near a 4,000-coin quadrant price disagrees by about
#: 5e-4 -- five times QUANT_EPS -- and `_qfloor` then lands the two backends on
#: different integers (measured: numpy 3,999 against XLA 4,000, gate 2). The
#: fraction is at most 256, where the same relative error is 3e-5, and the
#: scaling to coins afterwards is integer arithmetic that cannot disagree.
LAND_BIAS_STEPS = 256

#: Fixed-point unit of the grow value multiplier: GROW_ONE == x1.0. Values it
#: scales are int32 coins, so the multiplier is an integer too. Defined by the
#: planner, which does the scaling; aliased here for the decode.
GROW_ONE = P.GROW_ONE
GROW_MAX = 4.0
#: Ceiling of the `compact` gene: the largest Manhattan distance from the
#: shed-access spawn block to any tile, and so the number of distance bands the
#: planner's `_rank_near` can resolve. Defined by the planner; aliased here.
DIST_MAX = P.DIST_MAX

#: Saturated value of the `hire_bias` gene, in coins per hand [1.5].
#:
#: The scale is read off `plan.HIRE_BILLS`, which is a running sum of Fibonacci
#: numbers, so the *marginal* cost of the h-th hand is `fib(h)`: 34, 55, 89,
#: 144, 233, 377 for hands 9..14. A per-hand bias of `b` coins therefore pays
#: for every hand whose own fib cost is under `b` -- and the enumeration's
#: argmax turns that into a crew *target*, near enough to read off a table:
#:
#:     knob   0.10  0.26  0.39  0.70  2.00
#:     b        40   100   150   250   400
#:     crew      9    11    12    13    14   (funds permitting)
#:
#: The ceiling is the Kaggle field's own crew: `fib(14) = 377`, so a saturated
#: gene asks for the 14 hands the modal opponent fields on day 10 and no more.
#: Past that the enumeration has to justify the hand on the day's *work*, which
#: is the right way round -- measured 2026-08-28 in the real engine, a bias big
#: enough to demand 13+ hands from day 5 spends 12,425 coins on hire, holds back
#: `HIRE_BILLS[h + 1]` of every day's purse as `cash_reserve`, and leaves the
#: rung planting 0.5 strawberry tiles and finishing on 7,159 coins against the
#: unbiased 75,042. Signed, because the opposite -- a rung that demands margin
#: before it hires -- is a real strategy and `tanh` gives it for free.
HIRE_BIAS_MAX = 400.0

#: Day edges of the `hire_bias` buckets: days 0-5, 6-10, 11-20, 21+.
#:
#: The gene is four numbers, not one, because the Kaggle field's labour ramp is
#: a *shape* and one number cannot say it: the modal opponent fields 3-4 hands
#: on day 5 and 14 by day 10, and a season-constant bias big enough for the
#: late crew spends its purse on the cheap early hands instead (measured
#: 2026-08-28, `es/archetypes.py`'s `wheat_clone` v2 note -- day 5 goes 3 -> 7
#: while day 10 does not move at all).
#:
#: The edges are the season's own joints rather than an even split: day 6 is
#: the earliest a first wheat crop has been sold and a second quadrant is
#: affordable, day 11 is where the field's crew has finished ramping, and day
#: 21 is inside `LAST_SHED_DAY`'s wind-down, where a hand's remaining value is
#: what it can still harvest. Four is also as many as the block can be worth:
#: each bucket is a 32-wide column of weights, and the ES has to earn every one.
HIRE_BIAS_BUCKETS = (6, 11, 21)
assert len(HIRE_BIAS_BUCKETS) + 1 == PO.N_HIRE_BUCKETS

#: Ceiling of the crew-target ramp, in hired hands [g10].
#:
#: `spec.MAX_HANDS` and not a smaller number: the target is what the *field*
#: fields, and the Kaggle replays put the modal opponent at 12 hands and the
#: class-A clones at 14 by day 10. The enumeration still has to be able to pay
#: the fib bill, so the ceiling only bounds what the gene may ask for.
CREW_TARGET_MAX = float(spec.MAX_HANDS)

#: Day the ramp's logistic is centred on, `CREW_MID_MAX * sigmoid(z)`. The
#: whole season, so the gene can put the midpoint anywhere in it; at z = 0 it
#: is the middle of the season, which is irrelevant -- the height is 0 there.
CREW_MID_MAX = float(spec.N_DAYS)

#: Steepness of the ramp, `CREW_STEEP_MAX * sigmoid(z)`, in logits per day.
#: A logistic climbs from a tenth of its height to nine tenths in `2*ln 9 / k`
#: days, so the ceiling is 1.5 days -- as close to a step as a curve over 30
#: integer days can usefully be -- and z = 0 is 1.5 logits a day, i.e. ~3 days.
CREW_STEEP_MAX = 3.0

#: Fixed-point unit of the animal deferral: DEFER_ONE == x1.0 (no deferral).
#: Defined by the planner, which does the scaling; aliased here for the decode.
DEFER_ONE = P.DEFER_ONE

#: Ceiling of the forward-admit horizon, in days [g11].
#:
#: Six, which is `max(spec.CROP_WINDOW_START)` -- the melon's, and the longest
#: silence a planted tile can hold before it owes the day an op. A horizon past
#: it prices hands against work no crop on the board is still holding back.
FWD_DAYS_MAX = 6

#: Days of horizon per logit: the decode is `round(FWD_DAYS_GAIN * z)` [g11].
#:
#: Sized off the ES step, because a gene the search cannot *feel* is a dead
#: gene. The block shipped as `round(FWD_DAYS_MAX * sigmoid(z - 4))`, which is
#: exactly 0 at z = 0 -- but so is every perturbation of it: measured over 200
#: real boards from `tests/data/trajectory_obs.npz` with `flow135_g350_gpfwdfv`
#: and 512 isotropic draws at the live arm's sigma 0.02, the pre-activation
#: `z = gh @ g11 + gb11` has sd **0.0546** (`||gh|| ~ 2.34` over the 32-dim
#: tanh hidden, so `sigma * sqrt(||gh||^2 + 1)`), and `6 * sigmoid(0.05 - 4)`
#: is 0.11 of a day. **Not one** of the 512 decoded a single day -- nor at
#: sigma 0.03, nor at 0.05, where the whole population still read 0. The shift
#: buried the gene in the sigmoid's left tail and the ES saw a constant.
#:
#: A straight line through the origin instead, so the slope is a number that
#: can be set against that sd: one day of horizon needs `z >= 0.5 / 16 =
#: 0.031`, i.e. 0.57 of a one-sigma step, and the measured population then
#: decodes >= 1 day for 24.8 % of members on the median board (18.6 - 32.6 %
#: over the 200), >= 2 for 4.4 %, and >= 4 for none of them. That is the shape
#: a selection step can read: a minority of the population differs from the
#: centre by one or two days, and no member is thrown to the far end of the
#: range by noise alone.
#:
#: Still exactly inert at zero -- `_qfloor(16 * 0.0 + 0.5)` is `floor(0.5001)`,
#: which is 0 -- so every theta written before the block still plans byte for
#: byte, which is the property the append exists to keep.
FWD_DAYS_GAIN = 16.0

#: Largest fertilizer-timing look-ahead the `g12` gene can name, in days
#: [FERTENGINE].  An application covers `day .. day + 2`, so a tile's marginal
#: value peaks at most two days out (a one-time crop reaches its best day at
#: `window_start`, an ongoing crop on the eve of a fire); past that the look-
#: ahead only defers work the crew may never come back for.
FERT_DEFER_MAX = 3
#: Days of look-ahead per logit: the decode is `round(FERT_DEFER_GAIN * z)`,
#: the same `round(16 * z)` line `FWD_DAYS_GAIN` documents, and for the same
#: reason -- at sigma 0.02 a logistic would leave the gene in a zone where no
#: perturbation moves the horizon at all, while `16 * 0.02 = 0.32` gives a
#: measurable slope: `round(16 * z)` first steps at `|z| >= 1/32`, so ~1.6
#: sigma, and the antithetic pair straddles it.
FERT_DEFER_GAIN = 16.0

#: Clip on the `animal_mix` gene, in the herd want's own logit units.
#:
#: Not a `tanh`, deliberately: the want is a softmax over the three animal grow
#: scores, so a bias in *log-share* units is the readable unit here (a rung
#: that wants 2:1 sheep to cow writes `ln 2 = 0.69` of separation and can be
#: read back off the entry). The clip only keeps the exponent finite; the
#: softmax bounds the effect on its own, since the want saturates at one kind.
#: Exactly inert at zero -- 0 is interior, and `x + 0.0 == x`.
ANIMAL_MIX_CLIP = 10.0

# ---- HERD_RAMP: buy the herd EARLIER out of the day-0..9 purse -------------
#
# [SWITCH, OFF]  `2026-09-17-earlyramp.md` moved the day-0..9 purse the other
# way -- non-melon seed tiles took it and the herd starved (animals 17 -> 13.8,
# collected fertilizer 379 -> 230, their milk/fert revenue +6,432, ENG22
# -10,278).  That reading names the herd as what the purse buys, so this is the
# one untested direction on the same axis: the SAME `n_dev` free tiles, with
# `HERD_RAMP_SHIFT` of them pushed from `plant_total` to `animal_count` while
# `obs.day < HERD_RAMP_DAYS`.  Nothing else moves -- the mix `wa`, the budget
# grant that prices the animal in coins and `plan._wants`' clip to the tiles
# that exist all still run, so an unaffordable bump is a silent no-op and the
# feed bill stays the enumeration's problem, not this switch's.
#
# Guarded by a trace-time Python `if`, so the OFF branch is the shipped graph
# character for character (`tests/test_herd_ramp.py`).
HERD_RAMP_ON = False
HERD_RAMP_DAYS = 10
HERD_RAMP_SHIFT = 2

# ---- HERD_TILT: a DAY SLOPE on the crop/herd split -------------------------
#
# [GENE, inert at 0.0]  `2026-09-19-volumehi.md` censused the 15 hiband ship
# losses to the coin and found NOTHING on our side blocked in d10-19: hires
# level, plant VETO/NOSEED/TILE all 0.00, purse idling 15k-39k from d16,
# prod-ops level -- only the ASK is short (plantings 50.7 vs 84.9, wheat 28.9
# vs 70.5) while our d10-19 herd spend is +76 % (3,060 vs 1,740).  The cap is
# `plant_total = n_dev - sum(animal_want)`, and `animal_share = sig(head[6])`
# carries NO day term at all -- one crop/herd split for all 30 days.
#
# `HERD_TILT` is that missing term, in the split's own logit units:
#
#     animal_share = sig(head[6] + HERD_TILT * max(0, day - 12) / 10)
#
# Hinged at day 12 (the day `sum(macro.plant_target)` collapses to 0-4 in the
# census) and scaled by 10 days, so one unit of tilt is one logit per decade
# and the sign reads directly: NEGATIVE moves our own unit-turns off the herd
# chain and onto the crop chain LATE, leaving the early herd -- which
# `earlyramp`/`HERD_RAMP` name as what the opening purse buys -- untouched.
#
# [HERDTILT2, 2026-09-19] The hinge `max(0, .)` is the fix HERDTILT's census
# forced: the ORIGINAL two-sided `(day - 12)` made a NEGATIVE tilt RAISE the
# herd share before d12 (ANIM d10-11 went UP to 3,387 at -1.0) -- `earlyramp`
# inside the measurement window.  One-sided, d0-11 is the shipped split to the
# coin and only d12+ moves.
# It is a split of OUR labour, not a share of the town curve, so it is not the
# reallocation `carrotbid` prices as a gift.
#
# Guarded by a trace-time Python `if`, so at the default 0.0 the two lines
# below are the shipped graph character for character [LAW, as HERD_RAMP].
HERD_TILT = 0.0

# ---- TURN_COST: price a planting in TENDING TURNS, not just in grow score ---
#
# [GENE, inert at 0.0]  `2026-09-19-opscensus.md` censused every unit-turn of
# the 15 hiband ship losses to the coin: the d10-19 budget is LEVEL (2,715 vs
# 2,694 turns) and yet they plant +34 more.  The whole of it is MIX, not
# tending skill -- per crop the tending cost is the same on both sides, but
# 83 % of their d10-19 plantings are WHEAT at ~3.8 turns while our 19.4 melon
# + strawberry plantings eat 249 of our 380 water turns.  Measured off the same
# census (`fates[*].water + .fert`, our seat, n=2,712 plantings):
#
#     WHEAT 4.64 · CARROT 3.63 · TOMATO 9.56 · STRAWBERRY 11.35 · MELON 8.73
#
# `crop_logits` carries the grow score, the `cd` day bias and `crop_mix`, and
# NOTHING that says a strawberry tile costs three carrot tiles' worth of hands.
# `TURN_COST` is that missing term, in the softmax's own log-share units:
#
#     crop_logits -= TURN_COST * TURN_COST_TURNS      [day >= TURN_COST_DAY]
#
# so a POSITIVE value tilts the mix toward cheap-tending crops and the freed
# hands buy plantings.  The spread that matters is STRAW - WHEAT = 6.7 turns,
# so one unit of tilt is ~6.7 nats between them and 0.15 is ~1 nat.
#
# Hinged at day 10 like `HERD_TILT`, and for the same reason: d0-9 is the
# opening `earlyramp`/`meloneng` priced and it is not this gene's window --
# below the hinge the decode is the shipped one byte for byte.  It re-weights
# OUR OWN labour between OUR OWN tiles, so it is not the town-curve
# reallocation `carrotbid`/`cropmix` price as a gift -- but the mix does move
# supply onto the shared price curve, so the judge on dtheirs decides.
#
# Clipped by `CROP_MIX_CLIP`, the bound that was already on this expression.
# Guarded by a trace-time Python `if`, so at the default 0.0 the branch below
# is the shipped graph character for character [LAW, as HERD_RAMP/HERD_TILT].
TURN_COST = 0.0

#: Day the hinge opens.  d0-9 is untouched.
TURN_COST_DAY = 10

#: Mean WATER + FERTILIZE unit-turns per planting, our seat, in `spec.CROPS`
#: order -- read off `S/opscensus/raw/oc_hiband_*_s0.json` over all 2,712 of
#: our plantings on the 15 hiband ship losses.  A static table on purpose: the
#: census shows the per-crop cost is a property of the crop (theirs: 3.79 /
#: 3.31 / 9.82 / 11.21 / 9.21), not of the board or of who is tending.
TURN_COST_TURNS = (4.64, 3.63, 9.56, 11.35, 8.73)

# Same units and bound as animal_mix. This changes crop proportions only;
# maturity and market-absorption masks below still decide eligibility.
CROP_MIX_CLIP = 10.0

# ---- MELON gene: give the crop log-share readout a sigma-scale slope -------
#
# [SWITCH, OFF]  `cm`/`cb` (`policy.Outputs.crop_mix`) is the only zero-init
# path into the plant mix that does not go through a grow score, and it is the
# coordinate block an ES arm would name to learn *proportions*.  Measured at B
# (`flow193_g100_hr`, padded) on the real day-0 dawn of episode 108450468 and
# on the cold-start dawn: melon's log-share is -5.6455 and the exact additive
# bias that buys the first melon tile is **+2.0487 nats** (bisection on
# `cb[I_MELON]`, the decode below), +3.9303 for four, +4.9557 for eight and
# +5.7090 for twelve.  The readout's own gradient norm over `cm,cb` is 2.885,
# so a sigma-0.01 draw displaces melon's log-share by ~0.01 nats along its own
# best direction -- 71 standard deviations short of one tile.  That is the
# `2026-09-13-melon-sigma-reachability` zero, restated as a number: the gene is
# decodable but its gain is ~200x too small for the training sigma, exactly the
# `round(16 * z)` defect the 2026-09-09 gene-slope check was written for.
#
# ON, the readout is multiplied before the clip, so one sigma at 0.01 is
# 2.56 nats -- over the measured 2.0487 boundary, under the 3.9303 that would
# make every draw a four-tile jump.  The clip is unchanged and still applied
# last, so the expression stays bounded and a saturated gene is +-10 nats.
# Exactly inert at zero either way (`0.0 * G == 0.0`), and the OFF branch is
# the shipped expression character for character [LAW].
MELON_GENE_ON = False

#: `CROP_MIX_GAIN * sigma` is the per-draw log-share step.  256 * 0.01 = 2.56
#: nats > the measured 2.0487-nat first-tile boundary at B.
CROP_MIX_GAIN = 256.0

# ---- CROP-DAY gene: give the crop log-share a day index [SWITCH, OFF] -----
#
# `cm`/`cb` says one mixture for the whole season.  MACRO-EXTRACT section 3
# measured what the top five actually plant and it is not a mixture at all but
# a *block programme*: ymg_aq plants pure wheat on day 2 and pure strawberry on
# day 3, and the least-squares fit of that onto a season-constant `cb` dumps
# every tile on wheat (section 4 item 5).  WHEAT-SLOPE then showed the other
# half of the same fact -- a static wheat shift is reachable (0.93 sd) and
# loses on all 88 paired boards, because the shift it buys is the *season's*
# wheat share, not day 2's.  `cd` is the missing index: one log-share bias per
# crop per day bucket [CROP_DAY_BUCKETS], added to the same crop logits, so the
# mix the softmax reads can differ from day to day inside one theta.
#
# Read straight off theta (`params.cd`) rather than emitted by the head: the
# quantity is a proportion and the head already reaches the mix through `cm`,
# so a 32-wide matmul per bucket would be 288 coordinates to say what 45 say.
# Exactly inert at zero either way (`0.0 * G == 0.0`, `x + 0.0 == x`), and the
# OFF branch is the shipped expression character for character [LAW].
CROP_DAY_ON = False

#: Day edges of the `cd` buckets: days 0, 1, 2, 3, 4, 5, 6-10, 11-20, 21+.
#:
#: Per-day for the opening and then the hire bias's own joints (6, 11, 21).
#: The opening is where the block programme lives -- ymg_aq's pure-wheat day 2
#: and pure-strawberry day 3 are adjacent days, so a bucket holding both can
#: only average them, which is the season-constant failure one level down.
#: Past day 6 the top-five programmes are mixtures again (MACRO-EXTRACT
#: section 3) and a wider bucket is what the ES can afford to earn.  The hire
#: edges are a subset, so `HIRE_BIAS_BUCKETS`'s four-bucket scheme is this
#: block with coordinates tied and is measurable inside it.
CROP_DAY_BUCKETS = (1, 2, 3, 4, 5, 6, 11, 21)
assert len(CROP_DAY_BUCKETS) + 1 == PO.N_CROP_DAY_BUCKETS

#: `CROP_DAY_GAIN * sigma` is the per-draw log-share step, in nats.  The ES
#: trains at sigma 0.02, so 64 * 0.02 = 1.28 nats per standard deviation --
#: O(1) on the scale the softmax reads, and against the melon first-tile
#: boundary measured at B for the MELON gene (2.0487 nats) it is 1.6 sd for
#: the first tile.  `CROP_MIX_GAIN`'s 256 would be 5.12 nats a draw at this
#: sigma, which is a multi-tile jump every step; a raw gain of 1 would be
#: 0.02 nats, the 100x-dead gene the 2026-09-09 slope rule was written for.
CROP_DAY_GAIN = 64.0

#: Flip-per-logit for the switch genes: `plan`'s switch `i` is its module
#: default XOR `round(SWITCH_GAIN * z_i) > 0`, `z = gh @ sw + swb` [sw/swb].
#:
#: A *deadband*, not a sign test, and one-sided like `press` and `compact`: at
#: `z = 0` the decode is `floor(0.5 + eps) == 0`, so the untrained block is
#: every switch exactly where the module ships it, and a negative logit is the
#: same default rather than a second flip. A sign test (`z > 0`) would put half
#: the population on the far side of all ten switches at once and leave the
#: centre a measure-zero point the search never returns to.
#:
#: 8.0 is the measured gain, not a guess [GENE SLOPE RULE 2026-09-09]. Off B
#: (`flow193_g100_hr` padded) the head's `z` has sd 0.0672 at the training
#: sigma of 0.02, so the 1/(2*GAIN) threshold sits at 0.93 sd and **17 %** of a
#: 4,096-member antithetic population decodes a flip per gene (35 % at sigma
#: 0.05) -- a minority, so the centre is still the plan most members make, and
#: 1.7 flips per member rather than the 3.2 a gain of 16 gives.
#: `S/geneswitch/slope.py` is the measurement, `tests/test_geneswitch.py` the
#: bar it must keep clearing.
SWITCH_GAIN = 8.0

# ---- H1: tilt the plant mix towards unclaimed town appetite [SWITCH, OFF] ---
#
# Measured over 192 real-engine games against kagg2 (2026-08-30 profile):
# wheat is our worst channel at **41.9 coins/unit** over 190 units, with
# `corr(sellrev_WHEAT, margin) = -0.227`, while kagg2 pours 128 tiles and 670
# units of wheat into the same market; tomato is the mirror -- kagg2 plants and
# sells **zero**, the market holds `invend_TOMATO = -208` (scarce), and it is
# our best channel at **164.5 coins/unit** off 23 units a game.
#
# The planner already computes the scalar that separates them:
# `residual_drain`'s `share` column is the fraction of the town's *remaining*
# season appetite for a product that the supply on **both** boards has not yet
# claimed. Wheat's is pushed down by the opponent's 128 tiles; tomato's stays
# high because nobody grows it. The `absorb` gate below reads the same column
# but only as a hard threshold at the clip floor -- it can veto melon and it
# can say nothing at all about the five crops that sit between -0.2 and +1.2.
#
# This is that column as a *soft* logit on the mix instead, which is the
# general statement of H1 ("plant into demand nobody has claimed") rather than
# a wheat/tomato special case: nothing here names a crop, so it transfers to
# any opponent whose supply mix differs from ours. Added after the sharpness,
# in raw log-share units, for exactly the reason `animal_mix` is
# (`policy.py`'s `g8` note): a bias folded into the score before the sharpness
# is a different bias on every board.
#
# Not a gene: the theta layout is frozen [LAW], so this is a hand-set constant
# and the champion must decode identically with it off. OFF skips the add
# entirely rather than adding a zero, so not even a float rounding can differ.
#
# MEASURED 2026-08-30 at `PLANT_MIX_DRAIN_GAIN = 1.0`, 96 seeds x 2 seats
# against kagg2 (`--seed-base 20260828`), paired with the champion on
# (seed, seat) -- and the hypothesis is WRONG at this gain, decisively:
#
#     win 36.5% (champion 78.1) | mean margin -2,894 (champion +9,013)
#     paired diff -11,906, sd 10,717, t = -15.39
#     discordant: 5 games won that the champion lost, 85 lost that it won
#
# A logit of this size swamps a trained mix: the softmax's own sharpness is
# `1 + sig(head[7]) * 4` in [1, 5] over grow scores of order 1, so a gain of 1
# on a `share` column that spans ~1.4 is comparable to the whole learned
# signal, and the day plants what the drain says rather than what anything is
# worth. It also confirms the profile's own caveat from the other side: the
# tomato correlation is largely "we plant tomato in worlds where tomato pays",
# because forcing tomato in every world loses. A gain an order of magnitude
# smaller is the only version of this worth another run.
PLANT_MIX_DRAIN_ON = False
#: Logit gain on `share`. The five live crops span roughly 1.4 of `share`, so
#: 1.0 is about a 4x relative re-weighting between the ends of that span.
PLANT_MIX_DRAIN_GAIN = 1.0

_SOFTPLUS0 = float(np.log(2.0))


def _softplus(xp, z):
    return xp.maximum(z, 0.0) + xp.log1p(xp.exp(-xp.abs(z)))


def _unit_ratio(xp, z):
    """softplus(z) / softplus(0): exactly 1 at z = 0, positive everywhere."""
    return _softplus(xp, z) / _SOFTPLUS0


def _qfloor(xp, x):
    """`floor` with the cross-backend guard. Use for every decoded quantity.

    Absolute below ~100, relative above: `QUANT_EPS` covers the small decodes
    (fractions, counts), `QUANT_REL * |x|` the coin-scaled ones.
    """
    return xp.floor(x + xp.maximum(QUANT_EPS, QUANT_REL * xp.abs(x)))


def _largest_remainder(xp, weights, total, n):
    """Split `total` across `n` buckets proportionally, deterministically.

    Floor the proportional shares, then hand the leftover out to the largest
    fractional parts, ties going to the lower index. Keeps sum(counts) == total
    without any rounding drift.
    """
    # Shift once and derive both parts from the shifted value, so base and frac
    # cannot disagree about which side of the cliff this bucket is on.
    # `sum(base) <= total` still holds: base_i <= share_i + QUANT_EPS, so the sum
    # can exceed `total` only by n*QUANT_EPS, which is far below the 1 it would
    # take to change an integer total. `left` therefore stays non-negative.
    share = weights * total.astype(weights.dtype) + QUANT_EPS
    base = xp.floor(share).astype(xp.int32)
    left = total - xp.sum(base)
    frac = share - xp.floor(share)
    # rank by descending fraction, ties to lower index
    # Rank descending by fraction with a tiny index-ordered tiebreak, then
    # argsort-of-argsort turns that ordering into a rank without a scatter.
    key = -(frac * (2 * n) + (n - 1 - xp.arange(n, dtype=frac.dtype)) / n)
    rank = xp.argsort(xp.argsort(key))
    return base + (rank < left).astype(xp.int32)


def _softmax(xp, z):
    e = xp.exp(z - xp.max(z))
    return e / xp.sum(e)


def decide(xp, theta, obs: PolicyObs) -> P.Macro:
    """Run the network and turn its outputs into an executable Macro."""
    i32 = xp.int32
    params = PO.unpack(xp, theta)
    prod, glob, drain = features(xp, obs)
    # One projection, two readings: the per-product timing the shared encoder
    # gets (`fh`/`fs`) and the board total the global head gets (`fv`).
    boards = board_forecasts(xp, obs)
    out = PO.forward(xp, params, prod, glob, drain,
                     production_forecast(xp, obs, boards),
                     forward_value(xp, obs, boards),
                     market_momentum(xp, obs))
    scores, head = out.scores, out.head
    grow, sell = scores[:, 0], scores[:, 1]

    sig = lambda z: 1.0 / (1.0 + xp.exp(-z))

    aux = out.aux            # g5/gb5 block: zero (hence inert) for pre-g5 thetas

    # head[1] alone learned a threshold on nquad (measured 2026-08-23: +1.0
    # while broke, -0.5 once a second quadrant exists, with 50k in hand).
    # aux[1] scales a cash-to-price ratio so "rich relative to the next
    # quadrant" can push the decision; zero for pre-g5 thetas. Clipped: the
    # raw ratio reaches ~50, which would make one sigma step on gb5[1] a
    # 2.5-logit swing.
    #
    # Re-typed from a boolean to *coins* (PLANNER_V3_1 section 2): the planner
    # now prices a quadrant itself, and the gene is a signed bias on that
    # price, scaled by the quadrant's own cost so the transform is bounded and
    # exactly zero at z = 0. At init the planner therefore buys land iff land
    # pays; saturated positive the gene demands only that the quadrant not be
    # worth less than its price, saturated negative it demands a full price of
    # margin. It can never force a worthless quadrant nor refuse an arbitrarily
    # valuable one.
    land_cost = xp.asarray(spec.LAND_PRICES.astype(np.float32))[xp.clip(obs.nquad - 1, 0, 2)]
    afford = xp.clip(obs.money.astype(xp.float32) / land_cost - 1.0, -1.0, 4.0)
    land_price = xp.asarray(spec.LAND_PRICES)[xp.clip(obs.nquad - 1, 0, 2)].astype(i32)
    land_frac = _qfloor(xp, xp.tanh(head[1] + aux[1] * afford)
                        * LAND_BIAS_STEPS).astype(i32)
    land_bias = (land_price * land_frac) // LAND_BIAS_STEPS

    # M1: a quadrant bought this morning is developed this afternoon, so its
    # tiles are counted *before* development is sized -- `n_dev = dev_frac *
    # n_free` and `plant_total = n_dev - animal_count` are both capped by this
    # count, so a head that cannot see the new tiles can never ask for enough
    # plantings to fill them however willing the planner is.
    #
    # `land_ok` is "the gene has not vetoed it and it is affordable" -- `brain`
    # cannot run the valuation, so it keeps a boolean notion of "land is a live
    # candidate" and leaves the coins to `_derive`. The prediction is doubly
    # approximate (it knows neither the hire bill nor the reserve nor the
    # valuation), but one-sided and bounded: over-asking costs nothing on the
    # placement side (`plant_here` is masked by `free_slot`) and `plan._wants`
    # clips the seed want to the tiles that will exist.
    land_ok = ((land_bias > -land_price) & (obs.nquad < 4)
               & (obs.money.astype(xp.float32) >= land_cost)).astype(i32)
    n_free = n_free_slots(xp, obs, land=land_ok)

    # Animals and crops compete for the same free tiles; the head splits them.
    # One fraction for every day left a freshly bought quadrant empty for days
    # (forced-land counterfactual, 2026-08-23: 35 tiles idle all game). aux[2]
    # lets the share of free tiles raise development; zero for pre-g5 thetas.
    dev_frac = sig(head[5] + aux[2] * n_free.astype(xp.float32) / 25.0)
    n_dev = _qfloor(xp, dev_frac * n_free.astype(xp.float32)).astype(i32)
    if HERD_TILT:                           # see the HERD_TILT block above
        animal_share = sig(head[6] + HERD_TILT
                           * xp.maximum(obs.day.astype(xp.float32) - 12.0, 0.0)
                           / 10.0)
    else:
        animal_share = sig(head[6])
    animal_count = _qfloor(xp, animal_share * n_dev.astype(xp.float32)).astype(i32)
    if HERD_RAMP_ON:
        # Push up to HERD_RAMP_SHIFT of the day's development from crops to
        # animals while the early purse is the binding resource; `n_dev` is
        # unchanged, so `plant_total = n_dev - sum(animal_want)` pays for it.
        animal_count = xp.minimum(
            animal_count + xp.where(obs.day < HERD_RAMP_DAYS,
                                    i32(HERD_RAMP_SHIFT), i32(0)), n_dev)

    # Which animals: a proportional split of the day's acquisition across the
    # three kinds, exactly as the crops are split below. It replaces an
    # `argmax` over the same three grow scores, and the argmax was not a
    # tie-break detail -- at z = 0 all three scores are equal and `xp.argmax`
    # returns the first maximum, so an untrained policy bought geese and
    # nothing else, on every board, for the whole season. A split asks for some
    # of each and lets `budget.grant` price the mix in coins (`budget.L_ANIMALS`).
    #
    # `animal_mix` (`g8`/`gb8` column 1..3, zero -- hence inert -- for every
    # theta written before the block) is added *after* the sharpness, so it
    # stays in raw log-share units whatever `head[2]` does to the scores. It is
    # the only path to the want that does not go through the grow score, and
    # that is the whole point: `_unit_ratio(grow)` is what `budget.grant`
    # prices the animal at and it is clipped at `GROW_MAX`, so two scores far
    # enough apart to move the want are both still worth 4x and the cheaper
    # animal takes the pasture. Measured 2026-08-28 on `wool_specialist`: a
    # want of 0.67 sheep written in the grow score placed 21 COW and 0 SHEEP.
    a_mix = xp.clip(out.crew[1:], -ANIMAL_MIX_CLIP, ANIMAL_MIX_CLIP)
    wa = _softmax(xp, xp.stack([grow[spec.I_EGG], grow[spec.I_MILK], grow[spec.I_WOOL]])
                  * (1.0 + sig(head[2]) * 4.0) + a_mix)
    animal_want = _largest_remainder(xp, wa, animal_count, spec.N_ANIMALS)
    plant_total = n_dev - xp.sum(animal_want)

    # Which crops: proportional split of plant_total by grow score.
    # The OFF branch is the original expression, character for character, and
    # not a `+ 0.0` or a hoisted temporary [LAW]: XLA schedules and fuses the
    # whole of `decide` as one program, so *any* edit to the graph can move a
    # float32 rounding somewhere else in it. Measured 2026-08-30 -- naming the
    # product as a local and reading it back moved `hire_bias` by one coin on
    # 2 of the 2,400 fixture decisions of `tests/test_backend_agreement.py`,
    # with the switch off. Two branches keep the shipped program bit-identical.
    # Preserve the original expression for older layouts. The full layout
    # adds a learned log-share residual; zero padding must reproduce the old
    # decode on both backends (covered against the frozen incumbent source).
    if theta.shape[0] > PO.offset("cm"):
        crop_logits = grow[:spec.N_CROPS] * (1.0 + sig(head[7]) * 4.0)
        if PLANT_MIX_DRAIN_ON:
            crop_logits = crop_logits + PLANT_MIX_DRAIN_GAIN * drain[:spec.N_CROPS, 1]
        if CROP_DAY_ON:                         # see the CROP-DAY gene block above
            # Same selection as `hire_bias` below -- a count of the edges the
            # day has passed, then one dynamic index -- and the same units as
            # `crop_mix`, so the clip that bounds the exponent is the one that
            # was already there.
            cd_bucket = xp.sum((obs.day >= xp.asarray(
                np.asarray(CROP_DAY_BUCKETS, np.int32))).astype(i32), dtype=i32)
            crop_logits = crop_logits + xp.clip(
                CROP_DAY_GAIN * params.cd[:, cd_bucket], -CROP_MIX_CLIP, CROP_MIX_CLIP)
        if TURN_COST:                           # see the TURN_COST block above
            crop_logits = crop_logits - xp.clip(
                TURN_COST * xp.asarray(np.asarray(TURN_COST_TURNS, np.float32)),
                -CROP_MIX_CLIP, CROP_MIX_CLIP) * (
                    obs.day >= i32(TURN_COST_DAY)).astype(xp.float32)
        if MELON_GENE_ON:                       # see the MELON gene block above
            w = _softmax(xp, crop_logits + xp.clip(CROP_MIX_GAIN * out.crop_mix,
                                                   -CROP_MIX_CLIP, CROP_MIX_CLIP))
        else:
            w = _softmax(xp, crop_logits + xp.clip(out.crop_mix, -CROP_MIX_CLIP, CROP_MIX_CLIP))
    elif PLANT_MIX_DRAIN_ON:                    # [H1] see the block above
        w = _softmax(xp, grow[:spec.N_CROPS] * (1.0 + sig(head[7]) * 4.0)
                     + PLANT_MIX_DRAIN_GAIN * drain[:spec.N_CROPS, 1])
    else:
        w = _softmax(xp, grow[:spec.N_CROPS] * (1.0 + sig(head[7]) * 4.0))
    # Engine fact, not a gene: nothing is harvestable before
    # day + CROP_FIRST_YIELD_DAY, and `VAL.pay_day()` is the last day whose
    # harvest is sold -- so a crop harvested after it is never sold. It must be
    # harvestable by that day or the seed is thrown away. Masked weights are
    # renormalised; if nothing can mature, nothing is planted.
    #
    # Which day that is, is `plan.HORIZON_DROP_ON`'s question. OFF it is day 28
    # (the sale is decoded from the hour-0 shed, so a day-29 harvest never
    # reaches a lot); ON the day-29 DROP chain sells it, and wheat and carrot
    # become plantable on day 27, tomato on 21, strawberry and melon on 19.
    can_mature = (obs.day + xp.asarray(spec.CROP_FIRST_YIELD_DAY)
                  <= VAL.pay_day()).astype(xp.float32)
    w = w * can_mature
    # Market fact, and the second half of the same question. `can_mature` asks
    # whether the seed reaches the shed in time; `absorb` asks whether there is
    # anyone left to sell it to. `residual_drain`'s `share` column is the
    # fraction of the town's whole remaining appetite for a product that the
    # supply on both boards has not already claimed, so `share <= 0` says every
    # further unit is oversupply by construction -- it will meet a quote set by
    # the units queued ahead of it, not by today's.
    #
    # Melon is the case this exists for (measured 2026-08-26, route1 best_abs
    # vs kagg2 over 16 real-engine games): its whole season drain is the 30
    # town-centre ticks, its `above` curve is `sq` at 3.6x, so 158 units above
    # I0 take the quote to the $1 floor. Both seats between them commit 213.
    # kagg2 harvests first and books 120 units at 0.77x base; kagg3 arrives on
    # day 13 and books 96 at 0.32x, ~37 of them at or under 16 coins. Nothing
    # on the sell side can recover that -- the shed is already emptied into the
    # first lot of the morning after every harvest (`us_shed == us_sold` on
    # every day of the trace). The loss is committed at *planting* time, by
    # `valuation.py` pricing a tile's whole future output at today's hour-0
    # quote, which for melon on day 10 is 271 against a realized 84.
    #
    # The threshold is the clip floor, not zero. Measured over a season
    # (route1 best_abs vs kagg2, seed 1234): melon's `share` is pinned at
    # `-DRAIN_CLIP` from day 1 -- one melon tile on either board already
    # commits more than the town will eat all season -- while wheat, carrot,
    # tomato, strawberry and egg sit between -0.2 and +1.2 and cross zero
    # freely. A `share > 0` gate is therefore a knife edge on the five crops
    # that are fine and costs 5,250 coins a game in lost planting; `share >
    # -DRAIN_CLIP` names exactly the saturated market and nothing else. The
    # docstring on `DRAIN_CLIP` says the same thing from the other side:
    # saturating is the correct reading for melon and fertilizer, "every unit
    # of those two is oversupply by construction".
    #
    # The gate is a bias, not a constant: `tanh` is exactly 0.0 at zero theta,
    # so the shipped default is the clip-floor test above, and ES can walk the
    # threshold anywhere in (-2*DRAIN_CLIP, 0] -- saturated positive it plants
    # regardless, saturated negative it demands unclaimed appetite. Crops only:
    # the herd's three products are drained markets where the same test is
    # slack until day 21, and gating a placement on it would put an animal
    # purchase behind a threshold nothing measured asks for.
    absorb = (drain[:spec.N_CROPS, 1] + DRAIN_CLIP * xp.tanh(out.sat)
              > -DRAIN_CLIP).astype(xp.float32)
    w = w * absorb
    w_sum = xp.sum(w)
    # Guard only the exact-zero case: flooring the divisor at 1e-6 would
    # under-renormalise whenever 0 < w_sum < 1e-6 (renormalised weights would
    # sum to w_sum/1e-6, not 1, and _largest_remainder would under-allocate
    # plant_total). The untaken w_sum == 0 branch divides by 1.0 instead --
    # any nonzero placeholder works since xp.where discards it -- so there is
    # no NaN either way.
    w = xp.where(w_sum > 0, w / xp.where(w_sum > 0, w_sum, 1.0), w)
    plant_total = xp.where(w_sum > 0, plant_total, 0).astype(i32)
    plant_target = _largest_remainder(xp, w, plant_total, spec.N_CROPS)

    # The re-typed value outputs (PLANNER_V3_1 section 2). Each is quantized
    # where it becomes an integer, and none is a decision: the planner makes
    # those from these values and the engine's tables.
    #
    # `hold` is the one decode that is linear in its logit, so it is also the
    # one that can run away: clipped below `spec.COIN_CAP` both to keep the
    # coin values inside the range the planner's ratio arithmetic assumes and
    # because `.astype(int32)` of an unclipped float diverges between the
    # backends at the extreme (numpy wraps, XLA saturates). One cap, shared:
    # `budget.VALUE_CAP`, `plan`'s task-value clip and `sell.LIQUIDATE` are all
    # `spec.COIN_CAP`, which is what makes `LIQUIDATE < every decodable hold`
    # true by construction (`core/sell.py`'s reservation invariant).
    #
    # The cap sits *below* the price table's dearest quote (1,053,252, reached
    # only at the table's low end, inventory -5,000), so a reservation cannot
    # be decoded high enough to outbid the scarcest possible market. That is
    # not reachable in a season: the market opens at 10,000 units of every
    # product and the town removes under 1,700 of them over 30 days (a shop
    # eats at most 2 units a tick, 6 ticks a day, and the eighth shop only
    # unlocks on day 24), while both seats only ever *add* supply by selling.
    base = xp.asarray(_BASE)
    # Clipped *after* the guard: `QUANT_REL` adds about a coin at the cap, and
    # the cap is the invariant (`sell.LIQUIDATE < every decodable hold`).
    hold = xp.minimum(_qfloor(xp, 0.8 * base * _unit_ratio(xp, sell)),
                      spec.COIN_CAP - 1).astype(i32)                              # coins per unit kept
    press = _qfloor(xp, base * xp.maximum(xp.tanh(out.gate), 0.0)).astype(i32)    # coins per lot of delay
    grow_mult = _qfloor(xp, xp.minimum(_unit_ratio(xp, grow), GROW_MAX) * GROW_ONE).astype(i32)

    # The development genes (`g6`/`gb6`, zero -- hence inert -- for every theta
    # written before the block). Neither is a decision either: `compact` says
    # how many distance bands the planner may resolve when it picks *which*
    # free tiles to develop, and `dev_weight` what a planting or a placement is
    # worth to the labour router relative to a harvest.
    #
    # `compact` is one-sided, like `press`: `relu(tanh(z))`, so 0 at z = 0 and
    # a negative logit is "off" rather than "develop the far corners", which is
    # not a strategy anything measured wants. Saturated it is `DIST_MAX`, where
    # the planner's bucket key is `DIST_SHED` itself.
    compact = _qfloor(xp, DIST_MAX * xp.maximum(xp.tanh(out.dev[0]), 0.0)).astype(i32)
    # x1 at z = 0, capped at the same 4x as `grow_mult` -- which is what keeps
    # `v_plant * dev_weight` inside int32 against `plan`'s coin ceiling.
    dev_weight = _qfloor(xp, xp.minimum(_unit_ratio(xp, out.dev[1]), GROW_MAX)
                         * GROW_ONE).astype(i32)

    # The crew gene (`g8`/`gb8` column 0 plus `g9`/`gb9`, zero -- hence inert --
    # for every theta written before the block). Not a crew *count*: `plan`
    # section 1.5 still enumerates every affordable `h` and takes the argmax of
    # admitted task value less `HIRE_BILLS[h]`, and this is a signed per-hand
    # bias on that gain. `tanh` is exactly 0.0 at zero, so the enumeration adds
    # `0 * h` and the day hires exactly what it hired before the gene existed.
    #
    # Four biases, one per day bucket [HIRE_BIAS_BUCKETS], selected here rather
    # than in `plan`: the planner takes one integer, which keeps 1.5's
    # enumeration and both backends exactly as they were, and the day is a
    # *decode* input like every other feature the head reads. The selection is
    # a count of the edges the day has passed and then one dynamic index --
    # the same shape as the `LAND_PRICES` lookup a few lines up, so it is
    # three comparisons and a gather on either backend and no `where` chain.
    all_bias = _qfloor(xp, HIRE_BIAS_MAX * xp.tanh(out.hire)).astype(i32)
    bucket = xp.sum((obs.day >= xp.asarray(np.asarray(HIRE_BIAS_BUCKETS, np.int32))
                     ).astype(i32), dtype=i32)
    hire_bias = all_bias[bucket].astype(i32)

    # The crew ramp (`g10`/`gb10`, zero -- hence inert -- for every theta
    # written before the block). `hire_bias` is a constant per hand inside a
    # day bucket and so it can only ever *tilt* the enumeration; this is a
    # target the day is measured against, which is what the Kaggle loss
    # signature asks for (12 hands and 9k cash by day 10 against our 6 and
    # 3.3k, with the difference sitting in animals and coops).
    #
    # A logistic in the day, decoded here for the same reason the hire bucket
    # is: the planner takes one integer and the day is a decode input like
    # every other feature the head reads. `relu(tanh)` on the height rather
    # than `tanh`, because a negative target is not a strategy -- "hire fewer
    # than the enumeration wants" is already `hire_bias < 0` -- and it is what
    # makes the block exactly inert: at zero the height is 0.0, so the product
    # with the sigmoid is 0.0 whatever the midpoint and steepness decode to,
    # and `_qfloor(0.0)` is 0 on both backends.
    crew_top = CREW_TARGET_MAX * xp.maximum(xp.tanh(out.ramp[0]), 0.0)
    crew_mid = CREW_MID_MAX * sig(out.ramp[1])
    crew_steep = CREW_STEEP_MAX * sig(out.ramp[2])
    crew_target = xp.clip(
        _qfloor(xp, crew_top * sig(crew_steep * (obs.day.astype(xp.float32) - crew_mid))),
        0, spec.MAX_HANDS).astype(i32)
    # The deferral, in `DEFER_ONE` fixed point so the planner scales integers
    # and both backends agree exactly. One-sided like the height: "spend *more*
    # on animals while the crew is short" is the plant/animal split's own
    # decision (`head[6]`), not this gene's.
    animal_defer = xp.clip(_qfloor(xp, DEFER_ONE * xp.maximum(xp.tanh(out.ramp[3]), 0.0)),
                           0, DEFER_ONE).astype(i32)

    # The forward-admit horizon (`g11`/`gb11`, zero -- hence inert -- for every
    # theta written before the block). How many days ahead `plan` 1.5's hire
    # scan is allowed to project the board when it prices a crew, and nothing
    # else: the route, the admission and the market row all walk the work the
    # day actually has [FORWARD_ADMIT].
    #
    # Decoded here rather than in `plan` for the same reason the hire bucket
    # and the crew target are: the planner takes one integer and both backends
    # then trace the identical program. A *rounded* line, unlike every other
    # decode in this function, because this one is a small count and not a
    # fixed-point ratio -- and a line rather than the logistic the block
    # shipped with, because `FWD_DAYS_GAIN` documents the measurement that the
    # logistic's shift put the gene in a zone where no ES perturbation at
    # sigma 0.02 moved the horizon at all. The `+ 0.5` is the rounding, the
    # clip is the range, and `_qfloor` is the cross-backend floor, so the tie
    # at `x.5` breaks upward identically under numpy and XLA.
    #
    # Exactly inert at zero: `16 * 0.0 + 0.5` is 0.5, `_qfloor` of it is 0, and
    # a zero horizon is `age + 0 >= window`, the mask that was already there --
    # so `plan` skips the projected pass outright. Negative logits clip to the
    # same 0: "look back" is not a horizon.
    forward_days = xp.clip(
        _qfloor(xp, FWD_DAYS_GAIN * out.fwd + 0.5),
        0, FWD_DAYS_MAX).astype(i32)

    # The switch genes (`sw`/`swb`, zero -- hence inert -- for every theta
    # written before the block). int32[N_SWITCH_GENES], 1 where the day wants
    # `plan.SWITCH_GENES[i]` at the *other* value from the one the module
    # ships; `plan._sw` does the XOR, because only `plan` knows what the module
    # currently says and whether the lead has overridden it.
    #
    # Decoded for every theta, short or long: `PO.unpack` zero-pads a shorter
    # one, `z` is then exactly 0.0, and the vector is `plan.SWITCH_DEFAULT` --
    # every switch at the value its module constant ships with. Emitting the
    # zero vector rather than `None` keeps the decode *one object* for every
    # layout, which is what lets a pre-block theta and its padding be compared
    # field by field (`tests/test_crew_and_herd_mix.py`), and on the numpy path
    # the concrete zero still takes each site's original Python branch, so no
    # `where` is built and the shipped program is the one it always was.
    #
    # Read off `gh`, so a switch may depend on the board: a gene-switch is a
    # strictly wider object than the constant it replaces, which could only
    # ever be set for the whole season.
    switches = (_qfloor(xp, SWITCH_GAIN * out.switch + 0.5) > 0).astype(i32)
    # [g12] Days the fertilizer site looks ahead before spending a unit today,
    # decoded exactly as `forward_days` is and inert at zero for the same
    # reason: `16 * 0.0 + 0.5` is 0.5, `_qfloor` of it is 0, and a zero
    # look-ahead leaves `fert_cand` the expression it always was, so `plan`
    # skips the projected valuation outright.
    fert_defer = xp.clip(
        _qfloor(xp, FERT_DEFER_GAIN * out.ft + 0.5),
        0, FERT_DEFER_MAX).astype(i32)

    return P.Macro(
        plant_target=plant_target,
        animal_want=animal_want,
        land_bias=land_bias,
        hold=hold,
        press=press,
        grow_mult=grow_mult,
        compact=compact,
        dev_weight=dev_weight,
        hire_bias=hire_bias,
        crew_target=crew_target,
        animal_defer=animal_defer,
        forward_days=forward_days,
        switches=switches,
        fert_defer=fert_defer,
    )
