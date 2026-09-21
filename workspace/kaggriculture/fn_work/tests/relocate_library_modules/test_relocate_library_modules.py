"""relocate_library_modules 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from relocate_library_modules.relocate_library_modules import relocate_library_modules


def test_relocate_library_modules_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:relocate_library_modules"):
        relocate_library_modules()
