"""R2 calibrate：导入链+桩标记。"""

from __future__ import annotations

import pytest

from linkbench.calibrate import calibrate, gain_map


def test_module_importable():
    assert callable(calibrate.run_calibration)
    assert callable(gain_map.software_gain_to_db)


def test_stubs():
    with pytest.raises(NotImplementedError):
        calibrate.run_calibration([2422e6], [])
    with pytest.raises(NotImplementedError):
        gain_map.software_gain_to_db(0.0)
