# MOMREVIEW 2026-09-16 — the momentum result, and whether the agent watches value dynamics

Read-only reconstruction (MOMREVIEW box). Plain answers first, then tables.

## Q1. What was the result of the momentum changes?

**Nothing measurable — and we know exactly why.** The feature was built, wired end to end, trained six ways over two seeds and judged on seven engine families; the learned weights never changed a single executed plan.

The feature (`src/kagg3/core/brain.py:128-134`) is one normalized scalar per product, `(previous dawn's market inventory − today's) / T`. It is rotated once per day by the runtime (`src/kagg3/agent/runtime.py:67-77`) and by the simulator (`src/kagg3/sim/rollout.py:140-156`), and reaches the policy through two appended, zero-initialized gene blocks: `mh` (1→64, into the encoder's hidden pre-activation) and `ms` (1→2, into its grow/sell scores) — 66 parameters, layout 6,789 → 6,855 (`src/kagg3/core/policy.py:338,472-476`; rationale `policy.py:222-228`).

Three things were trained from B (flow193_g100_hr): pop 4,096, 124 episodes, 10 generations, lr 1.8e-4, seeds 311/312, no pooling, no model selection (`S/unitorder/momentum_relative_joint_campaign_20260914/config_J_seed311.json`):
* **mhms** — `train_only "mh,ms"`, the momentum genes alone, 66 live coordinates (`S/unitorder/momentum_train_prepare.py:190`).
* **H** — `train_only "w2,b2"`, the encoder's output head **only**. This is the *control*: no momentum coordinate moves (`config_H_seed311.json`).
* **J** — `train_only "mh,ms,w2,b2"`, momentum genes plus that head.

H and J were each run twice: mixed objective (`abs_weight 0.6`, `momentum_joint_campaign_20260913`) and pure relative (`abs_weight 0.0`, `momentum_relative_objective_campaign_20260913` for H, `momentum_relative_joint_campaign_20260914` for J).

**The decisive measurement is a plan diff, not a judge number.** The trained mhms centres came back with all 66 momentum coordinates finite and nonzero, and the gradient was real (66/66 nonzero, blended RMS 3.21/4.12 per seed). Replayed on the 120 recorded training dawns against B's exact output, seed 311 changed the *macro* on 15 dawns and seed 312 on 11 — and **both changed zero of the six plan arrays on all 120 dawns** (`docs/strategy/2026-09-13-momentum-qualification-and-training.md:636-644`; gradient table :471-478). The reviewers had already named the cause: the signal enters continuous scores that then pass through integer crop allocation, seed/tile/budget caps and marginal-sale constraints, so "a changed macro can leave the same feasible plan preferred" (same doc, :628-635).

The judge confirms it. mhms is **byte-identical to B on TOPB2** — same mean, sd, t and per-board split (`S/topb2/chain_summary.txt:46` vs `:108-109`) — and moves two boards on LIVE62 for +31 coins (`S/live62/chain_summary.txt:302` vs `:556`). Both seeds returned identical numbers to each other: two independent seeds converged on the same no-op.

Everything measured afterwards is therefore the **H head**, not momentum: J minus H is the momentum contribution and it is ≈0 on every family (relative H and relative J return identical LIVEC/LOSS10/NEXTHIGH rows). The head itself lost; two seeds agreed, so not a lottery. The lead closed the family 2026-09-14 and left the prepared H g11-20 continuation (`S/unitorder/momentum_h_continuation_campaign_20260914`) unlaunched (memory `momentum-family-closed-2026-09-14`).

**Nothing shipped.** `submission/theta.npy` is 6,789 float32, md5 7fcf3948, bit-identical to `artifacts/kagg2_games/thetas/flow193_g100_hr.npy`. The momentum block starts at offset 6,789 — it is not in the file. `policy.unpack` zero-pads a short theta (`policy.py:504-509`), so `mh`/`ms` decode as exact zeros and `market_momentum`'s contribution is exactly `+0.0`. **The genes are inert by absence, not by choice**; the runtime still computes and rotates the feature every day (`scripts/package_submission.py:125-155` passes `pass_prev_mkt_inv=True`) and multiplies it by zero.

Absolutes below are verified from judge logs; Δ vs B is the lead's recorded delta. B rows I verified: TOPB2 +1537 t 2.10 (`S/topb2/chain_summary.txt:46`), LIVE55 +10309 t 15.03 (`S/live62/chain_summary.txt:302`).

| family | boards/rows | arm | absolute | t | Δ vs B | verdict | source |
|---|---|---|---|---|---|---|---|
| TOPB2 | 20/40 | mhms 311+312 | +1537 | 2.10 | **0 (identical to B)** | no-op | S/topb2/chain_summary.txt:108-109 |
| LIVE55 | 55/110 | mhms 311+312 | +10340 | 15.20 | +31 (2 boards) | no-op | S/live62/chain_summary.txt:556,562 |
| TOPB2 | 20/40 | joint H 311/312 | +1259 / +1231 | 2.14 / 2.08 | −278 / −306 | lose | S/topb2/chain_summary.txt:111,113 |
| TOPB2 | 20/40 | joint J 311/312 | +1259 / +1231 | 2.14 / 2.08 | −278 / −306 | lose (= H) | S/topb2/chain_summary.txt:114,110 |
| TOPB2 | 20/40 | rel H 311/312 | +1222 / +1079 | 2.21 / 1.90 | −316 / −459 | lose | S/topb2/chain_summary.txt:115-116 |
| TOPB2 | 20/40 | rel J 311/312 | +1222 / +1079 | 2.21 / 1.90 | −316 / −459 | lose (= H) | S/topb2/chain_summary.txt:121-122 |
| LIVEC-H30 | 30/60 | rel J 311/312 | +327 / +363 | 0.69 / 0.75 | −445 / −409 | lose | …/momentum_relative_J_seed31x_strength/judge_evidence/02-LIVEC-H30.log |
| LIVEC-H30B | 30/60 | rel J 311/312 | +1201 / +1150 | 2.95 / 2.74 | +170 / +119 | level | …/03-LIVEC-H30B.log |
| LIVE55 | 55/110 | rel J 311/312 | +10129 / +10158 | 16.47 / 16.40 | −225 / −199 | level/lose | S/live62/chain_summary.txt:596,620 |
| LOSS10 | 10/20 | rel H+J, all seeds | −593 | −1.22 | −593 | lose | …/05-LOSS10.log |
| NEXT30 | 30/60 | rel J 311/312 | +3874 / +3881 | — | −84 / −77 | level | …/06-NEXT30.log |
| NEXTHIGH | 30/60 | rel J 311/312 | +2052 / +2055 | — | +8 / +10 | level | …/07-NEXTHIGH.log |
| NEXTHIGH | 30/60 | joint H 311/312 | +1469 / +1446 | — | −575 / −599 | lose | …/momentum_joint_H_seed31x_strength/…/07-NEXTHIGH.log |
| LOSS10 | 10/20 | joint H+J, all seeds | −926 | −1.51 | −926 | lose | …/momentum_joint_*_strength/…/05-LOSS10.log |
| — | — | H g11-20 continuation | **never launched** | — | — | closed | memory momentum-family-closed-2026-09-14 |

§115b needs POOLED180 ≥ +450 **and** t ≥ 3 on the increment; no arm came within reach on any family.

One honest positive: as a *predictor* the lag helps. Adding the nine previous-dawn deltas to all 234 existing feature columns cut mean squared error for next-day inventory movement in all nine products — melon +13.0 %, fertilizer +7.5 %, tomato +7.5 % — though carrot and tomato had negative median episode improvements (`docs/strategy/2026-09-13-momentum-prediction-check.md`). **Prediction improved; no decision did.** That gap is the whole result.

## Q2. Does the agent continue to monitor the dynamics of values?

**PARTIAL — and the live part is forward, not backward.**

The shipped agent reads **no history of any price or market value**. Every price-derived network input is a level taken at today's dawn. The one history feature built, `market_momentum`, is computed daily and multiplied by absent (zero) weights: a no-op in production.

What *is* dynamic is a **forward projection**. The planner does not price a new seed or animal at today's quote: it advances today's market inventory by the town's drain out to the crop's first-yield day and adds both seats' standing pipeline, then reads the price curve there (`src/kagg3/core/plan.py:6909-6911` → `src/kagg3/core/projector.py:261-270`), and prices each candidate seed and animal off that projected level (`plan.py:6922,6943-6951`). That models where price is *going*, from known drain and known committed supply — never where it has *been*. `valuation.py:20-21` states the intent: "Prices are today's hour-0 quotes — the Phase-1 projection. Opponent impact and multi-day drift are [LEARNED] and arrive with the Phase-2 genome."

The engine offers no history anyway: the observation carries `market = {"inventory": …, "prices": …}`, a snapshot re-derived each turn by `_refresh_prices` (`.venv/lib/python3.11/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py:181-182,209-212,628`). Any history must be accumulated by us across turns — exactly what `runtime.Runtime` does for `prev_mkt_inv` and `tell.RivalTell` per turn.

| feature | file:line | level or dynamic | consumer | live? |
|---|---|---|---|---|
| `(mkt_inv − I0)/T` | brain.py:521 (`prod` c0) | level | encoder → grow/sell | yes |
| `price/base` | brain.py:522 (`prod` c1) | level | encoder → grow/sell → crop & animal mix | yes |
| `log1p(base)`, `T/450`, `_BT`, `_AT` | brain.py:523-526 | static constants | encoder | yes |
| `daily_town_demand` | brain.py:527 | level (today's shops) | encoder | yes |
| own / opp producing tiles, own shed | brain.py:528-530 | level | encoder | yes |
| `mean(price/base)` | brain.py `glob` idx 19 | level, market-wide | **global head** (dev_frac, animal_share, land) | yes |
| drain gap / share | brain.py `expected_drain` | level + forward supply | encoder via `dh`/`ds` | yes |
| `production_forecast`, `forward_value` (h=1/3/7) | brain.py, genes `fh`/`fs`/`fv` | **forward** | encoder + head | yes |
| **`market_momentum`** | **brain.py:128, used :957** | **dynamic (1-day lag)** | genes `mh`/`ms` | **computed, weights absent → 0** |
| `projected_inv` / `inv_at_day` | projector.py:192,261 | **forward** (drain + pipeline) | `_candidates` seed/animal pricing, sell lots | yes |
| `open_pump_tell_keep0` (pot h0 vs h1) | plan.py:2064-2093 | dynamic (1-turn) | day-0 BUY row | `OPEN_PUMP_TELL_KEEP0_ON = False` |
| `RivalTell.batch()` / `.burst()` | agent/tell.py, runtime.py:46-62 | dynamic (per-turn inv delta) | sell-slot ranking | `RIVAL_TELL_ON` / `SELL_SLOT_RIVALRANK_ON` = False |
| `OPP_SUPPLY` forecast | plan.py:1832 | forward | projector | `OPP_SUPPLY_ON = False` |

`plan.py` holds no price history, EMA, trend or slope: grepping `prev`/`delta`/`hist`/`trend`/`slope`/`momentum`/`last_price` returns only routing geometry (`prev_x`/`prev_y`, plan.py:9695-9707) and day-flag comments.

### What this means for PRICE-AWARE PRODUCTION

Momentum is the **wrong carrier** for "stop producing a product whose price has collapsed"; the level/glut path is the right one, for three already-measured reasons. (1) The quantity is a *level*: under a fixed market table the quote is a deterministic function of current inventory, so a lag adds realized path information but **no new price level** (`docs/strategy/2026-09-13-price-momentum-review.md`, Answer). A product pinned at price 1 is fully described by today's inventory, and its momentum may be zero *because* it is at the floor. (2) The signal is aggregate and unidentified — town drain, both seats' trades and end-of-day shop draws all move it — "plausible but noisy" per the same review. (3) The genes were trained and **changed zero plans on 120 dawns**; that bottleneck sits downstream of the feature, so a new *input* into the same encoder scores risks the same fate. The veto belongs where the integers are decided, not where the logits are.

The machinery mostly exists — this is a gain problem, not a missing-feature problem. `_candidates` already values the k-th sheep as `grow_mult[WOOL] * clip(wool_stream + fert_stream − feed_cost)`, with `wool_stream` read off the **projected** wool curve (`plan.py:6946-6957`). The wool-at-1 pathology is visible right there: `fert_stream` is shared by every animal kind and independent of that animal's own product, so once wool revenue collapses the sheep is still bought for its fertilizer stream and clears the budget threshold. Per-product price reaches the *mix* only through `grow`, while the *total* production size is set by `head[5]` (dev_frac) and `head[6]` (animal_share), whose only price input is `glob[19]`, the market-wide mean — so one dead product can shift the share but cannot shrink the total.

Next levers, in cost order: (1) a per-product glut/floor feature into the **global head** (not the encoder), so total production can contract when one product dies; (2) a plan-side production veto in `_wants`/`_candidates` refusing a candidate whose *own-product* projected stream is below a threshold, decoupled from `fert_stream`, so a sheep bought for fertilizer is priced and judged as a fertilizer purchase; (3) if a temporal input is ever revived, feed previous-dawn inventory movement into the **planner's projection** (`inv_at_day`'s drain estimate), not another encoder logit — that is where a level error actually changes an integer.
