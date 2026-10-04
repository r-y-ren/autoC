"""[VRPDEADLINE1] one perf_counter deadline for route_vrp.apply: complete solutions are checkpointed; a timeout
returns the last checkpoint VERIFY accepts (never more hires than the insertion solution), and the planner's own
table only when no checkpoint exists yet. Parity with master on 600 recorded dawns: S/vrpdeadline1/parity.py."""
import collections
import pickle
from pathlib import Path

import _pin  # noqa: F401
import numpy as np
import pytest
from kagg3.core import plan as P
from kagg3.core import ops as O
from kagg3.agent import route_vrp as RV

DAYS = pickle.load(open(Path(__file__).parent / "data/route_vrp_days.pkl", "rb"))


def _hires(p):
    return int((p[3] == O.MO_HIRE).sum())


def _day14():
    return [x for x in DAYS if x[0] == 14][0]


class _Clock:
    """fake clock: 0 until expire(), then just past the search deadline (inside SAFETY_S, restore allowed)."""
    def __init__(self):
        self.t = 0.0; self.calls = 0; self.at = None

    def __call__(self):
        self.calls += 1
        if self.at is not None and self.calls > self.at:
            self.expire()
        return self.t

    def expire(self):
        self.t = RV.SAFETY_S - RV.RESERVE_S + 0.01


@pytest.fixture
def clock(monkeypatch):
    c = _Clock()
    monkeypatch.setattr(RV, "_CLOCK", c)
    return c


def test_no_deadline_is_master(monkeypatch):
    """no deadline fired: identical to a run with an infinite budget (the master output; 600-dawn proof in S/)."""
    monkeypatch.setattr(RV, "SAFETY_S", 1e9)
    for d, obs, plan in DAYS:
        a = RV.apply(plan, obs, d)
        monkeypatch.setattr(RV, "SAFETY_S", 1e6)
        b = RV.apply(plan, obs, d)
        monkeypatch.setattr(RV, "SAFETY_S", 1e9)
        assert all(np.array_equal(x, y) for x, y in zip(a, b))


def test_expire_mid_improve_returns_checkpoint(clock, monkeypatch):
    d, obs, plan = _day14()
    full = RV.apply(plan, obs, d)          # fake clock never expires: the complete solve
    seen = {"depth": 0, "ck": [], "fired": False}
    imp0, ck0 = RV.Solver.improve, RV.Solver._ckpt

    def improve(self, *a, **k):
        seen["depth"] += 1
        try:
            return imp0(self, *a, **k)
        finally:
            seen["depth"] -= 1

    def ckpt(self, routes):
        n = len(self.ckpts or [])
        ck0(self, routes)
        if self.ckpts is not None and len(self.ckpts) > n:
            seen["ck"].append((seen["depth"], len(self.ckpts[-1]["dropped"])))
            if seen["depth"] and not seen["fired"]:
                seen["fired"] = True; clock.expire()   # first improve pass done: the next check times out
    monkeypatch.setattr(RV.Solver, "improve", improve)
    monkeypatch.setattr(RV.Solver, "_ckpt", ckpt)
    st = collections.Counter()
    out = RV.apply(plan, obs, d, st)
    assert seen["fired"] and st["timeout"] == 1 and st["ckpt"] == 1
    assert seen["ck"][0] == (0, 0)                        # the insertion solution (same crew) was checkpointed first
    assert not all(np.array_equal(x, y) for x, y in zip(out, plan))   # not the planner table
    assert RV.verify(plan, out, obs, d)
    assert _hires(out) <= _hires(plan)                    # <= the insertion solution's crew (= planner's)
    assert _hires(full) <= _hires(out)
    m0, m1 = plan[3].copy(), out[3].copy()
    m0[m0 == O.MO_HIRE] = 0; m1[m1 == O.MO_HIRE] = 0
    assert np.array_equal(m0, m1)


def test_expire_in_crew_drop_keeps_earlier_drop(clock, monkeypatch):
    """a timeout after a successful crew reduction keeps that reduction (master discarded the whole day)."""
    d, obs, plan = _day14()
    full = RV.apply(plan, obs, d)
    assert _hires(full) <= _hires(plan) - 1
    ck0 = RV.Solver._ckpt

    def ckpt(self, routes):
        ck0(self, routes)
        if self.ckpts and len(self.ckpts[-1]["dropped"]) >= 1:
            clock.expire()
    monkeypatch.setattr(RV.Solver, "_ckpt", ckpt)
    st = collections.Counter()
    out = RV.apply(plan, obs, d, st)
    assert st["timeout"] == 1 and st["ckpt"] == 1 and st["dropped"] >= 1
    assert _hires(out) <= _hires(plan) - 1 and RV.verify(plan, out, obs, d)


def test_expire_before_first_checkpoint_returns_planner(clock):
    d, obs, plan = _day14()
    clock.at = 1        # apply() reads t0, every later read is past the deadline
    st = collections.Counter()
    out = RV.apply(plan, obs, d, st)
    assert st["timeout"] == 1 and st["ckpt"] == 0
    assert all(np.array_equal(x, y) and x.dtype == y.dtype for x, y in zip(out, plan))


def test_restore_respects_total_budget(clock, monkeypatch):
    """past SAFETY_S no checkpoint is even tried: the planner's table."""
    d, obs, plan = _day14()
    ck0 = RV.Solver._ckpt

    def ckpt(self, routes):
        ck0(self, routes)
        if self.ckpts:
            clock.t = RV.SAFETY_S + 1.0
    monkeypatch.setattr(RV.Solver, "_ckpt", ckpt)
    st = collections.Counter()
    out = RV.apply(plan, obs, d, st)
    assert st["timeout"] == 1 and st["ckpt"] == 0
    assert all(np.array_equal(x, y) for x, y in zip(out, plan))
