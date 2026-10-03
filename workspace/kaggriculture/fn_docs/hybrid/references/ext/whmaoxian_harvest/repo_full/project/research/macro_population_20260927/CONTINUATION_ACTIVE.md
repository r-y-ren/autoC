# Active continuation: preserve prior releases and validate before promotion

The user requests continued strategy improvement and real-game testing before delivery.
No new release or Kaggle upload has been made in this continuation.
Root V9, frozen V9/V10/R2 and the R2 archive remain the reference artifacts.

Completed current-continuation development:
- Full native-route screen: 672 new complete games, all valid. No global fixed route promoted.
- Early-liquidity screen: 576 rows, including 48 reused controls; 528 new games, all valid.
  Wheat liquidation damaged production. Mixed_h24 added one external win but lost all eight R2 games.
- Public commodity-direction predictor: 43,140 study rows, 43 features, 24 ExtraTrees.
  Numerical export parity was checked; prediction quality does not establish match strength.
- Idle commodity-cycle screen: 480 rows, including 48 reused controls; 432 new games, all valid.
  Eight newly played shadow games are INCLUDED in those 432. No external win gain.
  The complete synthetic cycle-check extension was denied; only earlier market-only assertions ran.
Current completed fresh full-game total before the next batch: 1,632.

Current experiment:
- noop_micro_jobs.json / noop_micro_results.jsonl: 7 physical-command-efficiency variants plus R2.
- Four already-seen development worlds; 384 total rows, 48 cached R2 controls, 336 new games.
- Arena PID316964 handles explicit manifests with six workers; inspect output before resuming.
- REPL PID294880 is the controller. Builder PID368016 exited normally.
- Exact no-op detection compares own physical state with and without one original command;
  only same-location care, conservative watering, fertilizer collection, and bounded harvest are tested.
  No production-route changes or market rewrite in this branch. Strength is not yet established.

Blocked branches retained incomplete: cycle augmentation builder (absent), advantage_learning
policy_core.py (options only), and prepare_weed_queue.py (missing output stage). Do not deploy these.
The 20 heldout replay views and previously reserved final-confirmation worlds remain unused.
