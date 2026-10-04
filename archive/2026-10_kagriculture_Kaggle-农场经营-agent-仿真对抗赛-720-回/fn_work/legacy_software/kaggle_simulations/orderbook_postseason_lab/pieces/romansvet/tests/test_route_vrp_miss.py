"""[VRPMISS1] ROUTE_VRP_MISS_ON: a route_vrp day still unsolved after the search + ROUTEOPT2 retry gets one more solve.
Data: three live vrp26 miss dawns (S/vrpmiss1 ledger): d14 (solved by the construct repair, M1), d11 (solved by the
spawn-robust re-solve, M2), d20 (unsolved by every cell: the planner's rows play)."""
import pickle
from pathlib import Path

import _pin  # noqa: F401
import numpy as np
import pytest
from kagg3.core import plan as P
from kagg3.core import ops as O
from kagg3.agent import route_vrp as RV

DAYS = pickle.load(open(Path(__file__).parent / "data/route_vrp_miss_days.pkl", "rb"))   # (day, obs, plan, tag)


@pytest.fixture
def sw(monkeypatch):
    monkeypatch.setattr(RV, "SAFETY_S", 1e9)   # load-independent
    keep = (P.ROUTE_VRP_MISS_ON, P.ROUTE_VRP_MISS_CELL, P.ROUTE_VRP_MISS_EXTRA_S)
    yield
    P.ROUTE_VRP_MISS_ON, P.ROUTE_VRP_MISS_CELL, P.ROUTE_VRP_MISS_EXTRA_S = keep


def _run(d, obs, plan):
    st = {}
    out = RV.apply(plan, obs, d, st, {"ledger": []})
    return out, st


def _same(a, b):
    return all(np.array_equal(x, y) for x, y in zip(a, b))


def test_off_is_the_fallback(sw):
    P.ROUTE_VRP_MISS_ON = False
    for d, obs, plan, tag in DAYS:
        out, st = _run(d, obs, plan)
        assert st.get("miss") == 1 and "days" not in st, tag
        assert _same(out, plan), tag


@pytest.mark.parametrize("cell,solved", [("M1", {0}), ("M2", {1}), ("M3", {0, 1}), ("M4", {0, 1})])
def test_cells_solve(sw, cell, solved):
    P.ROUTE_VRP_MISS_ON = True; P.ROUTE_VRP_MISS_CELL = cell
    for i, (d, obs, plan, tag) in enumerate(DAYS):
        out, st = _run(d, obs, plan)
        if i in solved:
            assert "days" in st and not st.get("miss"), (cell, tag)
            assert not _same(out, plan), (cell, tag)
            assert int((out[3] == O.MO_HIRE).sum()) <= int((plan[3] == O.MO_HIRE).sum())
            assert RV.verify(plan, out, obs, d)
        else:
            assert st.get("miss") == 1 and _same(out, plan), (cell, tag)
