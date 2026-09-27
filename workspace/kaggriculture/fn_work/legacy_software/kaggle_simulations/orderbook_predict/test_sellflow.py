# -*- coding: utf-8 -*-
"""R22 测试面：sellflow（卖流库构建 v2：top-30 重采+新旧合并+命中字段）。

v1 组（语义不回退，垫语料满足 ≥30 局门）：①迷你建库（键/窗/直方计数/对手席/
空槽/自家单排除）②无 renyxin 席跳过计数 ③坏文件 fail-closed 抛。
v2 组：①top-30 截取（55→30 按时间序）②新旧库合并（同键计数相加/新库 hit 字段
优先）③hit 字段计算（4 样本 3 命中→hits=3/rate=0.75）④样本 <3 缺省兼容
⑤<30 局抛 ⑥真跑建库（30 新+86 旧）记 evidence/sellflow_library_v2_realrun.json。
"""
from __future__ import annotations

import hashlib
import json
import os

import pytest

from orderbook_predict.sellflow import build_sellflow_library

REAL_FRESH_DIR = os.environ.get("SELLFLOW_REPLAY_DIR", "/tmp/kagr23")
REAL_AUX_DIR = os.environ.get("SELLFLOW_REAL_AUX_DIR", "/tmp/r33audit")
_EVIDENCE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "evidence", "sellflow_library_v2_realrun.json"
)


@pytest.fixture(autouse=True)
def _no_aux(monkeypatch):
    """默认屏蔽辅助库（真辅助语料 /tmp/r33audit 隔离）；用到辅助库的测试自行覆盖。"""
    monkeypatch.setenv("SELLFLOW_AUX_REPLAY_DIR", "")


def _mk_replay(
    team_names,
    opp_money,
    opp_wheat,
    opp_sells=None,
    own_sells=None,
    shops=None,
    n_steps=64,
    create_time=None,
):
    """构造迷你 replay：对手席发 opp_sells（附空槽），renyxin 席发 own_sells。"""
    opp_sells = opp_sells or {}
    own_sells = own_sells or {}
    shops = shops or {}
    if "renyxin" in team_names:
        renyxin_seat = team_names.index("renyxin")
        opp_seat = 1 - renyxin_seat
    else:
        renyxin_seat = None
        opp_seat = 1  # 无 renyxin 席：随便挂一席，整局会被跳过
    steps = []
    for i in range(n_steps):
        unlocked = list(shops.get(i, []))
        opp_orders = [["SELL", it, q] for (it, q) in opp_sells.get(i, [])] + [[]]
        own_orders = [["SELL", it, q] for (it, q) in own_sells.get(i, [])]
        players = []
        for seat in (0, 1):
            farms = [{"money": 3000.0}, {"money": 3000.0}]
            farms[opp_seat]["money"] = float(opp_money)
            market_orders = (
                opp_orders if seat == opp_seat else (own_orders if seat == renyxin_seat else [])
            )
            players.append(
                {
                    "action": {"farmer": ["PASS"], "hands": [], "market": market_orders},
                    "observation": {
                        "player": seat,
                        "farms": farms,
                        "market": {"inventory": {"WHEAT": opp_wheat}},
                        "town": {"unlocked_shops": unlocked},
                    },
                }
            )
        steps.append(players)
    out = {"info": {"TeamNames": list(team_names)}, "steps": steps}
    if create_time is not None:
        out["createTime"] = create_time
    return out


def _write(tmp_path, name, obj):
    p = tmp_path / name
    if isinstance(obj, str):
        p.write_text(obj, encoding="utf-8")
    else:
        p.write_text(json.dumps(obj), encoding="utf-8")
    return str(p)


def _pad(tmp_path, n, money_base=1000000):
    """垫 n 局无对手卖单语料（满足 ≥30 局门；不产生任何键/事件）。"""
    for i in range(n):
        _write(
            tmp_path,
            f"episode-pad{i}-replay.json",
            _mk_replay(["renyxin", "oppPad"], money_base + i, 9000, n_steps=8),
        )


