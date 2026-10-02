#!/bin/bash
# 26_selfplay_leg.sh -- seat the CURRENT BEST PACKAGE as a live opponent and play
# the candidate theta against it.  S/h2h's method, with the candidate seat made
# a theta instead of a second package.
#
#   usage: [WORKERS=4] [PKG=<tar.gz>] [IDS=<file>] [SEATS=2] \
#          bash S/pipeline/26_selfplay_leg.sh <label> <theta.npy>
#
# PKG defaults to the LIVE package `dist/submission_flow193_g100_hr_ft2_esr_wp_wpf.tar.gz`
# (sub 56335778).  Point it at S/pipeline/best/package.tar.gz once the loop has
# promoted one.
#
# THE sys.modules GOTCHA (the whole reason this file exists).  A packaged agent
# is a SECOND COPY of this repo.  Its `main.py` does a plain `from kagg3 import
# ...`, and if this process already imported the working tree's `kagg3` that
# import is a NO-OP -- the package silently runs the CURRENT planner against its
# own frozen theta, and the measurement is of nothing.  `eval_vs_baselines.py`
# handles this for ONE packaged seat (`_vendored_imports`: it drops `kagg3.*`
# from `sys.modules`, hides every `sys.path` entry a `kagg3` could come from,
# and clears `KAGG3_*` from the environment for the length of the game, then
# puts all three back).  Our seat is built BEFORE that context opens, so it is
# unaffected.
#   => ONE packaged agent + a `--theta` seat is SAFE with no renaming.
#   => TWO packaged agents in one worker are NOT: they share the one `kagg3`
#      slot and the second silently runs the first's planner.  That is why
#      S/h2h had to copy package B and rename `kagg3 -> kagg3wpf` inside it.
#      If you ever seat two packages here, do that rename first.
#
# TOWN PINNING.  `town_inject` matches the registry key as a SUBSTRING of the
# opponent path, so the opponent directory is named `opponent_B_<id>` per board
# (S/h2h's convention) and `KAGG3_TOWN_SCHEDULE` is the hiband registry.  Each
# board is played in BOTH seats (`--seats 2`) and the two rows are averaged into
# one observation, which is the judge's board statistic everywhere else.
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
name=$1; TH=$2
[ -n "$name" ] && [ -n "$TH" ] || die "usage: bash S/pipeline/26_selfplay_leg.sh <label> <theta.npy>"
case "$TH" in /*) ;; *) TH=$R/$TH ;; esac
[ -s "$TH" ] || die "no theta at $TH"
W=${WORKERS:-4}; SEATS=${SEATS:-2}
PKG=${PKG:-$R/dist/submission_flow193_g100_hr_ft2_esr_wp_wpf.tar.gz}
[ -s "$PKG" ] || die "no package at $PKG"
IDS=${IDS:-$R/S/winjudge/hiband_ids.txt}
TREE=$(tree_for "$TH") || exit 1
PAN=$R/S/pipeline/selfpanel
mkdir -p $PLOG $PAN

say "26_selfplay_leg: label=$name  opponent=$(basename $PKG) md5 $(md5sum $PKG | cut -c1-8)"
say "                 boards=$(wc -l < $IDS) seats=$SEATS tree=$TREE workers=$W"

# --- unpack the opponent ONCE, then one symlinked dir per pinned town ---------
ROOTD=$PAN/pkg_$(md5sum $PKG | cut -c1-8)
if [ ! -s $ROOTD/main.py ]; then
  rm -rf $ROOTD; mkdir -p $ROOTD
  tar -xzf "$PKG" -C $ROOTD || die "untar failed"
  [ -s $ROOTD/main.py ] || ROOTD=$(dirname "$(find $ROOTD -name main.py | head -1)")
  [ -s $ROOTD/main.py ] || die "no main.py in $PKG"
  say "unpacked -> $ROOTD (main.py md5 $(md5sum $ROOTD/main.py | cut -c1-8))"
else
  say "reusing $ROOTD"
fi
# The per-town directory is a symlink to the WHOLE unpacked package, never to
# its main.py alone.  A packaged `main.py` does
# `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))`, and
# `abspath` does NOT resolve symlinks -- so a symlinked main.py puts the EMPTY
# `opponent_B_<id>/` on sys.path, `from kagg3 import ...` raises, the agent
# passes every turn and scores exactly its 3,000 starting purse.  (Measured:
# that is precisely what happened the first time this script ran.)  Symlinking
# the directory makes the same path resolve to the package's own contents.
# S/melongenes' v48 panel gets away with a main.py symlink only because that
# agent is a single self-contained file with its source inlined.
LNK=$PAN/towns_$(md5sum $PKG | cut -c1-8); mkdir -p $LNK
opps=""
while read -r id; do
  [ -z "$id" ] && continue
  rm -rf $LNK/opponent_B_$id
  ln -sfn $ROOTD $LNK/opponent_B_$id
  opps="$opps $LNK/opponent_B_$id/main.py"
done < $IDS

PT=$PLOG/${name}_self_theta.npy
$PY $R/S/winjudge/pad_theta.py "$TH" "$PT" || die "pad refused the theta"
out=$R/S/lossflip/${name}_self.csv

cd $TREE || die "no $TREE"
KAGG3_TOWN_SCHEDULE=$R/S/winjudge/town_hiband.json PYTHONPATH=$TREE/src nice -n 10 $PY \
  $R/S/drainpin/on2b.py "$SW_ESR" --theta $PT --games 1 --seats $SEATS --workers $W \
  --seed-base 3300786901 --seed-per-opponent --opponents $opps \
  --csv $out > $PLOG/${name}.self.log 2>&1
rc=$?
rows=$(tail -n +2 $out 2>/dev/null | wc -l)
say "selfplay rc=$rc rows $rows -> $out"
[ "$rc" = 0 ] || { tail -15 $PLOG/${name}.self.log; die "selfplay leg failed (log $PLOG/${name}.self.log)"; }

# --- read it, S/h2h/report.py's per-town unit --------------------------------
$PY - "$out" <<'PY'
import csv, re, sys, math
rows = list(csv.DictReader(open(sys.argv[1])))
rec = {}
for r in rows:
    m = re.search(r"opponent_B_(\d+)", r["opponent"])
    if not m:
        continue
    rec.setdefault(m.group(1), []).append((float(r["mine"]), float(r["theirs"])))
d = [sum(a - b for a, b in v) / len(v) for v in rec.values()]
if not d:
    raise SystemExit("no opponent_B_<id> rows -- town pinning did not take")
n = len(d); mean = sum(d) / n
se = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1) / n) if n > 1 else float("nan")
w = sum(1 for x in d if x > 0); l = sum(1 for x in d if x < 0)
print(f"\nSELFPLAY  {n} towns ({len(rows)} rows)  cand {w} - {l} best (ties {n-w-l})"
      f"  mean d(cand-best) {mean:+8.0f} +- {se:6.0f}  t {mean/se if se else float('nan'):+5.2f}")
dead = [r for r in rows if float(r["theirs"]) <= 3000.0]
if dead:
    print(f"  *** {len(dead)}/{len(rows)} rows have theirs <= 3,000 = the STARTING PURSE. ***")
    print("  The packaged opponent did not act: it failed to import its own kagg3")
    print("  and passed every turn.  The leg is VOID -- fix the panel, do not read it.")
    raise SystemExit(3)
print("  Head-to-head strength is NOT ladder strength [h2h]: these coins are a")
print("  zero-sum split of ONE shared market, and an arm that takes coin off our")
print("  own clone can still gift a third-party engine.  Read it as a regression")
print("  check on the previous best, never as a rating forecast.")
PY
next "bash S/pipeline/20_judge.sh $name $TH        # the tape legs decide the bar"
