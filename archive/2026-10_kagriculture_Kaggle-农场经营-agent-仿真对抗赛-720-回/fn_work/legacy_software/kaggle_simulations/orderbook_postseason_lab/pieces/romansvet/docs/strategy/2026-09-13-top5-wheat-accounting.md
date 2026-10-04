# Saved top-five wheat accounting: a template-specific result

This no-game diagnostic uses exactly the two already-saved public wins for each
historical rank 1-5 in `S/top50/features.json`: Majkel1337 episodes 107773713
and 107779556, SpaTaro 107762721 and 107784471, feel the agi 107782433 and
107785473, Otter Vibe 107756423 and 107784468, and c0nrad 107779563 and
107785475, at their recorded seats. The selection and stop rule are constants
in `S/unitorder/top5_wheat_accounting.py`. Selection matches the earlier
hash-pinned feature catalogue. The author set the rule before computing new
action totals, but there is no separately timestamped pre-result manifest
proving that chronology. Published purchase counts were already known.

For each episode the helper reconstructs executed market totals from the saved
ledger and evaluates recorded unit actions sequentially against their observed
pre-action tiles and inventories. The wheat identity is

`initial + purchased + harvested = fed + sold + final + unaccounted loss`.

The residual makes this an accounting identity; it does not independently
prove that every physical flow was explained. Unaccounted loss is not assigned
to purchased or harvested wheat. Shed overflow is one possible contributor,
but these totals do not separately establish its cause. Mixed wheat inventory
does not reveal which source supplied a particular feed or sale.

| template / episode | bought | harvested | fed | sold | final | loss | product spend | animal output units | wheat bought / output |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Majkel / 107773713 | 129 | 680 | 353 | 438 | 1 | 17 | 4,485 | 841 | 0.153 |
| Majkel / 107779556 | 154 | 673 | 336 | 466 | 0 | 25 | 5,286 | 794 | 0.194 |
| SpaTaro / 107762721 | 436 | 662 | 458 | 635 | 3 | 2 | 16,221 | 1,020 | 0.427 |
| SpaTaro / 107784471 | 347 | 728 | 407 | 666 | 1 | 1 | 11,216 | 926 | 0.375 |
| feel the agi / 107782433 | 417 | 535 | 360 | 590 | 2 | 0 | 16,195 | 906 | 0.460 |
| feel the agi / 107785473 | 427 | 650 | 447 | 630 | 0 | 0 | 16,310 | 1,011 | 0.422 |
| Otter Vibe / 107756423 | 193 | 750 | 363 | 580 | 0 | 0 | 9,672 | 935 | 0.206 |
| Otter Vibe / 107784468 | 283 | 357 | 379 | 261 | 0 | 0 | 14,322 | 901 | 0.314 |
| c0nrad / 107779563 | 850 | 424 | 375 | 883 | 16 | 0 | 29,718 | 846 | 1.005 |
| c0nrad / 107785475 | 823 | 484 | 512 | 775 | 20 | 0 | 28,790 | 1,038 | 0.793 |

Product spend includes fertilizer purchases as well as wheat, so it is shown
as an audited episode total and is not mislabeled wheat spend. Animal output is
the physical sum of harvested egg, milk and wool plus collected fertilizer;
its sale revenue and item split remain in the JSON. These heterogeneous units
have different prices and production costs, so this ratio is not a comparable
economic-efficiency measure across templates. It is not a causal return
on purchased wheat: animals can produce without a current feed, while feeding
also affects survival and care bonuses.

## Stop decision

The frozen descriptive criterion required at least two non-Majkel templates to
have median purchased wheat per animal-output unit no greater than Majkel. The
template medians are Majkel 0.174, Otter Vibe 0.260, SpaTaro 0.401, feel the
agi 0.441, and c0nrad 0.899. There are zero supporters, so the stop fires.

Majkel's low purchased-wheat burden is real in these saved games, but it is not
a shared top-five signature: c0nrad reaches rank five with roughly five times
Majkel's ratio, and the other templates span the interval. This stops the proposed
generalization of this particular purchase/output ratio. It does not test
whether feed-input efficiency can improve B. It does not show that
Majkel's private schedule is bad, that B is efficient, or that one scalar can
reproduce the result. No B case was selected, no policy pilot follows, and no
new replay or simulation was used.

The JSON records SHA-256 provenance for every replay and ledger and preserves
all ten rows separately at `S/unitorder/top5_wheat_accounting.json`.

Independent Sol reproduction matched the full JSON byte-for-byte
(`bf764fcb93ae8324aaf07a4d846f0b654fc9c72e18adeb30ea38695556dd7dfa`).
It also verified all ten team/seat joins and public-farm equality between both
observers across every720-frame replay. The result remains limited to these
ten selected wins and the declared heterogeneous physical-unit ratio.

A targeted sequential-action incidence check found no WATER-before-wheat-
HARVEST collision in these cases. Three WATER/HARVEST collisions were all
HARVEST-before-WATER on strawberries; duplicate animal operations are handled
by the helper. Action validity still comes from actions and prestate, rather
than complete observed-delta verification.
