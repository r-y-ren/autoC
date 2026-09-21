"""discover_campaign_roots 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from shared.discover_campaign_roots import discover_campaign_roots


def test_discover_campaign_roots_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:discover_campaign_roots"):
        discover_campaign_roots()
