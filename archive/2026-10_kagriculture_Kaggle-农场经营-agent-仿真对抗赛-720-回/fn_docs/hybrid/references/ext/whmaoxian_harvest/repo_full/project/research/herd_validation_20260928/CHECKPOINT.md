# Active herd / production research — no approved submission

Frozen R2 SHA256 remains b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4.
No Kaggle upload and no replacement of the frozen V9/V10/R2 releases.
Controller: PID186740. Arena: PID175036. Check logs before resuming.

Completed current-turn main ledgers, all zero invalid at completion:
- herd_extended_results.jsonl: 896 (16 development worlds, four policies).
- repeat_results.jsonl: 280 (four development worlds, v1; NOT release eligible).
- v2_extended_results.jsonl: 448 (same 16 development worlds, two corrected policies).
- jit_results.jsonl: 112 (four-world procurement pilot).
- current_diagnostic_results.jsonl: 276 (46 fixed-action views, 40 original episodes).
- diverse_results.jsonl: 432 (four-world broader public-source panel).
Two additional single-game smoke tests are saved separately.
Older 56-game herd pilot was analyzed, not reexecuted in this total.

Findings: single-sheep no-milk gate preserved external win counts, no new losses
on the 16-world panel, but no net external win gains. Forced sheep lost milk-world
matches. Repeated two-sheep versions regressed against Dmitrii. JIT procurement
successfully pays before the original pickup deadline; known-loss-world smoke
vs R2 gained 9789 coins, but all six real loss diagnostics remain losses.
R2 reproduces each of the six original replay rewards exactly. One real loss
improved 3205 with JIT, another worsened1049. No rating claim is supported.
V1 repeated-herd cash guard incorrectly assumed fixed BUY_PRODUCT prices;
v2 vetoes substitutions on these dynamically-priced-purchase turns.

New Salem/Q45 public sources are provenance-pinned and source reviewed. Neither
is stronger than R2 on the tested four worlds. They are NOT live top-ten programs.
Current work builds exact-observation-aligned production route branches at turns
72/144 from current/archived public DEVELOPMENT demonstrations. Original final
heldout views remain unused. See route_provenance.json after builder finishes.
