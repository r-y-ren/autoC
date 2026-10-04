"""run_m1_m2_gates 真实测试（R6：M1 互胜门 + M2 五线）。

通道全注入（tmp 假件）：假引擎局/假 seated rollout/假四门；语料选取
规则（巨人锚局+强扩展轮转/最窄胜局回归/经济面普通局）为纯函数直接
实测；分档（GATES_PASS / BELOW_LINE / PIPELINE_BROKEN）逐档验证。
"""

import json

import pytest
from assemble_and_gate.run_m1_m2_gates import (
    COUNTS,
    GIANT_ANCHORS,
    THRESHOLDS,
    _income_curve,
    run_m1_m2_gates,
    select_economic_games,
    select_giant_games,
    select_regression_games,
)

_CAND = "/tmp/fake-cand-main.py"
_BASE = "/tmp/fake-base-main.py"


def _write_replay(tmp_path, ep):
    path = tmp_path / f"episode-{ep}-replay.json"
    path.write_text(json.dumps({"ep": ep}), encoding="utf-8")
    return str(path)


def _fake_corpus(tmp_path):
    """假语料：三巨人锚局 + 每巨人 2 强扩展（r26 败局 ≤−20k）+ 8 窄胜局
    + 普通局若干（含镜像/巨人其他局变体）。"""
    games = []

    def add(ep, round_, opp, margin, me_seat=0):
        games.append({"ep": ep, "round": round_, "me_seat": me_seat,
                      "opp": opp, "margin": float(margin),
                      "result": "W" if margin > 0 else (
                          "L" if margin < 0 else "T"),
                      "mirror": opp == "renyxin",
                      "replay_path": _write_replay(tmp_path, ep)})

    add(111653327, "round26", "statma", -36154, 1)     # 锚 statma
    add(111877080, "round27", "fuxi", -27083, 0)       # 锚 fuxi
    add(111898825, "round27", "42", -25075, 0)         # 锚 42
    # 强扩展池（round26 败局 ≤−20k，锚局除外）——最负优先
    add(900001, "round26", "SA", -50000)
    add(900002, "round26", "SB", -45000)
    add(900003, "round26", "SC", -40000)
    add(900004, "round26", "SD", -35000)
    add(900005, "round26", "SE", -30000)
    add(900006, "round26", "SF", -25000)
    add(900007, "round26", "WEAK_L", -5000)            # 不入池
    add(900008, "round27", "r27L", -60000)             # 非池来源轮
    # 胜局（回归集按 margin 最窄 8 局）
    for i, margin in enumerate((120, 200, 300, 400, 500, 600, 700, 800,
                                9000, 50000), start=1):
        add(910000 + i, "round26", f"W{i}", margin)
    # 普通局（经济面）
    for i in range(8):
        add(920000 + i, "round28", f"N{i}", -100 - i)
    add(930001, "round28", "renyxin", 1)               # 镜像剔除
    return games


def _runners_with(win_script, giant_ok=True, reg_delta=0.0,
                  econ_peak=13000.0, fourgate_pass=True):
    """假通道：h2h 胜负按 (seed, seat) 脚本；seated 按对手臂定制边际。"""
    def loader(path):
        return f"agent:{path}"

    def engine_game(fn0, fn1, seed):
        cand_seat = 0 if fn0.startswith("agent:" + _CAND) else 1
        won = win_script.get((seed, cand_seat), False)
        me = 20000.0 if won else 10000.0
        pair = [me, me]
        pair[cand_seat], pair[1 - cand_seat] = (30000.0, 10000.0) if won \
            else (10000.0, 30000.0)
        return {"rewards": pair, "statuses": ["DONE", "DONE"],
                "turns_played": 720, "suspicious_log_lines": []}

    def seated(replay, me_seat, agent, track=False):
        ep = replay["ep"]
        is_cand = agent.startswith("agent:" + _CAND)
        margin = 500.0 - reg_delta if is_cand else 500.0
        if ep in {a for _, a in GIANT_ANCHORS}:
            margin = 800.0 if (is_cand and giant_ok) else -5000.0
        out = {"finals": [15000.0, 14000.0],
               "margin": margin, "steps": 719}
        if track:
            out["peak_d14_17"] = econ_peak if is_cand else 0.0
            out["peak_day"] = 15
            out["season_peak"] = econ_peak if is_cand else 0.0
            out["season_peak_day"] = 15
        return out

    def fourgate(payload):
        return {"all_gates_pass": fourgate_pass,
                "passed": fourgate_pass}

    return {"load_agent": loader, "engine_game": engine_game,
            "seated": seated, "fourgate": fourgate}


