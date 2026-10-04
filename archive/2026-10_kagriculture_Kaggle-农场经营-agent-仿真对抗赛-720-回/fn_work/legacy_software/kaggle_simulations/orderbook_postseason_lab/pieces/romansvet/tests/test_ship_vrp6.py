"""SHIP_VRP6 (res940_vrp6) = res940_vrp5 + EMPTY_ROUTE_UNHIRE_ON [LABOUR1/SHIPUA1]: defaults + the unhire's own unit cases
(copied from LABOUR1 tests/test_labour1.py, whose other cases need LABOUR1-only planner switches not in this tree)."""
import _pin  # noqa: F401
from kagg3.core import plan as P
from kagg3.agent import route_vrp as RV


def test_ship_vrp6_defaults():
    assert P.EMPTY_ROUTE_UNHIRE_ON is True and P.ROUTE_VRP_REPAIR_ON is True
    assert (RV.REPAIR_LAST_DAY, RV.REPAIR_MS, RV.REPAIR_EJECT_K) == (20, 100, 4)


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
    st = {}
    r, u, dr = RV._unhire_empty(_FakeS(), routes, [0, 1, 2, 3], [], st)
    assert u == [0, 1, 2] and dr == [3] and r[2] == [2, 3] and r[1] == [1] and st["unhired"] == 1


def test_unhire_last_hand_empty_and_failure_keeps():
    r, u, dr = RV._unhire_empty(_FakeS(), {0: [0], 1: [1], 2: [], 3: []}, [0, 1, 2, 3], [4], {})
    assert u == [0, 1] and dr == [4, 3, 2]
    routes = {0: [0], 1: [], 2: [5], 3: [2]}
    r, u, dr = RV._unhire_empty(_FakeS(ok=False), routes, [0, 1, 2, 3], [], {})
    assert u == [0, 1, 2, 3] and dr == [] and r is routes
