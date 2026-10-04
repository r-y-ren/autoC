"""apply_market_edit_operators 真值测试：三算子各分支（时移/缩放/日帽）。"""

import pytest

from derive_market_variants.apply_market_edit_operators import \
    MARKET_SLOTS, apply_market_edit_operators, is_sell

N = 160  # > 2 天，覆盖日界语义


def _step(farmer=("NORTH",), hands=(), market=()):
    return {"farmer": list(farmer), "hands": [list(h) for h in hands],
            "market": [list(m) for m in market]}


def _route():
    route = [_step() for _ in range(N)]
    route[10]["market"] = [["SELL", "WHEAT", 4], ["HIRE"]]
    route[11]["market"] = [["SELL", "MILK", 7]]
    route[100]["market"] = [["SELL", "WHEAT", 2], ["BUY_SEED", "MELON", 3]]
    return route


def test_shift_sells_by_days_basic():
    route = _route()
    out = apply_market_edit_operators({
        "route": route, "operator": "shift_sells_by_days",
        "params": {"days": 1}})
    new = out["route"]
    # 10 步 SELL -> 82（+72）；非 SELL（HIRE）原地不动
    assert new[10]["market"] == [["HIRE"]]
    assert ["SELL", "WHEAT", 4] in new[82]["market"]
    # 100 步 SELL -> 172 越界钳位 159
    assert ["SELL", "WHEAT", 2] in new[159]["market"]
    assert ["BUY_SEED", "MELON", 3] in new[100]["market"]
    ch = out["changes"]
    assert ch["operator"] == "shift_sells_by_days"
    assert ch["orders"]["moved"] == 3
    assert ch["orders"]["dropped"] == 0
    assert ch["quantity_before"] == ch["quantity_after"] == 13  # 守恒（4+7+2）
    # 原件不被串改
    assert route[10]["market"][0] == ["SELL", "WHEAT", 4]


def test_shift_backward_clamps_at_zero():
    route = _route()
    out = apply_market_edit_operators({
        "route": route, "operator": "shift_sells_by_days",
        "params": {"days": -1}})
    new = out["route"]
    # 目标 10-72/11-72 < 0 -> 钳位 0（两单同落 0 步，槽未满）
    assert ["SELL", "WHEAT", 4] in new[0]["market"]
    assert ["SELL", "MILK", 7] in new[0]["market"]
    # 100-72=28 正常后移
    assert ["SELL", "WHEAT", 2] in new[28]["market"]
    assert new[10]["market"] == [["HIRE"]]


def test_shift_slot_overflow_uses_bounded_slack():
    """落点步槽满（=10）-> ±72 内顺延；绝不回卷磁带对面。"""
    route = _route()
    route[82]["market"] = [["HIRE"]] * MARKET_SLOTS      # 目标步满
    out = apply_market_edit_operators({
        "route": route, "operator": "shift_sells_by_days",
        "params": {"days": 1}})
    ch = out["changes"]
    assert ch["orders"]["dropped"] == 0
    placed = any(["SELL", "WHEAT", 4] in route2["market"]
                 for route2 in out["route"])
    assert placed
    assert ch["displacement"]["max"] <= 72


def test_shift_band_limits_window():
    route = _route()
    out = apply_market_edit_operators({
        "route": route, "operator": "shift_sells_by_days",
        "params": {"days": 1}, "band": [0, 11]})
    ch = out["changes"]
    assert ch["orders"]["moved"] == 1          # 仅步 10 的 SELL 在窗内
    assert ["SELL", "MILK", 7] in out["route"][11]["market"]


def test_scale_sell_quantities():
    route = _route()
    out = apply_market_edit_operators({
        "route": route, "operator": "scale_sell_quantities",
        "params": {"ratio": 0.75}})
    new = out["route"]
    assert ["SELL", "WHEAT", 3] in new[10]["market"]     # round(4*.75)=3
    assert ["SELL", "MILK", 5] in new[11]["market"]      # round(7*.75)=5
    assert new[100]["market"] == [["SELL", "WHEAT", 2],
                                  ["BUY_SEED", "MELON", 3]]  # 2*.75=1.5 银行家舍入仍 2
    ch = out["changes"]
    assert ch["orders"]["rescaled"] == 2                 # 只有 4/7 两单真被改
    assert ch["quantity_before"] == 13 and ch["quantity_after"] == 10
    # q=1 缩放后仍 ≥1
    tiny = [_step() for _ in range(4)]
    tiny[1]["market"] = [["SELL", "EGG", 1], ["HIRE"]]
    out2 = apply_market_edit_operators({
        "route": tiny, "operator": "scale_sell_quantities",
        "params": {"ratio": 0.5}})
    assert ["SELL", "EGG", 1] in out2["route"][1]["market"]


def test_daily_sell_cap_chronological_truncation():
    route = [_step() for _ in range(N)]
    # 第 1 天（步 72-143）：步 80 卖 WHEAT 30、步 90 卖 WHEAT 30 -> 帽 40
    route[80]["market"] = [["SELL", "WHEAT", 30]]
    route[90]["market"] = [["SELL", "WHEAT", 30], ["SELL", "MILK", 10]]
    out = apply_market_edit_operators({
        "route": route, "operator": "daily_sell_cap",
        "params": {"cap": 40}})
    new = out["route"]
    assert new[80]["market"] == [["SELL", "WHEAT", 30]]   # 时间序先到先得
    assert new[90]["market"] == [["SELL", "WHEAT", 10],   # WHEAT 截到帽
                                 ["SELL", "MILK", 10]]    # MILK 独立计帽
    ch = out["changes"]
    assert ch["orders"]["capped"] == 1
    assert ch["quantity_before"] == 70 and ch["quantity_after"] == 50


def test_daily_sell_cap_band_boundaries():
    route = [_step() for _ in range(N)]
    route[10]["market"] = [["SELL", "WHEAT", 50]]         # 第 0 天
    route[80]["market"] = [["SELL", "WHEAT", 50]]         # 第 1 天
    out = apply_market_edit_operators({
        "route": route, "operator": "daily_sell_cap",
        "params": {"cap": 20}})
    assert out["route"][10]["market"] == [["SELL", "WHEAT", 20]]
    assert out["route"][80]["market"] == [["SELL", "WHEAT", 20]]


def test_farmer_stream_never_touched():
    route = _route()
    ops = [
        ("shift_sells_by_days", {"days": 1}),
        ("shift_sells_by_days", {"days": -2}),
        ("scale_sell_quantities", {"ratio": 1.5}),
        ("daily_sell_cap", {"cap": 5}),
    ]
    for operator, params in ops:
        out = apply_market_edit_operators({
            "route": route, "operator": operator, "params": params})
        assert [(s["farmer"], s["hands"]) for s in out["route"]] == [
            (s["farmer"], s["hands"]) for s in route]


def test_fail_closed_inputs():
    with pytest.raises(ValueError, match="fail-closed"):
        apply_market_edit_operators({"route": [], "operator":
                                     "shift_sells_by_days"})
    with pytest.raises(ValueError, match="unknown market edit operator"):
        apply_market_edit_operators({"route": _route(), "operator": "magic"})
    for op, params in (("shift_sells_by_days", {}),
                       ("scale_sell_quantities", {}),
                       ("daily_sell_cap", {})):
        with pytest.raises(ValueError, match="needs params"):
            apply_market_edit_operators({"route": _route(),
                                         "operator": op,
                                         "params": params})


def test_is_sell_helper():
    assert is_sell(["SELL", "WHEAT", 1])
    assert not is_sell(["HIRE"])
    assert not is_sell("junk")
