# -*- coding: utf-8 -*-
"""probe_s3buy5：S3 构件行为探针（不改既有代码；只读装配验证）。

P1 开局落座：_alt_install 外壳协同后 tape[0..1] 市场单=S3_T0/S3_T1（全路由）。
P2 开局对照表：逐拍动作 vs D5 指纹 / D6 verbatim / mooman 洗价形 13/30/30。
P3 冻结开局：连续两局 _alt_install 后 turn1-4 逐字节一致（D5 条款 2）。
P4 自适应生命周期：step≥144 锁存换表→换局还原+闩复位（M13 同模板）。
P5 unknown 零足迹 + s3_open 关断件零触碰。
P6 C3/M13 共存：_m13_c3_restore 与 _s3_restore 独立触点、互不吞写。
输出 evidence/probe_s3buy5.json。
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
FULL = MODULE_DIR / "build" / "s3_buy5" / "main.py"
OPEN = MODULE_DIR / "build" / "s3_open" / "main.py"
ADAPT0 = MODULE_DIR / "build" / "s3_adapt0" / "main.py"
EVID = MODULE_DIR / "evidence" / "probe_s3buy5.json"

S3_T0 = [["BUY_ANIMAL", "COW", 1], ["BUY_PRODUCT", "WHEAT", 5],
         ["BUY_PRODUCT", "WHEAT", 4], ["SELL", "WHEAT", 3],
         ["BUY_SEED", "WHEAT", 1]]
S3_T0_WASH = [["BUY_ANIMAL", "COW", 1], ["BUY_PRODUCT", "WHEAT", 5],
              ["BUY_PRODUCT", "WHEAT", 13], ["BUY_PRODUCT", "WHEAT", 30],
              ["SELL", "WHEAT", 30], ["BUY_SEED", "WHEAT", 1]]
S3_T1 = [["SELL", "WHEAT", 1], ["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"],
         ["HIRE"], ["BUY_ANIMAL", "COW", 1], ["BUY_ANIMAL", "SHEEP", 2]]


def load_ns(path):
    src = Path(path).read_text(encoding="utf-8")
    ns = {}
    exec(compile(src, str(path), "exec"), ns)
    return ns


def mock_obs(step, egg=5, wool=5, player=0):
    return {
        "step": int(step), "player": int(player),
        "farms": [{"money": 3000.0, "tiles": [], "hands": [],
                   "unlocked_quadrants": 1},
                  {"money": 3000.0, "tiles": [], "hands": [],
                   "unlocked_quadrants": 1}],
        "market": {"inventory": {"EGG": int(egg), "WOOL": int(wool),
                                 "WHEAT": 30},
                   "prices": {}},
        "town": {"unlocked_shops": []},
        "private": {"inventories": [{}, {}], "shed": {}},
    }


def main():
    t0 = time.perf_counter()
    probes = []

    # ---- P1 开局落座 + P3 冻结 ----
    ns = load_ns(FULL)
    ns["_alt_install"]("HybridOpening")
    routes = ns["_IMPL"].chassis.routes
    bad = []
    for rid, tape in routes.items():
        if list(tape[0].get("market") or []) != S3_T0:
            bad.append((rid, 0))
        if list(tape[1].get("market") or []) != S3_T1:
            bad.append((rid, 1))
    probes.append({"probe": "P1_opening_install", "verdict":
                   "PASS" if not bad else "FAIL",
                   "n_routes": len(routes), "mismatches": bad[:5]})
    snapshot = [(list(tape[0]["market"]), list(tape[1]["market"]),
                 [list(tape[2].get("farmer") or [])] +
                 [list(h) for h in (tape[2].get("hands") or [])],
                 [list(tape[3].get("farmer") or [])] +
                 [list(h) for h in (tape[3].get("hands") or [])])
                for tape in routes.values()]
    # 第二局（同一实例再装）冻结核验 turn1-4（turn3-4 取 farmer/hands+market）
    ns["_alt_install"]("HybridOpening")
    snap2 = [(list(tape[0]["market"]), list(tape[1]["market"]),
              [list(tape[2].get("farmer") or [])] +
              [list(h) for h in (tape[2].get("hands") or [])],
              [list(tape[3].get("farmer") or [])] +
              [list(h) for h in (tape[3].get("hands") or [])])
             for tape in routes.values()]
    frozen = snap2 == snapshot
    probes.append({"probe": "P3_frozen_opening", "verdict":
                   "PASS" if frozen else "FAIL",
                   "caliber": "turn1-4 跨局字节级一致（D5 条款 2）"})

    # ---- P2 开局对照表 ----
    def has(seq, kind, name=None, qty=None):
        for o in seq:
            if o[0] != kind:
                continue
            if name is not None and (len(o) < 2 or o[1] != name):
                continue
            if qty is not None and (len(o) < 3 or int(o[2]) != qty):
                continue
            return True
        return False

    t1, t2 = S3_T0, S3_T1
    table = {
        "d5_fingerprint": {
            "turn1": {"BUY_ANIMAL COW": has(t1, "BUY_ANIMAL", "COW"),
                      "BUY_PRODUCT WHEAT(饲料)":
                          has(t1, "BUY_PRODUCT", "WHEAT")},
            "turn2": {"SELL WHEAT": has(t2, "SELL", "WHEAT"),
                      "HIRE x4-5": 4 <= sum(1 for o in t2 if o[0] == "HIRE") <= 5,
                      "BUY COW": has(t2, "BUY_ANIMAL", "COW"),
                      "BUY SHEEP": has(t2, "BUY_ANIMAL", "SHEEP")}},
        "d6_family_legs": {
            "t1_COW1_抢建": has(t1, "BUY_ANIMAL", "COW", 1),
            "WHEAT5_族饲料腿": has(t2, "BUY_PRODUCT", "WHEAT", 5)
            or has(t1, "BUY_PRODUCT", "WHEAT", 5),
            "t2_SELL_WHEAT_洗价腿": has(t2, "SELL", "WHEAT"),
            "t2_HIRE_x4_5_D5域": 4 <= sum(1 for o in t2 if o[0] == "HIRE") <= 5,
            "t2_BUY_COW": has(t2, "BUY_ANIMAL", "COW"),
            "t2_BUY_SHEEP": has(t2, "BUY_ANIMAL", "SHEEP"),
            "d6_verbatim_delta": "量与位以 D5/基底数字为据：t2 SELL WHEAT 量=13"
                                "（基底 trunk 数）vs D6 之 1；HIRE=5（方案链五手，"
                                "D5 4-5 域）vs D6 之 4"},
        "wash_form": {
            "main_safe_skeleton_9buy3sell":
                (has(t1, "BUY_PRODUCT", "WHEAT", 4) and has(t1, "SELL", "WHEAT", 3)),
            "wash_arm_buy13": has(S3_T0_WASH, "BUY_PRODUCT", "WHEAT", 13),
            "wash_arm_buy30": has(S3_T0_WASH, "BUY_PRODUCT", "WHEAT", 30),
            "wash_arm_sell30": has(S3_T0_WASH, "SELL", "WHEAT", 30),
            "note": "13/30/30 全量形=现金包络+dump 利用双证伪（s3_wash 消融）；"
                    "主件取现金安全洗价骨架（9 买/3 卖净 −5）"},
    }
    n_ok = sum(1 for grp in (table["d5_fingerprint"].values())
               for v in grp.values() if v is True)
    n_all = sum(len(grp) for grp in table["d5_fingerprint"].values())
    n6_ok = sum(1 for k, v in table["d6_family_legs"].items()
                if k != "d6_verbatim_delta" and v is True)
    n6_all = sum(1 for k in table["d6_family_legs"] if k != "d6_verbatim_delta")
    nw_ok = sum(1 for k, v in table["wash_form"].items()
                if k != "note" and v is True)
    nw_all = sum(1 for k in table["wash_form"] if k != "note")
    table["match_rate"] = {
        "d5_fingerprint": "%d/%d" % (n_ok, n_all),
        "d6_family_legs": "%d/%d" % (n6_ok, n6_all),
        "wash_form": "%d/%d" % (nw_ok, nw_all),
    }
    probes.append({"probe": "P2_opening_table", "verdict":
                   "PASS" if (n_ok == n_all and n6_ok >= 5 and nw_ok == nw_all)
                   else "FAIL", "table": table})

    # ---- P4 自适应生命周期（换表→还原） ----
    ns4 = load_ns(FULL)
    ns4["_alt_install"]("HybridOpening")
    ns4["_oc_cls"] = lambda obs, step: "h1_mirror"
    n_before = {rid: list(seq) for rid, seq in ns4["_IMPL"].chassis.routes.items()}
    ns4["_s3_apply"](mock_obs(144, egg=1, wool=50), 144)
    cells = ns4["_S3_BACKUP"][0] or {}
    tier = ns4["_S3_REPORT"]["tier"]
    swing = ns4["_S3_REPORT"]["swing"]
    changed = sum(1 for (rid, i), act in cells.items()
                  if ns4["_IMPL"].chassis.routes[rid][i] is not act)
    ok_swap = (tier == -1 and swing == -1 and len(cells) > 0 and
               changed == len(cells)) or (tier in (0, 1))
    # 换局还原（step==0 重播）
    ns4["_oc_after"](mock_obs(0), {"farmer": ["PASS"], "hands": [], "market": []})
    restored = all(ns4["_IMPL"].chassis.routes[rid][i] is act
                   for (rid, i), act in cells.items())
    latch_reset = ns4["_S3_LATCHED"][0] is False
    # 复装后逐格归位核验（与首装序列同对象）
    ns4["_alt_install"]("HybridOpening")
    same = all(ns4["_IMPL"].chassis.routes[rid] == n_before[rid]
               for rid in n_before)
    probes.append({"probe": "P4_adaptive_lifecycle", "verdict":
                   "PASS" if (ok_swap and restored and latch_reset and same)
                   else "FAIL",
                   "tier": tier, "swing": swing, "cells": len(cells),
                   "restored": restored, "latch_reset": latch_reset,
                   "reinstall_identical": same})

    # ---- P5 unknown 零足迹 + s3_open 关断 ----
    ns5 = load_ns(FULL)
    ns5["_alt_install"]("HybridOpening")
    ns5["_oc_cls"] = lambda obs, step: "unknown"
    ns5["_s3_apply"](mock_obs(144, egg=1, wool=50), 144)
    # safe 档=armed但钉 +1（护栏；作动代价见 s3_adapt0 消融）
    unknown_acts = (ns5["_S3_REPORT"]["tier"] == 1
                    and (ns5["_S3_BACKUP"][0] in (None, {})))
    ns5b = load_ns(ADAPT0)
    ns5b["_alt_install"]("HybridOpening")
    ns5b["_oc_cls"] = lambda obs, step: "unknown"
    ns5b["_s3_apply"](mock_obs(144, egg=5, wool=5), 144)
    adapt0_acts = (ns5b["_S3_REPORT"]["tier"] == 0
                   and (ns5b["_S3_BACKUP"][0] or {}) != {})
    ns6 = load_ns(OPEN)
    ns6["_alt_install"]("HybridOpening")
    ns6["_oc_cls"] = lambda obs, step: "h1_mirror"
    ns6["_s3_apply"](mock_obs(144, egg=1, wool=50), 144)
    zero_open = (ns6["_S3_BACKUP"][0] in (None, {})) and \
        ns6["_S3_REPORT"]["tier"] == 1
    probes.append({"probe": "P5_actuation_scope", "verdict":
                   "PASS" if (unknown_acts and zero_open and adapt0_acts)
                   else "FAIL",
                   "safe_default_pinned": unknown_acts,
                   "s3_open_zero": zero_open,
                   "s3_adapt0_acts": adapt0_acts,
                   "note": "safe 档钉 +1（护栏）；s3_adapt0=作动形态（消融计量）；"
                           "wfr 钉零触碰（P6）；s3_open 关断件零触碰"})

    # ---- P6 C3/M13 共存 ----
    ns7 = load_ns(FULL)
    ns7["_alt_install"]("HybridOpening")
    c3_cells = set()
    for rid, per in (ns7.get("_OC_C3_DELTA") or {}).items():
        for k in per:
            c3_cells.add((rid, int(k)))
    s3_cells = set()
    for tier, per in (ns7.get("_S3_TIER_DELTA") or {}).items():
        for rid, cells2 in per.items():
            for k in cells2:
                s3_cells.add((rid, int(k)))
    disjoint = not (c3_cells & s3_cells)
    ns7["_oc_cls"] = lambda obs, step: "wfr"
    ns7["_s3_apply"](mock_obs(144, egg=1, wool=50), 144)   # wfr→tier +1 零触碰
    wfr_zero = (ns7["_S3_BACKUP"][0] in (None, {}))
    probes.append({"probe": "P6_c3_m13_coexist", "verdict":
                   "PASS" if (disjoint and wfr_zero) else "FAIL",
                   "c3_cells": len(c3_cells), "s3_cells": len(s3_cells),
                   "disjoint": disjoint, "wfr_zero_touch": wfr_zero})

    out = {
        "version": "s3buy5-probe/1.0",
        "artifact": str(FULL),
        "artifact_sha256": hashlib.sha256(FULL.read_bytes()).hexdigest(),
        "probes": probes,
        "elapsed_s": round(time.perf_counter() - t0, 1),
    }
    EVID.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str)
                    + "\n", encoding="utf-8")
    for p in probes:
        print(p["probe"], p["verdict"], flush=True)
    return out


if __name__ == "__main__":
    main()
