# -*- coding: utf-8 -*-
"""R23 测试面：gates_r40（五门 R37-R39 管线重定向 fail-closed）。

4 例沿 B24 先例（orderbook_predict/test_gates_r38.py）：①全绿路 ②任一门红→
overall=False 且全跑不短路 ③fail-closed（门抛记红不逃逸；含剥块重算 helper
坏锚态）④h2h 独立 n 席位不双计（含辅对 r34a 不进门槛）。
"""
import hashlib
import json

import pytest

from orderbook_r40 import gates_r40 as G


@pytest.fixture()
def fake_pkg(tmp_path):
    pkg = tmp_path / "r40"
    pkg.mkdir()
    (pkg / "main.py").write_text("def agent(o, c=None):\n    return {}\n")
    (pkg / "submission.tar.gz").write_bytes(b"tar")
    (pkg / "build_manifest.json").write_text("{}")
    return pkg


def _gate(result_overrides=None, raise_exc=None):
    base = {"passed": True, "gates": {"load": True, "full_episodes": True,
                                      "determinism": True, "package": True},
            "axes": {}, "n": 8, "n_games": 16, "rate": 1.0,
            "threshold": G.H2H_WIN_THRESHOLD, "counting": "independent-seed",
            "seed_outcomes": {"win": 8, "draw": 0, "loss": 0, "incomplete": 0},
            "decided": 8, "run_level": {"rate": 1.0}, "all_done": True,
            "mean_margin": 100.0,
            "aux_vs_r34a": {"recorded": False, "gating": False},
            "per_opponent": {},
            "starve_free": True, "n_errors": 0, "n_starve_red_games": 0,
            "subset": True, "evidence_path": "/tmp/ev.json"}

    def thunk(*a, **k):
        if raise_exc:
            raise raise_exc
        out = dict(base)
        out.update(result_overrides or {})
        return out
    return thunk


def _patch_all(monkeypatch, **overrides):
    """五门全桩；overrides 按名换门（compliance/launch/h2h/lineage/starve）。"""
    mapping = {
        "compliance": "_gate_compliance",
        "launch": "_gate_launch_fourgate",
        "h2h": "_gate_h2h_vs_r37",
        "lineage": "_gate_lineage",
        "starve": "_gate_starve",
    }
    for key, attr in mapping.items():
        monkeypatch.setattr(G, attr, overrides.get(key, _gate()))
    monkeypatch.setattr(G, "_verify_ref_package",
                        lambda d, w: {"what": w, "match": True})


def test_verify_all_green_path(fake_pkg, tmp_path, monkeypatch):
    """① 全绿路：五门 monkeypatch 全绿 → overall=True，summary 落 tmp evidence。"""
    _patch_all(monkeypatch)
    ev = tmp_path / "ev"
    summary = G.verify_r40_gates(str(fake_pkg / "main.py"), evidence_dir=str(ev))
    assert summary["overall"] is True
    assert set(summary["gates_passed"].values()) == {True}
    assert summary["gates_passed"] == {
        "compliance": True, "launch": True, "h2h_vs_r37": True,
        "lineage": True, "starve": True}
    on_disk = json.loads((ev / G.SUMMARY_NAME).read_text())
    assert on_disk["protocol"] == "verify-r40/1.0"
    assert on_disk["overall"] is True
    assert "verify_r40_gates" in on_disk["source"]["rerun_command"]
    assert summary["mains"]["last_callable"] == G.R40_LAST_CALLABLE
    assert summary["mains"]["last_callable"] == "_route40_agent"


