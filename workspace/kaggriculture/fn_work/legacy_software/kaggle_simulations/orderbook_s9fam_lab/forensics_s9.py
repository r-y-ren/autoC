# -*- coding: utf-8 -*-
"""forensics_s9（s9 同族提胜精修 lab）：两大伤面法证（只跑法证局，不改既有代码）。

伤面①：S8 翻负 4 局（V89×2/tetsutani×2，语料=674000+i*159 块）——尖拍追加单的
  落位/量/时点 vs 对手同拍单：输在槽位？量？还是追加反而喂了对手价格？
伤面②：H 族 1k-5k 大败 4 局（crown 语料 H1 674710/674781/674355/674141 系）——
  大败的钱差结构（何时崩、崩在什么品），与微败（H1 675410 对照）截然不同的败法。

跑口：jsf._Tracer 双席逐拍 + 影子引擎逐单（column 槽位/first_price/slippage）+
_s8_apply 间谍（宿主动作 vs 尖拍层输出之 diff→追加单识别）。
证据 orderbook_s9fam_lab/evidence/forensics_raw.json；预算计入 s9 判决账本。
只写 orderbook_s9fam_lab/；不改既有代码；不提交；不发射。
"""
from __future__ import annotations

import copy
import json
import multiprocessing
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
REPO = KSIM_DIR.parents[2]
for p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_goose_lab"),
          str(KSIM_DIR / "orderbook_s1form_lab"), str(KSIM_DIR / "orderbook_r40")):
    if p not in sys.path:
        sys.path.insert(0, p)

import judge_s_form as jsf  # noqa: E402  只读复用

EVID_DIR = HERE / "evidence"
RAW_PATH = EVID_DIR / "forensics_raw.json"

S8 = KSIM_DIR / "orderbook_s8spike_lab" / "build" / "s8" / "main.py"
APPEND = KSIM_DIR / "orderbook_s1form_lab" / "build" / "s_append" / "main.py"
H1 = KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"
V89 = KSIM_DIR / "orderbook_v89_lab" / "build" / "v89_pure" / "main.py"
TETSU = KSIM_DIR / "orderbook_racegap_lab" / "opponents" / "tetsu1009" \
    / "main.py"

# 伤面①：S8 翻负 4 局（2 键×双席）
FLIP_KEYS = [(674477, "V89", V89), (677180, "tetsutani", TETSU)]
# 伤面②：H 族 1k-5k 大败 4 局（crown H1 语料）
HBIG_KEYS = [(674710, "H1", H1), (674781, "H1", H1),
             (674355, "H1", H1), (674141, "H1", H1)]
# 微败对照（与大败结构对比）
HMICRO_KEYS = [(675410, "H1", H1)]
ARMS = [("s8", S8), ("s_append", APPEND)]
WORKERS = 2

RUN_ROWS = []      # 全量局行（判决件复用：margin 面）


