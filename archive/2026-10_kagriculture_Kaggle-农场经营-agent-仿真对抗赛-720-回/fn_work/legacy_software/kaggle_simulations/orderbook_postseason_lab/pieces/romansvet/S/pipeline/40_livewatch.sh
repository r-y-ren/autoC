#!/bin/bash
# 40_livewatch.sh -- the LIVEWATCH read: how the two live submissions are doing.
#
#   usage: [DIR=S/livewatch9] bash S/pipeline/40_livewatch.sh
#
# Clones the last LIVEWATCH leg into a fresh numbered directory and runs its
# five steps in order.  The scripts use RELATIVE filenames, so cwd must be that
# directory -- that is the whole reason this wrapper exists.
#
#   fetch.py   -> ep_<sub>.json (EpisodeService/ListEpisodes) + lb.json
#                 (LeaderboardService/GetLeaderboard, competitionId 147734)
#   rows.py    -> games_<sub>.json
#   an.py      -> new_<sub>.json : games / W-L / rating / rank / last-20 / the
#                 delta against the PREVIOUS leg's games_*.json
#   getrep.py  -> replays/ep_<id>.json, the d2h0 step of each NEW loss
#   d2gate.py  -> d2gate_new.json : each new loss classified BAND vs ENGINE
#
# CREDENTIALS: none.  Both endpoints are called with a bare
# `Content-Type: application/json` header -- no cookie, no XSRF, no kaggle.json.
# EpisodeService/GetEpisodeReplay is DEAD (404): replays come from
# https://www.kaggleusercontent.com/episodes/<id>.json (~32 MB each).
#
# THE TWO HARD-CODED THINGS, BOTH NOW HANDLED HERE:
#   * the PREVIOUS leg's path (an.py ~:34) -- sed'd to leg N-1 below.
#   * the trajectory game-count lists (an.py ~:11 and ~:15) -- these used to be
#     literal tuples like `(87,95,100,107,...)` carried over from whichever leg
#     was cloned, so a leg two weeks later still printed the rating at game 87
#     and nothing near its own head.  The clone is now rewritten to call
#     `_traj(sub, rows)`, which reads the env var TRAJ_<subid> if you set one
#     and otherwise walks back from the CURRENT game count.  Override like:
#         TRAJ_56329775="150 160 165 170" bash S/pipeline/40_livewatch.sh
# The cloned fetch/rows/getrep/d2gate scripts carry historical hard-coded ids.
# Below we run temporary same-directory copies with the current ids, while
# an.py remains the committed statement of what the report compares.
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
set -o pipefail

# newest existing livewatch dir -> next number
last=$(ls -d $R/S/livewatch* 2>/dev/null | sed 's#.*/livewatch##' | grep -E '^[0-9]+$' | sort -n | tail -1)
DIR=${DIR:-$R/S/livewatch$((last + 1))}
case "$DIR" in /*) ;; *) DIR=$R/$DIR ;; esac
SRC=$R/S/livewatch$last
say "40_livewatch: cloning $SRC -> $DIR"
[ -d "$DIR" ] || { mkdir -p $DIR; cp $SRC/{fetch,rows,an,getrep,d2gate}.py $DIR/ || die "clone failed"; }
sed -i -E "s#S/livewatch[0-9]+/games_#S/livewatch$last/games_#g" $DIR/an.py

# --- the trajectory counts become ARGUMENTS, not literals --------------------
$PY - "$DIR/an.py" <<'PY'
import re, sys
p = sys.argv[1]
s = open(p).read()
HELP = '''import os as _os
def _traj(sub, rows):
    """Game counts to print the rating trajectory at.

    TRAJ_<subid> in the environment wins (space- or comma-separated).  With no
    override we walk back from THIS leg's own game count, so the read is always
    about the head of the run and never about whatever game number the leg this
    file was cloned from happened to care about.
    """
    v = _os.environ.get('TRAJ_%d' % sub)
    if v:
        return [int(x) for x in v.replace(',', ' ').split()]
    n = len(rows)
    return sorted({x for x in (n - 40, n - 30, n - 20, n - 10, n) if x > 1})
'''
if '_traj(' not in s:
    lines = s.splitlines(True)
    # insert the helper after the G={...} line (it needs nothing from it, but
    # that keeps the imports at the top where the next reader looks)
    for i, ln in enumerate(lines):
        if ln.startswith('G='):
            lines.insert(i + 1, HELP)
            break
    s = ''.join(lines)
    # for n in (87,95,...):   ->   for n in _traj(<sub>, G[<sub>]):
    out, sub = [], None
    for ln in s.splitlines(True):
        m = re.match(r"^print\('\\n(\d+) trajectory", ln)
        if m:
            sub = m.group(1)
        m2 = re.match(r"^(\s*)for n in \([\d,\s]+\):\s*$", ln)
        if m2 and sub:
            ln = "%sfor n in _traj(%s, G[%s]):\n" % (m2.group(1), sub, sub)
        out.append(ln)
    s = ''.join(out)
    open(p, 'w').write(s)
    print("an.py: trajectory counts are now _traj(sub, rows) -- override with TRAJ_<subid>")
else:
    print("an.py: already uses _traj()")
PY
say "an.py now diffs against S/livewatch$last; trajectory counts:"
grep -nE "for n in |games_%d'%s\)" $DIR/an.py | head -6

cd $DIR || die "no $DIR"
temps=()
cleanup_livewatch_temps() { [ ${#temps[@]} -eq 0 ] || rm -f "${temps[@]}"; }
trap cleanup_livewatch_temps EXIT
live_script() {
  case "$1" in
    fetch|rows) ids='(56489764, 56482921, 56472823)' ;;
    getrep|d2gate) ids='(56489764, 56482921)' ;;
    *) LIVE_RUN="$1.py"; return ;;
  esac
  tmp=".livewatch_${1}_$$.py"
  temps+=("$tmp")
  $PY - "$1.py" "$tmp" "$ids" <<'PY'
import re, sys
src, dst, ids = sys.argv[1:]
s = open(src).read()
s = s.replace('(56370365, 56335778, 56329775)', ids)
s = s.replace('(56370365, 56335778)', ids)
if src == 'd2gate.py':
    s = s.replace("    sub,g=allg[ep]", "    if ep not in allg: continue\n    sub,g=allg[ep]")
open(dst, 'w').write(s)
PY
  LIVE_RUN="$tmp"
}
for s in fetch rows an; do
  say "$s.py"
  live_script "$s"
  $PY "$LIVE_RUN" || die "$s.py failed (a 404 on the episode service means the endpoint moved -- see the header)"
done
say "getrep.py (downloads the d2h0 step of each new loss; ~32 MB per episode)"
live_script getrep
$PY "$LIVE_RUN" | tail -5
say "d2gate.py"
live_script d2gate
$PY "$LIVE_RUN" | tail -30

echo
echo "READ IT LIKE THIS:"
echo "  rating + rank + last-20 per sub; the LEADER and the TOP-5 BAR from lb.json;"
echo "  gap = our best rating - the bar.  Loss classes: BAND = the open-loop clone"
echo "  we already model, ENGINE/OTHER = a class the panel may not carry yet."
echo "SLOT LAW: Kaggle keeps only the NEWEST TWO submissions active.  Uploading"
echo "  one retires the OLDER of the two -- today that is our BEST agent."
next "many new ENGINE losses, or a new top-10 id?  bash S/pipeline/05_refresh_opponents.sh 3"
echo "  otherwise: bash S/pipeline/loop.sh"
