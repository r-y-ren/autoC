# 【中文】test_planner_calibration.py —— P2.6 投影校准契约测试
# ===========================================================================
# 钉住 P2.6 有界迭代（2026-09-19）落进 planner 层的三类校准性质：
#   1) 时点轴可投影性——project_season 对 timing_shift 非增（早买地/早建畜
#      群不劣），钳位处允许平票；封笔日（d20）后时点无关（诚实零方差）；
#   2) 保守偏置修正的回归钉——种子建植成本只在建设窗计一次、封笔后扩张
#      目标归零、买畜摊提限爬坡窗、买地日程制（无现金彩票）+产能耦合；
#   3) 选择器聚合数学性质——worst_case ≤ trimmed_mean、trim=0 退化为算术
#      平均、weighted 单调、tie-break 不再系统性偏袒 +0 时点。
# 纪律：与 test_planner_contract.py 同风格；全部确定性、stdlib-only。
# ===========================================================================

import importlib.util
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(HERE)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

from kaggle_simulations.agent.planner import plans, select  # noqa: E402


def _obs(**kw):
    base = dict(day=3, money=3000, herd=2,
                crops={"STRAWBERRY": 2, "WHEAT": 4, "MELON": 0},
                unlocked_quadrants=1,
                daily_demand={"STRAWBERRY": 3.0, "WHEAT": 10.0,
                              "MELON": 0.8})
    base.update(kw)
    return plans.build_obs_summary(**base)


def _spec(**kw):
    base = dict(opening="C", p1_branch="B2", capacity_tier="C1",
                p3_mode="HEALTHY", p4_clear="LOW", quota_scale=1.0,
                timing_shift=0, sell_discount=0.9)
    base.update(kw)
    return plans.PlanSpec(**base)


# ===========================================================================
# 1) 时点轴可投影性（P2.6 修正：修正前 J 对 timing_shift 恒零方差）
# ===========================================================================

class TestTimingAxisProjections:

    def test_timing_monotone_nondecreasing_toward_early_on_opening_state(self):
        """开局态（d3、象限未满）：时点越早投影不劣（钳位处允许平票）。"""
        obs = _obs()
        vals = [plans.project_season(_spec(timing_shift=s), obs)
                for s in plans.TIMING_SHIFTS]          # [-2,-1,0,1,2]
        assert all(a >= b for a, b in zip(vals, vals[1:])), vals
        assert max(vals) > min(vals)                   # 轴不再是常数

    def test_late_game_timing_is_honestly_flat(self):
        """封笔日（day>=PLANT_LAST_DAY）：扩张归零、日程过期 → 时点恒平。"""
        obs = _obs(day=20, money=20000,
                   crops={"STRAWBERRY": 30, "WHEAT": 16, "MELON": 12},
                   unlocked_quadrants=3)
        vals = {plans.project_season(_spec(timing_shift=s,
                                         capacity_tier="C2"), obs)
                for s in plans.TIMING_SHIFTS}
        assert len(vals) == 1                          # 全部相等

    def test_planting_closure_ignores_expansion_targets(self):
        """封笔后配额缩放不再影响田线（扩张既种不下也收不成）。"""
        obs = _obs(day=20, money=20000,
                   crops={"STRAWBERRY": 30, "WHEAT": 16, "MELON": 12},
                   unlocked_quadrants=3)
        a = plans.project_season(_spec(quota_scale=0.8), obs)
        b = plans.project_season(_spec(quota_scale=1.25), obs)
        assert a == b

    def test_seed_establishment_charged_once_within_build_window(self):
        """种子建植=建设窗一次性：宽档对窄档的 J 差等于解析式。

        旧实现漏窗口守卫、莓/瓜建植费被逐日重复计到季末（d10 放大
        ~20/3 倍、d20 达 20 倍）——本钉以解析等式防止回归。"""
        obs10 = _obs(day=10, money=5000, herd=8,
                     crops={"STRAWBERRY": 10, "WHEAT": 16, "MELON": 2},
                     unlocked_quadrants=3,
                     daily_demand={"STRAWBERRY": 8.0, "WHEAT": 12.0,
                                   "MELON": 1.5})
        # 全额健康（demand=REF→health=1）：莓/瓜日收入=格数×锚；种子
        # 总支出=(目标-现状)×单价（窗内摊提一次）。capacity=3×25=75 不钳。
        j08 = plans.project_season(_spec(capacity_tier="C3", quota_scale=0.8),
                                   obs10)
        j125 = plans.project_season(_spec(capacity_tier="C3",
                                          quota_scale=1.25), obs10)
        straw08, straw125 = 19, 30                     # round(24*q)
        melon08, melon125 = 10, 15                     # round(12*q)
        build_span = max(1, plans.STRAW_DEADLINE_DAY - 10)
        straw_days = melon_days = seed_frac = 0.0
        for day in range(10, 30):
            frac = 1.0 if day >= plans.PLANT_LAST_DAY else min(
                1.0, (day - 10) / build_span)
            straw_days += (straw125 - straw08) * frac
            melon_days += (melon125 - melon08) * frac
            if day < 10 + build_span:                  # 种子只摊提建设窗
                seed_frac += frac
        # 收入按折扣；种子建植=建设窗内 frac 加权摊提（不折扣）。
        analytic = (
            straw_days * plans.REVENUE_ANCHORS["STRAWBERRY"] * 0.9
            + melon_days * plans.REVENUE_ANCHORS["MELON"] * 0.9
            - (straw125 - straw08) * plans.SEED_PRICES["STRAWBERRY"]
            * seed_frac / build_span
            - (melon125 - melon08) * plans.SEED_PRICES["MELON"]
            * seed_frac / build_span
        )
        assert j125 - j08 == pytest.approx(analytic, abs=1.0)

    def test_capacity_coupling_values_land(self):
        """产能耦合：同计划在更多象限下投影更高（地有产能价值）。"""
        spec = _spec(capacity_tier="C1", quota_scale=1.25)
        j1 = plans.project_season(spec, _obs(unlocked_quadrants=1))
        j3 = plans.project_season(spec, _obs(unlocked_quadrants=3))
        assert j3 > j1

    def test_land_purchase_no_cash_lottery(self):
        """买地日程制：买入决策与现金水平无关（去彩票），只由日程定。"""
        spec = _spec(capacity_tier="C1", quota_scale=1.25)
        poor = plans.project_season(spec, _obs(money=100))
        rich = plans.project_season(spec, _obs(money=50000))
        # 现金不进入任何购买决策/收入耦合，J 差恰为起始现金差。
        assert rich - poor == pytest.approx(49900.0, abs=0.5)

    def test_herd_cost_window_matches_docstring_amortization(self):
        """买畜摊提限爬坡窗：总额守恒、时点只挪年金——早建畜群不劣。"""
        obs = _obs(day=3, money=3000, herd=0,
                   crops={"STRAWBERRY": 0, "WHEAT": 18, "MELON": 0},
                   unlocked_quadrants=1,
                   daily_demand={"STRAWBERRY": 8.0, "WHEAT": 12.0,
                                 "MELON": 1.5})
        j0 = plans.project_season(_spec(timing_shift=0), obs)
        j2 = plans.project_season(_spec(timing_shift=2), obs)
        # +2 平移：爬坡起点晚 2 天（herd_start 2→4，钳位不触发）→ 年金
        # 全程落后；摊提总额不变（窗平移不缩）。故 j0 > j2 严格，差值上界
        # = 推迟 2 天的年金积分 < 3 天全额年金。
        assert j0 > j2
        assert (j0 - j2) < 3.0 * 17 * plans.REVENUE_ANCHORS["HERD"] * 0.9


