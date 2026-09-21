"""codify_probes_policy 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from sync_documentation.codify_probes_policy import codify_probes_policy


def test_codify_probes_policy_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:codify_probes_policy"):
        codify_probes_policy(None)
