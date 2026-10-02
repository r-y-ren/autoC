"""Opponent-free price projection: exact own-impact table arithmetic.

PLANNER_V3_1 section 1.1. Verified facts this module stands on:

* price is monotone non-increasing in inventory for every product over the
  whole table (0 violations in 85,001 entries per row);
* the town raises prices: every shop instance consumes SHOP_CONSUME each
  SHOP_SELL_INTERVAL turns, the centre consumes one of everything but
  fertilizer once a day (turn 0);
* a sale at PRICE_FLOOR pays the seller but does not add to supply -- and
  since the table is monotone, quoting `price[inv + j]` for the j-th unit is
  still exact once the floor is reached (the walk in sim/market.py leans on
  the same fact);
* buys always drain supply.

Opponent impact is absent by construction -- that is the genes' job.  Under
`plan.OPP_SUPPLY_ON` (off by default) it is no longer absent: a measured
per-turn opponent supply curve is added to every projection, see
`opp_supply_to_turn` below.  With the switch off not one expression here
changes -- the `day` argument every projector takes is optional and the
opponent term is only reached when a caller passes it *and* the switch is on.

Array-agnostic (`xp` = numpy or jax.numpy). Turn arguments are Python ints,
so the tick counts fold at trace time. `core` must not import `sim` (the sim
imports `core`), which is why the quote walk is restated here.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from .. import spec

#: Longest quote walk: one order never moves more than a shed's worth.
K = spec.SHED_CAPACITY + 1

# ------------------------------------------------------------ opponent supply
#
# WHY THIS EXISTS. The opponents that beat us on Kaggle are open-loop scripts:
# `scripts/extract_opp_supply.py` reads their market rows out of the tape
# library and finds that two tapes of the same team agree on 96.6 % of their
# per-turn SELL / BUY_PRODUCT volumes (3 of 13 repeat teams are byte-identical
# all game, and every repeat team is identical through turn 51). Their future
# supply into the shared pot is therefore forecastable by turn and product,
# and a forecast is exactly what `projected_inv` is missing: it walks the town
# tick forward and nothing else, so it quotes lot 3 against an inventory the
# other seat has already flooded.
#
# WHAT IS ADDED. `S[turn, product]`, the population-mean *net* recorded units
# (SELL minus BUY_PRODUCT), cumulated from the day's hour 0 through the turn
# whose market is being projected -- inclusive, because both seats' orders
# resolve in the same market phase and the engine advances the shared
# inventory in lockstep across the pair (`sim/market.py`).
#
# WHAT IT IS NOT. It is the *recorded* row, not the executed one: a SELL the
# engine clipped to the seat's shed still counts at its recorded size, so the
# curve is an upper bound on real dumping. `OPP_SUPPLY_SCALE` is where that
# is priced; the paired engine run is what sets it.

#: Population mean over the whole tape library. `S_band6` / `S_wall6` /
#: `S_top10` sit beside it -- picking one of those fits the curve to the panel
#: it will be measured on, so the default is the field.
OPP_SUPPLY_DEFAULT_PATH = "artifacts/opp_supply/S_pop.npy"

#: (path, scale) -> (turn_cum int32[N_DAYS, TURNS_PER_DAY, 9],
#:                    day_prefix int32[N_DAYS + 1, 9]).
#: Both are rounded *after* cumulating: a per-turn mean of 0.3 units rounds to
#: nothing on its own but to a real dump over a day.
_OPP_TABLES: dict = {}


#: `plan`'s live module namespace, registered by `plan` at import (`plan`
#: imports this module, so the dependency cannot run the other way).
#:
#: The namespace and not `sys.modules`: `eval_vs_baselines._vendored_imports`
#: **deletes every `kagg3.*` entry from `sys.modules`** for the length of a
#: game that seats a packaged file agent -- which is every tape game -- so a
#: `sys.modules` lookup inside the planner reads None exactly when it matters
#: and the switch is silently off. Measured, not theorised: the first band6
#: leg run this way paired 192/192 identical to the switch-off reference.
#: A dict reference outlives the purge (the module object stays alive in the
#: agent closure) and still sees a harness's runtime `setattr`.
_PLAN_NS: dict | None = None


def bind_plan(ns):
    """Register `plan`'s `globals()`. Called by `plan` at import."""
    global _PLAN_NS
    _PLAN_NS = ns


# [SWITCH, RIVALSUPPLY2 2026-09-29] OPP_SUPPLY_FAMILY_ON: the curve is chosen per game by the rival's
# family (P48 / PQ4 / MEL = either before d10 / V56; `pop` before the step-1 latch), read live by
# `agent/runtime.Runtime._opp_family` and handed here.  The per-game latch lives in THIS module (the
# code that reads it), not in `plan`'s namespace, so a harness that re-imports `plan` cannot lose it.
#: The family curves, packaged beside this module (`opp_supply/S_<family>.npy`).
OPP_FAMILY_DIR = Path(__file__).resolve().parent / "opp_supply"
_OPP_FAMILY = {"fam": None}


