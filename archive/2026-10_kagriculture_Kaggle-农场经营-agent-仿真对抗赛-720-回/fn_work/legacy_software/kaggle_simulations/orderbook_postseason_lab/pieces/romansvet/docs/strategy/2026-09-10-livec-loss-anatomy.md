# LIVE-C loss anatomy — the 4 losses of the live file (flow172_g940 + tail pair)

2026-09-10. Judge **LIVE-C**: 8 pinned held-out boards cut from live sub 56140532
(`S/livec/provenance.txt`), opponents 2331–2502. Theta `flow172_g940.npy`, switches
`OPEN_PUMP_ON,TAIL_FILL_ON,BANK_BEFORE_LOT_ON` (hr arm: `flow172_g1000.npy` + `HIRE_ROW_ON`).
**Reproduction: 16/16 rows byte-exact** for all three csvs (`S/drainpin/on2b.py`, `--seed-base 777001
--seed-per-opponent`, `S/livec/ids.txt` order, pinned towns); ledgers from `scripts/replay_profile.py`
per-day accumulators. Both seats return identical coins on all 8 boards, so every number is one board-game.

## 1. Day bands — the d10–14 hole is a flat tax here too

Revenue gaps, *ours − theirs*:

| board (opp, rate) | margin | d0–9 | d10–14 | d15–29 | us final / op final |
|---|---|---|---|---|---|
| 107429978 l1aF 2381 | **−10,169** | +1,618 | −21,361 | +9,430 | 89,214 / 99,383 |
| 107430502 Kembang 2427 | **−560** | +263 | −20,827 | +18,807 | 81,407 / 81,967 |
| 107433383 ReinfLarping 2502 | **−115** | +1,446 | −22,489 | +19,592 | 84,055 / 84,170 |
| 107436314 -lingluo- 2476 | **−2,617** | +1,427 | −23,700 | +20,782 | 106,120 / 108,737 |
| *4 wins (mean)* | +12,507 | +994 | −21,491 | +31,962 | 109,350 / 96,842 |

d10–14 is −20.8…−23.8 k on losses **and** −18.6…−23.8 k on wins: the flat tax TOPB records
(`2026-09-10-topb-loss-anatomy-g1000.md` §2). Unlike TOPB, **our own purse is the swing**: d15–29 revenue
88,460 (loss) vs 107,893 (win), theirs 71,307 vs 75,930 — 81 % of the difference is ours. It tracks the
board's wool sink (`towncons_WOOL` 129 on losses, 228 on wins), which lifts both seats.

Product gap per loss board (all bands, mean of 4): FERT **−7,874**, WOOL **−6,294**, MELON −3,114,
WHEAT −1,327; CARROT +6,363, EGG +3,904, STRAW +3,578, MILK +968.

* **MELON** −17,440 in d10–14, +14,306 back in d15–29 on every board. They plant **12 melon d0**, dump
  72 u at d10–11 at **242/u**; we plant 15–17 on **d9–16**, sell 84–96 u at **152–166/u**, of which
  30–42 clear at **103–119/u** in d24–27 — our own glut.
* **FERT** is displacement: we `FERTILIZE` 174–211 times vs their 61 (both collect ~370), selling
  153–210 u where they sell 342–348 — bought back as +13.9 k of carrot/egg/strawberry.
* **WOOL** is **volume**, not price: 69–104 u vs their 161, at 54–118/u vs their 47–128/u.

## 2. Are they the TOPB clone family? Yes — same opening, poorer endgame

| feature (opp) | LIVE-C 2331–2502 | TOPB 2921–3001 |
|---|---|---|
| melon tiles, all planted d0 | **12.0** (4/4 boards) | 11.9–12.9 |
| hands at d10 / d29 | 11.0 / 11.0 | 11.0 |
| d10–11 melon dump | 72 u @ 242/u | 17.3–17.9 k |
| sheep / wool units | 6.0 / 161 | 6.1–8.7 / 146–186 |
| d15–29 revenue | **71,307** | **91,653** |

Identical build book (12 melon d0, 160 wheat tiles, 11 hands, pump opening); the only material
difference is the **late purse, 71.3 k vs 91.7 k** — consistent with `2026-09-11-top-tier-transfer.md` §2
(the top tier's edge is d20–29 price/unit, not the opening). They file 389 sell rows of 3.95 u to our
152 of 9.39 u, but in *this* band our realised price is already ahead (79.8 vs 76.7 coins/unit): the
deficit is 105 units of volume, where TOPB beats us on price.

## 3. What `g1000pair_hr` flips (8/16 → 12/16)

Two boards, 4 seat-games. Attribution vs the intermediate arm `g1000pair` (replayed here, 16/16 exact):

| board | g940 | g1000 | g1000+HR | flipped by |
|---|---|---|---|---|
| 107430502 | −560 | **+988** | +1,479 | the theta step |
| 107433383 | −115 | −350 | **+237** | **HIRE_ROW** |

**HIRE_ROW is a pure own-purse cost cut**: hires 267–274 → 256–266, `spend_hire` 5,144–6,136 → 4,504–5,616,
idle `PASS` unit-actions 848–933 → 670–682, revenue moving **< 250 coins in every product and band** on
3 of 4 loss boards (dOURS +491/+644/+944, dTHEIRS +0/+57/+120). On 107436314 it also buys a 10th cow
(+27 milk units), denying them 4,967 milk (dMARG +2,112).

## 4. Largest recoverable bucket

**Largest in coins: melon price.** Repricing our 84–96 units at their 242/u is **+7.4 k/board**, more
than the 4 loss margins combined. Signature **own purse** (they exit melon by d11, so theirs barely
moves). **Closed**: `2026-09-10-melon-route-capacity.md` §1/§4 (`MELON_OPEN_ON` 1.9 %, −19,557),
`2026-09-09-verdicts.txt` 2026-09-08T21:40Z (forced opening 94→26 %) and `FORWARD_ADMIT_ON` −9,224;
only the additive form (`2026-09-11-additive-melon.md` §4) is unbuilt.

**Largest still open: hire/idle overhead, ~2.65 k/board** — 6,282 of hires against their 3,630 at
12.4–13.4 % PASS vs 6.4–6.8 %. `HIRE_ROW_ON` already banks 491–1,038 with revenue flat and flipped a
loss board; its closure (`2026-09-09-verdicts.txt` 2026-09-04T21:28Z, "−378 t −0.75 n=768, closed") is
**stale, contradicted on three judges**: LIVE62 +453 t 3.59, TOPB +6,573 t 3.88, LIVE-C +1,109 t 3.08.
With 3 of 4 losses inside 2.7 k, this is the bucket that flips boards in this band.
