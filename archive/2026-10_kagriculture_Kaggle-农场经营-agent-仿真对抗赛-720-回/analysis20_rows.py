#!/usr/bin/env python3
"""analysis20 pool audit: pull + parse replays into compact rows.

Targets:
  a) r34a (56526029) ALL public episodes  (audit main body, ~95)
  b) r33  (56517991) public episodes MISSING from /tmp/r33audit (window, ~81)
  c) r33  public episodes already present in /tmp/r33audit (~42) -> parse in place, files kept

/tmp is tmpfs (2.8G free): NEW replays are streamed pull -> parse -> delete;
only compact rows are retained. Existing files are parsed in place and kept.

Row schema (per main-session spec):
  {episode, tag, opp, seat, res, margin, ourF, oppF, opp_band, opp_actions,
   opp_animals_end, margin_d10, margin_d20} + createTime, money_ratio,
   mirror_twin (fallback rule |margin|<500 AND money_ratio<0.01), statuses.

Output: /tmp/kagr_root/analysis20_rows.json (rewritten incrementally).
"""
import json, os, subprocess, sys, time

KAGGLE = "/home/renyxin/.local/bin/kaggle"
ROOT = "/tmp/kagr_root"
AUD = "/tmp/r33audit"
OUR = "renyxin"
SEED_VALUE = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}


def jload(x):
    return json.loads(x) if isinstance(x, str) else x


def band(f):
    return "weak<60k" if f < 60000 else ("mid60-90k" if f < 90000 else "strong>=90k")


def day_end_money(steps, seat, day):
    si = day * 24 + 23
    if si >= len(steps):
        si = len(steps) - 1
    f = jload(steps[si][0]["observation"]["farms"])
    return f[seat]["money"]


def parse_replay(fp, ep2tag, ep2time):
    d = json.load(open(fp))
    eid = d["info"]["EpisodeId"]
    names = d["info"]["TeamNames"]
    base = {"episode": eid, "tag": ep2tag.get(eid), "createTime": ep2time.get(eid)}
    if names.count(OUR) == 2:
        return dict(base, error="selfplay_renyxin_vs_renyxin", rewards=d.get("rewards"))
    if OUR not in names:
        return dict(base, error=f"renyxin not in {names}")
    seat = names.index(OUR)
    oseat = 1 - seat
    opp = names[oseat]
    steps = d["steps"]
    r = d["rewards"]
    our_r, opp_r = r[seat], r[oseat]
    if our_r is None or opp_r is None:
        return dict(base, error=f"reward None {r}")
    res = "W" if our_r > opp_r else ("L" if our_r < opp_r else "T")
    last = steps[-1][seat]["observation"]
    farms = jload(last["farms"])
    ourF, oppF = farms[seat]["money"], farms[oseat]["money"]
    # ---- opp action census (conventions from audit_r32r33.py) ----
    oseed_buys = oanimal_buys = osells = 0
    oland = obuild = ohire = 0
    for stp in steps:
        act = stp[oseat].get("action") or {}
        for m in act.get("market") or []:
            if isinstance(m, list) and len(m) >= 3 and m[0] == "BUY_SEED":
                oseed_buys += m[2]
            elif isinstance(m, list) and len(m) >= 3 and m[0] == "BUY_ANIMAL":
                oanimal_buys += m[2]
            elif isinstance(m, list) and len(m) >= 2 and m[0] == "SELL":
                osells += 1
        for c in act.get("farmer") or []:
            if not isinstance(c, str):
                continue
            if c == "BUY_LAND":
                oland += 1
            elif c.startswith("BUILD"):
                obuild += 1
        for h in act.get("hands") or []:
            for c in (h if isinstance(h, list) else [h]):
                if not isinstance(c, str):
                    continue
                if c == "BUY_LAND":
                    oland += 1
                elif c.startswith("BUILD"):
                    obuild += 1
                elif c == "HIRE":
                    ohire += 1
    oanimals = {}
    for trow in farms[oseat]["tiles"]:
        for v in trow:
            if isinstance(v, dict) and "animal" in v:
                oanimals[v["animal"]] = oanimals.get(v["animal"], 0) + 1
    o_d10 = day_end_money(steps, oseat, 10)
    o_d20 = day_end_money(steps, oseat, 20)
    m_d10 = day_end_money(steps, seat, 10)
    m_d20 = day_end_money(steps, seat, 20)
    mean_f = (ourF + oppF) / 2 or 1.0
    money_ratio = abs(ourF - oppF) / mean_f
    margin = our_r - opp_r
    row = dict(
        base,
        opp=opp, seat=seat, res=res, margin=round(margin, 1),
        ourF=ourF, oppF=oppF, opp_band=band(oppF),
        opp_actions={"seed_buys": oseed_buys, "animal_buys": oanimal_buys,
                     "sells": osells, "land": oland, "build": obuild, "hire": ohire},
        opp_animals_end=oanimals,
        margin_d10=round(m_d10 - o_d10, 0), margin_d20=round(m_d20 - o_d20, 0),
        money_ratio=round(money_ratio, 5),
        mirror_twin=bool(abs(margin) < 500 and money_ratio < 0.01),
    )
    return row


