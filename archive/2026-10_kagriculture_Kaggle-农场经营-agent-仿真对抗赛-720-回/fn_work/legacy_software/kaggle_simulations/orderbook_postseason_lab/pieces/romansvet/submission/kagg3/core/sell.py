"""The sell side [HEURISTIC, PLANNER_V3_1 section 1.2].

Two learned values per product: `hold`, what one unit is worth kept until
tomorrow, and `press`, the coins a unit is expected to lose per lot of delay
to opponent sales. Everything else is table arithmetic: the three lots' quote
curves from the projector (town ticks between lots, own earlier lots advancing
the later inventories), and a unit-by-unit greedy that gives each unit to the
lot whose *adjusted* marginal is highest and sells it only if that marginal
clears `hold`.

The adjustment has two parts. Timing pressure: `press * lot_index`. The
externality: a unit sold in lot l moves every later lot's start up by one,
which changes a later lot holding n units by `price[start + n] - price[start]`
(telescoping) -- charged to lot l so the greedy does not undercut its own
later sales. Verified opponent-free fact: selling later is weakly better on
every town-consumed product and exactly indifferent for fertilizer; with no
town and no pressure every lot quotes alike and ties fall to the earliest.

The reservation invariant
-------------------------
`LIQUIDATE = -spec.COIN_CAP` is strictly below **every decodable `hold`**:
`brain.decide` clips the reservation into `[0, COIN_CAP - 1]` (section 2), so
no learned reservation can ever reach it and `hold <= LIQUIDATE` is exactly
the day-29 liquidation mode [LAW, 0.4]. `allocate` tests that mode explicitly
rather than leaning on `best_adj >= hold`: an adjusted marginal is a *net*
value and can fall below `-COIN_CAP` on its own (a large `press` on a late
lot, or a deeply drained curve whose later-lot externality is worth more than
a million coins), and a liquidation that compares values would then quietly
keep units the law says must go.

Array-agnostic; the loop goes through core.loop so the simulator traces it.
Every value stays int32 on both backends: `np.cumsum`/`np.sum` widen an int32
input to int64 while their jnp counterparts do not (the hazard projector.py
documents), so both reductions pin `dtype`.
"""

from __future__ import annotations

from .. import spec
from . import loop
from . import ops as O
from . import projector as PJ

N_LOTS = len(O.SELL_TURNS)
#: Reservation that sells every unit whatever its adjusted marginal (day 29:
#: the terminal value of anything unsold is exactly zero [LAW, 0.4]). Below
#: every decodable `hold` -- see the module docstring's invariant.
LIQUIDATE = -spec.COIN_CAP

#: [REVFIX2 2026-09-29, astra review 3 finding 1] default OFF = the shipped arithmetic. ON: a unit sold at the $1
#: floor adds no supply (engine; sim/market.py), so the later lots' starts are REPLAYED (town drain between lots =
#: the inv_lots row differences) instead of `inv_lots + cumsum(lots)`. Identical to OFF whenever no priced unit
#: reaches the floor inventory (the numpy path returns the OFF body then).
FLOOR_IMPACT_ON = False
_FLOOR_CACHE = {}


def lot_inventories(xp, mkt_inv, shops, turns=None, day=None):
    """int[3, 9]: market inventory when each lot resolves, before any own sale
    that day.

    `turns` is the turns the three lots actually stand on -- `plan`'s
    `early_lot_turns()`, which is `O.SELL_TURNS` under the shipped
    `EARLY_SELL_MODE = "A"` and moves lots 2/3 up under "B"/"A21". It is an
    argument and not a `plan` import because `sell` is imported *by* `plan`;
    the default is the shipped layout, so every caller that does not care --
    and mode "A" itself -- reads exactly the curves it always read. Projecting
    a lot at a turn it is not sold on is what left lot 2 empty under mode "B":
    the allocator priced it against an 18-turn-drained shelf, put the whole
    day in lot 1, and the residue fell out of the day at hour 19.

    The curves are opponent-free unless `day` is given *and*
    `plan.OPP_SUPPLY_ON` is set, in which case each lot also carries the
    opponent supply forecast to land in the pot before it -- which is the
    whole point of that switch: lot 3 is the one the other seat has already
    flooded. The two arguments are independent; each defaults to the
    opponent-free, shipped-layout body.
    """
    if turns is None:
        turns = O.SELL_TURNS
    return xp.stack([PJ.projected_inv(xp, mkt_inv, shops, t, day) for t in turns])


