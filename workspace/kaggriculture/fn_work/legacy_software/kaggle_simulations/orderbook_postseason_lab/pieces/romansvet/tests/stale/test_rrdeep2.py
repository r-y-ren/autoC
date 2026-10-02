"""[RRDEEP2] ruin-recreate restarts knob: default off (1 chain) byte-identical; RESTARTS=1 == default; RESTARTS=2 is a valid
(VERIFYed) plan on the deep search and never applies past RR_DEEP_LAST_DAY."""
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
    assert RV.RR_RESTARTS == 1 and P.ROUTE_VRP_RR_RESTARTS is None
    assert RV._rr_restarts(14) == 1


def test_restarts(monkeypatch):
    monkeypatch.setattr(RV, "SAFETY_S", 1e9)
    d, obs, plan = _day(14)
    for n, v in (("ROUTE_VRP_RR_ITERS", 150), ("ROUTE_VRP_RR_K", 10), ("ROUTE_VRP_RR_RESOLVE_ON", True)):
        monkeypatch.setattr(P, n, v)
    deep = RV.apply(plan, obs, d, {})
    monkeypatch.setattr(P, "ROUTE_VRP_RR_RESTARTS", 1)
    assert SAME(deep, RV.apply(plan, obs, d, {}))                        # 1 restart == the single seed-0 chain
    monkeypatch.setattr(P, "ROUTE_VRP_RR_RESTARTS", 2)
    assert RV._rr_restarts(d) == (2 if RV.jit_live() else 1)
    r2 = RV.apply(plan, obs, d, {})
    assert RV.verify(plan, r2, obs, d)
    monkeypatch.setattr(P, "ROUTE_VRP_RR_DEEP_LAST_DAY", d - 1)
    assert RV._rr_restarts(d) == 1                                       # past the deep cut: shipped single chain
