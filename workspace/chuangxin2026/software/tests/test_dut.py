"""R3 dut：导入链+串口契约数据类+桩标记。"""

from __future__ import annotations

import pytest

from linkbench.dut import collector, fake_dut, serial_link


def test_dut_sample_fields():
    s = serial_link.DutSample(link="wifi", seq=1, ts_ms=0, per=0.0, tx_n=100, err_n=0)
    assert s.rssi_dbm is None and s.fw == ""


def test_stubs():
    with pytest.raises(NotImplementedError):
        serial_link.parse_dut_line(b"{}")
    with pytest.raises(NotImplementedError):
        collector.watch_links(1.0)
    assert callable(fake_dut.fake_stream)
