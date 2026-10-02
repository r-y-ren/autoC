# TOPB loss anatomy — `flow172_g1000` + tail pair, the 12 boards we still lose

2026-09-10. Judge **TOPB**: 20 held-out pinned top-ten tapes x 2 seats (`S/topb/ids.txt`, 2921.6–
3001.5). Theta `artifacts/kagg2_games/thetas/flow172_g1000.npy` (md5 `f091deb2`), switches
`OPEN_PUMP_ON,TAIL_FILL_ON,BANK_BEFORE_LOT_ON`. Engine replays only, no sim. Leg
(`S/topb/chain_summary.txt`): win 25.0→**40.0 %**, dMARG **+5,758** t 3.30 = ours +5,556 / theirs
−202, 6 flips 0 drops, 20/20 boards positive vs `flow135_g350`.

Replays: `S/topb/run.sh` + `--replay-dir --stats`; ledgers via `scripts/replay_profile.py`. The
re-run reproduces `S/lossflip/g1000pair_topb.csv` **40/40 rows exactly**.

## 1. The 20 boards

12 lost / 8 won; both seats agree everywhere (splitting materially only on 107246553, 107250728).
Band gaps = *our revenue − theirs*; d0–9 is within ±3.1 k on all 20 and is omitted.

| board (team) | margin s0/s1 | d10–14 | d15–29 |
|---|---|---|---|
| 107244957 Mengfei Li | **−645 / −645** | −22,133 | +22,592 |
| 107250521 cooked | **−1,234 / −1,234** | −22,766 | +19,366 |
| 107252679 Terry Luo | −5,749 / −6,443 | −20,836 | +16,366 |
| 107246553 binghua | −6,972 / −16,711 | −15,017 | +797 |
| 107248812 mtmr_s1 | −7,057 / −6,964 | −22,988 | +12,283 |
| 107250728 Otter Vibe | −8,343 / −12,918 | −13,951 | −13,581 |
| 107245770 Terry Luo | −8,584 / −8,584 | −25,650 | +17,509 |
| 107246551 DeeperNet | −8,737 / −8,737 | −23,045 | +12,431 |
| 107244033 SpaTaro | −9,157 / −8,473 | −22,586 | +8,184 |
| 107248813 Mengfei Li | −9,317 / −9,317 | −19,450 | +4,861 |
| 107233845 binghua | −9,804 / −10,608 | −10,735 | +1,679 |
| 107246911 Otter Vibe | **−22,106 / −22,106** | −15,494 | −20,199 |

Narrow (<5 k): **2**. 5–13 k: **9**. Structural (>15 k): **1**. Median board loss **−8.8 k**;
+8.8 k/game flips 6 of the 12, +9.0 k flips 7.

## 2. Day bands — the melon hole is *not* the discriminator

Means per board-seat (24 lost / 16 won seats):

| band | LOSS gap (ours/theirs) | WIN gap (ours/theirs) |
|---|---|---|
| d0–9 | +27 (14,430 / 14,403) | +584 (14,748 / 14,164) |
| d10–14 | **−19,554** (10,301 / 29,855) | **−22,338** (10,292 / 32,630) |
| d15–29 | +6,857 (98,510 / 91,653) | **+25,504** (98,308 / 72,805) |
| final | −8,769 (97,909 / 106,678) | +6,673 (99,859 / 93,186) |

The d10–14 melon pot (melon alone **−13,892**/game in the losses) is **larger on the 8 boards we
win**: a flat tax on all 20, not what separates a win from a loss.

## 3. Two-purse — our purse is identical; theirs is not

Our d15–29 revenue is **98,510 (losses) vs 98,308 (wins)** — 200 coins apart; tiles (179.5/178.4),
animals (18.7/18.0), hires (270.7/269.3), melon tiles (16.3/15.9), d9 cash (5,994/6,235) all level.
**87 % of the win/loss difference is the opponent's purse** (106,678 vs 93,186). Signature:
**denial never taken**, not displacement — we do not play worse where we lose, we never contest a
channel that pays them there. Their extra **+18,848** of d15–29 revenue:

