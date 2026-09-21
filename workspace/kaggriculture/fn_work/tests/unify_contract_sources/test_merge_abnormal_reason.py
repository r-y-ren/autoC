"""merge_abnormal_reason 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from unify_contract_sources.merge_abnormal_reason import merge_abnormal_reason


def test_merge_abnormal_reason_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:merge_abnormal_reason"):
        merge_abnormal_reason({})
