"""`plan.SHED_DEFICIT_ON`: the watering bonus the overflow projection forgets.

`SHED-CLIP` (2026-09-14) counted 21.6 units a game-seat destroyed at the shed
door under B's shipped switches, 15.4 of them at the nightly dump.  The only
planner guard is the forced sale, and it projects tonight's shed on
`view.t_yield` -- the *pre-watering* yield -- while a chain that waters a tile
before harvesting it banks `t_yield + 2` that same evening.  `plan.py` already
spells the corrected quantity three times over (`MELON_OPEN`'s `m_units`,
`MIDDAY_PLACE_V2`'s `mv_units`, `BANK_BEFORE_LOT_ON`'s `bl_units`), and ON is
that same term and nothing else.

OFF the expression is literally `view.t_yield`, so the shipped program is
unchanged: pinned below against a pristine `git archive c5f68ac src` tree, whole-
plan digests on four boards, exactly as `tests/test_prestock_v2.py` pins its
own switch.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile

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

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)

#: A wheat tile of this age is inside BOTH windows at once -- the bonus window
#: (`CROP_WINDOW_START` 2 .. `CROP_MAX_YIELD_DAY` 4) and the harvest window
#: (`age >= harvest_age`) -- so its chain is WATER then HARVEST on one tile,
#: which is precisely the shape `inflow` under-counts by two units.
WATER_HARVEST_AGE = 4


def _view(day=10, money=20_000, n_wh=8, age=WATER_HARVEST_AGE, shed_wh=0,
          shed_to=0, t_water=0, yld=6, nquad=1):
    """`n_wh` wheat tiles of `age` days, dry (`t_water == 0`) unless asked, on a
    shed already holding `shed_wh` wheat and `shed_to` tomato."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_day, t_wat, t_yield = z.copy(), z.copy(), z.copy()
    kind[:n_wh] = spec.KIND_PLANT
    occ[:n_wh] = spec.I_WHEAT
    t_day[:n_wh] = day - age
    t_yield[:n_wh] = yld
    t_wat[:n_wh] = t_water
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = shed_wh
    shed[spec.I_TOMATO] = shed_to
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=t_wat,
        t_cons=z.copy(), t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(nquad), price=BASE_PRICE,
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32))


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _macro()))


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


def _sold(plan):
    """Units offered by every SELL slot of the day, all turns, all products."""
    op, _arg, qty = plan[3:6]
    return int(qty[op == O.MO_SELL].sum())


def _chain_has(plan_view, macro, ops):
    """True when some reached tile's op chain carries every op in `ops`.

    Read off the emitted unit program, which is what `d.chain_op` becomes: a
    tile's chain is the run of ops one unit performs, so "both on one tile"
    shows up as both ops present in the same unit's row."""
    unit_op = _plan(plan_view, macro)[0]
    return any(all((row == o).any() for o in ops) for row in unit_op)


#: Four boards. `deficit` is a whole-shed scalar, so the pin needs a board that
#: overflows (`hot`), one that does not (`cool`), one whose tiles are already
#: watered so the bonus term is zero even ON (`wet`), and one with no plants at
#: all (`bare`).
PIN_BOARDS = (
    ("hot", dict(day=10, n_wh=8, shed_wh=50, shed_to=45)),
    ("cool", dict(day=10, n_wh=8, shed_wh=0, shed_to=0)),
    ("wet", dict(day=10, n_wh=8, shed_wh=50, shed_to=45, t_water=1)),
    ("bare", dict(day=12, n_wh=0, shed_wh=60, shed_to=38)),
)


def _own_digests():
    return {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}


def _head_digests():
    """The same four plans, built by a pristine `git archive c5f68ac src` tree in a
    subprocess.  The pin is the tree this switch was added to, not this file's
    own output, which is the only form of "OFF is character-identical" worth
    asserting (`tests/test_prestock_v2.py`)."""
    return _pin.tree_digests(__file__, ref=_pin.SHIPPED)


# =========================================================================
# OFF: the shipped program, character for character
# =========================================================================

def test_off_is_the_default():
    assert P.SHED_DEFICIT_ON is False


def test_off_plan_is_byte_identical_to_head():
    """The whole plan tuple, hashed, against a pristine HEAD tree."""
    assert _own_digests() == _head_digests()


# =========================================================================
# ON: the bonus, and only the bonus
# =========================================================================

def test_the_board_really_waters_before_it_harvests():
    """The premise of the arm, asserted rather than assumed: at
    `WATER_HARVEST_AGE` the wheat chain carries WATER *and* HARVEST, which is
    the tile `inflow` under-counts.  A tile already watered carries neither
    term."""
    assert _chain_has(_view(**PIN_BOARDS[0][1]), _macro(),
                      (O.OP_WATER, O.OP_HARVEST))
    assert not _chain_has(_view(**PIN_BOARDS[2][1]), _macro(), (O.OP_WATER,))


def test_on_adds_two_units_of_deficit_per_watered_harvest(monkeypatch):
    """`deficit` is not returned, but the forced sale it sizes is: every unit
    of deficit the projection gains is one more unit on a SELL row (the shed
    holds 95 sellable units against a deficit far under that).  Eight tiles
    that water and harvest = 16 units."""
    view = _view(**PIN_BOARDS[0][1])
    off = _sold(_plan(view))
    monkeypatch.setattr(P, "SHED_DEFICIT_ON", True)
    on = _sold(_plan(view))
    assert on - off == 2 * PIN_BOARDS[0][1]["n_wh"], (off, on)


@pytest.mark.parametrize("name", [b[0] for b in PIN_BOARDS[1:]])
def test_on_is_inert_where_the_bonus_cannot_apply(name, monkeypatch):
    """No overflow (`cool`), no dry tile (`wet`), no plant (`bare`): the term is
    zero or the deficit floors at zero, and the plan does not move."""
    view = _view(**dict(PIN_BOARDS)[name])
    off = _digest(_plan(view))
    monkeypatch.setattr(P, "SHED_DEFICIT_ON", True)
    assert _digest(_plan(view)) == off


def test_deficit_never_negative_and_never_oversells(monkeypatch):
    """`deficit = max(proj_eod - SHED_CAPACITY, 0)` keeps its floor ON: a shed
    with room to spare sells exactly what it sold OFF (a negative deficit would
    *reduce* the sale below it), and the forced sale still draws only on
    `spare = max(avail - s_qty, 0)`, so no board offers more than the dawn shed
    holds."""
    for shed_wh in (0, 10, 30, 50, 70, 94):
        for shed_to in (0, 5, 45):
            view = _view(day=10, n_wh=8, shed_wh=shed_wh, shed_to=shed_to)
            off = _sold(_plan(view))
            monkeypatch.setattr(P, "SHED_DEFICIT_ON", True)
            on = _sold(_plan(view))
            monkeypatch.setattr(P, "SHED_DEFICIT_ON", False)
            stock = shed_wh + shed_to
            assert on >= off, (shed_wh, shed_to, off, on)
            assert on <= stock, (shed_wh, shed_to, on, stock)


if __name__ == "__main__":                      # the HEAD-tree subprocess
    for _n, _d in _own_digests().items():
        print(_n, _d)
