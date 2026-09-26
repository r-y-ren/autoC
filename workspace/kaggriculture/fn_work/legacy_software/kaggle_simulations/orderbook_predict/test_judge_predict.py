# -*- coding: utf-8 -*-
"""R21 测试面：judge_predict（判决线/flip 组翻转与 realized 价）。

flip 组 = flip_stats 真测试（构造行，口径随实现同钉；行契约=parse 同构双席行
{step, seat, action, money, inventory, prices}）：
①晚崩判定——loss_phase 主导段口径（三段增量最负段：open=d10−0/mid=d20−
  d10/late=final−d20）：late 主导→晚崩+计翻正；mid 主导→非晚崩；次级标志
  lead_then_lost（margin_d10>0 或 d20>0）留档；
②非晚崩不计——mid 主导败局 counted=False、verdict.pass=None（不进翻正分母）；
③realized 价差——撞车品项优先序（STRAWBERRY 先于 MILK）、邻拍库存差分截断
  成交量、实现价=Σ(截断量×挂牌价)/Σ截断量，我 43 vs 对手 97 → delta −54；
  baseline 原局实现价在场→delta_px_gain 抬升观测；
④缺字段 UNKNOWN——行缺 action/money、空 states、baseline 缺 margin 探针
  → verdict="UNKNOWN" 不抛；
⑤对照资金差——final_delta=重演我席终局 money−原局基线；≥0 pass True、
  <0 pass False（胜局对照不翻负判据面）；
⑥避让/抢跑动作差分——原局卖单流 vs 重演卖单流逐品项 FIFO 对齐：提前=抢跑、
  顺延=避让、删除/新增同向计痕迹。

judge 组 = judge_predict_replay 编排真测试（重演引擎 agent.planner.twin
monkeypatch 合成状态+闭环 kaggle_environments.make 合成局；装载 last-callable/
原局统计/flip_stats 全真件）：
①编排小语料——5 局（3 败局含晚崩/中段+2 对照）→evidence 结构+聚合判据实数
  +h2h 主对+overall 绿；
②单局红不短路——1 局引擎抛→red+errors 计数+其余局照跑照聚合+overall 红；
③判据聚合三分支——全绿→POSITIVE；判据不达→NEGATIVE 逐判据归因（晚崩翻正
  不足/h2h 不足两路）；红局 fail-closed→判据全绿仍 NEGATIVE；
④语料缺失报错——空语料/文件缺失/非局号条目/重复条目→ValueError 含"语料缺失"。
"""
import json
import os
import sys

import pytest  # noqa: F401

try:
    from orderbook_predict import judge_predict
except ImportError:  # 兜底：直接以 orderbook_predict/ 为 sys.path 根跑测
    import judge_predict

flip_stats = judge_predict.flip_stats
judge_predict_replay = judge_predict.judge_predict_replay

_OUR = "renyxin"
_OPP = "techtech69"


# ---------------------------------------------------------------------------
# 构造件：逐步双席规范行（{step, seat, action, money, inventory, prices}）
# ---------------------------------------------------------------------------
def _act(*market):
    return {"farmer": ["PASS"], "hands": [], "market": [list(o) for o in market]}


def _row(step, seat, money, action=None, inv=None, prices=None):
    out = {"step": step, "seat": seat,
           "action": action if action is not None else _act(),
           "money": money}
    if inv is not None:
        out["inventory"] = dict(inv)
    if prices is not None:
        out["prices"] = dict(prices)
    return out


def _loss_base(our_seat=0, final=0.0, opp_final=3000.0, m10=-50.0,
               m20=-300.0, mf=-3000.0, kind="loss", sell_flow=None,
               realized=None):
    out = {"our_seat": our_seat, "kind": kind, "final_money": final,
           "opp_final_money": opp_final, "margin_d10": m10,
           "margin_d20": m20, "margin_final": mf}
    if sell_flow is not None:
        out["sell_flow"] = sell_flow
    if realized is not None:
        out["realized"] = realized
    return out


def _beat_rows(finals, steps=(0, 1)):
    """双席行对：末拍 money=(席0, 席1)。"""
    rows = []
    for t in steps:
        money = finals if t == steps[-1] else (3000.0, 3000.0)
        for s in (0, 1):
            rows.append(_row(t, s, float(money[s]), inv={}))
    return rows


