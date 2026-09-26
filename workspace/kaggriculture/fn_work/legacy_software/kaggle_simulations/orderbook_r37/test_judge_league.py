# -*- coding: utf-8 -*-
"""R20 测试面：judge_league（联赛线/count 组刀次）。

count 组 = count_shearings 真测试（构造行，口径随实现同钉；行契约=
parse_episode_states 输出逐步双席行 {step, seat, action, money, hands,
animals_grid, tiles, …}；单元='F'(farmer)/'hN'(hands 下标)，day=step//24）：
①计数对（刀数/轮数）——2 羊 3 天剪毛链（同单元同日 HARVEST→PLACE 'WOOL'
  认领）→ 6 刀/3 轮 + 按只 (席,x,y) 各 3；
②HARVEST 无 PLACE WOOL 的保守分支——未认领候选非羊格（牛格/空格）或位置
  不可解析 → 一律不计刀，residuals 留档（reason: non_sheep_cell /
  unresolved_position）；同钉选一口径的产物推断分支：未认领但羊格 HARVEST
  → 计刀（按产物推断，实现 docstring 留档）；
③非羊产物不计剪毛——PLACE MILK/PLACE EGG 链不认领（非 WOOL 投放）且牛/鹅
  格非羊格 → 不计；链认领但羊格观测非羊格（随身存量投放假认领）→ 以对羊格
  定义为准不计（reason: chain_contradicted）；
④care_rate/feed_rate 计算——牲畜日上单元日覆盖率（分子=执行 CARE/FEED 的
  单元日，分母=牲畜日全体单元日）；非牲畜日不进分母；无牲畜日→None；
⑤缺字段 UNKNOWN——缺 step/seat/action、非 dict 行、step 非整型、空输入
  → {"shearings": None, …, "unknown": True, "verdict": "UNKNOWN"} 不抛；
⑥真 replay 样本实算——/tmp/kagr22/episode-112938600-replay.json 经
  parse_episode_states 全双席解析实跑，输出记 evidence/count_shearings_
  sample.json（可复算：同源重算深等+定义级独立复扫+锚点钉死）。

judge 组 = judge_sheep_league 编排真测试（对打引擎 monkeypatch 合成局，
装载/count_shearings 打桩，行解析 parse_states 全真件）：①编排小联赛
evidence 结构+聚合+overall 绿；②判据两路红（刀次不足/h2h<0.55 独立归因）；
③单局失败标红不短路；④席位翻转双计防护（统计按独立 seed）。
"""
import hashlib
import json
from collections import Counter
from pathlib import Path

import pytest

try:
    from orderbook_r37 import judge_league
    from orderbook_r37.parse_states import parse_episode_states
except ImportError:  # 兜底：直接以 orderbook_r37/ 为 sys.path 根跑测
    import judge_league
    from parse_states import parse_episode_states

count_shearings = judge_league.count_shearings

_HERE = Path(__file__).resolve().parent
_EVIDENCE = _HERE / "evidence" / "count_shearings_sample.json"
_REPLAY = Path("/tmp/kagr22/episode-112938600-replay.json")


# ---------------------------------------------------------------------------
# 构造件：逐步双席规范行（单元指令形如 ["HARVEST"]/["PLACE","WOOL",12]/
# ["CARE"]/["FEED"]；animals_grid={(x,y): 牲畜条目}；位置=执行后值）
# ---------------------------------------------------------------------------
_SHEEP = {"type": "SHEEP", "kind": "PASTURE"}
_COW = {"type": "COW", "kind": "PASTURE"}
_GOOSE = {"type": "GOOSE", "kind": "COOP"}


def _row(step, seat=0, farmer_op=("PASS",), hands_ops=(), grid=None,
         hands_pos=(), farmer_pos=(0, 0)):
    return {
        "step": step, "seat": seat, "day": step // 24, "hour": step % 24,
        "action": {"farmer": list(farmer_op),
                   "hands": [list(op) for op in hands_ops], "market": []},
        "money": 0, "hands": [list(p) for p in hands_pos],
        "farmer": list(farmer_pos),
        "animals_grid": dict(grid) if grid else {}, "tiles": {}, "inventory": {},
    }


