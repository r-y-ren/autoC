# ===========================================================================
# test_run_dawn_planner.py —— 迁移件真实测试（B13）
# ---------------------------------------------------------------------------
# 覆盖（fn_docs/responsibility.md run_submission_agent · run_dawn_planner）：
#   ① 关键符号在场（黎明钩子/治理器/快照恢复/沙盒装载全家）+ 装载形态
#      （旧相对导入零在场，_SRC_FILES 十件序=旧 _SRC_MODULE_ORDER 序）；
#   ② R3 修复流入新链——旧 planner/select.py 名字序裁切（反例集 A=35.0）
#      vs 新 select 提供者值序裁切（65.0）差分；robust_select 别名在场；
#   ③ 等值抽查（≥2 路）——_drip_feed 滴灌/_signature 缓存键/scan_farm/
#      compute_town_demand/dawn_budget/_pick_rung 阶梯/governed_keys 键面+
#      快照-注入-恢复回环 旧新逐字节一致；dawn_hook 旗关零足迹；
#   ④ 文件头迁移登记（源 runtime.py sha256+登记适配 4 处+select 决策）。
# 装置：旧侧=software 根上插 sys.path 后 import planner.runtime（真值实现）；
#   新侧=load_agent_modules 装载整链后取 DTSP_RUNTIME_MODULE（exec 链铸件）。
# ===========================================================================

import hashlib
import sys
import types
from pathlib import Path

import pytest

from shared.discover_campaign_roots import discover_campaign_roots

_ROOTS = discover_campaign_roots(Path(__file__))
OLD_AGENT_DIR = _ROOTS["software_root"] / "kaggle_simulations" / "agent"
NEW_FILE = Path(__file__).resolve().parent.parent.parent / "src" / \
    "run_submission_agent" / "run_dawn_planner.py"
OLD_FILE = OLD_AGENT_DIR / "planner" / "runtime.py"

from run_submission_agent.load_agent_modules import load_agent_modules  # noqa: E402

if str(OLD_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(OLD_AGENT_DIR))


@pytest.fixture(scope="module")
def sides():
    """旧真值 runtime（import planner.runtime）与新 exec 链 runtime 各一。"""
    import planner.runtime as old_rt
    _ns, _agent = load_agent_modules()
    new_rt = _ns["DTSP_RUNTIME_MODULE"]
    return old_rt, new_rt


# ---------------------------------------------------------------------------
# ① 关键符号在场 + 装载形态
# ---------------------------------------------------------------------------

def test_key_symbols_present(sides):
    old_rt, new_rt = sides
    symbols = ["dawn_hook", "reset_state", "trace", "_now", "_cfg",
               "resolve_engine", "scan_farm", "compute_town_demand",
               "build_obs_summary", "update_opponent_ledger", "dawn_budget",
               "build_sandbox_agent", "agent_dir", "_drip_feed",
               "governed_keys", "take_pristine_snapshot", "apply_overrides",
               "restore_pristine", "_signature", "_pick_rung",
               "_rollout_refinement", "_fail_open", "_DEFAULTS", "_STATE",
               "_TRACE"]
    missing = [s for s in symbols if not hasattr(new_rt, s)]
    assert not missing, f"迁移件 exec 后缺失符号: {missing}"
    assert new_rt._DEFAULTS == old_rt._DEFAULTS


def test_exec_chain_adaptations_registered_in_body():
    import re
    body = NEW_FILE.read_text(encoding="utf-8").split('"""', 2)[2]
    # 旧相对导入零在场（登记①：装载器预绑定）——只认真代码行，登记注记
    # 中的引文（"（from . import X as _X）"）不属代码
    assert not re.search(r"^\s*from \. import", body, re.M)
    # _SRC_FILES 十件序=旧 _SRC_MODULE_ORDER 序（登记②③）
    assert '_SRC_FILES = ("_exec_chain/constants.py"' in body
    assert '"_exec_chain/entry.py")' in body
    assert '_SRC_MODULE_ORDER = (' in body      # 旧序保留为注释真值
    # agent_dir 登记④
    assert "os.path.dirname(os.path.abspath(__file__))" in \
        Path(NEW_FILE).read_text(encoding="utf-8")


