# CLIPCENSUS1 (2026-09-27): shed-room-clip escapes on the herd-heavy bed — (b) re-buy class 0.23/game pre-d27 → BUILD FEEDROOM2 (count bar met, value bar not)

## Method
- Tracer `S/clipcensus1/trace_bed.py` = `S/mc10trace1/trace.py` (eswork guard seat, head_940 + theta7659, SAFETY_S 1e9, REPAIR_MS 1e7,
  JIT router) + a VLOSSBED spec (`bed:0-24:<rival>`: LIVE250 dev board i, both seats, reacting kernel of `S/vloss1/bed.txt`) + hourly
  shed/money snapshots. `run.sh <spec> [arm] [extra]` = Stack A (vrp8_jit + CARE_RIDE_ON + SLIVER_ON), main-repo src (bedd759d).
- Identity: all 150 bed games are byte-identical (ours and theirs) to `S/feedroom1/bed/bedA_all.csv`, W 138/150.
  On the loss seats, 16 of the 28 match the FEEDROOM1 lossleg arm_a, which ran from another src and runner.
- `census.py` extends `starve.py`. An escape is an animal with t_cons ≥ 1 at dawn that is still unfed at h23.
  - A clip-bound day is one where the turn-1 shed-bound buys (wheat + fertiliser + animals in the pre-VRP plan) are ≥ the dawn room.
  - Clip-caused escapes = min(escapes, fed + escapes − (dawn wheat + planned wheat buy)).
  - Class (a) = min(clip-caused, not-hungry animals fed that day).
  - Class (b) = min(rest, room after the turn-3 lot, taken from the h4 snapshot).
  - Class (c) = the rest.
  - Days 27-28 are the horizon value escapes of FEEDNIGHT1 and FEEDKEEP1. They are reported separately as A/B/C.
- Value per escape = ANIMAL_COST + held units + lost fires to d29 × our realized product price on that board, minus the feed wheat saved.
  - lo = 1 unit per fire; hi = fully cared, min(held, 1 + interval).
- Calibration (`calib.py`): the same boards were re-run with FEEDROOM_ON (the hungry-first reorder). On each seat's first (a) day the dawn state is identical in both arms, so the escapes FEEDROOM_ON still has that night are the ones reorder cannot save.

## Numbers
| pop | games | esc/g | pre-d27 | clip/g | (a) | (b) | (c) | A | B | (b) value/g lo-hi | (a) value/g lo-hi |
|---|---|---|---|---|---|---|---|---|---|---|---|
| VLOSSBED Stack A | 150 | 5.17 | 1.31 | 0.89 | 0.380 | **0.233** | 0 | 0.187 | 0.093 | 145-314 (+B 43-61) | 198-431 |
| LOSSBANK 28 | 28 | 8.39 | 3.54 | 2.04 | 1.250 | **0.786** | 0 | 0 | 0 | 349-584 | 729-1,566 |
- Kinds, bed: (a) 39 C, 11 S, 7 G. (b) 34 S, 1 C. B 14 C.
  - Per-escape value: (b) 622-1,345 and (a) 522-1,135.
  - Pooled prices: wool 106, milk 89, egg 51, wheat 35.
- Concentration: bed (b) comes from 9 seats on 3 of the 25 boards (8, 9, 20). Bed (a) comes from boards 5, 11 and 24. Loss (b) comes from alejandroayest and suk1yak1.
- Day distribution:
  - Bed: every clip escape falls on d18-27. By day: d18 a8, d20-23 a47 b35, d26 a2, d27 A28 B14. There are none before d18.
  - Loss: d18-25.
- (c) = 0 everywhere. Room after lot 1 (45-71 on the (b) days) always covers the shortfall, and the purse at h4 is 44-66k.
- (a) calibration: FEEDROOM_ON saves 44/44 of the (a)-labelled escapes on the bed's first days and 29/29 on the loss seats. So the labels are right: those animals are in feed_pass.
  - Yet the FEEDROOM1 paired bed leg was Δours −47/game with 0 flips.
  - So the valuation model's (a) 198-431/g does not realise. Saved late animals at a 89 milk price pay about 0 net once the displaced bank/care feeds are counted.
- With FEEDROOM_ON, the bed's (b) rises to 0.287/game pre-d27 (43 escapes). The reorder moves the shortfall onto the next day's hungry sheep, so the ROOM half is the real bottleneck.

## Verdict: BUILD FEEDROOM2 (rule met on count: (b) 0.233/g pre-d27, 0.327/g with d27; value 145-314/g < 400)
- It needs a post-lot-1 wheat BUY row (turn ≥ 4) for the must-feed shortfall, capped at the h4 room, plus a VRP pickup + feed after the buy (route_vrp.py).
- Expect a small, board-concentrated gain: 3/25 bed boards; mostly d21-23 sheep on jammed sheds.
- Judge it paired (VLOSSBED + loss28 + dev100/held100) before believing the value model. The (a) analogue modelled +198-431/g and realised −47/g.

Files: S/clipcensus1/{trace_bed.py,run.sh,census.py,calib.py,census.tsv,census_loss.tsv,summary.txt,calib_bed.txt,calib_loss.txt}.
The pkls in `out/` are gitignored and can be regenerated in about 8.5 min for 4 processes.
