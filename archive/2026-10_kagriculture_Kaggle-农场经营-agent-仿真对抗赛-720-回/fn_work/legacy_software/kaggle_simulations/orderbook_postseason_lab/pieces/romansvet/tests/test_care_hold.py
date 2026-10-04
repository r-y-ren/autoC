"""`plan.CARE_HOLD_ON`: price CARE off the forward quote, not today's spot.

`care_pays` is `price[product] > price[WHEAT]` at hour 0. Over days 16-29 milk
falls 96 -> 33 while wheat climbs to 44, and the census's 43.1 fed-but-uncared
animal-days a game start at day 15 and peak on day 26 -- the same crossover.
But a care taken today banks a unit that fires at `h_next` and reaches the
market days later, once the town has drained the glut that crashed the quote;
the gate refuses the trade on a price the unit is never sold at.

ON the product side of that comparison becomes `max(spot, sales-window)`,
where the sales-window quote is `_candidates`' own `inv_h` -- the hour-0
inventory drained by the town to the product's first fire plus everything our
board has already committed to that market. So it is a realised-market read
and not `spec.PRICE_BASE`: our own glut is priced into it, and the `max` keeps
the switch monotone -- ON only ever loosens the gate.

The forward quote moves the gate and nothing else. The wheat side, `care_val`
(the term `feed_value` carries into the *purchase* test) and `v_care` (the
op's admitted labour value) all stay at spot: the first two keep the switch
off the BUY row, and the third keeps a care priced at a forward 267 against a
spot 33 from outbidding the ripe tomato beside it for today's turn. What ON
adds is the free half of the census -- a one-turn CARE on an animal the day is
already feeding.

The `test_off_*` half is the identity half, pinned on `test_route_early`'s
digests: OFF, `care_price` is `view.price[an_prod]` and `care_pays`,
`care_val` and `v_care` are the three expressions they always were.
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


#: Both fixtures pin `ROUTE_SPLIT_ON` off, as `test_tail_care` does: the OFF
#: digests below are the pre-split planner's. The three switches promoted on
#: 2026-09-03 go with it. `TAIL_CARE_ON` is the load-bearing one: it spends
#: the idle tail on the very FEED and CARE these boards count, so with it on
#: every board here cares its goose whatever `care_pays` decided, and this
#: file is about `care_pays`. `FEED_MANDATORY_ON` promotes the same tile into
#: the mandatory tier and `SURVIVAL_WATER_ON` re-ranks that tier.
@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "CARE_HOLD_ON", False)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)
    monkeypatch.setattr(P, "SURVIVAL_WATER_ON", False)
    monkeypatch.setattr(P, "TAIL_CARE_ON", False)
    monkeypatch.setattr(P, "FEED_MANDATORY_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "CARE_HOLD_ON", True)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)
    monkeypatch.setattr(P, "SURVIVAL_WATER_ON", False)
    monkeypatch.setattr(P, "TAIL_CARE_ON", False)
    monkeypatch.setattr(P, "FEED_MANDATORY_ON", False)


#: The census board in miniature: `n_goose` geese the day feeds anyway (they
#: are one night from escaping, so `must_feed` holds whatever the care does),
#: with the egg quote *under* the wheat quote so `care_pays` fails on spot.
#: The market itself is untouched at `MARKET_I0`, where the table pays 50 an
#: egg -- so the forward quote clears a `wheat_price` of 40 and fails one of
#: 400, which is the two-sided bracket the tests below read.
def _hold_board(n_goose=2, n_ripe=0, day=25, wheat=10, egg=10, wheat_price=40,
                t_bank=0, money=0, yld=6, age=5):
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_cons = z.copy()
    t_yield = z.copy()
    t_day = z.copy()
    bank = z.copy()
    kind[:n_goose], occ[:n_goose] = spec.KIND_COOP, 0
    t_cons[:n_goose] = 1
    t_day[:n_goose] = day - age
    bank[:n_goose] = t_bank
    hi = n_goose + n_ripe
    kind[n_goose:hi], occ[n_goose:hi] = spec.KIND_PLANT, spec.I_TOMATO
    t_yield[n_goose:hi] = yld
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = wheat
    price = BASE_PRICE.copy()
    price[spec.I_EGG] = egg
    price[spec.I_WHEAT] = wheat_price
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=t_cons, t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(1), price=price,
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32), t_bank=bank)


def _ops(view, macro=None):
    """The multiset of unit ops the day plans, as a set of op codes."""
    return set(int(x) for x in np.asarray(_plan(view, macro or _macro())[0]).ravel())


def _pair(view, monkeypatch, macro=None):
    """(plan off, plan on) on one board."""
    monkeypatch.setattr(P, "CARE_HOLD_ON", False)
    base = _plan(view, macro or _macro())
    monkeypatch.setattr(P, "CARE_HOLD_ON", True)
    return base, _plan(view, macro or _macro())


# =========================================================================
# OFF: byte-identical to the planner the switch was cut into
# =========================================================================

def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte. Pinned on
    `test_route_early`'s digests, taken off the tree at `a838700`."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_feeds_the_animal_and_refuses_the_care_the_spot_quote_prices(off):
    """The behaviour the switch exists to change. The day feeds the geese --
    they are a night from escaping -- and then declines the free one-turn CARE
    the feed exists to buy, because today's egg quote is under today's wheat
    quote. That is the census's 43.1 fed-but-uncared animal-days."""
    view = _hold_board(n_goose=3)
    assert int(view.price[spec.I_EGG]) < int(view.price[spec.I_WHEAT])
    ops = _ops(view)
    assert O.OP_FEED in ops, "the board's own feed did not plan"
    assert O.OP_CARE not in ops, "spot pricing planned a care"


