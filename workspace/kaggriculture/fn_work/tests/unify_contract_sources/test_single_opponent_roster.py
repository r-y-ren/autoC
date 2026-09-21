"""single_opponent_roster 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from unify_contract_sources.single_opponent_roster import single_opponent_roster


def test_single_opponent_roster_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:single_opponent_roster"):
        single_opponent_roster()
