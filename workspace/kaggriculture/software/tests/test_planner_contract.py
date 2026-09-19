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
                land_due_shift=0, herd_due_shift=0, sell_discount=0.9,
                liquidity_tier="STANDARD")
    base.update(kw)
    return plans.PlanSpec(**base)


class TestPlanSpecContract:

    def test_hash_and_equality_stable(self):
        a = _spec(quota_scale=1.25, land_due_shift=-2)
        b = _spec(quota_scale=1.25, land_due_shift=-2)
        assert a == b and hash(a) == hash(b)
        assert hash(plans.PlanSpec.from_json(a.to_json())) == hash(a)
        assert a != _spec(land_due_shift=2)          # -2/+2 可区分
        assert a != _spec(herd_due_shift=-1)         # K3 两轴独立可区分
        assert a != _spec(liquidity_tier="LOOSE")    # K2 钱包档可区分
        assert len({a, b, _spec()}) == 2             # 可入集合

    def test_json_roundtrip_and_stable_text(self):
        a = _spec(p4_clear="HEAVY", quota_scale=1.25, land_due_shift=4)
        text = a.to_json()
        assert text == json.dumps(a.to_dict(), sort_keys=True)
        assert plans.PlanSpec.from_json(text) == a
        assert text == a.to_json()                 # 两次序列化逐字节相同

    def test_key_is_canonical_and_sortable(self):
        keys = sorted(_spec(quota_scale=q).key() for q in plans.QUOTA_SCALES)
        assert len(set(keys)) == 3
        assert _spec().key().startswith("P|C|B2|C3|")
        ident = plans.identity_spec()
        assert ident.key().startswith("P|IDENT|")
        assert plans.identity_spec().key() == ident.key()   # 工厂确定

    def test_invalid_axes_raise_with_example(self):
        with pytest.raises(ValueError) as exc:
            plans.PlanSpec(opening="X", p1_branch="B2", capacity_tier="C3",
                           p3_mode="HEALTHY", p4_clear="LOW",
                           quota_scale=1.0, land_due_shift=0,
                           herd_due_shift=0, sell_discount=0.9)
        assert "示例" in str(exc.value)
        with pytest.raises(ValueError):
            _spec(quota_scale=1.3)                 # 25% 网格之外
        with pytest.raises(ValueError):
            _spec(land_due_shift=3)                # K3 土地日程域外
        with pytest.raises(ValueError):
            _spec(herd_due_shift=2)                # K3 买畜日程域外
        with pytest.raises(ValueError):
            _spec(liquidity_tier="TIGHT")          # K2 钱包档域外

    def test_identity_anchor_validation(self):
        """identity 守成点全轴=v13.8 原生锚：偏离任一轴显式抛错。"""
        assert plans.identity_spec().identity is True
        bad = dict(plans.identity_spec().to_dict(), quota_scale=0.8)
        with pytest.raises(ValueError):
            plans.PlanSpec.from_dict(bad)
        bad2 = dict(plans.identity_spec().to_dict())
        del bad2["quota_scale"]
        with pytest.raises(ValueError):
            plans.PlanSpec.from_dict(bad2)

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
        # identity 守成点恒在（K1，opening 恒 C）——断言只对网格计划
        assert {p.opening for p in plan_list if not p.identity} == {"B"}

    def test_r2_branch_by_opp_class(self):
        for cls, want in (("burst", "B1"), ("reduced", "B2"),
                          ("deferred", "B2"), ("melon_first", "B3")):
            obs = plans.build_obs_summary(
                day=1, money=3000, herd=0, crops={}, unlocked_quadrants=1,
                opp_class=cls, daily_demand={})
            plan_list = plans.enumerate_plans(obs)
            assert plan_list and \
                {p.p1_branch for p in plan_list if not p.identity} == {want}

    def test_r3_d6_gate(self):
        base = dict(day=6, money=9000, herd=12, unlocked_quadrants=2,
                    crops={"STRAWBERRY": 8, "WHEAT": 16},
                    daily_demand={"STRAWBERRY": 5})
        all_pass = plans.enumerate_plans(
            plans.build_obs_summary(d6_checks=[True] * 5, **base))
        assert {p.capacity_tier for p in all_pass if not p.identity} >= \
            {"C1", "C3"}
        q1_fail = plans.enumerate_plans(
            plans.build_obs_summary(d6_checks=[False, True, True, True, True],
                                    **base))
        # q1 挂：C1/C2 皆禁（identity 守成点 C2 恒在豁免，K1）
        assert {p.capacity_tier for p in q1_fail if not p.identity} == {"C3"}

    def test_r4_r5_late_game_freeze(self):
        obs = plans.build_obs_summary(
            day=25, money=2000, herd=12, crops={"STRAWBERRY": 20},
            unlocked_quadrants=3, opening_played="C", opp_class="burst",
            d6_checks=[True] * 5, p4_tier="MID", daily_demand={"STRAWBERRY": 6})
        plan_list = plans.enumerate_plans(obs)
        assert plan_list
        grid = [p for p in plan_list if not p.identity]
        assert {p.p3_mode for p in grid} == {"CATCHUP"}   # d12 现金 8k 分界
        assert {p.p4_clear for p in grid} == {"MID"}

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
                    and p.quota_scale == 1.0 and p.land_due_shift == 0
                    and p.herd_due_shift == 0 and p.sell_discount == 0.9)
        ov = plans.plan_to_knob_overrides(base)
        assert ov["PACK"] == "VOLUME_CROP"
        assert ov["_VOLUME_PLAN.straw_total_cap"] == 48
        assert ov["LINE_CAPS.STRAWBERRY"] == 48
        assert ov["SE_DUE_DAY"] == plans.SE_DUE_DAY_DEFAULT
        assert ov["LAND_PLAN.1"] == (4, 1700) and ov["LAND_PLAN.2"] == (7, 2700)
        # 卖出折扣→囤货门槛耦合（缺口清单第 1 条的唯一近似杠杆）
        assert ov["SELL_PLAN_HOLD_EDGE"] == 1.09
        # K2 钱包门档（STANDARD=v13.8 冻结值）
        assert ov["PLANNER_OVERRIDES.liquidity_floor"] == 350
        assert ov["PLANNER_OVERRIDES.cow_buy_reserve"] == 380

    def test_scaled_and_shifted(self):
        spec = _spec(capacity_tier="C1", quota_scale=1.25, land_due_shift=-2,
                     herd_due_shift=-1, sell_discount=0.9)
        ov = plans.plan_to_knob_overrides(spec)
        assert ov["_VOLUME_PLAN.straw_total_cap"] == 60        # 48*1.25
        assert ov["LINE_CAPS.MELON"] == 15                     # 12*1.25
        assert ov["SE_DUE_DAY"] == 8                           # 10-2
        assert ov["LAND_PLAN.1"] == (2, 1700) and ov["LAND_PLAN.2"] == (5, 2700)
        assert ov["SELL_PLAN_HOLD_EDGE"] == 1.09
        # K3 拆分：买畜日程独立驱动（herd_day_shift=herd_due_shift）
        assert ov["PLANNER_OVERRIDES.herd_day_shift"] == -1
        assert ov["PLANNER_OVERRIDES.animal_buy_last_day_shift"] == -1
        # K2 钱包档 LOOSE（反事实 V_WALLET 值域）
        loose = plans.plan_to_knob_overrides(_spec(liquidity_tier="LOOSE"))
        assert loose["PLANNER_OVERRIDES.liquidity_floor"] == 150
        assert loose["PLANNER_OVERRIDES.cow_buy_reserve"] == 150
        unb = plans.plan_to_knob_overrides(_spec(liquidity_tier="UNBOUNDED"))
        assert unb["PLANNER_OVERRIDES.liquidity_floor"] == 0
        assert unb["PLANNER_OVERRIDES.cow_buy_reserve"] == 0
        # 缺口清单：规划器本地键必须显式存在（执行器侧跳过）
        assert ov["PLANNER_LOCAL.sell_discount"] == 0.9
        assert ov["PLANNER_LOCAL.land_due_shift"] == -2
        assert ov["PLANNER_LOCAL.herd_due_shift"] == -1
        assert ov["PLANNER_LOCAL.p3_mode"] == "HEALTHY"

    def test_identity_overrides_are_native_face(self):
        """K1：identity 守成点覆盖面与常规计划同键集、全部值=v13.8 原生
        ——行为与旗关逐字节等价（同键集是 governed_keys 快照契约）。"""
        ov = plans.plan_to_knob_overrides(plans.identity_spec())
        c2 = plans.plan_to_knob_overrides(_spec(capacity_tier="C2",
                                                p4_clear="MID"))
        assert set(ov) == set(c2)
        assert ov["PLANNER_ENABLED"] is True
        # 原生锚逐键钉住（出处 src/constants.py）
        assert ov["LINE_CAPS.STRAWBERRY"] == 48
        assert ov["STRAW_QUAD_CAP_REGIME"] == 8
        assert ov["STRAW_TOTAL_CAP_REGIME"] == 24
        assert ov["SELL_PLAN_HOLD_EDGE"] == plans._SELL_HOLD_EDGE_BASE
        assert ov["PLANNER_OVERRIDES.sell_price_discount"] == 1.0
        assert ov["PLANNER_OVERRIDES.p4_force_tier"] == ""
        assert ov["PLANNER_OVERRIDES.sell_batch_mult"] == 1.0
        assert ov["PLANNER_OVERRIDES.herd_start_day"] == 0
        assert ov["PLANNER_OVERRIDES.herd_day_shift"] == 0
        assert ov["PLANNER_OVERRIDES.b_branch_force"] == ""
        assert ov["PLANNER_OVERRIDES.liquidity_floor"] == 350
        assert ov["PLANNER_OVERRIDES.cow_buy_reserve"] == 380
        assert ov["PLANNER_OVERRIDES.fuse_money_floor"] == 300
        assert ov["PLANNER_LOCAL.identity"] is True

    def test_deterministic_key_order(self):
        a = plans.plan_to_knob_overrides(_spec())
        b = plans.plan_to_knob_overrides(_spec())
        assert list(a.keys()) == list(b.keys())
        assert list(a.keys()) == sorted(a.keys())


