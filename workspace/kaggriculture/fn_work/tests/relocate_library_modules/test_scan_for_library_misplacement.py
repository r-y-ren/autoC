"""scan_for_library_misplacement 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from relocate_library_modules.scan_for_library_misplacement import scan_for_library_misplacement


def test_scan_for_library_misplacement_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:scan_for_library_misplacement"):
        scan_for_library_misplacement(None)
