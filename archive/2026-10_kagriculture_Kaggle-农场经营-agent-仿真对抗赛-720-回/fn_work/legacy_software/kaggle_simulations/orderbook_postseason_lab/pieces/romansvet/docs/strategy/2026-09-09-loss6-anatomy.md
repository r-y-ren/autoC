# 2026-09-09 — the six live losses of sub 56098262 (flow135_g350), measured

Measurement only; no lever proposals. Live theta `artifacts/kagg2_games/thetas/flow135_g350.npy`
(md5 204a84f0), packaged `dist/submission_flow135_g350.tar.gz` (md5 ca6b3769).
Working files under `S/loss6/`: `repro_pkg.csv`, `ledger_days.csv`, `ledger_summary.txt`,
`full.txt`, `attrib.txt`, `pass6.json`, `cluster.txt`, `superfam.txt`.
Replay jsons `S/ep_<ep>.json`; pinned tapes `artifacts/tape_actions_town/<ep>.npz`.

## 1. REPRODUCTION — byte-exact on all six

    cd .claude/worktrees/agent-a85c50163fb5dcbb7
    KAGG3_TOWN_SCHEDULE=$S/band2100p/town_schedules.json PYTHONPATH=$W/src \
    .venv/bin/python $S/fert2/on2.py "OPEN_PUMP_ON=True" \
      --me dist/submission_flow135_g350.tar.gz --games 1 --workers 4 \
      --seed-base 777001 --seed-per-opponent \
      --opponents artifacts/panel_opp_town/opponent_tape_<ep>/main.py ...

| episode | opponent (rating) | Kaggle ours / theirs | engine ours / theirs | delta |
|---|---|---|---|---|
| 107056463 | XJHya233 (1827) | 100,350 / 107,091 | **100,350 / 107,091** | 0 / 0 |
| 107067869 | williams (1969) | 93,410 / 103,138 | **93,410 / 103,138** | 0 / 0 |
| 107068399 | Hanaro (2009) | 68,014 / 69,132 | **68,014 / 69,132** | 0 / 0 |
| 107070717 | kuroko1t (2061) | 97,047 / 105,867 | **97,047 / 105,867** | 0 / 0 |
| 107072760 | datnt114 (1954) | 123,041 / 125,502 | **123,041 / 125,502** | 0 / 0 |
| 107079367 | saitamad (1936) | 101,703 / 123,937 | **101,703 / 123,937** | 0 / 0 |

Every game reproduces to the coin, in **both seats** (seat 0 and seat 1 return identical
totals — the tapes are seat-blind and the pinned town removes board randomness), `sd = 0`
per opponent. Nothing below is seed noise; these are the live games.

## 2. LEDGER

`S/loss6/ledger6.py` (a copy of `S/lossanat/ledger.py` with `OUT` repointed). Money
residual 0.29–0.69 % of gross on five games; **107072760 is 4.5 %** — its per-product
splits there are indicative, not exact (it has same-step two-way rows on one item).

### 2a. What is identical in all six

| item | ours | theirs |
|---|---|---|
| day-10 cash | 2.2k – 3.7k | **15.1k – 17.6k** |
| day-10 planted tiles | 42–48 | 32 (12 WHEAT + 20 STRAWBERRY, exactly) |
| day-10 quadrants | 3 | 2 |
| day-10 idle tiles on unlocked land | **12–16** | **0** |
| day-10 hands | 10 | 11 |
| melon dumped d10 + d11 | none | **60 u @ 247 + 12 u @ 220 = 17.4k**, identical on all six boards |
| our melon | 72–116 u sold d17–d29 at 220 falling to 4 | — |
| PASS share of unit-turns | **15.4–16.9 %** | 6.4–9.8 % |
| FERTILIZE orders | 171–189 | 61–98 |
| FERTILIZER units sold | 177–250 | **328–425** (mean +150 u, +6.7k gross, +4.1k net of their purchases) |

### 2b. Per-game attribution (full-game income delta by product, ours − theirs, k coins)