# =========================================================================
# ON: the forward quote pays for the care, and buys no wheat for it
# =========================================================================

def test_on_cares_the_animal_whose_forward_quote_clears_the_wheat(on, monkeypatch):
    """Same board. The market is at `MARKET_I0`, where the table pays 50 an
    egg once the town has drained to the goose's first fire, against a wheat
    quote of 40 -- so the unit the care banks does clear its wheat, and the
    CARE the spot quote refused is planned on the tile the day already feeds."""
    view = _hold_board(n_goose=3)
    base, got = _pair(view, monkeypatch)
    b, g = np.asarray(base[0]), np.asarray(got[0])
    assert O.OP_CARE not in [int(x) for x in b.ravel()]
    cares = np.argwhere(g == O.OP_CARE)
    assert len(cares) == 3, cares
    # Every CARE rides a FEED of the same unit: a care on an unfed animal
    # banks nothing (`kaggriculture.py:829`).
    for u, _ in cares:
        assert O.OP_FEED in [int(x) for x in g[u]], u
    # And the care is admitted at the *spot* net, not the forward one: on the
    # same board with ripe tomatoes and the turns to reach them, ON harvests
    # every one OFF did. A care priced at the forward quote would have outbid
    # them for the block's order, which is the `dev_weight` failure mode.
    slack = _hold_board(n_goose=3, n_ripe=6, money=20_000)
    base, got = _pair(slack, monkeypatch)
    assert (np.asarray(got[0]) == O.OP_CARE).sum() == 3
    assert ((np.asarray(got[0]) == O.OP_HARVEST).sum()
            == (np.asarray(base[0]) == O.OP_HARVEST).sum())


def test_on_still_refuses_a_care_the_forward_quote_cannot_pay(on, monkeypatch):
    """The gate is loosened, not removed. At a wheat quote of 400 the forward
    egg quote fails too, so ON plans the same day OFF does -- byte for byte."""
    view = _hold_board(n_goose=3, wheat_price=400)
    base, got = _pair(view, monkeypatch)
    for k in range(6):
        assert np.array_equal(np.asarray(base[k]), np.asarray(got[k])), k
    assert O.OP_CARE not in [int(x) for x in np.asarray(got[0]).ravel()]


def test_on_keeps_the_headroom_gate(on, monkeypatch):
    """`care_headroom` is untouched. A goose two days short of its first fire
    -- so tonight consumes nothing and `bank_carry` is the standing bank --
    with 3 already banked has nowhere to put a fourth (`max_held` is 4, and
    `bank_carry + 2 <= 4` fails at 3). The day still feeds it and neither
    setting cares it, byte for byte."""
    view = _hold_board(n_goose=3, age=2, t_bank=3)
    base, got = _pair(view, monkeypatch)
    ops = [int(x) for x in np.asarray(got[0]).ravel()]
    assert O.OP_FEED in ops, "the board's own feed did not plan"
    assert O.OP_CARE not in ops
    for k in range(6):
        assert np.array_equal(np.asarray(base[k]), np.asarray(got[k])), k


