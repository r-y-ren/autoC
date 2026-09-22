# -*- coding: utf-8 -*-
"""lead_protection_gates 真实测试（F4c：占位改真实，2026-09-22）。

三个覆盖面（tmp 语料小样，不依赖 /tmp/r26full、不装载真实 v5/v4b 包）：
1) 重演计算管线：tmp 小语料（孪生短季合成 + CORPUS.md 清单 + 最小投影
   形态回放件）——磁带跟随 callable 注入 → 重演终局与回放 rewards 逐位
   一致（注入点=峰值日起始步、席位、margin 计算全链路）；换分叉动作
   → 终局改变。语料缺失/CORPUS 缺失 fail-closed。
2) 等价比较器：构造短季局与回放注入局，v5==v4b（同 callable）→ 动作流
   逐字节一致；v5!=v4b → 分叉被捕获（identical=False、first_diffs 空否）。
3) 裁决 schema：_assemble_verdict 键契约与判据接线（wins>=7/14、非触发
   局>=8 且全同、任一门不可执行=整体 FAIL）。
"""
from __future__ import annotations

import json
import os
import sys

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_HYB = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import gate_common as gc                      # noqa: E402
import lead_protection_gates as lpg           # noqa: E402


PASS_ACT = {"farmer": ["PASS"], "hands": [], "market": []}
BUY_ACT = {"farmer": ["PASS"], "hands": [],
           "market": [["BUY_PRODUCT", "WHEAT", 2]]}


def _pass_agent(obs):
    return json.loads(json.dumps(PASS_ACT))


def _buy_agent(obs):
    return json.loads(json.dumps(BUY_ACT))


def _scripted_agent(buy):
    """确定性脚本策略：按 step 节律在 BUY/PASS 间切换（流非平凡）。"""
    def fn(obs):
        step = int(obs.get("step", 0) or 0)
        return json.loads(json.dumps(BUY_ACT if buy and step % 48 < 24
                                      else PASS_ACT))
    return fn


def _tapes_and_replay(seed, seat_fns, steps=72):
    """短季孪生自打（最小投影形态回放 + 双席动作磁带 + 终局）。"""
    from kaggle_simulations.agent.planner import twin
    head = gc.synthetic_season_head(seed, steps)
    state = twin.new_state_from_replay_head(head)
    replay = json.loads(json.dumps(head))
    tapes = [[], []]
    taken = 0
    while not state.env.done and taken < steps:
        pair = []
        for seat, fn in enumerate(seat_fns):
            action = json.loads(json.dumps(
                fn(state.seats[seat].observation)))
            tapes[seat].append(action)
            pair.append(action)
        twin.step(state, pair)
        replay["steps"].append([{"action": pair[0]}, {"action": pair[1]}])
        taken += 1
    finals = twin.final_money(state)
    replay["rewards"] = finals
    return replay, tapes, finals


def _write_tiny_corpus(root, games):
    """games: [(ep, me_seat, peak_day, replay, finals)] → CORPUS.md + 回放件。"""
    os.makedirs(root, exist_ok=True)
    rows = []
    for ep, me_seat, peak_day, replay, finals in games:
        with open(os.path.join(root, f"episode-{ep}-replay.json"), "w",
                  encoding="utf-8") as h:
            json.dump(replay, h, ensure_ascii=False)
        margin = finals[me_seat] - finals[1 - me_seat]
        rows.append(f"| {ep} | TestOpp | {me_seat} | {margin:.1f} | "
                    f"{finals[1 - me_seat]:.1f} | test | d{peak_day} | "
                    f"100.0 | 12345 |")
    with open(os.path.join(root, "CORPUS.md"), "w", encoding="utf-8") as h:
        h.write("# tmp 小样语料\n\n| 局号 (ep) | 对手 | 我席 | 原局 margin |"
                " 对手终局 | 对手段位 | 峰值日 | 峰值额 | 归档体积(字节) |\n"
                "|---|---|---|---|---|---|---|---|---|\n"
                + "\n".join(rows) + "\n")
    return root


def _tape_follower(tapes_by_ep_seat):
    def fn(obs):
        step = int(obs.get("step", 0) or 0)
        player = int(obs.get("player", 0) or 0)
        return json.loads(json.dumps(tapes_by_ep_seat[player][step]))
    return fn


