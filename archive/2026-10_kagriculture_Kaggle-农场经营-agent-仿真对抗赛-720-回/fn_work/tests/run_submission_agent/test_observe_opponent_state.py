# ===========================================================================
# test_observe_opponent_state.py —— 迁移件真实测试（B12）
# ---------------------------------------------------------------------------
# 覆盖（fn_docs/responsibility.md run_submission_agent · observe_opponent_state）：
#   ① 关键符号在场——迁移件 exec 进共享命名空间后逐名断言（15 件）；
#   ② 正文逐字等身——剥离文件头登记 docstring 后与旧源逐字节一致（零删改件）；
#   ③ 纯函数等值抽查——同输入下 旧源 exec vs 新源 exec 输出 repr 逐字节一致
#      （_farm_scan/_species_counts/_opp_production_calendar/_market_flow/
#      _opp_observer_update 日账五路）；
#   ④ 迁移登记——文件头 docstring 含 源文件路径 + 源 sha256（对当前旧树实算）+
#      剥离清单（本件=无）。
# 装置：命名空间按 main.py _load_pipeline 同款种子（copy/math/json/hashlib）
#   先 exec 旧树 constants.py（+market.py 供 _offset_from_price/_town_daily_demand
#   调用期解析），再 exec 旧/新本件——只读消费旧树源文件，不 import 进产品码。
# ===========================================================================

import hashlib
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

_ROOTS = discover_campaign_roots(Path(__file__))
OLD_SRC = _ROOTS["software_root"] / "kaggle_simulations" / "agent" / "src"
NEW_FILE = Path(__file__).resolve().parent.parent.parent / "src" / \
    "run_submission_agent" / "observe_opponent_state.py"
OLD_FILE = OLD_SRC / "observer.py"
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
    "hands": [[1, 1], [2, 2]],
}
PRIVATE = {"shed": {"SHEEP": 2}, "inventories": [{"COW": 1}, {}]}
OBS = {
    "player": 0, "day": 8, "hour": 5, "step": 200,
    "market": {"prices": {"STRAWBERRY": 120, "WHEAT": 25, "MILK": 160,
                          "WOOL": 200, "MELON": 250},
               "inventory": {"WHEAT": 10000, "MILK": 10010}},
    "town": {"unlocked_shops": ["SMOOTHIE_SHOP", "FARMERS_MARKET"]},
    "farms": [FARM, dict(FARM, money=800)],
}


# --------------------------------------------------------------------------
# ① 关键符号在场
# --------------------------------------------------------------------------

def test_key_symbols_present_after_exec():
    ns = _namespace(use_migrated=True)
    symbols = [
        "_farm_scan", "_count_crops", "_species_counts", "_market_flow",
        "_MARKET_MEM", "OBSERVER_ENABLED", "reset_observer",
        "observer_snapshot", "_opp_note_orders", "_opp_note_fills",
        "_opp_observer_update", "_observer_state_for", "est_opp_net",
        "est_opp_held", "est_opp_conf", "est_opp_supply_horizon",
        "_opp_production_calendar",
    ]
    missing = [s for s in symbols if s not in ns]
    assert not missing, f"迁移件 exec 后缺失符号: {missing}"
    assert ns["OBSERVER_ENABLED"] is True


# --------------------------------------------------------------------------
# ② 零删改件：正文与旧源逐字节一致（剥离文件头登记 docstring 后）
# --------------------------------------------------------------------------

def test_body_verbatim_matches_old_source():
    body = NEW_FILE.read_text(encoding="utf-8").split('"""', 2)[2]
    assert body == "\n\n" + OLD_FILE.read_text(encoding="utf-8")


# --------------------------------------------------------------------------
# ③ 纯函数等值抽查（旧源 exec vs 新源 exec，同输入同依赖基座）
# --------------------------------------------------------------------------

def test_farm_scan_and_species_counts_equivalent():
    old, new = _namespace(False), _namespace(True)
    assert repr(old["_farm_scan"](FARM)) == repr(new["_farm_scan"](FARM))
    assert (repr(old["_species_counts"](FARM, PRIVATE, 7))
            == repr(new["_species_counts"](FARM, PRIVATE, 7)))
    assert (repr(old["_count_crops"](FARM))
            == repr(new["_count_crops"](FARM)))


def test_production_calendar_equivalent():
    old, new = _namespace(False), _namespace(True)
    for day in (0, 12, 25):
        for horizon in (7, 14):
            assert (repr(old["_opp_production_calendar"](FARM, day, horizon))
                    == repr(new["_opp_production_calendar"](FARM, day,
                                                           horizon)))


def test_market_flow_sequence_equivalent():
    old, new = _namespace(False), _namespace(True)
    seq = [(3, {"WHEAT": 25, "MILK": 160}),
           (4, {"WHEAT": 24, "MILK": 158}),
           (5, {"WHEAT": 30, "MILK": 170})]
    got_old = [old["_market_flow"](0, d, pr) for d, pr in seq]
    got_new = [new["_market_flow"](0, d, pr) for d, pr in seq]
    assert repr(got_old) == repr(got_new)
    assert any(v for v in got_old[-1].values()), "EMA 流非平凡性护栏"


def test_observer_day_account_equivalent():
    old, new = _namespace(False), _namespace(True)
    old["_opp_observer_update"](OBS, None)
    new["_opp_observer_update"](OBS, None)
    snap_old = old["observer_snapshot"]()
    snap_new = new["observer_snapshot"]()
    assert repr(snap_old) == repr(snap_new)
    # est_* getter 同值（含置信帽消费路径）
    for item in ("WHEAT", "MILK"):
        assert (repr(old["est_opp_held"](item))
                == repr(new["est_opp_held"](item)))
        assert (repr(old["est_opp_conf"](item))
                == repr(new["est_opp_conf"](item)))


# --------------------------------------------------------------------------
# ④ 文件头迁移登记：源路径 + 源 sha256（对当前旧树实算）+ 剥离清单
# --------------------------------------------------------------------------

def test_header_docstring_registration():
    head = NEW_FILE.read_text(encoding="utf-8").split('"""')[1]
    old_sha = hashlib.sha256(OLD_FILE.read_bytes()).hexdigest()
    assert "源文件: software/kaggle_simulations/agent/src/observer.py" in head
    assert f"源 sha256: {old_sha}" in head
    assert "剥离清单" in head
    assert "无" in head.split("剥离清单")[1].split("\n")[0]
