"""迁移登记——run_submission_agent · load_agent_modules（B13，fn-implement，2026-09-21）

源文件: software/kaggle_simulations/agent/main.py（旧树冻结，零字节变更）
源 sha256: f1f46638b8b747b46282065f5e37f584a42d5f155a7b428b16d7be7625d185f7
剥离清单（R10 死码不迁）: 1 项——_SELLRACE_SHIP 死支（v14.3 发射开关，恒
  False=发射态门禁裁决位；置 True 的发射语义随 R10"死支不迁"整支不迁移，
  发射须协调者裁决后另行接线）。
形态: 薄装载器——本文件不是旧模块的逐字副本，而是 main.py 装载语义（_find_root
  腰带 / DTSP_RUNTIME_CONFIG / _MODULE_ORDER+_load_pipeline / 急切导入 / 尾部
  重绑五段）在 fn_work exec 链布局下的等形重写。装载序真值（旧 main.py 逐字）：
    _MODULE_ORDER = ("constants", "telemetry", "observer", "strategy",
                     "mission", "solver", "executor", "market", "wave", "entry")
  十名按 _CHAIN_FILES 映射到迁移件（constants/wave/entry 落 _exec_chain/ 基座
  位，telemetry/market 用函数件名，observer/strategy/mission/solver/executor 为
  B12 已迁五件）。planner 通道（P4.1 红线：装载窗内急切铸就，回合期零导入）：
  旧 `import planner.runtime as DTSP_RUNTIME_MODULE` → 新按 exec 链装载——
  _exec_chain/planner/ 四件各铸模块对象 + fn_work/src/robust_selection/ 三件
  合成 select 提供者（R3 值序修复版流入新链，robust_select=调用面别名）注入
  run_dawn_planner 命名空间后 exec 本件，铸成 DTSP_RUNTIME_MODULE。每次调用
  新铸一套 planner 运行态（旧树 sys.modules 缓存使多 agent 共享 planner.runtime
  的 per-player 键控状态；新链按装载隔离——键面同构，行为等价，登记此差异）。
  DTSP_RUNTIME_CONFIG 每次装载新铸 dict（旧 main 逐次 exec 字面量语义——测试
  按装载实例独立关旗的契约面保持）。
sys.path 腰带（P4.1 结构性保证）：无条件插入包根（本件目录，名字导入面）与
  fn_work/src（select 提供者 robust_selection 的导入面）。
上游: R1, R10（fn_docs/responsibility.md 功能块 run_submission_agent · load_agent_modules）
"""

import os
import sys
import types

__all__ = ["load_agent_modules", "DTSP_RUNTIME_CONFIG"]

_PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
_FNWORK_SRC = os.path.abspath(os.path.join(_PACKAGE_ROOT, ".."))

# 装载序真值（旧 main.py _MODULE_ORDER 逐字；fn_work 件名映射，序不变）。
_MODULE_ORDER = ("constants", "telemetry", "observer", "strategy",
                 "mission", "solver", "executor", "market", "wave", "entry")
_CHAIN_FILES = {
    "constants": "_exec_chain/constants.py",
    "telemetry": "record_shadow_telemetry.py",
    "observer": "observe_opponent_state.py",
    "strategy": "decide_macro_mode.py",
    "mission": "build_mission_pack.py",
    "solver": "solve_worker_routes.py",
    "executor": "execute_along_route.py",
    "market": "plan_market_orders.py",
    "wave": "_exec_chain/wave.py",
    "entry": "_exec_chain/entry.py",
}
# planner 通道件（旧 planner/ 包内相对导入 → exec 链模块对象注入；绑定名=旧
# runtime.py `from . import X as _X` 的 _X 名）。select 提供者另行合成。
_PLANNER_FILES = (
    ("_twin", "_exec_chain/planner/twin.py"),
    ("_plans", "_exec_chain/planner/plans.py"),
    ("_opponents", "_exec_chain/planner/opponents.py"),
    ("_wave", "_exec_chain/planner/wave_script.py"),
)
# select 提供者源（fn_work/src/robust_selection/ 三件，exec 进同一命名空间；
# 依赖序：叶子两件先行，主流程件随后——其内部绝对导入经腰带解析到同源模块）。
_SELECT_PROVIDER_FILES = ("robust_selection/aggregate_scores.py",
                          "robust_selection/break_ties_by_identity.py",
                          "robust_selection/robust_selection.py")

# 旧 main.py DTSP_RUNTIME_CONFIG 字面量逐字（键值语义见 planner/runtime._DEFAULTS）。
DTSP_RUNTIME_CONFIG = {
    "enabled": True,
    "seed": 1,                     # 孪生伪种子（线上真种子不可观测）
    "budget_cap_s": 0.85,          # 黎明规划硬帽（< actTimeout=1s）
    "rollout_models": ("pessimistic_fill",),   # P2.6 钉死搭档：悲观 0.75
    "ladder": ((6, 1), (4, 2), (3, 3), (2, 4), (1, 6)),
}

# 旧 main._load_pipeline 的种子 imports（十件共享一个命名空间，依赖
# copy/math/json/hashlib 在场——hoisted IMPORT_BLOCK 的等形）。
_SEED_IMPORTS = "; ".join(("import copy", "import math", "import json",
                           "import hashlib"))


