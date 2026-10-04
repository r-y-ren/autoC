"""test_layer_s（继承 R10 验收③(c)）：运行时五函数 + invariant/surplus/demand/harvest 用例组。"""

import pytest

import layer_s_block


# ---- 构造三用例（R10 验收③(c)）：夹具+真值在本组，gate_equivalence_precision 复用 ----
# 每用例函数返回 {"expected", "got", "evidence"}（c3 双面为 {"truncate_side",
# "keep_side"}，各含同款三键）；test_invariant_cases 断言真值（测试真值在此不
# 搬家），gate_equivalence_precision.constructed_invariant_cases 调用同一批夹具
# 函数作门级裁决（import 复用不复制，防漂移）。夹具均为真实链路形态：假
# plan_view 的步键只含 t>当前 step 的未来步（真 _cxs_plan_view 折叠区间
# [step+1, 718]），两次调用同值 → 确定性（surplus 交叉核对不触发）。


def _invariant_case_c1_no_trunc_when_future_plant():
    """用例①（不截）：未来步 t∈[649,671] 有可完成 plants 的 BUY_SEED 不截。

    决策步 650（≥648 截断层生效），磁带未来步 670 plants 5（670+48=718≤719
    可完成）→ 需求 5 全额保护：供给=库存0+保留单5+磁带未来买0=5=需求 →
    allowed=0 → 一张不删（含非种子单原样）。
    """
    plans = {670: {"plants": {"CARROT": 5}, "buy_seed": {}}}
    obs = _obs_with_seeds({"CARROT": 0}, step=650)
    market = [["SELL", "WHEAT", 2], ["BUY_SEED", "CARROT", 5]]
    got = layer_s_block._cxs_seed_truncate(obs, {"market": market}, _make_plan_view(plans))
    return {
        "expected": [["SELL", "WHEAT", 2], ["BUY_SEED", "CARROT", 5]],
        "got": got,
        "evidence": "step=650 tape plants@670 completable (670+48=718<=719): "
                    "demand 5 = supply (0+5+0) -> allowed 0, BUY_SEED kept",
    }


def _invariant_case_c2_trunc_when_no_opportunity():
    """用例②（截）：磁带唯一 plants 在 672（不可完成）不构成需求，供给超需求即截。

    决策步 650，磁带未来步 672 plants 5（672+48=720>719 不可完成，永不构成
    需求）且供给超需求（库存0+买单6>需求0）→ allowed=6 → 两张 CARROT 买单
    整单全删，非 BUY_SEED 订单原样保留。
    """
    plans = {672: {"plants": {"CARROT": 5}, "buy_seed": {}}}
    obs = _obs_with_seeds({"CARROT": 0}, step=650)
    market = [["BUY_SEED", "CARROT", 4], ["BUY_SEED", "CARROT", 2], ["SELL", "WHEAT", 3]]
    got = layer_s_block._cxs_seed_truncate(obs, {"market": market}, _make_plan_view(plans))
    return {
        "expected": [["SELL", "WHEAT", 3]],
        "got": got,
        "evidence": "step=650 tape plants@672 not completable (672+48=720>719): "
                    "demand 0 < supply (0+6+0) -> allowed 6, both CARROT orders dropped",
    }


def _invariant_case_c3_s671_boundary():
    """用例③（s671 边界双面）：671+48=719≤719 恰可完成、672 起永不。

    截面：决策步 671（磁带真实形态仅含 t≥672）确无后续可完成种植机会，库存
    已有富余（held 2 → 供给 2+3+0=5 > 需求 0）→ allowed=3 全删。
    不截面（P2 复审修正 2026-09-23：旧夹具在 step=671 的磁带里放 670 过去步
    plants——真 _cxs_plan_view 只折叠 t>step，属真实链路不可能形态）：决策步
    670，磁带未来步 671 plants 3（671+48=719≤719 恰好可完成）构成需求 →
    供给=0+3+0=3=需求 → allowed=0 不截；同磁带 672 plants 9 不计入。
    """
    # 截面：s671 的 BUY_SEED——磁带（t≥672）确无后续可完成种植机会才截。
    plans_trunc = {672: {"plants": {"CARROT": 5}, "buy_seed": {}}}
    obs_trunc = _obs_with_seeds({"CARROT": 2}, step=671)
    market_trunc = [["BUY_SEED", "CARROT", 3]]
    got_trunc = layer_s_block._cxs_seed_truncate(
        obs_trunc, {"market": market_trunc}, _make_plan_view(plans_trunc))
    # 不截面：决策步 670 的 BUY_SEED 被 671（最后可完成步）plants 保护。
    plans_keep = {671: {"plants": {"CARROT": 3}, "buy_seed": {}},
                  672: {"plants": {"CARROT": 9}, "buy_seed": {}}}
    obs_keep = _obs_with_seeds({"CARROT": 0}, step=670)
    market_keep = [["BUY_SEED", "CARROT", 3]]
    got_keep = layer_s_block._cxs_seed_truncate(
        obs_keep, {"market": market_keep}, _make_plan_view(plans_keep))
    return {
        "truncate_side": {
            "expected": [],
            "got": got_trunc,
            "evidence": "step=671 tape only t>=672: no completable opportunity "
                        "-> demand 0 < supply (2+3+0) -> allowed 3, order dropped",
        },
        "keep_side": {
            "expected": [["BUY_SEED", "CARROT", 3]],
            "got": got_keep,
            "evidence": "step=670 tape plants@671 exactly completable (671+48=719<=719): "
                        "demand 3 = supply (0+3+0) -> allowed 0, order kept",
        },
    }


