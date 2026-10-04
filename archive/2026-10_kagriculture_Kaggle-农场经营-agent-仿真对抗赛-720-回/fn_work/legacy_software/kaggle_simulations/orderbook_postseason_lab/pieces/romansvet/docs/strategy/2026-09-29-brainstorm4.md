# BRAINSTORM4 (2026-09-29, session 4 of the brainstorm loop; stream dir `S/brainstorm4/`, checkpoint `S/brainstorm4/checkpoint.txt`)

Seed (docs/strategy/2026-09-29-brainstorm3.md "Session summary", astra-brainstorm6.md): the first cell is `STRAW_WAIT1=(f,8)`, a bounded
one-day strawberry sale deferral at fixed production. The ledger comes first. The invariant to break is "at fixed production, withholding
supply gives the rival at least as much value as it gives us", and it must be broken with paired receipts.

## Round 1 (15:44Z-16:25Z)

**Verdict: STRAW_WAIT1 is KILLED by the ledger, with no build.** The demand test never passes against V56. In 65 v21 checks and 112 m40
checks at our d21-25 h17 sales, D24 is 19-37 (m40: 7-43) and the conservative rival estimate R_est is 32-77, so D24 > 2 R_est + 2 holds
**0 times**. Both f give exactly **0 deferred units, own 0, rival 0, margin 0** on 21/21 and 40/40 traces (bar +500 / +500). Even with the
rival's *actual* next-24h sales (an oracle that no public estimate can beat), the rule reaches only +12..+35 own and +24..+49 margin, because
our shed is at 100 around the night drop. The unconditional hold is margin-positive in the exact replay, which contradicts astra's
aggregate sensitivity. It is infeasible, though: shed peak 141-159, displacing 13-23 units a game. **Every timing move at fixed production
is worth at most +7 coins of margin per unit against V56. Timing is closed. The margin is in volume.** The round-2 cell is
`STRAW_FERT_FULL`. It fertilizes the 22-24 strawberry yield events per game that PFS leaves unfertilized while it sells 119 fertilizer units
at 48.5. Ledger: margin +1,766 on v21 and +1,160 on m40, own -1,014 / -706.

### Method (all local, 1 worker, nice 19 / ionice idle; no remote, no GPU)
- **Traces:** `S/brainstorm4/rec.py` is VBAND1's `vr.py` closed loop, with the PFS package tree (8d670dad, TRANSFER3 `tree/pfs`) plus the OFF
  string in seat 0 against the public V56 bank agent in the bit-exact fastenv. It adds a per-step trace:
  - the market inventory at step start;
  - both farms' per-step sold units and coins per product (`sales()` deltas);
  - both sheds after the step and the carried stock before it;
  - both raw market order lists;
  - both farms' strawberry tiles at every h17 (yield, fertilized_until_day, planted_day).
- **Coverage:** the 21 v21 boards and the 40 m40 boards (seat 0), at 10-11 s a game. Final money is **identical to the VBAND1 control rows
  21/21 and 40/40** (`res/tr_v21.jsonl.gz`, `res/tr_m40.jsonl.gz`).
- **Ledger:** `S/brainstorm4/ledger.py` replays the strawberry market exactly.
  - Engine mechanics: orders are walked slot by slot in the engine's per-unit lockstep (both players quote the same pre-commit inventory
    and commit in player order). A $1 unit adds no supply. The town drain (shops every 4 steps, the center every 24) is independent of
    inventory, so it is taken from the trace.
  - Baseline replay reproduces every recorded strawberry sale, units and coins, for both farms. There are 0 mismatched steps on v21.
    m40 has 1 step in each of 3 traces: an h23 rival sale of 1 unit at 9 coins, where the night drop inflates the shed read.
  - The no-op arm (f = 0) gives 0 / 0 on 61/61.
  - Counterfactuals move only our h17 units; every other order and both productions stay fixed.
  - `ledsum.py` builds the tables. `grad.py` gives the per-unit timing gradient for 7 products. `mval.py` gives the value of +1 unit sold.
    `fertled.py` is the round-2 pre-screen.

### A. STRAW_WAIT1 ledger
The rule is replayed as specified:
- It acts at our existing h17 strawberry sale on d21-25.
- It defers the units quoted < f, at most 8 in total.
- It requires D24 = 6 x (strawberry shops unlocked) + 1 > 2 R_est + 2. R_est = the rival's shed + carried strawberries + the ripe yield
  on its strawberry tiles + one day's growth per live plant (2 if fertilized). It uses no future shop draw.
- It requires projected shed room, taken as the realised trace occupancy + held <= 100 until the release.
- Deferred units are released at the next h17 regardless of price and are never deferred again.

