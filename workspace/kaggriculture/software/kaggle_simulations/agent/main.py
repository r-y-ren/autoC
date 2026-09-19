# Kaggriculture submission agent -- MULTI-MODULE tar.gz ENTRY (v13.1, M5+)
# ===========================================================================
# 提交件形态（2026-09-03 用户裁决）：tar.gz 多模块包（官方引擎
# get_last_callable 显式支持同目录导入："append exec_dir so that way
# python agents can import other files"）。本文件是唯一入口：
#   * 顶部 64 字节保留 "Kaggriculture submission agent" 标记（历史契约）；
#   * 按拓扑序把 src/ 九模块装载进同一扁平命名空间（与 src-split 时代
#     的静态合并语义完全一致，只是合并点从构建期移到导入期）；
#   * 把全部名字提升到本模块（历史测试按 main.<name> 直接访问）；
#   * def agent 是本文件最后一个 callable（官方 get_last_callable 契约）。
# 开发环：改 agent/src/*.py → 直接 pytest（无需构建）；打包提交：
#   python build.py  →  submission.tar.gz（确定性：固定成员序/零时间戳）。
# 模块序（扁平命名空间的装载序，禁止乱序）：
#   constants → telemetry → observer → strategy → mission → solver
#   → executor → market → entry
# ===========================================================================
import os
import sys


def _find_root():
    """Locate the package root carrying src/.

    The official loader (kaggle_environments.get_last_callable) exec's the
    raw source with an empty env -- __file__ is NOT defined there -- but it
    appends the entry's directory to sys.path before exec; a normal import
    (tests, arena) has __file__.  Prefer __file__, fall back to the sys.path
    entry that actually carries src/constants.py.
    """
    if "__file__" in globals():
        here = os.path.dirname(os.path.abspath(__file__))
        if os.path.isfile(os.path.join(here, "src", "constants.py")):
            return here
    for entry in reversed(sys.path):
        if entry and os.path.isfile(os.path.join(entry, "src",
                                                 "constants.py")):
            return os.path.abspath(entry)
    raise RuntimeError("package root with src/constants.py not found "
                       "(neither __file__ nor sys.path carries it)")


_HERE = _find_root()
# P4.1（2026-09-19，线上零接合根因修复·腰带层）：官方 loader 是
# append(exec_dir) → exec → pop()（vendored agent.py get_last_callable）——
# 条件插入在"exec_dir 已在 sys.path"（官方绝对路径场景）时跳过，pop 之后
# 整个回合期包根不可导入，黎明钩子的 planner 导入必死。无条件插入把
# "包根全程可导入"变成结构性保证（主修复 = 下方 DTSP_RUNTIME_MODULE
# 装载期急切导入；本插入是冗余防线，见 tests/test_p41_engagement_gate.py）。
sys.path.insert(0, _HERE)

_MODULE_ORDER = ("constants", "telemetry", "observer", "strategy",
                 "mission", "solver", "executor", "market", "entry")

# ===========================================================================
# DTSP 运行时总闸（Track-B P3，2026-09-19）。提交形态 = DTSP 开启：src/entry
# 的黎明钩子只在本名字存在时唤醒 planner/runtime（每天黎明孪生规划选计划
# → PLANNER_OVERRIDES 注入当日执行）。键值语义见 planner/runtime._DEFAULTS。
# 旗关等价不受影响：本名字不在 src 九模块内——旗关黄金（裸命名空间 exec
# src，无本名字）与 PLANNER_ENABLED=False 路径照旧逐字节等价
# （scripts/planner_flagoff_golden.py / tests/test_planner_flagoff_equiv.py）。
# ===========================================================================
DTSP_RUNTIME_CONFIG = {
    "enabled": True,
    "seed": 1,                     # 孪生伪种子（线上真种子不可观测）
    "budget_cap_s": 0.85,          # 黎明规划硬帽（< actTimeout=1s）
    "rollout_models": ("pessimistic_fill",),   # P2.6 钉死搭档：悲观 0.75
    "ladder": ((6, 1), (4, 2), (3, 3), (2, 4), (1, 6)),
}


def _load_pipeline():
    """Load the src fragments straight into THIS module's globals.

    Executing into globals() (not a side dict) is load-bearing: the
    fragments' functions must resolve knob reads through the same dict the
    tests patch (`main.<KNOB> = ...`) -- a side namespace silently
    disconnects that contract.  Seeding the stdlib imports first mirrors
    the old builder's hoisted IMPORT_BLOCK (the fragments share one
    namespace and rely on copy/math/json/hashlib being present).
    """
    exec("; ".join(("import copy", "import math", "import json",
                    "import hashlib")), globals())
    for mod in _MODULE_ORDER:
        path = os.path.join(_HERE, "src", mod + ".py")
        with open(path, "r", encoding="utf-8") as handle:
            source = handle.read()
        exec(compile(source, path, "exec"), globals())


_load_pipeline()
del _MODULE_ORDER, _load_pipeline

# P4.1 主修复：装载期（loader 的 append 窗口内，包根必在 sys.path）急切
# 导入 planner 并存进本命名空间——entry 的黎明钩子优先消费本名字，不再
# 依赖回合期的 sys.path（官方 loader 在 exec 后已 pop 掉解包目录，v1 的
# 回合期 import 在线上每黎明 ModuleNotFoundError → 静默旗关 → 19 局动作
# 流与 v13.8 逐字节一致）。模块对象不可 callable，不影响
# get_last_callable 的"最后 callable"契约（agent 仍是最后定义的 callable）。
# 失败不致命化：置 None → 入口回退回合期导入 → 再失败走既有旗关降级。
try:
    import planner.runtime as DTSP_RUNTIME_MODULE
except Exception:                          # noqa: BLE001 —— 包破损降级旗关
    DTSP_RUNTIME_MODULE = None

_agent_impl = agent          # src/entry.py 的实现
del agent                    # 下方 def agent 重绑定为本文件最后 callable


def agent(obs):
    """Entry point: one action dict per turn (official Quick-Start
    signature; thin forwarder -- the pipeline lives in src/entry.py)."""
    return _agent_impl(obs)
