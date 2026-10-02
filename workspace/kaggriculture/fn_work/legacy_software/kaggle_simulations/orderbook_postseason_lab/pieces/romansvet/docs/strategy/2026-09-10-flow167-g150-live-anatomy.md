# flow167_g150 vs the live theta on the 55 held-out live boards — anatomy

Date 2026-09-09/10. Agent: measurement. Sim = shed-fixed worktree `arms-next` @83cfe5c,
pinned-town action-tape seat, `shop_crn=True`. Engine reads from
`S/lossflip/flow167_g150_live62.csv`, `flow166_g170_live62.csv`, `flow135_g350_live62.csv`;
boards = `S/livewin/live_heldout_ids.txt` (55 tapes, held out of flow16x training).

Scripts / raw output: `S/g167live/` (`anat_live.py`, `analyze.py`, `compare_engine.py`,
`anat.npz`, `report.txt`, `engine_compare.txt`). Derived from the flow166_g170 anatomy
scripts in `S/g170live/`.

**Note on seats.** Every `*_live62.csv` records seat 0 and seat 1 rows with identical
purses for ~85 % of tapes, and the seat-0 and seat-1 aggregate reads are bit-identical
(win 34.5 / 50.9 / 52.7 % on both). The engine leg is therefore effectively 55 games, not
110; the "+20/−2" flip count in the brief is 10 flips and 1 drop counted twice. All tables
below use seat 0 = 55 unique boards.

## Engine head-to-head (55 boards, seat 0)

```
==================================================================================
ENGINE head-to-head, 55 held-out live boards (seat0; csv rows seat-duplicated)
==================================================================================
  live g135_g350  win  34.5%  mean margin     -294   excl2     +111
    flow167_g150  win  50.9%  mean margin    +2938   excl2    +3509
    flow166_g170  win  52.7%  mean margin    +2467   excl2    +3242
    flow167_g150  d    +3232 t  5.93 | excl2 d    +3398 t  6.15 | improved 43/55  >+1k 42  <-1k 8
    flow166_g170  d    +2761 t  4.02 | excl2 d    +3131 t  4.79 | improved 42/55  >+1k 38  <-1k 8

corr(d167,d166) over 55 boards = 0.699   (excl2 0.688)
paired d167-d166 = +471  t +0.95   excl2 +267 t +0.55

sign disagreements: 9/55
      tape     base     d167     d166     m167     m166
 107055322   +17495    +1998    -6381   +19493   +11114
 107131313    -3541     -164    +6905    -3705    +3364
 107032494    +7750    -2883    +2580    +4867   +10330
 106978598    +8088    +4671     -776   +12759    +7312
 106947809    +6026    -3921     +875    +2105    +6901
 106991516    +4321     -895    +3520    +3426    +7841
 107049618   +35369    +1974     -968   +37343   +34401
 107003041   +10810    +2713     -140   +13523   +10670
 107044716    -1876    +1791     -294      -85    -2170

WORST 5 boards (downside) each:
  flow167_g150: 107040955-4729  106947809-3921  107090008-3207  107032494-2883  107117102-2822   sum -17562  |  worst-10 sum -23742  P5 -2980  min -4729
  flow166_g170: 107088554-10564  107117102-7615  107040955-6669  106964817-6453  107055322-6381   sum -37682  |  worst-10 sum -49875  P5 -6518  min -10564

W/L transitions vs live theta:
  flow167_g150: flips 10  drops 1  net 9  win 50.9%
    flipped tapes: 106968689(base-4823) 106974180(base-6385) 106985187(base-2281) 107008497(base-2139) 107016108(base-338) 107068399(base-1118) 107072760(base-2461) 107108124(base-167) 107116818(base-295) 107154400(base-6995)
    dropped tapes: 107117102(base+287->-2535)
    flip base margins: mean -2700 median -2210 |base|<2500 on 7/10  range -6995..-167
  flow166_g170: flips 11  drops 1  net 10  win 52.7%
    flipped tapes: 106968689(base-4823) 106974180(base-6385) 106985187(base-2281) 107008497(base-2139) 107016108(base-338) 107035330(base-6958) 107068399(base-1118) 107072760(base-2461) 107108124(base-167) 107116818(base-295) 107131313(base-3541)
    dropped tapes: 107117102(base+287->-7328)
    flip base margins: mean -2773 median -2281 |base|<2500 on 7/11  range -6958..-167

Boards won by only one candidate:
  167-only wins: 107154400(+720/-3371)
  166-only wins: 107035330(+3971/-5326) 107131313(+3364/-3705)

ENGINE TWO-PURSE (own purse vs opponent purse), win/loss split by live theta result
                   set    n  dMARGIN167    dOURS  dTHEIRS |  dMARGIN166    dOURS  dTHEIRS
                   ALL   55       +3232    +3713     +481 |       +2761    +1709    -1052
       live-WIN boards   19       +2722    +3424     +702 |       +1158    +1134      -24
      live-LOSS boards   36       +3502    +3866     +364 |       +3607    +2013    -1594
             ALL excl2   53       +3398    +3670     +272 |       +3131    +1962    -1169
```

## Findings

### 1. Sim fidelity (55 boards, pinned-town action-tape seat)

