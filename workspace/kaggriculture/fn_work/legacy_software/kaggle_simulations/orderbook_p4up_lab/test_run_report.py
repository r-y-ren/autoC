# -*- coding: utf-8 -*-
"""test_run_report —— 样例报告组装判例（六读数齐备 + 阈值随判 + 文本渲染）。"""
import json
import os
import tempfile

from orderbook_p4up_lab import run_report as RR
from orderbook_p4up_lab.records import EpisodeRecord


def act(verb="HARVEST", market=()):
    return {"farmer": [verb], "hands": [], "market": [list(m) for m in market]}


def _stream(n=240, verb="HARVEST"):
    return [act(verb) for _ in range(n)]


def _grid(v):
    g = [[0] * 10 for _ in range(10)]
    g[0][0] = v
    return g


def _rec(i, world="A__B"):
    n = 240
    prices = [{"WOOL": 100}] * n
    return EpisodeRecord(
        episode=i, seat=0, team="ME", opp=f"OPP{i % 3}", margin=float(i - 1),
        stream=_stream(n), opp_stream=_stream(n, "CARE"), world=world,
        prices_t=prices, money_me=[0.0] * n, money_op=[0.0] * n,
        occ=_grid(5), pres=_grid(5),
        unlocked=[[1] * 10 for _ in range(10)])


class TestBuildReport:
    def _rep(self):
        recs = [_rec(i) for i in range(8)]
        return RR.build_report(recs)

    def test_six_readings_present(self):
        rep = self._rep()
        for k in ("C1_GLOBAL_WITHIN_WORLD", "C2_KINSHIP_MIRROR",
                  "C3_CONVERGENCE", "C4_LANGUAGE_FINGERPRINT",
                  "C5_CRATER", "C6_BOARD_HALFSPLIT"):
            assert k in rep["readings"], k

    def test_thresholds_carried(self):
        rep = self._rep()
        r = rep["readings"]
        assert r["C1_GLOBAL_WITHIN_WORLD"]["threshold"]
        assert r["C2_KINSHIP_MIRROR"]["threshold"]
        assert r["C3_CONVERGENCE"]["threshold"] == 1.0
        assert r["C4_LANGUAGE_FINGERPRINT"]["threshold"]
        assert r["C5_CRATER"]["threshold"]
        assert r["C6_BOARD_HALFSPLIT"]["threshold"]

    def test_spec_embedded_and_caveats(self):
        rep = self._rep()
        assert len(rep["criteria_spec"]) == 6
        assert rep["caveats"] and any("自报" in c for c in rep["caveats"])
        assert rep["version"] == "xray-p4up/1.0"
        assert rep["_generated_at"].endswith("Z")

    def test_tape_profile_and_baseline(self):
        rep = self._rep()
        assert rep["tape_profile"]["p25"] is None   # 全同流无分叉
        assert rep["baseline_lookup"]["baseline_self_reported"] is True
        # 基线同口径（仅胜局）子画像：_rec(i) margin=i-1 → 6 胜局
        assert rep["tape_profile_wins_only"]["n_games"] == 6
        assert rep["baseline_lookup_wins_only"] is not None

    def test_trajectory_passthrough(self):
        rep = RR.build_report([_rec(i) for i in range(8)],
                              trajectory=[1000 + 10 * i for i in range(12)])
        assert rep["readings"]["C3_CONVERGENCE"]["verdict"] == "WARMING UP"

    def test_render_text_markers(self):
        text = RR.render_text(self._rep())
        for mk in ("[C1]", "[C2]", "[C3]", "[C4]", "[C5]", "[C6]", "[TAPE]"):
            assert mk in text, mk

    def test_empty_records(self):
        rep = RR.build_report([])
        assert "error" in rep["readings"]


class TestFeatsCrosscheck:
    def test_day0_crosscheck(self):
        row = {
            "src": "x.parquet", "episode_id": 1, "date": "2026-09-23",
            "teams": ["TFC", "B"], "seed": 1, "rewards": [1.0, 2.0],
            "n_steps": 720,
            "players": [
                {"team": "TFC", "pi": 0, "day0_24": [[["PASS"], []]] * 24},
                {"team": "B", "pi": 1, "day0_24": [[["PASS"], []]] * 24},
            ],
        }
        row2 = json.loads(json.dumps(row))
        row2["episode_id"] = 2
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "feats.jsonl")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(json.dumps(row) + "\n" + json.dumps(row2) + "\n")
            out = RR.feats_band_crosscheck(p, "TFC")
        assert out["n_episodes"] == 2
        assert out["cls"] == "PURE_REPLAY"      # day0 全同
        assert out["window"] == "day0 (t<24)"

    def test_single_episode_insufficient(self):
        row = {"src": "x", "episode_id": 1, "teams": ["T", "B"], "rewards": [1, 0],
               "players": [{"team": "T", "pi": 0, "day0_24": []},
                           {"team": "B", "pi": 1, "day0_24": []}]}
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "feats.jsonl")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(json.dumps(row) + "\n")
            out = RR.feats_band_crosscheck(p, "T")
        assert out["status"] == "INSUFFICIENT_DATA"


class TestCLI:
    def test_main_writes_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            recs_path = os.path.join(td, "recs.jsonl")
            with open(recs_path, "w", encoding="utf-8") as fh:
                for i in range(8):
                    fh.write(json.dumps(_rec(i).to_compact(),
                                        ensure_ascii=False) + "\n")
            out_path = os.path.join(td, "report.json")
            rc = RR.main(["--records", recs_path, "--out", out_path])
            assert rc == 0
            with open(out_path, encoding="utf-8") as fh:
                rep = json.load(fh)
            assert rep["version"] == "xray-p4up/1.0"
            assert os.path.exists(os.path.splitext(out_path)[0] + ".txt")
