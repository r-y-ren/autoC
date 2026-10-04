# ===========================================================================
# test_record_shadow_telemetry.py —— 迁移件真实测试（B13）
# ---------------------------------------------------------------------------
# 覆盖（fn_docs/responsibility.md run_submission_agent · record_shadow_telemetry）：
#   ① 关键符号在场（遥测全家：开关/sink/快照/记录/调度 trace）；
#   ② 零删改件——正文（剥文件头登记 docstring 后）与旧源逐字节一致；
#   ③ 等值抽查——_telemetry_record_turn 同输入旧新 exec 的快照逐字节一致
#      （两路：常规回合计数 + sink 注入异常全吞旁路）、
#      _telemetry_wheat_alive/_telemetry_inventory_total 纯函数对照；
#   ④ 文件头迁移登记（源路径+源 sha256+剥离清单=无）。
# 装置：种子 imports + 旧树 constants 为共同依赖基座（MOVES/_get/
#   _quadrant_of/SEASON_DAYS），再 exec 旧/新本件（mission/market/observer
#   影子名缺席——其消费在 try/except 旁路内，两侧同构降信不抛）。
# ===========================================================================

import hashlib
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

_ROOTS = discover_campaign_roots(Path(__file__))
OLD_SRC = _ROOTS["software_root"] / "kaggle_simulations" / "agent" / "src"
NEW_FILE = Path(__file__).resolve().parent.parent.parent / "src" / \
    "run_submission_agent" / "record_shadow_telemetry.py"
OLD_FILE = OLD_SRC / "telemetry.py"
_SEED_IMPORTS = "import copy\nimport math\nimport json\nimport hashlib\n"


def _exec_into(ns, path):
    exec(compile(Path(path).read_text(encoding="utf-8"), str(path), "exec"), ns)


def _namespace(use_migrated):
    ns = {}
    exec(_SEED_IMPORTS, ns)
    _exec_into(ns, OLD_SRC / "constants.py")
    _exec_into(ns, NEW_FILE if use_migrated else OLD_FILE)
    return ns


FARM = {
    "unlocked_quadrants": ["NW"], "money": 1234.5, "farmer": [1, 1],
    "tiles": [
        [None,
         {"kind": "PLANT", "crop": "STRAWBERRY", "planted_day": 9,
          "yield_units": 2, "max_lifespan_step": 300},
         {"kind": "WEED"}],
        [{"animal": "COW", "placed_day": 2, "yield_units": 3,
          "fed_today": True},
         {"kind": "PLANT", "crop": "WHEAT", "planted_day": 5,
          "yield_units": 1},
         None],
        [None, None,
         {"kind": "PLANT", "crop": "WHEAT", "planted_day": 11,
          "consecutive_unwatered": 1, "yield_units": 4}],
    ],
    "hands": [[2, 2], [1, 0]],
}
PRIVATE = {"shed": {"WHEAT": 12, "FERTILIZER": 6},
           "inventories": [{"WHEAT": 3}, {"MILK": 2}]}
OBS = {"player": 0, "day": 4, "hour": 7, "step": 100,
       "farms": [FARM, FARM],
       "market": {"prices": {"WHEAT": 25, "MILK": 160, "WOOL": 200,
                             "STRAWBERRY": 120, "MELON": 250,
                             "FERTILIZER": 100}},
       "town": {"unlocked_shops": ["BAKERY"]}}
ACTIONS = [["EAST"], ["WATER"], ["PASS"], ["HARVEST"], ["FEED"]]
TASKS = [{"act": ["WATER"], "red": False}, {"act": ["FEED"], "red": True},
         {"act": ["CARE"], "red": False}]
TRACE = {"action_targets": {1: (1, 1), 3: (2, 1), 4: (0, 1)},
         "assign": {1: "w-1-1", 3: "h-2-1"}, "cross_quadrant": 2}
