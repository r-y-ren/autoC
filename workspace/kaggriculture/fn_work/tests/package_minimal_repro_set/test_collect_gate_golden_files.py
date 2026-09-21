"""collect_gate_golden_files 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from package_minimal_repro_set.collect_gate_golden_files import collect_gate_golden_files


def test_collect_gate_golden_files_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:collect_gate_golden_files"):
        collect_gate_golden_files([])
