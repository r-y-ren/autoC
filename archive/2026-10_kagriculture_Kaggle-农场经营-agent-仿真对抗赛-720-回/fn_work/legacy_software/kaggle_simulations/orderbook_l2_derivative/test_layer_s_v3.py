"""test_layer_s_v3：减量/安全边/观测速率矩阵 + invariant v3 组（九件）。

v3 块由 make 先生成到 tmp 再以独立模块名载入（_CXS_HOST=None 独立导入态，
沿 L1/v2 test 通道；双窗各一：w648 主跑 + w600 附加跑）。工具件沿
import test_layer_s 复用（_make_plan_view/_obs_with_seeds/_spy_plan_view/
_make_seq_plan_view/_FakeChassis/_tape——import 复用不复制，防漂移）。
v3 平衡面新增观测数据源：我方 farms 地块 planted_day（本文件 _obs_with_farms
构造真实链路形态——无 farms 的 L1 旧夹具形态对 v3 是"观测不可解析"→None→
品项原样，方向安全但非判定态）。
invariant v3 组九件（gate_equivalence_v3.constructed_cases_v3 后续 import 复用，
返回 {"expected","got","evidence"}；c3 双面同款）：R10 三件+c4/c5（减量语义
重校）+ 新四件（8→1 法证、安全边兜超种、[] 空槽、600 窗滴灌）。"""

import importlib.util
import sys
from pathlib import Path

import pytest

import make_layer_s_v3_block as maker

_THIS_DIR = Path(__file__).resolve().parent
_L1_DIR = _THIS_DIR.parent / "orderbook_l1_derivative"
_L1_BLOCK = _L1_DIR / "layer_s_block.py"
if str(_L1_DIR) not in sys.path:
    sys.path.insert(0, str(_L1_DIR))

import layer_s_block as l1_block  # noqa: E402  L1 对照面（只读，供行为对比）
import test_layer_s as l1_fixtures  # noqa: E402  R10 夹具库（import 复用）

# 夹具工具沿 test_layer_s import 复用（不复制防漂移）。
_make_plan_view = l1_fixtures._make_plan_view
_make_seq_plan_view = l1_fixtures._make_seq_plan_view
_spy_plan_view = l1_fixtures._spy_plan_view
_obs_with_seeds = l1_fixtures._obs_with_seeds
_FakeChassis = l1_fixtures._FakeChassis
_FakeImpl = l1_fixtures._FakeImpl
_tape = l1_fixtures._tape


def _tile(crop, planted_day):
    """在田地块假件（引擎 schema：PLANT 地块 dict，planted_day=种植当日）。"""
    return {"kind": "PLANT", "crop": crop, "planted_day": planted_day}


def _obs_with_farms(seeds, step, tiles=None, player=0):
    """v3 平衡面观测假件：L1 surplus 面（step+private.seeds）+ farms 观测面。"""
    return {
        "step": step,
        "player": player,
        "private": {"seeds": dict(seeds)},
        "farms": [{"tiles": tiles if tiles is not None else []}],
    }


def _load_v3(tmp_dir, window):
    out = Path(tmp_dir) / f"layer_s_block_v3_w{window}.py"
    maker.make(_L1_BLOCK, out, window=window)
    name = f"layer_s_block_v3_w{window}_under_test"
    spec = importlib.util.spec_from_file_location(name, out)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def v3_block(tmp_path_factory):
    """主跑窗 w648：make 到 tmp 再载入（变更集审计由 make 内建）。"""
    return _load_v3(tmp_path_factory.mktemp("v3_w648"), 648)


@pytest.fixture(scope="module")
def v3_block_w600(tmp_path_factory):
    """附加跑窗 w600（_CXS_FROM=600 构建期注入）。"""
    return _load_v3(tmp_path_factory.mktemp("v3_w600"), 600)


# ---- 减量/安全边/观测速率全矩阵（v3 逐面裁决 + L1 行为对比冒烟）----


