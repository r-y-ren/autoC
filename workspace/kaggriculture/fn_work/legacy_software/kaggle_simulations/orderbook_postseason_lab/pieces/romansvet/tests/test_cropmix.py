"""`plan.CROP_SCARCE_ON`: the crop MIX is picked on the dawn quote, and the
tile is sold on a different one.

`brain.decide` splits the day's tiles across the five crops with a softmax over
the head's `grow` score (`brain.py:1048-1064`), and the only price the head
reads is the hour-0 quote of *today* (`brain.py:552-553`).  The money for a
seed is priced somewhere else: `_candidates` walks each planting's units down
the sales-window curve -- hour-0 inventory drained to that crop's own first
yield plus this farm's committed pipeline (`plan.py:6919-6935`) -- so the
planner already knows what the tile will fetch and the mix never reads it.

Measured on 20 M & M & P & Q replays (`docs/strategy/2026-09-16-cropmix.md`):
MELON is planted at 0.94 of base and harvested at 0.64, STRAWBERRY 1.45 ->
1.55, and `r(dawn, harvest)` is 0.95 on CARROT but -0.18 on STRAWBERRY.

ON, `plant_target` is re-shared by a clipped `fwd / spot` ratio with the total
preserved to the tile.  THE SWITCH SHIPS OFF unless that document's legs say
otherwise.
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
#: has no `CROP_SCARCE_ON` at all.  A SHA, not `HEAD~1`, so the pin keeps its
#: meaning after the branch is merged.
PRE_SWITCH = "aad46ed"

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _quote(prod, inv_over):
    """The engine's quote for `prod` at `MARKET_I0 + inv_over`, off the
    engine's own table -- never a re-implementation of the curve."""
    tbl = spec.build_price_table()
    i = int(np.clip(spec.MARKET_I0 + inv_over - spec.PRICE_TABLE_LO,
                    0, spec.PRICE_TABLE_N - 1))
    return int(tbl[prod, i])


