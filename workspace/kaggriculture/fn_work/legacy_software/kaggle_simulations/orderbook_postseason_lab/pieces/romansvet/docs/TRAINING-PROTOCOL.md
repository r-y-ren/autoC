# TRAINING PROTOCOL (enforced, user laws 2026-09-27)

What is trained, on which code, how it is verified. One command answers all three:

```bash
bash /mnt/e/_work/kaggriculture3/S/pipeline/stage_check.sh            # STATUS (default: eswork1 rlfast1)
bash /mnt/e/_work/kaggriculture3/S/pipeline/stage_check.sh eswork1 rlfast1 nvtheta1 rlact1
```
Row = `STAGE | TREE PASS/FAIL | stage tree md5 | params esw/th/hd | running python PIDs + workers | last log line`.
TREE = md5 over `find kagg3 -name '*.py' -o -name '*.npy' -o -name '*.npz' | LC_ALL=C sort | xargs md5sum`
of `~/stage_<arm>/src` vs local master `src`. `/P` = a stage parameter file differs from live. Read-only.
A stage whose TREE is not PASS is **not training on master**: its output is not a candidate.

## 1. Laws

1. **master = the latest upload.** `src/kagg3` is byte-equal to the uploaded package tree (today, SRCSYNC2 09-27:
   vrp12_pfs, sub 56612145, tarball md5 2532e456, config commit dcacbd33 = `_pin.SHIPPED`). The second live slot is
   vrp10_esw (sub 56600971, md5 73f4af9a, tree `submission/vrp10_esw/`). It differs from master only in plan.py:
   `PLACEFEED_ON` and `PF_PUMPSAFE_ON` are False there. vrp9_cs 56600958 is retired.
2. **Every trainer runs on master src.** A stage on user@remote-host (`~/stage_<arm>`) is an rsync of
   master `src/` (wholesale, `--delete`) plus the arm's own `S/<arm>/` scripts. Nothing else is patched in.
3. **A trainer tunes ONLY a parameter file that exists in the shipped package:**
   - `kagg3/core/eswork_theta.npy` — ESWORK genes 0-5 (genes 6-9 are inert in shipped code and MUST stay 0);
   - `theta.npy` — planner theta, theta7659 md5 94a8ffd2 (package root; trainer copy `S/winjudge/ship7692/theta7659.npy`);
   - `residual_head.npz` — residual head, head_940 md5 769ff15e (package root; trainer copy
     `S/actionrl/flow257_ppo_selfplay/head_940.npz`).
   NEVER overwrite theta7659 / head_940; trained outputs get new names.
4. **Unshipped switches = dev branch, not a training arm.** Anything needing NONV_THETA, RL_ACT_*,
   RESIDUAL_N_RIVAL / RIVAL_FEAT_ON, CARE_RIDE, SLIVER, Q4_RELAY_*, ... runs on a dev branch until its code is
   committed to src AND shipped in a package. Its numbers are research, never a ship candidate.
5. **Continuous, never from scratch.** Runs go on till we win; flat = rollback, not kill. Every (re)launch
   resumes from the latest state file. Every upload re-syncs every stage (§3).
6. **Ship only via a package built FROM master src** (`scripts/package_submission.py`), never tarball+patch.
   Defaults = the shipped files [PKGFIX1]: bare `python scripts/package_submission.py --out <scratch>.tar.gz`
   = theta `submission/theta.npy` (94a8ffd2) + head `submission/residual_head.npz` (769ff15e) + src
   `eswork_theta.npy` (6928257a), every file byte-equal to the vrp10_esw tarball (tests/test_package_defaults.py).
   A new candidate overrides ONE file: `--theta <theta>` or `--residual <head.npz>`; `--no-residual` drops the head.
7. **Ship bar** (paired, two-purse rule; sim legs at SAFETY_S=1e9 + REPAIR_MS=1e7): dev100 net >= +1,
   held100 net >= +1, FRESH300 >= +3, tapes >= 0, faithful >= 0, delta-theirs t < 2. Tarball -> `dist/`.
   Uploads are the user's.

