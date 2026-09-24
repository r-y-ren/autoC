"""test_layer_l4：_ca_future_plant_demand 语义矩阵 + 七件构造用例（helper 源经 exec 独立可测）。

① test_demand_and_clamp_matrix：gate_equivalence_l3._clamp_ns/_clamp_tape 伪
上下文（inject_controller_clamp.CLAMP_HELPER_SRC 独立 exec）——k 胡萝卜+m
小麦 → demand=k+m、target=min(8, k+m+2)（+2 安全边封顶 8）；**需求相对激活
（2026-09-24 修订一轮）：day 24/26/27 三点同式**（无 day 键控）；后缀边界
（t≥step 计、t<step 不计）；天窗边界（小麦限 day≤_CA_TO=28、胡萝卜不限天）；
磁带读不到/异常/非 dict → demand None → target 8。
② test_high_demand_zero_footprint：需求充足局（demand+2≥8）target==8=原目标
（表达式仍写但行为同原式=零足迹）且 helper 确被调用（门控在需求不在 day）。
③ test_invariant_cases_l3：gate_equivalence_l3.constructed_cases_l3 真跑
   （无引擎，夹具直驱——R10 三件走 test_layer_s 真链路 layer_s_block，新四件走
   helper exec）：七件全过。
④ 变体组（R13 第二次调参）：tuned/lean=小麦槽权重 0.5/0.0——变体加权 helper
   源（inject_controller_clamp.clamp_helper_src）伪上下文 exec：demand=k+m×weight
   语义矩阵（day24/26/27 同式）/需求充足局零足迹与 fail-safe 永不抛不变。"""

import pytest

import gate_equivalence_l3 as g  # noqa: E402  (自带 L1/L2/HERE sys.path 自举)
import inject_controller_clamp  # noqa: E402  (HERE 已由上行走入 sys.path)


# ---------------------------------------------------------------------------
# ① 钳制 helper 语义矩阵（伪磁带 exec 级）
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("k,m", [
    (0, 0), (1, 0), (0, 1), (3, 2), (6, 3), (10, 0), (2, 7), (0, 8),
])
@pytest.mark.parametrize("day,step", [(27, 650), (26, 624), (24, 576)])
def test_demand_and_clamp_matrix(k, m, day, step):
    # route2 后缀 k 个 PLANT,CARROT + day28 窗内 m 个 PLANT,WHEAT
    # → demand=k+m、target=min(8, k+m+2)——day24/26/27 同式（需求相对激活）。
    # （step 取该 day 的代表步且 ≤ 磁带首条目 650，后缀含全磁带。）
    ns = g._clamp_ns(g._clamp_tape(k, m))
    assert ns["_ca_future_plant_demand"](0, 650) == k + m
    assert ns["_ca_clamped_target"](day, 0, step) == min(8, k + m + 2)


def test_demand_suffix_and_day_window_boundaries():
    # 后缀边界：PLANT,CARROT@t<step 不计、@t=step 计（≥当前步）；可读性锚
    # （PASS 步）保后缀可读使 k=m=0 语义="可读零需求"。
    ns = g._clamp_ns({649: {"farmer": ["PLANT", "CARROT"], "hands": []},
                      655: {"farmer": ["PASS"], "hands": []}})
    assert ns["_ca_future_plant_demand"](0, 650) == 0
    assert ns["_ca_clamped_target"](27, 0, 650) == 2
    ns = g._clamp_ns({650: {"farmer": ["PLANT", "CARROT"], "hands": []}})
    assert ns["_ca_future_plant_demand"](0, 650) == 1
    assert ns["_ca_clamped_target"](27, 0, 650) == 3
    # 天窗边界：PLANT,WHEAT@day29（t=700）不计；PLANT,CARROT@day29 仍计
    # （磁带自己的胡萝卜种植不限天）。
    ns = g._clamp_ns({700: {"farmer": ["PLANT", "WHEAT"], "hands": []}})
    assert ns["_ca_clamped_target"](27, 0, 650) == 2
    ns = g._clamp_ns({700: {"farmer": ["PLANT", "CARROT"], "hands": []}})
    assert ns["_ca_clamped_target"](27, 0, 650) == 3
    # hands 单元同计（farmer+hands 合并遍历）。
    ns = g._clamp_ns({651: {"farmer": ["PASS"],
                            "hands": [["PLANT", "CARROT"], ["PLANT", "WHEAT"]]}})
    assert ns["_ca_future_plant_demand"](0, 650) == 2


def test_clamp_fallbacks_never_raise():
    # 磁带读不到（后缀无可读步条目）/返回非 dict/抛异常 → demand None /
    # 捕获 → target=_CA_BUFFER(8)（fail-safe：回退 q 原公式行为，永不抛）。
    def _boom(seat, t):
        raise RuntimeError("tape down")

    for tape in ({}, _boom, lambda seat, t: "not-a-dict"):
        ns = g._clamp_ns(tape)
        assert ns["_ca_clamped_target"](27, 0, 650) == 8
    empty = g._clamp_ns({})
    assert empty["_ca_future_plant_demand"](0, 650) is None
    # 步条目在但均为空 dict（无可读单元）→ 同 None 语义。
    blank = g._clamp_ns({700: {}})
    assert blank["_ca_future_plant_demand"](0, 650) is None