# ===========================================================================
# 2) 投影器仍满足的既有序性质（P2.6 修正不得破坏）
# ===========================================================================

class TestOrderingPropertiesPreserved:

    def _midgame_obs(self):
        return _obs(day=10, money=5000, herd=8,
                    crops={"STRAWBERRY": 10, "WHEAT": 16, "MELON": 2},
                    unlocked_quadrants=2,
                    daily_demand={"STRAWBERRY": 5.0, "WHEAT": 12.0,
                                  "MELON": 1.0})

    def test_monotone_in_pressure_all_tiers(self):
        obs = self._midgame_obs()
        for tier in plans.CAPACITY_TIERS:
            spec = _spec(capacity_tier=tier)
            neutral = plans.project_season(spec, obs, {})
            pessim = plans.project_season(spec, obs, {"STRAWBERRY": 0.75})
            assert neutral > pessim, tier

    def test_monotone_in_discount_all_tiers(self):
        obs = self._midgame_obs()
        for tier in plans.CAPACITY_TIERS:
            hi = plans.project_season(_spec(capacity_tier=tier,
                                            sell_discount=0.9), obs)
            lo = plans.project_season(_spec(capacity_tier=tier,
                                            sell_discount=0.75), obs)
            assert hi > lo, tier

    def test_deterministic(self):
        obs = _obs()
        assert plans.project_season(_spec(), obs) == \
            plans.project_season(_spec(), obs)


# ===========================================================================
# 3) 选择器聚合数学性质（P2.6 选参面）
# ===========================================================================

