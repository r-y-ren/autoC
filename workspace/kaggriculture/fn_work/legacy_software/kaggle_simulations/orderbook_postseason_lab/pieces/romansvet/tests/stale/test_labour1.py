"""LABOUR1 switches [LABOUR_LEAD, EMPTY_ROUTE_UNHIRE_ON, LATE_ASK_FLOOR]: the planner's labour model priced
at the VRP router's turns, the empty-route HIRE bug, and the d20-27 short-crop ask floor (IDLE1 / EMPTY1).

Claims: all OFF by default and byte-identical to master on three days; LABOUR_LEAD overrides EST_LEAD in the
hire scan and the admit stage; LATE_ASK_FLOOR adds only wheat/carrot plantings, only on d20-27; the unhire drops
the last-hired hand when some kept hand has an empty route (moving the last hand's route onto it) and keeps the
solution when the spawn check fails.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import types

import numpy as np
import pytest

from kagg3 import spec
from kagg3.agent import route_vrp as RV
from kagg3.core import brain as B
from kagg3.core import plan as P

from test_budget_order import _macro
from test_endroute import _digest
from test_q4_prog import _board

DAYS = ((5, 2, 3000, 0), (12, 3, 9000, 0), (15, 4, 9000, 5))
MASTER = "142b226da349e5ab"     # master digest (tests/test_q4_relay.py, tests/test_wheatmix.py)


def _plan(view, pt=(2, 1, 0, 0, 0)):
    return tuple(np.asarray(a) for a in P.build_day(np, view, _macro(plant_target=np.array(pt, np.int32))))


def test_off_by_default():
    assert P.LABOUR_LEAD is None and P.LATE_ASK_FLOOR is None and P.EMPTY_ROUTE_UNHIRE_ON is False
    assert P.LATE_ASK_DAYS == (20, 27) and P._est_lead0() == P.EST_LEAD == 5
    for s in ("LABOUR_LEAD", "EMPTY_ROUTE_UNHIRE_ON", "LATE_ASK_FLOOR"):
        assert s not in P.SWITCH_GENES


@pytest.mark.parametrize("d,q,m,w", DAYS)
def test_off_byte_identical(d, q, m, w):
    assert _digest(_plan(_board(d, q, money=m, q4_wheat=w))) == MASTER


def test_labour_lead_override(monkeypatch):
    monkeypatch.setattr(P, "LABOUR_LEAD", 5)
    assert _digest(_plan(_board(12, 3))) == MASTER                  # override == EST_LEAD: same plan
    monkeypatch.setattr(P, "LABOUR_LEAD", 1)
    assert P._est_lead0() == 1


def _view(day, n_free_tiles=20):
    return types.SimpleNamespace(day=np.int32(day), n_free=n_free_tiles)


def test_late_ask_floor_short_crops_only(monkeypatch):
    monkeypatch.setattr(B, "n_free_slots", lambda xp, obs, land=None: np.int32(obs.n_free))
    monkeypatch.setattr(P, "LATE_ASK_FLOOR", 0.8)
    m = _macro(plant_target=np.array([2, 1, 3, 0, 0], np.int32))
    out = P._late_ask_floor(np, _view(22), m)
    tot = int(np.sum(m.plant_target)) + int(np.sum(m.animal_want))
    add = np.asarray(out.plant_target) - np.asarray(m.plant_target)
    assert int(add.sum()) == max(16 - tot, 0) and add[2:].tolist() == [0, 0, 0]
    assert add[spec.I_CARROT] == (int(add.sum()) * 1) // 3                     # split by the day's own 2:1 ask
    for d in (19, 28):                                                          # outside d20-27: untouched
        assert np.asarray(P._late_ask_floor(np, _view(d), m).plant_target).tolist() == [2, 1, 3, 0, 0]
    m0 = _macro(plant_target=np.array([0, 0, 1, 0, 0], np.int32))              # no short ask: all to wheat
    add0 = np.asarray(P._late_ask_floor(np, _view(24), m0).plant_target) - np.asarray(m0.plant_target)
    assert add0[spec.I_WHEAT] == int(add0.sum()) > 0 and add0[1:].tolist() == [0, 0, 0, 0]


class _FakeS:
    def __init__(self, ok=True):
        self.B = dict(frozen=(), hire_h={0: -1, 1: 0, 2: 0, 3: 1}, sp={0: (4, 4), 1: (4, 5), 2: (5, 4), 3: (5, 5)})
        self.ctx = None; self.cache = {}; self.ok = ok

    def fix_spawns(self, routes, units):
        return routes, self.ok

    def ev(self, u, r):
        return (10, 1, 0)


def test_unhire_moves_last_route_onto_empty_hand():
    routes = {0: [0], 1: [1], 2: [], 3: [2, 3]}
    r, u, dr = RV._unhire_empty(_FakeS(), routes, [0, 1, 2, 3], [], {})
    assert u == [0, 1, 2] and dr == [3] and r[2] == [2, 3] and r[1] == [1]


def test_unhire_last_hand_empty_and_failure_keeps():
    r, u, dr = RV._unhire_empty(_FakeS(), {0: [0], 1: [1], 2: [], 3: []}, [0, 1, 2, 3], [4], {})
    assert u == [0, 1] and dr == [4, 3, 2]
    routes = {0: [0], 1: [], 2: [5], 3: [2]}
    r, u, dr = RV._unhire_empty(_FakeS(ok=False), routes, [0, 1, 2, 3], [], {})
    assert u == [0, 1, 2, 3] and dr == [] and r is routes
