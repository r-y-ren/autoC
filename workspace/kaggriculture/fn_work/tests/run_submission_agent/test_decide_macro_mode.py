"""decide_macro_mode 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from run_submission_agent.decide_macro_mode import decide_macro_mode


def test_decide_macro_mode_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:decide_macro_mode"):
        decide_macro_mode({}, 0.0, {}, 0)
