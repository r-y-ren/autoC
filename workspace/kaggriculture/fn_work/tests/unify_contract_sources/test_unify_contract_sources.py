"""unify_contract_sources 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from unify_contract_sources.unify_contract_sources import unify_contract_sources


def test_unify_contract_sources_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:unify_contract_sources"):
        unify_contract_sources()
