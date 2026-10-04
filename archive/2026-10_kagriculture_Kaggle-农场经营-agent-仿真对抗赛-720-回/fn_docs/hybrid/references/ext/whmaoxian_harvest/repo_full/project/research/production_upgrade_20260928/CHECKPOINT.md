# Active production upgrade research — no approved release yet

Frozen R2 main SHA256: b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4.
No old release was modified and no Kaggle upload was made.
Controller REPL PID24656; six-worker arena PID38516. Inspect logs before resuming.

## Completed and verified this response
- herd_stage1: 896 full games, zero invalid, sixteen new development worlds.
- early: 420; replay_diagnostic: 48; both zero invalid.
- fusion: 882, including fourteen cached preflight games, zero invalid.
- fusion_diagnostic: 42; funded: 504; funded_diagnostic: 24; zero invalid.
- Above total: 2816 unique valid cases, including controls and diagnostics.
- Six economic replay audits matched every public farm state and final rewards.
- Six warehouse-loss audits also matched those replays; losses occur at day end.
- Route preflight: 28 valid. Results copied to route_choice_results.jsonl for reuse.
- Opening-goose preflight: four valid, copied to opening_mix_results.jsonl for reuse.

## Running / queued: verify before counting
- opening_mix:252 total; opening_mix_diagnostic:12.
- route_diagnostic:84; route_choice:1176 total including28 preflight.
- Route screen is a six-world Yarn development stratum, NOT unbiased ladder validation.

## Findings and next checks
Selective midgame sheep adds two external wins over R2 on192cases; force-sheep regresses.
Finish + selective herd beats R2 on17/18 direct development games but is not2800 evidence.
Turning off prediction/advance generally regresses. Funded earlier sheep improves margins, not external wins.
Fresh40 replays were selected by time and downloaded; contents remain unread for frozen evaluation.
Sixteen reserve seeds in herd_stage1_design.json also remain unused. Do not train on these.
