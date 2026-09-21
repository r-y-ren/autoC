# ===========================================================================
# test_run_submission_agent.py —— 顶层入口真实测试（B13）
# ---------------------------------------------------------------------------
# 覆盖（fn_docs/responsibility.md run_submission_agent · L0 顶层）：
#   ① agent_load_path 式可装载形态——importlib 按路径装载（官方装载语义
#      镜像），module.agent 可调用且为装载产物（get_last_callable 契约）；
#   ② 共享命名空间契约面——agent.__globals__ 即装载模块 globals（含
#      DTSP_RUNTIME_CONFIG/PLANNER_ENABLED/DTSP_RUNTIME_MODULE，旗关面
#      agent.__globals__[...] 直接访问与旧 main 同构）；
#   ③ 行为——空 obs/无 tiles 早退回 PASS；内部异常整体吞降级 PASS
#      （fail-open 第一道：patch _macro_plan 抛错仍回合法动作）；
#   ④ R10——_SELLRACE_SHIP 死支零在场；双装载实例 config 隔离。
# ===========================================================================

import importlib.util
import sys
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

_ROOTS = discover_campaign_roots(Path(__file__))
ENTRY_FILE = (_ROOTS["campaign_root"] / "fn_work" / "src" /
              "run_submission_agent" / "run_submission_agent.py")


def _load_module(tag):
    """kgenv.load_submission_agent 同构的路径装载（唯一模块名防缓存）。"""
    spec = importlib.util.spec_from_file_location(f"rsa_entry_{tag}", ENTRY_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# ① 可装载形态 + 最后 callable
# ---------------------------------------------------------------------------

def test_loadable_by_path_with_agent_callable():
    module = _load_module("face")
    agent = module.agent
    assert callable(agent)
    # 尾部重绑的薄前递（装载器 exec 铸，__globals__=模块 globals）
    assert agent.__globals__ is module.__dict__
    assert callable(module.__dict__["_agent_impl"])
    assert module.__dict__["_agent_impl"] is not agent


# ---------------------------------------------------------------------------
# ② 共享命名空间契约面
# ---------------------------------------------------------------------------

def test_agent_globals_is_shared_chain_namespace():
    module = _load_module("ns")
    g = module.agent.__globals__
    assert g["DTSP_RUNTIME_CONFIG"]["enabled"] is True   # 默认 DTSP 开
    assert g["PLANNER_ENABLED"] is False                # constants 默认旗关
    assert g["DTSP_RUNTIME_MODULE"] is not None         # P4.1 急切铸就
    assert callable(g["DTSP_RUNTIME_MODULE"].dawn_hook)
    for symbol in ("plan_market_orders", "_market_orders", "_solve_and_execute",
                   "_build_tasks", "_macro_plan", "CROPS", "SHED_CAPACITY"):
        assert symbol in g, f"链命名空间缺 {symbol}"


# ---------------------------------------------------------------------------
# ③ 行为（fail-open 第一道）
# ---------------------------------------------------------------------------

FARM = {"unlocked_quadrants": ["NW"], "money": 3000.0, "farmer": [3, 3],
        "tiles": [[None] * 7 for _ in range(7)], "hands": []}
OBS = {"player": 0, "day": 0, "hour": 5, "step": 5,
       "farms": [FARM, FARM],
       "market": {"prices": {"WHEAT": 25}},
       "town": {"unlocked_shops": []}}


def test_empty_and_tileless_obs_return_safe_pass():
    module = _load_module("pass")
    assert module.agent({}) == {"farmer": ["PASS"], "hands": [], "market": []}
    no_tiles = {"player": 0, "farms": [dict(FARM, tiles=[])], "day": 0,
                "hour": 5}
    assert module.agent(no_tiles) == {"farmer": ["PASS"], "hands": [],
                                      "market": []}


def test_internal_exception_degrades_to_pass():
    module = _load_module("failopen")
    def boom(player, obs, day):
        raise RuntimeError("injected pipeline failure")
    module._macro_plan = boom          # 共享命名空间注入（globals 查找面）
    out = module.agent(OBS)
    assert out == {"farmer": ["PASS"], "hands": [], "market": []}
    # 对照：不注错时同一 obs 产出真实非平凡动作
    module2 = _load_module("normal")
    out2 = module2.agent(OBS)
    assert set(out2) == {"farmer", "hands", "market"}
    assert out2["farmer"] != ["PASS"] or out2["market"]


# ---------------------------------------------------------------------------
# ④ R10 死支零在场 + 实例隔离
# ---------------------------------------------------------------------------

def test_sellrace_ship_absent_and_config_isolated():
    m1 = _load_module("iso1")
    m2 = _load_module("iso2")
    assert "_SELLRACE_SHIP" not in m1.__dict__          # R10 死支不迁
    c1 = m1.agent.__globals__["DTSP_RUNTIME_CONFIG"]
    c2 = m2.agent.__globals__["DTSP_RUNTIME_CONFIG"]
    assert c1 is not c2 and c1 == c2
    c1["enabled"] = False                                # 独立关旗不串扰
    assert c2["enabled"] is True
