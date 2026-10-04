# -*- coding: utf-8 -*-
"""R23 测试面：route_library（续段库/开局长相聚类/败局世界补路由）。

组内五件：迷你语料聚类 / 族键稳定（跨 build+runtime 同键）/ 败局世界覆盖审计 /
语料不足+解析失败即抛 / 真跑建库（evidence/route_library_realrun.json）。
"""
import json
from pathlib import Path

import pytest  # noqa: F401

try:
    from orderbook_r40 import route_library
except ImportError:  # 兜底：直接以 orderbook_r40/ 为 sys.path 根跑测
    import route_library
try:
    from orderbook_r40.runtime_r40 import _route40_select
except ImportError:
    from runtime_r40 import _route40_select

SHOP_ROUTE_MAP = {
    "BAKERY+FARMERS_MARKET": 5,
    "PET_CAFE+YARN_STORE": 9,
    "PIZZA_SHOP+SMOOTHIE_SHOP": 12,
}
LOSS_IDS = [113735225, 113817068, 113754147, 113852533, 113962831, 113724375,
            113837634, 113873625, 114064544, 113838925, 113764768, 113738419]


def _step_val(table, t):
    val = table.get(0, 0)
    for k in sorted(table):
        if k <= t:
            val = table[k]
    return val


def _make_replay(path, episode, hands_at, uq_at, crops_144, shops_144,
                 our_money_at, opp_money_at, opp_sells=(), opp_animals=None,
                 n_steps=150):
    """迷你 replay 生成：entry t 的观察=步标 t（与真 replay 同约定）。"""
    steps = []
    for t in range(n_steps):
        our_money = _step_val(our_money_at, t)
        opp_money = _step_val(opp_money_at, t)
        crops = dict(crops_144) if t == 144 else {}
        tiles = [[{"kind": "PLANT", "crop": c} for c, n in sorted(crops.items())
                  for _ in range(n)]]
        opp_tiles = [[{"kind": "PASTURE", "animal": a} for a, n in
                      sorted((opp_animals or {}).items()) for _ in range(n)]] \
            if (opp_animals and t == n_steps - 1) else [[]]
        farms = [
            {"money": float(opp_money), "hands": [], "unlocked_quadrants": ["NW"],
             "tiles": opp_tiles},
            {"money": float(our_money),
             "hands": [[0, 0]] * _step_val(hands_at, t),
             "unlocked_quadrants": ["NW"] * _step_val(uq_at, t),
             "tiles": tiles},
        ]
        sells = [s for s in opp_sells if s[0] == t]
        entries = []
        for seat in (0, 1):
            obs = {"day": t // 24, "hour": t % 24, "player": seat, "farms": farms,
                   "market": {"inventory": {"WHEAT": 9989},
                              "prices": {"MILK": 100, "WHEAT": 10}},
                   "town": {"unlocked_shops": list(shops_144) if t == 144 else []}}
            act = {"farmer": ["PASS"], "hands": [],
                   "market": [["SELL", s[1], s[2]] for s in sells] if seat == 0
                   else []}
            entries.append({"action": act, "observation": obs})
        steps.append(entries)
    data = {"info": {"TeamNames": ["opp", "renyxin"], "EpisodeId": episode},
            "rewards": [float(_step_val(opp_money_at, n_steps - 1)),
                        float(_step_val(our_money_at, n_steps - 1))],
            "steps": steps}
    Path(path).write_text(json.dumps(data), encoding="utf-8")
    return data


def _obs_stream(path, seat=1):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [e[seat]["observation"] for e in data["steps"]]


def _write_corpus(tmp_path, specs):
    files = []
    for i, spec in enumerate(specs):
        p = tmp_path / ("episode-%d-replay.json" % (1000 + i))
        _make_replay(p, 1000 + i, **spec)
        files.append(str(p))
    return files


