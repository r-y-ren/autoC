"""[ROUTEFILL1] ROUTE_FILL_MODE: default "ii" is byte-exact ROUTEOPT1 (digest of the routeopt1 branch's
route_vrp.apply over tests/data/route_vrp_days.pkl); i_fill plants into the solved routes with every planner task
kept and no hire removed; hybrid never removes more hires than mode ii; ii_fill keeps mode ii's drops."""
import collections
import hashlib
import pickle
from pathlib import Path

import _pin  # noqa: F401
import numpy as np
from kagg3.core import plan as P
from kagg3.core import ops as O
from kagg3.agent import route_vrp as RV

import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def _salepin_off(monkeypatch):
    """ROUTEFILL1 references predate SALEPIN1: run with FIX_FROZEN/VERIFY off (= res940_vrp routing)."""
    monkeypatch.setattr(P, "ROUTE_VRP_FIX_FROZEN", False)
    monkeypatch.setattr(P, "ROUTE_VRP_VERIFY", False)
    monkeypatch.setattr(P, "ROUTE_VRP_NEEDS_FIX_ON", False)   # VRPFALLBACK1 off (res940_vrp2 and earlier)


DAYS = pickle.load(open(Path(__file__).parent / "data/route_vrp_days.pkl", "rb"))
REF_MD5 = "1f849ca4dbaab2af5503d4184a1473ab"   # routeopt1 @ c2500ca4, same 4 days


def _with(mode, fn):
    old = P.ROUTE_FILL_MODE
    P.ROUTE_FILL_MODE = mode
    try:
        return fn()
    finally:
        P.ROUTE_FILL_MODE = old


def test_default_ii_parity():
    assert P.ROUTE_FILL_MODE == "ii"
    h = hashlib.md5()
    for d, obs, plan in DAYS:
        for x in RV.apply(plan, obs, d, None, {}):
            h.update(x.tobytes())
    assert h.hexdigest() == REF_MD5


def _ops(plan):
    c = collections.Counter()
    for u, lst in RV.parse_day(RV.plan_hours(plan, 23), 23)[2].items():
        for h, p, a in lst:
            if a[0] not in ("PICKUP", "DROP", "PLACE"):
                c[(p, a)] += 1
    return c


def test_i_fill_one_board_count():
    d, obs, plan = [x for x in DAYS if x[0] == 14][0]
    st = collections.Counter(); led = {}
    new = _with("i_fill", lambda: RV.apply(plan, obs, d, st, led))
    assert st["fills"] == 1 and st["dropped"] == 0          # this board's d14: 1 free tile admitted
    assert len(led["ledger"]) == 1
    extra = _ops(new) - _ops(plan)
    assert _ops(plan) - _ops(new) == collections.Counter()  # every planner task kept
    assert sum(v for (p, a), v in extra.items() if a[0] == "PLANT") == 1
    assert sum(v for (p, a), v in extra.items() if a[0] == "WATER") == 1
    hires = lambda p: int((p[3] == O.MO_HIRE).sum())
    assert hires(new) == hires(plan)
    st2 = collections.Counter()
    _with("hybrid", lambda: RV.apply(plan, obs, d, st2, {}))
    st3 = collections.Counter()
    RV.apply(plan, obs, d, st3, {})
    assert st2["fills"] == 1 and st2["dropped"] <= st3["dropped"]


def test_ii_fill_keeps_mode_ii_drops():
    d, obs, plan = [x for x in DAYS if x[0] == 14][0]
    st_ii = collections.Counter(); st_f = collections.Counter()
    RV.apply(plan, obs, d, st_ii, {})
    new = _with("ii_fill", lambda: RV.apply(plan, obs, d, st_f, {}))
    assert st_f["dropped"] == st_ii["dropped"] >= 1
    assert _ops(plan) - _ops(new) == collections.Counter()  # every planner task kept


def test_fill_survives_verify(monkeypatch):
    """[TOMATOFILL1] with ROUTE_VRP_VERIFY on, a committed fill's own DIG/PLANT/WATER must not fail VERIFY
    (before the fix every fill day fell back to the planner's plan); TOMATO is a supported fill crop."""
    monkeypatch.setattr(P, "ROUTE_VRP_VERIFY", True)
    d, obs, plan = [x for x in DAYS if x[0] == 14][0]
    for crop in ("CARROT", "TOMATO"):
        monkeypatch.setattr(P, "ROUTE_FILL_CROP", crop)
        st = collections.Counter(); led = {}
        new = _with("i_fill", lambda: RV.apply(plan, obs, d, st, led))
        assert st["verify_fail"] == 0 and st["fills"] == 1, (crop, st)
        assert sum(v for (p, a), v in (_ops(new) - _ops(plan)).items() if a == ("PLANT", crop)) == 1