| theta | mean \|sim−eng\| margin | median | max | >500 | W/L agree | corr |
|---|---|---|---|---|---|---|
| live flow135_g350_gpfwdfv_gb028 | 285 | 61 | 1,930 | 9/55 | 100.0 % | 0.999 |
| flow167_g150 | 220 | 58 | 1,131 | 11/55 | 98.2 % | 1.000 |

The **delta** is what matters and it reproduces: sim d +3,249 vs engine d +3,232,
per-board corr **0.991**, mean |diff| 232. Own-purse mean error 143/170 coins, opponent
purse 187/245. 14 of 55 boards exceed 500 on either theta (list in `report.txt` §1); the
worst, 107044716 (−1,930 on the live theta), is the only board where sim and engine
disagree on W/L for either theta. Fidelity is good enough that every conclusion below,
drawn from the sim, is an engine conclusion.

### 2. Two-purse — this is GROWTH, not denial

| set | n | d margin | d OURS | d THEIRS |
|---|---|---|---|---|
| ALL (sim) | 55 | +3,249 (t 6.05) | **+3,644** | **+395** |
| live-WIN boards | 19 | +2,769 (t 2.77) | +3,287 | +519 |
| live-LOSS boards | 36 | +3,503 (t 5.52) | +3,833 | +330 |
| ALL excl 2 outliers | 53 | +3,411 (t 6.27) | +3,593 | +182 |

Engine numbers agree within ~100 coins on every row. The opponent tape's purse is
essentially **untouched** (+395 season-end, +182 excluding the two outliers) — the entire
gain is our own purse. This is the clean growth signature, not a displacement or
denial-handed-back one, and it is the same size on boards the live theta already won
(+2,769) as on boards it lost (+3,503), i.e. broad, not a few close-loss rescues.

Confirming breadth: 43/55 boards improve in the engine (44/55 in sim), 42 by more than
+1,000, only 8 lose more than 1,000. Percentiles of the engine per-board delta:
5/25/50/75/95 = −2,980 / +1,061 / +3,262 / +4,834 / +11,418.

**The 10 flipped tapes** (20 board-seats) are NOT all close losses: base margins run
−6,995 … −167, mean −2,700, median −2,210, and only 7/10 are inside ±2,500. Two big
rescues (106974180 base −6,385 → +5,699; 107154400 base −6,995 → +720) plus a spread of
narrow ones. The two largest flips are own-purse driven (+12,202 and +3,349/−4,057).

### 3. Ranked product / structural diff (season means, live set)

The single biggest change is **when we sell, not what**: 19.6 SELL rows move out of hour 1
into hour 18 (h1 113.4→93.8, h18 21.9→39.2). Total SELL rows fall 139.6→136.2 and units
sold are flat (1,363→1,357), but **realised price per unit rises 92.01→95.05 (+3.3 %)**
and revenue +3,484 — which is the whole margin. Units per row 9.78→9.96.

Product mix (coins at band quotes): WOOL −1,964, CARROT +1,720, WHEAT −1,246,
MELON −1,058, EGG +1,056, MILK −659, FERTILIZER −478; net −2,607 in *volume* terms, i.e.
the mix change alone loses coins and the price/hour effect more than pays for it.

Structure — day 0 is nearly identical (BUY_ANIMAL GOO1/COW3/SHE2 both; HIRE 4 both;
d0 wheat pump 53 both; BUY_LAND 2 both; nquad 3 both). The changes are all mid/late:

- d0 seed split WHE10/CAR9 → **WHE12/CAR7**; season CARROT seed 27.9→36.0, WHEAT 94.3→91.2.
- HIRE d2 2.11 → 2.67 (season hire flat, 264.7→263.5).
- Herd: WHEAT occupants +0.57, CARROT −0.46, TOMATO −0.51 (d10-28 mean); BUILD_COOP
  +0.6, BUILD_PASTURE −0.9 — a small coop-for-pasture swap. Season BUY_ANIMAL
  GOOSE 2.84→3.42, COW 7.75→7.31, SHEEP 6.38→5.93 (fewer sheep = the WOOL drop).
- Tiles by band: wheat up d0-19 (8.4→9.7, 14.8→16.2) then **down d20-29** (16.4→13.4),
  carrot up late (d25-29 6.0→9.5), melon shifted later (d10-14 9.4→7.6, d20-24 6.0→8.1).
  Planted tiles +1.0-1.3 in d15-24 with idle down 3.6→2.9 — slightly better board fill.
- Unit ops barely move (PASS −55 of 6,591); PLANT orders CARROT +7.8, WHEAT −3.4.

### 4. The dropped board — 107117102 (vs Xander), base +287 → −2,535 (engine)

One tape, counted twice for the "−2" in the brief; **flow166_g170 drops the same tape and
drops it harder** (+287 → −7,328). It is a board we barely won. In the sim our own purse
goes **UP** +7,518 (88,678 → 96,196) — we play it better — but the opponent's purse goes
up +10,963 (88,164 → 99,127). We sell 42 more units (1,286→1,328) and +9,109 revenue, but
the extra supply, concentrated d16-28 (EGG +72, CARROT +35, TOMATO +12, MELON +12 against
WOOL −45, MILK −14, STRAWBERRY −14), moves the quotes the tape then sells into. This is
the two-purse "denial handed back" signature in reverse: our growth feeds theirs. The
margin is positive to d16 (+226) and bleeds out d17-23 (−497 … −1,236), recovering
partially d24-29. Herd on that board: WHEAT 4.1→5.9, TOMATO 5.8→3.9.

