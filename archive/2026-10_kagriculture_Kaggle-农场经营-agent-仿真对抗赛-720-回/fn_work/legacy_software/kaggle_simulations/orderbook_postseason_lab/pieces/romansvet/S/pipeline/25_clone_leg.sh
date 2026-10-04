#!/bin/bash
# 25_clone_leg.sh -- score one theta against the LIVE V48 CLONE, the rival that
# ANSWERS BACK.  S/melongenes/run_cell.sh's `v48` class with the theta made an
# argument instead of hard-wired to the shipped one.
#
#   usage: [WORKERS=4] [IDS=<file>] bash S/pipeline/25_clone_leg.sh <label> <theta.npy>
#
# WHY THIS LEG EXISTS.  A TAPE CANNOT REACT.  MELONGENES1 measured the same
# melon plate at +10,448 against the recording of a board and -15,451 against
# the exact V48 clone seated live on the SAME pinned town: the recording cannot
# re-price or re-time when we flood the book ahead of it.  Every tape leg --
# BAND250, ENGINE28, BAND2, HIBAND, and the REALES fitness itself -- therefore
# carries that phantom denial.  Any arm that moves the OPENING or the BOOK must
# clear this leg before it is believed.
#
# artifacts/panel_v48_hiband/opponent_tape_<id>/main.py is a symlink to the V48
# notebook's own source, so `town_inject`'s substring match still pins each
# board's town and the seat plays live.  Same registry (town_hiband.json), same
# seed base 3300786901, same ESR switch string, same --games 1 as the HIBAND
# judge leg, so the two are directly comparable board for board.
#
# Rows: S/lossflip/<label>_v48.csv.  Base rows for the SHIPPED package are
# S/lossflip/ship7692_v48.csv -- build them once with
#   bash S/pipeline/25_clone_leg.sh ship7692 S/winjudge/ship7692/theta7659.npy
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
name=$1; TH=$2
[ -n "$name" ] && [ -n "$TH" ] || die "usage: bash S/pipeline/25_clone_leg.sh <label> <theta.npy>"
case "$TH" in /*) ;; *) TH=$R/$TH ;; esac
[ -s "$TH" ] || die "no theta at $TH"
W=${WORKERS:-4}
IDS=${IDS:-$R/S/winjudge/hiband_ids.txt}
TREE=$(tree_for "$TH") || exit 1
[ -d $R/artifacts/panel_v48_hiband ] || die "artifacts/panel_v48_hiband missing -- the clone panel is not built on this box"
mkdir -p $PLOG

PT=$PLOG/${name}_v48_theta.npy
# PAD WITH THE TREE'S OWN pad_theta.py, not master's.  `tree_for` has already
# chosen the checkout whose policy.N_PARAMS can fly this theta; master's pad
# refuses anything longer than 7,692 ("a LONGER theta is a different layout"),
# so pairing master's pad with the alphafarm tree made this leg impossible to
# run on a 9,273-float REALES centre -- which is the only kind loop.sh produces.
$PY $TREE/S/winjudge/pad_theta.py "$TH" "$PT" || die "pad refused the theta"
opps=$(sed "s#^#$R/artifacts/panel_v48_hiband/opponent_tape_#; s#\$#/main.py#" $IDS | tr '\n' ' ')
out=$R/S/lossflip/${name}_v48.csv
say "25_clone_leg: label=$name boards=$(wc -l < $IDS) tree=$TREE workers=$W  (LIVE V48 clone in the opponent seat)"

cd $TREE || die "no $TREE"
KAGG3_TOWN_SCHEDULE=$R/S/winjudge/town_hiband.json PYTHONPATH=$TREE/src nice -n 10 $PY \
  $R/S/drainpin/on2b.py "$SW_ESR" --theta $PT --games 1 --workers $W \
  --seed-base 3300786901 --seed-per-opponent --opponents $opps \
  --csv $out > $PLOG/${name}.v48.log 2>&1
rc=$?
say "clone leg rc=$rc rows $(tail -n +2 $out 2>/dev/null | wc -l) -> $out"

if [ -s $R/S/lossflip/ship7692_v48.csv ] && [ "$name" != ship7692 ]; then
  echo; echo "=== vs the SHIPPED package on the clone leg (CRN, board = seats averaged) ==="
  $PY - "$name" <<'PY'
import csv, os, sys, math
R = "/mnt/e/_work/kaggriculture3"
sys.path.insert(0, R + "/S/judgekit")
import summary as J
b, e1 = J.read("{n}_v48.csv", "ship7692")
c, e2 = J.read("{n}_v48.csv", sys.argv[1])
if not b or not c:
    raise SystemExit(f"CLONE BASE/CAND MISSING {e1 or ''} {e2 or ''}")
bb, bc = J.boards(b, "v48"), J.boards(c, "v48")
k = [x for x in bb if x in bc]
d = [bc[x][0] - bb[x][0] for x in k]
dt = [bc[x][1] - bb[x][1] for x in k]
def t(v):
    n = len(v); m = sum(v)/n
    se = math.sqrt(sum((x-m)**2 for x in v)/(n-1)/n) if n > 1 else float("nan")
    return m, se, (m/se if se else float("nan"))
m, se, tt = t(d); mt, set_, ttt = t(dt)
w0 = sum(1 for x in k if bb[x][0] > 0); w1 = sum(1 for x in k if bc[x][0] > 0)
print(f"V48CLONE  {len(k):>4} boards   dmargin {m:+8.0f} se {se:5.0f} t {tt:+5.2f}"
      f"   dtheirs {mt:+8.0f} t {ttt:+5.2f}   wins {w0} -> {w1}")
print("  Δtheirs > 0 here is a REAL gift to a rival that can answer; a tape leg cannot see it.")
PY
fi
next "bash S/pipeline/20_judge.sh <label> <theta>     # the tape legs + the bar"
exit $rc
