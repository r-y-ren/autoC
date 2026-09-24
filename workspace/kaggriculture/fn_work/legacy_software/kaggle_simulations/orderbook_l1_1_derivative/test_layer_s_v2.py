"""test_layer_s_v2：净需求覆盖口径矩阵 + invariant v2 组（五件）。

v2 块由 make 先生成到 tmp 再以独立模块名载入（_CXS_HOST=None 独立导入态，
同 L1 test_layer_s 的测试通道）；R10 三件经 import test_layer_s 夹具复用
（夹具体内 layer_s_block 全局引用临时改指 v2 模块——import 复用不复制，
防漂移）；c4/c5 两件净口径新例的夹具函数留模块级供 gate_equivalence_v2.
constructed_cases_v2 后续 import 复用（返回 {"expected","got","evidence"}）。"""

import importlib.util
import sys
from pathlib import Path

import pytest

import make_layer_s_v2_block as maker

_THIS_DIR = Path(__file__).resolve().parent
_L1_DIR = _THIS_DIR.parent / "orderbook_l1_derivative"
_L1_BLOCK = _L1_DIR / "layer_s_block.py"
if str(_L1_DIR) not in sys.path:
    sys.path.insert(0, str(_L1_DIR))

import layer_s_block as l1_block  # noqa: E402  L1 对照面（只读，供行为对比冒烟）
import test_layer_s as l1_fixtures  # noqa: E402  R10 夹具库（import 复用）

# 夹具工具沿 test_layer_s import 复用（不复制防漂移）。
_make_plan_view = l1_fixtures._make_plan_view
_obs_with_seeds = l1_fixtures._obs_with_seeds


@pytest.fixture(scope="module")
def v2_block(tmp_path_factory):
    """先 make 到 tmp 再载入：v2 块以独立模块名 exec（diff 校验由 make 内建）。"""
    out = tmp_path_factory.mktemp("v2_block") / "layer_s_block_v2.py"
    maker.make(_L1_BLOCK, out)
    spec = importlib.util.spec_from_file_location("layer_s_block_v2_under_test", out)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


# ---- 净需求覆盖语义全矩阵（v2 口径逐面裁决 + L1 行为对比冒烟）----