class TestAggregationProperties:

    SCORES = {"m_a": 1.0, "m_b": 2.0, "m_c": 5.0, "m_d": 40.0}

    def test_trim_zero_is_plain_mean(self):
        mean = sum(self.SCORES.values()) / len(self.SCORES)
        assert select.aggregate_scores(self.SCORES, "trimmed_mean",
                                       trim_fraction=0.0) == \
            pytest.approx(mean)

    def test_worst_case_never_above_trimmed_mean(self):
        worst = select.aggregate_scores(self.SCORES, "worst_case")
        trimmed = select.aggregate_scores(self.SCORES, "trimmed_mean")
        assert worst <= trimmed

    def test_weighted_monotone_and_normalizes(self):
        weights = {"m_a": 1.0, "m_b": 1.0, "m_c": 1.0, "m_d": 1.0}
        even = select.aggregate_scores(self.SCORES, "weighted",
                                       weights=weights)
        assert even == pytest.approx(sum(self.SCORES.values()) / 4.0)
        tilted = dict(weights)
        tilted["m_a"] = 10.0                        # 低分模型加权 → 拉低
        assert select.aggregate_scores(self.SCORES, "weighted",
                                       weights=tilted) < even

    def test_timing_axis_not_pinned_to_zero_by_tie_break(self):
        """时点先验：J 有区分度时 argmax 跟随 J；J 全等时才落字典序。"""
        matrix = {
            "P|C|B1|C1|HEALTHY|LOW|1.00|-2|0.90": {"m": 10.0},
            "P|C|B1|C1|HEALTHY|LOW|1.00|+0|0.90": {"m": 9.0},
            "P|C|B1|C1|HEALTHY|LOW|1.00|+2|0.90": {"m": 8.0},
        }
        assert select.robust_select(matrix)["best"].endswith("-2|0.90")
        tied = {
            "P|C|B1|C1|HEALTHY|LOW|1.00|%+d|0.90" % s: {"m": 7.0}
            for s in plans.TIMING_SHIFTS}
        best = select.robust_select(tied)["best"]
        assert best.endswith("+0|0.90")            # 字典序：+0 最小
        assert select.robust_select(tied)["tie_break"] is not None


# ===========================================================================
# 4) bench 侧可配置 Ω（P2.6 选参轴的管线钉）
# ===========================================================================

class TestBenchConfigurableOmega:

    def _load_bench(self):
        path = os.path.join(SOFTWARE, "scripts", "planner_offline_bench.py")
        spec = importlib.util.spec_from_file_location(
            "planner_offline_bench_calib_test", path)
        module = importlib.util.module_from_spec(spec)
        sys.modules.setdefault("planner_offline_bench_calib_test", module)
        spec.loader.exec_module(module)
        return module

    def test_build_default_models_consumes_custom_pessimistic(self):
        from kaggle_simulations.agent.planner import opponents
        custom = opponents.PessimisticFill(price_discount=0.9)
        models = opponents.build_default_models(pessimistic=custom)
        assert models[3] is custom
        assert "0.9" in models[3].describe()

    def test_evaluate_injection_honours_selector_cfg(self, monkeypatch):
        """cfg 的 strategy/trim/weights/pessimistic 全链路进入 J 聚合。"""
        bench = self._load_bench()
        seen = {}

        class _FakeSelect:
            AGGREGATION_STRATEGIES = select.AGGREGATION_STRATEGIES
            DEFAULT_TRIM_FRACTION = select.DEFAULT_TRIM_FRACTION

            @staticmethod
            def robust_select(j_matrix, strategy="trimmed_mean",
                              weights=None, trim_fraction=0.25):
                seen["strategy"] = strategy
                seen["weights"] = weights
                seen["trim"] = trim_fraction
                seen["n_plans"] = len(j_matrix)
                key = sorted(j_matrix)[0]
                return {"best": key, "ranking": [(key, 0.0)],
                        "strategy": strategy, "tie_break": None,
                        "aggregates": {k: 0.0 for k in j_matrix}}

        class _FakeModel:
            name = "pessimistic_fill"

            def supply_pressure(self, obs_summary):
                return {"STRAWBERRY": 0.9}

            def describe(self):
                return "fake"

        monkeypatch.setattr(bench.select, "robust_select",
                            _FakeSelect.robust_select)
        monkeypatch.setattr(bench.opponents, "build_default_models",
                            lambda history=None, profile_path=None,
                            pessimistic=None: [_FakeModel()])
        monkeypatch.setattr(bench.plans, "enumerate_plans",
                            lambda obs_summary: [_spec(quota_scale=0.8),
                                                 _spec(quota_scale=1.25)])
        monkeypatch.setattr(bench.plans, "project_season",
                            lambda spec, obs, pressure: 1.0)
        monkeypatch.setattr(
            bench, "build_obs_summary_from_state",
            lambda deps, state, seat, day: plans.build_obs_summary(
                day=day, money=1000.0, herd=0, crops={}, unlocked_quadrants=1))

        class _StubDeps:
            def get(self, k, default=None):
                return {"v13_available": False}.get(k, default)

            def __getitem__(self, k):
                if k == "transition_actions":
                    return lambda replay: [None] * 600
                if k == "build":
                    return lambda replay, step: object()
                if k == "run_to_end":
                    return lambda state, actions: None
                if k == "final":
                    return lambda state: [111.0, 222.0]
                if k == "shops":
                    return {}
                if k == "towncenter":
                    return ()
                if k == "v13_available":
                    return False
                raise KeyError(k)

        row = bench.evaluate_injection(
            _StubDeps(), {}, 0, 72,
            {"episode": "t", "strategy": "weighted",
             "trim_fraction": 0.1,
             "weights": {"pessimistic_fill": 0.5},
             "pessimistic": None, "oracle": False})
        assert seen["strategy"] == "weighted"
        assert seen["weights"] == {"pessimistic_fill": 0.5}
        assert seen["trim"] == 0.1
        assert seen["n_plans"] == 2
        assert row["best_plan"] == _spec(quota_scale=0.8).key()
