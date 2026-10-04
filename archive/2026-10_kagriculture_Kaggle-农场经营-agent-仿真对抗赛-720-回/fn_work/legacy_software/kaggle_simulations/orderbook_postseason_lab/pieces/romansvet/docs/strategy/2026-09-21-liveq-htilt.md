# Live queue: HERDTILT2 hinge -1.0 — NO

2026-09-21. The exact layout-free coordinate is the module float
`brain.HERD_TILT`; the HERDTILT2 arm is `brain.HERD_TILT=-1.0`. The gate-only
shell environment bridge is `HERD_TILT=-1.0`, conditionally forwarded by
`S/actionrl/gate.sh` into `SW_EXTRA` as `,brain.HERD_TILT=-1.0`. It composes
with the shipped res940 stack: `theta7659.npy`, the current gene block, and
`S/actionrl/flow257_ppo_selfplay/head_940.npz` (MD5
`769ff15e7b79c91e1e04e013c962732c`). The code already contains HERDTILT2's
one-sided d12 hinge:
`sig(head[6] + HERD_TILT * max(0, day - 12) / 10)`.

Reproduction, CPU only, pinned BAND3 towns/seeds:

```bash
JAX_PLATFORMS=cpu LEG=band3 N=120 HERD_TILT=-1.0 LABEL=htilt_b3 \
  bash S/actionrl/gate.sh S/actionrl/flow257_ppo_selfplay/head_940.npz
.venv/bin/python S/winjudge/report_band3.py htilt_b3 a8_940b3
.venv/bin/python S/winjudge/report_perseat.py htilt_b3 a8_940b3 band3
```

The gate produced `S/lossflip/htilt_b3_band3.csv` with 240 rows.

## BAND3 board-averaged report

| leg | bds | rows | dmargin | se | t | dours (t) | dtheirs (t) | bett/wors | win% base→cand | flips |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BAND3 | 120 | 240 | **+9** | 73 | **+0.13** | +59 (+0.70) | **+49 (+1.23)** | 25/11 | 54.2→54.2 (65→65) | +0/−0 |

## BAND3 per-seat report

| rows | dmargin | se | t | dours | dtheirs | wins cand/base | flips (net) | sign p |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 240 | **+9.26** | 51.73 | **+0.18** | +58.60 | **+49.34** | 130/130 | +0/−0 (0) | n/a |

## Gate decision

**BAND2 NOT RUN.** Its trigger required BAND3 `dtheirs <= 0` and `t >= 1.0`;
this arm has `dtheirs = +49` and `t = 0.13` on the board-averaged judge, so it
fails both clauses.

**VERDICT: NO — do not queue for live A/B.** The packaging trigger also fails:
BAND3 is not gift-free and `t` is below 1.5. Net per-seat flips are 0, which
meets the nonnegative-flips clause but provides no positive win evidence. No
`dist/submission_res940_htilt.tar.gz` was created and there is consequently no
package MD5.
