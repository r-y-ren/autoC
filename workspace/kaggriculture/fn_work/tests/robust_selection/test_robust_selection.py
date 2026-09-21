"""robust_selection 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from robust_selection.robust_selection import robust_selection


def test_robust_selection_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:robust_selection"):
        robust_selection({}, 0.0)
