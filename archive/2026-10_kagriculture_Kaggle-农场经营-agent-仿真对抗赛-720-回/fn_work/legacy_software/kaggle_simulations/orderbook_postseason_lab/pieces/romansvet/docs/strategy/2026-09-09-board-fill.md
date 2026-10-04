# 2026-09-09 — which constraint leaves our tiles empty (board fill)

Worktree `board-fill` at `bdec0e9`. Judge: 3 pinned held-out boards
(episodes 106401414, 106773901, 106793159), our seat, theta
`flow135_g350_gpfwdfv_gb028`, town pinned from each tape's `_TOWN`
(`scratch/town3.json`, `scripts/town_inject.py`).

## 0. The brief's premise is inverted, and the real claim is narrower

The task was framed as "47 planted tiles for us against their 59 from day 10
on". That is not what the held-out ledger says. From
`docs/strategy/2026-09-09-reviews/heldout_boards.csv` (42 pinned boards, both
seats, live theta), day 10 hour 23:

| | ours | theirs |
|---|---|---|
| planted tiles | 44.5 | 33.1 |
| occupied tiles (plants + structures + animals) | 60.1 | 50.2 |
| quadrants | 2.9–3.0 | 2.0–2.1 |

**We out-plant them on 40 of 42 boards** (exceptions 106438084: 48 vs 68;
106802486: 39 vs 55.5). On the three probe boards we lead on all three
(106773901 38 v 32, 106793159 50 v 28.5, 106401414 50 v 32).

The claim that *is* in the record is different and comes from the 88-live-loss
ledger (`docs/strategy/2026-09-05-build-story.md:792`): "board fill (+3.5k;
**we leave 9 unlocked tiles empty from day 10 on, they leave 0.6**)". The gap
is not tiles planted, it is **idle tiles on land we already bought**: we own a
third quadrant they do not, and we do not fill it. So the question is
"why are ~9 of our own unlocked tiles empty every day", not "why do we plant
fewer tiles".

## Status

- [x] premise corrected against the held-out CSV
- [ ] Q1 per-day attribution (probe running)
- [ ] Q2 opponent's extra tiles / per-tile-day earnings
- [ ] Q3 cap vs budget
- [ ] Q4 lever

## 1. Per-day attribution: the plan-side cap is the whole story

Method: `plan.FILL_TRACE` (a `None`-by-default diagnostic sink added at
`src/kagg3/core/plan.py:139`, written at `:5741` inside `_derive` and completed
at `:6914` in `_plan_and_stats`) records, for the shipping pass-B `_derive` of
every day: `free_slot`, `n_build`, `plant_here`, `macro.plant_target`,
`plant_eff`, `view.seeds`, `seed_buy`, the seed lists' `wants`, `seed_cap`, and
the final `admitted & covered` masks. `scratch/fillprobe.py` runs one real
engine game per board, our seat, town pinned. Coins reproduce the held-out CSV
exactly (106401414 86,959/67,578; 106773901 101,483/132,057; 106793159
147,925/154,091), so this is the live game, not a surrogate.

Decomposition of an idle tile-day (`free_slot & ~built & ~planted`):

- **cap** — `sum(macro.plant_target) < free tiles after builds`; the brain's
  `n_dev = floor(dev_frac * n_free)`, `plant_total = n_dev - animals`
  (`brain.py:921-947`) simply did not ask for the tile.
- **tilecap** — `want_raw - w_seed`, the `seed_cap` clip in `_wants`
  (`plan.py:4707-4723`): today's builds took the tile first.
- **budget** — `w_seed - seed_buy`, the coins `budget.grant` refused.
- **route** — a tile in `plant_here` whose PLANT the admit loop dropped
  (`plant_here & ~(admitted & covered)`).

Day 10–29 totals, our seat:

| board | idle tile-days | cap | seed_cap clip | budget refused | route-dropped PLANTs |
|---|---|---|---|---|---|
| 106401414 | 250 | **250** | 0 | 0 | 0 |
| 106773901 | 201 | **197** | 0 | 4 | 0 |
| 106793159 | 196 | **196** | 0 | 0 | 2 |

Answers to Q1's five buckets, d10–29, pooled over the three boards
(647 idle tile-days): (a) no seed in shed **0**, (b) seed purchase not
admitted **4 = 0.6 %** (all cash, none the tile cap), (c) no unit-turn
**2 = 0.3 %**, (d) tile held by the plan cap **643 = 99.4 %**, (e) other **0**.

Labour is not close to binding either: over d10–29 the admit loop drops
9 of 1,173 queued tiles on 106401414 (0.8 %), 4 of 1,105 on 106773901 (0.4 %)
and 35 of 1,222 on 106793159 (2.9 %) — and only 2 of those are PLANTs.

