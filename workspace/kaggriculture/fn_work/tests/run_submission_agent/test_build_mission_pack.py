# ===========================================================================
# test_build_mission_pack.py —— 迁移件真实测试（B12）
# ---------------------------------------------------------------------------
# 覆盖（fn_docs/responsibility.md run_submission_agent · build_mission_pack）：
#   ① 关键符号在场（11 件，含任务包/影子包/enrich 升格全家）；
#   ② R10 剥离——WEED_RECLAIM "all" 死支零在场（正文无该分支形态）；行为
#      反证：现行 "planned" 档旧新逐字节一致；把死档值 "all" 打进两侧命名
#      空间时旧源多出 C3 变体 DIG(v=40) 任务、迁移副本没有（死支确被剥）；
#   ③ 纯函数等值抽查——_mission_cls/_mission_tier 升格矩阵、_build_tasks
#      （h5/h21 双时点）、_build_mission（mission_hash 逐字节一致）；
#   ④ 文件头迁移登记（源路径+源 sha256+剥离清单 1 项）。
# 装置：种子 imports + 旧树 constants/strategy/market 为共同依赖基座
#   （_field_alloc 与 _crop_future_value/_window 系），再 exec 旧/新本件。
# ===========================================================================

import hashlib
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

_ROOTS = discover_campaign_roots(Path(__file__))
OLD_SRC = _ROOTS["software_root"] / "kaggle_simulations" / "agent" / "src"
NEW_FILE = Path(__file__).resolve().parent.parent.parent / "src" / \
    "run_submission_agent" / "build_mission_pack.py"
OLD_FILE = OLD_SRC / "mission.py"
_SEED_IMPORTS = "import copy\nimport math\nimport json\nimport hashlib\n"


def _exec_into(ns, path):
    exec(compile(Path(path).read_text(encoding="utf-8"), str(path), "exec"), ns)


def _namespace(use_migrated, weed_mode=None):
    ns = {}
    exec(_SEED_IMPORTS, ns)
    for dep in ("constants", "strategy", "market"):
        _exec_into(ns, OLD_SRC / (dep + ".py"))
    _exec_into(ns, NEW_FILE if use_migrated else OLD_FILE)
    if weed_mode is not None:
        ns["WEED_RECLAIM_MODE"] = weed_mode
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
PRIVATE = {"shed": {"WHEAT": 12, "SHEEP": 1, "FERTILIZER": 6},
           "inventories": [{"WHEAT": 3}, {}],
           "seeds": {"STRAWBERRY": 3, "WHEAT": 6}}
PRICES = {"STRAWBERRY": 120, "WHEAT": 25, "MILK": 160, "WOOL": 200,
          "MELON": 250, "FERTILIZER": 100}


def _obs(hour):
    return {"player": 0, "day": 10, "hour": hour, "step": 250,
            "market": {"prices": PRICES},
            "town": {"unlocked_shops": ["SMOOTHIE_SHOP", "FARMERS_MARKET"]},
            "farms": [FARM, dict(FARM, money=800)]}


# 死支反证专用布局（6x6）：18 麦（wheat_room 耗尽）+ 7 空舍（结构需求满足）
# + (0,0) 杂草（NW 象限、牧场环外）→ 各作物相位/价格门全关，杂草不被规划。
_N = 6
_TILES = [[None] * _N for _ in range(_N)]
_TILES[0][0] = {"kind": "WEED"}
_SQUARES = [(x, y) for y in range(_N) for x in range(_N) if (x, y) != (0, 0)]
for _x, _y in _SQUARES[:18]:
    _TILES[_y][_x] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 0,
                      "yield_units": 1}
for _x, _y in _SQUARES[18:]:
    _TILES[_y][_x] = {"kind": "PASTURE"}
DEAD_BRANCH_FARM = {"unlocked_quadrants": ["NW"], "money": 5000.0,
                    "tiles": _TILES, "hands": [[2, 2]], "farmer": [2, 2]}
DEAD_BRANCH_PRIVATE = {"shed": {}, "inventories": [{}, {}], "seeds": {}}
_LOW_PRICES = {k: 10 for k in PRICES}
DEAD_BRANCH_OBS = {"player": 0, "day": 0, "hour": 21, "step": 21,
                   "market": {"prices": _LOW_PRICES},
                   "town": {"unlocked_shops": []},
                   "farms": [DEAD_BRANCH_FARM, DEAD_BRANCH_FARM]}


# --------------------------------------------------------------------------
# ① 关键符号在场
# --------------------------------------------------------------------------

def test_key_symbols_present_after_exec():
    ns = _namespace(use_migrated=True)
    symbols = [
        "_build_tasks", "_MISSION_DEADLINE_HOURS", "_MISSION_SHADOW",
        "_mission_cls", "_mission_tile_map", "_mission_tier",
        "_enrich_mission_tasks", "_build_mission", "_mission_shadow_update",
        "_mission_refresh_planned_sell", "mission_shadow",
    ]
    missing = [s for s in symbols if s not in ns]
    assert not missing, f"迁移件 exec 后缺失符号: {missing}"
    assert ns["_MISSION_DEADLINE_HOURS"]["HARVEST"] is None  # §2.2 D4 无硬死线


# --------------------------------------------------------------------------
# ② R10 剥离：WEED "all" 死支
# --------------------------------------------------------------------------

