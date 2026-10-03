# 起操控台服务+健康就绪后开浏览器；selfcheck 只验证服务/健康/URL；失败给可操作提示非 0 退出（责任文档演进轮一：launch_console/launch_console）
from __future__ import annotations


def launch_console(*, host: str = '0.0.0.0', port: int = 8000, selftest: bool = False, no_browser: bool = False):
    # 桩——签名意图详见 responsibility.md 演进轮一增量块
    raise NotImplementedError('unimplemented:fn:launch_console')
