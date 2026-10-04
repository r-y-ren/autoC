# -*- coding: utf-8 -*-
"""R28 测试面：判决线（判据=R28 ②原文：净加卖恒等违例 0∧镜像胜率 ≥0.55∧
实现价不降∧反制臂不翻车∧胜局对照不翻负∧h2h vs r40 ≥0.55；镜像板/反制臂编排
假局组夹具）。实现价读数一律走真 judge_r26.realized_price_stats（traced
states→reads），不以伪造 reads 盖住真 trace 链路。"""
from __future__ import annotations

import gzip
import json

import pytest

from orderbook_r43 import judge_r26 as j26
from orderbook_r45 import judge_r45 as j45

PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}

# ---- traced states 夹具（真 realized_price_stats 口径） -------------------
# 候选侧：d0 观察价 22→18、卖 10@18，日均价 20 → realized_px=0.9
CAND_STATES = [(0, {"market": {"prices": {"WHEAT": 22.0}}}, {"market": []}),
               (1, {"market": {"prices": {"WHEAT": 18.0}}},
                {"market": [["SELL", "WHEAT", 10]]})]
# 基线侧（r40）：d0 观察价 30→20、卖 10@20，日均价 25 → realized_px=0.8
BASE_STATES = [(0, {"market": {"prices": {"WHEAT": 30.0}}}, {"market": []}),
               (1, {"market": {"prices": {"WHEAT": 20.0}}},
                {"market": [["SELL", "WHEAT", 10]]})]


def make_runner(margins_by_arm, states_by_arm=None, opp_states=None,
                capture=None, raise_for=()):
    """假局组执行器：margin 按 arm（标量/逐行列表；None=红行）。

    reads 一律=真 judge_r26.realized_price_stats(traced states)（不伪造）；
    opp_states 给→行级补 reads_opp（基线侧读数）。
    """
    def runner(specs, cfg):
        seen = capture if capture is not None else []
        rows = []
        counter = {}
        for s in specs:
            arm = s.get("arm")
            if arm in raise_for:
                raise RuntimeError("fake runner boom: %s" % arm)
            seen.append(dict(s))
            idx = counter.get(arm, 0)
            counter[arm] = idx + 1
            m = margins_by_arm.get(arm, 0.0)
            if isinstance(m, (list, tuple)):
                m = m[idx % len(m)]
            if m is None:
                rows.append({"game_id": s["game_id"], "seed": s["seed"],
                             "arm": arm, "our_seat": s.get("our_seat", 0),
                             "margin": None, "error": "faked red"})
                continue
            states = (states_by_arm or {}).get(arm, CAND_STATES)
            row = {"game_id": s["game_id"], "seed": s["seed"], "arm": arm,
                   "our_seat": s.get("our_seat", 0), "margin": float(m),
                   "error": None, "reads": j26.realized_price_stats(states)}
            if opp_states is not None:
                row["reads_opp"] = j26.realized_price_stats(opp_states)
            rows.append(row)
        return rows
    return runner


def make_corpus(tmp_path, n=2):
    """26 败局语料同形态（.json.gz：seed/teams/steps）。"""
    d = tmp_path / "corpus"
    d.mkdir(exist_ok=True)
    for i in range(n):
        rec = {"seed": 1000 + i, "episode_id": 500 + i,
               "teams": ["opp", "renyxin"],
               "steps": [[dict(PASS_ACTION),
                          {"farmer": ["PASS"], "hands": [],
                           "market": [["SELL", "WOOL", 1]]}]
                         for _ in range(2)]}
        with gzip.open(d / ("episode-%d-strip.json.gz" % (500 + i)),
                       "wb") as fh:
            fh.write(json.dumps(rec).encode("utf-8"))
    return d


LEDGER_OK = {"g1": {"debts": [{"item": "WOOL", "qty": 5, "due_step": 100,
                               "advance_step": 96}],
                    "settled": [{"item": "WOOL", "qty": 5, "step": 100}]}}


# ============================ verify_net_identity ===========================
def test_verify_net_identity():
    """正例：逐局逐品 Σadvance=Σsettled → 违例 0。"""
    out = j45.verify_net_identity([{"game_id": "g1"}], LEDGER_OK)
    assert out["violations"] == 0
    assert out["ok"] is True
    assert out["checked_items"] == 1


