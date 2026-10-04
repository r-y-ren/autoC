#!/bin/bash
# 05_refresh_opponents.sh -- pull the newest high-band live games into the tape
# panel and expose them as a new judge leg, `LEGS=fresh`.
#
#   usage: [MINRATING=2700] [MAXEPS=10] [P=4] [STOP=select|download|cut|build] \
#          bash S/pipeline/05_refresh_opponents.sh [topN]
#
# RUN IT WEEKLY, or the moment 40_livewatch.sh shows a new id in the ladder
# top 10 or a run of losses classed ENGINE/OTHER rather than BAND.  The panel
# ages: every judge leg is a recording of a game that was played days ago.
#
# THE CAVEAT THAT GOVERNS EVERY TAPE LEG.  A TAPE CANNOT RE-PLAN.  MELONGENES1
# measured the same arm at +10,448 against the recording of a board and -15,451
# against the exact live clone on the SAME pinned town: the recording cannot
# re-price or re-time when we move the book ahead of it.  Fresh tapes make the
# panel CURRENT; they do not make it REACTIVE.  Anything that touches the
# opening or the order book still has to clear 25_clone_leg.sh.
#
# STAGES (STOP=<stage> halts after that one)
#   select    S/pipeline/select_fresh.py -- leaderboard + our own episodes,
#             credential-free; keeps opponents rated >= MINRATING that the panel
#             does not already carry; writes S/fresh/epseat.txt
#   download  S/fresh/dl.sh   -- kaggleusercontent.com/episodes/<id>.json (~32 MB
#             each; EpisodeService/GetEpisodeReplay is DEAD, it 404s)
#   cut       S/fresh/cut_all.sh -> cut_one.sh -- for each episode, at the
#             OPPONENT's seat: scripts/tape_opponent.py (drawn AND --with-town)
#             + scripts/make_tape_actions.py, into
#             artifacts/panel_opp_town/opponent_tape_<ep>/ and
#             artifacts/tape_actions_town/<ep>.npz
#   build     S/pipeline/build_fresh.py -- verification gates + the REGISTRY LAW
#             (an id that does not land in the town registry is NOT PINNED and
#             must not be judged [WINRATE2]); writes S/winjudge/fresh_ids.txt
#             and S/winjudge/town_fresh.json
#   classify  the d2 gate census of the new boards (melon / wheat / carrot tile
#             counts at day 2) so a genuinely NEW opponent class is visible
#             rather than averaged away.
#
# All of it is S/hiband's recipe with the directory changed; the three shell
# stages are generated from S/hiband's by substitution, so there is one recipe.
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
N=${1:-10}; MINRATING=${MINRATING:-2700}; MAXEPS=${MAXEPS:-10}; P=${P:-4}
F=$R/S/fresh
mkdir -p $F $R/artifacts/fresh_replays
stop() { [ "$STOP" = "$1" ] && { say "STOP=$1 -- halting here"; exit 0; }; return 0; }

say "05_refresh_opponents: topN=$N minrating=$MINRATING maxeps=$MAXEPS parallel=$P"

# ---- 1. select ---------------------------------------------------------------
$PY $R/S/pipeline/select_fresh.py $N $MAXEPS $MINRATING || die "selection failed"
n=$(grep -c . $F/epseat.txt 2>/dev/null || echo 0)
[ "$n" -gt 0 ] || { say "nothing new to add -- the panel is current"; exit 0; }
stop select

# ---- 2/3. generate the download + cut scripts from S/hiband's ----------------
for s in dl.sh cut_one.sh cut_all.sh; do
  sed 's#/S/hiband#/S/fresh#g; s#hiband_replays#fresh_replays#g' $R/S/hiband/$s > $F/$s
done
say "generated $F/{dl.sh,cut_one.sh,cut_all.sh} from S/hiband's (same recipe, new dirs)"

say "downloading $n replays (~32 MB each, 5 in parallel)"
bash $F/dl.sh | tail -5
stop download

say "cutting $n episodes at the OPPONENT seat (P=$P)"
P=$P bash $F/cut_all.sh | tail -3
stop cut

# ---- 4. build the leg --------------------------------------------------------
$PY $R/S/pipeline/build_fresh.py || die "build failed"
stop build

# ---- 5. what class are they? -------------------------------------------------
say "d2 census of the new boards (the classifier S/livewatch*/d2gate.py applies to losses)"
$PY - <<'PY'
import json, os
R = "/mnt/e/_work/kaggriculture3"
sel = json.load(open(f"{R}/S/fresh/sel_fresh.json"))
ids = [l.strip() for l in open(f"{R}/S/winjudge/fresh_ids.txt")] if \
    os.path.exists(f"{R}/S/winjudge/fresh_ids.txt") else []
keep = [r for r in sel if r["ep"] in ids]
print(f"{len(keep)} boards on the leg; opponents by rating band:")
for lo, hi in ((3000, 9999), (2900, 3000), (2800, 2900), (2700, 2800), (0, 2700)):
    k = [r for r in keep if lo <= r["opp_rating"] < hi]
    if k:
        print(f"  {lo}-{hi}: {len(k):>3} boards, we went "
              f"{sum(1 for r in k if r['won'])}-{sum(1 for r in k if not r['won'])}")
print("A band we lose HARD and did not carry before is a NEW CLASS: read its d2")
print("tile counts (melon/wheat/carrot) with S/livewatch8/d2gate.py before you")
print("train against it, or the panel just re-weights the class you already beat.")
PY

cat <<EOF

================ ADD THE LEG TO THE JUDGE ================
S/winjudge/judge.sh already carries a \`fresh\` leg:

    run_leg fresh   \${IDS_FRESH:-\$SELF/fresh_ids.txt}   \$SELF/town_fresh.json   3500787501

so the leg runs with

    LEGS=fresh WORKERS=4 bash S/winjudge/judge.sh <label> <theta.npy>

and the rows land in S/lossflip/<label>_fresh.csv.  Bank the SHIPPED package's
rows once before judging anything against them:

    LEGS=fresh WORKERS=4 bash S/winjudge/judge.sh ship7692 S/winjudge/ship7692/theta7659.npy

THE LABEL IS \`ship7692\`, NOT \`ship7692_fresh\`.  Every report reader opens
\`S/lossflip/<BASE>_<leg>.csv\` and BASE is \`ship7692\`, so a leg banked under the
label \`ship7692_fresh\` lands at \`ship7692_fresh_fresh.csv\` and the pairing
silently reports MISSING BASE.  (That is what the first end-to-end run of this
script did on 2026-09-19; the rows were right and the name was not.)  judge.sh
writes its per-leg summary as \`S/winjudge/ship7692/summary_<leg>.txt\`, so
re-using the \`ship7692\` label does NOT overwrite the banked band250 rows.
==========================================================
EOF
next "bash S/pipeline/20_judge.sh <label> <centre>   # then add LEGS=fresh as a 4th cell"
