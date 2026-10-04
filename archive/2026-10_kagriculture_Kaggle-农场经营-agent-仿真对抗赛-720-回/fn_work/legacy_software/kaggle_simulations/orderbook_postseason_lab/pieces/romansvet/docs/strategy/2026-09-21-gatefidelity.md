# GATEFIDELITY — reacting V48 does not reproduce a +5 point `head_940` win gain

2026-09-21, CPU engine gate.  The opponent is the exact public V48 notebook
source at `artifacts/panel_nb/v48/main.py`, seated as a live file agent so that
it observes and reacts to the shared market.  This is the reacting harness from
`S/pipeline/25_clone_leg.sh` / `S/melongenes/run_cell.sh`, not an action tape.

## Protocol

`S/gatefidelity/run.sh` evaluated 250 distinct pinned towns in both seats: the
120 canonical fresh BAND3 ids, followed by the 130 highest numeric episode ids
remaining in `S/winjudge/town_band3.json`.  Each id gets a path to the same V48
source so `town_inject` selects that id's real town schedule.  Seed base is
`3900788701`, `--seed-per-opponent`, one seed per town.  Thus each arm has 500
seat-games and the complete comparison has 1,000 engine games.

Both arms use the exact shipped `a8_940b3` configuration: theta7659 plus its
gene block and the standard shipped switch string.  The theta is byte-identical
to `S/winjudge/ship7692/theta7659.npy` (MD5
`94a8ffd245d4e57898d480b2b1ff01b4`).  Both arms name
`S/actionrl/flow257_ppo_selfplay/head_940.npz` (MD5
`769ff15e7b79c91e1e04e013c962732c`); the only treatment difference is
`RESIDUAL_ON=True` versus `RESIDUAL_ON=False`.

Exact reproducible command:

```bash
JAX_PLATFORMS=cpu WORKERS=8 N=250 bash S/gatefidelity/run.sh
```

The qualified run initially exposed a filename-only bug after both arms had
finished: the ON CSV was preserved, the runner's local assignment was fixed,
and the identically configured OFF arm was recomputed with:

```bash
JAX_PLATFORMS=cpu WORKERS=8 N=250 ARMS=off bash S/gatefidelity/run.sh
```

The final CSVs have 500 rows each, 250 opponents, and exactly equal
`(seed, opponent, seat)` key sets.  They are
`S/lossflip/head940_{on,off}_v48_band3.csv`; cohort order is frozen in
`S/gatefidelity/ids_250.txt`.

## Result

Wins are strict `mine - theirs > 0`, one row per seat-game.  Deltas are ON
minus OFF and use the format of `S/winjudge/report_perseat.py`.

| read | n | wins OFF→ON | win rate OFF→ON | flips +/− (net) | paired margin Δ (SE, t) | Δours | Δtheirs |
|---|---:|---:|---:|---:|---:|---:|---:|
| seat 0 | 250 | 200→203 | 80.0%→81.2% | +4/−1 (+3) | +236.99 (44.27, +5.35) | +232.43 | −4.56 |
| seat 1 | 250 | 201→204 | 80.4%→81.6% | +4/−1 (+3) | +251.79 (44.35, +5.68) | +245.29 | −6.50 |
| **all per-seat rows** | **500** | **401→407** | **80.2%→81.4%** | **+8/−2 (+6)** | **+244.39 (31.30, +7.81)** | **+238.86** | **−5.53** |

The exact two-sided sign test on the ten discordant per-seat outcomes is
`p=0.109375`.  The margin effect is clear and gift-free on average, but the win
effect is only **+1.2 percentage points** (six net wins in 500), not the
required **at least +5 points** (which would require at least 25 net wins here).

## Verdict

**NO: the reacting V48 leg does not reproduce a ≥ +5 point win-rate gain for
`head_940`.  This is not the powered gate.**  Reaction does not explain the
small BAND2/BAND3 tape flip count by revealing a live-sized win effect in this
clone matchup.  `head_940` improves paired margin by about 244 coins with
`t=7.81` and slightly lowers the opponent purse, but against this already
80%-won V48 cohort it changes too few outcomes to account for the roughly
+8-point live win-rate reading.

