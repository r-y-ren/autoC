"""PyVISA 后端（远期仪表到位后启用；PyVISA 惰性导入，未装不阻碍导入链）。"""

from __future__ import annotations

from linkbench.instruments.base import JammerSource, SpectrumAnalyzer


class PyVisaJammer(JammerSource):
    """SCPI 信号源（如 1433D）：resource_str 如 'TCPIP0::192.168.1.10::inst0::INSTR'。"""

    def __init__(self, resource_str: str) -> None:
        self.resource_str = resource_str


class PyVisaAnalyzer(SpectrumAnalyzer):
    """SCPI 频谱仪（如 RSA513A）。"""


# 注：方法实现全部继承 base 的桩，仪表到位后 fn-implement/演进周期覆写。