# ============================================================ 影子逐单 ==
def shadow_ticks(sinks, seed):
    """影子引擎逐拍逐单归因（jsf.shadow_books 同源口径，保留 per-step 记录）。"""
    try:
        base = str(KSIM_DIR.parent)
        if base not in sys.path:
            sys.path.insert(0, base)
        from kgenv import replay_profile as rp  # noqa: WPS433
    except Exception as exc:
        return {"error": repr(exc)[:120]}
    m = {0: {}, 1: {}}
    for seat in (0, 1):
        for entry in (sinks.get(seat) or []):
            m[seat][int(entry[0])] = (entry[1], entry[2])
    steps = sorted(set(m[0]) | set(m[1]))
    if not steps:
        return {"error": "empty_traces"}
    first = steps[0]
    pre0 = m[0].get(first, (None, None))[0] or m[1].get(first, (None, None))[0]
    pre1 = m[1].get(first, (None, None))[0] or pre0
    try:
        state = rp._s_snapshot(pre0, [pre0.get("private"), pre1.get("private")])
    except Exception as exc:
        return {"error": "snapshot: %r" % exc}
    ticks = {}
    mism = 0
    for s in steps:
        acts = [m[0].get(s, (None, None))[1], m[1].get(s, (None, None))[1]]
        acts = [a if isinstance(a, dict) else
                {"farmer": ["PASS"], "hands": [], "market": []} for a in acts]
        try:
            post, attr = rp._s_step(state, acts, s, jsf._SHADOW_CFG, int(seed))
        except Exception:
            mism += 1
            continue
        row = {0: [], 1: []}
        for pl in (0, 1):
            try:
                orders = attr["market"][pl]["orders"]
            except Exception:
                orders = []
            for o in orders:
                row[pl].append({
                    "col": o.get("column"), "type": o.get("type"),
                    "item": o.get("item"), "req": o.get("requested"),
                    "filled": o.get("filled"), "value": round(float(
                        o.get("value") or 0), 1),
                    "px0": o.get("first_price"), "abort": o.get("abort")})
        ticks[s] = row
        nxt = s + 1
        n0 = m[0].get(nxt, (None, None))[0]
        n1 = m[1].get(nxt, (None, None))[0]
        if n0 and n1:
            try:
                diff = rp._s_compare(post, n0,
                                     [n0.get("private"), n1.get("private")])
            except Exception:
                diff = ["compare_error"]
            if diff:
                mism += 1
                try:
                    state = rp._s_snapshot(n0,
                                           [n0.get("private"),
                                            n1.get("private")])
                except Exception:
                    state = post
            else:
                state = post
        else:
            state = post
    return {"ticks": ticks, "shadow_mismatch_steps": mism}


