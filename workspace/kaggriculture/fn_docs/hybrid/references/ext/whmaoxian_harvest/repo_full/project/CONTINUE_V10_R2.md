# V10-R2 — delivered locally; online rating not yet measured

Canonical upload file:
`submissions/release_v10_r2/submission.tar.gz` (651,310 bytes).
Source SHA256: `b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4`.
Archive SHA256: `25e4b6ed3f9e121e26d0b59c7a7625fb216a6210da0553809a3032913db92e9a`.
Entrypoint: `phase_b_agent`. Root main.py remains V9. Old V9 and V10 are unchanged.
Do not upload candidate_v10_r2: that is the rejected Phase-A candidate.
No Kaggle submission was made in this workflow.

## Final selection
The unchanged Phase-B similarity90 candidate was retained after additional trials.
Opening: net five wheat without the old buy-20/sell-15 loop.
Enhanced sell pressure is gated by public farm similarity >=0.90; otherwise the
conservative old-V10 market parameters remain. No opponent identity or test seed.
Read RELEASE_V10_R2.md and the release's evidence.json before further modification.

## Evidence and limitations
48 originally unseen worlds, both seats, six public programs: revision566/576wins,
oldV10474/576, V9472/576. Independent final validation totals2352valid games.
Direct:77/96wins againstV9;73/96againstoldV10. Reference styles144/144forallversions.
90 of92added primary wins are Aurax; do not represent improvement as uniform.
Recent fixed ladder traces regressed13/15oldV10 to11/15revision. They are static
counterfactual probes, not the private opponents' responsive programs.
14real old-loss traces reproduceoldV10; revision flips8in fixed-action diagnostics.
One of the newest losses worsened. Three final cases retain an unplaced cow.
Target2800 remains UNVERIFIED online. Do not infer Elo from local win rates.

## Latest extra studies and execution status
Continuation Phase C is at `research/v10_rebuild_20260926/continuation/phase_c/`.
Its 1,744 cargo-readiness games, 976 lead-risk games and 27 new-loss diagnostics
finished with zero invalid results. All twelve new mechanism variants were rejected
for release: no consistent additional win-point improvement. Source B was unchanged.
Total counted complete experimental/control/diagnostic games: 15,151. This is not
15,151 independent worlds, nor 15,151 games by the final candidate.
The finite arena session PID75316 exited normally with code0. No further batches
are queued. The controller REPL can be closed without losing saved evidence.
Original publisher had a st_size() metadata typo; only that size-property access
was repaired, leaving all strength gates and frozen agent bytes unchanged.
Byte-level final checks are in `submissions/release_v10_r2/final_receipt.json`.
Future candidates must use new confirmation worlds; do not recycle seen outcomes
as independent validation. Preserve failed experiments and original releases.
