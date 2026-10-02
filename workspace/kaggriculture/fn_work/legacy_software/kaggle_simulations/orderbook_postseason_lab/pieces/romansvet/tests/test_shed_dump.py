"""`plan.SHED_DUMP_ROW_ON`: the hour-23 overflow row.

The public V45 notebook's `_r148_overflow` (`docs/strategy/2026-09-16-v45-
notebook.md` sect.2.5 item 4), re-derived: at hour 23 every unit's carried
inventory is pushed into the shed and the part that does not fit is destroyed,
so on a day the projection says the deposit overflows this row sells exactly the
overflow out of the stock still standing in the shed -- and on every other day
it emits nothing at all.

OFF, `dump` is `None`, `_market` emits the rows it always emitted and
`rollout.MARKET_TURNS` is the six turns it always resolved, so the shipped
program is unchanged: pinned below against a pristine `git archive c5f68ac src`
tree, whole-plan digests on five boards, exactly as `tests/test_lot4.py` and
`tests/test_spread6.py` pin their own.
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
import test_shed_overflow as TSO
from test_budget_order import _macro
from test_spread6 import PIN_BOARDS, _sell_grid, _view

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture()
def on(monkeypatch):
    monkeypatch.setattr(P, "SHED_DUMP_ROW_ON", True)


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _macro()))


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


def _row23(view, macro=None):
    """int[9]: units of each product the dump row offers."""
    return _sell_grid(_plan(view, macro))[P.SHED_DUMP_ROW_TURN]


def _destroyed(view, macro=None):
    return int(P.build_day_stats(view, macro or _macro()).overflow_destroyed)


#: The `tests/test_shed_overflow.py` board and its own numbers: 20 ripe tomatoes
#: at the head of the sweep, 60 hungry geese behind them the empty purse's one
#: unit never reaches, 90 wheat in the shed. The day reserves one wheat per
#: hungry animal, so 60 of those 90 are hidden from the forced sale (0.9) and
#: `DOOMED` = 40 units are destroyed at the dump. It is the one board family in
#: the tree where the shed still HOLDS something at hour 23.
DOOMED = TSO.DOOMED


def _own_digests():
    out = {}
    for n, kw in PIN_BOARDS:
        out[n] = _digest(_plan(_view(**kw)))
    out["overflow"] = _digest(_plan(TSO._view(), TSO._macro()))
    out["fits"] = _digest(_plan(TSO._view(day=20), TSO._macro()))
    return out


def _head_digests():
    """The same seven plans, built by a pristine `git archive c5f68ac src` tree in
    a subprocess -- the pin is the tree this switch was added to, not this
    file's own output."""
    return _pin.tree_digests(__file__, ref=_pin.SHIPPED)


# =========================================================================
# OFF: the shipped program, byte for byte
# =========================================================================

def test_off_is_the_default():
    assert P.SHED_DUMP_ROW_ON is False
    assert P.SHED_DUMP_ROW_TURN == 23 == spec.TURNS_PER_DAY - 1
    assert P.SHED_DUMP_ROW_CHEAP_FIRST is True


def test_off_plan_is_byte_identical_to_head():
    """The whole plan tuple, hashed, against a pristine HEAD tree."""
    assert _own_digests() == _head_digests()