# ============================================================ 跑口 ==
def _load_spy(arm_path):
    """装载 arm 并对 _s8_apply 上间谍（记录宿主动作 vs 尖拍层输出）。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    entry = j23._load_entry(arm_path)
    g = getattr(entry, "__globals__", None)
    log = []
    if isinstance(g, dict) and "_s8_apply" in g:
        orig = g["_s8_apply"]

        def spy(observation, action):
            hm = None
            try:
                if isinstance(action, dict):
                    hm = copy.deepcopy(action.get("market"))
            except Exception:
                hm = None
            out = orig(observation, action)
            try:
                step = int((observation or {}).get("step", 0))
            except Exception:
                step = -1
            om = None
            try:
                if isinstance(out, dict):
                    om = copy.deepcopy(out.get("market"))
            except Exception:
                om = None
            log.append((step, hm, om))
            return out

        g["_s8_apply"] = spy
    return entry, log


def _diff_market(hm, om):
    """尖拍层 diff：[:len(host)] 前缀（qty 增=③topup），尾部=②追加单。"""
    hm = hm or []
    om = om or []
    topups, appends = [], []
    n = len(hm)
    for i in range(min(n, len(om))):
        if om[i] != hm[i]:
            topups.append({"col": i, "before": hm[i], "after": om[i]})
    for j in range(n, len(om)):
        appends.append({"col": j, "entry": om[j]})
    return topups, appends


def _chunk_forensics(payload):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    out_rows = []
    for spec in payload["specs"]:
        sinks = {0: [], 1: []}
        spy_log = []
        err = None
        try:
            our, spy_log = _load_spy(spec["arm_path"])
            opp = j23._load_entry(spec["opp_path"])
            a_us = jsf._Tracer(our, spec["our_seat"], sinks[spec["our_seat"]])
            a_opp = jsf._Tracer(opp, 1 - spec["our_seat"],
                                sinks[1 - spec["our_seat"]])
            a0, a1 = (a_us, a_opp) if spec["our_seat"] == 0 else (a_opp, a_us)
            games = [{"seed": int(spec["seed"]), "agents": [a0, a1]}]
        except Exception as exc:
            games = [{"seed": int(spec["seed"]), "agents": []}]
            err = repr(exc)[:120]
        res = sb.run_games(games, dict(payload.get("cfg") or {})) \
            if games and games[0]["agents"] else {"games": []}
        rr = (res.get("games") or [{}])[0]
        row = {"arm": spec["arm"], "seed": int(spec["seed"]),
               "seat": int(spec["our_seat"]), "opp": spec["opponent"],
               "group": spec.get("group"), "banks": rr.get("banks"),
               "error": err or rr.get("error"), "margin_clean": None,
               "tm_us": None, "tm_opp": None, "telemetry": None,
               "day_diff": {}, "top_drops": [], "per_item_rev": {},
               "segments": {}, "append_ticks": [], "race": {},
               "slot": {}, "feed": {}, "spy_summary": {},
               "shadow_mismatch_steps": 0}
        try:
            row["telemetry"] = jsf._snap_telemetry(our)
        except Exception:
            pass
        if row["banks"] is not None and row["error"] is None:
            try:
                e_us = jsf.end_reads(sinks[row["seat"]])
                e_opp = jsf.end_reads(sinks[1 - row["seat"]])
                row["tm_us"] = e_us.get("terminal_money")
                row["tm_opp"] = e_opp.get("terminal_money")
                if row["tm_us"] is not None and row["tm_opp"] is not None:
                    row["margin_clean"] = float(row["tm_us"]) - float(
                        row["tm_opp"])
            except Exception as exc:
                row["econ_error"] = repr(exc)[:100]
            try:
                sh = shadow_ticks(sinks, int(spec["seed"]))
                row["shadow_mismatch_steps"] = sh.get(
                    "shadow_mismatch_steps", 0)
                if not sh.get("error"):
                    _forensic_extract(row, sinks, spy_log, sh, spec)
            except Exception as exc:
                row["forensic_error"] = repr(exc)[:120]
        out_rows.append(row)
    return out_rows


def _forensic_extract(row, sinks, spy_log, sh, spec):
    """逐拍法证抽取：钱差轨迹/崩点/分品/追加单槽位竞速/喂价窗口。"""
    seat, oseat = int(spec["our_seat"]), 1 - int(spec["our_seat"])
    ticks = sh.get("ticks") or {}
    # ---- 钱差轨迹（obs.farms[.].money，按 player 口径归位）----
    money = {}   # step -> {player: money}
    for sk in (0, 1):
        for entry in (sinks.get(sk) or []):
            st = int(entry[0])
            obs = entry[1] or {}
            farms = obs.get("farms")
            if not isinstance(farms, list):
                continue
            try:
                player = int(obs.get("player", sk))
                money.setdefault(st, {})[player] = float(
                    farms[player].get("money"))
            except Exception:
                continue
    steps = sorted(money)
    diffs = {s: round(money[s][seat] - money[s][oseat], 1) for s in steps
             if seat in money[s] and oseat in money[s]}
    # 按日尾拍读钱差 + 日内最大跌幅
    day_end, day_delta, drops = {}, {}, []
    prev_end = 0.0
    for day in range(30):
        ds = [s for s in diffs if s // 24 == day]
        if not ds:
            continue
        end = diffs[max(ds)]
        day_end[str(day)] = end
        day_delta[str(day)] = round(end - prev_end, 1)
        prev_end = end
        for s in ds[1:]:
            drops.append((round(diffs[s] - diffs[s - 1], 1), s))
    drops.sort()
    row["day_diff"] = day_end
    row["day_delta"] = day_delta
    # ---- 崩点（top drops）+ 当拍双方逐单 ----
    for delta, s in drops[:6]:
        if delta >= -1e-9:
            continue
        who = ticks.get(s) or {0: [], 1: []}
        row["top_drops"].append({
            "step": s, "day": s // 24, "ddelta": delta,
            "us_orders": who.get(seat) or [], "opp_orders": who.get(oseat) or []})
    # ---- 分品营收（影子逐单 value，us/opp）+ 分段 ----
    seg = {"d0-6": [0, 6], "d7-13": [7, 13], "d14-20": [14, 20],
           "d21-27": [21, 27], "d28+": [28, 30]}
    per_item = {}
    seg_rev = {k: [0.0, 0.0] for k in seg}
    for s, two in ticks.items():
        for pl, key in ((seat, 0), (oseat, 1)):
            for o in (two.get(pl) or []):
                if o.get("type") != "SELL":
                    continue
                it = str(o.get("item"))
                d = per_item.setdefault(it, [0.0, 0.0])
                d[key] += float(o.get("value") or 0)
                for k, (a, b) in seg.items():
                    if a <= s // 24 < b:
                        seg_rev[k][key] += float(o.get("value") or 0)
    row["per_item_rev"] = {
        it: {"us": round(v[0], 1), "opp": round(v[1], 1),
             "diff": round(v[0] - v[1], 1)}
        for it, v in sorted(per_item.items())}
    row["segments"] = {
        k: {"us": round(v[0], 1), "opp": round(v[1], 1),
            "diff": round(v[0] - v[1], 1)} for k, v in seg_rev.items()}
    # ---- ①追加单逐拍：槽位/量/竞速 ----
    prices = {}
    for entry in (sinks.get(seat) or []):
        obs = entry[1] or {}
        px = ((obs.get("market") or {}) if isinstance(obs.get("market"),
                                                      dict) else {}).get(
            "prices") or {}
        prices[int(entry[0])] = {k: v for k, v in px.items()}
    n_app_ticks = app_col_sum = app_col_n = 0
    race_w = race_l = race_n = 0
    race_px_us = race_px_opp = 0.0
    fill_req = fill_done = 0
    opp_col_sum = opp_col_n = 0
    for step, hm, om in (spy_log or []):
        topups, appends = _diff_market(hm, om)
        if not appends and not topups:
            continue
        if appends:
            n_app_ticks += 1
        two = ticks.get(step) or {0: [], 1: []}
        us_orders = two.get(seat) or []
        op_orders = two.get(oseat) or []
        ev = {"step": step, "day": step // 24,
              "topups": [{"col": t["col"], "before": t["before"],
                          "after": t["after"]} for t in topups],
              "appends": [], "opp_sells": [], "px": {}}
        items = set()
        for a in appends:
            e = a["entry"]
            if not (isinstance(e, (list, tuple)) and len(e) >= 3):
                continue
            it = str(e[1])
            items.add(it)
            rec = {"col": a["col"], "item": it, "qty": e[2]}
            for o in us_orders:
                if o.get("type") == "SELL" and o.get("item") == it \
                        and o.get("col") == a["col"]:
                    rec.update(filled=o.get("filled"), value=o.get("value"),
                               px0=o.get("px0"), abort=o.get("abort"))
                    fill_req += float(o.get("req") or 0)
                    fill_done += float(o.get("filled") or 0)
                    app_col_sum += int(o.get("col") or 0)
                    app_col_n += 1
            ev["appends"].append(rec)
        for o in op_orders:
            if o.get("type") == "SELL" and o.get("item") in items:
                ev["opp_sells"].append(
                    {"col": o.get("col"), "item": o.get("item"),
                     "qty": o.get("req"), "filled": o.get("filled"),
                     "value": o.get("value"), "px0": o.get("px0")})
                opp_col_sum += int(o.get("col") or 0)
                opp_col_n += 1
                if o.get("filled") and o.get("value"):
                    race_n += 1
                    our_v = sum(float(x.get("value") or 0)
                                for x in ev["appends"]
                                if x.get("item") == o.get("item")
                                and x.get("filled"))
                    our_f = sum(float(x.get("filled") or 0)
                                for x in ev["appends"]
                                if x.get("item") == o.get("item"))
                    if our_f:
                        race_px_us += our_v
                        race_px_opp += float(o.get("value") or 0)
                        if (our_v / our_f) >= (float(o.get("value") or 0)
                                               / max(1e-9, float(
                                                   o.get("filled") or 1))):
                            race_w += 1
                        else:
                            race_l += 1
        for it in items:
            ev["px"][it] = prices.get(step, {}).get(it)
            nxt = [prices.get(step + k, {}).get(it) for k in (1, 2, 3, 4)]
            ev["px_next"] = ev.get("px_next", {})
            ev["px_next"][it] = [x for x in nxt if x is not None]
        row["append_ticks"].append(ev)
    row["spy_summary"] = {
        "n_calls": len(spy_log or []), "n_append_ticks": n_app_ticks,
        "n_append_orders": app_col_n, "n_topup_orders": sum(
            1 for e in row["append_ticks"] for t in e["topups"]),
        "fill_req": fill_req, "fill_done": fill_done,
        "fill_rate": round(fill_done / fill_req, 4) if fill_req else None}
    row["slot"] = {
        "append_col_mean": round(app_col_sum / app_col_n, 2)
        if app_col_n else None,
        "opp_col_mean": round(opp_col_sum / opp_col_n, 2) if opp_col_n else None,
        "append_cols": [e.get("col") for t in row["append_ticks"]
                        for e in t["appends"]],
        "opp_cols": [o.get("col") for t in row["append_ticks"]
                     for o in t["opp_sells"]]}
    row["race"] = {"n_same_tick": race_n, "we_better": race_w,
                   "we_worse": race_l,
                   "our_value": round(race_px_us, 1),
                   "opp_value": round(race_px_opp, 1),
                   "our_px": round(race_px_us / max(1e-9, fill_done), 2)
                   if fill_done else None}
    # ---- 喂价窗：追加拍后 24 拍同品对手营收 vs 我方（本臂内）----
    feed = {}
    for ev in row["append_ticks"]:
        s0 = ev["step"]
        for o in (ticks.get(s0) or {}).get(oseat) or []:
            if o.get("type") == "SELL":
                d = feed.setdefault(str(o.get("item")), [0.0, 0.0])
                d[1] += float(o.get("value") or 0)
        for o in (ticks.get(s0) or {}).get(seat) or []:
            if o.get("type") == "SELL":
                d = feed.setdefault(str(o.get("item")), [0.0, 0.0])
                d[0] += float(o.get("value") or 0)
    row["feed"] = {"append_tick_rev_by_item": {
        it: {"us": round(v[0], 1), "opp": round(v[1], 1)}
        for it, v in sorted(feed.items())}}


def play(specs, cfg):
    specs = list(specs)
    n = max(1, min(WORKERS * 2, max(1, len(specs))))
    tasks = [{"specs": specs[i::n], "cfg": dict(cfg or {})} for i in range(n)]
    tasks = [t for t in tasks if t["specs"]]
    if len(tasks) <= 1:
        parts = [_chunk_forensics(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(WORKERS, len(tasks))) as pool:
            parts = pool.map(_chunk_forensics, tasks)
    rows = []
    for part in parts:
        rows.extend(part)
    return rows


def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    specs = []
    for group, keys in (("flip", FLIP_KEYS), ("hbig", HBIG_KEYS),
                        ("hmicro", HMICRO_KEYS)):
        for seed, on, opath in keys:
            for seat in (0, 1):
                for arm, apath in ARMS:
                    specs.append({
                        "game_id": "s9f-%s|%s|%d-s%d-%s" % (
                            group, on, seed, seat, arm),
                        "seed": seed, "arm": arm, "arm_path": str(apath),
                        "our_seat": seat, "opp_path": str(opath),
                        "opponent": on, "group": group, "trace": True})
    auth_cache = KSIM_DIR / "orderbook_s1form_lab" / "evidence" / \
        "sim_auth_cache.json"
    auth = json.loads(auth_cache.read_text(encoding="utf-8")) \
        if auth_cache.is_file() else None
    rows = play(specs, {"engine": "auto", "bridge": auth,
                        "workers": WORKERS})
    RUN_ROWS.extend(rows)

    # ---- 伤面①摘要（翻负 4 局：槽位/量/竞速/喂价）----
    f1 = {"design": "S8 翻负 4 局（674477×V89、677180×tetsutani×双席）逐拍法证："
                    "尖拍追加单落位/量/时点 vs 对手同拍单（s8 vs s_append 同键对照）",
          "games": []}
    for seed, on, _ in FLIP_KEYS:
        for seat in (0, 1):
            g8 = _find(rows, "s8", seed, seat, on)
            gc = _find(rows, "s_append", seed, seat, on)
            f1["games"].append(_flip_digest(g8, gc))
    # ---- 伤面②摘要（H 族大败 4 局钱差结构）----
    f2 = {"design": "H 族 1k-5k 大败 4 局（crown H1 674710/674781/674355/"
                    "674141 系）钱差结构：何时崩、崩在什么品；微败对照 H1 675410",
          "games": []}
    for seed, on, _ in HBIG_KEYS + HMICRO_KEYS:
        for seat in (0, 1):
            g8 = _find(rows, "s8", seed, seat, on)
            gc = _find(rows, "s_append", seed, seat, on)
            f2["games"].append(_hbig_digest(g8, gc))
    out = {
        "version": "s9-family-forensics/1.0",
        "task": "S9 同族提胜精修法证：S8 翻负 4 局 + H 族 1k-5k 大败 4 局",
        "design": {
            "corpus": "flip=674477(V89)/677180(tetsutani)×双席；hbig=H1 "
                      "674710/674781/674355/674141×双席；hmicro=H1 "
                      "675410×双席；臂={s8(a59208fe), s_append(4608e9e0)}",
            "machine": "jsf._Tracer 逐拍 + 影子引擎逐单（column/first_price）"
                       "+ _s8_apply 间谍（宿主 vs 尖拍层 diff）",
            "caliber": "margin=终局 farms[obs.player] 差；钱差轨迹=逐拍 obs "
                       "farms money 差；分品营收=影子 SELL value（us/opp）"},
        "forensics_flip": f1,
        "forensics_hbig": f2,
        "rows": [{k: r.get(k) for k in
                  ("arm", "seed", "seat", "opp", "group", "margin_clean",
                   "tm_us", "tm_opp", "error", "shadow_mismatch_steps")}
                 for r in rows],
        "budget_note": "法证局次计入 s9 判决账本（28 局=14 键×双席×2 臂）",
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "elapsed_s": round(time.perf_counter() - t0, 1),
    }
    RAW_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1,
                                   default=str) + "\n", encoding="utf-8")
    # 完整逐局法证细节（判决件引用）
    (EVID_DIR / "forensics_full_rows.json").write_text(
        json.dumps(RUN_ROWS, ensure_ascii=False, indent=1,
                   default=str) + "\n", encoding="utf-8")
    print("FLIP:", json.dumps(f1["games"], ensure_ascii=False,
                              default=str)[:1500], flush=True)
    print("HBIG:", json.dumps(f2["games"], ensure_ascii=False,
                              default=str)[:1500], flush=True)
    print("DONE %.1fs rows=%d" % (time.perf_counter() - t0, len(rows)),
          flush=True)
    return out


def _find(rows, arm, seed, seat, opp):
    for r in rows:
        if r["arm"] == arm and r["seed"] == seed and r["seat"] == seat \
                and r["opp"] == opp:
            return r
    return None


def _flip_digest(g8, gc):
    g8 = g8 or {}
    gc = gc or {}
    return {
        "seed": g8.get("seed"), "opp": g8.get("opp"), "seat": g8.get("seat"),
        "margin_s8": g8.get("margin_clean"),
        "margin_s_append": gc.get("margin_clean"),
        "delta": round((g8.get("margin_clean") or 0)
                       - (gc.get("margin_clean") or 0), 1)
        if g8.get("margin_clean") is not None
        and gc.get("margin_clean") is not None else None,
        "spy": g8.get("spy_summary"), "slot": g8.get("slot"),
        "race": g8.get("race"),
        "append_ticks": (g8.get("append_ticks") or [])[:12],
        "feed": g8.get("feed"),
        "per_item_rev": g8.get("per_item_rev"),
        "per_item_rev_ctrl": gc.get("per_item_rev"),
        "day_delta_s8": g8.get("day_delta"),
        "day_delta_ctrl": gc.get("day_delta"),
    }


def _hbig_digest(g8, gc):
    g8 = g8 or {}
    gc = gc or {}
    return {
        "seed": g8.get("seed"), "opp": g8.get("opp"), "seat": g8.get("seat"),
        "margin_s8": g8.get("margin_clean"),
        "margin_s_append": gc.get("margin_clean"),
        "day_diff_s8": g8.get("day_diff"),
        "day_delta_s8": g8.get("day_delta"),
        "top_drops": g8.get("top_drops"),
        "per_item_rev": g8.get("per_item_rev"),
        "per_item_rev_ctrl": gc.get("per_item_rev"),
        "segments_s8": g8.get("segments"),
        "segments_ctrl": gc.get("segments"),
        "spy": g8.get("spy_summary"),
    }


if __name__ == "__main__":
    main()