# ===========================================================================
# 3b) P2.5 投影校准：全名面 + 可测行为差异 + 旗关等价（惰性旋钮通道）
# ===========================================================================

AGENT_SRC = SOFTWARE / "kaggle_simulations" / "agent" / "src"


def _knob_face(overrides):
    """plan_to_knob_overrides 输出中的 PLANNER_OVERRIDES 寄存器子面。"""
    return {k.split(".", 1)[1]: v for k, v in overrides.items()
            if k.startswith("PLANNER_OVERRIDES.")}


class TestKnobProjectionCalibration:

    def _load_constants_ns(self):
        """单独 exec constants.py 到干净命名空间（惰性旋钮层单测用）。"""
        ns = {}
        path = AGENT_SRC / "constants.py"
        exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"),
             ns)
        return ns

    def test_every_emitted_knob_has_a_read_site(self):
        """全名面静态审计：寄存器子面的每个键在 src/ 必须有
        _plan_knob("<键>" 读取点——杜绝"规划器发键、执行器无人消费"的
        假旋钮（首轮 official 复盘的 no-op 覆盖教训）。"""
        face = _knob_face(plans.plan_to_knob_overrides(_spec()))
        assert len(face) >= 20            # 29 键全名面（留演进余量）
        corpus = ""
        for path in sorted(AGENT_SRC.glob("*.py")):
            corpus += path.read_text(encoding="utf-8")
        missing = [k for k in sorted(face)
                   if f'_plan_knob("{k}"' not in corpus
                   and f"_plan_knob('{k}'" not in corpus]
        assert not missing, f"src/ 无读取点的伪旋钮: {missing}"

    def test_adjacent_plans_produce_distinct_overrides(self):
        """相邻档位计划的覆盖 dict 必须不同且寄存器子面非空——投影的
        行为可分性（P2.5 判据；首轮 34/42 no-op 覆盖的直接反义）。"""
        base = dict(opening="C", p1_branch="B2", p3_mode="HEALTHY",
                    p4_clear="MID", quota_scale=1.0, land_due_shift=0,
                    herd_due_shift=0, liquidity_tier="STANDARD",
                    sell_discount=0.9)
        pairs = [
            (_spec(capacity_tier="C2", **base),
             _spec(capacity_tier="C1", **base)),
            (_spec(capacity_tier="C2", **base),
             _spec(capacity_tier="C3", **base)),
            (_spec(p1_branch="B2", **{k: v for k, v in base.items()
                                      if k != "p1_branch"}),
             _spec(p1_branch="B1", **{k: v for k, v in base.items()
                                      if k != "p1_branch"})),
            (_spec(p3_mode="HEALTHY", **{k: v for k, v in base.items()
                                         if k != "p3_mode"}),
             _spec(p3_mode="CATCHUP", **{k: v for k, v in base.items()
                                         if k != "p3_mode"})),
            (_spec(p4_clear="MID", **{k: v for k, v in base.items()
                                      if k != "p4_clear"}),
             _spec(p4_clear="HEAVY", **{k: v for k, v in base.items()
                                        if k != "p4_clear"})),
            (_spec(sell_discount=0.9, **{k: v for k, v in base.items()
                                         if k != "sell_discount"}),
             plans.identity_spec()),
            (_spec(land_due_shift=0, **{k: v for k, v in base.items()
                                        if k != "land_due_shift"}),
             _spec(land_due_shift=4, **{k: v for k, v in base.items()
                                        if k != "land_due_shift"})),
            (_spec(herd_due_shift=0, **{k: v for k, v in base.items()
                                        if k != "herd_due_shift"}),
             _spec(herd_due_shift=-1, **{k: v for k, v in base.items()
                                         if k != "herd_due_shift"})),
            (_spec(liquidity_tier="STANDARD", **{k: v for k, v in base.items()
                                                 if k != "liquidity_tier"}),
             _spec(liquidity_tier="LOOSE", **{k: v for k, v in base.items()
                                              if k != "liquidity_tier"})),
        ]
        for a, b in pairs:
            oa, ob = plans.plan_to_knob_overrides(a), \
                plans.plan_to_knob_overrides(b)
            assert oa and ob
            assert oa != ob, f"相邻计划覆盖相同: {a.key()} vs {b.key()}"
            face_a, face_b = _knob_face(oa), _knob_face(ob)
            assert face_a and face_b
            assert set(face_a) == set(face_b)   # 全名面键集恒定（值不同）
            # 寄存器子面必异（行为差异的载体）——例外：K3 土地日程轴的
            # 载体是直写键（LAND_PLAN.<n>/SE_DUE_DAY，缺口清单机制），
            # 寄存器面允许相同、直写键必异。
            if a.land_due_shift != b.land_due_shift:
                assert any(oa[k] != ob[k] for k in oa
                           if not k.startswith("PLANNER_OVERRIDES.")
                           and k not in ("PLANNER_ENABLED",))
            else:
                assert face_a != face_b

    def test_flag_off_returns_default_even_with_overrides(self):
        """旗关等价的核心语义：寄存器有覆盖但 PLANNER_ENABLED=False 时
        _plan_knob 恒回默认值；旗开才消费覆盖；None 值视为未覆盖。"""
        ns = self._load_constants_ns()
        assert ns["PLANNER_ENABLED"] is False
        ns["PLANNER_OVERRIDES"]["mode_volume_price_min"] = 999
        ns["PLANNER_OVERRIDES"]["herd_day_shift"] = None
        assert ns["_plan_knob"]("mode_volume_price_min", 105) == 105
        assert ns["_plan_knob"]("herd_day_shift", 0) == 0
        ns["PLANNER_ENABLED"] = True
        assert ns["_plan_knob"]("mode_volume_price_min", 105) == 999
        assert ns["_plan_knob"]("herd_day_shift", 0) == 0    # None→默认
        assert ns["_plan_knob"]("uncovered_key", 7) == 7

    def test_bench_injection_turns_flag_on(self):
        """bench 的 apply_knob_overrides 必须把总旗与寄存器面打进命名
        空间（覆盖生效的装载契约）。"""
        bench = _load_bench()
        ns = self._load_constants_ns()
        overrides = plans.plan_to_knob_overrides(_spec())
        applied, _skipped = bench.apply_knob_overrides(ns, overrides)
        assert ns["PLANNER_ENABLED"] is True
        assert ns["PLANNER_OVERRIDES"], "寄存器面为空"
        assert "PLANNER_ENABLED" in applied
        assert any(k.startswith("PLANNER_OVERRIDES.") for k in applied)

    def test_tier_gates_coherent_with_axis_semantics(self):
        """C1=宽田提前一拍、C2=v13.8 逐字段镜像、C3=否决宽田（VOLUME
        日窗 99 禁入场）；safety 地板 10 全档不放宽（v7.2-V1 破产教训）。"""
        g = plans.TIER_MODE_GATES
        assert g["C1"]["vol_day"] == (5, 13) and g["C1"]["vol_price"] == 100
        assert g["C2"]["vol_day"] == (6, 12) and g["C2"]["vol_price"] == 105
        assert g["C3"]["vol_day"] == (99, 99)
        assert all(t["vol_herd"] == 10 for t in g.values())
        ov_c3 = _knob_face(plans.plan_to_knob_overrides(
            _spec(capacity_tier="C3")))
        assert ov_c3["mode_volume_day_start"] == 99


