# MELONREACT — the ceiling of a REACTIVE melon decision, measured before any gene

2026-09-17 08:48–09:40Z. Measurement box, **no `src/` change**. Branch `melonreact` off `70b98ff`.
`S/melonreact/{tell,boards,pot,oracle,judge,predict}.py` + `run_legs.sh`; rows `S/melonreact/rows/`
(4 fresh engine legs, 240 games, WORKERS=1); reports `S/melonreact/*.md`.

## 0. CLAIM AND VERDICT
Claim (lead, unmeasured): *"the only escape from the melon first-mover rent is a reactive day-10 melon
decision keyed to the rival's observable inventory."* **FALSIFIED on three counts.** (1)
`CROPS["MELON"]["first_yield_day"] = 10` — a tile planted on day 10 first yields on **day 20**, so the
d10-16 rent window is closed at *planting* time, by day 4-6; a day-10 decision cannot reach it.
(2) The key has no variance and the wrong sign: **59/60** top-10 tapes and **21/22** engine tapes plate
melon by d5, `r(rival day-0 melon, plate Δ) = −0.09`, firing on "rival shows no melon" = **−371/board**.
(3) Two purses: every plate arm hands *their* purse more than ours (**+10,763 vs +3,557** top-10;
+15,547 vs −676 ENG22), and MELONGIFT showed the gift is **non-melon**. **No gene spec written.**

## 1. Board set
`boards.py`: of 60 TOPLEG2+3 top-10 boards, 21 are retention-gated (≥0.85), lost by FT2 and carry
rival melon in d10-16 — the **18** with the largest rent exposure are the losing cut, the **7** gated
boards FT2 wins are the cost cut (a reactive rule fires there too). Melon is the largest negative line
of exactly this population (`2026-09-16-toploss.md` §2-3: −14,612 on the losers, 100 % PRICE). ENG22
is the second class; `tell.py` reads each rival's own action tape — no download, no engine.

## 2. The rent priced on the engine's curve (COUNTERFACTUAL, zero cost, 16 boards)
Melon (`base 250, above sq 3.60, T 300`) quotes `250−0.01x²` at `x` units above I0; 158 reach the
floor and both seats commit ~155, so the rent is a **queue position on one fixed pot**. `pot.py`
reverses that queue (our ~80 u take their recorded melon days, theirs slide to d21); drain swept.

| response | Δmargin drain 1 | drain 4 | Δ ours | Δ theirs |
|---|--:|--:|--:|--:|
| full queue reversal = **the whole rent** | **+9,599** | +3,318 | +4,839 | −4,760 |
| (a) sell earlier — only the ~17 u ripe in time | **+1,953** | +1,237 | +868 | −1,085 |
| (b) no melon planted after d5 (63 u gone) | **−10,647** | −15,152 | −8,756 | **+1,891** |

(a) is capped because only our 2.8 d0-9 tiles × 6 ≈ 17 u ripen before d16; the other 63 are planted
d10-19 and cannot sell before d20 at any price. **Neither (a) nor (b) is expressible by the 41-int
macro**: the melon share is a theta coordinate (`crop_mix`/`cd`), and the only melon knob,
`brain.MELON_GENE_ON`, scales all nine crops at once.

## 3. (c) the conditioned day-0 plate — MEASURED in the engine
`MELON_OPEN_ON` *is* expressible. Isolating control C1 (`BANK_BEFORE_LOT_ON=False` alone) = **−538
t −1.39** on the top 10 (+78 t 0.33 on ENG22): null, the loss is the plate's own.

| cut (M12 vs C1) | n | W | Δmargin | se | t | Δ ours | Δ theirs |
|---|--:|--:|--:|--:|--:|--:|--:|
| melon-rent LOSING boards | 18 | 5 | **−8,581** | 3,568 | −2.41 | +4,844 | +13,425 |
| gated boards FT2 WINS | 7 | 0 | **−14,843** | 4,963 | −2.99 | +584 | +15,427 |
| whole top-10 pool | 60 | 20 | **−7,206** | 2,127 | −3.39 | +3,557 | +10,763 |
| ENG22 engine class (banked MELONENG) | 22 | 2 | −16,224 | 2,311 | −7.02 | −676 | +15,547 |
| **ORACLE** — fire only where it wins | 60 | 20 | **+2,731** | 767 | +3.56 | +3,296 | +566 |

## 4. Can any observable pick the oracle's boards? No (82 boards, `predict.py`)
Oracle ceiling **+2,106/board**. Best **in-sample** threshold rule on anything the rival shows before
day 6: `fert ≤ 40` +404 (1 board), `u d10-16 ≥ 112` +266 (5), `m05 ≥ 18` +195 (2), `sellday ≤ 10.1`
+103 (5) — all in-sample maxima under the §115b +450 bar — and the proposed key `m0 ≤ 0` is **−371**
(r −0.09). The plate wins where the rival plates **more** melon, not less: unbuyable selection, not a tell.

## 5. Consequence
Reactive-melon family **CLOSED** at every handle: the whole pot is +9,599/board at zero cost, the only
arm that reaches it costs −7,206…−16,224 paired and gifts +10,763…+15,547, the reachable slice is
+1,953 COUNTERFACTUAL, and no pre-day-6 observation predicts the sign. The one *real* reactive melon
gate already ships: `brain.decide`'s `absorb` test on the shared drain share, threshold `out.sat` ∈
(−2·DRAIN_CLIP, 0], read every planting day and already walked by ES — it moves plantings, never the
d10-16 queue. Repro: `bash S/melonreact/run_legs.sh`, then `python S/melonreact/{judge,predict,pot,oracle}.py`.
