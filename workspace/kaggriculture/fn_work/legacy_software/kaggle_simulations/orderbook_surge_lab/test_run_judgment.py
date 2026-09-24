# -*- coding: utf-8 -*-
"""test_run_judgment —— 编排+短路+evidence schema 组（真引擎微局夹具）。"""
import json
import os

import pytest

from orderbook_surge_lab import corpus as C
from orderbook_surge_lab import phase_b as B
from orderbook_surge_lab import run_judgment as R
from orderbook_surge_lab.test_phase_b import _mini_replay  # 复用微局夹具


@pytest.fixture
def quiet_corpus(tmp_path):
    """双席全程 PASS 的微局语料（零 surge 日 → KILLED_A 短路面）。"""
    for ep in (201, 202):
        (tmp_path / f"episode-{ep}-replay.json").write_text(
            json.dumps(_mini_replay()), encoding="utf-8")
    return tmp_path


class TestRunJudgment:
    def test_killed_a_short_circuit_and_schema(self, quiet_corpus, tmp_path,
                                               capsys):
        ev = R.run_judgment(replay_dir=str(quiet_corpus),
                            evidence_dir=str(tmp_path / "ev"))
        assert ev["overall"] == "KILLED_A"
        assert ev["phase_b"] is None
        # evidence schema：source/phase_a/judge/overall
        for key in ("source", "phase_a", "judge", "overall", "generated_at",
                    "wall_s"):
            assert key in ev
        assert ev["source"]["corpus_phase_a"] == [201, 202]
        assert os.path.isfile(ev["source"]["phase_a_full_path"])
        assert "run_judgment.py" in ev["source"]["rerun_command"]
        # judgment.json 落盘且与返回一致
        on_disk = json.load(open(os.path.join(str(tmp_path / "ev"),
                                              "judgment.json"),
                                 encoding="utf-8"))
        assert on_disk["overall"] == "KILLED_A"
        assert ev["phase_a"]["panorama"]["n_games"] == 2
        out = capsys.readouterr().out
        assert "KILLED_A" in out

    def test_fail_closed_on_empty_dir(self, tmp_path, tmp_path_factory):
        empty = tmp_path_factory.mktemp("empty")
        ev = R.run_judgment(replay_dir=str(empty),
                            evidence_dir=str(tmp_path / "ev2"))
        assert ev["overall"] == "FAIL" and "Phase A fail-closed" in ev["error"]

    def test_positive_flow_with_fake_phase_b(self, quiet_corpus, tmp_path,
                                             monkeypatch):
        """编排正路：monkeypatch phase_b 重演为构造结果 → POSITIVE 落盘。"""
        real_select = C.corpus_select

        def fake_select(replay_dir, phase_a_report=None, n_wins_per_tag=4):
            base = real_select(replay_dir, phase_a_report)
            base["phase_b"] = {
                "losses": [{"episode": 201, "path": "x", "res": "L",
                            "treatable": True}],
                "wins": [{"episode": 202, "path": "y", "res": "W"}]}
            return base

        def fake_replay(corpus_b, report_a, l3_main, wall_budget_s=0.0,
                        log=None):
            def game(ep, res, deltas):
                arms = {}
                for s in (0, 1):
                    seat = arms[f"seat{s}"] = {"surge_days": [1], "control":
                                               {"margin": 0.0}}
                    for arm in B.ARMS:
                        seat[arm] = {"margin": deltas[arm], "delta":
                                     deltas[arm], "status": "DONE",
                                     "steps_n": 719, "red": False,
                                     "zerofootprint_wrapper": {"ok": True},
                                     "zerofootprint_stream": {
                                         "binding_ok": True,
                                         "first_alien_diff": None}}
                return {"episode": ep, "res": res, "treatable": res == "L",
                        "arms": arms}
            return {"per_game": [game(201, "L", {"A1": 40.0, "A2": 40.0,
                                                 "A3": 40.0}),
                                 game(202, "W", {"A1": 0.0, "A2": 0.0,
                                                 "A3": 0.0})],
                    "summary": {"n_games": 2, "n_replays": 16, "n_red": 0,
                                "wall_s": 0.1, "budget_stopped": False}}

        # 让 Phase A 报一个可处置 surge 日（否则短路 KILLED_A）
        import orderbook_surge_lab.phase_a as A
        orig_attr = A.phase_a_attribution

        def patched(entries, *a, **k):
            rep = orig_attr(entries, *a, **k)
            for g in rep["per_game"]:
                g["res"] = "L" if g["episode"] == 201 else "W"
                g["treatable"] = g["episode"] == 201
                g["treatable_surge_days"] = [1] if g["episode"] == 201 else []
                g["surge_days"] = [1] if g["episode"] == 201 else []
            rep["panorama"]["n_treatable_losses"] = 1
            rep["panorama"]["n_treatable_surge_days"] = 1
            return rep

        monkeypatch.setattr(C, "corpus_select", fake_select)
        monkeypatch.setattr(B, "phase_b_four_arm_replay", fake_replay)
        monkeypatch.setattr(A, "phase_a_attribution", patched)
        ev = R.run_judgment(replay_dir=str(quiet_corpus),
                            evidence_dir=str(tmp_path / "ev3"))
        assert ev["overall"] == "POSITIVE"
        assert ev["judge"]["winning_arm"] in B.ARMS
        assert ev["phase_b"]["summary"]["n_replays"] == 16
        assert ev["source"]["corpus_phase_b"]["losses"] == [201]
        # fake 语料无胜局 → 真实 select 的 sampling 记录空池（推导留痕）
        assert ev["source"]["win_sampling"]["per_tag"]["r32"]["pool"] == []
