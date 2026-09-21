"""solve_worker_routes 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from run_submission_agent.solve_worker_routes import solve_worker_routes


def test_solve_worker_routes_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:solve_worker_routes"):
        solve_worker_routes([], {}, {})
