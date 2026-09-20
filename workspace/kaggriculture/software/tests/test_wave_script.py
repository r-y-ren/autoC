# ===========================================================================
# tests/test_wave_script.py —— v15「点火重构」波次剧本引擎（M-A/B/C/D）测试
# ---------------------------------------------------------------------------
# 钉住四件事：
#   1) 旗关零足迹：WAVE_ENABLED=False（默认）时引擎可装载、全部钩子返回
#      原生值（计划补丁原样、市场事件空、卖单原序、sell_first False）；
#   2) 剧本开闸后的日历行为：d0 开局补丁（畜/种/保险）、d6/d10 资本波次、
#      crew 阶梯、首店身份路由、flush 市场事件、终局 glut 排序；
#   3) 校准互检：planner/wave_script.py 的日历镜像 == src/wave.py 权威表
#      （M-D：island-ga 基因组 + kaggri 一行 + gytdrop/2945 的落表正确性）；
#   4) M-C 分派：runtime._spec_knob_overrides/_spec_tail_score 对剧本候选
#      与 PlanSpec 的分派；WaveCandidate 键面与注入面契约。
# 纪律：不跑引擎对局（对局验证归 scripts/v15_*）；全部纯函数级。
# ===========================================================================

import os
import sys

import pytest

SOFTWARE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENT_DIR = os.path.join(SOFTWARE, "kaggle_simulations", "agent")
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

V15_MODULE_ORDER = ("constants", "telemetry", "observer", "strategy",
                    "mission", "solver", "executor", "market", "wave",
                    "entry")


def build_ns(wave_mode=False):
    """main.py 同语义装载扁平命名空间；wave_mode=True 时开剧本总闸。"""
    ns = {}
    exec("; ".join(("import copy", "import math", "import json",
                    "import hashlib")), ns)
    for mod in V15_MODULE_ORDER:
        path = os.path.join(AGENT_DIR, "src", mod + ".py")
        with open(path, "r", encoding="utf-8") as handle:
            source = handle.read()
        exec(compile(source, path, "exec"), ns)
    if wave_mode:
        ns["PLANNER_ENABLED"] = True
        ns["PLANNER_OVERRIDES"]["wave_mode"] = True
    return ns


def obs_min(day=0, shops=()):
    """最小 obs（剧本纯函数只消费 day/town.unlocked_shops/farms/player）。"""
    return {"player": 0, "day": day, "hour": 0,
            "town": {"unlocked_shops": list(shops)},
            "farms": [], "market": {"prices": {}}}


BASE_PLAN = {"mode": "DEFENSIVE", "volume": False, "scale": False,
             "straw_quad_cap": 8, "straw_total_cap": 24,
             "wheat_money_quad": 3, "crew_cap": 12, "herd_ceiling": 17}


# ---------------------------------------------------------------------------
# 1) 旗关零足迹
# ---------------------------------------------------------------------------

class TestFlagoffFootprint:
    def test_flag_off_overlay_returns_plan_unchanged(self):
        ns = build_ns(wave_mode=False)
        plan = dict(BASE_PLAN)
        out = ns["_wave_overlay"](0, obs_min(day=3), 3, plan)
        assert out == plan

    def test_flag_off_market_events_empty_and_sell_first_false(self):
        ns = build_ns(wave_mode=False)
        assert ns["_wave_market_events"](
            obs_min(0), None, {}, 0, 0, {"WOOL": 24}, {}) == []
        assert ns["_wave_sell_first"](6) is False

    def test_flag_off_crew_target_returns_native(self):
        ns = build_ns(wave_mode=False)
        assert ns["_wave_crew_target"](10, 8, 12, 999) == 999

    def test_flag_off_sell_ordering_is_identity(self):
        ns = build_ns(wave_mode=False)
        merged = [["BUY_ANIMAL", "COW", 1], ["SELL", "WOOL", 4],
                  ["SELL", "MELON", 6]]
        assert ns["_wave_merge_sells"](merged, {}, 10, False, {}) == merged

    def test_hooks_dead_without_wave_module(self):
        """wave.py 缺席时（如旧 golden 装载序）钩子死路：_crew_target/
        _macro_plan 走原生路径不抛异常。"""
        ns = {}
        exec("; ".join(("import copy", "import math", "import json",
                        "import hashlib")), ns)
        for mod in V15_MODULE_ORDER:
            if mod == "wave":
                continue
            path = os.path.join(AGENT_DIR, "src", mod + ".py")
            with open(path, "r", encoding="utf-8") as handle:
                exec(compile(source := handle.read(), path, "exec"), ns)
        assert ns["_crew_target"](10, 12, 0, 3, None) == 12


