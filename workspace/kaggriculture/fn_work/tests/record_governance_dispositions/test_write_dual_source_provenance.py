"""write_dual_source_provenance 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from record_governance_dispositions.write_dual_source_provenance import write_dual_source_provenance


def test_write_dual_source_provenance_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:write_dual_source_provenance"):
        write_dual_source_provenance({})