| product | theirs L / W | Δ | their units L/W |
|---|---|---|---|
| **WOOL** | 24,805 / 15,939 | **+8,866** | 148.9 / 108.2 |
| **MELON** | 3,974 / 0 | **+3,974** | 20.8 / 0.0 |
| TOMATO | 2,739 / 0 | +2,739 | 38.5 / 0.0 |
| STRAWBERRY | 23,576 / 20,969 | +2,606 | 206.9 / 234.2 |
| FERTILIZER | 5,486 / 6,249 | −764 | 153.2 / 191.5 |

Late wool + held-back melon = **12,840 of the 18,848**. On the four boards where the tape does not
dump the whole pot at d10–14 (107233845, 107246553, 107246911, 107250728: melon 3,221–10,594 vs the
clone's 17,440) it re-appears as d15–29 wool of 19,417–76,659 — four of our five deepest losses.

## 4. Wins vs losses

Town schedules do **not** discriminate (YARN_STORE 1.25/board on losses vs 1.13 on wins; all 20
towns end at 8 shops), nor do opponent melon tiles (12.9 vs 11.9). Our d10 pot share is **0 on all
20** — first melon revenue is d15+ everywhere (11,692–17,014). The only differences are theirs:
**animals 17.8 vs 15.6**, **d15–29 revenue 91,653 vs 72,805**.

## 5. Largest recoverable bucket

**d10–14, −19,554/game** (melon **−13,892**, wool −2,389, fertilizer −1,640, wheat −1,275).
Two-purse signature **own purse, empty**: we bank 10,301 there against their 29,855, so recovering
it is growth. It is the only bucket bigger than the 8.8 k median loss; 65 % of its melon half
(+9.0 k) flips 7 of the 12.

## Verdict

**Lever family: the d10–14 production window — the melon pot and the ramp that fills it.**
**Closed in the archive in every *built* form**: `2026-09-10-melon-route-capacity.md` §1/§4
(`MELON_OPEN_ON` pinned judge 1.9 %, −19,557; the route is not the wall, the swap is),
`2026-09-05-build-story.md:927-931` (`FORWARD_ADMIT_ON`, −6.4 k), `2026-09-09-board-fill.md`
(`PLANT_FILL_LATE_ON`, −5.6…−6.9 k own purse, +0/−10), `2026-09-09-pasture-cadence.md`
(`ANIMAL_RESTOCK_ON`, built, shipping OFF). The one **unbuilt** form is additive melon
(`MELON_ADD_ON`, spec `2026-09-11-additive-melon.md` §4), argued against there on d0 purse
arithmetic. What this adds: every rejection measured a **swap** on band/clone judges, and its
displacement landed in the herd — but on TOPB the herd is already level (18.7 vs 17.8) and our
purse is flat across wins and losses, so that displacement term should be smaller here.

**Paired experiment.** Build `MELON_ADD_ON` per `2026-09-11-additive-melon.md` §4 (OFF must decode
byte-for-byte). Arms: `g1000pair` vs `g1000pair + MELON_ADD_ON,MIDDAY_PLACE_ON,MIDDAY_PLACE_V2_ON`.
Judge TOPB (`S/topb/run.sh`, 20 tapes x 2 seats, `--seed-base 777001 --seed-per-opponent`, order
load-bearing), paired per board via `S/bank/paired.py`: board SE ≈ 1,500 at n=20 → **pass needs
Δmargin ≥ +3,000 (t ≥ 2)**, reporting Δours/Δtheirs and the re-measured d10–14 gap. Veto: LIVE55
(`S/live62/run.sh`) Δmargin ≥ −1,000 — the band killed every previous melon arm, and a 20-board
gate is never the only judge (`es-noise-floor-2026-09-05`).