# ---------------------------------------------------------------------------
# 2) 剧本开闸后的日历行为
# ---------------------------------------------------------------------------

class TestWaveOverlay:
    def test_d0_opening_patch(self):
        ns = build_ns(wave_mode=True)
        out = ns["_wave_overlay"](0, obs_min(day=0), 0, dict(BASE_PLAN))
        assert out["opening_seq_override"][0] == {"COW": 2, "SHEEP": 2}
        assert out["land_plan_override"] == {1: (6, 1300), 2: (10, 2300)}
        assert out["melon_total_cap"] == 7
        assert out["crew_cap"] >= 13

    def test_d6_capital_wave_adds_five_cows(self):
        ns = build_ns(wave_mode=True)
        out = ns["_wave_overlay"](0, obs_min(day=6), 6, dict(BASE_PLAN))
        assert out["opening_seq_override"][6] == {"COW": 5}

    def test_yarn_route_latches_six_sheep_d11(self):
        ns = build_ns(wave_mode=True)
        obs = obs_min(day=3, shops=["YARN_STORE"])
        out = ns["_wave_overlay"](0, obs, 3, dict(BASE_PLAN))
        assert out["wave_route"] == "WOOL"
        assert out["opening_seq_override"][11] == {"SHEEP": 6}

    def test_route_latches_once_first_shop_wins(self):
        ns = build_ns(wave_mode=True)
        ns["_wave_overlay"](0, obs_min(day=3, shops=["BAKERY"]), 3,
                            dict(BASE_PLAN))
        obs2 = obs_min(day=6, shops=["BAKERY", "YARN_STORE"])
        assert ns["_wave_route"](0, obs2) == "CAPITAL"

    def test_crew_ladder_calendar(self):
        ns = build_ns(wave_mode=True)
        assert ns["_wave_crew_target"](0, 4, 13, 0) == 5
        assert ns["_wave_crew_target"](5, 4, 13, 0) == 6
        assert ns["_wave_crew_target"](8, 6, 13, 0) == 8
        assert ns["_wave_crew_target"](10, 9, 13, 0) == 12
        assert ns["_wave_crew_target"](11, 9, 13, 0) == 13
        # 畜群地板保留（CARE 攒量靠 crew 覆盖）
        assert ns["_wave_crew_target"](2, 9, 13, 0) == 9
        # 帽约束
        assert ns["_wave_crew_target"](11, 4, 12, 0) == 12

    def test_melon_quad_cap_widened_only_in_wave(self):
        ns = build_ns(wave_mode=True)
        assert ns["_wave_melon_quad_cap"](6) == 7
        ns_off = build_ns(wave_mode=False)
        assert ns_off["_wave_melon_quad_cap"](6) == 6


class TestWaveMarketEvents:
    def test_d0_insurance_buy_first_slots(self):
        ns = build_ns(wave_mode=True)
        events = ns["_wave_market_events"](obs_min(0), None, {}, 0, 0, {},
                                           {})
        assert events == [["BUY_PRODUCT", "WHEAT", 5]]

    def test_wool_flush_sells_whole_shed(self):
        ns = build_ns(wave_mode=True)
        shed = {"WOOL": 24, "MILK": 0, "MELON": 0}
        events = ns["_wave_market_events"](obs_min(6), None, {}, 6, 3,
                                           shed, {})
        assert ["SELL", "WOOL", 24] in events

    def test_melon_flush_and_milk_flush(self):
        ns = build_ns(wave_mode=True)
        shed = {"MELON": 42, "MILK": 12}
        events = ns["_wave_market_events"](obs_min(10), None, {}, 10, 3,
                                           shed, {})
        assert ["SELL", "MELON", 42] in events
        assert ["SELL", "MILK", 12] in events
        # flush 窗外不强卖
        events9 = ns["_wave_market_events"](obs_min(9), None, {}, 9, 3,
                                            shed, {})
        assert all(o[1] != "MELON" for o in events9)

    def test_flush_days_sell_first(self):
        ns = build_ns(wave_mode=True)
        assert ns["_wave_sell_first"](6) is True
        assert ns["_wave_sell_first"](10) is True
        assert ns["_wave_sell_first"](7) is False


