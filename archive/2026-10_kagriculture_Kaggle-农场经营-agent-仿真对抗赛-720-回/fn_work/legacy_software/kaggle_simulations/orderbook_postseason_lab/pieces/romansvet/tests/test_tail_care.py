"""`plan.TAIL_CARE_ON`: spend the tail on FEED and then CARE.

The engine pays the pair and neither half alone
(`_daily_refresh_animals`, `kaggriculture.py:810-833`): production fires
whether or not the animal ate, so a feed buys survival and not units; the care
bonus is banked only `if cared_today and fed_today`, and an unfed production
night wipes whatever was banked. Over 16 real-engine replays the joint
counterfactual is +8,375 coins a game against +1,116 for feeding alone and
+1,974 for caring alone.

The tail is where both are affordable. `want_care = want_feed & care_ok` drops
the care whenever today's *spot* quote fails `care_pays`, which leaves 43.1
animal-days a game fed-but-uncared -- a free one-turn CARE the day already
paid the feed for -- while 595.9 unit-turns PASS in the last six hours and
354.8 wheat units ride in unit inventories to hour 23.

So the hop does two things the filler may not: it takes up to two turns on one
tile, and it revisits a tile a block already ran, which is exactly where the
fed-but-uncared animal is. It may not take a lone CARE on an animal nothing
feeds, and it may not take a FEED the unit has no wheat for.

The `test_off_*` half is the identity half, pinned on `test_route_early`'s
digests: OFF, `tail_care` is `None`, `_routes` compiles none of the hop and
every tail turn is the `O.OP_PASS` it was.
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
from test_route_early import (PIN, PIN_SEEDS, _digest, _plan, _seeded_case,
                              _view)

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

MOVES = (O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST)
#: What a cared turn may ever hold: the walk there, and the two day-flag ops.
CARE_OPS = MOVES + (O.OP_FEED, O.OP_CARE)

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


#: Both fixtures pin `ROUTE_SPLIT_ON` off, as `test_tail_fill` does: the OFF
#: digests below are the pre-split planner's, and the boards are arithmetic on
#: a farmer that starts at `ROUTE_BASE`.
#: `test_on_leaves_every_turn_the_route_owns_alone` runs the hop's one
#: invariant against the shipped default instead.
@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "TAIL_CARE_ON", False)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "TAIL_CARE_ON", True)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)


#: `n_goose` geese at the head of the serpentine, then `n_crop` ripe plants,
#: and a wheat quote *above* the egg quote so `care_pays` fails and the day
#: plans no CARE at all -- which is the whole of the census case. Each crop
#: stop is two turns (a step and a HARVEST), so `n_crop` is the dial that sets
#: how long a tail the block leaves.
#:
#: `crop=I_WHEAT` is the carrying board: a HARVEST on a wheat plant puts its
#: `yield_units` into the acting unit's own inventory, which is the wheat the
#: tail FEED spends. `crop=I_TOMATO` is the same board with an empty carry.
def _care_board(n_goose=2, n_crop=2, crop=None, t_cons=0, wheat=0, day=10,
                money=0, yld=6, crop_first=False):
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_cons_a = z.copy()
    t_yield = z.copy()
    t_day = z.copy()
    a0 = n_crop if crop_first else 0
    c0 = 0 if crop_first else n_goose
    kind[a0:a0 + n_goose], occ[a0:a0 + n_goose] = spec.KIND_COOP, 0
    t_cons_a[a0:a0 + n_goose], t_day[a0:a0 + n_goose] = t_cons, day - 5
    kind[c0:c0 + n_crop] = spec.KIND_PLANT
    occ[c0:c0 + n_crop] = spec.I_WHEAT if crop is None else crop
    t_yield[c0:c0 + n_crop] = yld
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = wheat
    price = BASE_PRICE.copy()
    price[spec.I_WHEAT] = 200                    # > EGG, so `care_pays` fails
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=t_cons_a, t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(4), price=price,
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32))


def _pair(view, macro, monkeypatch):
    """(plan with the switch off, plan with it on) on one board."""
    monkeypatch.setattr(P, "TAIL_CARE_ON", False)
    base = _plan(view, macro)
    monkeypatch.setattr(P, "TAIL_CARE_ON", True)
    return base, _plan(view, macro)


def _written(base, got):
    """[(unit, turn, op)] the switch wrote into a turn that used to PASS."""
    b, g = np.asarray(base[0]), np.asarray(got[0])
    return [(int(u), int(t), int(g[u, t]))
            for u, t in np.argwhere((b == O.OP_PASS) & (g != O.OP_PASS))]


# =========================================================================
# OFF: byte-identical to the planner the switch was cut into
# =========================================================================

def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte. Pinned on
    `test_route_early`'s digests, taken off the tree at `a838700`."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_passes_the_tail_beside_an_uncared_animal(off):
    """The behaviour the switch exists to change: the block feeds the goose it
    is routed through, `care_pays` refuses the care, and the unit then spends
    every remaining turn of the day on PASS a two-step walk away from it."""
    view = _care_board(n_goose=2, n_crop=2, crop=spec.I_TOMATO, t_cons=1, wheat=10)
    unit_op = np.asarray(_plan(view, _macro())[0])
    assert (unit_op == O.OP_FEED).any(), "the board's own feed did not plan"
    assert not (unit_op == O.OP_CARE).any(), "the board planned a care"
    last = int(np.nonzero(unit_op[0] != O.OP_PASS)[0].max())
    assert P.TPD - 1 - last >= 3, last


# =========================================================================
# ON: the tail feeds and cares, and nothing else moves
# =========================================================================

def test_on_feeds_then_cares_an_unfed_animal(on, monkeypatch):
    """The carrying case: the block harvests wheat into the unit's own
    inventory and ends beside geese the day priced no feed for, so the tail
    walks over and spends two turns on one tile -- FEED, then CARE."""
    view = _care_board(n_goose=3, n_crop=6, crop=spec.I_WHEAT, crop_first=True)
    base, got = _pair(view, _macro(), monkeypatch)
    wrote = _written(base, got)
    ops = [op for _, _, op in wrote]
    assert O.OP_FEED in ops and O.OP_CARE in ops, wrote
    # Same unit, and the CARE is the turn straight after the FEED: the bonus
    # banks only on a day the animal is also fed.
    (uf, tf), = [(u, t) for u, t, op in wrote if op == O.OP_FEED]
    (uc, tc), = [(u, t) for u, t, op in wrote if op == O.OP_CARE]
    assert (uc, tc) == (uf, tf + 1), wrote


def test_on_cares_the_animal_its_own_block_already_fed(on, monkeypatch):
    """The census's 43.1 animal-days: the day feeds the goose (it is one night
    from escaping) and `care_pays` then refuses the care that feed exists to
    buy. The hop revisits the tile the block already ran and banks the bonus
    for one turn and no wheat at all -- which is the case the filler's "tiles
    no block holds" rule excludes."""
    view = _care_board(n_goose=2, n_crop=2, crop=spec.I_TOMATO, t_cons=1, wheat=10)
    base, got = _pair(view, _macro(), monkeypatch)
    wrote = _written(base, got)
    assert [op for _, _, op in wrote][-1] == O.OP_CARE, wrote
    assert O.OP_FEED not in [op for _, _, op in wrote], wrote