ORDERS = [["BUY_PRODUCT", "WHEAT", 3], ["SELL", "WOOL", 4]]


# ---------------------------------------------------------------------------
# ① 关键符号在场
# ---------------------------------------------------------------------------

def test_key_symbols_present_after_exec():
    ns = _namespace(use_migrated=True)
    symbols = [
        "TELEMETRY_ENABLED", "set_telemetry_enabled", "set_telemetry_sink",
        "reset_telemetry", "telemetry_snapshot", "_telemetry_day_template",
        "_telemetry_record_turn", "scheduler_trace",
    ]
    missing = [s for s in symbols if s not in ns]
    assert not missing, f"迁移件 exec 后缺失符号: {missing}"


# ---------------------------------------------------------------------------
# ② 零删改件：正文与旧源逐字节一致
# ---------------------------------------------------------------------------

def test_body_byte_identical_to_old_source():
    body = NEW_FILE.read_text(encoding="utf-8").split('"""', 2)[2].lstrip("\n")
    old = OLD_FILE.read_text(encoding="utf-8")
    assert body == old


# ---------------------------------------------------------------------------
# ③ 等值抽查（≥2 路）
# ---------------------------------------------------------------------------

def test_record_turn_snapshot_equivalent():
    old, new = _namespace(False), _namespace(True)
    for ns in (old, new):
        ns["_telemetry_record_turn"](OBS, FARM, PRIVATE, ACTIONS, TASKS,
                                     TRACE, ORDERS)
    assert old["telemetry_snapshot"]() == new["telemetry_snapshot"]()
    day = new["telemetry_snapshot"]()["players"]["0"]["days"]["4"]
    # 非平凡性护栏：本回合计数真实落账（5 动作=1 移动+1 PASS+3 操作）
    assert day["turns"] == 1 and day["moving_turns"] == 1
    assert day["pass_count"] == 1 and day["effective_ops"] == 3
    assert day["wheat_alive"] == 2


def test_record_turn_sink_swallow_and_disable_equivalent():
    old, new = _namespace(False), _namespace(True)
    # 路 2：sink 抛异常全吞（旁路契约），快照仍逐字节一致
    def boom(event):
        raise RuntimeError("sink failure must never propagate")
    for ns in (old, new):
        ns["set_telemetry_sink"](boom)
        ns["_telemetry_record_turn"](OBS, FARM, PRIVATE, ACTIONS, TASKS,
                                     TRACE, ORDERS)
    assert old["telemetry_snapshot"]() == new["telemetry_snapshot"]()
    # 路 3：TELEMETRY_ENABLED=False 旁路（记录短路）
    for ns in (old, new):
        ns["reset_telemetry"]()
        ns["set_telemetry_enabled"](False)
        ns["_telemetry_record_turn"](OBS, FARM, PRIVATE, ACTIONS, TASKS,
                                     TRACE, ORDERS)
    assert old["telemetry_snapshot"]() == new["telemetry_snapshot"]()
    assert new["telemetry_snapshot"]()["players"] == {}   # 短路零落账


def test_pure_helpers_equivalent():
    old, new = _namespace(False), _namespace(True)
    assert old["_telemetry_wheat_alive"](FARM) == \
        new["_telemetry_wheat_alive"](FARM) == 2
    assert old["_telemetry_inventory_total"](PRIVATE) == \
        new["_telemetry_inventory_total"](PRIVATE) == 23


# ---------------------------------------------------------------------------
# ④ 文件头迁移登记
# ---------------------------------------------------------------------------

def test_header_docstring_registration():
    head = NEW_FILE.read_text(encoding="utf-8").split('"""')[1]
    old_sha = hashlib.sha256(OLD_FILE.read_bytes()).hexdigest()
    assert "源文件: software/kaggle_simulations/agent/src/telemetry.py" in head
    assert f"源 sha256: {old_sha}" in head
    assert "剥离清单" in head and "无" in head
