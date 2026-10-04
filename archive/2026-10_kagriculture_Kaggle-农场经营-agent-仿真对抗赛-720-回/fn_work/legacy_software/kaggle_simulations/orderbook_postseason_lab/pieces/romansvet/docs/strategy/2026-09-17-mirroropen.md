# MIRROROPEN — the engine class's opening as ONE package (2026-09-17)

USER QUESTION: *"why can't we do the same as the engine class?"*  Every PIECE of
the top-10 opening was read alone and lost (melon plate M12 −16,224 / their purse
+15,547 `2026-09-16-meloneng.md`; forced opening 94 → 26 %; tiles+hands −4,835).
The JOINT program had never been read.  It has now.

## 1 The switch (`plan.MIRROR_OPEN_ON`, OFF, `tests/test_mirror_open.py`)
Days 0-9, one package, no new genes: (a) the day-0 mix claims
`MIRROR_MELON_TILES`(12) for MELON through the existing `_melon_open` machinery
at all three `open_board()` sites; (b) `_mirror_crew` floors `crew_target` at
`MIRROR_HANDS_D0_9`(7) — the piece every single-lever test lacked; (c)
`_mirror_wheat_ask` adds `MIRROR_WHEAT_BUY`(9) units to each window day's BUY row
through `_rebuy_extra`; (d) fertilizer is the shipped `FERT_TIMING_ON`; (e) from
d10 the shipped FT2 policy — no site that reads `MELON_OPEN_ON` alone is touched,
so it composes with `BANK_BEFORE_LOT_ON` and FT2's own rows are its control.
OFF-identity: five pinned plans byte for byte `_pin.SHIPPED` (c5f68ac).

## 2 Smoke (8 pinned top-tier boards, sim, `S/mirroropen/smoke.py`)
| | FT2 | +MIRROR | the tapes |
|---|---|---|---|
| melon tiles standing d1 | 0.0 | **12.0** | 9.2 |
| first melon sale day | 16 | **12** | 11 |
| hands/day d0-9 | 4.50 | **3.23** | 6.05 |
| wheat bought, game | 122 | **82** | 137 |
| end money ours / theirs | 90,770 / 88,135 | 88,037 / **107,335** | — |

Leg (a) fires as designed.  **Legs (b) and (c) fire BACKWARDS**: the crew d0-9
FALLS 4.50 → 3.23 and bought wheat FALLS 122 → 82.  The crew floor is a *gain*
term the hire enumeration must still afford, and the twelve melon seeds are a
day-0 CASH claim — so the floor asks for hands the purse has already spent.  The
plate does not compete with the hands for TILES, it competes for COINS
(`2026-09-09-forced-opening` reappearing inside the package).

## 3 Judge (`LEGS=ace`, FT2 centre, `S/judgekit/mirroropen.txt`)
| leg | boards | d margin | t | d ours | d theirs | win |
|---|---|---|---|---|---|---|
| ENG22 (in sample) | 22 | −15,335 | −7.23 | −46 | **+15,288** | 40.9 → 13.6 |
| TOPLEG2 gated | 15 | −14,078 | −5.28 | +1,466 | **+15,545** | 13.3 → 6.7 |
| TOPLEG3 gated | 13 | −7,307 | −0.56 | +706 | **+8,012** | 38.5 → 23.1 |
| **pooled engine class** | 28 | **−10,935** | −1.80 | — | — | 25.0 → 14.3 |

The ONE allowed variant, `MIRROR_MELON_TILES=6, MIRROR_HANDS_D0_9=6`
(`S/judgekit/mirroropen6.txt`): ENG22 −15,919 t −10.13 (d ours −5,692, d theirs
+10,227), pooled engine class −7,750 t −1.06.  Half the plate is not half the
bill — it keeps the whole gift and now loses our purse as well.

## 4 Verdict — REJECT, hypothesis FALSIFIED as stated
The gift did **not** shrink: +15,288 / +15,545 against MELONENG's +15,547 — the
same number — and it is now paid while OUR purse is FLAT or up (+1,466 / +706
against M12's −676).  The gift was never vacated output we could buy back with
labour: the day-0 plate is a PRICE transfer, they sell the products our vacated
tiles no longer glut, a property of the SHARED POT and not of our labour bill
(`MELONGIFT`, `MELONRACE` −1,777/tile).
Two-purse rule again: a lever that leaves our purse level and lifts theirs by
15.5k is a loss whatever it does to our own ledger.

**MIRROR_OPEN family CLOSED.**  The engine-class opening loses piece by piece
AND as one package, at 12 tiles and at 6; the reason is not a piece we forgot to
copy but that the same board pays them and us differently through the shared pot.
Switch stays OFF.  Still open: their d10-19 melon PRICE (`TOPLOSS`, `MELONRACE`).