def test_on_leaves_an_unfed_animal_alone_when_the_unit_carries_no_wheat(on, monkeypatch):
    """The same board as the feed-then-care case with tomatoes in place of the
    wheat, so the unit reaches its tail with an empty inventory. A CARE on an
    animal the day never feeds banks nothing (`:829`), and the animal is not
    hungry enough for a bare survival feed either, so the hop must decline the
    tile and leave the turns as PASS."""
    view = _care_board(n_goose=3, n_crop=6, crop=spec.I_TOMATO, crop_first=True)
    base, got = _pair(view, _macro(), monkeypatch)
    assert _written(base, got) == []
    for k in range(3):
        assert np.array_equal(np.asarray(base[k]), np.asarray(got[k])), k


def test_on_respects_the_turns_the_tail_has_left(on, monkeypatch):
    """The goose is two steps back from where the block ends, so the visit
    costs three turns. With four turns of tail it is taken; with two -- one
    crop stop more, and nothing else changed -- it is not."""
    for n_crop, want in ((3, True), (4, False)):
        view = _care_board(n_goose=2, n_crop=n_crop, crop=spec.I_TOMATO,
                           t_cons=1, wheat=10)
        base, got = _pair(view, _macro(), monkeypatch)
        assert bool(_written(base, got)) is want, (n_crop, _written(base, got))


