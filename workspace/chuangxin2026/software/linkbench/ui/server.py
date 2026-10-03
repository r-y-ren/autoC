"""R11 顶层：Web 操控台服务（FastAPI 惰性导入——未装依赖时其余模块不受影响）。"""

from __future__ import annotations


def create_app():
    """构建 FastAPI 应用（挂 api 路由 + WS + 静态页）；返回 app 对象。"""
    raise NotImplementedError("unimplemented:fn:create_app")


def serve(host: str = "0.0.0.0", port: int = 8000) -> None:
    """启动服务（uvicorn）；启动失败/端口占用抛 OSError。"""
    raise NotImplementedError("unimplemented:fn:serve")
