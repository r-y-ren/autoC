"""MELONCOUNTER2: counter tiles vs a non-V melon opener (plan.MELON_COUNTER_ON, OFF byte-identical)."""
from kagg3 import spec
from kagg3.core import plan as P


def _obs(melon, other, shops=()):
    tiles = [[None] * 10 for _ in range(10)]
    k = 0
    for crop, n in (("MELON", melon), ("WHEAT", other)):
        for _ in range(n):
            tiles[k // 10][k % 10] = {"kind": "PLANT", "crop": crop}
            k += 1
    return {"farms": [{"tiles": [[None] * 10 for _ in range(10)]}, {"tiles": tiles}],
            "town": {"unlocked_shops": list(shops)}}


def test_off_by_default():
    assert P.MELON_COUNTER_ON is False
    assert P.MC_N == 0 and P.MC_RES is None and P.MC_CROP_LIVE is None
    assert P.MC_DAY == 2 and (P.MC_MELON_MIN, P.MC_MELON_MAX, P.MC_MIN_PLANTS) == (1, 10, 1)


def test_latch_reads_rival_melon_count():
    assert P.mc_fires(_obs(5, 15), 0) == 5
    assert P.mc_fires(_obs(10, 8), 0) == 10
    assert P.mc_fires(_obs(12, 8), 0) == 0      # V opening (11-12 melon) never fires
    assert P.mc_fires(_obs(0, 19), 0) == 0      # zero-melon class is the M20z gate's
    assert P.mc_fires(_obs(0, 0), 0) == 0


def test_crop_lookup_by_first_shop(monkeypatch):
    monkeypatch.setattr(P, "MC_CROP", "TOMATO")
    assert P.mc_crop_for(_obs(5, 5)) == spec.I_TOMATO
    monkeypatch.setattr(P, "MC_CROP", "LOOKUP")
    monkeypatch.setattr(P, "MC_LOOKUP", "BAKERY:CARROT;*:WHEAT;PET_CAFE:NONE")
    assert P.mc_crop_for(_obs(5, 5)) is None                      # no shop drawn yet
    assert P.mc_crop_for(_obs(5, 5, ["BAKERY"])) == spec.I_CARROT
    assert P.mc_crop_for(_obs(5, 5, ["YARN_STORE"])) == spec.I_WHEAT
    assert P.mc_crop_for(_obs(5, 5, ["PET_CAFE"])) is None        # class with no counter
