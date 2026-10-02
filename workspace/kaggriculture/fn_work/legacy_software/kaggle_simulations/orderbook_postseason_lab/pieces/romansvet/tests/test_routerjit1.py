"""[ROUTERJIT1] route_vrp compiled kernels (route_vrp_c.so via ctypes): the JIT path writes the SAME routes as the Python
path (every recorded fixture day, shipped and deep RR knobs, SAFETY_S 1e9), rv_eval == route_eval on random routes, and
the fallback rules (JIT off / library missing: deep knobs revert to the shipped (30, 8, off) search)."""
import pickle
import random
from pathlib import Path

import _pin  # noqa: F401
import numpy as np
import pytest
from kagg3.core import plan as P
from kagg3.agent import route_vrp as RV

DATA = Path(__file__).parent / "data"
FILES = ["route_vrp_days.pkl", "route_vrp_opt_days.pkl", "route_vrp_frozen_d17.pkl", "route_vrp_needs_d28.pkl"]


def _days():
    out = []
    for f in FILES:
        x = pickle.load(open(DATA / f, "rb"))
        x = x if isinstance(x, list) else [(x["day"], x["obs"], x["plan"])]
        out += [(t[0], t[1], t[2]) for t in x]
    return out


DAYS = _days()


@pytest.fixture
def clean(monkeypatch):
    monkeypatch.setattr(RV, "SAFETY_S", 1e9)
    monkeypatch.setattr(RV, "REPAIR_MS", 1e7)
    monkeypatch.setattr(RV, "DEEP_NEEDS_JIT", False)
    keep = (P.ROUTE_VRP_RR_ITERS, P.ROUTE_VRP_RR_K, P.ROUTE_VRP_RR_RESOLVE_ON, RV.JIT_ON)
    yield
    P.ROUTE_VRP_RR_ITERS, P.ROUTE_VRP_RR_K, P.ROUTE_VRP_RR_RESOLVE_ON, RV.JIT_ON = keep


def test_library_loads():
    assert RV._JL is not None, "route_vrp_c.so did not load (build: S/routerjit1/build.sh)"
    assert RV.JIT_ON is True and RV.DEEP_NEEDS_JIT is True


def _both(d, obs, plan):
    RV.JIT_ON = False; s1 = {}; a = RV.apply(plan, obs, d, s1)
    RV.JIT_ON = True; s2 = {}; b = RV.apply(plan, obs, d, s2)
    return a, b, s1, s2


@pytest.mark.parametrize("deep", [False, True])
def test_jit_equals_python(clean, deep):
    if deep:
        P.ROUTE_VRP_RR_ITERS, P.ROUTE_VRP_RR_K, P.ROUTE_VRP_RR_RESOLVE_ON = 150, 10, True
    n_changed = 0
    for d, obs, plan in DAYS:
        a, b, s1, s2 = _both(d, obs, plan)
        assert s1 == s2
        for x, y in zip(a, b):
            assert x.dtype == y.dtype and np.array_equal(x, y)
        n_changed += any(not np.array_equal(x, y) for x, y in zip(a, plan))
    assert n_changed >= 5   # the router rewrites most fixture days (the check is not vacuous)


def test_rv_eval_equals_route_eval(clean):
    rng = random.Random(7); n = 0
    for d, obs, plan in DAYS:
        last = 23 if d < 29 else 22
        B = RV.build(RV.plan_hours(plan, last), obs, d, last)
        S = RV.Solver(B)
        assert S._jctx() is not None
        m = len(S.stops)
        for u in B["units"]:
            for _ in range(40):
                r = rng.sample(range(m), rng.randint(0, min(m, 12)))
                py = RV.route_eval(r, B["sp"][u], B["start"][u], B["item_av"], B["end"], S.stops)
                S.cache = {}
                RV.JIT_ON = True
                assert S.ev(u, r) == py
                n += py is not None
    assert n > 50


def test_best_insert_equals_python(clean):
    rng = random.Random(11)
    for d, obs, plan in DAYS:
        last = 23 if d < 29 else 22
        B = RV.build(RV.plan_hours(plan, last), obs, d, last)
        S = RV.Solver(B); m = len(S.stops); units = list(S.units)
        for _ in range(30):
            idx = list(range(m)); rng.shuffle(idx); j = idx.pop()
            routes = {u: [] for u in units}
            for k in idx[:rng.randint(0, len(idx))]:
                routes[rng.choice(units)].append(k)
            RV.JIT_ON = False; S.cache = {}; a = S.best_insert(routes, j, units)
            RV.JIT_ON = True; S.cache = {}; b = S.best_insert(routes, j, units)
            assert a[1:] == b[1:] and (a[1] is None or a[0] == b[0])
            RV.JIT_ON = False; S.cache = {}; ra = S.construct(units)
            RV.JIT_ON = True; S.cache = {}; rb = S.construct(units)
            assert ra == rb and list(ra[0]) == list(rb[0])


def test_deep_knobs_need_jit(monkeypatch):
    monkeypatch.setattr(P, "ROUTE_VRP_RR_ITERS", 150)
    monkeypatch.setattr(P, "ROUTE_VRP_RR_K", 10)
    monkeypatch.setattr(P, "ROUTE_VRP_RR_RESOLVE_ON", True)
    assert RV._rr_knobs(20) == (150, 10, True)
    monkeypatch.setattr(RV, "JIT_ON", False)
    assert RV._rr_knobs(20) == RV._RR_SHIP
    monkeypatch.setattr(RV, "DEEP_NEEDS_JIT", False)
    assert RV._rr_knobs(20) == (150, 10, True)
    monkeypatch.setattr(RV, "JIT_ON", True)
    monkeypatch.setattr(RV, "_JL", None)
    monkeypatch.setattr(RV, "DEEP_NEEDS_JIT", True)
    assert RV._rr_knobs(20) == RV._RR_SHIP


def test_defaults_unchanged():
    """the switch strings own the deep knobs: route_vrp's own defaults stay the shipped search"""
    assert (RV.RR_ITERS, RV.RR_K, RV.RR_RESOLVE_ON) == (30, 8, False)


def test_plan_kill_switch(monkeypatch):
    """plan.ROUTE_VRP_JIT_ON False (switch string) turns the kernels off at the next apply(); default True is a no-op"""
    monkeypatch.setattr(RV, "SAFETY_S", 1e9)
    monkeypatch.setattr(RV, "JIT_ON", True)
    d, obs, plan = DAYS[0]
    RV.apply(plan, obs, d)
    assert RV.JIT_ON is True and P.ROUTE_VRP_JIT_ON is True
    monkeypatch.setattr(P, "ROUTE_VRP_JIT_ON", False)
    RV.apply(plan, obs, d)
    assert RV.JIT_ON is False and not RV.jit_live()