# ===========================================================================
# 3c) v3 K1 identity 守成档 + K3 日程轴拆分（round-24 法证终稿，2026-09-20）
# ===========================================================================

class TestIdentityGuardrail:

    def test_identity_always_enumerated_within_cap(self):
        """identity 守成点在任意局况恒在枚举面且总数 <=120（K1 第 0 项）。"""
        for day, kw in ((0, {}), (5, {"opp_class": "burst"}),
                        (25, {"opening_played": "C", "opp_class": "reduced",
                              "d6_checks": [False] * 5, "p4_tier": "HEAVY"})):
            obs = plans.build_obs_summary(
                day=day, money=5000, herd=8, crops={"STRAWBERRY": 10,
                                                    "WHEAT": 16},
                unlocked_quadrants=2, daily_demand={"STRAWBERRY": 5}, **kw)
            plan_list = plans.enumerate_plans(obs)
            assert 0 < len(plan_list) <= plans.MAX_PLAN_CANDIDATES
            assert sum(1 for p in plan_list if p.identity) == 1
            assert plans.identity_spec().key() in {p.key() for p in plan_list}

    def test_identity_overrides_behave_native(self):
        """identity 注入后 _plan_knob 全部回原生值（=旗关行为等价）。"""
        bench = _load_bench()
        ns = {}
        exec("import copy; import math; import json; import hashlib", ns)
        for mod in ("constants", "strategy", "market"):
            path = AGENT_SRC / f"{mod}.py"
            exec(compile(path.read_text(encoding="utf-8"), str(path),
                         "exec"), ns)
        applied, skipped = bench.apply_knob_overrides(
            ns, plans.plan_to_knob_overrides(plans.identity_spec()))
        assert ns["PLANNER_ENABLED"] is True
        assert ns["_plan_knob"]("liquidity_floor", 999) == 350
        assert ns["_plan_knob"]("cow_buy_reserve", 999) == 380
        assert ns["_plan_knob"]("sell_price_discount", 999) == 1.0
        assert ns["_plan_knob"]("b_branch_force", "sentinel") == ""
        assert ns["SE_DUE_DAY"] == plans.SE_DUE_DAY_DEFAULT
        assert ns["LINE_CAPS"]["STRAWBERRY"] == 48
        assert ns["SELL_PLAN_HOLD_EDGE"] == 1.05
        # 常规计划（LOOSE 钱包档）注入后旋钮确已偏离原生（通道活性对照）
        loose = next(p for p in plans.enumerate_plans(plans.build_obs_summary(
            day=10, money=5000, herd=8, crops={"STRAWBERRY": 10},
            unlocked_quadrants=2)) if p.liquidity_tier == "LOOSE")
        bench.apply_knob_overrides(
            ns, plans.plan_to_knob_overrides(loose))
        assert ns["_plan_knob"]("liquidity_floor", 999) == 150
        assert ns["_plan_knob"]("cow_buy_reserve", 999) == 150

    def test_near_tie_break_prefers_identity(self):
        """K1 近平 tie-break：最优对 identity 边际 <τ → 恒选守成点。"""
        tau = select.IDENTITY_TIEBREAK_TAU
        ident = plans.identity_spec().key()
        other = _spec(quota_scale=0.8).key()
        # 边际 0.3% < 0.5% → identity
        near = {ident: {"m": 100000.0}, other: {"m": 100300.0}}
        sel = select.robust_select(near, identity_key=ident)
        assert sel["best"] == ident
        assert sel["tie_break"] and "守成" in sel["tie_break"]
        # 边际 2% > 0.5% → 最优保持
        far = {ident: {"m": 100000.0}, other: {"m": 102000.0}}
        sel2 = select.robust_select(far, identity_key=ident)
        assert sel2["best"] == other
        # identity 自身最优时不触发
        top = {ident: {"m": 105000.0}, other: {"m": 100000.0}}
        assert select.robust_select(top, identity_key=ident)["best"] == ident
        # identity 不在矩阵（防御）→ 不触发、不异常
        no_ident = {"a": {"m": 1.0}, "b": {"m": 2.0}}
        assert select.robust_select(no_ident, identity_key=ident)["best"] == "b"
        # 关闭守成（identity_key=None）→ P2.6 行为
        assert select.robust_select(near)["best"] == other

    def test_projection_tied_wallet_siblings_default_conservative(self):
        """钱包档等值兄弟的字典序 tie-break 默认最保守档：投影器对钱包
        不可见 → 同 (tier,quota,land,herd) 的三档兄弟 J 全等，key 序必须
        让 STANDARD 先于 LOOSE/UNBOUNDED（钱包地板是安全不变式——
        official 复裁首跑 -39.8k 灾难注入=C1×1.25×LOOSE 字典序中签的
        直接反义钉）。"""
        siblings = {lt: _spec(liquidity_tier=lt).key()
                    for lt in plans.LIQUIDITY_TIERS}
        assert siblings["STANDARD"] < siblings["LOOSE"] \
            < siblings["UNBOUNDED"]
        matrix = {k: {"m": 100.0} for k in siblings.values()}
        assert select.robust_select(matrix)["best"] \
            == siblings["STANDARD"]

    def test_k3_split_axes_independent(self):
        """land/herd 两轴独立可投影：land 轴动买地日程、herd 轴动买畜日程。"""
        a = _spec(land_due_shift=4, herd_due_shift=0)
        b = _spec(land_due_shift=0, herd_due_shift=-1)
        oa, ob = plans.plan_to_knob_overrides(a), plans.plan_to_knob_overrides(b)
        assert oa["LAND_PLAN.2"] == (11, 2700) and ob["LAND_PLAN.2"] == (7, 2700)
        assert oa["PLANNER_OVERRIDES.herd_day_shift"] == 0
        assert ob["PLANNER_OVERRIDES.herd_day_shift"] == -1
        # 与旧 timing_shift 一轴双驱的过约束反义：4/0 与 0/-1 同时存在
        t = plans.plan_targets(a)
        assert t["land_dues"][2][0] == 11 and t["se_due"] == 14  # 钳到末窗


