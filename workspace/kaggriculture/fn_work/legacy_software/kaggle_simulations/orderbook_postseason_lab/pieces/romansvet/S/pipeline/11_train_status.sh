#!/bin/bash
# 11_train_status.sh -- read one REALES run, remote AND local, without touching it.
#
#   usage: bash S/pipeline/11_train_status.sh <run_name>
#
# Prints the log.tsv tail (the `hold_d` column is the ONLY column a judge leg is
# ever bought on -- train margin overfits, realeswatch §g10), the checkpoints
# available, and a LITERAL kill line with the PIDs filled in.
#
# NEVER `kill $(pgrep -f <run>)`: that expression matches the shell running it
# and the shell dies with exit 144.  This script prints the numbers; you read
# them and type `kill <n>` yourself.
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
run=$1
[ -n "$run" ] || die "usage: bash S/pipeline/11_train_status.sh <run_name>"

show() {  # show <where> <dir-listing-cmd> ...
  echo; echo "=== $1 ==="
}

# ---- remote ------------------------------------------------------------------
show "REMOTE $REMOTE:$STAGE/S/reales/$run"
timeout 90 ssh -o BatchMode=yes -o ConnectTimeout=10 $REMOTE "
  d=$STAGE/S/reales/$run
  if [ -d \$d ]; then
    echo '-- log.tsv (last 8) --'; tail -8 \$d/log.tsv 2>/dev/null || echo '(no log.tsv yet)'
    echo '-- hold column (gen<TAB>hold_d) --'
    awk -F'\t' 'NR==1{for(i=1;i<=NF;i++){if(\$i==\"gen\")g=i;if(\$i==\"hold_d\")h=i};next}
                h&&\$h!=\"nan\"{print \$g\"\t\"\$h}' \$d/log.tsv 2>/dev/null | tail -8
    echo '-- centres --'; ls -1 \$d/centre_*.npy 2>/dev/null | tail -6 || echo '(none yet)'
    echo '-- stdout tail --'; tail -3 \$d/stdout.log 2>/dev/null
  else echo '(no such run on the host)'; fi
  echo '-- PIDs --'; ps -eo pid,etime,args | grep -a -- '--run $run' | grep -v grep | cut -c1-120
" 2>&1

# ---- local -------------------------------------------------------------------
d=$AF/S/reales/$run
show "LOCAL $d"
if [ -d "$d" ]; then
  echo '-- log.tsv (last 8) --'; tail -8 "$d/log.tsv" 2>/dev/null || echo '(no log.tsv yet)'
  echo '-- hold column --'
  awk -F'\t' 'NR==1{for(i=1;i<=NF;i++){if($i=="gen")g=i;if($i=="hold_d")h=i};next}
              h&&$h!="nan"{print $g"\t"$h}' "$d/log.tsv" 2>/dev/null | tail -8
  echo '-- centres --'; ls -1 "$d"/centre_*.npy 2>/dev/null | tail -6 || echo '(none yet)'
else echo "(no such run locally)"; fi
# ONLY the python trainer itself.  A bare `--run <name>` match also catches the
# `ssh ... --run <name>` wrapper that LAUNCHED a REMOTE run from this box, and
# printing that pid under "TO KILL" invites you to kill your own session.
# The filter is on `comm` -- the process's OWN executable -- not on the command
# line, because a `bash -c` wrapper and an `ssh` both carry the whole launch
# string in their args and match any text grep looks for.
lfilter() { grep -a -- "--run $run" | grep -v grep | awk '$3 ~ /^[Pp]ython/'; }
echo '-- PIDs --'
ps -eo pid,etime,comm,args | lfilter | cut -c1-120

echo
echo "TO KILL (read the numbers, then type them -- never \`kill \$(pgrep -f ...)\`):"
lp=$(ps -eo pid,etime,comm,args | lfilter | awk '{print $1}' | tr '\n' ' ')
rp=$(timeout 60 ssh -o BatchMode=yes $REMOTE "ps -eo pid,comm,args | grep -a -- '--run $run' | grep -v grep | awk '\$2 ~ /^[Pp]ython/ {print \$1}'" 2>/dev/null | tr '\n' ' ')
[ -n "$lp" ] && echo "  local :  kill $lp"        || echo "  local :  (nothing running)"
[ -n "$rp" ] && echo "  remote:  ssh $REMOTE 'kill $rp'" || echo "  remote:  (nothing running)"

echo
echo "DECISION RULE (realeswatch): buy a judge leg only when hold_d > 0 AND the"
echo "centre actually moved.  A centre whose md5 equals the last judged one is"
echo "NOT a second measurement -- the engine is deterministic on a frozen centre."
next "bash S/pipeline/20_judge.sh <label> <that centre_gNN.npy>"
