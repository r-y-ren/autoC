# Does the loss band place its coin on the same missing turns as the top tier? — 2026-09-12

**Question.** `docs/strategy/2026-09-11-expressibility.md` measured the action
interface against 29 **top-tier** tapes and closed with caveat (v): *"the
2200-band clone we lose to has a different cadence and is not measured here."*
That matters because the SELL5 falsifier (`S/sell5`, `SELL5_TURNS =
(3, 7, 10, 14, 18)`) was designed against the top-tier number — 42.0 % of their
sell coin in restock windows 1/3/5 — and SELL5 buys windows 1 and 3 only.
If our actual losses put their coin somewhere else, SELL5 is aimed at the wrong
turns.

**Method.** Same classifier, same classification, three more sets. The only
change to `S/express/census.py` is CLI plumbing (`--ids --tapes --prefix
--title`) plus one restock-window table that is a pure re-aggregation of the
per-turn table it already printed; re-running the 29 ids reproduces
`S/express/census.md` line for line. Tables: `S/express/census_band.md`;
per-set reports and per-tape CSVs `S/express/census_{loss10,band85,live,pooled}.{md,csv}`;
id lists `S/express/ids_{loss10,band,live}.txt`.

| set | n | source |
|---|---:|---|
| TOP29 | 29 | the 2026-09-11 baseline (`S/express/ids.txt`) |
| LOSS10 | 10 | `S/bloss/loss_ids.txt` — the 2175-2381 opponents that beat B 19/20 (glut §32-33). **All 10 tapes present** in `artifacts/tape_actions_town`; nothing missing, nothing downloaded. |
| BAND85 | 85 | the weight-2 pinned training rungs of `S/flow209/launch_flow209.sh` = the ~1900-2100 band (`S/band2100p/town_schedules.json` is the pinned-town registry for all 538 cut tapes, not a band list, so the band set was taken from what the arm actually trains on) |
| LIVE48 | 48 | the opponent seat of **all 48 losses** in `S/leftover/manifest.json` (sub 56161192), cut from `S/ep_<id>.json` with `scripts/make_tape_actions.py --replay` into the scratchpad (48/48 converted, 719 frames each, no drops) |
| POOLED | 137 | the three above, unique episodes |

---

## The side-by-side

Sell coin in restock windows 1 (turns 4-7), 3 (12-15) and 5 (20-23) — the three
of six price windows our seat **never presents a sell order in**:

| set | sell coin | windows 1/3/5 | **share** | Δ vs top tier |
|---|---:|---:|---:|---:|
| TOP29 (baseline) | 5,774,300 | 2,424,480 | **42.0 %** | — |
| **LOSS10** | 2,507,365 | 1,216,475 | **48.5 %** | **+6.5 pt** |
| BAND85 | 17,046,280 | 6,559,110 | **38.5 %** | −3.5 pt |
| LIVE48 | 10,535,130 | 4,562,420 | **43.3 %** | +1.3 pt |
| POOLED | 29,011,245 | 11,898,960 | **41.0 %** | −1.0 pt |

Per window, share of each set's own sell coin:

| window | turns | our lots | TOP29 | LOSS10 | BAND85 | LIVE48 |
|---:|---|---|---:|---:|---:|---:|
| 0 | 0-3 | 1, 3 | 36.6 | 25.4 | 36.7 | 28.5 |
| **1** | 4-7 | none | 9.7 | **7.5** | 11.1 | 8.7 |
| 2 | 8-11 | 10 | 10.6 | 12.9 | 13.1 | 13.9 |
| **3** | 12-15 | none | 12.1 | **15.7** | 10.3 | 15.2 |
| 4 | 16-19 | 18 | 10.8 | 13.1 | 11.8 | 14.3 |
| **5** | 20-23 | none | 20.2 | **25.3** | 17.2 | 19.5 |

## Answer

