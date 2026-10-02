# GAPREVIEW1-B (2026-09-27, blind reviewer B): every arm we ran, mapped onto every decision the engine allows. What is still uncovered?

This review is read-only and ran no games.

**Sources:**
- BUILD-STORY.md lines 1-3300, read in full across 4 chunks.
- Every 2026-09-1x and 09-2x strategy doc (headers and verdict lines).
- `2026-09-26-ideas1.md` and `2026-09-11-lever-ranking.md`.
- The switch list in `plan.py`.
- `spec.py`.
- The engine itself: `.venv/.../kaggle_environments/envs/kaggriculture/kaggriculture.py` (`_apply_unit_action` L312-530, `_process_market` L544-630, `_daily_refresh_*` L752-833, `_end_of_day` L860-892).

**Outputs:**
- Arm ledger: `S/gapreview1/B_ledger.tsv`, 1,132 rows in 7 columns (name, date, axis, decision codes, verdict with paired/one-leg tag, key number, source line or doc), sorted by axis then date.
- Raw per-chunk parts: `B_ledger_p1..p5.tsv`.

The ledger has these rows per axis:

| axis | rows |
|---|---|
| RL/ES | 208 |
| infra/judge | 155 |
| analysis | 127 |
| routing | 109 |
| crop mix | 107 |
| selling/price | 86 |
| herd/feed/care | 78 |
| opp-conditioned | 63 |
| crew/hires | 62 |
| opening | 61 |
| land | 38 |
| endgame | 37 |

653 rows carry a paired verdict and 121 are tagged unpaired or one-leg.

## 1. Engine decision space, and what covered each decision

**Unit ops.** Every unit, every turn, gets one op:

| group | ops |
|---|---|
| movement | MOVE, PASS |
| shed | DROP, PICKUP |
| animals onto structures | PLACE |
| crops | PLANT, WATER, HARVEST, FERTILIZE, DIG |
| structures | BUILD_COOP, BUILD_PASTURE |
| animal husbandry | FEED (wheat only), COLLECT_FERTILIZER, CARE |

**Market queue.** Up to 10 orders per turn, lockstep per unit against the rival:
- HIRE (fib cost; hands vanish at night)
- BUY_LAND (fixed order NE, SW, SE: 1k, 2k, 4k)
- SELL
- BUY_PRODUCT (WHEAT and FERTILIZER only)
- BUY_SEED
- BUY_ANIMAL (lands in the shed and counts toward its 100 cap)

**Engine facts that matter here:**
- Reward is money only. Shed stock, animals and structures are worth 0 at the end.
- An unwatered planting weeds the same night.
- An animal escapes after 2 unfed nights.
- The care bank accrues on fed+cared nights. An unfed production night wipes it.
- Every live animal yields 1 fertilizer per night, fed or not.
- Fertilizer doubles the in-window water bonus for one-time crops and the per-production yield for ongoing crops.
- The town never drains fertilizer.

**Coverage key:**
- **COVERED**: a paired judge verdict exists.
- **PARTIAL**: judged on only one leg or board set, only as part of something else, or closed by census/arithmetic.
- **UNCOVERED**: never judged.