Variants:
- `Wo` = the same rule with the oracle R (the rival's actual next-24h sales).
- `U` = astra's comparison: hold every unit quoted < f at the d21-25 h17 sales, with no cap, no demand test and no room test, and release
  at d26 h17.

Each cell reads: units deferred / own delta / rival delta / margin delta / shed peak (occupancy + held) / units displaced over 100.

**v21 (21 traces, every trace):**

| trace | base own / rival straw coins | W40 def / own / rival / margin / peak / displ | W60 def / own / rival / margin / peak / displ | Wo40 def / own / rival / margin / peak / displ | Wo60 def / own / rival / margin / peak / displ | U40 def / own / rival / margin / peak / displ | U60 def / own / rival / margin / peak / displ |
|---|---|---|---|---|---|---|---|
| v_114925209 | 46217 / 30548 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 8 / +0 / +0 / +0 / 100 / 0 | 8 / +0 / +0 / +0 / 100 / 0 | 39 / +1361 / +43 / +1318 / 143 / 43 | 45 / +1649 / +43 / +1606 / 149 / 49 |
| v_114927542 | 26779 / 23733 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 19 / +827 / -574 / +1401 / 136 / 36 | 19 / +827 / -574 / +1401 / 136 / 36 |
| v_114935974 | 28726 / 30432 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 5 / +420 / +694 / -274 / 121 / 21 |
| v_114950104 | 49508 / 39797 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 |
| v_114964405 | 42582 / 29767 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 46 / +1850 / +978 / +872 / 150 / 50 | 56 / +2626 / +1405 / +1221 / 159 / 59 |
| v_114984838 | 12653 / 14981 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 6 / +412 / +160 / +252 / 108 / 8 | 6 / +412 / +160 / +252 / 108 / 8 |
| v_115002685 | 42270 / 27376 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 47 / +1374 / -19 / +1393 / 148 / 48 | 48 / +1422 / -19 / +1441 / 148 / 48 |
| v_115004539 | 48994 / 38891 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 1 / +117 / +117 / +0 / 111 / 11 |
| v_115025125 | 31792 / 27687 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 8 / +238 / -122 / +360 / 100 / 0 | 8 / +238 / -122 / +360 / 100 / 0 | 26 / +2636 / +989 / +1647 / 121 / 21 | 36 / +3962 / +1986 / +1976 / 131 / 31 |
| v_115079468 | 40852 / 32966 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 3 / +144 / +0 / +144 / 100 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 9 / +727 / +375 / +352 / 113 / 13 |
| v_115107745 | 38574 / 31159 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 8 / +399 / +153 / +246 / 99 / 0 | 8 / +399 / +153 / +246 / 99 / 0 | 17 / +1967 / +1817 / +150 / 118 / 18 | 27 / +3366 / +3320 / +46 / 128 / 28 |
| v_115150041 | 46121 / 36058 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 1 / +96 / +21 / +75 / 113 / 13 | 11 / +1207 / +394 / +813 / 123 / 23 |
| v_115079950 | 58809 / 46054 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 |
| v_115033934 | 44951 / 31773 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 13 / +1480 / +759 / +721 / 119 / 19 | 23 / +2732 / +1483 / +1249 / 129 / 29 |
| v_115030573 | 4118 / 2725 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 |
| v_115028747 | 34543 / 24599 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 20 / +1144 / -693 / +1837 / 131 / 31 | 24 / +1336 / -693 / +2029 / 135 / 35 |
| v_115026903 | 16470 / 16252 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 12 / +462 / -162 / +624 / 121 / 21 | 12 / +462 / -162 / +624 / 121 / 21 |
| v_115021555 | 18656 / 14684 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 2 / +92 / +55 / +37 / 104 / 4 | 3 / +115 / +69 / +46 / 105 / 5 |
| v_115016235 | 9911 / 10068 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 3 / +139 / +44 / +95 / 104 / 4 | 3 / +139 / +44 / +95 / 104 / 4 |
| v_115014355 | 34943 / 24922 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 3 / -54 / -334 / +280 / 100 / 0 | 3 / -54 / -334 / +280 / 100 / 0 | 26 / +1467 / +187 / +1280 / 136 / 36 | 27 / +1536 / +213 / +1323 / 137 / 37 |
| v_115012518 | 27313 / 19138 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 0 / +0 / +0 / +0 / 0 / 0 | 29 / +526 / -1277 / +1803 / 132 / 32 | 29 / +526 / -1277 / +1803 / 132 / 32 |
| **mean (n=21)** | | 0.0 / +0 / +0 / +0 / 0 / 0.0 | 0.0 / +0 / +0 / +0 / 0 / 0.0 | 1.3 / +28 / -14 / +42 / 100 / 0.0 | 1.4 / +35 / -14 / +49 / 100 / 0.0 | 14.6 / +754 / +111 / +643 / 150 / 18.3 | 18.3 / +1123 / +361 / +762 / 159 / 23.3 |


**m40 (40 traces; the per-trace table is in `S/brainstorm4/res/ledger_m40.md`):**

| trace | base own / rival straw coins | W40 def / own / rival / margin / peak / displ | W60 def / own / rival / margin / peak / displ | Wo40 def / own / rival / margin / peak / displ | Wo60 def / own / rival / margin / peak / displ | U40 def / own / rival / margin / peak / displ | U60 def / own / rival / margin / peak / displ |
|---|---|---|---|---|---|---|---|
| **mean (n=40)** | | 0.0 / +0 / +0 / +0 / 0 / 0.0 | 0.0 / +0 / +0 / +0 / 0 / 0.0 | 0.7 / +12 / -11 / +24 / 100 / 0.0 | 0.8 / +17 / -10 / +27 / 100 / 0.0 | 10.3 / +436 / +149 / +287 / 141 / 12.9 | 12.7 / +604 / +321 / +282 / 147 / 15.7 |

- m40: traces where the rule deferred >= 1 unit: W40 0/40, W60 0/40, Wo40 7/40, Wo60 8/40, U40 29/40, U60 31/40
- m40: W demand test at the d21-25 h17 sales: 112 checks, D24 7-43 (mean 27.1), conservative R_est 32-77 (mean 45.3); D24 > 2 R_est + 2 in 0
- m40: oracle next-24h rival strawberry sales at the same checks: 0-38 (mean 15.5); passes 47
- v21: traces where the rule deferred >= 1 unit: W40 0/21, W60 0/21, Wo40 4/21, Wo60 5/21, U40 15/21, U60 18/21
- v21: W demand test at the d21-25 h17 sales: 65 checks, D24 19-37 (mean 27.6), conservative R_est 33-77 (mean 44.2); D24 > 2 R_est + 2 in 0
- v21: oracle next-24h rival strawberry sales at the same checks: 0-38 (mean 14.3); passes 32

**Kill:** W40 and W60 have mean own 0 and margin 0 on both sets (bar +500 / +500).
- The demand test is the binding clause. Against V56 the rival's estimated supply is 33-77 units per 24 h, and demand is 7-43.
- Even with the oracle R, deferral fires on only 4-8 traces per set. The 8-unit cap and the shed limit it to +12..+35 own.
- **Astra's aggregate sensitivity overstated both purses 6-7x.** It gave U40 +4.6k / +4.6k / 0 and U60 +7.1k / +8.5k / -1.3k. The exact
  replay gives:
  - v21: U40 +754 / +111 / +643 and U60 +1,123 / +361 / +762;
  - m40: U40 +436 / +149 / +287 and U60 +604 / +321 / +282.
- **U's positive margin is a floor-clip effect.** Many held units would have sold at $1, and a $1 unit adds no supply. Released on d26
  above the floor, they add supply that V56's d26-28 book of about 44 units pays for.
- **U is infeasible.** Its shed peak is 141-159, displacing 12.9-23.3 units a game. Our shed is at 100 after the night drop on 103 of 504
  v21 nights.
- **With room enforced, the gain vanishes.** Room-capped reservation (hold below q while occupancy + held <= 100; all sold d28 h17), v21 /
  m40:
  - q = 2: 1.1 / 0.8 units held per game, margin +35 / +30;
  - q = 20: +25 / +36;
  - q = 40: +18 / +10.

### C. Where do paired receipts favour a timing change? (`res/grad_v21.txt`, `res/mval_v21.txt`)
**Timing gradient.** Move the last unit of each of our lots of 7 products (d12-28) one day later, or earlier to the first hour of the same
day it was in our shed. Exact paired replay, production fixed. Per-unit means:
- **Strawberry d23-28 h17 -> +24 h** (46 lots): own **+21.3**, rival **+18.8**, margin +2.5. Astra's invariant holds almost exactly.
- **Strawberry d18-22:** h17 later -19.2, h01 later -42.3.
- **Earlier moves:** every product and window is negative. Strawberry d23-28 h17 earlier: -26.4 own / -6.9 rival.
- **The only books where the rival gains less than we do** are WOOL d18-22 h17 later (+8.7 / +1.4 = **+7.3**), MILK d18-22 h17 later
  (+5.2) and TOMATO d23-28 h17 (+12.9 on 10 lots). These are coins per unit.
- **EGG:** within ±1 per unit (flat log price).
- **Beyond the gradient:** the $1-floor strawberry units of our d23-25 h17 lot favour us (held floor units cost the rival nothing and deny
  it after release: uncapped q=2 v21 own +26 / rival -294). The shed admits about 1 of them a game.

**Value of one extra unit** (+1 at our first sale of the day, v21, own / rival / margin):
- strawberry d14-18: **+3 / -201 / +204** (pure denial: our ~190 later units absorb our own price drop);
- strawberry d21: -4 / -130 / +126; strawberry d26-28: +46..+94 / -30..-67 / +113..+124;
- wool d10-13: +9 / -190 / +199; wool d26-28: +50..+78 / +103..+133 margin;
- milk d11-13: -29 / -176 / +129..+147;
- **egg d10-28: +40..+50 / -1..-7 / +47..+51.**

**Hypothesis (one line):** vs V56 no timing change at fixed production has paired receipts worth more than +7 coins per unit. The one
exception, holding the $1-floor strawberries off the supply curve, fits the shed only about once a game. The invariant stands for timing.
The margin is volume on the denial books, where +1 strawberry sold d14-18 is worth +204 margin and 0 own, against an egg's +48, and the
cheapest untaken volume is fertilizer that PFS sells.

**Evidence for the cell** (`res/strawfert_v21.txt`):
- PFS fertilizes **97 of its 128 strawberry yield events** (age 10/12/14/16, end of day). **31.3 per game are unfertilized**, 22.9 of them
  on d12-20.
- On those same days it sells fertilizer: **119 units per game at 48.5 coins**, 4-12 units a day. Fertilizer has no drain and a 0.2/unit
  slope.
- A fertilized watered yield event gives +2 instead of +1. PFS's planner admits an application only if its projected own value beats the
  unit's sale price (`v_fert`, FERT_VOLUME notes). Against V56 the own value of an extra strawberry is about 0, so the planner rationally
  sells the fertilizer. It cannot see the +200 denial.

**Round-2 cell: `STRAW_FERT_FULL=D`** (default 0 = OFF, byte-identical).
- **Rule:** for every own strawberry plant whose yield event falls at the end of day d <= D (d >= 12), with fertilized_until_day < d,
  reserve 1 fertilizer ahead of the fertilizer sale allocation and emit FERTILIZE on day d-1..d, on an idle hand turn (FARMAUDIT1: 306
  PASS hand-turns d10-19 per game).
- **Ledger** (`fertled.py`): each unfunded event gets +1 strawberry at our first strawberry sale at/after d+1 h17 and -1 fertilizer at our
  first fertilizer sale on/after d-2. Strawberry is replayed exactly. Fertilizer is linear: the lost sale, then +0.2 per removed unit on
  every later fertilizer sale of both purses.

| set | D | events funded/game | strawberry own / rival | fertilizer own / rival | own | rival | margin | traces > 0 |
|---|---|---|---|---|---|---|---|---|
| v21 | 17 | 15.0 | -9 / -2,907 | -665 / +665 | -674 | -2,242 | **+1,568** | 20/21 |
| v21 | 21 | 24.2 | +7 / -3,749 | -1,021 / +969 | -1,014 | -2,780 | **+1,766** | 19/21 |
| v21 | 26 | 30.7 | +68 / -4,083 | -1,216 / +1,104 | -1,148 | -2,979 | **+1,831** | 20/21 |
| m40 | 21 | 22.2 | +117 / -2,777 | -824 / +910 | -706 | -1,867 | **+1,160** | 26/37 |

(m40 has 37 of 40 traces: the 3 with the h23 read are excluded.)

**Proposed round-2 grid and bar:**
- **Grid:** D in {17, 21}. Build in a worktree off 8d670dad (pure PFS). OFF identity 6/6.
- **V56 v21 (21 g) + m40 (40 g), paired against the VBAND1 control rows:**
  - margin >= +1,000, t >= 2, on each set;
  - W >= 15/21 and >= 38/40;
  - own >= -1,200 (the ledger's price: our own strawberry book is flat against V56);
  - late egg / wool / milk units >= PFS;
  - strawberry units d15-17 >= PFS.
- **Then 80 g each vs p48c / pq4c / g0capsfix:** own >= +500, t >= 2. Their late strawberry price is 135-200, so there the extra units are
  own coins.
- **Kill test inside round 2:** count the events actually fertilized. Closed-loop V56 reaction is the unpriced risk.
- **Why this cell respects the five points:**
  - no d3-9 coin or tile (d12+, fertilizer PFS sells);
  - adds wall volume in d14-21;
  - animal products are untouched except fertilizer, a no-drain 0.2-slope book worth about 0 denial.


## Round 2 (16:20Z-16:45Z; orchestrator's grid + astra-brainstorm7 s1-2)

**Verdict.** STRAW_FERT_FULL is **KILLED** by the repaired ledger, and **nothing was built**.
- Corrected margin: v21 **0 (D17) / -3 (D21)**; m40 **0 / +8**. The bar was +1,000 on each set.
- At the actual end-of-day (EOD) state, PFS fertilizes **every** watered strawberry production night through d17 (0.0 unfertilized per
  game on both sets, matching YIELD1). It leaves 0.9-1.1 per game in d18-21 and 2.7-4.5 per game in d22-28.
- Round 1's 24.2 events per game came from the **h17 snapshot**. In v21, PFS makes 25 of its 60 d12-17 fertilizer applications between
  h17 and h23, and they cover all 15.0 d12-17 nights that looked unfertilized at h17.

**CARE_COMPLETE_18 census: margin +18 (v21) / +10 (m40).** PFS cares 122-130 of its 124-132 fed animal-days d10-17. Caring the remaining
1.4-2.4 would yield 0.19-0.53 extra units per game sold by d18. The prior of zero is confirmed.

**Round-3 proposal: `LATE_GOOSE=k`.** It passes a first-cut ledger on both sets but needs a tile-, shed- and labour-exact ledger before any
build (details at the end of this section).

### Traces (rec2.py)
- `S/brainstorm4/rec2.py` is `rec.py` plus, per step for our farm:
  - the before-step unit positions and op names;
  - a diff-encoded snapshot of every strawberry plant and every animal tile, with kind, what, yield, fert_until, planted/placed day,
    watered/fed, cared, consecutive_dry and pending care bonus.
- It re-recorded the same 21 v21 and 40 m40 boards (`res/t2_v21.jsonl.gz`, `res/t2_m40.jsonl.gz`). Final money is identical to the VBAND1
  control rows, 61/61.
- The EOD engine rule is checked on every production night: post yield = min(4, held + 1 + (watered and fertilized)) for plants, and
  min(max_held, held + 1 + banked bonus when fed) for animals. There are **0 misses** over 61 games.
- `grad.py` now caps every order to the recorded units instead of reading the shed. This fixes round 1's h23 night-drop read, and the milk
  and m40 books replay on 61/61.

### A. STRAW_FERT_FULL, repaired ledger (`fert2.py`, `res/fert2_*.jsonl`, `res/r2_AB.md`)
The four defects astra listed are repaired as follows:
1. **Coverage.** Production nights and coverage come from the EOD state: pre = before the h23 step, post = after it. "Watered" is post
   consecutive_dry == 0, "fertilized" is post fert_until >= d, and held yield is zero if a unit harvests the tile at h23. One added
   application sets fert_until = d+2, so it covers nights d and d+2. Gains are taken only while held + extra + 1 < 4. Extras are re-clipped
   on later nights, leave the tile at its next harvest, and sell at our first strawberry sale after that.
2. **Clock.** Everything uses the EOD state above, never the h17 snapshot.
3. **Funding.** The fertilizer must be in our shed on day d before h23, with base stock + kept - used >= 1. The unit is taken from the next
   fertilizer sale, or else from our latest d-1..d sale. Otherwise the application is unfunded.
4. **Exact fertilizer book.** Both books replay by lockstep walk: strawberry from `grad.py`, fertilizer from `fert_walk`, which includes
   both farms' BUY_PRODUCT, with bought units taken from the no-drain inventory identity. One step per game (V56's d27 h1 double sell
   around a buy) is not decomposed; it is carried as a consistent offset.

Resources are checked as well:
- Labour: our PASS unit-turns h1-22 must cover 1 + distance to the shed per application, plus one pickup.
- Shed: added units over 100 are counted.

| set | D | games | prod. nights | watered | watered+fert | watered unfert. (all days) | unwatered | cap-bound | EOD sanity misses | candidates d12-D | labour-dropped | unfunded | applications | extra strawberries sold | lost | strawberry own / rival | fertilizer own / rival (exact) | own | rival | margin | steps over 100 (added units) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v21 | 17 | 21 | 128.3 | 128.0 | 122.7 | 5.4 | 0.3 | 0.0 | 0.0 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | +0 / +0 | +0 / +0 | +0 | +0 | +0 | 0 |
| v21 | 21 | 21 | 128.3 | 128.0 | 122.7 | 5.4 | 0.3 | 0.0 | 0.0 | 0.48 | 0.29 | 0.00 | 0.19 | 0.38 | 0.00 | +0 / -5 | -4 / +4 | -4 | -1 | -3 | 3 |
| m40 | 17 | 40 | 111.4 | 111.1 | 107.3 | 3.8 | 0.3 | 0.0 | 0.0 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | +0 / +0 | +0 / +0 | +0 | +0 | +0 | 0 |
| m40 | 21 | 40 | 111.4 | 111.1 | 107.3 | 3.8 | 0.3 | 0.0 | 0.0 | 0.80 | 0.20 | 0.00 | 0.60 | 1.07 | 0.00 | +5 / -25 | -12 / +10 | -8 | -15 | +8 | 25 |

| set | games | fed animal-days d10-17 | fed but not cared | CAREs added | extra units sold by d18 (egg / milk / wool) | lost or sold after d18 | days short of PASS labour | own | rival | margin | EOD sanity misses |
|---|---|---|---|---|---|---|---|---|---|---|---|
| v21 | 21 | 123.6 | 1.43 | 1.43 | 0.19 (0.00 / 0.10 / 0.10) | 0.90 | 0.00 | -2 | -20 | +18 | 0.0 |
| m40 | 40 | 131.9 | 2.35 | 2.35 | 0.53 (0.03 / 0.50 / 0.00) | 1.25 | 0.03 | -3 | -12 | +10 | 0.0 |

**Reconciliation with round 1 and YIELD1** (`res/r2_reconcile.txt`). All figures are per game.

| set | window | production nights (EOD) | "unfertilized" at h17 (round-1 method) | unfertilized at EOD (watered) | fertilized between h17 and h23 | FERTILIZE ops at h17-23 / whole day |
|---|---|---|---|---|---|---|
| v21 | d12-17 | 52.6 | 15.0 | **0.0** | 15.0 | 25.3 / 60.2 |
| v21 | d18-21 | 52.1 | 9.2 | 0.9 | 8.3 | 16.0 / 40.9 |
| v21 | d22-28 | 23.6 | 7.1 | 4.5 | 2.6 | 31.9 / 90.0 |
| m40 | d12-17 | 49.8 | 13.9 | **0.0** | 13.9 | 25.6 / 60.0 |
| m40 | d18-21 | 45.2 | 8.6 | 1.1 | 7.4 | 15.6 / 38.4 |
| m40 | d22-28 | 16.4 | 4.2 | 2.7 | 1.5 | 33.0 / 90.2 |

The round-1 pre-screen was wrong at its first step: most of its 24.2 events per game were already fertilized between h17 and h23.
What remains is 0.19-0.60 fundable applications per game in d18-21, and it is worth nothing.

### B. CARE_COMPLETE_18 census (`care2.py`)
A CARE is added on every d10-17 day on which an animal was fed but not cared at EOD. The banked +1 is paid at that animal's next
production night if it is fed then. It is re-clipped at max_held, collected at the tile's next harvest, and counted only if sold by d18.
Each product is valued by exact paired replay. The CARE table is the second table in the `r2_AB.md` block above: **+18 / +10 margin** per
game.

### Round-3 pre-ledger: extra animals from d12
**Mechanism (`herdprobe.py`, `sheepled.py`).** Every existing PFS animal is already fed and cared, so the only herd volume left is **extra
animals**. PFS's herd stops growing at d14 (6.9 C / 3.5 G / 6.3 S at d14, unchanged at d24). PFS has idle labour (322-325 PASS unit-turns
d12-28) and money after d10.

