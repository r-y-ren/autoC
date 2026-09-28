# -*- coding: utf-8 -*-
"""R24 测试面：ab 组（B33：路线表/臂件构建/末 callable 语义/generic 闸门/
账本编排）+ run_r41_iteration（B36 桩保留）。判据=R24 ①②相关用例原文。"""
from __future__ import annotations

import pytest

from orderbook_r40 import ab_r41 as ab


# ---------------------------------------------- ab 组（B33） --

def test_build_alt_table_neighbor_vote():
    """邻域投票：共享一店的店对中非基座路线众数（并列取小）；无邻域弃样。"""
    base = {"A+B": 1, "A+C": 2, "B+C": 1, "D+E": 9}
    table = ab.build_alt_table(base)
    # A+B 邻域：A+C(route2 投票)、B+C(route1=基座 1 剔除) → alt=2
    assert table["A+B"] == 2
    # A+C 邻域：A+B(route1)、B+C(route1) → 两票 route1 → alt=1
    assert table["A+C"] == 1
    # B+C 邻域：A+B(1=基座剔除)、A+C(2) → alt=2
    assert table["B+C"] == 2
    # D+E 无邻域 → 弃样（不出表）
    assert "D+E" not in table


def test_build_alt_table_key_order_normalized():
    """店对键序归一：'B+A' 与 'A+B' 同键。"""
    table = ab.build_alt_table({"B+A": 1, "A+C": 2, "B+C": 1})
    assert "A+B" in table and "B+A" not in table


def test_pick_generic_route_plurality():
    """通用路线=覆盖店对最多（并列取小 route id）。"""
    assert ab.pick_generic_route({"A+B": 5, "A+C": 5, "B+C": 7}) == 5
    assert ab.pick_generic_route({"A+B": 5, "A+C": 7}) == 5


def test_build_ab_variant_control_identity():
    """control 臂=原字节恒等。"""
    text = "def _route40_select(observation, library=None):\n    return None\n"
    out = ab.build_ab_variant(text, "control")
    assert out["main_text"] == text
    assert out["arm"] == "control"
    assert out["arm_sha"] == ab._sha(text)


def test_build_ab_variant_alt_override():
    """alt 臂：前缀恒等+覆盖件在位+确定性+恰好一个新增 def。"""
    text = ("def _route40_select(observation, library=None):\n"
            "    return {'route': None}\n\n\n"
            "def _route40_agent(observation):\n"
            "    return _route40_select(observation)\n")
    table = {"A+B": 7}
    out1 = ab.build_ab_variant(text, "alt", table, {"A+B": 3}, 3)
    out2 = ab.build_ab_variant(text, "alt", table, {"A+B": 3}, 3)
    assert out1["main_text"].startswith(text)
    assert "AB_ALT" in out1["main_text"]
    assert out1["arm_sha"] == out2["arm_sha"]          # 确定性
    assert out1["main_text"].count("\ndef ") == \
        text.count("\ndef ") + 1                        # 只增覆盖件
    compile(out1["main_text"], "<t>", "exec")


def test_ab_alt_last_callable_semantics_preserved():
    """末 callable 语义：装载入口（末 callable）不被尾块顶替。"""
    text = ("def _route40_select(observation, library=None):\n"
            "    return {'route': None}\n\n\n"
            "def _route40_agent(observation):\n"
            "    return _route40_select(observation)\n")

    def _entry(src):
        ns = {}
        exec(compile(src, "<t>", "exec"), ns)
        entries = [v for v in ns.values() if callable(v)]
        return entries[-1]

    base_entry = _entry(text)
    alt = ab.build_ab_variant(text, "alt", {"A+B": 7}, {"A+B": 3}, 3)
    alt_entry = _entry(alt["main_text"])
    assert base_entry.__name__ == alt_entry.__name__ == "_route40_agent"


def test_ab_alt_override_forces_route_then_passthrough():
    """alt 覆盖行为：step144 命中表→强制路线；未命中→透传底选路。"""
    text = ("def _route40_select(observation, library=None):\n"
            "    return {'route': 105, 'family': 'BASE', 'confidence': 0.5}\n"
            "\n\n\ndef _route40_agent(observation):\n"
            "    return _route40_select(observation)\n")
    alt = ab.build_ab_variant(text, "alt", {"A+B": 7}, {"A+B": 3}, 3)
    ns = {}
    exec(compile(alt["main_text"], "<t>", "exec"), ns)
    sel = ns["_route40_select"]
    hit = {"step": 144, "town": {"unlocked_shops": ["B", "A"]}}
    assert sel(hit) == {"route": 7, "family": "AB_ALT", "confidence": 1.0}
    miss = {"step": 144, "town": {"unlocked_shops": ["X", "Y"]}}
    assert sel(miss)["family"] == "BASE"                 # 透传底选路
    early = {"step": 100, "town": {"unlocked_shops": ["B", "A"]}}
    assert sel(early)["family"] == "BASE"                # 锁存步前不动


