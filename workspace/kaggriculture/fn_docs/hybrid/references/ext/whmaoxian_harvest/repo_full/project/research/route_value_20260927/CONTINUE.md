# Current continuation: route value and independent production experiments

No new official release or Kaggle upload has been made. R2 remains immutable.
The previous 5,184 route-learning games were recovered, not newly replayed.
A 157-feature day-six selector was trained on their outcomes; 576 prefixes were
reconstructed to join causal features to outcomes. Prefixes are not full games.

Completed new complete games:
- pilot_results.jsonl: 528 valid. Learned route selection adds four external wins
  in 160 paired cases, all against one responsive proxy. Not a rating estimate.
- counter_screen_results.jsonl: 240 valid, covering 30 study-view proxies.
- daily_dispatch_20260927/smoke_results.jsonl: 84 valid; six greedy prototypes lose.
- daily_dispatch_20260927/v2_results.jsonl: 48 valid; bulk-supply variants still lose.
- daily_dispatch_20260927/routed_single_results.jsonl: one valid routed prototype.
  Herd/crop maintenance improved but root-crop replanting remained deficient.
Total completed new full games above: 901. No heldout replay views were opened.

Current finite processes: PID17912 runs broad_jobs.json (960 required);
PID50156 runs daily_dispatch_20260927/routed_v2_jobs.json (96 required, two workers).
Always check on-disk row counts and process status before resuming.
Broad candidates and worlds were frozen before their results. Proxy and public
program panels are separate. The 30 proxies use study views, not private code.

prepare_growth_data.py is incomplete after two denied final appends. Do not run it.
The routed-dispatch final append succeeded on an ordinary same-tool retry; no
permissions or tool routing were changed. The full routed manifest has 72 jobs,
but only its first case was run. Do not count the unplayed jobs.
macro_combo_jobs.json does not yet exist: build_macro_combo.py has not been run.
