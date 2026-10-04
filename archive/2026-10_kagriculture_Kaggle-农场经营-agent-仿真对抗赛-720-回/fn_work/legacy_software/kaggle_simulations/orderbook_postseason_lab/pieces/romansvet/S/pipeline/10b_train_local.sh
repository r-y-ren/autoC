#!/bin/bash
# 10b_train_local.sh -- the same REALES run on THIS box instead of the host.
#
#   usage: [FITNESS=tape|clone] [GENS=120] [POP=4] [WORKERS=8] [DRYRUN=1] \
#          bash S/pipeline/10b_train_local.sh <run_name> <centre.npy> [sigma] [floor]
#
# Identical flags to 10_train_remote.sh; only the tree and the interpreter
# change (the alphafarm worktree, the repo venv).  WORKERS=8 is the documented
# local setting (flow246_loss ran at 8), but 8 local workers saturate the box:
# do NOT start this while a judge leg or a second trainer is running.  Outputs
# land in $AF/S/reales/<run>/{log.tsv,stdout.log,centre_gNN.npy,work/}.
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
run=$1; CEN=$2; SIG=${3:-0.005}; FLOOR=${4:-0.002}
[ -n "$run" ] && [ -n "$CEN" ] || die "usage: bash S/pipeline/10b_train_local.sh <run_name> <centre.npy> [sigma] [floor]"
case "$CEN" in /*) ;; *) CEN=$R/$CEN ;; esac
[ -s "$CEN" ] || die "no centre at $CEN"
FITNESS=${FITNESS:-clone}; GENS=${GENS:-120}; POP=${POP:-4}; W=${WORKERS:-8}
case "$FITNESS" in tape) SCRIPT=S/reales/reales.py ;; clone) SCRIPT=S/reales/reales_clone.py ;;
  *) die "FITNESS=$FITNESS -- tape or clone" ;; esac

n=$($PY -c "import numpy;print(numpy.load('$CEN').reshape(-1).shape[0])")
[ "$n" = 9273 ] || die "centre is $n floats; the REALES line is 9,273"

HOLD=$AF/S/winrate/gate_ids.txt   # the 60 mined loss-gate boards (== flow245's hold_ids.txt)
#: `--coords mw2,mb2` is the WHOLE line: 221 floats at 9,052..9,273, i.e. the
#: MACRO HEAD only.  `reales_clone.coord_index()` holds every other coordinate
#: at the centre, so floats 0..7,691 -- the entire package theta -- CANNOT move
#: in this run.  Whatever it produces is unshippable from master by
#: construction; see 30_ship.sh's header and PIPELINE.md §1.
CMD="$PY $SCRIPT --run $run --centre $CEN --coords mw2,mb2 --hold-ids $HOLD \
 --gens $GENS --pop $POP --sigma $SIG --sigma-floor $FLOOR --sigma-halve-after 3 \
 --accept-margin 0 --lr 0.05 --hold-every 5 --ckpt-every 5 --seed $RANDOM \
 --workers $W --seats 1 --seed-base 3300786901"
say "10b_train_local: run=$run fitness=$FITNESS centre=$(basename $CEN) sigma=$SIG floor=$FLOOR"
echo "--- would run, cwd $AF ---"; echo "  PYTHONPATH=$AF/src $CMD"; echo

# The cap is on RUNS, and it is checked AFTER the dry-run print: a DRYRUN starts
# nothing, so a busy box is no reason to refuse to show the line.
# The filter is on `comm` -- the process's OWN executable -- exactly as
# 11_train_status.sh's `lfilter`.  A bare args match on 'S/reales/reales' also
# catches the `bash -c` wrapper AND the `ssh ... reales_clone.py` that launched
# a REMOTE run from this box, so ONE live local trainer used to read as FOUR and
# this script refused every time.
busy=$(ps -eo comm,args | grep -a 'S/reales/reales' | grep -v grep | awk '$1 ~ /^[Pp]ython/' | wc -l)
[ -n "$DRYRUN" ] && { say "DRYRUN=1 -- nothing started ($busy local REALES trainer(s) live, cap 2)"; exit 0; }
[ "${busy:-0}" -ge 2 ] && die "$busy REALES trainers already run locally -- two is the cap"

mkdir -p $AF/S/reales
cd $AF || die "no $AF"
PYTHONPATH=$AF/src nohup $CMD >> $AF/S/reales/$run.nohup.log 2>&1 &
say "started pid $!"
next "bash S/pipeline/11_train_status.sh $run"
