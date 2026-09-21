"""快照安全网迁移编排：复制九文件、修正 import 根（经 discover_campaign_roots）、跑绿门、出具迁移裁决（任一反例仍 xfail 即不通过）。

上游: R1（详见 fn_docs/responsibility.md）

实现要点（[改造]件，W1 收口）：
- 四步编排：①复制九文件自源套件（旧 snapshot_tests/ 只读，绝不回写）；
  ②重写迁移版 conftest（双根装配：fn_work/src 供 R2/R3 重定向后的
  select/bench 实现，旧树 software/+scripts/ 供其余测试面与 twin/v143
  参照——B13 前 fn_work agent 不存在，安全网始终测各件当前真值实现；
  根定位经 shared.discover_campaign_roots，R20：零字面战役路径）；
  ③refresh_frozen_values 按 R2/R3 影响清单刷新冻结值（strict xfail 转常
  规+双口径注记，白名单外零字节改动）；④子进程跑绿门并出具裁决。
- 绿门 = 迁移套件 -v 全绿（退出码 0、零 FAILED/ERROR/XFAIL/XPASS）
  且 R2/R3 四条反例全部以常规 PASSED 在场 且 逐字节不变复核通过
  （非白名单五件与源逐字节相等 + 白名单内受保护冻结字面量在场）。
- 裁决 dict：{overall, passed, xpassed_counterexamples, xfail_residual,
  migrated_files, failed, frozen_values_unchanged, summary, returncode}——
  前五键为契约面（fn_docs 意图：passed/xpassed/xfail 残留清单）。
- 幂等：每次自源全新复制再刷新（目标已存在即整批覆写九件），锚文本在
  源副本上必唯一命中；旧套件 62P+4xf 口径不受影响（源只读）。
- 纪律：不 import 旧树 scripts/；路径全程序化发现；无网络。
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

from migrate_snapshot_suite.refresh_frozen_values import (
    DEFAULT_IMPACT_LIST,
    SUITE_FILES,
    UNTOUCHED_FILES,
    check_protected_anchors,
    refresh_frozen_values,
)
from shared.discover_campaign_roots import discover_campaign_roots

__all__ = ["migrate_snapshot_suite", "COUNTEREXAMPLE_TESTS",
           "GREEN_GATE_TIMEOUT_S"]

# R2/R3 快照反例（迁移后必须以常规 PASSED 在场的四条；绿门核心判据）
COUNTEREXAMPLE_TESTS = (
    "test_counterexample_r2.py::test_bench_rollout_injects_into_actual_seat",
    "test_counterexample_r3.py::test_value_order_trimmed_mean_case_a",
    "test_counterexample_r3.py::test_value_order_trimmed_mean_case_b_"
    "pessimistic_restored",
    "test_counterexample_r3.py::test_pessimistic_score_moves_aggregate_"
    "under_value_order",
)

GREEN_GATE_TIMEOUT_S = 600

# 迁移套件期望规模：旧口径 62 常规通过 + 4 反例转常规 = 66 全绿零残留
EXPECTED_PASSED = 66

# 迁移版 conftest（双根装配；写入目标后即接管该套件的一切 sys.path 语义）
MIGRATED_CONFTEST = '''# conftest.py —— 迁移后快照安全网套件的路径装配（migrate_snapshot_suite 产物）
#
# 双根装配（W1 收口语义，2026-09-21）：
#   * fn_work/src —— R2/R3 重定向后的 select/bench 实现
#     （robust_selection / run_official_bench）；
#   * 旧树 software/ 与 software/scripts/ —— 其余测试面（agent 整局旗关
#     冻结、评级、契约、台账）与 twin / v143 参照继续指向旧树当前真值
#     （B13 前 fn_work agent 不存在，安全网始终测各件当前真值实现）。
# 根定位零字面战役路径（R20）：先按目录特征（blueprint.md+software+
# fn_docs 齐备者=战役根）自本文件上溯自举 fn_work/src——shared 包在
# fn_work/src 内，自举前不可 import，故特征组在此本地复刻一份——再经
# shared.discover_campaign_roots 统一定位旧树 software 根。
# 套件须位于 <战役根>/fn_work/tests/snapshot/（迁移产物树内）；孤立副本
# （无战役根上溯可达）fail-closed 拒跑——无旧树/fn_work 可指即无真值。
# 旧代码全树只读：本套件不写入 software/ 任何文件（运行期副作用仅
# __pycache__ 与 twin 引擎缓存目录，均 gitignored，与旧套件一致）。

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent          # <战役根>/fn_work/tests/snapshot

_CAMPAIGN_FEATURES = ("blueprint.md", "software", "fn_docs")
_CAMPAIGN_ROOT = None
for _cand in (_HERE, *_HERE.parents):
    if all((_cand / _f).exists() for _f in _CAMPAIGN_FEATURES):
        _CAMPAIGN_ROOT = _cand
        break
if _CAMPAIGN_ROOT is None:
    raise RuntimeError(
        "迁移套件 conftest 未找到战役根（特征=" + "+".join(_CAMPAIGN_FEATURES)
        + "）：套件须位于 <战役根>/fn_work/tests/snapshot/（迁移产物树内），"
        "孤立副本无旧树与 fn_work 实现可指，fail-closed 拒跑。")

_FNWORK_SRC = _CAMPAIGN_ROOT / "fn_work" / "src"
if str(_FNWORK_SRC) not in sys.path:
    sys.path.insert(0, str(_FNWORK_SRC))

from shared.discover_campaign_roots import discover_campaign_roots  # noqa: E402

_ROOTS = discover_campaign_roots(start_path=_HERE)
_SOFTWARE = _ROOTS["software_root"]              # <战役根>/software（旧树，只读）
_SCRIPTS = _SOFTWARE / "scripts"

for _p in (_SCRIPTS, _SOFTWARE):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
'''

_OUTCOME_RE = re.compile(
    r"^(?P<nodeid>\S+::\S+)[ \t]+(?P<outcome>PASSED|FAILED|ERROR|SKIPPED"
    r"|XFAIL|XPASS)\b", re.MULTILINE)


def _parse_outcomes(stdout: str) -> dict:
    """解析 pytest -v 输出为 {nodeid: outcome}（后见覆盖先见，值恒一致）。"""
    outcomes = {}
    for match in _OUTCOME_RE.finditer(stdout):
        outcomes[match.group("nodeid")] = match.group("outcome")
    return outcomes


def _summary_line(stdout: str) -> str:
    for line in reversed(stdout.splitlines()):
        stripped = line.strip().strip("=").strip()
        if stripped and ("passed" in stripped or "failed" in stripped
                         or "error" in stripped):
            return stripped
    return ""


def _nodeid_rel(nodeid: str) -> str:
    """绝对/相对 nodeid → "文件名::测试名"（跨 rootdir 形态归一）。"""
    head, _, tail = nodeid.partition("::")
    return f"{Path(head).name}::{tail}"


def migrate_snapshot_suite(source_suite, target) -> dict:
    """把快照安全网套件迁移入 fn_work 并跑绿门，出具迁移裁决。

    Args:
        source_suite: 源套件目录（<战役根>/snapshot_tests，九文件齐备，
            只读——迁移绝不回写源件）。
        target: 目标目录（<战役根>/fn_work/tests/snapshot；不存在即创建，
            已存在则九件整批覆写，幂等）。

    Returns:
        裁决 dict（契约五键 + 诊断扩展键）：
        {overall: bool, passed: int, xpassed_counterexamples: [nodeid…],
         xfail_residual: [nodeid…], migrated_files: [文件名…],
         failed: [nodeid…], frozen_values_unchanged: bool,
         summary: str, returncode: int}
        overall=True ⇔ 全绿 + 四条 R2/R3 反例全部常规 PASSED + 零
        XFAIL/XPASS 残留 + 冻结值逐字节不变复核通过。

    Raises:
        ValueError: 源套件缺件 / refresh 影响面校验失败（含锚未命中）。
    """
    source = Path(source_suite)
    target_dir = Path(target)

    # ---- ① 源校验 + 复制九文件（源只读）----
    missing = [name for name in SUITE_FILES
               if not (source / name).is_file()]
    if missing:
        raise ValueError(f"源套件缺件（快照安全网须九文件齐备）: {missing}"
                         f"——源={source}")
    target_dir.mkdir(parents=True, exist_ok=True)
    for name in SUITE_FILES:
        shutil.copyfile(source / name, target_dir / name)

    # ---- ② 重写迁移版 conftest（双根装配）----
    (target_dir / "conftest.py").write_text(
        MIGRATED_CONFTEST, encoding="utf-8", newline="")

    # ---- ③ 冻结值刷新（strict xfail 转常规 + 双口径注记，白名单圈禁）----
    _changed, _annotations = refresh_frozen_values(
        DEFAULT_IMPACT_LIST, target_dir)

    # ---- ④ 冻结值逐字节不变复核 ----
    frozen_ok = True
    for name in UNTOUCHED_FILES:
        if (target_dir / name).read_bytes() != \
                (source / name).read_bytes():
            frozen_ok = False
    if check_protected_anchors(target_dir):
        frozen_ok = False

    # ---- ⑤ 绿门：子进程跑迁移套件（conftest 自足，与进程 CWD 无关）----
    cmd = [sys.executable, "-m", "pytest", str(target_dir),
           "-v", "--tb=short", "-p", "no:cacheprovider"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=GREEN_GATE_TIMEOUT_S)
        stdout, returncode = proc.stdout, proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = (exc.stdout or b"").decode("utf-8", "replace") \
            if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        returncode = -1

    outcomes = _parse_outcomes(stdout)
    rel = {_nodeid_rel(k): v for k, v in outcomes.items()}
    passed_count = sum(1 for v in outcomes.values() if v == "PASSED")
    failed = sorted(k for k, v in outcomes.items() if v == "FAILED")
    xfail_residual = sorted(k for k, v in outcomes.items()
                            if v in ("XFAIL", "XPASS"))
    xpassed_counterexamples = sorted(
        rel_id for rel_id, v in rel.items()
        if rel_id in COUNTEREXAMPLE_TESTS and v == "PASSED")

    overall = (
        returncode == 0
        and not failed
        and passed_count == EXPECTED_PASSED
        and not xfail_residual
        and len(xpassed_counterexamples) == len(COUNTEREXAMPLE_TESTS)
        and frozen_ok
    )
    return {
        "overall": overall,
        "passed": passed_count,
        "xpassed_counterexamples": xpassed_counterexamples,
        "xfail_residual": [f"{k} ({rel[k]})" for k in xfail_residual],
        "migrated_files": sorted(SUITE_FILES),
        "failed": failed,
        "frozen_values_unchanged": frozen_ok,
        "summary": _summary_line(stdout),
        "returncode": returncode,
    }
