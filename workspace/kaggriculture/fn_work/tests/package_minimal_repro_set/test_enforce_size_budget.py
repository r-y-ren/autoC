"""enforce_size_budget 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from package_minimal_repro_set.enforce_size_budget import enforce_size_budget


def test_enforce_size_budget_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:enforce_size_budget"):
        enforce_size_budget([], {})