def test_src_files_order_matches_old_module_order(sides):
    old_rt, new_rt = sides
    files = list(new_rt._SRC_FILES)
    assert len(files) == len(old_rt._SRC_MODULE_ORDER) == 10
    # 首尾锚定（装载序由 load_agent_modules._MODULE_ORDER 持真值，
    # 其对旧 main.py 的逐字一致性由 test_load_agent_modules 钉住）
    assert files[0].endswith("constants.py") and files[-1].endswith("entry.py")
    stems = [f.rsplit("/", 1)[-1][:-3] for f in files]
    assert stems == ["constants", "record_shadow_telemetry",
                     "observe_opponent_state", "decide_macro_mode",
                     "build_mission_pack", "solve_worker_routes",
                     "execute_along_route", "plan_market_orders",
                     "wave", "entry"]


def test_planner_channel_bindings(sides):
    old_rt, new_rt = sides
    # 旧相对导入五名的 exec 链等形：模块对象预绑定在场
    for bind in ("_twin", "_plans", "_opponents", "_wave", "_select"):
        assert isinstance(getattr(new_rt, bind), types.ModuleType), bind
    # P4.1：装载窗内急切铸就（dawn_hook 可直调，无回合期导入依赖）
    assert callable(new_rt.dawn_hook)
    # agent_dir=包根锚（沙盒装载 _SRC_FILES 的定位点）
    assert Path(new_rt.agent_dir()).is_dir()
    assert (Path(new_rt.agent_dir()) / "_exec_chain" / "entry.py").is_file()


# ---------------------------------------------------------------------------
# ② R3 修复流入新链（select 提供者）
# ---------------------------------------------------------------------------

def test_r3_value_order_fix_flows_into_chain(sides):
    old_rt, new_rt = sides
    # 反例集 A（snapshot_tests/test_counterexample_r3.py 同源）：
    #   名字序裁切 → 35.0（旧真值实现现行输出）
    #   值序裁切   → 65.0（R3 修复）
    case_a = {"frozen_style_pool:winner_balanced": 60.0,
              "frozen_style_pool:wheat_suppressor": 100.0,
              "passive_extrapolation": 10.0,
              "pessimistic_fill": 70.0}
    assert old_rt._select.aggregate_scores(dict(case_a)) == 35.0
    assert new_rt._select.aggregate_scores(dict(case_a)) == 65.0


def test_robust_select_alias_face(sides):
    old_rt, new_rt = sides
    # robust_select=robust_selection 的调用面别名（旧 runtime 调用点逐字不变）
    assert new_rt._select.robust_select is new_rt._select.robust_selection
    j = {"P|A": {"m1": 100.0, "m2": 90.0}, "P|B": {"m1": 80.0, "m2": 95.0},
         "IDENT": {"m1": 99.0, "m2": 91.0}}
    a = old_rt._select.robust_select(dict(j), identity_key="IDENT")
    b = new_rt._select.robust_select(dict(j), identity_key="IDENT")
    assert a["best"] == b["best"]      # 该集两序同果（差分集在上一测试）


# ---------------------------------------------------------------------------
# ③ 等值抽查（≥2 路）
# ---------------------------------------------------------------------------

