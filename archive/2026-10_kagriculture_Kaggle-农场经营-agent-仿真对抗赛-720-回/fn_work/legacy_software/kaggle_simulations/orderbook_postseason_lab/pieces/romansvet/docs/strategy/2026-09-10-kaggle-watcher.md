# Kaggle live watcher (kagwatch) — 2026-09-10

Replaces the hard-coded session monitor `S/kaggle/watch_sub.py 56098262` (task `bm2gupwg0`)
with a submission-agnostic poller that can be pointed at the next upload the moment its id
is known, and that reports the number we actually care about: the post-ramp win rate against
opponents rated >= 1800, tested against the honest baseline.

`S` = `/tmp/claude-0/-mnt-e--work-kaggriculture3/8b388b22-9a4b-4bf0-8e3e-dc4aac1d5f04/scratchpad`

## Files

| file | role |
|---|---|
| `S/kagwatch/watch.sh <sub> [baseline=0.43] [--once\|--fg]` | launcher; detaches a 5-minute poller under `nohup` and prints its PID + log path |
| `S/kagwatch/watch.py` | the poller (stdlib only, no credentials) |
| `S/kagwatch/cutlosses.sh <sub> [max_eps=12]` | lists losses with no `artifacts/tape_actions_town/<ep>.npz` and prints the `S/cutloss.sh` command line for the newest ones — it never runs the cut |
| `S/kagwatch/<sub>.log` | every emitted line, append-only — **tail this from a session Monitor** |
| `S/kagwatch/<sub>.seen` / `<sub>.state` | reported episode ids / last announced rating (restart-safe) |
| `S/kagwatch/<sub>.out` | stdout+stderr mirror of the detached process |

## Starting it on a new submission

```bash
S=/tmp/claude-0/-mnt-e--work-kaggriculture3/8b388b22-9a4b-4bf0-8e3e-dc4aac1d5f04/scratchpad
$S/kagwatch/watch.sh <NEW_SUB_ID> 0.43          # detaches, prints PID + log path
# then, from the session:  Monitor  tail -F $S/kagwatch/<NEW_SUB_ID>.log
$S/kagwatch/watch.sh <NEW_SUB_ID> 0.43 --once   # one pass, foreground, no daemon
kill <PID>                                       # stop it
```

Options: `--ramp N` (games dropped as ramp, default 20), `--min-rating R` (default 1800),
`--interval S` (poll seconds, default 300).

## Output lines

```
WIN  ep 107179487 2026-09-09T16:23:30Z us 66841 vs 65730 Dresden (opp rating 1977)
LOSS ep 107182682 2026-09-09T16:35:35Z us 91093 vs 91221 KTAcosmo (opp rating 1872)
LB rating 1952.7
TALLY 56098262: 89-98 (47.6%) | post-ramp vs >=1800: 70-97 (41.9%) | rating 1952.7 | binomial p vs baseline 0.43: 0.8149
```

* one WIN/LOSS line per newly completed episode (a tie in coins counts as a non-win,
  matching `kaggle/watch_sub.py` and `drift/an.py`);
* a TALLY every 10th completed game (and one final TALLY under `--once`);
* an `LB rating <r>` line whenever the submission's own `updatedScore` moves >= 20 points
  (that score *is* its leaderboard rating; no second endpoint call is needed).

**post-ramp** = drop the first 20 games (the weak-opponent ramp) *and* every opponent rated
below 1800 by `initialScore`. The p-value is the exact two-sided binomial test of that
post-ramp record against the baseline, default 0.43 — the honest live baseline of
42.9 % vs >= 1800 from `docs/strategy/2026-09-09-field-drift.md`. A p well above 0.05 means
the new submission is **not yet distinguishable from the current agent**; that is the bar a
promotion has to clear, not the headline win rate, which the ramp inflates by ~6 points.

## Verification, 2026-09-09 19:55Z

`watch.sh 56098262 0.43 --once` on the live submission (187 settled games):

```
TALLY 56098262: 89-98 (47.6%) | post-ramp vs >=1800: 70-97 (41.9%) | rating 1952.7 | binomial p vs baseline 0.43: 0.8149
```

41.9 % post-ramp vs a 42.9 % baseline, p = 0.81 — the watcher reproduces the field-drift
number from an independent code path, which is the intended cross-check. Headline 47.6 %
minus post-ramp 41.9 % is the ramp+weak-opponent inflation, quantified.

Incremental behaviour was exercised by rewinding `.seen` by 24 games: 24 WIN/LOSS lines,
TALLYs at games 170 and 180, and one `LB rating 1952.7` line after a forced 1800 state.
Detached mode was started and killed against a dummy id; **no kagwatch process is left
running for 56098262** — the existing session monitor `bm2gupwg0` still covers it.

`cutlosses.sh 56098262` reports 98 losses, **0 uncut** (all already have town tapes).
On the previous submission `cutlosses.sh 56028553 4` reports 217 losses / 168 uncut and
prints `S/cutloss.sh 107113726 107136738 107150439 107175739`.

## Caveats

* The first run on a submission that already has games backfills `.seen` silently
  (one `START` line + one TALLY) so a mid-flight start does not dump hundreds of lines.
  A watcher started at upload time sees every game.
* A submission that Kaggle sidelines (active-submission limit) simply stops receiving
  episodes; the watcher goes quiet rather than reporting anything.
* Opponent rating is `initialScore` at the time of the game, so the >= 1800 filter is
  "who they were when we played them", not their current rating.
