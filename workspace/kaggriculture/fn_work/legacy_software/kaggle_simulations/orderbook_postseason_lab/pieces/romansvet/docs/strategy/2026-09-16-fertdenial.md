# FERTDENIAL — dumping harder is SELF-denial against the class it was aimed at

2026-09-16 13:42–14:50Z, branch `fertdenial` off master `4c6565b`. The one
direction `2026-09-16-fertreserve.md` §4 left open: our 218-unit fertilizer dump
is worth ~17.5k of the fertilizer-ENGINE class's purse, so **dump harder**.
Priced first, built second, REJECTED at both kill gates and at both signs.

## 1. VERDICT

1. **The denial channel is exact arithmetic.** FERTILIZER is the one product the
   town never drains (`kaggriculture.py:114`), so market inventory is a running
   total of net sells and the quote is linear in it:
   `price(inv) = max(1, round(100 − 0.2·(inv − 10000)))`
   (`MARKET_PARAMS`: base 100, T 200, above `linear`, target 0.40). One extra
   unit dumped takes **0.2 coins off every later fertilizer quote** — the
   rival's **and ours** — for the rest of the game.
2. **So denial has a SIGN, and on ENG22 it points at us.**
   `denial(day) = 0.2·(their units sold after day − OUR units sold after)`. The
   fertilizer-ENGINE cluster sells 211 units a game to our 218: an extra unit
   dumped at d20 is worth **−6.7 coins**. The V45 clone sells 397 to our 199:
   **+21.9**. §2. ENG22 is the HOSTILE leg for this mechanism, not the friendly
   one.
3. **`FERT_DUMP_ON` built, measured, REJECTED** — −91 / −5,212 on ENG22 and
   −80 / −4,745 on V45LEG. And the opposite sign is worse. §4.
