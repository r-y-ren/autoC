"""[ROUTEOPT1] ROUTE_VRP_ON: default ON (shipped res940_vrp; + SALEPIN1 FIX_FROZEN/VERIFY ON = res940_vrp2), deterministic, every planner task kept per tile, d29 untouched,
hires only removed (never added)."""
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


@pytest.fixture(autouse=True)
def _no_break(monkeypatch):
    monkeypatch.setattr(RV, "SAFETY_S", 1e9)   # [VRPDEADLINE1] load-independent (the 0.7 s break fires on a loaded box)


def _tile_ops(plan, last):
    hrs = RV.plan_hours(plan, last)
    B = RV.build(hrs, DAYS[0][1], 0, last) if False else None
    out = collections.Counter()
    for u, lst in RV.parse_day(hrs, last)[2].items():
        for h, p, a in lst:
            if a[0] not in ("PICKUP", "DROP", "PLACE"):
                out[(p, a)] += 1
    return out


def test_default_on():
    assert P.ROUTE_VRP_ON is True and P.ROUTE_VRP_SHADOW_ON is True


def test_deterministic_and_complete():
    for d, obs, plan in DAYS:
        a = RV.apply(plan, obs, d)
        b = RV.apply(plan, obs, d)
        for x, y in zip(a, b):
            assert np.array_equal(x, y)
        last = 23 if d < 29 else 22
        if d == 29:
            for x, y in zip(a, plan):
                assert np.array_equal(x, y)
            continue
        assert _tile_ops(a, last) == _tile_ops(plan, last), d
        hires = lambda p: int((p[3] == O.MO_HIRE).sum())
        assert hires(a) <= hires(plan)
        # every other market row untouched
        m0, m1 = plan[3].copy(), a[3].copy()
        m0[m0 == O.MO_HIRE] = 0; m1[m1 == O.MO_HIRE] = 0
        assert np.array_equal(m0, m1)


def test_mode2_drops_on_busy_day():
    d, obs, plan = [x for x in DAYS if x[0] == 14][0]
    st = collections.Counter()
    RV.apply(plan, obs, d, st)
    assert st["days"] == 1 and st["dropped"] >= 1


import os  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402

import pytest  # noqa: E402


@pytest.mark.skipif(not os.environ.get("KAGG3_ROUTEVRP_SLOW"), reason="slow: 3 engine games (~5 min, 3 workers)")
def test_engine_off_parity_3_boards():
    """ROUTE_VRP_ON=False: faithful-59 boards 0-2 in the ENGINE == the master csv, byte for byte."""
    root = Path(__file__).resolve().parents[1]
    env = dict(os.environ, ENG_LIMIT="3", JAX_PLATFORMS="cpu", KAGG3_ROOT=str(root), KAGG3_SRC=str(root / "src"),
               PYTHONPATH=f"{root / 'src'}:{root / 'scripts'}")
    subprocess.run([sys.executable, str(root / "S/routeopt1/eng.py"), "off3", "ROUTE_VRP_ON=False",
                    "/mnt/e/_work/kaggriculture3/S/actionrl/flow257_ppo_selfplay/head_940.npz", "--workers", "3"],
                   env=env, check=True, timeout=3000)
    got = [l.split(",")[4:6] for l in open(root / "S/routeopt1/eng_off3.csv").read().split()[1:]]
    assert got == [["101474", "103316"], ["124205", "133648"], ["100015", "106948"]]


def test_salepin1_subswitches_defaults():
    """SHIP_VRP2: FIX_FROZEN + VERIFY promoted ON; PIN_PICKUP stays OFF."""
    assert P.ROUTE_VRP_FIX_FROZEN is True and P.ROUTE_VRP_VERIFY is True and P.ROUTE_VRP_PIN_PICKUP is False


