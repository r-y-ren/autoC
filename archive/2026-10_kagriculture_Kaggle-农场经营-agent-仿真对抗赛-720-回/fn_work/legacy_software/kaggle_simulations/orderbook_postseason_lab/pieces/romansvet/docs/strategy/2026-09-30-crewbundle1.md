Stream: CREWBUNDLE1 (local, 1 worker; no remote runs)
Date: 2026-09-30 08:18Z-09:45Z
Verdict: NONE. No variant reaches the HOLD20 bar (coins >= 0.90 and value >= 0.90). The best frozen variant (m9, the default when the switch is on) scores HOLD20 coins 0.817 and value 0.751, against j4 at 0.805 and 0.738.

## What was built

This is an independent second implementation of the astra brainstorm15 per-hand crew rule set. It lives in the PROGRAMME3R direct executor, `src/kagg3/prog/direct.py`, behind `PROG_CREW_BUNDLE_ON`.

- **Code:** branch `crewbundle1_0930` in worktree `kagg3_wt_crewbundle1`, off 505affb0.
  - 7a497d88: verbatim tree_j4 overlay.
  - 28cbe1f7: the CB code.
  - 8bcb038c: the `cb_fert_a0` sub-flag.
- **Switches:**
  - `plan.PROG_CREW_BUNDLE_ON = False` is the default and is byte-identical to j4. The tune20 finals equal j4's exactly.
  - `True` applies CB_DEFAULTS.
  - A `"k=v;..."` string overrides sub-flags, as does the `PROG3_KNOBS` env var.
  - `runtime.act` passes the flag to DirectAgent.
- **Two dispatchers share the rule code:**
  - `cb_mode=1` (the default): a full per-hand matching dispatcher, `_cb_dispatch`.
    - One owner per started tile bundle. The visit is finished in order: FERTILIZE, then productive WATER, HARVEST, PLANT one seed, and WATER.
    - P0 rescue fires when slack is <= `cb_slack`.
    - P2 does every animal op in one visit: HARVEST, FEED, CARE, COLLECT.
    - P4 fertilizes wheat at age 2, or at age 3 before its water.
    - P5 harvest bundles, P6 plant and dig bundles (weeds join the planting assignment), and P7 eve feed and care plus productive watering.
    - Watering uses the simulator's phase predicate: annuals in their growth window, ongoing crops only on a fertilised eve, and anything with cu >= 1.
    - h20-23 promotion.
    - Global greedy matching on class x `cb_w` + travel, with ties broken by tile id, then hand id.
  - `cb_mode=0`: the same rules layered onto j4's greedy dispatcher, as priority edits, a busy-hand exclusion and a wheat seed claim.
- **Unchanged:** the market, opening, lots, land and hires are exactly as j4 emits them.
- **Judge:** the exact both-sides replay on local fastenv. `S/crewbundle1/scripts/ext.py` (the CREWSCHED1 copy plus act() timing) runs at about 3 s a game. `sm2.py` and `life.py` produce the table below.

## Results

Coins is the mean per-game ratio to MMPQ's final. Value is units x reference prices. Units are ours/MMPQ.

**HOLD20:** read once per frozen variant.

| variant | coins | value | wh | ca | to | st | me | eg | mi | wo | wheat cyc d | empty+weed d12-28 | fert/day | moves/day | deaths/g | wheat harv/g | p99 s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MMPQ truth | 1 | 1 | 580 | 233 | 134 | 230 | 75 | 231 | 173 | 154 | 3.43 | 4.7+1.8 | 12.7 | 120 | 19.1 | 172.6 | - |
| j4 (OFF) | 0.805 | 0.738 | 286 | 110 | 58 | 191 | 70 | 160 | 144 | 113 | 3.39 | 9.7+4.1 | 10.0 | 131 | 38.6 | 126.3 | 0.0023 |
| L1 = layered, all rules | 0.801 | 0.735 | 312 | 121 | 56 | 181 | 71 | 153 | 146 | 111 | 3.45 | 7.1+4.1 | 8.7 | 136 | 45.5 | 133.0 | 0.0045 |
| L2 = layered, phase water + fert age 2 | 0.810 | 0.751 | 318 | 117 | 58 | 188 | 72 | 161 | 147 | 115 | 3.47 | 8.4+4.0 | 9.1 | 137 | 41.9 | 136.0 | 0.0027 |
| **m9 = mode 1 (default)** | **0.817** | **0.751** | 305 | 118 | 63 | 179 | 69 | 187 | 136 | 125 | 3.76 | 4.8+5.2 | 7.7 | 132 | 44.7 | 129.2 | 0.0052 |

