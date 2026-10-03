"""操控台 API 路由（全部端点收口于此，R11/R12）。"""

from __future__ import annotations


def register_api(app) -> None:
    """把全部 REST 端点挂到 app：/api/health、/api/scenarios、/api/run（开始）、
    /api/stop、/api/estop（急停）、/api/runs（历史）、/api/runs/{id}/report、/api/demo。"""
    raise NotImplementedError("unimplemented:fn:register_api")