def test_any_red_overall_false_no_shortcircuit(fake_pkg, tmp_path, monkeypatch):
    """② 任一门红→overall=False 且全跑不短路（计数证明：五门逐一跑到）。"""
    called = []

    def wrap(name, thunk):
        def inner(*a, **k):
            called.append(name)
            return thunk(*a, **k)
        return inner

    _patch_all(monkeypatch,
               compliance=wrap("compliance", _gate()),
               launch=wrap("launch", _gate({"passed": False})),
               h2h=wrap("h2h", _gate()),
               lineage=wrap("lineage", _gate({"passed": False})),
               starve=wrap("starve", _gate()))
    summary = G.verify_r40_gates(str(fake_pkg), evidence_dir=str(tmp_path / "ev"))
    assert called == ["compliance", "launch", "h2h", "lineage", "starve"]
    assert summary["overall"] is False
    assert summary["gates_passed"]["launch"] is False
    assert summary["gates_passed"]["lineage"] is False
    assert summary["gates_passed"]["starve"] is True
    assert summary["gates"]["h2h_vs_r37"]["executed"] is True


def test_fail_closed_gate_raises(fake_pkg, tmp_path, monkeypatch):
    """③ fail-closed：门抛→记录+红，其余门照跑；剥块重算坏锚即抛不造假。"""
    called = []

    def wrap(name, thunk):
        def inner(*a, **k):
            called.append(name)
            return thunk(*a, **k)
        return inner

    _patch_all(monkeypatch,
               compliance=wrap("compliance", _gate()),
               launch=wrap("launch", _gate(raise_exc=RuntimeError("boom"))),
               h2h=wrap("h2h", _gate()),
               lineage=wrap("lineage", _gate()),
               starve=wrap("starve", _gate(raise_exc=SystemExit(2))))
    summary = G.verify_r40_gates(str(fake_pkg), evidence_dir=str(tmp_path / "ev"))
    assert called == ["compliance", "launch", "h2h", "lineage", "starve"]
    launch = summary["gates"]["launch"]
    assert launch["executed"] is False and launch["passed"] is False
    assert "RuntimeError: boom" in launch["error"]
    starve = summary["gates"]["starve"]
    assert starve["executed"] is False and starve["passed"] is False
    assert "SystemExit" in starve["error"]
    assert summary["overall"] is False

    # 剥块重算 helper（血统 tie 自证口径）：缺锚/多锚/分隔畸形 fail-closed
    core = G.BLOCK_ANCHOR.encode("utf-8")
    with pytest.raises(G.GateR40Error, match="期望恰 1"):
        G._block_prefix_sha(b"no anchor here")
    with pytest.raises(G.GateR40Error, match="期望恰 1"):
        G._block_prefix_sha(b"a " + core + b"\n\nx " + core + b"\n")
    with pytest.raises(G.GateR40Error, match="分隔畸形"):
        G._block_prefix_sha(b"prefix one-nl\n# " + core + b"\n")
    good = b"prefix-bytes\n" + b"\n\n# " + core + b" tail\n"
    assert G._block_prefix_sha(good) == hashlib.sha256(
        b"prefix-bytes\n").hexdigest()


