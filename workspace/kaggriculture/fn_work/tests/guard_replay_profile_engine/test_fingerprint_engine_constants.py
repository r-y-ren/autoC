"""fingerprint_engine_constants 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from guard_replay_profile_engine.fingerprint_engine_constants import fingerprint_engine_constants


def test_fingerprint_engine_constants_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:fingerprint_engine_constants"):
        fingerprint_engine_constants(None)