def test_balance_and_reduce_matrix(v3_block, v3_block_w600, monkeypatch):
    balance = v3_block._cxs_seed_balance
    reduce_orders = v3_block._cxs_reduce_orders

    # ⓪ 独立导入态结构不变式：宿主 None；末 callable=_cxs_agent；窗口/安全边/路由边界常数。
    assert v3_block._CXS_HOST is None
    assert [v for v in list(vars(v3_block).values()) if callable(v)][-1] is v3_block._cxs_agent
    assert v3_block._CXS_FROM == 648 and v3_block_w600._CXS_FROM == 600
    assert (v3_block._CXS_SAFETY_LOOKBACK_STEPS, v3_block._CXS_SAFETY_MIN_MARGIN) == (24, 2)
    assert v3_block._CXS_ROUTE_BOUNDARY == v3_block_w600._CXS_ROUTE_BOUNDARY == 648  # 与窗口解耦

    # ① R 各分支（balance 直调；obs 含 farms 空地块 → observed 0）：
    # ①a 赤字为正：demand=6（660+48=708≤719）、held=1、tf=0 → R=5+边0。
    plans_a = {660: {"plants": {"CARROT": 6}, "buy_seed": {}}}
    obs_a = _obs_with_farms({"CARROT": 1}, 650)
    kept_a = [["BUY_SEED", "CARROT", 10], ["SELL", "WHEAT", 2]]
    assert balance("CARROT", obs_a, kept_a, _make_plan_view(plans_a), 0) == 5
    # ①b 赤字 0（供给覆盖）：held=6=demand → R=0+边0（确证全减，非 None）。
    assert balance("CARROT", _obs_with_farms({"CARROT": 6}, 650),
                   [["BUY_SEED", "CARROT", 3]], _make_plan_view(plans_a), 0) == 0
    # ①c 三路口径 tf 计入：demand=6、held=0、tf=4（668>650 未来买）→ R=2
    #    （等价式验证：赤字=max(0,6−(0+4))=2；"供给+本回合量"式 max(0,6−4−0+8)=2 同值）。
    plans_c = {660: {"plants": {"CARROT": 6}, "buy_seed": {}},
               668: {"plants": {}, "buy_seed": {"CARROT": 4}}}
    assert balance("CARROT", _obs_with_farms({"CARROT": 0}, 650),
                   [["BUY_SEED", "CARROT", 8]], _make_plan_view(plans_c), 0) == 2
    # ①d 安全边 clamp 上界：observed 5（5 块近窗 CARROT 地块）、planned 1、demand 1
    #    → raw 4 → 钳 max(2,1)=2 → R=1+2=3。
    tiles_d = [[_tile("CARROT", 27) for _ in range(5)]]
    plans_d = {660: {"plants": {"CARROT": 1}, "buy_seed": {}}}
    assert balance("CARROT", _obs_with_farms({"CARROT": 0}, 650, tiles_d),
                   [["BUY_SEED", "CARROT", 8]], _make_plan_view(plans_d), 0) == 3
    # ①e 安全边下限（demand=0 仍保有）：observed 1（近窗 1 块+旧块 1 块排除）、
    #    planned 0、demand 0 → raw 1 → 钳 [0, max(2,0)=2] → margin 1 → R=1。
    tiles_e = [[_tile("CARROT", 27), _tile("CARROT", 20)]]
    assert balance("CARROT", _obs_with_farms({"CARROT": 0}, 650, tiles_e),
                   [["BUY_SEED", "CARROT", 5]], _make_plan_view({}), 0) == 1
    # ①f 负速率差钳 0：observed 0 < planned 3 → margin 0（反应层少种不产生负边）。
    assert balance("CARROT", _obs_with_farms({"CARROT": 0}, 650),
                   [["BUY_SEED", "CARROT", 5]],
                   _make_plan_view({660: {"plants": {"CARROT": 3}, "buy_seed": {}}}), 0) == 3
    # ①g None 面（不确定=品项原样）：
    obs_g = _obs_with_farms({"CARROT": 2}, 650)
    kept_g = [["BUY_SEED", "CARROT", 3]]
    plans_g = {660: {"plants": {"CARROT": 4}, "buy_seed": {}}}
    #   demand None：plan_view 返回 None / 抛异常 / 形参不可调用。
    assert balance("CARROT", obs_g, kept_g, _make_plan_view(None), 0) is None
    assert balance("CARROT", obs_g, kept_g, _make_plan_view(RuntimeError("boom")), 0) is None
    assert balance("CARROT", obs_g, kept_g, None, 0) is None
    #   current_plants None / 非法（负数/bool/str/半值 float）。
    assert balance("CARROT", obs_g, kept_g, _make_plan_view(plans_g)) is None
    for bad_cp in (-1, True, "8", 2.5, 1.5):
        assert balance("CARROT", obs_g, kept_g, _make_plan_view(plans_g), bad_cp) is None, bad_cp
    #   observation 库存面畸形（沿 L1 surplus 面）+ 缺 step。
    for bad_obs in (None, {"step": 650}, {"step": 650, "private": {}},
                    {"step": 650, "private": {"seeds": "x"}},
                    {"step": 650, "private": {"seeds": {"CARROT": "5"}}},
                    {"step": 650, "private": {"seeds": {"CARROT": 2.5}}},
                    {"step": 650, "private": {"seeds": {"CARROT": True}}},
                    {"player": 0, "private": {"seeds": {"CARROT": 2}}, "farms": [{"tiles": []}]}):
        assert balance("CARROT", bad_obs, kept_g, _make_plan_view(plans_g), 0) is None, bad_obs
    #   磁带非确定性：demand 调用取 a、磁带交叉核对取 b → replay≠demand → None。
    a = {660: {"plants": {"CARROT": 4}, "buy_seed": {}}}
    b = {660: {"plants": {"CARROT": 5}, "buy_seed": {}}}
    assert balance("CARROT", obs_g, kept_g, _make_seq_plan_view([a, b]), 0) is None
    assert balance("CARROT", obs_g, kept_g, _make_seq_plan_view([a, None]), 0) is None
    #   观测面（farms/planted_day）畸形 → margin None → 整体 None。
    for bad_tiles_obs in (
            {"step": 650, "player": 0, "private": {"seeds": {"CARROT": 2}}},          # 缺 farms
            {"step": 650, "player": 0, "private": {"seeds": {"CARROT": 2}}, "farms": "x"},
            {"step": 650, "player": 0, "private": {"seeds": {"CARROT": 2}}, "farms": [{}]},  # 缺 tiles
            {"step": 650, "player": 0, "private": {"seeds": {"CARROT": 2}}, "farms": [{"tiles": 7}]},
            {"step": 650, "player": 0, "private": {"seeds": {"CARROT": 2}},
             "farms": [{"tiles": [[_tile("CARROT", 27)], 7]}]},                        # 行非 list
            {"step": 650, "player": 0, "private": {"seeds": {"CARROT": 2}},
             "farms": [{"tiles": [[7]]}]},                                            # 地块非 dict
            {"step": 650, "player": 0, "private": {"seeds": {"CARROT": 2}},
             "farms": [{"tiles": [[{"kind": "PLANT", "crop": "CARROT", "planted_day": "27"}]]}]},
    ):
        assert balance("CARROT", bad_tiles_obs, kept_g, _make_plan_view(plans_g), 0) is None, bad_tiles_obs
    # ①h kept_orders 解析：[]/None 空槽可忽略（不触发 None）；非空畸形仍 None。
    assert balance("CARROT", _obs_with_farms({"CARROT": 6}, 650),
                   [[], None, ["BUY_SEED", "CARROT", 3]], _make_plan_view(plans_a), 0) == 0
    assert balance("CARROT", obs_g, [None], _make_plan_view(plans_g), 0) == 2  # 纯空槽表可解析
    for bad_kept in (None, "not-orders", {"0": ["BUY_SEED", "CARROT", 3]},
                     [["SELL", "WHEAT"]], [["BUY_LAND"]], [7],
                     [["BUY_SEED", "CARROT", "3"]], [["BUY_SEED", "CARROT", None]],
                     [["BUY_SEED", "CARROT", True]], [["BUY_SEED", "CARROT", 2.5]]):
        assert balance("CARROT", obs_g, bad_kept, _make_plan_view(plans_g), 0) is None, bad_kept

    # ② 减量形态（reduce_orders；沿 L1 骨架=窗口快道/品项分组/从后往前）：
    # ②a 从后往前逐单减+整单消失+槽位序保持：R=3（demand=3）、总购 7、excess 4 →
    #     末单 B2→0 消失、中单 B3→减 2 余 1、首单 B2 不动、SELL 原对象原位。
    plans_2a = {660: {"plants": {"CARROT": 3}, "buy_seed": {}}}
    obs_2a = _obs_with_farms({"CARROT": 0}, 650)
    market_2a = [["BUY_SEED", "CARROT", 2], ["SELL", "WHEAT", 1],
                 ["BUY_SEED", "CARROT", 3], ["BUY_SEED", "CARROT", 2]]
    got_2a = reduce_orders(obs_2a, {"market": market_2a}, _make_plan_view(plans_2a))
    assert got_2a == [["BUY_SEED", "CARROT", 2], ["SELL", "WHEAT", 1], ["BUY_SEED", "CARROT", 1]]
    assert got_2a[1] is market_2a[1]  # 非 BUY_SEED 槽位=同对象原位
    # ②b 法证 662 形 8→1（held0/kept8/tf0/demand1 → R=1+边0）：整单 8 减量至 1
    #     （对照 L1：allowed=7<8 整单不可删 → L1 原样保留 8——R11 痛点、R12 解）。
    plans_2b = {670: {"plants": {"CARROT": 1}, "buy_seed": {}}}  # 670+48=718≤719
    obs_2b = _obs_with_farms({"CARROT": 0}, 662)
    market_2b = [["BUY_SEED", "CARROT", 8]]
    assert reduce_orders(obs_2b, {"market": market_2b}, _make_plan_view(plans_2b)) == \
        [["BUY_SEED", "CARROT", 1]]
    market_l1 = [["BUY_SEED", "CARROT", 8]]
    l1_got = l1_block._cxs_seed_truncate(obs_2b, {"market": market_l1}, _make_plan_view(plans_2b))
    assert l1_got is market_l1 and l1_got == [["BUY_SEED", "CARROT", 8]]
    # ②c R ≥ 本回合购买总量 → 同对象零足迹（只减不加）。
    market_2c = [["BUY_SEED", "CARROT", 3]]
    assert reduce_orders(obs_2a, {"market": market_2c}, _make_plan_view(plans_a)) is market_2c
    # ②d R None（plan_view None）→ 同对象。
    market_2d = [["BUY_SEED", "CARROT", 5]]
    assert reduce_orders(obs_2a, {"market": market_2d}, _make_plan_view(None)) is market_2d
    # ②e 零足迹快道（原对象 is + plan_view 零调用）：step<648 / 空表 / 仅空槽垫单 /
    #     market 键缺失（→None 原样）。
    m_fast = [["BUY_SEED", "CARROT", 5]]
    pv_fast = _spy_plan_view({660: {"plants": {}, "buy_seed": {}}})
    assert reduce_orders(_obs_with_farms({}, 600), {"market": m_fast}, pv_fast) is m_fast
    assert pv_fast.calls == 0
    m_empty = []
    pv2 = _spy_plan_view(None)
    assert reduce_orders(_obs_with_farms({}, 650), {"market": m_empty}, pv2) is m_empty
    assert pv2.calls == 0
    m_slots = [[], None]
    pv3 = _spy_plan_view(None)
    assert reduce_orders(_obs_with_farms({}, 650), {"market": m_slots}, pv3) is m_slots
    assert pv3.calls == 0  # [] /None 不构成品项（669 形归类）
    pv4 = _spy_plan_view(None)
    assert reduce_orders(_obs_with_farms({}, 700), {}, pv4) is None and pv4.calls == 0
    # ②f 混合多品项互不干扰：CARROT 需求 0 → 全减至消失；WHEAT R=5=购买量 → 保留。
    plans_2f = {660: {"plants": {"WHEAT": 5}, "buy_seed": {}}}
    obs_2f = _obs_with_farms({}, 650)
    market_2f = [["BUY_SEED", "CARROT", 5], ["BUY_SEED", "WHEAT", 5]]
    assert reduce_orders(obs_2f, {"market": market_2f}, _make_plan_view(plans_2f)) == \
        [["BUY_SEED", "WHEAT", 5]]
    # ②g tuple 订单减量输出为规范 list：[("BUY_SEED","CARROT",4)]、R=3 → 减 1 余 3。
    market_2g = [("BUY_SEED", "CARROT", 4)]
    assert reduce_orders(obs_2a, {"market": market_2g}, _make_plan_view(plans_2a)) == \
        [["BUY_SEED", "CARROT", 3]]
    # ②h 安全边兜反应层超种（法证 670 形：实种 2>磁带视 1）：demand=1（671 恰可完成）、
    #     held=0、tf=0、observed 2（近窗 2 块；旧块 20 排除）、planned 1 → margin 1 →
    #     R=2（无安全边则 1=饿死第 2 株）→ 8 减至 2。
    tiles_2h = [[_tile("CARROT", 27), _tile("CARROT", 27), _tile("CARROT", 20),
                 None, "LOCKED"]]
    plans_2h = {671: {"plants": {"CARROT": 1}, "buy_seed": {}}}  # 671+48=719≤719
    obs_2h = _obs_with_farms({"CARROT": 0}, 670, tiles_2h)
    assert balance("CARROT", obs_2h, [["BUY_SEED", "CARROT", 8]], _make_plan_view(plans_2h), 0) == 2
    assert reduce_orders(obs_2h, {"market": [["BUY_SEED", "CARROT", 8]]},
                         _make_plan_view(plans_2h)) == [["BUY_SEED", "CARROT", 2]]
    # ②i 当前步 PLANT 消耗扣减链路（reduce→balance 传参）：held=10、当前步 8×PLANT →
    #     有效库存 2、demand=6 → R=4；对照无 PLANT（farmer PASS）→ R=6−10→0+0... 即
    #     供给覆盖 R=0+0 → 全减；畸形 action（farmer 非 list）→ 传 None → 品项原样。
    plans_2i = {660: {"plants": {"CARROT": 6}, "buy_seed": {}}}
    obs_2i = _obs_with_farms({"CARROT": 10}, 650)
    m_i = [["BUY_SEED", "CARROT", 5]]
    action_i = {"market": m_i, "farmer": ["PLANT", "CARROT"], "hands": [["PLANT", "CARROT"]] * 7}
    assert reduce_orders(obs_2i, action_i, _make_plan_view(plans_2i)) == [["BUY_SEED", "CARROT", 4]]
    m_i2 = [["BUY_SEED", "CARROT", 5]]
    action_i2 = {"market": m_i2, "farmer": ["PASS"]}
    assert reduce_orders(obs_2i, action_i2, _make_plan_view(plans_2i)) == []
    m_i3 = [["BUY_SEED", "CARROT", 5]]
    action_i3 = {"market": m_i3, "farmer": 7}  # 畸形 → current_plants None → 原样
    assert reduce_orders(obs_2i, action_i3, _make_plan_view(plans_2i)) is m_i3

    # ③ 四继承函数冒烟 + 常数沿 L1 逐字节继承（diff 校验的运行时投影）：
    # ③a _cxs_harvest_completable 边界（671 恰可完成/672 起永不；每作物两端）。
    assert v3_block._cxs_harvest_completable(671, "CARROT") is True
    assert v3_block._cxs_harvest_completable(672, "CARROT") is False
    deadline = v3_block._CXS_PLANT_DEADLINE_SUM
    for crop, fh in v3_block.FIRST_HARVEST_STEPS.items():
        assert v3_block._cxs_harvest_completable(deadline - fh, crop) is True, (crop, fh)
        assert v3_block._cxs_harvest_completable(deadline - fh + 1, crop) is False, (crop, fh)
    assert v3_block._CXS_FROM == l1_block._CXS_FROM == 648
    assert v3_block._CXS_SEASON_END == l1_block._CXS_SEASON_END
    assert v3_block._CXS_PLANT_DEADLINE_SUM == l1_block._CXS_PLANT_DEADLINE_SUM == 719
    assert v3_block.FIRST_HARVEST_STEPS == l1_block.FIRST_HARVEST_STEPS
    # ③b _cxs_completable_plant_demand 行为不变：混合步号只计可完成；buy_seed 不入。
    mixed = {
        600: {"plants": {"CARROT": 1}, "buy_seed": {}},
        670: {"plants": {"CARROT": 3}, "buy_seed": {"CARROT": 2}},
        672: {"plants": {"CARROT": 2}, "buy_seed": {}},  # 672+48=720>719 不计
    }
    assert v3_block._cxs_completable_plant_demand("CARROT", {"step": 650},
                                                 _make_plan_view(mixed)) == 4
    assert v3_block._cxs_completable_plant_demand("CARROT", {"step": 650},
                                                 _make_plan_view(None)) is None
    # ③c _cxs_plan_view 行为不变：独立态无 _IMPL → None；假 _IMPL 折叠同 L1。
    assert v3_block._cxs_plan_view({"step": 650, "player": 0}) is None
    route1 = _tape({647: {"farmer": ["PLANT", "CARROT"],
                          "hands": [["PLANT", "WHEAT"], ["PASS"]],
                          "market": [["BUY_SEED", "CARROT", 3]]}})
    route2 = _tape({
        648: {"farmer": ["PASS"], "market": [["BUY_SEED", "MELON", 2], ["SELL", "WHEAT", 1]]},
        660: {"farmer": ["PLANT", "CARROT"], "hands": [["PLANT", "CARROT"]]},
        670: {"farmer": ["PLANT", "BAMBOO"],
              "market": [["BUY_SEED", "BAMBOO", 5], ["BUY_SEED", "WHEAT", -4]]},
    })
    impl = _FakeImpl(_FakeChassis({0: {"route": 1}}, {1: route1, 2: route2}))
    monkeypatch.setattr(v3_block, "_IMPL", impl, raising=False)
    assert v3_block._cxs_plan_view({"step": 646, "player": 0}) == {
        647: {"plants": {"CARROT": 1, "WHEAT": 1}, "buy_seed": {"CARROT": 3}},
        648: {"plants": {}, "buy_seed": {"MELON": 2}},
        660: {"plants": {"CARROT": 2}, "buy_seed": {}},
        670: {"plants": {}, "buy_seed": {"WHEAT": 0}},
    }
    monkeypatch.setattr(l1_block, "_IMPL", impl, raising=False)  # L1 同 impl 对照
    assert v3_block._cxs_plan_view({"step": 646, "player": 0}) == \
        l1_block._cxs_plan_view({"step": 646, "player": 0})  # 同 impl 两版同值
    # ③c-2 路由解耦（2026-09-24 修正钉）：路由边界=基座硬事实 648，与截断窗口无关——
    # 双窗产物在边界两侧的折叠与 L1 逐值同（w648 行为=修正前；w600 在 t∈[600,648)
    # 读本席路由 1，若误用窗口作边界会读到 route2 的 WHEAT 单→红线）。
    route_own = _tape({
        601: {"farmer": ["PLANT", "CARROT"], "market": [["BUY_SEED", "CARROT", 7]]},
        630: {"farmer": ["PLANT", "WHEAT"], "hands": [["PLANT", "WHEAT"]]},
        647: {"farmer": ["PLANT", "CARROT"]},
    })
    route_two = _tape({
        630: {"farmer": ["PLANT", "WHEAT"], "market": [["BUY_SEED", "WHEAT", 9]]},
        640: {"farmer": ["PLANT", "MELON"], "market": [["BUY_SEED", "MELON", 4]]},
        648: {"farmer": ["PASS"], "market": [["BUY_SEED", "MELON", 2]]},
        660: {"farmer": ["PLANT", "CARROT"], "hands": [["PLANT", "CARROT"]]},
    })
    impl2 = _FakeImpl(_FakeChassis({0: {"route": 1}}, {1: route_own, 2: route_two}))
    monkeypatch.setattr(v3_block, "_IMPL", impl2, raising=False)
    monkeypatch.setattr(v3_block_w600, "_IMPL", impl2, raising=False)
    monkeypatch.setattr(l1_block, "_IMPL", impl2, raising=False)
    for step_probe in (600, 620, 640, 646, 647, 648, 650):
        obs_probe = {"step": step_probe, "player": 0}
        expected_fold = l1_block._cxs_plan_view(obs_probe)  # L1=基座路由换算真值
        assert v3_block._cxs_plan_view(obs_probe) == expected_fold, step_probe  # w648 行为钉
        assert v3_block_w600._cxs_plan_view(obs_probe) == expected_fold, step_probe  # w600 路由保真
    # 直接反证：step 620 的折叠含本席 630 WHEAT×2（route_own），不含 route2 的
    # 630 WHEAT 单+9 买单（若 w600 误以 600 为路由界，则 630/640 走 2 号路）。
    fold_620 = v3_block_w600._cxs_plan_view({"step": 620, "player": 0})
    assert fold_620[630] == {"plants": {"WHEAT": 2}, "buy_seed": {}}
    assert 640 not in fold_620  # route2 的 640 MELON 不得入窗（t<648 仍读本席路由）

    # ④ _cxs_agent 全链（假宿主+真减量层+假 plan_view）：
    class _Host:
        def __init__(self, action):
            self.action = action
            self.calls = []

        def __call__(self, observation, configuration=None):
            self.calls.append((observation, configuration))
            return self.action

    # ④a 全链减量：磁带唯一 plants@672 不可完成 → demand 0 → R=0 → 两张 CARROT 单
    #     消失、SELL 原位；宿主调用在 try 外原样收参。
    market_4 = [["BUY_SEED", "CARROT", 4], ["BUY_SEED", "CARROT", 2], ["SELL", "WHEAT", 3]]
    action_4 = {"market": market_4, "farmer": ["PASS"]}
    host = _Host(action_4)
    monkeypatch.setattr(v3_block, "_CXS_HOST", host)
    monkeypatch.setattr(v3_block, "_cxs_plan_view",
                        _spy_plan_view({672: {"plants": {"CARROT": 5}, "buy_seed": {}}}))
    obs_4 = _obs_with_farms({"CARROT": 0}, 650)
    cfg_4 = {"sentinel": True}
    got_4 = v3_block._cxs_agent(obs_4, cfg_4)
    assert got_4 == {"market": [["SELL", "WHEAT", 3]], "farmer": ["PASS"]}
    assert got_4 is not action_4 and got_4["farmer"] is action_4["farmer"]
    assert host.calls == [(obs_4, cfg_4)]
    # ④b 减量层抛异常 → 原样返回宿主 action（fail-safe 同对象）。
    action_4b = {"market": [["BUY_SEED", "CARROT", 5]]}
    monkeypatch.setattr(v3_block, "_CXS_HOST", _Host(action_4b))

    def _boom(observation, action, plan_view):
        raise RuntimeError("reduce boom")

    monkeypatch.setattr(v3_block, "_cxs_reduce_orders", _boom)
    monkeypatch.setattr(v3_block, "_cxs_plan_view", _spy_plan_view(None))
    assert v3_block._cxs_agent(_obs_with_farms({}, 650)) is action_4b
    # ④c 宿主异常向上传播（宿主调用在 try 外）。
    monkeypatch.setattr(v3_block, "_CXS_HOST",
                        lambda observation, configuration=None: (_ for _ in ()).throw(
                            RuntimeError("host boom")))
    with pytest.raises(RuntimeError):
        v3_block._cxs_agent({"step": 650})
    # ④d plan_view None → 品项原样（零删除原对象，慢道新 action dict 载原 market）。
    action_4d = {"market": [["BUY_SEED", "CARROT", 5], ["SELL", "WHEAT", 1]],
                 "farmer": ["PASS"]}
    monkeypatch.setattr(v3_block, "_CXS_HOST", _Host(action_4d))
    monkeypatch.setattr(v3_block, "_cxs_plan_view", _make_plan_view(None))
    got_4d = v3_block._cxs_agent(_obs_with_farms({}, 650))
    assert got_4d == action_4d and got_4d["market"] is action_4d["market"]
    # ④e step==0 复位钩子占位（无台账可复位——不抛即可）+ step<窗口界零足迹。
    action_4e = {"market": [["BUY_SEED", "CARROT", 5]]}
    monkeypatch.setattr(v3_block, "_CXS_HOST", _Host(action_4e))
    pv_4e = _spy_plan_view(None)
    monkeypatch.setattr(v3_block, "_cxs_plan_view", pv_4e)
    assert v3_block._cxs_agent({"step": 0}) is action_4e  # 复位钩子无害
    assert v3_block._cxs_agent(_obs_with_farms({}, 600)) is action_4e
    assert pv_4e.calls == 0

    # ⑤ 对照 L1：同输入下 v3 与 L1 输出差异恰为减量语义（保有总量=min(总购, R)，
    #     L1 整单删=保有总量 ≥ demand 的整单组合）。
    # ⑤a 一致面：demand 0、供给 0 → v3 全减至消失 == L1 全删。
    obs_5 = _obs_with_farms({"CARROT": 0}, 650)
    m_5 = [["BUY_SEED", "CARROT", 4], ["BUY_SEED", "CARROT", 2]]
    assert reduce_orders(obs_5, {"market": [["BUY_SEED", "CARROT", 4], ["BUY_SEED", "CARROT", 2]]},
                         _make_plan_view({})) == []
    assert l1_block._cxs_seed_truncate(obs_5, {"market": m_5}, _make_plan_view({})) == []
    # ⑤b 分歧面（整单不可回收 → 减量恰留真需求）：demand=3、总购 7 →
    #     v3 R=3 → [2,1]；L1 allowed=4 → 整单删末 2 与首 2 → [3]。两版保有均=3，
    #     形态差=减量（v3 前载保留）vs 整单（L1 中单保留）。
    plans_5b = {660: {"plants": {"CARROT": 3}, "buy_seed": {}}}
    m_5b = [["BUY_SEED", "CARROT", 2], ["BUY_SEED", "CARROT", 3], ["BUY_SEED", "CARROT", 2]]
    got_5b = reduce_orders(obs_5, {"market": [["BUY_SEED", "CARROT", 2], ["BUY_SEED", "CARROT", 3],
                                              ["BUY_SEED", "CARROT", 2]]},
                           _make_plan_view(plans_5b))
    assert got_5b == [["BUY_SEED", "CARROT", 2], ["BUY_SEED", "CARROT", 1]]
    l1_5b = l1_block._cxs_seed_truncate(obs_5, {"market": m_5b}, _make_plan_view(plans_5b))
    assert l1_5b == [["BUY_SEED", "CARROT", 3]]
    assert sum(o[2] for o in got_5b) == sum(o[2] for o in l1_5b) == 3
    # ⑤c 一致面（供给恰=需求）：demand 5=总购 5 → v3 R=5 保留 == L1 allowed=0 保留。
    plans_5c = {670: {"plants": {"CARROT": 5}, "buy_seed": {}}}
    m_5c = [["SELL", "WHEAT", 2], ["BUY_SEED", "CARROT", 5]]
    assert reduce_orders(obs_5, {"market": [["SELL", "WHEAT", 2], ["BUY_SEED", "CARROT", 5]]},
                         _make_plan_view(plans_5c)) == m_5c
    assert l1_block._cxs_seed_truncate(obs_5, {"market": m_5c}, _make_plan_view(plans_5c)) == m_5c

    # ⑥ 窗口隔离（双窗产物运行时界）：step 620 ∈ [600,648) → w600 减量生效、
    #     w648 快道原样（L1 亦 648 界原样）。
    plans_6 = {640: {"plants": {"CARROT": 2}, "buy_seed": {}}}  # 640+48=688≤719
    obs_6 = _obs_with_farms({"CARROT": 0}, 620)
    m_6 = [["BUY_SEED", "CARROT", 5]]
    assert v3_block_w600._cxs_reduce_orders(
        obs_6, {"market": [["BUY_SEED", "CARROT", 5]]}, _make_plan_view(plans_6)) == \
        [["BUY_SEED", "CARROT", 2]]
    assert reduce_orders(obs_6, {"market": m_6}, _make_plan_view(plans_6)) is m_6  # 局部绑定=未补丁原函数


