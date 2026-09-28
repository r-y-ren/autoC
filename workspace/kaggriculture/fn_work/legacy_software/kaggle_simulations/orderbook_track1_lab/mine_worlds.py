# -*- coding: utf-8 -*-
"""mine_worlds（track1 A 前置）：店对（world）定向 seed 挖掘——gengame 磁带重放。

背景：world（town.unlocked_shops 前二店）非 seed 纯函数（weeds RNG 逐空格抽），
idle 驱动 0/32 不可预测（实测）。但 H1/对手磁带在 step<144 的动作流一旦录制，
`kaggsim.Serve.gengame` 可按 (seed, 双方磁带) 极速重放并给出该动作流下的实现
world——用于**定向选 seed**（挖目标格），最终格归属仍以实跑 trace 为准（账本
逐单元记实际 face/pair，预测错配不入目标格）。

件：
- record_pair(opp_path, rec_seed)：kaggsim run_match(record=True) 录 H1 vs 对手
  双席动作磁带（+换席序一份）；
- predict_world(seed, lines0, lines1)：gengame→world_key（首二店，排序归一）；
- validate_on_k2()：对 K2 实测 32 seeds（ab_k2_ledger_realrun.json 已知格）
  验证预测命中率（录制 seed 不同于被预测 seed 防自证）；
- mine_target_cells(...)：扫描 seed 域→{cell: [seeds]} 候选。

只写 orderbook_track1_lab/。不改既有代码。
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
_KAGGSIM_PY = (KSIM_DIR.parents[1] / "tools" / "sim_bridge" / "src"
               / "src-python")
if str(_KAGGSIM_PY) not in sys.path:
    sys.path.insert(0, str(_KAGGSIM_PY))

from kaggsim.serve import Serve, run_match  # noqa: E402
from kaggsim.tape import action_to_line  # noqa: E402

H1_MAIN = (KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py")
OPPONENTS = (
    "orderbook_r37/build/main.py",
    "orderbook_2965_adopt/a/main.py",
    "orderbook_2965_adopt/b/main.py",
    "v48_derivative/main.py",
)
K2_LEDGER = (KSIM_DIR / "orderbook_iterk_lab" / "evidence"
             / "ab_k2_ledger_realrun.json")
REC_SEED_BASE = 960001          # 录制 seed 域（K2 556k/中性 672k/挖掘 780k 均不撞）
MINE_SEED_BASE = 780000         # 挖掘 seed 域
TARGET_CELLS = (
    "ICE_CREAM_SHOP+YARN_STORE",        # 优先格（K2 唯一正格线索）
    "ICE_CREAM_SHOP+ICE_CREAM_SHOP",
    "ICE_CREAM_SHOP+PET_CAFE",
    "ICE_CREAM_SHOP+PIZZA_SHOP",
    "ICE_CREAM_SHOP+SMOOTHIE_SHOP",
    "BAKERY+ICE_CREAM_SHOP",
    "BRUNCH_SPOT+ICE_CREAM_SHOP",
    "FARMERS_MARKET+ICE_CREAM_SHOP",
    "BAKERY+YARN_STORE",
    "BRUNCH_SPOT+YARN_STORE",
    "FARMERS_MARKET+YARN_STORE",
    "PET_CAFE+YARN_STORE",
    "PIZZA_SHOP+YARN_STORE",
    "SMOOTHIE_SHOP+YARN_STORE",
    "YARN_STORE+YARN_STORE",
)


def _load(path: str):
    from kaggsim.serve import load_agent
    return load_agent(path)


def _lines_from_trace(trace):
    """run_match trace→双席动作行（逐步，[lines_seat0, lines_seat1]）。"""
    a0, a1 = [], []
    for st in trace:
        acts = st.get("actions") or [None, None]
        a0.append(action_to_line(acts[0]) if acts[0] else "PASS")
        a1.append(action_to_line(acts[1]) if acts[1] else "PASS")
    return [a0, a1]


def record_pair(opp_rel: str, rec_seed: int, srv: Serve = None) -> dict:
    """录制 H1 vs 对手双席磁带（两个席位序各一份）。→ {tapes, banks, elapsed}。"""
    own = srv is None
    srv = srv or Serve()
    try:
        h1 = _load(str(H1_MAIN))
        opp = _load(str(KSIM_DIR / opp_rel))
        out = {}
        t0 = time.perf_counter()
        banks0, tr0 = run_match(h1, opp, int(rec_seed), srv, record=True)
        out["order_h1_first"] = {
            "lines": _lines_from_trace(tr0), "banks": list(banks0),
            "world": tr0[-1]["state"]["town"]["unlocked_shops"][:2]
            if tr0 else None}
        banks1, tr1 = run_match(opp, h1, int(rec_seed), srv, record=True)
        out["order_h1_second"] = {
            "lines": _lines_from_trace(tr1), "banks": list(banks1),
            "world": tr1[-1]["state"]["town"]["unlocked_shops"][:2]
            if tr1 else None}
        return {"tapes": out, "opp": opp_rel, "rec_seed": int(rec_seed),
                "elapsed_s": round(time.perf_counter() - t0, 2)}
    finally:
        if own:
            srv.close()


def predict_world(seed: int, lines0, lines1, srv: Serve, k: int = 2):
    """gengame 磁带重放→世界键（有序 '|' 连接；调用方自行排序归一）。"""
    js = srv.gengame(int(seed), lines0, lines1)
    shops = list((js.get("final") or {}).get("town", {}).get(
        "unlocked_shops") or [])
    return "|".join(str(s) for s in shops[:k]) if len(shops) >= k else None


def pair_key(world_key) -> str:
    """世界键→账本店对键（[:2] 排序 '+' 连接；与 ab_r41._pair_key 同口径）。"""
    if not world_key:
        return None
    return "+".join(sorted(str(s) for s in world_key.split("|")[:2]))


def k2_actual_pairs() -> dict:
    """K2 账本已知 (seed→pair)（实跑 trace 口径）。"""
    data = json.loads(K2_LEDGER.read_text(encoding="utf-8"))
    out = {}
    for u in data.get("units") or []:
        if u.get("seed") is not None and u.get("pair"):
            out[int(u["seed"])] = str(u["pair"])
    return out


def validate_on_k2(recordings: dict, srv: Serve = None) -> dict:
    """K2 32 seeds 预测命中率（录制 seed 均域外，无自证）。"""
    own = srv is None
    srv = srv or Serve()
    try:
        actual = k2_actual_pairs()
        rows = []
        for j, opp in enumerate(OPPONENTS):
            rec = recordings.get(opp)
            if rec is None:
                continue
            blk = [556000 + j * 1000 + i for i in range(8)]
            for s in blk:
                if s not in actual:
                    continue
                got = {}
                for order, tag in (("order_h1_first", "h1_seat0"),
                                   ("order_h1_second", "h1_seat1")):
                    lines = rec["tapes"][order]["lines"]
                    wk = predict_world(s, lines[0], lines[1], srv)
                    got[tag] = pair_key(wk)
                ok0 = got["h1_seat0"] == actual[s]
                ok1 = got["h1_seat1"] == actual[s]
                rows.append({"seed": s, "opponent": opp,
                             "actual": actual[s],
                             "pred_h1_seat0": got["h1_seat0"],
                             "pred_h1_seat1": got["h1_seat1"],
                             "match_seat0": ok0, "match_seat1": ok1,
                             "match_any": bool(ok0 or ok1),
                             "match_both": bool(ok0 and ok1)})
        n = len(rows)
        return {
            "n_seeds": n,
            "match_seat0": sum(r["match_seat0"] for r in rows),
            "match_seat1": sum(r["match_seat1"] for r in rows),
            "match_any": sum(r["match_any"] for r in rows),
            "match_both": sum(r["match_both"] for r in rows),
            "rows": rows,
        }
    finally:
        if own:
            srv.close()


def mine_target_cells(recordings: dict, seed_base: int = MINE_SEED_BASE,
                      n_seeds: int = 2000, k: int = 2, srv: Serve = None,
                      want: int = 10) -> dict:
    """扫 seed 域，为每个对手×目标格收集候选 seed（每 order 均预测为目标格）。"""
    own = srv is None
    srv = srv or Serve()
    try:
        found = {c: [] for c in TARGET_CELLS}
        n_pred = 0
        t0 = time.perf_counter()
        for opp in OPPONENTS:
            rec = recordings.get(opp)
            if rec is None:
                continue
            l0 = rec["tapes"]["order_h1_first"]["lines"]
            l1 = rec["tapes"]["order_h1_second"]["lines"]
            for i in range(int(n_seeds)):
                s = int(seed_base) + i
                w0 = predict_world(s, l0[0], l0[1], srv, k)
                w1 = predict_world(s, l1[0], l1[1], srv, k)
                n_pred += 2
                p0, p1 = pair_key(w0), pair_key(w1)
                if p0 is None or p0 != p1:
                    continue
                if p0 in found and len(found[p0]) < want:
                    found[p0].append({"seed": s, "opponent": opp})
        summary = {c: len(v) for c, v in found.items()}
        return {"found": found, "summary": summary,
                "n_predictions": n_pred,
                "elapsed_s": round(time.perf_counter() - t0, 2),
                "seed_base": int(seed_base), "n_seeds_scanned": int(n_seeds)}
    finally:
        if own:
            srv.close()


def main():
    srv = Serve()
    try:
        recordings = {}
        for j, opp in enumerate(OPPONENTS):
            rec = record_pair(opp, REC_SEED_BASE + j, srv)
            recordings[opp] = rec
            print("recorded", opp, rec["elapsed_s"], "s", flush=True)
        val = validate_on_k2(recordings, srv)
        print("VALIDATE:", {k: v for k, v in val.items() if k != "rows"},
              flush=True)
        for r in val["rows"]:
            print("  ", r["seed"], r["opponent"].split("/")[-2],
                  "actual=", r["actual"], "p0=", r["pred_h1_seat0"],
                  "p1=", r["pred_h1_seat1"],
                  "OK" if r["match_any"] else "MISS", flush=True)
        out = {"recordings": {
            opp: {"rec_seed": r["rec_seed"], "elapsed_s": r["elapsed_s"],
                  "banks": {o: v["banks"] for o, v in r["tapes"].items()},
                  "world_rec_seed": {o: v["world"]
                                     for o, v in r["tapes"].items()}}
            for opp, r in recordings.items()}, "validation": val}
        (MODULE_DIR / "evidence" / "mine_validate.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8")
        return out
    finally:
        srv.close()


if __name__ == "__main__":
    main()
