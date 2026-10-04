# The auto-judge watcher (2026-09-09)

Every remote ACCEPT today was judged by hand — fetch `real_gate_pending.npy`, md5-check it
against the previous record, run the LIVE62 leg, read the LIVE55 rule line, run LOSS20 —
at **1–3 h of latency** per record. With 13 days left that latency is the bottleneck, not
the compute. `S/autojudge/watch.sh` removes it.

## What it does

A persistent detached watcher (`nohup setsid`, one process per arm) that

1. **tails** each running arm's `real_gate.log` over ssh —
   `ssh -o ConnectTimeout=20 -o ServerAliveInterval=60 -o BatchMode=yes user@remote-host "tail -n0 -F ~/<stage>/artifacts/<arm>/real_gate.log"` —
   reconnecting after 60 s if the link drops (logged);
2. **matches only the record line** the trainer prints per accepted generation,
   `--- gen N (record) pinned: … -> ACCEPT`, never the `---   leg20: … -> ACCEPT` detail
   line underneath it (that would fire twice). `gen 0` is the seated baseline the arm
   started from and is skipped;
3. **fetches** `~/<stage>/artifacts/<arm>/real_gate_pending.npy` to
   `artifacts/kagg2_games/thetas/<arm>_g<N>.npy`. If pending is absent it takes
   `best_abs.npy`, waits 60 s, and retries pending once; which source was used is recorded
   in the verdict line and in the state file;
4. **md5-verifies** the fetched theta differs from the previous record for that arm
   (`S/autojudge/state_<arm>.md5`). Byte-identical means the remote had not refreshed
   pending — the candidate is **skipped and logged**, never judged as new;
5. **picks the worktree by theta width** — `np.load(...).shape[0]`: 6789 → `arms-next`,
   7053 → `drain-gene` (both verified against `N_PARAMS` on 2026-09-09). An unknown width
   is a FAILED line, never a guess;
6. **runs the legs sequentially at `--workers 6`** (a runtime `sed` of the 8-worker
   originals, so upstream edits to the legs are picked up): LIVE62 (`S/live62/run.sh`),
   then the LIVE55 rule line (`S/live55/flips.py`, read off the csv LIVE62 wrote), then
   LOSS20 (`S/loss20/run.sh` + `S/loss20/flips.py`);
7. **logs** every line to `S/autojudge/verdicts.txt` with a UTC stamp, and one summary
   line to `S/glut/verdicts.log`:
   `<stamp> AUTOJUDGE <name>: LIVE55 <line> | LOSS20 <line>`.

**Never two candidates at once** (`flock` on `S/autojudge/judge.lock`; queued, not dropped),
**never a re-run** of a name that already has `S/lossflip/<name>_live62.csv`, and every step
is guarded with a `FAILED` line into `verdicts.txt`. The remote is read-only throughout:
`ssh tail` and `scp` fetches only.

## Operating it

```
nohup setsid bash S/autojudge/watch.sh >> S/autojudge/watch.out 2>&1 &   # PID in watch.pid
DRYRUN=1 bash watch.sh --replay <arm> <stage> <local real_gate.log>      # parser only
LEGSOFF=1 bash watch.sh --judge <arm> <gen> <stage>                      # fetch+md5+worktree only
bash watch.sh --judge <arm> <gen> <stage>                                # judge one gen by hand
```

**Adding an arm**: edit the `ARMS` list at the top (`"<arm-dir> <stage-dir>"`, one per line),
kill the PID in `S/autojudge/watch.pid`, relaunch. Adding a theta width: `worktree_for`.

## Verified 2026-09-09

* Parser replayed against the finished `flow166` log (1,354 lines, five record ACCEPTs):
  matched gens 0/50/80/150/170 and **none** of the five `leg20:` detail lines; gen 0 skipped
  as the baseline, gen 170 skipped because its live62 csv already exists, gens 50/80/150
  correctly queued for fetch.
* Fetch + md5 + worktree selection exercised live against both arms: flow172 pending →
  6789 params → `arms-next`; flow168 pending → 7053 params → `drain-gene`; a second fetch of
  the same file hit the duplicate-md5 skip. The probe thetas were deleted afterwards and the
  state files renamed to the real gen-0 records they hold.
* **Not yet exercised end to end**: no ACCEPT has fired since launch, so the leg-running
  half has not run under the watcher itself (the leg scripts are the same ones used by hand
  all day, and the `--workers 6` copies were syntax-checked).

## Stage 2: the drawn-leg veto (added 2026-09-09 17:40Z)

The watcher above only ran **stage 1** of the promotion rule — the pinned live read (LIVE62 →
the LIVE55 rule line) plus LOSS20 — and then stopped, so every RULE PASS still waited on a
hand-run of the six drawn legs. `watch.sh` now runs stage 2 itself, inside the same `flock`,
so one candidate at a time still owns the box, legs included.

**When it runs.** Only on a `LIVE55 … RULE PASS` line (matched on the `l55` string the LOSS20
step already reads). Anything else logs `VETO SKIPPED` with the line it saw. This is the
gate `S/judge/judge.sh` calls "gate2": the drawn legs are never the promoter, only the veto.

