"""draft_revision_notes 单测（占位符全闭合断言）。"""
from __future__ import annotations

import pytest

from build_materials.draft_revision_notes import MaterialError, draft_revision_notes


def _table(keys):
    return {"keys": list(keys), "by_key": {k: [{"value": 1, "run": "r", "ts": "t"}]
                                           for k in keys}}


KEYS = ["lowbat_headwind/conformal_coverage", "lowbat_headwind/lead_p10_s",
        "lowbat_headwind/lead_median_s", "lowbat_headwind/lead_hit_rate",
        "link_degrade/detected", "link_degrade/false_alarms",
        "motor_fail/confirm_p90_s", "motor_fail/type_correct", "motor_fail/type_total"]


def test_all_placeholders_resolvable():
    import re
    out = draft_revision_notes(_table(KEYS), "frontier.md")
    ph = re.compile(r"\{\{METRICS:([a-zA-Z0-9_/\.\-]+)\}\}")
    keys = {m.group(1) for m in ph.finditer(out)}
    assert keys and keys <= set(KEYS)            # 草稿阶段占位符保留，键全可解析
    assert "人机分工记录" in out and "共形" in out


def test_missing_key_raises():
    with pytest.raises(MaterialError, match="引用键缺失"):
        draft_revision_notes(_table(KEYS[:-1]), "frontier.md")


def test_new_sections_present():
    """R19/R20/R22：评估卫生+安全滤波叙事+硬件采购表入稿。"""
    out = draft_revision_notes(_table(KEYS), "frontier.md")
    assert "评估卫生" in out and "tsfm-bench" in out          # R19
    assert "安全域投影" in out and "Sim-to-Real" in out        # R20
    assert "硬件采购表" in out and "Jetson Orin NX" in out     # R22
