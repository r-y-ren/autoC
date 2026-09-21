"""record_governance_dispositions 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from record_governance_dispositions.record_governance_dispositions import record_governance_dispositions


def test_record_governance_dispositions_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:record_governance_dispositions"):
        record_governance_dispositions([])
