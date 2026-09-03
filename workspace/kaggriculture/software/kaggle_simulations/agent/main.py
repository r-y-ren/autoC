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
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

_MODULE_ORDER = ("constants", "telemetry", "observer", "strategy",
                 "mission", "solver", "executor", "market", "entry")


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
_agent_impl = agent          # src/entry.py 的实现
del agent                    # 下方 def agent 重绑定为本文件最后 callable


def agent(obs):
    """Entry point: one action dict per turn (official Quick-Start
    signature; thin forwarder -- the pipeline lives in src/entry.py)."""
    return _agent_impl(obs)
