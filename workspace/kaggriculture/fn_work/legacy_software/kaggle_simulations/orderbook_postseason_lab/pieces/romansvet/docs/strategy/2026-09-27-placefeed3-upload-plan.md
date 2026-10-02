# vrp12_pfs upload plan (PLACEFEED3, prepared 2026-09-27 14:25Z, NOT uploaded)

Package: `dist/submission_res940_vrp12_pfs.tar.gz` md5 **2532e456d049577c30cad256ad1a2e07** (531,777 B).
- Built FROM src by `scripts/package_submission.py` defaults (theta7659 94a8ffd2, head_940 769ff15e, eswork_theta g30 6928257a).
- Worktree /mnt/e/_work/kagg3_wt_placefeed3, branch `ship_vrp12_pfs`: switch commit dcacbd33, tests commit ee4c77ff.
- It sits on placefeed3 c2a3a938, which sits on placefeed1 f67fddc9.
- Evidence: docs/strategy/2026-09-27-placefeed3.md. Pooled 574 g, +32/−14 flips, Δours +63, Δtheirs −762 (t −9.5), every leg ≥ −1, faithful-59 +3.

**Supersedes vrp11_pf** (`dist/submission_res940_vrp11_pf.tar.gz` d3afb07e). vrp11_pf's PLACEFEED kills the day-0 OPEN_PUMP (faithful-59 −3). Do NOT upload it.

## Slot
Replaces **vrp9_cs 56600958**. vrp10_esw 56600971 stays. The final pair is vrp10_esw + vrp12_pfs.

## What changes vs vrp10_esw (56600971)
- `src/kagg3/core/plan.py`: `PLACEFEED_ON = True`, `PF_PUMPSAFE_ON = True`. Other PF knobs are neutral (NOBUY False, DAY 0..99, HERD 999).
- The tarball differs from the vrp10_esw tarball only in `kagg3/core/plan.py`.
- Effect:
  - Sheep and geese placed today get FEED + CARE tonight (first wool fire 6 not 5, first egg 4 not 3).
  - On day 0 the feed comes from the pump's 5 KEEP units, so the 53/48 pump fires exactly as shipped.

## Checks done
- Smoke: LIVE250 board 0 seats 0/1 vs reacting V56 are coin-exact and act-md5-exact with in-repo ON (80,898/74,586; 82,127/75,104). Worst turn 0.34 s.
- Tests: `tests/_pin.py`, `tests/test_placefeed.py` exit 0 on ship_vrp12_pfs.

## Upload steps (user)
1. Kaggle: submit `dist/submission_res940_vrp12_pfs.tar.gz` (check md5 2532e456 first). FIFO: vrp9_cs 56600958 must be the one displaced.
2. After the sub id <SUB> is known:
   - On ship_vrp12_pfs, re-key `SHIPPED_PACKAGES["vrp12_pfs"]` to <SUB>.
   - Merge ship_vrp12_pfs into selfplay1. It already holds the PF code OFF (ba6488b8), so only the two switch lines and the tests change.
   - Set `_pin.SHIPPED` to that merge commit and run `tests/_pin.py tests/test_placefeed.py tests/test_ship_vrp10_esw.py`.
3. master: fast-forward. `submission/` gets the vrp12_pfs payload, the tarball and an UPLOAD.md row (sub, date, md5 2532e456).
4. Trainers (train only on the latest shipped code):
   - Append `,PLACEFEED_ON=True,PF_PUMPSAFE_ON=True` to the switch strings in S/eswork1/run_remote.sh, S/rlfast1/launch_ra1.sh and S/nvtheta1/nvt.py BASE_SW, or rsync master src.
   - Re-verify the board 0 rows, then relaunch by literal PID.
5. Run `S/livewatch17/api.py eps <SUB>` at the next status and update memory master-branch-rule.

## Executed (SRCSYNC2, 2026-09-27)
- User uploaded `dist/submission_res940_vrp12_pfs.tar.gz` (md5 2532e456) as **sub 56612145** at ~15:10Z. vrp9_cs 56600958 is retired. The final pair is **vrp10_esw 56600971 + vrp12_pfs 56612145**.
- ship_vrp12_pfs (dcacbd33 + ee4c77ff) is merged into selfplay1. `diff -r` of the tarball's kagg3/ vs src/kagg3: 0 lines, except the src-only trainer code es/, sim/ and agent/opening.py (same as SRCSYNC1).
- `_pin.SHIPPED` = **dcacbd33**: the config commit, following the a4c5cc9e convention. Its src is identical to the merge. `SHIPPED_PACKAGES`: 56612145 is live, 56600971 is live, 56600958 has `retired: True`.
- `tests/test_package_defaults.py` now checks byte-equality against the vrp12_pfs tarball. Exit 0 for `_pin.py`, `test_package_defaults.py`, `test_placefeed.py` and `test_eswork.py`.
- `submission/` root holds the vrp12_pfs payload. `submission/vrp10_esw/` holds the vrp10_esw tree. UPLOAD.md has the new row. master is fast-forwarded to selfplay1.
- Trainers were NOT touched (step 4). Every stage must re-sync to the new master (docs/TRAINING-PROTOCOL.md §3). Until it does, `S/pipeline/stage_check.sh` reports TREE FAIL on plan.py.
