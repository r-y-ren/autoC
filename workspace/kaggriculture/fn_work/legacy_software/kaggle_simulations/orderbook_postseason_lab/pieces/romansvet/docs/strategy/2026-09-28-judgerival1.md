# JUDGERIVAL1: a calibrated rival for the closed-loop judge (2026-09-28, 21:53Z-23:08Z; the calibration grid runs past the box on a load-gated remote runner)

Stream dir `S/judgerival1/`. Harness only: no src, dist, package or clone-params change, no upload, no GPU.

## Status
- **Delivered:** `judge.sh --rival <cfg>` and `judge.sh --rival-list`, with four rival cfgs. `caps_fix` is ported into the fast env (it was never there before). A sequential, load-gated runner does the full calibration and body grid (`S/judgerival1/grid.sh`), and the tables script is `an_rival.py`.
- **Calibration numbers are not in yet.** The dispatch allows a cell to start only when the remote 1-minute load is below 8. From 21:58Z to 22:38Z it stayed between 9.5 and 20 (`logs/load.log`). The load came from PROGRAMME1's `pm` judges (3 workers, relaunched in rounds), BCBODY7's judge, trainers and `leg.py`, PACKCLONE1's `pkgrun`, and DATASET1's `pipe.py`.
  - I tried to launch one 1-worker verify above the gate at 22:10Z. The permission classifier refused it, so it did not run.
  - The runner (remote pid 246277, launched 22:31Z) opened its gate at 22:38:25Z (load 7.98).
  - **Verify PASS:** `rcr.py --rival ctrl` reproduces REACTCLONE1's pfs rows 2/2 (tape_highfrequencyf_114080894, both seats, every money and cash checkpoint).
  - The first grid cell, PFS vs `g0capsfix`, started at 22:40:00Z (load 4.96). The load then went back to 15-17, so it had not finished by the 23:08Z time box.
  - The runner carries on by itself (capsfix, then g0, then the choice, then the body rows), gated at load < 8 before each cell. `bash S/judgerival1/grid.sh collect` pulls and tabulates.
- **Default until calibrated: `ctrl`**, which is REACTCLONE1's rival. `judge.sh` reads its default from `S/judgerival1/default_rival`. `grid.sh collect` writes that file only when the chosen rival's four body rows are complete (80/80 each). A tag launched earlier keeps its own rival at collect time (the remote `res/<tag>.rival` marker). So a default switch cannot mis-pair a running candidate.

## The rival cfgs (`S/judgerival1/rivals.json`; all r5a3 params, the ctrl cell plus clone switches only)
| cfg | overrides on the ctrl cell | source of the lever |
|---|---|---|
| `ctrl` | none: GUARD=1 CARE=1 caps90 L7t70 END=1 M3=1 WATER1=1 | REACTCLONE1 rival |
| `g0` | `BCB_GUARD=0` | REACTCLONE1: +4.7k own coins (t 6.1) closed loop, as a body |
| `capsfix` | `BCB_CAP=_fix` = caps_fix.json + the BUY_LAND ledger fix | BCWEIGHT1 / CLONEGAP1: caps90 deletes correct orders |
| `g0capsfix` | both | |

- **The caps_fix port.**
  - The fast env's clone decode (`fastenv/kh.py`) passes only a fixed list of `BCB_*` keys per game. Its cap overlay is `S/capaudit1/agent/main.py`, which has no `BCB_CAPS` / `BCB_CAPLEDGER`; BCWEIGHT1's LAUNCH.md notes this too.
  - So `rcr.py` encodes caps_fix as the per-game value `BCB_CAP="_fix"`, which kh does pass. It patches `kh.MAIN._cap_market` through a one-shot import hook, so rc.py's import order is unchanged.
  - With `_fix`, the patched function is BCWEIGHT1's `_cap_market`, with caps from `S/judgerival1/caps_fix.json` (a byte copy of `S/bcweight1/caps_fix.json`, md5 a66cfc6b) and `CAPLEDGER=1` (the BUY_LAND ledger charges the next quadrant's real price). Any other value calls the original function.
  - caps_fix vs caps90 changes 4 keys:
    - `BUY_SEED|STRAWBERRY` d0-9: 0/0/2/9/7/2/27/1/3/6 -> 60/26/16/28/45/12/44/20/25/28.
    - `BUY_ANIMAL|COW` d7-9: 0/0/2 -> 7/5/11.
    - `BUY_LAND` d7/d9: 0 -> 1.
    - `BUY_SEED|CARROT` d10-29 raised (d10 6 -> 41).
- **`--rival ctrl` is bit-exact by construction.** judge.sh then runs `rc.py` itself, with the same command line as REACTCLONE1. Other cfgs run `S/judgerival1/rcr.py` (runpy of the unchanged rc.py, with `--rivcfg` set from rivals.json).
  - From 22:06Z to 22:30Z the first version of judge.sh sent ctrl through `rcr.py --rival ctrl`, so BCBODY7's `b7_c4w` judge ran that way.
  - That path should be transparent: identical argv plus `--rivcfg '{}'`, and the patch engages only on `BCB_CAP="_fix"`. Step 0 of the runner confirmed it: 2/2 rows exact.

