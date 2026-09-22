"""regenerate_artifacts_lf 真实测试：normalize/classify、tmp 工件树 LF 重建 roundtrip 与双 sha、确定性幂等、真实树锚定（c8a17920=CRLF / 39ebe3=LF）。"""

import hashlib
import json

import pytest

from portable_test_baseline.regenerate_artifacts_lf import (
    ArtifactRebuildError,
    classify_line_endings,
    normalize_lf,
    regenerate_artifacts_lf,
)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# --------------------------------------------------------------------------- #
# normalize_lf / classify_line_endings 单元
# --------------------------------------------------------------------------- #

def test_normalize_lf_conversions():
    assert normalize_lf(b"a\r\nb\r\n") == b"a\nb\n"
    assert normalize_lf(b"a\rb") == b"a\nb"          # 孤 CR 亦规范化
    assert normalize_lf(b"a\nb") == b"a\nb"          # 已 LF 幂等
    assert normalize_lf(b"\r\n\r\n") == b"\n\n"


def test_classify_line_endings():
    assert classify_line_endings(b"a\nb\n") == "LF"
    assert classify_line_endings(b"a\r\nb\r\n") == "CRLF"
    assert classify_line_endings(b"a\r\nb\rc") == "MIXED"
    assert classify_line_endings(b"a\x00b\r\n") == "BINARY"


# --------------------------------------------------------------------------- #
# tmp 工件树：LF 重建 roundtrip + 双 sha 对照 + 打包件登记 + 确定性幂等
# --------------------------------------------------------------------------- #

@pytest.fixture()
def fake_repo(tmp_path):
    """tmp 工件仓：collA 含 CRLF/LF/二进制/缺失四类条目 + 空 collB index。"""
    repo = tmp_path / "repo"
    coll = repo / "collA"
    coll.mkdir(parents=True)
    crlf_bytes = b'{\r\n  "v": 1,\r\n  "name": "crlf-artifact"\r\n}\r\n'
    lf_bytes = b'{\n  "v": 2,\n  "name": "lf-artifact"\n}\n'
    (coll / "crlf_artifact.json").write_bytes(crlf_bytes)
    (coll / "lf_artifact.json").write_bytes(lf_bytes)
    tar = coll / "packed_artifact.tar.gz"
    tar.write_bytes(b"\x1f\x8b\x00binary payload\x00")  # 二进制（后缀+空字节）
    entries = [
        {"path": "collA/crlf_artifact.json", "sha256": _sha(crlf_bytes),
         "artifact_id": "crlf_artifact"},
        {"path": "collA/lf_artifact.json", "sha256": _sha(lf_bytes),
         "artifact_id": "lf_artifact"},
        {"path": "collA/packed_artifact.tar.gz", "sha256": _sha(tar.read_bytes()),
         "artifact_id": "packed_artifact"},
        {"path": "collA/gone_artifact.json", "sha256": "0" * 64,
         "artifact_id": "gone_artifact"},
    ]
    (coll / "index.json").write_text(
        json.dumps({"schema_version": "artifact-index/1.0", "collection": "collA",
                    "entries": entries}, indent=2) + "\n", encoding="utf-8")
    empty = repo / "collB"
    empty.mkdir()
    (empty / "index.json").write_text(
        json.dumps({"schema_version": "artifact-index/1.0", "collection": "collB",
                    "entries": []}, indent=2) + "\n", encoding="utf-8")
    return repo


def _run(repo, out):
    return regenerate_artifacts_lf(
        artifact_sources=repo, output_root=out,
        repo_root=repo, campaign_boundary=repo)


def test_lf_rebuild_roundtrip_and_dual_sha(fake_repo, tmp_path):
    out = tmp_path / "artifacts"
    artifacts_root, report = _run(fake_repo, out)
    assert artifacts_root == out

    # LF 重建 roundtrip：CRLF 工件写出为纯 LF 字节，内容不丢
    rebuilt = (out / "collA/crlf_artifact.json").read_bytes()
    assert b"\r" not in rebuilt
    assert rebuilt == normalize_lf(rebuilt)
    assert json.loads(rebuilt)["name"] == "crlf-artifact"
    # 已 LF 工件逐字节保持
    assert (out / "collA/lf_artifact.json").read_bytes() == \
        (fake_repo / "collA/lf_artifact.json").read_bytes()

    # 双 sha 对照：legacy（登记原值）与 LF 值双登记
    by_path = {row["path"]: row for row in report["dual_sha_table"]}
    crlf_row = by_path["collA/crlf_artifact.json"]
    assert crlf_row["status"] == "rebuilt_lf"
    assert crlf_row["legacy_registered_sha256"] == _sha(
        (fake_repo / "collA/crlf_artifact.json").read_bytes())
    assert crlf_row["lf_sha256"] == _sha(rebuilt)
    assert crlf_row["lf_sha256"] != crlf_row["legacy_registered_sha256"]
    assert crlf_row["disk_line_endings"] == "CRLF"
    lf_row = by_path["collA/lf_artifact.json"]
    assert lf_row["legacy_registered_sha256"] == lf_row["lf_sha256"] == \
        lf_row["disk_sha256"]

    # 二进制打包件：不重建，登记说明；缺失件：留档不炸
    bin_row = by_path["collA/packed_artifact.tar.gz"]
    assert bin_row["status"] == "skipped_binary"
    assert bin_row["lf_sha256"] is None
    assert by_path["collA/gone_artifact.json"]["status"] == "missing"

    # 重建 index：sha256 换 LF 值 + legacy 双口径保留
    rebuilt_index = json.loads((out / "collA/index.json").read_text(encoding="utf-8"))
    entries = {e["path"]: e for e in rebuilt_index["entries"]}
    assert entries["collA/crlf_artifact.json"]["sha256"] == crlf_row["lf_sha256"]
    assert entries["collA/crlf_artifact.json"]["legacy_sha256"] == \
        crlf_row["legacy_registered_sha256"]
    assert rebuilt_index["lf_rebuild"]["policy"].startswith("CRLF->LF")
    # 集合统计（tmp 口径：盘上即 CRLF → legacy 与盘一致；CRLF 变体计数在
    # 真实树锚定测试覆盖——那里盘上 LF 而 legacy 登记 CRLF 值）
    assert report["collections"]["collA"]["entries_total"] == 4
    assert report["collections"]["collA"]["rebuilt_lf"] == 2
    assert report["collections"]["collA"]["skipped_binary"] == 1
    assert report["collections"]["collA"]["missing"] == 1
    assert report["collections"]["collA"]["legacy_matches_disk"] == 2
    assert report["collections"]["collA"]["legacy_is_crlf_variant"] == 0
    assert report["totals"]["collections"] == 2
    # 报告文件落盘
    assert (out / "lf_rebuild_report.json").is_file()
    md = (out / "lf_rebuild_report.md").read_text(encoding="utf-8")
    assert "collA/crlf_artifact.json" in md