def test_salepin1_frozen_spawn_fix(monkeypatch):
    """[SALEPIN1] band tape 2146406401 d17: hand 7 frozen (mid-day DROP) was invisible to the spawn fixed point ->
    hand 8 routed from (5,5) but spawned on (4,4) -> PICKUP off an access tile, FEEDs missed. The recorded ship
    table fails VERIFY; FIX_FROZEN passes it; VERIFY falls back to the planner's table on the buggy solve."""
    d = pickle.load(open(Path(__file__).parent / "data/route_vrp_frozen_d17.pkl", "rb"))
    plan, obs, day = d["plan"], d["obs"], int(d["day"])
    monkeypatch.setattr(P, "ROUTE_VRP_FIX_FROZEN", False)   # switch-off = the res940_vrp ship
    monkeypatch.setattr(P, "ROUTE_VRP_NEEDS_FIX_ON", False)   # recorded day predates VRPFALLBACK1
    monkeypatch.setattr(P, "ROUTE_VRP_VERIFY", False)
    base = RV.apply(plan, obs, day)
    assert all(np.array_equal(x, y) for x, y in zip(base, d["new"]))
    assert not RV.verify(plan, base, obs, day)
    monkeypatch.setattr(P, "ROUTE_VRP_FIX_FROZEN", True)
    assert RV.verify(plan, RV.apply(plan, obs, day), obs, day)
    monkeypatch.setattr(P, "ROUTE_VRP_FIX_FROZEN", False)
    monkeypatch.setattr(P, "ROUTE_VRP_VERIFY", True)
    st = {}
    out = RV.apply(plan, obs, day, st)
    assert all(np.array_equal(x, y) for x, y in zip(out, plan)) and st.get("verify_fail") == 1 and not st.get("dropped")


def test_vrpfallback1_needs_fix_default_on():
    assert P.ROUTE_VRP_NEEDS_FIX_ON is True and P.ROUTE_VRP_NEEDS_TRIM is True   # SHIP_VRP3 (res940_vrp3)


def test_vrpfallback1_needs_fix_d28(monkeypatch):
    """[VRPFALLBACK1] dev board 17 d28: the planner feeds from wheat its own HARVEST stops carry and sells the rest
    of the shed at the h1 row; the VRP's routes pick 1 wheat more than the shed holds after that row -> VERIFY
    falls back (hire kept). NEEDS_FIX: harvested wheat rides with the unit + the h1 wheat SELL gives up the unit ->
    VERIFY passes, a hand is dropped, every planner (tile, op) kept, only HIRE rows and wheat SELL qty change."""
    d = pickle.load(open(Path(__file__).parent / "data/route_vrp_needs_d28.pkl", "rb"))
    plan, obs, day = d["plan"], d["obs"], int(d["day"])
    monkeypatch.setattr(P, "ROUTE_VRP_NEEDS_FIX_ON", False)   # switch-off = the res940_vrp2 ship
    st = {}
    out = RV.apply(plan, obs, day, st)
    assert st.get("verify_fail") == 1 and all(np.array_equal(x, y) for x, y in zip(out, plan))
    monkeypatch.setattr(P, "ROUTE_VRP_NEEDS_FIX_ON", True)
    st = {}
    out = RV.apply(plan, obs, day, st)
    assert not st.get("verify_fail") and st["dropped"] >= 1 and st.get("trim", 0) >= 1
    assert RV.verify(plan, out, obs, day)
    assert _tile_ops(out, 23) == _tile_ops(plan, 23)
    m0, m1 = plan[3].copy(), out[3].copy()
    m0[m0 == O.MO_HIRE] = 0; m1[m1 == O.MO_HIRE] = 0
    wheat = RV.spec.PRODUCTS.index("WHEAT")
    q0 = int(plan[5][(plan[3] == O.MO_SELL) & (plan[4] == wheat)].sum())
    q1 = int(out[5][(out[3] == O.MO_SELL) & (out[4] == wheat)].sum())
    assert 1 <= q0 - q1 <= st["trim"]
    assert int(((plan[3] == O.MO_SELL) & (plan[4] != wheat)).sum()) == int(((out[3] == O.MO_SELL) & (out[4] != wheat)).sum())
