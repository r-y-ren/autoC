"""compile_documents 单测（继承 doc-compile 验收方式）。"""
from __future__ import annotations

import json

import pytest

from build_materials.compile_documents import MaterialError, compile_documents

KEYS = {"lowbat_headwind/conformal_coverage": 0.91, "lowbat_headwind/lead_p10_s": 5.6,
        "lowbat_headwind/lead_median_s": 7.1, "lowbat_headwind/lead_hit_rate": 0.8,
        "link_degrade/detected": 1, "link_degrade/false_alarms": 0,
        "motor_fail/confirm_p90_s": 0.18, "motor_fail/type_correct": 1.0, "motor_fail/type_total": 1.0,
        "link_degrade/detected": 1}


def _prep(tmp):
    from build_materials.draft_revision_notes import draft_revision_notes
    table = {"keys": list(KEYS), "by_key": {k: [{"value": v, "run": "r", "ts": "t"}]
                                            for k, v in KEYS.items()}}
    (tmp / "metrics_table.json").write_text(json.dumps(table), encoding="utf-8")
    (tmp / "revision_notes.md").write_text(draft_revision_notes(table, "f.md"),
                                           encoding="utf-8")
    return tmp


def test_compile_fills_numbers(tmp_path):
    outs = compile_documents(str(_prep(tmp_path)))
    assert len(outs) == 2
    text = open(outs[0], encoding="utf-8").read()
    assert "5.6" in text and "0.18" in text and "{{METRICS:" not in text


def test_precheck_blocks_on_missing(tmp_path):
    d = _prep(tmp_path)
    tbl = json.loads((d / "metrics_table.json").read_text())
    tbl["by_key"].pop("motor_fail/confirm_p90_s")
    (d / "metrics_table.json").write_text(json.dumps(tbl), encoding="utf-8")
    with pytest.raises(MaterialError, match="不在引用表"):
        compile_documents(str(d))
