# ===========================================================================
# test_load_agent_modules.py —— 装载器真实测试（B13）
# ---------------------------------------------------------------------------
# 覆盖（fn_docs/responsibility.md run_submission_agent · load_agent_modules）：
#   ① 装载序真值——_MODULE_ORDER 与旧 main.py 的 _MODULE_ORDER 逐字一致
#      （ast 解析旧源取值比对，防漂移）+ 十件映射盘上存在；
#   ② 装载产物——(ns, agent) 返回；共享命名空间关键符号（十件代表+种子
#      imports）；尾部重绑 agent=最后 callable（_agent_impl=entry 实现）；
#      DTSP_RUNTIME_CONFIG 每次装载新铸（两装载实例隔离）；
#   ③ planner 通道——装载窗内急切铸就 DTSP_RUNTIME_MODULE（dawn_hook/
#      trace/reset_state 可用，P4.1 红线）；_SELLRACE_SHIP 死支零在场（R10）；
#      sys.path 腰带（包根+fn_work/src）；
#   ④ precheck 语义——缺件 fail-closed 抛 RuntimeError；装载后 agent 对
#      空 obs fail-open 回 PASS（入口契约快查）。
# ===========================================================================

import ast
import sys
from pathlib import Path

import pytest

from shared.discover_campaign_roots import discover_campaign_roots

_ROOTS = discover_campaign_roots(Path(__file__))
OLD_MAIN = (_ROOTS["software_root"] / "kaggle_simulations" / "agent" /
            "main.py")

from run_submission_agent import load_agent_modules as lam  # noqa: E402
from run_submission_agent.load_agent_modules import load_agent_modules  # noqa: E402,E501


def _old_module_order():
    """旧 main.py 的 _MODULE_ORDER 真值（ast 取字面量，防手抄漂移）。"""
    tree = ast.parse(OLD_MAIN.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and \
                isinstance(node.targets[0], ast.Name) and \
                node.targets[0].id == "_MODULE_ORDER":
            return tuple(ast.literal_eval(node.value))
    raise AssertionError("_MODULE_ORDER not found in old main.py")


# ---------------------------------------------------------------------------
# ① 装载序真值
# ---------------------------------------------------------------------------

def test_module_order_matches_old_main_truth():
    assert lam._MODULE_ORDER == _old_module_order() == (
        "constants", "telemetry", "observer", "strategy", "mission",
        "solver", "executor", "market", "wave", "entry")


def test_chain_files_exist_on_disk():
    pkg = Path(lam._PACKAGE_ROOT)
    for name, rel in lam._CHAIN_FILES.items():
        assert (pkg / rel).is_file(), f"{name} -> {rel} 缺件"
    for _bind, rel in lam._PLANNER_FILES:
        assert (pkg / rel).is_file(), f"planner 件 {rel} 缺件"


# ---------------------------------------------------------------------------
# ② 装载产物
# ---------------------------------------------------------------------------

def test_load_returns_shared_ns_and_last_callable():
    ns, agent = load_agent_modules()
    assert callable(agent) and agent.__globals__ is ns
    # 尾部重绑：entry 实现存 _agent_impl，agent 为薄前递（最后 callable）
    assert callable(ns["_agent_impl"]) and ns["_agent_impl"] is not agent
    # 十件代表符号 + 种子 imports（旧 _load_pipeline 契约面）
    for symbol in ("CROPS", "MARKET_PARAMS_EMB",           # constants
                   "TELEMETRY_ENABLED",                     # telemetry
                   "_farm_scan",                            # observer
                   "_macro_plan", "_decide_mode",           # strategy
                   "_build_tasks", "mission_shadow",        # mission
                   "_solve_and_execute",                    # solver
                   "_execute_routes",                       # executor
                   "plan_market_orders", "_market_orders",  # market
                   "_wave_enabled",                         # wave
                   "SHED_CAPACITY", "copy", "math", "json", "hashlib"):
        assert symbol in ns, f"共享命名空间缺 {symbol}"
    # 旧 main 的装载序契约侧影：entry 的 agent 实现不在 ns["agent"] 名下
    assert ns["agent"] is agent


def test_dtsp_config_fresh_per_load():
    ns1, _ = load_agent_modules()
    ns2, _ = load_agent_modules()
    # 每次装载新铸 dict（旧 main 逐次 exec 字面量语义——独立关旗契约面）
    assert ns1["DTSP_RUNTIME_CONFIG"] is not ns2["DTSP_RUNTIME_CONFIG"]
    assert ns1["DTSP_RUNTIME_CONFIG"] == ns2["DTSP_RUNTIME_CONFIG"] == {
        "enabled": True, "seed": 1, "budget_cap_s": 0.85,
        "rollout_models": ("pessimistic_fill",),
        "ladder": ((6, 1), (4, 2), (3, 3), (2, 4), (1, 6))}
    # 共享可变量隔离（market _STATE / telemetry _TELEMETRY 各自独立）
    assert ns1["_STATE"] is not ns2["_STATE"]
    assert ns1["_TELEMETRY"] is not ns2["_TELEMETRY"]


# ---------------------------------------------------------------------------
# ③ planner 通道 + R10 + 腰带
# ---------------------------------------------------------------------------

def test_planner_channel_eager_built():
    ns, _agent = load_agent_modules()
    rt = ns["DTSP_RUNTIME_MODULE"]
    # P4.1：装载窗内急切铸就（装载期在场，非回合期导入产物）
    assert rt is not None
    for attr in ("dawn_hook", "trace", "reset_state"):
        assert callable(getattr(rt, attr)), attr
    # 装载窗内即有 trace 视图（无任何 dawn 记录）
    assert rt.trace() == {"dawns": [], "failopens": [], "game_resets": 0,
                          "engaged": False}


def test_sellrace_ship_dead_branch_absent():
    ns, _agent = load_agent_modules()
    assert "_SELLRACE_SHIP" not in ns          # R10 死支不迁
    # 对照：旋钮本体（constants 里的 SELLRACE_MODE 旗面）保留
    assert ns["SELLRACE_MODE"] is False


def test_sys_path_belt_inserted():
    load_agent_modules()
    assert lam._PACKAGE_ROOT in sys.path
    assert lam._FNWORK_SRC in sys.path


# ---------------------------------------------------------------------------
# ④ precheck 语义 + 入口契约快查
# ---------------------------------------------------------------------------

def test_missing_module_fail_closed(tmp_path):
    with pytest.raises(RuntimeError, match="装载缺件"):
        load_agent_modules(str(tmp_path))


def test_agent_failopen_on_empty_obs():
    _ns, agent = load_agent_modules()
    assert agent({}) == {"farmer": ["PASS"], "hands": [], "market": []}
