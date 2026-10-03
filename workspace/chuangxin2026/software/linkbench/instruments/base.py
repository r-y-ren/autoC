"""R9 仪表抽象：干扰源/分析仪统一接口（B210 与未来 SCPI 仪表同接口，scenario 不翻修）。"""

from __future__ import annotations


class JammerSource:
    """干扰源抽象：样式/功率/开关。"""

    def set_style(self, style: str, params: dict) -> None:
        raise NotImplementedError("unimplemented:fn:JammerSource.set_style")

    def set_power_db(self, power_db: float) -> None:
        raise NotImplementedError("unimplemented:fn:JammerSource.set_power_db")

    def on(self) -> None:
        raise NotImplementedError("unimplemented:fn:JammerSource.on")

    def off(self) -> None:
        """急停路径必经：任何异常退出前必须先调用。"""
        raise NotImplementedError("unimplemented:fn:JammerSource.off")


class SpectrumAnalyzer:
    """分析仪抽象：取一段谱统计。"""

    def get_spectrum(self, freq_hz: int, bandwidth_hz: int) -> dict:
        raise NotImplementedError("unimplemented:fn:SpectrumAnalyzer.get_spectrum")
