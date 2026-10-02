"""[ROUTEOPT2] ROUTE_VRP_OPT_ON (optional tail tasks) / ROUTE_VRP_FIX_ON (unsolved-day retry): OPT default OFF,
FIX default ON since SHIP_VRP26 (bb4f077b, sub 56707958); the `sw` fixture starts both OFF (mode ii byte-exact); ON, every mandatory (non-tail) op is kept per tile, hires only removed, and the retry
recovers the recorded unsolved days."""
import collections
import pickle
from pathlib import Path

import _pin  # noqa: F401
import numpy as np
import pytest
from kagg3.core import plan as P
from kagg3.core import ops as O
from kagg3.agent import route_vrp as RV

DAYS = pickle.load(open(Path(__file__).parent / "data/route_vrp_opt_days.pkl", "rb"))   # d14, d23 (opt), d25, d16 (retry)
M0 = P.ROUTE_VRP_OPT_MARK


@pytest.fixture
def sw(monkeypatch):
    monkeypatch.setattr(RV, "SAFETY_S", 1e9)   # [VRPDEADLINE1] load-independent (the 0.7 s break fired on a loaded box)
    keep = (P.ROUTE_VRP_OPT_ON, P.ROUTE_VRP_FIX_ON, P.ROUTE_VRP_NEEDS_FIX_ON, P.ROUTE_VRP_REPAIR_ON,
            P.ROUTE_VRP_RR_ITERS, P.ROUTE_VRP_RR_K, P.ROUTE_VRP_RR_RESOLVE_ON, P.ROUTE_VRP_MISS_ON)
    P.ROUTE_VRP_OPT_ON = P.ROUTE_VRP_FIX_ON = False   # ROUTEOPT2 reference state (FIX ships ON since SHIP_VRP26; tests switch it on)
    P.ROUTE_VRP_NEEDS_FIX_ON = False   # ROUTEOPT2 references predate VRPFALLBACK1
    P.ROUTE_VRP_REPAIR_ON = False   # ... and VRPREPAIR1 (SHIP_VRP5 default ON)
    P.ROUTE_VRP_RR_ITERS = P.ROUTE_VRP_RR_K = P.ROUTE_VRP_RR_RESOLVE_ON = None   # ... and the deep RR knobs (SHIP_VRP8_JIT 150/10/ON solve the recorded unsolved days)
    P.ROUTE_VRP_MISS_ON = False   # ... and VRPMISS1 (SHIP_VRP27_VM_M3 default ON: M3 solves a recorded unsolved day, SHIPSYNC12)
    yield
    (P.ROUTE_VRP_OPT_ON, P.ROUTE_VRP_FIX_ON, P.ROUTE_VRP_NEEDS_FIX_ON, P.ROUTE_VRP_REPAIR_ON,
     P.ROUTE_VRP_RR_ITERS, P.ROUTE_VRP_RR_K, P.ROUTE_VRP_RR_RESOLVE_ON, P.ROUTE_VRP_MISS_ON) = keep


def _ops(plan, mand_only=False):
    out = collections.Counter()
    hrs = RV.plan_hours(plan, 23)
    for u, lst in RV.parse_day(hrs, 23)[2].items():
        for h, p, a in lst:
            if a[0] in ("PICKUP", "DROP", "PLACE"):
                continue
            if mand_only and M0 + 1 <= int(plan[1][u, h]) <= M0 + 3:
                continue
            out[(p, a)] += 1
    return out


def _hires(p):
    return int((p[3] == O.MO_HIRE).sum())


def test_defaults_shipped():
    """The shipped defaults (vrp27_vm_m3, sub 56718602, config ce0df430; SHIPSYNC12): OPT OFF, FIX ON (since vrp26_hyb_eve_vrp,
    sub 56707958, bb4f077b) and the VRPMISS1 unsolved-day retry M3 ON."""
    assert P.ROUTE_VRP_OPT_ON is False and P.ROUTE_VRP_FIX_ON is True
    assert P.ROUTE_VRP_MISS_ON is True and P.ROUTE_VRP_MISS_CELL == "M3" and P.ROUTE_VRP_MISS_EXTRA_S == 0.15


def test_off_equals_marks_ignored(sw):
    """OFF: the marks in unit_a are not read -> same rewrite as a plan with the marks stripped."""
    for d, obs, plan in DAYS:
        clean = tuple(np.array(x) for x in plan)
        m = (clean[1] > M0) & (clean[1] <= M0 + 3); clean[1][m] = 0
        a = RV.apply(plan, obs, d); b = RV.apply(clean, obs, d)
        for x, y in zip(a[:1] + a[2:], b[:1] + b[2:]):
            assert np.array_equal(x, y)


def test_opt_keeps_mandatory_and_drops_more(sw):
    P.ROUTE_VRP_OPT_ON = True
    for d, obs, plan in DAYS[:2]:
        st0 = collections.Counter(); st1 = collections.Counter()
        RV.OPT_USE = False
        a = RV.apply(plan, obs, d, st0)
        RV.OPT_USE = True
        b = RV.apply(plan, obs, d, st1)
        assert st1["dropped"] > st0["dropped"]
        assert _hires(b) < _hires(a) <= _hires(plan)
        got = _ops(b); want = _ops(plan, mand_only=True)
        assert all(got[k] >= v for k, v in want.items()), d


def test_fix_recovers(sw):
    P.ROUTE_VRP_OPT_ON = True
    for d, obs, plan in DAYS[2:]:
        st = collections.Counter(); RV.apply(plan, obs, d, st)
        assert st["miss"] == 1
        P.ROUTE_VRP_FIX_ON = True
        st = collections.Counter(); b = RV.apply(plan, obs, d, st)
        P.ROUTE_VRP_FIX_ON = False
        assert st["miss"] == 0 and st["recovered"] == 1 and st["dropped"] >= 2
        assert _ops(b) == _ops(plan)   # every planner task kept (frozen units keep their own rows)