class TestLiquidityKnobSrc:

    def test_liquidity_knob_bites_at_cash_gate(self):
        """K2 read-site 1：strategy._cash_gate_ok 的 liquidity_floor 随计划
        变（旗开 LOOSE=150），旗关恒回冻结值 350（黄金等价根基）。"""
        bench = _load_bench()
        ns_on = {}
        exec("import copy; import math; import json; import hashlib", ns_on)
        for mod in ("constants", "strategy", "market"):
            path = AGENT_SRC / f"{mod}.py"
            exec(compile(path.read_text(encoding="utf-8"), str(path),
                         "exec"), ns_on)
        applied, _skipped = bench.apply_knob_overrides(
            ns_on, {"PLANNER_ENABLED": True,
                    "PLANNER_OVERRIDES.liquidity_floor": 150,
                    "PLANNER_OVERRIDES.cow_buy_reserve": 150})
        assert "PLANNER_ENABLED" in applied
        bill0 = float(ns_on["_FIB_CUM"][0])
        assert ns_on["_cash_gate_ok"]({"money": bill0 + 150.0, "hands": []})
        assert not ns_on["_cash_gate_ok"]({"money": bill0 + 149.0,
                                           "hands": []})
        # 旗关（默认装载）：350 地板恒在
        ns_off = {}
        exec("import copy; import math; import json; import hashlib", ns_off)
        for mod in ("constants", "strategy", "market"):
            path = AGENT_SRC / f"{mod}.py"
            exec(compile(path.read_text(encoding="utf-8"), str(path),
                         "exec"), ns_off)
        assert not ns_off["_cash_gate_ok"]({"money": bill0 + 150.0,
                                            "hands": []})
        assert ns_off["_cash_gate_ok"]({"money": bill0 + 350.0, "hands": []})


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
        # 折扣单调：identity（原生 1.0）> 0.9 折扣计划（0.75 档已按 K6
        # 判定砍除——卖出侧挤压非杠杆）
        hi = plans.identity_spec()
        lo = _spec(sell_discount=0.9)
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
        # v3.1 标定语义：冷摘要（无对手证据）→ 信号 s=0 → 折扣=1.0
        # （弱/无证据对手 → 激进计划按真值评分）；None（rollout 余季
        # 延续段）显式走守旧常数路径（见 test_pessimistic_fill_wiring）
        assert pressure["STRAWBERRY"] == 1.0 and pressure["WHEAT"] == 1.0
        # 我方无卖单 → 无倾销
        assert model.propose_actions({"our_sell_plan": {}}, 11)["market"] == []

    def test_pessimistic_fill_validation(self):
        with pytest.raises(ValueError):
            opponents.PessimisticFill(price_discount=1.5)
        with pytest.raises(ValueError):
            opponents.PessimisticFill(dump_ratio=0.0)

    def test_default_model_set_shape(self):
        models = opponents.build_default_models(history=[])
        # P2.5 起内置双风格入池（赢家结构型/重小麦压制型，不再恒 no-op）
        assert [m.name for m in models] == [
            "passive_extrapolation",
            "frozen_style_pool:winner_balanced",
            "frozen_style_pool:wheat_suppressor",
            "pessimistic_fill"]

    def test_builtin_style_pool_available_and_distinct(self):
        # 内置画像可用且两风格行为可测地不同（不再恒 no-op）
        a = opponents.FrozenStylePool(use_builtin_pool=True, style_index=0)
        b = opponents.FrozenStylePool(use_builtin_pool=True, style_index=1)
        assert a.available and b.available
        assert a.name != b.name
        state = {"shed": {"WHEAT": 60, "STRAWBERRY": 40, "MELON": 20},
                 "herd": 4, "money": 6000}
        act_a = a.propose_actions(state, 5)
        act_b = b.propose_actions(state, 5)
        assert act_a["market"] and act_b["market"]
        assert act_a != act_b                       # 画像驱动可测行为差异
        # d8 前置带：day > herd_due_day 后停买（内置画像 herd_due_day=8）
        late = a.propose_actions(dict(state, herd=6), 9)
        assert ["BUY_ANIMAL", "COW", 1] not in late["market"]
        early = a.propose_actions(dict(state, herd=6), 8)
        assert ["BUY_ANIMAL", "COW", 1] in early["market"]
        # 压价系数只对内置画像启用（文件画像不发明语义）
        assert a.supply_pressure({})["STRAWBERRY"] < 1.0
        assert b.supply_pressure({})["WHEAT"] < 1.0
        assert "sprint_forensics_0919" in a.describe()


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

    def test_trimmed_mean_value_order_statistics(self):
        # v3.1 回归（2026-09-20 标定实测）：trimmed_mean 必须按【值序】
        # 裁切序统计量，不得按 name-sorted 顺序切片——键序≠值序时旧实现
        # kept=(值min+值max)、两个值中位反被裁（Ω=4 下悲观模型全局失敏，
        # 悲观折扣成死代码）。本样例刻意让键序与值序相反。
        scores = {"a": 4.0, "b": 1.0, "c": 3.0, "d": 2.0}
        # 值序 [1,2,3,4] → 裁两端 → (2+3)/2 = 2.5（旧实现按键序 a,b,c,d
        # 切 [1:3] 得 (1+3)/2 = 2.0）
        assert select.aggregate_scores(scores, "trimmed_mean") == 2.5
        # Ω=4 实测形态：悲观模型分值居中时必须进入聚合
        omega4 = {"frozen_style_pool:wheat_suppressor": 10960.13,
                  "frozen_style_pool:winner_balanced": 9495.99,
                  "passive_extrapolation": 13374.23,
                  "pessimistic_fill": 10015.45}
        assert select.aggregate_scores(omega4, "trimmed_mean") == \
            (10015.45 + 10960.13) / 2

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
# 6.5) v3.1 对手压力自适应折扣（plans.pressure_* + PessimisticFill 接线）
# ===========================================================================

