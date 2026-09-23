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
