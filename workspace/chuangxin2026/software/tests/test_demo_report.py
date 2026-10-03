"""R8 demo+report：桩。"""

from __future__ import annotations

import pytest

from linkbench.demo import demo
from linkbench.report import builder, curves


def test_stubs():
    with pytest.raises(NotImplementedError):
        demo.demo(quick=True)
    with pytest.raises(NotImplementedError):
        builder.build_report("runs/x")
    with pytest.raises(NotImplementedError):
        curves.plot_triple_curves("kpi.csv", "figs/")
