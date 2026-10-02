# First selected HARVEST: exact suffix result

The extra hand successfully harvested and banked3WHEAT, paying21coins to hire.
This is physical execution evidence, not a net-gain result: it removes an
existing crop and also changes the next shop unlock through the shared RNG.

The case was fixed from the static census before replay: episode107764944,
seat0,day8,seed1408844682,positiveSELLhour10/emptyHIREhour11. Currentcash1253,
required109 including originalreserve88; no later purchase/hire liability.
Spawn[5,4], NORTH,NORTH,HARVEST hours12–14, target[5,2], WHEAT plantedday5.
The target hasyield3 and remains legal on arrival before its lifespan240.

Root24343 completed exit0 undercap180+kill10, following four focusedroot tests
and independent review. Source-lock and static/funding/route/dependency hashes
are bound. Baseline both-seat replay is state-exact from the true seed through
EOD. The alternative preserves every baseline action, inserts onlyHIRE and the
new last hand's route, and never overlays a recorded state on the counterfactual.

Every pre-EOD snapshot asserts the actual extra hand's position, exact inventory
(empty then WHEAT3), target (originalplant thenNone), and hire-count/cash delta
before normalized comparison of all remaining physical state. Raw both-seat
actions/states/diffs are preserved at13hours. The baseline and alternative
actual `_drop_inventories_to_shed` calls are intercepted, restored in finally,
and their pre-drop shed/seeds/existing inventories match exactly. There isroom35
after existing inventories, so all3new WHEAT are accepted and0destroyed.

At EOD only the target tile differs between the farms' grids. However, the
additional empty tile consumes another weed-RNG draw and the town's thirdshop
changes from YARN_STORE to PET_CAFE. Both are exact reference-engine branches;
no town or weed difference is normalized away. Future crop production, prices,
replanning and opponent effects remain unmeasured. No terminalgain, channel
closure, performancepilot or promotion follows this single fixture.

Receipt `S/hireasset/harvest_suffix_first_root.json` SHA256
5c01725ac8e5aa73bdb87ebd8e5d0c7ed09225095342d04f3356481457951e54;
rootaudit/log adjacent. The two earlier fixed PASS/WATER fixtures are unchanged.