def _win_script_all(wins):
    """16 局（8 种子 × 2 席）胜局脚本。"""
    seeds = (101, 102, 103, 104, 201, 202, 203, 204)
    keys = [(seed, seat) for seat in (0, 1) for seed in seeds]
    return {key: (i < wins) for i, key in enumerate(keys)}


def _payload(tmp_path, runners):
    return {"package_main": _CAND, "package_tar": "/tmp/fake.tar.gz",
            "base_main": _BASE, "output_dir": str(tmp_path / "gates"),
            "corpus": _fake_corpus(tmp_path), "runners": runners}


def test_m1_m2_all_pass_grading(tmp_path):
    runners = _runners_with(_win_script_all(11))     # 11/16=0.6875
    report = run_m1_m2_gates(_payload(tmp_path, runners))
    m1 = report["m1"]
    assert m1["games"] == 16
    assert m1["win_rate_half_ties"] == 0.6875
    assert m1["win_fraction_strict"] == 0.6875
    assert m1["passed"] is True
    for key in ("h2h", "giants", "regression", "fourgate", "econ"):
        line = report["m2"]["lines"][key]
        assert line["error"] is None, line
        assert line["passed"] is True, (key, line)
    assert report["grading"]["overall"] == "GATES_PASS"


def test_below_line_grading_distinguishes_lines(tmp_path):
    runners = _runners_with(_win_script_all(8))      # 0.5<0.65, ≥0.45
    report = run_m1_m2_gates(_payload(tmp_path, runners))
    assert report["m1"]["passed"] is True            # M1 0.5 ≥ 0.45
    h2h = report["m2"]["lines"]["h2h"]
    assert h2h["passed"] is False                    # M2 线一 0.5 < 0.65
    assert report["grading"]["overall"] == "BELOW_LINE"
    assert "h2h" in report["grading"]["failed_lines"]


def test_giant_line_fail_registers_below_line(tmp_path):
    runners = _runners_with(_win_script_all(11), giant_ok=False)
    report = run_m1_m2_gates(_payload(tmp_path, runners))
    assert report["m2"]["lines"]["giants"]["passed"] is False
    assert report["grading"]["overall"] == "BELOW_LINE"


def test_regression_tolerance_and_flip(tmp_path):
    # 候选臂比 v48 臂差 2500（>1000 宽限）→ 回归线 FAIL
    runners = _runners_with(_win_script_all(11), reg_delta=2500.0)
    report = run_m1_m2_gates(_payload(tmp_path, runners))
    line = report["m2"]["lines"]["regression"]
    assert line["passed"] is False
    assert line["result"]["n_ok"] == 0
    assert report["grading"]["overall"] == "BELOW_LINE"


def test_econ_below_gate_fails_line(tmp_path):
    runners = _runners_with(_win_script_all(11), econ_peak=12000.0)
    report = run_m1_m2_gates(_payload(tmp_path, runners))
    line = report["m2"]["lines"]["econ"]
    assert line["passed"] is False
    assert line["result"]["best_peak_d14_17"] == 12000.0


def test_engine_error_grades_pipeline_broken(tmp_path):
    def engine_boom(fn0, fn1, seed):
        raise RuntimeError("engine gone")

    runners = _runners_with(_win_script_all(11))
    runners["engine_game"] = engine_boom
    report = run_m1_m2_gates(_payload(tmp_path, runners))
    assert report["grading"]["overall"] == "PIPELINE_BROKEN"
    assert report["m1"] is None
    assert report["m2"]["lines"]["h2h"]["runnable"] is False
    assert "engine" in report["m2"]["lines"]["h2h"]["error"]
    # 其余线不受牵连照常裁决
    assert report["m2"]["lines"]["giants"]["passed"] is True


