#!/bin/bash
# S/pipeline/_common.sh -- paths and rules every pipeline step shares.
# Sourced, never run.  Nothing here starts work.

R=/mnt/e/_work/kaggriculture3                       # master checkout (layout 7,692)
AF=$R/.claude/worktrees/alphafarm                   # REALES line   (layout 9,273)
PY=$R/.venv/bin/python
REMOTE=user@remote-host                         # remote training host
STAGE_CLONE=/home/user/stage_clone                 # CLONEES stage (default trainer)
STAGE_TAPE=/home/user/stage_head2                  # legacy tape-fitness stage
STAGE=${STAGE:-$STAGE_CLONE}
RPY=/home/user/kagg3/.venv/bin/python              # the remote interpreter
BEST=$R/S/pipeline/best                             # current best centre lives here
LEDGER=$R/S/pipeline/ledger.tsv
PLOG=$R/S/pipeline/logs

# LAW (do not "simplify" these away):
#   JAX_PLATFORMS=cpu           -- the local GPU is shared; probes never take it.
#   PYTHONPATH=<tree>/src       -- a REALES/judge run MUST import the tree whose
#                                  policy.N_PARAMS matches the theta it is flying.
#   BASE=ship7692               -- every judged arm is paired against the LIVE
#                                  package rows; a different base prices a
#                                  different switch (JUDGEBASE2 / WIDEPICK2).
#   WORKERS                     -- <= 2 local worker processes while another run
#                                  is in flight; the box has no spare cores.
#   never `kill $(pgrep -f X)`  -- that pattern matches the calling shell.  List
#                                  the PIDs, read them, then kill by number.
export JAX_PLATFORMS=cpu

# The ESR switch string the whole ledger is paired on.  Identical to
# S/winjudge/judge.sh's SW_BASE and S/melongenes/run_cell.sh's SW -- one string,
# three callers.  Gene-switch names in it sit at their SHIPPED default, so by
# plan._sw's precedence the candidate theta's GENE BLOCK rules (gene-block rule).
SW_ESR=OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True,brain.MELON_GENE_ON=True,brain.CROP_DAY_ON=True,ENDROUTE_ON=True,ENDROUTE2_ON=True,ENDROUTE2_SPLIT_ON=True,ENDROUTE_ROW2_ON=True,CLIP_CAP_ON=False,WIDE_PICK_ON=True,CARE_FILL_ON=True,OVERFLOW_GUARD_ON=True,OVERFLOW_GUARD_V2=True,OVERFLOW_GUARD_V3=True,LATE_EXEC_ON=True,ROUTE_VRP_ON=True,ROUTE_VRP_FIX_FROZEN=True,ROUTE_VRP_VERIFY=True,ROUTE_VRP_NEEDS_FIX_ON=True,ROUTE_VRP_REPAIR_ON=True

say()  { echo "[$(date -u +%H:%M:%SZ)] $*"; }
next() { echo; echo "NEXT: $*"; }
die()  { echo "FAIL: $*" >&2; exit 1; }

# tree_for <theta.npy>  -> prints the checkout whose N_PARAMS can fly it.
tree_for() {
  local n
  n=$($PY -c "import numpy,sys;print(numpy.load(sys.argv[1]).reshape(-1).shape[0])" "$1") || return 1
  if   [ "$n" -le 7692 ]; then echo "$R"
  elif [ "$n" -le 9273 ]; then echo "$AF"
  else echo "THETA IS $n LONG -- no checkout has that layout" >&2; return 1; fi
}