# ---- invariant v3 组（九件：R10 三件+c4/c5 减量语义重校 + 新四件）----
# 夹具函数模块级留档，gate_equivalence_v3.constructed_cases_v3 后续 import 复用
# （返回 {"expected","got","evidence"}；c3 双面 {"truncate_side","keep_side"}）。


def _invariant_case_c1_no_trunc_when_future_plant(mod):
    """用例①（不截·重校）：未来步有可完成 plants 的 BUY_SEED 不减。

    决策步 650，磁带 670 plants 5（670+48=718≤719）→ demand 5；held 0、tf 0 →
    R=5+边0（observed 0−planned 5→钳 0）= 购买总量 5 → excess 0 → 全保留原样。
    """
    plans = {670: {"plants": {"CARROT": 5}, "buy_seed": {}}}
    obs = _obs_with_farms({"CARROT": 0}, 650)
    market = [["SELL", "WHEAT", 2], ["BUY_SEED", "CARROT", 5]]
    got = mod._cxs_reduce_orders(obs, {"market": market}, _make_plan_view(plans))
    return {
        "expected": [["SELL", "WHEAT", 2], ["BUY_SEED", "CARROT", 5]],
        "got": got,
        "evidence": "step=650 tape plants@670 completable: demand 5, R=5 (deficit 5, "
                    "margin 0) == purchase 5 -> excess 0, all kept",
    }


