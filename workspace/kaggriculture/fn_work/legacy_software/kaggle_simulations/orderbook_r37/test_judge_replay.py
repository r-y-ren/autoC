# -*- coding: utf-8 -*-
"""R19 测试面：judge_replay（重演线/verdict 组三指标）。

verdict 组 = replay_guard_verdict 真测试（构造行，口径随实现同钉；行契约=
parse_episode_states 输出逐步双席行，本组不 import parse_states 平行件）：
①三指标算对——d2 前逃走 1 头（末见 cu=1、消失在 d1 末/d2 初日界拍）、
  买牲畜失败 1 张（钱格全程不动）、d1 h0 现金 1（step 24 拍）；双诱饵不计
  （day≥2 饿逃不计、轨迹 0 消失非饿逃不计）+ 成交单不计（钱扣即成交）；
②全绿路径 pass=True（现金≥4、零逃走、零买失败；含钱扣成交与上格成交两臂）；
③UNKNOWN 路径——缺 money 字段→verdict="UNKNOWN" 不抛、cash_d1h0=None；
④对手席隔离——对手席逃走/买失败不入我方指标；our_seat 可参数化（换席复算
  恰得对手侧指标）；
⑤final_delta 有/无基线两分支（有=终局 money−baseline_final，无=None）；
⑥FEED 退化推断——行未带 consecutive_unfed 子键：日结日对两日无 FEED 判饿逃，
  任一日有 FEED 即不计。

judge 组 = judge_cash_guard_replay 编排真测试（重演引擎 monkeypatch 合成状态，
装载 last-callable/parse_episode_states/replay_guard_verdict 全真件）：
①编排全流程——3 局小语料（2 灾难+1 对照）→evidence 结构+聚合三指标实数+
  对照 l1+overall 绿；②单局失败标红不短路——1 局引擎抛→errors 计数+其余照跑
  +overall 红；③判据聚合正确——构造红局（d2 死牛+买失败+现金 1）→聚合实数
  与 overall 判定 False；④语料缺失报错清晰——空语料/文件缺失→ValueError
  含"语料缺失"。
"""
import json  # noqa: F401
import os  # noqa: F401
import sys  # noqa: F401

import pytest  # noqa: F401

try:
    from orderbook_r37 import judge_replay
except ImportError:  # 兜底：直接以 orderbook_r37/ 为 sys.path 根跑测
    import judge_replay

replay_guard_verdict = judge_replay.replay_guard_verdict

_OUR = "renyxin"
_OPP = "techtech69"


# ---------------------------------------------------------------------------
# 构造件：逐步双席规范行（{step, seat, action, money, hands, animals_grid,
# tiles}；animals_grid={(x,y): 牲畜条目}，子键有则带、缺即省略）
# ---------------------------------------------------------------------------
def _act(*market):
    return {"farmer": ["PASS"], "hands": [], "market": [list(o) for o in market]}


def _row(step, money, grid=None, action=None, seat=_OUR):
    return {"step": step, "seat": seat,
            "action": action if action is not None else _act(),
            "money": money, "hands": [], "tiles": {},
            "animals_grid": dict(grid) if grid else {}}


def _entry(name, cu=None, fed=None):
    e = {"type": name, "kind": "PASTURE" if name in ("COW", "SHEEP") else "COOP"}
    if cu is not None:
        e["consecutive_unfed"] = cu
    if fed is not None:
        e["fed_today"] = fed
    return e


def _grids(cells):
    return {pos: _entry(*spec) for pos, spec in cells.items()}


