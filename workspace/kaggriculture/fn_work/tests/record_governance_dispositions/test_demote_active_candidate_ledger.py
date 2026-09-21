"""demote_active_candidate_ledger 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from record_governance_dispositions.demote_active_candidate_ledger import demote_active_candidate_ledger


def test_demote_active_candidate_ledger_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:demote_active_candidate_ledger"):
        demote_active_candidate_ledger({})
