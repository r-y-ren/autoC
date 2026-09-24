# -*- coding: utf-8 -*-
"""R15 单测：run_mix_judgment（编排+KILLED 双短路+evidence schema 组，全 mock）。"""
import json

import pytest

from orderbook_mix_lab import run_mix_judgment as R


def _sel():
    return {
        "losses26": [{"episode": 1, "path": "/tmp/a.json", "seat": 0,
                      "res": "L", "margin": -100.0}],
        "wins10": [{"episode": 2, "path": "/tmp/b.json", "seat": 1,
                    "res": "W", "margin": 1000.0}],
        "mirror": [{"episode": 3, "path": "/tmp/c.json"}],
        "sampling": {"seed_material": "20260925r15",
                     "seed_derivation": "x", "picked_wins": {"r32": [2]},
                     "mirror_pool": [3], "picked_mirror": [3],
                     "note": None},
        "errors": [],
    }


def _mm(pairs):
    return {"params": {"low_pct": 35}, "base_prices": {"WHEAT": 25},
            "base_prices_from_engine": True, "crash_items": ["MELON"],
            "scarce_items": ["WHEAT"], "items": {},
            "swap_pairs_ranked": pairs, "capacity_windows": {},
            "n_games": 86, "n_ok": 86, "errors": []}


def _variants_ok():
    return {"variants": [{"id": "vA", "pair": {"from": "MELON",
                                               "to": "WHEAT"},
                          "scale": 0.3, "feasible": True,
                          "main_path": "/tmp/vA/main.py", "moved_n": 4,
                          "target_n": 4}],
            "dropped": [],
            "audit": {"n_points": 3, "n_variants": 1, "n_dropped": 2,
                      "scales": [0.3], "max_variants": 16,
                      "l3_base": "x", "primary_route": "100",
                      "feasible_zero": False,
                      "money_floor_curve_source": "losses_day_end_min"}}


def _open_ok():
    return {"control": {}, "control_reuse": {"reused": 0, "fresh": 6,
                                             "spot_drift": [], "ok": True},
            "per_variant": {"vA": {"id": "vA", "games": {
                "1": {"res": "L", "seats": {"seat0": {"delta": 10}},
                      "game_delta": 10, "red": False},
                "2": {"res": "W", "seats": {"seat1": {"delta": 2}},
                      "game_delta": 2, "red": False}}}},
            "summary": {"n_variants": 1, "n_run_variants": 1, "n_games": 2,
                        "n_replays": 9, "control_fresh": 3,
                        "control_reused": 0, "reuse_ok": True,
                        "spot_drift": [], "budget": 1100,
                        "budget_stopped": False, "wall_s": 1.0,
                        "r14_evidence_ts": None}}


@pytest.fixture
def patched(monkeypatch, tmp_path):
    st = {}
    monkeypatch.setattr(R.C, "select_corpus_r15",
                        lambda rd, ar=None: st.get("sel", _sel()))
    monkeypatch.setattr(R.M, "phase_m_market_map",
                        lambda rd: st.get("mm", _mm([{
                            "from": "MELON", "to": "WHEAT", "score": 29.0,
                            "pct_gap": 74.7, "from_capacity": 39.0}])))
    monkeypatch.setattr(
        R.VG, "generate_mix_variants",
        lambda pairs, scales=(0.1, 0.2, 0.3), max_variants=16,
               l3_main_path=None, out_dir=None, base_context=None:
            st.get("variants", _variants_ok()))
    monkeypatch.setattr(R.OL, "openloop_replay_variants",
                        lambda vs, corpus, l3, reuse_r14_control=True,
                               budget=1100, log=None:
                            st.get("open", _open_ok()))
    monkeypatch.setattr(R.CL, "closedloop_probe",
                        lambda vs, mirror, l3, log=None: st.get(
                            "closed", {"per_variant": {}, "summary": {
                                "n_variants": 0, "n_runs": 0, "wall_s": 0.1}}))
    monkeypatch.setattr(R.J, "judge_mix_verdicts",
                        lambda ol, cl=None, killed=False: st.get(
                            "judge", {"per_variant": {}, "overall": "NEGATIVE",
                                      "winning_variant": None,
                                      "sensitivity": {}, "fail_closed": False}))
    monkeypatch.setattr(R, "_money_floor_curve", lambda eps: [3000.0] * 30)
    return st


