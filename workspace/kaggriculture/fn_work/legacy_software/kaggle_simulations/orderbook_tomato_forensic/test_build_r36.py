# -*- coding: utf-8 -*-
"""R18 测试面：build_r36（白名单条件构建+diff 审计+打包）。真基座（r34a 原文）
承载锚唯一性/构建链；重演面不跑（S3 CLI 承载）。"""
import json

import pytest

from orderbook_tomato_forensic import build_r36 as b36

R34A_MAIN = b36.R34A_MAIN


def test_cxtb_anchors_unique_on_real_r34a():
    text = open(R34A_MAIN, encoding="utf-8").read()
    for anchor in (b36.CXTB_MINREV_OLD, b36.CXTB_THEIR_OLD, b36.CXTB_SLACK_OLD):
        assert text.count(anchor) == 1


def test_constants_roundtrip_and_value():
    text = open(R34A_MAIN, encoding="utf-8").read()
    same = b36.apply_cxtb_constants(text, 9000, 0.75, 2.4)
    assert same == text                              # 基线幂等
    moved = b36.apply_cxtb_constants(text, 8000, 0.6, 2.0)
    assert "_CXTB_MIN_REVENUE = 8000" in moved
    assert "_CXTB_THEIR_UNITS = 0.6" in moved
    assert "_CXTB_DRAIN_SLACK = 2.0" in moved


def test_stepped_block_shape():
    block = b36.stepped_block_text((5, 5))
    compile(block, "stepped_block", "exec")          # 语法合法
    assert block.rstrip().endswith("_r36_agent = _r36_step_agent")
    assert "_R36_BATCHES = (5, 5)" in block
    with pytest.raises(b36.BuildR36Error):
        b36.stepped_block_text((5,))                 # 批数不足
    with pytest.raises(b36.BuildR36Error):
        b36.stepped_block_text((6, 5))               # 和 != 10


def test_build_no_adopt_raises(tmp_path):
    with pytest.raises(b36.BuildR36Error):
        b36.build_r36_conditional(
            {"wheat_threshold": {"adopt": False}}, R34A_MAIN, str(tmp_path))


def test_build_wheat_only(tmp_path):
    manifest = {"wheat_threshold": {"adopt": True, "threshold": 34}}
    summary = b36.build_r36_conditional(manifest, R34A_MAIN, str(tmp_path))
    assert summary["ok"] is True
    assert summary["adopted"] == {"wheat_threshold": 34}
    assert summary["last_callable"] == "_cxd_agent"     # 无阶梯尾块→官方入口不变
    assert summary["diff_attribution"] == {
        "blank_cosmetic": 1,                      # 守卫注释行
        "wheat_step91_threshold(scan winner)": 2}  # 代码行+遥测行
    text = open(str(tmp_path / "main.py"), encoding="utf-8").read()
    assert "if price < 34:" in text
    tar = str(tmp_path / "submission.tar.gz")
    assert open(tar, "rb").read()
    mf = json.load(open(str(tmp_path / "build_manifest.json"), encoding="utf-8"))
    assert mf["variant"] == "r36" and mf["tar_members"] == ["main.py"]


def test_build_stepped_and_constants(tmp_path):
    manifest = {
        "cxtb_stepped": {"adopt": True, "batches": (5, 5),
                         "density": 9000.0 / 80.0},
        "cxtb_constants": {"adopt": True, "min_revenue": 8000,
                           "their_units": 0.9, "drain_slack": 2.8},
    }
    summary = b36.build_r36_conditional(manifest, R34A_MAIN, str(tmp_path))
    assert summary["last_callable"] == "_r36_agent"
    assert set(summary["diff_attribution"]) <= {
        "cxtb_constants(scan winner)", "cxtb_stepped(appended tail block)",
        "blank_cosmetic"}
    assert "cxtb_constants(scan winner)" in summary["diff_attribution"]
    assert "cxtb_stepped(appended tail block)" in summary["diff_attribution"]


def test_audit_rejects_stray_diff(tmp_path):
    text = open(R34A_MAIN, encoding="utf-8").read()
    stray = text.replace("MAX_ORDERS=10", "MAX_ORDERS=11", 1)
    r36 = tmp_path / "main.py"
    r36.write_text(stray, encoding="utf-8")
    audit = b36.audit_diff_vs_r34a(R34A_MAIN, str(r36))
    assert audit["ok"] is False
    assert audit["attribution"].get("UNATTRIBUTED") == 1


def test_audit_expected_append_guard(tmp_path):
    text = open(R34A_MAIN, encoding="utf-8").read()
    block = b36.stepped_block_text((4, 3, 3))
    r36 = tmp_path / "main.py"
    r36.write_text(text + block, encoding="utf-8")
    ok = b36.audit_diff_vs_r34a(
        R34A_MAIN, str(r36), expected_stepped_append=block.split("\n"))
    assert ok["ok"] is True
    # 杂散行混入尾块：期望=干净块（构建面真值来自 stepped_block_text 生成器）
    # → 杂散行 hunk 不能命中期望块连续子段 → UNATTRIBUTED → 红。
    contaminated = block + "_MAX_ORDERS_HACK = 11\n"
    bad = tmp_path / "bad.py"
    bad.write_text(text + contaminated, encoding="utf-8")
    ko = b36.audit_diff_vs_r34a(
        R34A_MAIN, str(bad), expected_stepped_append=block.split("\n"))
    assert ko["ok"] is False and "UNATTRIBUTED" in ko["attribution"]
    # 期望块与实际不符 → 尾块 hunk 归 UNATTRIBUTED
    mismatch = b36.audit_diff_vs_r34a(
        R34A_MAIN, str(r36), expected_stepped_append=["_x = 1"])
    assert mismatch["ok"] is False
