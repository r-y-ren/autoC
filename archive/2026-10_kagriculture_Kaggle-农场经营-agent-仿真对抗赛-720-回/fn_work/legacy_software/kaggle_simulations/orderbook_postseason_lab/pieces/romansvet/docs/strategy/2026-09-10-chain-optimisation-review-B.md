# Chain optimisation — independent second review (B)

Blind review of the "optimise harvest → shed → sale → reinvestment together"
statement. Code from `.claude/worktrees/arms-next`. Read-only.

## 1. What the routing citation actually says

A **one-board descriptive sim probe** (pinned board 107056463, theta
`flow172_g170c`) tracking a forced 12-tile melon opening's 72 units, hour by hour. The wall is **deposit turn** — not sell rows (6/day vs their 7), shed
(100 > 72), hands or cadence — and `MIDDAY_PLACE_V2_ON` (`plan.py:922`) **already
fixes it**: 66/72 bank and sell same-day, +7,993 own / −996 theirs by d11 eod.
Verdict: *"the route model is not the wall… the pot is not the win… any melon arm
must be additive, not a swap."* Cited as evidence routing needs extending, it says
the opposite.

## 2. The three "isolated change" claims

**A. Idle workers — TRUE as census, FALSE as an open lever.** 17.06 all-PASS
hand-days a game, 100 % from `start >= n_tasks` (`plan.py:3455-3462`); 555 idle
unit-turns = 41 % of idle (2560-2566). Every fix was measured: `HIRE_ROW_ON` saves
+889 of bill in sim but reads **−378/game, se 506, t −0.75** over 768 paired engine
games → OFF (3487-3494). CREW_FROM_TASKS −4,580 t −28;
JOINT_PLATE crew floor band6 54.2 → **1.0 %**, −41.9k t −27; RAMP11 top10 69.4 →
55.6 %, −4.3k t −3.0. The *spending* fix won instead: `TAIL_CARE_ON` +263 t 3.70,
`TAIL_FILL_ON` HELD42 +775 t 3.31 / LEG20 +1,366.

**B. Early sale hits an empty shed — PARTLY; refuted for the shipped build.** The
mechanism is real: harvests ride in hands until `_end_of_day` dumps them, so
every lot sells yesterday's shed; moving lot 2 from turn 10 to turn 4 measured
*identical* (`plan.py:1741-1747`), and the lot ledger reads hour-2 772.7 units,
hour-11 **9.3**, hour-19 475.7 (1841). But instrumenting **every market order in
128 engine games found no refused BUY/HIRE row and no SELL row the shed could not
fill before d29** (`2026-09-05-build-story.md:817-822`); shrinking a lot to
hour-0-clearing units lost **−4,964 t −9.8**. No layout headroom remains:
`EARLY_SELL_ON=False` is −77 ± 95 (HELD42) / −54 ± 195 (LEG20), a 4th lot −77
t −0.54 (`2026-09-10-sell-hour-headroom.md`). Empty-shed asks appear only in the
*forced melon* arm.

**C. Melon displaces animals — TRUE, five paired engine builds.** MELON_OPEN alone
band6 54.2 → 15.1 %, −17,554 t −12.8; +MIDDAY_PLACE_V2 −18,561 t −11.3; MELON_D10
−18.6k t −13.6; MELON_D10B 54.2 → **13.0 %**, −22.1k t −15.5, COW 3 → 1, egg 2/day
vs 5-12, +31k price gift by d27 (`2026-09-04-verdicts.txt:376,386`); pinned judge
130 tapes 1.9 %, −19,557.

## 3. The chain in code

`plan.py` unless noted.

- **what/who harvests — theta.** `plant_target` 1667/5384, `animal_want` 5521,
  `grow_mult` 5292, `dev_weight` 5695, `compact` 5488, `land_bias` 5360,
  `forward_days` 5995, `hire_bias`/`crew_target` 6097-6099, `animal_defer` 4891.
- **harvest → shed — hard.** End-of-day dump; `DROP_ON` (315) return leg; mid-day
  banking only via `BANK_BEFORE_LOT_ON` (1858, **False** here) or
  `MIDDAY_PLACE_V2_ON` (922, False). No gene.
- **sale timing — hour-0 static.** `SELL_TURNS=(3,10,18)` `ops.py:126`,
  `MELON_LOT_TURNS` `ops.py:137`, `EARLY_SELL_ON/MODE` 2463/2466; `avail` is the
  hour-0 shed, allocator runs once at dawn (5222-5224).
- **sale allocation — theta.** `hold`, `press` → `sell.allocate` (`sell.py:100-138`).
- **cash → next purchase — hard.** "The whole BUY row resolves at turn 1, ahead of
  every sale" (5198); only BUY_LAND rides `SELL_TURNS[0]`'s tenth slot, discounted
  (5205-5228). Today's sales fund only tomorrow's purse.

All 12 Macro fields (3392-3404) decode in `brain.decide` (`brain.py:860`):
`land_bias` 898, `animal_want` 946, `plant_target` 1026, `hold` 1051, `press` 1053,
`grow_mult` 1054, `compact` 1066, `dev_weight` 1069, `hire_bias` 1089,
`crew_target` 1109, `animal_defer` 1116, `forward_days` 1140 — and nothing else.
A per-product sell-hour map "does not exist — a code change, not a knob".

## 4. Does ES already optimise the four jointly?

**Yes.** One theta, one fitness (engine outcome), all four arms reading the same
per-day Macro — joint by construction. The sell-hour probe shows ES moving units
lot-1 → lot-3 through `hold`/`press` unaided (h1 105.8 → 99.4 rows, h18 32.2 → 38.0).

The one step with **no** theta channel is the **deposit turn**, and its throughput
is measured and small: BANK's excursion **fires 0.67 times a game, moving 3.4 units
into lot 2** (`plan.py:1817-1818`); +191/game t 2.07 against a +1,500 bar, 187/384
games identical; widening it (`BANK_LOT=2`, 13 fires/game) **loses −1,257** (1846-1849).

## 5. Verdict — **RUN NARROWER**

"Evaluate the complete chain" names no switch, gene, arm or judge; as written it
is the ES loop that already runs. The pair citation is sound (engine H_dm +801,
LEG20 +1,403; +875 t 3.69 on the live theta) — but it ships in the package build,
so it is a *shipped baseline*, not a starting point. Melon: **DO NOT RUN**.

The pair's post-mortem names the residual: *route order* — "0 coins in hand at the
best rank a DROP could still reach by turn 10, against 505 the block eventually
harvests" (1826-1832), candidate rate 28 % → 3 %. Narrowest experiment: sim-screen
**`HARVEST_FIRST_ON` (1953) composed with the shipped pair** — never measured in
that combination — on the 128 pinned held-out boards, both seats, paired. Escalate
only if HELD42 t ≥ 2 **and** LEG20 Δmargin > 0; judge then = paired LIVE55 rule +
TOPB 20 held-out top-tier boards, drawn legs veto only. Alone it read −80/game
t −2.61 and "inert", so one screen is the budget.