### 5. Where the margin opens — d20-29, overwhelmingly

| band | cum d margin | opened in band | d OURS | d THEIRS |
|---|---|---|---|---|
| d0-4 | −181 | −181 | −181 | −0 |
| d5-9 | +245 | +426 | +247 | +2 |
| d10-14 | −32 | −277 | +111 | +143 |
| d15-19 | −256 | −223 | +172 | +428 |
| d20-24 | +936 | **+1,192** | +1,124 | +188 |
| d25-29 | +3,249 | **+2,313** | +3,644 | +395 |

**108 % of the season margin opens after d20**; through d19 we are 256 coins *behind*.
The pattern is identical on live-WIN boards (d20-29 +1,629/+1,879) and live-LOSS boards
(+961/+2,542). This is the late-harvest / late-sell-hour change cashing out, and it means
the edge is a *liquidation* edge, not an opening or a pot-race edge.

### 6. Head-to-head with flow166_g170 (engine, same 55 boards)

|  | live g135_g350 | flow167_g150 | flow166_g170 |
|---|---|---|---|
| win % | 34.5 | 50.9 (28/55) | **52.7 (29/55)** |
| mean margin | −294 | **+2,938** | +2,467 |
| d vs live | — | **+3,232 (t 5.93)** | +2,761 (t 4.02) |
| d excl 2 outliers | — | **+3,398 (t 6.15)** | +3,131 (t 4.79) |
| boards improved | — | 43/55 | 42/55 |
| worst 5 sum | — | **−17,562** | −37,682 |
| worst board | — | **−4,729** | −10,564 |
| P5 of per-board d | — | **−2,980** | −6,518 |
| d OURS / d THEIRS | — | +3,713 / +481 | +1,709 / −1,052 |

- Per-board delta correlation **0.699** (sim cross-check on the g170live npz: 0.697) —
  the two candidates are related but far from the same agent.
- **9/55 sign disagreements**, the largest: 107055322 (g167 +1,998, g166 −6,381),
  107131313 (−164 vs +6,905), 106978598 (+4,671 vs −776), 107032494 (−2,883 vs +2,580),
  106947809 (−3,921 vs +875).
- Paired D167 − D166 = **+471, t +0.95** (excl2 +267, t +0.55) — the mean-margin edge for
  g167 is **not** significant.
- Boards won by only one: g167-only **107154400** (+720 / −3,371); g166-only
  **107035330** (+3,971 / −5,326) and **107131313** (+3,364 / −3,705). The whole win-rate
  gap is those three boards, net one.
- Mechanism differs: g167 is pure growth (opponent +481); g166 gains 38 % of its margin
  by suppressing the tape (opponent −1,052, and −1,594 on live-LOSS boards).

## Recommendation

**flow166_g170 wins on the stated criterion (win rate first) by exactly one board of 55 —
inside the noise — while flow167_g150 wins every other read: +471 mean margin, a
2-point-higher t, and less than half the downside (worst-5 −17.6k vs −37.7k, worst board
−4.7k vs −10.6k).** If win rate is taken literally, upload g166; if the one-board gap is
treated as the coin flip it is, upload **flow167_g150** — it is the safer purse and the
cleaner (growth-only) mechanism.

Caveats: (a) the "+20/−2" and "52.7 vs 50.9 %" reads rest on 55 unique games, not 110 —
one board is 1.8 points, and a single board separates the candidates; (b) both candidates
open their margin only after d20, so both are exposed to any late-season market change;
(c) both drop the same board (107117102) for the same reason — our extra late supply
lifts the opponent's realised prices — and g166 drops it 2.9x harder.

## Raw sim/engine report