# 迷你语料 12 局/6 族：A(3,2胜) B(2,2胜) C(2,unknown route) E(1败 milk+1胜)
# F(1败 wool) G(1败 goose+1胜)。
def _mini_corpus_specs():
    A = dict(hands_at={0: 0, 1: 2}, uq_at={0: 1, 50: 2}, crops_144={"WHEAT": 5},
             shops_144=["BAKERY", "FARMERS_MARKET"])
    E = dict(hands_at={0: 0, 1: 1}, uq_at={0: 1}, crops_144={"MELON": 3},
             shops_144=["BAKERY", "FARMERS_MARKET"])
    G = dict(hands_at={0: 0, 1: 1}, uq_at={0: 1}, crops_144={"MELON": 3},
             shops_144=["PET_CAFE", "YARN_STORE"])
    return [
        # A 族 "2|1|WHEAT:5|BAKERY+FARMERS_MARKET" → route 5
        dict(A, our_money_at={0: 1000.0, 144: 2500.0, 149: 10000.0},
             opp_money_at={0: 1000.0, 144: 2000.0, 149: 9000.0}),
        dict(A, our_money_at={0: 1000.0, 144: 1000.0, 149: 12000.0},
             opp_money_at={0: 1000.0, 144: 1000.0, 149: 10000.0}),
        dict(A, our_money_at={0: 1000.0, 144: 2000.0, 149: 9500.0},
             opp_money_at={0: 1000.0, 144: 2100.0, 149: 10000.0}),
        # B 族 "3|1|WHEAT:5|PET_CAFE+YARN_STORE" → route 9
        dict(hands_at={0: 0, 1: 3}, uq_at={0: 1, 60: 2}, crops_144={"WHEAT": 5},
             shops_144=["PET_CAFE", "YARN_STORE"],
             our_money_at={0: 1000.0, 144: 1000.0, 149: 10200.0},
             opp_money_at={0: 1000.0, 144: 1000.0, 149: 10000.0}),
        dict(hands_at={0: 0, 1: 3}, uq_at={0: 1, 60: 2}, crops_144={"WHEAT": 5},
             shops_144=["PET_CAFE", "YARN_STORE"],
             our_money_at={0: 1000.0, 144: 1300.0, 149: 10400.0},
             opp_money_at={0: 1000.0, 144: 1000.0, 149: 10000.0}),
        # C 族 "2|1|WHEAT:5|FOO_SHOP+BAR_SHOP" → route unknown
        dict(A, shops_144=["FOO_SHOP", "BAR_SHOP"],
             our_money_at={0: 1000.0, 144: 1000.0, 149: 10700.0},
             opp_money_at={0: 1000.0, 144: 1000.0, 149: 10000.0}),
        dict(A, shops_144=["FOO_SHOP", "BAR_SHOP"],
             our_money_at={0: 1000.0, 144: 1000.0, 149: 9900.0},
             opp_money_at={0: 1000.0, 144: 1000.0, 149: 10000.0}),
        # E 族 "1|0|MELON:3|BAKERY+FARMERS_MARKET" → route 5；E1=milk 败局
        dict(E, our_money_at={0: 1000.0, 144: 1000.0, 149: 500.0},
             opp_money_at={0: 1000.0, 50: 2000.0, 144: 2000.0, 149: 2000.0},
             opp_sells=[(50, "MILK", 10)], opp_animals={"COW": 8}),
        dict(E, our_money_at={0: 1000.0, 144: 1000.0, 149: 3000.0},
             opp_money_at={0: 1000.0, 50: 2000.0, 144: 2000.0, 149: 2000.0},
             opp_sells=[(50, "MILK", 10)], opp_animals={"COW": 8}),
        # F 族 "4|2|CARROT:2|PIZZA_SHOP+SMOOTHIE_SHOP" → route 12；wool 败局
        dict(hands_at={0: 0, 1: 4}, uq_at={0: 1, 30: 2, 70: 3},
             crops_144={"CARROT": 2}, shops_144=["PIZZA_SHOP", "SMOOTHIE_SHOP"],
             our_money_at={0: 1000.0, 144: 1000.0, 149: 3000.0},
             opp_money_at={0: 1000.0, 144: 1000.0, 149: 5000.0},
             opp_animals={"SHEEP": 12}),
        # G 族 "1|0|MELON:3|PET_CAFE+YARN_STORE" → route 9；G1=goose 败局
        dict(G, our_money_at={0: 1000.0, 144: 1000.0, 149: 3000.0},
             opp_money_at={0: 1000.0, 144: 1000.0, 149: 5000.0},
             opp_animals={"GOOSE": 6}),
        dict(G, our_money_at={0: 1000.0, 144: 1000.0, 149: 6000.0},
             opp_money_at={0: 1000.0, 144: 1000.0, 149: 5000.0},
             opp_animals={"GOOSE": 6}),
    ]