def test_on_leaves_every_turn_the_route_owns_alone(monkeypatch):
    """Against the shipped defaults, on twelve seeded boards: the hop writes
    into PASS turns and nowhere else, so it changes no admission, no block cut
    and no market row -- every op the day already had is on the same turn, for
    the same unit, with the same argument."""
    for s in PIN_SEEDS + (100, 101):
        view, macro = _seeded_case(s)
        base, got = _pair(view, macro, monkeypatch)
        keep = np.asarray(base[0]) != O.OP_PASS
        for k in range(3):                       # unit_op, unit_a, unit_q
            assert np.array_equal(np.asarray(base[k])[keep],
                                  np.asarray(got[k])[keep]), (s, k)
        for k in (3, 4, 5):                      # mkt_op, mkt_a, mkt_q
            assert np.array_equal(np.asarray(base[k]), np.asarray(got[k])), (s, k)


def test_on_only_ever_writes_a_walk_a_feed_or_a_care(monkeypatch):
    """Nothing that needs a purchase or a PICKUP, and no HARVEST: the two ops
    the hop takes bank into tile state at end of day and carry nothing out.
    The seeded boards fire it, so this is not vacuous."""
    fired = 0
    for s in PIN_SEEDS + (100, 101):
        view, macro = _seeded_case(s)
        base, got = _pair(view, macro, monkeypatch)
        wrote = _written(base, got)
        fired += len(wrote)
        for u, t, op in wrote:
            assert op in CARE_OPS, (s, u, t, op)
    assert fired > 0, "the hop never fired on the seeded boards"


def test_on_never_cares_a_drop_day(on, monkeypatch):
    """A DROP day's tail is the walk home plus the DROP, measured from the
    block's last tile -- the hop would walk the unit off it."""
    for day in (O.LAST_SHED_DAY, O.LAST_SHED_DAY + 1):
        view, macro = _view(day=day, n_coop=8, n_ripe=24, yld=6, wheat=20,
                            money=8_000), _macro()
        base, got = _pair(view, macro, monkeypatch)
        if not P.DROP_ON:
            pytest.skip("DROP_ON is off")
        for k in range(3):
            assert np.array_equal(np.asarray(base[k]), np.asarray(got[k])), (day, k)


def test_on_composes_with_the_tail_filler(monkeypatch):
    """The two switches share the tail cursor and nothing else, and the care
    hop runs first. With the filler also on the invariant still holds, and
    every turn either switch writes carries one of their five ops."""
    monkeypatch.setattr(P, "TAIL_FILL_ON", True)
    both = CARE_OPS + (O.OP_WATER, O.OP_DIG, O.OP_COLLECT_FERT)
    for s in PIN_SEEDS:
        view, macro = _seeded_case(s)
        base, got = _pair(view, macro, monkeypatch)
        keep = np.asarray(base[0]) != O.OP_PASS
        for k in range(3):
            assert np.array_equal(np.asarray(base[k])[keep],
                                  np.asarray(got[k])[keep]), (s, k)
        for u, t, op in _written(base, got):
            assert op in both, (s, u, t, op)


#: `plan.EARLY_SELL_ON` went on by default on 2026-09-03: the day's first lot
#: rides turn 1 behind the BUY row instead of standing on `O.SELL_TURNS[0]`.
#: It is pinned off for this file the way `a838700`'s stack was pinned off for
#: the digest fixtures -- the pins and worked examples below are the plan
#: *before* it, and what this file is about (the tail's care) is a question the switch does
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