def _sha_of(lib):
    return hashlib.sha256(
        json.dumps(lib, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


# ---------------- v1 组（语义不回退；垫语料满足 v2 ≥30 局门） ----------------


def test_build_sellflow_library_keys_windows_hist(tmp_path):
    """v1①迷你 2 局：键/窗/直方计数/对手席/空槽/自家单排除（共享键 n_episodes=2）。"""
    # 两局同指纹 m500_w9000（opp_money=500, wheat=9000），事件共享键。
    _write(tmp_path, "episode-1-replay.json", _mk_replay(
        ["renyxin", "oppA"], 500, 9000,
        opp_sells={10: [("WHEAT", 5)], 50: [("WHEAT", 3)]},
        own_sells={10: [("MELON", 99)]},  # 自家单应被排除
        shops={10: ["BAKERY"], 50: ["BAKERY", "YARN_STORE"]},
    ))
    _write(tmp_path, "episode-2-replay.json", _mk_replay(
        ["oppB", "renyxin"], 500, 9000,  # renyxin 在席 1：考察能反向定对手席
        opp_sells={10: [("WHEAT", 2)], 60: [("CARROT", 4)]},
        shops={10: ["BAKERY"], 60: ["BAKERY", "YARN_STORE"]},
    ))
    _pad(tmp_path, 28)  # 垫语料满足 ≥30 局门（无卖单→不入键/直方）
    res = build_sellflow_library(str(tmp_path))
    lib, audit = res["library"], res["build_audit"]

    assert lib["version"] == "sellflow/2.0"
    keys = lib["keys"]
    assert set(keys) == {"OPEN1:BAKERY||m500_w9000", "BAKERY|YARN_STORE||m500_w9000"}

    k0 = keys["OPEN1:BAKERY||m500_w9000"]
    assert k0["n_episodes"] == 2
    assert k0["hist"] == {"0": {"WHEAT": {"qty_sum": 7, "count": 2, "qty_max": 5}}}

    k1 = keys["BAKERY|YARN_STORE||m500_w9000"]
    assert k1["n_episodes"] == 2
    assert k1["hist"] == {
        "1": {
            "WHEAT": {"qty_sum": 3, "count": 1, "qty_max": 3},
            "CARROT": {"qty_sum": 4, "count": 1, "qty_max": 4},
        }
    }

    g = lib["global"]
    assert g["n_episodes"] == 30
    assert g["hist"] == {
        "0": {"WHEAT": {"qty_sum": 7, "count": 2, "qty_max": 5}},
        "1": {
            "WHEAT": {"qty_sum": 3, "count": 1, "qty_max": 3},
            "CARROT": {"qty_sum": 4, "count": 1, "qty_max": 4},
        },
    }

    assert audit["n_files"] == 30
    assert audit["n_used"] == 30
    assert audit["n_skipped"] == 0
    assert audit["total_events"] == 4  # 自家 MELON 单+空槽均不计
    assert audit["n_aux_files"] == 0  # 辅助库默认屏蔽


def test_no_renyxin_seat_skipped(tmp_path):
    """v1②无 renyxin 席跳过计数：其事件不入库。"""
    _write(tmp_path, "episode-g-replay.json", _mk_replay(
        ["renyxin", "oppG"], 500, 9000,
        opp_sells={10: [("WHEAT", 5)]}, shops={10: ["BAKERY"]},
    ))
    _write(tmp_path, "episode-x-replay.json", _mk_replay(
        ["playerX", "playerY"], 999, 1111,  # 指纹 m999_w1111：应整局跳过
        opp_sells={10: [("CARROT", 7)]}, shops={10: ["BAKERY"]},
    ))
    _pad(tmp_path, 28)
    res = build_sellflow_library(str(tmp_path))
    lib, audit = res["library"], res["build_audit"]

    assert audit["n_files"] == 30
    assert audit["n_used"] == 29
    assert audit["n_skipped"] == 1
    assert audit["total_events"] == 1  # 仅 oppG 的 WHEAT
    assert lib["global"]["n_episodes"] == 29
    assert "OPEN1:BAKERY||m500_w9000" in lib["keys"]
    assert not any(k.endswith("m999_w1111") for k in lib["keys"])


def test_bad_file_fail_closed(tmp_path):
    """v1③坏文件 fail-closed 抛：坏 JSON 与结构缺失都抛 ValueError。"""
    # 合法局 + 坏 JSON → fail-closed（不静默跳过坏文件）
    _write(tmp_path, "episode-g-replay.json", _mk_replay(
        ["renyxin", "oppG"], 500, 9000,
        opp_sells={10: [("WHEAT", 5)]}, shops={10: ["BAKERY"]},
    ))
    _pad(tmp_path, 28)
    _write(tmp_path, "episode-bad-replay.json", "{ this is not json")
    with pytest.raises(ValueError):
        build_sellflow_library(str(tmp_path))

    # 结构缺失（无 steps）→ 同样 fail-closed
    d2 = tmp_path / "d2"
    d2.mkdir()
    _pad(d2, 29)
    _write(d2, "episode-s-replay.json", {"info": {"TeamNames": ["renyxin", "x"]}})
    with pytest.raises(ValueError):
        build_sellflow_library(str(d2))


# ---------------- v2 组（top-30 重采/合并/命中字段/真跑） ----------------


def _mk_top30_corpus(tmp_path, with_create_time):
    """55 局：id 1..55，指纹 m(1000+id)_w9000；createTime 随 id 递减（与 id 序反向）。"""
    for i in range(1, 56):
        ct = f"2026-01-01T00:00:{55 - i:02d}" if with_create_time else None
        _write(
            tmp_path,
            f"episode-{i}-replay.json",
            _mk_replay(
                ["renyxin", "oppT"], 1000 + i, 9000,
                opp_sells={10: [("WHEAT", 1)]}, shops={10: ["BAKERY"]},
                n_steps=16, create_time=ct,
            ),
        )


def test_top30_selection_by_create_time(tmp_path):
    """v2①a top-30 截取：55→30 按 createTime 时间序（与 id 序反向→取 id 1..30）。"""
    _mk_top30_corpus(tmp_path, with_create_time=True)
    res = build_sellflow_library(str(tmp_path))
    lib, audit = res["library"], res["build_audit"]

    assert audit["n_files"] == 55 and audit["n_selected"] == 30
    assert audit["n_used"] == 30
    # createTime 递减于 id → 最新 30 局=id 1..30（若误按 id 序会取 26..55）
    expect = {f"OPEN1:BAKERY||m{1000 + i}_w9000" for i in range(1, 31)}
    assert set(lib["keys"]) == expect
    assert audit["total_events"] == 30


def test_top30_fallback_episode_id_order(tmp_path):
    """v2①b 无 createTime 时以 episode id 序代时间序（最新 30=id 26..55）。"""
    _mk_top30_corpus(tmp_path, with_create_time=False)
    res = build_sellflow_library(str(tmp_path))
    lib, audit = res["library"], res["build_audit"]

    assert audit["n_selected"] == 30 and audit["n_used"] == 30
    expect = {f"OPEN1:BAKERY||m{1000 + i}_w9000" for i in range(26, 56)}
    assert set(lib["keys"]) == expect


def test_merge_new_and_aux(tmp_path, monkeypatch):
    """v2②新旧合并：同键计数相加（qty_sum/count 相加、qty_max 取 max）、
    hit 字段以新库为主（新库缺省→合并缺省；辅助键 v1 形照收）。"""
    # 新库 30 局：K1=m500 4 局（4,4,4,9）、K2=m600 2 局（4,4）+24 垫。
    for j, q in enumerate((4, 4, 4, 9)):
        _write(tmp_path, f"episode-n1-{j}-replay.json", _mk_replay(
            ["renyxin", "oppN"], 500, 9000,
            opp_sells={10: [("WHEAT", q)]}, shops={10: ["BAKERY"]}, n_steps=16))
    for j in range(2):
        _write(tmp_path, f"episode-n2-{j}-replay.json", _mk_replay(
            ["renyxin", "oppN"], 600, 9000,
            opp_sells={10: [("WHEAT", 4)]}, shops={10: ["BAKERY"]}, n_steps=16))
    _pad(tmp_path, 24)

    # 辅助库 7 局（v1 口径无 hit 字段）：K1 3 局（2）、K2 3 局（2）、K3 1 局（3）。
    aux = tmp_path / "aux"
    aux.mkdir()
    for j in range(3):
        _write(aux, f"episode-a1-{j}-replay.json", _mk_replay(
            ["renyxin", "oppA"], 500, 9000,
            opp_sells={10: [("WHEAT", 2)]}, shops={10: ["BAKERY"]}, n_steps=16))
    for j in range(3):
        _write(aux, f"episode-a2-{j}-replay.json", _mk_replay(
            ["renyxin", "oppA"], 600, 9000,
            opp_sells={10: [("WHEAT", 2)]}, shops={10: ["BAKERY"]}, n_steps=16))
    _write(aux, "episode-a3-0-replay.json", _mk_replay(
        ["renyxin", "oppA"], 700, 9000,
        opp_sells={10: [("WHEAT", 3)]}, shops={10: ["BAKERY"]}, n_steps=16))

    monkeypatch.setenv("SELLFLOW_AUX_REPLAY_DIR", str(aux))
    res = build_sellflow_library(str(tmp_path))
    lib, audit = res["library"], res["build_audit"]

    k1 = lib["keys"]["OPEN1:BAKERY||m500_w9000"]
    # 同键计数相加：qty_sum 21+6、count 4+3、qty_max max(9,2)；hit 字段=新库值。
    assert k1["n_episodes"] == 7
    assert k1["hist"]["0"]["WHEAT"] == {"qty_sum": 27, "count": 7, "qty_max": 9}
    assert k1["history_hits"] == 3 and k1["hit_rate"] == 0.75

    k2 = lib["keys"]["OPEN1:BAKERY||m600_w9000"]
    assert k2["n_episodes"] == 5
    assert k2["hist"]["0"]["WHEAT"] == {"qty_sum": 14, "count": 5, "qty_max": 4}
    # 新库（2 样本）本就缺省→合并后仍缺省（即便合并样本变多），= hit 字段新库为主。
    assert "history_hits" not in k2 and "hit_rate" not in k2

    # 辅助独有键照收（v1 形）。
    k3 = lib["keys"]["OPEN1:BAKERY||m700_w9000"]
    assert k3["n_episodes"] == 1
    assert k3["hist"] == {"0": {"WHEAT": {"qty_sum": 3, "count": 1, "qty_max": 3}}}
    assert "history_hits" not in k3

    g = lib["global"]
    assert g["n_episodes"] == 37
    assert g["hist"]["0"]["WHEAT"] == {"qty_sum": 44, "count": 13, "qty_max": 9}

    assert audit["n_selected"] == 30 and audit["n_used"] == 30
    assert audit["total_events"] == 6
    assert audit["n_aux_files"] == 7 and audit["n_aux_used"] == 7
    assert audit["n_aux_skipped"] == 0 and audit["n_aux_events"] == 7

    # 与纯新库对拍：hit 字段取值与新库一致（"以新库为主"）。
    monkeypatch.setenv("SELLFLOW_AUX_REPLAY_DIR", "")
    fresh_only = build_sellflow_library(str(tmp_path))["library"]["keys"][
        "OPEN1:BAKERY||m500_w9000"
    ]
    assert fresh_only["history_hits"] == k1["history_hits"]
    assert fresh_only["hit_rate"] == k1["hit_rate"]


def test_history_hits_calculation(tmp_path):
    """v2③hit 字段计算：4 样本 3 命中→history_hits=3、hit_rate=0.75（条目级落位）。"""
    for j, q in enumerate((4, 4, 4, 9)):
        _write(tmp_path, f"episode-h-{j}-replay.json", _mk_replay(
            ["renyxin", "oppH"], 500, 9000,
            opp_sells={10: [("WHEAT", q)]}, shops={10: ["BAKERY"]}, n_steps=16))
    _pad(tmp_path, 26)
    res = build_sellflow_library(str(tmp_path))
    entry = res["library"]["keys"]["OPEN1:BAKERY||m500_w9000"]

    # 窗 0 TOP-1=WHEAT，预期=均单量 21/4=5.25，±50%=[2.625,7.875]：
    # 4→命中 ×3，9→不命中 → hits=3、rate=3/4。字段与 n_episodes/hist 同级。
    assert entry == {
        "n_episodes": 4,
        "hist": {"0": {"WHEAT": {"qty_sum": 21, "count": 4, "qty_max": 9}}},
        "history_hits": 3,
        "hit_rate": 0.75,
    }


def test_history_hits_omitted_small_sample(tmp_path):
    """v2④样本 <3 缺省兼容：条目只留 v1 形（match v2 对缺字段条目按 v1 采纳）。"""
    for j in range(2):
        _write(tmp_path, f"episode-s-{j}-replay.json", _mk_replay(
            ["renyxin", "oppS"], 500, 9000,
            opp_sells={10: [("WHEAT", 4)]}, shops={10: ["BAKERY"]}, n_steps=16))
    _pad(tmp_path, 28)
    res = build_sellflow_library(str(tmp_path))
    entry = res["library"]["keys"]["OPEN1:BAKERY||m500_w9000"]

    # 2 局×1 窗=2 样本对 <3 → 字段缺省。
    assert set(entry) == {"n_episodes", "hist"}
    assert entry["n_episodes"] == 2
    assert entry["hist"] == {"0": {"WHEAT": {"qty_sum": 8, "count": 2, "qty_max": 4}}}


def test_min_corpus_fail_closed(tmp_path):
    """v2⑤语料 <30 局 fail-closed 抛 ValueError。"""
    _pad(tmp_path, 29)
    with pytest.raises(ValueError):
        build_sellflow_library(str(tmp_path))


def test_realrun_build_v2(tmp_path, monkeypatch):
    """v2⑥真跑建库（30 新+86 旧）：键数/hit 覆盖/库 sha 记 evidence；可复算断言。"""
    if not os.path.isdir(REAL_FRESH_DIR) or not os.path.isdir(REAL_AUX_DIR):
        pytest.skip(f"real corpus 不存在: {REAL_FRESH_DIR} / {REAL_AUX_DIR}")
    monkeypatch.setenv("SELLFLOW_AUX_REPLAY_DIR", REAL_AUX_DIR)

    res = build_sellflow_library(REAL_FRESH_DIR)
    lib, audit = res["library"], res["build_audit"]

    # 可复算 1：库 sha 可由 library 重算复现
    assert _sha_of(lib) == audit["sha256_of_library"]
    # 可复算 2：库 JSON 往返（可内嵌）后 sha 不变
    assert _sha_of(json.loads(json.dumps(lib))) == audit["sha256_of_library"]
    # 可复算 3：global 直方 count 总和 == 新鲜+辅助事件数
    gcount = sum(b["count"] for win in lib["global"]["hist"].values() for b in win.values())
    assert gcount == audit["total_events"] + audit["n_aux_events"]

    assert audit["n_files"] == 55 and audit["n_selected"] == 30
    assert audit["n_used"] == 30 and audit["n_skipped"] == 0
    assert audit["n_aux_files"] == 86 and audit["n_aux_used"] == 86
    assert audit["n_aux_skipped"] == 0
    assert audit["total_events"] > 0 and audit["n_aux_events"] > 0

    n_keys = len(lib["keys"])
    covered = sum(1 for e in lib["keys"].values() if "history_hits" in e)
    assert n_keys > 0 and 0 < covered <= n_keys
    for e in lib["keys"].values():
        if "history_hits" in e:
            assert isinstance(e["history_hits"], int) and e["history_hits"] >= 0
            assert 0.0 <= e["hit_rate"] <= 1.0

    evidence = {
        "replay_dir": REAL_FRESH_DIR,
        "aux_replay_dir": REAL_AUX_DIR,
        "n_files": audit["n_files"],
        "n_selected": audit["n_selected"],
        "n_used": audit["n_used"],
        "n_skipped": audit["n_skipped"],
        "total_events": audit["total_events"],
        "n_aux_files": audit["n_aux_files"],
        "n_aux_used": audit["n_aux_used"],
        "n_aux_skipped": audit["n_aux_skipped"],
        "n_aux_events": audit["n_aux_events"],
        "n_keys": n_keys,
        "hit_covered_keys": covered,
        "hit_coverage": covered / n_keys,
        "sha256_of_library": audit["sha256_of_library"],
    }
    os.makedirs(os.path.dirname(_EVIDENCE), exist_ok=True)
    with open(_EVIDENCE, "w", encoding="utf-8") as fh:
        json.dump(evidence, fh, indent=2, sort_keys=True)

    # 可复算 4：落盘 evidence 重载与实测一致
    with open(_EVIDENCE, "r", encoding="utf-8") as fh:
        assert json.load(fh) == evidence


def test_sellflow_realrun_constants_v2(monkeypatch):
    """真跑证据常量钉死（沿评审 P3b）：30 新+86 旧/键数/hit 覆盖/库 sha 可复算。"""
    ev = json.load(open(_EVIDENCE, encoding="utf-8"))
    assert ev["n_used"] == 30 and ev["n_aux_used"] == 86
    assert ev["total_events"] == 17570 and ev["n_aux_events"] == 29470
    assert ev["n_keys"] == 213 and ev["hit_covered_keys"] == 34
    assert ev["hit_coverage"] == ev["hit_covered_keys"] / ev["n_keys"]

    monkeypatch.setenv("SELLFLOW_AUX_REPLAY_DIR", REAL_AUX_DIR)
    out = build_sellflow_library(REAL_FRESH_DIR)
    blob = json.dumps(out["library"], sort_keys=True,
                     ensure_ascii=False, separators=(",", ":")).encode()
    assert hashlib.sha256(blob).hexdigest() == ev["sha256_of_library"]