**Model.** Each extra animal is placed on day P, fed and cared daily (as PFS does its own), and collected:
- sheep: 6 wool at P+5, then 4 every 3 days;
- cow: 6 milk at P+7, then 3 every 2 days;
- goose: 4 eggs at P+3, then 2 daily;
- all three: 1 fertilizer per day.

The product and fertilizer books are replayed exactly and paired. Costs:
- purchase: 300 / 400 / 500;
- feed: 1 wheat per day at our realised d12-28 wheat price (~35.5);
- tile: the displaced crop, charged 500 own (about a wheat relay tile over d12-28: 3 cycles x ~5 units x 36, less seeds).

P = d12 unless stated.

| set | animal x k | product units | product own / rival | fertilizer own / rival | feed / purchase / tile | **own** | **rival** | **margin** | margin > 0 | shed steps > 100 per game (max excess) | labour vs PASS d12-28 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| v21 | sheep x1 | 18 wool | +318 / -1,250 | +398 / -250 | -604 / -500 / -500 | -887 | -1,500 | +613 | 12/21 | - | 57 / 325 |
| v21 | cow x1 | 18 milk | +47 / -1,189 | +398 / -250 | -604 / -400 / -500 | -1,058 | -1,439 | +381 | 13/21 | - | 57 / 325 |
| v21 | goose x1 | 30 eggs | +1,356 / -91 | +398 / -250 | -604 / -300 / -500 | **+351** | -341 | **+692** | 21/21 | - | 57 / 325 |
| v21 | goose x2 | 60 eggs | +2,676 / -165 | +754 / -499 | -1,208 / -600 / -1,000 | **+622** | -664 | **+1,287** | 21/21 | 10.9 (14) | 113 / 325 |
| v21 | goose x3 | 90 eggs | +3,966 / -231 | +1,070 / -739 | -1,812 / -900 / -1,500 | **+824** | -970 | **+1,794** | 21/21 | 14.3 (21) | 170 / 325 |
| m40 | sheep x1 | 18 wool | +422 / -998 | +337 / -228 | -600 / -500 / -500 | -842 | -1,225 | +384 | 20/40 | - | 57 / 322 |
| m40 | goose x1 | 29 eggs | +1,348 / -52 | +337 / -228 | -600 / -300 / -500 | +284 | -280 | +564 | 37/40 | - | 57 / 322 |
| m40 | goose x2 | 57 eggs | +2,646 / -108 | +637 / -446 | -1,201 / -600 / -1,000 | **+483** | -553 | **+1,036** | 37/40 | 14.0 (41) | 113 / 322 |
| m40 | goose x3 | 86 eggs | +3,887 / -166 | +905 / -654 | -1,801 / -900 / -1,500 | **+591** | -820 | **+1,411** | 37/40 | 16.9 (63) | 170 / 322 |
| m40 | goose x3, P=d11 | 92 eggs | +4,124 / -189 | +1,000 / -740 | -1,907 / -900 / -1,500 | +817 | -929 | +1,746 | 38/40 | - | 180 / 322 |

