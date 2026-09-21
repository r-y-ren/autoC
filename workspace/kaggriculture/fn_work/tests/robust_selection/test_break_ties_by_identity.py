"""break_ties_by_identity 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from robust_selection.break_ties_by_identity import break_ties_by_identity


def test_break_ties_by_identity_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:break_ties_by_identity"):
        break_ties_by_identity({}, {})
