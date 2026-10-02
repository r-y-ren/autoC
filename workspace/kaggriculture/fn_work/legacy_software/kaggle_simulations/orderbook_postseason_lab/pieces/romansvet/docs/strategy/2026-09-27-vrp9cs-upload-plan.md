# vrp9_cs upload plan (prepared 2026-09-27 03:40Z, before the upload)

Packages: (1) `dist/submission_res940_vrp10_esw.tar.gz` md5 73f4af9a (ESSHIP1, vrp8_jit + ESWORK g30 theta; at upload also move ESWORK1 base/centre to cand_g030 and the trainer strings gain nothing — the theta is loaded from the stage plan: set KAGG3_ESWORK_NPY in run_remote.sh/launch_ra1.sh/nvt BASE); (2) `dist/submission_res940_vrp9_cs.tar.gz` md5 cd94b3342dce0f238046901a896d8040 (528,299 B) = vrp8_jit tarball + `S/stackjit1/pkg.py`
(plan.py only: CARE_RIDE_ON = True, SLIVER_ON = True). Legs: STACKJIT1 + STACKJIT2 (FRESH600 +7) + LOSSLEG1 neutral + MC10TRACE1 noise.
Real-engine smoke row (STACKJIT1, LIVE250 board 0 vs reacting V56): 79,477 / 74,767.

## Finding while preparing the ship tree
No commit in the repo holds the uploaded plan.py (`git log --all --find-object` of the vrp8_jit tarball's plan.py: none; its
runtime.py comes from 50106310 SHIP_VRP8; residual_head.py is not on master at all). Master's src/kagg3/core/plan.py differs from
the vrp8_jit tarball by 839 code lines. Since ~vrp8 the packages have been built by patching the previous tarball (pkg.py chain), so
the "master = uploaded code" rule holds only for `submission/` payloads, not for src/. Reconciling src is a separate task (SRCSYNC1,
not started); the branch `ship_vrp9cs` (worktree /mnt/e/_work/kagg3_wt_ship_vrp9cs) sits at master untouched.

## After the user reports the sub id (<SUB>)
1. selfplay1 (main checkout): `src/kagg3/core/plan.py` `CARE_RIDE_ON = True` (l.~5051), `SLIVER_ON = True` (l.~7923); run
   `tests/test_care_ride.py tests/test_sliver1.py tests/test_route_vrp_opt.py tests/test_stackjit1.py` (whichever exist);
   commit "SHIP vrp9_cs config: CARE_RIDE_ON + SLIVER_ON = sub <SUB>"; then `tests/_pin.py` SHIPPED = that commit; commit.
2. master: in /mnt/e/_work/kagg3_wt_ship_vrp9cs `git switch master && git merge --no-edit selfplay1` (strip BUILD-STORY/index
   markers with the sed line if needed); `mkdir -p submission && tar -xzf dist/…vrp9_cs.tar.gz -C /tmp/x && cp /tmp/x/{theta.npy,main.py,engine.lock.json} submission/`,
   copy the tarball into submission/, write submission/UPLOAD.md (sub, date, md5, recipe), commit.
3. Trainer strings (docs/strategy/2026-09-26-esjudge1.md §1): append `,CARE_RIDE_ON=True,SLIVER_ON=True` to the switch string in
   `S/eswork1/run_remote.sh`, `S/rlfast1/launch_ra1.sh` (VRP8 var) and `S/nvtheta1/nvt.py` BASE_SW; rsync `src/` + those three files to
   ~/stage_eswork1, ~/stage_rlact1, ~/stage_nvtheta1, ~/stage_rlfast2; `bash S/eswork1/run_remote.sh verify` and
   `bash S/nvtheta1/run.sh verify` must print 79,477 / 74,767 for board 0 (the vrp9_cs drive2 row) — if they print the vrp8_jit row
   (79,744 / 74,625) the string did not land. Then kill each trainer chain by literal PID and resume from its latest state
   (lines in 2026-09-26-esjudge1.md §5 and 2026-09-27-essigma1.md; NVT: `run.sh es 40`).
4. `SYNC=1 bash S/lossbank1/pull_losses.sh`; update memory master-branch-rule (active = vrp8_jit + vrp9_cs, vrp7 retired FIFO) and
   MEMORY.md; `S/livewatch17/api.py eps <SUB>` at the next status.

## Executed 2026-09-27 08:05Z (both uploaded ~07:45Z: vrp9_cs = 56600958, vrp10_esw = 56600971)
- selfplay1 a4c5cc9e: plan.ESWORK_THETA = shipped kagg3/core/eswork_theta.npy (g30, md5 6928257a); CARE_RIDE_ON/SLIVER_ON stay False
  (master = the LATEST upload = vrp10_esw; vrp9_cs = this tree with the two switches True and ESWORK_THETA None). tests/conftest.py pins
  every test to the None graph; tests/test_ship_vrp10_esw.py checks the shipped default. Named tests 30/30 pass. Pin 6d50a62a.
- master: fast-forward + submission/ = vrp10_esw payload (kagg3/ tree, main.py, theta, head, engine.lock) + submission/vrp9_cs/ + both
  tarballs + UPLOAD.md. src drift (SRCSYNC1) still open: the tarball trees in submission/ are the authoritative uploaded code.
- Trainers (all 4 stages rsynced, killed by literal PID, relaunched once each; see memory feedback-training-till-win): ESWORK1 centre ->
  cand_g030 (best_held 1759, base = vrp8_jit, addlegs with the 50-seat loss leg then es 40); NVTHETA1 es 40 from g27; RLACT1 resume u93;
  RLFAST2 resume u190. Verify: NVT seat-1 row 80,763 / 75,640 = vrp10; ESWORK identity 80,909 / 75,586 = vrp8_jit base.
- Lossbank SYNC push done (loss leg 50 seats, 25 boards, xr 26).
