"""Track-B P2 规划器契约测试（plans/opponents/select + planner_offline_bench）。

覆盖面（对应任务包判据）：
  1. PlanSpec 哈希/序列化稳定 + 越界值显式异常（带失败示例）；
  2. enumerate_plans：<=120 上限、确定性、过滤规则 R1-R6 逐条、
     R8 预算分配的 (tier,branch) 覆盖性；
  3. plan_to_knob_overrides：真实 v1.5 旋钮名映射 + 缺口键（PLANNER_LOCAL）；
  4. 选择器聚合数学性质：单调性/平票确定性/加权与截尾的非法输入；
  5. 悲观成交折扣生效 + 被动外推直方图 + 冻结画像缺失 no-op；
  6. bench harness 的注入/对比/归因逻辑（确定性 mini-stub 伪 twin）；
  7. 真 twin 集成（skip-unless-importable；语料缺失同样 skip）。

全程 stdlib-only、不依赖网络；时长预算 <90s（集成段单注入点 ~5s）。
"""

from __future__ import annotations

import json
import sys
import types
from pathlib import Path

import pytest

SOFTWARE = Path(__file__).resolve().parents[1]
if str(SOFTWARE) not in sys.path:
    sys.path.insert(0, str(SOFTWARE))

from kaggle_simulations.agent.planner import plans  # noqa: E402
from kaggle_simulations.agent.planner import opponents  # noqa: E402
from kaggle_simulations.agent.planner import select  # noqa: E402

BENCH_SCRIPT = SOFTWARE / "scripts" / "planner_offline_bench.py"
REPLAY_ROOT = SOFTWARE.parent / "references" / "data" / "online-replays"