def _price_at(xp, price_table, pos):
    """price_table[p, pos[l, p]] for a [3, 9] position array."""
    i32 = xp.int32
    idx = xp.clip(pos - spec.PRICE_TABLE_LO, 0, spec.PRICE_TABLE_N - 1)
    pid = xp.arange(spec.N_PRODUCTS, dtype=i32)[None, :]
    return price_table[pid, idx]


def adjusted_marginals(xp, price_table, inv_lots, lots, press, floor=None):
    """int[3, 9]: what the next unit in each lot is worth, net of timing
    pressure and of the externality on the later lots, given `lots` units
    already allocated."""
    if FLOOR_IMPACT_ON and floor is not False:   # floor False: allocate() proved no unit can reach the floor
        return _adjusted_marginals_floor(xp, price_table, inv_lots, lots, press)
    i32 = xp.int32
    before = xp.cumsum(lots, axis=0, dtype=i32) - lots      # own units in earlier lots
    start = inv_lots + before                               # each lot's first-unit inventory
    nxt = _price_at(xp, price_table, start + lots)          # quote of the next unit
    drop = nxt - _price_at(xp, price_table, start)          # <= 0 per lot
    # externality on later lots: sum of their drops, exclusive of this lot
    later = xp.flip(xp.cumsum(xp.flip(drop, 0), 0, dtype=i32), 0) - drop
    # [LOT4] The lot count is read off the allocation the caller handed in, not
    # off `N_LOTS`: `plan.LOT4_ON` adds a fourth afternoon row and is flipped
    # after import, so a module constant frozen at import would be wrong. With
    # three lots this is `arange(3)` -- the expression it always was.
    lot_ix = xp.arange(lots.shape[0], dtype=i32)[:, None]
    return nxt - press[None, :] * lot_ix + later


def _floor_start(xp, price_table):
    """int[9]: the first market inventory whose quote is the $1 floor (PRICE_TABLE_HI + 1 when none)."""
    import numpy as _np
    hit = _FLOOR_CACHE.get(id(price_table))
    if hit is not None and hit[0] is price_table:
        return hit[1]
    fl = price_table <= spec.PRICE_FLOOR
    first = xp.argmax(fl, axis=1).astype(xp.int32) + spec.PRICE_TABLE_LO
    out = xp.where(xp.any(fl, axis=1), first, spec.PRICE_TABLE_HI + 1).astype(xp.int32)
    if isinstance(price_table, _np.ndarray):
        _FLOOR_CACHE[id(price_table)] = (price_table, out)
    return out


def _floor_reachable(xp, price_table, inv_lots, avail, lots0):
    """numpy only: False when no round of this allocation can price a unit (probe included) at or past the floor
    inventory -- every lot then sells below it and the replay equals the shipped arithmetic; None otherwise."""
    import numpy as _np
    if xp is not _np:
        return None
    most = _np.maximum(avail, _np.sum(lots0, axis=0))
    return None if _np.any(_np.max(inv_lots, axis=0) + most >= _floor_start(xp, price_table)) else False


