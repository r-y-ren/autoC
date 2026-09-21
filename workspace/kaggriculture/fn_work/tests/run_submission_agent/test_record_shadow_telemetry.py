"""record_shadow_telemetry 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from run_submission_agent.record_shadow_telemetry import record_shadow_telemetry


def test_record_shadow_telemetry_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:record_shadow_telemetry"):
        record_shadow_telemetry({})
