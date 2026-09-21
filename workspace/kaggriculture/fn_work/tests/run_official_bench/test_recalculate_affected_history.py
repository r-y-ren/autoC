"""recalculate_affected_history 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from run_official_bench.recalculate_affected_history import recalculate_affected_history


def test_recalculate_affected_history_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:recalculate_affected_history"):
        recalculate_affected_history([])
