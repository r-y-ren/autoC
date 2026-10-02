#!/bin/bash
# stage_check.sh [arm ...]   (default: eswork1 rlfast1)            READ-ONLY on local and remote.
# One row per training stage user@remote-host:~/stage_<arm>:
#   (a) tree md5 of stage src/kagg3 (*.py *.npy *.npz) vs local master src/kagg3 -> PASS / FAIL
#   (b) the 3 shipped parameter files on the stage vs live (esw = src eswork_theta.npy, th = theta7659 94a8ffd2,
#       hd = head_940 769ff15e); TREE shows FAIL/P or PASS/P when one differs
#   (c) running python PIDs whose cwd is inside the stage (+ multiprocessing worker count), with cmdline
#   (d) last line + age of the newest *.log under stage S/<arm> (or stage S/ when that dir is absent)
# Protocol: docs/TRAINING-PROTOCOL.md.  Never kills, never writes anything anywhere.
set -u
ROOT=/mnt/e/_work/kaggriculture3
R=${REMOTE:-user@remote-host}
[ $# -eq 0 ] && set -- eswork1 rlfast1
LOC=$(cd "$ROOT/src" && find kagg3 -name '*.py' -o -name '*.npy' -o -name '*.npz' | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-8)
p8() { md5sum "$1" | cut -c1-8; }
# live parameters: eswork_theta.npy lives in src; theta.npy + residual_head.npz are package-root files (submission/)
LP="esw $(p8 $ROOT/src/kagg3/core/eswork_theta.npy) th $(p8 $ROOT/submission/theta.npy) hd $(p8 $ROOT/submission/residual_head.npz)"
echo "$(date -u +%Y-%m-%dT%H:%MZ)  master $(git -C $ROOT rev-parse --short=8 HEAD)  local src/kagg3 tree $LOC  params: $LP"
printf '%-9s | %-6s | %-8s | %-36s | %s\n' STAGE TREE md5 "PARAMS esw/th/hd" "PIDS  ||  last log line"
for A in "$@"; do
  OUT=$(ssh -o BatchMode=yes -o ConnectTimeout=10 "$R" bash -s "$A" <<'REMOTE' 2>&1
A=$1; ST=$HOME/stage_$A
if [ ! -d "$ST/src/kagg3" ]; then echo "HASH missing"; else
  cd "$ST/src" && echo "HASH $(find kagg3 -name '*.py' -o -name '*.npy' -o -name '*.npz' | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-8)"
  q() { [ -f "$1" ] && md5sum "$1" | cut -c1-8 || echo none; }   # trainer copies of theta7659 / head_940 (eswork.py:221)
  echo "PARAMS esw $(q kagg3/core/eswork_theta.npy) th $(q $ST/S/winjudge/ship7692/theta7659.npy) hd $(q $ST/S/actionrl/flow257_ppo_selfplay/head_940.npz)"
fi
W=0
for p in /proc/[0-9]*; do
  c=$(readlink "$p/cwd" 2>&1); case "$c" in "$ST"|"$ST"/*) ;; *) continue ;; esac
  a=$(tr '\0' ' ' < "$p/cmdline" 2>&1); case "$a" in *python*) ;; *) continue ;; esac
  case "$a" in *multiprocessing*) W=$((W+1)); continue ;; esac
  echo "PID ${p#/proc/} $(echo "$a" | cut -c1-160)"
done
echo "WORKERS $W"
D=$ST/S/$A; [ -d "$D" ] || D=$ST/S
L=$(find "$D" -name '*.log' -printf '%T@ %p\n' 2>&1 | sort -n | tail -1)
if [ -n "$L" ]; then f=${L#* }; age=$(( ( $(date +%s) - ${L%%.*} ) / 60 ))
  echo "LOG ${f#$ST/} (${age} min ago): $(tail -1 "$f" | tr -d '\r' | cut -c1-200)"; else echo "LOG none"; fi
REMOTE
)
  H=$(echo "$OUT" | sed -n 's/^HASH //p'); V=FAIL; [ "$H" = "$LOC" ] && V=PASS
  P=$(echo "$OUT" | sed -n 's/^PARAMS //p'); [ "$P" = "$LP" ] || V="$V/P"   # /P = a parameter file differs from live
  N=$(echo "$OUT" | grep -c '^PID '); W=$(echo "$OUT" | sed -n 's/^WORKERS //p')
  printf '%-9s | %-6s | %-8s | %-36s | %s main procs + %s workers\n' "$A" "$V" "${H:-?}" "${P:-?}" "$N" "${W:-?}"
  echo "$OUT" | grep '^PID ' | sed 's/^/            /'
  echo "$OUT" | grep '^LOG ' | sed 's/^/            /'
  echo "$OUT" | grep -vE '^(HASH|PARAMS|PID|WORKERS|LOG) ' | sed 's/^/            ssh: /'
done