# ---------------------------------------------------------------------------
# ①三指标算对（含 d2 前逃走 1 头/买牲畜失败 1 张/现金 1）+双诱饵不计
# ---------------------------------------------------------------------------
def test_replay_guard_verdict():
    cow = (4, 2)      # d2 前饿逃（末见 cu=1，d1 末拍→d2 初拍消失）
    goose = (2, 2)    # 诱饵：轨迹 0 消失（非饿逃）
    sheep_buy = (3, 3)   # step 36 成交买（step 37 上格）
    sheep_late = (5, 5)  # 诱饵：day≥2 饿逃（d2 末→d3 初消失）
    rows = [
        _row(24, 1.0, _grids({cow: ("COW", 1, False), goose: ("GOOSE", 0, True)})),
        _row(35, 500.0, _grids({cow: ("COW", 1, False), goose: ("GOOSE", 0, True)})),
        # 成交单：SHEEP 钱 500→100 同拍扣钱（提交拍执行后值）
        _row(36, 100.0, _grids({cow: ("COW", 1, False), goose: ("GOOSE", 0, True)}),
             _act(["BUY_ANIMAL", "SHEEP", 1])),
        _row(37, 100.0, _grids({cow: ("COW", 1, False), goose: ("GOOSE", 0, True),
                                sheep_buy: ("SHEEP", 0, True)})),
        _row(40, 100.0, _grids({cow: ("COW", 1, False),
                                sheep_buy: ("SHEEP", 0, True),
                                sheep_late: ("SHEEP", 0, True)})),  # GOOSE 消失
        _row(47, 81.0, _grids({cow: ("COW", 1, False),
                               sheep_buy: ("SHEEP", 0, True),
                               sheep_late: ("SHEEP", 0, True)})),
        _row(48, 81.0, _grids({sheep_buy: ("SHEEP", 0, True),
                               sheep_late: ("SHEEP", 0, True)})),  # COW 消失
        _row(65, 369.0, _grids({sheep_buy: ("SHEEP", 0, True),
                                sheep_late: ("SHEEP", 1, False)})),
        # 失败单：COW 钱格全程不动（369→369→369、COW 头数 0）
        _row(66, 369.0, _grids({sheep_buy: ("SHEEP", 0, True),
                                sheep_late: ("SHEEP", 1, False)}),
             _act(["BUY_ANIMAL", "COW", 1])),
        _row(67, 369.0, _grids({sheep_buy: ("SHEEP", 0, True),
                                sheep_late: ("SHEEP", 1, False)})),
        _row(71, 369.0, _grids({sheep_buy: ("SHEEP", 0, True),
                                sheep_late: ("SHEEP", 1, False)})),
        _row(72, 369.0, _grids({sheep_buy: ("SHEEP", 0, True)})),  # 迟到饿逃
    ]
    out = replay_guard_verdict(rows)
    assert set(out) == {"died_before_d2", "buy_failed", "cash_d1h0",
                        "final_delta", "verdict"}
    assert out["died_before_d2"] == 1        # 仅 d1 末/d2 初 COW 饿逃
    assert out["buy_failed"] == 1            # 仅 step 66 COW 静默丢弃
    assert out["cash_d1h0"] == 1.0           # step 24 拍（d1 hour0）
    assert out["final_delta"] is None        # 无基线
    assert out["verdict"] == {"pass": False}  # 现金 1 < 4


# ---------------------------------------------------------------------------
# ②全绿路径 pass=True（现金≥4、零逃走、零买失败）
# ---------------------------------------------------------------------------
def test_replay_guard_verdict_pass_path():
    cow = (0, 0)
    rows = [
        _row(24, 5.0, {}),
        _row(29, 500.0, {}),
        _row(30, 100.0, {}, _act(["BUY_ANIMAL", "COW", 1])),  # 钱扣成交（500→100）
        _row(31, 100.0, _grids({cow: ("COW", 0, True)})),
        _row(33, 300.0, _grids({cow: ("COW", 0, True)})),
        # 上格成交臂：钱不动、下一拍 COW 头数 0→1（1→2）即成交
        _row(34, 300.0, _grids({cow: ("COW", 0, True)}),
             _act(["BUY_ANIMAL", "COW", 1])),
        _row(35, 300.0, _grids({cow: ("COW", 0, True), (1, 0): ("COW", 0, True)})),
        _row(47, 300.0, _grids({cow: ("COW", 0, True), (1, 0): ("COW", 0, True)})),
        _row(48, 300.0, _grids({cow: ("COW", 0, True), (1, 0): ("COW", 0, True)})),
    ]
    out = replay_guard_verdict(rows)
    assert out["died_before_d2"] == 0
    assert out["buy_failed"] == 0
    assert out["cash_d1h0"] == 5.0
    assert out["verdict"] == {"pass": True}


