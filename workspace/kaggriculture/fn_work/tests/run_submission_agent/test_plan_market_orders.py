"""plan_market_orders 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from run_submission_agent.plan_market_orders import plan_market_orders


def test_plan_market_orders_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:plan_market_orders"):
        plan_market_orders({}, {}, {})