# ---------------------------------------------------------------------------
# flip 组
# ---------------------------------------------------------------------------
def test_flip_stats_late_collapse判定():
    """①晚崩判定（loss_phase 主导段口径）+lead_then_lost 次级标志。"""
    rows = _beat_rows((4000.0, 3000.0))
    out = flip_stats(rows, _loss_base())          # (−50,−300,−3000)→late 主导
    assert out["flip"]["late_collapse"] is True
    assert out["flip"]["dominant_segment"] == "late"
    assert out["flip"]["counted"] is True
    assert out["flip"]["lead_then_lost"] is False
    assert out["flip"]["delta_margin"] == 4000.0  # (1000)−(−3000)
    assert out["flip"]["flipped"] is True
    assert out["flip"]["rerun_win"] is True

    mid = flip_stats(rows, _loss_base(final=3000.0, opp_final=8100.0,
                                      m10=-2000.0, m20=-5000.0,
                                      mf=-5100.0))
    assert mid["flip"]["dominant_segment"] == "mid"   # open=−2000 最负

    lead = flip_stats(rows, _loss_base(final=2500.0, opp_final=3000.0,
                                       m10=100.0, m20=-50.0, mf=-500.0))
    assert lead["flip"]["late_collapse"] is True      # late=−450 主导
    assert lead["flip"]["lead_then_lost"] is True     # d10 领先但终局负


def test_flip_stats_non_late_not_counted():
    """②非晚崩不计：mid 主导败局 counted=False、pass=None。"""
    rows = _beat_rows((2600.0, 3000.0))
    out = flip_stats(rows, _loss_base(final=3000.0, opp_final=8100.0,
                                      m10=-2000.0, m20=-5000.0,
                                      mf=-5100.0))
    assert out["flip"]["late_collapse"] is False
    assert out["flip"]["counted"] is False
    assert out["verdict"] == {"kind": "loss", "counted": False, "pass": None}


def test_flip_stats_realized_price_gap():
    """③realized 价差：品项优先序+库存差分截断+提升观测。"""
    rows = [
        _row(0, 0, 3000.0, inv={"STRAWBERRY": 5, "MILK": 2},
             prices={"STRAWBERRY": 43.0, "MILK": 10.0}),
        _row(1, 0, 3215.0, _act(["SELL", "STRAWBERRY", 5],
                                ["SELL", "MILK", 2]),
             inv={}, prices={"STRAWBERRY": 43.0, "MILK": 10.0}),
        _row(0, 1, 3000.0, inv={"STRAWBERRY": 5, "MILK": 2},
             prices={"STRAWBERRY": 97.0, "MILK": 12.0}),
        _row(1, 1, 3485.0, _act(["SELL", "STRAWBERRY", 5],
                                ["SELL", "MILK", 2]),
             inv={}, prices={"STRAWBERRY": 97.0, "MILK": 12.0}),
    ]
    base = _loss_base(realized={"STRAWBERRY": {"our_px": 42.9,
                                               "opp_px": 97.0}})
    out = flip_stats(rows, base)
    rz = out["realized"]
    assert rz["item"] == "STRAWBERRY" and rz["collision"] is True
    assert rz["our_px"] == 43.0 and rz["opp_px"] == 97.0
    assert rz["delta_px"] == -54.0
    assert rz["our_qty"] == 5 and rz["opp_qty"] == 5
    assert rz["orig_delta_px"] == pytest.approx(-54.1)
    assert rz["delta_px_gain"] == pytest.approx(0.1, abs=1e-6)
    assert rz["notes"] == []


def test_flip_stats_missing_fields_unknown():
    """④缺字段→verdict="UNKNOWN" 不抛。"""
    good = _beat_rows((4000.0, 3000.0))
    no_money = [dict(r, money=None) for r in good]
    assert flip_stats(no_money, _loss_base())["verdict"] == "UNKNOWN"
    no_action = [dict(r, action=None) for r in good]
    assert flip_stats(no_action, _loss_base())["verdict"] == "UNKNOWN"
    assert flip_stats([], _loss_base())["verdict"] == "UNKNOWN"
    thin_base = _loss_base()
    del thin_base["margin_d20"]
    assert flip_stats(good, thin_base)["verdict"] == "UNKNOWN"
    # 缺 prices/inventory 子键不触发 UNKNOWN（指标尽力：实现价 None）
    bare = [_row(0, 0, 3000.0), _row(1, 0, 4000.0),
            _row(0, 1, 3000.0), _row(1, 1, 3000.0)]
    out = flip_stats(bare, _loss_base())
    assert out["verdict"] != "UNKNOWN"
    assert out["realized"]["item"] is None


