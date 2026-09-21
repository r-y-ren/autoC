"""archive_forensic_assets 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from archive_forensic_assets.archive_forensic_assets import archive_forensic_assets


def test_archive_forensic_assets_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:archive_forensic_assets"):
        archive_forensic_assets({})
