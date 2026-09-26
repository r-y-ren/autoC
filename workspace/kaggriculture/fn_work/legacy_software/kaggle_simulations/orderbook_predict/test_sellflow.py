# -*- coding: utf-8 -*-
"""R21 测试面：sellflow（卖流库构建/键检索形态）。

覆盖：①迷你 2 局建库（键/窗/直方计数/对手席/空槽/自家单排除）②无 renyxin
席跳过计数 ③坏文件 fail-closed 抛 ④真跑 86 局建库（evidence 记录+可复算断言）。
"""
from __future__ import annotations

import hashlib
import json
import os

import pytest

from orderbook_predict.sellflow import build_sellflow_library

REAL_REPLAY_DIR = os.environ.get("SELLFLOW_REPLAY_DIR", "/tmp/r33audit")
_EVIDENCE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "evidence", "sellflow_library_realrun.json"
)


def _mk_replay(
    team_names,
    opp_money,
    opp_wheat,
    opp_sells=None,
    own_sells=None,
    shops=None,
    n_steps=64,
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
    return {"info": {"TeamNames": list(team_names)}, "steps": steps}


def _write(tmp_path, name, obj):
    p = tmp_path / name
    if isinstance(obj, str):
        p.write_text(obj, encoding="utf-8")
    else:
        p.write_text(json.dumps(obj), encoding="utf-8")
    return str(p)


def test_build_sellflow_library_keys_windows_hist(tmp_path):
    """①迷你 2 局：键/窗/直方计数/对手席/空槽/自家单排除（共享键 n_episodes=2）。"""
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
    res = build_sellflow_library(str(tmp_path))
    lib, audit = res["library"], res["build_audit"]

    assert lib["version"] == "sellflow/1.0"
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
    assert g["n_episodes"] == 2
    assert g["hist"] == {
        "0": {"WHEAT": {"qty_sum": 7, "count": 2, "qty_max": 5}},
        "1": {
            "WHEAT": {"qty_sum": 3, "count": 1, "qty_max": 3},
            "CARROT": {"qty_sum": 4, "count": 1, "qty_max": 4},
        },
    }

    assert audit["n_files"] == 2
    assert audit["n_used"] == 2
    assert audit["n_skipped"] == 0
    assert audit["total_events"] == 4  # 自家 MELON 单+空槽均不计


def test_no_renyxin_seat_skipped(tmp_path):
    """②无 renyxin 席跳过计数：其事件不入库。"""
    _write(tmp_path, "episode-g-replay.json", _mk_replay(
        ["renyxin", "oppG"], 500, 9000,
        opp_sells={10: [("WHEAT", 5)]}, shops={10: ["BAKERY"]},
    ))
    _write(tmp_path, "episode-x-replay.json", _mk_replay(
        ["playerX", "playerY"], 999, 1111,  # 指纹 m999_w1111：应整局跳过
        opp_sells={10: [("CARROT", 7)]}, shops={10: ["BAKERY"]},
    ))
    res = build_sellflow_library(str(tmp_path))
    lib, audit = res["library"], res["build_audit"]

    assert audit["n_files"] == 2
    assert audit["n_used"] == 1
    assert audit["n_skipped"] == 1
    assert audit["total_events"] == 1  # 仅 oppG 的 WHEAT
    assert lib["global"]["n_episodes"] == 1
    assert "OPEN1:BAKERY||m500_w9000" in lib["keys"]
    assert not any(k.endswith("m999_w1111") for k in lib["keys"])


def test_bad_file_fail_closed(tmp_path):
    """③坏文件 fail-closed 抛：坏 JSON 与结构缺失都抛 ValueError。"""
    # 合法局 + 坏 JSON → fail-closed（不静默跳过坏文件）
    _write(tmp_path, "episode-g-replay.json", _mk_replay(
        ["renyxin", "oppG"], 500, 9000,
        opp_sells={10: [("WHEAT", 5)]}, shops={10: ["BAKERY"]},
    ))
    _write(tmp_path, "episode-bad-replay.json", "{ this is not json")
    with pytest.raises(ValueError):
        build_sellflow_library(str(tmp_path))

    # 结构缺失（无 steps）→ 同样 fail-closed
    d2 = tmp_path / "d2"
    d2.mkdir()
    _write(d2, "episode-s-replay.json", {"info": {"TeamNames": ["renyxin", "x"]}})
    with pytest.raises(ValueError):
        build_sellflow_library(str(d2))


def _sha_of(lib):
    return hashlib.sha256(
        json.dumps(lib, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def test_realrun_build_86(tmp_path):
    """④真跑 86 局建库：evidence 记 n_used/total_events/键数/库 sha；可复算断言。"""
    if not os.path.isdir(REAL_REPLAY_DIR):
        pytest.skip(f"real replay corpus 不存在: {REAL_REPLAY_DIR}")

    res = build_sellflow_library(REAL_REPLAY_DIR)
    lib, audit = res["library"], res["build_audit"]

    # 可复算 1：库 sha 可由 library 重算复现
    assert _sha_of(lib) == audit["sha256_of_library"]
    # 可复算 2：total_events == 全局直方 count 总和
    gcount = sum(
        b["count"] for win in lib["global"]["hist"].values() for b in win.values()
    )
    assert gcount == audit["total_events"]
    # 可复算 3：库 JSON 往返（可内嵌）后 sha 不变
    assert _sha_of(json.loads(json.dumps(lib))) == audit["sha256_of_library"]

    n_keys = len(lib["keys"])
    assert audit["n_used"] == 86
    assert audit["n_skipped"] == 0
    assert audit["n_used"] + audit["n_skipped"] == audit["n_files"]
    assert audit["total_events"] > 0
    assert n_keys > 0

    evidence = {
        "replay_dir": REAL_REPLAY_DIR,
        "n_files": audit["n_files"],
        "n_used": audit["n_used"],
        "n_skipped": audit["n_skipped"],
        "total_events": audit["total_events"],
        "n_keys": n_keys,
        "sha256_of_library": audit["sha256_of_library"],
    }
    os.makedirs(os.path.dirname(_EVIDENCE), exist_ok=True)
    with open(_EVIDENCE, "w", encoding="utf-8") as fh:
        json.dump(evidence, fh, indent=2, sort_keys=True)

    # 可复算 4：落盘 evidence 重载与实测一致
    with open(_EVIDENCE, "r", encoding="utf-8") as fh:
        assert json.load(fh) == evidence


def test_sellflow_realrun_constants():
    """真跑证据常量钉死（评审 P3b）：86 局/29,470 事件/158 键/库 sha 可复算。"""
    import json as _json, hashlib as _hl
    ev = _json.load(open(os.path.join(os.path.dirname(__file__), "evidence",
                                "sellflow_library_realrun.json"), encoding="utf-8"))
    assert ev["n_used"] == 86 and ev["total_events"] == 29470
    assert ev["n_keys"] == 158
    from orderbook_predict import sellflow as _sf
    out = _sf.build_sellflow_library("/tmp/r33audit")
    blob = _json.dumps(out["library"], sort_keys=True,
                       ensure_ascii=False, separators=(",", ":")).encode()
    assert _hl.sha256(blob).hexdigest() == ev["sha256_of_library"]