## 2. Arms

| ARM | parameter file it tunes | stage | script | resume state | fitness base (live pkg) | verify row (pinned game, seat 1) | ship path |
|---|---|---|---|---|---|---|---|
| **ESBAND1** = ESWORK1 run3 (ES, CPU, 2 procs; 09-27 15:18Z: chain bash 2576112/2576113, es python 2581391, workers 2581395 2581398; fitness = BAND 142 tape seats family-weighted (MELON .565) W_FLIP 1.5 + dev0-19 V56 guard; docs/strategy/2026-09-27-esband1.md) | `kagg3/core/eswork_theta.npy` genes 0-5 | `~/stage_esband1` (master 942b46cb, TREE PASS cdfc1618) | `S/esband1/run_remote.sh es 60` (`RUN=run3 PROCS=2`) | `S/esband1/run3/` state.json + centre.npy (centre = g30 = live) | vrp12_pfs = g30 + theta7659 + head_940 + PFS defaults (`run3/base.npz`) | `run_remote.sh verify`: 4 band seats (2 ZERO latched, MELON, V) = BANDLEG1 pfv1 IDENTICAL; esbase 142/142 identical | band net >= +1 gift-free -> `run3/cands/`, then STACKJIT legs, -> `src/kagg3/core/eswork_theta.npy`, package_submission.py, 5 legs |
| **ESBAND2** (ES, LOCAL CPU, cap 5 workers / 2 while floorhold1, nice 10; 09-27 17:50Z: chain bash 292793, es python 302149, workers 329898 329901 329902 (3, load cap; g1 ran 302511..302521); fitness = ESBAND1 band fitness (142 tape seats, MELON .565, W_FLIP 1.5) + dev0-19 guard; docs/strategy/2026-09-27-esband2.md) | theta7659 (`submission/theta.npy` 94a8ffd2, NEVER overwritten) 6,779 live NN floats, sigma 0.002; eswork g30 + head_940 frozen | local `S/esband2/stage/src` (git archive master 942b46cb, TREE cdfc1618 = master) | `S/esband2/run_local.sh es 60` (`PROCS=5`) | `S/esband2/run1/` state.json + centre.npy (centre = theta7659) | vrp12_pfs = theta7659 + g30 + head_940 + PFS defaults (`run1/base.npz`) | `run_local.sh verify`: 4 band seats (2 latched) = BANDLEG1 pfv1 IDENTICAL; esbase 142/142 identical | band net >= +2 -> `run1/cands/` (+ band table), then STACKJIT legs + reacting pool-kernel cross-check (tapes open-loop), new package via package_submission.py -> dist/ |
| ESWORK1 run2 (V56 legs) — STOPPED 09-27 15:20Z (literal PIDs 2563708 2563718 2563722 2563725), re-based as ESBAND1; state kept `~/stage_eswork1/S/eswork1/run2` gen 35 | `kagg3/core/eswork_theta.npy` genes 0-5 | `~/stage_eswork1` (vrp10 src, TREE FAIL) | `S/eswork1/run_remote.sh es 40` | `S/eswork1/run2/` | eswork_theta g30 (vrp10) | — | superseded by ESBAND1 |
| RLFAST2 (head PPO), TRAINFIX4 09-27 15:18Z re-based on master 942b46cb (tree cdfc1618, PASS), both from head_940 u0, fresh base gate: run2s GPU0 = CONTROL (no bank), wrapper bash 2575508, python 2575517, log `logs/rf2s_v12.log`; run3g1 GPU1 = band+loss bank `--xr S/bandbank1/xr_band.json` (136 rivals = 26 LOSSBANK1 + 110 POOL6-BAND, 1,088 extra games/update), wrapper bash 2575509, python 2575512, log `logs/rf3g1_band.log`; old runs -> `run2s_pre_trainfix4/`, `run3g1_xr_pre_trainfix4/` (docs/strategy/2026-09-27-trainfix4.md) | `residual_head.npz` (head_940 shape, shipped features only) | `~/stage_rlfast1` | `S/rlfast1/launch_rf2.sh --resume S/rlfast1/run2/heads/head_rf2_u{N}.npz --u0 {N}` | newest `S/rlfast1/run2/heads/head_rf2_u*.npz` | live package (theta7659 + g30 + head_940 anchor) | GAP: no verify script; head_940 in the harness must reproduce live 80763/75640 before any head counts | head -> package_submission.py --residual <head> from master src, 5 legs |
| NVTHETA1 | needs NONV_THETA (unshipped) | `~/stage_nvtheta1` | — | `S/nvtheta1/run2` | — | — | DEV BRANCH (being stopped) |
| RLACT1 | needs RL_ACT_* (unshipped) | `~/stage_rlact1` | — | `S/rlfast1/run3` | — | — | DEV BRANCH (being stopped) |

