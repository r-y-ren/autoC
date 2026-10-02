Stream: PROGRAMME3R (remote-only)
Date: 2026-09-30 (committed by DOCSYNC1; verbatim S/programme3r/results.txt, patch tree.diff, splits hold20.txt / tune20.txt)
Verdict: NONE - direct MMPQ rulebook executor (PROG_RB_DIRECT_ON), held-out ratio 0.805; V56 m40 W 0/40 dmargin -44,428 t -17.5, p48c -29,773 t -11.5

```
PROGRAMME3R results 2026-09-30T05:55Z (remote only; /mnt/e down). Tree: /home/user/stage_r/programme3r/tree_j4 (= copy of programme2r/tree + prog/direct.py + PROG_RB_DIRECT_ON hook); tree.diff vs programme2r/tree.
Executor: src/kagg3/prog/direct.py DirectAgent behind plan.PROG_RB_DIRECT_ON (runtime.act returns it first; no planner). Market = rulebook state machine
(d0 h0-h9 literal lists; SELL->HIRE->BUY_ANIMAL->BUY_LAND->BUY_SEED->BUY_PRODUCT; fixed wool/milk/melon lots d6-d12; milk/wool/straw sell-all at h1/5/9/13/17/21,
crops+eggs dusk h22-23 + dawn h0-1 keeping a feed-wheat reserve; land Q2 d6h3 / Q3 d8h6 (d9h3 if yarn<=d6) / Q4 d10h6 retried every step; hands 4,4,5,6,6,6,9,8,9,10,12..12,11,10;
herd by yarn/milk/egg draw; standing-tile crop targets by shop demand, wheat filler, no planting after d27). Units = greedy tile-task dispatcher (two passes: own-tile task, then
nearest task by distance+priority; shed jobs for animal/feed pickups) + d0 h0-h9 modal MMPQ unit tape. Knobs via env PROG3_KNOBS (defaults = the tuned values).

== FIDELITY: tuning 20 (programme2r fid20; used for tuning) ==
fin_j4_tune.jsonl n 20 | land exact 18 | d9 herd within1 5 | final>=90% 1 | ratio mean 0.740 med 0.735 min 0.637 | idle/day 1.9 (T 0.9) | wheat 261 (T 592) | str15-17 25.2 (T 50.0) | egg18-29 106.2 (T 147.0) | water/day 58.2 (T 56.6) | esc 11.6 (T 10.6) | term 10.9 (T 0.1) | p99 max 0.002
  first divergent step: market closed-loop median 9.0 | market teacher-forced median 9.0 | unit closed-loop median 10.0
  TF market-list match rate d0-9 0.349 d10-19 0.139 d20-29 0.149
  ep        opp            ratio   truth    ours  fd_mkt fd_unit tf_mkt land  herd(T/O d9 S-C-G)  idle T/O  wheat T/O  str T/O  egg T/O
  115305929 mudesteven     0.637  120227   76611     4      6      4 Y 3-5-8/3-5-4  0.4/ 1.9  546/ 269  48/ 35 184/140
  115284618 dong & shen    0.645  117489   75723     4      6      4 Y 11-3-5/8-3-3  0.9/ 2.7  487/ 176  29/ 16 145/ 62
  115281895 Rudolf HOUNLET 0.648  155187  100536     4      6      4 Y 3-5-6/3-5-4  0.7/ 0.8  557/ 191  64/ 43 172/120
  115295770 Kosuke.T       0.657  132082   86842    14     10     14 Y 3-5-7/3-5-3  1.4/ 1.6  581/ 244  64/ 43 235/117
  115297154 Pavel Filin    0.687   90961   62489    14     10     14 Y 3-8-5/3-7-5  0.9/ 1.8  710/ 382  51/ 23 278/166
  115316776 JR             0.694   96211   66806    14     10     14 Y 3-5-8/3-5-4  0.4/ 1.5  624/ 272  54/ 32 258/165
  115300199 Simon Rüba     0.698  121652   84969     4      6      4 Y 3-7-7/3-7-4  0.3/ 3.4  777/ 488  50/ 37 195/125
  115287407 Zorvella       0.701  125493   87929    14     10     14 Y 10-7-0/6-6-3  0.4/ 2.8  760/ 377  46/ 11  71/102
  115292955 yt0914         0.721  142833  102949    14     10     14 Y 11-3-2/8-3-2  0.7/ 2.1  532/ 239  44/ 18  85/ 97
  115283256 Alan Smith     0.725  123536   89585     4      6      4 Y 3-5-7/3-5-3  1.0/ 1.7  446/ 178  64/ 37 192/118
  115277707 Muhammed Ali K 0.744  188000  139844    14     10     14 Y 3-10-2/3-10-0  1.1/ 1.2  482/ 173  55/ 31  96/ 35
  115290180 Vikram         0.744  125883   93661     9     10      9 Y 3-7-6/3-7-3  0.7/ 2.1  708/ 310  52/ 17 144/ 93
  115288831 Adam Plow      0.752  127963   96270    14     10     14 Y 10-7-0/7-5-2  0.6/ 1.2  748/ 345  41/ 21  77/106
  115307119 tetsuro731     0.755  128811   97246     9     10      9 Y 3-8-3/3-7-3  0.3/ 0.8  637/ 174  62/ 25 109/ 99
  115279125 Chikkam Sandee 0.761  178637  135938     4      6      4 Y 3-8-5/3-7-5  1.5/ 1.6  400/ 151  57/  8 149/105
  115280498 Jithendra Madd 0.768  135248  103840     4      6      4 n 10-3-1/9-4-2  0.8/ 2.6  638/ 209  40/ 22 134/105
  115303056 Arpit Gole     0.784  153108  119972     9     10      9 Y 3-11-2/3-9-1  2.4/ 2.2  570/ 290  54/ 24  79/ 72
  115291571 xxxxyt         0.788  120579   95015     9     10      9 n 10-6-0/8-4-1  0.7/ 1.9  692/ 358  35/ 19  62/ 75
  115286005 Vibe Farmer    0.802  136499  109498    14     10     14 Y 10-7-0/9-4-2  1.1/ 2.4  391/ 162  37/ 17  94/ 80
  115283309 Pilea55        1.092  112028  122372     9     10      9 Y 3-7-3/3-7-4  1.2/ 2.5  550/ 227  54/ 26 181/141

== FIDELITY: held-out 20 (hold20.txt: V5 P48 6 DSM3 PQ4 3 other3, never used for tuning) ==
fin_j4_hold.jsonl n 20 | land exact 19 | d9 herd within1 3 | final>=90% 2 | ratio mean 0.805 med 0.788 min 0.586 | idle/day 2.5 (T 0.8) | wheat 286 (T 580) | str15-17 21.6 (T 45.6) | egg18-29 110.0 (T 164.3) | water/day 57.9 (T 58.4) | esc 11.1 (T 9.9) | term 8.3 (T 1.1) | p99 max 0.001
  first divergent step: market closed-loop median 9.0 | market teacher-forced median 9.0 | unit closed-loop median 10.0
  TF market-list match rate d0-9 0.349 d10-19 0.167 d20-29 0.192
  ep        opp            ratio   truth    ours  fd_mkt fd_unit tf_mkt land  herd(T/O d9 S-C-G)  idle T/O  wheat T/O  str T/O  egg T/O
  115331095 tomfng         0.586  122457   71747     9     10      9 Y 11-3-4/8-3-3  0.8/ 3.9  661/ 541  28/ 13 139/ 48
  115500225 DSM            0.652   88914   58007    14     10     14 Y 3-5-7/3-5-4  0.6/ 3.0  516/ 336  56/ 36 225/131
  115332535 XIAO MA        0.663  115220   76339     9     10      9 Y 3-5-7/3-5-4  0.6/ 2.3  401/ 175  52/ 26 175/123
  115338216 sAIzeria Harne 0.713   89248   63658     9     10      9 Y 3-5-8/3-5-4  1.0/ 1.6  711/ 377  54/ 29 339/260
  115381317 Majkel1337     0.727  130256   94711     9     10      9 Y 3-5-7/3-5-5  0.4/ 0.7  525/ 130  47/ 31 182/103
  115511452 Victor @ Tufa  0.732  123321   90281    14     10     14 Y 3-8-3/3-7-2  0.5/ 1.4  607/ 204  50/ 27 110/ 91
  115375047 Boey           0.739   73128   54034     4      6      4 Y 3-9-6/3-7-4  1.0/ 4.1  609/ 375  28/ 19 207/127
  115329573 Fedor          0.742  125406   93047     9     10      9 Y 3-5-7/3-5-4  0.7/ 1.1  442/ 279  54/ 35 159/104
  115516474 .              0.775  105827   81993    14     10     14 Y 3-8-4/3-8-2  0.8/ 1.3  725/ 290  50/ 10 137/109
  115489055 DSM            0.783   94676   74165    14     10     14 Y 3-8-2/3-7-2  0.8/ 2.0  350/ 272  62/ 25 179/122
  115332044 senkin13       0.793  151722  120304    14     10     14 Y 3-12-0/3-9-2  0.4/ 2.9  649/ 290  52/ 17  89/ 69
  115527664 DECEM          0.794   93667   74365     9     10      9 Y 3-8-3/3-8-3  1.1/ 2.2  612/ 354  57/ 11 242/151
  115495284 DSM            0.812  104989   85207    14     10     14 n 12-3-1/7-4-1  0.5/ 7.8  723/ 243  38/ 14 173/136
  115483954 Victor @ Tufa  0.816  119124   97182    14     10     14 Y 3-5-7/3-5-4  1.1/ 1.5  452/ 230  50/ 37 218/165
  115364745 Majkel1337     0.859  124613  107088     4      6      4 Y 15-3-0/8-4-0  0.9/ 1.7  552/ 282  22/ 26  95/ 43
  115464540 Vadim Vasilenk 0.860  129616  111442     9     10      9 Y 10-5-1/7-4-2  0.6/ 2.1  396/ 179  52/ 22  84/ 57
  115469218 Unknown Mother 0.876  102830   90116    14     10     14 Y 3-11-3/3-9-2  0.9/ 2.3  757/ 246  47/ 10 117/ 92
  115478811 Victor @ Tufa  0.900  125208  112634    14     10     14 Y 11-5-0/7-4-2  1.2/ 2.3  638/ 334  34/ 20  91/ 61
  115527662 DECEM          1.134   95360  108136     9     10      9 Y 3-8-3/3-8-5  0.9/ 2.9  553/ 267  55/  7 117/101
  115522605 DECEM          1.146  101866  116775     9     10      9 Y 10-5-3/7-4-2  0.6/ 1.9  725/ 309  24/ 18 208/106

== first-divergence progress on tune20 (median step; market = exact order list vs MMPQ's at the same step; unit = farmer+hands list) ==
start v1 (r_a1):   first divergent step: market closed-loop median 9.0 | market teacher-forced median 9.0 | unit closed-loop median 0.0
end j4:          first divergent step: market closed-loop median 9.0 | market teacher-forced median 9.0 | unit closed-loop median 10.0

== runtime-hook cross-check (fid.py, PROGRAMME2R harness, runtime.make_agent + --sw PROG_RB_DIRECT_ON=True, hold20) ==
identical finals 20/20 | apply p99 (structified obs, per step) max 0.0024 s, mean 0.0014 s | errs 0

== V56 reacting bank agent (vr.py seat 0, paired vs S/vband1/res/v56_ctl_*) ==
j4_m40_w*.csv n 40 | W 0 (ctl 38) | own 82037 rival 118603 margin -36566 (ctl +7862) | dmargin -44428 t -17.51 | down -24433 t -12.89 | drival +19994 t 10.65 | flips +0 -38
   units ours/ctl: str15-17 21.5/48.5 | milk18-29 83.3/101.5 | wool18-29 55.5/101.5 | egg18-29 115.0/68.6 | errs 0
   worst dmargin: tape_akmr_113252431 -74523 (m -68514 ctl +6009), tape_liminhai_114014766 -72177 (m -52624 ctl +19553), tape_rsturley_113375513 -69515 (m -62082 ctl +7433)
j4_v21_w*.csv n 21 | W 0 (ctl 13) | own 82932 rival 121341 margin -38410 (ctl +3099) | dmargin -41508 t -16.94 | down -19895 t -14.25 | drival +21614 t 9.16 | flips +0 -13
   units ours/ctl: str15-17 21.5/50.9 | milk18-29 94.0/97.7 | wool18-29 42.2/77.4 | egg18-29 121.9/84.3 | errs 0
   worst dmargin: v_115021555 -66525 (m -56817 ctl +9708), v_115026903 -56052 (m -52635 ctl +3417), v_115002685 -52885 (m -57408 ctl -4523)

== p48c clone (rcr.py --rival p48c, boards_p48_16, both seats; ctl = PROGRAMME2R pfsp = PFS on the same tree) ==
j4p vs pfsp n 32 | W 12 (ctl 32) | own 92126 rival 95358 margin -3233 (ctl own 112978 rival 86437 margin +26541) | dmargin -29773 t -11.51 | down -20852 t -9.55 | drival +8922 t 5.67 | flips +0 -20
p48s scripted rival: /home/user/stage_r/p48rival1r/res/p48s does not exist -> not run

== first divergent step distribution (step: games) ==
tune20 start v1: market {4: 7, 9: 13} | unit {0: 20}
tune20 end j4:   market {4: 7, 9: 5, 14: 8} | unit {6: 7, 10: 13}
hold20 j4:       market {4: 2, 9: 9, 14: 9} | unit {6: 2, 10: 18}
Causes, in order of earliest divergence: step 4 = the 8 % d0 h4 melon-seed branch (MMPQ buys MELON 2 at h4; wheat price >= 30 at h4 only occurs in that branch, but it also
occurs at 27-29: not resolved); step 6/10 unit = d0 h6-h9 unit tape (92 % modal) and the controller from h10 (MMPQ unit lists 41-89 % modal at h10-h23);
step 9 = the 37 % d0 h9 branch (no seed buy; not money-determined: 216-241 vs 221-241); step 14 = d0 h14 SELL WHEAT 1 vs 2 when money <= 31 (both at 22-31).

== same 20 games as PROGRAMME2R fid20 (tune20), truth / PROGRAMME2R rb17 / PROGRAMME3R j4 ==
final ratio mean 1 / 0.804 / 0.740 | land exact 20 / 17 / 18 | d9 herd within 1 20 / 0 / 5 | final >= 90 % 20 / 2 / 1 | idle unit-turns/day d10-28 0.9 / 15.2 / 1.9
wheat units sold 592 / 342 / 261 | strawberry d15-17 50.0 / 30.6 / 25.2 | eggs d18-29 147 / 92.5 / 106.2 | waterings/day 56.6 / 49.9 / 58.2
revenue gap per game (tune20, obs-price x units, a14 build): wheat -13.5k, wool -7.2k, strawberry -5.4k, tomato -4.2k, carrot -3.3k, egg -3.0k, milk -2.1k, fert -1.6k (total -40.6k)
knob plateau: 40+ single/combined knob probes (sweeps s1-s12) all within 0.68-0.74 on tune20; the remaining gap is the unit-level labour schedule (moves 138/day vs MMPQ 122, actions 154 vs 176; wheat cycle 3.9-5 days vs 3.35).

BARS: land >= 18/20: tune 18, hold 19 PASS | d9 herd >= 16/20: 5 / 3 FAIL | idle <= 3: 1.9 / 2.5 PASS | wheat >= 500: 261 / 286 FAIL | final >= 90 % on >= 15/20: 1 / 2 FAIL
V56 m40 W >= 37 & margin >= +6k: W 0/40, -36.6k FAIL | v21 W >= 12: 0/21 FAIL | p48c margin >= 0: -3.2k (W 12/32) FAIL | apply p99 < 0.65 s: 0.0024 s PASS
VERDICT: NONE (no candidate; no package). Slips: 3 (see checkpoint.txt).
```