| ep | opp (rating) | margin | income Δ | spend Δ | decisive item | size |
|---|---|---|---|---|---|---|
| 107056463 | XJHya233 1827 | −6,741 | −16.3 | −9.6 | FERTILIZER −6.6 (196 u vs 333), then CARROT −3.9, MELON −3.4 | −6.6k |
| 107067869 | williams 1969 | −9,728 | −8.3 | +1.4 | STRAWBERRY −9.8 (175 u vs 262) + WHEAT −6.3 + WOOL −6.0, against our TOMATO +17.6 | −9.8k |
| 107068399 | Hanaro 2009 | −1,118 | −11.4 | −10.2 | FERTILIZER −6.5 (215 u vs 346); low-money board, our 10.2k lower spend nearly saves it | −6.5k |
| 107070717 | kuroko1t 2061 | −8,820 | −12.0 | −3.3 | MILK −8.8 (122 u vs 231; **5 cows vs 8**), FERT −7.1, MELON −4.8 | −8.8k |
| 107072760 | datnt114 1954 | −2,461 | −2.2 | +0.2 | WOOL −8.9 + FERT −8.4, nearly repaid by our STRAWBERRY +11.6 and MILK +7.0 (11 cows vs 8) | −8.9k |
| 107079367 | saitamad 1936 | **−22,234** | −27.4 | −5.1 | **MILK −20.9** (129 u vs 239 at the same 191/u; **4 cows vs 8**), FERT −8.8, STRAW −6.8, our WOOL +6.4 | **−20.9k** |

Melon is a **constant tax, not the decider**: their 72 units are worth 17.4k in every game;
ours are worth 12.7–15.1k off 72–116 units, so the melon line is only −2.3 to −4.8k
(mean −3.2k) even though the day-10 *cash* gap it opens is −12 to −15k on every board.

### 2c. The saitamad −22k game, closest look

Their 123,937 = 154.5k income − 33.6k spend + 3k start. By product (units / coins / c-per-u):
MILK 239 / 45.7k / 191 · WOOL 187 / 30.5k / 163 · STRAWBERRY 252 / 25.7k / 102 ·
FERTILIZER 425 / 20.1k / 47 · MELON 72 / 17.4k / 242 · WHEAT 370 / 14.5k / 39 ·
CARROT 16 / 0.5k · TOMATO 0 · EGG 0.
By day (k): d0-9 16, **d10 18**, d11-19 64, d20-29 57.

Ours: 127.1k income − 28.5k spend. The entire 27.4k income gap is three lines —
MILK −20.9, FERTILIZER −8.8, STRAWBERRY −6.8 — against WOOL +6.4 and EGG +2.6.
**Milk is a pure volume gap at an identical shared price**: 129 u vs 239 u at 191/u.
Cause is herd composition, not care: total herd 16 vs 16, but our herd walks
C3/S2 (d0) → C3/S5 (d6) → C3/S8 (d9) → **C4/S12** (d12) while theirs walks
C2/S2 → C6/S2 → C8/S5 → **C8/S9**. We bought sheep where they bought cows.
Across the six games the relationship is tight: **corr(cow delta, milk delta) = 0.91,
slope +3.35k per cow**; corr(sheep delta, wool delta) = 0.92, slope +2.87k per sheep.
Cows pay ~1.2x what sheep pay, and we substituted 4 cows for 3 extra sheep.
The town on that board opened YARN_STORE on d3 (the only wool sink) and then
ICE_CREAM d6/d18, PIZZA d9, SMOOTHIE d21/d24 — **five milk sinks after the wool one**.
On 107072760, where SMOOTHIE/ICE_CREAM/PIZZA came first, we bought 11 cows and won milk +7.0k.
Our melon there also self-crashed: 116 units liquidated d18→d29 at 219, 199, 162, 109, 53, 25, 7, **4**.

## 3. CLASSIFICATION against the 88-loss ledger (`docs/strategy/2026-09-05-build-story.md:788`)

The four known classes were: day-0 melon block dumped d10 (+14.1k), daily fertilizer
collection (+7.0k), daily milk care (+5.1k), board fill (+3.5k, 9 idle unlocked tiles).

