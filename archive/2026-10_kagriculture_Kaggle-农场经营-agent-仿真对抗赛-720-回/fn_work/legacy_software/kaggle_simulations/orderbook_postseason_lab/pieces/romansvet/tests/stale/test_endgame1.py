"""ENDGAME1: END_GAME_ON gap-gated closing controller (OFF by default; OFF = the runtime never calls it)."""
import copy

import numpy as np
import pytest

from kagg3 import spec
from kagg3.agent import endgame as EG
from kagg3.core import plan as P


def _obs(day=23, hour=0, m0=50000.0, m1=50000.0, t0=None, t1=None, shed=None, inv=10000):
    tiles = lambda extra: [[(extra or {}).get((x, y)) for x in range(10)] for y in range(10)]
    return {"day": day, "hour": hour, "player": 0,
            "farms": [{"money": m0, "tiles": tiles(t0), "hands": []}, {"money": m1, "tiles": tiles(t1), "hands": []}],
            "private": {"shed": dict(shed or {}), "inventories": [{}]},
            "market": {"inventory": {n: inv for n in spec.PRODUCTS}, "prices": {n: 1 for n in spec.PRODUCTS}},
            "town": {"unlocked_shops": []}}


def _plant(crop, y, mls=720, planted=20):
    return {"kind": "PLANT", "crop": crop, "yield_units": y, "planted_day": planted, "max_lifespan_step": mls,
            "watered_today": False, "fertilized_until_day": -1, "consecutive_unwatered": 0}


def test_defaults_off():
    assert P.END_GAME_ON is False and P.END_GAME_SELL_NOW is False and P.END_GAME_DENY is False
    assert P.END_GAME_DAY == 23 and float(P.END_GAME_T) == 3000.0


def test_apply_roundtrip_restores_base(monkeypatch):
    monkeypatch.setattr(P, "_END_GAME_BASE", None)
    base = {n: copy.copy(getattr(P, n)) for n in ("RELAY_FILL_ON", "RELAY_DAYS", "CREW_LEVEL_ON", "CREW_LEVEL_CAP",
                                                  "END_GAME_SELL_NOW", "V15_DODGE_ON", "V15_DODGE_TURN")}
    try:
        P.end_game_apply(-1)
        assert P.RELAY_FILL_ON is True and P.RELAY_DAYS == (0, 27) and P.CREW_LEVEL_CAP == (12, 12)
        assert P.END_GAME_SELL_NOW is False
        P.end_game_apply(1)
        assert P.END_GAME_SELL_NOW is True and P.RELAY_FILL_ON == base["RELAY_FILL_ON"]
        P.end_game_apply(2)
        assert P.END_GAME_SELL_NOW is True and P.V15_DODGE_ON is True and P.V15_DODGE_TURN == 14
        P.end_game_apply(0)
        for n, v in base.items():
            assert getattr(P, n) == v, n
    finally:
        P.end_game_apply(0)


def test_rival_stock_harvest_feed_and_sale():
    rs = EG.RivalStock()
    a = _obs(hour=5, t1={(1, 1): _plant("WHEAT", 5), (2, 2): {"kind": "PASTURE", "animal": "COW", "yield_units": 3,
                                                               "fed_today": False}})
    rs.observe(a, 0)
    rs.record_orders([["SELL", "MILK", 2]])          # OUR row (2 milk) -- not the rival's
    b = copy.deepcopy(a)
    b["hour"] = 6
    b["farms"][1]["tiles"][1][1] = None               # wheat harvested (5 u)
    b["farms"][1]["tiles"][2][2].update(yield_units=0, fed_today=True)   # 3 milk collected, 1 wheat fed
    b["market"]["inventory"]["MILK"] += 2 + 1         # our 2 + the rival's 1 milk sold (step 557: no town tick)
    rs.observe(b, 0)
    assert rs.est[spec.I_WHEAT] == 4 and rs.est[spec.I_MILK] == 2 and rs.est.sum() == 6


def test_decaying_plant_is_not_a_harvest():
    rs = EG.RivalStock()
    a = _obs(hour=5, t1={(1, 1): _plant("TOMATO", 4, mls=23 * 24 + 6)})
    rs.observe(a, 0)
    b = copy.deepcopy(a)
    b["hour"] = 6
    b["farms"][1]["tiles"][1][1]["yield_units"] = 3
    rs.observe(b, 0)
    assert rs.est.sum() == 0


def test_decide_states():
    z = np.zeros(8, np.int64)
    assert EG.decide(_obs(m0=50000, m1=56000), 0, z, 3000)[0] == EG.BEHIND
    assert EG.decide(_obs(m0=56000, m1=50000), 0, z, 3000)[0] == EG.AHEAD
    assert EG.decide(_obs(m0=51000, m1=50000), 0, z, 3000)[0] == EG.EVEN
    rv = _obs(m0=56000, m1=50000, t1={(3, 3): _plant("WHEAT", 25)}, shed={"WHEAT": 3})
    assert EG.decide(rv, 0, z, 3000, deny=True)[0] == EG.DENY
    assert EG.decide(rv, 0, z, 3000, deny=False)[0] == EG.AHEAD
    # standing yield and our shed count at the lot quote
    o, t, _ = EG.estimate(_obs(shed={"WHEAT": 10}, t1={(0, 0): _plant("CARROT", 4)}), 0, z)
    assert o - 50000 == EG.lot_value(np.array([10, 0, 0, 0, 0, 0, 0, 0]), [10000] * 9)
    assert t - 50000 == EG.lot_value(np.array([0, 4, 0, 0, 0, 0, 0, 0]), [10000] * 9)


def test_runtime_off_builds_no_tracker():
    from kagg3.agent import runtime
    rt = runtime.Runtime.__new__(runtime.Runtime)
    runtime.Runtime.__init__(rt, lambda *a: None)
    assert rt.eg is None and rt.eg_state == 0
    src = open(runtime.__file__).read()
    assert "if P.END_GAME_ON:" in src and "if self.eg is not None and P.END_GAME_ON:" in src