# ---------------------------------------------------------------------------
# ③UNKNOWN 路径（缺 money 字段：不抛）
# ---------------------------------------------------------------------------
def test_replay_guard_verdict_unknown():
    rows = [
        {"step": 24, "seat": _OUR, "action": _act(), "hands": [],
         "animals_grid": {}, "tiles": {}},
        {"step": 25, "seat": _OUR, "action": _act(), "hands": [],
         "animals_grid": {}, "tiles": {}},
    ]
    out = replay_guard_verdict(rows)  # 缺字段不抛
    assert set(out) == {"died_before_d2", "buy_failed", "cash_d1h0",
                        "final_delta", "verdict"}
    assert out["verdict"] == "UNKNOWN"
    assert out["cash_d1h0"] is None
    assert out["died_before_d2"] == 0 and out["buy_failed"] == 0


# ---------------------------------------------------------------------------
# ④对手席隔离 + our_seat 可参数化
# ---------------------------------------------------------------------------
def test_replay_guard_verdict_opponent_seat():
    cow = (4, 2)
    opp_rows = [
        _row(24, 22.0, _grids({cow: ("COW", 1, False)}), seat=_OPP),
        _row(47, 22.0, _grids({cow: ("COW", 1, False)}), seat=_OPP),
        _row(48, 22.0, {}, seat=_OPP),                    # 对手饿逃 1 头
        _row(65, 369.0, {}, seat=_OPP),
        _row(66, 369.0, {}, _act(["BUY_ANIMAL", "COW", 1]), seat=_OPP),
        _row(67, 369.0, {}, seat=_OPP),                   # 对手买失败 1 张
    ]
    our_rows = [
        _row(24, 4.0, {}),
        _row(47, 4.0, {}),
        _row(48, 4.0, {}),
        _row(66, 4.0, {}),
    ]
    out = replay_guard_verdict(our_rows + opp_rows)
    assert out["died_before_d2"] == 0 and out["buy_failed"] == 0
    assert out["cash_d1h0"] == 4.0
    assert out["verdict"] == {"pass": True}
    # 参数化换席复算：恰得对手侧指标（席位名从行取）
    out_opp = replay_guard_verdict(our_rows + opp_rows, our_seat=_OPP)
    assert out_opp["died_before_d2"] == 1
    assert out_opp["buy_failed"] == 1
    assert out_opp["cash_d1h0"] == 22.0
    assert out_opp["verdict"] == {"pass": False}


# ---------------------------------------------------------------------------
# ⑤final_delta 有/无基线两分支
# ---------------------------------------------------------------------------
def test_replay_guard_verdict_final_delta():
    rows = [
        _row(24, 4.0, {}),
        _row(700, 67608.0, {}),
    ]
    with_base = replay_guard_verdict(rows, baseline_final=86518.0)
    assert with_base["final_delta"] == 67608.0 - 86518.0  # r37−实况
    assert with_base["verdict"] == {"pass": True}
    no_base = replay_guard_verdict(rows)
    assert no_base["final_delta"] is None                 # 无基线→None
    assert no_base["verdict"] == {"pass": True}


# ---------------------------------------------------------------------------
# ⑥FEED 退化推断（行未带 consecutive_unfed 子键）
# ---------------------------------------------------------------------------
def test_replay_guard_verdict_feed_fallback():
    cow = (4, 2)
    bare = _grids({cow: ("COW",)})  # 仅 type，无 consecutive_unfed/fed_today
    dead_beat = [
        _row(24, 4.0, bare),
        _row(47, 4.0, bare),
        _row(48, 4.0, {}),
    ]
    out = replay_guard_verdict(dead_beat)
    assert out["died_before_d2"] == 1   # 日结日对（d0,d1）无 FEED→判饿逃

    fed_d1 = dead_beat[:2] + [_row(40, 4.0, bare, _act(["FEED"]))] + dead_beat[2:]
    out_d1 = replay_guard_verdict(sorted(fed_d1, key=lambda r: r["step"]))
    assert out_d1["died_before_d2"] == 0  # d1 有 FEED→非连续两日无喂

    fed_d0 = dead_beat[:1] + [_row(10, 4.0, bare, _act(["FEED"]))] + dead_beat[1:]
    out_d0 = replay_guard_verdict(sorted(fed_d0, key=lambda r: r["step"]))
    assert out_d0["died_before_d2"] == 0  # d0 有 FEED→非连续两日无喂


