"""R4 record：导入链+桩标记。"""

from __future__ import annotations

import pytest

from linkbench.record import monitor, recorder


def test_stubs():
    with pytest.raises(NotImplementedError):
        recorder.record_run(None, 1.0, __import__("pathlib").Path("runs/x"))
    with pytest.raises(NotImplementedError):
        monitor.spectrum_stats(None, 1e6)
