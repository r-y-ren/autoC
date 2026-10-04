# Round 10 complete-route investment counterfactual

Frozen V9 SHA-256: `6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3`. The official local Kaggriculture environment is `kaggle-environments==1.32.7`. This is a diagnostic, **not** a V10 candidate or a claim against current private DSM code. The opponent here is the old public replay-derived proxy `experiments/round8_top2_dsm_strict.py`.

## Feasible missing action family

At hour 144, V9's `_router` chooses one full tape after the first two shops become visible. Existing compatible route tapes sometimes differ in an animal investment but share the executed opening. The clean example is route 101 (buy two geese, pick up, build coops, place them) versus route 105 (same schedule with two cows and pastures). They have the same actions through hour 144 and only 17 differing hours through hour 647. Selecting an **entire** alternate tape before the day-6 commitment is physically coherent; merely changing `BUY_ANIMAL` would leave pickups, structures and placement inconsistent. See `analyze_route_neighbors.py` and `arlene_mechanism_comparison.md` for the larger route graph and source provenance.

That coherence does not imply positive return. Routes 101 and 105 have identical native EGG/MILK `SELL` schedules through hour 647; the first native EGG sale is not until hour 360 (day 15). Their input orders still differ: route 105 requests two additional fertilizer units. Egg output starts sooner, but a planned egg sale does not necessarily occur soon afterward. Product harvested into a worker's inventory is not cash until it reaches the shed and a market `SELL` executes. At the route decision, a robust selector would need the extra animal and input costs, feed, actual CARE and HARVEST schedule, shed delivery, finite market slots, own price impact, rival price impact and unknown later shop demand. It must store the chosen route inside the Chassis before `_IMPL` reads it; an outer action wrapper is too late.

## One-world official engine comparison

`route_counterfactual_smoke.py` and `route_counterfactual_smoke.json` compare two full 720-step games from already-inspected Round 9 diagnostic seed `242588832`, seat 0, same old DSM proxy. In the second game only, the in-memory router changes V9's natural route 105 to full route 101 at hour 144, with observed opening `BRUNCH_SPOT, SMOOTHIE_SHOP`. This is not a Round 10 development, confirmation or reserve world and is not used to fit a selection threshold. Both games ended `DONE, DONE` and had identical eight-shop sequences.

| Scenario | V9 terminal bank | DSM proxy bank | V9 margin |
| --- | ---: | ---: | ---: |
| Frozen route 105, two cows | 136,439 | 120,310 | +16,129 |
| Forced full route 101, two geese | 134,262 | 121,721 | +12,541 |

The goose route saved 200 coins on day 6 and visibly placed two geese instead of two cows: day 7 held six cows and two geese, versus eight cows in the unchanged route. Its own bank was 1,209 lower by day 14 and 2,177 lower at the terminal step. The proxy's bank rose 1,411 under the altered shared market, so the paired score margin fell 3,588. Both terminal sheds were empty for EGG, MILK and WHEAT. The daily checkpoints in the JSON are observations, not an assertion that each intermediate difference came solely from milk/egg sales; opponent actions react to the altered shared market.

This directly rejects a simplistic "two egg shops ⇒ geese" or "geese mature earlier ⇒ higher net value" rule. It does **not** establish that cows dominate on all shop combinations. No route-selector candidate was promoted from this single pair; branch feasibility is shown, but a state-based conservative bank-margin model and more diverse development games would be required before any change to V9.

## Reproduction and scope

`route_counterfactual_smoke.py` loads the exact frozen source twice and changes only a Chassis router attribute inside one local process; it writes `route_counterfactual_smoke.json`. It does not edit V9, submit to Kaggle, use private top-player agents, or touch Round 10 confirmation/reserve seeds. The script's forced route is intentionally tied to this diagnostic world and **must not be submitted**. Public V9 ancestry and license notices remain in the original source.