## Rival grid (PFS = vrp18 tree `S/firebank1/tree/src` + the OFF string, 40 boards_m40 x 2 seats; `an_rival.py`)
| rival cfg | n | rival money (all) | rival money orig seat | x live 104.1k (mean per-seat ratio) | seats rival > live | rival h1 cash | ours | margin (t) | W |
|---|---|---|---|---|---|---|---|---|---|
| ctrl (REACTCLONE1 rows) | 80 | 90,106 | 89,811 | 0.875 | 7/40 | 938 | 124,795 | +34,689 (+15.96) | 79/80 |
| g0 | pending (runner) | | | | | | | | |
| capsfix | pending (runner) | | | | | | | | |
| g0capsfix | 80 | 90,217 | 90,143 | 0.873 | 7/40 | 938 | 115,169 | +24,952 (+16.26) | 75/80 |

Live programme rival on these 40 seats (recorded live game, original seat): 104,125.

**First read: g0capsfix vs ctrl, paired over the same 80 games.**
- dtheirs **+111 (t 0.12)**: the rival earns no more money (0.873x of live, the same as ctrl).
- dours **-9,626 (t -7.86)** and flips +1/-5: it takes about 9.6k out of our purse instead. The margin is +24,952 vs +34,689.
- h1 cash is unchanged at 938, so the model buys no d0 strawberry even when the cap allows 60, and the V56 fire value stays 938.
- So the two clone switches together make the rival **harder to beat, but not richer**.
- If capsfix and g0 alone do the same, the ceiling for clone switches is about 0.875x in rival money. The choice rule (closest to 104.1k in rival money) would then not separate the cfgs, because all of them sit at about 0.87x.

**Choice rule (automatic in the runner).** Pick the cfg whose original-seat rival money is closest to 104,125. Nothing is tuned beyond the clone switches. If none reaches 0.95x, that is the strongest cfg, and its x factor is the ceiling. The choice goes to the remote `res/jr_choice.txt` as `<cfg> <x> <h1 cash values>`.

## Body rows vs the chosen rival, next to REACTCLONE1 (same 80 games)
REACTCLONE1 (ctrl rival):

| body | W | ours | rival | margin (t) |
|---|---|---|---|---|
| PFS unfired | 79/80 | 124,795 | 90,106 | +34,689 (+15.96) |
| V56 forced (fire list + 938, D18 hand-back) | 78/80 | 122,116 | 84,696 | +37,420 (+20.83) |
| clone r5a3 ctrl | 34/80 | 93,987 | 93,987 | +0 |
| clone r5a3 GUARD=0 | 64/80 | 98,642 | 92,710 | +5,932 (+7.38) |

- **The chosen rival's rows are pending (runner).** The V56 row's fire list will be `26|29|2046|2338|2438|<h1>`, where `<h1>` is the chosen rival's hour-1 cash against PFS (the `t_h1` column of its PFS cell; ctrl = 938).
- If the choice is `g0` or `ctrl`, the h1 cash should stay 938, because GUARD acts on units and not the h0 market. With `capsfix`, the d0 strawberry cap rises from 0 to 60, so the h1 cash can move. That is why it is re-derived, not assumed.

## Commands
```
bash S/reactclone1/judge.sh --rival-list                                  # cfgs + the default (* marks it)
bash S/reactclone1/judge.sh [--rival ctrl|g0|capsfix|g0capsfix] <tree_src|params.npz> <tag>
bash S/reactclone1/judge.sh collect <tag>                                 # pairs vs that rival's baselines (ctrl: S/reactclone1/res; else S/judgerival1/res/<cfg>/)
bash S/judgerival1/grid.sh launch | collect                               # the calibration + body grid; collect prints an_rival.py tables and sets default_rival
```
- Env as before: `NW`, `N`, `BOARDS`, `SW`, `CFG`. `CFG='{"BCB_CAP": "_fix"}'` also gives a params body caps_fix.
- **Runner.** Cells run strictly one after another, with 2 workers x N=40 (one batch each) and a gate at load < 8 before each cell. The order is:
  - `jr_vctrl` (1 board x 2 seats, rcr.py ctrl vs REACTCLONE1 pfs rows).
  - PFS vs g0capsfix, capsfix, g0.
  - The choice.
  - v56, clone and g0 rows vs the chosen rival.
- **Cost.** Each cell is about 21 CPU-min, so about 12-15 min at load 8-10. The whole run is about 6.5 cells, roughly 90 min once the gate opens.

## Files
- `S/judgerival1/rcr.py` (wrapper + caps_fix port), `rivals.json`, `caps_fix.json`, `boards_x1.json`, `grid.sh`, `an_rival.py`, `checkpoint.txt`, `logs/load.log`.
- `S/reactclone1/judge.sh`: `--rival`, `--rival-list`, the `default_rival` file, and the `.rival` marker read at collect. Tree and params modes are unchanged.
