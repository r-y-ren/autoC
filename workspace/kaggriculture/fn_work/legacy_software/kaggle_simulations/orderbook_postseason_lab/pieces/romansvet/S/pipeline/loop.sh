#!/bin/bash
# loop.sh -- THE MAIN ENTRY.  Unattended self-improvement cycles: train from the
# current best centre, judge what the hold-out column recommends, promote it if
# it beats the soft bar, and STOP when it clears the ship bar so you can upload.
#
#   usage: [CYCLES=4] [GENS=15] [WHERE=remote|local] [FITNESS=clone|tape] \
#          [WORKERS=4] [CLONE=1] [SELF=1] [DRYRUN=1] bash S/pipeline/loop.sh
#
# THE FULL CYCLE (what you actually run overnight):
#   CYCLES=4 GENS=15 WHERE=remote FITNESS=clone WORKERS=4 bash S/pipeline/loop.sh
#
# THE REDUCED CYCLE (no training at all -- judge a centre that already exists,
# write the ledger row, exercise promote/ship).  This is the loop's own smoke
# test and it is what was run to verify the wiring on 2026-09-19:
#   CYCLES=1 JUDGE_ONLY=<centre.npy> LEGS_ONLY=hiband CLONE=0 SELF=0 \
#     WORKERS=2 bash S/pipeline/loop.sh
# JUDGE_ONLY skips steps 2-3 entirely: no launch, no wait, no checkpoint pick.
# LEGS_ONLY puts the bar on ONE cell (56 boards, ~15 min) instead of POOLED511
# (~90 min), so the row it banks is a PROMOTE-grade read and never a ship one.
#
# ONE CYCLE
#   1. best centre        S/pipeline/best/centre.npy, initialised on first run
#                         from the alphafarm REALES centre `S/heades/centre9273.npy`
#                         (the shipped 7,692 body + a zero 1,581-float macro head,
#                         i.e. byte-identical play to the shipped package).
#   2. train              GENS generations of REALES on the 221 `mw2,mb2` coords
#                         (10_train_remote.sh / 10b_train_local.sh).  Opponent
#                         panel = the 56 HIBAND pinned tapes; hold-out = the 60
#                         disjoint mined loss-gate boards.
#   3. pick               the newest checkpoint whose `hold_d` > 0 AND whose md5
#                         differs from the last judged centre.  No such centre =>
#                         NO JUDGE LEG IS SPENT and the cycle logs a skip.  A
#                         frozen centre re-reads its own numbers; that is not a
#                         second measurement [realeswatch §g10].
#   4. extra legs         CLONE=1 the live V48 clone (a rival that answers back),
#                         SELF=1 the previous best package seated live.  Neither
#                         is a bar; both are regression checks recorded in the
#                         ledger.
#   5. judge              20_judge.sh -> POOLED511 + HIBAND, paired vs `ship7692`.
#   6. promote            PROMOTE bar (Δtheirs <= 0, t >= 2, net flips >= 0) --
#                         soft, because a promoted centre is only the next
#                         cycle's starting point, not an upload.
#   7. ship-ready         SHIP bar (Δtheirs <= 0, t >= 3, net flips > 0).  On a
#                         pass the loop writes S/pipeline/SHIP-READY and STOPS.
#                         Uploading is the user's job -- 30_ship.sh builds and
#                         smokes the tarball, nothing here touches Kaggle.
#   8. ledger             one row per cycle in S/pipeline/ledger.tsv.
#
# COST.  A generation is ~14-16 min (pop 4, workers 8).  GENS=15 is ~4 h, then
# ~1.5 h of judge legs at WORKERS=4.  Budget ~6 h per cycle and run it overnight.
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
CYCLES=${CYCLES:-4}; GENS=${GENS:-15}; WHERE=${WHERE:-remote}
# clone, not tape: CLONEES1 measured a TAPE-TRAINED head at -245/board against
# the live clone, which is why 10_train_remote.sh defaults the same way.  These
# two defaults must agree or the loop trains one fitness and the manual claims
# another.
FITNESS=${FITNESS:-clone}; W=${WORKERS:-4}; CLONE=${CLONE:-1}; SELF=${SELF:-1}
mkdir -p $BEST $PLOG
if [ -n "$JUDGE_ONLY" ]; then
  case "$JUDGE_ONLY" in /*) ;; *) JUDGE_ONLY=$R/$JUDGE_ONLY ;; esac
  [ -s "$JUDGE_ONLY" ] || die "JUDGE_ONLY=$JUDGE_ONLY -- no such centre"
  CYCLES=1
  say "JUDGE-ONLY cycle: no training.  Centre $(basename $JUDGE_ONLY), legs [${LEGS_ONLY:-all}]"
fi

# ---- 0. the best centre ------------------------------------------------------
if [ ! -s $BEST/centre.npy ]; then
  src=$AF/S/heades/centre9273.npy
  [ -s $src ] || die "no $src -- the alphafarm worktree is missing"
  cp $src $BEST/centre.npy
  say "initialised $BEST/centre.npy from $src (9,273 floats; the 1,581-float macro"
  say "head is ZERO, so this centre plays exactly like the shipped package)"
fi
[ -s $BEST/judged.md5 ] || echo none > $BEST/judged.md5

say "loop: cycles=$CYCLES gens=$GENS where=$WHERE fitness=$FITNESS workers=$W clone=$CLONE self=$SELF"
say "best = $BEST/centre.npy md5 $($PY -c "import numpy,hashlib;print(hashlib.md5(numpy.load('$BEST/centre.npy').tobytes()).hexdigest()[:8])")"
[ -n "$DRYRUN" ] && { say "DRYRUN=1 -- printing the plan only"; }

for c in $(seq 1 $CYCLES); do
  run=loop_c$(printf %02d $c)_$(date -u +%m%d%H%M)
  echo; echo "================== CYCLE $c/$CYCLES  run=$run =================="

  # ---- 2. train --------------------------------------------------------------
  if [ -n "$JUDGE_ONLY" ]; then
    CEN=$JUDGE_ONLY; gen=n/a; hold=-
    md5=$($PY -c "import numpy,hashlib;print(hashlib.md5(numpy.load('$CEN').tobytes()).hexdigest()[:8])")
    say "judge-only: $CEN  md5 $md5 (no training, no hold read -- hold_d is '-')"
  else
  if [ "$WHERE" = remote ]; then
    FITNESS=$FITNESS GENS=$GENS WORKERS=8 DRYRUN=$DRYRUN \
      bash $R/S/pipeline/10_train_remote.sh $run $BEST/centre.npy 0.005 0.002 || die "launch failed"
    RDIR=$STAGE/S/reales/$run
  else
    FITNESS=$FITNESS GENS=$GENS WORKERS=8 DRYRUN=$DRYRUN \
      bash $R/S/pipeline/10b_train_local.sh $run $BEST/centre.npy 0.005 0.002 || die "launch failed"
    RDIR=$AF/S/reales/$run
  fi
  [ -n "$DRYRUN" ] && { say "DRYRUN: would now wait for $GENS gens, then judge"; continue; }

  # ---- wait for the run to reach GENS (or die) -------------------------------
  say "waiting for $run to reach gen $GENS (~$((GENS * 15)) min); checking every 10 min"
  while :; do
    sleep 600
    if [ "$WHERE" = remote ]; then
      g=$(timeout 60 ssh -o BatchMode=yes $REMOTE "tail -1 $RDIR/log.tsv 2>/dev/null | cut -f1")
      alive=$(timeout 60 ssh -o BatchMode=yes $REMOTE "ps -eo args | grep -a -- '--run $run' | grep -cv grep")
    else
      g=$(tail -1 $RDIR/log.tsv 2>/dev/null | cut -f1)
      alive=$(ps -eo args | grep -a -- "--run $run" | grep -cv grep)
    fi
    case "$g" in ''|gen) g=0 ;; esac
    say "  gen ${g:-0}/$GENS  alive=${alive:-0}"
    [ "${g:-0}" -ge "$GENS" ] 2>/dev/null && break
    [ "${alive:-0}" -eq 0 ] && { say "  the run is gone -- taking whatever it left"; break; }
  done

  # ---- 3. pick the centre ----------------------------------------------------
  if [ "$WHERE" = remote ]; then
    mkdir -p $PLOG/$run
    scp -q $REMOTE:$RDIR/log.tsv $PLOG/$run/log.tsv 2>/dev/null
    scp -q "$REMOTE:$RDIR/centre_g*.npy" $PLOG/$run/ 2>/dev/null
    LOG=$PLOG/$run/log.tsv; CDIR=$PLOG/$run
  else
    LOG=$RDIR/log.tsv; CDIR=$RDIR
  fi
  # newest gen with a POSITIVE hold read, rounded down to a --ckpt-every 5 gen
  pick=$($PY - "$LOG" <<'PY'
import sys
best = None
for ln in open(sys.argv[1]):
    f = ln.rstrip("\n").split("\t")
    if not f or f[0] == "gen":
        hdr = f
        continue
    try:
        g = int(f[0]); h = float(f[hdr.index("hold_d")])
    except (ValueError, IndexError):
        continue
    if h == h and h > 0:            # not nan, and positive
        best = (g, h)
print(f"{best[0]} {best[1]}" if best else "none 0")
PY
)
  gen=${pick% *}; hold=${pick#* }
  if [ "$gen" = none ]; then
    say "NO CENTRE WITH hold_d > 0 -- no judge leg spent this cycle [realeswatch]"
    $PY $R/S/pipeline/ledger.py $c $run $BEST/centre.npy $GENS "$hold" - - - - no no
    continue
  fi
  CEN=$CDIR/centre_g$(printf %02d $gen).npy
  [ -s "$CEN" ] || CEN=$CDIR/centre_final.npy
  [ -s "$CEN" ] || { say "hold was +$hold at gen $gen but no checkpoint exists -- skipping"; continue; }
  md5=$($PY -c "import numpy,hashlib;print(hashlib.md5(numpy.load('$CEN').tobytes()).hexdigest()[:8])")
  if [ "$md5" = "$(cat $BEST/judged.md5)" ]; then
    say "centre md5 $md5 is the one already judged -- the search did not move."
    say "A frozen centre reprints its own numbers; no leg spent."
    $PY $R/S/pipeline/ledger.py $c $run "$CEN" $GENS "$hold" - - - - no no
    continue
  fi
  say "picked gen $gen hold +$hold  $CEN  md5 $md5"
  fi

  # ---- 4. extra legs ---------------------------------------------------------
  CL=-; SL=-
  if [ "$CLONE" = 1 ]; then
    WORKERS=$W bash $R/S/pipeline/25_clone_leg.sh ${run} "$CEN" > $PLOG/$run.clone.txt 2>&1
    CL=$PLOG/$run.clone.txt; tail -4 $CL
  fi
  if [ "$SELF" = 1 ]; then
    PKG=${PKG:-$R/dist/submission_flow193_g100_hr_ft2_esr_wp_wpf.tar.gz} \
      WORKERS=$W bash $R/S/pipeline/26_selfplay_leg.sh ${run} "$CEN" > $PLOG/$run.self.txt 2>&1
    SL=$PLOG/$run.self.txt; tail -5 $SL
  fi

  # ---- 5/6/7. judge, promote, ship ------------------------------------------
  WORKERS=$W BAR=promote LEGS_ONLY="$LEGS_ONLY" bash $R/S/pipeline/20_judge.sh $run "$CEN"
  pv=$?
  echo "$md5" > $BEST/judged.md5
  POOL=$PLOG/${run}.pool511.txt
  if [ -s "$POOL" ]; then
    $PY $R/S/pipeline/verdict.py "$POOL" --bar ship
    sv=$?
  else
    # A LEGS_ONLY cycle has no 511-board table, and one cell is not a ship read
    # [JOINTFREE2].  SHIP-READY is not evaluated at all rather than evaluated
    # on 56 boards.
    say "no POOLED511 table (reduced cycle) -- the SHIP bar is NOT evaluated"
    POOL=-; sv=1
  fi

  prom=no
  if [ $pv -eq 0 ]; then
    cp "$CEN" $BEST/centre.npy; cp "$CEN" $BEST/centre_$md5.npy; prom=yes
    say "PROMOTED -> $BEST/centre.npy (md5 $md5); the next cycle starts here"
  else
    say "not promoted -- the next cycle restarts from the SAME best centre with a"
    say "fresh seed.  Two cycles with no promotion: shrink the step (sigma 0.002)"
    say "or change the fitness (FITNESS=clone)."
  fi

  ship=no
  if [ $sv -eq 0 ]; then
    ship=yes
    cp "$CEN" $R/S/pipeline/SHIP-READY.npy
    { echo "cycle $c  run $run  centre $CEN  md5 $md5  $(date -u)"; } > $R/S/pipeline/SHIP-READY
    say "*** SHIP BAR PASSED *** -> $R/S/pipeline/SHIP-READY"
  fi

  gcol=$GENS; [ -n "$JUDGE_ONLY" ] && gcol=0        # a judge-only cycle trained nothing
  $PY $R/S/pipeline/ledger.py $c $run "$CEN" "$gcol" "$hold" \
      "$POOL" $PLOG/${run}.hiband.txt "$CL" "$SL" $prom $ship

  if [ $sv -eq 0 ]; then
    echo
    say "STOPPING: a candidate clears the ship bar and an upload is a HUMAN step."
    # 30_ship.sh routes the tree off the theta's length, so the command is the
    # same either way -- but SAY which tree it will pick and what that costs,
    # because a 9,273 centre is a LAYOUT MOVE and not a packaging step.
    shipn=$($PY -c "import numpy;print(numpy.load('$R/S/pipeline/SHIP-READY.npy').reshape(-1).shape[0])")
    if [ "$shipn" -gt 7692 ]; then
      say "this centre is $shipn floats: 30_ship.sh routes it to the ALPHAFARM tree ($AF, layout 9,273)"
      say "  and prints the LAYOUT-MOVE checklist -- N_PARAMS, tests/_pin.py, the ES baseline all move together."
    else
      say "this centre is $shipn floats: 30_ship.sh routes it to MASTER (layout 7,692), an ordinary package."
    fi
    next "bash S/pipeline/30_ship.sh $R/S/pipeline/SHIP-READY.npy $run
      then UPLOAD TWICE back to back (the two-slot law), then 35_buildstory.sh, then edit tests/_pin.py"
    exit 0
  fi
done

echo
say "loop finished $CYCLES cycles with no ship-ready candidate."
column -t -s $'\t' $LEDGER 2>/dev/null | tail -8
next "bash S/pipeline/40_livewatch.sh      # has the ladder moved under us?"
echo "  then re-run with a different FITNESS (clone), or open a new knob: S/pipeline/50_new_switch.md"