- **Sheep and cows.** Their wool and milk carry large denial (-1.0k to -1.25k to V56 per animal). Their own coins do not cover purchase,
  feed and tile, so their margin is +0.4-0.6k per animal and positive in only half the games.
- **Geese.** They are the only extra animal that is own-positive after costs. Eggs hold about 44 coins per unit and V56 barely sells eggs.
  The fertilizer they drop adds about +0.25k of fertilizer denial per goose. PFS's own-coin planner buys only 1.5 geese on d10-14, even
  though the ledger values each extra goose at +0.3k own.
- **Risks:**
  - The tile charge decides the sign of own. At a 700-coin tile, k=3 own falls to about +0.0-0.2k.
  - The shed: held extras cross 100 on 11-17 steps per game in this crude timing, which assumes each extra sits in the shed from dawn.
  - Labour: 113-170 of the 322-325 idle unit-turns are needed.
  - GEESE1 (09-19) closed an early-geese target as a gift on the old judge.
  - Clones under-sell eggs to 30-43 % of the real P48 figure, so the egg price against real P48 is unknown.

**Round-3 cell: `LATE_GOOSE=k`** (default 0 = OFF).
- **Rule:** on d11-12, buy k geese beyond PFS's own purchases. Build a coop on each of the first k tiles freed by a harvest, taking them
  before PFS replants. Include the geese in PFS's feed, care and collect routines, with k more feed wheat reserved per day.
