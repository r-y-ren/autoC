"""regenerate_artifacts_lf 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from portable_test_baseline.regenerate_artifacts_lf import regenerate_artifacts_lf


def test_regenerate_artifacts_lf_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:regenerate_artifacts_lf"):
        regenerate_artifacts_lf(None)