def _invariant_case_c2_trunc_when_no_opportunity(mod):
    """用例②（全减·重校）：磁带唯一 plants 不可完成 → R=0 ≡ 整单删形态。

    决策步 650，磁带 672 plants 5（672+48=720>719 不构成需求）→ demand 0；
    held 0、tf 0 → R=0+边0（observed 0−planned 5 钳 0）→ 两张 CARROT 单减至 0
    消失（≡R10 整单删形态）、SELL 原位。
    """
    plans = {672: {"plants": {"CARROT": 5}, "buy_seed": {}}}
    obs = _obs_with_farms({"CARROT": 0}, 650)
    market = [["BUY_SEED", "CARROT", 4], ["BUY_SEED", "CARROT", 2], ["SELL", "WHEAT", 3]]
    got = mod._cxs_reduce_orders(obs, {"market": market}, _make_plan_view(plans))
    return {
        "expected": [["SELL", "WHEAT", 3]],
        "got": got,
        "evidence": "step=650 tape plants@672 not completable: demand 0, R=0 -> excess 6, "
                    "both CARROT orders reduced to zero (vanish), SELL kept",
    }


def _invariant_case_c3_s671_boundary(mod):
    """用例③（s671 边界双面·重校）：671+48=719≤719 恰可完成、672 起永不。

    截面：决策步 671（磁带真实形态仅含 t≥672）确无后续可完成种植机会 → demand 0、
    held 2 → R=0+边0 → 单减至 0 消失。不截面：决策步 670，磁带 671 plants 3
    （恰可完成）→ demand 3、held 0、tf 0 → R=3+边0（observed 0−planned 12 钳 0；
    planned 含 672 不可完成株 9）= 购买总量 3 → 全保留。
    """
    plans_trunc = {672: {"plants": {"CARROT": 5}, "buy_seed": {}}}
    obs_trunc = _obs_with_farms({"CARROT": 2}, 671)
    got_trunc = mod._cxs_reduce_orders(
        obs_trunc, {"market": [["BUY_SEED", "CARROT", 3]]}, _make_plan_view(plans_trunc))
    plans_keep = {671: {"plants": {"CARROT": 3}, "buy_seed": {}},
                  672: {"plants": {"CARROT": 9}, "buy_seed": {}}}
    obs_keep = _obs_with_farms({"CARROT": 0}, 670)
    got_keep = mod._cxs_reduce_orders(
        obs_keep, {"market": [["BUY_SEED", "CARROT", 3]]}, _make_plan_view(plans_keep))
    return {
        "truncate_side": {
            "expected": [],
            "got": got_trunc,
            "evidence": "step=671 tape only t>=672: demand 0, held 2 -> R=0, order "
                        "reduced to zero (vanish)",
        },
        "keep_side": {
            "expected": [["BUY_SEED", "CARROT", 3]],
            "got": got_keep,
            "evidence": "step=670 tape plants@671 exactly completable: demand 3, R=3 "
                        "== purchase 3 -> kept",
        },
    }