| # | decision (engine op) | arms that covered it (ledger names) | best verdict | status |
|---|---|---|---|---|
| M01 | d0 capital split: seeds / animals / land / hands (purse 3,000) | MELON_OPEN, SCRIPTOPEN, MIRROR_OPEN, OPENPKG1, WOOLFIRST1, SHEEPFIRST1, BOEY2, MELONVRP1, NONV2 | all gift or own loss; OPENPKG1 −23 pooled, BOEY2 −92 | COVERED |
| M02 | d0 price pump (wheat BUY/SELL round trip) | OPEN_PUMP (+410, shipped ON), PUMPOFF3, KNOBV56 `OPEN_PUMP_ON=False` (dev +3, fails FRESH) | kept ON | COVERED |
| M03 | crop choice per planting (mix) | CROP_SCARCE, CROPMIX, TOMATO15, CARROTFLAT1-3, ENGMIX1, WHEATMIX1, TOMATOFILL1, CONTEST1, MELONCOUNTER2 | all ≤ 0 or gift | COVERED |
| M04 | planting volume, i.e. how many tiles are asked for | PLANT_ASK, VOLUMEHI, JOINTLIFT, PLANT_FILL_LATE, RELAYFILL1, FILLWORK1, GAPFIX1, SLIVER1 (shipped in vrp9_cs), ESWORK1 g30 (shipped) | shipped by ES genes; hand fills gift | COVERED |
| M05 | planting day and hour | PLANTTIMING (ceiling 0), EVE_STOCK, EVENING_SEED, LATEPLANT1, ENDWAVE1, VRPREPAIR3 last day | closed | COVERED |
| M06 | which tile gets which crop | TILEALLOC (−335), ROUTE_EFF, GAPCENSUS1/2, GAPFIX1 share-rule fill (paired, −1..−3) | closed | COVERED |
| M07 | which tile holds a coop or pasture (structure siting) | none; the site is `_rank_near(dev_key)` inside the plant chain | — | **UNCOVERED** |
| M08 | watering | DRYDEATH1 (0.12 deaths/g), WATERAUDIT, CREWAUDIT1b (99.9 % same-day), SURVIVAL_WATER (shipped), CREW24_H23_WATER | census plus paired inert | COVERED |
| M09 | fertilizer application (crop, day) | FERT_TIMING (SHIP +2,845), SAME_DAY_FERT (−29.6k), WHEATCYCLE1 (fert@2 PARKED), IDEAS1 late fert saturated | shipped | COVERED |
| M10 | fertilizer source and sale (collect / buy / sell / hold) | FERT_RESERVE (−32.7k), FERTDENIAL (both signs), FERTSALE1 FERT_DUMP (9 cells ≤ 0), FERTCOW | closed | COVERED |
| M11 | harvest timing (melon age 10 vs 12, wheat @3, ongoing cadence against the yield cap) | melon race family, WHEATCYCLE1 (harvest@3 loses), CARETIMING (harvest ceiling +0), HARVEST_FIRST, YIELD1 | closed | COVERED |
| M12 | DIG of spent crops, weeds, same-day replant | ENDFIX1 LATE_EXEC (SHIP), NOOPAUDIT, REPLANT_SAME_TURN | shipped | COVERED |
| M13 | Q2/Q3 purchase day | LAND 09-14 (earlier: −881 band, sim), WHEATMIX1-Q3_EARLY (d8, −9), BOEY1 Q2 d6 (−36), NONV2 Q2 d3 (tapes only), NONV1 Q3 d9 (tapes) | earlier and Q2-later lose | **PARTIAL**: Q3 later or skipped never run |
| M14 | Q4 purchase | Q4PROG1, Q4VRP1, Q4RELAY1, RELAY12, Q4LIMIT1, Q4FIX1, Q4DIG1, ESWORK Q4 gene | closed 8 times | COVERED |
| M15 | hires per day | HIRELEVEL1, KNOBVRP1, KNOBV56b, CREW24, JOINTLIFT, CREWPUSH, LABOUR1, EMPTY_ROUTE_UNHIRE (SHIP) | shipped | COVERED |
| M16 | hire timing within the day, and queue row | HIRE_ROW (SHIP), DAWN0, WIDE_PICK/WIDE_PICK_FREE (SHIP), H1WAIT | shipped | COVERED |
| M17 | unit routing and task assignment | ROUTE_* handles, ROUTENN1-3, ROUTE_VRP (SHIP), VRPREPAIR (SHIP), RRDEPTH1, ROUTERJIT1 (SHIP), RRDEEP2, RLROUTER1 | shipped; depth closed | COVERED |
| M18 | animal species, count and day | HERDVRP1 (8/8 gift), HERDTILT/2, GEESE1, EGGDOSE1, EGGS2, ENGHERD1, NONV4, ANIMAL_DEFER, WOOLPRICE | closed | COVERED |
| M19 | feeding (who, which night, wheat bought or grown) | FEEDFIRE, FEEDKEEP1, FEEDNIGHT1, FEEDROOM1 (built, unjudged) and FEEDROOM2 (paired NO SHIP), FEED_MANDATORY (ON) | closed | COVERED |
| M20 | care | CARE_FILL (SHIP), CARE_RIDE (SHIP in vrp9_cs), CARE_FED (dev +3, denial-only), CARE_HOLD, CAREAUDIT1 | shipped | COVERED |
| M21 | feed and care on the placement night | CREWAUDIT1 → PLACEFEED1: 123 g, flips +6/−2, Δtheirs −921 (t −4.86), Δours −53; NO SHIP on the Δours bar | paired | **PARTIAL**: rejected on own purse while flips and margin are positive; the herd-gated variant was never run |
| M22 | collecting animal products against the `max_held` cap | ACTSCAN (reach-bound), CREWAUDIT1 (cap losses ≤ rival), YIELD1 | census only | PARTIAL, no gap: census shows no loss |
| M23 | which day to sell (hold across days) | SELLDAY, LOTDEPTH, SELLAUDIT1 (paired replay gift), ENDSELL, RESALE1 | closed | COVERED |
| M24 | which hour or row to sell in | LOT4 (SHIP), LOT5, EARLY_SELL (ON), EARLY_SELL_MODE B (−7,976), SELL_SPREAD, SLIP1, CHURNPRICE1, DAWNSELL | shipped | COVERED |
| M25 | lot size and order split | SPREAD6 (−1,802), DRIPSELL1, LOT_SPLIT, SELL-LOT/WOOL (paired, allocator right) | closed | COVERED |
| M26 | queue slot against the rival's lockstep | SELL_SLOT_PRIORITY (SHIP), SLOTLOCK, SLOTMIRROR, RIVALRANK, V15_DODGE, SELLFIRST | shipped | COVERED |
| M27 | shed room, overflow, dusk clip | OVERFLOW2-4 (SHIP), CLIP_CAP, SHED_DUMP, CLIPCENSUS1 | shipped | COVERED |
| M28 | market buys: seeds, prestock, feed wheat | PRESTOCK/V2 (−326), DSMSEED1, TRADER (engine law), FEEDROOM2 | closed | COVERED |
| M29 | wheat or fertilizer resale arbitrage | RESALE1 (every cell −3..0), WHEAT-REBUY (round trip exactly 0), FERTDENIAL | closed | COVERED |
| M30 | end-of-game liquidation and last routes | ENDROUTE/ROW2/ENDROUTE2/SPLIT (SHIP), ENDSELL, ENDGAME1, ENDWAVE1 | shipped | COVERED |
| M31 | rival-class tell and gating | ENGINE_GATE (ON), NONV1-4, M20z (shipped, tapes only), NVTHETA1/NVTSHIP1, ENGGATE1, RIVAL_TELL | shipped | **PARTIAL**: M20z rests on 8 open-loop tapes (NONV3: no reacting 0-melon agent exists) |
| M32 | price denial or contest against the rival | OPP_MIX, OPP_SUPPLY, CONTEST1 (6 cells lose), MELONDENY1, WOOLDENY1, DENYFILL1 (arithmetic), MELONVETO | closed | COVERED |
| M33 | seat asymmetry | SEATFLIP1 (same-board P1−P0 = 0) | closed | COVERED |
| M34 | whole-policy learners (ES/PPO/distil/search) | theta ES plateau, ESV56/57, ESSCRATCH, ESLOSS1, ESWORK1 (g30 SHIP), head PPO flow25x-268, RLV57, RLSCRATCH, RLFAST2, BESTRESP1-6, MPCFEAS | ESWORK g30 shipped; rest closed or running | COVERED, with one sub-gap (G2) |
| M35 | shop-draw inference (the per-day `Random(seed)`) | 09-05 build story "seed inference is dead"; MPCFEAS (zero seed bits at d0) | closed by law | COVERED |

