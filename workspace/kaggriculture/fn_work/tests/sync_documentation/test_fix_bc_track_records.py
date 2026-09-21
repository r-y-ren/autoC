"""fix_bc_track_records 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from sync_documentation.fix_bc_track_records import fix_bc_track_records


def test_fix_bc_track_records_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:fix_bc_track_records"):
        fix_bc_track_records(None)