```
==============================================================================
1. SIM vs ENGINE FIDELITY  (55 board-seats = seat0 only)
==============================================================================
 init: sim margin     -231 win  34.5%   engine margin     -294 win  34.5%
       |sim-eng| margin: mean      285  median       61  max     1930   >500 on 9/55 boards
       |sim-eng| own purse mean     143 max    2242;  opp purse mean     187 max     966
       W/L agreement 100.0%   corr(sim,eng) 0.999
  rec: sim margin    +3018 win  52.7%   engine margin    +2938 win  50.9%
       |sim-eng| margin: mean      220  median       58  max     1131   >500 on 11/55 boards
       |sim-eng| own purse mean     170 max    2007;  opp purse mean     245 max    2971
       W/L agreement  98.2%   corr(sim,eng) 1.000

DELTA (g167_g150 - live): sim    +3249   engine    +3232   corr 0.991   mean|diff| 232

boards with |sim-eng| margin > 500 (either theta):
      tape   st  init_sim  init_eng        d   rec_sim   rec_eng        d
 106964817    0    +16030    +17090    -1060    +16342    +16268      +74
 106985187    0     -1028     -2281    +1253     +7721     +8852    -1131
 106994269    0     +6624     +8235    -1611    +11944    +12621     -677
 107015564    0     +4765     +4395     +370     +8248     +7657     +591
 107018738    0     -3126     -3535     +409       -31      -640     +609
 107023915    0        -5     -1056    +1051     -1378     -2112     +734
 107040955    0      -592     -1314     +722     -5160     -6043     +883
 107044716    0     -3806     -1876    -1930      +293       -85     +378
 107055322    0    +16579    +17495     -916    +18660    +19493     -833
 107072760    0     -2099     -2461     +362     +3154     +2553     +601
 107089992    0     -1717     -1918     +201      -354     -1078     +724
 107095149    0    -13555    -13960     +405    -14071    -14752     +681
 107101394    0    +17938    +16266    +1672    +18491    +17527     +964
 107160628    0    -10425    -11105     +680     -6405     -6255     -150
(count 14 of 55)

==============================================================================
2. TWO-PURSE on the live set (rec - init)
==============================================================================
                     set    n   init_m    rec_m        d      t    dOURS  dTHEIRS  win%i  win%r
                     ALL   55     -231    +3018    +3249  +6.05    +3644     +395   34.5   52.7
   WIN-boards (live won)   19   +12060   +14828    +2769  +2.77    +3287     +519  100.0   94.7
 LOSS-boards (live lost)   36    -6719    -3216    +3503  +5.52    +3833     +330    0.0   30.6
     ALL excl 2 outliers   53     +167    +3578    +3411  +6.27    +3593     +182   35.8   54.7

-- same table on ENGINE numbers (for reference)
                     ALL   55     -294    +2938    +3232  +5.93    +3713     +481   34.5   50.9
   WIN-boards (live won)   19   +12104   +14826    +2722  +2.76    +3424     +702  100.0   94.7
 LOSS-boards (live lost)   36    -6838    -3336    +3502  +5.34    +3866     +364    0.0   27.8
     ALL excl 2 outliers   53     +111    +3509    +3398  +6.15    +3670     +272   35.8   52.8

-- FLIPPED boards (engine L->W), base margin and where the swing came from (sim purses)
      tape  st  eng_base   eng_new  sim_base   sim_new     simd    dOURS  dTHEIRS
 107154400   0     -6995      +720     -6929      +477    +7406    +3349    -4057
 106974180   0     -6385     +5699     -6311     +5759   +12070   +12202     +132
 106968689   0     -4823     +1991     -4859     +1945    +6804    +7764     +960
 107072760   0     -2461     +2553     -2099     +3154    +5253    +7879    +2626
 106985187   0     -2281     +8852     -1028     +7721    +8749    +5938    -2811
 107008497   0     -2139     +4512     -1953     +4806    +6759    +5838     -921
 107068399   0     -1118      +436     -1168      +390    +1558    +2198     +640
 107016108   0      -338     +2181      -274     +2172    +2446    +7255    +4809
 107116818   0      -295     +3918      -324     +3893    +4217    +4250      +33
 107108124   0      -167     +2957      -121     +3005    +3126    +3345     +219
flipped n=10  mean base margin -2700  median -2210  |base|<2500 on 7/10

-- broad-gain check: distribution of engine d-margin over all 55 boards
  pct 5/25/50/75/95 = -2980 +1061 +3262 +4834 +11418   boards improved 43/55  >+1000 42  <-1000 8
  sim d-margin: pct -3279 +1054 +3373 +4870 +10484   improved 44/55

==============================================================================
3. RANKED PRODUCT / STRUCTURAL DIFF (rec - init, live set, season)
==============================================================================
  product          dqty     coins
  WOOL            -11.8     -1964
  CARROT          +31.6     +1720
  WHEAT           -27.4     -1246
  MELON            +0.4     -1058
  EGG             +20.3     +1056
  MILK             -5.8      -659
  FERTILIZER      -12.2      -478
  TOMATO           +0.5       +38
  STRAWBERRY       -4.3       -17
  TOTAL            -8.8     -2607

-- ordered sell qty by product x 5-day band (init -> rec), coins
  d 0-4   tot     -205  | CARROT    -205  WHEAT      +0  TOMATO      +0  STRAWB      +0
  d 5-9   tot     +338  | WHEAT    +258  WOOL    +134  CARROT     -47  FERTIL     -11
  d10-14  tot     -296  | STRAWB    +300  WOOL    -276  FERTIL    -268  MILK    -168
  d15-19  tot    -1375  | MELON   -1654  WOOL    -634  STRAWB    +525  EGG    +290
  d20-24  tot     -469  | MELON    -339  EGG    +312  WOOL    -171  MILK    -168
  d25-29  tot     -601  | CARROT   +1814  WHEAT   -1506  WOOL   -1018  MELON    +935

== STRUCTURE (season / eod means) ==
  BUY_ANIMAL season                    init=GOO2.84/COW7.75/SHE6.38   rec=GOO3.42/COW7.31/SHE5.93
  BUY_ANIMAL d0                        init=GOO1.00/COW3.00/SHE2.00   rec=GOO1.00/COW3.00/SHE2.00
  BUY_SEED d0                          init=WHE10.00/CAR9.00/TOM0.00/STR0.00/MEL0.00   rec=WHE12.00/CAR7.00/TOM0.00/STR0.00/MEL0.00
  BUY_SEED season                      init=WHE94.3/CAR27.9/TOM4.7/STR29.5/MEL15.4   rec=WHE91.2/CAR36.0/TOM5.2/STR28.8/MEL15.7
  HIRE qty d0/d1/d2                    init=4.00/1.00/2.11   rec=4.00/1.00/2.67
  HIRE qty season                      init=264.69   rec=263.53
  hands d1 / d5 / d10-28               init=0.00/0.00/0.00   rec=0.00/0.00/0.00
  nquad d29                            init=3.00   rec=3.00
  BUY_LAND rows                        init=2.00   rec=2.00
  SELL rows executed (season)          init=139.4   rec=136.2
  sold units / revenue                 init=1363/125449   rec=1357/128933
  realised price/unit                  init=92.01   rec=95.05
  units per SELL row                   init=9.78   rec=9.96
  OPP rev / units / rows               init=128537/1550.1/250.4   rec=128956/1549.9/250.4
  d0 wheat pump (BUY_PRODUCT WHEAT)    init=53.0   rec=53.0
  final purse ours/theirs              init=100752/100984   rec=104396/101379

-- market row types (season)
  0              init= 6712.27  rec= 6717.36  d    +5.09
  HIRE           init=  264.69  rec=  263.53  d    -1.16
  BUY_LAND       init=    2.00  rec=    2.00  d    +0.00
  BUY_SEED       init=   52.40  rec=   51.05  d    -1.35
  BUY_ANIMAL     init=   11.65  rec=   11.58  d    -0.07
  BUY_PRODUCT    init=   17.38  rec=   18.18  d    +0.80
  SELL           init=  139.60  rec=  136.29  d    -3.31

-- HERD by occupant (eod mean d10-28)
  WHEAT        init= 2.74  rec= 3.31  d +0.57
  CARROT       init= 7.61  rec= 7.15  d -0.46
  TOMATO       init= 6.08  rec= 5.57  d -0.51

-- TILES by crop, by 5-day band (eod mean, init->rec)
  d 0-4   WHEA  8.4-> 9.7 | CARR  5.6-> 4.5 | TOMA  0.0-> 0.0 | STRA  2.0-> 2.2 | MELO  0.0-> 0.0
  d 5-9   WHEA  8.2-> 7.5 | CARR  1.2-> 1.2 | TOMA  0.0-> 0.0 | STRA 19.6->20.3 | MELO  1.4-> 0.6
  d10-14  WHEA 14.8->16.2 | CARR  0.1-> 0.2 | TOMA  0.2-> 0.3 | STRA 27.2->27.6 | MELO  9.4-> 7.6
  d15-19  WHEA 10.0->10.6 | CARR  0.3-> 0.3 | TOMA  1.8-> 1.6 | STRA 29.2->28.7 | MELO 13.2->14.2
  d20-24  WHEA 14.9->12.8 | CARR  3.1-> 5.3 | TOMA  4.4-> 4.7 | STRA 17.1->16.0 | MELO  6.0-> 8.1
  d25-29  WHEA 16.4->13.4 | CARR  6.0-> 9.5 | TOMA  3.9-> 4.2 | STRA  4.1-> 2.7 | MELO  0.9-> 1.0

-- planted / idle tiles by band (eod mean, init->rec)
  d 0-4   planted  16.0-> 16.4   idle   2.9->  2.6   coop  1.0-> 1.0  pasture  5.1-> 5.0
  d 5-9   planted  30.3-> 29.6   idle  10.6-> 11.3   coop  1.2-> 1.5  pasture  7.9-> 7.6
  d10-14  planted  51.8-> 51.9   idle   6.6->  7.0   coop  2.7-> 3.2  pasture 13.9->12.9
  d15-19  planted  54.4-> 55.4   idle   3.6->  2.9   coop  2.8-> 3.4  pasture 14.1->13.2
  d20-24  planted  45.5-> 46.8   idle  12.5-> 11.6   coop  2.8-> 3.4  pasture 14.1->13.2
  d25-29  planted  31.2-> 30.8   idle  26.8-> 27.6   coop  2.8-> 3.4  pasture 14.1->13.2

-- ordered SELL rows by hour (season, init->rec)
  h1   init=113.38  rec= 93.80  d -19.58
  h3   init=  0.95  rec=  0.53  d  -0.42
  h10  init=  3.42  rec=  2.82  d  -0.60
  h18  init= 21.85  rec= 39.15  d +17.29

-- PLANNED unit ops (unmasked, season sum)
  PASS           init=   6590.6  rec=   6535.3  d     -55.3
  EAST           init=    816.1  rec=    835.3  d     +19.2
  NORTH          init=    538.2  rec=    554.6  d     +16.3
  WEST           init=    975.4  rec=    988.1  d     +12.7
  COLLECT_FERTILIZER init=    380.4  rec=    369.7  d     -10.7
  WATER          init=    853.6  rec=    861.9  d      +8.3
  HARVEST        init=    419.9  rec=    426.0  d      +6.1
  SOUTH          init=    331.0  rec=    325.8  d      -5.2
  PLANT          init=    171.7  rec=    176.1  d      +4.4
  FERTILIZE      init=    183.8  rec=    187.7  d      +3.9
  PICKUP         init=    302.8  rec=    306.1  d      +3.3
  FEED           init=    314.3  rec=    311.8  d      -2.5
  CARE           init=    292.7  rec=    293.6  d      +0.9
  BUILD_PASTURE  init=     14.1  rec=     13.2  d      -0.9
  BUILD_COOP     init=      2.8  rec=      3.4  d      +0.6
  DROP           init=     10.3  rec=      9.8  d      -0.4
  DIG            init=     25.2  rec=     24.8  d      -0.3
  PLACE          init=     17.0  rec=     16.7  d      -0.3

-- PLANT orders by crop (unmasked, season)
  WHEAT        init=   94.3  rec=   90.9  d    -3.4
  CARROT       init=   27.8  rec=   35.6  d    +7.8
  TOMATO       init=    4.7  rec=    5.1  d    +0.4
  STRAWBERRY   init=   29.5  rec=   28.8  d    -0.7
  MELON        init=   15.4  rec=   15.7  d    +0.3

==============================================================================
4. DROPPED BOARDS (engine W->L): 107117102
==============================================================================
n=1  engine +287 -> -2535   sim +514 -> -2931
  sim ours 88678 -> 96196  (+7518)   theirs 88164 -> 99127  (+10963)

  per-day (drop board): d, cash init->rec, opp init->rec, hands, planted, sold_n, sold_rev
  d0   cash       36->      56 (    +20)  opp       70->      70  hands  0.0-> 0.0  plant 19.0->19.0  soldn  48.0-> 48.0  rev    1463->   1463
  d1   cash        6->      26 (    +20)  opp      133->     133  hands  0.0-> 0.0  plant 19.0->19.0  soldn  48.0-> 48.0  rev    1463->   1463
  d2   cash      596->     616 (    +20)  opp      246->     246  hands  0.0-> 0.0  plant 19.0->19.0  soldn  54.0-> 54.0  rev    2055->   2055
  d3   cash      679->     609 (    -70)  opp      327->     327  hands  0.0-> 0.0  plant 14.0->16.0  soldn  60.0-> 60.0  rev    2635->   2635
  d4   cash     1454->    1284 (   -170)  opp      726->     726  hands  0.0-> 0.0  plant  9.0-> 9.0  soldn  93.0-> 87.0  rev    4072->   3892
  d5   cash     1039->     997 (    -42)  opp      831->     829  hands  0.0-> 0.0  plant 25.0->20.0  soldn 135.0->137.0  rev    5760->   5802
  d6   cash      637->     611 (    -26)  opp      835->     834  hands  0.0-> 0.0  plant 32.0->28.0  soldn 142.0->144.0  rev    6350->   6392
  d7   cash     2222->    2265 (    +43)  opp      553->     550  hands  0.0-> 0.0  plant 35.0->33.0  soldn 157.0->160.0  rev    8510->   8639
  d8   cash     1633->    1576 (    -57)  opp     1368->    1363  hands  0.0-> 0.0  plant 38.0->36.0  soldn 165.0->171.0  rev    9122->   9386
  d9   cash     3582->    3915 (   +333)  opp     2257->    2244  hands  0.0-> 0.0  plant 37.0->38.0  soldn 194.0->197.0  rev   12305->  12492
  d10  cash     1660->    2468 (   +808)  opp    15789->   15770  hands  0.0-> 0.0  plant 49.0->50.0  soldn 219.0->216.0  rev   14566->  14568
  d11  cash     1659->    2653 (   +994)  opp    15838->   15813  hands  0.0-> 0.0  plant 54.0->56.0  soldn 235.0->235.0  rev   15842->  16020
  d12  cash      741->    1218 (   +477)  opp    18550->   18518  hands  0.0-> 0.0  plant 57.0->59.0  soldn 237.0->239.0  rev   15948->  16232
  d13  cash     2489->    2922 (   +433)  opp    20407->   20405  hands  0.0-> 0.0  plant 56.0->59.0  soldn 256.0->260.0  rev   18028->  18532
  d14  cash     3540->    4777 (  +1237)  opp    23624->   23637  hands  0.0-> 0.0  plant 55.0->56.0  soldn 273.0->288.0  rev   19898->  21276
  d15  cash     7679->    9190 (  +1511)  opp    26778->   26779  hands  0.0-> 0.0  plant 55.0->57.0  soldn 325.0->360.0  rev   24475->  26322
  d16  cash    15560->   15786 (   +226)  opp    34554->   34991  hands  0.0-> 0.0  plant 56.0->59.0  soldn 373.0->408.0  rev   33191->  33468
  d17  cash    22523->   22026 (   -497)  opp    39102->   39554  hands  0.0-> 0.0  plant 57.0->59.0  soldn 432.0->456.0  rev   40640->  40174
  d18  cash    30492->   29195 (  -1297)  opp    45078->   45824  hands  0.0-> 0.0  plant 56.0->59.0  soldn 482.0->505.0  rev   49582->  48180
  d19  cash    40022->   37360 (  -2662)  opp    49945->   51096  hands  0.0-> 0.0  plant 57.0->59.0  soldn 561.0->577.0  rev   59275->  56791
  d20  cash    47693->   45660 (  -2033)  opp    55617->   56948  hands  0.0-> 0.0  plant 54.0->55.0  soldn 622.0->642.0  rev   67905->  65557
  d21  cash    55412->   52924 (  -2488)  opp    61564->   63273  hands  0.0-> 0.0  plant 50.0->53.0  soldn 690.0->714.0  rev   76080->  73337
  d22  cash    61131->   60046 (  -1085)  opp    64194->   66678  hands  0.0-> 0.0  plant 39.0->48.0  soldn 765.0->787.0  rev   82052->  81293
  d23  cash    64523->   63287 (  -1236)  opp    66605->   70601  hands  0.0-> 0.0  plant 38.0->44.0  soldn 829.0->848.0  rev   85667->  84936
  d24  cash    65467->   66668 (  +1201)  opp    69422->   74893  hands  0.0-> 0.0  plant 38.0->42.0  soldn 858.0->894.0  rev   87076->  88997
  d25  cash    69155->   72375 (  +3220)  opp    71000->   77167  hands  0.0-> 0.0  plant 40.0->41.0  soldn 922.0->964.0  rev   91077->  95146
  d26  cash    71303->   75957 (  +4654)  opp    72390->   79167  hands  0.0-> 0.0  plant 38.0->41.0  soldn 964.0->1018.0  rev   93508->  99588
  d27  cash    75329->   80246 (  +4917)  opp    76245->   84065  hands  0.0-> 0.0  plant 33.0->36.0  soldn 1035.0->1083.0  rev   97787-> 104206
  d28  cash    79740->   86109 (  +6369)  opp    79519->   88739  hands  0.0-> 0.0  plant 21.0->25.0  soldn 1115.0->1157.0  rev  102286-> 110191
  d29  cash    88678->   96196 (  +7518)  opp    88164->   99127  hands  9.0->10.0  plant  2.0-> 6.0  soldn 1286.0->1328.0  rev  111312-> 120421

  drop board: ordered sell qty by product (season, init->rec)
    EGG            139.0 ->   211.0  d   +72.0
    WOOL           152.0 ->   107.0  d   -45.0
    CARROT         169.0 ->   204.0  d   +35.0
    STRAWBERRY     275.0 ->   261.0  d   -14.0
    MILK            81.0 ->    67.0  d   -14.0
    TOMATO           8.0 ->    20.0  d   +12.0
    MELON           84.0 ->    96.0  d   +12.0
    FERTILIZER     132.0 ->   124.0  d    -8.0
    WHEAT          252.0 ->   254.0  d    +2.0
  drop board: herd d10-28 WHEAT 4.1->5.9 CARRO 3.9->3.8 TOMAT 5.8->3.9
  drop board: BUY_ANIMAL d0 init GOO1.0/COW3.0/SHE2.0  rec GOO1.0/COW3.0/SHE2.0

==============================================================================
5. WHERE THE MARGIN OPENS (per-day, all 55 boards)
==============================================================================
  d   ours_i   ours_r   dOURS theirs_i  dTHEIRS  dMARGIN dMARG/day       hands       plant        idle         soldn
  0       49       69     +20       54       +0      +20       +20  0.00-> 0.00  19.0-> 19.0   0.0->  0.0   48.0->  48.0
  1       19       39     +20      161       +0      +20        +0  0.00-> 0.00  19.0-> 19.0   0.0->  0.0   48.0->  48.0
  2      607      606      -1      196       +0       -1       -21  0.00-> 0.00  19.0-> 19.0   0.0->  0.0   54.0->  54.0
  3      625      599     -26      215       +0      -26       -26  0.00-> 0.00  14.0-> 16.0   4.9->  3.0   60.0->  60.0
  4     1478     1297    -181      376       -0     -181      -155  0.00-> 0.00   9.2->  8.9   9.6-> 10.0   93.0->  87.0
  5      768      961    +192      465       -1     +193      +374  0.00-> 0.00  23.1-> 19.5  19.4-> 23.1  134.9-> 136.9
  6      647      650      +3      752       +1       +2      -191  0.00-> 0.00  27.3-> 26.1  14.9-> 15.9  142.4-> 144.3
  7     2432     2541    +110      432       +1     +109      +107  0.00-> 0.00  31.1-> 30.1  11.0-> 11.8  159.2-> 161.6
  8     1573     1732    +160     1115       +7     +153       +44  0.00-> 0.00  35.4-> 36.1   4.2->  3.5  171.2-> 175.0
  9     4539     4786    +247     2308       +2     +245       +92  0.00-> 0.00  34.6-> 35.9   3.6->  2.4  201.4-> 202.7
 10     2913     3322    +409    16891       +0     +409      +164  0.00-> 0.00  45.0-> 44.9  14.3-> 15.2  230.2-> 227.6
 11     3551     4028    +476    17099      +13     +464       +55  0.00-> 0.00  51.2-> 51.0   7.2->  7.9  248.2-> 246.9
 12     3042     3048      +7    20659      +26      -19      -482  0.00-> 0.00  54.0-> 53.8   4.1->  4.6  255.1-> 253.2
 13     5709     5751     +42    22838      +62      -21        -2  0.00-> 0.00  55.0-> 55.4   3.0->  3.1  281.8-> 278.7
 14     8069     8180    +111    26798     +143      -32       -12  0.00-> 0.00  53.7-> 54.2   4.3->  4.2  308.3-> 307.1
 15    12885    13013    +128    31718     +317     -189      -157  0.00-> 0.00  54.1-> 54.7   3.9->  3.7  365.6-> 366.4
 16    19344    19459    +115    38688     +348     -233       -44  0.00-> 0.00  54.6-> 55.2   3.5->  3.1  424.0-> 424.2
 17    25780    26381    +600    44134     +407     +193      +426  0.00-> 0.00  54.8-> 55.9   3.2->  2.5  479.7-> 483.3
 18    33206    33331    +126    50317     +414     -289      -482  0.00-> 0.00  54.4-> 55.8   3.6->  2.6  535.3-> 537.1
 19    41175    41348    +172    54901     +428     -256       +33  0.00-> 0.00  54.1-> 55.5   4.0->  2.8  607.4-> 606.5
 20    48762    48227    -534    59893     +346     -880      -624  0.00-> 0.00  50.8-> 51.5   7.2->  6.9  674.4-> 669.8
 21    56198    55383    -814    65362     +260    -1074      -194  0.00-> 0.00  47.8-> 49.1  10.2->  9.3  745.6-> 739.8
 22    62863    62890     +27    70038      +87      -60     +1014  0.00-> 0.00  42.9-> 45.5  15.2-> 12.9  819.0-> 812.2
 23    67413    67902    +490    73048     +189     +301      +361  0.00-> 0.00  43.0-> 43.9  15.0-> 14.5  877.9-> 872.1
 24    70636    71761   +1124    76273     +188     +936      +635  0.00-> 0.00  43.2-> 44.1  14.9-> 14.2  925.6-> 923.8
 25    75173    77492   +2319    79743     +129    +2189     +1253  0.00-> 0.00  41.8-> 41.9  16.3-> 16.5  987.3-> 987.9
 26    78693    81501   +2807    83395     +117    +2691      +502  0.00-> 0.00  40.9-> 40.8  17.1-> 17.6 1042.7->1044.3
 27    83922    87254   +3333    87277     +250    +3083      +392  0.00-> 0.00  37.5-> 36.6  20.6-> 21.8 1114.1->1116.3
 28    89179    92835   +3656    92834     +364    +3292      +209  0.00-> 0.00  27.0-> 25.6  31.1-> 32.8 1190.7->1190.1
 29   100752   104396   +3644   100984     +395    +3249       -43  9.40-> 8.96   9.0->  9.2  49.1-> 49.2 1363.4->1356.5

-- margin opened per 5-day band (sim, eod cash difference)
  d 0-4    cum dMARGIN     -181   opened in band     -181   (ours     -181, theirs       -0)
  d 5-9    cum dMARGIN     +245   opened in band     +426   (ours     +247, theirs       +2)
  d10-14   cum dMARGIN      -32   opened in band     -277   (ours     +111, theirs     +143)
  d15-19   cum dMARGIN     -256   opened in band     -223   (ours     +172, theirs     +428)
  d20-24   cum dMARGIN     +936   opened in band    +1192   (ours    +1124, theirs     +188)
  d25-29   cum dMARGIN    +3249   opened in band    +2313   (ours    +3644, theirs     +395)

-- same, WIN-boards vs LOSS-boards
  WIN  d 0-4   cum     -186  band     -186
  WIN  d 5-9   cum     +302  band     +488
  WIN  d10-14  cum      +13  band     -289
  WIN  d15-19  cum     -740  band     -753
  WIN  d20-24  cum     +889  band    +1629
  WIN  d25-29  cum    +2769  band    +1879
  LOSS d 0-4   cum     -178  band     -178
  LOSS d 5-9   cum     +215  band     +393
  LOSS d10-14  cum      -56  band     -271
  LOSS d15-19  cum       -0  band      +56
  LOSS d20-24  cum     +961  band     +961
  LOSS d25-29  cum    +3503  band    +2542

==============================================================================
6. HEAD-TO-HEAD  flow167_g150 vs flow166_g170 (engine, same 55 boards)
==============================================================================
  win%: live 34.5  g167 50.9  g166 52.7
  mean d: g167 +3232 (t 5.93)   g166 +2761 (t 4.02)
  excl2 : g167 +3398  g166 +3131
  corr(D167,D166) = 0.699;  paired D167-D166 +471 t +0.95
  sign disagreements 9/55
  worst5 g167: 107040955-4729 106947809-3921 107090008-3207 107032494-2883 107117102-2822  sum -17562  min -4729
  worst5 g166: 107088554-10564 107117102-7615 107040955-6669 106964817-6453 107055322-6381  sum -37682  min -10564

  SIM cross-check (g170live npz): g166 sim d +2814  g167 sim d +3249  corr 0.697
```