The cap is **proportional**, which is why it never converges: `dev_frac` is a
sigmoid, so `plant_target` is a fixed *fraction* of the free tiles and the
absolute idle count grows with the board. On 106401414 the shape is
`free 29 → plant 10` on day 24 and `free 31 → plant 10` on day 27.

## 2. What the opponent puts on the extra tiles, and what it is worth

The three tapes are one clone (near-identical action streams). Their PLANT
census, read straight off `artifacts/tape_actions_town/<ep>.npz`:

| | 106401414 | 106773901 | 106793159 |
|---|---|---|---|
| their season plantings | 240 | 240 | 236 |
| **our** season plantings (traced) | 194 | 162 | 167 |

Their shape is a **wheat turnover machine**: 7 WHEAT a day, every day, from
d12 to d24, plus one day-0 melon block (7 wheat + 12 melon), a strawberry
push d5–d11, and a carrot tail d23–27. They hold *fewer* tiles than we do
(33 planted at d10 vs our 44.5) and recycle them 1.4× as often. So the
"extra tiles" are not extra land — they are extra *plantings* on the same
small board.

Value per tile-day: our own realised wheat is 2.87 units a planting at 41
coins over a 3.1–3.9 day life = **25–30 coins a tile-day gross**, ~330 coins
of seed a game (`plan.py:4212-4232`, measured over 32 McGrain replays). The
ledger's 9 idle unlocked tiles × 20 days = 180 tile-days × 25–30 = 4.5–5.4k
gross, ~3.5–4.5k net of seed. **The +3.5k figure is the right order of
magnitude** — but it is a gross land figure that prices zero labour, and the
labour is the thing that is scarce (see §3).

## 3. Which binds — and the dry run

The cap binds, alone (§1: 99.1 % of idle tile-days). The seed budget refuses
4 tile-days in 451; the seed_cap/build clip refuses 0; the route refuses 0.

Dry run = the same three engine games with `PLANT_FILL_ON = True` (v2, the
reserve-priced wheat fill), our seat, same pinned towns:

| board | plantings OFF→ON | idle tile-days d10–29 OFF→ON | PLANTs the route dropped d10–29 OFF→ON | our coins OFF→ON | margin OFF→ON |
|---|---|---|---|---|---|
| 106401414 | 194 → **252** | 250 → **71** | 0 → 3 | 86,959 → 80,096 | +19,381 → +10,507 |
| 106773901 | 162 → **241** | 201 → **97** | 0 → 28 | 101,483 → 95,607 | −30,574 → −15,915 |
| 106793159 | 167 → **223** | 196 → **99** | 0 → 45 | 147,925 → 142,367 | −6,166 → −14,856 |

So **yes, lifting the cap changes the plan and closes the fill gap** — it puts
us at or past the opponent's 236–240 plantings and cuts idle tile-days by
50–72 %. And it costs **5.6–6.9k of our own purse on every board**, with 0
outcome flips. Queued tasks the route cannot reach go 9 → 50, 4 → 87 and
35 → 79 over d10–29: the labour that was slack at the shipped tile count is
the binding constraint at the opponent's.

## 4. The lever: `PLANT_FILL_LATE_ON`

Built, shipping OFF, `src/kagg3/core/plan.py:4318-4353` (doc) and `:5428-5453`
(6 lines of code); test `tests/test_plant_fill_late.py` (7 tests, all pass,
OFF pinned on `test_route_early`'s `a838700` digests).

Claim: v2's whole loss is priced in the herd (WOOL 152→136, FERTILIZER
191→144, EGG 50.6→20.9, COW 7.6→7.1) and the only days that damage can be
done are the days the herd is still being acquired, because the channel is
`n_free` → `n_dev` → `animal_count` (brain.py:915-924). The trace says the
fill has nothing to protect after day 12: `macro.animal_want` is `[0,0,0]` on
15 of 18 days from d12 on 106401414 and all 17 from d13 on 106773901;
`n_build` is 0 on every day after 12 on both; `_fill_cap`'s reserve is already
0 there. **v2 was spending its herd bill on the ramp** (day 5: 15 tiles planned
against a fill cap of 22). ON, the fill is refused before
`PLANT_FILL_FROM_DAY = 12` and is the v2 fill after it.

Why it does not buy PASS turns the way the crew-ramp levers did: the extra
work enters as PLANT/WATER *tasks*, which the admit stage prices and cuts
(`n_admit`, `plan.py:6446`) — it can drop the fill, it cannot idle a unit for
it. The PASS the crew ramp bought was bought by hiring a hand with no route.

NOT VERIFIED: the switch has had no paired engine run. Its own dry-run
prior is that the late half of v2 is where the +5.6–6.9k loss is *not*
(route drops d20–29 are where the ON legs lose their tasks), so it may still
lose. The test pins mechanics only.

Targeted tests run: `tests/test_route_early.py tests/test_plant_fill_late.py
tests/test_day_stats.py` — 28 passed, exit 0, both switches OFF.

Commit `cd8a040` on worktree `board-fill`.
