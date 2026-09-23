"""test_layer_s（继承 R10 验收③(c)）：运行时五函数 + invariant/surplus/demand/harvest 用例组。"""

import layer_s_block


def test_invariant_cases():
    raise NotImplementedError("unimplemented:fn:test_invariant_cases")


def test_surplus_uncertain_returns_none():
    raise NotImplementedError("unimplemented:fn:test_surplus_uncertain_returns_none")


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