def _invariant_case_c4_covered_buyback_reduced_to_zero(mod):
    """用例④（减·重校）：供给已覆盖需求（赤字 0）→ 回买单减至 0 消失。

    决策步 650，磁带 660 plants 4（可完成 → demand 4）；库存恰 4 → 赤字
    max(0, 4−4)=0；observed 0−planned 4 → 边 0 → R=0 → 回买单 qty3 全减消失、
    SELL 原位。
    """
    plans = {660: {"plants": {"CARROT": 4}, "buy_seed": {}}}
    obs = _obs_with_farms({"CARROT": 4}, 650)
    market = [["SELL", "WHEAT", 1], ["BUY_SEED", "CARROT", 3]]
    got = mod._cxs_reduce_orders(obs, {"market": market}, _make_plan_view(plans))
    return {
        "expected": [["SELL", "WHEAT", 1]],
        "got": got,
        "evidence": "step=650 held 4 covers demand 4: deficit 0, margin 0 -> R=0, "
                    "buy-back reduced to zero, SELL kept",
    }


def _invariant_case_c5_short_true_future_plant_kept(mod):
    """用例⑤（保·重校）：三路口径供给<需求（真未来种植）→ 保留。

    决策步 650，磁带 660 plants 6（可完成 → demand 6）；held 2、tf 0 → 赤字
    6−2=4 → R=4+边0 ≥ 购买总量 3 → 全保留（对照 L1 allowed=0 同保）。
    """
    plans = {660: {"plants": {"CARROT": 6}, "buy_seed": {}}}
    obs = _obs_with_farms({"CARROT": 2}, 650)
    market = [["BUY_SEED", "CARROT", 3]]
    got = mod._cxs_reduce_orders(obs, {"market": market}, _make_plan_view(plans))
    return {
        "expected": [["BUY_SEED", "CARROT", 3]],
        "got": got,
        "evidence": "step=650 three-path supply (held 2) < demand 6: R=4 >= purchase 3 "
                    "-> order kept",
    }