**SRCSYNC2 (09-27 ~15:10Z upload of vrp12_pfs 56612145):** master src moved. plan.py now has `PLACEFEED_ON = True` and
`PF_PUMPSAFE_ON = True`. Every stage in the table above still runs the vrp10_esw src until it is re-synced by the
§3 checklist (rsync master src wholesale, then re-verify the pinned row, then relaunch by literal PID). [ESBAND1 15:18Z: `~/stage_esband1` synced to 942b46cb, TREE PASS.] Until then
`S/pipeline/stage_check.sh` reports TREE FAIL for it, and its output is not a candidate. Remote not touched by SRCSYNC2. TRAINFIX4 (15:18Z): `~/stage_rlfast1` re-synced (PASS cdfc1618), both RLFAST arms relaunched; `~/stage_eswork1` / `~/stage_esband1` owned by the ES agent.

RLFAST2 caveat (SRCSYNC1): `ppo_fast.py` references RL_ACT_ON/OBS/N_FEAT and RESIDUAL_N_RIVAL/RIVAL_FEAT_ON,
none of which are in the live package. Until TRAINFIX2 makes it train a head on the shipped
`kagg3/core/residual_head.py` features only, and stage_check shows TREE PASS + the verify row matches, its
heads are research, not candidates.

## 3. Per-upload re-sync checklist (every stage, same firing as the upload)

1. Record each trainer's full cmdline: `ssh R 'tr "\0" " " < /proc/<PID>/cmdline'` (PIDs from stage_check).
2. **Kill literal PIDs only** (main + multiprocessing workers), never `pkill -f` / `kill $(pgrep -f ...)`;
   confirm with a second ssh (`stage_check.sh <arm>` shows `0 main procs + 0 workers`).
3. **rsync master src wholesale**: `rsync -a --delete /mnt/e/_work/kaggriculture3/src/ R:~/stage_<arm>/src/`
   (the `--delete` covers `kagg3/`), then the arm's own scripts `S/<arm>/*.py *.sh` (no src edits on the stage).
4. `bash S/pipeline/stage_check.sh <arm>` -> TREE `PASS`, params `esw <live> th 94a8ffd2 hd 769ff15e`.
5. Run the arm's verify row (§2); a mismatch stops the arm (the harness is not the live package).
6. If the upload shipped a trained parameter, move the arm's centre/anchor to it (e.g. ESWORK centre ->
   cand_g030 at the vrp10_esw upload) — keep the previous state as `*_pre_<label>` copies.
7. **Resume** from the latest state with the recorded cmdline (`setsid nohup ... &`), never from scratch.
8. `stage_check.sh` again: 1 main proc per arm, log line advancing. Note the rows in the upload's BUILD-STORY entry.

## 4. Rule for a new arm

A new arm must name, in its launch doc and its first log line, the **shipped parameter file it tunes**
(`eswork_theta.npy` genes 0-5 / `theta.npy` / `residual_head.npz`), its stage `~/stage_<arm>`, script,
resume state, fitness base (= live package) and verify row, and must pass `stage_check.sh <arm>` before its
first generation. If it needs any code or switch not in master src, it is a **dev branch**: it does not get a
stage slot as a training arm, and it becomes one only after its code is committed to src and shipped.
Then add it to the §2 table.
