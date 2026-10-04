"""archive_bc_models 镜像测试：登记态（零物理移动）/字节实测/缺目录 fail-closed。"""

from pathlib import Path

import pytest

from archive_forensic_assets.archive_bc_models import archive_bc_models


@pytest.fixture()
def fake_models_dir(tmp_path):
    models = tmp_path / "software" / "bc_track" / "models"
    models.mkdir(parents=True)
    (models / "bc_model_v1.py").write_bytes(b"x" * 100)
    (models / "bc_model_v2.py").write_bytes(b"y" * 140)
    (models / "train_report.json").write_bytes(b"{}")
    (models / "train_report_v1.json").write_bytes(b"{}")
    (models / "train_report_v2.json").write_bytes(b"{}")
    return models


def test_registry_only_registration_no_physical_move(fake_models_dir, tmp_path):
    result = archive_bc_models(fake_models_dir)
    assert result["mode"] == "registry-only"
    assert result["moved"] is False
    assert len(result["entries"]) == 5
    assert result["total_bytes"] == 100 + 140 + 2 + 2 + 2
    assert result["weights_bytes"] == 240
    for entry in result["entries"]:
        assert set(entry) == {"file", "size_bytes", "kind", "reason",
                              "postwar_dest"}
        assert entry["postwar_dest"] == f"forensics_archive/bc_models/{entry['file']}"
        assert entry["kind"] in ("权重", "报告")
    kinds = {e["file"]: e["kind"] for e in result["entries"]}
    assert kinds["bc_model_v1.py"] == "权重"
    assert kinds["train_report.json"] == "报告"
    # 零物理移动：源件全在、归档区目录未建
    assert len(list(fake_models_dir.iterdir())) == 5
    assert not (tmp_path / "forensics_archive").exists()


def test_missing_dir_fail_closed(tmp_path):
    with pytest.raises(ValueError, match="models 目录不存在"):
        archive_bc_models(tmp_path / "nope")


def test_empty_dir_fail_closed(tmp_path):
    empty = tmp_path / "models"
    empty.mkdir()
    with pytest.raises(ValueError, match="为空"):
        archive_bc_models(empty)
