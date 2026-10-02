"""[PACKV3] SHIP_VRP15_K2FIRE contract: the KERNEL2 candidate v3 (MELONHYBRID4 A4 + the KERNEL2FIRE1 real-h0 whitelist
26|29|2338|2438 + the STEP0TIME1 lazy V56 load) is the tree's DEFAULT, the LE.SWITCHES gene block carries the same switches
(every shipped switch rides the block, incl. PLACEFEED_ON + PF_PUMPSAFE_ON), the 4-value FIRE_CASH list survives both parsers
(the block splits on ',', the runtime on '|'), the whitelist overrides CASH_MAX / ZERO_CASH, and the pin row names the config
commit.  Named-file test: .venv/bin/python -m pytest tests/test_kernel2_v3_package.py"""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))
from kagg3.core import plan as P  # noqa: E402
from kagg3.agent import runtime as RT  # noqa: E402

V3 = {"KERNEL2_ON": True, "KERNEL2_NOOP_H0": False, "KERNEL2_INHERIT": True, "KERNEL2_FIRE_CASH": "99999",   # PACK20: no live value (PACK18: 26|29|2046|2338|2438)
      "KERNEL2_PRELOAD": False, "KERNEL2_HANDBACK_DAY": 18}   # PACKHB1: + the D18 hand-back
FIRE_SET = {99999}   # PACK20 vrp20: sentinel only, no live h1 (vrp18 = {26, 29, 2046, 2338, 2438}; vrp15/vrp17 = {26, 29, 2338, 2438})
FS = lambda k, x: str(x) if k == "KERNEL2_FIRE_CASH" else x   # PACK20: the block parses "99999" to int 99999; kernel2_cash_list(str()) is the same set


def _gene_block():
    src = (ROOT / "S/actionrl/live_expert.py").read_text()
    m = re.search(r"^SWITCHES = \((.*?)^\)", src, re.S | re.M)
    return ast.literal_eval("(" + m.group(1) + ")")


def _items():
    return dict(i.partition("=")[::2] for i in _gene_block().split(","))


def _le_value(raw):   # S/actionrl/live_expert._value, verbatim (the module imports jax + head, so it is not imported here)
    if raw in ("True", "False"):
        return raw == "True"
    for fn in (int, float):
        try:
            return fn(raw)
        except ValueError:
            pass
    return raw


def test_plan_defaults_are_v3():
    for k, v in V3.items():
        assert getattr(P, k) == v, k
    assert P.KERNEL2_PRELOAD is False                                          # lazy V56 (STEP0TIME1)
    assert P.KERNEL2_ZERO_CASH == "" and P.KERNEL2_CASH_MAX == 2550            # ignored under FIRE_CASH, left at defaults
    assert P.KERNEL2_ZERO_BACK is False and P.KERNEL2_PFS_H0MERGE is False     # not part of v3
    assert P.PLACEFEED_ON is True and P.PF_PUMPSAFE_ON is True                 # vrp12_pfs body kept


def test_gene_block_carries_v3_and_equals_plan_defaults():
    items = _items()
    for k, v in V3.items():
        assert FS(k, _le_value(items[k])) == v, k
    assert "KERNEL2_ZERO_CASH" not in items
    assert items["PLACEFEED_ON"] == "True" and items["PF_PUMPSAFE_ON"] == "True"
    for k, raw in items.items():
        if not k.startswith("brain."):
            assert FS(k, _le_value(raw)) == FS(k, getattr(P, k)), k     # applying the block to this tree is a no-op (FIRE_CASH: same set)


def test_fire_cash_list_parses_to_four_values():
    assert RT.kernel2_cash_list(P.KERNEL2_FIRE_CASH) == FIRE_SET
    assert RT.kernel2_cash_list(_le_value(_items()["KERNEL2_FIRE_CASH"])) == FIRE_SET
    assert RT.kernel2_cash_list(_le_value("2438")) == {2438}    # a single value becomes int; str() keeps the latch working
    assert RT.kernel2_cash_list("") == set()


SENT = {"farmer": ["PASS"], "hands": [], "market": []}


def _latch(cash, player=0):
    """The REAL Runtime._kernel2 step-0 + step-1 latch under this tree's defaults; the kernel callable is a stub (no V56
    exec) and INHERIT is switched off by the caller only so step 1 needs no full obs (real games: PACKV3 proofs)."""
    farms = [{"money": 1409}, {"money": 1409}]
    farms[1 - player]["money"] = cash
    rt = RT.Runtime(lambda *a, **k: None)
    assert rt._kernel2({"step": 0, "day": 0, "hour": 0, "player": player, "farms": farms}, None) is None   # real PFS h0
    assert rt.k2_fn is None                                                                               # lazy: nothing V56
    rt.k2_fn = lambda obs, config=None: dict(SENT)
    a = rt._kernel2({"step": 1, "day": 0, "hour": 1, "player": player, "farms": farms}, None)
    assert (a is None) == (rt.k2_mode == "pfs")
    return rt.k2_mode


