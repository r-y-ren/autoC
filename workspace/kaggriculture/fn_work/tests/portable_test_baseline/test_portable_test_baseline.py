"""portable_test_baseline 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from portable_test_baseline.portable_test_baseline import portable_test_baseline


def test_portable_test_baseline_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:portable_test_baseline"):
        portable_test_baseline()