def pull(id_):
    fp = f"{AUD}/episode-{id_}-replay.json"
    if os.path.exists(fp) and os.path.getsize(fp) > 1000:
        return fp, "have"
    for attempt in (1, 2):
        try:
            p = subprocess.run([KAGGLE, "competitions", "replay", str(id_)],
                               capture_output=True, text=True, timeout=600, cwd=AUD)
        except subprocess.TimeoutExpired:
            p = None
        if p and p.returncode == 0 and os.path.exists(fp) and os.path.getsize(fp) > 1000:
            return fp, "pulled"
        time.sleep(5)
    return None, "FAIL"


def main():
    os.makedirs(AUD, exist_ok=True)
    meta = {"r34a": 56526029, "r33": 56517991}  # r34a first: audit main body, priority on rate limits
    ep2tag, ep2time = {}, {}
    have_ids = {int(f.split("-")[1]) for f in os.listdir(AUD) if f.startswith("episode-")}
    targets = []  # (id, group)
    for tag, ref in meta.items():
        lst = json.load(open(f"{ROOT}/episodes-{tag}-{ref}.json"))
        pub = [e for e in lst if "PUBLIC" in e.get("type", "")]
        for e in pub:
            ep2tag[e["id"]] = tag
            ep2time[e["id"]] = e["createTime"]
        pub.sort(key=lambda e: e["createTime"])
        if tag == "r34a":
            targets += [(e["id"], "a_r34a_full") for e in pub]
        else:
            targets += [(e["id"], "b_r33_window") for e in pub if e["id"] not in have_ids]
            targets += [(e["id"], "c_r33_prior") for e in pub if e["id"] in have_ids]
    print(f"targets: a={sum(1 for _, g in targets if g == 'a_r34a_full')} "
          f"b={sum(1 for _, g in targets if g == 'b_r33_window')} "
          f"c={sum(1 for _, g in targets if g == 'c_r33_prior')}", flush=True)

    out_fp = f"{ROOT}/analysis20_rows.json"
    state = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
             "groups": {}, "rows": [], "fails": [], "selfplay": []}
    done = 0
    t0 = time.time()
    for eid, grp in targets:
        fp, status = pull(eid)
        if status == "FAIL":
            state["fails"].append({"episode": eid, "group": grp})
            print(f"FAIL {grp} {eid}", flush=True)
        else:
            try:
                row = parse_replay(fp, ep2tag, ep2time)
            except Exception as ex:
                state["fails"].append({"episode": eid, "group": grp, "parse_error": str(ex)[:200]})
                print(f"PERR {grp} {eid} {ex}", flush=True)
                row = None
            if row is not None:
                if "error" in row:
                    state["selfplay"].append(row) if "selfplay" in row["error"] else state["fails"].append(
                        {"episode": eid, "group": grp, "row_error": row["error"]})
                    print(f"ERR  {grp} {eid} {row['error']}", flush=True)
                else:
                    row["group"] = grp
                    state["rows"].append(row)
            if status == "pulled":
                os.remove(fp)  # tmpfs capacity: stream delete after parse
        done += 1
        if done % 5 == 0 or done == len(targets):
            state["groups"] = {g: sum(1 for r in state["rows"] if r.get("group") == g)
                               for g in ("a_r34a_full", "b_r33_window", "c_r33_prior")}
            tmp = out_fp + ".tmp"
            json.dump(state, open(tmp, "w"), ensure_ascii=False)
            os.replace(tmp, out_fp)
            el = time.time() - t0
            print(f"[{done}/{len(targets)}] rows={len(state['rows'])} fails={len(state['fails'])} "
                  f"elapsed={el:.0f}s eta={el / done * (len(targets) - done):.0f}s", flush=True)
    state["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    state["groups"] = {g: sum(1 for r in state["rows"] if r.get("group") == g)
                       for g in ("a_r34a_full", "b_r33_window", "c_r33_prior")}
    json.dump(state, open(out_fp, "w"), ensure_ascii=False)
    print("DONE", json.dumps(state["groups"]), "fails:", len(state["fails"]),
          "selfplay:", len(state["selfplay"]), flush=True)


if __name__ == "__main__":
    main()