def test_invariant_cases():
    # 构造三用例真值断言（R10 验收③(c)；夹具函数同被
    # gate_equivalence_precision.constructed_invariant_cases 复用）。
    c1 = _invariant_case_c1_no_trunc_when_future_plant()
    assert c1["got"] == c1["expected"]

    c2 = _invariant_case_c2_trunc_when_no_opportunity()
    assert c2["got"] == c2["expected"]

    c3 = _invariant_case_c3_s671_boundary()
    assert c3["truncate_side"]["got"] == c3["truncate_side"]["expected"]
    assert c3["keep_side"]["got"] == c3["keep_side"]["expected"]


def test_surplus_uncertain_returns_none():
    # 零误杀验收（_cxs_seed_surplus 的 None 路径全组）：③demand None ④两次
    # plan_view 结果不一致 ⑤kept_orders 畸形 ⑥observation 种子字段缺失/异常。
    # 全组传 current_plants=0（确证当前步无该品种植——隔离所测失败面；None
    # 入口语义另见 test_surplus_current_plants_unknown_returns_none）。
    plans = {650: {"plants": {"CARROT": 4}, "buy_seed": {}}}  # 650+48=698≤719 → demand=4
    obs = {"step": 650, "private": {"seeds": {"CARROT": 2}}}
    kept = [["BUY_SEED", "CARROT", 3]]

    # ③ demand 不确定：plan_view 返回 None / 调用抛异常 / 形参不可调用 → None。
    assert layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_plan_view(None), 0) is None
    assert layer_s_block._cxs_seed_surplus(
        "CARROT", obs, kept, _make_plan_view(RuntimeError("tape parse boom")), 0
    ) is None
    assert layer_s_block._cxs_seed_surplus("CARROT", obs, kept, None, 0) is None

    # ④ 两次 plan_view 结果不一致（非确定性）：demand 调用取 a、本函数再调取 b，
    # 重算需求 5 ≠ 4 被交叉核对捕获 → None；第二次返回非 dict 同样 None。
    a = {650: {"plants": {"CARROT": 4}, "buy_seed": {}}}
    b = {650: {"plants": {"CARROT": 5}, "buy_seed": {}}}
    assert layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_seq_plan_view([a, b]), 0) is None
    assert layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_seq_plan_view([a, None]), 0) is None

    # ⑤ kept_orders 畸形 → None：容器非 list/tuple / 短订单（无论操作类型）/
    # 订单非序列 / 本品项 BUY_SEED qty 非整数（str/None/bool/半值 float）。
    bad_kept = [
        None,
        "not-orders",
        {"0": ["BUY_SEED", "CARROT", 3]},
        [["BUY_SEED", "CARROT"]],                    # 长度<3 的本品项单
        [["SELL", "WHEAT"]],                         # 非 BUY_SEED 短单同样不可解析
        [["BUY_LAND"]],                              # 同上（无法确认不是本品项）
        [7],                                         # 订单非 list/tuple
        [None],
        [["BUY_SEED", "CARROT", "3"]],               # qty 字符串
        [["BUY_SEED", "CARROT", None]],
        [["BUY_SEED", "CARROT", True]],              # bool 非计数
        [["BUY_SEED", "CARROT", 2.5]],               # 半粒种子
    ]
    for bad in bad_kept:
        got = layer_s_block._cxs_seed_surplus("CARROT", obs, bad, _make_plan_view(plans), 0)
        assert got is None, bad

    # ⑥ observation 种子字段缺失/类型异常 / step 缺失或非整数 → None。
    bad_obs = [
        None,
        {"step": 650},                                        # 缺 private
        {"step": 650, "private": {}},                         # 缺 seeds
        {"step": 650, "private": {"seeds": "x"}},             # seeds 非 dict
        {"step": 650, "private": {"seeds": {"CARROT": "5"}}},  # 库存计数字符串
        {"step": 650, "private": {"seeds": {"CARROT": 2.5}}},
        {"step": 650, "private": {"seeds": {"CARROT": True}}},
        {"private": {"seeds": {"CARROT": 2}}},                # 缺 step（无法判 t>当前步）
        {"step": "650", "private": {"seeds": {"CARROT": 2}}},  # step 非整数
    ]
    for bad in bad_obs:
        got = layer_s_block._cxs_seed_surplus("CARROT", bad, kept, _make_plan_view(plans), 0)
        assert got is None, bad


def test_harvest_boundary_s671():
    # 契约锚点用例（责任文档 harvest 边界组）：CARROT/WHEAT 首收 48 步级。
    # 671+48=719 ≤ 719 → True（day27+2=29 恰可完成：引擎天粒度，评审
    # 2026-09-23 修正 off-by-one，旧界 718 误杀此步）；672+48=720 > 719 → False。
    assert layer_s_block._cxs_harvest_completable(671, "CARROT") is True
    assert layer_s_block._cxs_harvest_completable(672, "CARROT") is False
    assert layer_s_block._cxs_harvest_completable(671, "WHEAT") is True
    assert layer_s_block._cxs_harvest_completable(672, "WHEAT") is False


def test_harvest_per_crop_boundaries():
    # 每种作物两端边界各一：s = 719-fh → True（恰可完成）；s = 720-fh → False。
    deadline = layer_s_block._CXS_PLANT_DEADLINE_SUM
    for crop, fh in layer_s_block.FIRST_HARVEST_STEPS.items():
        assert layer_s_block._cxs_harvest_completable(deadline - fh, crop) is True, (crop, fh)
        assert layer_s_block._cxs_harvest_completable(deadline - fh + 1, crop) is False, (crop, fh)