def test_flip_stats_control_final_delta():
    """⑤对照资金差（胜局对照不翻负判据面）。"""
    rows = _beat_rows((5100.0, 3000.0))
    base = _loss_base(final=5000.0, opp_final=3000.0, m10=1000.0,
                      m20=1500.0, mf=2000.0, kind="control")
    out = flip_stats(rows, base)
    assert out["final_delta"] == 100.0
    assert out["flip"]["counted"] is False          # 胜局对照非晚崩不计
    assert out["verdict"] == {"kind": "control", "counted": False,
                              "pass": True}
    bad = flip_stats(_beat_rows((4900.0, 3000.0)), base)
    assert bad["final_delta"] == -100.0
    assert bad["verdict"]["pass"] is False


def test_flip_stats_dodge_frontrun_diff():
    """⑥避让/抢跑=动作差分痕迹（FIFO 对齐：提前=抢跑/顺延=避让）。"""
    rows = [
        _row(8, 0, 3100.0, _act(["SELL", "STRAWBERRY", 5]), inv={}),
        _row(33, 0, 3200.0, _act(["SELL", "STRAWBERRY", 3]), inv={}),
        _row(8, 1, 3000.0, inv={}),
        _row(33, 1, 3000.0, inv={}),
    ]
    base = _loss_base(sell_flow={"STRAWBERRY": [[10, 5.0], [30, 5.0]]})
    out = flip_stats(rows, base)
    assert out["front_runs"] == 1    # 10→8 提前
    assert out["dodges"] == 1        # 30→33 顺延
    # 原局剩单=避让删除痕迹（第 3 张无配对→避让+1）
    out2 = flip_stats(rows, _loss_base(
        sell_flow={"STRAWBERRY": [[10, 5.0], [30, 5.0], [50, 4.0]]}))
    assert out2["dodges"] == 2
    assert out2["front_runs"] == 1


# ===========================================================================
# judge 组：judge_predict_replay 编排真测试（重演/闭环引擎合成，统计全真件）
# ===========================================================================
_HERE = os.path.dirname(os.path.abspath(__file__))
_KSIM_ROOT = os.path.dirname(_HERE)
if _KSIM_ROOT not in sys.path:
    sys.path.insert(0, _KSIM_ROOT)

import kaggle_environments  # noqa: E402
from agent.planner import twin as _twin_mod  # noqa: E402

_AGENT_SRC = ('def agent(obs):\n'
              '    return {"farmer": ["PASS"], "hands": [], "market": []}\n')


def _farm(money):
    return {"money": float(money), "hands": [], "farmer": [0, 0],
            "tiles": [[None, None]]}


def _scripted_replay(tmp_path, ep, m10, m20, mf):
    """505 步最小双席 replay：day 终探针=(m10, m20)，终局 margin=mf（席0 我方队）。"""
    anchors = [(0, float(m10)), (263, float(m10)), (503, float(m20)),
               (504, float(mf))]

    def margin_at(si):
        for (a0, v0), (a1, v1) in zip(anchors, anchors[1:]):
            if si <= a0:
                return v0
            if si <= a1:
                return v0 + (v1 - v0) * (si - a0) / float(a1 - a0)
        return float(mf)

    steps = []
    for si in range(505):
        m = margin_at(si)
        pair = []
        for seat in (0, 1):
            pair.append({
                "action": {"farmer": ["PASS"], "hands": [], "market": []},
                "observation": {"day": si // 24, "hour": si % 24,
                                "farms": [_farm(3000.0 + m if seat == 0
                                                else 3000.0),
                                          _farm(3000.0)],
                                "private": {}}})
        steps.append(pair)
    path = tmp_path / ("episode-%d-replay.json" % ep)
    path.write_text(json.dumps({
        "steps": steps, "rewards": [3000.0 + float(mf), 3000.0],
        "info": {"EpisodeId": ep, "TeamNames": [_OUR, _OPP]}}),
        encoding="utf-8")
    return str(path)


class _FakeObs:
    def __init__(self, frame, player):
        self.farms = frame["farms"]
        self.market, self.town = {}, {}
        self.day, self.hour, self.step = frame["day"], frame["hour"], frame["step"]
        self.player, self.private = player, {}
        self.remainingOverageTime = 60.0


