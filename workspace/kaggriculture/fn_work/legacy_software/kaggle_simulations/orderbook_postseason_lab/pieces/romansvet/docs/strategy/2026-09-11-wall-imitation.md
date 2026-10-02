# 2026-09-11 — Macro-level imitation of the wall (joint, not piecewise)

**The reframe under test.** Every *single* piece of the top tier's program that was forced
through our planner lost (FORWARD_ADMIT ×3, RAMP11, MELON_OPEN / 2-16 melon floor,
JOINT_PLATE). The hypothesis: they lost because they were *pieces* — a melon plate with our
crew curve, or their crew with our basket — and the wall only pays as a whole. Today's tie
census gave the tool to test it: the theta→plan interface is 42 integers (`P.Macro`), and
`KAGG3_PIN_INTS` can SET the 12 coarse ones per observation. So: impose the **whole** wall
opening on candidate B and measure.

**Answer: the planner reproduces the wall's opening to the tile, and it is a −24.2 k trade on
TOPB2 and −31.4 k on LIVE-C. The joint configuration is not what the single-piece forcings were
missing — it is worse than the melon piece alone.**

Tools: `S/wall/` (this run), `/root/wt_wall` = private copy of the `arms-next` worktree with
`S/ties/brain.patch` applied and extended. Nothing under `src/` in main or `arms-next` touched.

## 0. The tool: literal-integer pins

`S/ties/brain.patch` pins the coarse `Macro` fields at what a **reference theta** decodes. No
theta of ours decodes 12 melon at d0, so the reference form cannot express the wall. The patch
was extended in the private copy (`/root/wt_wall/src/kagg3/core/brain.py`, `_pin_vals` /
`PIN_KEEP`): the same env var also accepts an npz of **literal per-day tables** keyed by `Macro`
field name, first axis = day, sentinel `-999` = "leave the planner's own integer". Unset it is
the identity (`decide` = `_decide`), exactly as the census patch is.

## 1. The wall's ledger, d0-d12 (TOPB2, 4 tapes, both seats, `S/topledger/wall_B8.npz`)

Three of the first four TOPB2 tapes (107448662 / 107450553 / 107454465) are the **same program,
tile for tile**; 107457053 is a different (18 WHEAT + 1 MELON) file. Canonical tape 107448662,
tiles [W,C,T,S,M] and animals [G,C,S] per day, hires from the tape's `mop` MO_HIRE row:

    day    0    1    2    3    4    5    6    7    8    9   10   11   12
    WHEAT  7    7    7    7    7    3    5    9    5    5   12   20   24
    STRAW  0    0    0    0    0    4   12   16   20   20   20   33   33
    MELON 12   12   12   12   12   12   12   12   12   12    0    0    0     <- the pot at d10
    COW    2    2    3    4    4    4    6    8    8    8    8    8    8
    SHEEP  2    2    2    2    2    2    2    2    4    5    6    6    6
    GOOSE  0    0    0    0    0    0    0    0    0    0    2    3    3
    hires  5    3    4    5    4    4    7    7    8    8   11   10    9     (21 by d4)

Candidate B on the same boards (`S/wall/table.py`): d0 **11 WHEAT + 8 CARROT, 0 MELON**,
4 COW + 1 SHEEP + 1 GOOSE; first melon tile d4, 4.5 at d10, 9.5 at d12; cash at d10 3,401 vs
their 13,777. B's own day-0 `Macro` decodes `plant_target [11,11,0,0,0]`, `animal_want [1,4,1]`,
**`crew_target` 0 on d0-d5** (hands come from `hire_bias`/the enumeration, not the ramp gene).

*Ledger caveat:* the `hands` column is `State.nhands` read after eod, which is 0 for both seats
every day (hands reset nightly) — crew is measured from the tape and from the pinned ask, not
from that column.

## 2. The map: which coarse field carries which wall observable

| wall observable | coarse `Macro` field | pinned? |
|---|---|---|
| tiles planted per crop, per day | `plant_target` int[5] | yes |
| animals acquired per kind, per day | `animal_want` int[3] | yes |
| hands hired today | `crew_target` int (0..`spec.MAX_HANDS`=16) | yes |
| plant *timing* | the day axis of the tables | yes |
| quadrant purchase (d6, d11) | `land_bias` int — **signed coins**, not a count | no |
| route tightness | `compact` int 0..`DIST_MAX` | no |
| hire-scan horizon | `forward_days` int | no |

`land_bias`, `compact`, `forward_days` have **no wall observable**: they are our planner's own
internal prices/horizons, not anything a tape emits. They stay at B's values (documented gap;
land purchase lands d5/d10 for us against their d6/d11, ≈1 day early, not a channel).

`S/wall/mk_pin.py` writes `pin_wall.npz` (joint), `pin_wall_lab.npz` (crew only),
`pin_wall_plant.npz` (plant only) and `pin_wall_v2.npz` (joint + the full d0-d12 plate).

## 3. Imposition: does our planner execute the wall's opening?