def test_verify_net_identity_imbalance_violations():
    """反例：提前卖 5/到期抵扣 3 → 违例 ≥1+明细。"""
    bad = {"g1": {"debts": [{"item": "WOOL", "qty": 5, "due_step": 100,
                             "advance_step": 96}],
                  "settled": [{"item": "WOOL", "qty": 3, "step": 100}]}}
    out = j45.verify_net_identity(["g1"], bad)
    assert out["violations"] >= 1
    row = [d for d in out["detail"] if d.get("kind") == "identity_violation"][0]
    assert row["advanced"] == 5 and row["settled"] == 3
    assert out["ok"] is False


def test_verify_net_identity_ledger_missing_fail_closed():
    """台账缺失→违例计 1（fail-closed）。"""
    assert j45.verify_net_identity(["g1"], None)["violations"] == 1
    assert j45.verify_net_identity(["g1"], "oops")["violations"] == 1
    out = j45.verify_net_identity(["g1"], {"g2": LEDGER_OK["g1"]})
    assert out["violations"] >= 1
    assert any(d.get("kind") == "ledger_missing" for d in out["detail"])
    # 台账缺 debts/settled 结构→违例（fail-closed）
    assert j45.verify_net_identity(["g1"], {"g1": {"debts": []}})[
        "violations"] >= 1


def test_verify_net_identity_multi_game_multi_item():
    led = {"g1": {"debts": [{"item": "WOOL", "qty": 2, "due_step": 10,
                             "advance_step": 8},
                            {"item": "MILK", "qty": 1, "due_step": 12,
                             "advance_step": 9}],
                  "settled": [{"item": "WOOL", "qty": 2, "step": 10},
                              {"item": "MILK", "qty": 1, "step": 12}]},
           "g2": {"debts": [{"item": "WOOL", "qty": 3, "due_step": 20,
                             "advance_step": 18}],
                  "settled": [{"item": "WOOL", "qty": 3, "step": 20}]}}
    assert j45.verify_net_identity(["g1", "g2"], led)["violations"] == 0


# ========================= run_mirror_counter_judgment ======================
def test_run_mirror_counter_judgment():
    """镜像板+反制臂编排（假局组夹具）：seated 双席位、独立 seed n 报、
    镜像=克隆/指纹 ≥0.95 专组、反制=Wool Front-Runner 构造对手。"""
    capture = []
    runner = make_runner({"mirror": 100.0, "counter": 50.0}, capture=capture)
    out = j45.run_mirror_counter_judgment(
        {"main_path": "/tmp/r45_main.py"},
        {"groups": [{"arm": "mirror", "n": 3}, {"arm": "counter", "n": 2}],
         "runner": runner, "seed_base": 1000})
    arms = {a["arm"]: a for a in out["arms"]}
    assert set(arms) == {"mirror", "counter"}
    for arm, n in (("mirror", 3), ("counter", 2)):
        row = arms[arm]
        assert {"arm", "n", "wins", "losses", "ties", "mean_margin"} <= set(row)
        assert row["n"] == n                      # 独立 seed（席位翻转不双计）
        assert row["wins"] == n and row["losses"] == 0
        assert row["win_rate"] == 1.0
        assert row["mean_margin"] > 0
    # seated 双席位：每 seed 两局（seat 0/1），对手席互换；trace=True 真链路
    mirror_specs = [s for s in capture if s["arm"] == "mirror"]
    assert len(mirror_specs) == 3 * 2
    assert sorted({s["our_seat"] for s in mirror_specs}) == [0, 1]
    assert all(s["trace"] is True for s in capture)   # 回行须带 reads
    # 镜像对手=克隆/指纹 ≥0.95
    opp = out["opponents"]["mirror"]
    assert opp["kind"] == "clone_mirror"
    assert opp["fingerprint"] >= 0.95
    # 反制对手=Wool Front-Runner 构造（orderbook_predict 先例复用）
    cop = out["opponents"]["counter"]
    assert cop["kind"] == "wool_front_runner"
    assert cop["config"] == {"sniff_window": 2, "dump_qty": 48,
                             "anti_shock": True}
    counter_specs = [s for s in capture if s["arm"] == "counter"]
    assert all(s["agents"][1 if s["our_seat"] == 0 else 0].get("counter",
               {}).get("kind") == "wool_front_runner"
               for s in counter_specs)
    assert out["independent_seeds"] is True and out["seated"] is True