# ===========================================================================
# judge 组：judge_cash_guard_replay 编排真测试（重演引擎 monkeypatch 合成状态）
# ===========================================================================
_KSIM_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _KSIM_ROOT not in sys.path:
    sys.path.insert(0, _KSIM_ROOT)

from agent.planner import twin as _twin_mod  # noqa: E402

judge_cash_guard_replay = judge_replay.judge_cash_guard_replay

_GREEN_SRC = ('def agent(obs):\n'
              '    return {"farmer": ["PASS"], "hands": [], "market": []}\n')
_BUY_SRC = ('def agent(obs):\n'
            '    return {"farmer": ["PASS"], "hands": [],\n'
            '            "market": [["BUY_ANIMAL", "COW", 1]]}\n')
_DIS1, _DIS2 = 112938600, 112968467   # 灾难局固定 id（判据归属面）


def _mini_replay(tmp_path, name, episode, final_money=100.0):
    """parse_episode_states 可解的最小双席 replay（2 拍），末拍资金=基线。"""
    def _farm(money):
        return {"money": money, "hands": [], "farmer": [0, 0],
                "tiles": [[None, None], [None, None]]}

    steps = []
    for t in range(2):
        pair = []
        for _seat in range(2):
            pair.append({
                "action": {"farmer": ["PASS"], "hands": [], "market": []},
                "observation": {"day": 0, "hour": t,
                                "farms": [_farm(3000.0), _farm(3000.0)],
                                "private": {}}})
        steps.append(pair)
    for seat in (0, 1):
        steps[-1][seat]["observation"]["farms"][seat]["money"] = final_money
    path = tmp_path / name
    path.write_text(json.dumps({
        "steps": steps, "rewards": [final_money, final_money],
        "info": {"EpisodeId": episode,
                 "TeamNames": [_OPP, _OUR]}}), encoding="utf-8")
    return str(path)


def _farm(money, tiles):
    return {"money": money, "hands": [], "farmer": [0, 0], "tiles": tiles}


def _frames(money24=10.0, final=200.0, cow=None):
    """26 拍合成状态（step 24 有拍可取现金）；cow=(x,y,cu,末见拍) 可选。"""
    frames = []
    for i in range(26):
        tiles = [[None, None], [None, None]]
        if cow is not None and i <= cow[3]:
            tiles[cow[1]][cow[0]] = {
                "animal": "COW", "kind": "PASTURE",
                "consecutive_unfed": cow[2], "fed_today": False}
        money = final if i == 25 else (money24 if i >= 24 else 1000.0)
        frames.append({"step": i, "day": i // 24, "hour": i % 24,
                       "farms": [_farm(money, tiles), _farm(money, tiles)]})
    return frames


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
            obs.farms, obs.day, obs.hour = frame["farms"], frame["day"], frame["hour"]
        self.seats[0].observation.step = frame["step"]
        if self.i >= len(self.frames) - 1:
            self.env.done = True


class _FakeTwin:
    """合成重演引擎：逐局给帧剧本；可按局号抛（红局面）。"""

    def __init__(self, frames_by_ep, raise_for=()):
        self.frames_by_ep = frames_by_ep
        self.raise_for = set(raise_for)
        self.state = None

    def load_engine(self, *a, **k):
        return "fake-bundle"

    def build_state_from_replay(self, replay, step_index, bundle=None):
        ep = int((replay.get("info") or {}).get("EpisodeId") or 0)
        if ep in self.raise_for:
            raise ValueError(f"synthetic engine boom @{ep}")
        self.state = _FakeState(self.frames_by_ep[ep])
        return self.state

    def replay_transition_actions(self, replay):
        n = len(self.state.frames) - 1
        pair = [{"farmer": ["PASS"], "hands": [], "market": []}] * 2
        return [list(pair) for _ in range(n)]

    def step(self, state, pair):
        state.advance()
        return state


