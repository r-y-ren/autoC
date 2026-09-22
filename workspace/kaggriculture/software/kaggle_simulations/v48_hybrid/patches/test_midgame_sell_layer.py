# -*- coding: utf-8 -*-
"""patches/test_midgame_sell_layer.py —— P1 中期卖出层 v2 单元测试。

v2（只补发收窄版，F3 根因修复）覆盖：
  一、day<13 透传（d0/d6 毛 flush/d10 瓜 flush/d12 一律剧本原样）；
  二、tape 承重线不补发（含当日稍后步有 tape 卖单的产线）；
  三、N 天前瞻判定（tape_sells_within 边界 + 内嵌日历与基底
     _V48_ROUTES 六变体并集的现场重推导一致性）；
  四、只补发语义（tape 全透传、量=min(库存,吸收,保守上限 6)、清判据门、
     整点批次、行数上限、v1 破产/流动性遗产移除、囤态零动作）；
  五、反克隆/终局/d26+ 让位保留；
  六、fail-safe 与集成缝（非 SELL 单保留、确定性、入参不可变）。
运行：python -m pytest <本文件> -q
"""

import base64
import json
import os
import re
import sys
import zlib

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import midgame_sell_layer as msl  # noqa: E402


# ---- 测试观测工厂 --------------------------------------------------------
def make_obs(step, shed, prices, money=5000.0, shops=None, flow=None,
             farms=None):
    obs = {"step": step, "prices": prices, "shed": shed, "money": money}
    if shops is not None:
        obs["unlocked_shops"] = shops
    if flow is not None:
        obs["flow"] = flow
    if farms is not None:
        obs["farms"] = farms
    return obs


def base_farms(plants=1):
    tile = {"kind": "PLANT"}
    return [{"hands": [], "quadrants_owned": 1, "tiles": [[tile] * plants]},
            {"hands": [], "quadrants_owned": 1, "tiles": [[tile] * plants]}]


# d13+ 激活帧但需避开反克隆让位时，用 distant farms 或不带 farms。
FARMS_DISTANT = None          # 无 farms → clone_distance=inf，不触发让位


# ===========================================================================
# 一、day<13 透传（v2 接管窗收窄）
# ===========================================================================
def test_day_before_13_passes_tape_verbatim():
    """d0/d6（羊毛 flush）/d10（瓜 flush）/d12 一律透传：清判据+空窗+有库
    存也不接管（v1 的 step24 起接管是 F3 根因，v2 废除）。"""
    for step in (5, 24 * 6 + 3, 24 * 10 + 6, 24 * 12 + 23):
        obs = make_obs(step=step, shed={"WHEAT": 50},      # d13 空窗线
                       prices={"WHEAT": 15}, shops=["FARMERS_MARKET"],
                       flow={"WHEAT": 3.0})
        tape = [["SELL", "WOOL", 9], ["SELL", "FERTILIZER", 4]]
        assert msl.plan_midgame_sells(obs, tape) == tape, step


def test_day13_first_frame_supplement_fires():
    """d13（接管窗首日）hour6：WHEAT 空窗+清+库存 50 → 补发首批 2
    （量=min(50, 吸收 7, cap 6)=6 → 批次 [2,2,2]）。"""
    obs = make_obs(step=24 * 13 + 6, shed={"WHEAT": 50},
                   prices={"WHEAT": 15}, shops=["FARMERS_MARKET"],
                   flow={"WHEAT": 3.0})
    out = msl.plan_midgame_sells(obs, [])
    assert out == [["SELL", "WHEAT", 2]]


def test_defer_probe_boundary_day12_vs_day13():
    """should_defer_to_tape 边界：d12 尾步 True；d13（无农场视图）False。"""
    assert msl.should_defer_to_tape(
        {"step": 24 * 12 + 23, "prices": {}, "shed": {}}) is True
    assert msl.should_defer_to_tape(
        {"step": 24 * 13 + 6, "prices": {}, "shed": {}}) is False