def _invariant_case_c6_8to1_forensic(mod):
    """用例⑥（新·8→1 减量恰留真需求）：法证 662 形五数代入。

    R11 法证五数表：662 形 held_eff=0/kept[8]/tape_future=0/demand=1 →
    allowed=7<8 整单不可删（1/8 真需求绑定）。v3：R=max(0, 1−(0+0))+边0=1
    （observed 0、planned 1 → 速率差 −1 钳 0）→ 单 8 减量至 1——恰留真需求。
    """
    plans = {670: {"plants": {"CARROT": 1}, "buy_seed": {}}}
    obs = _obs_with_farms({"CARROT": 0}, 662)
    market = [["BUY_SEED", "CARROT", 8]]
    got = mod._cxs_reduce_orders(obs, {"market": market}, _make_plan_view(plans))
    return {
        "expected": [["BUY_SEED", "CARROT", 1]],
        "got": got,
        "evidence": "step=662 forensic (held 0/kept 8/tf 0/demand 1): R=1 -> 8 reduced "
                    "to 1 (L1 whole-order rule kept all 8)",
    }


def _invariant_case_c7_margin_backstop_reactive_overshoot(mod):
    """用例⑦（新·安全边兜反应层超种）：670 形实种 2>磁带视 1。

    决策步 670（day 27）：我方 farms 近窗（planted_day≥26）CARROT 在田 2 块
    （旧块 planted_day 20 不计）、磁带 671 plants 1（恰可完成 → demand 1）→
    held 0、tf 0、赤字 1；速率差=observed 2−planned 1=1 → 边 1（≤ max(2,1)）→
    R=2——无安全边则 R=1 必饿死第 2 株（反应层种植磁带不可见）。
    """
    tiles = [[_tile("CARROT", 27), _tile("CARROT", 27), _tile("CARROT", 20)]]
    plans = {671: {"plants": {"CARROT": 1}, "buy_seed": {}}}
    obs = _obs_with_farms({"CARROT": 0}, 670, tiles)
    market = [["BUY_SEED", "CARROT", 8]]
    got = mod._cxs_reduce_orders(obs, {"market": market}, _make_plan_view(plans))
    return {
        "expected": [["BUY_SEED", "CARROT", 2]],
        "got": got,
        "evidence": "step=670 reactive overshoot (observed 2 > planned 1): R=1+margin 1 "
                    "=2 -> 8 reduced to 2, no starvation",
    }


