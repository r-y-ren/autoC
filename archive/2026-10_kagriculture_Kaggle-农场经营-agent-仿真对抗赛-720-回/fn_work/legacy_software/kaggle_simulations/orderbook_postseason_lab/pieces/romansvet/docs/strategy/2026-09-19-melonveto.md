# MELONVETO — refusing the melon tile costs more than the tile, at every dose

2026-09-19, branch `herdtilt`. [[melondump]] closed the melon SALE side (one-way ratchet, we already sell at the first dawn lot on 60/60 board-days, the hold counterfactual is negative) and named the one decision left: their 147 units walk the book to `I0 + 127` **before our first melon unit exists**, so our post-d10 melon plantings (12.3/board at 8.75 water turns each, [[opscensus]]) look like dead labour. `plan.MELON_VETO_FLOOD_ON` is that veto — at dawn, `day >= MELON_VETO_FLOOD_DAY` (10) **and** `view.mkt_inv[I_MELON] >= spec.MARKET_I0 + MELON_VETO_FLOOD_K` (60, the same `I0` `_I0_COL` indexes) sets the day's melon `plant_target` to **0**, redistributing nothing. A DEVELOPMENT change and not a mix change on purpose: [[turncost]] re-shared the same tiles onto wheat and gifted +316. `_melon_veto` (`plan.py:7909`) runs after every mix rewrite, before `MACRO_EXEC` (`plan.py:9590`), behind a trace-time Python `if`.

**Byte-identity OFF**: ship7692 + ESR on the first 2 HIBAND ids = 4 rows, `seed/mine/theirs/moves/move_turns/noops/unsold/quads` identical **to the coin** to banked `ship7692_hiband.csv` (HIBAND Δ +0); `tests/test_herd_ramp.py` **35/35**, two new pins — the whole six-array plan on 7 boards (below/on/past the hinge × book quiet / at `K` / dead) digested against `_pin.SHIPPED` `09af88b`, and an ON pin that melon goes to zero, only there, the total falling by exactly melon's share.

## 1. Dose — HIBAND 56 boards, CRN vs `ship7692`, `SW_EXTRA=,MELON_VETO_FLOOD_K=<K>`

| K | Δmargin | se | **t** | Δours | Δtheirs | bett/wors | wins | flips | worst |
|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| **100** | **+0** | 0 | — | +0 | +0 | 0/0 | 41→41 | +0/−0 | −19,542 |
| **60** | **+0** | 113 | **+0.00** | −90 | **−90** | 13/10 | 41→**42** | **+1/−0** | **−17,500** |
| **20** | **−6,629** | 644 | **−10.29** | **−7,973** | −1,344 | 5/51 | 41→**14** | +0/−27 | −20,878 |

`K = 100` never fires: the book does not reach `I0 + 100` while a melon tile is still being asked for. POOLED278 was never run — its precondition is HIBAND Δ > 0 at t ≥ 2, and the best cell is 0.00.

## 2. Census — 10 MELONDUMP boards, ON vs OFF, CRN (`S/melonveto/{run_census.sh,report.py,probe_md.py}`)

OPSCENSUS + MELONDUMP probes verbatim (one `KAGG3_SRC` line), OFF arm their banked `raw/`. At `K = 60` the gate binds on **2/10** boards (melon plantings 11.6 → 11.0, 4 boards move at all): mean Δmargin **+294**, Δours +226, **Δtheirs −68**, 3 better / 1 worse / 6 flat, our melon 83.1 → 79.0 units at 150 → 152/u. Its one real board is [[melondump]]'s own `110504774` — melon plantings 10 → 5, melon water 108 → 65, Δ **+1,730** (theirs −307) — but the freed turns buy **wheat 71 → 76 and fert 155 → 158**, and the melon it still sells is 78 → 48 units at 22 → 35/u. The win is the wheat, not the withheld melon.

## 3. Why the dose refuses it

`K = 20` is the mechanism test and it is unambiguous: **Δours −7,973**, wins 41 → 14, 27 straight flips. Our melon line is ~12.4k of revenue a board at a realised **150/u** — the `22/u` tail [[melondump]] priced is 65 of 78 units on ONE board, not the line. Δtheirs is **−1,344** too, so this is not a gift we are buying out of: it is our own production we are destroying, and [[opscensus]]'s 8.75 water turns per melon plant are expensive and still worth paying. `K = 60` survives only by almost never firing, and what it does is REDISTRIBUTE — the 8 negative-base boards it touches gain +2,703, the 15 positive-base ones lose −2,689, net +14 over 56 = **+0**. A win-rate reshuffle at zero margin, under every bar.

**VERDICT: NO SHIP.** `MELON_VETO_FLOOD_ON` stays **OFF**, byte-identical, layout-free and pinned — a free planting-side switch whose `K = 60` cell is gift-free, win-positive (+1/−0) and +2,042 on the worst board, should a WINRATE gate ever want it. The **melon channel is CLOSED on both sides**: [[melondump]] the sale, this the planting. The arrival gap is real and it is not actionable — our melon is late and cheap and it is still the best thing those tiles do.

Repro: `LEGS=hiband WORKERS=4 SW_EXTRA=,MELON_VETO_FLOOD_ON=True[,MELON_VETO_FLOOD_K=<K>] bash S/winjudge/judge.sh melonveto_k<K> S/winjudge/ship7692/theta7659.npy`; `bash S/melonveto/run_census.sh && python S/melonveto/report.py`. `raw_on/` gitignored.
