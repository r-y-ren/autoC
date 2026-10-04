# R11 day-11 melon allocation: frozen experimental candidate

Candidate: `experiments/round11_crop_optimizer.py`, SHA-256 `70bd3cee0385cabb22aab549633450fd71cc1f09512353d660ae892b314fe766`. Built reproducibly from frozen V9 by `build_round11_crop_optimizer.py` and `experiments/round11_crop_optimizer_suffix.txt`; it wraps the **actual final** `round9_slack_agent`. V9 and root `main.py` are unchanged. This is an experiment, not a release or Kaggle submission.

## Mechanism

V9's native day-11 route buys/plants 13 strawberries in seed-order prefixes 5, 9 and 13. The candidate may substitute the first 5 or 9 with melon while retaining at least four strawberries. It changes only existing `BUY_SEED` and `PLANT` commands, hence uses the same land, hire, worker positions and daily watering route. Once harvested melon is actually in the shed, it sells it using an available market slot. The program does not forecast deposits in the same turn as sale. If the native 13-seed route is absent, it leaves V9 untouched.

The choice compares full patch cash flow to the 13-strawberry baseline at official per-unit market prices, updating market inventory after each simulated unit sale (so melon sales reduce later melon quotes). It prices the existing visible crop stock in both alternatives, capturing the effect of removing strawberry output on other owned strawberries. Current inventory, market parameters, shop instances and visible planted tiles are read from the observation. Unknown future strawberry-buying shops and new rival output are varied across three declared scenarios; future shop identity, rival private stock, replay seed, player identity and opponent identity are not read. Melon has no shop buyer and only town-center demand. A candidate must clear an absolute gain budget and a bounded downside budget. The model assumes 3 saleable melons per replaced tile, compared with 4 physically harvested in one old smoke; it estimates native berry waves at 2 units per tile, excluding sites the first two native passes miss.

The change corrects a major R10 estimator defect: three inspected **old diagnostic** V9 replays actually harvested 95–97 units from the day-11 13-berry tranche, whereas R10 V2 valued only 78. The same three tapes show roughly 25 fertilizer actions and repeated watering on those tiles in days 20–26. Crop substitution therefore has a materially larger opportunity cost than the R10 tomato-only proposal assumed. These are physical route observations, not an opponent-specific rule.

## Bounded official smoke

`results/round11_crop_optimizer_smoke_1829941733.json`: completed valid game against the old public-replay-derived DSM proxy. The candidate chose 9 melons and verified 9 bought, 9 planted, 36 units harvested and 36 sold; telemetry errors 0. Terminal difference was −19,311 versus frozen V9's previously recorded −23,525 in this **already-known** diagnostic world. This confirms execution, not generalization.

`results/round11_crop_optimizer_smoke_242588832.json`: completed valid game in a previously inspected high-berry-price world. The candidate selected 0 substitutions, and the terminal difference was +16,129, matching the frozen V9 diagnostic. It confirms the no-operation branch.

The two old worlds were seen during design and **must not** be counted as evidence of win-rate lift. The price model does not know future crop acquisitions, labor failures or competing sales timing. The frozen candidate must pass fresh, paired, both-seat development games across diverse opponent families before any consideration for a release. Do not use R10/R11 confirmation or reserve worlds to tune this candidate, and do not infer performance against current private top submissions from the old DSM proxy.
