# parse_serial_line 桩阶段测试（与被测函数同名镜像）
import pytest

from src.collect_dut_samples.parse_serial_line import parse_serial_line


def test_parse_serial_line_stub():
    assert callable(parse_serial_line)
    with pytest.raises(NotImplementedError):
        parse_serial_line(b'{}')
