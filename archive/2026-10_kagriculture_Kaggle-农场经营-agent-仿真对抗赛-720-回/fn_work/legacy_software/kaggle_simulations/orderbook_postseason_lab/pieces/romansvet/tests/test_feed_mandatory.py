"""`plan.FEED_MANDATORY_ON`: a feed that carries a care is mandatory work.

`mandatory` admits `want_feed & must_feed` -- only an animal already one day
hungry. Every other feed sits in the value tail, and `_routes` cuts each block
at the last tile whose whole chain the budget reaches, so the tail is exactly
where a feed and the care riding on it die together. The census counts 3.0 of
our animals starving mid-season against the opponent's none, and 31 % of our
animal-days banking no care bonus against their 12 %.

ON the tier test becomes `want_feed & (must_feed | care_ok)`, which is
`must_feed` widened by exactly `want_care` (`want_care = want_feed & care_ok`).
So the promoted tile is one the day already decided to feed *and* care: the
wheat is bought and rationed upstream by `want_feed`, and the switch moves
nothing but admission order -- it cannot buy or divert a single wheat.

The exposure is the smallest a tier promotion can have. Promoting development
to this tier measured -23,312 +- 9,198 coins (`dev_weight`'s note), because
the route order carries no value information inside a tier and anything
admitted ahead of a harvest spends the turns that harvest needed. A FEED and a
CARE are one turn each on a tile the block is routed through anyway.

The `test_off_*` half is the identity half, pinned on `test_route_early`'s
digests: OFF, `mand_feed` *is* `must_feed` and the tier expression is the one
it always was.
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
from test_budget_order import _macro
from test_route_early import PIN, PIN_SEEDS, _digest, _plan, _seeded_case

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


#: Both fixtures pin `ROUTE_SPLIT_ON` off (the OFF digests are the pre-split
#: planner's) and the other two switches of the 2026-09-03 stack with it:
#: `SURVIVAL_WATER_ON` re-ranks the same mandatory tier this file is about,
#: and `TAIL_CARE_ON` writes FEEDs and CAREs into the tail the boards below
#: count.
@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "FEED_MANDATORY_ON", False)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)
    monkeypatch.setattr(P, "SURVIVAL_WATER_ON", False)
    monkeypatch.setattr(P, "TAIL_CARE_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "FEED_MANDATORY_ON", True)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)
    monkeypatch.setattr(P, "SURVIVAL_WATER_ON", False)
    monkeypatch.setattr(P, "TAIL_CARE_ON", False)


#: `n_ripe` ripe tomatoes at the head of the serpentine and `n_goose` geese
#: behind them, so the herd is both the low-value work and the far work. The
#: geese are *not* hungry (`t_cons = 0`), so no survival feed is due: their
#: whole claim on a turn is the care the feed banks -- worth `price[EGG] -
#: price[WHEAT]` = 25 against a ripe tomato's 360. That is the tail
#: `_routes` cuts, and the tier is the only thing that can save it.
#:
#: `wheat_price` above the egg quote turns `care_ok` off and leaves a feed
#: with no care on it, which is the case the switch must *not* promote.
def _herd_board(n_goose=4, n_ripe=20, day=12, wheat=10, wheat_price=25,
                money=0, yld=6):
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_yield = z.copy()
    t_day = z.copy()
    kind[:n_ripe], occ[:n_ripe] = spec.KIND_PLANT, spec.I_TOMATO
    t_yield[:n_ripe] = yld
    hi = n_ripe + n_goose
    kind[n_ripe:hi], occ[n_ripe:hi] = spec.KIND_COOP, 0
    t_day[n_ripe:hi] = day - 5
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = wheat
    price = BASE_PRICE.copy()
    price[spec.I_WHEAT] = wheat_price
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=z.copy(), t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(4), price=price,
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32))


def _pair(view, monkeypatch, macro=None):
    """(plan off, plan on) on one board."""
    monkeypatch.setattr(P, "FEED_MANDATORY_ON", False)
    base = _plan(view, macro or _macro())
    monkeypatch.setattr(P, "FEED_MANDATORY_ON", True)
    return base, _plan(view, macro or _macro())


def _count(plan, op):
    return int((np.asarray(plan[0]) == op).sum())


def _buy_row(plan):
    """[(op, arg, qty)] of the live orders on the BUY turn."""
    op, arg, qty = plan[3:6]
    return [(int(op[O.TURN_BUY, s]), int(arg[O.TURN_BUY, s]), int(qty[O.TURN_BUY, s]))
            for s in range(spec.MAX_MARKET_ORDERS)
            if int(op[O.TURN_BUY, s]) != O.MO_NONE]


# =========================================================================
# OFF: byte-identical to the planner the switch was cut into
# =========================================================================

def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte. Pinned on
    `test_route_early`'s digests, taken off the tree at `a838700`."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_cuts_the_care_bearing_feed_off_the_value_tail(off):
    """The behaviour the switch exists to change. The day wants the feeds --
    they clear 1.4's value test and the shed has the wheat -- but they price at
    25 coins against a ripe tomato's 360, so `_routes` cuts every one of them
    off the end of the block and the herd goes unfed and uncared."""
    plan = _plan(_herd_board(), _macro())
    assert _count(plan, O.OP_HARVEST) > 0, "the board harvested nothing"
    assert _count(plan, O.OP_FEED) == 0, "the tail was not tight enough"
    assert _count(plan, O.OP_CARE) == 0


def test_on_keeps_the_care_bearing_feed_on_the_same_tight_budget(on, monkeypatch):
    """Same board, same purse, same crew. The feeds are now in the mandatory
    tier, so admission takes them ahead of the tomatoes and every one of them
    reaches the route -- each with the CARE it exists to buy."""
    view = _herd_board()
    base, got = _pair(view, monkeypatch)
    assert _count(base, O.OP_FEED) == 0
    assert _count(got, O.OP_FEED) == 4, _count(got, O.OP_FEED)
    assert _count(got, O.OP_CARE) == 4, _count(got, O.OP_CARE)
    # The turns come out of the harvests, which is the trade the switch makes.
    assert _count(got, O.OP_HARVEST) < _count(base, O.OP_HARVEST)


def test_on_does_not_promote_a_feed_with_no_care_on_it(on, monkeypatch):
    """The tier widens by `want_care` and by nothing else. With the wheat quote
    above the egg quote `care_ok` is false, the feeds carry no care, and the
    day is the one OFF plans -- byte for byte."""
    view = _herd_board(wheat_price=60)
    base, got = _pair(view, monkeypatch)
    assert _count(got, O.OP_CARE) == 0
    for k in range(6):
        assert np.array_equal(np.asarray(base[k]), np.asarray(got[k])), k


def test_on_buys_and_diverts_no_wheat(on, monkeypatch):
    """`want_feed` is `feed_pass & (feed_rank < wheat_avail)` and is settled
    before the tier is read, so the promotion cannot buy a wheat, ration one
    away from a hungrier animal, or displace a seed, an animal or the land row.
    The BUY row is order for order OFF's on the herd board, on a board that
    has to buy its wheat, and on twelve seeded boards."""
    for view in (_herd_board(), _herd_board(wheat=0, money=8_000),
                 _herd_board(n_goose=8, n_ripe=26, wheat=3, money=3_000)):
        base, got = _pair(view, monkeypatch)
        assert _buy_row(base) == _buy_row(got), _buy_row(got)
    for s in PIN_SEEDS:
        view, macro = _seeded_case(s)
        base, got = _pair(view, monkeypatch, macro)
        assert _buy_row(base) == _buy_row(got), s


#: `plan.EARLY_SELL_ON` went on by default on 2026-09-03: the day's first lot
#: rides turn 1 behind the BUY row instead of standing on `O.SELL_TURNS[0]`.
#: It is pinned off for this file the way `a838700`'s stack was pinned off for
#: the digest fixtures -- the pins and worked examples below are the plan
#: *before* it, and what this file is about (the mandatory feed) is a question the switch does
#: not answer either way. `tests/test_early_sell.py` owns both halves of it.
@pytest.fixture(autouse=True)
def _early_sell_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", False)


#: `plan.TAIL_FILL_ON` and `plan.BANK_BEFORE_LOT_ON` went on by default on
#: 2026-09-09 (the tail pair, `docs/strategy/2026-09-10-ship-pair.md`). The
#: OFF digests in this file were taken before the pair existed and still mean
#: what they meant -- "OFF, this file's switch leaves the planner it was cut
#: into alone" -- so the pair is pinned off here the way `EARLY_SELL_ON` and
#: `OPEN_PUMP_ON` were pinned off before it (`854b86b`).
#: `tests/test_tail_fill.py` and `tests/test_bank_before_lot.py` own the two.
@pytest.fixture(autouse=True)
def _tail_pair_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "TAIL_FILL_ON", False)
    monkeypatch.setattr(P, "BANK_BEFORE_LOT_ON", False)
