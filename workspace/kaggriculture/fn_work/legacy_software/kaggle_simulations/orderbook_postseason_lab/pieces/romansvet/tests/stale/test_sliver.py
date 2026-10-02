"""[SLIVER1] SLIVER_ON: plantings in the route-end idle turns of the solved VRP crew (route_vrp.sliver).
OFF: apply() over tests/data/route_vrp_days.pkl is byte-identical to master 7fd8971b (digest taken from
`git archive 7fd8971b src`, SAFETY_S lifted). ON: no hire removed or added beyond mode ii's own, every planner task kept,
the only extra ops are one PLANT + one WATER per fill tile, VERIFY passes, the seed buy rides an hour 0-3 BUY_SEED row."""
import collections
import hashlib
import pickle
from pathlib import Path

import _pin  # noqa: F401
import numpy as np
import pytest
from kagg3 import spec
from kagg3.core import plan as P
from kagg3.core import ops as O
from kagg3.agent import route_vrp as RV

DAYS = pickle.load(open(Path(__file__).parent / "data/route_vrp_days.pkl", "rb"))
REF_MD5 = "60bca228b7ab97e41b2878975d0b947f"   # master 7fd8971b, default switches, same 4 days (0, 14, 22, 29)


@pytest.fixture(autouse=True)
def _clock(monkeypatch):
    monkeypatch.setattr(RV, "SAFETY_S", 1e9)


def _on(monkeypatch, mode, k=2, crop="WHEAT", d0=0, d1=26):
    for n, v in (("SLIVER_ON", True), ("SLIVER_MODE", mode), ("SLIVER_K", k), ("SLIVER_CROP", crop),
                 ("SLIVER_DAY0", d0), ("SLIVER_DAY1", d1)):
        monkeypatch.setattr(P, n, v)


def _ops(plan):
    c = collections.Counter()
    for u, lst in RV.parse_day(RV.plan_hours(plan, 23), 23)[2].items():
        for h, p, a in lst:
            if a[0] not in ("PICKUP", "DROP", "PLACE"):
                c[(p, a)] += 1
    return c


def _unit_ops(plan):
    return RV.parse_day(RV.plan_hours(plan, 23), 23)[2]


def _seed_qty(plan, ci):
    mop, ma, mq = plan[3], plan[4], plan[5]
    return int(mq[(mop == O.MO_BUY_SEED) & (ma == ci)].sum())


def _day(d):
    return [x for x in DAYS if x[0] == d][0]


def test_off_parity():
    assert P.SLIVER_ON is False
    h = hashlib.md5()
    for d, obs, plan in DAYS:
        for x in RV.apply(plan, obs, d, None, {}):
            h.update(x.tobytes())
    assert h.hexdigest() == REF_MD5


def test_crop_choice(monkeypatch):
    monkeypatch.setattr(P, "SLIVER_CROP", "WHEAT")
    assert {RV._sliver_crop(d) for d in (10, 20, 26)} == {"WHEAT"}
    monkeypatch.setattr(P, "SLIVER_CROP", "BEST")
    assert (RV._sliver_crop(10), RV._sliver_crop(16), RV._sliver_crop(17), RV._sliver_crop(26), RV._sliver_crop(27)) \
        == ("STRAWBERRY", "STRAWBERRY", "CARROT", "CARROT", "WHEAT")


@pytest.mark.parametrize("mode,n", [("same", 1), ("near", 2)])
def test_d14_fills(monkeypatch, mode, n):
    d, obs, plan = _day(14)
    st0 = collections.Counter()
    off = RV.apply(plan, obs, d, st0, {})
    _on(monkeypatch, mode)
    st = collections.Counter(); fs = {}
    new = RV.apply(plan, obs, d, st, fs)
    assert st["verify_fail"] == 0 and st["timeout"] == 0 and st["sliver"] == n, st
    assert st["dropped"] == st0["dropped"]
    hires = lambda p: int((p[3] == O.MO_HIRE).sum())
    assert hires(new) == hires(off)
    assert _ops(plan) - _ops(new) == collections.Counter()          # every planner task kept
    extra = _ops(new) - _ops(plan)
    tiles = {p for _d, _c, p in fs["all"]}
    assert len(tiles) == n and all(c == "WHEAT" and dd == 14 for dd, c, _p in fs["all"])
    assert extra == collections.Counter({(p, a): 1 for p in tiles for a in (("PLANT", "WHEAT"), ("WATER",))})
    ft = obs["farms"][obs["player"]]["tiles"]
    harvested = {p for (p, a) in _ops(plan) if a == ("HARVEST",)}
    planted = {p for (p, a) in _ops(plan) if a[0] == "PLANT"}
    for p in tiles:
        assert p not in planted
        if mode == "same":
            assert p in harvested and ft[p[1]][p[0]]["crop"] in ("WHEAT", "CARROT", "MELON")
        else:
            assert ft[p[1]][p[0]] is None or p in harvested
    # the new PLANT follows the same unit's HARVEST on that tile (same) / is the unit's last work but its WATER (near)
    for u, lst in _unit_ops(new).items():
        for i, (h, p, a) in enumerate(lst):
            if a[0] == "PLANT" and p in tiles:
                assert lst[i + 1][1:] == (p, ("WATER",)) and lst[i + 1][0] == h + 1
                if mode == "same":
                    assert lst[i - 1][1:] == (p, ("HARVEST",)) and lst[i - 1][0] == h - 1
                else:
                    assert all(a2[0] in ("PICKUP", "DROP", "PLACE") for _h2, _p2, a2 in lst[i + 2:])
    ci = spec.CROPS.index("WHEAT")
    assert _seed_qty(new, ci) - _seed_qty(off, ci) == st["sliver_buy"]
    rows = np.argwhere((new[3] == O.MO_BUY_SEED) & (new[4] == ci) & (new[5] != off[5]))
    assert all(h <= 3 for h, _s in rows)


def test_day_window_is_off(monkeypatch):
    d, obs, plan = _day(14)
    off = RV.apply(plan, obs, d, None, {})
    _on(monkeypatch, "near", d0=15)
    new = RV.apply(plan, obs, d, None, {})
    assert all(np.array_equal(a, b) for a, b in zip(off, new))


def test_k_gate(monkeypatch):
    """a hand needs >= SLIVER_K free turns after its last stop: K = 24 admits nothing."""
    d, obs, plan = _day(14)
    off = RV.apply(plan, obs, d, None, {})
    _on(monkeypatch, "near", k=24)
    st = collections.Counter()
    new = RV.apply(plan, obs, d, st, {})
    assert st["sliver"] == 0 and all(np.array_equal(a, b) for a, b in zip(off, new))