def _invariant_case_c8_empty_slot_ignored(mod):
    """用例⑧（新·空槽垫单可忽略）：669 形 [] 解析洞修正。

    market 含 []/None 空槽垫单：不构成品项、不计入 kept、不触发 None（法证
    669 形在 L1 严格解析下整层 None 零回收）；本例 demand 0、held 0 → R=0 →
    真实 BUY 单减至 0 消失，空槽原位保留。
    """
    obs = _obs_with_farms({"CARROT": 0}, 650)
    market = [[], None, ["BUY_SEED", "CARROT", 5]]
    got = mod._cxs_reduce_orders(obs, {"market": market}, _make_plan_view({}))
    return {
        "expected": [[], None],
        "got": got,
        "evidence": "step=650 empty-slot pads [] / None ignored (not malformed): real "
                    "order R=0 reduced to zero, pads kept in place",
    }


def _invariant_case_c9_window600_drip(mod_w600):
    """用例⑨（新·600 窗滴灌局回收）：窗口参数化运行时面。

    决策步 620（∈[600,648)）：w600 产物 _CXS_FROM=600 → 减量层生效；磁带 640
    plants 2（640+48=688≤719 → demand 2）→ R=2+边0 → 单 5 减至 2。同输入下
    w648 产物与 L1（648 界）均快道原样（5 不减）。
    """
    plans = {640: {"plants": {"CARROT": 2}, "buy_seed": {}}}
    obs = _obs_with_farms({"CARROT": 0}, 620)
    market = [["BUY_SEED", "CARROT", 5]]
    got = mod_w600._cxs_reduce_orders(obs, {"market": market}, _make_plan_view(plans))
    return {
        "expected": [["BUY_SEED", "CARROT", 2]],
        "got": got,
        "evidence": "step=620 in [600,648): w600 window active (R=2 -> 5 reduced to 2); "
                    "w648/L1 fast-path keep 5",
    }


