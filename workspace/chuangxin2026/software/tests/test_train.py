"""R7 train：分组 CV/谱图/远程派发桩。"""

from __future__ import annotations

import pytest

from linkbench.train import cv_grouped, remote, spectrogram, trainer


def test_stubs():
    with pytest.raises(NotImplementedError):
        spectrogram.make_spectrogram(None)
    with pytest.raises(NotImplementedError):
        cv_grouped.grouped_split("dataset_index.json")
    with pytest.raises(NotImplementedError):
        remote.dispatch_toolbox("train.py", [])
    with pytest.raises(NotImplementedError):
        trainer.train_model("runs/dataset_v1")
    with pytest.raises(NotImplementedError):
        trainer.evaluate("m", "d")
