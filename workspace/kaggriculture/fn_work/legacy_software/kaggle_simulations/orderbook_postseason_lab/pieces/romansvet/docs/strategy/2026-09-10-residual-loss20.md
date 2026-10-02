# 2026-09-10 — the residual 15 of LOSS20 under flow172_g60

20 pinned tapes of sub 56098262's live losses (`flow135_g350`, 0/20); `flow172_g60` wins 5, so
these are the other **15**. Engine (`S/lossflip/*_loss20.csv`) is truth; per-day and per-channel
numbers are **sim, descriptive only** (|Δmargin| vs engine 153, W/L agreement 100 %).
Files `S/resid20/`.

## 1. The fifteen (engine coins)

    ep          opponent (rating)              live      g60   g60 ours/theirs
    107088554   HD h Joratos      1932       -8,099  -13,764   101,270/115,034
    107095149   cm391             1945      -13,960  -11,864   111,529/123,393
    107090008   LuanHengYu        1961       -8,042   -9,384   127,758/137,142
    107079367   saitamad          1936      -22,234   -8,015   104,159/112,174
    107134203   DI27 RF           2047       -8,009   -6,777   110,630/117,407
    107056463   XJHya233          1827       -6,741   -6,450   102,181/108,631
    107144702   Aleix Lopez       2024       -7,788   -6,122    85,322/ 91,444
    107125425   Boiled-Sweet-Pot  1945       -8,281   -4,407   134,690/139,097
    107109832   high freq farming 2061      -16,154   -3,690   150,399/154,089
    107070717   kuroko1t          2061       -8,820   -2,694   100,643/103,337
    107140814   An V1             2025       -9,758   -1,307    89,589/ 90,896
    107089992   KongKongDe        1966       -1,918   -1,235   133,154/134,389
    107081922   Crop It Like It's 1988       -7,690   -1,097   120,987/122,084
    107092814   WBF_USA_NYC       1983       -6,527     -921    76,518/ 77,439
    107067869   williams          1969       -9,728     -413    98,140/ 98,553
    mean        1978                         -9,583   -5,209   109,798/115,007

All 20 tapes run one identical opening: d0 = 7 WHEAT + 12 MELON seed, 2 COW + 2 SHEEP, 5 HIRE;
21–22 hires by d4; 2 BUY_LAND. One clone, not fifteen opponents.

## 2. Two-purse, g60 − live (engine)

Residual 15 (n=30): ΔMARGIN **+4,369** (t 4.6) = Δours **+2,996** / Δtheirs −1,373, 69 % own.
Flipped 5 (n=10): +7,619 (t 8.2) = +5,061/−2,558, 66 %. Two-thirds growth, one-third denial —
2.3 k short.

## 3. Day-band ledger, residual 15 (theirs−ours, g60 eod cash)

    band     gap at end   opened      ours    theirs
    d0-4         -1,158   -1,158     1,554       396
    d5-9         -3,682   -2,524     6,070     2,387
    d10-14      +19,442  +23,125     8,192    27,635
    d15-19      +15,389   -4,053    44,731    60,120
    d20-29       +5,052  -10,337   109,844   114,897

**One band is the whole loss.** Revenue d10–14: theirs 33,486 (233 u @ 143.8) vs ours 10,756
(92 u @ 117). Top three channels:

1. **MELON ≈ −15 k.** 12 planted d0, pot dumped d10–11 (7 SELL rows; quote 270→226→215). We
   hold **0 melon tiles before d10**, sell our 84 units from **d18** at 220 falling to 113.
2. **MILK+WOOL ≈ −4 k.** 14.7 pasture tiles at d20 vs 12.7; 8.2 MILK + 3.5 WOOL rows.
3. **FERTILIZER ≈ −3 k.** 92 season SELL rows; our whole season is 182 units.

Openings — **theirs** 7 WHEAT+12 MELON, 22 hires by d4, 32 tiles at d10, **0 idle**; **g60**
9 WHEAT+10 CARROT, 21 hires by d4, 46.6 tiles, **13.3 idle**. g60 closed the crew ramp (live
theta 14.9 hires by d4); the d0 basket is untouched.

## 4. One pattern, not several

Degenerate. All 15 have gap(d14) in **+15.0 k…+22.8 k** — so do the 5 g60 *wins* (+18.7 k).
`corr(final gap, gap_d14) = +0.06`; `corr(final gap, d14→d29 recovery) = −0.86`. The 15 recover
+14.4 k after d14, the flipped 5 +24.7 k: boards differ only in how fast our late engine repays
the same d10 hole. Season: 1,359 u @ 99.1 in 139 rows vs 1,548 u @ 91.6 in 249.

## 5. Verdict

Move **d10–14 income**, nothing else: d0–9 is already ours (−3.7 k) and d15–29 already repays
14 k. Concretely, melon in the ground on d0 so it harvests into the 265 quote — the
**FORWARD_ADMIT blocker** (hire enumeration prices hands on today's tasks; melon tiles emit none
for six days), not a fitness term. Second: 13.3 idle tiles at d10 against their 0. A late arm
cannot pay — g60 out-earns them 10.1 k in d20–29 and still loses.

**Exclusions: none.** Four tapes drift under the live theta — 107088554 (−356/+166, ≈0.5 k on a
−13.8 k board), 107095149 (−21), 107134203 (+28/−55), 107108124 (−1, a g60 *win*). None is near
a verdict; keep all 15, flagging 107088554.