def test_run_mirror_counter_judgment_seed_fold_and_red_counting():
    """席位翻转折叠+单局红按负计入（不短路）。"""
    # seed A 双席全胜→胜；seed B 席位分歧→平；seed C 单局红→计入负
    runner = make_runner({"mirror": [10.0, 10.0, 10.0, -10.0, 10.0, None]})
    out = j45.run_mirror_counter_judgment(
        {"main_path": "/tmp/r45_main.py"},
        {"groups": [{"arm": "mirror", "seeds": [11, 12, 13]}],
         "runner": runner})
    row = out["arms"][0]
    assert row["n"] == 3
    assert row["wins"] == 1 and row["ties"] == 1 and row["losses"] == 1
    assert row["incomplete"] == 1
    assert row["red_seeds"] == [13]
    assert row["win_rate"] == pytest.approx((1 + 0.5 * 1) / 3)
    assert row["median_margin"] == 10.0           # Δ 中位（不翻负判据用）


def test_run_mirror_counter_judgment_unrunnable_red():
    """组不可跑→fail-closed 记红。"""
    out = j45.run_mirror_counter_judgment(
        {"main_path": "/tmp/r45_main.py"},
        {"groups": [{"arm": "mirror", "n": 2}],
         "runner": make_runner({}, raise_for=("mirror",))})
    row = out["arms"][0]
    assert row["red"] is True
    assert row["win_rate"] == 0.0
    assert out["errors"]


def test_run_mirror_counter_judgment_replay_games_seated_false(tmp_path):
    """显式局组（败局重演形态）：单局单席、tape 对手、不折叠双席。"""
    capture = []
    runner = make_runner({"replay_loss": 30.0}, capture=capture)
    out = j45.run_mirror_counter_judgment(
        {"main_path": "/tmp/r45_main.py"},
        {"groups": [{"arm": "replay_loss", "seated": False, "games": [
            {"game_id": "replay-1", "seed": 11, "our_seat": 1,
             "opponent": {"type": "tape", "actions": [dict(PASS_ACTION)]}},
            {"game_id": "replay-2", "seed": 12, "our_seat": 1,
             "error": "parse failed"}]}],
         "runner": runner})
    row = out["arms"][0]
    assert row["n"] == 2
    assert row["wins"] == 1 and row["losses"] == 1   # 解析红按负计入
    assert len(capture) == 1                          # 红局不进 runner
    assert capture[0]["agents"][0]["type"] == "tape"  # our_seat=1→tape 在 0 位
    assert capture[0]["trace"] is True                # 显式局组同样走真 trace


# ============================== judge_r45 ==================================
def _judge(tmp_path, runner, **extra):
    cfg = {"runner": runner, "n_seeds": 2,
           "traces": [{"game_id": "g1"}], "ledger": LEDGER_OK,
           "baseline_realized_px": 0.85,
           "evidence_path": str(tmp_path / "ev.json"),
           "groups": [{"arm": "mirror", "n": 2}, {"arm": "counter", "n": 2},
                      {"arm": "control_win", "n": 2,
                       "opponent": {"type": "python", "path": "/tmp/ctrl.py"}},
                      {"arm": "h2h_r40", "n": 2,
                       "opponent": {"type": "python", "path": "/tmp/r40.py"}}]}
    corpus = extra.pop("corpus", [])
    cfg.update(extra)
    return j45.judge_r45({"main_path": "/tmp/r45_main.py"}, corpus, cfg)


def test_judge_r45(tmp_path):
    """全绿：判据全 PASS→POSITIVE；evidence 契约键齐。"""
    ev = _judge(tmp_path, make_runner({"mirror": 100.0, "counter": 50.0,
                                       "h2h_r40": 20.0, "control_win": 30.0}))
    assert ev["verdict"] == "POSITIVE"
    assert all(c["verdict"] == "PASS" for c in ev["criteria"].values())
    # evidence 契约
    assert {"_generated_at", "source", "arms", "criteria", "verdict"} <= set(ev)
    assert isinstance(ev["source"]["commands"], list) and ev["source"]["commands"]
    assert ev["source"]["seed_base"] == j45.SEED_BASE
    for row in ev["arms"]:
        assert {"arm", "n", "wins", "losses", "ties", "mean_margin"} <= set(row)
    assert set(ev["criteria"]) == set(j45.CRITERIA_KEYS)
    assert (tmp_path / "ev.json").exists()


