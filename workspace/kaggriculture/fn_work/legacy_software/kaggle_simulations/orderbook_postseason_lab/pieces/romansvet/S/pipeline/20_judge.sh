#!/bin/bash
# 20_judge.sh -- judge one centre against the SHIPPED package on every leg the
# ledger is paired on, then print the bar.  REALESJUDGE's recipe, wrapped.
#
#   usage: [WORKERS=4] [BASE=ship7692] [BAR=ship|promote] [LEGS_ONLY="..."] \
#          [SMOKE=<n>] bash S/pipeline/20_judge.sh <label> <centre.npy>
#
# Legs, all vs BASE (default `ship7692` = the LIVE package, layout 7,692):
#   POOLED278 = BAND250 (250 held-out band tapes) + TOPLEG2/3 (60 top-10 tapes,
#               28 of them the ENGINE28 retention class)   -> label  <label>
#   BAND2     = 233 more pinned band tapes, disjoint, rung 3100 -> <label>_b2
#   HIBAND    = the 56 pinned tapes of the >= 2,700 band we ACTUALLY play now
#                                                           -> <label>_hi
# then POOLED511 = 278 + 233 read by S/winjudge/report_pool511.py.
#
# WHICH TREE.  `judge.sh` flies the checkout it lives in, so a 9,273-float
# REALES centre MUST be judged from the alphafarm worktree and a <= 7,692 theta
# from master.  This script picks the tree for you from the theta's length and
# prints which one it used; the leg CSVs land in the SHARED $R/S/lossflip, so
# the labels pool across trees exactly as REALESJUDGE's did.
#
# SMOKE=<n> runs the SAME THREE-LEG CHAIN on the first n ids of every leg --
# band250 + topleg2 + topleg3, then band2, then hiband -- and then the real
# readers (report_hiband, report_pool511, verdict).  It proves the whole reader
# chain on ~5n boards instead of 511.  A short id file is a DIFFERENT board
# set (a PREFIX still pairs, because `--seed-per-opponent` draws the seed from
# the id's POSITION), so smoke rows are written under `<label>_smoke*` and must
# NEVER be banked or compared against a real label.
#
# LEGS_ONLY="hiband" runs ONE leg set instead of the three, and puts the bar on
# THAT cell.  It is the reduced cycle `loop.sh JUDGE_ONLY=` uses: 56 boards
# instead of 511, ~15 min instead of ~90.  The verdict it prints says HIBAND,
# not POOLED511, and it is NOT a ship read -- HIBAND is 56 boards of one band
# and JOINTFREE2 is the standing warning about reading flips off whichever leg
# was already banked.  Promote on it; never ship on it.
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
name=$1; CEN=$2
[ -n "$name" ] && [ -n "$CEN" ] || die "usage: bash S/pipeline/20_judge.sh <label> <centre.npy>"
case "$CEN" in /*) ;; *) CEN=$R/$CEN ;; esac
[ -s "$CEN" ] || die "no centre at $CEN"
W=${WORKERS:-4}; BASE=${BASE:-ship7692}; BAR=${BAR:-ship}
TREE=$(tree_for "$CEN") || exit 1
N=$($PY -c "import numpy;print(numpy.load('$CEN').reshape(-1).shape[0])")
M=$($PY -c "import numpy,hashlib;print(hashlib.md5(numpy.load('$CEN').tobytes()).hexdigest()[:8])")
mkdir -p $PLOG

say "20_judge: label=$name theta=$(basename $CEN) ($N floats, md5 $M) base=$BASE workers=$W bar=$BAR"
say "          tree=$TREE   (its policy.N_PARAMS is what can fly this theta)"

IDS_ENV=""
if [ -n "$SMOKE" ]; then
  name=${name}_smoke
  for spec in BAND250:$TREE/S/winjudge/band250_ids.txt \
              BAND2:$TREE/S/winjudge/band2_ids.txt \
              HIBAND:$TREE/S/winjudge/hiband_ids.txt \
              TOPLEG2:$TREE/S/topleg2/ids.txt \
              TOPLEG3:$TREE/S/topleg3/ids.txt; do
    k=${spec%%:*}; f=${spec#*:}
    head -$SMOKE "$f" > $PLOG/smoke_${k}.txt
    IDS_ENV="$IDS_ENV IDS_${k}=$PLOG/smoke_${k}.txt"
  done
  say "SMOKE=$SMOKE -- the first $SMOKE ids of EACH of the five legs ($((SMOKE*5)) boards),"
  say "  label $name, the full three-leg + POOLED511 reader chain, NOT bankable"
fi

run() {  # run <extra-label-suffix> <LEGS>
  local lbl=$name$1 legs=$2
  say "leg(s) [$legs] -> label $lbl"
  ( cd $TREE && env $IDS_ENV LEGS="$legs" WORKERS=$W BASE=$BASE bash S/winjudge/judge.sh "$lbl" "$CEN" ) \
      > $PLOG/${lbl}.judge.log 2>&1
  local rc=$?
  tail -20 $PLOG/${lbl}.judge.log
  [ $rc -eq 0 ] || say "WARN leg [$legs] rc=$rc (log $PLOG/${lbl}.judge.log)"
  return $rc
}

if [ -n "$LEGS_ONLY" ]; then
  say "LEGS_ONLY=[$LEGS_ONLY] -- ONE cell, not POOLED511.  A reduced cycle, not a ship read."
  run "_hi" "$LEGS_ONLY" || die "leg [$LEGS_ONLY] failed"
  echo; echo "================ $LEGS_ONLY ================"
  $PY $R/S/winjudge/report_hiband.py "${name}_hi" "$BASE" | tee $PLOG/${name}.hiband.txt
  $PY $R/S/pipeline/verdict.py $PLOG/${name}.hiband.txt --bar $BAR
  v=$?
  echo
  echo "NOT a POOLED511 read: 56 boards of ONE band.  Re-judge without LEGS_ONLY"
  echo "before anything is shipped [JOINTFREE2: flips do not pool off one leg]."
  echo "per-leg report:  $TREE/S/winjudge/logs/${name}_hi.report.log"
  next "drop LEGS_ONLY for the real 511-board read:  bash S/pipeline/20_judge.sh $name $CEN"
  exit $v
fi

run ""     "band250 topleg2 topleg3" || die "POOLED278 leg failed"
run "_b2"  "band2"                   || die "BAND2 leg failed"
run "_hi"  "hiband"                  || die "HIBAND leg failed"

echo; echo "================ HIBAND (the band we play now) ================"
$PY $R/S/winjudge/report_hiband.py "${name}_hi" "$BASE" | tee $PLOG/${name}.hiband.txt

echo; echo "================ POOLED511 (278 + 233, disjoint) ================"
$PY $R/S/winjudge/report_pool511.py "$name" "$BASE" "${name}_b2" "$BASE" \
    | tee $PLOG/${name}.pool511.txt

$PY $R/S/pipeline/verdict.py $PLOG/${name}.pool511.txt --bar $BAR
v=$?

echo
echo "per-leg reports:  $TREE/S/winjudge/logs/${name}.report.log"
echo "                  $PLOG/${name}.pool511.txt   $PLOG/${name}.hiband.txt"
echo "leg CSVs (shared across trees): $R/S/lossflip/${name}*_{band250,topleg2,topleg3,band2,hiband}.csv"
if [ -n "$SMOKE" ]; then
  echo
  echo "SMOKE READ -- $((SMOKE*5)) boards, NOT a verdict.  It proves the chain:"
  echo "  pad_theta -> $TREE -> five leg CSVs -> report_hiband + report_pool511 -> verdict."
  next "drop SMOKE= for the real 511-board read:  bash S/pipeline/20_judge.sh ${name%_smoke} $CEN"
elif [ $v -eq 0 ] && [ "$BAR" = ship ]; then
  next "bash S/pipeline/30_ship.sh $CEN $name      # build + smoke the tarball, then YOU upload"
else
  next "no ship.  Keep training, or promote for the next cycle:  BAR=promote bash S/pipeline/20_judge.sh $name $CEN"
fi
exit $v
