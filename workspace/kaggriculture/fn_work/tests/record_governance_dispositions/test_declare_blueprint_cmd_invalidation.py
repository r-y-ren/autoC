"""declare_blueprint_cmd_invalidation 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from record_governance_dispositions.declare_blueprint_cmd_invalidation import declare_blueprint_cmd_invalidation


def test_declare_blueprint_cmd_invalidation_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:declare_blueprint_cmd_invalidation"):
        declare_blueprint_cmd_invalidation([])
