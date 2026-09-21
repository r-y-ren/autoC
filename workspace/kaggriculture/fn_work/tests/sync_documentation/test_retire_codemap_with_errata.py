"""retire_codemap_with_errata 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from sync_documentation.retire_codemap_with_errata import retire_codemap_with_errata


def test_retire_codemap_with_errata_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:retire_codemap_with_errata"):
        retire_codemap_with_errata([])