# ---------------------------------------------------------------------------
# 1) 重演计算管线
# ---------------------------------------------------------------------------
def test_replay_gate_pipeline_roundtrip(tmp_path):
    """磁带跟随注入 → 重演终局 == 回放 rewards（管线正确性金标准）。"""
    replay1, tapes1, finals1 = _tapes_and_replay(
        7001, [_buy_agent, _pass_agent])       # 我席(0)=买入 → 败局
    replay2, tapes2, finals2 = _tapes_and_replay(
        7002, [_buy_agent, _pass_agent])       # 对席(0)=买入 → 我席(1)胜
    corpus = _write_tiny_corpus(str(tmp_path), [
        (990001, 0, 1, replay1, finals1),
        (990002, 1, 1, replay2, finals2)])
    follower = _tape_follower({0: tapes1[0], 1: tapes2[1]})
    res = lpg.run_replay_gate(corpus, v5_callable=follower)
    assert res["n"] == 2
    assert res["wins"] == 1          # 990002 我席(1)赢（对席买入变穷）
    g1, g2 = res["per_game"]
    assert g1["ep"] == 990001 and g1["me_seat"] == 0
    assert g1["injection_step"] == 1 * lpg.STEPS_PER_DAY   # 峰值日起始步
    assert g1["orig_margin"] == pytest.approx(
        replay1["rewards"][0] - replay1["rewards"][1])
    assert g1["replay_margin"] == pytest.approx(g1["orig_margin"])
    assert g1["replay_finals"] == pytest.approx(replay1["rewards"])
    assert g1["win"] is False and g1["flipped"] is False
    assert g2["ep"] == 990002 and g2["win"] is True
    assert g2["replay_margin"] == pytest.approx(g2["orig_margin"])
    # 短季无 d24+：P4 形态遥测恒零
    assert g1["p4_trigger_meter"]["form_present_calls"] == 0
    # 判据固定 >=7/14：小样 n=2 必然不过
    assert res["passed"] is False


def test_replay_gate_pipeline_divergence(tmp_path):
    """换分叉动作（恒 PASS vs 磁带含买入）→ 终局改变（注入真实生效）。"""
    replay, tapes, finals = _tapes_and_replay(
        7003, [lambda o: json.loads(json.dumps(BUY_ACT)), _pass_agent])
    corpus = _write_tiny_corpus(str(tmp_path),
                                [(990003, 0, 1, replay, finals)])
    res = lpg.run_replay_gate(corpus, v5_callable=_pass_agent)
    g = res["per_game"][0]
    assert g["replay_margin"] != pytest.approx(g["orig_margin"])


def test_replay_gate_fail_closed(tmp_path):
    with pytest.raises(ValueError):          # CORPUS.md 缺失
        lpg.run_replay_gate(str(tmp_path))
    empty = tmp_path / "empty"
    empty.mkdir()
    (empty / "CORPUS.md").write_text(
        "# 无清单行\n| a | b |\n|---|---|\n", encoding="utf-8")
    with pytest.raises(ValueError):          # 清单行为空
        lpg.run_replay_gate(str(empty))


# ---------------------------------------------------------------------------
# 2) 等价比较器
# ---------------------------------------------------------------------------
def test_equivalence_comparator_identical(tmp_path):
    replay, _, finals = _tapes_and_replay(
        7004, [_pass_agent, _pass_agent])
    p = tmp_path / "episode-990004-replay.json"
    p.write_text(json.dumps(replay, ensure_ascii=False), encoding="utf-8")
    game_set = [
        {"kind": "constructed", "seed": 7005, "episode_steps": 72,
         "opp_kind": _pass_agent, "me_seat": 0},
        {"kind": "constructed", "seed": 7006, "episode_steps": 72,
         "opp_kind": _pass_agent, "me_seat": 1},
        {"kind": "replay", "ep": 990004, "me_seat": 0,
         "replay_path": str(p), "inject_step": 0},
    ]
    same = _scripted_agent(buy=True)
    res = lpg.run_equivalence_face(game_set, v5_callable=same,
                                   v4b_callable=same)
    assert res["n"] == 3 and res["n_identical"] == 3
    assert res["n_excluded_by_trigger"] == 0
    assert all(g["identical"] for g in res["per_game"])
    assert all(g["first_diffs"] == [] for g in res["per_game"])
    assert res["passed"] is False           # n=3 < 8：判据未到（比较器全同）


