"""refresh_frozen_values 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from migrate_snapshot_suite.refresh_frozen_values import refresh_frozen_values


def test_refresh_frozen_values_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:refresh_frozen_values"):
        refresh_frozen_values([])