**Same family, different turns inside it — and the shift is away from the two
turns SELL5 adds and towards the one window it deliberately refuses.** The
mechanism is identical on every set: sale *timing* outside our four lot turns is
81-85 % of all inexpressible coin (LOSS10 84.5 %, LIVE48 81.8 %, BAND85 81.0 %,
TOP29 81.9 %), the farm half is 92-94 % expressible everywhere, and even the
UNION over every switch leaves ~half the coin unreachable (LOSS10 45.5 %
expressible vs TOP29 49.6 %). So the interface claim is *not* a top-tier
artefact: the band we actually lose to is, if anything, marginally further
outside our decoder than the top tier (expressible coin 19.0 % vs 17.9 %
SHIPPED, but windows 1/3/5 48.5 % vs 42.0 %). What changes is *where* inside the
day. The loss band is **not a turn-0 dumper**: turn 0 carries 8.9 % of its sell
coin against the top tier's 19.3 %, and the A1 turn-0 hole drops from 19.9 % to
9.8 % of inexpressible coin. Its coin moves instead into the **evening tail**
(window 5 25.3 % vs 20.2 %, with turn 21 alone at **12.1 % vs 6.6 %** — the
d13-21 wool/melon dump the LOSS10 anatomy already named) and into **window 3**
(15.7 % vs 12.1 %, turns 13/15 at 6.3/5.3 %). Window 1 — where SELL5's turn-7
lot goes — is the *only* window where the loss band is **quieter** than the top
tier (7.5 % vs 9.7 %). Net, SELL5's two new lots reach windows 1+3 = **23.2 %**
of LOSS10 sell coin vs 21.8 % of TOP29's, so the lever is not misaimed — it is
worth about the same against both — but against the band we lose to it leaves
the single largest unreachable block, window 5 at **25.3 %**, untouched; that
one block is bigger than both windows SELL5 buys. The live-loss set (LIVE48,
43.3 %, turn 21 at 8.4 %) sits between the two, which is what you expect when
the ladder mixes both classes.

**Reading for the campaign.** (1) Run SELL5 as staged — the falsifier is valid
against our real losses, not just the top tier, and it covers ~23 % of the sell
coin on both. (2) If it buys anything, the *next* interface step is the
window-5 lot (a lot at turn 21), not a richer function on the lots we have: it
is the biggest single hole against the loss band (25.3 %) and the second biggest
against the top tier (20.2 %). `S/sell5/README.md` documents why turn 21 was
left out (it moves `SELL_TURNS[-1]` and with it `TURN_PRESTOCK`, the DROP-day
budget, `MIDDAY_PLACE_V2_TURN` and the day-29 chain) — that is a planner change,
and this census says it is the one worth paying for. (3) The LOTS block
(flow208) still covers 0 % of the inexpressible coin by construction on every
set; its reach is the 22.2 % (LOSS10) / 22.6 % (LIVE48) / 29.0 % (BAND85) of
sell coin already landing on turns 1/3/10/18.

**Caveats.** All four from the 29-tape census carry over unchanged (reference
pricing at the base quote, not live quotes; the qty ≥ 900 dump-all rows priced
at zero, which understates the d27-29 tail — and the loss band's tail is exactly
where its coin is, so **its 25.3 % window-5 share is a floor**; unit "order"
checks only the PICKUP-block rule; `BUY_PRODUCT` at d0 turn 0 scored
inexpressible). New ones: LIVE48 tapes were cut without `--with-town` (the
classifier reads only the action arrays, so this is cosmetic); BAND85 is the
weight-2 rung slice of the live arm, not a rating-filtered re-cut; 6 of the 10
LOSS10 ids also appear in LIVE48, so those two sets are not independent; and
LOSS10 is a **loss-selected** set of ten tapes — per the 2026-09-11 anatomy they
are one public band clone on tomato-poor towns, so its cadence is that clone's
cadence, measured cleanly, but its 10-tape sample is not a random draw from the
2200 band.
