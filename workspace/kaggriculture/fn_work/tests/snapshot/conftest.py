# conftest.py —— 迁移后快照安全网套件的路径装配（migrate_snapshot_suite 产物）
#
# 双根装配（W1 收口语义，2026-09-21）：
#   * fn_work/src —— R2/R3 重定向后的 select/bench 实现
#     （robust_selection / run_official_bench）；
#   * 旧树 software/ 与 software/scripts/ —— 其余测试面（agent 整局旗关
#     冻结、评级、契约、台账）与 twin / v143 参照继续指向旧树当前真值
#     （B13 前 fn_work agent 不存在，安全网始终测各件当前真值实现）。
# 根定位零字面战役路径（R20）：先按目录特征（新布局 fn_docs+fn_work 齐备
# 或旧布局 blueprint.md+software+fn_docs 齐备者=战役根）自本文件上溯自举
# fn_work/src——shared 包在 fn_work/src 内，自举前不可 import，故特征组在
# 此本地复刻一份——再经 shared.discover_campaign_roots 统一定位旧树
# software 根（新布局=fn_work/legacy_software）。
# 套件须位于 <战役根>/fn_work/tests/snapshot/（迁移产物树内）；孤立副本
# （无战役根上溯可达）fail-closed 拒跑——无旧树/fn_work 可指即无真值。
# 旧代码全树只读：本套件不写入旧树任何文件（运行期副作用仅
# __pycache__ 与 twin 引擎缓存目录，均 gitignored，与旧套件一致）。

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent          # <战役根>/fn_work/tests/snapshot

# 战役根特征（本地复刻，自举前不可 import shared）：新布局=fn_docs+fn_work
# 两件齐备（2026-09-23 大整合后唯一形态）；兼容旧布局 blueprint.md+software+
# fn_docs。software 锚=战役根/software（旧）或 fn_work/legacy_software（新）。
_CAMPAIGN_FEATURES = ("fn_docs", "fn_work")
_CAMPAIGN_FEATURES_LEGACY = ("blueprint.md", "software", "fn_docs")
_CAMPAIGN_ROOT = None
for _cand in (_HERE, *_HERE.parents):
    _new = all((_cand / _f).exists() for _f in _CAMPAIGN_FEATURES)
    _legacy = all((_cand / _f).exists() for _f in _CAMPAIGN_FEATURES_LEGACY)
    if _new or _legacy:
        _CAMPAIGN_ROOT = _cand
        break
if _CAMPAIGN_ROOT is None:
    raise RuntimeError(
        "迁移套件 conftest 未找到战役根（特征=" + "+".join(_CAMPAIGN_FEATURES)
        + " 或 " + "+".join(_CAMPAIGN_FEATURES_LEGACY) + "）：套件须位于 "
        "<战役根>/fn_work/tests/snapshot/（迁移产物树内），孤立副本无旧树"
        "与 fn_work 实现可指，fail-closed 拒跑。")

_FNWORK_SRC = _CAMPAIGN_ROOT / "fn_work" / "src"
if str(_FNWORK_SRC) not in sys.path:
    sys.path.insert(0, str(_FNWORK_SRC))

from shared.discover_campaign_roots import discover_campaign_roots  # noqa: E402

_ROOTS = discover_campaign_roots(start_path=_HERE)
_SOFTWARE = _ROOTS["software_root"]              # 旧树根（software/ 或 fn_work/legacy_software，只读）
_SCRIPTS = _SOFTWARE / "scripts"

for _p in (_SCRIPTS, _SOFTWARE):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