- **Grid:** k in {2, 3}.
- **Ledger v2, first:**
  - the displaced crop is the one PFS actually planted on that tile (its harvests and sales repriced exactly);
  - eggs stay on the tile until PFS's actual collection cadence (held cap 4);
  - shed room with overflow protection, with 0 displaced;
  - route-feasible labour.
- **Ledger bar:** margin >= +1,000 and own >= 0 on EACH set.
- **Then build (worktree off 8d670dad), OFF identity 6/6.** V56 v21 + m40 closed loop: margin >= +1,000 at t >= 2, W >= 15/21 and >= 38/40,
  own >= 0, late egg / wool / milk >= PFS. Then 80 games against p48c / pq4c / g0capsfix: own >= +500 at t >= 2 and margin >= 0.

### Round-2 hypothesis check
**The orchestrator's hypothesis ("survives at about half") fails.** Two-night coverage never came into play, because the EOD state leaves no
d12-17 night uncovered. The corrected margin is about 0, not +500-1,000, so it is not PROMISING. The general finding stands and extends:
through d21, PFS's own production is complete on fertilizer, water, care and the held cap. Late volume can only come from extra production
units: extra animals, or tiles, which are full. Among extra animals only geese pay their own way.


## Round 3 (16:47Z-17:10Z; orchestrator's grid + astra-brainstorm8 s1)

