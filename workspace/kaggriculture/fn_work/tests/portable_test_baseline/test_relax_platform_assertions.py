"""relax_platform_assertions 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from portable_test_baseline.relax_platform_assertions import relax_platform_assertions


def test_relax_platform_assertions_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:relax_platform_assertions"):
        relax_platform_assertions(None)