class TestPressureAdaptiveDiscount:

    @staticmethod
    def _obs(day, *, opp_herd=0, opp_quads=1, opp_money=0.0, my_money=2000.0):
        return plans.build_obs_summary(
            day=day, money=my_money, herd=3, crops={}, unlocked_quadrants=1,
            opponent={"herd": opp_herd, "crops": {}, "money": opp_money,
                      "quads": opp_quads})

    def test_prior_window_semantics_parameterized(self):
        # 先验窗语义（参数化）：PRIOR_DAYS=1 时 d0-d1 恒全悲观（v14.2
        # 回退面）；标定烘焙默认为 open（PRIOR_DAYS=-1，无先验窗）——
        # smoke 实测开窗与否零选局效应，两档均入预登记网格。
        for day in (0, 1, 5):
            obs = self._obs(day, opp_herd=12, opp_quads=3)
            assert plans.pressure_strength(obs, prior_days=1) == 1.0
        gated_weak = self._obs(1, opp_herd=0, opp_quads=1)
        assert plans.pressure_strength(gated_weak, prior_days=1) == 1.0
        assert plans.pressure_strength(gated_weak, prior_days=-1) == 0.0
        # 烘焙默认 = open：无先验窗，d0 即信号接管
        assert plans.PRESSURE_PRIOR_DAYS == -1
        assert plans.pressure_strength(self._obs(0)) == 0.0

    def test_baked_calibration_defaults(self):
        # 预登记标定选中 C8_open_H12_L3（v31_calibration.json）：
        # 值序裁切修复 + 自适应开 + H12 + LIQ 0.3；强端恒 0.75
        assert plans.PRESSURE_HERD_REF == 12.0
        assert plans.PRESSURE_QUAD_REF == 3
        assert plans.PRESSURE_MONEY_GAP_REF is None
        assert plans.PRESSURE_LIQ_PENALTY == 0.3
        assert plans.PRESSURE_ADAPTIVE is True
        assert plans.PRESSURE_DISC_STRONG == 0.75

    def test_monotone_in_opponent_assets(self):
        # 畜群/象限任一增强 → s 非降、折扣非增（悲观随对手增强）
        prev_s, prev_d = -1.0, 2.0
        for herd, quads in ((0, 1), (4, 1), (8, 1), (8, 2), (12, 3)):
            obs = self._obs(10, opp_herd=herd, opp_quads=quads)
            s, d = plans.pressure_strength(obs), plans.pressure_discount(obs)
            assert s >= prev_s and d <= prev_d
            prev_s, prev_d = s, d
        obs = self._obs(10, opp_herd=12, opp_quads=3)
        assert plans.pressure_strength(obs) == 1.0
        assert plans.pressure_discount(obs) == 0.75

    def test_weak_opponent_relaxes_to_face_value(self):
        # 弱对手（低畜群单象限）→ 折扣 → 1.0（激进计划按真值评分）
        obs = self._obs(5, opp_herd=0, opp_quads=1)
        assert plans.pressure_discount(obs) == 1.0
        # 资金差信号默认关（预登记标定依据）：囤钱型弱对手不触发悲观
        obs_rich = self._obs(13, opp_herd=0, opp_quads=1, opp_money=24000.0,
                             my_money=300.0)
        assert plans.PRESSURE_MONEY_GAP_REF is None
        assert plans.pressure_discount(obs_rich) == 1.0

    def test_adaptive_off_restores_constant(self):
        obs = self._obs(5, opp_herd=12, opp_quads=3)
        try:
            plans.PRESSURE_ADAPTIVE = False
            assert plans.pressure_discount(obs) == 0.75
            assert plans.pressure_strength(obs) == 1.0
        finally:
            plans.PRESSURE_ADAPTIVE = True

    def test_strong_end_is_the_v142_constant(self):
        # 硬约束：强端=0.75（v14.2 全局常数语义不变）
        assert plans.PRESSURE_DISC_STRONG == 0.75

    def test_pessimistic_fill_wiring(self):
        model = opponents.PessimisticFill()
        # 冷摘要（无对手证据）→ 信号 s=0 → 1.0（v3.1 标定语义）
        assert model.supply_pressure({})["STRAWBERRY"] == 1.0
        # None（rollout 余季延续段）→ 显式守旧常数路径
        assert model.supply_pressure(None)["HERD"] == 0.75
        # 弱对手 → 1.0；强对手 → 强端 0.75
        weak = self._obs(5, opp_herd=0, opp_quads=1)
        strong = self._obs(13, opp_herd=12, opp_quads=3)
        assert model.supply_pressure(weak) == {
            k: 1.0 for k in
            ("STRAWBERRY", "MELON", "CARROT", "WHEAT", "HERD")}
        assert model.supply_pressure(strong)["WHEAT"] == 0.75
        # 自适应只影响投影器评分，不改倾销动作
        action = model.propose_actions(
            {"our_sell_plan": {"STRAWBERRY": 8}}, 10)
        assert action["market"] == [["SELL", "STRAWBERRY", 8]]

    def test_pessimistic_fill_describe_mentions_adaptive(self):
        text = opponents.PessimisticFill().describe()
        assert "自适应" in text and "0.75" in text

    def test_liq_penalty_scores_wallet_tiers(self):
        # 钱包档可见性（评分项）：LOOSE/UNBOUNDED 在模型现金跌破 STANDARD
        # 地板时记罚分；STANDARD 恒无罚分；系数 0 = 关（v14.2 语义）
        obs = plans.build_obs_summary(
            day=5, money=300.0, herd=3, crops={"STRAWBERRY": 10},
            unlocked_quadrants=1)

        def _spec(tier):
            return plans.PlanSpec(opening="C", p1_branch="B1",
                                  capacity_tier="C1", p3_mode="HEALTHY",
                                  p4_clear="LOW", quota_scale=1.25,
                                  land_due_shift=0, herd_due_shift=0,
                                  sell_discount=0.9, liquidity_tier=tier)
        loose, std = _spec("LOOSE"), _spec("STANDARD")
        try:
            plans.PRESSURE_LIQ_PENALTY = 0.0
            assert plans.project_season(loose, obs, {}) == \
                plans.project_season(std, obs, {})
            plans.PRESSURE_LIQ_PENALTY = 0.3
            assert plans.project_season(loose, obs, {}) < \
                plans.project_season(std, obs, {})
            assert plans.project_season(std, obs, {}) == \
                plans.project_season(std, obs, {})      # 确定性
        finally:
            plans.PRESSURE_LIQ_PENALTY = 0.0

    def test_pressure_note_is_audit_shaped(self):
        note = plans.pressure_discount_note(self._obs(13, opp_herd=12,
                                                     opp_quads=3))
        assert note["strength"] == 1.0 and note["discount"] == 0.75
        assert note["adaptive"] is True and note["prior_days"] == -1

    def test_invalid_reference_values_rejected(self):
        obs = self._obs(5)
        with pytest.raises(ValueError):
            plans.pressure_strength(obs, herd_ref=0)
        with pytest.raises(ValueError):
            plans.pressure_strength(obs, quad_ref=1)




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
