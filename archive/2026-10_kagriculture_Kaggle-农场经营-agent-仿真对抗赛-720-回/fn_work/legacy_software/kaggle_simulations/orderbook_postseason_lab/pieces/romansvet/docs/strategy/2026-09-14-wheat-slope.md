# WHEAT slope on the crop-mix gene: reachable, and it loses

**VERDICT: cb[WHEAT] is a strong, ES-reachable lever (+8 d10 wheat tiles = 0.93 sd at sigma 0.02,
1.86 sd at 0.01) and moving it closes the whole −6,619 WHEAT ledger line while LOSING the game —
−11,699 (t −5.74) at z=+0.01 and −14,335 (t −6.99) at z=+0.02 vs the ymg_aq top five, −26,075
(t −13.98) vs the band clone, and the negative direction loses too (−10,632 / −44,568). 0 wins in
88 paired games over five z values: B is a local optimum here and the wheat line is not a lever.**

Scope: decode sweep + paired CRN sim only (no engine game, no training arm, no launch). Tools
(new): `S/wheat_slope/{slope.py,ledger_multi.py,report.py}`; `ledger_multi.py` is a multi-theta
copy of `S/topledger3/ledger.py`. Switch set via the runner's `--switches`
(`brain.MELON_GENE_ON=True`); B = `flow193_g100_hr.npy` padded to `policy.N_PARAMS` = 7,020;
`z` = `theta[policy.offset("cb") + spec.I_WHEAT]`.

## 1. Decode slope, 80 synthetic dawns, gene ON

80 dawns = nquad 1-4 x money {3k,8k,20k,60k} x day {0,5,10,20,29}, built as
`tests/test_melon_gene.py` builds its five (`initial_state` + `rollout.policy_obs`): *synthetic*
dawns on empty land, NOT replayed game states. Cells = mean `plant_target` W/C/T/S/M over that
day's 16 states; gene OFF decodes the z=0.00 row for every z.

| cb[WHEAT] | d0 W/C/T/S/M | d5 | d10 | d20 |
|---|---|---|---|---|
| −0.02 | 0.00/5.62/0/8.06/9.56 | 0.00/4.00/0/9.44/6.12 | 0.00/2.25/0/10.81/3.12 | 0.00/11.31/0.31/0/0 |
| −0.01 | 0.44/5.44/0/7.81/9.56 | 0.31/3.69/0/9.44/6.12 | 0.31/2.12/0/10.62/3.12 | 2.25/9.25/0.12/0/0 |
| 0.00 | 3.75/3.38/0/7.19/8.94 | 2.88/2.31/0/8.69/5.69 | 2.00/1.25/0/10.06/2.88 | 8.38/3.25/0/0/0 |
| **+0.01** | **10.75**/0.75/0/5.12/6.62 | **8.50**/0.38/0/6.62/4.06 | **6.19**/0.25/0/7.81/1.94 | **11.38**/0.25/0/0/0 |
| **+0.02** | **17.06**/0/0/2.88/3.31 | **13.62**/0/0/4.00/1.94 | **10.69**/0/0/4.69/0.81 | **11.62**/0/0/0/0 |
| +0.05 | 23.06/0/0/0.06/0.12 | 19.44/0/0/0.12/0 | 16.00/0/0/0.19/0 | 11.62/0/0/0/0 |

Monotone, both signs live, and `gene ON at z=0` decodes **identically** to `gene OFF` on all 80
dawns (asserted in `slope.py`). Tiles are conserved — d10 displacement: z=+0.01 WHEAT +4.19 /
CARROT −1.00 / STRAWBERRY −2.25 / MELON −0.94; z=+0.02 +8.69 / −1.25 / −5.38 / −2.06; z=+0.05
+14.00 / −1.25 / −9.88 / −2.88. **Tomato never moves** (masked by `can_mature`/absorb here).

