# -*- coding: utf-8 -*-
"""R19/R20 测试面：parse_states（逐步双席规范行/考古口径 step↔si 差 1）。

parse_episode_states 真测试五组（责任契约 fn_docs/hybrid/responsibility.md
【R19/R20 增补·共享函数】parse_episode_states 行 + B19 实现口径）：
①真 replay 实解析——/tmp/kagr22 灾难局 6 局任一（720 步×2 席）：1440 行、
  行序 rows[2*t+seat]、逐步双席齐、契约字段齐、animals_grid⊆tiles、牲畜条目
  带 type/fed_today/consecutive_unfed、tiles 条目带 type；
②最小合法 replay（2 步 2 席）——构造件全等断言：字段值/两格映射 (x,y) 取法
  （tiles[y][x]）/identity→type 改名/观察子键缺即省略（GOOSE 格无 fed_today
  即不出现在条目）/inventory 合计（shed+seeds+inventories）/per-own private
  （两席 inventory 互异）；
③缺字段/格式不符即抛——24 例：顶层/steps/双席/action/observation/day/hour/
  farms/private/money/hands/tiles/farmer 缺、坏型、cell 非 None/LOCKED/dict、
  cell 缺 crop/kind、obs.step 与记录序不符 → ValueError 且消息含缺什么；
④坏 JSON/不存在即抛——坏 JSON→ValueError、缺文件→FileNotFoundError；
⑤口径钉住（step 换算）——step=replay 原生序 si（rows[i].step==i//2，非磁带
  步）；磁带 step X 动作在 step=X+1 行：三张 HIRE（由 si=24 观测算出）落
  step 25 行且状态为执行后值（money 22.0→18.0）；d1 h0 判据取 step 24 行
  （day==1,hour==0，现金席0=22.0/席1=1.0，分析22 race_table techtech69 局
  我1/对手22）；羊格 (4,1) type=SHEEP 在 step 700 席0 行。
"""
import json
from pathlib import Path

import pytest  # noqa: F401

try:
    from orderbook_r37 import parse_states
except ImportError:  # 兜底：直接以 orderbook_r37/ 为 sys.path 根跑测
    import parse_states

parse_episode_states = parse_states.parse_episode_states

_HERE = Path(__file__).resolve().parent
_REPLAY_DIR = Path("/tmp/kagr22")
_EPISODE_IDS = (112938600, 112968467, 112976582, 113002280, 113094793, 113099386)
_NAMED = _REPLAY_DIR / "episode-112938600-replay.json"  # 法证钉值取自该局
_CONTRACT_KEYS = {"step", "seat", "action", "money", "hands", "animals_grid", "tiles"}


# ---------------------------------------------------------------------------
# 构造件：最小合法 replay（2 步 2 席）
# ---------------------------------------------------------------------------
def _mini() -> dict:
    plant = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 0,
             "watered_today": True, "consecutive_unwatered": 0,
             "fertilized_until_day": -1, "max_lifespan_step": 168,
             "yield_units": 1}
    cow = {"kind": "PASTURE", "animal": "COW", "fed_today": True,
           "consecutive_unfed": 0, "cared_today": True,
           "fertilizer_available": False, "pending_care_bonus": 0,
           "placed_day": 0, "yield_units": 0}
    coop = {"kind": "COOP"}
    goose = {"kind": "COOP", "animal": "GOOSE"}  # 无 fed_today/consecutive_unfed
    tiles = [[plant, cow, None], ["LOCKED", coop, goose]]

    def farm(money, hands, farmer):
        return {"farmer": farmer, "hands": hands, "hires_today": 0,
                "money": money, "tiles": tiles, "unlocked_quadrants": ["NW"]}

    def entry(t, seat):
        obs = {
            "day": 0, "hour": t,
            "farms": [farm(100.0 + t, [[0, 0]], [1, 1]),
                      farm(200.0 + t, [], [2, 0])],
            "player": seat,
            "private": ({"shed": {"COW": 1, "WOOL": 2}, "seeds": {"WHEAT": 3},
                         "inventories": [{"WOOL": 1}, {"COW": 2}]} if seat == 0
                        else {"shed": {"COW": 5}, "seeds": {}, "inventories": []}),
            "remainingOverageTime": 60,
            "town": {"unlocked_shops": []},
        }
        if seat == 0:  # 实物口径：席0 带 step、席1 全缺
            obs["step"] = t
        action = ({"farmer": ["PASS"], "hands": [], "market": []} if t == 0 else
                  {"farmer": ["NORTH"], "hands": [["PASS"]],
                   "market": [["SELL", "WHEAT", 1]]})
        return {"action": action, "info": {}, "observation": obs,
                "reward": 0, "status": "ACTIVE"}

    return {"configuration": {}, "id": "mini", "info": {"TeamNames": ["a", "b"]},
            "statuses": ["ACTIVE", "ACTIVE"],
            "steps": [[entry(0, 0), entry(0, 1)], [entry(1, 0), entry(1, 1)]]}


