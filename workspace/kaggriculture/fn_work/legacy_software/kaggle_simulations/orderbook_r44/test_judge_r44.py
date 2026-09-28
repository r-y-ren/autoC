# -*- coding: utf-8 -*-
"""R27 测试面：判决线（判据=R27 ②原文——判据阈值三分支/消融边际/安慰剂/
择优评分序/计分对注记）。安慰剂面用真实迷你 main 假件驱动（不跑真局）。"""
from __future__ import annotations

import pytest

from orderbook_r44 import judge_r44 as j44

ACT_BASE = {"farmer": ["PASS"], "hands": [], "market": []}

# r40 自打参考轨迹：step1=严格新高触发面；step2/3=非触发拍（零足迹判定点）
FACE_STATES = [
    (0, {"step": 0, "market": {"prices": {"EGG": 50, "WHEAT": 30}}}, ACT_BASE),
    (1, {"step": 1, "market": {"prices": {"EGG": 55}}}, ACT_BASE),
    (2, {"step": 2, "market": {"prices": {"EGG": 55}}}, ACT_BASE),
    (3, {"step": 3, "market": {"prices": {"EGG": 40}}}, ACT_BASE),
]

MAIN_IDENTICAL = (
    "def _glutgate_agent(observation, configuration=None):\n"
    "    return {'farmer': ['PASS'], 'hands': [], 'market': []}\n")
MAIN_TRIGGER_DIFF = (
    "def _dayhigh_agent(observation, configuration=None):\n"
    "    step = observation.get('step')\n"
    "    if step == 1:\n"
    "        return {'farmer': ['PASS'], 'hands': [],\n"
    "                'market': [['SELL', 'EGG', 1]]}\n"
    "    return {'farmer': ['PASS'], 'hands': [], 'market': []}\n")
MAIN_ROGUE_A = (
    "def _dayhigh_agent(observation, configuration=None):\n"
    "    step = observation.get('step')\n"
    "    if step == 3:\n"
    "        return {'farmer': ['PASS'], 'hands': [],\n"
    "                'market': [['SELL', 'EGG', 1]]}\n"
    "    return {'farmer': ['PASS'], 'hands': [], 'market': []}\n")
MAIN_ROGUE_B = MAIN_ROGUE_A.replace("_dayhigh_agent", "_glutgate_agent")


def _mains(tmp_path, a_body=MAIN_TRIGGER_DIFF, b_body=MAIN_IDENTICAL):
    out = {}
    for form, body in (("A", a_body), ("B", b_body), ("AB", b_body)):
        p = tmp_path / ("%s_main.py" % form.lower())
        p.write_text(body, encoding="utf-8")
        out[form] = str(p)
    return out


def _fake_runner(margins_by_arm, pxs_by_arm):
    """假判决跑口：按形态给 margin/实现价；face 局回灌参考轨迹。"""
    def _run(specs, cfg):
        rows = []
        for spec in specs:
            if spec.get("kind") == "face":
                rows.append({"game_id": spec["game_id"],
                             "seed": spec["seed"], "seat": 0, "arm": "face",
                             "kind": "face", "banks": [0.0, 0.0],
                             "error": None, "margin": 0.0, "reads": {},
                             "states": list(FACE_STATES)})
                continue
            arm = spec["arm"]
            mv = margins_by_arm.get(arm, 0.0)
            m = mv(spec["seed"], spec["our_seat"]) if callable(mv) else mv
            px = pxs_by_arm.get(arm, 0.0)
            rows.append({"game_id": spec["game_id"], "seed": spec["seed"],
                         "seat": spec["our_seat"], "arm": arm, "kind": "pair",
                         "banks": [0.0, 0.0], "error": None,
                         "margin": float(m),
                         "reads": {"realized_px": px,
                                   "terminal_money": 100000.0,
                                   "stranding": 0.0}, "states": None})
        return rows
    return _run


def _judge(monkeypatch, tmp_path, margins, pxs, n_seeds=20, name="ev.json",
           **cfg):
    mains = _mains(tmp_path)
    monkeypatch.setattr(j44, "_run_rows", _fake_runner(margins, pxs))
    return j44.judge_r44(mains, None, dict(
        {"n_seeds": n_seeds, "evidence_path": str(tmp_path / name)}, **cfg))


# ------------------------------------------------------------ 判据三分支 --
def test_judge_criteria_pass(monkeypatch, tmp_path):
    """过：A 臂三判据全达成+B 臂等价面恒等∧AB 边际>0→POSITIVE。"""
    ev = _judge(monkeypatch, tmp_path,
                {"A": 3000.0, "B": 3000.0, "AB": 3500.0},
                {"A": 0.85, "B": 0.85, "AB": 0.85})
    assert ev["criteria"]["A"]["verdict"] == "PASS"
    assert ev["criteria"]["A"]["achieved"] == 3
    assert ev["criteria"]["B"]["verdict"] == "PASS"      # 恒等+边际 500>0
    assert ev["criteria"]["AB"]["verdict"] == "PASS"
    assert ev["verdict"] == "POSITIVE"
    assert ev["placebo"]["b_equiv_face"]["value"] is True
    assert ev["placebo"]["a_zero_footprint"]["value"] is True
    pick = j44.pick_launch_form(ev)
    assert pick["launch_form"] == "AB"                    # 达成 4>3>2