def test_pure_helpers_equivalent(sides):
    old_rt, new_rt = sides
    # 路 1：_drip_feed 滴灌（SELL 日量÷24、BUY 仅首回合全量）
    day_action = {"market": [["SELL", "WOOL", 48], ["BUY_ANIMAL", "COW", 2],
                             ["BUY_PRODUCT", "WHEAT", 5],
                             ["SELL", "MELON", 3], ["BAD"], ["SELL", "X", 0]]}
    for first_turn in (True, False):
        assert repr(old_rt._drip_feed(dict(day_action), first_turn)) == \
            repr(new_rt._drip_feed(dict(day_action), first_turn))
    # 路 2：_signature 缓存键（同 obs 同摘要 → 同键；异日 → 异键）
    farm = {"unlocked_quadrants": ["NW"], "money": 4321.5,
            "tiles": [[{"crop": "WHEAT"}, {"animal": "COW"}], [None, None]]}
    obs = {"farms": [farm, farm], "market": {"inventory": {"WHEAT": 9950}},
           "town": {"unlocked_shops": ["BAKERY"]}, "private": {"shed": {"WHEAT": 3}}}
    summary = {"money": 4321.5, "herd": 1, "crew": 5, "crops": {"WHEAT": 1},
               "unlocked_quadrants": 1, "opponent": {"herd": 2},
               "prices": {"WHEAT": 26.0}}
    assert old_rt._signature(3, 0, summary, obs) == new_rt._signature(3, 0, summary, obs)
    assert old_rt._signature(3, 0, summary, obs) != old_rt._signature(4, 0, summary, obs)
    # 路 3：scan_farm / compute_town_demand / dawn_budget
    assert old_rt.scan_farm(farm) == new_rt.scan_farm(farm)
    module = types.SimpleNamespace(
        SHOPS={"BAKERY": ["EGG", "WHEAT"], "YARN_STORE": ["WOOL"]},
        TOWN_CENTER_PRODUCTS=("WHEAT", "MILK"))
    assert old_rt.compute_town_demand(module, ["YARN_STORE", "BAKERY"]) == \
        new_rt.compute_town_demand(module, ["YARN_STORE", "BAKERY"])
    for pool in (60.0, 30.0, 0.26, None, "bad"):
        o = {"remainingOverageTime": pool} if pool is not None else {}
        assert repr(old_rt.dawn_budget(o, 5, {})) == \
            repr(new_rt.dawn_budget(o, 5, {}))


def test_pick_rung_and_governed_face_equivalent(sides):
    old_rt, new_rt = sides
    # 路 4：_pick_rung 阶梯（速率未实测先验×2 余量，两侧同构）
    assert old_rt._pick_rung({}, 0.9, 1) == new_rt._pick_rung({}, 0.9, 1)
    assert old_rt._pick_rung({}, 0.05, 1) == new_rt._pick_rung({}, 0.05, 1)
    # 路 5：governed 键面 + 快照-注入-恢复回环（fail-open 的等价根基）
    keys = sorted(old_rt.governed_keys(old_rt._plans.identity_spec()))
    keys_new = sorted(new_rt.governed_keys(new_rt._plans.identity_spec()))
    assert keys == keys_new and len(keys) >= 10
    for rt in (old_rt, new_rt):
        ns = {"PLANNER_ENABLED": False, "PLANNER_OVERRIDES": {}}
        for key in keys:
            base = key.split(".", 1)[0]
            if "." in key and base not in ns:
                ns[base] = {}
        snap = rt.take_pristine_snapshot(ns, keys)
        rt.apply_overrides(ns, {"PLANNER_ENABLED": True,
                                "PLANNER_OVERRIDES.sell_price_discount": 0.8})
        assert ns["PLANNER_ENABLED"] is True
        rt.restore_pristine(ns)
        assert ns["PLANNER_ENABLED"] is False and ns["PLANNER_OVERRIDES"] == {}


def test_dawn_hook_flagoff_zero_footprint(sides):
    old_rt, new_rt = sides
    # 旗关（enabled=False）首行短路：零状态写入、零命名空间污染
    for rt in (old_rt, new_rt):
        rt.reset_state()
        ns = {"PLANNER_ENABLED": False, "PLANNER_OVERRIDES": {"k": 1}}
        before = dict(ns)
        out = rt.dawn_hook({"day": 0, "hour": 0}, ns, {"enabled": False})
        assert out is None and ns == before
        assert rt.trace()["dawns"] == [] and rt.trace()["failopens"] == []


# ---------------------------------------------------------------------------
# ④ 文件头迁移登记
# ---------------------------------------------------------------------------

def test_header_docstring_registration():
    head = NEW_FILE.read_text(encoding="utf-8").split('"""')[1]
    old_sha = hashlib.sha256(OLD_FILE.read_bytes()).hexdigest()
    assert "源文件: software/kaggle_simulations/agent/planner/runtime.py" in head
    assert f"源 sha256: {old_sha}" in head
    assert "登记适配（4 处" in head
    assert "值序修复版流入新链" in head        # select 提供者决策登记
