# ===========================================================================
# test_plan_market_orders.py —— 迁移件真实测试（B13）
# ---------------------------------------------------------------------------
# 覆盖（fn_docs/responsibility.md run_submission_agent · plan_market_orders）：
#   ① 关键符号在场（市场层全家：镜像定价/优先级/预算仿真/卖出计划器/
#      sellrace/committed_spend 状态件）；
#   ② R10 剥离——_note_buys 死 shim 零在场（正文无 def _note_buys）；行为
#      反证：旧 ns 有 _note_buys、迁移 ns 无；_note_buy_order 本体双侧在场；
#   ③ 纯函数等值抽查——_market_price_emb 曲线网格（双侧偏移×9 品类）、
#      _market_order_priority 优先级矩阵（10 单型×末日/常日）、
#      plan_market_orders 端到端预算仿真（混合订单×预算/库容约束）同输入
#      旧新 exec 输出逐字节一致；
#   ④ 文件头迁移登记（源路径+源 sha256+剥离清单 1 项）。
# 装置：种子 imports + 旧树 constants 为共同依赖基座（CROPS/ANIMALS/
#   MARKET_PARAMS_EMB/_get/_dist 等），再 exec 旧/新本件。
# ===========================================================================

import hashlib
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

_ROOTS = discover_campaign_roots(Path(__file__))
OLD_SRC = _ROOTS["software_root"] / "kaggle_simulations" / "agent" / "src"
NEW_FILE = Path(__file__).resolve().parent.parent.parent / "src" / \
    "run_submission_agent" / "plan_market_orders.py"
OLD_FILE = OLD_SRC / "market.py"
_SEED_IMPORTS = "import copy\nimport math\nimport json\nimport hashlib\n"


def _exec_into(ns, path):
    exec(compile(Path(path).read_text(encoding="utf-8"), str(path), "exec"), ns)


def _namespace(use_migrated):
    ns = {}
    exec(_SEED_IMPORTS, ns)
    _exec_into(ns, OLD_SRC / "constants.py")
    _exec_into(ns, NEW_FILE if use_migrated else OLD_FILE)
    return ns


# ---------------------------------------------------------------------------
# ① 关键符号在场
# ---------------------------------------------------------------------------

def test_key_symbols_present_after_exec():
    ns = _namespace(use_migrated=True)
    symbols = [
        "_STATE", "_town_daily_demand", "_buy_pace", "_note_buy_order",
        "_hire_cost", "_market_price_emb", "_market_order_priority",
        "plan_market_orders", "buy_product_cost", "_affordable_buy_units",
        "_project_price", "_market_gates", "_sell_plan_dawn",
        "sell_plan_shadow", "_finalize_sell_plan_batches",
        "_sellrace_leads", "_market_orders",
    ]
    missing = [s for s in symbols if s not in ns]
    assert not missing, f"迁移件 exec 后缺失符号: {missing}"


# ---------------------------------------------------------------------------
# ② R10 剥离：_note_buys 死 shim
# ---------------------------------------------------------------------------

def test_dead_shim_absent_in_body():
    body = NEW_FILE.read_text(encoding="utf-8").split('"""', 2)[2]
    assert "def _note_buys" not in body


def test_dead_shim_behavioral_counterproof():
    old, new = _namespace(False), _namespace(True)
    # 旧源有 shim；迁移副本没有（死 shim 确被剥）；本体双侧在场且行为一致。
    assert callable(old["_note_buys"])
    assert "_note_buys" not in new
    assert callable(new["_note_buy_order"])
    old["_note_buy_order"](0, 3, 5, 2)
    new["_note_buy_order"](0, 3, 5, 2)
    assert repr(old["_STATE"]) == repr(new["_STATE"])


# ---------------------------------------------------------------------------
# ③ 纯函数等值抽查（≥2 路）
# ---------------------------------------------------------------------------