def _load_bench():
    """按脚本路径装载 bench 模块（twin 缺失的机器上仅纯函数可用）。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "planner_offline_bench_test", str(BENCH_SCRIPT))
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("planner_offline_bench_test", module)
    spec.loader.exec_module(module)
    return module


# ===========================================================================
# 1) PlanSpec：哈希/序列化/校验
# ===========================================================================

def _spec(**kw):
    base = dict(opening="C", p1_branch="B2", capacity_tier="C3",
                p3_mode="HEALTHY", p4_clear="LOW", quota_scale=1.0,
                timing_shift=0, sell_discount=0.9)
    base.update(kw)
    return plans.PlanSpec(**base)


class TestPlanSpecContract:

    def test_hash_and_equality_stable(self):
        a = _spec(quota_scale=1.25, timing_shift=-2)
        b = _spec(quota_scale=1.25, timing_shift=-2)
        assert a == b and hash(a) == hash(b)
        assert hash(plans.PlanSpec.from_json(a.to_json())) == hash(a)
        assert a != _spec(timing_shift=2)          # +2/-2 可区分
        assert len({a, b, _spec()}) == 2           # 可入集合

    def test_json_roundtrip_and_stable_text(self):
        a = _spec(p4_clear="HEAVY", sell_discount=0.75)
        text = a.to_json()
        assert text == json.dumps(a.to_dict(), sort_keys=True)
        assert plans.PlanSpec.from_json(text) == a
        assert text == a.to_json()                 # 两次序列化逐字节相同

    def test_key_is_canonical_and_sortable(self):
        keys = sorted(_spec(quota_scale=q).key() for q in plans.QUOTA_SCALES)
        assert len(set(keys)) == 3
        assert _spec().key().startswith("P|C|B2|C3|")

    def test_invalid_axes_raise_with_example(self):
        with pytest.raises(ValueError) as exc:
            plans.PlanSpec(opening="X", p1_branch="B2", capacity_tier="C3",
                           p3_mode="HEALTHY", p4_clear="LOW",
                           quota_scale=1.0, timing_shift=0,
                           sell_discount=0.9)
        assert "示例" in str(exc.value)
        with pytest.raises(ValueError):
            _spec(quota_scale=1.3)                 # 25% 网格之外
        with pytest.raises(ValueError):
            _spec(timing_shift=3)

    def test_from_dict_fail_closed(self):
        with pytest.raises(ValueError):
            plans.PlanSpec.from_dict({"opening": "C"})
        with pytest.raises(ValueError):
            plans.PlanSpec.from_dict(dict(_spec().to_dict(), typo=1))


# ===========================================================================
# 2) enumerate_plans：上限/确定性/过滤规则
# ===========================================================================

class TestEnumeratePlans:

    def test_day0_within_cap_and_full_tier_branch_coverage(self):
        obs = plans.build_obs_summary(
            day=0, money=3000, herd=0, crops={}, unlocked_quadrants=1,
            daily_demand={"STRAWBERRY": 4, "WHEAT": 10})
        plan_list, notes = plans.enumerate_plans_audited(obs)
        assert 0 < len(plan_list) <= plans.MAX_PLAN_CANDIDATES
        assert {"C1", "C2", "C3"} <= {p.capacity_tier for p in plan_list}
        assert {"B1", "B2"} <= {p.p1_branch for p in plan_list}
        assert len({p.key() for p in plan_list}) == len(plan_list)
        assert any(n.startswith("R8") for n in notes)

    def test_determinism_same_input_same_output(self):
        obs = plans.build_obs_summary(
            day=10, money=5000, herd=8, crops={"STRAWBERRY": 10, "WHEAT": 16},
            unlocked_quadrants=2, daily_demand={"STRAWBERRY": 5})
        a = [p.key() for p in plans.enumerate_plans(obs)]
        b = [p.key() for p in plans.enumerate_plans(obs)]
        assert a == b and 0 < len(a) <= plans.MAX_PLAN_CANDIDATES

    def test_r1_opening_frozen_after_day3(self):
        obs = plans.build_obs_summary(
            day=3, money=3000, herd=0, crops={}, unlocked_quadrants=1,
            opening_played="B", daily_demand={})
        plan_list = plans.enumerate_plans(obs)
        assert plan_list and {p.opening for p in plan_list} == {"B"}

    def test_r2_branch_by_opp_class(self):
        for cls, want in (("burst", "B1"), ("reduced", "B2"),
                          ("deferred", "B2"), ("melon_first", "B3")):
            obs = plans.build_obs_summary(
                day=1, money=3000, herd=0, crops={}, unlocked_quadrants=1,
                opp_class=cls, daily_demand={})
            plan_list = plans.enumerate_plans(obs)
            assert plan_list and {p.p1_branch for p in plan_list} == {want}

    def test_r3_d6_gate(self):
        base = dict(day=6, money=9000, herd=12, unlocked_quadrants=2,
                    crops={"STRAWBERRY": 8, "WHEAT": 16},
                    daily_demand={"STRAWBERRY": 5})
        all_pass = plans.enumerate_plans(
            plans.build_obs_summary(d6_checks=[True] * 5, **base))
        assert {p.capacity_tier for p in all_pass} >= {"C1", "C3"}
        q1_fail = plans.enumerate_plans(
            plans.build_obs_summary(d6_checks=[False, True, True, True, True],
                                    **base))
        assert {p.capacity_tier for p in q1_fail} == {"C3"}   # q1 挂：C1/C2 皆禁

    def test_r4_r5_late_game_freeze(self):
        obs = plans.build_obs_summary(
            day=25, money=2000, herd=12, crops={"STRAWBERRY": 20},
            unlocked_quadrants=3, opening_played="C", opp_class="burst",
            d6_checks=[True] * 5, p4_tier="MID", daily_demand={"STRAWBERRY": 6})
        plan_list = plans.enumerate_plans(obs)
        assert plan_list
        assert {p.p3_mode for p in plan_list} == {"CATCHUP"}   # d12 现金 8k 分界
        assert {p.p4_clear for p in plan_list} == {"MID"}

    def test_r6_opening_cash_gate(self):
        obs = plans.build_obs_summary(
            day=0, money=1600, herd=0, crops={}, unlocked_quadrants=1,
            daily_demand={})
        plan_list = plans.enumerate_plans(obs)
        assert {p.opening for p in plan_list} <= {"B", "C"}    # A(1800) 买不起

    def test_build_obs_summary_rejects_unknown_crop(self):
        with pytest.raises(ValueError):
            plans.build_obs_summary(day=0, money=1, herd=0,
                                    crops={"PUMPKIN": 1},
                                    unlocked_quadrants=1)


# ===========================================================================
# 3) plan_to_knob_overrides：旋钮映射 + 缺口键
# ===========================================================================

class TestKnobOverrides:

    def test_base_plan_quota_and_timing(self):
        obs = plans.build_obs_summary(day=12, money=9000, herd=12,
                                      crops={"STRAWBERRY": 20, "WHEAT": 16},
                                      unlocked_quadrants=3,
                                      opening_played="C", opp_class="burst",
                                      d6_checks=[True] * 5,
                                      daily_demand={"STRAWBERRY": 6})
        plan_list = plans.enumerate_plans(obs)
        base = next(p for p in plan_list if p.capacity_tier == "C1"
                    and p.quota_scale == 1.0 and p.timing_shift == 0
                    and p.sell_discount == 0.9)
        ov = plans.plan_to_knob_overrides(base)
        assert ov["PACK"] == "VOLUME_CROP"
        assert ov["_VOLUME_PLAN.straw_total_cap"] == 48
        assert ov["LINE_CAPS.STRAWBERRY"] == 48
        assert ov["SE_DUE_DAY"] == plans.SE_DUE_DAY_DEFAULT
        assert ov["LAND_PLAN.1"] == (4, 1700) and ov["LAND_PLAN.2"] == (7, 2700)
        # 卖出折扣→囤货门槛耦合（缺口清单第 1 条的唯一近似杠杆）
        assert ov["SELL_PLAN_HOLD_EDGE"] == 1.09

    def test_scaled_and_shifted(self):
        spec = _spec(capacity_tier="C1", quota_scale=1.25, timing_shift=-2,
                     sell_discount=0.75)
        ov = plans.plan_to_knob_overrides(spec)
        assert ov["_VOLUME_PLAN.straw_total_cap"] == 60        # 48*1.25
        assert ov["LINE_CAPS.MELON"] == 15                     # 12*1.25
        assert ov["SE_DUE_DAY"] == 8                           # 10-2
        assert ov["LAND_PLAN.1"] == (2, 1700) and ov["LAND_PLAN.2"] == (5, 2700)
        assert ov["SELL_PLAN_HOLD_EDGE"] == 1.15               # 悲观→早卖
        # 缺口清单：规划器本地键必须显式存在（执行器侧跳过）
        assert ov["PLANNER_LOCAL.sell_discount"] == 0.75
        assert ov["PLANNER_LOCAL.animal_buy_day_shift"] == -2
        assert ov["PLANNER_LOCAL.p3_mode"] == "HEALTHY"

    def test_deterministic_key_order(self):
        a = plans.plan_to_knob_overrides(_spec())
        b = plans.plan_to_knob_overrides(_spec())
        assert list(a.keys()) == list(b.keys())
        assert list(a.keys()) == sorted(a.keys())


# ===========================================================================
# 4) project_season：相对排序性质
# ===========================================================================

class TestProjectSeason:

    def _obs(self):
        return plans.build_obs_summary(
            day=10, money=5000, herd=8, crops={"STRAWBERRY": 10, "WHEAT": 16,
                                               "MELON": 2},
            unlocked_quadrants=2, daily_demand={"STRAWBERRY": 5, "WHEAT": 12,
                                                "MELON": 1.0})

    def test_deterministic(self):
        spec = _spec()
        assert plans.project_season(spec, self._obs()) == \
            plans.project_season(spec, self._obs())

    def test_monotone_in_pressure_and_discount(self):
        spec = _spec()
        pessim = plans.project_season(spec, self._obs(),
                                      {"STRAWBERRY": 0.75})
        neutral = plans.project_season(spec, self._obs(), {})
        assert neutral > pessim                  # 悲观压价必然降低投影
        hi = _spec(sell_discount=0.9)
        lo = _spec(sell_discount=0.75)
        assert plans.project_season(hi, self._obs()) > \
            plans.project_season(lo, self._obs())

    def test_differentiates_tiers(self):
        vals = {tier: plans.project_season(_spec(capacity_tier=tier),
                                           self._obs())
                for tier in plans.CAPACITY_TIERS}
        assert len(set(vals.values())) == 3


# ===========================================================================
# 5) 对手模型集 Ω
# ===========================================================================

class TestOpponentModels:

    def test_passive_extrapolation_histogram(self):
        model = opponents.PassiveExtrapolation(window=3)
        history = [{"day": d, "sells": {"WHEAT": 10 + 2 * d},
                    "animal_buys": 0} for d in range(3)]
        action = model.propose_actions({"history": history}, 3)
        assert action["farmer"] == ["PASS"]
        assert action["market"] == [["SELL", "WHEAT", 12]]   # (10+12+14)/3
        # 冷启动：诚实 PASS（不编造节奏）
        cold = model.propose_actions({"history": []}, 0)
        assert cold == {"farmer": ["PASS"], "hands": [], "market": []}
        assert model.supply_pressure({}) == {}

    def test_passive_market_order_cap(self):
        model = opponents.PassiveExtrapolation()
        sells = {f"ITEM{i}": 1 for i in range(14)}
        action = model.propose_actions({"history": [{"day": 0, "sells": sells,
                                                     "animal_buys": 0}]}, 1)
        assert len(action["market"]) <= 10                   # 官方语义上限

    def test_frozen_style_pool_missing_profile_noop(self):
        model = opponents.FrozenStylePool(profile_path=None)
        assert not model.available
        action = model.propose_actions({"shed": {"WHEAT": 50}}, 7)
        assert action["farmer"] == ["PASS"] and action["market"] == []
        assert "不伪造" in model.describe()

    def test_frozen_style_pool_with_profile(self, tmp_path):
        profile = {"styles": [{"name": "rancher", "herd_target": 14,
                               "animal": "COW",
                               "crop_pref": {"MILK": 2.0, "WHEAT": 1.0},
                               "daily_sell_cap": 6}]}
        path = tmp_path / "profile.json"
        path.write_text(json.dumps(profile), encoding="utf-8")
        model = opponents.FrozenStylePool(profile_path=str(path))
        assert model.available
        action = model.propose_actions(
            {"shed": {"MILK": 10, "WHEAT": 10}, "herd": 5, "money": 4000}, 7)
        ops = action["market"]
        assert ["SELL", "MILK", 4] in ops                   # 6×2/3
        assert ["SELL", "WHEAT", 2] in ops                  # 6×1/3
        assert ["BUY_ANIMAL", "COW", 1] in ops              # 5<14 且现金宽裕

    def test_pessimistic_fill_dump_and_discount(self):
        model = opponents.PessimisticFill()                  # 默认 0.75
        assert model.price_discount == 0.75
        action = model.propose_actions(
            {"our_sell_plan": {"STRAWBERRY": 8, "MELON": 3}}, 10)
        assert action["market"] == [["SELL", "MELON", 3],
                                    ["SELL", "STRAWBERRY", 8]]
        pressure = model.supply_pressure({})
        assert pressure["STRAWBERRY"] == 0.75 and pressure["WHEAT"] == 0.75
        # 我方无卖单 → 无倾销
        assert model.propose_actions({"our_sell_plan": {}}, 11)["market"] == []

    def test_pessimistic_fill_validation(self):
        with pytest.raises(ValueError):
            opponents.PessimisticFill(price_discount=1.5)
        with pytest.raises(ValueError):
            opponents.PessimisticFill(dump_ratio=0.0)

    def test_default_model_set_shape(self):
        models = opponents.build_default_models(history=[])
        assert [m.name for m in models] == ["passive_extrapolation",
                                            "frozen_style_pool",
                                            "pessimistic_fill"]


# ===========================================================================
# 6) 鲁棒选择器：聚合数学性质
# ===========================================================================

class TestRobustSelect:

    def test_aggregation_known_values(self):
        scores = {"a": 1.0, "b": 2.0, "c": 3.0, "d": 4.0}
        assert select.aggregate_scores(scores, "worst_case") == 1.0
        assert select.aggregate_scores(scores, "weighted",
                                       weights={"a": 1, "b": 1, "c": 1,
                                                "d": 1}) == 2.5
        # trimmed_mean：n=4、trim=0.25 → 每端裁 1 → (2+3)/2
        assert select.aggregate_scores(scores, "trimmed_mean") == 2.5
        assert select.aggregate_scores({"only": 7.0}, "trimmed_mean") == 7.0

    def test_monotonicity_property(self):
        base = {"m1": 10.0, "m2": 20.0, "m3": 30.0, "m4": 40.0}
        for strategy in ("trimmed_mean", "worst_case", "weighted"):
            weights = {"m1": 1, "m2": 2, "m3": 1, "m4": 1}
            ref = select.aggregate_scores(base, strategy,
                                          weights=weights)
            for raised in ("m1", "m2", "m3", "m4"):
                bumped = dict(base)
                bumped[raised] += 5.0
                assert select.aggregate_scores(
                    bumped, strategy, weights=weights) >= ref, (
                    strategy, raised)

    def test_tie_break_lexicographic_and_order_free(self):
        matrix = {"plan_b|1": {"m1": 5.0}, "plan_a|2": {"m1": 5.0},
                  "plan_c|3": {"m1": 1.0}}
        result = select.robust_select(matrix)
        assert result["best"] == "plan_a|2"
        assert result["tie_break"] and "字典序" in result["tie_break"]
        shuffled = {"plan_c|3": {"m1": 1.0}, "plan_a|2": {"m1": 5.0},
                    "plan_b|1": {"m1": 5.0}}
        assert select.robust_select(shuffled)["best"] == "plan_a|2"
        assert result["ranking"][0][1] == result["ranking"][1][1] == 5.0

    def test_input_errors(self):
        with pytest.raises(ValueError):
            select.aggregate_scores({}, "trimmed_mean")
        with pytest.raises(ValueError):
            select.aggregate_scores({"a": 1.0}, "mean")
        with pytest.raises(ValueError):
            select.aggregate_scores({"a": 1.0}, "weighted")     # 缺 weights
        with pytest.raises(ValueError):
            select.aggregate_scores({"a": 1.0}, "weighted",
                                    weights={"a": -1.0})
        with pytest.raises(ValueError):
            select.robust_select({})
        with pytest.raises(ValueError):
            select.aggregate_scores({"a": 1.0}, "trimmed_mean",
                                    trim_fraction=0.5)


# ===========================================================================
# 7) bench harness 逻辑（mini-stub 伪 twin，不依赖真 twin/真回放）
# ===========================================================================

class _StubEnv:
    def __init__(self):
        self.configuration = {"episodeSteps": 24}

    @property
    def done(self):
        return False


class _StubState:
    """最小孪生替身：money 随我方动作语义推进；观察面够 obs_summary 用。"""

    def __init__(self, money0, steps_left):
        self.money = list(money0)
        self.steps_left = steps_left
        self.env = _StubEnv()
        farms = [{"money": float(m), "tiles": [[None] * 4 for _ in range(4)],
                  "unlocked_quadrants": ["NW"]} for m in money0]
        self.seats = []
        for i in range(2):
            obs = types.SimpleNamespace(
                farms=farms, market={"prices": {"STRAWBERRY": 120.0}},
                town={"unlocked_shops": ["YARN_STORE"]}, day=0, hour=0,
                step=0, player=i, private={}, remainingOverageTime=None)
            self.seats.append(types.SimpleNamespace(observation=obs))


def _make_stub_deps(dtsp_gain=10.0, reactive_gain=100.0):
    """deps 契约的确定性替身：反应式每步 +reactive_gain、DTSP 每步
    +dtsp_gain（经由 overrides 是否为 None 区分）；对手动作不影响资金。"""
    bench = _load_bench()

    def build(replay, step):
        rewards = replay["rewards"]
        return _StubState([rewards[0], rewards[1]], steps_left=24)

    def transition_actions(replay):
        return [[None, ["PASS"]] for _ in range(len(replay["steps"]) - 1)]

    def run_to_end(state, actions):
        for _ in actions:
            state.steps_left -= 1
        return state

    def step(state, pair):
        mine, _theirs = pair
        state.steps_left -= 1
        if mine is None:
            pass
        elif mine == "__reactive__":
            state.money[0] += reactive_gain
        else:
            state.money[0] += dtsp_gain
        return state

    def v13_factory(overrides=None):
        if overrides:
            return (lambda obs: "__dtsp__"), [], []
        return (lambda obs: "__reactive__"), [], []

    return {"build": build, "transition_actions": transition_actions,
            "run_to_end": run_to_end, "step": step,
            "final": lambda s: [float(m) for m in s.money],
            "shops": {"YARN_STORE": ["WOOL"]}, "towncenter": (),
            "v13_available": True, "v13_factory": v13_factory,
            "_bench": bench}


def _stub_replay(n_steps=24):
    return {"rewards": [5000.0, 4000.0],
            "steps": [{"actions": None} for _ in range(n_steps)]}


@pytest.mark.skipif(BENCH_SCRIPT.parent.name != "scripts",
                    reason="bench 脚本不在位")
class TestBenchLogic:

    def test_select_injection_steps(self):
        bench = _load_bench()
        assert bench.select_injection_steps(720, (3, 10, 20)) == [72, 240, 480]
        assert bench.select_injection_steps(100, (3, 10, 20)) == [72, 98]
        assert bench.select_injection_steps(720, (5, 3, 5)) == [72, 120]
        with pytest.raises(ValueError):
            bench.select_injection_steps(1, (3,))

    def test_compute_town_demand_engine_semantics(self):
        bench = _load_bench()
        shops = {"BAKERY": ["EGG", "WHEAT"], "YARN_STORE": ["WOOL"],
                 "PET_CAFE": ["CARROT"]}
        demand = bench.compute_town_demand(
            shops, ["BAKERY", "YARN_STORE"],
            towncenter_products=("FERTILIZER", "WHEAT"))
        # 每 4 步 1 抽 → 6 抽/日，两产品店各分一半；单产品店 12/日；镇心 +1
        assert abs(demand["EGG"] - 3.0) < 1e-9
        assert abs(demand["WHEAT"] - 4.0) < 1e-9     # 3 + 镇心 1
        assert abs(demand["WOOL"] - 12.0) < 1e-9     # 12；镇心抽取列表无毛
        assert "FERTILIZER" not in demand

    def test_extract_opponent_history(self):
        bench = _load_bench()
        replay = {"steps": [
            None,                                             # t=0 头部
            {"0": {"action": None},
             "1": {"action": {"market": [["SELL", "WHEAT", 5]]}}},
            {"0": {"action": None},
             "1": {"action": {"market": [["SELL", "WHEAT", 2],
                                         ["BUY_ANIMAL", "COW", 1]]}}},
            {"0": {"action": None}, "1": {"action": None}},
        ]}
        history = bench.extract_opponent_history(replay, 1, 3)
        # t=0..2 三次转移全部落在 day 0（24 步/日）；t=2 动作为 None
        assert history == [{"day": 0, "sells": {"WHEAT": 7},
                            "animal_buys": 1}]

    def test_attribute_failure_paths(self):
        bench = _load_bench()
        ok = bench.attribute_failure(0.0, 100.0, 90.0, 105.0, None, None,
                                     "k", eps=1.0)
        assert ok == {"judge_fail": False, "twin_noise": False,
                      "opponent_model_gap": False, "plan_space_gap": False,
                      "reason": "pass"}
        noise = bench.attribute_failure(50.0, 100.0, 90.0, 50.0, None, None,
                                        "k")
        assert noise["twin_noise"] and not noise["plan_space_gap"]
        model_gap = bench.attribute_failure(0.0, 100.0, 90.0, 80.0, 99.0,
                                            "other", "k")
        assert model_gap["opponent_model_gap"]
        space_gap = bench.attribute_failure(0.0, 100.0, 90.0, 80.0, 80.0,
                                            "k", "k")
        assert space_gap["plan_space_gap"] \
            and not space_gap["opponent_model_gap"]

    def test_apply_knob_overrides_paths(self):
        bench = _load_bench()
        ns = {"SE_DUE_DAY": 10, "LINE_CAPS": {"MELON": 12},
              "LAND_PLAN": {1: (4, 1700), 2: (7, 2700)}}
        overrides = {"SE_DUE_DAY": 8, "LINE_CAPS.MELON": 15,
                     "LAND_PLAN.1": (2, 1700),
                     "PLANNER_LOCAL.sell_discount": 0.75, "PACK": "MIXED",
                     "NOT_A_KNOB": 1, "GHOST.cap": 2}
        applied, skipped = bench.apply_knob_overrides(ns, overrides)
        assert ns["SE_DUE_DAY"] == 8
        assert ns["LINE_CAPS"]["MELON"] == 15
        assert ns["LAND_PLAN"][1] == (2, 1700)              # 整数键路径
        skipped_by_key = dict(skipped)
        assert "planner-local" in skipped_by_key["PLANNER_LOCAL.sell_discount"]
        assert "planner-local" in skipped_by_key["PACK"]
        assert "NOT_A_KNOB" in skipped_by_key and "GHOST.cap" in skipped_by_key
        assert set(applied) == {"SE_DUE_DAY", "LINE_CAPS.MELON",
                                "LAND_PLAN.1"}

    def test_evaluate_injection_stub_dtsp_wins(self):
        deps = _make_stub_deps(dtsp_gain=200.0, reactive_gain=100.0)
        bench = deps["_bench"]
        if bench.TWIN_IMPORT_ERROR is not None:
            pytest.skip("planner 模块导入不可用（twin 未合流机器）")
        row = bench.evaluate_injection(deps, _stub_replay(), 0, 12,
                                       {"episode": "stub", "oracle": False})
        assert row["twin_noise"] == 0.0                     # stub 重演=真值
        assert row["dtsp_vs_reactive"] > 0 and row["dtsp_vs_history"] > 0
        assert not row["judge_fail"]
        assert row["n_plans"] <= 120 and row["best_plan"]

    def test_evaluate_injection_stub_plan_space_gap(self):
        # DTSP 增益低于反应式 → judge_fail → oracle(全部=dtsp 增益)
        # 越不过反应式 → plan_space_gap
        deps = _make_stub_deps(dtsp_gain=10.0, reactive_gain=100.0)
        bench = deps["_bench"]
        if bench.TWIN_IMPORT_ERROR is not None:
            pytest.skip("planner 模块导入不可用（twin 未合流机器）")
        row = bench.evaluate_injection(deps, _stub_replay(), 0, 12,
                                       {"episode": "stub", "oracle": True,
                                        "oracle_top_k": 3})
        assert row["judge_fail"] and row["dtsp_vs_reactive"] < 0
        assert row["oracle_best"] is not None
        assert row["plan_space_gap"] and not row["opponent_model_gap"]
        assert not row["twin_noise_flag"]


# ===========================================================================
# 8) 真 twin 集成（skip-unless-importable；语料缺失同 skip）
# ===========================================================================

def _twin_ready():
    try:
        from kaggle_simulations.agent.planner import twin  # noqa: F401
        twin.load_engine()
        return True
    except Exception:                                      # noqa: BLE001
        return False


@pytest.mark.skipif(not _twin_ready(), reason="真 twin 不可导入/指纹不符")
class TestTrueTwinIntegration:

    def test_single_injection_end_to_end(self):
        bench = _load_bench()
        assert bench.TWIN_IMPORT_ERROR is None
        episodes, _skipped = bench.find_episodes(
            str(REPLAY_ROOT), ("round20",), limit=1, team="renyxin")
        if not episodes:
            pytest.skip("round20 官方回放语料不在机（gitignored 数据）")
        deps = bench.make_twin_deps()
        assert deps["v13_available"]
        episode = episodes[0]
        with open(episode["path"], "r", encoding="utf-8") as handle:
            replay = json.load(handle)
        row = bench.evaluate_injection(
            deps, replay, episode["me_seat"], 240,
            {"episode": episode["episode"], "oracle": False})
        # P1 保真门：孪生按官方动作流重演必须与回放真值逐位一致
        assert row["twin_noise"] == 0.0
        assert row["truth_me"] == row["twin_resim_me"]
        assert row["reactive_proxy"] is False
        assert 0 < row["n_plans"] <= 120
        assert row["dtsp_me"] >= 0.0 and row["reactive_me"] >= 0.0
