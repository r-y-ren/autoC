"""`plan.IDLE_TAIL_HOPS_ON`: the tail filler's hop budget, re-read off the engine.

IDLEOPS (`docs/strategy/2026-09-16-idleops.md`, `S/idleops/idle.py`) replayed 34
Kaggle games through the engine's own `_apply_unit_action` and classified every
idle unit-op of both seats.  Our shipped pair idles 706 ops a game (10.5 %)
against M & M & P & Q's 335 (5.1 %), and the split by where the op sits inside
its own unit-day is dawn 297 / gap 10 / **tail 398** for us against 76 / 6 / 243
for them.  The dawn half is the turn-1 BUY-row law, whose family is closed
(`ROUTE_FREEFIRST_ON`, `PRESTOCK_V2_ON`).  The tail half is `TAIL_HOPS`: the
filler's candidate mask is read off the MORNING board, where every unadmitted
plant tile still has `t_water == 0`, so what runs out at the end of a tail is
hops and not candidates.

ON, the filler loop unrolls `IDLE_TAIL_HOPS` (4) hops instead of `TAIL_HOPS`
(2); every gate, mask and strike-off inside the hop is `TAIL_FILL_ON`'s own.
THE SWITCH SHIPS OFF unless that document's legs say otherwise.
"""
from __future__ import annotations

import os
import sys

import _pin

_pin.bootstrap()

import contextlib

import numpy as np

from kagg3 import spec
from kagg3.core import plan as P

from test_budget_order import _macro          # safe: kagg3 is already loaded

#: The commit this branch was cut from -- master's shipped pair, whose planner
#: has no `IDLE_TAIL_HOPS_ON` at all.  A SHA, not `HEAD~1`, so the pin keeps its
#: meaning after the branch is merged.
PRE_SWITCH = "e1fecfa"


