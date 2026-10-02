# Intraday market controller — independent review B (blind, 2026-09-10)

Judged tree `.claude/worktrees/arms-next` (HEAD 45f8217); `agent/runtime.py` and switch defaults are
byte-identical to main, but **differ from the flow180 lineage**: `ship-pair`/`drain-pair` ship
`BANK_BEFORE_LOT_ON = TAIL_FILL_ON = True` (`plan.py:1871`/`:2615`) where these have both False.

## Claim table

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 1 | plan built at hour 0, replayed | **TRUE** | `runtime.py:30-34` rebuilds only on `hour == 0` / no plan / new day; `render.py:52-60` indexes cached op arrays by turn. `core/loop.py` is a backend shim, not a runtime concept. |
| 2 | only a narrow opening exception revises the market | **TRUE; that exception is coded but OFF** | `runtime.py:42-44` patches the cached plan from the hour-1 pot; `OPEN_PUMP_TELL_KEEP0_ON = False` (`plan.py:1276`). |
| 3 | shipped intraday switches | ON: `OPEN_PUMP_ON` `plan.py:1173`, `OPEN_PUMP_SLOT0_ON` `:1244`, `EARLY_SELL_ON` "A" `:2463`, `TAIL_CARE_ON` `:2697`, `DROP_ON` `:315` (terminal day only). OFF here, ON in the pair tree: `BANK_BEFORE_LOT_ON`, `TAIL_FILL_ON`. OFF everywhere: `MIDDAY_PLACE_ON` `:773`, `MIDDAY_PLACE_V2_ON` `:922`, `SAME_DAY_FERT_ON` `:1010`, `MIDDAY_DROP_ON` `:383`, `OPP_SUPPLY_ON` `:1507`. |
| 4 | mid-day "actual inventory" is a real input | **FALSE for harvest; reachable only by a purpose-built excursion** | Unit ops resolve before the same turn's market, so a PLACE at hour h is sellable in hour h's row (`plan.py:877-880`) — but harvest otherwise sits in unit inventory until `sim/eod.py:210 drop_inventories`, and SELL is capped by `shed[item]` (`sim/market.py:5`). `plan.py:6575-6581`: "the day's harvest reaches the shed at end-of-day and is sold tomorrow morning, so the hour-0 stock is exactly what the lots can draw on." |
| 5 | feed reservations / expected deposits are new information | **FALSE — priced at hour 0** | `plan.py:6579-6590` nets `wheat_reserved = sum(want_feed)` and `fert_reserved = n_fert_eff` out of `avail` before `SELL.allocate`; the forced-overflow leg projects tonight's shed (`:6618-6630`). |
| 6 | react to a failed purchase | **FALSE — no signal** | `plateau-review-verdicts.md:108-112`: orders refused **3.96×/game = 0.07 % of 5,666 acting turns**, **0 of 1,971 BUY rows**, 0 HIRE/LAND/PLACE/DROP/PICKUP/MOVE; only signature is d21-29 SELL rows short ~19 units (liquidation sizing). "A re-plan-on-refusal hook has nothing to react to." |
| 7 | production-timing features exist | **TRUE, but hour-0 macro inputs** | `brain.production_forecast` (`brain.py:492`), `forward_value` (`:444`); genes `fh`/`fs`/`gp`/`fv` (`policy.py:379`/`:416`/`:439`) — consumed once in `policy.decide` (`:860-869`) → `Macro` → `build_day`. Prior verdict: "already implemented … **inert**" (`plateau-review-verdicts.md:49`). |

## Levers measured paired in the engine