# ===========================================================================
# 二、tape 承重线不补发（供给曲线连坐）
# ===========================================================================
def test_load_bearing_line_within_horizon_no_supplement():
    """d14 WHEAT（d17 有 tape 卖单，间隔 3≤N）→ 承重线：清+库存也不补。"""
    obs = make_obs(step=24 * 14 + 6, shed={"WHEAT": 50},
                   prices={"WHEAT": 15}, shops=["FARMERS_MARKET"],
                   flow={"WHEAT": 3.0})
    assert msl.plan_midgame_sells(obs, []) == []


def test_same_day_tape_sell_counts_as_load_bearing():
    """d13 MILK（tape 当日即有卖单）→ 承重线不补。"""
    obs = make_obs(step=24 * 13 + 6, shed={"MILK": 40},
                   prices={"MILK": 100}, shops=["YARN_STORE"],
                   flow={"MILK": 3.0})
    assert msl.plan_midgame_sells(obs, []) == []


def test_tape_sell_this_step_skips_item_and_passes_through():
    """tape 本步已卖该线：不重复补发，剧本单原样透传（v48 原生节奏优先）。"""
    obs = make_obs(step=24 * 13 + 6, shed={"WHEAT": 50},
                   prices={"WHEAT": 15}, shops=["FARMERS_MARKET"],
                   flow={"WHEAT": 3.0})
    out = msl.plan_midgame_sells(obs, [["SELL", "WHEAT", 8]])
    assert out == [["SELL", "WHEAT", 8]]


def test_non_planner_item_tape_passthrough():
    """非接管面（FERTILIZER）剧本卖单在激活帧也一律透传。"""
    obs = make_obs(step=24 * 13 + 6, shed={}, prices={"FERTILIZER": 80},
                   shops=[], flow={"FERTILIZER": 3.0})
    assert msl.plan_midgame_sells(obs, [["SELL", "FERTILIZER", 4]]) == \
        [["SELL", "FERTILIZER", 4]]


# ===========================================================================
# 三、N 天前瞻判定
# ===========================================================================
def test_tape_sells_within_boundaries():
    """N=3 前瞻窗边界：WHEAT（tape 卖日 17）d13 自由 / d14-d17 承重；
    MELON（卖日 21）d17 自由（21-17=4>3）/ d18 承重；CARROT（卖日 29）
    d25 自由 / d26 承重；含当日（d17 对 WHEAT 为 True）。"""
    assert msl.tape_sells_within("WHEAT", 13, 3) is False
    for day in (14, 15, 16, 17):
        assert msl.tape_sells_within("WHEAT", day, 3) is True, day
    assert msl.tape_sells_within("MELON", 17, 3) is False
    assert msl.tape_sells_within("MELON", 18, 3) is True
    assert msl.tape_sells_within("CARROT", 25, 3) is False
    assert msl.tape_sells_within("CARROT", 26, 3) is True


def test_egg_never_load_bearing_and_horizon_override():
    """EGG 全程无 tape 卖单 → 任意日自由；horizon 显式参数覆盖默认。"""
    for day in (13, 20, 25):
        assert msl.tape_sells_within("EGG", day, 3) is False
    assert msl.tape_sells_within("WHEAT", 13, 4) is True     # 17∈[13,17]
    assert msl.DEFAULT_CONFIG["tape_lookahead_days"] == 3


