# The win-first gate (`--real-gate-metric winfirst`)

Working note, 2026-09-10. Build agent, worktree `.claude/worktrees/drain-gene`
off `d4317f5` (leg20-gate trainer + drain-mix gene + shed fix).

## Why

The campaign promotes **WIN RATE FIRST**: the local judge moves the record when
the win count on the held-out live set rises with few drops and the margin is
not down. The gate's newest metric does not.

`--real-gate-metric leg20` accepts iff the paired coin delta over the
leg-family games is `> 0` **and** the all-games delta is `>= 0`. On 2026-09-10
flow168 refused a candidate that took the held-out live family from **98 wins
to 108** (+14 flips against -4 drops), because the family margin delta read
**-608 a game**. A margin-only rule can be the exact opposite of the rule the
record is kept on, and on that round it was.

(Set size, counted off the deployed script: `--real-gate-leg-family` lists
**56** tapes, all 56 seated in the 103-opponent field, so the family is 56
boards = 112 games of the round's 206. The brief for this change said 55/110;
nothing below depends on which, but the recipe's thresholds are quoted
against 56.)

Two things were wrong, not one:

1. **The wrong currency.** Coins are the price of a win, not the win.
2. **The wrong unit.** On a pinned town both seats replay the identical live
   game, so those "112 games" are **56 boards**. Every flip the log counts is
   counted twice, and so is every threshold set against it.

## Checkpoint log

- **T+0** Read `leg_family_delta`, `pinned_tally`, `paired_stats`,
  `RealGate.__init__` / `_decide_pinned` / `_leg20_verdict` / `_log_pinned` /
  `_start` / `state`, `scripts/train.py:setup_real_gate` and the argparse
  block; fetched the remote `~/launch_flow168.sh` read-only.
- **T+25** Code in `src/kagg3/es/train.py` and `scripts/train.py`; six tests
  appended to `tests/test_pinned_gate.py`.
- **T+40** Recipe and `docs/strategy/2026-09-10-launch_flow176.sh`. Direct
  check of `leg_family_delta` + `_winfirst_verdict` on hand-built rows
  (no subprocess): 2 family boards, 1 flip, family -4,000/game, all-games
  -2,667/game -> ACCEPT at slack 5,000, refuse at slack 0, refuse at
  min_flips 2.

## What was added

`--real-gate-metric winfirst`, sharing every piece of the `leg20` plumbing --
the same `--real-gate-leg-family`, the same pinned rows (nothing extra is
played), the same `real_gate.log`, the same `leg20_*` verdict keys and record
columns. New flag: `--real-gate-margin-slack COINS` (float, default `0.0`,
coins **per game**), refused under any other metric.

**The rule.** ACCEPT iff all three hold:

* **(a)** net family **BOARDS** (flips minus drops, seats grouped by
  `(seed, opponent)` and their margins summed within the board) `>=`
  `--real-gate-min-flips`. That flag is read again here, **in boards, not
  games** -- 56 live boards, not 112 rows. Both the once-banner and every
  decision line say so.
* **(b)** the family paired margin delta `>= -margin_slack` coins a game, so a
  win gain may spend a bounded amount of margin.
* **(c)** the all-games paired margin delta `>= -margin_slack` a game as well
  -- the same floor `leg20` puts under itself, so the family cannot be bought
  off the rest of the pinned set.

A round the statistic cannot be taken on -- no shared game, or a family tape
the round never played -- is **REFUSED**, exactly as under `leg20`.

The log line:

```
---   winfirst: family boards +14/-4 net +10 (min 6) | family delta -608/game | all-games delta +37/game | slack 800 -> ACCEPT
---   family flipped: 107056463 107067869 ...
---   family dropped: 107101394 ...
```

Re-centre, record, replicate and `best_abs` bookkeeping are untouched: this
changes only which rounds return `accepted`.

## Code

* `src/kagg3/es/train.py`
  * `leg_family_delta` -- now also returns `leg_boards`, `leg_flips`,
    `leg_drops`, `leg_flipped`, `leg_dropped`: the same family rows read as
    seat-grouped boards.
  * `RealGate.__init__` -- `margin_slack` parameter; the metric list gains
    `winfirst`; the pinned/family refusals now cover both family metrics; the
    slack is refused when negative and when any other metric is selected.
  * `RealGate.margin_slack_of`, `RealGate.state()["margin_slack"]`.
  * `RealGate._winfirst_verdict` (new), `_decide_pinned` (one
    `leg_family_delta` call, two rules over it), `_log_pinned` (the
    `winfirst:` line plus `family flipped`/`family dropped`), `_start` (the
    once-banner that names the BOARD unit).
* `scripts/train.py` -- `--real-gate-margin-slack`; `winfirst` in
  `--real-gate-metric`; `setup_real_gate` refusals (metric without pinned,
  metric without family, family tape not in the field, family without either
  metric, slack negative, slack without `winfirst`, slack without
  `--real-gate`); the startup banner and the resume note.