def test_rebuild_deterministic_idempotent(fake_repo, tmp_path):
    out1, out2 = tmp_path / "run1", tmp_path / "run2"
    _, report1 = _run(fake_repo, out1)
    _, report2 = _run(fake_repo, out2)
    # 镜像工件与重建 index 逐字节幂等（报告 JSON 含 output_root 记录字段，单独比对内容表）
    files1 = sorted(p.relative_to(out1) for p in out1.rglob("*") if p.is_file()
                    and p.name not in ("lf_rebuild_report.json",))
    files2 = sorted(p.relative_to(out2) for p in out2.rglob("*") if p.is_file()
                    and p.name not in ("lf_rebuild_report.json",))
    assert files1 == files2
    for rel in files1:
        assert (out1 / rel).read_bytes() == (out2 / rel).read_bytes(), rel
    # 对照表与计数两次运行一致（同盘上状态 → 双 sha 表确定）
    assert report1["dual_sha_table"] == report2["dual_sha_table"]
    assert report1["totals"] == report2["totals"]
    assert report1["collections"] == report2["collections"]


def test_empty_source_set_fails_closed(tmp_path):
    with pytest.raises(ArtifactRebuildError, match="空集|未发现"):
        regenerate_artifacts_lf(artifact_sources=tmp_path, output_root=tmp_path / "o",
                                repo_root=tmp_path, campaign_boundary=tmp_path)


def test_entry_outside_boundary_rejected(fake_repo, tmp_path):
    # 越界条目：index 引用边界外路径 → fail-closed
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.json").write_bytes(b"{}\n")
    sneaky = fake_repo / "collC"
    sneaky.mkdir()
    (sneaky / "index.json").write_text(json.dumps({
        "entries": [{"path": "../outside/secret.json", "sha256": "0" * 64}]}),
        encoding="utf-8")
    with pytest.raises(ArtifactRebuildError, match="越出安全边界"):
        regenerate_artifacts_lf(
            artifact_sources=[sneaky / "index.json"], output_root=tmp_path / "o",
            repo_root=fake_repo, campaign_boundary=fake_repo)


# --------------------------------------------------------------------------- #
# 真实树锚定（只读旧树，产物落 tmp）：双 sha 事实 c8a17920=CRLF / 39ebe3=LF
# --------------------------------------------------------------------------- #

def test_real_tree_anchor_dual_sha(tmp_path):
    from portable_test_baseline.regenerate_artifacts_lf import discover_export_indexes
    indexes = discover_export_indexes()
    collections = {p.parent.name for p in indexes}
    assert {"ablations", "external", "online"} <= collections

    _, report = regenerate_artifacts_lf(output_root=tmp_path / "real")
    anchor = next(row for row in report["dual_sha_table"]
                  if row["path"].endswith("champ-vs-champ-r3p0-smoke.json"))
    # 源事实锚定：旧 index 登记 CRLF 值，POSIX 盘上/LF 重建值为 39ebe3…
    assert anchor["legacy_registered_sha256"] == \
        "c8a17920b075fe40efa6fa5839b70b88e9dc1b71840179d39e0dd892dd7ba814"
    assert anchor["lf_sha256"] == \
        "39ebe38bc841f880e0e2a30b9d8762b1a227baaec72bfc50e2574961d2f63d04"
    assert anchor["disk_line_endings"] == "LF"  # POSIX fresh clone 口径
    assert report["collections"]["ablations"]["entries_total"] == 47
    assert report["collections"]["ablations"]["legacy_is_crlf_variant"] >= 1
    # 打包工件类登记（真实 submission.tar.gz，不重建）：398P 基线时 ×3；
    # R8/R9 交付（80b68e2/1046215）在旧树新增 v48_hybrid 族 6 包 → 现值 ×9
    assert report["totals"]["packaging_not_rebuilt"] == 9
    rebuilt_file = tmp_path / "real" / anchor["path"]
    assert b"\r" not in rebuilt_file.read_bytes()
