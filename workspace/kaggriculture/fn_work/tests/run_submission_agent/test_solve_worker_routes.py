# ===========================================================================
# test_solve_worker_routes.py —— 迁移件真实测试（B12）
# ---------------------------------------------------------------------------
# 覆盖（fn_docs/responsibility.md run_submission_agent · solve_worker_routes）：
#   ① 关键符号在场（8 件）；
#   ② R10 剥离三件零在场——_two_opt_segment/_dawn_crew_size/_schedule_units
#      在 exec 后命名空间与正文（剥登记头后）均零命中；
#   ③ 纯函数等值抽查——_two_opt_feasible/_seq_deadlines_ok/_solve_routes
#      （现役形 planned_hands=0+unit_pos、诊断形 planned_hands=None）与
#      现役链 _solve_and_execute（constants→telemetry→observer→strategy→
#      mission→solver→executor→market 全链装载，仅 solver 换迁移件）；
#   ④ 文件头迁移登记（源路径+源 sha256+剥离清单 3 项）。
# ===========================================================================

import hashlib
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

_ROOTS = discover_campaign_roots(Path(__file__))
OLD_SRC = _ROOTS["software_root"] / "kaggle_simulations" / "agent" / "src"
NEW_FILE = Path(__file__).resolve().parent.parent.parent / "src" / \
    "run_submission_agent" / "solve_worker_routes.py"
OLD_FILE = OLD_SRC / "solver.py"
_SEED_IMPORTS = "import copy\nimport math\nimport json\nimport hashlib\n"
# main.py _MODULE_ORDER 的前八位（wave/entry 属其余批次，与本件无关）
_CHAIN_BEFORE = ("constants", "telemetry", "observer", "strategy", "mission")
_CHAIN_AFTER = ("executor", "market")

STRIPPED = ("_two_opt_segment", "_dawn_crew_size", "_schedule_units")


def _exec_into(ns, path):
    exec(compile(Path(path).read_text(encoding="utf-8"), str(path), "exec"), ns)


def _namespace(use_migrated, chain=False):
    ns = {}
    exec(_SEED_IMPORTS, ns)
    for dep in _CHAIN_BEFORE if chain else ("constants",):
        _exec_into(ns, OLD_SRC / (dep + ".py"))
    _exec_into(ns, NEW_FILE if use_migrated else OLD_FILE)
    if chain:
        for dep in _CHAIN_AFTER:
            _exec_into(ns, OLD_SRC / (dep + ".py"))
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
         None,
         {"kind": "PLANT", "crop": "WHEAT", "planted_day": 5,
          "yield_units": 1}],
        [None, None,
         {"kind": "PLANT", "crop": "STRAWBERRY", "planted_day": 11,
          "consecutive_unwatered": 1, "yield_units": 0}],
    ],
    "hands": [[1, 1], [2, 2]],
}
PRIVATE = {"shed": {"WHEAT": 12, "FERTILIZER": 6},
           "inventories": [{"WHEAT": 3}, {}]}
PRICES = {"STRAWBERRY": 120, "WHEAT": 25, "MILK": 160, "WOOL": 200,
          "MELON": 250, "FERTILIZER": 100}


def _obs(hour):
    return {"player": 0, "day": 10, "hour": hour, "step": 250,
            "market": {"prices": PRICES},
            "town": {"unlocked_shops": ["SMOOTHIE_SHOP"]},
            "farms": [FARM, dict(FARM, money=800)]}


TASKS = [
    {"w": 98, "x": 0, "y": 2, "act": ["WATER"], "key": ("water", 0, 2),
     "v": 300.0, "red": True, "need": None, "units": None,
     "deadline": 21},
    {"w": 85, "x": 2, "y": 0, "act": ["HARVEST"], "key": ("harvest", 2, 0),
     "v": 500.0, "red": False, "need": None, "units": None,
     "deadline": None},
    {"w": 88, "x": 1, "y": 0, "act": ["FEED"], "key": ("feed", 1, 0),
     "v": 460.0, "red": False, "need": "WHEAT", "units": None,
     "deadline": 16},
    {"w": 40, "x": 1, "y": 1, "act": ["PICKUP", "WHEAT", 5],
     "key": ("pickup_w", 0), "v": 300.0, "red": False, "need": None,
     "units": None, "deadline": None},
]


# --------------------------------------------------------------------------
# ① 关键符号在场
# --------------------------------------------------------------------------