4. **`FERT_BUY_DUMP` needs no run**: BUY_PRODUCT is quoted at the *post-buy*
   inventory (`kaggriculture.py:601`, "so a buy/sell round-trip against an
   unchanged market nets zero"), so a round trip moves neither cash nor
   inventory — **no denial at all**, and buy-early/dump-late *raises* the quote
   while it holds the units. Ceiling **0**.
5. **`FERT_DUMP_FRONT` ceiling +79 (ENG22) / +196 (V45) a game in its own
   ledger** — under +450 before the two-purse discount, and in the family
   `2026-09-16-slotmirror.md` closed yesterday (exact rival model: +4,839
   modelled, −23 paid). Not built.

## 2. The instrument — 10 real-engine boards, both seats, shipped pair

`S/fertdenial/probe.py` + `report.py` → `instrument.csv`: both seats' every
FERTILIZER row, its slot and the inventory it was quoted against, out of
`env.steps`. (`steps[t]` carries the state *after* the action it also carries,
so a row is priced at `inv_path[t-1]`; executed units cap at the seat's shed
plus what its units carry — which reproduces `S/fertreserve`'s 218.4 units sold
to the coin and the inventory path to 3-11 %.)

| per game | 5 ENG22 | 5 V45LEG clones |
|---|---:|---:|
| OUR fertilizer units sold | 218.4 | 199.2 |
| **THEIR** units sold | **211.2** | **397.2** |
| their units bought | 12.2 | 68.2 |
| our / their fertilizer revenue | 12,568 / 12,666 | 10,576 / 18,724 |
| their fert revenue as % of their purse | 12.3 % | 17.3 % |
| our FERTILIZE ops (of which day ≥ 20) | 182.6 (81.0) | 184.2 (81.6) |
| our COLLECT_FERTILIZER | 401.4 | 389.8 |
| turns where BOTH sell fert (we are first) | 5.0 (0.2) | 13.4 (3.4) |

**Class split: all 10 opponents sell fertilizer** — 156-286 units on ENG22,
392-406 on V45LEG (a literal `SELL FERTILIZER <shed>` every turn it has any).
No abstaining class to deny. **Denial slope per extra unit dumped on day d:**

| day | 5 | 10 | 15 | 18 | 20 | 22 | 24 | 26 | 28 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ENG22 | −1.4 | −2.7 | −7.5 | −6.4 | **−6.7** | −3.0 | −1.4 | −0.5 | −0.7 |
| V45LEG | +39.2 | +36.7 | +27.8 | +24.0 | **+21.9** | +21.1 | +15.2 | +11.5 | +5.0 |

`FERTRESERVE`'s +17,556 read this slope from the other end at a 107-unit step;
at the margin, per seat, it is −6.7. **Ceilings before building:** (a) front-run
+79/+196; (b) `FERT_DUMP` 81 late applications × (sale 37 + denial − application
value) = −650 ENG22 / **+1,540** V45; (c) buy-dump 0. Only (b) cleared the bar.

## 3. What was built

`FERT_DUMP_ON` (default **OFF**), `FERT_DUMP_DAY = 20`, `FERT_DUMP_BONUS = 20`:
one `where` at the site that decides which tiles are fertilized. From
`FERT_DUMP_DAY`, `fert_bar` rises by `FERT_DUMP_BONUS`, so the unit's sale is
charged at its quote **plus** the denial it buys. An addition, not
`FERT_VOLUME`'s multiple, for the reason H3 records — a multiple of a collapsing
quote stops binding after ~d16. Nothing downstream needs plumbing: `n_fert_want`
falls, `fert_reserved` falls, `avail[I_FERT]` rises, `SELL.allocate` sells them.

`tests/test_fertdenial.py` (11, pass): whole-plan sha256 OFF-identity on five
boards against a pristine `git archive 4c6565b src` subprocess; `BONUS = 0` and
every day before `FERT_DUMP_DAY` re-evaluate to OFF; the bar swept to the coin
(six 120-coin applications survive every bonus to 19, none survives 20); the
refused units are SOLD and no other product moves; `jit == numpy`, one traced
program serving both sides of the day gate.

## 4. The legs — the shipped bar is a local optimum in BOTH directions

Paired per board × seat against the banked shipped pair (`S/lossflip/c2_combo_*`,
legitimate because OFF is master to the byte). ENG22 22 tapes / 44 games,
V45LEG 30 post-09-15 clone tapes / 60 games. Bar +100 and t ≥ 2.

| `DAY`/`BONUS` | | ENG22 | V45LEG | flips |
|---|---|---:|---:|---|
| 20 / **+999** `fdall` | no application from d20 | **−5,212** (t −6.79) | **−4,745** (t −8.92) | −4, −12 |
| 20 / **+20** `fd20` | the clone denial value | **−91** (t −0.64) | **−80** (t −1.12) | 0, 0 |
| — / 0 | **the shipped bar** | 0 | 0 | — |
| 20 / **−20** `fdneg` | apply MORE from d20 | **−20,972** (t −1.78) | **−19,091** (t −2.31) | −1, −7 |
| 0 / **−20** `fdneg0` | apply more all season | **−968** (t −2.73) | **−1,958** (t −2.89) | −1, −5 |

**REJECT, every arm, both legs.** No POOLED180 cut, none warranted: nothing came
within 1,000 coins of the bar over 208 games. **Monotone in suppression** (+20
costs 85, +999 costs 5,000): the 81 late applications are not marginal —
refusing them loses ~60 coins a unit *net of* the extra sale and the denial, so
a late application is worth **90-100 coins against a 37-coin quote** and
`fert_val > price` is a tight bar. The other sign is worse: a −20 bar admits
applications worth less than the unit and `fert_short` BUYS units to make them
(−20,972 at sd 55,157, a variance blow-up). And the clone leg, given its best
case, still paid **−80** against a **+1,540** ledger —
`counterfactuals-overstate` again: the coins denied to the clone are real and
smaller than the crop the application would have grown.

## 5. Standing

* **The fertilizer market-denial family is CLOSED at both signs and all three
  candidates** — hold (`FERT_FLOOR`, `FERT_RESERVE`), dump (`FERT_DUMP`), slot
  (`FERT_DUMP_FRONT`, `slotmirror` under it), round trip (`FERT_BUY_DUMP`).
* **The durable number**: any fertilizer denial lever is worth
  `0.2 · U · (their remaining units − ours)`, and against the ENG22 engine
  cluster that difference is **negative** — we are the bigger seller. Size the
  next "deny their price" idea with that subtraction before building it.
* `FERT_DUMP_ON` ships OFF and stays; master `src` is byte-identical OFF.
* `S/fertdenial/`: `run_all.sh` (`instrument`|`gates`), `probe.py`, `report.py`,
  `instrument.csv`, `raw/` (10 board json), leg csvs `fd20_* fdall_* fdneg_*
  fdneg0_*`.
