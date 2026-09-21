"""assert_bots_constants_match_wheel 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from unify_contract_sources.assert_bots_constants_match_wheel import assert_bots_constants_match_wheel


def test_assert_bots_constants_match_wheel_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:assert_bots_constants_match_wheel"):
        assert_bots_constants_match_wheel()