**What it runs.** `S/legs/legs.sh <name> <worktree> S/judge/<name>_legs` through a runtime
`sed` of `--workers 10` → `--workers 6`, exactly as the LIVE62/LOSS20 copies are made, so an
upstream edit of `legs.sh` is picked up. The six ALL rows it writes are copied into
`S/autojudge/verdicts.txt` as they land. **Legs are never re-run** for a name whose
`S/judge/<name>_legs/summary.txt` already contains `LEGSDONE`; that candidate is pooled from
the csvs on disk instead (the same guard shape as the `<name>_live62.csv` skip in stage 1).

**How the verdict is read.** Pooled `top10@777001 + today41@777001` **by board** — the two
seats of a `(seed, opponent)` board averaged into ONE observation, i.e. the statistic
`S/bank/paired.py` prints as `t` (`stats(rows, boards)`), never the inflated row-level
`t_rows`. 320 + 328 = 648 boards. Wins are counted per board the same way (board mean margin
> 0), and the contested win rate (`paired.contested`, tapes the base does not win on every
board) is pooled across both legs and logged beside it. The line appended to both
`S/autojudge/verdicts.txt` and `S/glut/verdicts.log`:

```
AUTOJUDGE <name> VETO: pooled <boards> d-margin <m> t <t> wins <b>-><c> contested <cw> -> CLEAR|VETO
```

**The rule.** `VETO` only when the pooled seat-grouped `t <= -2` — a significantly negative
drawn margin. A drawn **win-rate dip alone does not veto**
(`docs/strategy/2026-09-10-drawn-vs-pinned.md`): the drawn legs fold most open-loop tapes, so
the base already wins 8/8 on a large ceiling bucket where a candidate can only give margin
back. A `nan` t (no spread) reads CLEAR. A missing csv or an unparseable pool is a `FAILED
veto pool` line, never a silent CLEAR.

**Manual mode.** `bash watch.sh --veto <name> <worktree>` runs stage 2 alone for a candidate
whose stage 1 already passed (it takes the same lock); `DRYRUN=1 bash watch.sh --veto <name>
<worktree>` launches nothing and only pools whatever csvs are already in
`S/judge/<name>_legs`. Use it for any candidate judged by an older copy of the watcher.

### Verified 2026-09-09

* **Reproduces the hand read.** `DRYRUN=1 … --veto flow166_g170` on the existing
  `S/judge/flow166_g170_legs` printed
  `pooled 648 d-margin +355 t 0.57 wins 560->550 contested 81.4%->84.3% (40/472) -> CLEAR`
  — boards, margin, t and wins all identical to the hand-computed 2026-09-09 17:20Z line in
  `S/glut/verdicts.log`; the contested pair is new. Nothing was launched and the legs
  directory was not touched.
* The `LEGSDONE` guard and the DRYRUN "would run" path were both exercised (the latter on a
  name with no legs directory at all).
* Fixed while wiring it: `local name=$1 … O=$S/judge/${name}_legs` expands **all** words of
  `local` before any of its assignments take effect, so `O` came out as `judge/_legs`. `O` is
  now assigned on its own line.
* **Not yet exercised**: the non-DRYRUN paths — no leg has been launched by the watcher, and
  the `--veto` lock path was not run because the box's lock was busy with `flow172_g90`'s
  stage 1.
* **Caveat, 17:39Z**: three orphaned watcher generations from earlier restarts are still
  tailing (`97192/97193`, `2889/2890`, `3697/3698` and their `handle` children) — a restart
  that kills only the PID in `watch.pid` leaves its tail loops alive, which is why every
  ACCEPT is logged four times. They run the **pre-veto** code, and whichever generation wins
  the `flock` first is the one that judges; the others then hit the "already judged" skip and
  stage 2 never runs. Kill them (or use `--veto` by hand afterwards). This restart killed the
  whole 3992 tree — `3992 3995 3996 3999 4001 4000 4002` — but left its in-flight
  `flow172_g90` judge subshell (4843) running.

## 2026-09-11T11:43Z — arm-name pattern widened

The hold-out leg selector (`run_legs`) and `judged_already` matched `flow187*|flow188*|flow189*|flow19[0-9]*`. The first flow2xx record (flow200 g10) therefore got the 72-board LIVE-C leg and no vsB line. Both patterns now also match `flow2[0-9][0-9]*`. Any future arm family (flow3xx) needs the same edit — or replace the pattern with a numeric test on the arm index ≥ 187.

## 2026-09-11T12:13Z — restart while judging loses the record

The watcher tails `real_gate.log` with `tail -n0 -F`, so a record printed before a restart is never re-seen. Killing the process group mid-judge also kills its legs and leaves partial csvs (which `leg_done` may or may not treat as complete). Before restarting: `flock -n /root/kagg3_judge.lock true` and check for `run.sh` children in the watcher pgid; if busy, wait for the JUDGED line. After any restart, list remote `cands/` against local `AUTOJUDGE-vsB` lines and `--judge` the gaps by hand.