**Yes — the opening reproduces.** `S/wall/wall_joint8.npz`, our seat, mean of 8 boards:

    day        0    1    2    3    4    5    6    7    8    9   10   11   12
    WHEAT    7.0  7.8  7.8  7.8  4.8  4.2  5.0  5.5  3.8  6.8 12.8 23.2 24.5
    MELON   12.0 12.0 12.0 12.0 12.0 12.0 12.0 12.0 12.0 12.0  0.0  2.8  3.8
    CARROT   0.0                                             0.2  0.8  1.0
    tiles   19.0 19.8 19.8 20.0 20.0 20.0 25.8 28.5 38.5 42.5 38.2 53.8 58.2
    shed M                                                  72.0

d0 is the wall's basket exactly (7 WHEAT + 12 MELON, 19 tiles, no carrot); the 12-tile plate is
held to d9 and **all 72 melon units are cut on d10**, the same 72 the clone cuts. The claim
"`plant_target` melon 0/16,800 decisions" was about the incumbent theta; the executor has no
trouble with the plate.

### The three residuals, with numbers (canonical 3 tapes, 6 boards)

1. **Deposit turn — the melon banks a day late.** 72 units are in the *shed* at d10 eod and
   clear on **d11 at avg 153.2/unit** against the clone's same-day **198.4**; ≈ **3.3 k** on the
   pot alone. This is exactly `2026-09-10-melon-route-capacity.md` §3: a harvest lands in the
   unit and only an excursion banks it. (That doc's fix, `MIDDAY_PLACE_V2_ON`, is measured in §4.)
2. **The animal line is refused, and the pin makes it worse.** The pin *asks* for the wall's
   acquisitions (COW +1 d2, +1 d3, +2 d6, +2 d7 → 8 by d7). We stand at **2.7 cows at d7 and
   3.0 at d12** — against B's own unpinned **4.7 / 6.3** and the wall's **8 / 8**. The 12-tile
   plate drains the purse (d6 cash 451) and `budget.grant` refuses the animal candidates, so
   asking for the wall's animals *delivers fewer animals than not asking*. At d20: COW 6.3 → 3.0,
   SHEEP 5.0 → 3.0.
3. **Idle tiles.** Melon emits no task for six days: idle tiles d5-d9 **9.6** against B's 3.1 and
   the wall's 1.6 — the crew the pin hires has nothing to load.

### Iterations (three, as budgeted)

* **v1 `pin_wall.npz`** — d0 basket + `melon = 0` on d1-d9 (so our own late melon does not double
  the plate) + the wall's animal acquisitions d0-d11 + its hires d0-d12.
* **v2 `pin_wall_v2.npz`** — v1 plus the wall's **full d0-d12 plate** (the strawberry ramp
  d5-d9, the d10-d12 wheat/straw ramp). Idle d5-d9 got *worse* (13.0), not better.
* **v3** — v1 plus `MIDDAY_PLACE_ON,MIDDAY_PLACE_V2_ON`, the route fix
  `2026-09-10-melon-route-capacity.md` §4 names for the deposit turn. On these boards under B it
  does **not** bank the pot on d10 (shed still holds 72 at d10 eod); it buys +2.0 k of d11 cash
  and loses more overall.

The residual after three iterations is unchanged in direction: **the pot banks on d11 at ~153
against their 198, the animal line stands at 3 cows against their 8, and 9.6 tiles are idle
d5-d9.** None of the three is a decode gap — `Macro` carries the right integers; they are
execution gaps (`budget.grant` refusing, `sim/units.py:97` `OP_DROP`/eod banking the harvest).

## 4. Engine-exact screen, paired vs B

`S/wall/screen_pin.py` (= `S/simscreen/screen.py` with the worktree taken from `KAGG3_TREE`),
theta `flow193_g100_hr` in every row, shipped `hr` switches, identical frozen boards. The
board lists hold each (tape, seed) twice, once per seat, and a pinned-town open-loop tape makes
the seats near-degenerate (14 of 20 TOPB2 pairs carry the identical margin), so the **honest unit
is the game**: the two seat rows are averaged before the paired t (`S/wall/pair.py`).

**TOPB2 — 40 boards = 20 games** (B's board-level win here is 32.5 %, the documented figure;
30.0 % on the game unit).

| arm | win % | margin | Δmargin | sd | t | Δours | Δtheirs | flips |
|---|---|---|---|---|---|---|---|---|
| B (ref) | 30.0 | −1,472 | — | — | — | — | — | — |
| **+ wall JOINT (v1)** | **5.0** | −25,681 | **−24,209** | 12,382 | **−8.74** | −4,717 | **+19,492** | 0 / −5 |
| + planting only | 5.0 | −22,685 | −21,214 | 9,840 | −9.64 | −3,020 | +18,194 | 0 / −5 |
| + labour only | 25.0 | −2,051 | **−580** | 1,591 | −1.63 | −641 | −61 | 0 / −1 |
| + v2 full plate | 5.0 | −29,159 | −27,687 | 12,432 | −9.96 | −4,791 | +22,897 | 0 / −5 |
| + v3 MIDDAY_PLACE_V2 | 5.0 | −32,138 | −30,667 | 9,278 | −14.78 | −9,236 | +21,431 | 0 / −5 |

