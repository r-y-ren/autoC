# Kaggriculture V38 — Smarter Feed, Stronger Margins

V38 builds on our V37 agent with more selective feed spending, protected sales
of surplus fertilizer, and more precise crop and worker planning. It keeps the
existing thirteen shop routes and responds to the observed game state.

The feeding rule compares the value of production and care with the cost of
wheat. It may omit a feed only for an animal that is currently safe from an
immediate starvation escape, and only when the following day's own route
contains another feeding opportunity. The final production dawn is handled
separately. This scheduling guard was checked against complete game
trajectories, including the survival of every original animal.

Fertilizer sales protect the remaining scheduled pickups and dedicated crop
work. Worker planning accounts for actual hire locations, travel, finite crop
yields and committed inputs before spending additional cash.

This notebook contains the complete frozen agent. Run all five code cells to
write `main.py`, check its integrity, and create
`submission_competitive_v38.tar.gz` in `/kaggle/working`.
No attached dataset, donor download, training, installation or GPU is needed.
The normal path only builds the package. Four optional complete games are
available through `RUN_GAME_CHECKS = True` in the first cell and require the
already installed official `kaggle-environments` version 1.32.7.

The results below are local validation against V37. A live ladder rating is
not guaranteed; this notebook does not submit to Kaggle automatically.

