"""run_equivalence_gate 单测。

覆盖契约（fn_docs/responsibility.md 共享函数节 + R1）：
①对旧树默认判据=pass（快照 62P+4xf 冻结口径，真实 subprocess 复跑快照套件，~37s）；
②gate_options 启用未知判据名 → fail-closed（不静默忽略；顺带覆盖默认判据显式 skip 路径）；
③裁决结构键完整（overall/criteria/逐项 name-status-detail-values/溯源字段）。
测试自身零字面战役路径（R20：三根经 discover_campaign_roots 发现，自举同 conftest 约定）。
"""

from pathlib import Path
import sys

# 防御性自举：仓外 CWD + 绝对路径调用时 pytest rootdir 推断会截掉 fn_work/tests/conftest.py
# （confcutdir），此处按 __file__ 程序化补 src 入 sys.path（幂等；R20：不写字面战役路径）。
_SRC_DIR = Path(__file__).resolve().parents[2] / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

import pytest

from shared.discover_campaign_roots import discover_campaign_roots
from shared.run_equivalence_gate import run_equivalence_gate

ROOTS = discover_campaign_roots()
# W1 旧树冻结口径（R1：快照 62P+4xf）——期望值属契约数字，非战役路径
SNAPSHOT_BASELINE = {"passed": 62, "xfailed": 4}


@pytest.fixture(scope="module")
def old_tree_verdict():
    """对旧树全量跑一次门（真实 subprocess 复跑快照套件，~37s），①③共用不重复计费。"""
    return run_equivalence_gate(ROOTS["software_root"])


def test_default_gate_passes_on_old_tree(old_tree_verdict):
    verdict = old_tree_verdict
    assert verdict["overall"] == "pass"
    snap = next(c for c in verdict["criteria"] if c["name"] == "snapshot_suite")
    assert snap["status"] == "pass"
    for key, want in SNAPSHOT_BASELINE.items():
        assert snap["values"][key] == want, f"{key} 偏离冻结口径"
    for key in ("failed", "xpassed", "errors"):
        assert snap["values"][key] == 0
    # 可选判据未启用 → skip（detail 即原因），不计入整体失败
    flagoff = next(c for c in verdict["criteria"] if c["name"] == "flagoff_golden")
    assert flagoff["status"] == "skip"
    assert flagoff["detail"]


def test_unknown_criterion_fail_closed():
    # 显式关闭默认判据以免复跑 37s 套件；fail-closed 面只验"未知判据名必须 fail"
    verdict = run_equivalence_gate(
        ROOTS["software_root"],
        gate_options={"no_such_criterion": True,
                      "snapshot_suite": {"enabled": False}},
    )
    assert verdict["overall"] == "fail"
    unknown = [c for c in verdict["criteria"] if c["name"] == "no_such_criterion"]
    assert len(unknown) == 1
    assert unknown[0]["status"] == "fail"
    assert unknown[0]["detail"]
    # 关闭侧对照：已知判据显式关闭 → skip+原因（可关可跳，未知必 fail）
    snap = next(c for c in verdict["criteria"] if c["name"] == "snapshot_suite")
    assert snap["status"] == "skip"
    assert snap["detail"]


def test_verdict_structure_keys_complete(old_tree_verdict):
    verdict = old_tree_verdict
    assert set(verdict) == {"overall", "criteria", "agent_load_path", "campaign_root"}
    assert verdict["overall"] in ("pass", "fail")
    assert verdict["criteria"] and isinstance(verdict["criteria"], list)
    for criterion in verdict["criteria"]:
        assert set(criterion) == {"name", "status", "detail", "values"}
        assert isinstance(criterion["name"], str) and criterion["name"]
        assert criterion["status"] in ("pass", "fail", "skip")
        assert isinstance(criterion["detail"], str)
        assert isinstance(criterion["values"], dict)
    # 溯源字段：目标 agent 装载路径与战役根均经 R20 发现（非字面路径）
    assert verdict["agent_load_path"] == str(ROOTS["software_root"])
    assert verdict["campaign_root"] == str(ROOTS["campaign_root"])