def test_judge_r45_mirror_threshold_branch(tmp_path):
    """镜像胜率阈值分支：0.55 边界 PASS、0.50 FAIL。"""
    margins = [1.0, 1.0] * 11 + [-1.0, -1.0] * 9      # 11 胜 9 负/20 seeds
    groups = [{"arm": "mirror", "n": 20},
              {"arm": "counter", "n": 2},
              {"arm": "control_win", "n": 2,
               "opponent": {"type": "python", "path": "/tmp/ctrl.py"}},
              {"arm": "h2h_r40", "n": 2,
               "opponent": {"type": "python", "path": "/tmp/r40.py"}}]
    ev = _judge(tmp_path, make_runner({"mirror": margins, "counter": 1.0,
                                       "h2h_r40": 1.0, "control_win": 1.0}),
                n_seeds=20, groups=groups)
    assert ev["criteria"]["mirror_win_rate"]["value"] == pytest.approx(0.55)
    assert ev["criteria"]["mirror_win_rate"]["verdict"] == "PASS"
    margins2 = [1.0, 1.0] * 10 + [-1.0, -1.0] * 10
    ev2 = _judge(tmp_path, make_runner({"mirror": margins2, "counter": 1.0,
                                        "h2h_r40": 1.0, "control_win": 1.0}),
                 n_seeds=20, groups=groups)
    assert ev2["criteria"]["mirror_win_rate"]["verdict"] == "FAIL"
    assert ev2["verdict"] == "NEGATIVE"


def test_judge_r45_counter_and_h2h_threshold_branches(tmp_path):
    """反制不翻车（≥0.50）/h2h ≥0.55 阈值分支。"""
    ev = _judge(tmp_path, make_runner({"mirror": 1.0, "counter": [-1.0, -1.0],
                                       "h2h_r40": 1.0, "control_win": 1.0}))
    assert ev["criteria"]["counter_not_flipped"]["verdict"] == "FAIL"
    ev2 = _judge(tmp_path, make_runner({"mirror": 1.0, "counter": 1.0,
                                        "h2h_r40": [-1.0, -1.0],
                                        "control_win": 1.0}))
    assert ev2["criteria"]["h2h_vs_r40"]["verdict"] == "FAIL"
    # 反制边界：1 胜 1 负 → 0.50 PASS（不翻车）
    ev3 = _judge(tmp_path, make_runner({"mirror": 1.0,
                                        "counter": [1.0, -1.0],
                                        "h2h_r40": 1.0, "control_win": 1.0}))
    assert ev3["criteria"]["counter_not_flipped"]["value"] == pytest.approx(0.5)
    assert ev3["criteria"]["counter_not_flipped"]["verdict"] == "PASS"


def test_judge_r45_control_not_negative_branch(tmp_path):
    """胜局对照不翻负（入判据闸 verdict）：翻负 FAIL/Δ 中位 ≥0 PASS/缺组 FAIL。"""
    groups = [{"arm": "mirror", "n": 2}, {"arm": "counter", "n": 2},
              {"arm": "control_win", "n": 2,
               "opponent": {"type": "python", "path": "/tmp/ctrl.py"}},
              {"arm": "h2h_r40", "n": 2,
               "opponent": {"type": "python", "path": "/tmp/r40.py"}}]
    # 翻负：对照组全负（Δ 中位<0 且胜率 0）→FAIL→verdict NEGATIVE
    ev = _judge(tmp_path, make_runner({"mirror": 1.0, "counter": 1.0,
                                       "h2h_r40": 1.0,
                                       "control_win": -20.0}), groups=groups)
    assert ev["criteria"]["control_not_negative"]["value"] == {
        "win_rate": 0.0, "median_margin": -20.0}
    assert ev["criteria"]["control_not_negative"]["verdict"] == "FAIL"
    assert ev["verdict"] == "NEGATIVE"
    # Δ 中位 ≥0（胜率 <0.5 亦不翻负）→PASS
    games = [{"game_id": "c-%d" % i, "seed": 3000 + i, "our_seat": 0,
              "opponent": {"type": "python", "path": "/tmp/opp.py"}}
             for i in range(5)]
    ev2 = _judge(tmp_path, make_runner({"mirror": 1.0, "counter": 1.0,
                                        "h2h_r40": 1.0,
                                        "control_win": [0.0, 0.0, 0.0, -5.0,
                                                        -5.0]}),
                 groups=groups[:2] + [{"arm": "control_win", "seated": False,
                                       "games": games}, groups[3]])
    assert ev2["criteria"]["control_not_negative"]["value"] == {
        "win_rate": 0.3, "median_margin": 0.0}
    assert ev2["criteria"]["control_not_negative"]["verdict"] == "PASS"
    # 缺对照组→FAIL（fail-closed）
    ev3 = _judge(tmp_path, make_runner({"mirror": 1.0, "counter": 1.0,
                                        "h2h_r40": 1.0}),
                 groups=groups[:2] + [groups[3]])
    assert ev3["criteria"]["control_not_negative"]["verdict"] == "FAIL"


