# Day-5 plan alternatives: eight validated season-end labels

The revised bounded CPU run completed with exit 0. Its logged work ran from
14:29:19Z through 14:38:19Z, inside the 600-second process limit. The earlier
attempt timed out and supplied zero labels; it is preserved separately.

These are the preselected first four H30-development tapes from
`S/isearch/boards_dev.json`, both tape seats, with unchanged B or `compact+1`
at day 5 only. Both branches then follow ordinary B to the exact simulator
terminal boundary. Candidate plans are NumPy arrays injected into the unchanged
simulator; hidden state, tape and future randomness form labels only and are
kept outside the proposed selector input fields.

## Validation and descriptive result

All eight B terminal results match the preserved **simulator** baseline
`S/isearch/lc.csv` exactly in own coins, opponent coins and margin. Its `seat`
column is the action-tape seat (`S/wall/screen_pin.py` writes controlled money
from `1-seat`). Exact key coverage was checked before comparison. The first
injected B day also matches ordinary advance, its duplicate agrees, and the
existing NumPy/JAX macro and plan checks pass. This is simulator consistency;
it is not a new real-engine validation of the alternative.

| development tape | own delta | opponent delta | margin delta |
|---|---:|---:|---:|
| 107463847 | -648 | -1274 | +626 |
| 107464824 | +523 | -26 | +549 |
| 107465620 | +462 | +318 | +144 |
| 107465820 | -1571 | +206 | -1777 |

Each row averages the two mirrored seat-games of that tape. The fixed
alternative's descriptive mean is -114.5 coins per board. A hindsight oracle
choosing B whenever the alternative loses would average +329.75 on these four
boards. That oracle uses future results and is unavailable at runtime; four
boards cannot establish a usable predictor or support promotion. No family
statistics are pooled.

The first fixture's equal next-day cash/inventory had concealed a later +626
margin change. This establishes why short labels are insufficient for this
choice. The remaining question is whether current permitted observations
predict its sign on a larger development family. No gate has been trained,
and no held-out outcome has been used to choose one.

## Preserved evidence and next scope

Runner at commit `724687a`, script SHA-256
`73f965d63d760e4ec9ca4f4486a9d09adfd1228737fc93aae13952e5181b9615`.
Artifacts under `S/planselect/`:

- `day5_labels_retry.json` and `.log`: completed eight-label output and stages.
- `day5_labels_baseline_audit.json`: exact baseline check and input hashes.
- `day5_labels_dawn.pkl`, SHA-256
  `5e26e1bfac9fb0d77efd6b17de6a036b3cc585c1a7dd9814cf12012040b57cdb`.
- `day5_labels_day6.pkl`, SHA-256
  `2954ab82451e485165874ccacacb76d2bc45a386b180d9e6e15227386907a41e`.

Root tool session 26093 is terminal exit 0. Do not rerun it. Checkpoints belong
to this exact source/configuration and cannot be reused after source or sample
changes. The next staged scope is all thirty tapes in the same development
family, both seats, the same day-5 alternative and separate artifact paths.
Candidate/feature/calibration choices must be fixed before the remaining
labels, with the four-board exploratory history disclosed. H30B and NEXT30
are excluded from fitting. A complete-family run has not launched yet.
