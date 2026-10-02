# Shipped-OFF switch sweep on the pinned judge (sim)

Agent, 2026-09-09, 90-min box from 11:31Z. Tool: `S/simprobe/run.sh`
(docs/strategy/2026-09-09-simprobe.md) — sim on the engine's exact pinned
boards, HELD42 (84) + LEG20 (20) + LOSS12 (24), both seats, paired against
the cached knob-free base `base_4d1adb3fef.csv` (worktree
`.claude/worktrees/arms-next` @ bdec0e9, theta
`flow135_g350_gpfwdfv_gb028.npy`).

`OPEN_PUMP_ON` **already ships True** (plan.py:1173), so the cached base is
the live configuration and adding `OPEN_PUMP_ON=True` to an arm is a no-op.
Every arm below is one switch at its shipped companion constants.

Verdict rule: PASS if LEG20 d-margin > 0 **and** HELD42 d-margin >= 0.
LEG20 > +1,000 is flagged for an engine confirmation.

## 1. Inventory — every `^[A-Z_0-9]+_ON = False` in arms-next

29 switches: 28 in `core/plan.py`, 1 in `core/brain.py`.

| # | switch | line | one-line doc | class |
|---|--------|------|--------------|-------|
| 1 | MIDDAY_DROP_ON | plan:383 | second DROP block per unit so the return leg costs the walk, not the tail of the day | NEVER |
| 2 | SHED_OVERFLOW_ON | plan:565 | forced sale of projected shed overflow | MEASURED-DRAWN-ONLY (band6 190/192 identical, "closed" 09-06) |
| 3 | MELON_OPEN_ON | plan:643 | the recorded top-tier 12-melon day-0 opening, planner-native | MEASURED-PINNED (130 tapes, −19,557; skip) |
| 4 | MELON_LOT_EARLY_ON | plan:653 | move the dump day's three melon rows to turns (6,7,8) | inert without MELON_OPEN_ON (doc: "read only when MELON_OPEN_ON") |
| 5 | MIDDAY_PLACE_ON | plan:773 | rewrite the melon excursion's rank/op | asserts require MELON_OPEN_ON or V2 — not runnable alone |
| 6 | MIDDAY_PLACE_V2_ON | plan:922 | bank melon mid-day to the day's last sell row | MEASURED (−101, excursion list); inert w/o melon |
| 7 | SAME_DAY_FERT_ON | plan:1010 | apply fertilizer the day it is bought | MEASURED-DRAWN-ONLY (LAST_DAY=29 = −27,186 t −15.6) |
| 8 | OPEN_DENY_ON | plan:1083 | the MELON_OPEN day-0 board without the dump-day rows | NEVER (shares MELON_OPEN's dead sites) |
| 9 | OPEN_PUMP_TELL_KEEP0_ON | plan:1276 | per-turn patch when the other seat pumped too | NEVER — **submission-path only, the rollout cannot see it: NOT RUNNABLE in the sim** |
| 10 | ENDGAME_TOMATO_ON | plan:1362 | plant into the town's late tomato lottery | MEASURED-DRAWN-ONLY (TILES 12/16 dose-responsive loss); **shipped TILES=0 → inert at shipped constants** |
| 11 | LATE_STRAW_CAP_ON | plan:1438 | from day 15 move the mix's strawberry share onto the other crops | NEVER |
| 12 | OPP_SUPPLY_ON | plan:1507 | opponent's measured supply curve into the price projector | MEASURED-DRAWN-ONLY (−2,972 / −3,616, t −3.8/−4.8) |
| 13 | OPP_MIX_ON | plan:1572 | read the other seat's committed tiles into the plant mix | claimed inert (latediv), never a pinned d-margin |
| 14 | BANK_BEFORE_LOT_ON | plan:1858 | excursion: bank a block's harvest before the early sell lot | NEVER |
| 15 | HARVEST_FIRST_ON | plan:1953 | order a block's harvest ranks ahead of its carried-input ranks | NEVER |
| 16 | PRESTOCK_ON | plan:2052 | a BUY order at TURN_PRESTOCK, hire rows moved | NEVER — **assert plan:2478 forbids it with the shipped EARLY_SELL_ON: NOT RUNNABLE alone** |
| 17 | ROUTE_EARLY_ON | plan:2158 | start a unit's route while the BUY row it does not need is pending | MEASURED-PINNED (arm in flight, launched 11:29Z) |
| 18 | MARKET_PACK_ON | plan:2327 | pack the day's two market rows onto other turns | NEVER — **assert plan:2478 forbids it with EARLY_SELL_ON: NOT RUNNABLE alone** |
| 19 | TAIL_FILL_ON | plan:2589 | fill a unit's PASS tail with up to 2 hops to the nearest free task | MEASURED-DRAWN-ONLY (bundled with CARE_FILL, band6) |
| 20 | CARE_FILL_ON | plan:2795 | 4 CARE hops in the tail on owned, fed animals | MEASURED-PINNED (+0/−0, H +54, LEG20 +46; skip) |
| 21 | CARE_HOLD_ON | plan:2878 | hold the care price at the animal's product quote | MEASURED-PINNED (H −332, LEG20 −277; skip) |
| 22 | ANIMAL_DEFER_ON | plan:3134 | half-price animal candidates on days 0-7 (shortfall spike) | NEVER |
| 23 | HIRE_ROW_ON | plan:3497 | reconcile the hire bill with the day's rows | MEASURED-DRAWN-ONLY (engine −378/game t −0.75, n=768) |
| 24 | FORWARD_ADMIT_ON | plan:3537 | override the g11 gene: admit tiles whose op lands within N days | MEASURED-DRAWN-ONLY (hand probe 94→65 %) |
| 25 | FERT_FLOOR_ON | plan:3656 | a price floor under the fertilizer sale (1/2 of base quote) | NEVER |
| 26 | FERT_VOLUME_ON | plan:3779 | an application must be worth 2x the unit it burns | MEASURED-DRAWN-ONLY (paired runs 09-04, closed) |
| 27 | PLANT_FILL_ON | plan:4308 | a second grant that fills idle unlocked tiles | MEASURED-PINNED via PLANT_FILL_LATE (H −6,275, LEG20 −6,551; family closed) |
| 28 | WHEAT_VOLUME_ON | plan:4526 | move 1/3 of the non-wheat plant target onto wheat | MEASURED-DRAWN-ONLY (paired runs 09-04, closed) |
| 29 | PLANT_MIX_DRAIN_ON | brain:805 | tilt the plant mix by the residual-drain estimate | MEASURED-PINNED (3 gains, dose-responsive loss; skip) |

Counts: **MEASURED-PINNED 6** (skip) · **MEASURED-DRAWN-ONLY 9** (candidate) ·
**NEVER 9** (candidate) · **structurally not runnable / inert alone 5**
(MELON_LOT_EARLY, MIDDAY_PLACE, MIDDAY_PLACE_V2, OPEN_PUMP_TELL_KEEP0,
PRESTOCK/MARKET_PACK are 2 of them).

## 2. Screen — one switch per arm, `OPEN_PUMP_ON=True` added (a no-op: it ships True)

Paired against `base_4d1adb3fef.csv` (arms-next @ bdec0e9, flow135_g350_gpfwdfv_gb028).
Base win rates: HELD42 21.4 %, LEG20 70.0 %, LOSS12 25.0 %.

| arm (switch) | HELD42 d-margin (t) flips +/- | LEG20 d-margin (t) | LOSS12 d-margin (t) | verdict | wall |
|---|---|---|---|---|---|
| sw_tail_fill | +775 (t +3.31) +2/-0 | +1,366 (t +2.61) | -354 (t -1.23) | PASS **FLAG** | 691s |
| sw_bank_lot | +165 (t +2.15) +0/-0 | +209 (t +1.82) | +166 (t +0.71) | PASS | 783s |
| sw_late_straw | -60 (t -0.50) +0/-0 | -152 (t -1.34) | -462 (t -3.87) | FAIL | 533s |
| sw_animal_defer | -36,544 (t -27.72) +0/-18 | -40,652 (t -9.59) | -36,391 (t -17.96) | FAIL | 538s |
| sw_opp_supply | +617 (t +2.54) +6/-0 | +47 (t +0.12) | -733 (t -1.61) | PASS | 734s |
| sw_fert_floor | -3,551 (t -16.77) +0/-8 | -3,172 (t -10.03) | -4,117 (t -9.78) | FAIL | 736s |
| sw_opp_mix | +2 (t +0.06) +0/-0 | +35 (t +1.45) | -5 (t -1.45) | PASS (inert) | 621s |
| sw_shed_ovf | 0 (t 0) +0/-0 | 0 (t 0) | 0 (t 0) | FAIL (exactly inert) | 635s |
| route_early | -158,893 (t -72.88) +0/-18 | -165,371 (t -29.35) | -157,868 (t -39.98) | FAIL | 776s |
| **sw_tail_bank** (TAIL_FILL+BANK_BEFORE_LOT) | +817 (t +3.50) +2/-0 | **+1,404** (t +2.70) | +575 (t +1.35) | PASS **FLAG** | 939s |
| sw_harvest_first | +1 (t +0.07) +0/-0 | -24 (t -1.47) | -24 (t -0.37) | FAIL (inert) | 835s |
| sw_midday_drop | -4,311 (t -10.29) +0/-6 | -2,686 (t -3.89) | -3,220 (t -7.08) | FAIL | 719s |
| sw_open_deny | -25,855 (t -19.50) +1/-18 | -30,074 (t -9.82) | -27,114 (t -16.75) | FAIL | 738s |
| sw_same_day_fert | -29,560 (t -25.12) +0/-16 | -30,688 (t -11.75) | -28,260 (t -12.42) | FAIL | 810s |
| sw_forward_admit | -8,676 (t -12.11) +0/-10 | -6,361 (t -5.75) | -8,178 (t -8.98) | FAIL | 705s |

`route_early` (ROUTE_EARLY_ON) was launched by the harness at 11:29Z, not by
this sweep; it is listed because it is the same judge and the same base.


## 3. Flagged for engine confirmation

**`TAIL_FILL_ON`** — the only arm with LEG20 > +1,000. HELD42 +775 (t +3.31,
sd 2,142) with **+2 flips / -0 drops** (106479420 both seats), LEG20 +1,366
(t +2.61, no flip either way, base win 70 % held), LOSS12 -354 (t -1.23, no
flip). Positive on the two validated sets, negative and non-significant on the
unvalidated one. This is the switch that fills a unit's PASS tail with up to
`TAIL_HOPS = 2` hops to the nearest free task, on top of the shipped
`TAIL_CARE_ON`. Its only prior read (verdicts 2026-09-05 15:04Z) was a DRAWN
band6 bundle with `CARE_FILL_ON` + HOPS 4, which lost win rate; alone, on the
pinned judge, it gains. **Recommend a paired engine leg.**

Second, much weaker: **`BANK_BEFORE_LOT_ON`** +165 / +209 / +166, all three
sets positive, zero flips, 44 % of boards identical. Below the flag bar and
inside the lottery band, but it is the only other switch that is positive
everywhere. Cheap to fold into the same engine leg as a second arm.

## 4. What this refutes

* **`ROUTE_EARLY_ON` is not a marginal lever, it is a catastrophe on the pinned
  judge**: -158,893 HELD42 / -165,371 LEG20, win 21.4 -> 0.0 %, 18/18 held-out
  boards dropped, **0 % of boards identical**. The switch was landed at 6cbb3e1
  ("let a unit start its route while the BUY row it does not need is pending")
  and its tests only gate on `value_dropped`. A whole-season collapse of this
  size on every board is the signature of a broken compiled route, not a
  strategy loss — worth a code look before anyone re-tries the idea.
* **`ANIMAL_DEFER_ON` -36,544** (18/18 dropped): half-pricing animal candidates
  on days 0-7 destroys the ramp. Shortfall family stays closed.
* **`FERT_FLOOR_ON` -3,551** (+0/-8): the price floor under the fertilizer sale
  holds units the shed needs. Closed.
* **`SHED_OVERFLOW_ON` is exactly inert on the pinned judge** (0 coins on all
  122 boards) — the 2026-09-06 drawn read (190/192 identical) was right.
* **`OPP_MIX_ON` is inert** (+2 / +35 / -5), confirming the latediv claim from
  the other side: the shop -> mix response is learned inside theta.
* **`OPP_SUPPLY_ON` is NOT the -3k the drawn band6 legs said**: pinned HELD42
  +617 (t +2.54) with +6 flips / -0 drops, LEG20 +47 (level), LOSS12 -733.
  It passes the letter of the rule but LEG20 is noise; the +6 held-out flips
  are worth one confirmation leg if a slot is free.
* **`LATE_STRAW_CAP_ON` is level** (-60 / -152 / -462, no flips).

## 5. Not run in the box

* `MARKET_PACK_ON` and `PRESTOCK_ON` — `assert` at plan.py:2478 forbids either
  with the shipped `EARLY_SELL_ON = True`. Reading them means turning off a
  promoted +2,184 t 5.1 lever, i.e. a bundle, not a single-switch arm.
* `OPEN_PUMP_TELL_KEEP0_ON` — submission-path only; `kagg3.sim.rollout` never
  runs the runtime's per-turn hook, so the sim cannot read it at all.
* `ENDGAME_TOMATO_ON` — shipped `ENDGAME_TOMATO_TILES = 0` makes it a literal
  no-op at its shipped companion constants. (The harness's `amix10_tom1` arm,
  gain 1.0 + `ENDGAME_TOMATO_SHOPS = 1` on the `care-cov` worktree, is
  -8,798 HELD42 / -13,056 LEG20 / +2/-11 flips — the tomato family stays shut.)
* `MELON_LOT_EARLY_ON`, `MIDDAY_PLACE_ON`, `MIDDAY_PLACE_V2_ON` — all three are
  inert or assert-blocked without `MELON_OPEN_ON`, which is -19,557 on this
  same judge.
* Out of time, still un-run and still candidates: `HARVEST_FIRST_ON`,
  `MIDDAY_DROP_ON`, `SAME_DAY_FERT_ON` (at LAST_DAY 29, known -27k drawn),
  `HIRE_ROW_ON`, `FORWARD_ADMIT_ON`, `FERT_VOLUME_ON`, `WHEAT_VOLUME_ON`,
  `OPEN_DENY_ON`. Each is one 10-13 min arm against the cached base.

## 6. Follow-up round (13:50Z box) — the eight leftovers + the pair

Six of the eight ran; none asserts against the shipped configuration
(`SAME_DAY_FERT_ON`'s guard at plan.py:2552 only excludes the melon excursion
and `BANK_BEFORE_LOT`, both off in its arm). Results are in the table above.

**The pair is the result.** `TAIL_FILL_ON + BANK_BEFORE_LOT_ON` together:
HELD42 **+817** (t +3.50, +2 flips / -0 drops), LEG20 **+1,404** (t +2.70),
LOSS12 **+575** (t +1.35) — positive on all three sets, which neither switch
manages alone (TAIL_FILL is -354 on LOSS12, BANK is +209 on LEG20). The two do
not interfere: the combination is almost exactly TAIL_FILL + BANK, so the
excursion clock and the tail cursor are independent. **This is the arm to
confirm in the engine**, not TAIL_FILL alone.

Everything else in this round is a loss or a null:

* `HARVEST_FIRST_ON` +1 / -24 / -24, zero flips — **inert on the pinned judge**.
  Ordering a block's harvest ranks ahead of its carried-input ranks changes
  nothing the route was not already doing. Closed.
* `MIDDAY_DROP_ON` -4,311 (+0/-6) — a second DROP block per unit costs the walk
  without banking anything the end-of-day drop was not going to bank. Closed.
* `SAME_DAY_FERT_ON` -29,560 (+0/-16) at its shipped `LAST_DAY = 29`, which
  **reproduces the 2026-09-04 drawn engine read (-27,186 t -15.6) on live
  pinned towns**. The COLLECT-at-the-head-of-every-day pathology in that
  ledger is real on the judge too. Closed for good at LAST_DAY 29.
* `OPEN_DENY_ON` -25,855 (+1/-18) — as predicted from its shared day-0 sites,
  it is `MELON_OPEN_ON`'s disaster (-19,557) with a slightly different opening.
  The day-0 melon opening family is closed from a third direction.
* `FORWARD_ADMIT_ON` -8,676 (+0/-10) at `FORWARD_ADMIT_DAYS = 3` — the override
  loses to the `g11` gene the ES trained. Confirms the hand probe (94 -> 65 %)
  on the pinned judge and on the shipped opening rather than a forced one.
  The forward horizon belongs to theta; do not override it.

Still un-run after this round: `HIRE_ROW_ON`, `FERT_VOLUME_ON`,
`WHEAT_VOLUME_ON` — all three already carry paired *engine* reads on drawn
boards (HIRE_ROW -378/game t -0.75 at n=768; FERT/WHEAT_VOLUME closed
2026-09-04), so they were the cheapest three to drop when the box ran out.
Each is one ~12 min arm against the cached base.