The ledger has **no uncovered mechanism-level decision with a large premise**. Every engine op has at least one paired arm, apart from structure siting (M07). What remains is either narrow or sits in how a verdict was read.

## 2. Gap list (strict: an item counts only if no paired verdict closes it)

### G1 — M21 placement-night feed+care: rejected on Δours while flips and margin are positive
- **(a) Why it is open.** PLACEFEED1 was judged paired and failed only the Δours > 0 bar. That bar exists to stop a gift, but the final ranking is Bradley-Terry on wins.
- **(b) Prior evidence** (`2026-09-27-placefeed1.md` §4):
  - Pooled over 123 games: flips +6/−2, Δmargin +868, Δtheirs −921 (t −4.86), Δours −53 (t −0.28). FRESH50 gives +1/−0.
  - The own-purse sign follows the herd. Boards with fewer than 5 sheep placements: Δours +199, Δtheirs −229. With 5-9: +449 / −326. With 10 or more: −759 / −2,169.
  - The cause is wool's `sq` curve above I0: first-fire wool cheapens later lots.
- **(c) Probe.** Gate PLACEFEED so it fires only while our planned sheep count is below N, with N in {6, 9}. The sheep count is roughly exogenous: placements went 14 to 15. Run 2 cells plus the ungated arm on FRESH300, held100 and the reacting pool, against vrp10_esw. Expected: gated Δours +100..+300/g gift-free, and net flips +1..+4 per 300.
- **(d) Rank: 1.** The code exists (branch `placefeed1`), and the only thing missing is the gate. Caveat: the split by sheep count is post hoc, which is why it has to be judged on FRESH boards.

