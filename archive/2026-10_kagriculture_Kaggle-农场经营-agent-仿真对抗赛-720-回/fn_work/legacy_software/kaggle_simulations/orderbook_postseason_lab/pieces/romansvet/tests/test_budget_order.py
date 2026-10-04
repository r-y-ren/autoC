"""The purse goes to marginal purchase candidates by value per coin.

`build_day` prices one wheat per passing feed, one fertilizer per application,
the k-th seed of each crop and the k-th animal, each in coins against its
engine-curve cost, and grants them best ratio first down the purse
(PLANNER_V3_1 section 1.3). Land is the exception only in being lumpy:
one quadrant is not a marginal unit of anything, so it is priced separately by
`budget.marginal_gain` -- the coins the candidates behind the wall would earn
-- and compared two ways ahead of the greedy, with the learned gene reduced to
a signed coin bias on that comparison (`test_land_value.py`).

The market row keeps a *fixed* slot layout regardless, which these tests also
pin: the budget never grants more than the money on hand, so the engine can
honour the row in any sequence -- while a row permuted per policy would hand
the two seats different layouts and break the standing assumption in
`sim/market.py`.
"""
from __future__ import annotations

import os
import sys

import _pin

# `kagg3` FIRST, out of the tree this process is meant to measure: the
# shared fixtures below do their own `sys.path.insert(0, "src")` and import
# `kagg3` on the way in, so a module that imported one of them first loaded
# THIS tree into a `--digests` subprocess and pinned the tree against itself
# (`tests/_pin.py`).
_pin.bootstrap()

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import projector as PJ