def test_judge_r45_realized_px_no_drop_branch(tmp_path):
    """实现价不降：候选(真 reads 0.9)≥基线 PASS、<基线 FAIL、基线缺失 FAIL。"""
    ok = _judge(tmp_path, make_runner({"mirror": 1.0, "counter": 1.0,
                                       "h2h_r40": 1.0, "control_win": 1.0}),
                baseline_realized_px=0.85)
    assert ok["criteria"]["realized_px_no_drop"]["verdict"] == "PASS"
    drop = _judge(tmp_path, make_runner({"mirror": 1.0, "counter": 1.0,
                                         "h2h_r40": 1.0,
                                         "control_win": 1.0}),
                  baseline_realized_px=0.95)
    assert drop["criteria"]["realized_px_no_drop"]["verdict"] == "FAIL"
    miss = _judge(tmp_path, make_runner({"mirror": 1.0, "counter": 1.0,
                                         "h2h_r40": 1.0,
                                         "control_win": 1.0}),
                  baseline_realized_px=None)
    assert miss["criteria"]["realized_px_no_drop"]["verdict"] == "FAIL"


def test_judge_r45_realized_px_from_states_reuse_judge_r26(tmp_path):
    """realized_price_stats 复用 judge_r26（无 reads 时按 traced states 读数）。"""
    states = [(0, {"market": {"prices": {"WHEAT": 30.0}}},
               {"market": [["SELL", "WHEAT", 10]]}),
              (718, {"market": {"prices": {"WHEAT": 40.0}},
                     "farms": [{"money": 1000.0}],
                     "private": {"shed": {}}}, {"market": []})]

    def runner(specs, cfg):
        return [{"game_id": s["game_id"], "seed": s["seed"], "arm": s["arm"],
                 "our_seat": s.get("our_seat", 0), "margin": 1.0,
                 "error": None, "states": states} for s in specs]

    ev = _judge(tmp_path, runner, baseline_realized_px=0.5)
    assert ev["criteria"]["realized_px_no_drop"]["value"]["candidate"] == 1.0
    assert ev["criteria"]["realized_px_no_drop"]["verdict"] == "PASS"


def test_judge_r45_realized_ok_true_real_trace_chain(tmp_path):
    """P0 证据：真 trace 链路（j26._chunk 回行形状、reads=真 realized_price_
    stats）下 realized_ok 可为 True，v28 判正可达——基线侧两条路径皆接通。"""
    cand_reads = j26.realized_price_stats(CAND_STATES)
    base_reads = j26.realized_price_stats(BASE_STATES)
    assert cand_reads["realized_px"] == 0.9        # 真函数算出的候选侧读数
    assert base_reads["realized_px"] == 0.8        # 真函数算出的基线侧读数

    def _chunk_row(s, reads, reads_opp=None):
        """j26._chunk 回行形状（keys 同 _chunk）：margin 由 banks+seat 归一。"""
        seat = int(s.get("our_seat", 0) or 0)
        banks = [20000.0, 10000.0] if seat == 0 else [10000.0, 20000.0]
        row = {"game_id": s["game_id"], "seed": s["seed"], "seat": seat,
               "arm": s.get("arm"), "banks": banks, "error": None,
               "margin": float(banks[seat] - banks[1 - seat]),
               "reads": reads}
        if reads_opp is not None:
            row["reads_opp"] = reads_opp          # 行级补基线侧读数
        return row

    groups = [{"arm": "mirror", "n": 2}, {"arm": "counter", "n": 2},
              {"arm": "control_win", "n": 2,
               "opponent": {"type": "python", "path": "/tmp/ctrl.py"}},
              {"arm": "h2h_r40", "n": 2,
               "opponent": {"type": "python", "path": "/tmp/r40.py"}}]
    # 路径①行级 reads_opp（同局配对基线；无 config 定桩）
    ev = _judge(tmp_path,
                lambda specs, cfg: [_chunk_row(s, cand_reads,
                                               reads_opp=base_reads)
                                    for s in specs],
                groups=groups, baseline_realized_px=None)
    assert ev["criteria"]["realized_px_no_drop"]["value"] == {
        "candidate": 0.9, "baseline": 0.8}
    assert ev["criteria"]["realized_px_no_drop"]["verdict"] == "PASS"
    assert ev["verdict"] == "POSITIVE"            # 判正可达（真链路实证）

    # 路径②基线臂（baseline_r40=r40 自镜像结构基线；无 config 定桩）
    def runner_arm(specs, cfg):
        return [_chunk_row(s, base_reads if s.get("arm") == "baseline_r40"
                           else cand_reads) for s in specs]

    groups_b = groups[:3] + [
        {"arm": "baseline_r40", "n": 2,
         "agent": {"type": "python", "path": "/tmp/r40.py"},
         "opponent": {"type": "python", "path": "/tmp/r40.py"}},
        groups[3]]
    ev2 = _judge(tmp_path, runner_arm, groups=groups_b,
                 baseline_realized_px=None)
    assert ev2["criteria"]["realized_px_no_drop"]["value"] == {
        "candidate": 0.9, "baseline": 0.8}
    assert ev2["criteria"]["realized_px_no_drop"]["verdict"] == "PASS"
    assert ev2["verdict"] == "POSITIVE"


