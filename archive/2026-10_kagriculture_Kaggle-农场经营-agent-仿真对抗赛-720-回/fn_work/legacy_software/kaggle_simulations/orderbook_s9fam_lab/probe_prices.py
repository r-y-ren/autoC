# -*- coding: utf-8 -*-
"""probe_prices（s9 法证补针）：翻负局 s8 干预拍的实价与当日价格剖面（2 局）。

目的：③ topup 干预（翻负局 WOOL mid-band 挪卖假设）的实价标定——为分品阈重标
提供证据。输出 evidence/probe_prices.json。
只写 orderbook_s9fam_lab/；不改既有代码；不提交；不发射。
"""
from __future__ import annotations

import copy
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
for p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_goose_lab"),
          str(KSIM_DIR / "orderbook_s1form_lab"), str(KSIM_DIR / "orderbook_r40")):
    if p not in sys.path:
        sys.path.insert(0, p)

import judge_s_form as jsf  # noqa: E402

S8 = KSIM_DIR / "orderbook_s8spike_lab" / "build" / "s8" / "main.py"
V89 = KSIM_DIR / "orderbook_v89_lab" / "build" / "v89_pure" / "main.py"
TETSU = KSIM_DIR / "orderbook_racegap_lab" / "opponents" / "tetsu1009" / "main.py"


def main():
    os.chdir(KSIM_DIR)
    auth = json.loads((KSIM_DIR / "orderbook_s1form_lab" / "evidence"
                       / "sim_auth_cache.json").read_text(encoding="utf-8"))
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    out = []
    for seed, opath, on in ((674477, V89, "V89"), (677180, TETSU, "tetsutani")):
        sinks = {0: [], 1: []}
        entry = j23._load_entry(S8)
        g = entry.__globals__
        orig = g["_s8_apply"]
        log = []

        def spy(observation, action):
            hm = None
            try:
                if isinstance(action, dict):
                    hm = copy.deepcopy(action.get("market"))
            except Exception:
                hm = None
            o = orig(observation, action)
            try:
                log.append((int((observation or {}).get("step", 0)), hm,
                            copy.deepcopy(o.get("market")) if isinstance(
                                o, dict) else None))
            except Exception:
                pass
            return o

        g["_s8_apply"] = spy
        opp = j23._load_entry(opath)
        a0 = jsf._Tracer(entry, 0, sinks[0])
        a1 = jsf._Tracer(opp, 1, sinks[1])
        sb.run_games([{"seed": int(seed), "agents": [a0, a1]}],
                     {"engine": "auto", "bridge": auth})
        px = {}
        for e in sinks[0]:
            obs = e[1] or {}
            mp = (obs.get("market") or {}) if isinstance(obs.get("market"),
                                                         dict) else {}
            px[int(e[0])] = dict(mp.get("prices") or {})
        rows = []
        for step, hm, om in log:
            if om is None or hm is None or om == hm:
                continue
            n = len(hm)
            topups, appends = [], []
            for i in range(min(n, len(om))):
                if om[i] != hm[i]:
                    topups.append((i, hm[i], om[i]))
            for j in range(n, len(om)):
                appends.append((j, om[j]))
            rows.append({"step": step, "day": step // 24,
                         "topups": topups, "appends": appends,
                         "px": {k: px.get(step, {}).get(k)
                                for k in ("WOOL", "MILK", "WHEAT", "MELON")},
                         "day_wool_path": [px.get(s, {}).get("WOOL")
                                           for s in range(step // 24 * 24,
                                                          step // 24 * 24 + 24)
                                           if s in px]})
        out.append({"seed": seed, "opp": on, "interventions": rows})
    (HERE / "evidence" / "probe_prices.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, default=str)[:3000])


if __name__ == "__main__":
    main()
