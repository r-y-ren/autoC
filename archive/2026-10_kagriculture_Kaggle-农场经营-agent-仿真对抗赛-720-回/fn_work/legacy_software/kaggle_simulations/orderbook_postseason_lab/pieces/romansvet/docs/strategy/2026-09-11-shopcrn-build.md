# KAGG3_SHOP_CRN: common random numbers for the end-of-day shop draw (2026-09-11)

Build + verification only. Nothing launched; `src/` untouched in arms-next and
main. Tree `/root/tree_shopcrn`; patch `S/shopcrn/sim_shopcrn.patch`.

## Mechanism (cites)

* `sim/eod.py:71` `host_stream` — a **fresh** `random.Random((seed*1_000_003)^day)`
  per day. Days do not carry over; the coupling is not stream position.
* `sim/eod.py:~150` `spawn_weeds` — 2 words per **empty** tile, seat 0 then
  seat 1, returns `used`.
* `sim/eod.py:267` `end_of_day` — `base = SHOP_CRN_BASE if shop_crn else 2*used`;
  `unlock_shop` reads `words[base+k]`, 1 word per attempt, `>>28` rejecting ≥8.

The shop word's **index is our tile count**. Draws/day = `2*used` + ~2.
`STREAM_WORDS` 416, `SHOP_CRN_BASE` 400 = one past any weed walk.

**The flag already existed** as `--shop-crn` / `Config.shop_crn` (commit
`a85b008`, 2026-09-06), unused by any arm. This build adds only the env-var
face `KAGG3_SHOP_CRN=1` (`SHOP_CRN_ENV`, read once at import), so a rig that
drives an existing launcher byte-for-byte can reach it. No seat in the key:
the unlock is one town-wide `choice`, `st.shops` shared.

## Premise (confirmed)

Exhaustive over every tile count, 3 boards × 30 days: **65.6 % (11,804/18,000)**
of ±1-empty-tile steps change that day's shop; the tile stays planted, so every
later day re-rolls too. End-to-end, B vs a σ-0.02 perturbation, 42 boards: shop
sequences differ on **40/42 boards, 1,038 board-days**.

## Verification

| test | result |
|---|---|
| inert (unset) | patched vs SAME tree unpatched, 42 boards × 29 days: money **coin-exact**, shop sequence identical |
| marginal | 9,000 board-days (300 boards × 30 d): ON-vs-OFF χ² homogeneity **p 0.817**, KS **p 1.000**; vs uniform OFF p 0.355, ON p 0.837 |
| fitness | B, 42 boards: OFF −16,469, ON −18,838, **Δ −2,368 (sd 20,880, se 3,222, t −0.74)** = level |
| the fix | ON: B vs the σ-0.02 perturbation differ on **0/42 boards, 0 board-days** |
| trace-time | `SHOP_CRN_ENV` assigned once at import; `end_of_day` never reads `os.environ`; the branch is a Python `if` on two bools → baked in at trace |

## Caveats

1. First inert read said FAIL: baseline `S/localarm/tree` differs from
   arms-next in `plan.py`/`train.py`. The baseline must be the same tree.
2. **Pinned-town boards already have this**: `unlock_shop` lets a recorded town
   override the draw, so on every judge leg and `S/simscreen` board the
   treatment is a no-op. The lottery it removes is live only where the shop is
   *drawn* — check which training rungs those are before costing a gain.
3. Boards = `artifacts/tape_actions`, both seats, arbitrary seeds: only the
   paired Δ means anything.
4. TRAINING ONLY. Never for an engine leg, fidelity gate or package build.

Rig: `S/shopcrn/run_onestep_shopcrn.sh` (MODE=shopcrn|both, same pre-registered
E3c bar as §75), **not launched**. `S/dither/stage_tree.sh` now takes
`SHOPCRN=1` next to `DITHER=1`; the patches touch disjoint files.