| Lever | margin | t | n | outcome |
|---|---|---|---|---|
| **Minimal mid-day revisit** (shrink the lot to units still clearing the hour-0 quote) — *the proposal itself* | **−4,964** | — | 128 games | **DROPPED**; denial signature, their purse +2,015 (`2026-09-05-build-story.md:816-829`) |
| `OPP_SUPPLY` — react to opponent supply, scale 1.0 / 0.5 | **−2,972 / −3,616** | **−3.80 / −4.81** | 192 | **CLOSED**, win 54.2→46.9 %, dose-responsive the wrong way (`plan.py:1485-1495`) |
| `MIDDAY_PLACE_V2` same-day deposit+row; `COLLECT_DROP` mid-day drop; `COLLECT_DAY_SELL`; `LATE_LOT` | **−2,589** (theirs +2,776); +1,010 pinned / **−1,441 drawn**; +100 no flip; turn-22 row **sold zero** of 4,846 asked | −3.80 | 96–131 | **SAME-DAY-SALE FAMILY CLOSED (4 builds)** (`2026-09-04-verdicts.txt:175`) |
| `SAME_DAY_FERT`, `EARLY_SELL` "Z"/"Z1", `MIDDAY_DROP`, `MELON_D10`, `EARLY_MILK`, `HIRE_ROW`, shop-adaptive family | −27,186 / −5,511; −4,658 / −773; −2,713; −18.6k; −1,592; −378; rest dose-responsively negative | −15.6; −2.76; −13.6; −0.75 | — | **ALL CLOSED** |
| `SELL_CADENCE` 4/6 rows and `SELL_TURNS` variants | −324 / −348; −165, −77 | ≤0.94 | 42 held-out | **SELL-HOUR FAMILY CLOSED — "do not revisit"** |
| `DROP_EARLY`, `WOOL_DUMP_D13`, pump-aware hour-1 row | **byte-identical to OFF** (192/192, 192/192, 392/392) | — | — | **INERT; families closed** |
| Route insertion/exchange **oracle** — ceiling on re-routing | **429 value units/game = 0.08 %** | — | 2,880 days | **Dropped** |
| `BANK_BEFORE_LOT`+`TAIL_FILL` pair — bank a block's harvest **before** the early lot | **+875** LIVE55, +1,403 LEG20 | **3.69**, 37/53 | 110 | **PROMOTED** in `ship-pair`/`drain-pair` — an **hour-0 route/sale coupling**, not a mid-day revision; `BANK_LOT=2` variant −1,257 |
| `EARLY_SELL` "A" (dawn re-schedule); `OPEN_PUMP` (hour-0/1 opening row) | +2,184; **+20,509**, panel24 64→87 % | 5.13; 12.7 | 768; 24 | **PROMOTED**; `EARLY_SELL` now **spent** (−77 HELD42 under g60) |

**~28 levers measured; three ever won, and all three are hour-0 decisions** — a dawn schedule, a day-0
opening row, a dawn route/sale coupling. No mid-day *revision* has ever won. Adjudicated verbatim at
`plateau-review-verdicts.md:50`: *"revise market decisions during the day | closed: goods reach the
shed at end of day; every excursion lost/level; refusals 0.07 %"*.

## Verdict: DO NOT RUN as written — RUN NARROWER

All four named inputs are void (claims 4-7); the proposal's own minimal form was run and lost
**−4,964/game**; the re-routing ceiling is 0.08 %. Family bound **+0.1–1.7k/game against a −10.3k
loss margin** (`2026-09-09-verdicts.txt:1034`).

**Smallest experiment instead** (one line, already written, no new inference):
set `OPEN_PUMP_TELL_KEEP0_ON = True` (`plan.py:1276`; hour-1 patch `runtime.py:42-44`,
`plan.open_pump_tell_keep0` `:1703-1737`, both tested). It is the only intraday branch never priced in
the engine; it fires once on day 0 and reads the one mid-day fact that provably exists — the other
seat's hour-0 wheat draw off the hour-1 pot. Run it on the flow180 pair tree.

**Judge**: paired LIVE55 vs the LIVE base — d-margin > 0, seat-grouped |t| ≥ 2 (both seats averaged
into one observation first), ≥ 28/53 positive (`2026-09-09-judge-live55.md:19-27`); drawn legs veto
only (grouped t ≤ −2). On failure, close the family rather than narrowing again.
