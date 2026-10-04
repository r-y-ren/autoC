# Kaggriculture Engine Mechanics: a field guide from the source

Everything below is read directly from the public engine (`kaggle_environments/envs/kaggriculture/kaggriculture.py`). No strategy: just the rules, including a few that are easy to miss.


## The clock and the board
- **30 days × 24 turns** = 720 steps. `day = step // 24`, `hour = step % 24`.
- **10×10 board**, four 5×5 quadrants. You start with NW unlocked; the rest unlock in order **NE → SW → SE** at **1000 / 2000 / 4000**.
- The **shed** sits at the center; exactly four tiles touch it: (4,4), (5,4), (4,5), (5,5). `DROP` and `PICKUP` only work from these.
- Movement onto LOCKED tiles is allowed (units can walk anywhere in bounds): but tile *operations* no-op on locked ground.


## Crops: and the mechanic most people miss

| crop | seed | window | max units | ongoing |
|---|---|---|---|---|
| WHEAT | 10 | age 2–4 | 6 | no |
| CARROT | 20 | age 2–3 | 4 | no |
| TOMATO | 50 | from age 8, every 1d | 4 | yes |
| STRAWBERRY | 100 | from age 10, every 2d | 4 | yes |
| MELON | 80 | age 6–12 | 6 | no |

**One-shot crops (wheat/carrot/melon) gain +1 yield unit per WATER *during the window***: the yield accrues on the water op itself, not at harvest. Water wheat on ages 2, 3, 4 → 3 units. Miss the window days and the units never exist. **Fertilized waters count double.**

**Ongoing crops** tick at midnight instead: each interval day, +1 unit (+2 if watered *and* fertilized that day), held up to `max_yield`.

**Two unwatered days kills any plant**: it becomes a WEED tile.

**Weeds only spawn on empty tiles** (0.5% per tile per night). A tile that's never empty overnight can't grow one. Planting onto a weed silently no-ops: dig first.


## Animals

| animal | cost | structure | first yield | interval | product |
|---|---|---|---|---|---|
| GOOSE | 300 | COOP | day 4 | 1d | EGG |
| COW | 400 | PASTURE | day 8 | 2d | MILK |
| SHEEP | 500 | PASTURE | day 6 | 3d | WOOL |

- Buy → animal appears in the **shed**; someone must PICKUP and PLACE it onto a matching empty structure.
- **FEED daily** (consumes 1 wheat from the feeder's inventory). Two unfed days = the animal **escapes** (gone).
- **CARE + FEED on the same day** banks a bonus: the next yield tick gives +1 extra unit.
- Animals produce **fertilizer daily** (collectable). `FERTILIZE` covers a plant for **2 days** (`until = day + 2`).


## Hands and the midnight reset
- `HIRE` cost is `fib(n)` for the n-th hire *that day*: 1, 1, 2, 3, 5, 8… resets daily.
- **All hands vanish at midnight.** So does their carried inventory: but it isn't lost:
- **Midnight banks every unit's inventory into the shed automatically, free.** Overflow beyond the shed cap (100) is **discarded**.
- Seeds never pass through the shed or inventories: they're consumed straight from your seed stock by PLANT.


## The market
Price is a deterministic function of current market inventory:

```
price(inv) = base + sign · amp · f(|inv − I0|)
```

- Below I0 (scarcity) prices rise along one curve; above I0 (glut) they fall along another. Each product has its own base, curve shapes (linear / sqrt / sq / log) and steepness: wool and melon punish gluts hard (sq), wheat's glut side is a gentle log.
- **Sells execute unit by unit**, each at the price of the current inventory: dumping N units walks the price down as you go.
- **Buys are quoted at post-buy inventory**: a buy/sell round trip against an unchanged market nets exactly zero. `BUY_PRODUCT` exists only for WHEAT and FERTILIZER.
- Both players share one market. Everything either of you sells moves the same curves.


## The town
- Every 3 days the town unlocks a shop, **drawn with replacement** (duplicates happen; each copy consumes independently).
- Shops consume products from the market hourly: draining inventory and therefore **raising prices** on what they eat.
- Consumption is weighted per product; **wheat's weight is 5×**: bakeries, pizza shops, brunch spots and ice-cream shops all eat it.


## Small print worth knowing
- The engine RNG is seeded per `(seed, day)`: replays are exactly reproducible.
- HARVEST no-ops on zero yield; PLACE needs the right empty structure under you; DROP dumps your whole inventory (up to shed room).
- Final score is simply your money at the end of step 719.

Corrections welcome: everything here should be checkable against the source file.
