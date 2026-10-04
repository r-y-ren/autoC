#!/usr/bin/env python3
"""FRESH: turn the cut episodes in S/fresh/cut into a judge-ready leg.

    .venv/bin/python S/pipeline/build_fresh.py

Structure = S/hiband/build_set.py -- same verification gates, same REGISTRY LAW:
every id MUST land in town_schedules.json or it is NOT pinned and must not be
judged [WINRATE2 LAW].  Writes S/fresh/{ids.txt, town_schedules.json} and the
judge-kit copies S/winjudge/{fresh_ids.txt, town_fresh.json}.

Seed rung 3500787501 -- a rung no other leg uses, so FRESH boards never collide
with BAND250 (2900...), BAND2 (3100...), HIBAND (3300...) or the toplegs.
"""
from __future__ import annotations

import json
import os
import re
import sys

import numpy as np

sys.path.insert(0, "src")
from kagg3.es import tape_actions as TA  # noqa: E402

R = "/mnt/e/_work/kaggriculture3"
T = f"{R}/S/fresh"
BASE = f"{R}/S/winjudge/town_hiband.json"      # the largest registry on disk
SB0 = 3500787501


def main():
    sel = json.load(open(f"{T}/sel_fresh.json"))
    rows = []
    for c in sel:
        ep = str(c["ep"])
        log = f"{T}/cut/{ep}.out"
        rec = dict(c, ep=ep, verify_drawn="MISSING", verify_town="MISSING",
                   steps=0, acting=0, unlocks=0, ok=False, sched=None)
        if os.path.exists(log):
            lines = [l for l in open(log).read().splitlines() if l.startswith("episode ")]
            if lines:
                m = re.search(r"(\d+) steps, (\d+) acting", lines[0])
                rec["verify_drawn"] = "verified" if ", verified" in lines[0] else "UNVERIFIED"
                if m:
                    rec["steps"], rec["acting"] = int(m.group(1)), int(m.group(2))
            if len(lines) >= 2:
                rec["verify_town"] = "verified" if ", verified" in lines[1] else "UNVERIFIED"
        pk = f"{R}/artifacts/panel_opp_town/opponent_tape_{ep}/main.py"
        npz_t = f"{R}/artifacts/tape_actions_town/{ep}.npz"
        npz_d = f"{R}/artifacts/tape_actions/{ep}.npz"
        rec["pkg"] = os.path.exists(pk)
        rec["npz_town"], rec["npz_drawn"] = os.path.exists(npz_t), os.path.exists(npz_d)
        if rec["pkg"] and rec["npz_town"]:
            z = np.load(npz_t)
            rec["sched"] = [[int(a), str(b)] for a, b in TA.town_schedule(z["town"].astype(np.int32))]
            rec["unlocks"] = len(rec["sched"])
        rec["ok"] = (rec["verify_drawn"] == "verified" and rec["verify_town"] == "verified"
                     and rec["pkg"] and rec["npz_town"] and rec["npz_drawn"] and rec["unlocks"] > 0)
        rows.append(rec)

    rows.sort(key=lambda r: (-float(r["opp_rating"] or 0), r["ep"]))
    good = [r for r in rows if r["ok"]]
    print(f"cut {len(rows)} episodes, {len(good)} fully verified")
    for r in rows:
        if not r["ok"]:
            print("  DROP", r["ep"], r["verify_drawn"], r["verify_town"],
                  "pkg" if r["pkg"] else "NOPKG")
    if not good:
        raise SystemExit("nothing verified -- the leg is NOT built (this is the gate working)")

    open(f"{T}/ids.txt", "w").write("".join(r["ep"] + "\n" for r in good))
    base = json.load(open(BASE))
    out = dict(base)
    added = 0
    for r in good:
        if r["ep"] in out:
            print("  ALREADY IN REGISTRY", r["ep"])
            continue
        out[r["ep"]] = r["sched"]
        added += 1
    json.dump(out, open(f"{T}/town_schedules.json.tmp", "w"), indent=1)
    chk = json.load(open(f"{T}/town_schedules.json.tmp"))
    assert all(chk[k] == v for k, v in base.items()) and list(chk)[:len(base)] == list(base), \
        "prior rows disturbed -- REFUSING to write the registry"
    os.replace(f"{T}/town_schedules.json.tmp", f"{T}/town_schedules.json")
    missing = [r["ep"] for r in good if r["ep"] not in chk]
    assert not missing, f"NOT PINNED: {missing}"

    open(f"{R}/S/winjudge/fresh_ids.txt", "w").write("".join(r["ep"] + "\n" for r in good))
    json.dump(out, open(f"{R}/S/winjudge/town_fresh.json", "w"), indent=1)
    print(f"town registry {len(base)} -> {len(chk)} (+{added}); FRESH {len(good)} boards, "
          f"seed base {SB0}")
    for i, r in enumerate(good):
        print(f"  {i:>2} {r['ep']} {float(r['opp_rating'] or 0):>7.1f} "
              f"{'LOSS' if not r['won'] else 'WIN '} seat{r['opp_seat']} "
              f"live {r['my'] - r['their']:+8.0f} seed {SB0 + 1000003 * i}")
    print("\nID ORDER IS LOAD-BEARING: --seed-per-opponent draws seed(board i) = "
          f"{SB0} + 1000003*i, so reordering fresh_ids.txt is a DIFFERENT board set.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
