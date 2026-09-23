"""test_layer_s（继承 R10 验收③(c)）：运行时五函数 + invariant/surplus/demand/harvest 用例组。"""

import pytest

import layer_s_block


def test_invariant_cases():
    # 构造三用例（R10 验收③(c)，责任文档 constructed_invariant_cases 契约在
    # test_layer_s 的接线面——gate_equivalence_precision 复用同构夹具）：
    # ①未来仍有可完成 PLANT 机会的 BUY_SEED 不截；②确无未来机会且供给超需求
    # 的截；③s671 边界：CARROT BUY_SEED@672 时刻（当前 step=671）仅当磁带
    # 确无后续可完成种植机会才截。假 plan_view 构造（两次调用同值→确定性）。
    # ① 磁带有可完成机会（670+48=718≤718）→ 需求 5 全额保护：供给=库存0+
    #    保留单5+磁带未来买0=5=需求 → allowed=0 → 一张不删（含非种子单原样）。
    plans_a = {670: {"plants": {"CARROT": 5}, "buy_seed": {}}}
    obs_a = _obs_with_seeds({"CARROT": 0}, step=650)
    market_a = [["SELL", "WHEAT", 2], ["BUY_SEED", "CARROT", 5]]
    got_a = layer_s_block._cxs_seed_truncate(obs_a, {"market": market_a}, _make_plan_view(plans_a))
    assert got_a == [["SELL", "WHEAT", 2], ["BUY_SEED", "CARROT", 5]]

    # ② 确无可完成机会（磁带唯一 plants 在 671：671+48=719>718 不构成需求）且
    #    供给超需求（库存0+买单6>需求0）→ allowed=6 → 两张 CARROT 买单整单
    #    全删，非 BUY_SEED 订单原样保留。
    plans_b = {671: {"plants": {"CARROT": 5}, "buy_seed": {}}}
    obs_b = _obs_with_seeds({"CARROT": 0}, step=650)
    market_b = [["BUY_SEED", "CARROT", 4], ["BUY_SEED", "CARROT", 2], ["SELL", "WHEAT", 3]]
    got_b = layer_s_block._cxs_seed_truncate(obs_b, {"market": market_b}, _make_plan_view(plans_b))
    assert got_b == [["SELL", "WHEAT", 3]]

    # ③ s671 边界双面：672+48=720>718 → 672 步 plants 永不构成需求。
    #    截面：磁带确无后续可完成种植机会（672 plants 全不计入）且库存已有
    #    富余（held 2 → 供给 2+3+0=5 > 需求 0）→ allowed=3 全删。
    plans_c1 = {672: {"plants": {"CARROT": 5}, "buy_seed": {}}}
    obs_c1 = _obs_with_seeds({"CARROT": 2}, step=671)
    market_c1 = [["BUY_SEED", "CARROT", 3]]
    got_c1 = layer_s_block._cxs_seed_truncate(obs_c1, {"market": market_c1}, _make_plan_view(plans_c1))
    assert got_c1 == []
    #    不截面：库存无富余（held 0）且 kept 内即全部供给（磁带无 t>671 买单），
    #    670 步（670+48=718≤718 恰可完成）plants 3 构成需求 → 供给=需求=3 →
    #    allowed=0 不截。
    plans_c2 = {670: {"plants": {"CARROT": 3}, "buy_seed": {}},
                672: {"plants": {"CARROT": 9}, "buy_seed": {}}}
    obs_c2 = _obs_with_seeds({"CARROT": 0}, step=671)
    market_c2 = [["BUY_SEED", "CARROT", 3]]
    got_c2 = layer_s_block._cxs_seed_truncate(obs_c2, {"market": market_c2}, _make_plan_view(plans_c2))
    assert got_c2 == [["BUY_SEED", "CARROT", 3]]


