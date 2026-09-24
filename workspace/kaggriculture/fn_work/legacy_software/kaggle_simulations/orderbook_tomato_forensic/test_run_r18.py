# -*- coding: utf-8 -*-
"""R18 测试面：run_r18（编排/出口三预绑定裁决/失败留痕）。"""
import json

import pytest

from orderbook_tomato_forensic import run_r18 as rr


def _forensics(face_alive, wheat_adopt, wheat_threshold=None):
    return {
        "cxtb": {"face_alive": face_alive, "fire_rate": 0.1 if face_alive else 0.0,
                 "evidence_path": "evidence/forensic_cxtb.json"},
        "wheat": {"adopt": wheat_adopt,
                  "best": ({"threshold": wheat_threshold} if wheat_adopt
                           else None),
                  "evidence_path": "evidence/forensic_wheat.json"},
    }


def _patch_stage(monkeypatch, *, cxtb_skip=False, adopt_stepped=False,
                 adopt_constants=False, build_ok=True, gates_overall=True):
    calls = {"build": 0, "gates": 0}

    def fake_adjudicate(face_alive, forensic_result=None, corpus=None,
                        r34a_main_path=None, replay_dir=None,
                        replay_driver=None, write_evidence=True):
        if cxtb_skip:
            return {"skipped": "face_not_alive", "adopt_stepped": False,
                    "adopt_constants": None, "params_stepped": None,
                    "params_constants": None, "evidence_path": None}
        return {"adopt_stepped": adopt_stepped,
                "adopt_constants": adopt_constants,
                "params_stepped": ({"batches": [5, 5], "density": 112.5}
                                   if adopt_stepped else None),
                "params_constants": ({"min_revenue": 8000, "their_units": 0.75,
                                      "drain_slack": 2.4}
                                     if adopt_constants else None),
                "evidence_path": "evidence/adjudicate_cxtb.json"}

    def fake_build(manifest, r34a_main_path=None, out_dir=None):
        calls["build"] += 1
        if not build_ok:
            raise RuntimeError("build boom")
        return {"ok": True, "adopted": {}, "main_sha256": "x",
                "main_bytes": 1, "tar_sha256": "y", "tar_bytes": 2,
                "last_callable": "_cxd_agent", "diff_attribution": {},
                "out_dir": out_dir}

    def fake_gates(pkg):
        calls["gates"] += 1
        return {"overall": gates_overall,
                "gates_passed": {"launch": gates_overall,
                                 "h2h_vs_r34a": gates_overall,
                                 "lineage": gates_overall,
                                 "starve_subset": gates_overall,
                                 "diff_audit": gates_overall}}

    monkeypatch.setattr(rr._fx, "adjudicate_cxtb_variants", fake_adjudicate)
    monkeypatch.setattr(rr._b36, "build_r36_conditional", fake_build)
    monkeypatch.setattr(rr._g36, "verify_r36_gates", fake_gates)
    return calls


def test_full_flow_positive(tmp_path, monkeypatch):
    calls = _patch_stage(monkeypatch, adopt_stepped=True,
                         gates_overall=True)
    summary = rr.run_r18_iteration(_forensics(True, True, 38),
                                   out_dir=str(tmp_path))
    assert summary["verdict"] == "POSITIVE"
    assert summary["launch_ready"] is True
    assert calls["build"] == 1 and calls["gates"] == 1
    saved = json.load(open(summary["run_summary_path"], encoding="utf-8"))
    assert saved["verdict"] == "POSITIVE"


def test_face_dead_no_wheat_killed_t(tmp_path, monkeypatch):
    calls = _patch_stage(monkeypatch, cxtb_skip=True)
    summary = rr.run_r18_iteration(_forensics(False, False),
                                   out_dir=str(tmp_path))
    assert summary["verdict"] == "KILLED_T"
    assert summary["launch_ready"] is False
    assert calls["build"] == 0            # 无 adoptable → 不构建


def test_face_alive_inert_negative(tmp_path, monkeypatch):
    calls = _patch_stage(monkeypatch, cxtb_skip=False, adopt_stepped=False)
    summary = rr.run_r18_iteration(_forensics(True, False),
                                   out_dir=str(tmp_path))
    assert summary["verdict"] == "NEGATIVE"
    assert calls["build"] == 0


def test_built_gates_fail_negative(tmp_path, monkeypatch):
    calls = _patch_stage(monkeypatch, adopt_stepped=True, gates_overall=False)
    summary = rr.run_r18_iteration(_forensics(True, False),
                                   out_dir=str(tmp_path))
    assert summary["verdict"] == "NEGATIVE"
    assert calls["build"] == 1 and calls["gates"] == 1


def test_fail_closed_leaves_trace(tmp_path, monkeypatch):
    _patch_stage(monkeypatch, adopt_stepped=True, build_ok=False)
    with pytest.raises(RuntimeError):
        rr.run_r18_iteration(_forensics(True, False), out_dir=str(tmp_path))
    saved = json.load(open(str(tmp_path / "evidence" / "run_summary.json"),
                           encoding="utf-8"))
    assert saved["launch_ready"] is False
    assert "build boom" in saved["error"]
