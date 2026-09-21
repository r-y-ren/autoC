# conftest.py —— 快照安全网套件的路径装配（fn-ladder 阶段四）
#
# 与 software/tests/conftest.py 同一做法：把 software/ 根插进 sys.path
# （kgenv / kaggle_simulations 可导入）；另外把 scripts/ 也插进去——
# 席位错位反例（test_counterexample_r2.py）需要直接 import
# planner_offline_bench 与 v143_sellrace_gates 两个模块。
# 旧代码全树只读：本套件不写入 software/ 任何文件（运行期副作用仅
# __pycache__ 与 twin 引擎缓存目录 exports/probes/twin_fidelity/
# engine_cache/，均为 gitignored 运行时缓存，与既有测试套件一致）。

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SOFTWARE = os.path.join(_HERE, "..", "software")
_SOFTWARE = os.path.abspath(_SOFTWARE)
_SCRIPTS = os.path.join(_SOFTWARE, "scripts")

for _p in (_SCRIPTS, _SOFTWARE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