def test_dead_branch_absent_in_body():
    body = NEW_FILE.read_text(encoding="utf-8").split('"""', 2)[2]
    assert 'WEED_RECLAIM_MODE == "all"' not in body


def test_dead_branch_behavioral_counterproof():
    # 现行档 "planned"：旧新逐字节一致（行为不变判据）。
    old = _namespace(False, weed_mode="planned")
    new = _namespace(True, weed_mode="planned")
    t_old = old["_build_tasks"](DEAD_BRANCH_OBS, DEAD_BRANCH_FARM,
                                DEAD_BRANCH_PRIVATE, 0)[0]
    t_new = new["_build_tasks"](DEAD_BRANCH_OBS, DEAD_BRANCH_FARM,
                                DEAD_BRANCH_PRIVATE, 0)[0]
    assert repr(t_old) == repr(t_new)
    # 死档 "all"（R10 裁决不迁）：旧源多出 C3 变体 DIG(v=40)，迁移副本没有。
    old_all = _namespace(False, weed_mode="all")
    new_all = _namespace(True, weed_mode="all")
    t_old_all = old_all["_build_tasks"](DEAD_BRANCH_OBS, DEAD_BRANCH_FARM,
                                        DEAD_BRANCH_PRIVATE, 0)[0]
    t_new_all = new_all["_build_tasks"](DEAD_BRANCH_OBS, DEAD_BRANCH_FARM,
                                        DEAD_BRANCH_PRIVATE, 0)[0]
    assert [t for t in t_old_all if t["act"] == ["DIG"] and t["v"] == 40]
    assert not [t for t in t_new_all if t["act"] == ["DIG"] and t["v"] == 40]


# --------------------------------------------------------------------------
# ③ 纯函数等值抽查
# --------------------------------------------------------------------------

def test_enrichment_cls_tier_equivalent():
    old, new = _namespace(False), _namespace(True)
    raw = [
        {"w": 98, "x": 0, "y": 2, "act": ["WATER"], "key": ("water", 0, 2),
         "v": 300.0, "red": True, "need": None, "units": None},
        {"w": 100, "x": 1, "y": 0, "act": ["FEED"], "key": ("feed", 1, 0),
         "v": 460.0, "red": True, "need": "WHEAT", "units": None},
        {"w": 85, "x": 2, "y": 0, "act": ["HARVEST"], "key": ("h", 2, 0),
         "v": 500.0, "red": False, "need": None, "units": None},
        {"w": 56, "x": 1, "y": 1, "act": ["CARE"], "key": ("care", 1, 1),
         "v": 260.0, "red": False, "need": None, "units": None},
        {"w": 96, "x": 1, "y": 1, "act": ["PICKUP", "WHEAT", 5],
         "key": ("pickup_w", 0), "v": 300.0, "red": False, "need": None,
         "units": None},
    ]
    tile_map = old["_mission_tile_map"](FARM)
    assert (repr(old["_enrich_mission_tasks"](raw, tile_map, 10))
            == repr(new["_enrich_mission_tasks"](raw, tile_map, 10)))


def test_build_tasks_equivalent_two_hours():
    old, new = _namespace(False), _namespace(True)
    for hour in (5, 21):
        result_old = old["_build_tasks"](_obs(hour), FARM, PRIVATE, 10)
        result_new = new["_build_tasks"](_obs(hour), FARM, PRIVATE, 10)
        assert repr(result_old) == repr(result_new)
    # 非平凡性护栏：该布局应铺出覆盖多操作类的非空任务表
    tasks_late = new["_build_tasks"](_obs(21), FARM, PRIVATE, 10)[0]
    assert tasks_late
    assert len({t["act"][0] for t in tasks_late}) >= 3


def test_build_mission_hash_equivalent():
    old, new = _namespace(False), _namespace(True)
    for planned_sell in (None, 0, 7):
        tasks = old["_build_tasks"](_obs(21), FARM, PRIVATE, 10)[0]
        m_old = old["_build_mission"](_obs(21), FARM, PRIVATE, 10, {},
                                      tasks, planned_sell=planned_sell)
        m_new = new["_build_mission"](_obs(21), FARM, PRIVATE, 10, {},
                                      tasks, planned_sell=planned_sell)
        assert repr(m_old) == repr(m_new)
        assert m_old["mission_hash"] == m_new["mission_hash"]
    # 影子缓存两席位行为一致
    assert (repr(old["_mission_shadow_update"](0, 10, 21, _obs(21), FARM,
                                               PRIVATE, {}, tasks))
            == repr(new["_mission_shadow_update"](0, 10, 21, _obs(21), FARM,
                                                  PRIVATE, {}, tasks)))


# --------------------------------------------------------------------------
# ④ 文件头迁移登记
# --------------------------------------------------------------------------

def test_header_docstring_registration():
    head = NEW_FILE.read_text(encoding="utf-8").split('"""')[1]
    old_sha = hashlib.sha256(OLD_FILE.read_bytes()).hexdigest()
    assert "源文件: software/kaggle_simulations/agent/src/mission.py" in head
    assert f"源 sha256: {old_sha}" in head
    assert "剥离清单" in head and "1 项" in head
    assert 'WEED_RECLAIM_MODE == "all"' in head  # 登记头如实记录被剥项