def test_harvest_conservative_true_on_missing_or_bad_input():
    # 零误杀铁律：未知作物 / None / 类型异常 / 常数表缺失 → 一律 True（不截）。
    assert layer_s_block._cxs_harvest_completable(718, "BAMBOO") is True  # 未知作物
    assert layer_s_block._cxs_harvest_completable(None, "CARROT") is True  # step=None
    assert layer_s_block._cxs_harvest_completable(671, None) is True  # crop=None
    assert layer_s_block._cxs_harvest_completable(671, ["CARROT"]) is True  # crop 不可哈希
    assert layer_s_block._cxs_harvest_completable("671", "CARROT") is True  # step 非数
    assert layer_s_block._cxs_harvest_completable(671, "CARROT", {}) is True  # 覆盖表缺常数
    assert layer_s_block._cxs_harvest_completable(671, "CARROT", 48) is True  # 覆盖表非映射
    assert layer_s_block._cxs_harvest_completable(671, "CARROT", {"CARROT": None}) is True
    assert layer_s_block._cxs_harvest_completable(671, "CARROT", {"CARROT": "48"}) is True


def test_harvest_explicit_table_override():
    # first_harvest_steps 形参：显式表生效；None=回退模块级表（672+48=720>719→False）。
    assert layer_s_block._cxs_harvest_completable(671, "CARROT", {"CARROT": 47}) is True  # 718≤719
    assert layer_s_block._cxs_harvest_completable(671, "CARROT", {"CARROT": 48}) is True  # 719≤719 恰边界
    assert layer_s_block._cxs_harvest_completable(672, "CARROT", {"CARROT": 48}) is False  # 720>719
    assert layer_s_block._cxs_harvest_completable(671, "CARROT", None) is True  # 模块表：719≤719
    assert layer_s_block._cxs_harvest_completable(672, "CARROT", None) is False


# ---- _cxs_completable_plant_demand 用例组（demand：逐品项可完成种+收的 PLANT 种子需求）----

_OBS = {"step": 650}  # 本函数不读 observation 内容，仅透传给 plan_view


def _make_plan_view(retval):
    """plan_view 假件：retval 为 Exception 实例则抛出，否则原样返回。"""
    def view(obs):
        if isinstance(retval, Exception):
            raise retval
        return retval
    return view


def test_demand_mixed_steps_sum_only_completable():
    # ① 混合步号求和：CARROT(fh=48) 600/670 可完成计入（670+48=718≤719），
    # 672 超期不计（672+48=720>719）；同条目 buy_seed 数量不入 demand。
    plans = {
        600: {"plants": {"CARROT": 1}, "buy_seed": {}},
        670: {"plants": {"CARROT": 3}, "buy_seed": {"CARROT": 2}},
        672: {"plants": {"CARROT": 2}, "buy_seed": {}},
    }
    got = layer_s_block._cxs_completable_plant_demand("CARROT", _OBS, _make_plan_view(plans))
    assert got == 4


def test_demand_crop_absent_returns_zero():
    # ② 品项不在任何 plants → 0（确证无未来需求），不是 None。
    plans = {650: {"plants": {"WHEAT": 3}, "buy_seed": {"MELON": 1}}}
    got = layer_s_block._cxs_completable_plant_demand("CARROT", _OBS, _make_plan_view(plans))
    assert got == 0


def test_demand_plan_view_none_or_raises_returns_none():
    # ③④ plan_view 返回 None / 调用抛异常 → None（不确定=上游零截断）。
    assert layer_s_block._cxs_completable_plant_demand("CARROT", _OBS, _make_plan_view(None)) is None
    assert layer_s_block._cxs_completable_plant_demand(
        "CARROT", _OBS, _make_plan_view(RuntimeError("tape parse boom"))
    ) is None


def test_demand_plan_view_not_callable_returns_none():
    # plan_view 形参本身为 None / 非可调用对象 → None。
    assert layer_s_block._cxs_completable_plant_demand("CARROT", _OBS, None) is None
    assert layer_s_block._cxs_completable_plant_demand("CARROT", _OBS, "not-a-callable") is None


def test_demand_malformed_structure_returns_none():
    # ⑤ 结构畸形：外层非 dict / 条目非 dict / plants 非 dict / 计数非数
    # （字符串、None、bool、非整浮点）→ 一律 None。
    bad_cases = [
        ["not", "a", "dict"],                           # 外层非 dict
        {650: 3},                                       # 条目非 dict
        {650: {"plants": ["CARROT"], "buy_seed": {}}},  # plants 非 dict
        {650: {"plants": {"CARROT": "3"}}},             # 计数非数（字符串）
        {650: {"plants": {"CARROT": None}}},            # 计数 None
        {650: {"plants": {"CARROT": True}}},            # bool 非计数
        {650: {"plants": {"CARROT": 2.5}}},             # 半粒种子=不可解析
    ]
    for bad in bad_cases:
        got = layer_s_block._cxs_completable_plant_demand("CARROT", _OBS, _make_plan_view(bad))
        assert got is None, bad


def test_demand_no_plant_within_horizon_returns_zero():
    # ⑥ horizon 内无 PLANT：空计划 / 仅 buy_seed / plants 为空 / 条目缺 plants 键 → 0。
    empty_cases = [
        {},
        {660: {"plants": {}, "buy_seed": {"CARROT": 5}}},
        {660: {"buy_seed": {"CARROT": 5}}},
    ]
    for plans in empty_cases:
        got = layer_s_block._cxs_completable_plant_demand("CARROT", _OBS, _make_plan_view(plans))
        assert got == 0, plans


