"""migrate_snapshot_suite 真实测试：裁决结构键完整 + 绿门 + 真实目标迁移。

对齐 fn_docs/responsibility.md migrate_snapshot_suite 块主节核验命令
（fn_work/tests 全绿 + 两反例转常规通过，继承 R1/R2/R3）：
① 绿门裁决 dict 结构键完整（契约五键 + 类型）；
② 真实目标迁移（<战役根>/fn_work/tests/snapshot/，本批验收物）：全绿
   66=62 旧常规 + 4 反例转常规、R2/R3 反例全部常规 PASSED、零 xfail
   残留、其余冻结值逐字节不变（module 级只跑一次，~1min）；
③ 迁移面形状：conftest 双根装配零字面战役路径；非白名单件与源逐字节
   相等；R2/R3 文件重定向至 fn_work 实现；
④ fail-closed：源套件缺件 → ValueError（迁移前拒）。
"""

from pathlib import Path

import pytest

from migrate_snapshot_suite.migrate_snapshot_suite import (
    COUNTEREXAMPLE_TESTS,
    EXPECTED_PASSED,
    migrate_snapshot_suite,
)
from migrate_snapshot_suite.refresh_frozen_values import SUITE_FILES, UNTOUCHED_FILES
from shared.discover_campaign_roots import discover_campaign_roots

# 契约面五键（fn_docs 责任块：passed/xpassed/xfail 残留清单）
VERDICT_KEYS = {
    "overall", "passed", "xpassed_counterexamples",
    "xfail_residual", "migrated_files",
}


@pytest.fixture(scope="module")
def roots():
    return discover_campaign_roots(start_path=Path(__file__))


@pytest.fixture(scope="module")
def real_migration(roots):
    """真实目标迁移 + 绿门（本批验收物；整批覆写幂等，module 级一次）。"""
    source = roots["campaign_root"] / "snapshot_tests"
    target = roots["campaign_root"] / "fn_work" / "tests" / "snapshot"
    verdict = migrate_snapshot_suite(source, target)
    return verdict, source, target


def test_verdict_structure_keys_complete(real_migration):
    """① 裁决 dict 结构键完整与类型面。"""
    verdict, _source, _target = real_migration
    assert VERDICT_KEYS <= set(verdict)
    assert isinstance(verdict["overall"], bool)
    assert isinstance(verdict["passed"], int)
    assert isinstance(verdict["xpassed_counterexamples"], list)
    assert isinstance(verdict["xfail_residual"], list)
    assert sorted(verdict["migrated_files"]) == sorted(SUITE_FILES)
    assert "66 passed" in verdict["summary"]


def test_green_gate_on_real_target(real_migration):
    """② 绿门：全绿 + R2/R3 反例全部转常规通过 + 零 xfail 残留。"""
    verdict, _source, _target = real_migration
    assert verdict["overall"] is True, verdict
    assert verdict["passed"] == EXPECTED_PASSED == 66
    assert sorted(verdict["xpassed_counterexamples"]) == \
        sorted(COUNTEREXAMPLE_TESTS)
    assert verdict["xfail_residual"] == []
    assert verdict["failed"] == []
    assert verdict["returncode"] == 0


def test_frozen_values_byte_identical_off_whitelist(real_migration):
    """③a 逐字节不变：agent 整局旗关冻结/评级/契约/台账/README 与源相等
    （旗关整局 [59730.0, 59835.0] 等冻结值零改动）。"""
    verdict, source, target = real_migration
    assert verdict["frozen_values_unchanged"] is True
    for name in UNTOUCHED_FILES:
        assert (target / name).read_bytes() == (source / name).read_bytes()
    agent = (target / "test_agent_characterization.py") \
        .read_text(encoding="utf-8")
    assert "FROZEN_REWARDS = [59730.0, 59835.0]" in agent


def test_migration_redirect_shape(real_migration):
    """③b 重定向面：conftest 双根装配（discover_campaign_roots + 特征
    自举）零字面战役路径；R2/R3 文件指向 fn_work 实现、xfail 全数退役。"""
    _verdict, _source, target = real_migration
    conftest = (target / "conftest.py").read_text(encoding="utf-8")
    assert "discover_campaign_roots" in conftest
    assert "workspace/" not in conftest and "autoC" not in conftest
    planner = (target / "test_planner_select_characterization.py") \
        .read_text(encoding="utf-8")
    assert "from robust_selection.aggregate_scores import" in planner
    assert "from kaggle_simulations.agent.planner.select import" \
        not in planner
    r3 = (target / "test_counterexample_r3.py").read_text(encoding="utf-8")
    assert "from robust_selection.aggregate_scores import aggregate_scores" \
        in r3
    r2 = (target / "test_counterexample_r2.py").read_text(encoding="utf-8")
    assert "run_official_bench.rollout_with_replay_opponent import" in r2
    assert "import planner_offline_bench" not in r2
    # strict xfail 装饰器全数退役（文件头历史叙述可留档，装饰器不留）
    for name in ("test_counterexample_r2.py", "test_counterexample_r3.py"):
        assert "@pytest.mark.xfail" not in \
            (target / name).read_text(encoding="utf-8")


def test_migrate_rejects_missing_source_files(roots, tmp_path):
    """④ fail-closed：源套件缺件（九文件不齐）→ ValueError 拒迁。"""
    bad_source = tmp_path / "incomplete_suite"
    bad_source.mkdir()
    (bad_source / "conftest.py").write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="源套件缺件"):
        migrate_snapshot_suite(bad_source, tmp_path / "out")
