"""rollout_with_replay_opponent 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from run_official_bench.rollout_with_replay_opponent import rollout_with_replay_opponent


def test_rollout_with_replay_opponent_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:rollout_with_replay_opponent"):
        rollout_with_replay_opponent(None, None, None, 0)
