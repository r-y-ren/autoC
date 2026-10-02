# MELONGENES1 — the opening melon plate made PROGRAMMABLE, and raced
2026-09-19 07:33–09:02Z, branch `melongenes` off `d35fcfb9`. Falsifier **before** any trainer.
`plan.MELON_PLATE_TILES` / `MELON_PLATE_DAY`, `tests/test_melon_plate.py`, `S/melongenes/`.
## 0. VERDICT — do NOT build the trainer. No cell, in any class, raises win rate above base.
vs the **exact V48 clone** the plate takes board wins **89.3 % → 7.1 %**, margin **+6,762 → −22,936**
(Δ −29,697, t −16.6, flips +0/−23), monotone in tiles, **theirs up in every cell**. It WINS the race it
was built to win (first melon d20 → d11, 72 u into d10-18 at 165.6) and loses anyway; the day axis has
one live value. MELONENG's −16,224 was no band artefact — it reproduces on the band we now play against
a **reactive** seat. **Family CLOSED; both floats stay 0.0 and free, layout untouched.**
## 1. The switch — the plate WITHOUT the package (`_melon_plate`)
`MELON_OPEN_ON` is the plate as a *package*: 12 tiles on d0 **plus** a dump-day excursion, a
`MIDDAY_PLACE` wall and `plan.py:3791`'s assert forbidding `BANK_BEFORE_LOT_ON` — which the shipped ESR
string carries, so MELONENG could only read it against FT2 *minus* that switch. The floats are the
plate's **size and date alone**: one `plant_target` rewrite on one day in `_melon_open`'s own
`_MELON_PAY_RANK` (wheat last, sum preserved, melon only raised), the crop sold by the ordinary lot
allocator since our dawn melon shed already *equals* that day's melon sells 60/60 [MELONDUMP §3]. So it
composes with the shipped package and a trainer could move it as two genes. Flown like `brain.HERD_TILT`.
## 2. Byte-identity at 0 — both levels (11 tests green)
`melon_plate_on()` is a Python `if` read at TRACE time. **Plan**: six-array digests on the first two
`test_route_early` seeded boards pinned to the **pre-switch master `d35fcfb9`** at shipped defaults —
`8feb802135bbe2e2`, `a570427be251bf1e`. **Engine** (`coin_pin.sh`): 2 HIBAND boards × 2 seats × 2
purses, ESR with and without the floats named at 0 — **COIN-EXACT, 4 rows**.
## 3. vs the exact V48 clone — HIBAND towns, CRN, no shop lottery
V48's `main.py` is the notebook's `SOURCE_BYTES` [V48LEG], symlinked per-id under
`artifacts/panel_v48_hiband/` so `town_inject` still pins each board's town: exact and **reactive**.
Base ran all 56 towns (**82.1 % / +5,494 se 910**; real tapes read 73.2 % / +3,300 [HIBAND]); arms ran
the **first 28 ids in the same order**, so `seed(i)=SB+1000003·i` is the base's own seed. Board = seats
averaged; right half = the melon line (`census.py`, 2 boards, seat 0).

| cell | win % | margin | theirs | Δ (t) | flips | our u/px | d10-18 u/px | 1st d | **their u/px** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **BASE** | **89.3** | **+6,762** | 101,271 | — | — | 99 / 159.8 | 0 / — | d20 | 66 / 244.5 |
| t4 d0 | 14.3 | −8,690 | 111,083 | −15,451 (−11.35) | +1/−22 | 129 / 126.0 | 24 / 206.7 | **d11** | 66 / 244.5 |
| t8 d0 | 7.1 | −15,121 | 117,361 | −21,882 (−12.58) | +0/−23 | 140 / 112.0 | 48 / 188.1 | **d11** | 66 / 244.5 |
| t12 d0 | 7.1 | −22,936 | 121,569 | **−29,697** (−16.60) | +0/−23 | 160 / 94.6 | 72 / 165.6 | **d11** | 66 / 244.5 |
| t4/t8/t12 **d2** | 89.3 | +6,762 | 101,271 | **0** (0.00) | +0/−0 | 99 / 159.8 | 0 / — | d20 | 66 / 244.5 |

**`MELON_PLATE_DAY=2` is a structural NO-OP**: on `110504774` the planner's `plant_target` sums to
**d0 22, d1 0, d2 0, d3 7, d4 11, d5 20**, so `min(TILES, plant_total)` is zero after the opening day (a
date trainer needs d3+). **The race is won and still lost**: the rival's melon line never moves — 66 u
at 244.5 in all seven cells — so there is no denial to collect (their melon is sold by d11 on this band
[MELONDUMP]); our own melon price falls 159.8 → 94.6 down a squared curve that never refills; and their
purse rises **+9,812 / +16,090 / +20,298 on the NON-MELON crops our tiles stopped growing**. MELONGIFT
against a reactive seat, with the channel finally named.
## 4. vs ENGINE tapes (4 ENGINE-OTHER HIBAND + ENGINE28 = one CRN leg of 32)
ENG32 base **28.1 % / −480**; t4 d0 **−7,273** (t −1.98) at 15.6 %, t8 d0 **−7,863** (−2.21) at 25.0 %,
t12 d0 **−12,749** (−3.30) at 15.6 %, all d2 cells exactly 0. ENGINE28 alone: +1,441 at 32.1 % → −7,237
/ −7,071 / −12,764 (−2.99), win 32.1 → 17.9 / 28.6 / 17.9 %. The 4 ENGINE-OTHER HIBAND tapes sit at 0 %
win already, −13,927 → −7,522 / −13,406 (−2.35) / −12,646. Same sign and shape as MELONENG, theirs up
every cell (105,852 → 111,610 / 117,171 / 120,412). **Best cell per class: tiles = 0, i.e. today.**
**LESSON — a tape cannot react.** That same t12 d0 cell reads **+10,448** on `110504774` against the
TAPE seat, their melon price cut 201 → 94: a recording cannot re-price or re-time when you flood the
book ahead of it, so the flood *looks* like denial. Seat the live clone and it is a gift. Race the
opponent that reacts before building the thing that learns.
Repro `bash S/melongenes/run_grid.sh v48h|eng32`, `run_census.sh`, `coin_pin.sh`; readers `report.py
<class> [ids]`, `census.py`; `raw/md_*.json` gitignored.
