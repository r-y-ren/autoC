# ===========================================================================
# test_execute_along_route.py —— 迁移件真实测试（B12）
# ---------------------------------------------------------------------------
# 覆盖（fn_docs/responsibility.md run_submission_agent · execute_along_route）：
#   ① 关键符号在场（10 件）；
#   ② 零删改件——正文（剥文件头登记 docstring 后）与旧源逐字节一致；
#   ③ 纯函数等值抽查——_stop_done 完成判据矩阵、_execute_routes（常日
#      沿线行走/D1 断言触发、幂等 REPLAN 门两连击、d29 DROP→SELL 队列）
#      同输入旧新 exec 输出逐字节一致；
#   ④ 文件头迁移登记（源路径+源 sha256+剥离清单=无）。
# 装置：种子 imports + 旧树 constants + market（供 sell_plan_shadow 调用期
#   解析，EOD 断言路径），再 exec 旧/新本件。
# ===========================================================================

import hashlib
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

_ROOTS = discover_campaign_roots(Path(__file__))
OLD_SRC = _ROOTS["software_root"] / "kaggle_simulations" / "agent" / "src"
NEW_FILE = Path(__file__).resolve().parent.parent.parent / "src" / \
    "run_submission_agent" / "execute_along_route.py"
OLD_FILE = OLD_SRC / "executor.py"
_SEED_IMPORTS = "import copy\nimport math\nimport json\nimport hashlib\n"


def _exec_into(ns, path):
    exec(compile(Path(path).read_text(encoding="utf-8"), str(path), "exec"), ns)


def _namespace(use_migrated):
    ns = {}
    exec(_SEED_IMPORTS, ns)
    for dep in ("constants", "market"):
        _exec_into(ns, OLD_SRC / (dep + ".py"))
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
         None,
         {"kind": "PLANT", "crop": "WHEAT", "planted_day": 5,
          "yield_units": 1}],
        [None, None,
         {"kind": "PLANT", "crop": "STRAWBERRY", "planted_day": 11,
          "consecutive_unwatered": 1, "yield_units": 0}],
    ],
    "hands": [[2, 2]],
}
PRICES = {"STRAWBERRY": 120, "WHEAT": 25, "MILK": 160, "WOOL": 200,
          "MELON": 250, "FERTILIZER": 100}


def _obs(day, hour):
    return {"player": 0, "day": day, "hour": hour, "step": 24 * day + hour,
            "market": {"prices": PRICES},
            "town": {"unlocked_shops": ["SMOOTHIE_SHOP"]},
            "farms": [FARM, dict(FARM, money=800)]}


TASKS = [
    {"w": 98, "x": 0, "y": 2, "act": ["WATER"], "key": ("water", 0, 2),
     "v": 300.0, "red": True, "need": None, "units": None,
     "deadline": 21, "tier": "D1", "cls": "OBLIGATION"},
    {"w": 85, "x": 2, "y": 0, "act": ["HARVEST"], "key": ("harvest", 2, 0),
     "v": 500.0, "red": False, "need": None, "units": None,
     "deadline": None, "tier": "D4", "cls": "YIELD"},
]
ROUTES = [{"worker": 0, "sector": "NW", "etas": [],
           "stops": [t["key"] for t in TASKS], "tasks": [dict(t) for t in TASKS]},
          {"worker": 1, "sector": None, "etas": [], "stops": [], "tasks": []}]


# --------------------------------------------------------------------------
# ① 关键符号在场
# --------------------------------------------------------------------------

def test_key_symbols_present_after_exec():
    ns = _namespace(use_migrated=True)
    symbols = ["_REPLAN_MEM", "_EXEC_DONE_MEM", "_D29_SELL_QUEUE",
               "_replan_signature", "_replan_gate", "_executor_tiles",
               "_stop_done", "_remaining_harvest_inflow",
               "_planned_sell_today", "_execute_routes"]
    missing = [s for s in symbols if s not in ns]
    assert not missing, f"迁移件 exec 后缺失符号: {missing}"
    assert ns["EXECUTOR_D1_ASSERT"] is True
    assert ns["EXECUTOR_EOD_ASSERT"] is True


# --------------------------------------------------------------------------
# ② 零删改件：正文与旧源逐字节一致
# --------------------------------------------------------------------------

def test_body_verbatim_matches_old_source():
    body = NEW_FILE.read_text(encoding="utf-8").split('"""', 2)[2]
    assert body == "\n\n" + OLD_FILE.read_text(encoding="utf-8")


