"""migrate_snapshot_suite 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from migrate_snapshot_suite.migrate_snapshot_suite import migrate_snapshot_suite


def test_migrate_snapshot_suite_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:migrate_snapshot_suite"):
        migrate_snapshot_suite(None, None)
