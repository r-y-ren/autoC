# The live pinned set: today's wins, not only today's losses (2026-09-09)

`S` = `/tmp/claude-0/-mnt-e--work-kaggriculture3/8b388b22-9a4b-4bf0-8e3e-dc4aac1d5f04/scratchpad`.
Source: Kaggle `ListEpisodes` for submission **56098262** (flow135_g350), pulled 2026-09-09,
saved at `S/livewin_eps.json`; per-episode split at `S/livewin/day.json`.

## 1. What the day looked like

181 episodes are listed for the submission (list re-pulled at the end of the pass), 180 with an
opponent seat, of which **72 were created on 2026-09-09 UTC**; the other 108 are 09-08. All 72 are
`COMPLETED`.

| | n | opp rating (median / range) | coin margin (median / range) |
|---|---|---|---|
| wins | **30** | 1986 / 1893–2126 | +7,322 / +21 … +40,025 |
| losses | **42** | 1993 / 1827–2070 | −6,976 / −166 … −22,234 |
| ties | 0 | | |

**41.7 % on the day** (30/72). The two pools are drawn from the *same* rating band — the median
opponent we beat (1986) and the median opponent who beat us (1993) are seven points apart, and the
margin distributions are near mirror images. Nothing about the opponent selects the outcome; the
board and the shop draw do.

## 2. Why the wins had to be cut

The promotion read (`S/loss20/run.sh`, doc `2026-09-09-loss20-leg.md`) was twenty pinned-town
tapes cut from **losses only**. That is a conditioned sample: every board in it is one the
champion already lost. Scoring a candidate theta there answers "can it rescue our worst boards",
which is a strict subset of "is it better on the live population", and it is the exact shape the
`counterfactuals-overstate` rule warns about — selection on the outcome makes any replayed
improvement look larger than it is, because the only direction a lost board can move is up.

Adding the wins closes the loop in both directions: a candidate that wins the losses by giving
back boards we already hold now pays for it in the same leg, which a loss-only set cannot see.
The set is also simply the day: 61 of 71 live boards, not 41 hand-picked ones.

## 3. What was cut

All **42 losses** are cut (drawn tape in `artifacts/tape_actions/` + `panel_opp/`, pinned-town tape
in `artifacts/tape_actions_town/` + `panel_opp_town/`, and a row in
`S/band2100p/town_schedules.json`); verified present for all 42. Forty-one were already cut before
this pass; the forty-second, **107160628** (15:00Z, lost 86,094–97,306 to *yuya* @1995), landed
during it and was cut by another worker — it is folded into the set here, not re-cut.

**20 of the 30 wins** were cut in this pass, chosen evenly spaced across the day's chronological
win list so the sample spans the whole opponent-rating range (1922–2063, median 1979) rather than
one block of hours. Ten wins were left uncut by the task's 20-per-pass cap:

    106952734  106972558  106982086  106992876  106999279
    107027538  107041306  107062150  107088001  107135005

`S/cutloss.sh` needed **no change** — no `cutwin.sh` was written. Its only outcome-dependent-looking step is
`tape_opponent.py --ours "OurTeam"`, and `resolve_seat()` resolves that to "the seat that is
not ours" — it never inspects rewards. The tape it cuts from a win is the opponent's seat, i.e.
the loser this time, and byte-exactness is verified by the same `verify()` replay of every recorded
action (each cut printed `verified` / `verified, town`). Package build, the town-schedule row and
the rsync/scp push to the remote are identical.

## 4. The set

`S/livewin/live_ids.txt` — every episode of 2026-09-09 that is now cut, in a **load-bearing**
order: the twenty `S/loss20/ids.txt` ids first and unchanged, then the remaining losses in
chronological order, then the wins. `--seed-per-opponent` draws `seed_base + SEED_STRIDE*(i+1)`
off the **list index** (`scripts/eval_vs_baselines.py:53-73`), so every id that keeps its position
keeps its seed and stays paired with the existing `S/lossflip/*_loss20.csv` rows. Never reorder,
never insert — only append.

The set is **62 tapes = 124 games** at both seats × 1 seed (`--seed-per-opponent`,
`seed-base 777001`), against 40 for the LOSS20 leg it supersedes — at the ~120-board target the
promotion read was aiming for, and now 62/72 = 86 % of the live day rather than a loss-conditioned
41/41.

Composition, in file order:

| lines | n | what |
|---|---|---|
| 1–20 | 20 | the `S/loss20/ids.txt` block, byte-identical and in place (seeds preserved) |
| 21–42 | 22 | the day's remaining losses, chronological |
| 43–62 | 20 | the wins cut in this pass, chronological |

No leg was run. Nothing here has been scored yet: the 42 loss boards keep the seeds their
`S/lossflip/*_loss20.csv` rows already used only for lines 1–20; lines 21–62 are fresh seeds with
no baseline csv, so the first champion run on this set is also its base.
