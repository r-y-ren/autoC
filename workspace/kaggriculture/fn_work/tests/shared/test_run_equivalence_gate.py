"""run_equivalence_gate 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from shared.run_equivalence_gate import run_equivalence_gate


def test_run_equivalence_gate_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:run_equivalence_gate"):
        run_equivalence_gate(None)
