"""downgrade_dormant_assets 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from downgrade_dormant_assets.downgrade_dormant_assets import downgrade_dormant_assets


def test_downgrade_dormant_assets_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:downgrade_dormant_assets"):
        downgrade_dormant_assets()
