# 【中文】test_planner_calibration.py —— P2.6 投影校准契约测试（v3 轴更新）
# ===========================================================================
# 钉住 P2.6 有界迭代（2026-09-19）落进 planner 层的三类校准性质（v3 K3
# 日程轴拆分后沿 land_due_shift/herd_due_shift 两轴重述）：
#   1) 日程轴可投影性——project_season 对 land_due_shift 非增（早买地
#      不劣：产能更早解锁），钳位处允许平票；封笔日（d20）后日程无关
#      （诚实零方差）；herd_due_shift 只平移畜群爬坡（晚建不劣，反向
#      严格）；
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
                land_due_shift=0, herd_due_shift=0, sell_discount=0.9,
                liquidity_tier="STANDARD")
    base.update(kw)
    return plans.PlanSpec(**base)


# ===========================================================================
# 1) 日程轴可投影性（P2.6 修正 + v3 K3 拆分）
# ===========================================================================

class TestTimingAxisProjections:

    def test_land_shift_monotone_nondecreasing_toward_early(self):
        """开局态（d3、象限未满）：买地越早投影不劣（钳位处允许平票）。"""
        obs = _obs()
        vals = [plans.project_season(_spec(land_due_shift=s), obs)
                for s in plans.LAND_DUE_SHIFTS]      # [-2,-1,0,2,4]
        assert all(a >= b for a, b in zip(vals, vals[1:])), vals
        assert max(vals) > min(vals)                   # 轴不再是常数

    def test_late_game_timing_is_honestly_flat(self):
        """封笔日（day>=PLANT_LAST_DAY）：扩张归零、日程过期 → 日程恒平。"""
        obs = _obs(day=20, money=20000,
                   crops={"STRAWBERRY": 30, "WHEAT": 16, "MELON": 12},
                   unlocked_quadrants=3)
        vals = {plans.project_season(_spec(land_due_shift=s,
                                           capacity_tier="C2"), obs)
                for s in plans.LAND_DUE_SHIFTS}
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
        """买畜摊提限爬坡窗：总额守恒、时点只挪年金——早建畜群不劣。

        v3 K3：herd_due_shift 独立驱动（-1 提前一天），与买地轴解耦。"""
        obs = _obs(day=3, money=3000, herd=0,
                   crops={"STRAWBERRY": 0, "WHEAT": 18, "MELON": 0},
                   unlocked_quadrants=1,
                   daily_demand={"STRAWBERRY": 8.0, "WHEAT": 12.0,
                                 "MELON": 1.5})
        j0 = plans.project_season(_spec(herd_due_shift=0), obs)
        j_1 = plans.project_season(_spec(herd_due_shift=-1), obs)
        # -1 平移：爬坡起点早 1 天 → 年金全程领先；摊提总额不变
        # （窗平移不缩）。故 j_1 > j0 严格。
        assert j_1 > j0

    def test_land_and_herd_axes_are_independent(self):
        """K3 拆分的投影侧语义：land 轴动产能日程、herd 轴动年金日程，
        两轴同动不互相湮没（买地日程不再被买畜日程绑架，反之亦然）。
        注：两者经饲料耦合（herd 需求 vs 麦产量←产能←买地）存在真实
        交互，故只断言方向一致与边际同号，不断言精确可分。"""
        obs = _obs()
        j_land = plans.project_season(_spec(land_due_shift=-2), obs) - \
            plans.project_season(_spec(land_due_shift=0), obs)
        j_herd_on_late_land = plans.project_season(
            _spec(land_due_shift=-2, herd_due_shift=-1), obs) - \
            plans.project_season(_spec(land_due_shift=-2), obs)
        j_herd_on_base_land = plans.project_season(
            _spec(land_due_shift=0, herd_due_shift=-1), obs) - \
            plans.project_season(_spec(land_due_shift=0), obs)
        assert j_land > 0                      # 早买地产能更早
        assert j_herd_on_late_land > 0 and j_herd_on_base_land > 0


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
        """折扣单调（同参数包内）：identity（原生 1.0，K1 守成点）> 同档
        0.9 折扣计划。跨档的产能边（如 C1）可以合理压过折扣差——那是
        容量轴的语义，不是折扣轴的反例。"""
        obs = self._midgame_obs()
        hi = plans.project_season(plans.identity_spec(), obs)
        lo = plans.project_season(_spec(capacity_tier="C2",
                                        p3_mode="HEALTHY", p4_clear="MID",
                                        sell_discount=0.9), obs)
        assert hi > lo

    def test_deterministic(self):
        obs = _obs()
        assert plans.project_season(_spec(), obs) == \
            plans.project_season(_spec(), obs)


# ===========================================================================
# 3) 选择器聚合数学性质（P2.6 选参面 + v3 K1 近平守成）
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
        """日程先验：J 有区分度时 argmax 跟随 J；J 全等时才落字典序
        （v3 键编码：L0 原生锚 < LN 负档 < LP 正档，等值兄弟默认守成）。"""
        def key(shift):
            code = "0" if shift == 0 else (f"N{-shift}" if shift < 0
                                           else f"P{shift}")
            return f"P|C|B1|C1|HEALTHY|LOW|1.00|L{code}|H0|" \
                   f"LQ0|0.90"
        matrix = {key(-2): {"m": 10.0}, key(0): {"m": 9.0}, key(4): {"m": 8.0}}
        assert select.robust_select(matrix)["best"] == key(-2)
        tied = {key(s): {"m": 7.0} for s in plans.LAND_DUE_SHIFTS}
        best = select.robust_select(tied)["best"]
        assert best.endswith("L0|H0|LQ0|0.90")   # 字典序：L0（原生锚）最小
        assert select.robust_select(tied)["tie_break"] is not None

    def test_identity_near_tie_guard(self):
        """K1 近平守成：边际 <τ → identity；≥τ → 最优保持（确定性）。"""
        tau = select.IDENTITY_TIEBREAK_TAU
        ident = plans.identity_spec().key()
        other = "P|C|B2|C3|HEALTHY|LOW|1.00|L0|H0|LQ0|0.90"
        near = {ident: {"m": 100.0}, other: {"m": 100.0 + tau * 50.0}}
        assert select.robust_select(near, identity_key=ident)["best"] == ident
        far = {ident: {"m": 100.0},
               other: {"m": 100.0 + tau * 50.0 + 1.0}}
        assert select.robust_select(far, identity_key=ident)["best"] == other


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
                              weights=None, trim_fraction=0.25,
                              identity_key=None, **_kw):
                seen["strategy"] = strategy
                seen["weights"] = weights
                seen["trim"] = trim_fraction
                seen["identity_key"] = identity_key
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