def _read(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def _exec_into(ns, path):
    exec(compile(_read(path), path, "exec"), ns)


def _exec_module(module_name, path):
    """按路径 exec 铸模块对象（__file__ 实测路径播种——路径锚语义保持）。"""
    module = types.ModuleType(module_name)
    module.__file__ = path
    _exec_into(vars(module), path)
    return module


def _belt(package_root):
    """P4.1 腰带：无条件插入（旧 main 对包根的结构性保证；新链另含 fn_work/src
    ——select 提供者内部绝对导入的解析面）。幂等。"""
    for path in (package_root,
                 os.path.abspath(os.path.join(package_root, ".."))):
        if path not in sys.path:
            sys.path.insert(0, path)


def _build_select_provider(fnwork_src):
    """select 提供者：robust_selection 三件源码 exec 进同一模块命名空间。

    R3 值序修复版流入新链（旧 planner/select.py 名字序裁切缺陷不迁）；
    robust_select=robust_selection 的调用面别名（旧 runtime 调用点逐字不变），
    DEFAULT_TRIM_FRACTION/IDENTITY_TIEBREAK_TAU/aggregate_scores 随源在场。
    """
    module = types.ModuleType("run_submission_agent._exec_chain.select")
    module.__file__ = os.path.join(fnwork_src, "robust_selection",
                                   "robust_selection.py")
    for rel in _SELECT_PROVIDER_FILES:
        _exec_into(vars(module), os.path.join(fnwork_src, rel))
    module.robust_select = module.robust_selection
    return module


def _build_planner_runtime(package_root, fnwork_src):
    """planner 通道急切装载（P4.1 红线：装载窗内完成，无回合期导入）。

    铸 run_dawn_planner 模块对象（__file__=本包实测路径——agent_dir/
    resolve_engine 的路径锚），先注入 _twin/_plans/_opponents/_wave/_select
    五名（旧相对导入的 exec 链等形），再 exec 其源码。
    """
    module = types.ModuleType("run_submission_agent.run_dawn_planner")
    module.__file__ = os.path.join(package_root, "run_dawn_planner.py")
    ns = vars(module)
    for bind, rel in _PLANNER_FILES:
        ns[bind] = _exec_module(
            f"run_submission_agent._exec_chain.planner.{bind.lstrip('_')}",
            os.path.join(package_root, rel))
    ns["_select"] = _build_select_provider(fnwork_src)
    _exec_into(ns, module.__file__)
    return module


def load_agent_modules(package_root=None, ns=None):
    """按旧 main.py 装载语义 exec 十件+planner 通道进共享命名空间。

    Args:
        package_root: 包根目录（默认=本件所在目录）。缺件 fail-closed 抛
            RuntimeError（build precheck 同步收口的模块缺失面）。
        ns: 目标命名空间（默认新铸 dict）。传 globals() 时入口 agent 的
            __globals__ 即共享命名空间（旧 main._load_pipeline 的 exec into
            globals() 契约面——测试按 agent.__globals__[...] 直接访问保持）。

    Returns:
        (ns, agent)——agent 为重绑后的最后 callable（薄前递，__globals__=ns；
        官方 get_last_callable 契约位；entry 实现存 ns["_agent_impl"]）。
    """
    root = os.path.abspath(package_root if package_root is not None
                           else _PACKAGE_ROOT)
    missing = [name for name in _MODULE_ORDER
               if not os.path.isfile(os.path.join(root, _CHAIN_FILES[name]))]
    missing += [rel for _bind, rel in _PLANNER_FILES
                if not os.path.isfile(os.path.join(root, rel))]
    if not os.path.isfile(os.path.join(root, "run_dawn_planner.py")):
        missing.append("run_dawn_planner.py")
    if missing:
        raise RuntimeError(f"装载缺件（fail-closed）: {missing} @ {root}")
    _belt(root)
    if ns is None:
        ns = {}
    # 种子 imports → DTSP_RUNTIME_CONFIG（每次装载新铸 dict）→ 十件按序 exec。
    exec(_SEED_IMPORTS, ns)
    ns["DTSP_RUNTIME_CONFIG"] = dict(DTSP_RUNTIME_CONFIG)
    for name in _MODULE_ORDER:
        _exec_into(ns, os.path.join(root, _CHAIN_FILES[name]))
    # planner 通道（装载窗内急切铸就；entry 钩子优先消费，回合期导入回退不可达）。
    ns["DTSP_RUNTIME_MODULE"] = _build_planner_runtime(
        root, os.path.abspath(os.path.join(root, "..")))
    # 尾部重绑（旧 main 尾段等形）：entry 的 agent → _agent_impl，重定义薄前递
    # 为命名空间最后 callable（exec 定义使 __globals__=ns——旗关面按
    # agent.__globals__["DTSP_RUNTIME_CONFIG"] 操作的契约保持）。
    ns["_agent_impl"] = ns["agent"]
    del ns["agent"]
    exec("def agent(obs):\n"
         "    \"\"\"Entry point: one action dict per turn (official Quick-Start\n"
         "    signature; thin forwarder -- the pipeline lives in the exec chain).\"\"\"\n"
         "    return _agent_impl(obs)\n", ns)
    return ns, ns["agent"]