def set_opp_family(fam):
    """[SWITCH, RIVALSUPPLY2] the current game's rival family (None = not yet known -> `pop`)."""
    _OPP_FAMILY["fam"] = fam


def opp_family():
    return _OPP_FAMILY["fam"]


def _opp_switch():
    """(path, scale) when `plan.OPP_SUPPLY_ON`, else None.

    `plan` not imported -> the switch is off, which is the byte-identical
    path. Read at call time, because the harnesses set the flag on the live
    module after import.
    """
    ns = _PLAN_NS
    if ns is None:
        plan = sys.modules.get(__name__.rsplit(".", 1)[0] + ".plan")
        ns = getattr(plan, "__dict__", None)
    if ns is not None and ns.get("OPP_SUPPLY_FAMILY_ON", False):       # [SWITCH, RIVALSUPPLY2]
        fam = str(ns.get("OPP_SUPPLY_FAMILY_FORCE", "") or "") or _OPP_FAMILY["fam"] or "pop"
        if fam == "NONE":                                               # [SWITCH, RSFIX1] off-list rival: S_OTH or no curve
            oth = OPP_FAMILY_DIR / "S_OTH.npy"
            if not oth.exists():
                return None
            return (str(oth), float(ns.get("OPP_SUPPLY_SCALE", 1.0)))
        return (str(OPP_FAMILY_DIR / f"S_{fam}.npy"), float(ns.get("OPP_SUPPLY_SCALE", 1.0)))
    if ns is None or not ns.get("OPP_SUPPLY_ON", False):
        return None
    return (ns.get("OPP_SUPPLY_PATH", OPP_SUPPLY_DEFAULT_PATH),
            float(ns.get("OPP_SUPPLY_SCALE", 1.0)))


def _opp_path(path: str) -> Path:
    p = Path(path)
    if p.exists():
        return p
    root = Path(__file__).resolve().parents[3]      # src/kagg3/core -> repo
    if (root / path).exists():
        return root / path
    raise FileNotFoundError(
        f"OPP_SUPPLY_ON is set but the supply curve {path!r} is missing "
        f"(build it with scripts/extract_opp_supply.py)")


def _opp_tables(key):
    """Cumulative supply tables for `key = (path, scale)`, built once."""
    tables = _OPP_TABLES.get(key)
    if tables is None:
        path, scale = key
        s = np.load(_opp_path(path)).astype(np.float64)
        assert s.shape == (spec.EPISODE_STEPS, spec.N_PRODUCTS), s.shape
        by_day = s.reshape(spec.N_DAYS, spec.TURNS_PER_DAY, spec.N_PRODUCTS)
        turn_cum = np.rint(scale * by_day.cumsum(1)).astype(np.int32)
        day_tot = by_day.sum(1)
        prefix = np.concatenate([np.zeros((1, spec.N_PRODUCTS)),
                                 day_tot.cumsum(0)])
        tables = (turn_cum, np.rint(scale * prefix).astype(np.int32))
        _OPP_TABLES[key] = tables
    return tables


def _day_index(xp, day):
    """`day` clipped into the season, as an index both backends accept."""
    return xp.clip(xp.asarray(day).astype(xp.int32), 0, spec.N_DAYS - 1)


def opp_supply_to_turn(xp, day, turn: int):
    """int[9]: forecast opponent units in the pot when `turn` resolves on
    `day`, cumulated from that day's hour 0. Zero when the switch is off."""
    key = _opp_switch()
    if key is None or day is None:
        return None
    turn_cum, _ = _opp_tables(key)
    h = min(max(int(turn), 0), spec.TURNS_PER_DAY - 1)
    return xp.asarray(turn_cum[:, h, :])[_day_index(xp, day)]


def opp_supply_over_days(xp, day, days_ahead):
    """int[9]: forecast opponent units added between `day`'s hour 0 and
    `days_ahead` whole days later -- `days_ahead` scalar or per product, the
    shape `inv_at_day` takes. Zero when the switch is off."""
    key = _opp_switch()
    if key is None or day is None:
        return None
    _, prefix = _opp_tables(key)
    pre = xp.asarray(prefix)
    i32 = xp.int32
    zero9 = xp.zeros(spec.N_PRODUCTS, i32)
    pid = xp.arange(spec.N_PRODUCTS, dtype=i32)
    d0 = _day_index(xp, day) + zero9
    d1 = xp.clip(d0 + xp.asarray(days_ahead).astype(i32), 0, spec.N_DAYS)
    return pre[d1, pid] - pre[d0, pid]