def test_tape_sell_days_matches_base_routes():
    """内嵌日历 == 基底 _V48_ROUTES 六变体 SELL 单 day 并集（现场重推导）。

    推导口径与模块头一致：解 b85|zlib blob → 逐变体扫 market SELL →
    按 item 求 day 并集（day=step//24）。
    """
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "..", "..", "v48_derivative", "main.py")
    src = open(base_path, "r", encoding="utf-8").read()
    idx = src.index("_V48_ROUTES = json.loads")
    end = src.index(')).decode("utf-8"))', idx)
    blob = "".join(re.findall(r"'([^']*)'", src[idx:end]))
    routes = json.loads(
        zlib.decompress(base64.b85decode(blob)).decode("utf-8"))
    assert len(routes) == 6
    derived = {}
    for name, steps in routes.items():
        for i, act in enumerate(steps or []):
            for o in (act or {}).get("market", []) or []:
                if isinstance(o, (list, tuple)) and o and o[0] == "SELL":
                    derived.setdefault(o[1], set()).add(i // 24)
    derived_days = {k: tuple(sorted(v)) for k, v in derived.items()}
    assert set(derived_days) <= set(msl.TAPE_SELL_DAYS)
    for item, days in msl.TAPE_SELL_DAYS.items():
        assert derived_days.get(item, ()) == tuple(days), item


def test_carrot_gap_window_supplements():
    """CARROT d20-25 空窗（tape d19 卖完、d29 才再卖）：清+库存 → 补发。"""
    obs = make_obs(step=24 * 20 + 6, shed={"CARROT": 30},
                   prices={"CARROT": 20}, shops=["PET_CAFE"],
                   flow={"CARROT": 3.0})
    # PET_CAFE 单产品店：吸收=6×2+1=13 → 量=min(30,13,6)=6 → 批 [2,2,2]
    assert msl.plan_midgame_sells(obs, []) == [["SELL", "CARROT", 2]]


# ===========================================================================
# 四、只补发语义
# ===========================================================================
def test_supplement_qty_is_min_of_stock_absorption_cap():
    """量=min(库存, 吸收表日帽, 保守上限 6)：FARMERS_MARKET 下 WHEAT 吸收
    7 → 量 6 → 批 [2,2,2]；库存 2 → 量 2 → 批 [1,1]；零商铺 → 吸收 1。"""
    common = dict(prices={"WHEAT": 15}, shops=["FARMERS_MARKET"],
                  flow={"WHEAT": 3.0})
    obs = make_obs(step=24 * 13 + 6, shed={"WHEAT": 50}, **common)
    assert msl.plan_midgame_sells(obs, []) == [["SELL", "WHEAT", 2]]
    obs = make_obs(step=24 * 13 + 6, shed={"WHEAT": 2}, **common)
    assert msl.plan_midgame_sells(obs, []) == [["SELL", "WHEAT", 1]]
    obs = make_obs(step=24 * 13 + 6, shed={"WHEAT": 30}, prices={"WHEAT": 15},
                   shops=[], flow={"WHEAT": 3.0})
    assert msl.plan_midgame_sells(obs, []) == [["SELL", "WHEAT", 1]]


def test_hold_verdict_tape_passthrough_no_suppression():
    """囤态（投影≥现价×1.05，MELON 180/flow-3 → 投影 189.6）：零补发，
    且剧本卖单原样透传（v1 的囤态压制分支已删除——F3 根因）。"""
    obs = make_obs(step=24 * 13 + 6, shed={"MELON": 50},
                   prices={"MELON": 180}, shops=["FARMERS_MARKET"],
                   flow={"MELON": -3.0})
    assert msl._verdict("MELON", {"prices": {"MELON": 180},
                                  "flow": {"MELON": -3.0}},
                        msl.DEFAULT_CONFIG) == "hold"
    out = msl.plan_midgame_sells(obs, [["SELL", "WOOL", 24],
                                       ["SELL", "FERTILIZER", 4]])
    assert out == [["SELL", "WOOL", 24], ["SELL", "FERTILIZER", 4]]


def test_off_hour_no_emission_second_slot():
    """计划时点整点发射：hour8 零产出；hour12 发第二批（WHEAT 量 6 的
    第 2 批=2）。"""
    common = dict(shed={"WHEAT": 50}, prices={"WHEAT": 15},
                  shops=["FARMERS_MARKET"], flow={"WHEAT": 3.0})
    assert msl.plan_midgame_sells(make_obs(24 * 13 + 8, **common), []) == []
    assert msl.plan_midgame_sells(make_obs(24 * 13 + 12, **common), []) == \
        [["SELL", "WHEAT", 2]]


def test_max_four_supplement_lines(monkeypatch):
    """补发线行数上限 4：清空日历后 5 条清线（量均 1，名序）只发前 4，
    WOOL 落选。"""
    monkeypatch.setattr(msl, "TAPE_SELL_DAYS", {})
    obs = make_obs(step=24 * 13 + 6,
                   shed={"STRAWBERRY": 5, "MELON": 5, "WOOL": 5, "MILK": 5,
                         "CARROT": 5},
                   prices={"STRAWBERRY": 90, "MELON": 180, "WOOL": 150,
                           "MILK": 110, "CARROT": 20},
                   shops=[], flow={"STRAWBERRY": 3.0, "MELON": 3.0,
                                   "WOOL": 3.0, "MILK": 3.0, "CARROT": 3.0})
    out = msl.plan_midgame_sells(obs, [])
    assert [o[1] for o in out] == ["CARROT", "MELON", "MILK", "STRAWBERRY"]


def test_v1_lifelines_removed():
    """v1 遗产移除：破产生命线（资金<200 不再替换式倾销）与流动性
    tranche（资金<1200 囤态不再强发）在 v2 均不存在——低资金帧只按
    只补发语义行动。"""
    # 破产帧：WOOL 承重线（d13 tape 有卖单）→ 剧本原样，无倾销
    obs = make_obs(step=24 * 13 + 6, shed={"WOOL": 30, "FERTILIZER": 8},
                   prices={"WOOL": 150}, money=150.0, shops=["YARN_STORE"])
    assert msl.plan_midgame_sells(obs, [["SELL", "WOOL", 5]]) == \
        [["SELL", "WOOL", 5]]
    # 流动性帧（v1 该帧无视时点即发 tranche 6）：v2 无该分支，非整点
    # WHEAT（自由线但 hour=3）零产出
    obs = make_obs(step=24 * 13 + 3, shed={"WHEAT": 30},
                   prices={"WHEAT": 15}, money=1000.0, shops=[],
                   flow={"WHEAT": 3.0})
    assert msl.plan_midgame_sells(obs, []) == []


def test_zero_price_floor_segment_clears():
    """零价格（地板段）→ 清；零商铺日帽 1，首批 1 件。"""
    obs = make_obs(step=24 * 13 + 6, shed={"WHEAT": 30},
                   prices={"WHEAT": 0}, shops=[])
    assert msl.plan_midgame_sells(obs, []) == [["SELL", "WHEAT", 1]]


# ===========================================================================
# 五、反克隆/终局/d26+ 让位保留
# ===========================================================================
def test_arbitration_clone_active_frame_defers():
    """反克隆激活帧（step≥160 且近克隆，距离≤2.0）→ 剧本原样（v2 在
    d13+ 窗内同样让位——镜像局 P1 因此静止，属预期保守性）。"""
    obs = make_obs(step=24 * 13 + 6, shed={"WHEAT": 50}, prices={"WHEAT": 15},
                   flow={"WHEAT": 3.0}, farms=base_farms(plants=1))
    assert msl.clone_distance(obs) <= 2.0
    tape = [["SELL", "WOOL", 9]]
    assert msl.plan_midgame_sells(obs, tape) == tape


def test_arbitration_clone_window_distant_farms_planner_runs():
    """step≥160 但农场差异大（距离>2.0）→ 接管运行：WHEAT 空窗补发。"""
    obs = make_obs(step=24 * 13 + 6, shed={"WHEAT": 50}, prices={"WHEAT": 15},
                   shops=["FARMERS_MARKET"], flow={"WHEAT": 3.0},
                   farms=[base_farms(1)[0], base_farms(6)[1]])
    assert msl.clone_distance(obs) > 2.0
    assert msl.plan_midgame_sells(obs, []) == [["SELL", "WHEAT", 2]]


def test_arbitration_terminal_frame_defers():
    """终局帧（step≥717）→ 剧本原样。"""
    obs = make_obs(step=718, shed={"WHEAT": 30}, prices={"WHEAT": 15},
                   flow={"WHEAT": 3.0})
    tape = [["SELL", "WHEAT", 9]]
    assert msl.plan_midgame_sells(obs, tape) == tape


def test_arbitration_endgame_regime_defers():
    """终局倾销段（day≥26）→ 剧本原样。"""
    obs = make_obs(step=26 * 24 + 6, shed={"WHEAT": 30}, prices={"WHEAT": 15},
                   flow={"WHEAT": 3.0})
    tape = [["SELL", "WHEAT", 12]]
    assert msl.plan_midgame_sells(obs, tape) == tape


# ===========================================================================
# 六、fail-safe 与集成缝
# ===========================================================================
def test_failsafe_bad_price_type_falls_back_to_tape():
    """计划器异常（价格类型坏值）→ 回退剧本默认卖单。"""
    obs = make_obs(step=24 * 13 + 6, shed={"WHEAT": 30},
                   prices={"WHEAT": "not-a-price"}, shops=["FARMERS_MARKET"],
                   flow={"WHEAT": 3.0})
    tape = [["SELL", "WHEAT", 7]]
    assert msl.plan_midgame_sells(obs, tape) == tape


def test_failsafe_missing_shed_view_falls_back_to_tape():
    """无库存视图（shed 整体缺失）→ 不接管，剧本原样。"""
    obs = {"step": 24 * 13 + 6, "prices": {"WHEAT": 15}, "money": 5000.0}
    tape = [["SELL", "WHEAT", 7]]
    assert msl.plan_midgame_sells(obs, tape) == tape


def test_empty_shed_no_emission():
    """空库存：零补发；非接管面剧本卖单仍透传。"""
    obs = make_obs(step=24 * 13 + 6, shed={}, prices={"WHEAT": 15},
                   shops=["FARMERS_MARKET"], flow={"WHEAT": 3.0})
    assert msl.plan_midgame_sells(obs, [["SELL", "FERTILIZER", 4]]) == \
        [["SELL", "FERTILIZER", 4]]
    assert msl.plan_midgame_sells(obs, []) == []


def test_apply_to_market_orders_preserves_non_sells():
    """集成缝助手：非 SELL 单原位保留；囤态 SELL 照样透传（不压制）；
    空窗清线补发追加在尾部。"""
    market = [["BUY_PRODUCT", "WHEAT", 5], ["SELL", "WOOL", 24]]
    obs_hold = make_obs(step=24 * 13 + 6, shed={"MELON": 50},
                        prices={"MELON": 180}, shops=["FARMERS_MARKET"],
                        flow={"MELON": -3.0})
    assert msl.apply_to_market_orders(obs_hold, market) == market

    obs_clear = make_obs(step=24 * 13 + 6, shed={"WHEAT": 50},
                         prices={"WHEAT": 15}, shops=["FARMERS_MARKET"],
                         flow={"WHEAT": 3.0})
    assert msl.apply_to_market_orders(
        obs_clear, [["BUY_PRODUCT", "WHEAT", 5]]) == \
        [["BUY_PRODUCT", "WHEAT", 5], ["SELL", "WHEAT", 2]]


def test_apply_to_market_orders_defer_frame_verbatim():
    """仲裁帧：整张 market 列表原样返回（含 SELL）。"""
    obs = make_obs(step=718, shed={"WHEAT": 30}, prices={"WHEAT": 15})
    market = [["BUY_PRODUCT", "WHEAT", 5], ["SELL", "WHEAT", 24]]
    assert msl.apply_to_market_orders(obs, market) == market


def test_determinism_same_obs_same_action():
    """R5 确定性：同 obs 重复调用结果逐字节一致；入参不被 mutate。"""
    obs = make_obs(step=24 * 13 + 6, shed={"WHEAT": 50, "EGG": 10},
                   prices={"WHEAT": 15, "EGG": 40}, shops=["FARMERS_MARKET"],
                   flow={"WHEAT": 3.0})
    tape = [["SELL", "FERTILIZER", 4]]
    tape_snapshot = [list(o) for o in tape]
    r1 = msl.plan_midgame_sells(obs, tape)
    r2 = msl.plan_midgame_sells(obs, tape)
    assert r1 == r2
    assert tape == tape_snapshot
    # 量序：WHEAT 量 6 → 批 [2,2,2]；EGG 量 min(10, 吸收 1, 6)=1 → 批 [1]
    assert r1 == [["SELL", "FERTILIZER", 4], ["SELL", "WHEAT", 2],
                  ["SELL", "EGG", 1]]