### G2 — M34: extrapolating the one ES step that shipped (ESWORK g30)
- **(a) Why it is open.**
  - 09-11 lever-ranking E1/E2 proposed theta soup and step extrapolation and never ran them. No ledger row exists.
  - The ESWORK g32 σ×4 reject tested random-perturbation width, not the accepted direction.
  - ESSHIP1 shows g30 is a candidate that the ES itself rejected as a centre, so its step length was never tuned.
- **(b) Prior evidence.**
  - g30 passes every leg: held +1,759, dev100 Δours +638, FRESH +6 dours +522 t 6.2.
  - The 09-11 h* curvature fit said accepted steps are 3-10× too large, which argues for k < 1. The ES plateau (−124 ± 47) argues the direction may be noise.
- **(c) Probe.** Zero build. Take θ(k) = θ_base + k·(g30 − θ_base) for k in {0.5, 1.5, 2.0}, i.e. `ESWORK_THETA` = k·cand_g030 if the base is zero-genes, and check that first. Run dev100, held100 and FRESH300 in the SIMGAP1 exact sim against vrp10_esw. A monotone dose response either gives a free theta or halves every future ES step. Expected ±1-3 flips per 100.
- **(d) Rank: 2.**

### G3 — M07 structure siting (coop and pasture tile)
- **(a) Why it is open.** It was never proposed. The site falls out of `_rank_near(dev_key)` in the plant chain (plan.py ~11180-11256). No ledger row touches the site of a structure.
- **(b) Prior evidence.**
  - Every animal pulls a wheat pickup and a feed visit every other day ("hungry on day+1, day+3", plan.py:10441).
  - ROUTERAUDIT1 found the router slack is crew size (oracle +722 bill/g). CREWAUDIT1 shows turns/unit 2.41 against the rival's 3.08, with idle 578 against 479.
  - GAPCENSUS: outer corners are 62 % empty d6-8.
  - So distance matters only if the herd sits far from the shed.
- **(c) Probe.**
  1. A census first, 0 games: mean Manhattan distance from shed to structure, ours vs rival, from the CREWAUDIT1 engine-hooked replays (`S/crewaudit1`).
  2. Only if ours is at least 1 step farther: a near-shed siting rank behind a switch, on dev100 + FRESH300.
- Expected +0..+200/g own, gift-free, since volume does not change.
- **(d) Rank: 3.** Cheap to kill.

### G4 — M13: Q3 bought later or skipped
- **(a) Why it is open.** Only three directions were judged:
  - Earlier Q3: LAND 09-14 is sim-only against a tape seat, pre-VRP; WHEATMIX1-Q3_EARLY d8 went −9.
  - Q2 later: BOEY1 Q2 d6, −36, gift.
  - Q2 d3: NONV2, tapes only.