| class | present? | measured size here |
|---|---|---|
| d10 melon pot | **6/6**, identical tape behaviour | −3.2k mean on the melon line; −12…−15k on the day-10 cash position |
| fertilizer | **6/6** | −6.7k mean *income* line, **−4.1k mean net of their fert purchases** (they buy 46–131 u, we buy 1–11); our COLLECT_FERT is *higher* (362–440 orders vs 363–389) — the units go into 171–189 FERTILIZE orders (theirs 61–98) instead of the market |
| pasture / animal product | **6/6** | milk+wool combined −4.1 to −14.5k; driven by **herd mix**, see below |
| board fill | **6/6** | 12–16 idle unlocked tiles at d10 vs their 0; PASS 15.4–16.9 % vs 6.4–9.8 % |
| late liquidation into a dead price (`S/lossanat/report.md`) | **6/6** on melon | our melon realises 109–176/u vs their 242/u |

**Nothing here is a new opponent behaviour or a new loss family.** The one thing that is
*sharper* than the ledger's wording is the pasture item: the ledger attributes it to
**care coverage** (+108 CARE / +64 FEED orders, `docs/strategy/2026-09-09-care-coverage.md`).
On these six the CARE/FEED gap is small (ours 276–342 CARE vs theirs 365–417) and the
animal-product swing is carried almost entirely by **how many of the 15–18 animals are
cows**: 0.91 correlation, 3.35k/cow, and it is the whole of the −22k game. That is a
*composition* effect on an equal-sized herd, distinguishable from care coverage, and it is
the item that turns a −3k board into a −22k board. It is adjacent to, but not the same as,
the parked JOINT_PLATE "sheep/cow floors from wool/milk sinks" lever
(`build-story.md:433`), which was rejected on its crew-floor side.

## 4. OPPONENT FAMILY — one family, no new ones

Fingerprint = the multiset of day-0 market rows from the pinned tapes (`S/loss6/superfam.py`).

Day-0 signature census over all 168 pinned tapes on disk:
**(5 HIRE, 2 COW, 2 SHEEP, 12 MELON seeds) = 148 tapes (88 %)**; next largest bucket has 3.
All six losses are in that core family, and **all 148 of them sell ≥55 MELON on day 10**
(156/168 tapes do). Every one also runs the hour-0 wheat pump.

| ep | opponent | rating | sub-cluster (sim ≥ 0.95 on d0+d1 rows) | distinguishing detail |
|---|---|---|---|---|
| 107056463 | XJHya233 | 1827 | n=18 (incl. top-ten-era 107018738) | h0 pump 13; wheat churn h3–h12; melon seeds trickled |
| 107068399 | Hanaro | 2009 | n=4 (107005652, 107010600, 106796826) | same as above, smaller h3 churn (sim 0.88 to 107056463) |
| 107067869 | williams | 1969 | n=39 (incl. 107009663, 107015397, 107015401, 107016108) | h0 pump 13; 12 melon seeds in one h1 row |
| 107070717 | kuroko1t | 2061 | **same cluster, sim 1.00 to 107067869** | identical day-0/1 to williams |
| 107072760 | datnt114 | 1954 | n=14 (incl. 107000107, 107008216/406/497, 107014375/982) | double h0 pump (buy 13/sell 13/buy 13); melon seeds d0 h6–h17 |
| 107079367 | saitamad | 1936 | singleton | **h0 pump 30 units** instead of 13 — the only difference |

The sub-clusters differ only in the *size and staging* of the hour-0 wheat pump and whether
the 12 melon seeds are bought in one row or trickled. Strategically they are one clone.
kuroko1t (2061) and williams (1969) are byte-identical through day 1; saitamad is a
singleton purely because of a 30-unit pump. **No new family, and rating does not track the
opening** — the 2061 and the 1827 play the same day 0.

## 5. Caveats

* 107072760's ledger residual is 4.5 % of gross (others ≤ 0.7 %); its product split is
  indicative. Its final coins reproduce exactly, so the margin and the day-level money
  path are exact regardless.
* The cow→milk slope is fitted on n = 6 games; the sign and the 0.91 correlation are solid,
  the 3.35k/cow coefficient is not a promotion-grade estimate.
* Family fingerprints use day-0+1 market rows only. Two tapes in one cluster can still
  diverge later; the melon d10 dump was checked separately and holds for 148/148.