def _patch_twin(monkeypatch, fake):
    monkeypatch.setattr(_twin_mod, "load_engine", fake.load_engine)
    monkeypatch.setattr(_twin_mod, "build_state_from_replay",
                        fake.build_state_from_replay)
    monkeypatch.setattr(_twin_mod, "replay_transition_actions",
                        fake.replay_transition_actions)
    monkeypatch.setattr(_twin_mod, "step", fake.step)


# ---------------------------------------------------------------------------
# judge ①编排全流程：3 局小语料→evidence 结构+聚合+overall 绿
# ---------------------------------------------------------------------------
def test_judge_cash_guard_replay_orchestration(tmp_path, monkeypatch):
    pkg = tmp_path / "main.py"
    pkg.write_text(_GREEN_SRC, encoding="utf-8")
    paths = [
        _mini_replay(tmp_path, "g1-replay.json", _DIS1, final_money=100.0),
        _mini_replay(tmp_path, "g2-replay.json", _DIS2, final_money=100.0),
        _mini_replay(tmp_path, "g3-replay.json", 99900001, final_money=100.0),
    ]
    fake = _FakeTwin({_DIS1: _frames(money24=10.0, final=200.0),
                      _DIS2: _frames(money24=11.0, final=200.0),
                      99900001: _frames(money24=12.0, final=250.0)})
    _patch_twin(monkeypatch, fake)
    out = judge_cash_guard_replay(str(pkg), paths)

    # evidence 结构（逐局三指标+对照资金差+overall+语料清单+source）
    assert set(out) >= {"generated_at", "pkg_path", "method", "corpus",
                        "games", "aggregate", "overall", "errors", "source"}
    assert out["corpus"]["n_disaster"] == 2 and out["corpus"]["n_control"] == 1
    assert len(out["games"]) == 3
    assert set(out["source"]) >= {"rerun_command", "replay_pull_command",
                                  "replay_cache_dirs"}
    # 逐局：双席位各演一遍、灾难局无基线、对照局有对照资金差
    for g in out["games"][:2]:
        assert g["kind"] == "disaster" and not g["red"]
        for key in ("seat0", "seat1"):
            run = g["runs"][key]
            assert run["verdict"] == {"pass": True}
            assert run["cash_d1h0"] >= 4 and run["died_before_d2"] == 0
            assert run["buy_failed"] == 0
            assert run["final_delta"] is None       # 灾难局不传基线
    ctrl = out["games"][2]
    assert ctrl["kind"] == "control"
    for key in ("seat0", "seat1"):
        run = ctrl["runs"][key]
        assert run["baseline_final"] == 100.0       # 原局实况终局资金
        assert run["final_delta"] == 150.0          # 250−100（r37−实况）
    # 聚合三指标实数+对照 l1+overall 绿
    agg = out["aggregate"]
    assert agg["disaster"]["died_before_d2_sum"] == 0
    assert agg["disaster"]["buy_failed_sum"] == 0
    assert agg["disaster"]["cash_d1h0_min"] == 10.0
    assert agg["control"]["final_delta_l1_min"] == 150.0
    assert agg["control"]["n_negative"] == 0
    assert out["overall"]["pass"] is True
    assert out["overall"]["criteria"] == {
        "died_before_d2_zero": True, "buy_failed_zero": True,
        "cash_d1h0_ge_4": True, "control_final_delta_nonneg": True}
    assert out["errors"] == []