class TestWaveSellOrdering:
    def test_impact_order_puts_fast_crasher_first(self):
        ns = build_ns(wave_mode=True)
        prices = {"WOOL": 200.0, "MELON": 250.0}
        # 瓜 sq 曲线大单压价更深（影响分 = q×Δp 更大）→ 排前
        merged = [["SELL", "WOOL", 24], ["SELL", "MELON", 100]]
        out = ns["_wave_merge_sells"](merged, prices, 10, False, {})
        assert out[0][1] == "MELON"
        assert out[1][1] == "WOOL"

    def test_impact_score_zero_keeps_deterministic_order(self):
        ns = build_ns(wave_mode=True)
        prices = {"WOOL": 200.0}
        merged = [["SELL", "WOOL", 2], ["SELL", "MELON", 1]]
        out = ns["_wave_merge_sells"](merged, prices, 10, False, {})
        assert out == merged          # 零影响分对 → (0, item) 字典序稳定

    def test_terminal_day_uses_glut_exposure_score(self):
        ns = build_ns(wave_mode=True)
        prices = {"WOOL": 200.0, "MELON": 250.0}
        opp = {"MELON": 40, "WOOL": 0}
        merged = [["SELL", "WOOL", 20], ["SELL", "MELON", 20]]
        out = ns["_wave_merge_sells"](merged, prices, 29, True, opp)
        assert [o[1] for o in out] == ["MELON", "WOOL"]

    def test_single_sell_and_non_sell_rows_keep_order(self):
        ns = build_ns(wave_mode=True)
        merged = [["BUY_ANIMAL", "COW", 1], ["SELL", "WOOL", 4]]
        out = ns["_wave_merge_sells"](merged, {"WOOL": 200.0}, 6, False, {})
        assert out == merged


# ---------------------------------------------------------------------------
# 3) M-D 校准互检（planner 镜像 == src 权威表；island-ga/kaggri 落表）
# ---------------------------------------------------------------------------