def test_net_coverage_matrix(v2_block, monkeypatch):
    surplus = v2_block._cxs_seed_surplus

    # ⑦e（先于任何补丁）独立导入态结构不变式：宿主 None；末 callable=_cxs_agent
    # （注入态"末 callable=官方入口"语义在测试态的同构投影，沿 L1 断言式）。
    assert v2_block._CXS_HOST is None
    assert [v for v in list(vars(v2_block).values()) if callable(v)][-1] is v2_block._cxs_agent

    # ① 磁带未来购买不再计入供给（对照构造：L1 版放行、v2 拒删）。
    # demand=4（660+48=708≤719）；净供给=0+3=3 < 4 → v2 允许删 0（拒删）；
    # L1 三路供给=0+3+磁带未来买4=7 ≥ 4 → 允许删 3（放行整单删）。
    plans1 = {
        660: {"plants": {"CARROT": 4}, "buy_seed": {}},  # 可完成 → demand=4
        670: {"plants": {}, "buy_seed": {"CARROT": 4}},  # 磁带未来买 4：v2 不计
    }
    obs1 = _obs_with_seeds({"CARROT": 0}, step=650)
    kept1 = [["BUY_SEED", "CARROT", 3]]
    assert surplus("CARROT", obs1, kept1, _make_plan_view(plans1), 0) == 0
    assert l1_block._cxs_seed_surplus("CARROT", obs1, kept1, _make_plan_view(plans1), 0) == 3
    # 截断层对照：同一市场 L1 删该单、v2 原对象保留（零足迹）。
    m_l1 = [["BUY_SEED", "CARROT", 3]]
    m_v2 = [["BUY_SEED", "CARROT", 3]]
    assert l1_block._cxs_seed_truncate(obs1, {"market": m_l1}, _make_plan_view(plans1)) == []
    got_trunc_v2 = v2_block._cxs_seed_truncate(obs1, {"market": m_v2}, _make_plan_view(plans1))
    assert got_trunc_v2 is m_v2  # allowed=0 → 零删除零足迹

    # ② 净供给=库存−当前步消耗+保留单（current_plants 语义沿 L1）；
    # v2 需求只调一次 plan_view（无二次一致性交叉核对），L1 调两次。
    plans2 = {660: {"plants": {"CARROT": 4}, "buy_seed": {}}}  # demand=4
    obs2 = _obs_with_seeds({"CARROT": 10}, step=650)
    kept2 = [["BUY_SEED", "CARROT", 5], ["SELL", "WHEAT", 2]]  # 他品项订单不串扰

    def _counting_pv(retval):
        calls = []

        def view(obs):
            calls.append(obs)
            return retval
        return view, calls

    pv_v2, calls_v2 = _counting_pv(plans2)
    got2 = v2_block._cxs_seed_surplus("CARROT", obs2, kept2, pv_v2, 8)
    assert got2 == 3 == max(0, 10 - 8) + 5 - 4  # 有效库存 2 + 保留单 5 − 需求 4
    assert len(calls_v2) == 1  # v2 唯一一次 plan_view 消费点（需求）
    pv_l1, calls_l1 = _counting_pv(plans2)
    l1_block._cxs_seed_surplus("CARROT", obs2, kept2, pv_l1, 8)
    assert len(calls_l1) == 2  # L1 需求一次+磁带重算交叉核对一次

    # 超扣钳 0（plants>held 不产生负供给）：3−8 → 0 后正常放行。
    got2b = surplus("CARROT", _obs_with_seeds({"CARROT": 3}, step=650),
                    [["BUY_SEED", "CARROT", 2]], _make_plan_view({}), 8)
    assert got2b == 2  # min(max(0, 0+2−0), 2)

    # ③ 需求>净供给 → 0（确证无剩余），不是 None。
    plans3 = {650: {"plants": {"CARROT": 6}, "buy_seed": {}}}  # 650+48=698≤719 → demand=6
    got3 = surplus("CARROT", _obs_with_seeds({"CARROT": 2}, step=650),
                   [["BUY_SEED", "CARROT", 3]], _make_plan_view(plans3), 0)
    assert got3 == 0 and got3 is not None  # 净供给 5 < 6

    # ④ demand None → None（plan_view 返回 None / 抛异常 / 形参不可调用）。
    obs4 = _obs_with_seeds({"CARROT": 2}, step=650)
    kept4 = [["BUY_SEED", "CARROT", 3]]
    assert surplus("CARROT", obs4, kept4, _make_plan_view(None), 0) is None
    assert surplus("CARROT", obs4, kept4, _make_plan_view(RuntimeError("tape parse boom")), 0) is None
    assert surplus("CARROT", obs4, kept4, None, 0) is None

    # ⑤ kept_orders 畸形 → None（容器非 list/tuple / 短订单无论操作类型 /
    # 订单非序列 / 本品项 qty 非整数：str/None/bool/半值 float）。
    plans5 = {650: {"plants": {"CARROT": 4}, "buy_seed": {}}}  # demand=4
    obs5 = _obs_with_seeds({"CARROT": 2}, step=650)
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
        assert surplus("CARROT", obs5, bad, _make_plan_view(plans5), 0) is None, bad

    # ⑤b observation 库存字段缺失/类型异常 → None；current_plants 非法 → None。
    bad_obs = [
        None,
        {"step": 650},                                          # 缺 private
        {"step": 650, "private": {}},                           # 缺 seeds
        {"step": 650, "private": {"seeds": "x"}},               # seeds 非 dict
        {"step": 650, "private": {"seeds": {"CARROT": "5"}}},   # 库存计数字符串
        {"step": 650, "private": {"seeds": {"CARROT": 2.5}}},
        {"step": 650, "private": {"seeds": {"CARROT": True}}},
    ]
    for bad in bad_obs:
        assert surplus("CARROT", bad, kept4, _make_plan_view(plans5), 0) is None, bad
    for bad_cp in (-1, -8, True, "8", 2.5, 1.5):
        assert surplus("CARROT", obs5, kept4, _make_plan_view(plans5), bad_cp) is None, bad_cp
    # v2 不再读 observation["step"]（磁带供给项已删，无 t>当前步过滤需求）：
    # 缺 step 仍可判（净供给完全可解析），L1 则 None。
    no_step = {"private": {"seeds": {"CARROT": 2}}}
    assert surplus("CARROT", no_step, kept4, _make_plan_view(plans5), 0) == 1
    assert l1_block._cxs_seed_surplus("CARROT", no_step, kept4, _make_plan_view(plans5), 0) is None

    # ⑥ 允许删除量 ≤ 本回合该品项购买量（删除对象只可能是本回合订单）。
    plans6 = {650: {"plants": {}, "buy_seed": {}}}  # demand=0
    got6 = surplus("CARROT", _obs_with_seeds({"CARROT": 10}, step=650),
                   [["BUY_SEED", "CARROT", 2]], _make_plan_view(plans6), 0)
    assert got6 == 2  # min(max(0, 10+2−0), 2)：原始剩余 12 钳到本回合购买量 2

    # ⑦a _cxs_harvest_completable 行为不变（671 恰可完成/672 永不；每作物两端）。
    assert v2_block._cxs_harvest_completable(671, "CARROT") is True
    assert v2_block._cxs_harvest_completable(672, "CARROT") is False
    deadline = v2_block._CXS_PLANT_DEADLINE_SUM
    for crop, fh in v2_block.FIRST_HARVEST_STEPS.items():
        assert v2_block._cxs_harvest_completable(deadline - fh, crop) is True, (crop, fh)
        assert v2_block._cxs_harvest_completable(deadline - fh + 1, crop) is False, (crop, fh)
    # 常数沿 L1 逐字节继承（diff 校验的运行时投影）。
    assert v2_block._CXS_FROM == l1_block._CXS_FROM == 648
    assert v2_block._CXS_SEASON_END == l1_block._CXS_SEASON_END
    assert v2_block._CXS_PLANT_DEADLINE_SUM == l1_block._CXS_PLANT_DEADLINE_SUM == 719
    assert v2_block.FIRST_HARVEST_STEPS == l1_block.FIRST_HARVEST_STEPS

    # ⑦b _cxs_completable_plant_demand 行为不变：混合步号只计可完成；
    # buy_seed 不入需求。
    mixed = {
        600: {"plants": {"CARROT": 1}, "buy_seed": {}},
        670: {"plants": {"CARROT": 3}, "buy_seed": {"CARROT": 2}},
        672: {"plants": {"CARROT": 2}, "buy_seed": {}},  # 672+48=720>719 不计
    }
    assert v2_block._cxs_completable_plant_demand("CARROT", {"step": 650}, _make_plan_view(mixed)) == 4
    assert v2_block._cxs_completable_plant_demand("CARROT", {"step": 650}, _make_plan_view(None)) is None

    # ⑦c _cxs_seed_truncate 整链（内部调 v2 surplus）：从后往前整单删+槽位保持。
    # 净供给=0+7、demand=3 → allowed=4：末单 qty2 删（2）、中单 qty3 跳过
    # （2+3>4）、首单 qty2 删（2+2≤4）；SELL 原位保留、无重排无插入。
    plans7 = {660: {"plants": {"CARROT": 3}, "buy_seed": {}}}  # 660+48=708≤719
    obs7 = _obs_with_seeds({"CARROT": 0}, step=650)
    market7 = [["BUY_SEED", "CARROT", 2], ["SELL", "WHEAT", 1],
               ["BUY_SEED", "CARROT", 3], ["BUY_SEED", "CARROT", 2]]
    got7 = v2_block._cxs_seed_truncate(obs7, {"market": market7}, _make_plan_view(plans7))
    assert got7 == [["SELL", "WHEAT", 1], ["BUY_SEED", "CARROT", 3]]

    # ⑦d _cxs_agent 全链冒烟（假宿主+假 plan_view+真截断层含 v2 surplus）：
    # 磁带唯一 plants 在 672（不可完成，demand=0）→ 净供给=0+6=6 → 两张 CARROT
    # 买单整单删、SELL 原位保留；宿主调用在 try 外原样收参。
    class _Host:
        def __init__(self, action):
            self.action = action
            self.calls = []

        def __call__(self, observation, configuration=None):
            self.calls.append((observation, configuration))
            return self.action

    market8 = [["BUY_SEED", "CARROT", 4], ["BUY_SEED", "CARROT", 2], ["SELL", "WHEAT", 3]]
    action8 = {"market": market8, "farmer": ["PASS"]}
    host = _Host(action8)
    monkeypatch.setattr(v2_block, "_CXS_HOST", host)
    monkeypatch.setattr(v2_block, "_cxs_plan_view",
                        _make_plan_view({672: {"plants": {"CARROT": 5}, "buy_seed": {}}}))
    obs8 = _obs_with_seeds({"CARROT": 0}, step=650)
    cfg8 = {"sentinel": True}
    got8 = v2_block._cxs_agent(obs8, cfg8)
    assert got8 == {"market": [["SELL", "WHEAT", 3]], "farmer": ["PASS"]}
    assert got8 is not action8 and got8["farmer"] is action8["farmer"]  # 浅拷贝建新 dict
    assert host.calls == [(obs8, cfg8)]  # 宿主调用在 try 外，参数透传

    # ⑧ 与 L1 的行为对比冒烟：差异恰体现"磁带未来供给"项。
    # ⑧a 无磁带未来购买 → 两版逐值相同（净口径退化为 L1 减磁带项）。
    for plans_x, held_x, kept_x, cp_x in [
        ({650: {"plants": {"CARROT": 4}, "buy_seed": {}}},
         1, [["BUY_SEED", "CARROT", 10], ["SELL", "WHEAT", 2]], 0),
        ({672: {"plants": {"CARROT": 5}, "buy_seed": {}}},
         0, [["BUY_SEED", "CARROT", 4], ["BUY_SEED", "CARROT", 2]], 0),
        ({660: {"plants": {"CARROT": 5}, "buy_seed": {}}},
         10, [["BUY_SEED", "CARROT", 5]], 8),
    ]:
        obs_x = _obs_with_seeds({"CARROT": held_x}, step=650)
        l1v = l1_block._cxs_seed_surplus("CARROT", obs_x, kept_x, _make_plan_view(plans_x), cp_x)
        v2v = surplus("CARROT", obs_x, kept_x, _make_plan_view(plans_x), cp_x)
        assert v2v == l1v, (plans_x, l1v, v2v)
    # ⑧b 有磁带未来购买且两版均未触钳制 → 差值恰=磁带未来购买量。
    plans_diff = {
        650: {"plants": {"CARROT": 6}, "buy_seed": {}},   # demand=6（698≤719）
        660: {"plants": {}, "buy_seed": {"CARROT": 4}},   # 磁带未来买 4（t>650）
    }
    obs_d = _obs_with_seeds({"CARROT": 0}, step=650)
    kept_d = [["BUY_SEED", "CARROT", 8]]
    l1d = l1_block._cxs_seed_surplus("CARROT", obs_d, kept_d, _make_plan_view(plans_diff), 0)
    v2d = surplus("CARROT", obs_d, kept_d, _make_plan_view(plans_diff), 0)
    assert (l1d, v2d) == (6, 2) and l1d - v2d == 4  # 差值=磁带未来购买量 4
    # ⑧c 方向不变式：v2 ≤ L1 恒成立（净供给只会更小→删得更少，更保守）。
    assert v2d <= l1d