**LIVE-C — 120 boards = 60 games.**

| arm | win % | margin | Δmargin | sd | t | Δours | Δtheirs | flips |
|---|---|---|---|---|---|---|---|---|
| B (ref) | 71.7 | +5,279 | — | — | — | — | — | — |
| + wall JOINT | **1.7** | −26,138 | **−31,417** | 9,717 | **−25.04** | −10,285 | **+21,131** | 0 / −42 |

**The joint arm is worse than the planting piece alone by 3.0 k.** Adding the wall's crew and
animal schedule to the melon corner does not rescue it — it costs another 3 k, because the pin
asks for animals the drained purse then refuses (§3.2). The labour piece on its own is free to
within noise (−580, t −1.63) — consistent with `2026-09-11-labour-compounding.md`: labour does
not compound, and the wall's crew curve is not its edge.

## 5. Where the coins actually go — the band ledger (canonical 3 tapes, 6 boards)

End-of-band gap, **theirs − ours** (positive = we are behind), B vs B+wall-JOINT:

| band | B | + wall JOINT | Δ(gap) |
|---|---|---|---|
| d0-4 | −659 | +290 | +949 |
| d5-9 | −3,340 | −309 | +3,031 |
| **d10-14** | **+18,745** | **+16,940** | **−1,805** |
| d15-19 | +12,025 | +23,398 | +11,373 |
| d20-29 | −1,882 | +31,331 | **+33,213** |

At d12 the wall opening is genuinely **ahead on our own purse** (11,816 vs 8,375 coins) — the
d10-14 hole the campaign has been chasing since `2026-09-10-residual-loss20.md` **does close**,
by 1,805 coins — and the season is then lost by 44.6 k over d15-29. Two thirds of that is **their
purse, not ours**: theirs at d29 90,461 → 111,837 (+21.4 k), ours 92,343 → 80,507 (−11.8 k);
our season units fall 1,446 → 1,251, cows at d20 6.3 → 3.0, sheep 5.0 → 3.0.

**That is the finding.** Our 11 WHEAT + 8 CARROT opening is a *denial* asset — it suppresses the
clone's prices for the whole season. The wall's melon plate is not: it is a one-day cash spike
that hands the clone its own market back and starves our animal line. `MELON_OPEN −19,557`
(2026-09-09), `MELON_D10 −31 k price gift by d27` (2026-09-04) and `JOINT_PLATE −41.9 k` were
never "the piece without its partners" — this is the whole program, executed to the tile, and it
loses by the same mechanism and the same order of magnitude.

## 6. Verdict

* **(a) Does the joint wall configuration reproduce the wall's opening? YES.** 7 WHEAT + 12
  MELON at d0, plate held to d9, 72 units cut on d10 — the planner executes it once the coarse
  integers are set. The planner is **not** the wall for the opening. What it cannot do (all
  execution, not decode): bank the pot the same day (d11 at 153 vs 198, ≈3.3 k —
  `sim/units.py:97` `OP_DROP` + `eod` end-of-day banking, and the route order at
  `plan.py:817-880`); buy the wall's animals out of a plate-drained purse
  (`core/budget.py:146` `grant` refusing `plan.py:5521`'s `b_want`; 2.7 cows at d7 against B's
  own 4.7 — *asking* for them delivers fewer than not asking); keep the crew loaded while 12
  melon tiles emit no task for six days (idle 9.6 vs 1.6).
* **(b) Does it beat B on TOPB2? NO — decisively.** −24,209 coins, t −8.74, 30.0 % → 5.0 %,
  five losses flipped and none won. No engine legs are warranted; none were run.
* **(c) Does it hold LIVE-C? NO.** −31,417, t −25.04, 71.7 % → 1.7 %, 42 flips.

**Consequence for the campaign.** The standing diagnosis — "move d10-14 income, nothing else"
(`2026-09-10-residual-loss20.md` §5) — is **falsified as a target**. The band closes and the game
is lost by 44.6 k afterwards, two thirds of it in the opponent's purse. Imitation of the wall at
the Macro level is closed: piecewise (six prior forcings) and jointly (five arms today), on the
same boards, with the same sign. The top-tier edge that remains unexplained is **not** the
opening — it is the d15-29 channels the planner-ceiling review already isolated (sell-lot
granularity, `ops.py:126 SELL_TURNS`, verdict (c)), and our own opening should be defended as a
denial asset rather than traded away.

**Reusable tool.** `KAGG3_PIN_INTS` now accepts literal per-day `Macro` tables
(`/root/wt_wall/src/kagg3/core/brain.py`, `S/wall/mk_pin.py`). Any future "what if our planner
did X" question about tiles / animals / hands / timing is now a 12-minute screen, not an arm.