**sd-at-sigma** (bisection on z, d10 mean; base WHEAT 2.00 tiles): **+1 wheat tile** needs
z* = 0.00289 = **0.29 sd @ sigma 0.01, 0.14 sd @ 0.02**; **+8 tiles** (ymg_aq's 16.3) needs
z* = 0.01862 = **1.86 sd @ 0.01, 0.93 sd @ 0.02**. STRAWBERRY (base 10.06): +1 tile z* = 0.00172
(0.17 / 0.09 sd); **+8 is unreachable** — the d10 mean saturates at 16.19 (+6.13) by z=+0.05 and
does not move up to z=0.20 (land, not log-share, binds); displacement at z=+0.02 is S +6.00,
MELON −2.88, WHEAT −1.88, CARROT −1.25.

## 2. Identity gate — PASSES within the tree, FAILS across trees (read this before §3)

The shipped ledger runners load `.claude/worktrees/arms-next/src` = the **6,789** layout, which
has no `cm`/`cb` (and no market-momentum input) and cannot carry the gene at all, so
`ledger_multi.py` loads the repo `src` (7,020). Three gates:

| gate | result |
|---|---|
| gene ON @ z=0 vs gene OFF, **same 7,020 tree**, 12 ymg_aq games | **all 14 arrays BIT-EQUAL** (`raw_YMG` z=0 vs `raw_GATEOFF`): the switch is inert in the simulator, not just in the decoder |
| 7,020 tree @ z=0 vs `S/topledger3/raw_B.npz` (6,789 worktree) | **NOT bit-equal**: pooled margin −13,751.4 vs −13,721.6 = **−29.8 coins**, 4/12 boards differ, max 770 |
| 7,020 tree @ z=0 vs `S/melon_decomp/raw_B.npz` (6,789 worktree) | **NOT bit-equal**: pooled margin −418.0 vs −107.8 = **−310.2 coins**, 28/40 boards differ, max 1,561 |

So the gate as specified (0 coins against the stored `raw_B.npz`) **fails**: zero-padding into
the 7,020 layout is decode-identical but not *rollout*-identical (float32 summation order tips an
occasional integer market threshold over 30 days). The drift is a property of the two source
trees, **not of the gene** (gate 1 is bit-equal): ±30 coins pooled on the ymg_aq set, ±310 on the
band set, against signals of −11.7k to −26.1k. Every §3/§6 number is **within-tree paired**, so
the drift cancels there.

## 3. Paired CRN sim margins

All arms: switches `OPEN_PUMP_ON,TAIL_FILL_ON,BANK_BEFORE_LOT_ON,HIRE_ROW_ON` +
`brain.MELON_GENE_ON=True`, `shop_crn=True`, pinned towns, tape opponent, CRN across z.

### (a) ymg_aq top five — the 6 retention>=0.95 boards of `S/topledger3/boards.json` x 2 seats

| z | ours | theirs | margin | Δmargin vs z=0 | t | wins | our wheat tiles d10 | d20 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 93,127 | 106,879 | −13,751 | — | — | 0/12 | 8.5 | 9.5 |
| +0.01 | 89,864 | 115,314 | −25,451 | **−11,699** (sd 7,057) | **−5.74** | 0/12 | 14.5 | 11.8 |
| +0.02 | 90,887 | 118,974 | −28,087 | **−14,335** (sd 7,100) | **−6.99** | 0/12 | **21.9** | **19.2** |

The tape opponent runs 16.2 wheat tiles at d10 and 19.4 at d20: **z=+0.02 matches ymg_aq's wheat
tile count and loses 14.3k more.**

Season net by line (ours − theirs, coins/game; Δ vs z=0 in brackets):
| line | z=0 | z=+0.01 | z=+0.02 |
|---|---:|---:|---:|
| WHEAT | −6,643 | −4,116 (**+2,527**) | **+230 (+6,872)** |
| STRAWBERRY | −3,072 | −10,524 (−7,452) | −14,958 (**−11,885**) |
| WOOL | −5,697 | −5,472 (+226) | −3,476 (+2,221) |
| MELON | −1,551 | −4,572 (−3,021) | −8,104 (−6,553) |
| CARROT | −758 | −3,296 (−2,538) | −4,399 (−3,641) |

Our units sold (z 0 → +0.01 → +0.02): WHEAT 314.7/395.1/499.5, STRAWBERRY 205.2/194.0/151.2,
CARROT 91.8/35.2/15.8, MELON 90.0/74.2/57.9, WOOL flat 121.7/126.4.

**The −6,619 WHEAT line is real and the gene closes all of it (+6,872, to +230)** — paid for by
−11,885 strawberry, −6,553 melon, −3,641 carrot: tiles are conserved and the crops given up sell
into scarcity at 105-167/unit while wheat clears at 34-37. Two thirds of the loss is *their* gain
(106,879 → 118,974): 185 extra wheat units do not move their price (their 1,145-unit buy leg
absorbs them) while vacating the strawberry/melon rows hands them the prices
`2026-09-14-melon-decomposition.md` priced.

### (b) Band clone — 20 TOPB2 + 20 LIVE-C rows of `S/melon_decomp/boards.json` (40 games)

Subset, not all 68 (the time box allowed 80 rollout rows): rows 0:20 and 40:60 of the stored
list, so both clone families are covered. Pairing is within-board, so the subset costs only
power. UNVERIFIED for the 28 unrun rows.

| z | ours | theirs | margin | Δmargin vs z=0 | t | wins | our wheat tiles d10 | d20 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 102,253 | 102,671 | −418 | — | — | 0/40 | 8.9 | 8.0 |
| +0.02 | 94,762 | 121,256 | −26,493 | **−26,075** (sd 11,793) | **−13.98** | 0/40 | 12.4 | 21.2 |

| line | z=0 | z=+0.02 |
|---|---:|---:|
| WHEAT | −1,339 | +7,141 (**+8,481**) |
| STRAWBERRY | +6,460 | −10,517 (**−16,978**) |
| WOOL | −1,798 | −3,770 (−1,973) |
| MELON | −3,890 | −7,211 (−3,321) |
| CARROT | +975 | −2,899 (−3,874) |

Same mechanism, twice as expensive: strawberry is our largest surplus against the clone (+6,460),
so converting it to wheat destroys 16,978 of it and hands the clone +18,585 end coins. **0/40.**

## 4. Prior art: the W00/W01 crop_mix ES arms already sampled this direction

`S/unitorder/crop_mix{,_w01}_campaign_20260914/config_C_seed31{3,4}.json`: `train_only = cm,cb`,
**sigma 0.5**, lr 3.6, pop 4096, gens 10, `tape_score = margin`, `pinned_fixed_seed`, opponents =
`S/rotband/artifacts/tape_actions_town/1081xxxxx.npz` — **band-clone town tapes only, no top-five
tape in either arm**. Both REJECTED on all seven families
(`docs/strategy/2026-09-12-HANDOFF-RESTART.md:54-57`).

UNVERIFIED (arithmetic from `2026-09-14-melon-reachability.md` §3, not re-measured): at sigma 0.5
with the gene OFF `cm,cb` moves a crop log-share 0.5 x 2.885 = 1.44 nats per aligned sd, so our
gained z=+0.01 (2.56 nats) is ~1.8 sd — ~4 % of a 4,096 population (~150 candidates), consistent
with the 302-316/4096 melon crossings quoted there.
**So W00/W01 did sample the +4-tile wheat shift, on band tapes, and their fitness rejected it** —
which §3(b) now explains quantitatively (−26,075 at z=+0.02).

## 5. Can an ES arm at sigma 0.01-0.02 reach it, and would fitness see it?

Yes on reach, no on value. With `MELON_GENE_ON` and the 7,020 centre, one aligned sd at sigma
0.02 (0.93 sd) buys the full +8 d10 wheat tiles that close the gap to ymg_aq and +1 tile costs
0.14-0.29 sd, so unlike melon (71-168 sd OFF) wheat is *not* gated by decoder gain: the
population would straddle 0-16 wheat tiles at both training sigmas and the integer decision would
get real fitness variation. The problem is the sign. Every tape set we can score against prices
this direction negative: the band-clone tapes (rotband / TOPB2 / LIVE-C) pay −26,075 at z=+0.02
and were the fitness that already rejected W00/W01; the six pinned ymg_aq tapes — the only ones
where the WHEAT line is −6,619 and the only set whose fitness could *see* the top-five wheat
deficit — pay −11,699 / −14,335. No tape set in the repo scores a wheat-up crop mix positive, and
on the ymg_aq boards we reach their exact tile count (21.9/19.2 vs 16.2/19.4) and lose more. So
the −6,619 line is **not a missing action we fail to express**: it is the accounting shadow of
their larger cleared land and labour base, and imitating the tile count without the base converts
our scarce-price rows (strawberry 105/u, melon 167/u) into a 34-37/unit commodity sold into their
own 1,145-unit buy leg. An ES arm on `cb[WHEAT]` at sigma 0.01-0.02 would learn the opposite
sign — and §6 shows that sign loses faster still.

## 6. The negative direction (the "sell less wheat" hypothesis) loses faster

Wheat is our worst channel (34-37/unit), so the obvious reading of §3 is "give wheat up".
Same 12 ymg_aq games, CRN, gene ON:

| z | ours | theirs | margin | Δmargin vs z=0 | t | wins | our wheat tiles d10 | d20 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| −0.01 | 86,375 | 110,759 | −24,384 | **−10,632** (sd 2,937) | **−12.54** | 0/12 | 5.0 | 4.6 |
| −0.02 | 72,720 | 131,039 | −58,319 | **−44,568** (sd 13,022) | **−11.86** | 0/12 | 0.8 | 0.5 |

Season net by line, Δ vs z=0: at z=−0.01 WHEAT **−6,063** (to −12,706), MELON +1,737, CARROT
+1,167, STRAWBERRY +922, WOOL −164; at z=−0.02 WHEAT −13,028, STRAWBERRY −7,454, WOOL −6,820,
MELON +1,283, CARROT +1,596. Our wheat units fall 314.7 → 197.0 → 110.7 while strawberry units
barely move (205 → 234 → 247): the freed tiles cannot be re-sold because the strawberry/melon
rows are already at their absorption limits (the same ceiling §1 found in the decode —
strawberry saturates at +6.1 tiles). Wheat is not a leak to plug; it is the **overflow channel**
that monetises tiles the priced rows cannot absorb.

**Shape over the five z values (ymg_aq):** −44,568 / −10,632 / **0** / −11,699 / −14,335 — a
strict local optimum in this decoded coordinate, both signs, on the opponent class whose ledger
line motivated the question (the §76 pattern of `2026-09-03-dominant-strategy.md`, one gene
deeper).

## 7. Files

`S/wheat_slope/{slope.py,ledger_multi.py,report.py}`; rollouts `raw_YMG.npz` (12 boards x z
0/+0.01/+0.02), `raw_YMGNEG.npz` (−0.01/−0.02), `raw_BAND.npz` (40 boards x 0/+0.02),
`raw_GATEOFF.npz`; `boards_*.json`, `*.log`. 432+190+450+193 s CPU. `S/topledger3/ledger.py`
and `S/melon_decomp/ledger.py` unmodified; nothing under `src/` or `scripts/` touched.
