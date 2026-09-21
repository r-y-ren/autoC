"""prune_mainline_import_graph 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from downgrade_dormant_assets.prune_mainline_import_graph import prune_mainline_import_graph


def test_prune_mainline_import_graph_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:prune_mainline_import_graph"):
        prune_mainline_import_graph(None)