def test_key_symbols_present_after_exec():
    ns = _namespace(use_migrated=True)
    symbols = ["_seg_len", "_seq_deadlines_ok", "_two_opt_feasible",
               "_NEED_CHUNK", "_solve_routes", "_ASSIGN_MEM",
               "_current_units", "_solve_and_execute"]
    missing = [s for s in symbols if s not in ns]
    assert not missing, f"迁移件 exec 后缺失符号: {missing}"


# --------------------------------------------------------------------------
# ② R10 剥离三件零在场
# --------------------------------------------------------------------------

def test_stripped_symbols_absent_everywhere():
    ns = _namespace(use_migrated=True)
    for sym in STRIPPED:
        assert sym not in ns, sym
    body = NEW_FILE.read_text(encoding="utf-8").split('"""', 2)[2]
    for sym in STRIPPED:
        assert sym not in body, sym


# --------------------------------------------------------------------------
# ③ 纯函数等值抽查
# --------------------------------------------------------------------------

def test_two_opt_feasible_equivalent():
    old, new = _namespace(False), _namespace(True)
    for hour in (3, 20):
        seq = [dict(t) for t in TASKS]
        assert (repr(old["_two_opt_feasible"](seq, (1, 1), hour))
                == repr(new["_two_opt_feasible"](seq, (1, 1), hour)))
        seq2 = [dict(t) for t in TASKS[:3]]
        assert (repr(old["_two_opt_feasible"](seq2, (0, 0), hour))
                == repr(new["_two_opt_feasible"](seq2, (0, 0), hour)))


def test_solve_routes_live_shape_equivalent():
    old, new = _namespace(False), _namespace(True)
    kw = dict(planned_hands=0, hour=3, unit_pos=[(1, 1), (2, 2)],
              sticky=None)
    assert (repr(old["_solve_routes"](FARM, PRIVATE, 10, TASKS, **kw))
            == repr(new["_solve_routes"](FARM, PRIVATE, 10, TASKS, **kw)))
    # 载货腿+sticky 连续性通道
    kw2 = dict(planned_hands=0, hour=3, unit_pos=[(2, 0), (0, 2)],
               sticky={0: str(("harvest", 2, 0))})
    assert (repr(old["_solve_routes"](FARM, PRIVATE, 10, TASKS, **kw2))
            == repr(new["_solve_routes"](FARM, PRIVATE, 10, TASKS, **kw2)))


def test_solve_routes_dawn_diagnostic_shape_equivalent():
    # 诊断形（planned_hands=None/unit_pos=None）：旧源回退臂在 constants-only
    # 基座下同样折算 0 计划船员（_crew_target 缺名被 _dawn_crew_size 内部
    # try/except 吞掉）——迁移副本的 None→0 归一与其等值。
    old, new = _namespace(False), _namespace(True)
    assert (repr(old["_solve_routes"](FARM, PRIVATE, 10, TASKS))
            == repr(new["_solve_routes"](FARM, PRIVATE, 10, TASKS)))


def test_solve_and_execute_full_chain_equivalent():
    old = _namespace(False, chain=True)
    new = _namespace(True, chain=True)
    tasks = old["_build_tasks"](_obs(5), FARM, PRIVATE, 10)[0]
    assert (repr(old["_solve_and_execute"](_obs(5), FARM, PRIVATE, 10,
                                           tasks))
            == repr(new["_solve_and_execute"](_obs(5), FARM, PRIVATE, 10,
                                              tasks)))
    late_tasks = old["_build_tasks"](_obs(20), FARM, PRIVATE, 10)[0]
    assert (repr(old["_solve_and_execute"](_obs(20), FARM, PRIVATE, 10,
                                           late_tasks))
            == repr(new["_solve_and_execute"](_obs(20), FARM, PRIVATE, 10,
                                              late_tasks)))


# --------------------------------------------------------------------------
# ④ 文件头迁移登记
# --------------------------------------------------------------------------

def test_header_docstring_registration():
    head = NEW_FILE.read_text(encoding="utf-8").split('"""')[1]
    old_sha = hashlib.sha256(OLD_FILE.read_bytes()).hexdigest()
    assert "源文件: software/kaggle_simulations/agent/src/solver.py" in head
    assert f"源 sha256: {old_sha}" in head
    assert "剥离清单" in head and "3 项" in head
    for sym in STRIPPED:
        assert sym in head  # 登记头如实记录被剥三件