class _FakeState:
    def __init__(self, frames):
        self.frames, self.i = frames, 0
        self.env = type("E", (), {"done": False})()
        self.seats = [type("S", (), {})() for _ in range(2)]
        for seat in range(2):
            self.seats[seat].observation = _FakeObs(frames[0], seat)

    def advance(self):
        self.i += 1
        frame = self.frames[self.i]
        for seat in range(2):
            obs = self.seats[seat].observation
            obs.farms = frame["farms"]
            obs.day, obs.hour = frame["day"], frame["hour"]
        self.seats[0].observation.step = frame["step"]
        if self.i >= len(self.frames) - 1:
            self.env.done = True


class _FakeTwin:
    """合成重演引擎：逐 (episode, 运行序) 给终局资金对；可按局号抛（红局面）。

    运行序约定=judge 编排序（每局席0 先、席1 后）→ finals_by_ep[ep][seq]。
    """

    def __init__(self, finals_by_ep, raise_for=()):
        self.finals_by_ep = finals_by_ep
        self.raise_for = set(raise_for)
        self.calls = {}

    def load_engine(self, *a, **k):
        return "fake-bundle"

    def build_state_from_replay(self, replay, step_index, bundle=None):
        ep = int((replay.get("info") or {}).get("EpisodeId") or 0)
        if ep in self.raise_for:
            raise ValueError("synthetic engine boom @%d" % ep)
        idx = self.calls.get(ep, 0)
        self.calls[ep] = idx + 1
        finals = self.finals_by_ep[ep][idx]
        frames = [
            {"step": 0, "day": 0, "hour": 0,
             "farms": [_farm(3000.0), _farm(3000.0)]},
            {"step": 1, "day": 0, "hour": 1,
             "farms": [_farm(finals[0]), _farm(finals[1])]}]
        self.state = _FakeState(frames)
        return self.state

    def replay_transition_actions(self, replay):
        return [[{"farmer": ["PASS"], "hands": [], "market": []}] * 2]

    def step(self, state, pair):
        state.advance()
        return state


def _frame(t, money):
    def _entry(seat):
        return {
            "action": {"farmer": ["PASS"], "hands": [], "market": []},
            "observation": {
                "step": t, "day": t // 24, "hour": t % 24,
                "farms": [_farm(money[0]), _farm(money[1])],
                "private": {"shed": {}, "seeds": {}, "inventories": []},
                "player": seat, "remainingOverageTime": 60.0},
            "reward": float(money[seat]), "status": "DONE"}
    return [_entry(0), _entry(1)]


class _FakeEnv:
    """合成闭环局：按 (seed, 同 seed 第几局) 从 outcomes 表定胜负。

    局序约定=judge 编排序（每 seed seat0 先、seat1 后）→ seq 即我方坐席。
    """

    def __init__(self, spec, seed):
        self._spec = spec
        self._seed = seed
        self.steps = []
        self.logs = []

    def run(self, agents):
        seq = self._spec["calls"].setdefault(self._seed, 0)
        self._spec["calls"][self._seed] = seq + 1
        if (self._seed, seq) in self._spec["boom"]:
            raise RuntimeError("synthetic engine boom")
        outcome = self._spec["outcomes"][self._seed][seq]
        money = [95.0, 95.0]
        if outcome == "win":
            money[seq] = 100.0
            money[1 - seq] = 90.0
        elif outcome == "loss":
            money[seq] = 90.0
            money[1 - seq] = 100.0
        self.steps = [_frame(t, money) for t in range(3)]


# 5 局语料脚本：(episode, m10, m20, mf, finals_run0, finals_run1)
_GREEN_GAMES = (
    (1001, -50.0, -300.0, -3000.0, (4000.0, 3000.0), (2000.0, 6100.0)),
    (1002, -30.0, -150.0, -1000.0, (2500.0, 3000.0), (1500.0, 4600.0)),
    (1003, -20.0, -80.0, -500.0, (2600.0, 3000.0), (2800.0, 3100.0)),
    (1004, 1000.0, 1500.0, 2000.0, (5100.0, 3000.0), (3000.0, 3100.0)),
    (1005, 200.0, 300.0, 500.0, (3600.0, 3000.0), (3000.0, 3600.0)),
)


def _games_with(finals_overrides):
    out = []
    for ep, m10, m20, mf, f0, f1 in _GREEN_GAMES:
        f0, f1 = finals_overrides.get(ep, (f0, f1))
        out.append((ep, m10, m20, mf, f0, f1))
    return out