def test_equivalence_comparator_detects_fork(tmp_path):
    replay, _, finals = _tapes_and_replay(
        7007, [_pass_agent, _pass_agent])
    p = tmp_path / "episode-990007-replay.json"
    p.write_text(json.dumps(replay, ensure_ascii=False), encoding="utf-8")
    game_set = [
        {"kind": "constructed", "seed": 7008, "episode_steps": 72,
         "opp_kind": _pass_agent, "me_seat": 0},
        {"kind": "replay", "ep": 990007, "me_seat": 0,
         "replay_path": str(p), "inject_step": 0},
    ]
    res = lpg.run_equivalence_face(
        game_set, v5_callable=_scripted_agent(buy=True),
        v4b_callable=_scripted_agent(buy=False))
    assert res["n_identical"] == 0
    assert all(not g["identical"] for g in res["per_game"])
    assert all(g["first_diffs"] for g in res["per_game"])   # 分叉定位非空
    assert res["passed"] is False


# ---------------------------------------------------------------------------
# 3) 裁决 schema
# ---------------------------------------------------------------------------
def _fake_replay(wins, n):
    return {"wins": wins, "n": n, "per_game": [],
            "passed": wins >= lpg.REPLAY_WIN_MIN
            and n == lpg.REPLAY_N_EXPECTED}


def _fake_equiv(n_identical, n):
    return {"n_identical": n_identical, "n": n, "per_game": [],
            "passed": n >= lpg.EQUIV_MIN and n_identical == n}


def _fake_launch(ok=True):
    return {"fourgate_pass": ok, "patches_tests_pass": ok,
            "passed": ok}


_RUN_OK = {"replay_gate": True, "equivalence": True, "launch_recheck": True}
_NO_ERR = {}


def test_verdict_schema_all_pass():
    v = lpg._assemble_verdict(_fake_replay(7, 14), _fake_equiv(8, 8),
                              _fake_launch(True), dict(_RUN_OK),
                              dict(_NO_ERR), {"tar_sha256": "x"}, 1.5)
    assert v["overall"] == "PASS"
    assert {"protocol", "generated_utc", "v5_identity", "replay_gate",
            "equivalence", "launch_recheck", "overall",
            "wall_s"} <= set(v)
    assert v["replay_gate"]["wins"] == 7 and v["replay_gate"]["n"] == 14
    assert v["replay_gate"]["passed"] is True
    assert v["equivalence"]["n_identical"] == 8 and v["equivalence"]["n"] == 8
    assert v["equivalence"]["passed"] is True
    assert v["launch_recheck"]["passed"] is True
    assert v["replay_gate"]["error"] is None


def test_verdict_criterion_wiring():
    mk = lambda r, e, l: lpg._assemble_verdict(
        r, e, l, dict(_RUN_OK), dict(_NO_ERR), {}, 0.0)["overall"]
    assert mk(_fake_replay(6, 14), _fake_equiv(8, 8),
              _fake_launch(True)) == "FAIL"        # 重演 6/14 差一局
    assert mk(_fake_replay(7, 13), _fake_equiv(8, 8),
              _fake_launch(True)) == "FAIL"        # 语料不满 14 局
    assert mk(_fake_replay(7, 14), _fake_equiv(7, 7),
              _fake_launch(True)) == "FAIL"        # 非触发局 <8
    assert mk(_fake_replay(7, 14), _fake_equiv(7, 8),
              _fake_launch(True)) == "FAIL"        # 8 局中 1 局分叉
    assert mk(_fake_replay(7, 14), _fake_equiv(8, 8),
              _fake_launch(False)) == "FAIL"       # 发射复检红


def test_verdict_not_runnable_fail_closed():
    runnable = {"replay_gate": False, "equivalence": True,
                "launch_recheck": True}
    errors = {"replay_gate": "ValueError: 语料缺失: /x"}
    v = lpg._assemble_verdict(None, _fake_equiv(8, 8), _fake_launch(True),
                              runnable, errors, {}, 0.0)
    assert v["overall"] == "FAIL"
    assert v["replay_gate"]["runnable"] is False
    assert "语料缺失" in v["replay_gate"]["error"]
    assert v["replay_gate"]["wins"] is None