def test_fourgate_fail_below_line(tmp_path):
    runners = _runners_with(_win_script_all(11), fourgate_pass=False)
    report = run_m1_m2_gates(_payload(tmp_path, runners))
    assert report["m2"]["lines"]["fourgate"]["passed"] is False
    assert report["grading"]["overall"] == "BELOW_LINE"


def test_report_canonical_strips_walls_and_writes(tmp_path):
    runners = _runners_with(_win_script_all(11))
    payload = _payload(tmp_path, runners)
    report = run_m1_m2_gates(payload)
    text = (tmp_path / "gates" / "m1m2_report.json").read_text(
        encoding="utf-8")
    assert "wall_s" not in text
    assert report["paths"]["report"].endswith("m1m2_report.json")
    assert (tmp_path / "gates" / "m1m2_runtime.json").exists()


def test_canonical_strip_covers_fourgate_timing_telemetry():
    """四门 gate2 的 max/mean/p99_step_ms 是墙钟派生测量——双跑必抖，
    必须剥离（真管线 double-run mismatch 的实证根因）。"""
    from assemble_and_gate.run_m1_m2_gates import _strip_walls
    noisy = {"gate2_episodes": [
        {"rewards": [1.0, 2.0], "wall_s": 3.4, "max_step_ms": 4.27,
         "mean_step_ms": 0.22, "p99_step_ms": 0.59}], "ok": True}
    clean = _strip_walls(noisy)
    assert clean == {"gate2_episodes": [{"rewards": [1.0, 2.0]}],
                     "ok": True}


def test_select_giant_games_rule(tmp_path):
    games = _fake_corpus(tmp_path)
    by_name = select_giant_games(games)
    for name in ("statma", "fuxi", "42"):
        picks = by_name[name]
        assert len(picks) >= COUNTS["giant_per_name_min"]
        assert any(g["opp"] == name for g in picks)      # 锚局在内
    # 强扩展按严重度轮转：statma→最负 2 局，fuxi→次 2 局，42→再次 2 局
    eps = [g["ep"] for g in by_name["statma"]
           if g["opp"] not in ("statma",)]
    assert 900001 in eps and 900002 in eps
    eps42 = [g["ep"] for g in by_name["42"] if g["opp"] != "42"]
    assert 900005 in eps42 and 900006 in eps42


def test_select_regression_narrowest_wins(tmp_path):
    games = _fake_corpus(tmp_path)
    picks = select_regression_games(games)
    assert len(picks) == COUNTS["reg_n"]
    margins = [g["margin"] for g in picks]
    assert margins == sorted(margins)
    # 最窄 8 局：镜像 W(1.0) + 120..700（先例口径回归集不剔镜像）
    assert max(margins) == 700.0


def test_select_economic_ordinary_exclusions(tmp_path):
    games = _fake_corpus(tmp_path)
    picks = select_economic_games(games)
    assert len(picks) == COUNTS["econ_n"]
    taken = ({ep for _, ep in GIANT_ANCHORS}
             | {g["ep"] for g in games
                if g["round"] == "round26" and g["result"] == "L"
                and g["margin"] <= -20000.0}
             | {g["ep"] for g in select_regression_games(games)})
    assert all(g["ep"] not in taken and not g["mirror"]
               and g["opp"] not in ("statma", "fuxi", "42")
               for g in picks)
    eps = [g["ep"] for g in picks]
    assert eps == sorted(eps)


def test_income_curve_and_window():
    # series[j] = 第 j 步行动前资金；d14 内每步净增 1000 → d14 毛收入 24k
    series = [0.0] * (30 * 24 + 1)
    for j in range(336, 361):
        series[j] = 1000.0 * (j - 336)
    curve = _income_curve(series)
    assert curve[13] == 0.0
    assert curve[14] == 24000.0
    assert curve[15] == 0.0
    lo, hi = 14, 18
    assert max(curve[lo:hi]) == 24000.0