def test_demand_multi_actor_units_accumulate():
    # ⑦ 同步多 actor：单步 plants 计数>1 全额计入；跨步累计；他品项不串扰。
    plans = {
        650: {"plants": {"CARROT": 4}, "buy_seed": {}},           # 同步 4 actor 各 1 格
        655: {"plants": {"CARROT": 3, "WHEAT": 9}, "buy_seed": {}},  # WHEAT 不入 CARROT 需求
    }
    got = layer_s_block._cxs_completable_plant_demand("CARROT", _OBS, _make_plan_view(plans))
    assert got == 7


# ---- _cxs_seed_surplus 用例组（surplus：允许删除量=min(max(0,供给−需求),本回合购买量)）----


def _make_seq_plan_view(seq):
    """序列假件：按调用次序逐个返回 seq 元素（Exception 实例则抛出）；耗尽抛 StopIteration。"""
    it = iter(seq)

    def view(obs):
        rv = next(it)
        if isinstance(rv, Exception):
            raise rv
        return rv

    return view


def _obs_with_seeds(seeds, step=650):
    """surplus 用观测假件：private.seeds 为库存（基座字段路径 private.seeds.get(crop, 0)）。"""
    return {"step": step, "private": {"seeds": dict(seeds)}}


def test_surplus_positive_returns_supply_minus_demand():
    # ① surplus 为正：允许删除量 = 供给(有效库存+保留单+磁带未来) − 需求，未触钳制。
    # demand=4（650+48=698≤719）；供给=1-0+10+0=11 → 允许 7（< 本回合购买 10，未钳）。
    plans = {650: {"plants": {"CARROT": 4}, "buy_seed": {}}}
    obs = _obs_with_seeds({"CARROT": 1})
    kept = [["BUY_SEED", "CARROT", 10], ["SELL", "WHEAT", 2]]  # 他品项订单不影响本品项
    got = layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_plan_view(plans), 0)
    assert got == 7 == (1 + 10 + 0) - 4


def test_surplus_supply_below_demand_returns_zero():
    # ② 供给 ≤ 需求 → 0（确证无剩余），不是 None。
    plans = {650: {"plants": {"CARROT": 4}, "buy_seed": {}}}  # demand=4
    obs = _obs_with_seeds({"CARROT": 1})
    kept = [["BUY_SEED", "CARROT", 1]]  # 供给=1-0+1+0=2 ≤ 4
    got = layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_plan_view(plans), 0)
    assert got == 0 and got is not None


def test_surplus_clamped_to_kept_purchase():
    # ⑦ 钳制：允许删除量不超过本回合该品项购买量（删除对象只可能是本回合订单）。
    plans = {650: {"plants": {}, "buy_seed": {}}}  # demand=0
    obs = _obs_with_seeds({"CARROT": 10})
    kept = [["BUY_SEED", "CARROT", 2]]
    got = layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_plan_view(plans), 0)
    assert got == 2  # min(max(0, 10-0+2-0), 2)：原始剩余 12 被钳到本回合购买量 2


def test_surplus_tape_future_buy_counts_and_past_excluded():
    # ⑧ 磁带未来 BUY_SEED 计入供给且只累 t>当前步（650）：651 的 4 计入、649 的 7 不计。
    # demand=6（650 步 plants）；库存 0、保留单 8：有未来单 → 供给 0-0+8+4=12 → 允许 6；
    # 无未来单（过去单不计）→ 供给 8 → 允许 2。若 649 的 7 被误计入则得 8，两断言皆破。
    future = {
        649: {"plants": {}, "buy_seed": {"CARROT": 7}},   # 过去买单不计（649<650）
        650: {"plants": {"CARROT": 6}, "buy_seed": {}},   # 当前步需求计入、当前步买单不计
        651: {"plants": {}, "buy_seed": {"CARROT": 4}},   # 未来买单计入
    }
    obs = _obs_with_seeds({"CARROT": 0}, step=650)
    kept = [["BUY_SEED", "CARROT", 8]]
    got = layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_plan_view(future), 0)
    assert got == 6 == (0 + 8 + 4) - 6
    past_only = {
        649: {"plants": {}, "buy_seed": {"CARROT": 7}},
        650: {"plants": {"CARROT": 6}, "buy_seed": {}},
    }
    got2 = layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_plan_view(past_only), 0)
    assert got2 == 2 == (0 + 8 + 0) - 6


def test_surplus_current_plants_deducted_tight_balance_no_overdelete():
    # ⑨（评审例 2026-09-23）当前步 PLANT 消耗扣减后紧平衡不超删：held=10、
    # plants=8 → 有效库存 2；kept 单 5、磁带未来买 5、demand=12 → 供给
    # 2+5+5=12=需求 → 允许删 0（不扣减则 10+5+5−12=3 → 钳 5 → 超删至多 5，误杀向）。
    plans = {
        650: {"plants": {"CARROT": 12}, "buy_seed": {}},  # 650+48=698≤719 → demand=12
        660: {"plants": {}, "buy_seed": {"CARROT": 5}},   # 660>650 → 磁带未来买 5
    }
    obs = _obs_with_seeds({"CARROT": 10}, step=650)
    kept = [["BUY_SEED", "CARROT", 5]]
    got = layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_plan_view(plans), 8)
    assert got == 0 and got is not None