- Q3 later (d11-13) or a conditional skip was never run under the VRP router.
- **(b) Prior evidence.** LAND 09-14 says the day-10 buy is gate-bound, not cash-bound. Q2-later loses heavily. The Q4 family says each extra quadrant is crew-limited, which is the only argument that a later Q3 could pay.
- **(c) Probe.** A land-day offset in {+1, +2, +3} on Q3 only, on dev100 and held100 in the exact sim against V56: 3 cells, about 600 games. Expected 0 ± 2 flips. The prior is negative.
- **(d) Rank: 4.**

### G5 — M31: the shipped M20z zero-melon plate, on open-loop evidence only
- **(a) Why it is open.** NONV3 found no reacting zero-melon agent, so the only paired evidence is 8 open-loop tapes (+4). MELONLOGIC1 re-read 5 seats (net +1) and found tine.sh live at −23.5k with the latch ON, against +8.8k OFF.
- **(b) Prior evidence.** The Tz latch fires on 4 of 275 live games, so the class is about 1.5 %.
- **(c) Probe.** Run M20z ON/OFF on every banked seat where Tz fires: LOSSBANK2's 17 seats, LIVEWATCH16's 18 non-V tapes, and the tine.sh tape. That is under 100 tape games. The output is a keep/remove call for the final pair. Expected ±1 flip on about 1.5 % of games.
- **(d) Rank: 5.** The EV is tiny, but it is a shipped switch with no closed-loop evidence.

### Below the line (PARTIAL, but closed by census or size; not worth a probe)
| item | status | why closed |
|---|---|---|
| FEEDROOM1 hungry-first feed order | built, never judged | CLIPCENSUS1 sized it: 0.23 escapes/g, < 400 coins |
| WHEATCYCLE1 fert@2 | PARKED | the engine gives no yield, only crew time |
| DENYFILL1 dump denial | executed 0 dumps | CONTEST1 closed planting-for-denial paired |
| EGG per-product lot slope (09-14) | no arm | LOT4, SLIP1 and CHURNPRICE1 (95-99.7 % of day max) supersede it |
| Care on cow pre-production nights | ops wasted | engine cap: 1+7 → 6. Crew is not binding (idle 578), so this is worth ≈ 0 |
| MELON_ADD_ON (09-11 P5) | never built | the melon family closed paired 9+ times; OPENPKG1 last |

## 3. Verdict: top 5 gaps by expected value
Nothing uncovered and large remains. Of the 35 decisions, 32 have a paired arm. M22 is census-only with no loss, M35 is closed by engine law, and M07 (structure siting) was never judged. The residual value is in narrow items and one verdict rule.

| # | gap | probe | cost |
|---|---|---|---|
| 1 | G1 PLACEFEED gated on herd size | code exists on `placefeed1`. Add the sheep-count gate N ∈ {6, 9} and judge it plus the ungated arm on FRESH300, held100 and the pool. Expected +1..+4 flips per 300, gift-free | 2 agent-h, ~1,000 games |
| 2 | G2 ESWORK g30 step dose response, k ∈ {0.5, 1.5, 2.0} | zero build, exact sim, dev100, held100, FRESH300. Expected ±1-3 flips per 100 | 1 agent-h, ~1,500 games |
| 3 | G3 structure siting | census of shed distance from the CREWAUDIT1 replays (0 games), then a near-shed switch only if ours is at least 1 step worse. Expected ≤ +200/g | 0.5 agent-h + 0 games (then 1.5 h and ~400 games) |
| 4 | G4 Q3 later by +1..+3 days | 3-cell grid against V56 on dev100 and held100. Expected 0 ± 2 flips | 1 agent-h, ~600 games |
| 5 | G5 M20z closed-loop re-check | ON/OFF on every banked Tz-firing seat. The output is a keep/remove call for the final pair | 1 agent-h, ~100 tape games |

Coordinator note: the PLACEFEED1 result (09-27, doc plus BUILD-STORY L3298) landed after CREWAUDIT1 listed it OPEN. It is now paired, and G1 is its gated follow-up, not the original gap.