# --------------------------------------------------------------------------
# ③ 纯函数/执行等值抽查
# --------------------------------------------------------------------------

def test_stop_done_matrix_equivalent():
    old, new = _namespace(False), _namespace(True)
    tiles = (None, {}, {"kind": "WEED"}, {"watered_today": True},
             {"fed_today": False}, {"cared_today": True},
             {"yield_units": 2}, {"yield_units": 0},
             {"fertilized_until_day": 9}, {"fertilized_until_day": 11},
             {"animal": "COW"}, {"kind": "PLANT"})
    acts = (None, ["WATER"], ["FEED"], ["CARE"], ["FERTILIZE"], ["DIG"],
            ["HARVEST"], ["PLACE"], ["PLANT"], ["BUILD_PASTURE"])
    got_old = [[old["_stop_done"](t, a, 10) for a in acts] for t in tiles]
    got_new = [[new["_stop_done"](t, a, 10) for a in acts] for t in tiles]
    assert repr(got_old) == repr(got_new)


def test_execute_routes_walk_and_d1_assert_equivalent():
    old, new = _namespace(False), _namespace(True)
    private = {"shed": {"WHEAT": 2}, "inventories": [{}, {}]}
    # 常日：farmer(1,1) 未在首站(0,2) → 行走；D1 断言不触发
    got_old = old["_execute_routes"](_obs(10, 5), FARM, private, 10, ROUTES)
    got_new = new["_execute_routes"](_obs(10, 5), FARM, private, 10, ROUTES)
    assert repr(got_old) == repr(got_new)
    assert got_old[0][0] != ["PASS"]
    # 晚钟：D1 死线 21 vs ETA 越线 → replan=True（两连击被幂等闸压平）
    late = _obs(10, 20)
    r1_old = old["_execute_routes"](late, FARM, private, 10, ROUTES)
    r2_old = old["_execute_routes"](late, FARM, private, 10, ROUTES)
    r1_new = new["_execute_routes"](late, FARM, private, 10, ROUTES)
    r2_new = new["_execute_routes"](late, FARM, private, 10, ROUTES)
    assert repr((r1_old, r2_old)) == repr((r1_new, r2_new))


def test_execute_routes_d29_liquidation_equivalent():
    old, new = _namespace(False), _namespace(True)
    # d29 内联清算：farmer 在仓口 (1,1)（board=3 的 _shed_access 成员）且随身
    # 有货 → DROP 入 _D29_SELL_QUEUE；hand 无货 → PASS。
    private = {"shed": {}, "inventories": [{"WHEAT": 5, "MILK": 2}, {}]}
    got_old = old["_execute_routes"](_obs(29, 8), FARM, private, 29, [])
    got_new = new["_execute_routes"](_obs(29, 8), FARM, private, 29, [])
    assert repr(got_old) == repr(got_new)
    assert got_old[0][0] == ["DROP"]
    assert repr(old["_D29_SELL_QUEUE"]) == repr(new["_D29_SELL_QUEUE"])
    assert new["_D29_SELL_QUEUE"][0] == {"MILK": 2, "WHEAT": 5}
    # 不在仓口 → 朝最近仓口行走
    farm_far = dict(FARM, farmer=[0, 2])
    obs_far = _obs(29, 8)
    obs_far["farms"] = [farm_far, farm_far]
    got_old = old["_execute_routes"](obs_far, farm_far, private, 29, [])
    got_new = new["_execute_routes"](obs_far, farm_far, private, 29, [])
    assert repr(got_old) == repr(got_new)
    assert got_old[0][0] in (["EAST"], ["WEST"], ["NORTH"], ["SOUTH"])


def test_remaining_harvest_inflow_equivalent():
    old, new = _namespace(False), _namespace(True)
    tile_map = old["_executor_tiles"](FARM)
    assert (repr(old["_remaining_harvest_inflow"](ROUTES, tile_map, 10))
            == repr(new["_remaining_harvest_inflow"](ROUTES, tile_map, 10)))


# --------------------------------------------------------------------------
# ④ 文件头迁移登记
# --------------------------------------------------------------------------

def test_header_docstring_registration():
    head = NEW_FILE.read_text(encoding="utf-8").split('"""')[1]
    old_sha = hashlib.sha256(OLD_FILE.read_bytes()).hexdigest()
    assert "源文件: software/kaggle_simulations/agent/src/executor.py" in head
    assert f"源 sha256: {old_sha}" in head
    assert "剥离清单" in head
    assert "无" in head.split("剥离清单")[1].split("\n")[0]