def _view(day=12, money=20_000, nquad=3, shops=4, standing=(), seeds=4, animals=()):
    """A board carrying `standing` = ((crop, n_tiles, age), ...) live plants and
    `animals` = ((animal, n_tiles), ...) stocked pastures.  Every plant is
    unwatered and every animal has a unit of fertilizer waiting, which is the
    morning board the filler's candidate mask is read off."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ, t_day = z - 1, z.copy()
    t_favail = z.copy()
    at = 0
    for crop, n, age in standing:
        kind[at:at + n] = spec.KIND_PLANT
        occ[at:at + n] = crop
        t_day[at:at + n] = day - age
        at += n
    for an, n in animals:
        kind[at:at + n] = spec.KIND_PASTURE
        occ[at:at + n] = an
        t_favail[at:at + n] = 1
        at += n
    inv = np.full(spec.N_PRODUCTS, int(spec.MARKET_I0), np.int32)
    tbl = spec.build_price_table()
    i0 = int(np.clip(spec.MARKET_I0 - spec.PRICE_TABLE_LO, 0, spec.PRICE_TABLE_N - 1))
    price = np.array([int(tbl[p, i0]) for p in range(spec.N_PRODUCTS)], np.int32)
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=z.copy(), t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(),
        t_favail=t_favail, shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.full(spec.N_CROPS, seeds, np.int32), money=np.int32(money),
        nquad=np.int32(nquad), price=price, mkt_inv=inv,
        shops=np.full(spec.N_SHOPS, int(shops), np.int32))


MIX = np.array([4, 3, 2, 2, 2], np.int32)
ZERO = np.zeros(spec.N_CROPS, np.int32)

PIN_BOARDS = (
    # name, view kwargs, plant_target
    ("wide_plants", dict(day=12, standing=((spec.I_WHEAT, 30, 1),
                                           (spec.I_TOMATO, 10, 9))), ZERO),
    ("plants_mix",  dict(day=12, standing=((spec.I_WHEAT, 20, 2),
                                           (spec.I_CARROT, 14, 1))), MIX),
    ("herd",        dict(day=15, standing=((spec.I_WHEAT, 16, 1),),
                         animals=((spec.I_COW, 4), (spec.I_SHEEP, 4))), ZERO),
    ("late",        dict(day=22, shops=6, standing=((spec.I_TOMATO, 12, 10),
                                                    (spec.I_STRAWBERRY, 8, 12))), ZERO),
    ("small",       dict(day=8, money=6_000, standing=((spec.I_WHEAT, 10, 1),)), MIX),
    ("big",         dict(day=18, money=60_000, shops=6,
                         standing=((spec.I_WHEAT, 25, 2), (spec.I_MELON, 10, 8),
                                   (spec.I_TOMATO, 8, 9))), MIX),
)

#: The two boards the extra hops reach, measured by `S/idleops/probe_hops.py`.
FIRING = ("plants_mix", "small")


def _plan(view, target):
    return tuple(np.asarray(a)
                 for a in P.build_day(np, view, _macro(plant_target=target)))


def _own_digests():
    return {n: _pin.digest(_plan(_view(**kw), t)) for n, kw, t in PIN_BOARDS}


@contextlib.contextmanager
def _knob(on=True):
    was = P.IDLE_TAIL_HOPS_ON
    P.IDLE_TAIL_HOPS_ON = on
    try:
        yield
    finally:
        P.IDLE_TAIL_HOPS_ON = was


def _work(view, target):
    """Unit ops the day actually spends, i.e. everything that is not a PASS."""
    op = _plan(view, target)[0]
    return int((np.asarray(op) != P.O.OP_PASS).sum())


# =========================================================================
# OFF is master, byte for byte
# =========================================================================

def test_off_is_the_default():
    assert P.IDLE_TAIL_HOPS_ON is False
    assert P.tail_hops() == P.TAIL_HOPS == 2


def test_off_plan_is_byte_identical_to_master():
    """Whole-plan sha256 on six boards against a pristine `e1fecfa` tree.
    That tree predates FERT_TIMING (shipped ON since sub 56284867), so the
    fertilizer knob is held OFF for the comparison."""
    was = P.FERT_TIMING_ON
    P.FERT_TIMING_ON = False
    try:
        own = _own_digests()
    finally:
        P.FERT_TIMING_ON = was
    assert own == _pin.tree_digests(__file__, PRE_SWITCH)


def test_on_moves_the_hop_count_and_nothing_else_about_the_filler():
    with _knob():
        assert P.tail_hops() == P.IDLE_TAIL_HOPS == 4
    assert P.TAIL_FILL_ON is True, "the filler this switch resizes must be on"


# =========================================================================
# ON: what the extra hops may and may not do
# =========================================================================

def test_on_changes_the_plan_where_the_tail_is_open():
    """The property the switch exists for: on a board whose unadmitted tiles
    still offer carry-free work, the third and fourth hops take some of it."""
    moved = []
    for name, kw, t in PIN_BOARDS:
        v = _view(**kw)
        off = _plan(v, t)
        with _knob():
            on = _plan(v, t)
        if any(not np.array_equal(a, b) for a, b in zip(off, on)):
            moved.append(name)
    assert set(moved) == set(FIRING), moved


def test_on_never_takes_work_away():
    """A hop can only turn a PASS into an op: the filler writes into turns the
    block has already given up (`f_left`), and its gate refuses a hop that does
    not fit."""
    for name, kw, t in PIN_BOARDS:
        v = _view(**kw)
        off = _work(v, t)
        with _knob():
            on = _work(v, t)
        assert on >= off, f"{name}: {on} < {off}"
        if name in FIRING:
            assert on > off, f"{name}: the switch fired but added no op"


def test_a_board_with_no_open_tail_is_the_off_plan():
    """`big` hires a crew that spends its day inside its blocks, so there is
    nothing for a third hop to reach and the plan is byte-identical."""
    v = _view(**dict(PIN_BOARDS[-1][1]))
    off = _plan(v, PIN_BOARDS[-1][2])
    with _knob():
        on = _plan(v, PIN_BOARDS[-1][2])
    assert all(np.array_equal(a, b) for a, b in zip(off, on))


def test_no_gene_is_appended():
    """The magnitude is a module constant, not a theta coordinate: the layout
    is frozen [LAW] and an appended gene is only worth its slope if an ES arm
    is going to train it."""
    from kagg3.core import policy as PO
    assert "th" not in dict(PO.SHAPES), \
        "an IDLE_TAIL_HOPS gene was appended without a measured slope"


if __name__ == "__main__":
    for _n, _d in _own_digests().items():
        print(_n, _d)
