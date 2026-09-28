# -*- coding: utf-8 -*-
"""R28 测试面：run_r45_iteration（全链编排+读数门三分支+fail-closed 传递）。"""
from __future__ import annotations

import gzip
import json

from orderbook_r45 import run_r45 as r45

# ---- 构建夹具（与 build/gates 测试面同形态） ------------------------------
BASE_SRC = '''# fixture r40 base main
MONEY = 3000

def _host_agent(observation, configuration=None):
    return {"farmer": ["PASS"], "hands": [], "market": []}
'''
LEDGER_SRC = ("def _ledger_entry(item, qty, due_step, advance_step):\n"
              "    return {'item': item, 'qty': qty, 'due_step': due_step,\n"
              "            'advance_step': advance_step}\n")
GATE_SRC = ("def _valley_gate_ok(quote, base):\n"
            "    return quote >= base\n")
ADV_SRC = ("def _advance_agent(observation, configuration=None):\n"
           "    try:\n"
           "        return _ADV_HOST_AGENT(observation)\n"
           "    except Exception:\n"
           "        return {'farmer': ['PASS'], 'hands': [], 'market': []}\n")
MODS = {"debt_ledger": LEDGER_SRC, "valley_gate": GATE_SRC,
        "advance_layer": ADV_SRC}
LEDGER_OK = {"g1": {"debts": [{"item": "WOOL", "qty": 5, "due_step": 100,
                               "advance_step": 96}],
                    "settled": [{"item": "WOOL", "qty": 5, "step": 100}]}}
FAKE_BUILD = {
    "ok": True, "main_path": "/tmp/r45_pkg/main.py",
    "tar_path": "/tmp/r45_pkg/submission.tar.gz",
    "man_path": "/tmp/r45_pkg/build_manifest.json",
    "main_sha256": "aa" * 32, "tar_sha256": "bb" * 32,
    "manifest": {"description":
                 "public derivative with debt-ledgered advance selling"},
}
FAKE_JUDGE_POS = {"verdict": "POSITIVE", "arms": [],
                  "criteria": {"net_identity": {"verdict": "PASS"}}}
FAKE_GATES_POS = {"gates": {}, "overall": {"passed": True}}


def _cfg(tmp_path, **over):
    cfg = {
        "base_main": str(tmp_path / "base_main.py"),
        "params": {"modules": dict(MODS)},
        "out_dir": str(tmp_path / "build"),
        "evidence_dir": str(tmp_path / "evidence"),
        "run_pytest": True,
        "pytest_runner": lambda: {"ok": True},
        "reading_gate": {"readings": {"r40": 1700.0, "r34a-new": 1741.2}},
    }
    cfg.update(over)
    return cfg


def _patch_all(monkeypatch, judge=FAKE_JUDGE_POS, gates=FAKE_GATES_POS):
    monkeypatch.setattr("orderbook_r45.build_r45.build_r45",
                        lambda *a, **k: dict(FAKE_BUILD))
    monkeypatch.setattr("orderbook_r45.judge_r45.judge_r45",
                        lambda *a, **k: dict(judge))
    monkeypatch.setattr("orderbook_r45.gates_r45.verify_r45_gates",
                        lambda *a, **k: dict(gates))


def test_run_r45_iteration(tmp_path, monkeypatch):
    """全链绿：判正+五门绿+读数门 ≥1656→交 standing 发射（台账留痕）。"""
    _patch_all(monkeypatch)
    out = r45.run_r45_iteration(_cfg(tmp_path))
    assert out["launch_decision"]["decision"] == "LAUNCH"
    assert out["verdict"]["verdict"] == "POSITIVE"
    assert out["verdict"]["launch_ready"] is True
    assert out["launch_decision"]["action"] == "交 standing 发射（台账）"
    assert "CLI" in out["launch_decision"]["next_cli"]     # 发射动作留 CLI 缝
    led = json.loads((tmp_path / "evidence" / "launch_ledger.json").read_text(
        encoding="utf-8"))
    assert led["entry"]["main_sha256"] == FAKE_BUILD["main_sha256"]
    assert "standing" in led["entry"]["auth"]
    assert led["entry"]["reading_gate"]["min_converged"] == 1700.0
    assert set(out) >= {"build", "judgment", "gates", "verdict",
                        "launch_decision"}


def test_run_r45_reading_gate_below_threshold(tmp_path, monkeypatch):
    """读数门 <1656→收档（判正仍不发射——读数门即计分对保护）。"""
    _patch_all(monkeypatch)
    out = r45.run_r45_iteration(_cfg(
        tmp_path,
        reading_gate={"readings": {"r40": 1650.0, "r34a-new": 1700.0}}))
    assert out["launch_decision"]["decision"] == "ARCHIVE"
    assert "读数门未过" in out["launch_decision"]["reason"]
    assert out["verdict"]["verdict"] == "POSITIVE"       # 判正
    assert out["verdict"]["launch_ready"] is False       # 但收档
    assert (tmp_path / "evidence" / "archive_ledger.json").exists()


