#!/usr/bin/env python3
"""Pick NEW high-rated opponents out of our own live episodes.

    python S/pipeline/select_fresh.py <topN> <max_eps_per_team> [minrating]

Credential-free, exactly the two endpoints LIVEWATCH uses:
  LeaderboardService/GetLeaderboard   competitionId 147734  -> the ladder
  EpisodeService/ListEpisodes         submissionId          -> our games

WHY OUR OWN EPISODES.  A tape is a recording of ONE SEAT OF ONE GAME, and the
only games we can download in full are the ones we played.  So "refresh the
panel against the ladder top N" really means: among the games WE played, keep
the ones whose opponent is a top-N team (or rated >= minrating) and that the
panel does not already carry.  A top-N agent we have never been paired with
cannot be taped at all -- that is a limit of the data, not of this script.

Writes S/fresh/{lb.json, sel_fresh.json, epseat.txt, skipped.json}.
epseat.txt is `<episode id> <opponent seat>` per line -- the input S/fresh/dl.sh
and cut_all.sh read, same format as S/hiband/epseat.txt.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request

R = "/mnt/e/_work/kaggriculture3"
sys.path.insert(0, os.path.join(R, "S", "kaggle"))
from seat import agent_index  # noqa: E402  the ONLY place the seat default lives

T = os.path.join(R, "S", "fresh")
COMP = 147734
OUR_SUBS = [56335778, 56329775]          # the two live slots; edit when they change
API = "https://www.kaggle.com/api/i/competitions."


def post(path, body, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(
                API + path, data=json.dumps(body).encode(),
                headers={"Content-Type": "application/json"})
            return json.loads(urllib.request.urlopen(req, timeout=120).read())
        except Exception as e:                                   # noqa: BLE001
            print(f"  retry {k+1}/{tries} {path}: {e}")
            time.sleep(4 * (k + 1))
    raise SystemExit(f"{path} failed after {tries} tries")


def main(topn="10", maxeps="10", minrating="2700"):
    topn, maxeps, minrating = int(topn), int(maxeps), float(minrating)
    os.makedirs(T, exist_ok=True)

    lb = post("LeaderboardService/GetLeaderboard", {"competitionId": COMP})
    json.dump(lb, open(f"{T}/lb.json", "w"))
    teams = lb.get("teams") or lb.get("leaderboardTeams") or []
    top = teams[:topn]
    topnames = {str(t.get("teamName") or t.get("displayName") or "") for t in top}
    # NOTE the leaderboard row carries teamName but NOT a score field we can
    # read here, and ListEpisodes does not fill the opponent's teamName either.
    # So the top-N NAME filter is a best-effort second chance and the filter
    # that actually does the work is `rating >= minrating`, taken from the
    # episode's own `updatedScore`.  Verified 2026-09-19: top-3 names resolve,
    # opponent names come back empty, 10 boards selected on rating alone.
    print(f"ladder top {topn}: " + ", ".join(str(t.get("teamName"))[:20] for t in top))

    have = set()
    for f in ("hiband_ids.txt", "band250_ids.txt", "band2_ids.txt"):
        p = f"{R}/S/winjudge/{f}"
        if os.path.exists(p):
            have |= {l.strip() for l in open(p) if l.strip()}
    have |= {d.split("_")[-1] for d in os.listdir(f"{R}/artifacts/panel_opp_town")
             if d.startswith("opponent_tape_")}
    print(f"panel already carries {len(have)} board ids")

    sel, skipped, per_team = [], [], {}
    for sub in OUR_SUBS:
        eps = post("EpisodeService/ListEpisodes", {"submissionId": sub})
        rows = eps.get("episodes") or []
        agents = {a["episodeId"]: a for a in []}                # placeholder, see below
        print(f"sub {sub}: {len(rows)} episodes")
        for e in sorted(rows, key=lambda r: str(r.get("endTime")), reverse=True):
            ep = str(e.get("id") or e.get("episodeId") or "")
            ag = e.get("agents") or []
            if not ep or len(ag) != 2:
                continue
            mine = next((a for a in ag if str(a.get("submissionId")) == str(sub)), None)
            opp = next((a for a in ag if a is not mine), None)
            if mine is None or opp is None:
                continue
            team = str(opp.get("teamName") or opp.get("submission", {}).get("teamName") or "")
            rating = float(opp.get("updatedScore") or opp.get("initialScore") or 0)
            # SEAT LAW [S/kaggle/seat.py, docs/strategy/2026-09-16-nbintel2.md]:
            # the feed is proto3 and OMITS `index` when it is 0, so a MISSING
            # index means SEAT 0.  Defaulting the opponent to 1 is the NBINTEL2
            # bug and it cuts the tape at OUR OWN seat.  `agent_index` is the
            # only place that default is allowed to live.
            rec = dict(ep=ep, our_sub=str(sub), end=str(e.get("endTime")),
                       my=float(mine.get("reward") or 0), their=float(opp.get("reward") or 0),
                       my_seat=agent_index(mine), opp_seat=agent_index(opp),
                       opp_sub=opp.get("submissionId"), opp_team=team, opp_rating=rating)
            if rec["my_seat"] == rec["opp_seat"]:
                skipped.append(dict(rec, why="both agents report the same seat"))
                continue
            rec["won"] = rec["my"] > rec["their"]
            if ep in have:
                skipped.append(dict(rec, why="already in the panel"))
                continue
            if team not in topnames and rating < minrating:
                skipped.append(dict(rec, why=f"rating {rating:.0f} < {minrating:.0f} and not top-{topn}"))
                continue
            if per_team.get(team, 0) >= maxeps:
                skipped.append(dict(rec, why=f"already took {maxeps} from {team}"))
                continue
            per_team[team] = per_team.get(team, 0) + 1
            sel.append(rec)
        time.sleep(1.2)

    sel.sort(key=lambda r: (-r["opp_rating"], r["ep"]))
    json.dump(sel, open(f"{T}/sel_fresh.json", "w"), indent=1)
    json.dump(skipped, open(f"{T}/skipped.json", "w"), indent=1)
    open(f"{T}/epseat.txt", "w").write("".join(f"{r['ep']} {r['opp_seat']}\n" for r in sel))
    print(f"\nSELECTED {len(sel)} new boards ({len(skipped)} skipped) -> {T}/epseat.txt")
    for r in sel[:20]:
        print(f"  {r['ep']}  seat{r['opp_seat']}  {r['opp_team'][:24]:<26} {r['opp_rating']:>7.1f}"
              f"  {'WIN ' if r['won'] else 'LOSS'} {r['my']-r['their']:+9.0f}")
    for t, n in sorted(per_team.items(), key=lambda x: -x[1]):
        print(f"  team {t[:30]:<32} {n} boards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(*sys.argv[1:4]))
