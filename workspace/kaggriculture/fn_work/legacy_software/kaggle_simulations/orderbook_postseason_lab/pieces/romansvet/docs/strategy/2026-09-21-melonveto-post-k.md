# MELONVETO_POST K dose — BAND3

2026-09-21. `_melon_veto` used the shared `MELON_VETO_FLOOD_K = 60`; there
was no gate-only environment path for the post-head threshold. Added
`MELONVETO_POST_K = 60`, used only by the post-residual call and conditionally
forwarded by `S/actionrl/gate.sh`. Unset behavior remains the K=60 behavior.

CRN-paired against `a8_940b3`, 120 boards / 240 seat rows:

| K | dmargin | se | t | dours | dtheirs | per-seat wins cand/base | flips |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 40 | -6,863 | 427 | -16.07 | -7,631 | -768 | 44/130 | +2/-88 |
| 60 (`vpost_b3`) | +145 | 71 | +2.02 | +1 | -144 | 130/130 | +0/-0 |
| 80 | +0 | 0 | — | +0 | +0 | 130/130 | +0/-0 |

Proof, real BAND3 board `110822437`, seat 0: post-head melon target
`K40/K60/K80 = 0/2/2` on d11 at `I0+49`, then `0/0/1` on d12 at `I0+60`.

**VERDICT: NO SHIP.** No K reaches paired-margin t >= 3; K=40 also has negative net flips, while K=60 is t=2.02 and K=80 is inert.
All fail the BAND3 rule, so no K-triggered BAND2 gate was run and the switch stays OFF.