def _view(money, nquad=1):
    """A blank board: every tile free, nothing planted, nothing in the shed."""
    z = np.zeros(100, np.int32)
    return P.DayView(
        day=np.int32(0),
        kind=np.full(100, spec.KIND_EMPTY, np.int32), occ=z - 1,
        t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(), t_yield=z.copy(),
        t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(nquad),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


def one_kind(kind, n):
    """`animal_want` asking for `n` of one animal and none of the others.

    What `animal_count=n` meant before a day could buy more than one kind: the
    fixtures that only ever wanted geese say so explicitly now."""
    want = np.zeros(spec.N_ANIMALS, np.int32)
    want[kind] = n
    return want


def geese(n):
    return one_kind(spec.I_GOOSE - spec.I_GOOSE, n)     # animal index 0


def _macro(**kw):
    base = {
        "plant_target": np.zeros(spec.N_CROPS, np.int32),
        "animal_want": np.zeros(spec.N_ANIMALS, np.int32),
        "land_bias": np.int32(0),
        "hold": np.full(spec.N_PRODUCTS, 10_000, np.int32),  # hold everything unless a test lowers it
        "press": np.zeros(spec.N_PRODUCTS, np.int32),
        "grow_mult": np.full(spec.N_PRODUCTS, brain.GROW_ONE, np.int32),
        "compact": np.int32(0),                             # the plain sweep rank
        "dev_weight": np.int32(brain.GROW_ONE),             # x1
        "hire_bias": np.int32(0),                           # the enumeration alone
        "crew_target": np.int32(0),                         # no crew ramp
        "animal_defer": np.int32(0),                        # nothing waits for it
        "forward_days": np.int32(0),                        # the scan reads today alone
    }
    # [g12] Appended after the pins in `tests/test_fertengine.py` were cut, and
    # those run this helper against a pristine PRE-`g12` `src` tree in a
    # subprocess -- so the field is named only when the planner has it.
    if "fert_defer" in P.Macro._fields:
        base["fert_defer"] = np.int32(0)
    base.update(kw)
    return P.Macro(**base)


def _buy_qty(view, macro, mo_op):
    """Quantity the day's plan commits to one market op, over the whole block.

    Not `O.TURN_BUY` alone: since M2 the day's BUY_LAND rides the spare slot of
    `O.SELL_TURNS[0]`, and a helper that read one row would score it at zero and
    pass by under-counting."""
    op, _, qty = P.build_day(np, view, macro)[3:6]
    return int(qty[op == mo_op].sum())


def _overhead(view, macro):
    """Coins `build_day` takes off `view.money` before the buy side sees any.

    Two terms, both functions of the hire count the day's own enumeration
    picks [1.5]: the crew's fib bill, and the cash reserve kept back for
    tomorrow's crew (`plan.cash_reserve`). Read back off a probe build rather
    than assumed, because the count is the planner's decision and not the
    fixture's.

    The probe states `HIRE_ROW_ON` off (shipped on at `b1bde4f`). That switch
    trims the emitted HIRE row to the hands `_routes` actually loaded, but the
    budget above it still spends and reserves against the *enumerated*
    `n_hire` -- so the trimmed row is no longer the count this measurement is
    after, and reading it made the stated purse 2 coins short on a board with
    one idle hand (TESTFIX3 2026-09-17; it cost
    `test_grow_multiplier_tilts_the_seed_mix` its sixth wheat seed). The trim
    itself is untouched in every plan the tests below assert on;
    `tests/test_hire_row.py` owns it.
    """
    trim = P.HIRE_ROW_ON
    P.HIRE_ROW_ON = False
    try:
        op = P.build_day(np, view, macro)[3]
    finally:
        P.HIRE_ROW_ON = trim
    n = int((op == O.MO_HIRE).sum())
    return int(spec.HIRE_COST[:n].sum()) + int(P.cash_reserve(np, np.int32(n), view.day))


def _purse_view(purse, macro, nquad=1, shape=lambda v: v):
    """A view whose **buy-side purse** is `purse`, not whose `money` is.

    Every arithmetic assertion in this file is about what the greedy does with
    a given number of coins, so the fixture states that number and this adds
    the day's overhead on top. `shape` applies the board the test wants before
    the overhead is measured, since the hire count depends on it.

    Iterated, because raising the money can raise the hire count and so the
    overhead; it settles on the first or second step for every board here, and
    the loop asserts that rather than trusting it.
    """
    view = shape(_view(purse, nquad))
    for _ in range(4):
        over = _overhead(view, macro)
        nxt = shape(_view(purse + over, nquad))
        if _overhead(nxt, macro) == over:
            return nxt
        view = nxt
    raise AssertionError("the day's hire overhead does not settle at this purse")


# One goose (300) and one quadrant (1000) together cost 1300; 1000 buys exactly
# one of them, so land's two-way comparison is the only thing that decides which.
#
# `_view` is a hundred EMPTY tiles, so nothing on this board is LOCKED and a
# purchase would unlock no tile at all: its computed value is exactly zero, and
# the gene's coin bias is therefore the whole of the comparison here. That is
# the point -- land no longer wins on affordability alone.
PURSE = int(spec.LAND_PRICES[0])


def test_a_quadrant_the_gene_insists_on_is_granted_ahead_of_the_greedy():
    macro = _macro(land_bias=np.int32(PURSE), animal_want=geese(1))
    view = _purse_view(PURSE, macro)
    assert _buy_qty(view, macro, O.MO_BUY_LAND) == 1
    assert _buy_qty(view, macro, O.MO_BUY_ANIMAL) == 0


def test_a_quadrant_worth_nothing_is_refused_at_zero_bias():
    """The central pin of the new design, and the inverse of the old one: with
    no tiles behind the wall the quadrant earns nothing, so a policy that has
    learned nothing hands the purse to the goose instead."""
    macro = _macro(land_bias=np.int32(0), animal_want=geese(1))
    view = _purse_view(PURSE, macro)
    assert _buy_qty(view, macro, O.MO_BUY_LAND) == 0
    assert _buy_qty(view, macro, O.MO_BUY_ANIMAL) == 1


def test_without_the_request_the_purse_goes_to_the_greedy():
    macro = _macro(land_bias=np.int32(-PURSE), animal_want=geese(1))
    view = _purse_view(PURSE, macro)
    assert _buy_qty(view, macro, O.MO_BUY_LAND) == 0
    assert _buy_qty(view, macro, O.MO_BUY_ANIMAL) == 1


def test_value_per_coin_decides_between_seeds_and_an_animal():
    # 300 coins on a blank day-0 board: a melon seed's six units sell at
    # I0 - 10 for 1,611 coins (ratio 20.1 per 80-coin seed) and beat one goose
    # -- 25 eggs from I0 - 4 (1,172) plus 28 fertilizers from I0 (2,725) less
    # 14 feed wheat at 25 (350), so 3,547 per 300, ratio 11.8. Three melons
    # take 240 of the 300 and the fourth no longer fits.
    macro = _macro(animal_want=geese(1), plant_target=np.array([0, 0, 0, 0, 30], np.int32))
    view = _purse_view(300, macro)
    assert _buy_qty(view, macro, O.MO_BUY_SEED) == 3
    assert _buy_qty(view, macro, O.MO_BUY_ANIMAL) == 0
    # floor the melon market and the goose wins
    inv = view.mkt_inv.copy()
    inv[spec.I_MELON] = spec.MARKET_I0 + 40_000
    assert _buy_qty(view._replace(mkt_inv=inv), macro, O.MO_BUY_ANIMAL) == 1


def test_grow_multiplier_tilts_the_seed_mix():
    # A 60-coin purse: six wheat seeds at 10, or three carrots at 20. The hand
    # the day hires to plant the wheat, and the coins it keeps back for
    # tomorrow's crew, sit on top of that and `_purse_view` supplies them.
    macro = _macro(plant_target=np.array([30, 30, 0, 0, 0], np.int32))
    view = _purse_view(60, macro)
    op, arg, qty = P.build_day(np, view, macro)[3:6]
    seeds = {int(arg[O.TURN_BUY, s]): int(qty[O.TURN_BUY, s]) for s in range(spec.MAX_MARKET_ORDERS)
             if int(op[O.TURN_BUY, s]) == O.MO_BUY_SEED}
    assert seeds.get(spec.I_WHEAT, 0) == 6 and seeds.get(spec.I_CARROT, 0) == 0
    grow = np.full(spec.N_PRODUCTS, brain.GROW_ONE, np.int32)
    grow[spec.I_CARROT] = 1024
    op, arg, qty = P.build_day(np, view, macro._replace(grow_mult=grow))[3:6]
    seeds = {int(arg[O.TURN_BUY, s]): int(qty[O.TURN_BUY, s]) for s in range(spec.MAX_MARKET_ORDERS)
             if int(op[O.TURN_BUY, s]) == O.MO_BUY_SEED}
    assert seeds.get(spec.I_CARROT, 0) == 3 and seeds.get(spec.I_WHEAT, 0) == 0


def test_the_buy_row_layout_is_fixed_whatever_is_bought():
    view = _view(3000)
    macro = _macro(land_bias=np.int32(PURSE), animal_want=geese(2),
                   plant_target=np.array([3, 2, 0, 0, 0], np.int32))
    plan = P.build_day(np, view, macro)
    op = plan[3][O.TURN_BUY]
    live = [int(o) for o in op if int(o) != O.MO_NONE]
    assert live == [O.MO_BUY_SEED, O.MO_BUY_SEED, O.MO_BUY_ANIMAL]
    # ... and land has left this row for the spare slot of the first SELL turn
    assert int(plan[3][O.SELL_TURNS[0], spec.MAX_MARKET_ORDERS - 1]) == O.MO_BUY_LAND


def test_shed_room_caps_the_grant_without_stranding_the_coins():
    """Shed room is a [LAW] cap, and it must be applied to the *wants*.

    The market clips BUY_PRODUCT and BUY_ANIMAL to `SHED_CAPACITY - sum(shed)`
    slot by slot, so a shed with two units of room takes two units whatever
    the plan asks for. The old category walk deducted only what it actually
    bought, so room it refused stayed in the purse for the next category --
    and a greedy that budgets against unclipped wants and clips afterwards
    loses that money instead: here it would hand 1,500 coins to five geese
    the shed cannot hold and leave the seeds with the change.

    Ten hungry geese and a shed 98 full: room 2, and the egg multiplier puts
    the goose (ratio ~27) ahead of the wheat feed (~12) and the wheat seed
    (~10.1), so the animal list is served first and is exactly the list the
    room refuses.
    """
    view = _view(1600)
    kind, occ, t_cons = view.kind.copy(), view.occ.copy(), view.t_cons.copy()
    kind[:10], occ[:10], t_cons[:10] = spec.KIND_COOP, 0, 1      # ten geese, unfed yesterday
    shed = view.shed.copy()
    shed[spec.I_MELON] = spec.SHED_CAPACITY - 2                  # room for two units
    view = view._replace(kind=kind, occ=occ, t_cons=t_cons, shed=shed)
    grow = np.full(spec.N_PRODUCTS, brain.GROW_ONE, np.int32)
    grow[spec.I_EGG] = 1024
    macro = _macro(animal_want=geese(5), grow_mult=grow,
                   plant_target=np.array([20, 0, 0, 0, 0], np.int32))

    op, arg, qty = P.build_day(np, view, macro)[3:6]
    row = O.TURN_BUY
    shed_bound = sum(int(qty[row, s]) for s in range(spec.MAX_MARKET_ORDERS)
                     if int(op[row, s]) in (O.MO_BUY_PRODUCT, O.MO_BUY_ANIMAL))
    seeds = sum(int(qty[row, s]) for s in range(spec.MAX_MARKET_ORDERS)
                if int(op[row, s]) == O.MO_BUY_SEED)

    assert shed_bound <= 2                    # the law
    assert seeds == 20                        # ... and the coins it refused still bought seeds

    # nothing over-commits: price the row the way the engine walks it
    inv = PJ.projected_inv(np, view.mkt_inv, view.shops, row)
    quotes = PJ.buy_quotes(np, P.default_price_table(), inv)
    spent = 0
    for s in range(spec.MAX_MARKET_ORDERS):
        o, a, q = int(op[row, s]), int(arg[row, s]), int(qty[row, s])
        if q == 0:
            continue
        if o == O.MO_BUY_PRODUCT:
            spent += int(quotes[a, :q].sum())
        elif o == O.MO_BUY_SEED:
            spent += q * int(spec.CROP_SEED_COST[a])
        elif o == O.MO_BUY_ANIMAL:
            spent += q * int(spec.ANIMAL_COST[a])
        elif o == O.MO_BUY_LAND:
            spent += int(spec.LAND_PRICES[int(view.nquad) - 1])
    assert spent <= 1600


def test_three_way_shed_contention_does_not_strand_the_purse():
    """All three shed-bound lists wanting the room at once.

    Feed wheat, fertilizer applications and a new animal all land in the shed
    and share one room. Bounding each want by the whole room and clipping the
    answer afterwards lets the greedy fund three times the room in units and
    binds the coins of the two thirds the clamp then discards: measured on
    this board, 607 of a 700-coin purse went unspent and four wheat seeds were
    bought where sixteen more were affordable. The room belongs inside the
    greedy.

    Day 10, ten hungry geese (wheat want 10), three tomatoes due for
    fertilizer (want 3), five animals wanted, a shed 98 full -- room 2, and
    every one of the three wants exceeds it. The purse the walk sees is 700;
    the hands 1.5 hires for the feeds and the coins it keeps for tomorrow's
    crew sit on top of it (`_purse_view`).
    """
    def _shape(v):
        v = v._replace(day=np.int32(10))
        kind, occ, t_cons, t_day = (v.kind.copy(), v.occ.copy(),
                                    v.t_cons.copy(), v.t_day.copy())
        kind[:10], occ[:10], t_cons[:10] = spec.KIND_COOP, 0, 1
        kind[10:13], occ[10:13], t_day[10:13] = spec.KIND_PLANT, spec.I_TOMATO, 2
        shed = v.shed.copy()
        shed[spec.I_MELON] = spec.SHED_CAPACITY - 2
        return v._replace(kind=kind, occ=occ, t_cons=t_cons, t_day=t_day, shed=shed)

    grow = np.full(spec.N_PRODUCTS, brain.GROW_ONE, np.int32)
    grow[spec.I_EGG] = 1024                      # the goose outranks the seed
    macro = _macro(animal_want=geese(5), grow_mult=grow,
                   plant_target=np.array([60, 0, 0, 0, 0], np.int32))
    view = _purse_view(700, macro, shape=_shape)

    op, arg, qty = P.build_day(np, view, macro)[3:6]
    row = O.TURN_BUY
    inv = PJ.projected_inv(np, view.mkt_inv, view.shops, row)
    quotes = PJ.buy_quotes(np, P.default_price_table(), inv)
    spent = shed_bound = seeds = 0
    for s in range(spec.MAX_MARKET_ORDERS):
        o, a, q = int(op[row, s]), int(arg[row, s]), int(qty[row, s])
        if q == 0:
            continue
        if o == O.MO_BUY_PRODUCT:
            spent += int(quotes[a, :q].sum())
            shed_bound += q
        elif o == O.MO_BUY_SEED:
            spent += q * int(spec.CROP_SEED_COST[a])
            seeds += q
        elif o == O.MO_BUY_ANIMAL:
            spent += q * int(spec.ANIMAL_COST[a])
            shed_bound += q
        elif o == O.MO_BUY_LAND:
            spent += int(spec.LAND_PRICES[int(view.nquad) - 1])

    assert shed_bound <= 2                       # the law
    assert spent <= 700                          # never over-commits
    # two geese (600) and ten wheat seeds (100): the whole purse, none of it
    # reserved for units the shed would have refused
    assert seeds == 10 and spent == 700


def test_macro_has_no_order():
    assert "order" not in P.Macro._fields


#: `plan.OPEN_PUMP_ON` went on by default on 2026-09-04: on day 0 the plan buys
#: `OPEN_PUMP_UNITS` wheat behind the hire row and sells it back from the BUY
#: row's head slot, to quote the class-A opening's own wheat off a drained pot.
#: It is pinned off for this file the way `0772ed3` pinned `EARLY_SELL_ON` off
#: for the modules it moved under: the fixed BUY-row layout it pins was taken
#: before the pump put a SELL in `B_WHEAT`'s empty slot on day 0, and the
#: question it asks -- that the layout does not shift with what is bought -- is
#: the same either way.
#: `tests/test_open_pump.py` owns both halves of the switch.
@pytest.fixture(autouse=True)
def _open_pump_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "OPEN_PUMP_ON", False)
