# Is the flow172 lineage drifting from the top tier? g200 vs g170c on TOPB

Judge: **TOPB**, 20 held-out pinned top-ten tapes, 40 seats, engine csvs `S/lossflip/*_topb.csv`.
The sim (`S/topbdrift/anat_topb.py`) is descriptive — mean |Δ| 800 coins, and it reproduces the
g200−g170c delta at corr 0.87.

## Lineage vs base (engine, paired)

| theta | TOPB dMARG (SE, t) | TOPB ours/theirs | win | LIVE55 dMARG | LIVE55 ours/theirs | win |
|---|---|---|---|---|---|---|
| g60 | +2,628 (1554, +1.69) | +3,720 / **+1,092** | 35 % | +4,592 | +3,372 / −1,220 | 58.2 % |
| g170c | +2,692 (1506, +1.79) | +3,666 / **+974** | 35 % | +5,534 | +3,333 / −2,201 | 65.5 % |
| g200 | +1,868 (1559, +1.20) | +2,632 / **+764** | 20 % | +5,421 | +3,200 / −2,222 | 65.5 % |

## Q1 — dropped seats: 3 boards x 2 seats, zero gains

| board | opponent | tape opening d0 | g170c | g200 | Δours | Δtheirs |
|---|---|---|---|---|---|---|
| 107244033 | SpaTaro #2 2999.9 | 6 hires d0 +6 d1; 7 melon/7 wheat; 2 cow 2 sheep; BUY 14+12+10 WHEAT | **+5,739** | −7,225 | −13,141 | −177 |
| 107242091 | Himanshu Kumar #3 2994.1 | self-pump BUY/SELL 13 WHEAT h0+h1; 5 hires h1; 12 melon 7 wheat | +790 | −53 | −580 | +263 |
| 107251183 | cooked #7 2943.7 | same clone + 5-wheat churn every hour h4–h11 | +1,091 | −243 | −636 | +698 |

Two were coin-flip seats (g170c margin ≤ 1.1 k); only SpaTaro is a real loss.


## Q2 — two-purse: not backfiring denial

| g200 − g170c | ours | theirs | margin |
|---|---|---|---|
| TOPB (40) | −1,034 | −210 | −824 |
| LIVE55 (110) | −134 | −21 | −113 |

Both purses fall — the drop is **our purse**, not denial handed back. The band/top-tier asymmetry
is real but **lineage-wide**: vs the band the lineage takes 2.2 k off the opponent, vs the top tier
it hands them 0.8–1.1 k, already at g60. LIVE55 margin is ~2x optimistic vs the top tier.

## Q3 — day bands and channels (sim, g200 − g170c, coins opened)

| band | all 40 | 3 drop boards | other 17 |
|---|---|---|---|
| d0–9 | −84 | −51 | −90 |
| d10–14 | −316 | −1,510 | −105 |
| d15–19 | +75 | −982 | +261 |
| d20–29 | −445 | −2,011 | −168 |

Openings identical (9 wheat/10 carrot, 1 goose/4 cow/1 sheep, 53-wheat pump, 4 hires d0+d1); nothing
moves before d10. Channels, all 40: WOOL −2.4 u (−494), EGG −5.2 u (−280), STRAWBERRY
+1.8 u (+273); sell rows h18 −1.9, h1 −1.7; hires 274.6→274.5; price/unit 86.42→86.32. On
107244033 it is 10x larger: MELON −9 u (−3,556), WOOL −28 u (−2,894) traded for EGG +46 (+2,684),
STRAWBERRY +22 (+2,110); realised **price/unit 67.7 → 61.4**.

## Q4 — verdict: **noise at n=20 + one g200-specific board**

- TOPB g200−g170c per board: −824, SE 729, **t −1.13**; without 107244033, −185, SE 370, t −0.50.
- g200 ≥ g170c on 9 of 20 boards (best +2,662, +2,283).
- 107244033 is g200-specific and is where g170c scored its *largest* lineage gain (+12.4 k over
  base): a single-board swing. Its mechanism is a mid-game **mix shift out of melon+wool into
  strawberry+egg**, −6.3 coins/unit on a melon-race board; absent in aggregate.

**For the g260/g300 queue:** judge on TOPB *paired margin*, never win count — the 35→20 % headline
is three boards, two of them ties.
