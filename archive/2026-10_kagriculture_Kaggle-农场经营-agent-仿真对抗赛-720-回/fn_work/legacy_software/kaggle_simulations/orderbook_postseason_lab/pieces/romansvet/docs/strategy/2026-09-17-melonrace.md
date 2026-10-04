# MELONRACE — can we out-run the top 10 to the day-10 melon pot?

2026-09-17 08:58–09:15Z. Arithmetic box, **no src change, no engine leg** (step 2 says no at every plate size, so step
4 was not entered). Worktree `kaggriculture3-melonrace` (branch `melonrace`, off `70b98ff`).
`S/melonrace/{sched.py,pot.py}` + banked `sched_*.txt`, `pot.txt`.

## 0. VERDICT — no. The race is winnable and it is not worth the land.
`spec.CROP_SATURATE_AGE[I_MELON] == 10` (`min(12, max(10, 6+6−2))`), so MELONENG's plate **already harvested at age
10** — there is no two-day shift left to buy. What it did lose is the *row order*: its measured day-10 quote is
**195.6/u against their 224.2/u**, i.e. the plate sold BEHIND them. Winning that row is worth at most **+5,026 pair
coins at 12 tiles** (+1,257 at 3) against a measured ENG22 bill of **−16,224** (−5,563 at 3). Best case per plate:
**−4,306 / −8,287 / −11,198**. No cell to run.
## 1. Class schedule off the tapes (`sched.py`; 22 ENG22 + 60 TOPLEG/TOPLEG2)
ENG22 SELL MELON units ordered per day — 22/22 tapes sell melon, **none before d10**. Median / mean: **d10 46.5 /
38.5**, d11 6.0 / 6.7, d12-19 0.0 / 26.4, d20-29 0.0 / 15.8, total median **84 u**; 81.9 % lands in d10-19 and the
first melon day is **d10 on every tape** (median first step 249). TOPLEG + TOPLEG2 medians agree (84 u; d10 36; d10-19
72). Day-10 hours: first unit **h04** (1.1 u), bulk **h09-h13** (cum 25.8 of 38.5), tail to h23 — so the row race is
decided between **h00 and h09**.
## 2. The pot on the engine's own curve (`pot.py`, `market_price` imported)
`p(k) = 250 − 0.01k²` above I0=10000 (`sq`, target 3.6); below side `log` +20 % → p(−10)=**271**; floor 1 at **k =
158**. **No SHOP lists MELON** — the only refill is TOWN_CENTER, 1 u/24 steps = **30 u a game**. So the whole-game
melon pot is **188 u for BOTH seats**, of which the MELONGIFT C1 census already sells **153.6** (ours 79.2, theirs
74.4): **82 % consumed at baseline.**

Model calibrated on the C1/M12 ledger (their 74.4 u on the tape schedule; our 14.4 u d10-19 + 64.8 u d20-29 at the
LOT4 hour; plate commit 0.8, displacing 1.55 u of our late melon/tile). Melon line only, Δ vs C1:

| plate | d12 h17 (age 12) | d10 h13 (race lost) | d10 h00 (race won) |
|---|---:|---:|---:|
| P=3  | +2,225 | +2,480 | **+2,876** |
| P=6  | +4,291 | +4,961 | **+5,629** |
| P=12 | +7,409 | +9,328 | **+11,054** |

The whole day-12 → day-10 shift is +651/+1,338/+3,645 — **already banked** (age 10 is what MELONENG played). The
row-order remainder is +396/+668/+1,726 in the model, +1,257/+2,513/+5,026 priced off the measured M12 ledger (the
generous ceiling in §0).
## 3. Denial — one extra unit of ours inserted at pot position k
Pair Δmargin = p(k) + (N−M)·0.02k with N=74.4 theirs, M=79.2 ours still to come; **N−M = −4.8**, so our self-harm
slightly exceeds the denial and the line is carried by p(k) alone:

| k | 0 | 40 | 80 | 100 | 120 | 157 |
|---|--:|---:|---:|----:|----:|----:|
| we earn p(k) / their loss / our loss | 250/0/0 | 234/60/63 | 186/119/127 | 150/149/158 | 106/179/190 | 4/234/249 |
| **pair Δmargin** | **250** | **230** | **178** | **140** | **94** | **−11** |

Denial first exceeds our own take at **k = 100** (p = 150); pair Δmargin stays positive to k ≈ 157. On the melon line
**more melon is always better**, monotone in tiles — the engine agrees (+5,105 pair melon line at M12). **The melon
line is not the constraint; there is no denial-positive plate because there is no denial-negative one.**
## 4. Answer to the user
We *can* out-run them on the row: melon holds 6 units from age 8 but HARVEST unlocks at age 10, so on day 10 we
harvest at h00 and — after one shed DROP, since `_commit_unit` sells from the SHED, not from hands — reach the market
row around h01-h05, ahead of their h04 first unit and well ahead of the h09-h13 bulk. The engine does not forbid the
race; it makes it worthless. The melon curve is **flat at the top, steep only at the tail** (p(0)=250, p(50)=225,
p(75)=194), so being first across the first 75 units buys ~40 coins/u — while the 188-unit pot is already 82 % drained
by the two seats' 153 existing units, so every unit a plate adds is priced at the tail whoever sells first. Winning
the row doubles the melon line (+425 → +845/tile) and the tiles still cost **−1,777/tile** of non-melon production
(the MELONGIFT price gift on strawberry/milk/wool we stop supplying) — **short by 2.1×**. The d10-19 melon rent is a
first-mover *allocation* of a fixed pot, not an asset. MELON_OPEN stays CLOSED and the day-10 race closes with it.

Repro: `python S/melonrace/sched.py S/eng22/ids.txt` ; `python S/melonrace/pot.py`.
