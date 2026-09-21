"""迁移登记——run_submission_agent · 顶层入口（B13，fn-implement，2026-09-21）

源文件: software/kaggle_simulations/agent/main.py（旧树冻结，零字节变更）
源 sha256: f1f46638b8b747b46282065f5e37f584a42d5f155a7b428b16d7be7625d185f7
剥离清单（R10 死码不迁）: 1 项——_SELLRACE_SHIP 死支（随装载器 load_agent_
  modules 一并不迁，登记见该件文件头）。
形态: 官方装载语义下的单回合入口（agent_load_path 式可装载形态）——本文件经
  路径装载（importlib / kgenv.load_submission_agent / 官方 get_last_callable
  的 exec 窗）时，module 级先系 sys.path 腰带（P4.1：装载窗先行、无条件插入
  ——包根+fn_work/src，与旧 main 的 _HERE 腰带同构），再调 load_agent_modules
  把十件+planner 通道 exec 进**本模块 globals**（=旧 main._load_pipeline 的
  exec into globals() 语义：入口 agent 的 __globals__ 即共享命名空间——按
  agent.__globals__["DTSP_RUNTIME_CONFIG"]/["PLANNER_ENABLED"]/["DTSP_RUNTIME_
  MODULE"] 直接访问的契约面保持）。装载器尾部已把 entry 的 agent 重绑为
  _agent_impl 并 exec 重定义薄前递 agent——该 def 是本命名空间最后定义的
  callable（官方 get_last_callable 契约；模块对象不可 callable 不受影响）。
行为契约: obs→观察旁路→黎明 DTSP 钩子→宏计划→任务→四层求解→市场→雇工→
  排序→预算截断；整体 try/except → 合法 PASS（fail-open 第一道，永不崩）；
  与现役行为逐字节等价（判据=run_equivalence_gate 全 pass + 双目标旗关冻结）。
上游: R1, R10（fn_docs/responsibility.md 功能块 run_submission_agent）
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))

# sys.path 腰带（P4.1，装载窗内先行）：包根（load_agent_modules 的名字导入面）
# + fn_work/src（select 提供者 robust_selection 的导入面）。装载器内还会
# 无条件重插（双保险，语义同旧 main 的无条件 insert）。
for _belt in (_HERE, os.path.abspath(os.path.join(_HERE, "..", ".."))):
    if _belt not in sys.path:
        sys.path.insert(0, _belt)

from load_agent_modules import load_agent_modules  # noqa: E402

# 十件+planner 通道 exec 进本模块 globals；装载器尾段重绑 agent=最后 callable
# （entry 实现存 _agent_impl；下方无再定义——agent 即装载器 exec 铸的薄前递，
# __globals__=本模块 globals=共享命名空间）。
load_agent_modules(_HERE, ns=globals())
