#!/bin/bash
# 00_env.sh -- is this box able to run the loop?  Read-only, ~30 s.
#
#   usage: bash S/pipeline/00_env.sh
#
# Checks, in order: the venv; JAX_PLATFORMS; both checkouts and their layouts;
# ssh to the training host; the shipped package in dist/ against the hash
# tests/_pin.py pins; and whether master is clean.  Prints PASS/WARN/FAIL per
# line and exits non-zero only on a FAIL (a WARN is something you may choose to
# live with, e.g. a dirty tree during development).
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
bad=0
ok()   { echo "PASS  $*"; }
warn() { echo "WARN  $*"; }
no()   { echo "FAIL  $*"; bad=1; }

say "00_env: checking the box"

[ -x $PY ] && ok "venv     $PY" || no "venv     $PY missing"
[ "$JAX_PLATFORMS" = cpu ] && ok "jax      JAX_PLATFORMS=cpu (local GPU stays free)" \
                           || no "jax      JAX_PLATFORMS=$JAX_PLATFORMS -- must be cpu"

for t in "$R:7692" "$AF:9273"; do
  d=${t%:*}; want=${t#*:}
  got=$(PYTHONPATH=$d/src $PY -c "from kagg3.core import policy as P;print(P.N_PARAMS)" 2>/dev/null)
  [ "$got" = "$want" ] && ok "layout   $d N_PARAMS=$got" \
                       || no "layout   $d N_PARAMS=${got:-?} (expected $want)"
done

if timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 $REMOTE "test -d $STAGE" 2>/dev/null; then
  ok "remote   $REMOTE:$STAGE reachable"
  n=$(timeout 30 ssh -o BatchMode=yes $REMOTE "ps -eo args | grep -a 'S/reales/reales' | grep -cv grep" 2>/dev/null)
  echo "      remote REALES processes running: ${n:-?}   (11_train_status.sh reads them)"
else
  no "remote   $REMOTE:$STAGE not reachable -- 10_train_remote.sh cannot run (use 10b local)"
fi

# --- shipped package vs tests/_pin.py -----------------------------------------
PKG=$R/dist/submission_flow193_g100_hr_ft2_esr_wp_wpf.tar.gz     # sub 56335778
if [ -s "$PKG" ]; then
  m=$(md5sum "$PKG" | cut -c1-8)
  ok "package  $(basename $PKG) md5 $m"
else
  no "package  $PKG missing"
fi
if [ -s $R/tests/_pin.py ]; then
  ref=$(grep -aoE '^SHIPPED = "[0-9a-f]+"' $R/tests/_pin.py | grep -oE '[0-9a-f]{7,}')
  if git -C $R cat-file -e "${ref}^{commit}" 2>/dev/null; then
    ok "pin      tests/_pin.py SHIPPED = $ref ($(git -C $R log -1 --format=%s $ref | cut -c1-60))"
  else
    no "pin      tests/_pin.py SHIPPED = '${ref:-?}' does not resolve to a commit"
  fi
  echo "      tests/_pin.py SHIPPED is a GIT REF of the shipped planner, not an md5."
  echo "      It MOVES at every upload (30_ship.sh prints the edit).  It holds NO"
  echo "      test functions of its own, so pytest on it collects nothing -- check"
  echo "      the pin by running the NAMED files that import it:"
  echo "        JAX_PLATFORMS=cpu $PY -m pytest -q tests/test_widepick.py tests/test_geneswitch.py"
  echo "      (NEVER run the whole suite: \`pytest -q tests\` OOMs this box.)"
else
  no "pin      tests/_pin.py missing"
fi

# --- git ----------------------------------------------------------------------
b=$(git -C $R rev-parse --abbrev-ref HEAD)
[ "$b" = master ] && ok "git      on master $(git -C $R rev-parse --short HEAD)" \
                  || warn "git      on '$b', not master (master = latest upload + production code)"
if [ -z "$(git -C $R status --porcelain -uno)" ]; then ok "git      tracked tree clean"
else warn "git      tracked files modified:"; git -C $R status --porcelain -uno | head -8 | sed 's/^/      /'; fi

[ -s $BEST/centre.npy ] && ok "best     $BEST/centre.npy $($PY -c "import numpy;print(numpy.load('$BEST/centre.npy').shape[0])") floats" \
                        || warn "best     $BEST/centre.npy absent -- loop.sh will initialise it from centre9273.npy"

echo
[ $bad -eq 0 ] && say "00_env OK" || say "00_env has FAILs"
next "bash S/pipeline/loop.sh            # the unattended self-improvement loop"
echo "  or: bash S/pipeline/11_train_status.sh <run>   # read a run already in flight"
exit $bad
