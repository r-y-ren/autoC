"""`plan.REBUY_ON` and `MACRO_MODE "rebuy"`: the market-PURCHASE channel.

WHEAT-REBUY (`docs/strategy/2026-09-14-wheat-rebuy.md`). ymg_aq buys 1,144.7
units of market wheat a season and sells 1,476.9 -- 332.8 own units through a
pot it keeps re-buying. Two arms ask whether that purchase leg is worth
anything to us:

* `REBUY_ON` / `REBUY_N` / `REBUY_DAYS` -- our OWN clock: `REBUY_N` extra units
  of wheat on the day's turn-1 BUY row, every day in the window, sold by
  tomorrow's lots like any other stock.
* `MACRO_MODE "rebuy"` (site 9) -- the schedule's own `buy_target[day][WHEAT]`
  as a FLOOR on that row.

Both are off in the shipped program, and the OFF half pins that: the constants
exist, the plan tuple does not move.
"""
from __future__ import annotations

import json
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

ND = spec.N_DAYS


def _view(money=3000, nquad=1, day=0, shed=None):
    z = np.zeros(100, np.int32)
    sh = np.zeros(spec.N_ITEMS, np.int32) if shed is None else shed
    return P.DayView(
        day=np.int32(day),
        kind=np.full(100, spec.KIND_EMPTY, np.int32), occ=z - 1,
        t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(), t_yield=z.copy(),
        t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=sh, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(nquad),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


def _macro(**kw):
    base = {
        "plant_target": np.zeros(spec.N_CROPS, np.int32),
        "animal_want": np.zeros(spec.N_ANIMALS, np.int32),
        "land_bias": np.int32(0),
        "hold": np.full(spec.N_PRODUCTS, 10_000, np.int32),
        "press": np.zeros(spec.N_PRODUCTS, np.int32),
        "grow_mult": np.full(spec.N_PRODUCTS, brain.GROW_ONE, np.int32),
        "compact": np.int32(0),
        "dev_weight": np.int32(brain.GROW_ONE),
        "hire_bias": np.int32(0),
        "crew_target": np.int32(0),
        "animal_defer": np.int32(0),
        "forward_days": np.int32(0),
    }
    # [g12] Appended after the pins in `tests/test_fertengine.py` were cut, and
    # those run this helper against a pristine PRE-`g12` `src` tree in a
    # subprocess -- so the field is named only when the planner has it.
    if "fert_defer" in P.Macro._fields:
        base["fert_defer"] = np.int32(0)
    base.update(kw)
    return P.Macro(**base)


def _sched(tmp_path, buy=None, tag="rebuy"):
    d = dict(tag=tag,
             sell_hour=[[-1] * spec.N_ITEMS] * ND,
             hands_target=[0] * ND,
             animals_target=[[0] * spec.N_ANIMALS] * ND,
             tiles_target=[[0] * spec.N_CROPS] * ND,
             land_target=[0] * ND)
    if buy is not None:
        d["buy_target"] = buy
    p = tmp_path / "sched.json"
    p.write_text(json.dumps(d))
    return str(p)


@pytest.fixture
def off():
    was = (P.MACRO_EXEC_ON, P.MACRO_SCHEDULE, P.MACRO_MODE,
           P.REBUY_ON, P.REBUY_N, P.REBUY_DAYS)
    yield
    (P.MACRO_EXEC_ON, P.MACRO_SCHEDULE, P.MACRO_MODE,
     P.REBUY_ON, P.REBUY_N, P.REBUY_DAYS) = was


def _plan(view, macro):
    return [np.asarray(x) for x in P.build_day(np, view, macro)]


def _wheat_buy(view, macro):
    op, a, q = _plan(view, macro)[3:6]
    return int(q[(op == O.MO_BUY_PRODUCT) & (a == spec.I_WHEAT)].sum())


def _wheat_buy_turns(view, macro):
    op, a, _ = _plan(view, macro)[3:6]
    return sorted({int(t) for t in
                   np.nonzero(((op == O.MO_BUY_PRODUCT)
                               & (a == spec.I_WHEAT)).any(axis=1))[0]})


# ------------------------------------------------------------------ OFF half

def test_rebuy_off_is_the_shipped_default():
    assert P.REBUY_ON is False
    assert P.REBUY_N == 0
    assert P.REBUY_DAYS == (10, 25)
    assert "rebuy" in P.MACRO_MODES and P._MACRO_SITES[9] == ("rebuy",)


def test_setting_the_size_alone_changes_nothing(off):
    """`REBUY_N` is read only inside `if REBUY_ON:` -- the size is inert on its
    own, on the four boards the arm is built to change."""
    macro = _macro(plant_target=np.array([8, 0, 0, 0, 0], np.int32),
                   animal_want=np.array([0, 2, 1], np.int32))
    views = [_view(day=12, money=9000), _view(day=12, money=60000),
             _view(day=20, money=6000), _view(day=5, money=9000)]
    before = [_plan(v, macro) for v in views]
    P.REBUY_N = 40
    for i, (v, b) in enumerate(zip(views, before)):
        for j, (x, y) in enumerate(zip(b, _plan(v, macro))):
            assert np.array_equal(x, y), f"board {i} field {j} moved with REBUY_ON False"


def test_a_schedule_with_buy_rows_is_inert_under_every_other_mode(off, tmp_path):
    """Site 9 fires under `"rebuy"` alone: `plate0` with the same JSON is the
    plan `plate0` always was (the stored raws stay comparable)."""
    macro = _macro()
    view = _view(day=12, money=9000)
    P.macro_load(_sched(tmp_path, buy=[[40] + [0] * (spec.N_ITEMS - 1)] * ND))
    P.MACRO_EXEC_ON = True
    P.MACRO_MODE = "plate0"
    with_buy = _plan(view, macro)
    P.macro_load(_sched(tmp_path, buy=None))
    without = _plan(view, macro)
    for j, (x, y) in enumerate(zip(with_buy, without)):
        assert np.array_equal(x, y), f"field {j} moved: plate0 read the buy row"


# ------------------------------------------------------------------- ON half

def test_rebuy_buys_the_extra_units_on_the_buy_row(off):
    """A rich day inside the window buys `REBUY_N` units more wheat than B,
    and it buys them on turn 1 -- the one market row that carries a purchase."""
    macro = _macro()
    view = _view(day=12, money=60000)
    base = _wheat_buy(view, macro)
    P.REBUY_ON, P.REBUY_N = True, 40
    assert _wheat_buy(view, macro) == base + 40
    assert _wheat_buy_turns(view, macro) == [O.TURN_BUY]


def test_rebuy_is_windowed(off):
    macro = _macro()
    P.REBUY_ON, P.REBUY_N, P.REBUY_DAYS = True, 40, (10, 25)
    for day, extra in ((9, 0), (10, 40), (25, 40), (26, 0)):
        v = _view(day=day, money=60000)
        P.REBUY_ON = False
        base = _wheat_buy(v, macro)
        P.REBUY_ON = True
        assert _wheat_buy(v, macro) == base + extra, f"day {day}"


def test_rebuy_is_clipped_by_the_purse_and_the_shed(off):
    """The two engine clips still bind: a poor day buys what it can pay for
    (`buy_walk`) and a full shed buys nothing (`_inventory_orders`' room)."""
    macro = _macro()
    P.REBUY_ON, P.REBUY_N = True, 40
    poor = _wheat_buy(_view(day=12, money=300), macro)
    assert 0 < poor < 40, poor
    full = np.zeros(spec.N_ITEMS, np.int32)
    full[spec.I_MELON] = spec.SHED_CAPACITY
    assert _wheat_buy(_view(day=12, money=60000, shed=full), macro) == 0


def test_macro_mode_rebuy_buys_the_schedules_row(off, tmp_path):
    """Site 9: `buy_target[day][WHEAT]` is a floor on the day's BUY row."""
    macro = _macro()
    view = _view(day=12, money=60000)
    base = _wheat_buy(view, macro)
    rows = [[0] * spec.N_ITEMS for _ in range(ND)]
    rows[12][spec.I_WHEAT] = 60
    P.macro_load(_sched(tmp_path, buy=rows))
    P.MACRO_EXEC_ON, P.MACRO_MODE = True, "rebuy"
    assert _wheat_buy(view, macro) == max(base, 60)
    assert _wheat_buy_turns(view, macro) == [O.TURN_BUY]
    # a day the tape bought nothing on is the day B always planned
    assert _wheat_buy(_view(day=13, money=60000), macro) == \
        _wheat_buy_off(_view(day=13, money=60000), macro)


def _wheat_buy_off(view, macro):
    was = P.MACRO_EXEC_ON
    P.MACRO_EXEC_ON = False
    try:
        return _wheat_buy(view, macro)
    finally:
        P.MACRO_EXEC_ON = was


def test_an_old_schedule_decodes_to_an_empty_buy_row(off, tmp_path):
    """Schedules written before WHEAT-REBUY have no `buy_target` key; the
    decode pads them to zero, so `"rebuy"` on an old JSON is B."""
    macro = _macro()
    view = _view(day=12, money=60000)
    base = _wheat_buy(view, macro)
    P.macro_load(_sched(tmp_path, buy=None))
    assert P.MACRO_SCHEDULE["buy"].shape == (ND, spec.N_ITEMS)
    assert int(P.MACRO_SCHEDULE["buy"].sum()) == 0
    P.MACRO_EXEC_ON, P.MACRO_MODE = True, "rebuy"
    assert _wheat_buy(view, macro) == base
