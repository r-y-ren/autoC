# Head-off BAND3 — 2026-09-21

```bash
JAX_PLATFORMS=cpu WORKERS=6 N=120 LEGS=band3 bash S/winjudge/judge.sh ship7692b3 S/winjudge/ship7692/theta7659.npy
.venv/bin/python S/winjudge/report_band3.py a8_940b3 ship7692b3
.venv/bin/python S/winjudge/report_perseat.py a8_940b3 ship7692b3 band3
.venv/bin/python S/winjudge/report_perseat.py a8_257_940b2 ship7692b2 band2
```

`S/lossflip/ship7692b3_band3.csv` has 240 rows and the same CRN keys/order as `a8_940b3`.
Sample head-off/head-on `ours` deltas are −227, −371, +429, and −927, confirming the head is off.

| read | leg | rows | dmargin (SE, t) | dours | dtheirs | wins base→head | flips +/− (net) |
|---|---:|---:|---:|---:|---:|---:|---:|
| board averaged | BAND3 | 240 | +211 (47, +4.46) | +224 | +13 | 63→65 | +2/−0 (+2) |
| per seat | BAND3 | 240 | +211.30 (33.91, +6.23) | +224.25 | +12.95 | 126→130 | +4/−0 (+4) |
| per seat, reference | BAND2 | 466 | +325.45 (28.37, +11.47) | +299.69 | −25.76 | 348→350 | +6/−4 (+2) |

Yes: head_940 shows **+4 net per-seat win flips on BAND3** (54% head-on wins), alongside the live +230 rating and 2,775 vs 2,524 matched score.
BAND2 is **+2 for head-on minus head-off**; the cited −2 is the reverse, head-off-minus-head-on orientation used by the `ship7692b2` row.
Thus the head's win effect is positive on both legs, and stronger on loss-enriched BAND3 than on 75% win BAND2.