# ---- invariant v2 组（五件：R10 三件复用 + v2 净口径两件新例）----


def _run_fixture_under(fixture, v2_module):
    """R10 夹具在 v2 块上重演：夹具体内 layer_s_block 全局引用临时改指 v2 模块。"""
    original = l1_fixtures.layer_s_block
    l1_fixtures.layer_s_block = v2_module
    try:
        return fixture()
    finally:
        l1_fixtures.layer_s_block = original


def _invariant_case_c4_net_covered_buyback_deleted(v2_module):
    """用例④（v2 新增·删）：窗口内非磁带回买单且净供给已覆盖需求 → 删。

    决策步 650，磁带 660 plants 4（660+48=708≤719 可完成 → demand=4）；库存
    已有 4（恰=需求，任何当回合买单都是回买冗余），市场多一张回买单 qty3 →
    净供给 4+3=7 ≥ 4 → allowed=min(3,3)=3 → 回买单整单删、非 BUY_SEED 原样
    原位保留。
    """
    plans = {660: {"plants": {"CARROT": 4}, "buy_seed": {}}}
    obs = _obs_with_seeds({"CARROT": 4}, step=650)
    market = [["SELL", "WHEAT", 1], ["BUY_SEED", "CARROT", 3]]
    got = v2_module._cxs_seed_truncate(obs, {"market": market}, _make_plan_view(plans))
    return {
        "expected": [["SELL", "WHEAT", 1]],
        "got": got,
        "evidence": "step=650 net supply (4+3) covers demand 4 -> allowed 3, "
                    "non-tape buy-back order dropped, SELL kept",
    }


