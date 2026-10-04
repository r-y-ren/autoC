# V10-R2 — frozen candidate in independent confirmation, not released

Continuation workspace: `research/v10_rebuild_20260926/continuation/`.
Original root V9, `submissions/release_v9` and `submissions/release_v10` are immutable.
The previous checkpoint is preserved in `continuation/previous_handoff.md`.

## Current frozen selection
Source: `continuation/generation5/advance36.py` (relative to rebuild workspace).
SHA-256: `e03333c6bef0c83764d56f1cc958782f032c5bbdc0684bae1cc2ccd6b61f3e7c`.
Entrypoint: `r2_opening_agent`.
Changes: net-five wheat opening; observed-stock threshold 4; own sale reservations
24 turns; conditional sale-advance window 36 turns. No opponent identities/test seeds.
Selection and development evidence: `continuation/selection.json`.

## Completed continuation development
Generation 4: 1280/1280 valid full games. Extended development: 768/768 valid.
Generation 5: 896/896 valid. Chosen candidate: public panel 128 wins/128;
hard counter population 63 wins, 18 ties, 15 losses/96. Keep these panels separate.
Longer-window and reserve crossovers were rejected after actual games.
Earlier rebuild data and failed prototypes remain unchanged.

## Active finite batches — verify before resuming
Confirmation PID 54228: `continuation/confirmation_jobs.json` ->
`continuation/confirmation_results.jsonl`, 1920 full jobs, 8 workers.
Actual archive validation PID 8112: root `build_release_round8.py` generic profile,
stage `submissions/candidate_v10_r2`; log `continuation/technical_build.log`.
Remote REPL PID 60924 holds Popen handles, but use ledgers if session is lost.
Imports can take minutes before the first result; do not duplicate active processes.

## Finish without contaminating confirmation
Read `continuation/CONFIRMATION_PROTOCOL.md`. Six actual public programs and 48
unseen worlds, both seats, candidate/V9/V10. Marketshock and Structured were unused
in development. No score can be inferred from their names or notebook titles.
Do not tune the frozen source on these confirmation outcomes.
Once all 1920 finish, call `gate.check()` with continuation on Python's import path.
Gates include positive paired improvement, no substantial family regression,
public points >=0.80, each family >=0.50, and direct old-version points >=0.65.
Run `continuation/verify_official.py` for 12 official file-path cross-checks against
frozen confirmation cases. It writes `official_crosscheck.json`.
`continuation/publish.py` refuses release without the gates, technical validation,
official cross-checks and source/archive hash equality. Review before invoking.
Publish destination is a NEW directory `submissions/release_v10_r2`; no online upload.
After publication write final Chinese README and evidence summary, verify original
hashes and all finite jobs have ended. Never claim a measured 2800 rating.

## Feedback already checked
Uploaded replay 113447926 is self-validation: both logs 719 records, no stderr.
Actual public V10 submission is 56560965. Latest captured row: 2026-09-26 11:05 UTC,
103 public matches, 92 wins, post-game rating 1909.878; no opponents >=2000 in sample.
Largest loss reproduced exactly: opening cash 1 led to missed hiring/feed.
Known-loss fixed-action diagnostics improved 0/11 -> 8/11 for h24, but these are
NOT closed-loop tests against the opponents' actual private programs.

## Superseding update: Phase A FAILED, continue Phase B
The frozen 36-turn candidate failed its independent per-family gate:
Fieldcraft 83/96 versus old V10 91/96. Do NOT publish it despite 555/576 aggregate wins.
Original repaired confirmation has 1920 valid full games. Failed MarketShock loader
attempts are preserved in continuation/confirmation_initial_attempt; the intended
module.agent adapter was tested in all 288 affected cases. Receipt retained.
12 actual official file-path cases match fast screening exactly (both coins/actions).
Technical archive validation passed but does not override the strength failure.

Next workspace: continuation/phase_b. Read PLAN.md and phase_a_rejection.json.
Generation6 PID78556: 528 full development jobs -> continuation/generation6_results.jsonl.
The four Phase-A Fieldcraft regression worlds are now diagnostic DEVELOPMENT data.
New revised candidate needs new final confirmation seeds; do not reuse old holdout.
Persistent finite-batch runner PID75316 (session_arena.py), eight reusable workers,
accepts one JSON line {manifest:absolute_path,output:absolute_path}; exit with {exit:true}.
It starts no tests autonomously. Use only when ARENA_READY.
Offline pressure audit PID80212 finished, phase_b/pressure_audit.json; no hidden
opponent values are passed to the candidate. Premia often carried, not yet in shed.
Phase-A style_stress has completed, but its scores remain unread. Keep its policies
out of candidate selection and test the final revised candidate on fresh style seeds.

## Latest continuation: Phase C cargo-readiness ablation (2026-09-26)
Phase B completed 2352 valid final-validation games and passed its original gates.
Its staged source is b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4.
No release_v10_r2 has been published. Review phase_b/summarize_probes.py limitations:
most new wins were Aurax; latest-ladder fixed traces were 11/15 versus old V10 13/15.
Do not call the aggregate a measured 2800 rating or hide these limitations.
Phase C lives at continuation/phase_c. Six readiness candidates plus Phase B and
old V10 are in development_jobs.json: 1744 complete-game jobs, eight worlds,
six public programs, three counter variants, three direct references, 26 probes.
Persistent arena PID75316 is executing this finite batch. A second finite batch,
fresh_loss_jobs.json (27 jobs for three NEW public losses), has been queued once.
Read the JSONL outputs before retrying; do not duplicate active work.
Remote controller REPL is PID110900; the frozen historical releases are unchanged.
Phase C adds public-position-derived carried-goods constraints to sale pressure.
Synthetic mechanism tests passed. No private opponent information is used by it.
Any new source selected after this study needs NEW frozen final-validation worlds.
This work did not submit anything to Kaggle or change account settings.