def test_off_leaves_the_sim_market_turns_alone_and_on_adds_the_dump_turn():
    """`sim/rollout` reads the row set at import, after the runner has set the
    switches; OFF it must be the shipped row set (four lots since LOT4 went ON
    at turn 17, 2026-09-16 ship-lot4)."""
    def turns(sw):
        return subprocess.run(
            [sys.executable, "-c",
             "import sys; sys.path.insert(0, 'src')\n"
             "from kagg3.core import plan as P\n" + sw +
             "from kagg3.sim import rollout as R; print(R.MARKET_TURNS)"],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    assert turns("") == "(0, 1, 2, 3, 10, 17, 18)"
    assert turns("P.SHED_DUMP_ROW_ON = True\n") == "(0, 1, 2, 3, 10, 17, 18, 23)"


# =========================================================================
# ON: the size of the row
# =========================================================================

def test_the_row_is_exactly_the_units_the_night_would_destroy(on):
    """The mechanism: `DOOMED` units are projected to die at the dump, and the
    row offers exactly `DOOMED` units of the one product still standing in the
    shed at hour 23 -- no more (it is an amount, not a price) and no less."""
    view = TSO._view()
    assert _destroyed(view, TSO._macro()) == DOOMED
    row = _row23(view, TSO._macro())
    assert int(row[spec.I_WHEAT]) == DOOMED
    assert int(row.sum()) == DOOMED


def test_the_row_moves_no_other_row_of_the_day(monkeypatch):
    """Strictly additional volume: every earlier turn of the plan is the plan
    OFF, array for array. `lots`, `s_qty` and the reservation gate are not
    touched, so nothing the allocator decided moves."""
    view = TSO._view()
    monkeypatch.setattr(P, "SHED_DUMP_ROW_ON", False)
    off = _plan(view, TSO._macro())
    monkeypatch.setattr(P, "SHED_DUMP_ROW_ON", True)
    onp = _plan(view, TSO._macro())
    for i, (a, b) in enumerate(zip(off, onp)):
        if i < 3:                                   # the unit ops: untouched
            assert np.array_equal(a, b), f"unit array {i} moved"
        else:                                       # op/arg/qty: turn 23 only
            moved = np.nonzero((a != b).any(axis=1))[0].tolist()
            assert moved in ([], [P.SHED_DUMP_ROW_TURN]), f"market array {i} {moved}"


def test_the_row_keeps_the_reservation_of_a_task_the_route_reaches(on):
    """Four coops in FRONT of the ripe tiles are fed, so their wheat is picked
    up before hour 23 and the row may not offer it: the projection charges the
    pickups the route actually makes (`blk`), and the ask falls with them."""
    view = TSO._view(lead_coops=4)
    n = _destroyed(view, TSO._macro())
    assert 0 < n < DOOMED
    assert int(_row23(view, TSO._macro()).sum()) == n


def test_the_row_is_empty_on_a_day_the_deposit_fits(on):
    """Every board of the shared pin set, plus the same overflow board played on
    an ordinary day: the projection says tonight's deposit fits, so the row is
    not there at all."""
    assert _destroyed(TSO._view(day=20), TSO._macro()) == 0
    assert int(_row23(TSO._view(day=20), TSO._macro()).sum()) == 0
    for name, kw in PIN_BOARDS:
        assert _destroyed(_view(**kw)) == 0, name
        assert int(_row23(_view(**kw)).sum()) == 0, name


def test_the_row_is_empty_when_the_day_has_already_offered_its_whole_shed(on):
    """THE MEASURED CASE, and the reason this switch is a zero on the shipped
    agent (`docs/strategy/2026-09-16-sheddump.md`): 20 units in the shed and
    120 ripening, so 20 units die at the dump -- and all 20 are already on a
    lot, so there is nothing left at hour 23 to sell. A SELL draws on the SHED
    and the doomed units are in the crew's HANDS until `eod.drop_inventories`
    runs."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ, t_yield = z - 1, z.copy()
    kind[:20] = spec.KIND_PLANT
    occ[:20] = spec.I_TOMATO
    t_yield[:20] = 6
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = 20
    view = P.DayView(
        day=np.int32(13), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=z.copy(), t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(1000), nquad=np.int32(4),
        price=np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32))
    assert _destroyed(view) == 20
    assert int(_row23(view).sum()) == 0


def test_the_row_never_outruns_the_ask_or_the_standing_stock(on):
    """Two bounds over a sweep of the overflow board: the row never offers more
    than the night would destroy, and never more than the shed can hold up at
    hour 23 (dawn stock less everything already offered)."""
    for kw in (dict(), dict(n_ripe=10), dict(n_ripe=30), dict(lead_coops=4),
               dict(lead_coops=12), dict(wheat=40), dict(wheat=100),
               dict(yld=2), dict(yld=20), dict(day=20), dict(money=5000)):
        view, macro = TSO._view(**kw), TSO._macro()
        row = _row23(view, macro)
        assert (row >= 0).all(), kw
        assert int(row.sum()) <= _destroyed(view, macro), kw
        offered = _sell_grid(_plan(view, macro))[:P.SHED_DUMP_ROW_TURN].sum(axis=0)
        stand = np.maximum(np.asarray(view.shed)[:spec.N_PRODUCTS] - offered, 0)
        assert (row <= stand).all(), (kw, row.tolist(), stand.tolist())


if __name__ == "__main__":
    for k, v in _own_digests().items():
        print(k, v)