def test_judge_criteria_fail(monkeypatch, tmp_path):
    """不过：带外/实现价低/h2h 红+AB 边际≤0→NEGATIVE（仪器未破防）。"""
    ev = _judge(monkeypatch, tmp_path,
                {"A": -500.0, "B": -500.0, "AB": -600.0},
                {"A": 0.7, "B": 0.7, "AB": 0.7})
    checks = ev["criteria"]["A"]["checks"]
    assert checks["realized_px_median"]["verdict"] == "FAIL"
    assert checks["terminal_money_delta"]["verdict"] == "FAIL"
    assert checks["h2h"]["verdict"] == "FAIL"
    assert ev["criteria"]["B"]["checks"]["ab_marginal"]["verdict"] == "FAIL"
    assert ev["criteria"]["AB"]["verdict"] == "FAIL"
    assert ev["verdict"] == "NEGATIVE"


def test_judge_threshold_edges(monkeypatch, tmp_path):
    """判据阈值三分支（过/不过/边际）：终局钱带 [2k,4k] 含端点、实现价
    0.80 恰线。"""
    cases = [
        (3000.0, 0.85, "PASS", "PASS"),    # 过
        (500.0, 0.70, "FAIL", "FAIL"),     # 不过
        (2000.0, 0.80, "PASS", "PASS"),    # 边际：带低缘+阈恰线（含端点）
        (4000.0, 0.80, "PASS", "PASS"),    # 边际：带高缘
        (1999.0, 0.85, "FAIL", "PASS"),
        (4001.0, 0.85, "FAIL", "PASS"),
        (3000.0, 0.79, "PASS", "FAIL"),
    ]
    for i, (m, px, exp_t, exp_px) in enumerate(cases):
        ev = _judge(monkeypatch, tmp_path,
                    {"A": m, "B": m, "AB": m + 500.0},
                    {"A": px, "B": px, "AB": px},
                    name="ev%d.json" % i)
        checks = ev["criteria"]["A"]["checks"]
        assert checks["terminal_money_delta"]["verdict"] == exp_t, (m,)
        assert checks["realized_px_median"]["verdict"] == exp_px, (px,)


def test_judge_h2h_boundary(monkeypatch, tmp_path):
    """h2h 边际：11/20=0.55 恰线过；10/20=0.5 不过（同 seed 双席折叠独立 n）。"""
    def win11(seed, seat):
        return 4000.0 if seed % 20 < 11 else -1.0

    def win10(seed, seat):
        return 4000.0 if seed % 20 < 10 else -1.0

    for i, (fn, exp, exp_val) in enumerate(
            ((win11, "PASS", 0.55), (win10, "FAIL", 0.5))):
        ev = _judge(monkeypatch, tmp_path,
                    {"A": fn, "B": fn, "AB": fn},
                    {"A": 0.85, "B": 0.85, "AB": 0.85},
                    name="h%d.json" % i)
        h = ev["criteria"]["A"]["checks"]["h2h"]
        assert h["verdict"] == exp
        assert h["value"] == exp_val
        assert ev["arms"][0]["n"] == 20                   # 独立 seed n


# -------------------------------------------------------------- 消融边际 --
def test_judge_ab_marginal_gate(monkeypatch, tmp_path):
    """单件消融：B 效应=AB vs A 边际；边际 0→B 臂红，A 臂仍可判正。"""
    ev = _judge(monkeypatch, tmp_path,
                {"A": 3000.0, "B": 3000.0, "AB": 3000.0},
                {"A": 0.85, "B": 0.85, "AB": 0.85})
    assert ev["ablation"]["b_effect"]["value"] == 0.0
    assert ev["criteria"]["B"]["checks"]["ab_marginal"]["verdict"] == "FAIL"
    assert ev["criteria"]["B"]["verdict"] == "FAIL"
    assert ev["criteria"]["A"]["verdict"] == "PASS"
    assert ev["verdict"] == "POSITIVE"


