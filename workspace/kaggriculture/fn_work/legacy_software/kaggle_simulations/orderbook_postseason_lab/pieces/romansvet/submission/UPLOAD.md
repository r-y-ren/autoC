# Final Kaggle uploads

Two submissions were active at the deadline (2026-09-30 23:59 UTC).

| | vrp27_vm_m3 | vrp26_hyb_eve_vrp |
|---|---|---|
| Kaggle submission | 56718602 | 56707958 |
| Uploaded (UTC) | 2026-09-30 ~20:58 | 2026-09-30 ~13:00 |
| Archive md5 | `1133b789592a586aaecb9683c56ea3c3` | `2dcd6d44f1e9fc4a9c006d0dd33dafb3` |
| Files | 37 | 37 |
| In this repository | yes, this folder | no separate copy |

## vrp27_vm_m3 (this folder)

This folder is the unpacked archive, file for file. `python scripts/package_submission.py`
rebuilds the same archive from `src/` with the md5 above.

It is vrp26 plus `ROUTE_VRP_MISS_ON = True` in `kagg3/core/plan.py`: on days where
the crew router finds no solution, it repairs the construction and re-solves
instead of falling back.

## vrp26_hyb_eve_vrp

The same agent without that router repair. Two files differ from vrp27:
`kagg3/core/plan.py` and `kagg3/agent/route_vrp.py`. With `ROUTE_VRP_MISS_ON = False`
the vrp27 code played identically to vrp26 in our paired checks.

## History

Earlier uploads and the evidence for each are in
[`docs/strategy/BUILD-STORY.md`](../docs/strategy/BUILD-STORY.md).
