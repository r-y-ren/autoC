# Round 8 public sources and market-layer fusion

2026-09-22. All three notebook sources were extracted with AST literals and standard-library decoders. No notebook cell was executed. The decoded source and every nested literal exec were audited before local testing. The original release files were not modified.

## Sources and inspection

- [Fieldcraft, version 4](https://www.kaggle.com/code/hakdevelopment/kaggriculture-2887-score-fieldcraft-agent): `external/round8/fieldcraft/main.py` and `mirror_plan.py`. Its notebook NOTICE/LICENSE literals are retained verbatim as separate files. Decoded code imports only its local plan module and math. A potentially useful economic layer can skip an unprofitable animal feed while checking survival and tomorrow's planned feeding, then sell the saved wheat. That mechanism needs an independent adaptation; its whole agent was weaker in the screening below.
- [Master Hybrid, version 4](https://www.kaggle.com/code/haideptry/the-2965-master-hybrid-engine): `external/round8/master2965/main.py`. Its SHA-256 matches the notebook's declared `93831c18a43c49312a71fa67171224681c52c3fade0259403e8d8fae7973565f`. It combines inherited V56 mechanisms with R148 overflow recovery, ADV selling existing cash stock up to three turns before its scheduled sale, IG closing empty sale slots, and late seed/fertilizer cuts. The title's rating and benchmark claims are not independently verified by our small test.
- [Ice and Fire, version 13](https://www.kaggle.com/code/leoprovorov/a-song-of-ice-and-fire-fixed-flexible): `external/round8/icefire/main.py`. The final Water Repair layer matches an exact whole-observation fingerprint at step 506 from a specific historical validation scenario. This is a highly specific lookup patch, not evidence of broad production improvement. It did not activate in our two games. Its earlier inherited source remains a usable alternative opponent.

The latter two notebooks package main.py only; original inherited Apache notices inside those files are retained. Each contains two literal embedded exec blocks, for deterministic physical semantics and a terminal planner; these were parsed recursively. No network or subprocess execution was found. An optional `V92_SELL_LIB` environment variable can activate local JSON file loading. It was absent on this host before screening; tests must assert absence or clear it explicitly without printing its value.

Static extraction/audit scripts and full import/call inventories: `research/round8/extract_public_sources.py`, `audit_public_sources.py`, `public_source_audit.json`. Exact nested source copies are stored alongside each main.py. Fieldcraft's `SheepPen.request` is a local game method, not an HTTP request.

## One-world functionality and strength screening

Using official engine 1.32.7, seed84000, both seats versus frozen v7:

| Public source | Seat0 margin | Seat1 margin | Result |
|---|---:|---:|---|
| Fieldcraft | -6683 | -6683 | 0 wins / 2 losses |
| Master Hybrid | +574 | +574 | 2 wins / 0 losses |
| Ice and Fire | -1711 | -1711 | 0 wins / 2 losses |

All six games completed 720 states with DONE/DONE, no stderr, and zero exposed silent-error/fallback counters. Maximum candidate action duration was 0.097 seconds on this host. This is one world, not evidence of leaderboard rating. Data: `results/round8_public_sources_screen.json`.

## Exact-source fusions and bounded alternatives

The builder `research/round8/build_public_fusions.py` asserts the frozen v7 and Master source hashes. It preserves v7 byte-for-byte, appends exact attributed upstream component slices, and adds an explicit last-callable wrapper. That wrapper exposes the component telemetry and synchronizes the final emitted order list to v7's next-turn race detector. Entry names, hashes, component hashes and declared modifications are in `public_fusion_manifest.json`.

- `experiments/round8_advance.py`: ADV only.
- `experiments/round8_fullfusion.py`: R148 + ADV + IG. IG replaces unexecutable cash sales with empty slots, then fills those slots with later effective cash sales while leaving other order positions in place. It does not introduce a new production route.
- `experiments/round8_r148.py`: R148 only; constructed and interface-checked, not locally screened in this subtask.
- `experiments/round8_fullfusion_bounded.py`: same full fusion, with ADV and its frontloading operation both disabled from step696 onward. This avoids overriding the final day's original planner. Constructed and interface-checked; no screening results claimed here.

Both exact-source candidates used the first four frozen development worlds, candidate seat0, against v7 and v6: eight games each, sixteen total. These worlds and opponent lineages are correlated and cannot be treated as sixteen independent samples.

| Seed | ADV vs v7 | ADV vs v6 | Full fusion vs v7 | Full fusion vs v6 |
|---|---:|---:|---:|---:|
| 1118262502 | -291 | -65 | -291 | -65 |
| 457648937 | +472 | +640 | +1295 | +640 |
| 1921079672 | +312 | +633 | +312 | +633 |
| 733556107 | +3615 | +4303 | +3626 | +4351 |

Each candidate won 6/8. Full fusion was equal or better than ADV in all eight paired settings, with improvements +823, +11 and +48 in three settings. R148 itself activated zero times in these eight games; those differences come from IG's queue changes, not overflow recovery. No claim of general benefit is justified until a larger independent panel. The first world remains a regression against both existing versions.

All sixteen games were valid with zero exposed silent errors; the slowest candidate action was 0.319 seconds on this host. Full data: `results/round8_public_fusions_screen.json`. No final release was promoted and nothing was submitted online.