def test_whitelist_overrides_cash_max_and_zero_cash(monkeypatch):
    monkeypatch.setattr(P, "KERNEL2_INHERIT", False)
    for c in FIRE_SET:
        for seat in (0, 1):
            assert _latch(c, seat) == "v56", c
    W36 = (1, 4, 8, 17, 19, 23, 26, 29, 34, 73, 76, 117, 160, 163, 182, 190, 444, 456, 553, 564, 620, 638, 661, 938, 1616, 2046, 2322,
           2338, 2438, 2477, 2485, 2492, 2511, 2593, 2600, 2904)   # SHIPSYNC5: vrp19w's wide list (live sub 56649892) must stay PFS on vrp20
    for c in W36 + (488, 1088, 1303, 1409, 2464, 20, 189, 191, 988, 1020, 2015, 2885, 2867, 2045, 2047, 2, 3, 939, 2601, 2550, 2854, 0, 33, 55, 2339, 2467):   # vrp15/17/18/19w fire values + ZERO / self / no-fire / V / no-op-h0 keys
        for seat in (0, 1):
            assert _latch(c, seat) == "pfs", c   # PACK20: every vrp15/17/18/19w fire value stays PFS


def test_lazy_load_wiring():
    src = (ROOT / "src/kagg3/agent/runtime.py").read_text()
    assert "self.k2_fn = kernel2_load() if P.KERNEL2_PRELOAD else None" in src      # step 0: nothing V56 when False
    assert "if self.k2_fn is None:\n            self.k2_fn = kernel2_load()" in src   # fired step 1: exec'd on demand


def test_pin_row_names_the_config_commit():
    import _pin
    row = _pin.SHIPPED_PACKAGES["vrp20_pfsoff"]           # PACK20, LIVE sub 56652418 (this tree's defaults); SHIPSYNC5 moved the shipped pin here
    assert row["ref"] == "b940d667" and _pin.SHIPPED == "b940d667" and row["sub"] == 56652418
    assert row["md5"] == "e5d84f03"
    w = _pin.SHIPPED_PACKAGES["vrp19w_k2wide"]   # live vrp19w row kept (sub 56649892)
    assert w["ref"] == "81090f6a" and w["md5"] == "e490347d" and w["sub"] == 56649892 and not w.get("retired")
    assert row["switches"]["KERNEL2_HANDBACK_DAY"] == V3["KERNEL2_HANDBACK_DAY"] == 18
    assert {k: row["switches"][k] for k in ("KERNEL2_ON", "KERNEL2_NOOP_H0", "KERNEL2_INHERIT", "KERNEL2_PRELOAD")} == {
        "KERNEL2_ON": 1, "KERNEL2_NOOP_H0": 0, "KERNEL2_INHERIT": 1, "KERNEL2_PRELOAD": 0}
    assert row["switches"]["KERNEL2_FIRE_CASH"] == V3["KERNEL2_FIRE_CASH"]
    assert _pin.SHIPPED_PACKAGES[56612145]["md5"] == "2532e456"      # vrp12 row kept
    assert _pin.SHIPPED_PACKAGES["vrp14_k2real"]["md5"] == "233430d3"   # vrp14 row kept (alternative candidate)
    assert _pin.SHIPPED_PACKAGES["vrp15_k2fire"]["md5"] == "1929f224"   # vrp15 row kept (retired by 56646827)
    assert _pin.SHIPPED_PACKAGES["vrp17_k2hb"]["ref"] == "ec2a6042" and _pin.SHIPPED_PACKAGES["vrp17_k2hb"]["md5"] == "11fd0f57"   # vrp17 row kept (sub 56643352, retired by 56649892)
    assert _pin.SHIPPED_PACKAGES["vrp18_k2hb2046"]["ref"] == "599f8881" and _pin.SHIPPED_PACKAGES["vrp18_k2hb2046"]["md5"] == "d6ed14d6"   # vrp18 row kept (sub 56646827, retired by 56652418)
    assert _pin.SHIPPED_PACKAGES["vrp18_k2hb2046"]["sub"] == 56646827 and _pin.SHIPPED_PACKAGES["vrp18_k2hb2046"]["retired"]