# ---------------------------------------------------------- 安慰剂（仪器）--
def test_judge_killed_on_placebo_breach(monkeypatch, tmp_path):
    """安慰剂破防→KILLED：A 非触发拍留痕、B 等价面不恒等各判一回。"""
    mains = _mains(tmp_path, a_body=MAIN_ROGUE_A, b_body=MAIN_IDENTICAL)
    monkeypatch.setattr(j44, "_run_rows", _fake_runner(
        {"A": 3000.0, "B": 3000.0, "AB": 3500.0},
        {"A": 0.85, "B": 0.85, "AB": 0.85}))
    ev = j44.judge_r44(mains, None, {"n_seeds": 20,
                                     "evidence_path": str(tmp_path / "k1")})
    assert ev["placebo"]["a_zero_footprint"]["value"] is False
    assert ev["verdict"] == "KILLED"
    pick = j44.pick_launch_form(ev)
    assert pick["launch_form"] is None                     # KILLED→全收档

    mains = _mains(tmp_path, a_body=MAIN_TRIGGER_DIFF, b_body=MAIN_ROGUE_B)
    monkeypatch.setattr(j44, "_run_rows", _fake_runner(
        {"A": 3000.0, "B": 3000.0, "AB": 3500.0},
        {"A": 0.85, "B": 0.85, "AB": 0.85}))
    ev = j44.judge_r44(mains, None, {"n_seeds": 20,
                                     "evidence_path": str(tmp_path / "k2")})
    assert ev["placebo"]["b_equiv_face"]["value"] is False
    assert ev["verdict"] == "KILLED"


# ---------------------------------------------------------- evidence 契约 --
def test_judge_evidence_contract(monkeypatch, tmp_path):
    ev = _judge(monkeypatch, tmp_path,
                {"A": 3000.0, "B": 3000.0, "AB": 3500.0},
                {"A": 0.85, "B": 0.85, "AB": 0.85}, n_seeds=12)
    assert ev["_generated_at"]
    assert isinstance(ev["source"]["commands"], list) \
        and ev["source"]["commands"]
    assert ev["source"]["seed_base"] == j44.SEED_BASE
    assert len(ev["source"]["seeds"]) == 12                # seed 登记
    assert [r["arm"] for r in ev["arms"]] == list(j44.FORMS)
    for row in ev["arms"]:
        assert set(row) == {"arm", "n", "wins", "losses", "ties",
                            "mean_margin"}
    assert set(ev["criteria"]) >= set(j44.FORMS) | {"placebo"}
    assert ev["verdict"] in ("POSITIVE", "NEGATIVE", "KILLED")


def test_judge_requires_three_forms():
    with pytest.raises(ValueError):
        j44.judge_r44({"A": "/tmp/a.py"}, None, {})


# ------------------------------------------------------------ 择优评分序 --
def _crit(achieved, h2h, px, verdict, total=4):
    return {"achieved": achieved, "total": total, "h2h": h2h,
            "realized_px": px, "verdict": verdict}


def test_pick_prefers_criteria_achieved_count():
    ev = {"verdict": "POSITIVE", "criteria": {
        "A": _crit(3, 0.9, 0.95, "PASS", total=3),
        "B": _crit(2, 0.9, 0.95, "PASS", total=2),
        "AB": _crit(4, 0.5, 0.5, "PASS")}}
    out = j44.pick_launch_form(ev)
    assert out["launch_form"] == "AB"                      # 达成数首要
    assert out["archived_forms"] == ["A", "B"]


def test_pick_h2h_then_realized_tiebreak():
    ev = {"verdict": "POSITIVE", "criteria": {
        "A": _crit(3, 0.60, 0.90, "PASS"),
        "B": _crit(3, 0.70, 0.80, "PASS"),
        "AB": _crit(3, 0.60, 0.85, "PASS")}}
    out = j44.pick_launch_form(ev)
    assert out["launch_form"] == "B"                       # 同达成→h2h
    ev = {"verdict": "POSITIVE", "criteria": {
        "A": _crit(3, 0.60, 0.82, "PASS"),
        "B": _crit(3, 0.60, 0.85, "PASS"),
        "AB": _crit(3, 0.60, 0.85, "FAIL")}}
    out = j44.pick_launch_form(ev)
    assert out["launch_form"] == "B"                       # 同 h2h→实现价
    assert "评分序" in out["rationale"]


def test_pick_form_order_final_tiebreak():
    ev = {"verdict": "POSITIVE", "criteria": {
        "A": _crit(3, 0.60, 0.85, "PASS"),
        "B": _crit(3, 0.60, 0.85, "PASS"),
        "AB": _crit(3, 0.60, 0.85, "PASS")}}
    out = j44.pick_launch_form(ev)
    assert out["launch_form"] == "A"                       # 全同→形态序定桩
    assert out["archived_forms"] == ["B", "AB"]


def test_pick_no_pass_archives_all():
    ev = {"verdict": "NEGATIVE", "criteria": {
        "A": _crit(1, 0.3, 0.6, "FAIL", total=3),
        "B": _crit(0, 0.3, 0.6, "FAIL", total=2),
        "AB": _crit(1, 0.3, 0.6, "FAIL")}}
    out = j44.pick_launch_form(ev)
    assert out["launch_form"] is None
    assert out["archived_forms"] == ["A", "B", "AB"]       # 全收档
    assert "全收档" in out["rationale"]


def test_pick_scoring_pair_note():
    ev = {"verdict": "NEGATIVE", "criteria": {}}
    out = j44.pick_launch_form(ev)
    assert out["scoring_pair"]["pair"] == ["r34a-new 56637411", "r44 本件"]
    assert "挤 r37 保 r40" in out["scoring_pair"]["note"]