def test_ab_generic_gate():
    """const 闸门：基座≠强制线才强制；同线→透传（零对照污染）。"""
    text = ("def _route40_select(observation, library=None):\n"
            "    return {'route': 5, 'family': 'BASE', 'confidence': 0.5}\n"
            "\n\n\ndef _route40_agent(observation):\n"
            "    return _route40_select(observation)\n")
    built = ab.build_ab_variant(text, "generic", {}, {"A+B": 5, "C+D": 9}, 9)
    ns = {}
    exec(compile(built["main_text"], "<t>", "exec"), ns)
    sel = ns["_route40_select"]
    spec = {"step": 144, "town": {"unlocked_shops": ["B", "A"]}}
    assert sel(spec) == {"route": 9, "family": "AB_CONST",
                         "confidence": 1.0}              # 5≠9 → 强制
    same = {"step": 144, "town": {"unlocked_shops": ["C", "D"]}}
    assert sel(same)["family"] == "BASE"                 # 9=9 → 透传


def test_pick_timing_routes_extremes():
    """时机两极：加权卖货步最小=early、最大=late（真磁带画像）。"""
    from pathlib import Path
    main_text = Path(ab.DEFAULT_R40_MAIN).read_text(encoding="utf-8")
    base = ab._base_route_map()
    timing = ab.pick_timing_routes(main_text, base)
    prof = ab.route_timing_profiles(main_text, base)
    assert timing["early"] == min(prof, key=lambda r: (prof[r], r))
    assert timing["late"] == max(prof, key=lambda r: (prof[r], r))
    assert prof[timing["early"]] < prof[timing["late"]]


def test_run_ab_experiments_ledger_pairing(monkeypatch, tmp_path):
    """账本编排：两处理臂配对/家族统计/样本不足→账本落盘后抛。"""
    base = ab._base_route_map()
    generic = ab.pick_generic_route(base)
    timing = ab.pick_timing_routes(
        __import__("pathlib").Path(ab.DEFAULT_R40_MAIN).read_text(
            encoding="utf-8"), base)
    arm_route = {"generic": generic, "early": timing["early"],
                 "late": timing["late"]}
    pair = next(k for k in sorted(base)
                if base[k] not in set(arm_route.values()))
    calls = []

    def fake_play(specs, cfg):
        specs = list(specs)
        calls.append([s["arm"] for s in specs])
        rows = []
        for s in specs:
            row = {"game_id": s["game_id"], "seed": s["seed"],
                   "seat": s["our_seat"], "arm": s["arm"],
                   "opponent": "opp", "error": None,
                   "banks": [5000.0, 4000.0] if s["our_seat"] == 0
                   else [4000.0, 5000.0]}
            if s["arm"] == "control":
                row["face"] = "L|M|L"
                row["pair"] = pair
                row["margin"] = 1000.0
            else:
                row["face"] = None
                row["pair"] = None
                row["margin"] = {"generic": 1500.0, "early": 1400.0,
                                 "late": 1200.0}[s["arm"]]
            rows.append(row)
        return rows

    monkeypatch.setattr(ab, "_ab_play_batch", fake_play)
    led_path = tmp_path / "ledger.json"
    cfg = {"n_seeds": 4, "seed_base": 1, "min_paired": 1,
           "opponents": ["orderbook_r37/build/main.py"],
           "workers": 1, "ledger_path": str(led_path)}
    out = ab.run_route_ab_experiments(None, cfg)
    led = out["ledger"]
    assert led["n_units_planned"] == 8          # 4 seeds × 双席
    assert led["n_units_paired"] == 8
    assert led["n_units_treated"] == {"generic": 8, "early": 8, "late": 8}
    assert calls[0][0] == "control" and calls[1][0] == "generic" and \
        calls[2][0] == "early" and calls[3][0] == "late"
    fam = led["arm_stats"]["families"]["L|M|L"]
    assert fam["generic"]["n"] == 8 and fam["generic"]["mean_delta"] == 500.0
    assert fam["early"]["mean_delta"] == 400.0
    assert fam["late"]["mean_delta"] == 200.0
    assert led["arm_stats"]["arm_routes"]["generic"] == generic
    assert led_path.is_file()

    # 样本不足→账本先落盘后抛
    cfg2 = dict(cfg)
    cfg2["min_paired"] = 100
    with pytest.raises(ValueError):
        ab.run_route_ab_experiments(None, cfg2)
    assert led_path.is_file()


# ------------------------------------------- run_r41_iteration（B36） --

def test_run_r41_iteration():
    raise NotImplementedError("unimplemented:fn:run_r41_iteration")