def _buy_row(plan):
    """[(op, arg, qty)] of the live orders on the BUY turn."""
    op, arg, qty = plan[3:6]
    return [(int(op[O.TURN_BUY, s]), int(arg[O.TURN_BUY, s]), int(qty[O.TURN_BUY, s]))
            for s in range(spec.MAX_MARKET_ORDERS)
            if int(op[O.TURN_BUY, s]) != O.MO_NONE]


def test_on_buys_no_wheat_the_day_plan_cannot_afford(on, monkeypatch):
    """The switch must not reach the BUY row. `care_val` -- the term
    `feed_value` carries into the purchase test -- stays at the spot quote, so
    a care-only feed still has to clear the wheat's own marginal quote at
    today's price, and a care the forward quote newly pays for rides a feed the
    day was buying anyway. On three census boards with an empty or short shed
    and a purse to buy with, and on twelve seeded boards, the BUY row is order
    for order the one OFF emitted -- same wheat, same seed, same animals, same
    land.

    What does move is the HIRE row: the cares raise the day's admitted value,
    and the enumeration answers by taking one more hand where the bill pays.
    That is the enumeration doing its job on a bigger task list, not a
    purchase the care smuggled past it."""
    boards = [_hold_board(n_goose=g, wheat=w, money=m, n_ripe=r)
              for g, w, m, r in ((3, 0, 6_000, 0), (6, 2, 20_000, 8),
                                 (3, 0, 900, 4))]
    for view in boards:
        base, got = _pair(view, monkeypatch)
        assert _buy_row(base) == _buy_row(got), _buy_row(got)
        assert (np.asarray(got[0]) == O.OP_CARE).any(), "the board planned no care"
    for s in PIN_SEEDS:
        view, macro = _seeded_case(s)
        base, got = _pair(view, monkeypatch, macro)
        assert _buy_row(base) == _buy_row(got), s


#: `plan.EARLY_SELL_ON` went on by default on 2026-09-03: the day's first lot
#: rides turn 1 behind the BUY row instead of standing on `O.SELL_TURNS[0]`.
#: It is pinned off for this file the way `a838700`'s stack was pinned off for
#: the digest fixtures -- the pins and worked examples below are the plan
#: *before* it, and what this file is about (the care reserve) is a question the switch does
#: not answer either way. `tests/test_early_sell.py` owns both halves of it.
@pytest.fixture(autouse=True)
def _early_sell_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", False)


#: `plan.TAIL_FILL_ON` and `plan.BANK_BEFORE_LOT_ON` both went on by default on
#: 2026-09-09 (the tail pair, `docs/strategy/2026-09-10-ship-pair.md`). The
#: OFF digests above were taken before the pair existed, so they are pinned off
#: here the way `EARLY_SELL_ON` is; `tests/test_tail_fill.py` and
#: `tests/test_bank_before_lot.py` own the two switches.
@pytest.fixture(autouse=True)
def _tail_pair_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "TAIL_FILL_ON", False)
    monkeypatch.setattr(P, "BANK_BEFORE_LOT_ON", False)


#: Three more switches went on by default AFTER the `a838700` digests above
#: were taken, and all three move the market rows the pin hashes: `HIRE_ROW_ON`
#: (`b1bde4f`), `LOT4_ON` with `LOT4_TURN = 17`
#: (`docs/strategy/2026-09-16-lot4.md`, POOLED180 +791 t 13.19, sub 56276165)
#: and `SELL_SLOT_PRIORITY_ON` (`docs/strategy/2026-09-16-slotprio.md`, +459
#: t 7.31 on the lot-4 combo, sub 56277270). They are pinned off here exactly
#: as `EARLY_SELL_ON` and the tail pair above are: with the three stated off,
#: this tree reproduces the `a838700` digests byte for byte (measured,
#: TESTFIX3 2026-09-17), so the pin keeps its meaning -- "OFF, this file's
#: switch leaves the planner it was cut into alone" -- instead of silently
#: becoming a hash of three later ships. `tests/test_lot4.py` and
#: `tests/test_slotprio.py` own those.
@pytest.fixture(autouse=True)
def _later_market_ships_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "HIRE_ROW_ON", False)
    monkeypatch.setattr(P, "LOT4_ON", False)
    monkeypatch.setattr(P, "SELL_SLOT_PRIORITY_ON", False)
