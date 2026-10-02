"""[VRPOBJ1] one objective: route_eval's pickup placement, rcost and the checkpoint ranking share route_key/sol_key."""
from kagg3.agent import route_vrp as RV


def _case():
    A = RV.Stop((7, 5)); A.dur = 1
    C = RV.Stop((9, 4)); C.dur = 1; C.need["WHEAT"] = 1
    return [A, C]


def test_route_key_lexicographic():
    assert RV.route_key(10, 23) < RV.route_key(11, 0)          # elapsed first
    assert RV.route_key(10, 3) < RV.route_key(10, 4)           # moves break ties
    assert RV.route_key(10, 24) < RV.route_key(11, 0)          # a route makes <= 24 moves: lexicographic per route


def test_pickup_placement_uses_route_key():
    stops = _case(); r = [0, 1]; pav = 10
    sims = {pi: RV._sim(r, (2, 3), 0, pi, 1, pav, 24, stops) for pi in (0, 1)}
    assert sims[0][:2] == (20, 10) and sims[1][:2] == (17, 14)   # master (finish + moves) picked pi=0: 30 < 31
    v = RV.route_eval(r, (2, 3), 0, {"WHEAT": pav}, 24, stops)
    assert v[3] == 1 and v[0] == 17
    assert RV.route_key(v[0], v[1]) == min(RV.route_key(s[0], s[1]) for s in sims.values())


def test_rcost_is_route_key():
    stops = _case()
    B = dict(stops=stops, units=[0], frozen=set(), sp={0: (2, 3)}, start={0: 0}, item_av={"WHEAT": 10}, end=24)
    S = RV.Solver(B)
    v = S.ev(0, [0, 1])
    assert S.rcost(0, [0, 1]) == RV.route_key(v[0] - 0, v[1]) == S.cost(v)


def test_sol_key_crew_first():
    cheap_route_more_crew = RV.sol_key([], 5.0)
    one_less_hand = RV.sol_key([3], 50.0)
    assert one_less_hand < cheap_route_more_crew
    assert RV.sol_key([3], 5.0) < RV.sol_key([3], 6.0)
    assert RV.sol_key([4], 99.0) < RV.sol_key([3], 1.0)   # fib(4)=3 > fib(3)=2: dropping the dearer hand wins


def test_timeout_restores_in_sol_key_order(monkeypatch):
    """on the deadline, checkpoints are tried best sol_key first (crew bill, then route cost), not latest first."""
    import pickle
    from pathlib import Path
    import _pin  # noqa: F401
    DAYS = pickle.load(open(Path(__file__).parent / "data/route_vrp_days.pkl", "rb"))
    d, obs, plan = [x for x in DAYS if x[0] == 14][0]
    tried = []
    solve0 = RV.solve_plan

    def solve(*a, **k):
        solve0(*a, **k)
        raise RV._Timeout()   # full search ran, all checkpoints recorded; now take the timeout path

    monkeypatch.setattr(RV, "solve_plan", solve)
    monkeypatch.setattr(RV, "SAFETY_S", 1e9)
    monkeypatch.setattr(RV, "_restore", lambda plan_, obs_, day_, ck: tried.append(ck["key"]))
    st = {}
    RV.apply(plan, obs, d, st)
    assert st["timeout"] == 1 and len(tried) >= 2
    assert tried == sorted(tried)
