# OPSCENSUS — the d10-19 unit-turn budget, ours vs theirs, on the 15 hiband ship losses

2026-09-19, local, `master`. New instrument `S/opscensus/probe.py` (hooks `_apply_unit_action`,
`_daily_refresh_plants`, `_decay_plants`, `_do_hire`, `_commit_unit`): every farmer/hand turn with its
op, whether it CHANGED state, and its target; plus the fate of every planting read off the engine.
Same theta/switch string/seeds/town as [[volumehi]] — final purses reproduce `ship7692/hiband.csv`
**to the coin on 15/15 seats**, so the hooks are non-perturbing. `S/opscensus/{probe,report.py,run_all.sh}`,
raw `S/opscensus/raw/` (gitignored, 27 s/board).

## 1. The budget — effective unit-turns, mean per board, d10-19 (ours / theirs)

| op | LOSS15 | Δ | ENGINE-4 | BAND-11 |
|---|---|---:|---|---|
| PLANT | 51 / **85** | **+34** | 54 / 79 | 50 / 87 |
| WATER | 380 / **429** | **+49** | 382 / 451 | 379 / 421 |
| FERTILIZE | **77** / 41 | **−36** | 74 / 58 | 78 / 35 |
| HARVEST crop | 98 / 106 | +8 | 97 / 111 | 98 / 104 |
| HARVEST animal | **67** / 56 | −11 | 74 / 54 | 64 / 56 |
| FEED / CARE / COLLECT | 507 / 503 | −4 | 523 / 471 | 501 / 515 |
| PICKUP+DROP (carry) | **131** / 91 | **−40** | 139 / 105 | 128 / 86 |
| PLACE+BUILD+DIG | 14 / **49** | +35 | 17 / 50 | 13 / 48 |
| MOVE | 1,160 / 1,169 | +9 | 1,164 / 1,221 | 1,158 / 1,150 |
| **PASS (idle)** | **231** / 165 | **−66** | 216 / 246 | **236 / 135** |
| **TOTAL** | **2,715 / 2,694** | −21 | 2,741 / 2,847 | 2,705 / 2,638 |

Per target (LOSS15): plantings WHEAT 28.9/**70.5** · MELON **12.3**/0.0 · STRAW 7.1/12.2; water turns
WHEAT 125/**229** · MELON **75**/25 · STRAW 174/170; fert STRAW **48**/32, WHEAT 28/9. Animals level
(feed 166/165, care 164/172, collect 177/170). Market orders (no unit-turns) SELL 439/**797**.

## 2. Fate of every planting made d10-19 (ours / theirs)

| | LOSS15 | ENGINE-4 |
|---|---|---|
| made | 50.7 / **84.9** | 54.0 / 79.2 |
| harvested | 81 % / 83 % | 83 % / 81 % |
| **WEEDED** | **0.1 / 0.7** (0 % / 1 %) | 0.0 / 2.0 |
| expired on the vine | **7.1** / 4.1 | 7.2 / 3.2 |
| dug / alive at d29 | 0.0 / 8.3 · 2.3 / 1.5 | 0.0 / 6.5 · 2.0 / 3.2 |
| yielded ≥ 1 unit | 100 % / 99 % | 100 % / 98 % |
| WATER turns / planting | **6.15** / 4.70 | 5.94 / 4.41 |
| FERT turns / planting | **0.91** / 0.47 | 0.91 / 0.70 |
| water / *paying* plant, WHEAT | 4.06 / 3.82 | 4.08 / 3.56 |
| … MELON | **8.75** / — | 8.91 / — |
| … STRAWBERRY | 9.48 / 9.30 | 9.66 / 9.46 |

## 3. Answers

**(a)** Totals are level (2,715 / 2,694), so their +34 plantings and +49 water turns (+129 with
DIG/MOVE) are funded out of three cells that are OURS: **PASS idle +66**, **carry PICKUP/DROP +40**,
**FERTILIZE +36** = 142 turns. Idle alone is 8.5 % of our budget (BAND-11: 236 vs 135).
**(b)** Yes — 4.70 vs **6.15** water turns per planting — but **not by tending more cheaply**: per crop
the cost is the same on both sides (WHEAT 3.82 vs 4.06, STRAW 9.30 vs 9.48). It is **MIX**: 83 % of
their d10-19 plantings are WHEAT at ~3.8 turns, while our 19.4 melon+strawberry plantings eat **249 of
our 380 water turns**. Nobody's plants die (weeded 0.1 / 0.7) — [[idlework]]'s weed law does not bind
here; what binds is turns-per-plant. Our own 7.1 expiries are the melon/straw tail.
**(c)** **None.** The three absorbing cells are each ≤ 66 turns against ~130 needed, and their switches
are closed by mechanism (`IDLE_TAIL_HOPS_ON` / [[idleops]], [[idlework]]; `CLIP_FERT_SKIP_ON` is a clip
rule, and FERT is productive at +2/water). Every switch that reaches the **mix** — `CROP_SCARCE_ON`
[[engtail]], `WHEAT_VOLUME_ON`, `PLANT_MIX_DRAIN_ON` (t −15.4 at gain 1.0) — is rejected or gifts on
the shared curve. No judge run: there is no lever to fly.

**VERDICT** — the ask is not the only cap ([[volumehi]]) and the turns are not missing: our plant mix
costs **1.45 more water turns per planting**, and the crop score in `brain.decide` carries **no
turn-cost term**. That, not a bigger ask, is the shape of the next gene.
