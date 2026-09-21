"""aggregate_scores 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from robust_selection.aggregate_scores import aggregate_scores


def test_aggregate_scores_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:aggregate_scores"):
        aggregate_scores({}, 0)