def test_surplus_uncertain_returns_none():
    # 零误杀验收（_cxs_seed_surplus 的 None 路径全组）：③demand None ④两次
    # plan_view 结果不一致 ⑤kept_orders 畸形 ⑥observation 种子字段缺失/异常。
    plans = {650: {"plants": {"CARROT": 4}, "buy_seed": {}}}  # 650+48=698≤718 → demand=4
    obs = {"step": 650, "private": {"seeds": {"CARROT": 2}}}
    kept = [["BUY_SEED", "CARROT", 3]]

    # ③ demand 不确定：plan_view 返回 None / 调用抛异常 / 形参不可调用 → None。
    assert layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_plan_view(None)) is None
    assert layer_s_block._cxs_seed_surplus(
        "CARROT", obs, kept, _make_plan_view(RuntimeError("tape parse boom"))
    ) is None
    assert layer_s_block._cxs_seed_surplus("CARROT", obs, kept, None) is None

    # ④ 两次 plan_view 结果不一致（非确定性）：demand 调用取 a、本函数再调取 b，
    # 重算需求 5 ≠ 4 被交叉核对捕获 → None；第二次返回非 dict 同样 None。
    a = {650: {"plants": {"CARROT": 4}, "buy_seed": {}}}
    b = {650: {"plants": {"CARROT": 5}, "buy_seed": {}}}
    assert layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_seq_plan_view([a, b])) is None
    assert layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_seq_plan_view([a, None])) is None

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
        got = layer_s_block._cxs_seed_surplus("CARROT", obs, bad, _make_plan_view(plans))
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
        got = layer_s_block._cxs_seed_surplus("CARROT", bad, kept, _make_plan_view(plans))
        assert got is None, bad


def test_harvest_boundary_s671():
    # 契约锚点用例（责任文档 harvest 边界组）：CARROT/WHEAT 首收 48 步级。
    # 671+48=719 > 718 → False（来不及=构成截断理由）；670+48=718 ≤ 718 → True。
    assert layer_s_block._cxs_harvest_completable(671, "CARROT") is False
    assert layer_s_block._cxs_harvest_completable(670, "CARROT") is True
    assert layer_s_block._cxs_harvest_completable(671, "WHEAT") is False
    assert layer_s_block._cxs_harvest_completable(670, "WHEAT") is True


def test_harvest_per_crop_boundaries():
    # 每种作物两端边界各一：s = 718-fh → True（恰可完成）；s = 718-fh+1 → False。
    end = layer_s_block._CXS_SEASON_END
    for crop, fh in layer_s_block.FIRST_HARVEST_STEPS.items():
        assert layer_s_block._cxs_harvest_completable(end - fh, crop) is True, (crop, fh)
        assert layer_s_block._cxs_harvest_completable(end - fh + 1, crop) is False, (crop, fh)


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
    # first_harvest_steps 形参：显式表生效；None=回退模块级表（671+48>718→False）。
    assert layer_s_block._cxs_harvest_completable(671, "CARROT", {"CARROT": 47}) is True
    assert layer_s_block._cxs_harvest_completable(671, "CARROT", {"CARROT": 48}) is False
    assert layer_s_block._cxs_harvest_completable(671, "CARROT", None) is False


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
    # ① 混合步号求和：CARROT(fh=48) 600/670 可完成计入（670+48=718≤718），
    # 671 超期不计（671+48=719>718）；同条目 buy_seed 数量不入 demand。
    plans = {
        600: {"plants": {"CARROT": 1}, "buy_seed": {}},
        670: {"plants": {"CARROT": 3}, "buy_seed": {"CARROT": 2}},
        671: {"plants": {"CARROT": 2}, "buy_seed": {}},
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
    # ① surplus 为正：允许删除量 = 供给(库存+保留单+磁带未来) − 需求，未触钳制。
    # demand=4（650+48=698≤718）；供给=1+10+0=11 → 允许 7（< 本回合购买 10，未钳）。
    plans = {650: {"plants": {"CARROT": 4}, "buy_seed": {}}}
    obs = _obs_with_seeds({"CARROT": 1})
    kept = [["BUY_SEED", "CARROT", 10], ["SELL", "WHEAT", 2]]  # 他品项订单不影响本品项
    got = layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_plan_view(plans))
    assert got == 7 == (1 + 10 + 0) - 4