def ticks_before(turn: int) -> tuple[int, int]:
    """(shop ticks, centre ticks) fired before the market resolves at `turn`.

    A turn runs unit ops, then market orders, then the town tick, so the ticks
    of turns 0 .. turn-1 have fired: shop ticks at every multiple of
    SHOP_SELL_INTERVAL, the centre tick at turn 0 (step % 24 == 0).
    """
    turn = int(turn)
    shop = (turn + spec.SHOP_SELL_INTERVAL - 1) // spec.SHOP_SELL_INTERVAL
    center = 1 if turn >= 1 else 0
    return shop, center


def town_tick_units(xp, shops):
    """int[9]: units the town's shops remove per shop tick."""
    return shops.astype(xp.int32) @ xp.asarray(spec.SHOP_CONSUME)


def projected_inv(xp, mkt_inv, shops, turn: int, day=None):
    """int[9]: market inventory when the market resolves at `turn`, from the
    hour-0 inventory, before any own order that turn.

    Opponent-free unless the caller passes `day` *and* `plan.OPP_SUPPLY_ON` is
    set, in which case the day's forecast opponent supply through `turn` is
    added -- see the module header.

    May go negative, deliberately: the engine does not clip `mkt_inv` either,
    and `sell_quotes` clips the *table index*, which is where the price curve
    actually bottoms out. Clamping here would diverge from the sim.
    """
    shop, center = ticks_before(turn)
    inv = (mkt_inv.astype(xp.int32)
           - shop * town_tick_units(xp, shops)
           - center * xp.asarray(spec.TOWN_CENTER_CONSUME))
    opp = opp_supply_to_turn(xp, day, turn)
    return inv if opp is None else inv + opp


def sell_quotes(xp, price_table, inv):
    """int[9, K]: price paid for the j-th unit (j = 0..K-1) of each product
    sold solo from inventory `inv` -- the engine's quote walk, tabulated."""
    j = xp.arange(K, dtype=xp.int32)
    idx = xp.clip(inv.astype(xp.int32)[:, None] + j[None, :] - spec.PRICE_TABLE_LO,
                  0, spec.PRICE_TABLE_N - 1)
    return xp.take_along_axis(price_table, idx, axis=1)


def sell_revenue(xp, quotes, qty):
    """int[9]: revenue of selling `qty[p]` units along `quotes[p]`.

    int32 on both backends: `np.cumsum` would upcast an int32 input to int64
    while `jnp.cumsum` would not, so the dtype is pinned rather than inherited.
    It fits: the dearest quote in the table is 1,053,252 and the walk is at
    most K = 101 units, so no partial sum passes 1.07e8.
    """
    cum = xp.cumsum(quotes, axis=1, dtype=xp.int32)
    q = xp.clip(qty.astype(xp.int32), 0, K - 1)
    last = xp.take_along_axis(cum, xp.maximum(q - 1, 0)[:, None], axis=1)[:, 0]
    return xp.where(q > 0, last, 0)


def marginal_quote(xp, quotes, sold):
    """int[9]: what the next unit fetches after `sold[p]` units have gone."""
    s = xp.clip(sold.astype(xp.int32), 0, K - 1)
    return xp.take_along_axis(quotes, s[:, None], axis=1)[:, 0]


def buy_quotes(xp, price_table, inv):
    """int[9, K]: price paid for the j-th unit (j = 0..K-1) of each product
    bought solo from inventory `inv`. Every unit drains one, so the j-th is
    quoted at `inv - 1 - j` -- the engine's walk, tabulated."""
    j = xp.arange(K, dtype=xp.int32)
    idx = xp.clip(inv.astype(xp.int32)[:, None] - 1 - j[None, :] - spec.PRICE_TABLE_LO,
                  0, spec.PRICE_TABLE_N - 1)
    return xp.take_along_axis(price_table, idx, axis=1)


#: Shop ticks per day: one every SHOP_SELL_INTERVAL turns.
SHOP_TICKS_PER_DAY = spec.TURNS_PER_DAY // spec.SHOP_SELL_INTERVAL


def daily_town_units(xp, shops):
    """int[9]: units the town removes per whole day -- six shop ticks plus
    the centre's one of everything but fertilizer."""
    return SHOP_TICKS_PER_DAY * town_tick_units(xp, shops) + xp.asarray(spec.TOWN_CENTER_CONSUME)


def inv_at_day(xp, mkt_inv, shops, days_ahead, day=None):
    """int[9]: the hour-0 inventory advanced `days_ahead` days of town drain
    (scalar or int[9]), before any own order -- opponent-free unless the
    caller passes `day` and `plan.OPP_SUPPLY_ON` is set. The engine has no
    inventory floor, so none is applied; the price table's low end is the only
    clamp, taken by the caller's table read."""
    inv = (mkt_inv.astype(xp.int32)
           - xp.asarray(days_ahead).astype(xp.int32) * daily_town_units(xp, shops))
    opp = opp_supply_over_days(xp, day, days_ahead)
    return inv if opp is None else inv + opp
