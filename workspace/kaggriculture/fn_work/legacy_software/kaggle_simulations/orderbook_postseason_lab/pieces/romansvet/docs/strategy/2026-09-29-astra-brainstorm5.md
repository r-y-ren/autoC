# ASTRA BRAINSTORM 5 — third participant: BRAINSTORM3 round-2 review (STRAW_WALL accounting, EARLY_COW_TILE preferred, session-3 verdict draft)
Date: 2026-09-29 15:08-15:11Z | Model: gpt-6-astra (reasoning high, read-only, ephemeral) | Prompt: S/astra_bs5/prompt.md

**1. STRAW_WALL’s +3k forecast does not survive accounting for our full strawberry book.** Preserving PFS’s supply is established; profitable expansion beyond PFS is untested.

The measured response is not one linear slope. On v21, PFS→G2 gives **19.5/20.3 = 0.96 coins/unit**; G2→CLS gives **26.2/9.3 = 2.82**. These interventions also change our later production. Neither identifies the effect of adding 10–30 units above PFS. [VCHECK1](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-29-vcheck1.md)

The instantaneous curve is **−1.92 coins/inventory-unit above I0**, until the **1-coin floor**; below I0 it uses a square root. Town demand is **1/day**, plus **6/day per strawberry shop**. Demand changes which curve segment subsequent sales encounter; ten additional units do not mechanically “expire after ten days,” because both counterfactuals experience demand. Floor-priced sales add no inventory. [Curve](/mnt/e/_work/kaggriculture3/src/kagg3/spec.py:154), [sale mechanics](/mnt/e/_work/kaggriculture3/src/kagg3/sim/market.py:94)

Our exposed book is **191 late units on v21 / 163 on m40**, besides approximately 50 early units—not just those 50. A uniform 15-coin late-price reduction costs us **2,865 / 2,445**, before new-unit revenue. V56 loses **3,120** on 208 units: the late-book margin advantage is only **255 / 675**.

Here is a corrected **sensitivity calculation, not an identified full-game expectation**. Assume `q=2.5n`, extra early units initially worth 190, common slope 1.5, our late exposure 191, and half of our 50 early units exposed. Include seeds and marginal-unit price pressure:

`Δmargin ≈ 190q − 100n + 1.5q(R − 216) − 0.75q²`.

| Total extra tiles n | Early units q | Δown | Δmargin V56, R=208 | P48, R=155 | PQ4, R=168 |
|---:|---:|---:|---:|---:|---:|
| 2 | 5 | −889 | +671 | +274 | +371 |
| 4 | 10 | −1,815 | +1,305 | +510 | +705 |
| 6 | 15 | −2,779 | +1,901 | +709 | +1,001 |

P48/PQ4 columns hold our exposure and slope constant **only for comparison**; their actual values need measurement. Additional later harvests contribute revenue **and further repricing**; care, displaced production and rival reactions remain excluded. Thus **+3k V56 / +2k P48 at n=4 is not a supported expectation**.

Resource accounting must precede games:

- Define **n total additional plantings across d5–7**, not +n each dawn; otherwise the advertised dose can triple.
- Seeds cost **200/400/600**. KEEP’s priority supplies no new cash: reserve baseline seeds, feed, land, animals and hires first; admit extras only from the remainder.
- A free Q2 tile today may be committed tomorrow. Reserve its occupancy through the strawberry’s four production events, ages **10/12/14/16**.
- Survival requires watering without two consecutive missed days: roughly **5n watering actions before first yield**, plus planting, harvesting, travel and subsequent care. No additional hands are free.

DRAWREACT2 already found **+7.9 tiles/shop** in PFS and strawberry-expansion own losses of **−4.9k / −8.6k** in two cells. Those larger substitutions do not reject a capped wall, but they reject “own approximately flat” as the default. [DRAWREACT2](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-29-drawreact2.md)

**Amended grid:** audit the 12 prefixes first; test total caps **n={0,2,4}**, dropping 6. Preserve all baseline commitments; log actual extra plantings and sales. Require OFF identity **6/6**. V56 bars: v21 **Δmargin≥1,000, paired t≥2, W≥13**; m40 **Δmargin≥0, W≥38**; both **Δown≥−500**, d15–17 units **≥PFS+2n**, no protected-sale delays or extra escapes. Select at most one dose, then run **80 games each** against p48c/pq4c/g0capsfix with **Δmargin≥0, Δown≥−500, W≥control**. These clone reads establish tolerability, not transfer to 155/168-unit rivals.

**2. I prefer `EARLY_COW_TILE=1` for the last round.**

Exact proposed semantics: pure PFS; at most **one cow advanced per game**, during **d3–4**, after realized receipts. Use a just-harvested NW wheat/carrot tile only when its replacement crop has a reserved feasible placement. Buy only with **400 plus incremental feed** remaining after protected commitments, and a feasible pasture/placement route using idle work. Count the cow toward subsequent PFS targets; never add a compensating cow. No dawn stock floor, seed-priority override or replay-only future information.

The **10/12 ledger** supports feasibility; it does not establish that a live executor can reproduce those choices. The failed dawn implementation’s **−4,781 margin** is evidence against that implementation, not against the midday transaction. [Round 2](/mnt/e/_work/kaggriculture3/S/astra_bs5/round2_excerpt.md)

Grid: **OFF/ON × first 10 preregistered boards × V56/p48c = 40 games**, one seat. Include ineligible boards as no-ops. Bar: pooled **Δown≥200, board-clustered t≥2**, **Δmargin≥0 in each rival family**, unchanged total cow purchases, no strawberry/melon sale delays, no extra escapes. This is a mechanism screen; promotion still requires larger reads.