def test_judge_r45_net_identity_fail_closed(tmp_path):
    """净加卖恒等违例>0→判决红（fail-closed 传递）。"""
    bad_ledger = {"g1": {"debts": [{"item": "WOOL", "qty": 5, "due_step": 10,
                                    "advance_step": 8}],
                         "settled": [{"item": "WOOL", "qty": 2, "step": 10}]}}
    ev = _judge(tmp_path, make_runner({"mirror": 1.0, "counter": 1.0,
                                       "h2h_r40": 1.0, "control_win": 1.0}),
                ledger=bad_ledger)
    assert ev["criteria"]["net_identity"]["verdict"] == "FAIL"
    assert ev["criteria"]["net_identity"]["value"] >= 1
    assert ev["verdict"] == "NEGATIVE"
    # 台账缺失→违例计 1→红
    ev2 = _judge(tmp_path, make_runner({"mirror": 1.0, "counter": 1.0,
                                        "h2h_r40": 1.0, "control_win": 1.0}),
                 ledger=None)
    assert ev2["criteria"]["net_identity"]["value"] == 1
    assert ev2["verdict"] == "NEGATIVE"


def test_judge_r45_replay_corpus_group(tmp_path):
    """26 败局重演语料→replay_loss 臂逐局 WL；在库默认目录=26 局。"""
    corpus = make_corpus(tmp_path, n=3)
    capture = []
    ev = _judge(tmp_path, make_runner({"mirror": 1.0, "counter": 1.0,
                                       "h2h_r40": 1.0,
                                       "replay_loss": [1.0, -1.0, 1.0]},
                                      capture=capture),
                groups=None, corpus=str(corpus))
    replay = [a for a in ev["arms"] if a["arm"] == "replay_loss"][0]
    assert replay["n"] == 3
    assert replay["wins"] == 2 and replay["losses"] == 1
    assert replay["seated"] is False
    specs = [s for s in capture if s.get("arm") == "replay_loss"]
    assert len(specs) == 3
    assert all(s["agents"][0]["type"] == "tape" or
               s["agents"][1]["type"] == "tape" for s in specs)
    # 缺省局组恒含胜局对照（内容配置化；缺→红记）
    assert any(a["arm"] == "control_win" for a in ev["arms"])
    # 在库 26 败局语料（R28 判据原文口径）
    in_repo = sorted(j45.REPLAY_CORPUS_DEFAULT.glob("episode-*.json*"))
    assert len(in_repo) == 26


def test_judge_r45_fail_closed_runner_error(tmp_path):
    """局组不可跑→镜像臂红记→判据红→NEGATIVE（fail-closed 传递）。"""
    ev = _judge(tmp_path, make_runner({"counter": 1.0, "h2h_r40": 1.0,
                                       "control_win": 1.0},
                                      raise_for=("mirror",)))
    assert ev["criteria"]["mirror_win_rate"]["verdict"] == "FAIL"
    assert ev["verdict"] == "NEGATIVE"