# ---------------------------------------------------------------------------
# judge ②单局失败标红不短路：1 局抛→errors 计数+其余照跑
# ---------------------------------------------------------------------------
def test_judge_cash_guard_replay_red_no_shortcircuit(tmp_path, monkeypatch):
    pkg = tmp_path / "main.py"
    pkg.write_text(_GREEN_SRC, encoding="utf-8")
    paths = [
        _mini_replay(tmp_path, "g1-replay.json", _DIS1, final_money=100.0),
        _mini_replay(tmp_path, "g2-replay.json", _DIS2, final_money=100.0),
        _mini_replay(tmp_path, "g3-replay.json", 99900001, final_money=100.0),
    ]
    fake = _FakeTwin({_DIS1: _frames(money24=10.0, final=200.0),
                      _DIS2: _frames(money24=11.0, final=200.0),
                      99900001: _frames(money24=12.0, final=250.0)},
                     raise_for={_DIS2})
    _patch_twin(monkeypatch, fake)
    out = judge_cash_guard_replay(str(pkg), paths)

    assert len(out["games"]) == 3                     # 不短路：全跑完
    bad = out["games"][1]
    assert bad["red"] is True and "boom" in bad["error"]
    assert out["games"][0]["red"] is False            # 其余照跑
    assert out["games"][0]["runs"]["seat0"]["cash_d1h0"] == 10.0
    assert out["games"][2]["runs"]["seat1"]["final_delta"] == 150.0
    assert out["errors"] and out["overall"]["n_errors"] == 1
    assert out["overall"]["n_red_games"] == 1
    assert out["overall"]["pass"] is False            # fail-closed


# ---------------------------------------------------------------------------
# judge ③判据聚合正确：构造红局→聚合实数+overall 判定 False
# ---------------------------------------------------------------------------
def test_judge_cash_guard_replay_aggregate_red(tmp_path, monkeypatch):
    pkg = tmp_path / "main.py"
    pkg.write_text(_BUY_SRC, encoding="utf-8")        # 每拍买牛、永不成交
    paths = [
        _mini_replay(tmp_path, "g1-replay.json", _DIS1, final_money=100.0),
        _mini_replay(tmp_path, "g2-replay.json", _DIS2, final_money=100.0),
        _mini_replay(tmp_path, "g3-replay.json", 99900001, final_money=100.0),
    ]
    fake = _FakeTwin({
        _DIS1: _frames(money24=10.0, final=200.0,
                       cow=(0, 0, 1, 24)),            # d2 前饿逃 1 头/席
        _DIS2: _frames(money24=1.0, final=200.0),     # d1 h0 现金 1<4
        99900001: _frames(money24=12.0, final=250.0)})
    _patch_twin(monkeypatch, fake)
    out = judge_cash_guard_replay(str(pkg), paths)

    agg = out["aggregate"]
    assert agg["disaster"]["died_before_d2_sum"] == 2      # 1 头×2 席位
    assert agg["disaster"]["buy_failed_sum"] >= 2          # 静默丢单计入
    assert agg["disaster"]["cash_d1h0_min"] == 1.0         # 构造红局
    assert agg["control"]["final_delta_l1_min"] == 150.0   # 对照臂不翻负
    assert out["overall"]["criteria"] == {
        "died_before_d2_zero": False, "buy_failed_zero": False,
        "cash_d1h0_ge_4": False, "control_final_delta_nonneg": True}
    assert out["overall"]["pass"] is False
    assert out["errors"] == [] and out["overall"]["n_red_games"] == 0


# ---------------------------------------------------------------------------
# judge ④语料缺失报错清晰
# ---------------------------------------------------------------------------
def test_judge_cash_guard_replay_corpus_missing(tmp_path):
    pkg = tmp_path / "main.py"
    pkg.write_text(_GREEN_SRC, encoding="utf-8")
    with pytest.raises(ValueError, match="语料缺失"):
        judge_cash_guard_replay(str(pkg), [])
    with pytest.raises(ValueError, match="语料缺失"):
        judge_cash_guard_replay(str(pkg), [str(tmp_path / "nope-replay.json")])
    with pytest.raises(ValueError, match="语料缺失"):
        judge_cash_guard_replay(str(pkg), ["not-an-episode"])