**Verdict: LATE_GOOSE is KILLED by ledger v2 for k = 2 and k = 3. Nothing was built.**
- **First killing term: the coop tile's cost to both purses, measured exactly.** C is our own loss, R the rival's gain. v21: C 1,460 / 2,273, R 365 / 586 (k = 2 / 3). m40: C 1,385 / 2,242, R 777 / 1,399.
- **Margin fails even with free labour.** Add those measured C and R to astra's round-2 pre-ledger with a zero tile charge: v21 margin +462 / +435 and m40 -126 / -729, all below +1,000. Own sits at about 0 (+162 / +51 on v21, +98 / -151 on m40).
- **Second term: actions.** PFS's idle PASS runs cannot carry the routine: a goose is placed by d12 in 4/21 and 5/40 games at k=1, and in at most 2/40 at k ≥ 2. The priced alternative, one extra hand hired each day after PFS's last hire, costs exactly **1,867 (v21) / 2,198 (m40) per game**. With it, every cell is about -1.4k to -2.9k in margin.
- **Engine run with the hired tender:** own **-2,876 / -4,165** and margin **-3,207 / -4,803** on v21; own **-3,243 / -4,545** and margin **-4,284 / -6,268** on m40. Margin is > 0 in 0 of 61 games in every cell.

### Method: an engine-exact counterfactual (`goose_cf.py`, `goose_routes.py`, traces `rec3.py`)
- **Traces.** `rec3.py` = `rec2.py` plus the raw actions of both seats per step (`res/t3_*.jsonl.gz`). An open-loop replay of both seats'
  recorded actions in the fastenv reproduces final money exactly: **baseline identity 61/61**. VBAND1 control money is also 61/61.
- **Counterfactual.** The same replay with OUR actions edited. The rival's actions are untouched (fixed flows). Both purses' final money
  deltas therefore contain every book exactly, including the repricing of every product for both farms. `sales()` deltas decompose them.