def test_surplus_supply_below_demand_returns_zero():
    # ② 供给 ≤ 需求 → 0（确证无剩余），不是 None。
    plans = {650: {"plants": {"CARROT": 4}, "buy_seed": {}}}  # demand=4
    obs = _obs_with_seeds({"CARROT": 1})
    kept = [["BUY_SEED", "CARROT", 1]]  # 供给=1+1+0=2 ≤ 4
    got = layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_plan_view(plans))
    assert got == 0 and got is not None


def test_surplus_clamped_to_kept_purchase():
    # ⑦ 钳制：允许删除量不超过本回合该品项购买量（删除对象只可能是本回合订单）。
    plans = {650: {"plants": {}, "buy_seed": {}}}  # demand=0
    obs = _obs_with_seeds({"CARROT": 10})
    kept = [["BUY_SEED", "CARROT", 2]]
    got = layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_plan_view(plans))
    assert got == 2  # min(max(0, 12-0), 2)：原始剩余 12 被钳到本回合购买量 2


def test_surplus_tape_future_buy_counts_and_past_excluded():
    # ⑧ 磁带未来 BUY_SEED 计入供给且只累 t>当前步（650）：651 的 4 计入、649 的 7 不计。
    # demand=6（650 步 plants）；库存 0、保留单 8：有未来单 → 供给 0+8+4=12 → 允许 6；
    # 无未来单（过去单不计）→ 供给 8 → 允许 2。若 649 的 7 被误计入则得 8，两断言皆破。
    future = {
        649: {"plants": {}, "buy_seed": {"CARROT": 7}},   # 过去买单不计（649<650）
        650: {"plants": {"CARROT": 6}, "buy_seed": {}},   # 当前步需求计入、当前步买单不计
        651: {"plants": {}, "buy_seed": {"CARROT": 4}},   # 未来买单计入
    }
    obs = _obs_with_seeds({"CARROT": 0}, step=650)
    kept = [["BUY_SEED", "CARROT", 8]]
    got = layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_plan_view(future))
    assert got == 6 == (0 + 8 + 4) - 6
    past_only = {
        649: {"plants": {}, "buy_seed": {"CARROT": 7}},
        650: {"plants": {"CARROT": 6}, "buy_seed": {}},
    }
    got2 = layer_s_block._cxs_seed_surplus("CARROT", obs, kept, _make_plan_view(past_only))
    assert got2 == 2 == (0 + 8 + 0) - 6


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
    plans = {660: {"plants": {"CARROT": 3}, "buy_seed": {}}}  # 660+48=708≤718
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
    # WHEAT 有可完成需求 5（660+48=708≤718）且供给=需求 → 全额保护；
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
    # （假宿主+真截断层+假 plan_view 全链路）：磁带唯一 plants 在 671
    # （671+48=719>718 不构成需求）且无磁带未来买 → 供给=0+6+0=6 > 需求 0 →
    # allowed=6 → 两张 CARROT 买单整单删、SELL 原位保留。
    market = [["BUY_SEED", "CARROT", 4], ["BUY_SEED", "CARROT", 2], ["SELL", "WHEAT", 3]]
    action = {"market": market, "farmer": ["PASS"]}
    _patch_host(monkeypatch, action)
    pv = _spy_plan_view({671: {"plants": {"CARROT": 5}, "buy_seed": {}}})
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
    # 2 号路 671 步 CARROT PLANT（671+48=719>718 → 不构成需求）且磁带无未来
    # CARROT 买单 → 供给=库存0+保留单6+磁带0=6 → allowed=6 → 两张 CARROT 买单全删。
    route2 = _tape({671: {"farmer": ["PLANT", "CARROT"]}})
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
