# conftest.py —— 快照安全网套件的路径装配（fn-ladder 阶段四）
#
# 与旧 software/tests/conftest.py 同一做法：把旧树 software 根插进
# sys.path（kgenv / kaggle_simulations 可导入）；另外把 scripts/ 也插进去——
# 席位错位反例（test_counterexample_r2.py）需要直接 import
# planner_offline_bench 与 v143_sellrace_gates 两个模块。
# 旧树根定位（2026-09-23 大整合后）：自本文件上溯按目录特征发现战役根
# （新布局=fn_docs+fn_work 齐备或旧布局 blueprint.md+software+fn_docs 齐备），
# software 锚=战役根/software（旧）或 fn_work/legacy_software（新），fail-closed。
# 旧代码全树只读：本套件不写入旧树任何文件（运行期副作用仅
# __pycache__ 与 twin 引擎缓存目录 exports/probes/twin_fidelity/
# engine_cache/，均为 gitignored 运行时缓存，与既有测试套件一致）。

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))

_CAMPAIGN_FEATURES = ("fn_docs", "fn_work")
_CAMPAIGN_FEATURES_LEGACY = ("blueprint.md", "software", "fn_docs")
_SOFTWARE = None
_candidate = _HERE
while True:
    _new = all(os.path.exists(os.path.join(_candidate, _f))
               for _f in _CAMPAIGN_FEATURES)
    _legacy = all(os.path.exists(os.path.join(_candidate, _f))
                  for _f in _CAMPAIGN_FEATURES_LEGACY)
    if _new or _legacy:
        _sw = os.path.join(_candidate, "software")
        _SOFTWARE = _sw if os.path.isdir(_sw) else os.path.join(
            _candidate, "fn_work", "legacy_software")
        break
    _parent = os.path.dirname(_candidate)
    if _parent == _candidate:
        break
    _candidate = _parent
if _SOFTWARE is None:
    raise RuntimeError(
        "快照套件 conftest 未找到战役根（特征=" + "+".join(_CAMPAIGN_FEATURES)
        + " 或 " + "+".join(_CAMPAIGN_FEATURES_LEGACY) + "）：套件须位于 "
        "<战役根>/snapshot_tests/，孤立副本无旧树可指，fail-closed 拒跑。")

_SCRIPTS = os.path.join(_SOFTWARE, "scripts")

for _p in (_SCRIPTS, _SOFTWARE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
