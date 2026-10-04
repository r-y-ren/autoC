"""demote_active_candidate_ledger 真实测试：时点闸（可注入时钟，收口前拒绝/收口后放行）、记录态、快照门、降级物理语义。"""

import datetime as dt
import json
from pathlib import Path

import pytest

from record_governance_dispositions.demote_active_candidate_ledger import (
    DEFAULT_SNAPSHOT,
    DEMOTION_PLAN,
    GATE_DATE,
    DemotionGateError,
    demote_active_candidate_ledger,
)

_SNAP = {
    "schema_version": "1.0",
    "working": {"label": "v14.3-sellrace-working", "status": "development",
                "sha256": "f1f46638b8b7"},
    "last_promoted_frozen": {"label": "v72-frozen", "status": "frozen",
                             "sha256": "c44e2b254686"},
    "published_holdout": {"status": "published", "attempt_index": 5},
    "online_submission_refs": [],
}


def test_gate_refuses_physical_action_before_closeout(tmp_path):
    ledger = tmp_path / "active_candidate.json"
    ledger.write_text(json.dumps({"schema_version": "1.0", "working": {}}), encoding="utf-8")
    # 收口前（含收口日当日）：execute=True 一律 DemotionGateError，台账零写入
    for now in (dt.date(2026, 9, 21), dt.date(2026, 9, 29), GATE_DATE):
        with pytest.raises(DemotionGateError, match="时点闸拒绝"):
            demote_active_candidate_ledger(
                _SNAP, now=now, execute=True, ledger_path=ledger,
                campaign_root=tmp_path, output_path=tmp_path / "d.md",
            )
    assert json.loads(ledger.read_text(encoding="utf-8")) == {"schema_version": "1.0", "working": {}}


def test_gate_permits_and_executes_after_closeout(tmp_path):
    ledger = tmp_path / "active_candidate.json"
    original = {"schema_version": "1.0", "working": {"label": "v14.3"}, "extra": [1, 2]}
    ledger.write_text(json.dumps(original), encoding="utf-8")
    out = tmp_path / "d.md"
    verdict = demote_active_candidate_ledger(
        _SNAP, now=dt.date(2026, 10, 1), execute=True, ledger_path=ledger,
        campaign_root=tmp_path, output_path=out,
    )
    assert verdict["executed"] is True
    assert verdict["gate"]["physical_action"] == "executed"
    assert verdict["gate"]["phase"] == "post-closeout"
    demoted = json.loads(ledger.read_text(encoding="utf-8"))
    assert demoted["schema_version"] == "1.0-historical"
    assert demoted["demoted_at"] == "2026-10-01"
    assert demoted["historical"] == original  # 原内容整体收进 historical，可回滚
    text = out.read_text(encoding="utf-8")
    assert "已执行" in text and "时点闸" in text


def test_record_only_mode_always_allowed(tmp_path):
    out = tmp_path / "d.md"
    verdict = demote_active_candidate_ledger(
        _SNAP, now=dt.date(2026, 9, 21), campaign_root=tmp_path, output_path=out,
    )
    assert verdict["executed"] is False
    assert verdict["gate"]["physical_action"] == "record-only"
    text = out.read_text(encoding="utf-8")
    assert "现状快照" in text and "降级预案" in text and "时点闸" in text
    assert "v72-frozen" in text and "online_submission_refs" in text
    assert "空=无在册线上引用" in text
    assert "DemotionGateError" in text  # 闸语义入档
    # 注入 datetime 亦可（取 date）
    verdict2 = demote_active_candidate_ledger(
        _SNAP, now=dt.datetime(2026, 9, 21, 23, 59), campaign_root=tmp_path, output_path=out,
    )
    assert verdict2["gate"]["now"] == "2026-09-21"


def test_snapshot_gate_and_bad_clock(tmp_path):
    with pytest.raises(ValueError, match="缺失键"):
        demote_active_candidate_ledger({"schema_version": "1.0"}, campaign_root=tmp_path,
                                       output_path=tmp_path / "x.md")
    with pytest.raises(ValueError, match="now 必须为"):
        demote_active_candidate_ledger(_SNAP, now="2026-09-21", campaign_root=tmp_path,
                                       output_path=tmp_path / "x.md")


def test_default_snapshot_records_v72_era():
    assert DEFAULT_SNAPSHOT["last_promoted_frozen"]["label"] == "v72-frozen"
    assert DEFAULT_SNAPSHOT["online_submission_refs"] == []
    assert "v72 时代" in DEFAULT_SNAPSHOT["era_summary"]
    assert DEMOTION_PLAN["not_now"].startswith("不现在补记")