def _install(monkeypatch, finals_by_ep, outcomes, raise_for=()):
    fake = _FakeTwin(finals_by_ep, raise_for=raise_for)
    monkeypatch.setattr(_twin_mod, "load_engine", fake.load_engine)
    monkeypatch.setattr(_twin_mod, "build_state_from_replay",
                        fake.build_state_from_replay)
    monkeypatch.setattr(_twin_mod, "replay_transition_actions",
                        fake.replay_transition_actions)
    monkeypatch.setattr(_twin_mod, "step", fake.step)
    spec = {"outcomes": outcomes, "calls": {}, "boom": set()}
    monkeypatch.setattr(
        kaggle_environments, "make",
        lambda name, configuration=None, debug=False:
            _FakeEnv(spec, int(configuration["seed"])))
    return spec


def _run_judge(tmp_path, monkeypatch, finals_overrides=None,
               main_outcomes=None, raise_for=()):
    os.makedirs(str(tmp_path), exist_ok=True)
    finals_overrides = finals_overrides or {}
    games = _games_with(finals_overrides)
    finals_by_ep, paths = {}, []
    for ep, m10, m20, mf, f0, f1 in games:
        paths.append(_scripted_replay(tmp_path, ep, m10, m20, mf))
        finals_by_ep[ep] = [f0, f1]
    pkg = tmp_path / "main.py"
    pkg.write_text(_AGENT_SRC, encoding="utf-8")
    opp = tmp_path / "opp.py"
    opp.write_text(_AGENT_SRC, encoding="utf-8")
    outcomes = dict(main_outcomes or {1000: ["win", "win"],
                                      2000: ["loss", "loss"]})
    outcomes.setdefault(1000, ["win", "win"])
    outcomes.setdefault(2000, ["loss", "loss"])
    _install(monkeypatch, finals_by_ep, outcomes, raise_for=raise_for)
    bench = {"main_opponent": str(opp), "secondary_opponent": str(opp),
             "seeds_main": [1000], "seeds_secondary": [2000]}
    return judge_predict_replay(str(pkg), paths, bench=bench)


# ---------------------------------------------------------------------------
# judge ①编排小语料：5 局→evidence 结构+聚合判据实数+overall 绿
# ---------------------------------------------------------------------------
def test_judge_predict_replay_orchestration_small_corpus(tmp_path, monkeypatch):
    ev = _run_judge(tmp_path, monkeypatch)
    assert set(ev) >= {"generated_at", "pkg_path", "method", "corpus",
                       "games", "aggregate", "overall", "errors", "source"}
    assert ev["corpus"]["n_entries"] == 5
    assert ev["corpus"]["n_loss_entries"] == 3
    assert ev["corpus"]["n_control_entries"] == 2
    assert ev["corpus"]["n_unique_games"] == 5
    assert len(ev["games"]) == 5
    for g in ev["games"]:
        assert not g["red"] and set(g["runs"]) == {"seat0", "seat1"}
        for run in g["runs"].values():
            assert run["verdict"] != "UNKNOWN"
    assert set(ev["source"]) >= {"rerun_command", "replay_pull_command",
                                 "replay_cache_dirs", "bench"}
    # 聚合判据实数（脚本实算）：晚崩 3 局翻正 2、对照 min 100、h2h 主对 1.0
    loss_b = ev["aggregate"]["losses"]
    assert loss_b["n_games"] == 3 and loss_b["n_late"] == 3
    assert loss_b["n_flipped"] == 2
    assert loss_b["flip_ratio"] == round(2 / 3, 4)
    assert loss_b["criterion_met"] is True and loss_b["expected_late"] == 15
    by_ep = {v["episode"]: v for v in loss_b["per_game"]}
    assert by_ep[1001]["delta_margin_min"] == 1100.0   # 双席 min>0 翻正
    assert by_ep[1002]["delta_margin_min"] == 500.0
    assert by_ep[1003]["delta_margin_min"] == -200.0   # min≤0 不翻
    assert by_ep[1003]["flipped"] is False
    ctrl_b = ev["aggregate"]["controls"]
    assert ctrl_b["n_games"] == 2 and ctrl_b["final_delta_min"] == 100.0
    assert ctrl_b["n_negative"] == 0 and ctrl_b["criterion_met"] is True
    h2h = ev["aggregate"]["h2h"]
    assert h2h["main"]["n_independent"] == 1
    assert h2h["main"]["h2h_rate"] == 1.0
    assert h2h["main"]["h2h_threshold"] == 0.55
    assert h2h["secondary"]["h2h_rate"] == 0.0        # 辅对仅观测
    assert ev["overall"]["criteria"] == {
        "control_not_flipped": True, "late_flip_ge_third": True,
        "h2h_vs_r37_ge_055": True}
    assert ev["overall"]["pass"] is True
    assert ev["overall"]["verdict"] == "POSITIVE"
    assert ev["overall"]["n_red_games"] == 0 and ev["errors"] == []


