# Resume checklist — machine restart requested by the user at 2026-09-11T12:33Z

## State at save
- **Remote (survives the restart; ssh user@remote-host, tree ~/stage_hr, NOT git):** GPU0 flow200 (python pid 950184, g67; records g10 judged = loss #1 vs B, g30 UNJUDGED — see step 2), GPU1 flow201 (pid 957416, g9; no record yet). Staged, not launched: ~/launch_flow202.sh (md5 ea732ba5, NEXT) > ~/launch_flow199.sh (fallback). Remote towns 538, tapes 538.
- **Local (dies with the restart):** flow198 arm (top-tier rotation, g160 seed, --abs-pairs 32) at g36, records g0/g10 (g10 judged = loss #1 vs B); judge_local.sh flow198; auto-judge watcher pid 80618 (ARMS flow200 + flow201, fixed flow2xx pattern); Kaggle watchers (56161192 B, 56143250 hr); manual judge `watch.sh --judge flow200 30 stage_hr` (pid 80741, mid-run); all Monitors; the /loop cron (:07/:30); the /goal hook.
- **Kaggle:** B (56161192, flow193_g100_hr adf27cb0) 58W-20L 2391 at g78, LIVE; hr (56143250, g1000_pair_hr 8274d577) 136W-57L 2580 = LB entry. Top-10 cutoff ~2943. Decision in force: B > A > hr on both ladder-replay studies (docs/strategy/2026-09-11-b-ladder-paired.md, -hr-ladder-paired.md) → next candidate REPLACES hr, B stays; falsifier: B rating ≥ hr by ~g200.
- **Judge:** promotion = beats candidate B on the five paired legs (TOPB2, LIVEC-H30, LIVEC-H30B, LIVE62, LOSS10 informational); base csvs S/lossflip/flow193_g100_hr_*.csv. Every arm's g10 record reads below B (seed noise). Losses vs B: flow200 1 (g10), flow201 0, flow198 1 (g10). Rule 4: third loss → launch flow202 on the freed GPU.
- **Everything durable:** S/ (git-excluded, on /mnt/e), docs/strategy/2026-09-10-verdicts.txt (= S/glut/verdicts.log), consensus §1-§40, build story, memory dir. /tmp scratchpad + task outputs are lost.

## Re-arm sequence (in order)
1. `cd /mnt/e/_work/kaggriculture3 && nohup setsid bash S/autojudge/watch.sh >> S/autojudge/watch.out 2>&1 &` — ARMS already flow200/flow201; the watcher only sees records printed AFTER it starts.
2. **Gap-judge (12:45Z NOTE: `--judge` fetches best_abs = the SEAT for stage_hr arms; instead `scp ~/stage_hr/artifacts/<arm>/cands/gNNNNN_record.npy artifacts/kagg2_games/thetas/<arm>_g<N>_hr.npy`, verify md5 vs cands/index.jsonl, then `watch.sh --legs <arm>_g<N>_hr <abs path>` detached)** every remote `cands/gNNNNN_record.npy` (flow200, flow201) that has no `AUTOJUDGE-vsB <arm>_g<N>_hr` line in S/glut/verdicts.log: first delete any INCOMPLETE csv in S/lossflip/<name>_*.csv (complete row counts: topb2 41, livech 61, livech2 61, live62 125, loss10 21), then `nohup setsid bash S/autojudge/watch.sh --judge <arm> <gen> stage_hr >> S/autojudge/legs_manual.out 2>&1 &` one at a time (they queue on /root/kagg3_judge.lock — never wrap in another flock). Start with flow200 g30 (its topb2 + livech csvs are complete and kept).
3. Kaggle watchers: `nohup bash S/kaggle/watch.sh 56161192 &` and `nohup bash S/kaggle/watch.sh 56143250 &` + a Monitor on each (they print KAGWATCH lines every 10 min; seen_*.txt dedups).
4. Local arm: `nohup setsid bash S/localarm/launch_flow198.sh >/dev/null 2>&1 &` (the block from S/flow198/swap_local.sh is copied below) — or, if flow198's g10 loss plus a second read argue against it, stage the next local arm. Then `nohup setsid bash S/localarm/judge_local.sh flow198 >/dev/null 2>&1 &`. Every local probe/agent exports JAX_PLATFORMS=cpu.
5. `/loop 60m <the campaign prompt>` (verbatim in memory session-handoff-2026-09-10.md; answer "This session only").
6. `python3 S/agents/finals.py` needs the new session's tasks dir path (edit T).
7. Rules in force: Opus for every subagent; never TaskOutput an agent task; no polling (Monitors / single bounded waits); before killing the watcher check `flock -n /root/kagg3_judge.lock true` AND its run.sh children; ssh launches hang the local client → kill the local ssh pid, verify by second ssh; kill by exact pid after reading /proc/<pid>/cmdline; never delete remote artifacts; only uploads need the user.

## flow198 launch block (from S/flow198/swap_local.sh)
```bash
log "flow194 reached gen=${gen:-?} exit_lines=${ex:-?}"
if [ "${ex:-0}" -lt 1 ]; then
  kill $PID && log "SIGTERM sent to $PID"
  for i in $(seq 1 30); do sleep 10; kill -0 $PID 2>/dev/null || { log "flow194 exited"; break; }; done
fi
tail -n 2 $LOG | cut -c1-120 >> $OUT
sleep 15
nohup setsid bash S/localarm/launch_flow198.sh >/dev/null 2>&1 &
sleep 5
nohup setsid bash S/localarm/judge_local.sh flow198 >/dev/null 2>&1 &
sleep 90
```
7. When the watcher is next restarted: `mv S/autojudge/watch.sh.next S/autojudge/watch.sh` first (fixes --judge for stage_hr arms; edited as a copy because bash reads the running script incrementally).
