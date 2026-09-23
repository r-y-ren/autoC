"""test_layer_s（继承 R10 验收③(c)）：运行时五函数 + invariant/surplus/demand/harvest 用例组。"""

import layer_s_block


def test_invariant_cases():
    raise NotImplementedError("unimplemented:fn:test_invariant_cases")


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