def test_h2h_independent_n_seat_flips_not_double_counted(tmp_path, monkeypatch):
    """④ h2h 判据按独立 n 算（席位翻转不双计）+辅对 r34a 记录不进门槛。"""
    per_game = []
    for seed in range(101, 109):
        for seat, winner in ((0, "cand"), (1, "tie")):
            per_game.append({"seed": seed, "cand_seat": seat,
                             "statuses": ["DONE", "DONE"], "winner": winner,
                             "rewards": [1.0, 0.0], "margin": 1.0})
    summary = G._seed_level_summary(per_game)
    assert summary["n_games"] == 16          # 双席 16 局
    assert summary["n"] == 8                 # 独立局数 n=seed 数，不双计
    assert summary["run_rate"] == 0.75       # run 级互胜率（不作判据）
    assert summary["rate"] == 0.5            # seed 级：8 平→(0+0.5*8)/8
    assert summary["seed_outcomes"] == {"win": 0, "draw": 8, "loss": 0,
                                        "incomplete": 0}

    aux_loss = [{"seed": s, "cand_seat": seat, "statuses": ["DONE", "DONE"],
                 "winner": "opp", "rewards": [0.0, 1.0], "margin": -1.0}
                for s in range(101, 109) for seat in (0, 1)]
    calls = []

    def fake_run(l1_main, verbatim_main, seeds=None, evidence_path=None,
                 l1_expected_names=None, verbatim_expected_names=None):
        assert set(l1_expected_names) == {G.R40_LAST_CALLABLE}
        if verbatim_main == G.R37_MAIN:
            assert set(verbatim_expected_names) == {G.R37_LAST_CALLABLE}
            calls.append("main")
            return {"passed": True, "n": 16, "wins": 8, "losses": 0, "ties": 8,
                    "rate": 0.75, "mean_margin": 50.0, "per_game": per_game,
                    "evidence_path": evidence_path}
        assert verbatim_main == G.R34A_MAIN
        assert set(verbatim_expected_names) == {G.R34A_LAST_CALLABLE}
        calls.append("aux")
        return {"passed": False, "n": 16, "wins": 0, "losses": 16, "ties": 0,
                "rate": 0.0, "mean_margin": -50.0, "per_game": aux_loss,
                "evidence_path": evidence_path}

    monkeypatch.setattr(G._h2h_base, "run", fake_run)
    res = G._gate_h2h_vs_r37("/x/main.py", str(tmp_path / "h2h.json"),
                             aux_r34a=True)
    assert calls == ["main", "aux"]
    assert res["passed"] is False          # 判据跟独立 n 走，不跟 run 级
    assert res["n"] == 8 and res["rate"] == 0.5
    assert res["run_level"]["rate"] == 0.75
    aux = res["aux_vs_r34a"]               # 辅对红只记录，不进门槛
    assert aux["gating"] is False and aux["recorded"] is True
    assert aux["rate"] == 0.0

    # 反向：8 seed 两席皆胜 → seed 级 1.0 过门（独立 n=8），辅对全负不拖红
    win_games = [{"seed": s, "cand_seat": seat, "statuses": ["DONE", "DONE"],
                  "winner": "cand", "rewards": [1.0, 0.0], "margin": 1.0}
                 for s in range(101, 109) for seat in (0, 1)]
    summary = G._seed_level_summary(win_games)
    assert summary["n"] == 8 and summary["rate"] == 1.0
    assert summary["seed_outcomes"]["win"] == 8

    def fake_run_green_main(l1_main, verbatim_main, seeds=None,
                            evidence_path=None, l1_expected_names=None,
                            verbatim_expected_names=None):
        main_pair = verbatim_main == G.R37_MAIN
        calls.append("main" if main_pair else "aux")
        games = win_games if main_pair else aux_loss
        return {"passed": True, "n": 16, "wins": 8, "losses": 0, "ties": 0,
                "rate": 1.0, "mean_margin": 50.0, "per_game": games,
                "evidence_path": evidence_path}

    monkeypatch.setattr(G._h2h_base, "run", fake_run_green_main)
    calls.clear()
    res = G._gate_h2h_vs_r37("/x/main.py", str(tmp_path / "h2h.json"),
                             aux_r34a=True)
    assert calls == ["main", "aux"]
    assert res["passed"] is True and res["n"] == 8 and res["rate"] == 1.0
    assert res["aux_vs_r34a"]["rate"] == 0.0
    assert res["aux_vs_r34a"]["gating"] is False

    # 辅对可选（缺省关）：只跑主对，aux 记 recorded=False 且不影响判据
    calls.clear()
    res = G._gate_h2h_vs_r37("/x/main.py", str(tmp_path / "h2h.json"))
    assert calls == ["main"]
    assert res["aux_vs_r34a"] == {"recorded": False, "gating": False,
                                 "note": "辅对 r34a 可选记录未启用（不进门槛）"}
    assert res["passed"] is True