_COW_ENTRY = {"type": "COW", "kind": "PASTURE", "fed_today": True,
              "consecutive_unfed": 0, "cared_today": True,
              "fertilizer_available": False, "pending_care_bonus": 0,
              "placed_day": 0, "yield_units": 0}
_GOOSE_ENTRY = {"type": "GOOSE", "kind": "COOP"}  # 缺即省略子键
_PLANT_TILE = {"type": "WHEAT", "kind": "PLANT", "planted_day": 0,
               "watered_today": True, "consecutive_unwatered": 0,
               "fertilized_until_day": -1, "max_lifespan_step": 168,
               "yield_units": 1}
_COW_TILE = {"type": "PASTURE", "animal": "COW", "fed_today": True,
             "consecutive_unfed": 0, "cared_today": True,
             "fertilizer_available": False, "pending_care_bonus": 0,
             "placed_day": 0, "yield_units": 0}
_MINI_GRIDS = (
    {(1, 0): _COW_ENTRY, (2, 1): _GOOSE_ENTRY},
    {(0, 0): _PLANT_TILE, (1, 0): _COW_TILE,
     (1, 1): {"type": "COOP"}, (2, 1): {"type": "COOP", "animal": "GOOSE"}},
)


def _dump(tmp_path, payload) -> str:
    p = tmp_path / "replay.json"
    if isinstance(payload, str):
        p.write_text(payload, encoding="utf-8")
    else:
        p.write_text(json.dumps(payload), encoding="utf-8")
    return str(p)


def _first_real() -> Path:
    for eid in _EPISODE_IDS:
        p = _REPLAY_DIR / f"episode-{eid}-replay.json"
        if p.is_file():
            return p
    raise FileNotFoundError(f"真 replay 样本缺失：{_REPLAY_DIR}/episode-*-replay.json")


# ---------------------------------------------------------------------------
# ①真 replay 实解析（6 局任一）
# ---------------------------------------------------------------------------
def test_real_replay_structure():
    rows = parse_episode_states(str(_first_real()))
    assert len(rows) == 1440  # 6 局均 720 步 × 2 席
    for i, row in enumerate(rows):
        assert row["step"] == i // 2 and row["seat"] == i % 2  # rows[2*t+seat]
        assert _CONTRACT_KEYS <= set(row)
        assert set(row["action"]) == {"farmer", "hands", "market"}
        assert isinstance(row["day"], int) and isinstance(row["hour"], int)
        assert set(row["animals_grid"]) <= set(row["tiles"])
        for entry in row["animals_grid"].values():
            assert {"type", "fed_today", "consecutive_unfed"} <= set(entry)
        for entry in row["tiles"].values():
            assert "type" in entry
    assert sorted({r["step"] for r in rows}) == list(range(720))