def _reasons(out):
    return [(r["step"], r["seat"], r["unit"], r["reason"])
            for r in out["shearings"]["residuals"]]


def _unknown_shape(out):
    return (out["shearings"] is None and out["care_rate"] is None
            and out["feed_rate"] is None and out["unknown"] is True
            and out["verdict"] == "UNKNOWN")


# ---------------------------------------------------------------------------
# judge 组：judge_sheep_league 编排真测试（对打引擎 kaggle_environments.make
# monkeypatch 合成局、装载/count_shearings 打桩；行解析 parse_states 全真件）：
# ①编排小联赛——6 局（3 独立 seed×2 席：主对/强样本/mirror 各 1 seed）→
#   evidence 结构+聚合（主对 h2h/分组胜率/刀次双臂分布）+overall 绿；
# ②判据聚合正确两路红——刀次不足（刀轮/每羊 min=4<5）→shearings_5_achieved
#   红而 h2h 绿；主对全负 h2h=0.0<0.55→h2h 红而刀次绿（各自独立归因）；
# ③单局失败标红不短路——1 局引擎抛→red+errors 计数+其余局照跑照聚合+
#   overall 红（fail-closed 不短路）；
# ④席位翻转双计防护——主对 3 seed×2 席=6 局：统计按独立 seed n=3 报（seed
#   级胜/平/负 tally、h2h=(胜+0.5平)/独立局=0.8333），席位翻转对不双计。
# ---------------------------------------------------------------------------
import kaggle_environments

try:
    from orderbook_surge_lab import phase_b
except ImportError:  # 兜底：直接以 orderbook_r37/ 为 sys.path 根跑测
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from orderbook_surge_lab import phase_b

_R37 = _HERE / "build" / "main.py"
_R34A = _HERE.parent / "orderbook_2965_adopt" / "a" / "main.py"
_OPP = _HERE.parent / "orderbook_l3_derivative" / "variant_tuned" / "main.py"


def _farm(money):
    return {"money": float(money), "hands": [], "farmer": [0, 0],
            "tiles": [[{"kind": "PASTURE", "animal": "SHEEP"}]]}


def _frame(t, money):
    def _entry(seat):
        return {
            "action": {"farmer": ["PASS"], "hands": [], "market": []},
            "observation": {
                "step": t, "day": t // 24, "hour": t % 24,
                "farms": [_farm(money[0]), _farm(money[1])],
                "private": {"shed": {}, "seeds": {}, "inventories": []},
                "player": seat, "remainingOverageTime": 60.0,
            },
            "reward": float(money[seat]), "status": "DONE",
        }
    return [_entry(0), _entry(1)]


