"""[VRPREPAIR1] bounded repair at a failed crew drop (regret-2 insertion + 1-step ejection chain), ROUTE_VRP_REPAIR_ON."""
import pickle
from pathlib import Path
import numpy as np
import _pin  # noqa: F401
from kagg3.core import plan as P
from kagg3.agent import route_vrp as RV

DAYS = pickle.load(open(Path(__file__).parent / "data/route_vrp_days.pkl", "rb"))


def _st(tile, early=0, late=RV.INF, dur=1):
    s = RV.Stop(tile); s.early = early; s.late = late; s.dur = dur
    return s


def _eject_case():
    """hand 0 holds A (0,2) window [0,2]; the dropped stop J (0,1) must start at t=1 and only hand 0 reaches it.
    J then A on hand 0 misses A's window, so J fits nowhere until A moves to hand 2 (starts next to it)."""
    stops = [_st((0, 2), 0, 2), _st((0, 1), 1, 1)]
    B = dict(stops=stops, units=[0, 1, 2], frozen=set(), sp={0: (0, 0), 1: (9, 9), 2: (0, 3)},
             start={0: 0, 1: 1, 2: 0}, item_av={}, end=24)
    return RV.Solver(B)


def test_eject_chain_places_blocked_stop(monkeypatch):
    monkeypatch.setattr(RV, "SAFETY_S", 1e9)
    S = _eject_case(); base = {0: [0], 2: []}
    assert S.best_insert({0: [0], 2: []}, 1, [0, 2])[1] is None          # plain insertion (mode ii) fails
    r2 = S._repair(base, [1], [0, 2], RV._CLOCK() + 10)
    assert r2 == {0: [1], 2: [0]}
    assert all(S.ev(u, r2[u]) is not None for u in (0, 2))
    assert base == {0: [0], 2: []}                                       # inputs untouched


def test_repair_respects_time_limit():
    S = _eject_case()
    assert S._repair({0: [0], 2: []}, [1], [0, 2], RV._CLOCK() - 1) is None


def test_off_is_byte_identical_and_on_saves_a_hand(monkeypatch):
    monkeypatch.setattr(RV, "SAFETY_S", 1e9)
    d, obs, plan = [x for x in DAYS if x[0] == 0][0]
    monkeypatch.setattr(P, "ROUTE_VRP_REPAIR_ON", False)
    st0 = {}; off = RV.apply(plan, obs, d, st0)
    monkeypatch.setattr(RV.Solver, "_repair", lambda *a, **k: (_ for _ in ()).throw(AssertionError("repair ran while OFF")))
    st1 = {}; off2 = RV.apply(plan, obs, d, st1)
    assert all(np.array_equal(a, b) for a, b in zip(off, off2)) and "rep_try" not in st0
    monkeypatch.undo(); monkeypatch.setattr(RV, "SAFETY_S", 1e9)
    monkeypatch.setattr(P, "ROUTE_VRP_REPAIR_ON", True)
    st2 = {}; on = RV.apply(plan, obs, d, st2)
    assert st2["rep_ok"] >= 1 and st2["dropped"] == st0["dropped"] + 1 and "verify_fail" not in st2
    assert RV.verify(plan, on, obs, d)
    hires = lambda p: int((p[3] == RV.O.MO_HIRE).sum())
    assert hires(on) == hires(off) - 1


def test_last_day_cutoff(monkeypatch):
    """[VRPREPAIR3] REPAIR_LAST_DAY=29 is byte-identical to the uncut repair; a cutoff below the day equals OFF."""
    monkeypatch.setattr(RV, "SAFETY_S", 1e9)
    d, obs, plan = [x for x in DAYS if x[0] == 0][0]
    monkeypatch.setattr(P, "ROUTE_VRP_REPAIR_ON", True)
    on = RV.apply(plan, obs, d, {})
    monkeypatch.setattr(RV, "REPAIR_LAST_DAY", 29)
    assert all(np.array_equal(a, b) for a, b in zip(on, RV.apply(plan, obs, d, {})))
    monkeypatch.setattr(RV, "REPAIR_LAST_DAY", d - 1)
    st = {}; cut = RV.apply(plan, obs, d, st)
    monkeypatch.setattr(P, "ROUTE_VRP_REPAIR_ON", False)
    off = RV.apply(plan, obs, d, {})
    assert all(np.array_equal(a, b) for a, b in zip(cut, off)) and st["rep_try"] == 0


def test_ship_vrp5_defaults():
    """SHIP_VRP5 (res940_vrp5): repair ON, cut at day 20, (REPAIR_MS, REPAIR_EJECT_K) = (100, 4)."""
    assert P.ROUTE_VRP_REPAIR_ON is True
    assert (RV.REPAIR_LAST_DAY, RV.REPAIR_MS, RV.REPAIR_EJECT_K) == (20, 100, 4)
