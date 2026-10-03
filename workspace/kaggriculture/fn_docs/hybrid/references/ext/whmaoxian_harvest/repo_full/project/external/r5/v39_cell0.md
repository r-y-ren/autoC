# Kaggriculture V39 — Ready Before the Rush

V39 consolidates our strongest tested additions to V38: production-calendar
feeding, bounded wheat replenishment, earlier protection of scheduled grain
pickups, and stock reserved before a turn with a full market queue.

The agent keeps thirteen shop routes and uses observed inventory, worker
positions, cash and market state. Grain protection starts when the shop route
is known. Current cash must cover all requested purchases at conservative
quotes; future harvests and sale proceeds do not count as available cash.
Changes preserve existing order slots and reject additional overnight overflow.

This is a tested submission candidate. The original independent comparison
showed higher cash and a small net win gain, but did not establish a positive
win-rate confidence bound. The exact results and that limitation are retained
below; no live ladder rating is guaranteed.

Run the five code cells to create `main.py` and
`submission_competitive_v39.tar.gz` in `/kaggle/working`. The complete agent is
embedded as ordinary Python source. No attached input, download, installation,
training or GPU is needed. The default run only builds and verifies the package.

Set `RUN_GAME_CHECKS = True` in the first cell to run four optional complete
games with the already installed `kaggle-environments` 1.32.7 engine. The
notebook creates the archive and does not submit it automatically.

