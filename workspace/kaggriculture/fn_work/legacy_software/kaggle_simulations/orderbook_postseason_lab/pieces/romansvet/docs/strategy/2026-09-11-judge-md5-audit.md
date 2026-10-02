# Judge md5 audit — which theta bytes did each verdict actually judge?

2026-09-11, read-only audit (agent, 40-min box). Trigger: the 12:38Z defect note —
`S/autojudge/watch.sh --judge <arm> <gen> <stage>` calls `judge_one`, which fetches
`artifacts/<arm>/best_abs.npy`, NOT the saved `cands/gNNNNN_record.npy` that the automatic
RECORD path (`judge_record`) uses. For flow196/197/198/200/201 `best_abs.npy` is still
byte-identical to the seat (md5 `7fcf3948` = candidate B = `flow193_g100_hr.npy`, confirmed
`--init-theta artifacts/kagg2_games/thetas/flow193_g100.npy` in every remote launcher), so a
by-hand `--judge` on those arms would judge B against B.

## Verdict-by-verdict

"judged md5" = md5 of the local theta file the legs were pointed at, verified to have been
written BEFORE the leg csvs and never rewritten after (mtime proof below).
"truth md5" = the md5 recorded in the arm's `cands/index.jsonl` for that gen.

| arm | gen | verdict line (UTC) | judged md5 | truth md5 | class |
|---|---|---|---|---|---|
| flow194 (local) | g10 record | 02:48Z (AUTOJUDGE) | `f674a006` | `f674a006` g00010_record | CORRECT |
| flow194 (local) | g100 record | 05:25Z (AUTOJUDGE) | `e11df4a9` | `e11df4a9` g00100_record | CORRECT |
| flow196 | g10 record | 07:54Z | `36fa747f` | `36fa747f` g00010_record | CORRECT |
| flow196 | g60 record | 08:49Z | `ab444985` | `ab444985` g00060_record | CORRECT |
| flow196 | g100 **periodic, by hand** | 10:44:18Z | `618e90f9` | `618e90f9` g00100_periodic | CORRECT |
| flow197 | g10 record | 09:49:43Z | `4b6b88cf` | `4b6b88cf` g00010_record | CORRECT |
| flow197 | g100 **periodic, by hand** | 11:27:21Z | `ceb51bff` | `ceb51bff` g00100_periodic | CORRECT |
| flow197 | g140 record | 12:08:11Z | `d142c781` | `d142c781` g00140_record | CORRECT |
| flow198 (local) | g10 record | 12:22:02Z | `c78698a8` | `c78698a8` g00010_record | CORRECT |
| flow200 | g10 record | 11:50:31Z | `d943bac6` | `d943bac6` g00010_record | CORRECT |
| flow200 | g30 — **by-hand `--judge flow200 30`** | 12:22:02–12:32:08Z | `7fcf3948` (seat, fetched) | `13b7a6b0` g00030_record | **NO VERDICT** — guard fired |
| flow200 | g30 — re-judged from the scp'd cand via `--legs` | legs start 12:40:28Z (in flight) | `13b7a6b0` | `13b7a6b0` g00030_record | CORRECT (in flight) |
| flow201 | g0 | 12:19:48Z | — | — | SKIP (gen 0 = seat), no verdict |

No other judged names exist for these arms: `S/lossflip/` holds exactly the 11 names above.

## Why "judged md5" is the md5 the legs really ran on

1. **Provenance lines.** Every automatic verdict logs `fetched cands/gNNNNN_record.npy -> ... md5 <8>`
   (verdicts.txt lines 552, 578, 593, 666, 707, 721) — the `judge_record` path, never `best_abs`.
   The two local arms went through `S/localarm/judge_local.sh`, which `cp`s
   `artifacts/<arm>/cands/gNNNNN_record.npy` and logs the md5 (judge_local.log 02:39:31, 05:17:00,
   12:02:59) — it never touches `best_abs.npy`.
2. **Mtime ordering.** For all 11 names the theta `.npy` mtime precedes the first leg csv and
   follows none of them, so the file was not swapped under a running or finished leg:
   e.g. flow197_g140 theta 11:51:42 → legs 11:54:36…12:08:10; flow198_g10 theta 12:02:59 →
   legs 12:13:34…12:22:01. Current md5 == judged md5.
