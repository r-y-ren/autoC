"""急停管理器：任何异常路径必须先停 TX 再退出（安全优先，硬件失联也触发）。"""

from __future__ import annotations


class EstopManager:
    """全局急停：arm() 注册回调；fire() 触发全部回调并置位；state 只升不降（本次运行内）。"""

    def __init__(self) -> None:
        self._callbacks: list = []
        self._fired = False
        self._reason: str | None = None

    def arm(self, callback) -> None:
        """注册一个急停回调（如 backend.off()）；fire 时按注册序同步调用。"""
        raise NotImplementedError("unimplemented:fn:EstopManager.arm")

    def fire(self, reason: str) -> None:
        """触发急停（幂等）；reason 记入 run.log。"""
        raise NotImplementedError("unimplemented:fn:EstopManager.fire")

    @property
    def state(self) -> str:
        """返回 'armed' | 'fired'（含 reason 摘要）。"""
        raise NotImplementedError("unimplemented:fn:EstopManager.state")
