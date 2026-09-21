"""record_governance_dispositions 顶层真实测试：信封校验 fail-closed、三叶编排+schema 校验、汇编落盘、默认载荷。"""

import datetime as dt
from pathlib import Path

import pytest

from record_governance_dispositions.record_governance_dispositions import (
    DEFAULT_DUAL_SOURCE_EVIDENCE,
    KIND_ACTIVE_CANDIDATE,
    KIND_BLUEPRINT_INVALIDATION,
    KIND_PROVENANCE,
    default_disposition_list,
    record_governance_dispositions,
    validate_record_schema,
)

_PROV = DEFAULT_DUAL_SOURCE_EVIDENCE
_CMDS = [
    {"id": "doc-compile", "cmd": "typst compile … docs/report.typ", "missing_path": "docs/report.typ"},
    {"id": "doc-consistency", "cmd": "python …/docs/check_report_metrics.py",
     "missing_path": "docs/check_report_metrics.py"},
]
_SNAP = {
    "schema_version": "1.0",
    "working": {"label": "v14.3-sellrace-working", "status": "development", "sha256": "f1f466…"},
    "last_promoted_frozen": {"label": "v72-frozen", "status": "frozen", "sha256": "c44e2b…"},
    "online_submission_refs": [],
}


def _make_campaign(tmp_path: Path) -> Path:
    prov = tmp_path / "software/kaggle_simulations/opponents/PROVENANCE.md"
    prov.parent.mkdir(parents=True)
    prov.write_text("Author: kaitofukami\n", encoding="utf-8")
    readme = tmp_path / "software/kaggle_simulations/v48plus/README.md"
    readme.parent.mkdir(parents=True, exist_ok=True)
    readme.write_text("V48: Ahmed Berat Ozer\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "g.md").write_text("无关\n", encoding="utf-8")
    return tmp_path


def _list():
    return [
        {"kind": KIND_PROVENANCE, "payload": _PROV},
        {"kind": KIND_BLUEPRINT_INVALIDATION, "payload": _CMDS},
        {"kind": KIND_ACTIVE_CANDIDATE, "payload": _SNAP},
    ]


def test_orchestrates_three_leaves_and_assembly(tmp_path):
    camp = _make_campaign(tmp_path)
    out = tmp_path / "assembly.md"
    verdict = record_governance_dispositions(
        _list(), now=dt.date(2026, 9, 21), campaign_root=camp, output_path=out,
    )
    assert verdict["schema_valid"] is True
    assert [d["status"] for d in verdict["dispositions"]] == ["recorded"] * 3
    # 三叶输出均落在 tmp 战役根 fn_docs 下（未写真实战役树）
    fn_docs = camp / "fn_docs"
    for name in ("provenance_dadee25a.md", "blueprint_cmd_invalidation.md",
                 "active_candidate_disposition.md"):
        assert (fn_docs / name).is_file(), name
    assert out.is_file()
    text = out.read_text(encoding="utf-8")
    assert "provenance_dadee25a.md" in text and "blueprint_cmd_invalidation.md" in text
    assert "active_candidate_disposition.md" in text
    assert "schema 校验" in text and "| True |" in text
    # 降级叶为记录态（编排面不暴露 execute）
    demo = verdict["dispositions"][2]["verdict"]
    assert demo["executed"] is False and demo["gate"]["physical_action"] == "record-only"


def test_envelope_schema_fail_closed(tmp_path):
    camp = _make_campaign(tmp_path)
    with pytest.raises(ValueError, match="不在枚举"):
        record_governance_dispositions(
            _list() + [{"kind": "nuke_everything", "payload": {}}],
            campaign_root=camp, output_path=tmp_path / "a.md",
        )
    with pytest.raises(ValueError, match="缺叶"):
        record_governance_dispositions(_list()[:2], campaign_root=camp,
                                       output_path=tmp_path / "a.md")
    with pytest.raises(ValueError, match="重复叶"):
        record_governance_dispositions(
            _list() + [{"kind": KIND_PROVENANCE, "payload": _PROV}],
            campaign_root=camp, output_path=tmp_path / "a.md",
        )
    with pytest.raises(ValueError, match="为空"):
        record_governance_dispositions([], campaign_root=camp, output_path=tmp_path / "a.md")


def test_record_schema_gate_detects_marker_loss(tmp_path):
    fn_docs = tmp_path / "fn_docs"
    fn_docs.mkdir(parents=True)
    good_prov = ("# 双源\n源A kaitofukami；源B ahmedberatozer；两账号间未定；"
                 "ref 56400478\n残留清单：…\n")
    (fn_docs / "provenance_dadee25a.md").write_text(good_prov, encoding="utf-8")
    (fn_docs / "blueprint_cmd_invalidation.md").write_text(
        "# 失效\ndoc-compile / doc-consistency 指向文件不存在；静默事实：run-29\n",
        encoding="utf-8",
    )
    (fn_docs / "active_candidate_disposition.md").write_text(
        "# 处置\n时点闸 2026-09-30；降级预案；v72-frozen；online_submission_refs 空\n",
        encoding="utf-8",
    )
    results = validate_record_schema(fn_docs)
    assert set(results) == {"provenance_dadee25a.md", "blueprint_cmd_invalidation.md",
                            "active_candidate_disposition.md"}
    # 抹掉一个标记 → fail-closed
    (fn_docs / "provenance_dadee25a.md").write_text("# 双源（缺标记）\n", encoding="utf-8")
    with pytest.raises(ValueError, match="缺 schema 标记"):
        validate_record_schema(fn_docs)
    # 删一件 → 缺记录
    (fn_docs / "provenance_dadee25a.md").write_text(good_prov, encoding="utf-8")
    (fn_docs / "blueprint_cmd_invalidation.md").unlink()
    with pytest.raises(ValueError, match="处置记录缺失"):
        validate_record_schema(fn_docs)


def test_default_disposition_list_carries_repo_facts():
    dl = default_disposition_list()
    assert [e["kind"] for e in dl] == [KIND_PROVENANCE, KIND_BLUEPRINT_INVALIDATION,
                                       KIND_ACTIVE_CANDIDATE]
    ev = dl[0]["payload"]
    assert ev["online_ref"] == 56400478
    assert ev["original_attribution"] == "两账号间未定"
    assert [s["account"] for s in ev["sources"]] == ["kaitofukami", "ahmedberatozer"]
    assert [c["id"] for c in dl[1]["payload"]] == ["doc-compile", "doc-consistency"]
    assert dl[2]["payload"]["online_submission_refs"] == []


def test_empty_payload_falls_back_to_defaults(tmp_path):
    camp = _make_campaign(tmp_path)
    verdict = record_governance_dispositions(
        [
            {"kind": KIND_PROVENANCE, "payload": None},
            {"kind": KIND_BLUEPRINT_INVALIDATION, "payload": []},
            {"kind": KIND_ACTIVE_CANDIDATE, "payload": {}},
        ],
        campaign_root=camp, output_path=tmp_path / "a.md",
    )
    assert verdict["schema_valid"] is True