def test_surplus_current_plants_unknown_returns_none():
    # ⑩ current_plants=None（当前步消耗未知）→ 直接 None（零误杀：不确定=不截），
    # 即便其余输入完全可解析；参数校验：负数 / bool / 字符串 / 半值 float → None。
    plans = {650: {"plants": {"CARROT": 4}, "buy_seed": {}}}
    obs = _obs_with_seeds({"CARROT": 1})
    kept = [["BUY_SEED", "CARROT", 3]]
    assert layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_plan_view(plans)) is None
    for bad in (-1, -8, True, "8", 2.5, 1.5):
        got = layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_plan_view(plans), bad)
        assert got is None, bad


def test_surplus_current_plants_above_held_clamps_to_zero():
    # ⑪ plants > held：有效库存钳 0（不为负、不污染供给式）——3−8 → 0 而非 −5。
    plans = {}
    obs = _obs_with_seeds({"CARROT": 3}, step=650)
    kept = [["BUY_SEED", "CARROT", 2]]
    got = layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_plan_view(plans), 8)
    assert got == 2  # min(max(0, 0+2+0−0), 2)：钳 0 后正常放行


# ---- _cxs_seed_truncate 用例组（truncate：纯减法过滤主函数）----


def _spy_plan_view(retval):
    """快道零足迹用假件：返回 retval 并计数调用（快道断言 plan_view 零调用）。"""
    def view(obs):
        view.calls += 1
        return retval
    view.calls = 0
    return view


def test_truncate_fast_paths_return_original_object():
    # ① 零足迹快道（原对象 is 断言 + plan_view 零调用）：
    # step<648 / market 为空表 / 无 BUY_SEED / market 键缺失（→None 原样）。
    m1 = [["BUY_SEED", "CARROT", 5]]
    pv1 = _spy_plan_view({660: {"plants": {}, "buy_seed": {}}})
    got1 = layer_s_block._cxs_seed_truncate(
        _obs_with_seeds({}, step=600), {"market": m1}, pv1)
    assert got1 is m1 and pv1.calls == 0  # step=600<648

    m2 = []
    pv2 = _spy_plan_view(None)
    got2 = layer_s_block._cxs_seed_truncate(
        _obs_with_seeds({}, step=650), {"market": m2}, pv2)
    assert got2 is m2 and pv2.calls == 0  # 无 market 订单（空表）

    m3 = [["SELL", "WHEAT", 2], ["HIRE", 1, 0]]
    pv3 = _spy_plan_view(None)
    got3 = layer_s_block._cxs_seed_truncate(
        _obs_with_seeds({}, step=700), {"market": m3}, pv3)
    assert got3 is m3 and pv3.calls == 0  # 无 BUY_SEED

    pv4 = _spy_plan_view(None)
    got4 = layer_s_block._cxs_seed_truncate(_obs_with_seeds({}, step=700), {}, pv4)
    assert got4 is None and pv4.calls == 0  # market 键缺失 → 原样（None）


def test_truncate_crop_uncertain_means_zero_truncation():
    # ② 品项 None→零截断：plan_view 整卷 None → 全体品项零截断（内容原样）；
    # 单品项 None（该品项 plants 计数畸形）→ 仅该品项保留、他品项照常截；
    # kept 含 len<3 短单 → surplus 不可解析 → 同样零截断。
    obs = _obs_with_seeds({}, step=650)
    m = [["BUY_SEED", "CARROT", 5], ["BUY_SEED", "WHEAT", 5]]
    got = layer_s_block._cxs_seed_truncate(obs, {"market": m}, _make_plan_view(None))
    assert got == m

    weird = {660: {"plants": {"WEIRD": "x"}, "buy_seed": {}}}  # WEIRD 计数畸形
    m2 = [["BUY_SEED", "WEIRD", 2], ["BUY_SEED", "CARROT", 5]]
    got2 = layer_s_block._cxs_seed_truncate(obs, {"market": m2}, _make_plan_view(weird))
    assert got2 == [["BUY_SEED", "WEIRD", 2]]  # CARROT 需求0→全删；WEIRD None→保留

    m3 = [["BUY_SEED", "CARROT", 5], ["SELL", "WHEAT"]]  # len<3 短单 → kept 不可解析
    got3 = layer_s_block._cxs_seed_truncate(obs, {"market": m3}, _make_plan_view({}))
    assert got3 == m3


def test_truncate_back_to_front_whole_order_deletion_keeps_slots():
    # ③ 从后往前整单删除 + 槽位顺序保持：allowed=min(max(0, 0+7−3), 7)=4 →
    # 末单 qty2 删（累计2）、中单 qty3 超额跳过（2+3>4 继续向前）、首单 qty2
    # 删（2+2≤4）；SELL 原位保留，无重排无插入。
    plans = {660: {"plants": {"CARROT": 3}, "buy_seed": {}}}  # 660+48=708≤719
    obs = _obs_with_seeds({"CARROT": 0}, step=650)
    market = [["BUY_SEED", "CARROT", 2], ["SELL", "WHEAT", 1],
              ["BUY_SEED", "CARROT", 3], ["BUY_SEED", "CARROT", 2]]
    got = layer_s_block._cxs_seed_truncate(obs, {"market": market}, _make_plan_view(plans))
    assert got == [["SELL", "WHEAT", 1], ["BUY_SEED", "CARROT", 3]]