def test_run_r45_reading_gate_data_missing(tmp_path, monkeypatch):
    """读数门数据缺失→收档（fail-closed）：缺失/单件/非数值三分形态。"""
    _patch_all(monkeypatch)
    for readings in (None, {"r40": 1700.0}, {"r40": 1700.0, "r34a": None},
                     {"r40": "1700", "r34a": 1741.2}):
        out = r45.run_r45_iteration(
            _cfg(tmp_path, reading_gate={"readings": readings}))
        assert out["launch_decision"]["decision"] == "ARCHIVE"
        assert "数据缺失" in out["launch_decision"]["reason"]
    out2 = r45.run_r45_iteration(_cfg(tmp_path, reading_gate=None))
    assert out2["launch_decision"]["decision"] == "ARCHIVE"


def test_run_r45_fail_closed_build_error(tmp_path, monkeypatch):
    """构建红（三件不齐/白名单外）→fail-closed 收档，不进判决。"""
    def boom(*a, **k):
        raise RuntimeError("三件不齐")

    monkeypatch.setattr("orderbook_r45.build_r45.build_r45", boom)
    out = r45.run_r45_iteration(_cfg(tmp_path))
    assert out["verdict"]["verdict"] == "NEGATIVE"
    assert out["launch_decision"]["decision"] == "ARCHIVE"
    assert out["build"]["ok"] is False
    assert out["judgment"] is None
    assert "三件不齐" in out["launch_decision"]["reason"]


def test_run_r45_fail_closed_pytest_red(tmp_path, monkeypatch):
    """pytest 红（R28 ①未过）→fail-closed 收档。"""
    _patch_all(monkeypatch)
    out = r45.run_r45_iteration(_cfg(tmp_path,
                                     pytest_runner=lambda: {"ok": False}))
    assert out["launch_decision"]["decision"] == "ARCHIVE"
    assert "pytest 红" in out["launch_decision"]["reason"]
    assert out["verdict"]["verdict"] == "NEGATIVE"


def test_run_r45_fail_closed_judge_negative(tmp_path, monkeypatch):
    """判负→五门跳过+收档（判决先行预绑定）。"""
    _patch_all(monkeypatch, judge={"verdict": "NEGATIVE", "arms": [],
                                   "criteria": {}})
    out = r45.run_r45_iteration(_cfg(tmp_path))
    assert out["gates"] == {"skipped": True, "overall": {"passed": False}}
    assert out["verdict"]["verdict"] == "NEGATIVE"
    assert out["launch_decision"]["decision"] == "ARCHIVE"


def test_run_r45_fail_closed_gates_red(tmp_path, monkeypatch):
    """五门红→收档（判正也不发射）。"""
    _patch_all(monkeypatch,
               gates={"gates": {}, "overall": {"passed": False,
                                               "failed_gates": ["h2h_vs_r40"]}})
    out = r45.run_r45_iteration(_cfg(tmp_path))
    assert out["verdict"]["verdict"] == "NEGATIVE"
    assert out["launch_decision"]["decision"] == "ARCHIVE"
    assert "门禁红" in out["launch_decision"]["reason"]


def make_e2e_runner():
    """假局组执行器（判决+五门共用）：smoke 双席自打带 DONE/预算/sha；其余
    臂带 margin+reads。"""

    def runner(specs, cfg):
        rows = []
        for s in specs:
            row = {"game_id": s["game_id"], "seed": s["seed"],
                   "arm": s.get("arm"), "our_seat": s.get("our_seat", 0),
                   "margin": 10.0, "error": None,
                   "statuses": ["DONE", "DONE"], "max_step_s": 0.2,
                   "actions_sha256": "sha-%s" % s["game_id"],
                   "reads": {"realized_px": 0.9}}
            rows.append(row)
        return rows

    return runner


def test_run_r45_end_to_end_all_green(tmp_path):
    """端到端真接线：真构建→假局组判决→五门→读数门 LAUNCH。"""
    base = tmp_path / "base_main.py"
    base.write_text(BASE_SRC, encoding="utf-8")
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    for i in range(2):
        rec = {"seed": 2000 + i, "episode_id": 600 + i,
               "teams": ["opp", "renyxin"],
               "steps": [[{"action": {"farmer": ["PASS"], "hands": [],
                                      "market": []}},
                          {"action": {"farmer": ["PASS"], "hands": [],
                                      "market": []}}] for _ in range(2)]}
        with gzip.open(corpus / ("episode-%d-strip.json.gz" % (600 + i)),
                       "wb") as fh:
            fh.write(json.dumps(rec).encode("utf-8"))
    out = r45.run_r45_iteration(_cfg(
        tmp_path, base_main=str(base), out_dir=str(tmp_path / "build"),
        runner=make_e2e_runner(), corpus=str(corpus),
        traces=[{"game_id": "g1"}], ledger=dict(LEDGER_OK),
        baseline_realized_px=0.85, n_seeds=2,
        reading_gate={"readings": {"r40": 1700.0, "r34a-new": 1741.2}}))
    assert out["launch_decision"]["decision"] == "LAUNCH"
    assert out["verdict"]["verdict"] == "POSITIVE"
    assert out["judgment"]["verdict"] == "POSITIVE"
    assert out["gates"]["overall"]["passed"] is True
    assert (tmp_path / "build" / "build_manifest.json").exists()
    assert (tmp_path / "build" / "submission.tar.gz").exists()
    assert (tmp_path / "evidence" / "launch_ledger.json").exists()