3. **Deterministic-output falsifier (independent of every log).** The legs are seed-pinned
   (`--seed-base`, `--seed-per-opponent`), so the same theta reproduces a csv to the byte. All
   12 `*_topb2.csv` and all 11 `*_live62.csv` for these names — including candidate B's own
   `flow193_g100_hr_*.csv` — have **distinct** md5s. A SEAT verdict would have produced a csv
   byte-identical to B's; a STALE one, identical to an earlier gen's. Neither occurs.
   The paired vsB lines agree: none is the all-zero, zero-flip line a B-vs-B run must give.

### One loose end, closed
The flow196 g100 periodic legs were launched by hand with the theta path
`/artifacts/kagg2_games/thetas/flow196_g100p_hr.npy` (root-relative; the leg logs show
`agent=/artifacts/...`). That path no longer exists, so those exact bytes cannot be re-hashed.
It is nevertheless CORRECT: `eval_vs_baselines.py` `np.load(theta_path)` raises on a missing
file and all four legs completed with full csvs (41/61/61/125 rows), so the file existed;
the campaign log at 10:35Z records "fetched g00100_periodic (md5 618e90f9)"; the repo copy
written one minute later is `618e90f9`, identical to the remote `cands/g00100_periodic.npy`;
and the csv-fingerprint test above rules out both B and every earlier flow196 record.
flow197's periodic run used the fully-qualified repo path and needs no such argument.

## What the defect actually did

The by-hand `--judge flow200 30` (pid 80741, started 12:22Z after the watcher restart collision
at 12:13Z) is the **only** invocation of the defective path against any of these arms. It behaved
as designed for a seat collision:

* `wait_for_record` polled `best_abs.npy` for 360 s, always `7fcf3948` → TIMEOUT 12:28:07Z;
* it then fetched `best_abs.npy` (the seat) **over** `thetas/flow200_g30_hr.npy`, destroying the
  correct g30 record theta `judge_record` had fetched at 12:08:12Z;
* the duplicate-md5 guard matched `S/autojudge/state_flow200.md5` (`7fcf3948 flow200_seat`),
  retried twice, logged `SKIP duplicate md5 ... NOT judged` at 12:32:08Z and `rm -f`'d the file.

So no B-vs-B leg ever ran; the cost was the deleted theta and ~10 minutes. The g30 read was then
done correctly by `scp cands/g00030_record.npy` + `watch.sh --legs <name> <path>` (theta written
12:39:37Z, `13b7a6b0`, legs from 12:40:28Z).

**The guard is the only thing standing between `--judge` and a seat verdict, and it holds only
while `state_<arm>.md5` still carries the seat.** After any `judge_one` the state file is
overwritten with whatever was last fetched, and a fresh arm has an empty state for a while
(`SEED flow200 no best_abs.npy and no seat md5` 10:48:16Z; `SEED flow201 ...` 12:12:17Z) — in that
window `--judge` would judge `best_abs` with no duplicate check at all. Treat `--judge` as unusable
for `stage_hr` arms; use scp of the cand + `--legs <name> <path>`.

## Conclusion

* **Verdicts that must be re-run: none.** Every recorded AUTOJUDGE / AUTOJUDGE-vsB / by-hand
  verdict for flow194, flow196, flow197, flow198, flow200 and flow201 judged the correct
  candidate bytes. There is no SEAT, STALE or UNKNOWN verdict in the set.
* **Rule 4 kills are unaffected.**
  * flow196 (killed at g172, 10:48Z): the three losses vs B rested on `36fa747f` (g10),
    `ab444985` (g60), `618e90f9` (g100 periodic) — all the arm's own candidates.
  * flow197 (killed at g140, 12:11Z): `4b6b88cf` (g10), `ceb51bff` (g100 periodic),
    `d142c781` (g140) — likewise.
  * flow198 loss #1 (`c78698a8`) and flow200 loss #1 (`d943bac6`) also stand.
* **Still open (not an md5 problem):** flow200 g30 (`~/stage_hr/artifacts/flow200/cands/g00030_record.npy`,
  `13b7a6b0`) was judging when this audit ran — its verdict is the arm's second read and is the only
  outstanding one. The 11:43Z hold-out-pattern defect (flow200_g10 first judged on the 72-board
  LIVEC22 set) was already found and re-run at 11:50Z on the same, correct theta.