def test_build_route_library_mini_corpus(tmp_path):
    """迷你语料聚类：族项/segments/best_route/unknown 族口径。"""
    files = _write_corpus(tmp_path, _mini_corpus_specs())
    out = route_library.build_route_library(files, {
        "min_games": 10, "shop_route_map": SHOP_ROUTE_MAP})
    lib = out["library"]
    assert out["build_audit"] is lib["build_audit"]
    assert lib["version"] == "routelib/1.0"
    fams = lib["families"]
    assert set(fams) == {
        "2|1|WHEAT:5|BAKERY+FARMERS_MARKET",
        "3|1|WHEAT:5|PET_CAFE+YARN_STORE",
        "2|1|WHEAT:5|FOO_SHOP+BAR_SHOP",
        "1|0|MELON:3|BAKERY+FARMERS_MARKET",
        "4|2|CARROT:2|PIZZA_SHOP+SMOOTHIE_SHOP",
        "1|0|MELON:3|PET_CAFE+YARN_STORE",
    }
    fam_a = fams["2|1|WHEAT:5|BAKERY+FARMERS_MARKET"]
    assert fam_a["n_games"] == 3
    assert fam_a["win_rate"] == pytest.approx(2 / 3)
    assert fam_a["margin_mean"] == pytest.approx((1000.0 + 2000.0 - 500.0) / 3)
    assert fam_a["best_route"] == 5
    seg = fam_a["segments"]["5"]
    assert seg["n"] == 3 and seg["win_rate"] == pytest.approx(2 / 3)
    assert seg["margin_mean"] == pytest.approx((500.0 + 2000.0 - 400.0) / 3)
    fam_c = fams["2|1|WHEAT:5|FOO_SHOP+BAR_SHOP"]
    assert fam_c["n_games"] == 2 and fam_c["win_rate"] == 0.5
    assert fam_c["segments"] == {}      # unknown 局不进 segments
    assert fam_c["best_route"] is None  # unknown 胜局不进选优
    fam_f = fams["4|2|CARROT:2|PIZZA_SHOP+SMOOTHIE_SHOP"]
    assert fam_f["best_route"] is None  # 无胜局族无 best_route
    assert fam_f["segments"]["12"]["n"] == 1
    assert lib["default"]["n_games"] == 12
    assert lib["default"]["win_rate"] == pytest.approx(7 / 12)
    assert lib["default"]["best_route"] == 5   # 胜局续段 margin 均值最优
    audit = out["build_audit"]
    assert audit["n_games"] == 12 and audit["n_families"] == 6
    assert audit["coverage"] == pytest.approx(4 / 6)  # C(unknown)/F(无胜局) 未覆盖
    assert len(audit["library_sha"]) == 64


def test_family_key_stable(tmp_path):
    """族键稳定：双跑建库同键同 sha；runtime 同观察流出同族键同选路。"""
    files = _write_corpus(tmp_path, _mini_corpus_specs())
    cfg = {"min_games": 10, "shop_route_map": SHOP_ROUTE_MAP}
    out1 = route_library.build_route_library(files, cfg)
    out2 = route_library.build_route_library(files, cfg)
    assert sorted(out1["library"]["families"]) == sorted(out2["library"]["families"])
    assert out1["build_audit"]["library_sha"] == out2["build_audit"]["library_sha"]
    latch = route_library._load_latch(cfg)
    for f in files:
        row = route_library._parse_game(f, "renyxin", latch)
        stream = _obs_stream(f)
        _route40_select._fp_state = None
        res = {}
        for t in range(0, 150):
            res = _route40_select(stream[t], out1["library"])
        assert res["family"] == row["family_key"]          # 跨件同键
        fam_entry = out1["library"]["families"][row["family_key"]]
        assert res["route"] == fam_entry["best_route"]      # 跨件同选路
        assert _route40_select(stream[149], out1["library"]) == res  # 锁定


def test_defeat_worlds_coverage_audit(tmp_path):
    """败局世界覆盖审计：三型归族+covered 判定+uncovered 清单。"""
    files = _write_corpus(tmp_path, _mini_corpus_specs())
    out = route_library.build_route_library(files, {
        "min_games": 10, "shop_route_map": SHOP_ROUTE_MAP})
    worlds = out["library"]["defeat_worlds"]
    assert set(worlds) == {"milk_flow", "wool_flow", "goose_flow"}
    assert worlds["milk_flow"]["families"] == ["1|0|MELON:3|BAKERY+FARMERS_MARKET"]
    assert worlds["milk_flow"]["covered"] is True   # E 族有胜局 best_route=5
    assert worlds["wool_flow"]["families"] == ["4|2|CARROT:2|PIZZA_SHOP+SMOOTHIE_SHOP"]
    assert worlds["wool_flow"]["covered"] is False  # F 族无胜局
    assert worlds["goose_flow"]["families"] == ["1|0|MELON:3|PET_CAFE+YARN_STORE"]
    assert worlds["goose_flow"]["covered"] is True  # G 族有胜局 best_route=9
    assert "2|1|WHEAT:5|BAKERY+FARMERS_MARKET" not in \
        worlds["milk_flow"]["families"]            # 胜局族不入败局世界
    assert set(out["build_audit"]["uncovered_families"]) == {
        "2|1|WHEAT:5|FOO_SHOP+BAR_SHOP", "4|2|CARROT:2|PIZZA_SHOP+SMOOTHIE_SHOP"}