def _view(day=10, money=30_000, nquad=3, shops=3, standing=(), inv_over=None,
          seeds=8):
    """A board carrying `standing` = ((crop, n_tiles, age), ...) live plants,
    which is what puts units into `_pipeline_units` and so moves `fwd` away
    from `spot` for those crops and for no others."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_day, t_yield = z.copy(), z.copy()
    at = 0
    for crop, n, age in standing:
        kind[at:at + n] = spec.KIND_PLANT
        occ[at:at + n] = crop
        t_day[at:at + n] = day - age
        at += n
    inv = np.full(spec.N_PRODUCTS, int(spec.MARKET_I0), np.int32)
    for p, over in (inv_over or {}).items():
        inv[p] = spec.MARKET_I0 + int(over)
    price = np.array([_quote(p, int(inv[p]) - spec.MARKET_I0)
                      for p in range(spec.N_PRODUCTS)], np.int32)
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=z.copy(), t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.full(spec.N_CROPS, seeds, np.int32), money=np.int32(money),
        nquad=np.int32(nquad), price=price, mkt_inv=inv,
        shops=np.full(spec.N_SHOPS, int(shops), np.int32))


#: A mix that asks for every crop, so the re-share has something to move.
MIX = np.array([6, 4, 3, 3, 4], np.int32)

PIN_BOARDS = (
    # name, view kwargs, plant_target
    ("flat",    dict(day=10), MIX),
    ("glut",    dict(day=10, standing=((spec.I_MELON, 12, 2),
                                       (spec.I_STRAWBERRY, 8, 3))), MIX),
    ("early",   dict(day=4, shops=1, standing=((spec.I_WHEAT, 20, 1),)), MIX),
    ("late",    dict(day=19, shops=6,
                     standing=((spec.I_TOMATO, 10, 4), (spec.I_MELON, 6, 5))), MIX),
    ("drained", dict(day=14, shops=6,
                     inv_over={spec.I_MELON: 400, spec.I_WHEAT: -300}), MIX),
    ("nothing", dict(day=10), np.zeros(spec.N_CROPS, np.int32)),
)


def _plan(view, target):
    return tuple(np.asarray(a)
                 for a in P.build_day(np, view, _macro(plant_target=target)))


def _own_digests():
    return {n: _pin.digest(_plan(_view(**kw), t)) for n, kw, t in PIN_BOARDS}


@contextlib.contextmanager
def _knob(on=True):
    was = P.CROP_SCARCE_ON
    P.CROP_SCARCE_ON = on
    try:
        yield
    finally:
        P.CROP_SCARCE_ON = was


def _scarce(view, target):
    """`plant_target` after the re-share, called directly."""
    tbl = np.asarray(P.default_price_table())
    out = P._crop_scarce(np, view, _macro(plant_target=target), tbl)
    return np.asarray(out.plant_target)


# =========================================================================
# OFF is master, byte for byte
# =========================================================================

def test_off_is_the_default():
    assert P.CROP_SCARCE_ON is False


def test_off_plan_is_byte_identical_to_master():
    """Whole-plan sha256 on six boards against a pristine `aad46ed` tree."""
    assert _own_digests() == _pin.tree_digests(__file__, PRE_SWITCH)


# =========================================================================
# ON: what the re-share may and may not do
# =========================================================================

def test_on_moves_the_mix_on_a_glut_board():
    """The property the switch exists for: a board carrying twelve melon and
    eight strawberry tiles has a pipeline the dawn quote cannot see, so the ON
    plan must differ from the OFF plan in at least one array."""
    v = _view(day=10, standing=((spec.I_MELON, 12, 2), (spec.I_STRAWBERRY, 8, 3)))
    off = _plan(v, MIX)
    with _knob():
        on = _plan(v, MIX)
    assert any(not np.array_equal(a, b) for a, b in zip(off, on)), \
        "ON is inert on the glut board the switch is an argument about"
    assert _scarce(v, MIX)[spec.I_MELON] < MIX[spec.I_MELON]


def test_the_total_is_preserved_to_the_tile():
    """A MIX change and not a development change: everything that reads
    `sum(plant_target)` -- `n_dev`, `_seed_room`, the land valuation -- must
    see the number it saw."""
    for n, kw, t in PIN_BOARDS:
        got = _scarce(_view(**kw), t)
        assert int(got.sum()) == int(np.asarray(t).sum()), (n, got, t)


def test_a_crop_the_brain_ruled_out_stays_at_zero():
    """`can_mature` and `absorb` are still the last word on what may be
    planted: the re-share multiplies the want, so a zero want stays zero."""
    t = np.array([6, 0, 0, 5, 4], np.int32)
    v = _view(day=10, standing=((spec.I_MELON, 12, 2),))
    got = _scarce(v, t)
    assert int(got[spec.I_CARROT]) == 0 and int(got[spec.I_TOMATO]) == 0


def test_a_market_that_will_not_move_is_the_off_plan():
    """`fwd / spot` is exactly 1.0 with no pipeline and no town drain, so the
    ratio is `CROP_SCARCE_ONE` on every crop and `_take_lr` returns the mix
    unchanged -- the identity that makes this a correction and not a second
    mechanism."""
    v = _view(day=10, shops=0, standing=())
    assert np.array_equal(_scarce(v, MIX), MIX)
    off = _plan(v, MIX)
    with _knob():
        on = _plan(v, MIX)
    assert all(np.array_equal(a, b) for a, b in zip(off, on))


def test_the_ratio_is_clipped_both_ways():
    """No crop's share may move by more than a third relatively -- the whole
    lesson of `PLANT_MIX_DRAIN_ON` (-11,906 at t -15.4, `brain.py:876`)."""
    assert P.CROP_SCARCE_LO / P.CROP_SCARCE_ONE >= 0.7
    assert P.CROP_SCARCE_HI / P.CROP_SCARCE_ONE <= 1.4
    # a board glutted past the floor on melon still keeps melon tiles
    v = _view(day=10, standing=((spec.I_MELON, 30, 2),),
              inv_over={spec.I_MELON: 2_000})
    got = _scarce(v, MIX)
    assert int(got[spec.I_MELON]) >= 1


def test_no_gene_is_appended():
    """The magnitude is a module constant, not a theta coordinate: the layout
    is frozen [LAW] and an appended gene is only worth its slope if an ES arm
    is going to train it.  This one is judged as a fixed clip."""
    from kagg3.core import policy as PO
    assert "cs" not in dict(PO.SHAPES), \
        "a CROP_SCARCE gene was appended without a measured slope"


if __name__ == "__main__":
    for _n, _d in _own_digests().items():
        print(_n, _d)
