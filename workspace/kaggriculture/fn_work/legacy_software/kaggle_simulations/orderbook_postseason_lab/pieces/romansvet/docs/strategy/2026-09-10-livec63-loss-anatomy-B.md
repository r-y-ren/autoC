# LIVE-C63 loss anatomy — independent second read (B)

Blind re-derivation. Judge **LIVE-C63** = the full ≥2300 pool of live sub 56140532 (63 pinned
boards, 24 L / 39 W live). Theta `flow172_g940.npy` + `OPEN_PUMP_ON,TAIL_FILL_ON,BANK_BEFORE_LOT_ON`,
worktree `arms-next`, `--seed-base 777001 --seed-per-opponent`, pinned towns.
**Reproduction: 126/126 rows byte-exact** vs `S/lossflip/g940pair_livec.csv` (all 7 columns);
ledgers from `scripts/replay_profile.py`.

Record **79/126 games = 62.7 %, margin +3,212 SE 718**; **40 W / 23 L** by board (one flips vs live).
8 of 63 boards differ between seats (shop draw), one flips — seat is not a driver. Loss margins
median **−3,749**, mean −4,496; **11 of 23 inside 3 k**, 15 inside 5 k.

## 1. Day band and product — the split is d15–29, and it is 62 % ours

Revenue, ours − theirs (Welch across boards):

| band | LOSS (23) | WIN (40) | L−W (SE) | t |
|---|---|---|---|---|
| d0–9 | +1,199 | +848 | +351 (201) | +1.75 |
| d10–14 | −22,206 | −21,991 | −215 (492) | −0.44 |
| **d15–29** | **+15,911** | **+28,341** | **−12,430 (1,391)** | **−8.94** |

The d10–14 melon hole is a **flat tax** — identical on boards we win, as TOPB records. Purse split
of the d15–29 swing: **ours 99,913 → 107,666 (−7,753, t −1.43)**, theirs 84,002 → 79,325 (+4,677,
t +0.95) — 62 % is our own purse. Product margin (all days), only two separate:

| product | LOSS | WIN | L−W (SE) | t |
|---|---|---|---|---|
| WOOL | −6,937 | −198 | **−6,739 (1,710)** | **−3.94** |
| TOMATO | +831 | +5,640 | **−4,808 (1,292)** | **−3.72** |
| FERTILIZER | −7,401 | −6,977 | −423 (699) | −0.61 |
| MELON | −3,317 | −3,276 | −41 (194) | −0.21 |

The other five products are ≤ ±1.6 k at |t| ≤ 1.3. FERT (−7.2 k/board) and MELON (−3.3 k/board)
are level taxes, not discriminators.

## 2. Losses cluster on the **shop draw**, and it is visible before day 10

| board feature | LOSS | WIN | t |
|---|---|---|---|
| FARMERS_MARKET count | 0.65 | 1.25 | −2.64 |
| ICE_CREAM_SHOP | 1.48 | 0.82 | +2.16 |
| SMOOTHIE_SHOP | 1.30 | 0.80 | +2.03 |
| YARN_STORE | 0.83 | 1.12 | −1.36 |
| `towncons_TOMATO` | 170 | 270 | −3.71 |
| `towncons_STRAW` / `_MILK` | 495 / 391 | 425 / 307 | +2.39 / +2.36 |
| opponent rating | 2508 | 2474 | +2.00 |

Nothing in their build separates (melon 12.0, plant 236, sheep 7.0, hires 263; |t| ≤ 1.3).
**Sink index** = FM + YARN − ICE_CREAM − SMOOTHIE: L −1.30 vs W +0.75, r(margin) **+0.408**, ≥ 0 →
73 % correct. Restricted to the **d3/d6/d9 unlocks** (all that is knowable pre-day-10) it still
reads **L −0.87 vs W +0.28, t −3.88, r +0.386, 71.4 % vs a 63.5 % base**. Our own pre-d10 state
carries none: d10 money margin t −0.32, our d10 cash t +0.85, hands t +0.52, quads t 0.00.
**The predictor is the town, not us.**

## 3. The one own-purse bucket: wool **volume**, not price

Our coins/unit matches or beats theirs in every yarn bucket — not a price gap:

| YARN_STORE count | n | our sheep / theirs | our wool u / theirs | our ppu / theirs | wool margin |
|---|---|---|---|---|---|
| 0 | 20 | 3.7 / 6.0 | 56 / 161 | 67 / 48 | −4,012 |
| 1 | 28 | 6.6 / 6.8 | 131 / 178 | 132 / 131 | −5,207 |
| 2 | 11 | 11.2 / 8.6 | 237 / 219 | 190 / 190 | **+4,106** |

Their herd is flat (6.0/6.8/8.6); ours is a step function that under-shoots until two yarn stores
appear — and the bucket where we out-build them is the one we win. On the **16 YARN≥1 loss boards**
we sell 123 u to their 188 at 136/u = **8.9 k gross**; net of pasture/feed/labour expect **2–3 k**,
the size that flips 11 of 23 losses. Whole-set wool margin −2,658 SE 1,049 **t −2.54**.

## 4. Smallest paired test — and the archive says it is nearly closed

One constant, `SHEEP_FLOOR`: with ≥1 YARN_STORE unlocked, floor the sheep want at 8 (their level).
Paired on LIVE-C63 (63 boards × 2 seats, ~25 min at 6 workers) against this theta+switch set, then
the LIVE55/TOPB veto.

Archive: today's verdicts close the **turn** form (`WOOL_FIRST_LOT_ON` 10:37Z — TOPB level, LIVE55
89.1 → 81.8 %) and the **day** form (`WOOL_SINK_HOLD_ON` 10:48Z — no-op, hold decodes 0–87 vs a
160–200 marginal); both entries name the residue "when wool **LANDS** = sheep timing/count = herd
family, closed as a hand lever; ES's `animal_want` gene owns it". `ANIMAL_DEFER` −28 k on TOPB;
herd-mix/herd-latency closed 2026-09-06/07. The **count** form gated on a live sink is the only
unmeasured variant, inside a family closed in every other form — worth one 40-minute screen, not a
build. If it reads level, LIVE-C63's losses are a **board draw** (the sink index explains 17 % of
margin variance) and the next honest target is the flat FERT/hire tax, not wool.