class TestCalibrationCrossCheck:
    def _planner_wave(self):
        from kaggle_simulations.agent.planner import wave_script
        return wave_script

    def test_planner_mirror_matches_src_tables(self):
        wave = self._planner_wave()
        ns = build_ns(wave_mode=False)
        assert wave.WAVE_CAL["crew_ladder"] == ns["WAVE_CREW_LADDER"]
        assert wave.WAVE_CAL["opening_herd"] == ns["WAVE_OPENING_HERD"][0]
        assert wave.WAVE_CAL["herd_waves"] == ns["WAVE_HERD_WAVES"]
        assert wave.WAVE_CAL["herd_waves_yarn"] == ns["WAVE_HERD_WAVES_YARN"]
        assert wave.WAVE_CAL["land_waves"] == ns["WAVE_LAND_WAVES"]
        assert wave.WAVE_CAL["flush"] == ns["WAVE_FLUSH_DAYS"]
        assert wave.WAVE_CAL["milk_flush_from"] == ns["WAVE_MILK_FLUSH_FROM"]
        assert wave.WAVE_CAL["melon_tiles"] == \
            ns["WAVE_OPENING_SEEDS"]["MELON"]
        for item, weight in wave.WAVE_CAL["glut"].items():
            assert ns["WAVE_GLUT_WEIGHTS"][item] == weight

    def test_island_ga_genome_d0_anchor(self):
        """island-ga envelope（MIT）：d0 = COW×2+SHEEP×2，NW 即日播种，
        NE d6 / SW d10 / SE 不开。"""
        ns = build_ns(wave_mode=True)
        assert ns["WAVE_OPENING_HERD"][0] == {"COW": 2, "SHEEP": 2}
        assert ns["WAVE_LAND_WAVES"][1][0] == 6      # NE d6
        assert ns["WAVE_LAND_WAVES"][2][0] == 10     # SW d10
        assert 3 not in ns["WAVE_LAND_WAVES"]        # SE 永不买
        # kaggri 一行开局：麦种 9 ∈ [5,10]（少买）、d0 过夜 ≤600
        wheat_seeds = ns["WAVE_OPENING_SEEDS"]["WHEAT"]
        assert 5 <= wheat_seeds <= 10
        d0_cost = (2 * ns["ANIMALS"]["COW"]["cost"]
                   + 2 * ns["ANIMALS"]["SHEEP"]["cost"]
                   + ns["WAVE_OPENING_SEEDS"]["MELON"]
                   * ns["CROPS"]["MELON"]["seed"]
                   + wheat_seeds * ns["CROPS"]["WHEAT"]["seed"])
        assert ns["WAVE_OPENING_EOD_CASH_MAX"] == 600
        assert d0_cost <= 3000 - ns["WAVE_OPENING_EOD_CASH_MAX"] + 5 * 26

    def test_v48_calendar_anchors(self):
        """v48 default 日历：crew 阶梯 6/8/12/13、瓜 7、d6 地+牛、d10 地。"""
        ns = build_ns(wave_mode=False)
        ladder = dict(ns["WAVE_CREW_LADDER"])
        assert ladder[5] == 6 and ladder[8] == 8
        assert ladder[10] == 12 and ladder[11] == 13
        assert ns["WAVE_OPENING_SEEDS"]["MELON"] == 7
        assert ns["WAVE_HERD_WAVES"][6] == {"COW": 5}
        assert ns["WAVE_LAND_WAVES"][1][0] == 6
        assert ns["WAVE_LAND_WAVES"][2][0] == 10

    def test_2945_day11_sheep_five_clips(self):
        """2945 VE1：day-11 放羊 = 5 次剪毛（首产夜 d16、间隔 3 →
        d16/19/22/25/28 五个生产夜，收割日 ≤29 全可变现）。"""
        ns = build_ns(wave_mode=False)
        spec = ns["ANIMALS"]["SHEEP"]
        placed = 11
        evenings = [placed + spec["first_yield_day"] - 1 + k * spec["interval"]
                    for k in range(5)]
        assert evenings == [16, 19, 22, 25, 28]
        assert evenings[-1] + 1 <= ns["SEASON_DAYS"] - 1 + 1  # d29 可卖
        assert 11 in ns["WAVE_HERD_WAVES_YARN"]


# ---------------------------------------------------------------------------
# 4) M-C 分派契约
# ---------------------------------------------------------------------------

class TestRuntimeDispatch:
    def _runtime(self):
        from kaggle_simulations.agent.planner import runtime, wave_script
        return runtime, wave_script

    def test_wave_candidate_key_and_overrides(self):
        _runtime, wave = self._runtime()
        cand = wave.wave_candidate()
        assert cand.key() == wave.WAVE_KEY
        assert cand.knob_overrides() == {"PLANNER_ENABLED": True,
                                         "PLANNER_OVERRIDES.wave_mode": True}
        assert cand.key() > "P|"          # 与 PlanSpec 键面不同域

    def test_spec_dispatch(self):
        from kaggle_simulations.agent.planner import plans
        runtime, wave = self._runtime()
        cand = wave.wave_candidate()
        assert runtime._spec_knob_overrides(cand) == \
            {"PLANNER_ENABLED": True, "PLANNER_OVERRIDES.wave_mode": True}
        spec = plans.identity_spec()
        assert runtime._spec_knob_overrides(spec) == \
            plans.plan_to_knob_overrides(spec)
        tail = {"day": 20, "herd": 12, "crops": {"STRAWBERRY": 20}}
        assert runtime._spec_tail_score(cand, tail, None) > 0.0

    def test_wave_absent_from_enumerate(self):
        """剧本不进旋钮变体枚举面（三选一里它是独立候选）。"""
        from kaggle_simulations.agent.planner import plans
        summary = plans.build_obs_summary(day=0, money=3000.0, herd=0,
                                          crops={}, unlocked_quadrants=1)
        assert all(not getattr(s, "wave", False)
                   for s in plans.enumerate_plans(summary))


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
