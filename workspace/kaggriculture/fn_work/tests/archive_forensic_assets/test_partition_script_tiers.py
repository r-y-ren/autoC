"""partition_script_tiers 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from archive_forensic_assets.partition_script_tiers import partition_script_tiers


def test_partition_script_tiers_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:partition_script_tiers"):
        partition_script_tiers([])
