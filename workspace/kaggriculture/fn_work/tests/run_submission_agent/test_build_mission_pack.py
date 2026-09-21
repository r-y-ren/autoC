"""build_mission_pack 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from run_submission_agent.build_mission_pack import build_mission_pack


def test_build_mission_pack_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:build_mission_pack"):
        build_mission_pack("", {})
