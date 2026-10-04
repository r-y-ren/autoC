# TOPB loss anatomy, g1000pair — independent second read (B)

Blind re-derivation. Judge = `S/lossflip/g1000pair_topb.csv`, 20 held-out top-tier pinned boards
x 2 seats. **Reproduction: 40/40 rows byte-exact** (`S/drainpin/on2b.py`, theta
`artifacts/kagg2_games/thetas/flow172_g1000.npy`, `--seed-base 777001 --seed-per-opponent`,
tapes in `S/topb/ids.txt` order, `KAGG3_TOWN_SCHEDULE=S/band2100p/town_schedules.json`).
Ledgers from `scripts/replay_profile.py` over the dumped replays (scratchpad `B/`).

Record: **16/40 games, 8/20 boards, mean margin −2,592** (base `flow135_g350_topb.csv`: −8,350).

## Q1 — the losses

| board | margin | | board | margin |
|---|---|---|---|---|
| 107246911 | −22,106 | | 107248812 | −7,010 |
| 107246553 | −11,842 | | 107252679 | −6,096 |
| 107250728 | −10,630 | | **107250521** | **−1,234** |
| 107233845 | −10,206 | | **107244957** | **−645** |
| 107248813 | −9,317 | | 107244033 | −8,815 |
| 107246551 | −8,737 | | 107245770 | −8,584 |

Wins: 107252688 +16,896, 107246552 +10,446, 107247899 +9,036, 107240026 +6,779,
107242091 +4,243, 107249999 +2,559, 107251183 +2,537, 107250536 +887.

10 of 12 losses are **structural** (≥ 5k); only 107244957 and 107250521 are narrow.

## Q2/Q3 — day-band and product ledger (means, us vs opponent)

| revenue band | LOSS us | LOSS op | LOSS gap | WIN us | WIN op | WIN gap |
|---|---|---|---|---|---|---|
| d0-9 | 14,430 | 14,403 | +27 | 14,748 | 14,164 | +584 |
| d10-14 | 10,301 | 29,855 | **−19,554** | 10,292 | 32,630 | −22,338 |
| d15-29 | 98,510 | 91,653 | +6,857 | 98,308 | 72,805 | **+25,503** |
| final coins | 97,909 | 106,678 | −8,769 | 99,859 | 93,186 | +6,673 |

The d10-14 hole (their melon dump: op MELON d10-14 = 13,892 on losses, 17,276 on wins; ours 0)
is **the same size on boards we win**. It is a tax, not a discriminator. The whole separation is
d15-29, and it is **their purse**: our late revenue is flat (98,510 vs 98,308, Δ −202) while
theirs swings 91,653 vs 72,805 (Δ **+18,848**).

Their d15-29 revenue, win → loss: WOOL 15,939 → 24,805 (**+8,866**), MELON 0 → 3,974, TOMATO
0 → 2,739, STRAWBERRY 20,969 → 23,576, rest ≤ +0.5k. Per-product margin swing (us−op gap, wins
minus losses): **WOOL +6,875**, TOMATO +4,505, EGG +3,206, MELON +1,145, others ≤ ±1.3k.

## Q4 — what separates wins from losses

| feature (board mean) | WIN (8) | LOSS (12) |
|---|---|---|
| our final coins | 99,859 | 97,909 |
| their final coins | 93,186 | **106,678** |
| their SHEEP / wool units | 6.1 / 146 | 8.7 / 186 |
| our SHEEP / wool units | 6.6 / 130 | 8.6 / 165 |
| their wool revenue | 23,368 | **32,460** |
| our wool revenue | 25,395 | 27,611 |
| wool coins/unit us vs op | 145 vs 152 | **144 vs 160** |
| wool sell-day median us vs op | 17.0 vs 14.9 | 19.7 vs 18.2 |
| town wool sink (`towncons_WOOL`) | 268 | 294 |
| their melon revenue | 17,276 | 17,865 |

Not the schedule: YARN_STORE count is 1.1 on wins, 1.2 on losses, and our sheep count already
tracks the wool sink (corr +0.88; theirs +0.64). Margin correlates with the **wool revenue gap
+0.66** and the late-band gap +0.89, but with wool *unit share* only +0.13. We match volume and
lose price: 144/unit against 160, median 1.5 days later, 22 units before d16 against their 46.

## Q5 — largest recoverable bucket, and whether it is closed

**Bucket: late wool, ~6.9k/game of the 15.4k win/loss swing.** Signature = **opponent's purse**
(our coins are flat across wins and losses; theirs move 13.5k), i.e. denial, not displacement —
with one own-purse sliver: repricing the 165 wool units we already sell on the loss boards at
their 160/unit is **+1,993 coins/game** and costs no tile and no sheep.

Already measured, and closed four ways — `docs/strategy/2026-09-09-verdicts.txt`:
- 2026-09-05 11:39Z **wool push** (herd-mix logit) rejected dose-responsively, −4.8k/−12.9k.
- 2026-09-06 02:30Z **LATE_SHEEP_CAP** rejected: freed tiles go to wheat, −33.6k on one board.
- 2026-09-06 22:40Z **HERD_LOCK** wool-only: "shop-adaptive herd family closed (both halves)".
- 2026-09-06 12:15Z **WOOL_DUMP (wool13)**: *inert* — and its ledger already names this exact
  mechanism: "our wool leaves at h18 (`DROP_ON` appends mid-day banked yield to the LAST lot,
  `plan.py:6577-6596`) vs the clone's h0-h16 → d16 ours 160/u vs theirs 189/u". Its successor
  `S/dropearly` was also inert on band6 (re-screen 2026-09-07 06:35Z).

So the volume half is closed. The price half is **not tested**: both levers that targeted it were
byte-identical, and `docs/strategy/2026-09-10-sell-hour-headroom.md` records that a per-product
sell-hour map "does not exist — the product→lot split is `sell.allocate`'s greedy on learned
hold/press, not a turn table". That greedy, made wool-first into the earliest lot on boards with a
live wool sink, is the one wool sub-lever with a measured mechanism and no non-inert measurement.