## Tests

`tests/test_pinned_gate.py`, appended (fake evaluator only -- no engine):

| test | what it pins |
| --- | --- |
| `test_winfirst_accepts_wins_that_cost_a_bounded_number_of_coins` | the flow168 case: +1 net board on a **-4,000/game** family delta accepted at `slack 5000`; the log line verbatim |
| `test_winfirst_refuses_too_few_boards_however_many_coins` | +10,000/game and no board turned round is a refusal at `min_flips 2` |
| `test_winfirst_refuses_a_margin_loss_past_the_slack` | 2 flips, -12,000/game, `slack 800` -> refuse |
| `test_winfirst_counts_one_board_not_two_seats` | `pinned_flips == 2` (rows) while `winfirst_flips == 1` (board) |
| `test_winfirst_needs_a_family_and_a_slack_it_may_read` | constructor refusals + `margin_slack` through `state()` |
| `test_winfirst_is_refused_on_the_command_line_without_a_family` | the six `setup_real_gate` refusals |

One existing assertion changed: the bad-metric message is now
`'win', 'margin', 'leg20' or 'winfirst'`.

## RECIPE -- launch_flow176 (do not launch from here)

`launch_flow176` is the remote's **deployed** `~/launch_flow168.sh` (fetched
read-only 2026-09-10, `ssh user@remote-host 'cat ~/launch_flow168.sh'`,
22,700 bytes -- note it is NOT the copy in
`docs/strategy/2026-09-09-launch_flow168.sh`, which predates the 56-tape
held-out family and the `flow166_g170` init) with **six** edits and nothing
else -- plus a rewritten header comment block (the flow168 one describes an
init and a stage this arm does not change). The finished script is committed
beside this note as `docs/strategy/2026-09-10-launch_flow176.sh`; its command
line is reproduced from a fresh fetch by:

```bash
ssh user@remote-host 'cat ~/launch_flow168.sh' > launch_flow176.sh
sed -i 's/--real-gate-metric leg20/--real-gate-metric winfirst/' launch_flow176.sh
sed -i 's/--real-gate-min-flips 3/--real-gate-min-flips 6 --real-gate-margin-slack 800/' launch_flow176.sh
sed -i 's/--run flow168/--run flow176/' launch_flow176.sh
sed -i 's/--seed 268 --lr/--seed 276 --lr/' launch_flow176.sh
sed -i 's/CUDA_VISIBLE_DEVICES=0 python/CUDA_VISIBLE_DEVICES=__GPU__ python/' launch_flow176.sh
sed -i 's#artifacts/flow168#artifacts/flow176#g' launch_flow176.sh
```

The gate line then reads:

```
--real-gate --real-gate-every 100 --real-gate-seed-base 20260904 \
--real-gate-metric winfirst \
--real-gate-leg-family 106947809,...,107160628      # the 56 held-out tapes, unchanged \
--real-gate-pinned artifacts/town_schedules.json --real-gate-pinned-seats 2 \
--real-gate-min-flips 6 --real-gate-margin-slack 800 \
--real-gate-recentre 3 --real-gate-workers 10 \
--real-gate-opponent <the same 103 packages>
```

**Why those numbers.** `--real-gate-min-flips 6` is six net **boards** of 56 --
under `leg20` the same flag was 3 and was not read at all; six is roughly half
the +10 net the refused flow168 candidate showed, so a candidate of that shape
passes and a one-board wobble does not. `--real-gate-margin-slack 800` is a
little above that candidate's -608 a game: the wins it bought are affordable,
a multi-thousand-coin collapse is not.

**Before launching (not done here):**

1. The remote is not a git repo. `rsync` this worktree's `src/ scripts/ tests/`
   over `~/stage_draingene` -- without the new code `scripts/train.py` refuses
   `--real-gate-metric winfirst` at argparse (the failure we want).
2. `sed -i "s/__GPU__/N/g" ~/launch_flow176.sh` for the free GPU, then
   `nohup bash ~/launch_flow176.sh &`.
3. First 200 generations: check `artifacts/flow176/real_gate.log` carries the
   `=== metric winfirst:` banner and that the `winfirst:` decision line's
   board count is about **half** the `FLIPS +n` on the line above it. If the
   two are equal, the seats are not being grouped and the run is judging on
   the wrong unit.

## Unverified

* Nothing was rsynced, launched, or run against the real engine; every test
  here uses the fake evaluator.
* `--real-gate-min-flips 6` and `--real-gate-margin-slack 800` are reasoned
  from the single flow168 round quoted above, not calibrated over arms the way
  `leg20` was (`docs/strategy/2026-09-09-judge-calibration.md`).
* The remote `~/launch_flow168.sh` may move again; the recipe is pinned to the
  22,700-byte fetch of 2026-09-10.
