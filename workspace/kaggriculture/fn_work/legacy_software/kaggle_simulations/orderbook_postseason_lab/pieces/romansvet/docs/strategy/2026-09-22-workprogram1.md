# WORK_PROGRAM1 — funded service bundles falsified

Date: 2026-09-22. Verdict: **KILL / OFF**.

## Mechanism

`WORK_PROGRAM_ON=False` is the shipped default.  When enabled, the controller
exposes action 0 (incumbent) plus at most seven feasible bundles from the
current public board/book state.  A bundle contains 0--2 current-work hires,
one crop, 0--2 free tiles or existing-animal service, a cash reserve, and a
per-worker obligation assignment.  A planted tile is admitted only after
seed, PLANT, every WATER through its earliest sale day, HARVEST and deposit are
compiled; post-season, overlapping, unassigned, or unfunded chains are
rejected.  Hires are driven only by service due today, excluding FWDHIRE.

The planner applies the funded ask after the residual, preserves the reserve
through both derivations, adds at most two affordable hands, promotes complete
existing-service chains in admission/route order, and bypasses `HIRE_ROW` trim
only for an explicit programme hire.  Runtime owns one session per seat and
can replace only the unexecuted plan suffix.  Inputs are `DayView`/public tile
arrays and actual purse/inventory/book; no episode/seed IDs, tapes, or future
towns enter selection.

## Exact reacting-V56 development gate

The precommitted STRAW_SWAP1 selection supplies 100 boards, 50 per physical
seat, with the same seeds, towns and live V56 opponent.  Incumbent was 59 wins
(seat 0/1: 27/32).  Deltas are candidate minus paired incumbent.  `chains` is
the strict executed lifecycle count: PLANT, WATER on every day through the
tile's HARVEST; `hires` sums executed daily peak hands.

| preset | wins | b/c/net | mean Δours | mean Δtheirs | extra hires | extra chains | seat 0/1 wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| incumbent | 59 | 0/0/0 | 0.00 | 0.00 | 0 | 0 | 27/32 |
| existing service only | 2 | 0/57/−57 | −4,604.12 | +15,061.14 | −769 | +115 | 2/0 |
| cap 8 | 56 | 2/5/−3 | +431.85 | +1,050.73 | +163 | −1 | 24/32 |
| cap 16 | 56 | 2/5/−3 | +431.85 | +1,050.73 | +163 | −1 | 24/32 |
| cap 24 | 56 | 2/5/−3 | +431.85 | +1,050.73 | +163 | −1 | 24/32 |

The 8-hire cap never bound, so all three hire presets are exact identities.
They bought 163 more daily hands yet completed one fewer full planted service
chain and gifted V56 1,051 coins per board.  Existing-service priority did
more complete chains but displaced profitable production and gifted 15,061.
This is the same failure shape the gift bound and paid-hands kill were meant to
catch, not a learning failure.

An initial preset-1 diagnostic exposed an unintended `HIRE_ROW`-trim bypass
for zero-hire bundles; that run was discarded, the bypass was restricted to
explicit hires, and all reported rows were freshly rerun.  OFF parity then
matched `master` byte-for-byte on three pinned boards; the focused test file
passed.  No preset reached net +3 with Δtheirs ≤ 0, so held-out V56 and exact
LIVE302 were not opened and the switch remains OFF.

Artifacts: `S/actionrl/work_program1/{split.json,base_dev.csv,preset1_dev.csv,preset2_dev.csv,preset3_dev.csv,preset4_dev.csv,report.json}`.

(Code + tests live on branch workprog1, commit 74f45c7f; not merged.)
