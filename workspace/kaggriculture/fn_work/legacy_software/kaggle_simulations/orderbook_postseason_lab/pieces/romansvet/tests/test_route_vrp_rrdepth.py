"""[RRDEPTH1] VRP search depth knobs: defaults byte-identical, (150, 10, re-solve ON) changes the d14 routes."""
import pickle
from pathlib import Path
import numpy as np
import _pin  # noqa: F401
from kagg3.core import plan as P
from kagg3.agent import route_vrp as RV

DAYS = pickle.load(open(Path(__file__).parent / "data/route_vrp_days.pkl", "rb"))
SAME = lambda a, b: all(np.array_equal(x, y) for x, y in zip(a, b))


def _day(d):
    return [x for x in DAYS if x[0] == d][0]


def test_defaults():
    assert (RV.RR_ITERS, RV.RR_K, RV.RR_RESOLVE_ON, RV.RR_DEEP_LAST_DAY) == (30, 8, False, 29)
    assert (P.ROUTE_VRP_RR_ITERS, P.ROUTE_VRP_RR_K, P.ROUTE_VRP_RR_RESOLVE_ON, P.ROUTE_VRP_RR_DEEP_LAST_DAY) == (None,) * 4


def test_defaults_byte_identical_and_deep_changes_d14(monkeypatch):
    monkeypatch.setattr(RV, "SAFETY_S", 1e9)
    d, obs, plan = _day(14)
    base = RV.apply(plan, obs, d, {})
    for n, v in (("ROUTE_VRP_RR_ITERS", 30), ("ROUTE_VRP_RR_K", 8), ("ROUTE_VRP_RR_RESOLVE_ON", False),
                 ("ROUTE_VRP_RR_DEEP_LAST_DAY", 29)):
        monkeypatch.setattr(P, n, v)
    assert SAME(base, RV.apply(plan, obs, d, {}))                        # explicit shipped values == None defaults
    monkeypatch.setattr(P, "ROUTE_VRP_RR_ITERS", 150); monkeypatch.setattr(P, "ROUTE_VRP_RR_K", 10)
    monkeypatch.setattr(P, "ROUTE_VRP_RR_RESOLVE_ON", True)
    st = {}; deep = RV.apply(plan, obs, d, st)
    assert not SAME(base, deep) and RV.verify(plan, deep, obs, d)
    monkeypatch.setattr(P, "ROUTE_VRP_RR_DEEP_LAST_DAY", d - 1)           # cut below the day == shipped search
    assert SAME(base, RV.apply(plan, obs, d, {}))


def test_rr_wall_switch(monkeypatch):
    """[RRSPEED1] ROUTE_VRP_RR_WALL_S: None default; an unbounded wall == the plain deep search; wall 0 turns the
    re-solve loop off (and never cuts RR below the shipped 30), so (30, 8, ON) at wall 0 == shipped."""
    assert RV.RR_WALL_S is None and P.ROUTE_VRP_RR_WALL_S is None
    monkeypatch.setattr(RV, "SAFETY_S", 1e9)
    d, obs, plan = _day(14)
    base = RV.apply(plan, obs, d, {})
    monkeypatch.setattr(P, "ROUTE_VRP_RR_ITERS", 150); monkeypatch.setattr(P, "ROUTE_VRP_RR_K", 10)
    monkeypatch.setattr(P, "ROUTE_VRP_RR_RESOLVE_ON", True)
    deep = RV.apply(plan, obs, d, {})
    monkeypatch.setattr(P, "ROUTE_VRP_RR_WALL_S", 1e9)
    assert SAME(deep, RV.apply(plan, obs, d, {}))
    monkeypatch.setattr(P, "ROUTE_VRP_RR_ITERS", 30); monkeypatch.setattr(P, "ROUTE_VRP_RR_K", 8)
    monkeypatch.setattr(P, "ROUTE_VRP_RR_WALL_S", 0.0)
    assert SAME(base, RV.apply(plan, obs, d, {}))
