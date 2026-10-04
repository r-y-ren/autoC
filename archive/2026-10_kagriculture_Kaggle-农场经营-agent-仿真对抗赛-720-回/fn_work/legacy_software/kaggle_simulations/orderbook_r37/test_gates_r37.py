# -*- coding: utf-8 -*-
"""R19/R20 测试面：gates_r37（四门+h2h≥0.55 独立 n 报+饿死零容忍+谱系）。"""
import json

import pytest

from orderbook_r37 import gates_r37 as G


@pytest.fixture()
def fake_pkg(tmp_path):
    pkg = tmp_path / "r37"
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
            "mean_margin": 100.0, "per_opponent": {},
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
        "h2h": "_gate_h2h_vs_r34a",
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
    summary = G.verify_r37_gates(str(fake_pkg / "main.py"), evidence_dir=str(ev))
    assert summary["overall"] is True
    assert set(summary["gates_passed"].values()) == {True}
    assert summary["gates_passed"] == {
        "compliance": True, "launch": True, "h2h_vs_r34a": True,
        "lineage": True, "starve": True}
    on_disk = json.loads((ev / G.SUMMARY_NAME).read_text())
    assert on_disk["protocol"] == "verify-r37/1.0"
    assert on_disk["overall"] is True
    assert "verify_r37_gates" in on_disk["source"]["rerun_command"]
    assert summary["mains"]["last_callable"] == G.R37_LAST_CALLABLE


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
    summary = G.verify_r37_gates(str(fake_pkg), evidence_dir=str(tmp_path / "ev"))
    assert called == ["compliance", "launch", "h2h", "lineage", "starve"]
    assert summary["overall"] is False
    assert summary["gates_passed"]["launch"] is False
    assert summary["gates_passed"]["lineage"] is False
    assert summary["gates_passed"]["starve"] is True
    assert summary["gates"]["h2h_vs_r34a"]["executed"] is True


def test_fail_closed_gate_raises(fake_pkg, tmp_path, monkeypatch):
    """③ fail-closed：门抛→记录+红，其余门照跑，overall=False。"""
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
    summary = G.verify_r37_gates(str(fake_pkg), evidence_dir=str(tmp_path / "ev"))
    assert called == ["compliance", "launch", "h2h", "lineage", "starve"]
    launch = summary["gates"]["launch"]
    assert launch["executed"] is False and launch["passed"] is False
    assert "RuntimeError: boom" in launch["error"]
    starve = summary["gates"]["starve"]
    assert starve["executed"] is False and starve["passed"] is False
    assert "SystemExit" in starve["error"]
    assert summary["overall"] is False


def test_h2h_independent_n_seat_flips_not_double_counted(tmp_path, monkeypatch):
    """④ h2h 判据按独立 n 算（席位翻转不双计）：run 级 0.75 绿但 seed 级 0.5 红。"""
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

    def fake_run(l1_main, verbatim_main, seeds=None, evidence_path=None,
                 l1_expected_names=None, verbatim_expected_names=None):
        assert set(l1_expected_names) == {G.R37_LAST_CALLABLE}
        assert set(verbatim_expected_names) == {G.R34A_LAST_CALLABLE}
        assert verbatim_main == G.R34A_MAIN
        return {"passed": True, "n": 16, "wins": 8, "losses": 0, "ties": 8,
                "rate": 0.75, "mean_margin": 50.0, "per_game": per_game,
                "evidence_path": evidence_path}

    monkeypatch.setattr(G._h2h_base, "run", fake_run)
    res = G._gate_h2h_vs_r34a("/x/main.py", str(tmp_path / "h2h.json"))
    assert res["passed"] is False          # 判据跟独立 n 走，不跟 run 级
    assert res["n"] == 8 and res["rate"] == 0.5
    assert res["run_level"]["rate"] == 0.75

    # 反向：8 seed 两席皆胜 → seed 级 1.0 过门（独立 n=8）
    win_games = [{"seed": s, "cand_seat": seat, "statuses": ["DONE", "DONE"],
                  "winner": "cand", "rewards": [1.0, 0.0], "margin": 1.0}
                 for s in range(101, 109) for seat in (0, 1)]
    summary = G._seed_level_summary(win_games)
    assert summary["n"] == 8 and summary["rate"] == 1.0
    assert summary["seed_outcomes"]["win"] == 8


def test_verify_requires_built_main(tmp_path):
    with pytest.raises(G.GateR37Error):
        G.verify_r37_gates(str(tmp_path), evidence_dir=str(tmp_path / "ev"))


def test_official_call_argcount_truncation():
    """官方 runner 入参截断语义：单参件收单参、双参件收双参、__name__ 透传。"""
    seen = {}

    def one(obs):
        seen["one"] = obs
        return {"a": 1}

    def two(obs, configuration=None):
        seen["two"] = (obs, configuration)
        return {"a": 2}

    w1, w2 = G._OfficialCall(one), G._OfficialCall(two)
    assert w1.__name__ == "one" and w2.__name__ == "two"
    assert w1("o1", {"cfg": 1}) == {"a": 1} and seen["one"] == "o1"
    assert w2("o2", {"cfg": 2}) == {"a": 2}
    assert seen["two"] == ("o2", {"cfg": 2})
