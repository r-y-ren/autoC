#!/bin/bash
# 10_train_remote.sh -- stage the REALES tree to the training host and launch a
# run exactly the way flow250_clone was launched [2026-09-19-reales5].
#
#   usage: [FITNESS=clone|tape] [GENS=120] [POP=4] [WORKERS=8] [SEED=1250] \
#          [DRYRUN=1] [SMOKE=1] [RESTAGE=1] \
#          bash S/pipeline/10_train_remote.sh <run_name> <centre.npy> [sigma] [floor]
#
#   sigma default 0.005, floor default 0.002  -- flow250's values.  The floor is
#   LAW-adjacent: flow245 was launched with NO --sigma-floor, took the 0.01
#   default, and spent seven generations unable to shrink further [realeswatch
#   §g15].  ALWAYS pass it explicitly.
#
#   DRYRUN=1   print the exact stage + launch lines and stop.  Nothing is copied.
#   SMOKE=1    run the reales5 1-BOARD PROBE in the FOREGROUND on the host
#              (--max-train 1 --gens 0, NO --assert-base) and stop.  ~20 s of
#              engine after the import.  This is the "does the staged tree still
#              play?" check; it writes into S/reales/<run>_smoke and touches no
#              live run.
#   RESTAGE=1  re-rsync even while a REALES run is alive on the host.  DEFAULT
#              IS NOT TO: the live run's workers re-import $STAGE/src on every
#              board, so replacing those bytes mid-run silently changes the
#              fitness it is measuring.  A stage is only refreshed when the box
#              is idle, or with this flag and your eyes open.
#
# FITNESS=clone  (THE DEFAULT) S/reales/reales_clone.py, branch alphafarm.
#               The LIVE V48 CLONE sits in the opponent seat and RE-PLANS, both
#               seats averaged into one board.  TRAIN = S/melongenes/hiband28_ids.txt
#               (28), HOLD = hiband28b_ids.txt (the other 28).  Launched with
#               --assert-base 89.3,6762,101271: g0 must reproduce the MELONGENES1
#               base to the coin or the episode is a different one and the run is
#               void.  Stage $STAGE_CLONE.
# FITNESS=tape  LEGACY, kept only because the whole flow243-248 ledger is on it:
#               S/reales/reales.py, the 56 HIBAND tapes as train and the 60 mined
#               loss-gate boards as hold-out.  CLONEES1 is the reason it is no
#               longer the default -- a TAPE-TRAINED HEAD READS -245/BOARD AGAINST
#               THE CLONE.  A tape cannot re-price or re-time, so the fitness it
#               maximises carries phantom denial.  Stage $STAGE_TAPE.
#
# THE CLONE STAGE IS SELF-CONTAINED [reales5].  It is NOT a copy of the whole
# checkout and it does NOT symlink the host's ~/kagg3/artifacts.  Three facts
# make it work and each one was paid for:
#   1. `reales_clone.py` reads $KAGG3_ART (falling back to its own ROOT), so the
#      opponent panel it opens is $STAGE/artifacts/..., not /mnt/e/... .  The
#      launch MUST export KAGG3_ART=$STAGE or the run dies on a Windows path.
#   2. The engine python is /home/user/kagg3/.venv/bin/python.  The system
#      python3 has jax+numpy but NO kaggle_environments.  That venv's
#      kaggriculture.py sha256 MATCHES vendor/engine.lock.json, so the host
#      plays the same game this box does -- and it is passed BOTH as the
#      interpreter and as `--python`, because the trainer shells out per board.
#   3. The 56 opponent dirs are SYMLINKS to one panel_nb/v48/main.py, recreated
#      on the host rather than copied (20 MB, and the host's disk sits at 99 %).
#      `town_inject`'s substring match still pins each board's town.
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
run=$1; CEN=$2; SIG=${3:-0.005}; FLOOR=${4:-0.002}
[ -n "$run" ] && [ -n "$CEN" ] || die "usage: bash S/pipeline/10_train_remote.sh <run_name> <centre.npy> [sigma] [floor]"
case "$CEN" in /*) ;; *) CEN=$R/$CEN ;; esac
[ -s "$CEN" ] || die "no centre at $CEN"
FITNESS=${FITNESS:-clone}; GENS=${GENS:-120}; POP=${POP:-4}; W=${WORKERS:-8}
SEED=${SEED:-1250}     # flow249=1249, flow250=1250; bump it for a second seat
case "$FITNESS" in
  clone) SCRIPT=S/reales/reales_clone.py; STAGE=$STAGE_CLONE
         GATE=$STAGE/S/melongenes/hiband28_ids.txt      # TRAIN, 28 boards
         HOLD=$STAGE/S/melongenes/hiband28b_ids.txt     # HOLD,  the other 28
         EXTRA="--seats 2 --win-bonus 2000 --assert-base 89.3,6762,101271 --python $RPY" ;;
  tape)  SCRIPT=S/reales/reales.py;       STAGE=$STAGE_TAPE
         # gate_ids_hi.txt (56, TRAIN) and gate_ids.txt (60, HOLD) are DISJOINT
         # by construction, and gate_ids.txt is byte-identical (md5 eb6f85b4...)
         # to the copy flow248 pointed at inside flow245's output directory.
         GATE=$STAGE/S/winrate/gate_ids_hi.txt
         HOLD=$STAGE/S/winrate/gate_ids.txt
         EXTRA="--seats 1" ;;
  *) die "FITNESS=$FITNESS -- clone (default) or tape (legacy)" ;;
esac

n=$($PY -c "import numpy;print(numpy.load('$CEN').reshape(-1).shape[0])")
[ "$n" = 9273 ] || die "centre is $n floats; the REALES line is 9,273 (pad with S/pipeline/loop.sh's init)"
say "10_train_remote: stage=$STAGE run=$run fitness=$FITNESS centre=$(basename $CEN) ($n floats) sigma=$SIG floor=$FLOOR gens=$GENS pop=$POP workers=$W seed=$SEED"

# ---- the launch, one string, printed and run verbatim ------------------------
ENVS="KAGG3_ART=$STAGE JAX_PLATFORMS=cpu CUDA_VISIBLE_DEVICES= PYTHONPATH=$STAGE/src"
ARGS="--run $run --centre $STAGE/S/pipeline/in_${run}.npy --coords mw2,mb2 \
 --gate-ids $GATE --hold-ids $HOLD --gens $GENS --pop $POP --sigma $SIG --sigma-floor $FLOOR \
 --sigma-halve-after 3 --accept-margin 0 --lr 0.05 --hold-every 5 --ckpt-every 5 \
 --seed $SEED --workers $W --seed-base 3300786901 $EXTRA"
LAUNCH="mkdir -p $STAGE/S/reales/$run && cd $STAGE && $ENVS nohup $RPY $SCRIPT $ARGS \
 > $STAGE/S/reales/$run/stdout.log 2>&1 &"

# The reales5 probe: ONE board, ZERO generations, and NO --assert-base (the base
# cell is a 28-board number; asserting it against one board would fail by
# construction).  It proves the staged tree, the engine python and the opponent
# symlinks, and it costs 2 games.
PROBE="cd $STAGE && $ENVS $RPY $SCRIPT --run ${run}_smoke --centre $STAGE/S/heades/centre9273.npy \
 --coords mw2,mb2 --gate-ids $GATE --hold-ids $HOLD --gens 0 --max-train 1 --workers 2 \
 --seats 2 --win-bonus 2000 --python $RPY --seed $SEED --seed-base 3300786901"

echo
echo "--- would stage (clone = the self-contained reales5 tree) ---"
echo "  ssh $REMOTE 'mkdir -p $STAGE/S/{reales,drainpin,melongenes,heades,pipeline} \\"
echo "                        $STAGE/S/winjudge/ship7692 $STAGE/artifacts/panel_nb/v48'"
echo "  rsync -a --delete $AF/src/ $REMOTE:$STAGE/src/        # the 9,273 tree"
echo "  rsync -a $AF/scripts/ $AF/pyproject.toml  $REMOTE:$STAGE/..."
echo "  rsync -a $AF/S/reales/reales_clone.py $AF/S/drainpin/ $AF/S/heades/centre9273.npy ..."
echo "  rsync -a S/melongenes/hiband28{,b}_ids.txt S/winjudge/{town_hiband.json,hiband_ids.txt,ship7692/} ..."
echo "  rsync -a artifacts/panel_nb/v48/ $REMOTE:$STAGE/artifacts/panel_nb/v48/"
echo "  ssh $REMOTE  # 56 opponent dirs recreated as SYMLINKS, never copied"
echo "  scp $CEN $REMOTE:$STAGE/S/pipeline/in_${run}.npy"
echo "--- would launch ---"
echo "  ssh $REMOTE '$LAUNCH'"
echo "--- 1-board probe (SMOKE=1) ---"
echo "  ssh $REMOTE '$PROBE'"
echo

if [ -n "$DRYRUN" ]; then
  say "DRYRUN=1 -- nothing staged, nothing launched"
  next "SMOKE=1 to probe the staged tree with one board, or re-run bare to start it"
  exit 0
fi

# ---- how busy is the host? ---------------------------------------------------
busy=$(timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 $REMOTE \
        "ps -eo args | grep -a 'S/reales/reales' | grep -cv grep") \
  || die "cannot reach $REMOTE"

if [ -n "$SMOKE" ]; then
  say "SMOKE=1 -- 1-board probe on the STAGED tree (no rsync, no nohup, ~20 s of engine)"
  timeout 600 ssh -o BatchMode=yes $REMOTE "$PROBE" 2>&1 | tail -12
  next "bare run to launch for real, or DRYRUN=1 to re-read the command"
  exit 0
fi

if [ "${busy:-0}" -ge 2 ]; then
  die "the host already runs $busy REALES processes -- two is the cap.  11_train_status.sh prints the PIDs."
fi

# ---- stage -------------------------------------------------------------------
if [ "${busy:-0}" -gt 0 ] && [ -z "$RESTAGE" ]; then
  say "NOT re-staging: $busy REALES run(s) alive on the host and their workers"
  say "re-import \$STAGE/src on every board.  Pass RESTAGE=1 to override."
elif [ "$FITNESS" = clone ]; then
  say "staging the self-contained clone tree -> $REMOTE:$STAGE"
  timeout 60 ssh -o BatchMode=yes $REMOTE \
    "mkdir -p $STAGE/S/reales $STAGE/S/drainpin $STAGE/S/melongenes $STAGE/S/heades \
              $STAGE/S/pipeline $STAGE/S/winjudge/ship7692 $STAGE/artifacts/panel_nb/v48" \
    || die "cannot prepare $REMOTE:$STAGE"
  rsync -a --delete "$AF/src/" $REMOTE:$STAGE/src/                       || die "rsync src failed"
  rsync -a "$AF/scripts/" $REMOTE:$STAGE/scripts/                        || die "rsync scripts failed"
  rsync -a "$AF/pyproject.toml" $REMOTE:$STAGE/                          || die "rsync pyproject failed"
  rsync -a "$AF/S/reales/reales_clone.py" $REMOTE:$STAGE/S/reales/       || die "rsync trainer failed"
  rsync -a "$AF/S/drainpin/" $REMOTE:$STAGE/S/drainpin/                  || die "rsync drainpin failed"
  rsync -a "$AF/S/heades/centre9273.npy" $REMOTE:$STAGE/S/heades/        || die "rsync centre failed"
  rsync -a "$R/S/melongenes/hiband28_ids.txt" "$R/S/melongenes/hiband28b_ids.txt" \
        $REMOTE:$STAGE/S/melongenes/                                     || die "rsync ids failed"
  rsync -a "$R/S/winjudge/town_hiband.json" "$R/S/winjudge/hiband_ids.txt" \
        $REMOTE:$STAGE/S/winjudge/                                       || die "rsync registry failed"
  rsync -a "$R/S/winjudge/ship7692/" $REMOTE:$STAGE/S/winjudge/ship7692/ || die "rsync ship rows failed"
  rsync -a "$R/artifacts/panel_nb/v48/" $REMOTE:$STAGE/artifacts/panel_nb/v48/ || die "rsync v48 failed"
  say "recreating the 56 opponent dirs as symlinks (never copied)"
  timeout 120 ssh -o BatchMode=yes $REMOTE "
    cd $STAGE/artifacts || exit 1
    while read -r id; do
      [ -n \"\$id\" ] || continue
      mkdir -p panel_v48_hiband/opponent_tape_\$id
      ln -sfn $STAGE/artifacts/panel_nb/v48/main.py panel_v48_hiband/opponent_tape_\$id/main.py
    done < $STAGE/S/winjudge/hiband_ids.txt
    ls panel_v48_hiband | wc -l" || die "symlink pass failed"
else
  say "staging the LEGACY tape tree -> $REMOTE:$STAGE (tapes stay on the host)"
  timeout 60 ssh -o BatchMode=yes $REMOTE \
    "mkdir -p $STAGE/S/pipeline && ln -sfn ~/kagg3/artifacts $STAGE/artifacts" \
    || die "cannot prepare $REMOTE:$STAGE"
  rsync -a --delete "$AF/src" "$AF/S" "$AF/scripts" "$AF/tests" $REMOTE:$STAGE/ || die "rsync failed"
fi

timeout 60 ssh -o BatchMode=yes $REMOTE "mkdir -p $STAGE/S/pipeline $STAGE/S/reales/$run" || die "mkdir failed"
scp -q "$CEN" $REMOTE:$STAGE/S/pipeline/in_${run}.npy || die "scp centre failed"
say "launching"
timeout 60 ssh -o BatchMode=yes $REMOTE "$LAUNCH" || die "launch failed"
sleep 5
timeout 60 ssh -o BatchMode=yes $REMOTE "ps -eo pid,args | grep -a -- '--run $run' | grep -v grep" | head -3

next "bash S/pipeline/11_train_status.sh $run     # log.tsv tail, hold column, centres, kill line"
echo "  a generation is ~14-16 min at pop 4 / workers 8; hold is read at g1 then every 5."
echo "  g0 must print '[clonees] BASE CHECK ... PASS' -- if it does not, the run is void."
