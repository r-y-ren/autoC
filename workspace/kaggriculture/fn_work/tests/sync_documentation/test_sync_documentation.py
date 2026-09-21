"""sync_documentation 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from sync_documentation.sync_documentation import sync_documentation


def test_sync_documentation_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:sync_documentation"):
        sync_documentation()
