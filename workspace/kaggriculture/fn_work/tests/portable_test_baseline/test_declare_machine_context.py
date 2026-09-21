"""declare_machine_context 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from portable_test_baseline.declare_machine_context import declare_machine_context


def test_declare_machine_context_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:declare_machine_context"):
        declare_machine_context(None)