# ---------------------------------------------------------------------------
# ②最小合法 replay（2 步 2 席）全等断言
# ---------------------------------------------------------------------------
def test_minimal_replay_exact(tmp_path):
    rows = parse_episode_states(_dump(tmp_path, _mini()))
    assert len(rows) == 4
    assert rows[0] == {
        "step": 0, "seat": 0, "day": 0, "hour": 0,
        "action": {"farmer": ["PASS"], "hands": [], "market": []},
        "money": 100.0, "hands": [[0, 0]], "farmer": [1, 1],
        "animals_grid": _MINI_GRIDS[0], "tiles": _MINI_GRIDS[1],
        "inventory": {"COW": 3, "WOOL": 3, "WHEAT": 3},
    }
    assert rows[1]["seat"] == 1 and rows[1]["money"] == 200.0
    assert rows[1]["hands"] == [] and rows[1]["farmer"] == [2, 0]
    assert rows[1]["inventory"] == {"COW": 5}  # private 为该席私有
    assert rows[2] == dict(rows[0], step=1, hour=1, money=101.0,
                           action={"farmer": ["NORTH"], "hands": [["PASS"]],
                                   "market": [["SELL", "WHEAT", 1]]})
    assert rows[3]["step"] == 1 and rows[3]["seat"] == 1 and rows[3]["money"] == 201.0
    # 取法钉：GOOSE 格（网格 [1][2]）→ 键 (2,1)；缺观察子键即省略
    assert rows[0]["animals_grid"][(2, 1)] == {"type": "GOOSE", "kind": "COOP"}
    assert rows[0]["tiles"][(1, 0)]["type"] == "PASTURE"
    assert rows[0]["tiles"][(0, 0)]["type"] == "WHEAT"


# ---------------------------------------------------------------------------
# ③缺字段/格式不符即抛
# ---------------------------------------------------------------------------
def _no_steps(d):
    return {k: v for k, v in d.items() if k != "steps"}


_MUTATIONS = [
    ("top_not_dict", lambda d: [], "顶层"),
    ("no_steps", _no_steps, "steps"),
    ("steps_one_seat", lambda d: (d["steps"][0].pop(), d)[1], "席"),
    ("entry_not_dict", lambda d: (d["steps"][0].__setitem__(0, 5), d)[1], "dict"),
    ("no_action", lambda d: (d["steps"][0][0].pop("action"), d)[1], "action"),
    ("no_observation", lambda d: (d["steps"][0][0].pop("observation"), d)[1],
     "observation"),
    ("action_not_dict", lambda d: (d["steps"][0][0].__setitem__("action", []), d)[1],
     "action"),
    ("action_no_market", lambda d: (d["steps"][0][0]["action"].pop("market"), d)[1],
     "market"),
    ("obs_no_day", lambda d: (d["steps"][0][0]["observation"].pop("day"), d)[1], "day"),
    ("obs_no_hour", lambda d: (d["steps"][0][0]["observation"].pop("hour"), d)[1],
     "hour"),
    ("obs_no_farms", lambda d: (d["steps"][0][0]["observation"].pop("farms"), d)[1],
     "farms"),
    ("obs_no_private", lambda d: (d["steps"][0][0]["observation"].pop("private"), d)[1],
     "private"),
    ("obs_step_mismatch",
     lambda d: (d["steps"][1][1]["observation"].__setitem__("step", 9), d)[1], "step"),
    ("farms_one", lambda d: (d["steps"][0][0]["observation"].__setitem__(
        "farms", d["steps"][0][0]["observation"]["farms"][:1]), d)[1], "farms"),
    ("farm_no_money",
     lambda d: (d["steps"][0][0]["observation"]["farms"][0].pop("money"), d)[1],
     "money"),
    ("farm_no_hands",
     lambda d: (d["steps"][0][0]["observation"]["farms"][0].pop("hands"), d)[1],
     "hands"),
    ("farm_no_farmer",
     lambda d: (d["steps"][0][0]["observation"]["farms"][0].pop("farmer"), d)[1],
     "farmer"),
    ("farm_no_tiles",
     lambda d: (d["steps"][0][0]["observation"]["farms"][0].pop("tiles"), d)[1],
     "tiles"),
    ("money_not_num", lambda d: (d["steps"][0][0]["observation"]["farms"][0]
                                 .__setitem__("money", "100"), d)[1], "money"),
    ("tiles_not_list", lambda d: (d["steps"][0][0]["observation"]["farms"][0]
                                  .__setitem__("tiles", 5), d)[1], "tiles"),
    ("tiles_row_not_list", lambda d: (d["steps"][0][0]["observation"]["farms"][0]
                                      ["tiles"].__setitem__(0, 5), d)[1], "tiles"),
    ("cell_bad_type", lambda d: (d["steps"][0][0]["observation"]["farms"][0]
                                 ["tiles"][0].__setitem__(2, 7), d)[1], "tiles"),
    ("cell_no_identity", lambda d: (d["steps"][0][0]["observation"]["farms"][0]
                                    ["tiles"][0].__setitem__(1, {"animal": "COW"}),
                                    d)[1], "crop/kind"),
    ("private_not_dict", lambda d: (d["steps"][0][0]["observation"]
                                    .__setitem__("private", 3), d)[1], "private"),
    ("inventories_not_list", lambda d: (d["steps"][0][0]["observation"]["private"]
                                        .__setitem__("inventories", 5), d)[1],
     "inventories"),
]