def test_orchestration_full_flow(patched, tmp_path, capsys):
    out = R.run_mix_judgment(replay_dir="/tmp/x", out_dir=str(tmp_path),
                             l3_main="L3")
    assert out["overall"] == "NEGATIVE"
    ev_path = tmp_path / "mix_judgment.json"
    assert ev_path.exists()
    ev = json.loads(ev_path.read_text("utf-8"))
    for key in ("source", "corpus", "phase_m", "variants", "openloop",
                "closedloop", "judge", "overall", "wall_s"):
        assert key in ev
    assert "rerun_command" in ev["source"] and ev["source"]["method_notes"]
    assert ev["corpus"]["losses26"] == [1] and ev["corpus"]["mirror"] == [3]
    capsys.readouterr()  # 控制台摘要不崩即可


def test_killed_shortcircuit_zero_pairs(patched, tmp_path):
    patched["mm"] = _mm([])
    out = R.run_mix_judgment(replay_dir="/tmp/x", out_dir=str(tmp_path),
                             l3_main="L3")
    assert out["overall"] == "KILLED"
    assert "零合格置换对" in out["judge"]["killed_reason"]
    assert out["variants"] is None and out["openloop"] is None


def test_killed_shortcircuit_zero_feasible(patched, tmp_path):
    var = _variants_ok()
    var["variants"] = []
    var["audit"]["feasible_zero"] = True
    var["audit"]["n_variants"] = 0
    patched["variants"] = var
    out = R.run_mix_judgment(replay_dir="/tmp/x", out_dir=str(tmp_path),
                             l3_main="L3")
    assert out["overall"] == "KILLED"
    assert "全部参数点不可行" in out["judge"]["killed_reason"]
    assert out["openloop"] is None


def test_fail_closed_s1(patched, tmp_path):
    sel = _sel()
    sel["errors"] = [{"episode": 9, "error": "缺回放件"}]
    patched["sel"] = sel
    out = R.run_mix_judgment(replay_dir="/tmp/x", out_dir=str(tmp_path),
                             l3_main="L3")
    assert out["overall"] == "FAIL" and "S1 fail-closed" in out["error"]


def test_closedloop_runs_for_openloop_positive(patched, tmp_path):
    st = patched
    st["judge"] = {"per_variant": {"vA": {"openloop_positive": True}},
                   "overall": "POSITIVE", "winning_variant": "vA",
                   "sensitivity": {}, "fail_closed": False}
    # 编排筛 POSITIVE 变体：monkeypatch J.variant_openloop_positive
    import orderbook_mix_lab.judge_mix as JM
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(JM, "variant_openloop_positive",
                        lambda games: (True, {"n_loss": 1}))
    monkeypatch.setattr(R.J, "variant_openloop_positive",
                        lambda games: (True, {"n_loss": 1}))
    called = {"cl": 0}
    st["closed"] = {"per_variant": {"vA": {"rate": 0.5, "median_margin": 10,
                                           "wins": 4, "runs": 8,
                                           "red_runs": 0}},
                    "summary": {"n_variants": 1, "n_runs": 8, "wall_s": 0.1}}

    def cl_spy(vs, mirror, l3, log=None):
        called["cl"] += 1
        assert [v["id"] for v in vs] == ["vA"]
        return st["closed"]

    monkeypatch.setattr(R.CL, "closedloop_probe", cl_spy)
    try:
        out = R.run_mix_judgment(replay_dir="/tmp/x", out_dir=str(tmp_path),
                                 l3_main="L3")
        assert called["cl"] == 1
        assert out["closedloop"]["per_variant"]["vA"]["rate"] == 0.5
    finally:
        monkeypatch.undo()
