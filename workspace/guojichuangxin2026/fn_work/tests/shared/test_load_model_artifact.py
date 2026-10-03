"""load_model_artifact 单测。"""
from __future__ import annotations

import pickle

import pytest

from shared.load_model_artifact import ModelArtifactError, load_model_artifact

FEATS = ["f1", "f2"]


def _torch_ckpt(path):
    import torch
    torch.save({"state_dict": {}, "feature_names": FEATS, "version": "v1",
                "kind": "tcn"}, path)


def test_torch_ok_and_missing(tmp_path):
    p = tmp_path / "m.pt"
    _torch_ckpt(p)
    blob = load_model_artifact(str(p), FEATS)
    assert blob["version"] == "v1"
    with pytest.raises(ModelArtifactError, match="train_tcn"):
        load_model_artifact(str(tmp_path / "nope.pt"), FEATS)


def test_feature_mismatch_and_no_version(tmp_path):
    p = tmp_path / "m.pt"
    _torch_ckpt(p)
    with pytest.raises(ModelArtifactError, match="特征"):
        load_model_artifact(str(p), ["f1", "other"])
    p2 = tmp_path / "bad.pt"
    import torch
    torch.save({"state_dict": {}, "feature_names": FEATS}, p2)
    with pytest.raises(ModelArtifactError, match="版本戳"):
        load_model_artifact(str(p2), FEATS)


def test_pickle_classifier(tmp_path):
    p = tmp_path / "clf.pkl"
    with open(p, "wb") as fh:
        pickle.dump({"model": "fake", "feature_names": FEATS, "version": "v0"}, fh)
    blob = load_model_artifact(str(p), FEATS)
    assert blob["model"] == "fake"
