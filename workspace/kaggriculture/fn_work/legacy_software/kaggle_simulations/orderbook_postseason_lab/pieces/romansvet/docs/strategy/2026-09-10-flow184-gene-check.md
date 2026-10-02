# flow184: is the plant-floor gene moving? (2026-09-10, gen 17 mean)

Read-only check of the running arm's ES mean, pulled from
`user@remote-host:~/stage_slope/artifacts/flow184/theta.npy` to
`artifacts/kagg2_games/thetas/flow184_mean_now.npy`.

## The block is moving

`theta[6789:6954]` L2 **0.1974**, max |v| **0.0285**, all 165 coordinates
nonzero (`g12` 6789:6949 L2 0.1921; `gb12` 6949:6954 L2 0.0456, values
`[-0.0110, -0.0249, -0.0229, -0.0214, -0.0189]`). `theta[:6789]` is
**byte-identical** to `flow172_g1000.npy` (max abs diff 0.0) — `--train-only`
is holding. This is *not* flow151: the coordinates receive gradient.

## But the mean decodes no floor at all

Decoding `clip(_qfloor(8·z + 0.5), 0, 16)/16` over the 2,400 recorded
observations in `tests/data/trajectory_obs.npz` (`opp_t_day`/`opp_t_yield`
default to zero), `PLANT_FLOOR_ON=True`:

| | any crop | melon |
|---|---|---|
| nonzero-floor fraction | **0.0000** | **0.0000** |

Mean floor is 0.0000 for all five crops. The decode needs `z ≥ 0.0625`; the
mean's logits are WHEAT +0.0010, CARROT −0.1758, TOMATO −0.2234, STRAWBERRY
−0.1848, MELON −0.1733. Melon's *best* board is 0.164 short of the threshold.

**Selection is burying the gene, not ignoring it.** Against an undirected-walk
null of the same per-coordinate magnitude, the observed mean logit is
**−7.6 sigma**. The population fraction that decodes a floor has collapsed with
it: at the zero init, 48 antithetic pairs at sigma 0.02 moved melon on 19.05 %
of (member, board) pairs and some crop on 64.6 %; around the gen-17 mean it is
**melon 0.12 %, any crop 22.5 %** (that residual is wheat, still near zero).
Once melon's population fraction hits zero the block becomes unsearchable by
drift, whatever the decode can express.

## Logging and gate

`log.jsonl` records **no theta-norm or per-block field** — the trajectory
cannot be reconstructed from it. `mean_win` 0.583 (g1) → 0.678 (g17); the win
rate is climbing on the rest of the theta, which is frozen, so it is rung noise.
The gen-10 real gate **ran and ACCEPTED** (120 games, 80 → 84 wins, net +4,
margin +4,294 → +4,353), written to `best_abs.npy` at gen 18.