def test_truncate_partial_allowed_deletes_latest_only():
    # ④ 部分 allowed：allowed=min(max(0, 0+7−5), 7)=2 → 从后往前仅末单 qty2
    # 可整删（0+2≤2），中单/首单（2+3>2、2+2>2）保留——删后面的单、保留前面的单。
    plans = {660: {"plants": {"CARROT": 5}, "buy_seed": {}}}
    obs = _obs_with_seeds({"CARROT": 0}, step=650)
    market = [["BUY_SEED", "CARROT", 2], ["SELL", "WHEAT", 1],
              ["BUY_SEED", "CARROT", 3], ["BUY_SEED", "CARROT", 2]]
    got = layer_s_block._cxs_seed_truncate(obs, {"market": market}, _make_plan_view(plans))
    assert got == [["BUY_SEED", "CARROT", 2], ["SELL", "WHEAT", 1], ["BUY_SEED", "CARROT", 3]]


def test_truncate_mixed_crops_independent():
    # ⑤ 混合多品项互不干扰：CARROT 无可完成需求（plants 无该键）→ 全删；
    # WHEAT 有可完成需求 5（660+48=708≤719）且供给=需求 → 全额保护；
    # CARROT 的截断不触碰 WHEAT 单。
    plans = {660: {"plants": {"WHEAT": 5}, "buy_seed": {}}}
    obs = _obs_with_seeds({}, step=650)
    market = [["BUY_SEED", "CARROT", 5], ["BUY_SEED", "WHEAT", 5]]
    got = layer_s_block._cxs_seed_truncate(obs, {"market": market}, _make_plan_view(plans))
    assert got == [["BUY_SEED", "WHEAT", 5]]


def test_truncate_never_drops_non_seed_orders():
    # ⑥ 非 BUY_SEED 订单永不被删：allowed 覆盖全部 CARROT 买单（需求0、
    # 供给0+9 → allowed=9）时也只删 BUY_SEED，SELL/PLANT 等原样原位保留。
    obs = _obs_with_seeds({}, step=650)
    market = [["SELL", "WHEAT", 2], ["BUY_SEED", "CARROT", 9],
              ["PLANT", "CARROT", 4], ["SELL", "MELON", 1]]
    got = layer_s_block._cxs_seed_truncate(obs, {"market": market}, _make_plan_view({}))
    assert got == [["SELL", "WHEAT", 2], ["PLANT", "CARROT", 4], ["SELL", "MELON", 1]]


def test_truncate_current_step_plants_counted_and_malformed_action_zero_truncation():
    # ⑦ truncate 传参链路（评审 2026-09-23 修正②）：action farmer+hands 的当前步
    # PLANT 被正确统计并扣减库存（held=10/plants=8 → 有效 2；demand=12、kept 5、
    # 磁带未来买 5 → 供给 2+5+5=12=需求 → allowed=0 不截）；对照无 PLANT 则
    # 供给 20 → allowed=5 → 整单删；畸形 action（farmer 非 list）→ 计数解析失败
    # → 逐品项 current_plants=None → surplus None → 零截断（原对象）。
    plans = {
        650: {"plants": {"CARROT": 12}, "buy_seed": {}},  # demand=12（698≤719）
        660: {"plants": {}, "buy_seed": {"CARROT": 5}},   # 磁带未来买 5
    }
    obs = _obs_with_seeds({"CARROT": 10}, step=650)
    pv = _make_plan_view(plans)

    market = [["BUY_SEED", "CARROT", 5]]
    action = {"market": market, "farmer": ["PLANT", "CARROT"],
              "hands": [["PLANT", "CARROT"]] * 7}  # farmer 1 + hands 7 = 当前步 8×PLANT
    got = layer_s_block._cxs_seed_truncate(obs, action, pv)
    assert got is market  # allowed=0 → 零截断零足迹

    market2 = [["BUY_SEED", "CARROT", 5]]
    action2 = {"market": market2, "farmer": ["PASS"]}  # 对照：当前步无 PLANT
    got2 = layer_s_block._cxs_seed_truncate(obs, action2, pv)
    assert got2 == []  # 供给 10+5+5=20 → allowed=min(8,5)=5 → 整单删

    market3 = [["BUY_SEED", "CARROT", 5]]
    action3 = {"market": market3, "farmer": 7}  # 畸形：farmer 非 list → 解析失败
    got3 = layer_s_block._cxs_seed_truncate(obs, action3, pv)
    assert got3 is market3  # current_plants=None → surplus None → 零截断


# ---- _cxs_agent 用例组（运行时入口：六条路径 + 独立导入态结构不变式）----


class _RecordingHost:
    """假宿主：固定返回 action，记录 (observation, configuration) 调用序列。"""

    def __init__(self, action):
        self.action = action
        self.calls = []

    def __call__(self, observation, configuration=None):
        self.calls.append((observation, configuration))
        return self.action


def _patch_host(monkeypatch, action):
    host = _RecordingHost(action)
    monkeypatch.setattr(layer_s_block, "_CXS_HOST", host)
    return host


def test_agent_standalone_host_absent_and_is_last_callable():
    # 独立导入态结构不变式：宿主不存在（模块首部无可捕获 callable → _CXS_HOST=None，
    # 测试注入通道=monkeypatch 模块级 _CXS_HOST）；_cxs_agent 是本模块最后 callable
    # （注入态"末 callable=_cxs_agent"官方入口语义在测试态的同构投影）。
    assert layer_s_block._CXS_HOST is None
    last = [v for v in list(vars(layer_s_block).values()) if callable(v)][-1]
    assert last is layer_s_block._cxs_agent


