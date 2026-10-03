# EstopManager：全局急停管理器（注册回调→按序触发→状态只升不降）


class EstopManager:
    def arm(self, callback):
        """注册停发射回调。"""
        raise NotImplementedError('unimplemented:fn:EstopManager.arm')

    def fire(self, reason: str) -> None:
        """触发急停（幂等），reason 入 run.log。"""
        raise NotImplementedError('unimplemented:fn:EstopManager.fire')

    @property
    def state(self) -> str:
        """'armed' | 'fired'（含原因摘要）。"""
        raise NotImplementedError('unimplemented:fn:EstopManager.state')
