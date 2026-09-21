"""evaluate_plan_portfolio 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from run_official_bench.evaluate_plan_portfolio import evaluate_plan_portfolio


def test_evaluate_plan_portfolio_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:evaluate_plan_portfolio"):
        evaluate_plan_portfolio([], [], 0)