def test_agent_step_below_from_same_object_and_plan_view_unused(monkeypatch):
    # ① step<648 → 返回宿主动作同对象且 plan_view 零调用；宿主按
    # (observation, configuration) 原样收参（configuration 透传）。
    market = [["BUY_SEED", "CARROT", 5]]
    action = {"market": market, "farmer": ["PASS"]}
    host = _patch_host(monkeypatch, action)
    pv = _spy_plan_view({660: {"plants": {}, "buy_seed": {}}})
    monkeypatch.setattr(layer_s_block, "_cxs_plan_view", pv)
    obs = {"step": 600, "player": 0}
    cfg = {"sentinel": True}
    got = layer_s_block._cxs_agent(obs, cfg)
    assert got is action  # 同对象零足迹
    assert pv.calls == 0  # plan_view 零调用（快道早于截断层）
    assert host.calls == [(obs, cfg)]  # 宿主调用在 try 外，参数原样透传
    got2 = layer_s_block._cxs_agent(obs)
    assert got2 is action and host.calls[-1] == (obs, None)  # configuration 缺省 None


def test_agent_no_seed_orders_same_object_zero_footprint(monkeypatch):
    # ② step≥648 无 BUY_SEED → 同对象零足迹；market 缺失 / action 非 dict /
    # observation 非 dict（解析异常）同样原样返回宿主产物。
    action = {"market": [["SELL", "WHEAT", 2], ["HIRE", 1, 0]], "farmer": ["PASS"]}
    pv = _spy_plan_view(None)
    _patch_host(monkeypatch, action)
    monkeypatch.setattr(layer_s_block, "_cxs_plan_view", pv)
    assert layer_s_block._cxs_agent({"step": 700}) is action  # 无 BUY_SEED
    assert pv.calls == 0

    action2 = {"farmer": ["PASS"]}  # market 键缺失
    _patch_host(monkeypatch, action2)
    assert layer_s_block._cxs_agent({"step": 700}) is action2
    assert pv.calls == 0

    action3 = ["not", "a", "dict"]  # 宿主动作非 dict
    _patch_host(monkeypatch, action3)
    assert layer_s_block._cxs_agent({"step": 700}) is action3

    action4 = {"market": [["BUY_SEED", "CARROT", 5]]}  # observation 非 dict → 解析异常
    _patch_host(monkeypatch, action4)
    assert layer_s_block._cxs_agent(None) is action4  # fail-safe：原样返回
    assert pv.calls == 0  # 全程未触 plan_view


def test_agent_truncates_via_full_chain_with_fakes(monkeypatch):
    # ③ 有 BUY_SEED → dict(action, market=…) 且被过滤单恰为截断层判定量
    # （假宿主+真截断层+假 plan_view 全链路）：磁带唯一 plants 在 672
    # （672+48=720>719 不构成需求）且无磁带未来买 → 供给=0+6+0=6 > 需求 0 →
    # allowed=6 → 两张 CARROT 买单整单删、SELL 原位保留。
    market = [["BUY_SEED", "CARROT", 4], ["BUY_SEED", "CARROT", 2], ["SELL", "WHEAT", 3]]
    action = {"market": market, "farmer": ["PASS"]}
    _patch_host(monkeypatch, action)
    pv = _spy_plan_view({672: {"plants": {"CARROT": 5}, "buy_seed": {}}})
    monkeypatch.setattr(layer_s_block, "_cxs_plan_view", pv)
    obs = _obs_with_seeds({"CARROT": 0}, step=650)
    got = layer_s_block._cxs_agent(obs)
    assert got == {"market": [["SELL", "WHEAT", 3]], "farmer": ["PASS"]}
    assert got is not action  # 慢道按契约建新 action dict（dict(action, market=…)）
    assert got["farmer"] is action["farmer"]  # 浅拷贝：其余键值仍原对象
    assert pv.calls >= 1  # 截断层确实消费了 plan_view（全链路非空转）


def test_agent_plan_view_none_zero_truncation(monkeypatch):
    # ④ 宿主正常但 plan_view None → 品项 None→零截断链路：内容原样相等，
    # market 仍零删除原对象（慢道新 action dict 载原 market）。
    market = [["BUY_SEED", "CARROT", 5], ["SELL", "WHEAT", 1]]
    action = {"market": market, "farmer": ["PASS"]}
    _patch_host(monkeypatch, action)
    monkeypatch.setattr(layer_s_block, "_cxs_plan_view", _make_plan_view(None))
    got = layer_s_block._cxs_agent(_obs_with_seeds({}, step=650))
    assert got == action and got["market"] is market


def test_agent_truncate_exception_falls_back_to_host_action(monkeypatch):
    # ⑤ 截断层抛异常 → 返回基座 action 原样（fail-safe，同对象，绝不崩）。
    action = {"market": [["BUY_SEED", "CARROT", 5]]}
    _patch_host(monkeypatch, action)

    def _boom(observation, action, plan_view):
        raise RuntimeError("truncate boom")

    monkeypatch.setattr(layer_s_block, "_cxs_seed_truncate", _boom)
    monkeypatch.setattr(layer_s_block, "_cxs_plan_view", _spy_plan_view(None))
    assert layer_s_block._cxs_agent(_obs_with_seeds({}, step=650)) is action


def test_agent_host_exception_propagates(monkeypatch):
    # ⑥ 宿主调用在 try 之外：宿主抛异常 → 向上传播，不被 fail-safe 吞噬
    # （宿主坏了不是本层责任——与 ⑤ 的边界）。
    def _boom_host(observation, configuration=None):
        raise RuntimeError("host boom")

    monkeypatch.setattr(layer_s_block, "_CXS_HOST", _boom_host)
    with pytest.raises(RuntimeError):
        layer_s_block._cxs_agent({"step": 650})