class _FakeEnv:
    """合成局引擎：按 (seed, 同 seed 第几局) 从 outcomes 表定胜负。

    局序约定=judge 编排序（每 seed seat0 先、seat1 后）→ seq 即 r37 坐席。
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


def _count_ok(rows):
    return {"shearings": {"total": 55, "rounds": [17, 20, 23, 26, 29],
                          "round_count": 5,
                          "per_sheep": {(0, 1, 1): 5, (0, 2, 2): 5},
                          "residuals": [], "unattributed": []},
            "care_rate": 1.0, "feed_rate": 0.9, "unknown": False,
            "verdict": None}


def _install(monkeypatch, outcomes, boom=(), count_fn=None):
    spec = {"outcomes": outcomes, "calls": {}, "boom": set(boom)}
    monkeypatch.setattr(
        phase_b, "load_l3_callable",
        lambda path: (lambda obs: {"farmer": ["PASS"], "hands": [],
                                   "market": []}))
    monkeypatch.setattr(
        kaggle_environments, "make",
        lambda name, configuration=None, debug=False:
            _FakeEnv(spec, int(configuration["seed"])))
    monkeypatch.setattr(judge_league, "count_shearings", count_fn or _count_ok)
    return spec


def test_judge_sheep_league(monkeypatch):
    """①编排小联赛（6 局）→evidence 结构+聚合+overall 绿。"""
    _install(monkeypatch, {1000: ["win", "win"], 2000: ["win", "win"],
                          9000: ["tie", "tie"]})
    ev = judge_league.judge_sheep_league(str(_R37), str(_R34A), [str(_OPP)],
                                         n_games=6)
    for key in ("generated_at", "pkg_path", "pkg_sha256", "method", "config",
                "games", "aggregate", "overall", "errors", "source"):
        assert key in ev
    assert ev["overall"]["pass"] is True
    assert ev["overall"]["criteria"] == {
        "shearings_5_achieved": True, "h2h_vs_r34a_ge_055": True,
        "win_games_not_flipped": True}
    assert ev["overall"]["n_red_games"] == 0 and ev["errors"] == []
    assert len(ev["games"]) == 6
    cfg = ev["config"]
    assert cfg["n_games_requested"] == 6 and cfg["n_games_executed"] == 6
    assert cfg["n_independent_planned"] == 3 and cfg["seats_per_seed"] == 2
    assert cfg["in_acceptance_range"] is False     # 6 局小配置供测试
    assert cfg["arms"]["main"]["seeds"] == [1000]
    assert cfg["arms"]["strong"][0]["seeds"] == [2000]
    assert cfg["arms"]["mirror"]["seeds"] == [9000]
    main_b = ev["aggregate"]["main"]
    assert main_b["n_games"] == 2 and main_b["n_independent"] == 1
    assert main_b["h2h_rate"] == 1.0 and main_b["h2h_threshold"] == 0.55
    assert main_b["seed_outcomes"] == {"win": 1, "draw": 0, "loss": 0,
                                       "incomplete": 0}
    assert ev["aggregate"]["strong"]["rate"] == 1.0
    assert ev["aggregate"]["mirror"]["rate"] == 0.5
    sh = ev["aggregate"]["shearings"]
    assert sh["threshold"] == 5.0
    assert sh["rounds"] == {"n": 6, "min": 5.0, "median": 5.0,
                            "achieve_rate": 1.0}
    assert sh["per_sheep_min"]["min"] == 5.0
    assert sh["arms"] == {"rounds_min_ge_5": True, "per_sheep_min_ge_5": True}
    g0 = ev["games"][0]
    assert g0["winner"] == "ours" and g0["red"] is False
    assert g0["shearings_rounds"] == 5.0 and g0["shearings_per_sheep_min"] == 5.0
    assert g0["care_rate"] == 1.0 and g0["feed_rate"] == 0.9
    assert ev["source"]["seeds"]["main"] == [1000]


def test_judge_sheep_league_knives_red(monkeypatch):
    """②刀次不足路红：刀轮/每羊 min=4<5→判据红而 h2h 绿；每羊臂独立归因。"""
    def _count_low(rows):
        return {"shearings": {"total": 4, "rounds": [17, 20, 23, 26],
                              "round_count": 4, "per_sheep": {(0, 1, 1): 4},
                              "residuals": [], "unattributed": []},
                "care_rate": 1.0, "feed_rate": 1.0, "unknown": False,
                "verdict": None}

    _install(monkeypatch, {1000: ["win", "win"], 2000: ["win", "win"],
                          9000: ["tie", "tie"]}, count_fn=_count_low)
    ev = judge_league.judge_sheep_league(str(_R37), str(_R34A), [str(_OPP)],
                                         n_games=6)
    crit = ev["overall"]["criteria"]
    assert crit["shearings_5_achieved"] is False   # 刀次不足路红
    assert crit["h2h_vs_r34a_ge_055"] is True      # h2h 独立归因绿
    assert ev["overall"]["pass"] is False
    sh = ev["aggregate"]["shearings"]
    assert sh["rounds"]["min"] == 4.0 and sh["rounds"]["achieve_rate"] == 0.0
    assert sh["arms"] == {"rounds_min_ge_5": False,
                          "per_sheep_min_ge_5": False}

    def _count_pmin_low(rows):   # 刀轮 5 但每羊 min=4 → 每羊臂独立红
        return {"shearings": {"total": 9, "rounds": [17, 20, 23, 26, 29],
                              "round_count": 5,
                              "per_sheep": {(0, 1, 1): 5, (0, 2, 2): 4},
                              "residuals": [], "unattributed": []},
                "care_rate": 1.0, "feed_rate": 1.0, "unknown": False,
                "verdict": None}

    _install(monkeypatch, {1000: ["win", "win"], 2000: ["win", "win"],
                          9000: ["tie", "tie"]}, count_fn=_count_pmin_low)
    ev2 = judge_league.judge_sheep_league(str(_R37), str(_R34A), [str(_OPP)],
                                          n_games=6)
    assert ev2["overall"]["criteria"]["shearings_5_achieved"] is False
    assert ev2["aggregate"]["shearings"]["arms"] == {
        "rounds_min_ge_5": True, "per_sheep_min_ge_5": False}


def test_judge_sheep_league_h2h_red(monkeypatch):
    """②h2h 路红：主对全负 rate=0.0<0.55→h2h 红而刀次绿（不翻负同源承载）。"""
    _install(monkeypatch, {1000: ["loss", "loss"], 2000: ["win", "win"],
                          9000: ["tie", "tie"]})
    ev = judge_league.judge_sheep_league(str(_R37), str(_R34A), [str(_OPP)],
                                         n_games=6)
    crit = ev["overall"]["criteria"]
    assert crit["shearings_5_achieved"] is True    # 刀次独立归因绿
    assert crit["h2h_vs_r34a_ge_055"] is False
    assert crit["win_games_not_flipped"] is False  # 胜率判承载=同源判定
    main_b = ev["aggregate"]["main"]
    assert main_b["h2h_rate"] == 0.0
    assert main_b["seed_outcomes"] == {"win": 0, "draw": 0, "loss": 1,
                                       "incomplete": 0}
    assert ev["overall"]["pass"] is False


def test_judge_sheep_league_red_no_shortcircuit(monkeypatch):
    """③单局引擎抛→标红计入 errors，其余局照跑照聚合，overall 红。"""
    _install(monkeypatch, {1000: ["win", "win"], 2000: ["win", "win"],
                          9000: ["tie", "tie"]}, boom={(1000, 1)})
    ev = judge_league.judge_sheep_league(str(_R37), str(_R34A), [str(_OPP)],
                                         n_games=6)
    games = ev["games"]
    assert len(games) == 6                        # 不短路：全计划局照跑
    reds = [g for g in games if g["red"]]
    assert len(reds) == 1
    assert reds[0]["seed"] == 1000 and reds[0]["our_seat"] == 1
    assert "synthetic engine boom" in reds[0]["error"]
    assert len(ev["errors"]) == 1 and ev["errors"][0]["seed"] == 1000
    assert ev["overall"]["n_red_games"] == 1
    assert ev["overall"]["pass"] is False         # 零红局∧零 errors fail-closed
    main_b = ev["aggregate"]["main"]
    assert main_b["seed_outcomes"]["incomplete"] == 1    # 半残对不入 h2h
    assert main_b["h2h_rate"] == 0.0
    assert ev["aggregate"]["strong"]["rate"] == 1.0      # 其余臂照聚合
    assert ev["aggregate"]["mirror"]["rate"] == 0.5


def test_judge_sheep_league_seat_pair_nocount(monkeypatch):
    """④席位翻转双计防护：6 局=3 独立 seed，h2h=(胜+0.5平)/独立局=0.8333。"""
    _install(monkeypatch, {1000: ["win", "win"], 1001: ["win", "win"],
                          1002: ["win", "loss"],
                          2000: ["win", "win"], 9000: ["tie", "tie"]})
    ev = judge_league.judge_sheep_league(str(_R37), str(_R34A), [str(_OPP)],
                                         n_games=10)
    main_b = ev["aggregate"]["main"]
    assert main_b["n_games"] == 6 and main_b["n_independent"] == 3  # 双计防护
    assert main_b["seeds"] == [1000, 1001, 1002]
    assert main_b["seed_outcomes"] == {"win": 2, "draw": 1, "loss": 0,
                                       "incomplete": 0}
    assert main_b["h2h_rate"] == 0.8333    # (2 胜+0.5×1 平)/3 独立局
    assert main_b["run_scores"] == {"wins": 5, "ties": 0, "losses": 1}
    pairs = {}
    for g in ev["games"]:
        if g["group"] == "main":
            pairs.setdefault(g["seed"], []).append(g["our_seat"])
    assert pairs == {1000: [0, 1], 1001: [0, 1], 1002: [0, 1]}
    assert ev["config"]["n_independent_planned"] == 5
    assert ev["config"]["seats_per_seed"] == 2


# ---------------------------------------------------------------------------
# ①计数对（刀数/轮数）：2 羊 3 天剪毛链
# ---------------------------------------------------------------------------
def test_count_shearings():
    rows = []
    for d in (1, 2, 3):
        base = 24 * d
        # 同拍双链：F 剪 (1,1) 羊A、h0 剪 (2,2) 羊B，次拍各 PLACE WOOL 认领
        rows.append(_row(base, farmer_op=("HARVEST",), hands_ops=[("HARVEST",)],
                         grid={(1, 1): _SHEEP, (2, 2): _SHEEP},
                         hands_pos=((2, 2),), farmer_pos=(1, 1)))
        rows.append(_row(base + 1, farmer_op=("PLACE", "WOOL", 3),
                         hands_ops=[("PLACE", "WOOL", 3)],
                         grid={(1, 1): _SHEEP, (2, 2): _SHEEP},
                         hands_pos=((2, 2),), farmer_pos=(1, 1)))
    out = count_shearings(rows)
    sh = out["shearings"]
    assert (sh["total"], sh["round_count"]) == (6, 3)     # 计数对（刀数/轮数）
    assert sh["rounds"] == [1, 2, 3]
    assert sh["per_sheep"] == {(0, 1, 1): 3, (0, 2, 2): 3}
    assert sh["residuals"] == [] and sh["unattributed"] == []
    assert out["unknown"] is False and out["verdict"] is None


# ---------------------------------------------------------------------------
# ②HARVEST 无 PLACE WOOL 的保守分支 + 选一口径（按产物推断）同钉
# ---------------------------------------------------------------------------
def test_count_shearings_lone_harvest_conservative():
    # 全程无 PLACE WOOL：非羊格（牛格/空格）与位置不可解析 → 一律不计刀
    rows = [
        _row(24, farmer_op=("HARVEST",), grid={(2, 2): _COW}, farmer_pos=(2, 2)),
        _row(25, farmer_op=("HARVEST",), grid={}, farmer_pos=(5, 5)),
        _row(26, farmer_op=("PASS",), hands_ops=[("HARVEST",)], hands_pos=()),
    ]
    out = count_shearings(rows)
    sh = out["shearings"]
    assert sh["total"] == 0 and sh["rounds"] == [] and sh["round_count"] == 0
    assert sh["per_sheep"] == {}          # 零刀→空映射（不可归属才记 None）
    assert _reasons(out) == [
        (24, 0, "F", "non_sheep_cell"),
        (25, 0, "F", "non_sheep_cell"),
        (26, 0, "h0", "unresolved_position"),
    ]
    assert sh["unattributed"] == []


def test_count_shearings_lone_harvest_product_inference():
    # 选一口径（实现 docstring 留档）：未认领但羊格 HARVEST → 按产物推断计刀
    rows = [
        _row(24, farmer_op=("HARVEST",), grid={(1, 1): _SHEEP}, farmer_pos=(1, 1)),
        _row(25, farmer_op=("PASS",), hands_ops=[("HARVEST",)],
             grid={(2, 2): _SHEEP}, hands_pos=((2, 2),)),
        _row(26),
    ]
    out = count_shearings(rows)
    sh = out["shearings"]
    assert sh["total"] == 2 and sh["rounds"] == [1]
    assert sh["per_sheep"] == {(0, 1, 1): 1, (0, 2, 2): 1}
    assert sh["residuals"] == [] and sh["unattributed"] == []


# ---------------------------------------------------------------------------
# ③非羊产物（PLACE MILK/EGG）不计剪毛 + 链假认领以对羊格定义为准
# ---------------------------------------------------------------------------
def test_count_shearings_non_wool_products():
    rows = [
        # day1：牛格 HARVEST→PLACE MILK（非 WOOL 投放不认领）
        _row(24, farmer_op=("HARVEST",), grid={(2, 2): _COW}, farmer_pos=(2, 2)),
        _row(25, farmer_op=("PLACE", "MILK", 2), farmer_pos=(2, 2)),
        # day2：鹅格 HARVEST→PLACE EGG（同上）
        _row(48, farmer_op=("HARVEST",), grid={(3, 3): _GOOSE}, farmer_pos=(3, 3)),
        _row(49, farmer_op=("PLACE", "EGG", 1), farmer_pos=(3, 3)),
        # day3：牛格 HARVEST 后同单元同日 PLACE 'WOOL'（随身存量投放）→ 假认领
        _row(72, farmer_op=("HARVEST",), grid={(5, 5): _COW}, farmer_pos=(5, 5)),
        _row(73, farmer_op=("PLACE", "WOOL", 1), farmer_pos=(5, 5)),
    ]
    out = count_shearings(rows)
    sh = out["shearings"]
    assert sh["total"] == 0 and sh["per_sheep"] == {}
    assert _reasons(out) == [
        (24, 0, "F", "non_sheep_cell"),      # MILK 链不认领
        (48, 0, "F", "non_sheep_cell"),      # EGG 链不认领
        (72, 0, "F", "chain_contradicted"),  # WOOL 链认领但格非羊→不计
    ]


# ---------------------------------------------------------------------------
# ④care_rate/feed_rate 计算（牲畜日上单元日覆盖率）
# ---------------------------------------------------------------------------
def test_count_shearings_care_feed_rates():
    grid = {(1, 1): _SHEEP}
    rows = [
        # day1 有牲畜格：F CARE、h0 FEED、h1 PASS → 3 单元日
        _row(24, farmer_op=("CARE",), hands_ops=[("FEED",), ("PASS",)],
             grid=grid, hands_pos=((0, 0), (1, 0)), farmer_pos=(0, 1)),
        _row(25, farmer_op=("PASS",), hands_ops=[("PASS",), ("PASS",)],
             grid=grid, hands_pos=((0, 0), (1, 0)), farmer_pos=(0, 1)),
        # day2 无牲畜格：CARE/FEED 不进分母（覆盖率不变）
        _row(48, farmer_op=("CARE",), hands_ops=[("FEED",)],
             grid={}, hands_pos=((0, 0),), farmer_pos=(0, 1)),
    ]
    out = count_shearings(rows)
    assert out["care_rate"] == pytest.approx(1 / 3)
    assert out["feed_rate"] == pytest.approx(1 / 3)
    # 无牲畜日 → 覆盖率未定义（None）
    out2 = count_shearings([_row(24, farmer_op=("CARE",), hands_ops=[("FEED",)],
                                 hands_pos=((0, 0),))])
    assert out2["care_rate"] is None and out2["feed_rate"] is None


# ---------------------------------------------------------------------------
# ⑤缺字段 UNKNOWN（不抛）
# ---------------------------------------------------------------------------
def test_count_shearings_unknown_missing_fields():
    good = _row(24, farmer_op=("HARVEST",), grid={(1, 1): _SHEEP}, farmer_pos=(1, 1))
    for bad in ([{"step": 1, "seat": 0}],                       # 缺 action
                [{"step": 1, "action": {"farmer": ["PASS"], "hands": [],
                                        "market": []}}],        # 缺 seat
                [{"seat": 0, "action": {"farmer": ["PASS"], "hands": [],
                                        "market": []}}],        # 缺 step
                [["not", "a", "dict"]],                         # 非 dict 行
                [{"step": "24", "seat": 0,
                  "action": {"farmer": ["PASS"], "hands": [], "market": []}}],
                [],                                             # 空输入
                None):                                          # 无输入
        out = count_shearings(bad)
        assert _unknown_shape(out), bad
    # 一行缺关键字段即整局 UNKNOWN（指标不残算）
    assert _unknown_shape(count_shearings([good, {"step": 2, "seat": 0}]))


# ---------------------------------------------------------------------------
# ⑥真 replay 样本实算（输出记 evidence/count_shearings_sample.json，可复算）
# ---------------------------------------------------------------------------
def _definition_rescan(rows):
    """定义级独立复扫：对羊格的动物格 HARVEST 事件数（product=WOOL）。"""
    total, days = 0, set()
    per: Counter = Counter()
    for r in rows:
        units = []
        fu = r["action"].get("farmer")
        if isinstance(fu, list) and fu and isinstance(fu[0], str):
            units.append(("F", fu))
        for i, h in enumerate(r["action"].get("hands") or []):
            if isinstance(h, list) and h and isinstance(h[0], str):
                units.append((i, h))
        for unit, op in units:
            if not op or op[0] != "HARVEST":
                continue
            if unit == "F":
                pos = r["farmer"]
            else:
                pos = r["hands"][unit] if unit < len(r["hands"]) else None
            if not (isinstance(pos, list) and len(pos) == 2):
                continue
            entry = (r.get("animals_grid") or {}).get((pos[0], pos[1]))
            if isinstance(entry, dict) and entry.get("type") == "SHEEP":
                total += 1
                days.add(r["step"] // 24)
                per[(r["seat"], pos[0], pos[1])] += 1
    return total, sorted(days), dict(per)


def _ser(result):
    """结果 → 证据 JSON 形态（per_sheep 键 (席,x,y) → 's席:x,y'）。"""
    out = {k: json.loads(json.dumps(v))
           for k, v in result.items() if k != "shearings"}
    sh = dict(result["shearings"])
    if sh.get("per_sheep") is not None:
        sh["per_sheep"] = {"s%d:%d,%d" % k: v
                          for k, v in sorted(sh["per_sheep"].items())}
    out["shearings"] = sh
    return out


@pytest.mark.skipif(not _REPLAY.exists(), reason="真样本缺失（/tmp/kagr22）")
def test_count_shearings_real_sample_recomputable():
    assert _EVIDENCE.exists(), \
        "缺一次性实算产物 evidence/count_shearings_sample.json"
    saved = json.loads(_EVIDENCE.read_text(encoding="utf-8"))
    assert saved["source"] == str(_REPLAY)
    assert saved["source_sha256"] == hashlib.sha256(
        _REPLAY.read_bytes()).hexdigest()

    rows = parse_episode_states(str(_REPLAY))
    out = count_shearings(rows)
    sh = out["shearings"]
    assert _ser(out) == saved["result"]            # 一次性产物=可复算（深等）

    # 定义级独立复扫（对羊格 HARVEST 事件）与计刀/按只/刀轮全对账
    total, days, per = _definition_rescan(rows)
    assert total == 124                            # 锚点：真样本刀数（双席）
    assert sh["total"] == total + len(sh["unattributed"])
    assert sh["rounds"] == days == [
        6, 9, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
        28, 29]
    assert sh["round_count"] == 19
    assert sh["per_sheep"] == per                  # 按只可复算（席,x,y）
    assert len(sh["per_sheep"]) == 21              # 11 羊格(席0)+10 羊格(席1)
    seat0 = sum(n for (seat, _, _), n in per.items() if seat == 0)
    seat1 = sum(n for (seat, _, _), n in per.items() if seat == 1)
    assert (seat0, seat1) == (65, 59)              # 锚点：逐席刀数
    assert per[(0, 3, 4)] == 8 and per[(0, 3, 2)] == 4 and per[(1, 3, 2)] == 4
    assert (1, 6, 2) not in per                    # 席1 (6,2) 无羊（镜像分歧）
    assert sh["unattributed"] == [] and sh["per_sheep"] is not None

    # 保守分支留档对账：全部未计刀候选 + 假认领 1 例（step366 席1 h6）
    assert Counter(r["reason"] for r in sh["residuals"]) == {
        "non_sheep_cell": 770, "unresolved_position": 32,
        "chain_contradicted": 1}
    assert [r for r in sh["residuals"] if r["reason"] == "chain_contradicted"] \
        == [{"step": 366, "seat": 1, "unit": "h6", "day": 15,
             "reason": "chain_contradicted"}]

    # 照顾覆盖率锚点：263/632（CARE）、219/632（FEED）单元日占比
    assert out["care_rate"] == pytest.approx(263 / 632)
    assert out["feed_rate"] == pytest.approx(219 / 632)
    assert out["unknown"] is False and out["verdict"] is None