My subjective **P(pass)=35%** for that screen, versus **15%** for STRAW_WALL clearing the amended full sequence. These are decision priors, not fitted probabilities; EARLY_COW_TILE’s chance of clearing STRAW_WALL’s **+1k V56** bar is **≤10%**. I prefer its bounded **36–46-hour advance** and testable funding source.

**3. Session-3 verdict draft:**

- **Determinant:** strawberry supply sold before the rival wave controls a large shared revenue book; reducing ours **51→21** moved V56’s late price **89→135**. This establishes preservation, not unlimited expansion.
- **KEEP:** restores strawberry timing and price. G2+KEEP gives V margins **+422/−569**; CLS+KEEP still loses **−1,958**, including rival wool **+2,656**.
- **Reinvestment closed:** protecting seeds leaves only approximately **+0.3 cows/+0.3 sheep/+0.6 geese**; clone own gains **+413/+566** miss the **+1.5k, t≥2** bar.
- **Tile use:** **10/12** prefixes permit a midday cow advance; dawn stock floors cannot express it without funding changes.
- **Open:** expansion beyond PFS, executor feasibility, ESHEAD’s VCHECK2, and faithful programme transfer. P48GRAPH3 still has **42.8/69.2 productive tiles**, Q3 d8 **2/16**; gate 1 remains unmet.
- **BRAINSTORM4 seed:** measure **timing at fixed lifetime production**—advance existing plantings or receipts while pricing both books, with board-stratified demand and faithful-rival confirmation.

**4. Round 2 does not change the two-PFS-copies recommendation:** neither KEEP nor held bs2lp establishes a replacement gain. ESHEAD’s **+4,880 own/+1,498 margin** clone result remains pending VCHECK2; one FIFO upload would retire PFS and leave CLS live, so restoring **PFS+PFS** still requires two uploads.

## Prompt

## ASTRA BRAINSTORM 5 (2026-09-29 15:05Z) — third participant: BRAINSTORM3 round 2 review, before the final round 3

You are the standing third participant of BRAINSTORM3. Repo /mnt/e/_work/kaggriculture3 (read-only). Read first: docs/strategy/2026-09-29-astra-brainstorm4.md (your round-1 review incl. its prompt with the full context), S/astra_bs5/round2_excerpt.md (round 2 of docs/strategy/2026-09-29-brainstorm3.md), docs/strategy/2026-09-29-vcheck1.md, docs/strategy/2026-09-29-esheadcl1.md (a third candidate: head offsets, m76 own +4,880 margin +1,498, V56 read running as VCHECK2), and the tail of S/p48graph3/checkpoint.txt (the port with P48's own d0; gate 1 pending).

### Round-2 result
KEEP restores the wall: on V56's live boards our d15-17 strawberries 21 -> 50 (CLS) / 31 -> 48 (G2) and V56's late price 135 / 109 -> 90 (PFS 89). G2+KEEP passes V56 (v21 W 13 -> 17, margin +422; m40 W 38 = 38, margin -569) but on the TRANSFER3 screen it is harmless, not a gain (p48c own +413 t 0.6 margin -169; g0capsfix own +566 margin +1,124): with the seeds kept, reinvestment adds +0.3 cows / +0.3 sheep / +0.6 geese by d9. The d5-9 seed coins were the purse; the reinvest line is closed. CLS+KEEP fails v21 on wool (cows-first leaves 2.6 sheep; V56 wool +2,656). EARLY_COW_TILE: ledger 10/12 feasible (a d3 h15 cow on a just-harvested wheat tile, 36-46 h before PFS's d5 cow) but no planner switch can express it (the HERD_PLAN floor buys at d3 h1 with the strawberry seeds, -4.8k); it needs a mid-day executor buy; not built. Agent's round-3 proposal: STRAW_WALL="<n>:5:7" on PURE PFS: +n in {2,4,6} strawberry tiles planted d5-7 from free Q2 slots (never melon/animal tiles) with KEEP's seed priority; measured slope ~1.5 coins of V56 late price per extra d15-17 unit we sell -> ~250-320 rival coins per unit, own ~flat; +4 tiles ~ +10 units ~ +3k margin vs V56 (planning); V56 v21 + m40 first (v21 margin >= +1k t >= 2, W >= 13; m40 margin >= 0, W >= 37; strawberries >= PFS + 2n), then 80 g each vs p48c / pq4c / g0capsfix (margin >= 0, own >= -500). Facts to weigh: the town center absorbs 1 unit/product/24 turns; V56's wave is 208 units d18-29 fixed; P48's is 155, PQ4's 168, Majkel's 189; our own late strawberries also sell into the same book (price pressure on our own units); PFS's strawberry planting scales with the shop draw already (DRAWREACT2: +7.9 tiles per shop, same as the programme); the invariant "our late volume is our denial" was established from V losses = rich-town draws (VLOSS1).

### Deliver (markdown, ≤ 1,200 words, numbers not adjectives)
1. STRAW_WALL critique: is the 1.5 coins/unit slope linear over +10..+30 units, what do our own strawberry units lose in price, where do the +n tiles' seeds/hands/water come from without touching melons/animals, and what is the expected margin vs V56 / P48 / PQ4 per n with the price pressure on our own book? Amend the grid/bars if needed (exact).
2. The round-3 choice (the session's last round): STRAW_WALL vs one alternative you would prefer (exact switch, grid, bar, P(pass)), and why.
3. Session-3 verdict draft in ≤ 6 bullets (what is established: the determinant, KEEP, the closed reinvest line, the tile-use finding; what is open), and the seed for BRAINSTORM4.
4. Slot: with vrp21_clsearch live and V-losing, bs2lp and esheadcl held, the two-PFS-copies recommendation standing: does anything in round 2 change it (2 sentences)?