def test_agent_full_stack_with_fake_impl_and_real_plan_view(monkeypatch):
    # 全栈集成：假宿主 + 真 _cxs_plan_view（假 _IMPL 双路磁带）+ 真截断层。
    # 2 号路 672 步 CARROT PLANT（672+48=720>719 → 不构成需求）且磁带无未来
    # CARROT 买单 → 供给=库存0+保留单6+磁带0=6 → allowed=6 → 两张 CARROT 买单全删。
    route2 = _tape({672: {"farmer": ["PLANT", "CARROT"]}})
    _patch_impl(monkeypatch, {0: {"route": 1}}, {1: _tape({}), 2: route2})
    market = [["BUY_SEED", "CARROT", 4], ["BUY_SEED", "CARROT", 2], ["SELL", "WHEAT", 3]]
    action = {"market": market, "farmer": ["PASS"]}
    _patch_host(monkeypatch, action)
    obs = {"step": 650, "player": 0, "private": {"seeds": {"CARROT": 0}}}
    got = layer_s_block._cxs_agent(obs)
    assert got == {"market": [["SELL", "WHEAT", 3]], "farmer": ["PASS"]}


# ---- _cxs_plan_view 用例组（内联适配器：基座磁带折叠 → 截断层只读视图）----


class _FakeChassis:
    def __init__(self, players, routes):
        self.players = players
        self.routes = routes


class _FakeImpl:
    def __init__(self, chassis):
        self.chassis = chassis


def _tape(entries):
    """720 槽磁带假件：entries={t: 步字典}，其余步 None（越界/非 dict=空步）。"""
    tape = [None] * 720
    for t, entry in entries.items():
        tape[t] = entry
    return tape


def _patch_impl(monkeypatch, players, routes):
    impl = _FakeImpl(_FakeChassis(players, routes))
    monkeypatch.setattr(layer_s_block, "_IMPL", impl, raising=False)
    return impl


def test_plan_view_standalone_without_impl_returns_none():
    # 独立导入测试态：基座 _IMPL 单例不存在 → None（不确定=零截断）。
    assert layer_s_block._cxs_plan_view({"step": 650, "player": 0}) is None


def test_plan_view_folds_tapes_with_day27_route_switch(monkeypatch):
    # 折叠契约：plants=farmer+hands 的 PLANT 逐品计数；buy_seed=market 中
    # BUY_SEED qty（max(0,int) 钳非负）；t≥648 走 2 号路（day27 路由换算，
    # 侦察行号 2168/2342/2583/4888）；未知作物不入表；空步不入表。
    route1 = _tape({647: {"farmer": ["PLANT", "CARROT"],
                          "hands": [["PLANT", "WHEAT"], ["PASS"]],
                          "market": [["BUY_SEED", "CARROT", 3]]}})
    route2 = _tape({
        648: {"farmer": ["PASS"],
              "market": [["BUY_SEED", "MELON", 2], ["SELL", "WHEAT", 1]]},
        660: {"farmer": ["PLANT", "CARROT"], "hands": [["PLANT", "CARROT"]]},
        670: {"farmer": ["PLANT", "BAMBOO"],
              "market": [["BUY_SEED", "BAMBOO", 5], ["BUY_SEED", "WHEAT", -4]]},
    })
    _patch_impl(monkeypatch, {0: {"route": 1}}, {1: route1, 2: route2})
    got = layer_s_block._cxs_plan_view({"step": 646, "player": 0})
    assert got == {
        647: {"plants": {"CARROT": 1, "WHEAT": 1}, "buy_seed": {"CARROT": 3}},
        648: {"plants": {}, "buy_seed": {"MELON": 2}},  # 648 起切 2 号路；SELL 不入
        660: {"plants": {"CARROT": 2}, "buy_seed": {}},
        670: {"plants": {}, "buy_seed": {"WHEAT": 0}},  # BAMBOO 不在表；负 qty 钳 0
    }


def test_plan_view_all_empty_steps_returns_none(monkeypatch):
    # 整卷无 plants/buys → out 为空 → None（磁带步全空 / 越界 None 均为空步）。
    _patch_impl(monkeypatch, {0: {"route": 1}}, {1: _tape({}), 2: _tape({})})
    assert layer_s_block._cxs_plan_view({"step": 646, "player": 0}) is None


def test_plan_view_guard_paths_return_none(monkeypatch):
    # 守卫面：席位无路由（players 缺席）/route 不在 routes/step<0（缺省 -1）/
    # observation 非 dict / 磁带读取抛异常 → 一律 None（适配器不抛）。
    _patch_impl(monkeypatch, {}, {1: _tape({})})
    assert layer_s_block._cxs_plan_view({"step": 650, "player": 0}) is None
    _patch_impl(monkeypatch, {0: {"route": 9}}, {1: _tape({})})
    assert layer_s_block._cxs_plan_view({"step": 650, "player": 0}) is None
    _patch_impl(monkeypatch, {0: {"route": 1}}, {1: _tape({})})
    assert layer_s_block._cxs_plan_view({"player": 0}) is None  # 缺 step → -1
    assert layer_s_block._cxs_plan_view(None) is None  # observation 非 dict

    class _Boom:
        @property
        def chassis(self):
            raise RuntimeError("chassis boom")

    monkeypatch.setattr(layer_s_block, "_IMPL", _Boom(), raising=False)
    assert layer_s_block._cxs_plan_view({"step": 650, "player": 0}) is None
