# V10 revision research — in progress, not released

Workspace: `research/v10_rebuild_20260926/`.
Original root V9 and `submissions/release_v9`, `submissions/release_v10` are immutable.
No revised submission has been uploaded or approved.

## Verified online evidence
V10 submission 56560965: first captured real public panel 94 matches, 83 wins, 11 losses; latest captured post-game rating 1873.4268. Team leaderboard at capture displayed V9 instead. Uploaded replay 113447926 is self-validation, not a ranked opponent match.
Largest V10 loss 113488570 was reproduced exactly. Day-zero closing cash 1 caused an early hiring/feed chain failure. Safe net-five-unit opening removes the unnecessary initial grain round trip.

## Completed research
- 360 complete opening-sweep games, all valid; 20-unit sham control matched old V10 coins in all 40 cases.
- 150 complete closed-loop games with three additional real public programs, all valid.
- 658 complete generation-2 ablation games, all valid. Observed-stock threshold 4 and a 24-turn sales window deserve further work. Much of the initial point gain is versus references, so this is NOT sufficient promotion evidence.
- 799 72-turn opening functional checks, all valid; these are NOT complete games or wins. Rejected q24-last-single-lot because it killed all cows in 6 cases.
- Fast screening calls unchanged official transition functions and matched 1,438 observations on each of two official validation games; final release still needs official file-path loading and isolated parity validation.
- Three current leader-view successful task programs were exactly reconstructed at the engine level, but local reactive intent prototypes remain much weaker than V10. They are not valid strength anchors.

## Active bounded batches at checkpoint
Combination batch: `combination_jobs.json` -> `combination_results.jsonl`, 1476 full-match jobs, six workers. Additional real-program development batch: `additional_development_jobs.json` -> `additional_development_results.jsonl`, 160 full-match jobs, two workers. Check process state and ledgers before resuming; do not duplicate active jobs.
All batches are finite/resumable. `batch.py` verifies source hashes. Keep static traces, local-population games, old-reference games, and real public programs in separate reported panels.

## Still required
Select only after complete cross-family development results, add harder counter-candidates, extend development worlds, freeze one source, then use new confirmation worlds and unused actual programs. `marketshock` and `structured` are reserved actual-program tests; no performance runs yet. Four current team families and second traces are also reserved diagnostics. No score claim may be inferred solely from a public notebook title or static replay victory.
