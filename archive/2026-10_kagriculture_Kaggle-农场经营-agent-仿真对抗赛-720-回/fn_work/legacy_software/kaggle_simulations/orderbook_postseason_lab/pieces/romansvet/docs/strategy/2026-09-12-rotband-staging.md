# ROTBAND public-replay staging — 2026-09-12

## Result

The offline portion is complete under `S/rotband/`. The cached public leaderboard contains 769 rows in 2400–2950. After known episode, team-name, team-ID, own-submission, and judge exclusions, 566 teams remain. `team_pool.json` deterministically selects 180 unique teams, rating-stratified across 2947.6–2400.8. This exceeds the required 120, so a 120-tape window can change 30 tapes per rotation.

No network acquisition or replay cutting was run. Public replay use still requires the coordinator's rules confirmation. No production source, shared artifact registry, judge, consensus, log, or git state was changed.

## Leakage barrier

`build_exclusions.py` writes `exclusions.json` from local provenance. Its current result is 856 held episode IDs, 221 team names, and 126 team IDs. The explicit judge map contains 306 unique IDs: TOPB2 20, LIVE-C 102, LIVE62 62, NEXT30 primary plus extension 44, NEXTHIGH 30, and BAND40 primary plus extension 48. Some judge families overlap, hence the unique total.

NEXT30 is fully held out. It is absent from the team pool and is never added as an anchor. `verify_and_window.py` refuses any cut whose episode appears anywhere in the 856-ID exclusion set and asserts every emitted 120-ID window has zero overlap. Known provenance teams are avoided before episode lookup. The online picker also rejects games against our own submissions. Evaluation sets are neither copied nor pooled into this support set.

The private registry is `S/rotband/private_registry.json`; it contains only tape hashes and town lengths. Cuts live under `S/rotband/artifacts/`. Nothing is appended to `S/band2100p/town_schedules.json` or the shared artifact trees.

## Determinism and rotation

The input snapshot is `S/nexthigh/lb.json`, 8,265,426 bytes, sha256 `a14b5083eeb2806c669d358c1ee26d50dd223573056d43348f0fbd1d1fffcc0e`. Selection sorts by descending rating then team ID and takes 180 integer-spaced positions from the 566 eligible rows. `planned_windows.json` fixes six deterministic 120-team acquisition windows at stride 30; `windows.json` later maps verified episodes into executable tape windows. Current output hashes:

* `exclusions.json`: `a9042bb423fa277f9778b3f270fa592d08f643ab23c44b0f416badb75dc9ce53`
* `team_pool.json`: `941e390b500887a15736d637487a8e1b3fa418beeda79e3e8714123707d7a277`
* `planned_windows.json`: `0e8426cdc192f816fae6b5a8ef47d3efe65a006fd1585ed8bf4a6c9129549dce`

After at least 121 cuts verify, `verify_and_window.py` sorts them by rating, team ID, and episode ID. It emits circular 120-tape windows with stride 30. With 180 verified tapes, successive windows retain 90 and replace 30 tapes; six starts cover the pool before wrapping.

Directly changing the rung list on `--resume` is unsafe: resume restores the old ladder and appends newly supplied tapes rather than replacing the window. The separate rotation owner is responsible for a safe checkpoint converter. This data pipeline only emits immutable windows and makes no resume claim. The trainer's token-bucket scheduler can alternatively consume all 180 rungs over generations if the memory and episode layout permits it.

## Exact next steps after rules approval

Run from the repository root:

```bash
export JAX_PLATFORMS=cpu
.venv/bin/python S/rotband/build_exclusions.py
.venv/bin/python S/rotband/select_teams.py --pool 180
.venv/bin/python S/rotband/pick_episodes.py
.venv/bin/python S/rotband/download.py
bash S/rotband/cut_all.sh
.venv/bin/python S/rotband/verify_and_window.py --size 120 --stride 30
```

`download.py` and `cut_all.sh` cap concurrency at two workers. Before training, require: at least 121 verified tapes (target 180), `judge_overlap=0`, a stable private registry, all selected tape files present on the training host, and a launcher/precheck that resolves one chosen window or the full token-bucket pool without including NEXT30. The acquisition may return fewer episodes than teams because a team can lack a usable recent public win or narrow loss; if verified count is at most 120, refresh the public leaderboard and select a larger team pool rather than weakening exclusions.

## Files

`build_exclusions.py` and `exclusions.json` are the auditable leakage manifest. `select_teams.py` and `team_pool.json` are the completed offline selection. `pick_episodes.py`, `download.py`, `cut_one.sh`, and `cut_all.sh` are staged acquisition/cutting. `verify_and_window.py` is the final fidelity gate and deterministic window builder. `README.md` gives the short operator sequence.
