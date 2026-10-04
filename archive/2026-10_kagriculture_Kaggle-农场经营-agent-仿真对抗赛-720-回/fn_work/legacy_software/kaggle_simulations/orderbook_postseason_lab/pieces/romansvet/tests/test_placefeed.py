"""PLACEFEED1 [SWITCH `PLACEFEED_ON`, default OFF]: a sheep placed today is fed and cared tonight.

The engine pays an animal's first production `1 + pending_care_bonus`, and pending grows only on fed+cared nights
(kaggriculture.py L826-830); FEED/CARE act on any tile holding an animal, the one placed this turn included (L505-530).
OFF the planner builds the feed/care list from dawn's animal tiles, so today's placements are never on it (CREWAUDIT1:
17.5/17.5 placements a game skip the night). ON the placement chain is PLACE -> FEED -> CARE on the same tile, and the
wheat for it is on the turn-1 BUY row when the shed has none."""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np
from test_budget_order import _macro
from test_mixed_herd import _placed, _view, _want

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P


def _unit_seq(plan, u):
    return [int(x) for x in plan[0][u]]


def test_placefeed_feeds_and_cares_same_day_sheep(monkeypatch):
    monkeypatch.setattr(P, "PLACEFEED_ON", False); monkeypatch.setattr(P, "PF_PUMPSAFE_ON", False)   # SHIP_VRP12_PFS: shipped default is ON
    view = _view(money=10_000, pastures=2, day=0, full=True)
    macro = _macro(animal_want=_want(s=2))
    off = P.build_day(np, view, macro)
    monkeypatch.setattr(P, "PLACEFEED_ON", True)
    on = P.build_day(np, view, macro)
    assert _placed(off).get(spec.I_SHEEP, 0) == 2 and _placed(on).get(spec.I_SHEEP, 0) == 2
    assert int((off[0] == O.OP_FEED).sum()) == 0 and int((off[0] == O.OP_CARE).sum()) == 0
    assert int((on[0] == O.OP_FEED).sum()) == 2 and int((on[0] == O.OP_CARE).sum()) == 2
    # every FEED/CARE comes after that unit's sheep PLACE (same chain), and the wheat is bought on the turn-1 row
    for u in range(on[0].shape[0]):
        seq = _unit_seq(on, u)
        places = [i for i, x in enumerate(seq) if x == O.OP_PLACE and int(on[1][u][i]) == spec.I_SHEEP]
        for i, x in enumerate(seq):
            if x in (O.OP_FEED, O.OP_CARE):
                assert places and i > min(places), (u, seq)
    op, arg, qty = on[3:6]
    wheat = sum(int(qty[O.TURN_BUY, s]) for s in range(spec.MAX_MARKET_ORDERS)
                if int(op[O.TURN_BUY, s]) == O.MO_BUY_PRODUCT and int(arg[O.TURN_BUY, s]) == spec.I_WHEAT)
    assert wheat >= 2, wheat
    # and it is picked up: the unit carrying the sheep also carries wheat
    picks = on[1][on[0] == O.OP_PICKUP]
    assert spec.I_WHEAT in set(int(i) for i in picks)


def _pump_units(plan):
    """Units of wheat the turn-1 row buys (the OPEN_PUMP leg is a BUY_PRODUCT WHEAT of OPEN_PUMP_UNITS there)."""
    op, arg, qty = plan[3:6]
    return sum(int(qty[O.TURN_BUY, s]) for s in range(spec.MAX_MARKET_ORDERS)
               if int(op[O.TURN_BUY, s]) == O.MO_BUY_PRODUCT and int(arg[O.TURN_BUY, s]) == spec.I_WHEAT)


def _pump_row(plan):
    """(op, arg, qty) of every live order on the pump's two rows (hour 0 and the turn-1 sell-back)."""
    op, arg, qty = plan[3:6]
    return [(t, int(op[t, s]), int(arg[t, s]), int(qty[t, s])) for t in (O.TURN_HIRE, O.TURN_BUY)
            for s in range(spec.MAX_MARKET_ORDERS) if int(op[t, s]) != O.MO_NONE]


def test_pumpsafe_keeps_the_opening_pump(monkeypatch):
    """PLACEFEED3: day 0 with the pump armed. PLACEFEED1 alone buys the placement wheat, `wheat_buy == 0` fails
    and the 53/48 pump is gone; `PF_PUMPSAFE_ON` keeps the OFF pump rows exactly and feeds from OPEN_PUMP_KEEP."""
    monkeypatch.setattr(P, "PLACEFEED_ON", False); monkeypatch.setattr(P, "PF_PUMPSAFE_ON", False)   # SHIP_VRP12_PFS: shipped default is ON
    monkeypatch.setattr(P, "OPEN_PUMP_ON", True)
    view = _view(money=10_000, pastures=2, day=0, full=True)
    macro = _macro(animal_want=_want(s=2))
    off = P.build_day(np, view, macro)
    monkeypatch.setattr(P, "PLACEFEED_ON", True)
    pf1 = P.build_day(np, view, macro)
    monkeypatch.setattr(P, "PF_PUMPSAFE_ON", True)
    on = P.build_day(np, view, macro)
    pump = [r for r in _pump_row(off) if r[1] in (O.MO_BUY_PRODUCT, O.MO_SELL) and r[2] == spec.I_WHEAT]
    assert pump, _pump_row(off)                              # the fixture's day 0 pumps OFF
    assert [r for r in _pump_row(pf1) if r[1] in (O.MO_BUY_PRODUCT, O.MO_SELL) and r[2] == spec.I_WHEAT] != pump
    assert [r for r in _pump_row(on) if r[1] in (O.MO_BUY_PRODUCT, O.MO_SELL) and r[2] == spec.I_WHEAT] == pump
    assert int((on[0] == O.OP_FEED).sum()) == 2 and int((on[0] == O.OP_CARE).sum()) == 2
    assert int((off[0] == O.OP_FEED).sum()) == 0


def test_pumpsafe_is_inert_off_the_pump_day(monkeypatch):
    monkeypatch.setattr(P, "PLACEFEED_ON", False); monkeypatch.setattr(P, "PF_PUMPSAFE_ON", False)   # SHIP_VRP12_PFS: shipped default is ON
    view = _view(money=10_000, pastures=2, day=3, full=True)
    macro = _macro(animal_want=_want(s=2))
    monkeypatch.setattr(P, "PLACEFEED_ON", True)
    a = P.build_day(np, view, macro)
    monkeypatch.setattr(P, "PF_PUMPSAFE_ON", True)
    b = P.build_day(np, view, macro)
    assert all(np.array_equal(x, y) for x, y in zip(a, b))


def test_ship_vrp12_pfs_default_on():
    """SHIP_VRP12_PFS (PLACEFEED3 2026-09-27): res940_vrp12_pfs ships PLACEFEED_ON with PF_PUMPSAFE_ON, other knobs neutral."""
    assert P.PLACEFEED_ON is True and P.PF_PUMPSAFE_ON is True
    assert P.PF_NOBUY_ON is False and (P.PF_DAY_MIN, P.PF_DAY_MAX, P.PF_HERD_MAX) == (0, 99, 999)
