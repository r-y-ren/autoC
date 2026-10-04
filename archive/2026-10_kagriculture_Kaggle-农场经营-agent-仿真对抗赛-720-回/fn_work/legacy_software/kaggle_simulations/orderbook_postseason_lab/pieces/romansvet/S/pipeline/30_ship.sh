#!/bin/bash
# 30_ship.sh -- build the submission tarball, SMOKE it, and print the three
# manual steps (pin, BUILD-STORY, upload).  It never uploads anything.
#
#   usage: [OUT=<path>] [DRY=1] [TREE=<checkout>] bash S/pipeline/30_ship.sh <theta.npy> <label>
#
#   DRY=1  puts the tarball in a scratch dir instead of dist/ and prints the
#          pin edit / BUILD-STORY paragraph without writing either file.  (The
#          script never edited tests/_pin.py or BUILD-STORY.md anyway: DRY only
#          keeps dist/ clean, which is what makes a rehearsal safe.)
#
# ============================ THE LAYOUT LAW ================================
# THE TREE IS CHOSEN BY THE THETA'S LENGTH, AUTOMATICALLY.  The packager copies
# `main.py` + the in-tree `src/kagg3` + `theta.npy` out of ONE checkout, and
# that checkout has to be the one whose `policy.N_PARAMS` matches the theta:
#
#     <= 7,692 floats  ->  master           (the production/ship tree)
#      = 9,273 floats  ->  $AF, alphafarm   (master + the macro head)
#
# That is `tree_for` in `_common.sh`, the same router the judge uses, so a
# centre is packaged by the same rule it was judged by.  `TREE=<checkout>`
# still overrides it and says so loudly.  A 9,273 package is a LAYOUT MOVE and
# the checklist for one is printed below, not left to memory.
#
# THE MACRO HEAD IS NOT IN MASTER AT ALL.  `git grep -n mw2 src/` is EMPTY on
# master and hits `core/policy.py` + `core/brain.py` on the `alphafarm`
# worktree.  So the packaged 7,692 planner does not read the head; it has no
# code that could.  Consequences, in order:
#
#   * `S/reales/reales_clone.py` (the default REALES trainer) perturbs ONLY the
#     head: `coord_index()` runs from `PO.offset(<group>)` to the next group's
#     offset, and the four groups are mw1@7692 mb1@9036 mw2@9052 mb2@9260.
#     "Everything outside the mask -- including the rest of the head -- is held
#     at the centre."  The BODY (floats 0..7,691) is STRUCTURALLY FROZEN.
#   * The first 7,692 floats of a REALES centre ARE the package theta.  With
#     `--coords mw2,mb2` (221 coords, the line `loop.sh` drives) those 7,692
#     floats are the SHIPPED theta, byte for byte -- so packaging it from
#     master reproduces the CURRENT submission and ships NOTHING.  That is the
#     `head-only centre: nothing to ship` refusal below, and it is checked with
#     a real `cmp` against $SHIP_REF, not assumed.
#   * A REALES centre is therefore shippable in exactly two ways: (a) the
#     trainer moved the first 7,692 floats -- no current trainer does -- or
#     (b) the ALPHAFARM TREE ITSELF is packaged, layout 9,273, head included.
#     (b) is now the AUTOMATIC route for a 9,273 centre, and it is smoked:
#     `centre9273.npy` builds a 24-file archive whose planner reads the head
#     and which returns the SHIPPED COINS TO THE UNIT (184,456 / 129,457),
#     because that centre's mw2/mb2 are zero and `macro_delta` is then exactly
#     0.0.  alphafarm was merged onto master on 2026-09-19, so the 9,273 tree
#     is master's plan.py plus the head, not master-minus-two-commits.
#   * A centre whose body prefix is the shipped theta AND whose mw2/mb2 are all
#     zero is INERT through either route -- it plans the shipped day.  Master
#     refuses it outright; the 9,273 route refuses an upload of it and allows
#     DRY=1, because that build is the documented coin-exact self-test.
# ============================================================================
#
# Recipe, exactly as sub 56335778 (md5 9df145d9, 355,730 B, 24 files) was built:
#   .venv/bin/python scripts/package_submission.py --theta <theta> --out dist/<name>.tar.gz
#   bash S/widepickship/run_smoke.sh dist/<name>.tar.gz
# The smoke is NOT optional [FERTENGINE: "always smoke the tarball"]: it extracts
# the archive, cds inside it, scrubs PYTHONPATH so the repo is unreachable, and
# proves the packaged planner plays 720 steps with 0 bad status on two fixed
# seeds -- and that those two seeds return the SAME COINS as the in-tree planner.
. "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
TH=$1; name=$2
[ -n "$TH" ] && [ -n "$name" ] || die "usage: bash S/pipeline/30_ship.sh <theta.npy> <label>"
case "$TH" in /*) ;; *) TH=$R/$TH ;; esac
[ -s "$TH" ] || die "no theta at $TH"
SHIP_REF=${SHIP_REF:-$R/artifacts/kagg2_games/thetas/flow193_g100_hr.npy}
N=$($PY -c "import numpy;print(numpy.load('$TH').reshape(-1).shape[0])")
# THE ROUTE IS AUTOMATIC: the tree is the one whose layout can fly this theta.
# <= 7,692 -> master (production).  9,273 -> $AF (alphafarm, macro head).  Same
# router as the judge (`tree_for`), so a centre is packaged by the rule it was
# judged by.  TREE= still overrides, and an override that disagrees with the
# router is called out rather than silently obeyed.
AUTO_TREE=$(tree_for "$TH") || die "no checkout has this theta's layout"
TREE=${TREE:-$AUTO_TREE}
NP=$(PYTHONPATH=$TREE/src $PY -c "from kagg3.core import policy as P;print(P.N_PARAMS)")
MASTER_NP=$(PYTHONPATH=$R/src $PY -c "from kagg3.core import policy as P;print(P.N_PARAMS)")
if [ "$TREE" != "$AUTO_TREE" ]; then
  say "WARNING: TREE= overrides the router.  $N floats route to $AUTO_TREE; you asked for $TREE (layout $NP)."
fi
say "route: $N-float theta -> $(basename $TREE) tree (layout $NP)"

# ---- 0. the head-only refusal ------------------------------------------------
# A centre longer than master's 7,692 carries a macro head master cannot read.
# Its first 7,692 floats are the whole of what a 7,692 package would fly, so if
# the trainer left them at the shipped values there is, literally, nothing to
# ship.  `cmp` on the raw bytes -- not a tolerance, not a norm.
if [ "$N" -gt "$MASTER_NP" ]; then
  TMPD=$(mktemp -d); trap 'rm -rf "$TMPD"' EXIT
  $PY - "$TH" "$SHIP_REF" "$MASTER_NP" "$TMPD" <<'PYEOF' || die "could not cut the body prefix"
import sys, numpy as np
th, ref, np_, d = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
a = np.load(th).reshape(-1).astype(np.float32)[:np_]
b = np.load(ref).reshape(-1).astype(np.float32)
b = np.concatenate([b, np.zeros(np_ - b.shape[0], np.float32)]) if b.shape[0] < np_ else b[:np_]
a.tofile(d + "/body.bin"); b.tofile(d + "/ship.bin")
PYEOF
  if cmp -s "$TMPD/body.bin" "$TMPD/ship.bin"; then
    BODY_SAME=1
  fi
  # Is the head itself inert?  mw2 is the head's OUTPUT matrix and mb2 its bias,
  # so mw2 == 0 and mb2 == 0 means `macro_delta` returns exactly 0.0 whatever
  # mw1/mb1 hold -- the 9,273 planner then plans the 7,692 day.  Read through
  # the PACKAGING tree's own SHAPES offsets; master has no mw2 to ask about.
  HEAD_INERT=$(PYTHONPATH=$TREE/src $PY - "$TH" "$NP" "$MASTER_NP" <<'PYEOF'
import sys, numpy as np
th, np_, mnp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
a = np.load(th).reshape(-1).astype(np.float32)
if np_ <= mnp:
    print(1); raise SystemExit      # master cannot read a head at all
from kagg3.core import policy as P
sh = dict(P.SHAPES)
z = all(not np.any(a[P.offset(g):P.offset(g) + int(np.prod(sh[g]))]) for g in ("mw2", "mb2") if g in sh)
print(1 if z else 0)
PYEOF
)
  if [ "${BODY_SAME:-0}" = 1 ] && [ "$HEAD_INERT" = 1 ]; then
    MSG="INERT centre: nothing to ship.
  $TH is $N floats; its first $MASTER_NP are byte-identical to
  $SHIP_REF (cmp), and the head's mw2/mb2 are all zero, so macro_delta is
  exactly 0.0 and BOTH routes plan the live submission's day.  master cannot
  even read the head (git grep -n mw2 src/ is empty); alphafarm reads it and
  gets nothing.  Train the body, or train mw2/mb2 until they move."
    [ -n "${DRY:-}" ] && say "WARNING: $MSG
  DRY=1, so the build continues -- this is the documented coin-exact self-test
  (720/0 at 184,456 / 129,457).  It is a rehearsal, never an upload." || die "$MSG"
  elif [ "${BODY_SAME:-0}" = 1 ]; then
    say "body prefix is the SHIPPED theta, but the head MOVED (mw2/mb2 non-zero) -- the $N package is a LAYOUT MOVE carrying the head"
  else
    say "body prefix MOVED vs $(basename $SHIP_REF) -- a $N centre is a LAYOUT MOVE; packaging $TREE"
  fi
fi
# Only now: a theta longer than the PACKAGING tree's layout would be truncated.
[ "$N" -le "$NP" ] || die "theta is $N floats, $TREE's layout is $NP -- see the header; this is a MERGE, not a package.
  Drop the TREE= override and the router sends this centre to $AUTO_TREE."

if [ -n "${DRY:-}" ]; then
  OUT=${OUT:-${SCRATCH:-/tmp}/submission_${name}.tar.gz}
  case "$OUT" in $R/dist/*) die "DRY=1 refuses to write into dist/ -- set OUT to a scratch path" ;; esac
  say "DRY=1: dist/, tests/_pin.py and BUILD-STORY.md are NOT touched"
else
  OUT=${OUT:-$R/dist/submission_${name}.tar.gz}
fi
say "30_ship: theta=$(basename $TH) ($N of $NP floats) tree=$TREE -> $OUT"

# ---- 1. build ----------------------------------------------------------------
cd $TREE || exit 1
mkdir -p "$(dirname "$OUT")"
$PY scripts/package_submission.py --theta "$TH" --out "$OUT" || die "packaging failed"
MD5=$(md5sum "$OUT" | cut -d' ' -f1)
say "built $OUT  md5 $MD5  $(stat -c%s "$OUT") bytes  $(tar -tzf "$OUT" | wc -l) files"

# ---- 2. SMOKE (never skip) ---------------------------------------------------
say "smoking the tarball (extracted, cwd inside it, PYTHONPATH scrubbed)"
bash $R/S/widepickship/run_smoke.sh "$OUT" | tee $PLOG/${name}.smoke.log
grep -qE "720|0 bad" $PLOG/${name}.smoke.log || say "WARN: could not see '720 steps / 0 bad' in the smoke output -- READ IT before uploading"

# ---- 3a. the LAYOUT-MOVE checklist, printed only when the layout moves -------
# A 9,273 package is not a bigger 7,692 package.  Three things move together and
# a ship that moves one of them is a ship that fails the next test run.
if [ "$NP" -ne "$MASTER_NP" ]; then
cat <<EOF

================ LAYOUT MOVE -- $MASTER_NP -> $NP ==========================
This archive was built from $TREE, NOT master.  It carries
the MACRO HEAD, and the head is the reason the layout is $NP.  Three things
move together; do all three or none.

(L1) N_PARAMS.  The production layout becomes $NP.  master's
     src/kagg3/core/policy.py has no mw1/mb1/mw2/mb2 in SHAPES and
     \`git grep -ln mw2 -- src/\` on master is EMPTY, so shipping this means
     merging the alphafarm tree's policy.py + brain.py INTO master (the head,
     \`macro_delta\`, and the SHAPES entries) and making $NP the number every
     tool reads.  Until that merge, master cannot rebuild this package.

(L2) tests/_pin.py.  SHIPPED is a git ref of the shipped PLANNER TREE, and the
     shipped tree is now a $NP tree.  Commit the ship tree, set SHIPPED to that
     commit, append the '#:' paragraph, then run the named files (never the
     whole suite).  The pinned fixtures were cut on a $MASTER_NP planner: a head
     that is NOT inert changes plans, so expect to re-cut them and say so in the
     paragraph.  An inert head (mw2/mb2 zero) leaves every fixture alone.

(L3) The ES BASELINE.  Every centre in S/pipeline/best, every ledger row and
     every banked base CSV (BASE=ship7692) was measured against a $MASTER_NP
     package.  After this ship the base is the $NP package: re-bank ship rows
     under a NEW label and re-point BASE, or every later Δ is measured against
     a submission that is no longer live.  \`tree_for\` already routes judging;
     it is the BASE that does not move by itself.

============================================================================
EOF
fi

# ---- 3b. the manual steps ----------------------------------------------------
cat <<EOF

================ MANUAL STEPS -- nothing below is automated ================

(1) tests/_pin.py
    SHIPPED is a GIT REF of the shipped planner tree and it MOVES at every
    upload.  Commit the ship tree first, then edit the one line and append the
    '#:' paragraph the file keeps for each move:

        current:  $(grep -aoE '^SHIPPED = "[0-9a-f]+"' $R/tests/_pin.py)
        new:      SHIPPED = "<the ff commit of this ship tree>"

    tests/_pin.py has NO test functions of its own -- pytest on it collects
    nothing.  Check the pin through the NAMED files that import it (never the
    whole suite, it OOMs this box):

        JAX_PLATFORMS=cpu $PY -m pytest -q tests/test_widepick.py tests/test_geneswitch.py
        JAX_PLATFORMS=cpu $PY -m pytest -q tests/test_route_freefirst.py tests/test_unit_pickups.py \\
                                            tests/test_prestock_v2.py tests/test_submission_runs.py
    (last ship: 60 passed and 30 passed; tests/test_route_split.py has 2 known
     pre-existing failures.)

(2) docs/strategy/BUILD-STORY.md -- append at EVERY ship AND every reject.
    Paragraph template, fill the bracketed parts:

### BUILDSTORY<N> — UPLOAD <submission id> ($(date -u +%Y-%m-%d\ %H:%MZ))

\`dist/$(basename $OUT)\` (md5 ${MD5:0:8}, ship tree <commit>,
<the switch list / what changed>, layout $NP) uploaded by the user as submission
<id>, replacing <the retired id>.  Active slots: <id A> and <id B>.
Judged edge over the previous package: POOLED511 <dmargin> t <t>, Δtheirs <g>,
net flips <f>.  Smoke: 720 steps / 0 bad, seeds 20260821 <coins> / 7 <coins>,
identical to the in-tree planner.

    and one row in S/buildstory/index.tsv (same columns as the rows above it).

(3) UPLOAD -- yours, not this script's.  THE TWO-SLOT LAW:
    Kaggle keeps only the NEWEST TWO submissions active.  Uploading ONE retires
    the OLDER of the two -- which today is 56329775, our BEST agent at 2,858.
    So either upload TWICE BACK-TO-BACK (the new package into both slots, which
    retires the weak 2,316 agent and keeps a copy of the strong one), or HOLD
    until you have two packages worth the two slots.  Uploading once, casually,
    throws away the rating we have.

(4) AFTER the upload, record it in master with the existing recorder:

        bash S/ship/sync_master.sh <ship-commit> $OUT <kaggle-sub-id>

    It refuses unless the checkout is on master, verifies every kagg3/*.py in
    the tarball is byte-identical to src/kagg3 at the ship commit, ff/merges
    master to it, rewrites submission/ from the tarball and regenerates
    submission/UPLOAD.md.  (It hard-codes an old Co-Authored-By trailer; fix
    the trailer by hand if you care.)  master = the latest upload + production
    code, and this is what keeps that true.

NOTE ON REPRODUCIBILITY: the archive is deterministic (sorted entries, mtime 0,
uid/gid 0, compresslevel 9), so the same source tree and theta give the same
md5.  The converse bites: master HEAD already carries OFF/zero module defaults
that the shipped tree did not (HERD_TILT, TURN_COST, SELL_SPREAD_ON,
MELON_PLATE_TILES, ...).  They are behaviourally byte-identical but they are
DIFFERENT SOURCE BYTES, so a rebuild from HEAD will NOT reproduce md5 9df145d9.
To reproduce a past package exactly, build from \`git archive <ship commit> src\`.

============================================================================
EOF
next "after uploading: bash S/pipeline/40_livewatch.sh in a few hours (>= 40 games before you believe a rating)"