def test_market_price_emb_grid_equivalent():
    old, new = _namespace(False), _namespace(True)
    for item in ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON",
                 "EGG", "MILK", "WOOL", "FERTILIZER"):
        for inventory in (0, 5000, 9900, 10000, 10050, 10200, 12000, 20000):
            a = old["_market_price_emb"](item, inventory)
            b = new["_market_price_emb"](item, inventory)
            assert a == b, f"{item}@{inventory}: {a} != {b}"
    # 非平凡性护栏：上下侧曲线确有差异（引擎镜像定价活跃）
    ns = new
    assert ns["_market_price_emb"]("MELON", 10000) == 250
    assert ns["_market_price_emb"]("MELON", 10400) < 250   # sq 上侧压价
    assert ns["_market_price_emb"]("WOOL", 9600) > 200     # log 下侧抬价


def test_market_order_priority_matrix_equivalent():
    old, new = _namespace(False), _namespace(True)
    orders = [
        ["SELL", "MELON", 5], ["BUY_PRODUCT", "WHEAT", 3],
        ["BUY_ANIMAL", "COW", 2], ["BUY_LAND", "NE"],
        ["HIRE"], ["BUY_SEED", "WHEAT", 9], ["BUY_SEED", "MELON", 7],
        ["BUY_PRODUCT", "FERTILIZER", 1], ["PASS"], [],
    ]
    for day in (0, 5, 28, 29):
        for order in orders:
            assert (old["_market_order_priority"](order, day)
                    == new["_market_order_priority"](order, day)), \
                f"{order}@d{day} priority drifted"
    # 末日只卖语义钉住
    assert new["_market_order_priority"](["SELL", "MELON", 5], 29) == 100
    assert new["_market_order_priority"](["HIRE"], 29) == -1


def test_plan_market_orders_budget_simulation_equivalent():
    old, new = _namespace(False), _namespace(True)
    orders = [
        ["BUY_PRODUCT", "WHEAT", 5], ["SELL", "WOOL", 24],
        ["SELL", "MELON", 42], ["BUY_ANIMAL", "COW", 5],
        ["BUY_LAND", "NE"], ["HIRE"], ["HIRE"], ["HIRE"],
        ["BUY_SEED", "MELON", 7], ["BUY_SEED", "WHEAT", 9],
        ["SELL", "MILK", 30], ["BUY_ANIMAL", "SHEEP", 6],
    ]
    for money, shed_count in ((3000.0, 0), (3000.0, 60), (12000.0, 10),
                              (95.0, 40)):
        for day in (0, 10, 29):
            kwargs = dict(day=day, max_orders=10, shed_capacity=100,
                          hires_today=0, hands_count=5, quadrants_owned=1,
                          prices={"WHEAT": 25, "WOOL": 200, "MELON": 250,
                                  "MILK": 160, "FERTILIZER": 100},
                          shed_stock={"WOOL": 24, "MELON": 42, "MILK": 30},
                          market_inventory={"WHEAT": 10000, "WOOL": 10000,
                                            "MELON": 10000, "MILK": 10000,
                                            "FERTILIZER": 10000})
            a = old["plan_market_orders"](orders, money, shed_count, **kwargs)
            b = new["plan_market_orders"](orders, money, shed_count, **kwargs)
            assert repr(a) == repr(b), f"budget sim m={money} s={shed_count} d={day}"
    # 非平凡性护栏：穷预算截断真实生效（无可变现库存时钱包即硬界——
    # 买单逐件按曲线价成交，花光即止）
    poor = new["plan_market_orders"](orders, 95.0, 0, day=0,
                                     prices={"WHEAT": 25}, shed_stock={})
    assert len(poor["accepted"]) <= 10
    assert poor["committed_spend"] <= 95.0 + 1e-9
    assert poor["remaining_money"] >= 0.0
    assert poor["truncated"] is True


# ---------------------------------------------------------------------------
# ④ 文件头迁移登记
# ---------------------------------------------------------------------------

def test_header_docstring_registration():
    head = NEW_FILE.read_text(encoding="utf-8").split('"""')[1]
    old_sha = hashlib.sha256(OLD_FILE.read_bytes()).hexdigest()
    assert "源文件: software/kaggle_simulations/agent/src/market.py" in head
    assert f"源 sha256: {old_sha}" in head
    assert "剥离清单" in head and "1 项" in head
    assert "_note_buys" in head          # 登记头如实记录被剥项
