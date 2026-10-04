# Next-lever review: measure forward vacancy before another post-sale variant

## Decision

Do not build another sell, smoothie, or post-sale policy variant from the
selected H30 outcomes.  The one missing measurement that can change the
post-sale decision is **forward vacancy**: whether a route-feasible target that
is empty after the sale would have remained unused by B until the injected
crop's first harvest.

The existing feasibility predicate measures only the current day's trailing
PASS suffix.  It calls a tile available when a unit can reach and plant it
today.  That does not establish that the tile is spare productive capacity.

## Preserved-replay result

`S/postlot/forward_vacancy.py` reads the complete paired H30 traces and the
coin-exact OFF baseline.  It uses every firing, without selecting wins or
losses and without combining H30 with another family.

All **44/44** injected targets are used by OFF B before the injected melon's
first harvest ten days after planting.  The median first use is only **two
days** after the hook: 30 targets become STRAWBERRY, 12 MELON, and two CARROT.
There are zero forward-vacant targets in this family.

The action chronology agrees with displacement rather than additive capital:

- after the first firing in each of the 40 firing games, the next day's market
  row and unit route differ from OFF; the median route difference is 21 of 24
  unit-action rows;
- the first changed SELL program appears a median four days after injection,
  six days before the injected melon can yield;
- the full-H30 decomposition already shows the consequences: later own order
  changes drive the largest own losses, while altered shared inventory raises
  the proceeds of unchanged opponent orders.

These facts identify a displacement risk that explains how 44 valid, watered,
six-yield harvests can still lose margin.  On H30 the hook does not deploy cash
into land that OFF B leaves idle through harvest: it takes a tile B was about
to use and changes the crop schedule before its new crop produces anything.
The paired replay does not isolate target reuse from the seed cost, changed
route, daily replanning, or shared-market path, so it does not assign every
later cash effect to displacement.  This is mechanism evidence for H30, not
promotion evidence and not a claim about H30B or any held-out family.

## The single diagnostic

Run a forward-vacancy census on an independent, outcome-blind B replay corpus.
For each existing seed-only route opportunity, retain the exact target chosen
by the runtime geometry rule and inspect the unchanged B replay through that
crop's first-yield day.  Count an opportunity only when the target stays
`None`/`WEED` for the whole horizon.  Report each replay family separately.

The prospective trigger is: positive settled post-sale cash, an
action-preserving route with PLANT+WATER, and a target predicted from current
and past permitted state to remain unused until first harvest.  Its expected
causal change is to reduce replacement of B's next
strawberry/melon/carrot planting and make more of the extra yield additive.
Delayed SELL divergence is a diagnostic hypothesis, not a guaranteed result:
the seed cost alone can change the next daily plan.

Report the forward-vacant opportunity frequency separately for each mechanism
corpus and use its observed coverage to decide whether implementation is worth
an engine read.  Any prospective online proxy must use only current and past
permitted state; measure and report its precision and coverage against the
replay-defined future-vacancy label.  If those measurements support a usable
trigger, the cheapest valid causal test is one default-off engine pilot on a
fresh family with the trigger frozen.  Require all injected crops to harvest,
report whether SELL divergence begins before harvest, and require positive own
coins with no opponent shared-price gain larger than the own gain.  Promotion
evidence must still be read per family under the standing rules.

Reproduce the H30 mechanism result with:

```bash
JAX_PLATFORMS=cpu .venv/bin/python S/postlot/forward_vacancy.py
```

This diagnostic is cheaper and more decisive than H30-selected thresholds:
it uses existing replays, tests the additive-capacity premise directly, and
provides a falsifier before another variant or engine evaluation is spent.
