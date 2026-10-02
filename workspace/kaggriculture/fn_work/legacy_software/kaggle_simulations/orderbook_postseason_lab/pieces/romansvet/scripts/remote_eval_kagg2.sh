#!/usr/bin/env bash
# Track one run's best_abs.npy in the REAL engine against the two fixed
# yardsticks: the engine's `starter` agent and the previous submission
# (kaggriculture2/main.py, 150-170k coins a game).
#
# `scripts/eval_vs_baselines.py` seats a theta directly (`--theta`), so nothing
# has to be packaged: only a packaged *opponent* needs a file path, and kagg2
# already is one. Every seed is played in both seats, so seat bias cannot
# flatter the number.
#
# 24 seeds (48 games vs kagg2) per row, not 8: the margin's standard error is
# 14,182 coins a game, so 16 games resolve +-3,546 and the effects being chased
# are 5-14k. The per-game CSV is kept -- `scripts/paired_ci.py` compares two
# rows *paired*, which is another halving of the interval for free, and it
# cannot do that from a summary line.
#
# The seed base is unchanged and the draw is a prefix stream, so the 24 seeds
# open with the same 8 the 16-game rows used: a 48-game CSV and an 8-seed one
# still share 16 matched (seed, seat) games for `paired_ci.py`. 96 games (both
# opponents, both seats) measured 190 s wall at `--workers 3` on a 12-core
# CPU -- 2.6 % of the 2 h cadence per run, 5.3 % for the two the loop tracks.
#
# Usage: scripts/remote_eval_kagg2.sh artifacts/p2s0 [games] [workers]
# Env: PY (python), KAGG2 (opponent path), KAGG2_CSV_KEEP (CSVs to retain).
# Appends one line to artifacts/kagg2_track.tsv. Run from the repo root.
set -u -o pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

RUN_DIR="${1:?usage: remote_eval_kagg2.sh RUN_DIR [games] [workers]}"
GAMES="${2:-24}"
WORKERS="${3:-3}"
SEED_BASE=20260825
KAGG2="${KAGG2:-../kaggriculture2/main.py}"
PY="${PY:-$ROOT/.venv/bin/python}"
TRACK="$ROOT/artifacts/kagg2_track.tsv"
# One CSV is 5-6 kB (96 rows, no replay dump) and one row lands every 2 h per
# run. The cap bounds the directory at a few MB on a host whose root disk sits
# at 97 % full; 1,000 files is ~40 days of two runs, longer than any comparison
# anyone reaches back for.
CSV_DIR="$ROOT/artifacts/kagg2_games"
CSV_KEEP="${KAGG2_CSV_KEEP:-1000}"

RUN_DIR="${RUN_DIR%/}"
RUN="$(basename "$RUN_DIR")"
THETA="$RUN_DIR/best_abs.npy"

if [ ! -f "$THETA" ]; then
    echo "$(date -Is) $RUN: no $THETA yet, skipping" >&2
    exit 1
fi
if [ ! -f "$KAGG2" ]; then
    echo "$(date -Is) $RUN: no $KAGG2, skipping" >&2
    exit 1
fi

# The generation the weights come from: the last record in the run's log.
GEN="$(tail -n 1 "$RUN_DIR/log.jsonl" 2>/dev/null | grep -o '"gen": *[0-9]*' | grep -o '[0-9]*')"
GEN="${GEN:-unknown}"

# Kept, not scratch: every paired comparison between two rows reads it back.
# One row per game and no replay dump, so the file stays a few kB; a second row
# for a generation already measured overwrites it rather than accumulating.
mkdir -p "$CSV_DIR" || exit 1
CSV="$CSV_DIR/${RUN//[^A-Za-z0-9._-]/_}_${GEN//[^A-Za-z0-9._-]/_}.csv"

# The weights this row is about to describe. `best_abs.npy` is overwritten in
# place every time the run sets a new record, so an hour after the row lands
# there is no way back to the theta it measured -- which is what any later
# in-sim/real comparison needs. Copied here, next to the per-game CSV and keyed
# the same way, so the row, its games and its theta are one triple.
THETA_DIR="$CSV_DIR/thetas"
mkdir -p "$THETA_DIR" || exit 1
ARCHIVED="$THETA_DIR/${RUN//[^A-Za-z0-9._-]/_}_g${GEN//[^A-Za-z0-9._-]/_}.npy"
cp -f "$THETA" "$ARCHIVED"
# Evaluate the archived copy, not the live file: every worker `np.load`s the
# theta per game, and a live run that sets a new record mid-eval would
# otherwise have the later games measure a different theta from the earlier
# ones (seen 2026-08-28: flow9's starter games ran on one record, its kagg2
# games on the next, and the archived theta matched neither row).
THETA="$ARCHIVED"

SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

# `eval_vs_baselines.py` writes the CSV once, after the last game. Dropping any
# previous file for this generation first is what makes the `-s` test below
# mean "this eval produced it" rather than "some eval once did".
rm -f "$CSV"

nice -n 19 "$PY" scripts/eval_vs_baselines.py \
    --theta "$THETA" \
    --opponents starter "$KAGG2" \
    --games "$GAMES" --workers "$WORKERS" \
    --seed-base "$SEED_BASE" --csv "$CSV" > "$SCRATCH/out.txt" 2>&1
RC=$?
if [ $RC -ne 0 ] || [ ! -s "$CSV" ]; then
    echo "$(date -Is) $RUN: eval failed (rc=$RC)" >&2
    tail -n 20 "$SCRATCH/out.txt" >&2
    rm -f "$CSV"                    # a truncated CSV would be read back as data
    exit 1
fi

# The CSV carries mine/theirs per game but no win column; `kagg2_track_row.py`
# recomputes the win rate the way the eval script scores it (a tie counts a
# half) and adds the two intervals. It appends the row and echoes it.
SUMMARY="$("$PY" scripts/kagg2_track_row.py "$CSV" \
    --run "$RUN" --gen "$GEN" --kagg2 "$KAGG2" \
    --ts "$(date -Is)" --track "$TRACK")"
if [ -z "$SUMMARY" ]; then
    echo "$(date -Is) $RUN: could not summarise $CSV" >&2
    exit 1
fi
printf '%s\n' "$SUMMARY"

# Oldest-first prune, by mtime, of this directory only.
ls -1t "$CSV_DIR" 2>/dev/null | tail -n "+$((CSV_KEEP + 1))" | while read -r old; do
    rm -f "$CSV_DIR/$old"
done
