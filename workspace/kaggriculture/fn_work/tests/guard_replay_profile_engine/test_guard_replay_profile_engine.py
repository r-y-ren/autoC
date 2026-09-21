"""guard_replay_profile_engine 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from guard_replay_profile_engine.guard_replay_profile_engine import guard_replay_profile_engine


def test_guard_replay_profile_engine_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:guard_replay_profile_engine"):
        guard_replay_profile_engine()