- **Placement rule (one rule, no oracle).** The coop sites are the first k of our recorded PLANT WHEAT/CARROT actions on d11 h0-d12 h22.
  The same unit builds a coop instead. The displaced crop and every later use PFS made of that tile then vanish (later
  PLANT/WATER/FERTILIZE there are engine no-ops). Sites not stocked by d12 are cancelled.
- **Wheat-neutral rule (feed and displaced wheat, no double count).** Whenever our shed wheat falls below the baseline's, the deficit is
  bought (BUY_PRODUCT WHEAT, exact price walk). A surplus is added to our next wheat sale. PFS's own animals therefore stay fed. Without this
  rule, the open-loop replay of two wheat-site coops starved PFS's herd: game 1 lost 17 milk and 7 wool, own -3,236.
- **Sites only (no geese)** measures the tile cost exactly: C = -Δown and R = Δrival. It includes the seeds, work and wheat freed by
  the displaced crop. (Astra's bounds, m40: own ≥ 0 needs C ≤ 1,483 / 2,091; margin ≥ 1,000 needs C + R ≤ 1,036 / 1,911.)
- **Routes (`goose_routes.py`).** Minimal daily routine: FEED + CARE. The first variant draws on PFS's PASS runs. A run may start anywhere;
  the unit walks to the shed for wheat (and the goose on placement day), then tours the coops, and walks back unless the run ends at h23.
  Alternatively, a unit already carrying wheat from its own recorded pickup can serve from a later run.
- **Hired tender.** When the PASS runs fail, one hand is hired each day after PFS's last hire, so no index shifts. It spawns on a
  shed-access tile. That same step it buys the day's feed wheat (and the geese on d11-12). It then walks PICKUP → coops
  (PLACE / FEED / CARE / COLLECT_FERTILIZER / HARVEST) → shed and DROPs. Extra eggs and manure ride PFS's own sale orders, raised by the
  shed surplus.

**Tile-choice rule of this ledger** (for comparison with GOOSE1's placement; the per-game site list is `res/goose_sites.md`):
- **Which tiles:** the first k of OUR recorded PLANT actions whose crop is WHEAT or CARROT, taken in step order and then unit index, from
  d11 h0 to d12 h22.
- **Where:** the tile under the planting unit. It is EMPTY at that moment, because it is a harvested tile being replanted.
- **Edit:** the same unit issues BUILD_COOP instead of that PLANT. The goose is bought and placed later the same day.
- **Result:** all 183 sites (61 games x 3) are **WHEAT replants on d11, between h7 and h16**. They lie 4-6 steps from the nearest
  shed-access tile: mostly the south edge (x 0-4, y 7-9), plus some north-west and north-east tiles such as (0,3) and (8,1).
- **k=2** uses the first two sites of the k=3 list.
- **Cost measured:** C / R is the loss of each tile's later rotations. Those rotations are the ones PFS actually made on it, so they
  include later melon, strawberry, carrot and tomato plantings and, on m40, a pasture.

**Idle-run feasibility** (`res/goose_routes_*.txt`):

| set | k | placed by d12 on idle runs | goose-days served after placement | games with ≥ 2 unserved days in a row (escape) | extra hand every day d12-28 (exact cost, fib of PFS's daily hire count) |
|---|---|---|---|---|---|
| v21 | 1 | 4/21 | 29/65 (45 %) | 4/4 | 1,867 |
| v21 | 2 / 3 | 0/21 | - | - | 1,867 |
| m40 | 1 | 5/40 | 28/82 (34 %) | 5/5 | 2,198 |
| m40 | 2 / 3 | 2/40 and 1/40 | 5/32 and 1/16 | all | 2,198 |

PFS's idle time comes as 3-9-turn fragments at the end of the day, on 1-3 units. A coop sits 4.3-4.9 steps from the shed, and every day
needs a wheat pickup at the shed. The goose routine does not fit into those fragments.

**Engine books** (`res/goose_summary.md`; per game; own / rival coins per product):

| set | mode | k | games | ident | own | rival | margin | margin > 0 | own spend (geese, feed, hires, neutral wheat) | WHEAT own/riv | CARRO own/riv | TOMAT own/riv | STRAW own/riv | MELON own/riv | EGG own/riv | MILK own/riv | WOOL own/riv | FERTI own/riv | hires | escapes | geese alive d29 | shed peak / base | extra full nights |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v21 | sites only (C, R) | 2 | 21 | 21 | -1460 | +365 | -1825 | 0/21 | +924 | +268/+243 | -176/+20 | -187/+39 | -195/+99 | -326/+0 | -16/+3 | +22/+9 | -93/+64 | +166/-146 | 0.0 | 0 | 0.00 | 100 / 100 | -1.24 |
| v21 | sites only (C, R) | 3 | 21 | 21 | -2273 | +586 | -2859 | 0/21 | +1322 | +340/+348 | -230/+26 | -200/+48 | -342/+136 | -652/+0 | -38/+4 | +27/+31 | -88/+149 | +232/-205 | 0.0 | 0 | 0.00 | 100 / 100 | -1.19 |
| m40 | sites only (C, R) | 2 | 40 | 40 | -1385 | +777 | -2162 | 0/40 | +888 | +290/+410 | -170/+26 | -186/+46 | -197/+37 | -400/+0 | -8/+0 | +8/+29 | +28/+517 | +138/-133 | 0.0 | 0 | 0.00 | 100 / 100 | -1.70 |
| m40 | sites only (C, R) | 3 | 40 | 40 | -2242 | +1399 | -3640 | 0/40 | +1440 | +442/+599 | -255/+36 | -218/+75 | -259/+78 | -643/+0 | -29/+1 | +4/+240 | -39/+778 | +195/-192 | 0.0 | 0 | 0.00 | 100 / 100 | -2.02 |
| v21 | hired tender | 2 | 21 | 21 | -2876 | +331 | -3207 | 0/21 | +4418 | +623/+485 | -274/+33 | -204/+44 | -299/+168 | -375/+0 | +1548/-92 | +20/+35 | -109/+91 | +611/-586 | 16.2 | 4 | 1.52 | 100 / 100 | +2.19 |
| v21 | hired tender | 3 | 21 | 21 | -4165 | +638 | -4803 | 0/21 | +5326 | +744/+614 | -287/+33 | -222/+48 | -456/+227 | -715/+0 | +1502/-89 | +22/+57 | -110/+237 | +682/-659 | 16.2 | 4 | 1.76 | 100 / 100 | +2.00 |
| m40 | hired tender | 2 | 40 | 40 | -3243 | +1041 | -4284 | 0/40 | +4437 | +604/+778 | -227/+33 | -206/+46 | -294/+110 | -527/+0 | +1393/-54 | -5/+74 | -27/+726 | +482/-499 | 14.3 | 17 | 1.32 | 100 / 100 | +1.07 |
| m40 | hired tender | 3 | 40 | 40 | -4545 | +1723 | -6268 | 0/40 | +5419 | +788/+989 | -322/+46 | -235/+78 | -322/+167 | -775/+0 | +1315/-49 | -10/+297 | -90/+991 | +526/-548 | 14.3 | 19 | 1.48 | 100 / 100 | +1.18 |

- **Reading the sites-only rows.** Removing two or three d11-12 wheat/carrot replants loses more than the wheat. The tile's later
  rotations go too: melon -326 to -775, strawberry -195 to -456, carrot, tomato. So do, on m40, a later pasture that PFS would have
  built there, which is why rival wool rises by +517 / +778. The rival gains R = 365-1,399.
- **Reading the hired-tender rows.** The engine also loses geese: 4/21 and 17-19/40 games have an escape, and 1.3-1.8 geese per game are
  alive at d29. This happens on days when PFS's last hire is too late for the tender's route. Those rows are therefore pessimistic about
  eggs: +1.3-1.5k, against the round-2 pre-ledger's +2.7-4.0k.

**Composite bound (the fair statement).** Astra's round-2 pre-ledger (eggs, manure, feed, purchase; tile charge 0), plus the measured
C and R, plus the exact hire cost:

| set, k | pre-ledger own / margin (tile 0) | - C (own), - C - R (margin) | = with free labour | - hired tender | = with priced labour |
|---|---|---|---|---|---|
| v21, 2 | +1,622 / +2,287 | -1,460 / -1,825 | **+162 / +462** | -1,867 | **-1,705 / -1,405** |
| v21, 3 | +2,324 / +3,294 | -2,273 / -2,859 | **+51 / +435** | -1,867 | **-1,816 / -1,432** |
| m40, 2 | +1,483 / +2,036 | -1,385 / -2,162 | **+98 / -126** | -2,198 | **-2,100 / -2,324** |
| m40, 3 | +2,091 / +2,911 | -2,242 / -3,640 | **-151 / -729** | -2,198 | **-2,349 / -2,927** |

**Which term killed it.**
1. **C + R.** Each coop tile's rotations over d11-29 are worth about 700-750 own coins to us, plus 180-470 to the rival when removed.
   Even with free labour, margin fails the bar on both sets.
2. **Actions.** The routine does not fit PFS's idle fragments, and a daily tender costs 1.9-2.2k.

Feed is covered by the wheat-neutral rule and is not a separate killer. Displacement: the shed peak stays at 100 (same as base), with
+1-2 more full nights per game in the tender runs.

**The orchestrator's round-3 hypothesis fails** ("survives at k=2, not k=3"). Neither k survives. The tile is the price, not the second
coop's feed wheat.

## Session summary (BRAINSTORM4, three rounds, 15:44Z-17:10Z)
1. **Timing is closed against V56 at fixed production.**
   - Exact paired unit replay: no timing move is worth more than +7 coins/unit.
   - STRAW_WAIT1 fired 0 times in 61 traces. The one invariant-breaking lever (holding $1-floor strawberries) is shed-bound at +10..+36.
2. **Margin against V56 is volume on the denial books** (+1 strawberry on d14-18 = +204 margin at +3 own). PFS's own production is
   **complete through d21** at the end-of-day state: fertilizer 100 % to d17, care 99 %, water, and the held cap.
3. **Added production units cost at least what they return.**
   - Each coop/pasture tile carries about 700-760 own coins of rotations, and removing them hands the rival 180-470. PFS's idle labour comes in unusable
     fragments, and a daily hand costs 1.9-2.2k.
   - Result: LATE_GOOSE (the only own-positive animal) fails; sheep and cows fail earlier.
   - PFS sits at a tile-and-labour optimum that no PFS-internal cell of this session could beat.
4. **Tools left for the next session:** the per-step trace recorder with raw actions (`rec3.py`), the engine-exact open-loop counterfactual
   (`goose_cf.py`), the exact paired book walks (`grad.py`, `fert2.py`), and the end-of-day yield / care census.

**BRAINSTORM5 first cell (astra's seed, agreed): PLANTGAP1.** Explain and reproduce the port's missing 27.6 productive tiles
(P48GRAPH4: 41.6 vs 69.2 productive, 14.4 vs 18.4 herd) before reopening programme-transfer economics. By this session's finding, a tile's
yield is the binding currency, and the programme gets 28 more of them from the same map.