def test_high_demand_zero_footprint():
    # 需求充足局（demand+2≥8）：target==8==原 _CA_BUFFER（表达式仍写但行为同
    # 原式=零足迹）；helper 确被调用（需求相对激活——门控在需求不在 day，
    # day6/24/27 三点全查询）。
    calls = []
    tape = g._clamp_tape(6, 4)                    # demand=10 → +2=12 ≥ 8
    ns = g._clamp_ns(lambda seat, t: calls.append((seat, t)) or tape.get(t, {}))
    for day, step in ((6, 144), (24, 576), (27, 650)):
        assert ns["_ca_clamped_target"](day, 0, step) == 8
    assert calls and all(t >= 144 for _seat, t in calls)   # 确走磁带（无条件）
    # 对照：需求走低（k=2,m=1 → demand=3）时 day24 即收敛（修订一轮主诉求）
    low = g._clamp_ns(g._clamp_tape(2, 1))
    assert low["_ca_clamped_target"](24, 0, 576) == min(8, 3 + 2)


# ---------------------------------------------------------------------------
# ③ 七件构造用例真跑（constructed_cases_l3：R10 三件+新四件）
# ---------------------------------------------------------------------------
def test_invariant_cases_l3():
    got = g.constructed_cases_l3()
    assert set(got) == {
        "c1_no_trunc_when_future_plant", "c2_trunc_when_no_opportunity",
        "c3_s671_boundary", "c4_clamp_trigger_demand_plus_two",
        "c5_day28_swap_no_starve", "c6_clamp_fallback_returns_buffer",
        "c7_high_demand_zero_footprint", "all_pass"}
    for name in ("c1_no_trunc_when_future_plant", "c2_trunc_when_no_opportunity",
                 "c4_clamp_trigger_demand_plus_two", "c5_day28_swap_no_starve",
                 "c6_clamp_fallback_returns_buffer",
                 "c7_high_demand_zero_footprint"):
        assert set(got[name]) == {"pass", "evidence"}, name
        assert got[name]["pass"] is True, (name, got[name]["evidence"])
        assert isinstance(got[name]["evidence"], str) and got[name]["evidence"]
    c3 = got["c3_s671_boundary"]
    assert set(c3) == {"truncate_side", "keep_side", "pass"}
    assert c3["pass"] is True
    assert c3["truncate_side"]["pass"] is True and c3["keep_side"]["pass"] is True
    assert got["all_pass"] is True


# ---------------------------------------------------------------------------
# ④ R13 第二次调参变体（tuned/lean）：加权口径 helper 语义（变体源独立 exec）
# ---------------------------------------------------------------------------
def _variant_ns(mode, tape):
    """伪上下文 exec 变体加权 helper 源（gate_equivalence_l3._clamp_ns 的变体版）。

    tape 可为 dict（t→act；缺省步 {}）或 callable(seat, t)→act；注入
    _ca_tape/_CA_BUFFER/_CA_TO 三依赖（与 fine 装载面同构）。"""
    if callable(tape):
        tape_fn = tape
    else:
        mapping = dict(tape or {})
        tape_fn = lambda seat, t: mapping.get(t, {})  # noqa: E731
    ns = {"_CA_BUFFER": 8, "_CA_TO": 28, "_ca_tape": tape_fn}
    exec(compile(inject_controller_clamp.clamp_helper_src(mode),
                 f"<clamp_helper_{mode}>", "exec"), ns)
    return ns


@pytest.mark.parametrize("mode,weight", [("tuned", 0.5), ("lean", 0.0)])
@pytest.mark.parametrize("k,m", [(0, 0), (2, 4), (5, 6), (6, 4), (10, 0), (1, 9)])
def test_variant_demand_weight_matrix(mode, weight, k, m):
    # 变体需求口径=胡萝卜全计+day≤28 小麦槽×weight（int 截断收在 clamp 侧）；
    # day24/26/27 同式（表达式与 fine 同形——需求相对激活不因权重变形）。
    ns = _variant_ns(mode, g._clamp_tape(k, m))
    want = k + m * weight
    assert ns["_ca_future_plant_demand"](0, 650) == want
    for day, step in ((24, 576), (26, 624), (27, 650)):
        assert ns["_ca_clamped_target"](day, 0, step) == min(8, int(want) + 2)


@pytest.mark.parametrize("mode", ["tuned", "lean"])
def test_variant_zero_footprint_and_fallback(mode):
    # 需求充足局零足迹不变（demand+2≥8 → min 封顶 8=原目标）；fail-safe
    # 永不抛（读不到/非 dict/异常 → 8）——starve 零容忍门的构造面锚。
    ns = _variant_ns(mode, g._clamp_tape(6, 4))
    assert ns["_ca_clamped_target"](27, 0, 650) == 8
    assert ns["_ca_clamped_target"](24, 0, 576) == 8
    for tape in ({}, lambda seat, t: "not-a-dict",
                 lambda seat, t: (_ for _ in ()).throw(RuntimeError("tape down"))):
        bad = _variant_ns(mode, tape)
        assert bad["_ca_clamped_target"](27, 0, 650) == 8
    # 权重口径对照：同 k 下 m>0 抬需求幅度=weight（tuned 半计/lean 不计）
    weight = inject_controller_clamp._WHEAT_SLOT_WEIGHTS[mode]
    with_w = _variant_ns(mode, g._clamp_tape(2, 4))["_ca_future_plant_demand"](0, 650)
    without_w = _variant_ns(mode, g._clamp_tape(2, 0))["_ca_future_plant_demand"](0, 650)
    assert with_w - without_w == 4 * weight