def _invariant_case_c5_net_short_true_future_plant_kept(v2_module):
    """用例⑤（v2 新增·保）：净供给<需求（真未来种植）→ 保留。

    决策步 650，磁带 660 plants 6（可完成 → 真未来种植需求 6）；库存 2 + 当
    回合买单 3 = 净供给 5 < 6 → allowed=0 → 回买单保留。磁带 670 的未来买单 4
    不计入供给（v2 净口径：磁带单由各自回合同判定守护）——对照 L1 三路供给
    2+3+4=9 ≥ 6 → allowed=3 → 同输入 L1 会删（见测试内对照断言）。
    """
    plans = {
        660: {"plants": {"CARROT": 6}, "buy_seed": {}},   # 真未来种植需求 6
        670: {"plants": {}, "buy_seed": {"CARROT": 4}},   # 磁带未来买：v2 不计供给
    }
    obs = _obs_with_seeds({"CARROT": 2}, step=650)
    market = [["BUY_SEED", "CARROT", 3]]
    got = v2_module._cxs_seed_truncate(obs, {"market": market}, _make_plan_view(plans))
    return {
        "expected": [["BUY_SEED", "CARROT", 3]],
        "got": got,
        "evidence": "step=650 net supply (2+3) < real demand 6 (tape future buy 4 "
                    "not counted) -> allowed 0, order kept",
    }


