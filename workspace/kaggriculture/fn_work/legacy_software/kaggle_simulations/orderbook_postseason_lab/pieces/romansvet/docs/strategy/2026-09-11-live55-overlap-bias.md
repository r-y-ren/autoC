# LIVE55 gate-board overlap bias, flow172 lineage (2026-09-11)

**Question:** flow172's remote gate (`--real-gate-opponent` / `--real-gate-leg-family`,
`docs/strategy/2026-09-09-launch_flow172.sh`) selects on 12 tapes that also sit in the
LIVE55 held-out set (`S/livewin/live_heldout_ids.txt`) — exactly the 12 leg-family ids
(107056463, 107067869, 107068399, 107070717, 107072760, 107079367, 107081922, 107088554,
107089992, 107090008, 107092814, 107095149). Method follows `S/live55/flips.py`: base =
`flow135_g350`, key (seed, opponent id, seat), delta = (mine−theirs)cand −
(mine−theirs)base, seat-averaged to one board observation.

**Result: no inflation — a small, real *deflation*.** Across all 8 flow172 candidates the
12 gate boards score *lower*, not higher, than the 43 clean boards. Pooled (gate mean −
nongate mean) over 8 candidates = **−562, SE 188, t −2.99**. The gate is not propping up
the LIVE55 headline; selection on the leg-family metric trades away margin on those same
boards relative to the untouched 43. (The 2 "nonexact" ids `flips.py` normally excludes
sit inside the 12-board gate set, so NonGate43 below is already the clean/excl-2 set.)

| candidate | Gate12 mean(SE) | NonGate43 mean(SE), t, pos | Diff | LIVE43 win% base→cand |
|---|---|---|---|---|
| flow172_g60 | +4245(1611) | +4689(620) t7.6 38/43 | −444 | 44.2→69.8 |
| flow172_g170c | +4352(1971) | +5864(748) t7.8 38/43 | −1511 | 44.2→74.4 |
| flow172_g200 | +4590(2082) | +5653(717) t7.9 38/43 | −1064 | 44.2→74.4 |
| flow172_g260 (g300 theta) | +5701(1759) | +6042(714) t8.5 38/43 | −341 | 44.2→79.1 |
| flow172_g400 | +6217(1860) | +6169(712) t8.7 38/43 | +48 | 44.2→74.4 |
| **g60pair** | +4602(1802) | **+5227(660) t7.9 38/43** | −625 | **44.2→73.3** |
| g170cpair | +6356(1734) | +6301(697) t9.0 39/43 | +55 | 44.2→75.6 |
| **g300pair** | +6017(1891) | **+6630(704) t9.4 38/43** | −614 | **44.2→79.1** |
| **pooled diff** | | | **−562 (SE188,t−2.99)** | |

All LIVE43 (clean, non-gate, n=43 boards/86 games) t-values clear |t|≥2 on their own —
the LIVE55 headline was not being bought by the overlap; g300pair and g60pair (the flow172
"clean" rule reads) hold at t9.4/38-43 and t7.9/38-43 respectively with no gate boards in
sight. Method: `S/overlap/analyze.py`; sources `S/lossflip/<name>_live62.csv`.
