"""B210 后端：USRP B210 实现的 JammerSource/Analyzer（UHD/GNU Radio 惰性导入）。"""

from __future__ import annotations

from linkbench.instruments.base import JammerSource, SpectrumAnalyzer


class B210Jammer(JammerSource):
    """CH1=注入 TX；软件增益步进=功率细档（增益顶=scenario safety.max_tx_gain_db）。"""

    def __init__(self, serial: str | None = None) -> None:
        self.serial = serial


class B210Monitor(SpectrumAnalyzer):
    """CH2=监测 RX（自校 JSR / 平坦度核验）。"""


# 注：方法实现全部继承 base 的桩（标记同名），fn-implement 阶段覆写。