**TUNE20:** j4 scores coins 0.740 and value 0.733. MMPQ has deaths 21.4/g and 176.4 wheat harvests a game. Every row comes from `S/crewbundle1/logs/batch.txt`.

- **Mode 1, first builds:** strict classes with cb_w 3 scored cb1 0.397 and cb2 0.588.
- **Mode 1, W=1:**
  - m1 0.687: wheat yield 4.80 and eggs 182, but strawberries 117.
  - Adding ongoing fertiliser, harvest at y >= 1 and en-route work gives m3 0.723 (value 0.739).
  - m9 with slack 4 scores 0.722 (value 0.737, deaths 41.8, wheat harvests 117.5).
- **Mode 1 knob grid:** every cell is <= m9.
  - W: W=0 0.587, W=2 0.659.
  - hyst 3: 0.717.
  - slack: 2 gives 0.713, 6 gives 0.708.
  - Survival class: cls_surv 3 gives 0.706, cls_surv 1 gives 0.680.
  - cb_wh3 4: 0.710.
  - Fertilise earlier: cb_fert_a0 1 gives 0.714, 0 gives 0.708.
  - No en-route work: 0.703.
- **Layered, one rule at a time:** every cell is within 0.706-0.743, which is noise around 0.740.
  - phase water: 0.738
  - fert age 2: 0.731
  - wheat seed buffer: 0.720
  - busy owner: 0.706
  - P0 at h20: 0.731
  - animals only when full: 0.743
- **Layered, other probes:**
  - Deadline urgency grid: 0.632-0.717.
  - No-detour grid: 0.697-0.724.
  - Combos c1-c5: 0.700-0.725.

## Findings

1. **The rule set moves units between products, not coins.** Both implementations plateau at 0.70-0.74 on TUNE20 and 0.80-0.82 on HOLD20. This matches PROGRAMME3R's knob plateau and PLANTDEATH1.
   - Wheat rises by 20-40 units, and mode 1 moves eggs +27 and wool +12.
   - Strawberry, tomato and milk lose about as much.
2. **Wheat lifecycle, j4 on TUNE20, plantings d10-26:**
   - j4: 116 planted, 95 harvested, 20 lost. The losses are 8 dry at age 2, 7 decayed at age 5 and 4 dry at age 4. Yield is 4.07 a harvest, mostly age 3 at 4 units and age 4 at 4 units.
   - MMPQ: 148 planted, 147 harvested, 1.3 lost. Yield is 4.99 a harvest: age 3 at 5 units 52 times, and age 4 at 6 units 58 times.
3. **Why the lost tiles die:** they get zero visits for two days. A 13-hand crew carries a backlog of 50-100 open tasks at h0 and still 28 at h23. On a death day in mode 1, 28 tiles have cu >= 1 at h1 and 8 are still unwatered at h23.
   - Earlier P0 cut deaths from 55.9 a game (m7, slack 0) to 40.2 (m13, slack 6), but the labour comes out of animals and strawberries, so coins stay flat.
   - The executor's labour per coin is the wall, not rule order. MMPQ makes 176 actions and 122 moves a day with the same hands; we make about 155 actions and 132 moves.
4. **Seed stock is not the planting gap.** The wheat seed buffer reached MMPQ's h0 stock and changed nothing (0.720). SEEDSTOCK1 agrees.

## Bar

HOLD20 coins >= 0.90 and value >= 0.90: best 0.817 / 0.751. **CANDIDATE BODY: NONE.** No V56 run and no package.

Slips: 1. The 09:06Z checkpoint line was stamped ahead of the clock (actual 09:00Z).