def _adjusted_marginals_floor(xp, price_table, inv_lots, lots, press):
    """FLOOR_IMPACT_ON body of `adjusted_marginals`: each lot's marginal = replayed day revenue with one more
    unit in that lot minus the replayed revenue of `lots`, minus `press * lot`. The replay walks the lots in
    order: a lot of q units from inventory s pays price[s + j], j < q (the solo walk, exact because every
    quote past the floor inventory F is the floor), then advances the inventory by min(q, max(0, F - s)); the
    town drain between lots is the difference of consecutive `inv_lots` rows."""
    import numpy as _np
    i32 = xp.int32
    n_lots = lots.shape[0]
    F = _floor_start(xp, price_table)
    lot_ix = xp.arange(n_lots, dtype=i32)[:, None]
    if xp is _np:
        before = xp.cumsum(lots, axis=0, dtype=i32) - lots
        if not _np.any(inv_lots + before + lots >= F[None, :]):
            # no priced unit (incl. the probe unit) reaches the floor: the replay IS the shipped arithmetic
            start = inv_lots + before
            nxt = _price_at(xp, price_table, start + lots)
            drop = nxt - _price_at(xp, price_table, start)
            later = xp.flip(xp.cumsum(xp.flip(drop, 0), 0, dtype=i32), 0) - drop
            return nxt - press[None, :] * lot_ix + later
        width = max(PJ.K, int(_np.max(lots)) + 2)
    else:
        width = PJ.K
    eye = (xp.arange(n_lots, dtype=i32)[:, None, None] == xp.arange(n_lots, dtype=i32)[None, :, None]).astype(i32)
    q = xp.concatenate([lots[None].astype(i32), lots[None].astype(i32) + eye], axis=0)   # [1 + L, L, 9]
    j = xp.arange(width, dtype=i32)
    pid = xp.arange(spec.N_PRODUCTS, dtype=i32)[None, :, None]
    cur = xp.broadcast_to(inv_lots[0].astype(i32), q.shape[::2]).astype(i32)            # [1 + L, 9]
    rev = xp.zeros(q.shape[::2], i32)
    for l in range(n_lots):
        if l:
            cur = cur + (inv_lots[l] - inv_lots[l - 1]).astype(i32)[None, :]
        idx = xp.clip(cur[:, :, None] + j[None, None, :] - spec.PRICE_TABLE_LO, 0, spec.PRICE_TABLE_N - 1)
        walk = price_table[pid, idx]                                                   # [1 + L, 9, width]
        ql = q[:, l, :]
        rev = rev + xp.sum(xp.where(j[None, None, :] < ql[:, :, None], walk, 0), axis=2, dtype=i32)
        cur = cur + xp.minimum(ql, xp.maximum(0, F[None, :] - cur))
    return (rev[1:] - rev[0][None, :] - press[None, :] * lot_ix).astype(i32)


def allocate(xp, price_table, mkt_inv, shops, avail, hold, press,
             lots0=None, inv_lots=None, rounds=None, turns=None, day=None):
    """int[3, 9]: units of each product to sell in each lot.

    Each round gives at most one unit per product to its best adjusted lot,
    iff that lot's adjusted marginal clears the reservation value -- or the
    reservation is the liquidation sentinel, which sells regardless. Ties:
    argmax takes the earliest lot.

    `rounds` defaults to `K - 1`, a full shed's worth of units; a caller that
    knows a tighter bound (the forced-overflow continuation, at most
    `SHED_CAPACITY` units) may pass its own. `lots0` continues the greedy from
    an allocation already made, so the continuation charges each further unit
    the curve the earlier ones left. `inv_lots` skips the projection when the
    caller has already built it; `turns` is the lot layout that projection is
    built on when it does not (`lot_inventories`), and `day` is forwarded to
    the same projection -- both do nothing when `inv_lots` is given, and `day`
    does nothing while the opponent switch is off.
    """
    i32 = xp.int32
    if inv_lots is None:
        inv_lots = lot_inventories(xp, mkt_inv, shops, turns, day)
    if rounds is None:
        rounds = PJ.K - 1
    # [LOT4] Off the projection's own row count, for the reason
    # `adjusted_marginals` states; `inv_lots` has one row per lot of `turns`.
    n_lots = int(inv_lots.shape[0])
    lot_ix = xp.arange(n_lots, dtype=i32)[:, None]
    avail = avail.astype(i32)
    hold = hold.astype(i32)
    press = press.astype(i32)
    if lots0 is None:
        lots0 = xp.zeros((n_lots, spec.N_PRODUCTS), i32)
    # `hold <= LIQUIDATE` is the terminal/forced mode, tested on the
    # reservation and not on the value it gates -- see the module docstring.
    liquidate = hold <= LIQUIDATE
    floor = None
    if FLOOR_IMPACT_ON:
        floor = _floor_reachable(xp, price_table, inv_lots, avail, lots0)

    def body(lots):
        adj = adjusted_marginals(xp, price_table, inv_lots, lots, press, floor)
        best = xp.argmax(adj, axis=0)
        best_adj = xp.max(adj, axis=0)
        take = (xp.sum(lots, axis=0, dtype=i32) < avail) & ((best_adj >= hold) | liquidate)
        return lots + ((lot_ix == best[None, :]) & take[None, :]).astype(i32)

    return loop.repeat(xp, rounds, body, lots0.astype(i32))