def test_invariant_cases_v3(v3_block, v3_block_w600):
    # R10 三件（c1-c3）+c4/c5：减量语义重校后真值断言 + 同输入 L1 对照
    # （三例口径下 L1 与 v3 输出一致——整单删≡减至 0，或全保≡R≥总购）。
    c1 = _invariant_case_c1_no_trunc_when_future_plant(v3_block)
    assert c1["got"] == c1["expected"]
    l1_c1 = l1_block._cxs_seed_truncate(
        _obs_with_farms({"CARROT": 0}, 650),
        {"market": [["SELL", "WHEAT", 2], ["BUY_SEED", "CARROT", 5]]},
        _make_plan_view({670: {"plants": {"CARROT": 5}, "buy_seed": {}}}))
    assert l1_c1 == c1["expected"]

    c2 = _invariant_case_c2_trunc_when_no_opportunity(v3_block)
    assert c2["got"] == c2["expected"]
    l1_c2 = l1_block._cxs_seed_truncate(
        _obs_with_farms({"CARROT": 0}, 650),
        {"market": [["BUY_SEED", "CARROT", 4], ["BUY_SEED", "CARROT", 2], ["SELL", "WHEAT", 3]]},
        _make_plan_view({672: {"plants": {"CARROT": 5}, "buy_seed": {}}}))
    assert l1_c2 == c2["expected"]  # 整单删 ≡ 减至 0：两版一致面

    c3 = _invariant_case_c3_s671_boundary(v3_block)
    assert c3["truncate_side"]["got"] == c3["truncate_side"]["expected"]
    assert c3["keep_side"]["got"] == c3["keep_side"]["expected"]

    c4 = _invariant_case_c4_covered_buyback_reduced_to_zero(v3_block)
    assert c4["got"] == c4["expected"]

    c5 = _invariant_case_c5_short_true_future_plant_kept(v3_block)
    assert c5["got"] == c5["expected"]

    # 新四件：8→1 法证 / 安全边兜超种 / 空槽忽略 / 600 窗滴灌。
    c6 = _invariant_case_c6_8to1_forensic(v3_block)
    assert c6["got"] == c6["expected"]
    # c6 对照面：同输入 L1 整单纪律零回收（allowed=7<8）——减量语义的判决性差异。
    l1_c6 = l1_block._cxs_seed_truncate(
        _obs_with_farms({"CARROT": 0}, 662),
        {"market": [["BUY_SEED", "CARROT", 8]]},
        _make_plan_view({670: {"plants": {"CARROT": 1}, "buy_seed": {}}}))
    assert l1_c6 == [["BUY_SEED", "CARROT", 8]]

    c7 = _invariant_case_c7_margin_backstop_reactive_overshoot(v3_block)
    assert c7["got"] == c7["expected"]

    c8 = _invariant_case_c8_empty_slot_ignored(v3_block)
    assert c8["got"] == c8["expected"]
    # c8 对照面：同输入 L1 的 [] 严格解析触发 None → 整层零回收（669 形洞）。
    l1_c8 = l1_block._cxs_seed_truncate(
        _obs_with_farms({"CARROT": 0}, 650),
        {"market": [[], None, ["BUY_SEED", "CARROT", 5]]}, _make_plan_view({}))
    assert l1_c8 == [[], None, ["BUY_SEED", "CARROT", 5]]

    c9 = _invariant_case_c9_window600_drip(v3_block_w600)
    assert c9["got"] == c9["expected"]
    # c9 对照面：同输入 w648 与 L1 均 648 界快道原样（窗口参数化的运行时投影）。
    obs_c9 = _obs_with_farms({"CARROT": 0}, 620)
    m_c9 = [["BUY_SEED", "CARROT", 5]]
    plans_c9 = {640: {"plants": {"CARROT": 2}, "buy_seed": {}}}
    assert v3_block._cxs_reduce_orders(obs_c9, {"market": [["BUY_SEED", "CARROT", 5]]},
                                       _make_plan_view(plans_c9)) == [["BUY_SEED", "CARROT", 5]]
    assert l1_block._cxs_seed_truncate(obs_c9, {"market": m_c9},
                                       _make_plan_view(plans_c9)) == m_c9
