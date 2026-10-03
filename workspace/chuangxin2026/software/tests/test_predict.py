"""R7 predict：数据类+桩。"""

from __future__ import annotations

import pytest

from linkbench.predict import predictor


def test_prediction_dataclass():
    p = predictor.StylePrediction(sigmf_base="x", predicted="cw", truth=None, probabilities={})
    assert p.truth is None


def test_stub():
    with pytest.raises(NotImplementedError):
        predictor.predict_styles("m", "s")