def test_corpus_fail_closed(tmp_path):
    """fail-closed：语料 <30 局即抛；坏 JSON/步标错位即抛。"""
    with pytest.raises(ValueError):
        route_library.build_route_library(
            _write_corpus(tmp_path, [dict(_mini_corpus_specs()[0])] * 5))
    tmp2 = tmp_path / "corpus2"
    tmp2.mkdir()
    files = _write_corpus(tmp2, [dict(_mini_corpus_specs()[0])] * 30)
    Path(files[3]).write_text("{ not json", encoding="utf-8")
    with pytest.raises(ValueError):
        route_library.build_route_library(files, {"shop_route_map": SHOP_ROUTE_MAP})
    tmp3 = tmp_path / "corpus3"
    tmp3.mkdir()
    files = _write_corpus(tmp3, [dict(_mini_corpus_specs()[0])] * 30)
    bad = json.loads(Path(files[5]).read_text(encoding="utf-8"))
    bad["steps"][7][1]["observation"]["hour"] = 99   # 步标错位
    Path(files[5]).write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(ValueError):
        route_library.build_route_library(files, {"shop_route_map": SHOP_ROUTE_MAP})


def test_realrun_build_evidence():
    """真跑建库：kagr23+kagr22+analysis24 败局 12 局→evidence 落盘。"""
    bases = [Path("/tmp/kagr23"), Path("/tmp/kagr22")]
    if not all(b.is_dir() for b in bases):
        pytest.skip("真跑语料缺失: /tmp/kagr23 /tmp/kagr22")
    files = []
    for b in bases:
        files += [str(p) for p in sorted(b.glob("episode-*-replay.json"))]
    located = []
    for eid in LOSS_IDS:
        hit = next((Path(base) / ("episode-%d-replay.json" % eid)
                    for base in ("/tmp/kagr23", "/tmp/kagr22", "/tmp/kagr24")
                    if (Path(base) / ("episode-%d-replay.json" % eid)).exists()),
                   None)
        if hit is None:
            pytest.skip("败局 replay 缺（需 kaggle CLI 拉取）: %d" % eid)
        located.append(str(hit))
    out = route_library.build_route_library(files + located, None)
    lib, audit = out["library"], out["build_audit"]
    assert audit["n_games"] == 77          # 55+16+6 去重后
    assert audit["n_families"] >= 10
    assert 0.0 < audit["coverage"] <= 1.0
    worlds = lib["defeat_worlds"]
    assert all(worlds[w]["families"] for w in worlds)
    latch = route_library._load_latch({})
    assert latch is not None               # r37 锁存表自动发现
    rows = []
    seen = set()
    for f in files + located:
        r = route_library._parse_game(f, "renyxin", latch)
        if r["episode"] in seen:
            continue                      # 败局文件与 kagr23/kagr22 重复按 episode 去重
        seen.add(r["episode"])
        rows.append({"episode": r["episode"], "family_key": r["family_key"],
                     "win": r["win"], "margin": r["margin"],
                     "seg_margin": r["seg_margin"], "route": r["route"]})
    rows.sort(key=lambda r: r["episode"])
    known = sum(1 for r in rows if r["route"] != "unknown")
    wins = sum(1 for r in rows if r["win"])
    ev = {
        "corpus": {"sources": [str(b) for b in bases] + ["analysis24 败局 12 局"],
                   "n_games": audit["n_games"],
                   "loss_ids": LOSS_IDS,
                   "route_known_games": known, "win_games": wins},
        "build_audit": audit,
        "defeat_worlds": worlds,
        "families": {k: v for k, v in sorted(lib["families"].items())},
        "games": rows,
        "library": lib,
    }
    ev_path = Path(__file__).resolve().parent / "evidence" / \
        "route_library_realrun.json"
    ev_path.parent.mkdir(parents=True, exist_ok=True)
    ev_path.write_text(json.dumps(ev, ensure_ascii=False, indent=1),
                       encoding="utf-8")
    assert ev_path.exists() and known > 0 and wins > 0