def test_invariant_cases_v2(v2_block):
    # R10 三件沿 import test_layer_s 夹具复用（夹具全局 layer_s_block 临时改指
    # v2 块——三例磁带均无未来买单，L1/v2 净口径同值，真值不变）。
    c1 = _run_fixture_under(l1_fixtures._invariant_case_c1_no_trunc_when_future_plant, v2_block)
    assert c1["got"] == c1["expected"]

    c2 = _run_fixture_under(l1_fixtures._invariant_case_c2_trunc_when_no_opportunity, v2_block)
    assert c2["got"] == c2["expected"]

    c3 = _run_fixture_under(l1_fixtures._invariant_case_c3_s671_boundary, v2_block)
    assert c3["truncate_side"]["got"] == c3["truncate_side"]["expected"]
    assert c3["keep_side"]["got"] == c3["keep_side"]["expected"]

    # v2 两件净口径新例。
    c4 = _invariant_case_c4_net_covered_buyback_deleted(v2_block)
    assert c4["got"] == c4["expected"]

    c5 = _invariant_case_c5_net_short_true_future_plant_kept(v2_block)
    assert c5["got"] == c5["expected"]

    # c5 对照面：同输入下 L1（三路供给计磁带未来买 4 → 供给 9−需求 6 → 钳 3）
    # 会整单删——恰体现 v2 净口径"真未来种植保留"的方向性差异。
    plans_c5 = {
        660: {"plants": {"CARROT": 6}, "buy_seed": {}},
        670: {"plants": {}, "buy_seed": {"CARROT": 4}},
    }
    l1_got = l1_block._cxs_seed_truncate(
        _obs_with_seeds({"CARROT": 2}, step=650),
        {"market": [["BUY_SEED", "CARROT", 3]]},
        _make_plan_view(plans_c5))
    assert l1_got == []
