"""package_minimal_repro_set 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from package_minimal_repro_set.package_minimal_repro_set import package_minimal_repro_set


def test_package_minimal_repro_set_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:package_minimal_repro_set"):
        package_minimal_repro_set({}, {})
