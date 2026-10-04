## 11. Editable cattle discovery arms

These are **unsubmitted experimental policies**, not a replacement for the default agent or a claimed improvement. They test whether changing up to two or four scheduled sheep purchases to cows can help when the currently visible shops favor milk. Purchases, pickup, placement, harvest accounting, and sale capacity form one coherent change.

The gate requires at least two currently unlocked milk-consuming shops, no Yarn Store, milk price at least wool price, and a compatible existing herd. Purchases must be confirmed before workers are redirected. Travel, pasture construction, care, feeding, harvest visits, and hiring stay on the base schedule. Extra milk is sold only at an existing sale slot, bounded by tracked extra harvest and available stock.

Mechanical checks passed on a day-eight segment: both variants bought, picked up, and placed two cows, handled failed and partial purchases, and respected extra-sale limits. The cap is an upper bound; unresolved animal delivery can prevent later substitutions. Full-game evidence and broad confirmation are separate requirements. Historical livestock experiments on an older base do not transfer their win records to these agents.

Run the next cell to write `cattle_cap_2.py` and `cattle_cap_4.py`. Edit either file, then enable the final benchmark cell. The 24 jobs compare both arms with the unchanged feed baseline on four selected public histories in both seats. The supplied rival action schedules are diagnostic controls, not recovered adaptive opponents. This small discovery set cannot establish a population win rate.
