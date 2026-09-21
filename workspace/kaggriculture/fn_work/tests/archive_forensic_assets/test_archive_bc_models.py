"""archive_bc_models 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from archive_forensic_assets.archive_bc_models import archive_bc_models


def test_archive_bc_models_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:archive_bc_models"):
        archive_bc_models(None)