# ---------------------------------------------------------------------------
# judge ②单局红不短路
# ---------------------------------------------------------------------------
def test_judge_predict_replay_red_game_not_shortcircuit(tmp_path, monkeypatch):
    ev = _run_judge(tmp_path, monkeypatch, raise_for={1003})
    assert len(ev["games"]) == 5                  # 全量照跑
    assert ev["overall"]["n_red_games"] == 1
    assert len(ev["errors"]) == 1 and ev["errors"][0]["episode"] == 1003
    red_g = [g for g in ev["games"] if g.get("episode") == 1003][0]
    assert red_g["red"] is True and "synthetic engine boom" in red_g["error"]
    others = [g for g in ev["games"] if g.get("episode") != 1003]
    assert all(not g["red"] for g in others)      # 其余局照跑照聚合
    assert ev["aggregate"]["losses"]["n_late"] == 2
    assert ev["overall"]["pass"] is False
    assert ev["overall"]["verdict"] == "NEGATIVE"


# ---------------------------------------------------------------------------
# judge ③判据聚合三分支
# ---------------------------------------------------------------------------
def test_judge_predict_replay_criteria_three_branches(tmp_path, monkeypatch):
    # 分支一：全绿→POSITIVE
    green = _run_judge(tmp_path / "g", monkeypatch)
    assert green["overall"]["criteria"] == {
        "control_not_flipped": True, "late_flip_ge_third": True,
        "h2h_vs_r37_ge_055": True}
    assert green["overall"]["pass"] is True

    # 分支二：判据不达→NEGATIVE，逐判据归因（晚崩翻正不足 0/3）
    (tmp_path / "b").mkdir()
    late_fail = _run_judge(
        tmp_path / "b", monkeypatch,
        finals_overrides={1001: ((0.0, 3100.0), (2000.0, 6100.0)),
                          1002: ((2500.0, 3000.0), (1500.0, 2400.0))})
    assert late_fail["aggregate"]["losses"]["n_flipped"] == 0
    assert late_fail["overall"]["criteria"] == {
        "control_not_flipped": True, "late_flip_ge_third": False,
        "h2h_vs_r37_ge_055": True}
    assert late_fail["overall"]["pass"] is False

    # 分支二'：h2h 不达（主对全负 0.0<0.55）
    (tmp_path / "c").mkdir()
    h2h_fail = _run_judge(
        tmp_path / "c", monkeypatch,
        main_outcomes={1000: ["loss", "loss"], 2000: ["win", "win"]})
    assert h2h_fail["overall"]["criteria"] == {
        "control_not_flipped": True, "late_flip_ge_third": True,
        "h2h_vs_r37_ge_055": False}
    assert h2h_fail["overall"]["pass"] is False

    # 分支三：红局 fail-closed→判据全绿仍 NEGATIVE
    (tmp_path / "d").mkdir()
    red = _run_judge(tmp_path / "d", monkeypatch, raise_for={1005})
    assert red["overall"]["criteria"] == {
        "control_not_flipped": True, "late_flip_ge_third": True,
        "h2h_vs_r37_ge_055": True}
    assert red["overall"]["pass"] is False
    assert red["overall"]["verdict"] == "NEGATIVE"


# ---------------------------------------------------------------------------
# judge ④语料缺失报错
# ---------------------------------------------------------------------------
def test_judge_predict_replay_corpus_missing_raises(tmp_path):
    pkg = tmp_path / "main.py"
    pkg.write_text(_AGENT_SRC, encoding="utf-8")
    with pytest.raises(ValueError, match="语料缺失"):
        judge_predict_replay(str(pkg), [])
    with pytest.raises(ValueError, match="语料缺失"):
        judge_predict_replay(str(pkg), [str(tmp_path / "nope-replay.json")])
    with pytest.raises(ValueError, match="语料缺失"):
        judge_predict_replay(str(pkg), ["not-an-episode-id"])
    ok = _scripted_replay(tmp_path, 1001, -50.0, -300.0, -3000.0)
    with pytest.raises(ValueError, match="语料缺失"):
        judge_predict_replay(str(pkg), [ok, ok])     # 重复条目


def test_make_counter_opponent():
    raise NotImplementedError("unimplemented:fn:make_counter_opponent")
