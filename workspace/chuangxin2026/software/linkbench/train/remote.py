"""远程算力派发：训练作业 → /toolbox（4070 笔记本），本地 CPU 为降级路径。"""

from __future__ import annotations


def dispatch_toolbox(script: str, args: list[str]) -> int:
    """把训练脚本派发到 toolbox 远程算力执行；不可达时由调用方降级本地。返回退出码。"""
    raise NotImplementedError("unimplemented:fn:dispatch_toolbox")
