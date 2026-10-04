# Market behavior-cloning integration: completed, not promoted

This supersedes CHECKPOINT.md and the older RESUME_AFTER_MARKET_BC.md.
The forest is integrated into standalone agents. It is NOT a new release.
No submission archive was created or uploaded. Target 2800 remains unverified.

## Completed work
14 active integration variants and one shadow variant were generated.
Weights were not retrained: the previously frozen 44,736-example forest was used.
Inputs remain own observations, public state, and causal own history only.
Runtime needs only the standard library; candidate files contain numeric trees.

The 16 shadow/control games passed: 5,752 shadow actions exactly matched R2.
Those 16 rows are INCLUDED in the 396-game first screen, not counted twice.
Two separate official file-path runs matched the screen's whole-game actions
and terminal coins. Observed maximum official callback: 0.711794 seconds.
Action safeguards and second-generation/reservation synthetic checks passed.

Full experimental games: 396 initial + 1,232 expanded + 528 guarded = 2,156.
All recorded experimental games were valid. The two official cross-check games
are separate technical tests. The 176 R2 control rows used for guarded comparisons
were already part of expanded development and were not played or counted again.

## Strength result
On the eight-world expanded design, each of six original expanded candidates,
three guarded candidates, and R2 won 96/96 versus six public implementations,
and 42/64 versus four locally reconstructed responsive proxies.
Thus there was NO net additional external-panel win count.
The proxies are NOT the current top-ten private programs. No rating is inferred.

Direct R2 results (wins/losses/ties, 16 games per candidate):
- conditional35: 9/5/2; conditional55: 5/5/6; add_p55_q4: 3/7/6.
- balanced35_guarded: 9/7/0; hold_p55_q8_guarded: 3/7/6;
  imitate25_guarded: 7/9/0.
Unguarded holding variants are not release-eligible: later cancellation can
conflict with R2's already-booked future-sale reservations. They remain as
unaltered experiment evidence. Guarded versions preserve reserved sale items.
Passing technical checks does not certify strategy quality or 2800 strength.
All tested integrated candidates are retained for research, not promoted.

## Evidence and provenance
Use screen_results.summary.json, extended_results.summary.json and
 guarded_results.summary.json alongside their raw manifests/JSONL files.
Guarded summaries do not contain the baseline rows, so their paired gain fields
are null. The identical-design baseline is in extended_results.jsonl.
shadow_parity.json and official_shadow.json document the actual parity checks.
The 20 final heldout top-ten replay views remain unopened; no release-level
independent validation or submission-package certification occurred here.

Additional numeric-export checker and final-gate script writes were blocked.
They were NOT recreated elsewhere and their checks were not claimed to pass.
Earlier model export tests are historical evidence only. Basic summaries used
an existing allowed script, not the blocked final-gate evaluator.
The timeout write prepare_early_add.py was later confirmed absent (ENOENT).
No early-window variants or matches were created or run.
Finite arena PID 257084 completed all batches and exited with code 0.
The intermittent connection recovered sufficiently for final reads and hashes.
Root V9, frozen V9/V10/R2 sources, and R2 archive hashes were reverified unchanged.