@pytest.mark.parametrize("name,mutate,match", _MUTATIONS,
                         ids=[m[0] for m in _MUTATIONS])
def test_missing_or_bad_fields_raise(tmp_path, name, mutate, match):
    payload = mutate(_mini())
    with pytest.raises(ValueError, match=match):
        parse_episode_states(_dump(tmp_path, payload))


# ---------------------------------------------------------------------------
# ④坏 JSON/不存在即抛
# ---------------------------------------------------------------------------
def test_bad_json_and_missing_file(tmp_path):
    with pytest.raises(ValueError, match="JSON"):
        parse_episode_states(_dump(tmp_path, "{not json"))
    with pytest.raises(FileNotFoundError):
        parse_episode_states(str(tmp_path / "no-such-replay.json"))


# ---------------------------------------------------------------------------
# ⑤口径钉住（step 换算）
# ---------------------------------------------------------------------------
def test_step_caliber_pinned():
    rows = parse_episode_states(str(_NAMED))
    # step = replay 原生序 si（非磁带步）：rows[i] 就是 steps[i//2][i%2]
    for i in (0, 1, 2, 3, 47, 48, 49, 50, 51, 1439):
        assert rows[i]["step"] == i // 2 and rows[i]["seat"] == i % 2
    # d1 h0 判据取 step 24 行（day==1,hour==0）；现金钉分析22 race_table
    # （techtech69 局 d1 h0 我1/对手22，席0=techtech69）
    r24_0, r24_1 = rows[2 * 24], rows[2 * 24 + 1]
    assert (r24_0["day"], r24_0["hour"], r24_0["money"]) == (1, 0, 22.0)
    assert (r24_1["day"], r24_1["hour"], r24_1["money"]) == (1, 0, 1.0)
    # 磁带 step X 动作在 step=X+1 行：三张 HIRE（由 si=24=磁带步 24 观测算出）
    # 落 step 25 行，且该行状态为执行后值（money 22.0→18.0、手 0→3）
    r25_0 = rows[2 * 25]
    assert r25_0["action"]["market"] == [["HIRE"], ["HIRE"], ["HIRE"]]
    assert r25_0["money"] == 18.0 and len(r25_0["hands"]) == 3
    # 牲畜格实测钉：step 700 席0 行 (x,y)=(4,1) 即 tiles[1][4]
    r700_0 = rows[2 * 700]
    sheep = r700_0["animals_grid"][(4, 1)]
    assert sheep["type"] == "SHEEP" and sheep["consecutive_unfed"] == 1
    assert sheep["fed_today"] is False and sheep["cared_today"] is False
    assert r700_0["tiles"][(4, 1)]["type"] == "PASTURE"
