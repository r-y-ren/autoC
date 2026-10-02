# NOOPAUDIT — ineffective orders census + NOOP_FIX_ON (NO SHIP)

Branch `noopaudit` from eseng1 (caeb6620, shipped res940_cfog3). 2026-09-23T00:30Z. Reacting-V56 dev100 (live250 0..99), CPU.
Hook `S/noopaudit/audit.py` (read-only on engine: unit action pre/post, market commits, PLANT veto); `census.py` → `census.tsv`, `summary.txt`.

## Census (OFF, per game)
| class | /game | where | root cause (engine rule) | at stake |
|---|---:|---|---|---|
| SELL_CLIP_ALL_SOLD | 12.1 | d29 end rows | "sell all" qty 100 > shed stock; every unit in shed sold | 0 (by design) |
| SELL_ZERO_STOCK | 10.7 | d29 end rows | sell order for an item with 0 in shed | 0 |
| WATER_ON_DECAYED | 8.2 | d20-29, hands | spent ongoing crop decays from dawn (`_decay_plants`), WEED by hour 2(y-1); planner never sees `max_lifespan_step` | 1 turn each, 71 % followed by PASS |
| HARVEST_ON_DECAYED | 1.2 | d20-29, hands | same tiles; harvest routed at hour ≥ 7, tile dead by hour ≤ 2 | 2.3 units/game (~240 coins nominal) |
| DROP_EMPTY_INV | 1.3 | d29 h17-22 | end-route DROP by a hand carrying nothing | 1 turn, then PASS |
| CARE_ALREADY | 0.4 | h22-23 | tail care on an already-cared animal | 1 turn, then PASS |
| other (PICKUP/FERT/FEED/PLANT) | 0.1 | — | — | ~0 |
| BUY/HIRE rejections, PLANT veto | 0 | — | never occur | 0 |

Total unit no-ops 11.3/game (= econcensus `ineffective_orders`); 9.4 of them are the decayed-tile class, which WATERAUDIT
already counted as WATER_NOOP*/HARVEST_NOOP*. No cash / stock / shed / veto rejection exists on our seat.

## Bug and fix (`NOOP_FIX_ON=False`, runtime-read, plan.py + agent/parse.py)
Genuine planner bug: the mandatory tier assumes "a deadline harvest keeps its units until tomorrow"; for a spent
ongoing crop (tomato/strawberry after its final fire, day `last`) the engine sets `max_lifespan_step=(last+1)*24`, so
unharvested units rot from the next dawn and the next day's WATER/HARVEST orders cannot succeed.
- `NOOP_FIX_EXPIRE` (part 1): harvest of a spent ongoing crop on day `last` joins the mandatory tier.
- `NOOP_FIX_DOA` (part 2): `parse_view` shows a tile that is WEED before hour `NOOP_DOA_H`=3 (engine-exact from
  `max_lifespan_step`) as yield 0 / watered, so no route goes there. No new work either way.
OFF: `tests/test_noop_fix.py` 8 passed (planner digest pin, engine-decay cases); engine OFF parity 3/3 boards byte-equal.
Effect: unit no-ops 11.25 → 1.93/game (ON), decayed-tile orders 9.44 → 0.05; EXPIRE alone cuts rotted attempted units 2.30 → 0.69.

## Gate (reacting-V56 dev100, paired vs fresh OFF 67-33)
| cell | L→W | W→L | net | Δours | Δtheirs | identical |
|---|---:|---:|---:|---:|---:|---:|
| NOOP_FIX (both) | 1 | 2 | −1 | +19 (se 26) | +30 | 31 |
| DOA only | 1 | 1 | 0 | +44 | +48 | 37 |
| EXPIRE only | 0 | 3 | −3 | −54 | +61 | 76 |

Ship bar (dev net ≥ +1 AND Δtheirs ≤ 0) failed by every cell → held-out / tapes / ENGINE legs not run (conditional gate, as EXPIRY1).
**Verdict: NO SHIP.** The bug is real and the fix removes it, but the freed turns are worth ~0 (they were end-of-day
tail turns followed by PASS) and forcing the last-day harvest displaces better-valued work (−54). Flag stays OFF.
Ineffective-orders channel CLOSED: the remaining 1.9/game are zero-value d29/h23 tail turns.
Reproduce: `WORKERS=11 [ZX=",NOOP_FIX_EXPIRE=False"] bash S/noopaudit/run.sh <off|on|doa|exp> 0 100 dev`; census: `python S/noopaudit/census.py S/noopaudit/audit_dev_off S/noopaudit/`.
