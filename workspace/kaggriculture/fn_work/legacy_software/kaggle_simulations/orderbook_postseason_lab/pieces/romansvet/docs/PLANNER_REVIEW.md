# Planner architecture review

Reviewed 2026-08-24 against the implementation in `src/kagg3/core/`, the pinned
Kaggriculture engine, the simulator, tests, training code, and the project design
documents.

## Verdict

The overall architecture is strong, but the current planner is not the best
possible implementation. Keep the once-per-day network and deterministic shared
compiler; redesign the executor and action vocabulary. Several current choices
create deterministic losses that additional ES training cannot learn around.

The following foundations should be preserved:

- one network evaluation per day, satisfying the runtime constraint;
- one array-agnostic planner implementation shared by JAX and numpy;
- static-shaped action arrays that compile efficiently under JAX;
- integer macro decisions and deterministic tie-breaking;
- learned budget-category and labour-priority ordering;
- bit-exact simulation and cross-backend release gates.

At review time, all 108 existing tests passed, including simulator-equivalence
tests. That proves the current design is implemented faithfully; it does not show
that the planner's restricted action space is strategically optimal.

## Critical findings

### 1. The budget walk does not predict what is actually bought

This is the most important correctness issue.

The planner budgets wheat and fertilizer as `quantity * hour-0 price`. The engine
instead:

- applies turn-0 town consumption before turn-1 purchases;
- quotes a product at post-buy inventory;
- reprices every individual unit;
- may be affected by the opponent buying the same product;
- stops when money or shed capacity runs out.

Compare `core/plan.py:306-381` with the unit-by-unit quote walk in
`sim/market.py:50-84` and `sim/market.py:199-251`.

Consequently, `wheat_avail` and `fert_avail` can exceed the quantities the engine
really purchases. Later PICKUP, FEED, and FERTILIZE actions then silently no-op.
The claim that every task is clamped to what was actually bought is therefore not
generally true.

Suggested changes:

- add market inventory, town demand, and shed headroom to `DayView`;
- reuse the shared price-walk logic when calculating affordable quantities;
- include shed-capacity limits;
- use a conservative allowance for opponent-coupled product purchases, or allow
  the executor to clamp resource-dependent work after the completed purchase.

### 2. One-day harvest latency is a planner choice, not an engine limitation

The engine supports this same-day chain:

1. HARVEST into unit inventory;
2. return to a shed-access tile;
3. DROP into the shed;
4. SELL later in the same day.

Unit actions happen before market actions, so DROP and SELL can occur on the same
turn. The simulator deliberately omits DROP because the current planner never
emits it (`docs/DESIGN.md:157-161`).

A stronger day schedule can support:

```text
morning work tour -> return/drop -> afternoon sell -> optional second tour
```

This would permit day-29 harvest revenue, improve liquidity, and reduce
end-of-day shed overflow. Implementing DROP in the simulator and equivalence
tests is required before exposing it to the planner.

### 3. The late-planting gate is provably wrong for one-time crops

`brain.decide` checks `CROP_FIRST_YIELD_DAY`, while one-time crops are normally
harvested at `CROP_MAX_YIELD_DAY`. This permits deterministic write-offs:

- wheat planted on days 25-26;
- carrot planted on day 26;
- melon planted on days 17-18.

Use `first_yield_day` for ongoing crops and `max_yield_day` for one-time crops,
then require harvest and sale feasibility under the selected revenue schedule.

### 4. Task selection is value-blind and routing is locality-blind

The task score only sees broad flags such as harvest, survival, feed, and
development. It does not represent:

- product value or banked quantity;
- decay or terminal deadline;
- production cadence;
- marginal fertilizer or CARE return;
- overflow risk;
- incremental travel caused by selecting a task.

After scoring, a global sequence sorted by task value can jump repeatedly across
the board. This wastes turns walking even when the selected task set is good.

A better deterministic pipeline is:

1. assign each task a learned or economic urgency;
2. select a feasible task set under labour capacity;
3. cluster selected tasks spatially by unit;
4. route locally inside each cluster.

A quadrant/stripe partition followed by a local serpentine traversal is a simple
baseline. A deterministic greedy-insertion route over at most 100 tiles is also
small enough for this environment.

### 5. Spatial development is inefficient

Free slots are allocated in serpentine order beginning near `(0, 0)`, while the
shed is near the board centre. Early animals and high-touch crops can therefore
be placed far from the shed.

Placement should account for future maintenance cost:

- animals and frequently harvested crops near the shed;
- low-touch one-time crops farther away;
- empty structures selected by value and route fit, not serpentine position.

### 6. Fixed crop and animal cadence wastes labour

Current actuator rules include:

- harvesting ongoing crops whenever any yield is banked;
- harvesting animal products whenever any yield is banked;
- collecting every available fertilizer unit;
- feeding only for survival or globally every day;
- caring for every fed animal when CARE is enabled;
- watering ongoing plants only for survival.

Stronger deterministic cadence rules should:

- batch harvests near the product's held-yield cap;
- collect fertilizer only when its expected value exceeds labour and storage cost;
- feed on production days when a CARE bank must pay out;
- water fertilized ongoing crops on production-fire days;
- apply CARE only when its bonus will survive and not be lost to the yield cap.

### 7. Shed overflow cannot safely be left entirely to ES

The policy sees current shed fill, but its feature vector lacks enough information
to forecast the exact planned additions. In particular, it does not expose
per-product banked harvest totals or the scheduled collection workload.

The planner already knows the intended harvest operations and should:

- forecast end-of-day additions;
- make room through sales where possible;
- prioritize harvests by value when room is insufficient;
- avoid collecting low-value fertilizer that displaces higher-value output;
- eventually use same-day DROP and SELL routes.

### 8. Purchases happen before sales

The current schedule hires at turn 0, buys at turn 1, and starts selling at turn
2. Existing shed stock therefore cannot finance today's development.

Expose a small number of learned schedule templates, for example:

- `hire -> buy -> sell`: earliest development;
- `sell -> buy -> work`: liquidity-constrained expansion;
- `work -> drop -> sell`: terminal-day or capacity-constrained liquidation.

These remain deterministic and require only one policy evaluation per day.

### 9. The macro action is too restrictive

Important restrictions include:

- only one animal type handled per day;
- at most one quadrant bought per day;
- one global sell-lot count;
- one global feeding cadence and CARE switch;
- no cash reserve;
- no harvest or fertilizer-collection threshold;
- forced restocking of every compatible empty structure.

A modest expansion could add:

- `animal_target[3]` instead of one kind and count;
- `land_count` or a land budget;
- per-product sell timing or a small schedule bucket;
- `cash_reserve`;
- product/animal harvest thresholds;
- fertilizer collection and use targets;
- an optional empty-structure conversion target.

This is still a tiny action space compared with per-turn control.

### 10. Newly bought land cannot be developed on the purchase day

The planner constructs tasks from the hour-0 board. A quadrant bought at turn 1
is therefore left idle until at least the next day.

When the budget walk grants land, the compiler can include the soon-to-be
unlocked quadrant in its post-purchase task set and route units there after turn
1. The macro decoder must also size development against current free tiles plus
the prospective 25 tiles, with the planner clamping back if the purchase is not
granted.

### 11. Positional rationing and forced restocking hide strategy

When wheat or fertilizer is short, serpentine rank determines which tile receives
it. This ignores survival urgency, product value, CARE payout, and route
feasibility. Compatible empty structures are also restocked even when the learned
animal count is zero.

Allocate scarce inputs by marginal value and make restocking obey an explicit
animal target.

### 12. Fertilizer is not protected consistently

Wheat required for feeding is reserved from sales, but planned fertilizer is not.
With a feed pickup present, the fertilizer pickup moves to turn 3 while the first
fertilizer sale executes at turn 2, potentially selling the supply expected by
the route.

Reserve every planned input until its pickup completes, or schedule sales only
after all relevant pickups.

### 13. Terminal-day actions need explicit treatment

Day 29 executes only hours 0-22 and has no end-of-day inventory drop. Hiring,
buying seeds, animals, or land on that day cannot produce a later return and
directly reduces final money. The day feature lets a network potentially learn
to avoid this, but the macro action still permits deterministic terminal losses.

Add terminal feasibility masks for unrecoverable spending and, after DROP is
implemented, a dedicated final-day harvest-and-liquidate schedule.

## Policy feature gaps

The shared product encoder is a good inductive bias, but the current products are
not structurally identical under the supplied features. Add features for:

- seed or animal capital cost;
- ongoing versus one-time production;
- maximum banked yield;
- estimated maintenance labour per output unit;
- feed requirement;
- current banked harvest and harvestable value;
- time to next production;
- projected shed overflow;
- mandatory versus optional task counts;
- estimated route workload.

The hiring head in particular should see the workload the planner is likely to
generate. `PolicyObs` contains `t_day` and `t_yield`, but most of this information
is not currently summarized into the network features; it does not contain the
full survival and cadence state used by `build_day` either.

## Recommended target architecture

Preserve the current high-level split while strengthening the compiler:

```text
hour-0 state
    -> small learned macro policy
    -> exact provisioning and terminal-value checks
    -> value-aware task construction
    -> spatial assignment and deterministic routing
    -> optional return-to-shed/drop/sell phase
    -> static 24-turn arrays
```

The network still decides strategy once per day. Fixed machinery should enforce
engine semantics, resource feasibility, terminal feasibility, storage limits,
and route efficiency. Learned outputs should decide genuine trade-offs such as
what to produce, what to sell, expansion, cash reservation, scarce-input value,
and optional task priorities.

## Implementation priority

Suggested order, from low-risk deterministic fixes to broader action-space work:

1. Fix the one-time crop maturity gate.
2. Add terminal-day guards against unrecoverable spending.
3. Make product-buy budgeting price-walk and shed-capacity aware.
4. Reserve fertilizer and remove forced restocking.
5. Add capacity-aware harvest and fertilizer collection.
6. Improve feed, water, CARE, and harvest cadence.
7. Replace the score-sorted global route with locality-aware assignment.
8. Implement DROP in the simulator and add same-day harvest/sale routes.
9. Add schedule templates that allow selling before purchases.
10. Expand the macro only after the executor stops hiding or destroying useful
    strategic decisions.

## Validation and ablation plan

Do not judge the redesign only by self-play ladder win rate. Instrument the
simulator and record, per episode:

- requested versus actually purchased resources;
- no-op resource-dependent actions;
- walking, pickup-idle, working, and unused unit turns;
- mature yield left unharvested;
- end-of-day overflow by product and value;
- terminal unsold inventory and terminal spending;
- harvested units per harvest operation;
- collected fertilizer used, sold, overflowed, or left unsold;
- cash unavailable because sales occur after purchases.

For every material planner change:

1. run numpy/JAX backend agreement and engine equivalence;
2. train multiple seeds under equal rollout budgets;
3. evaluate on a fixed external suite, not only the moving self-play pool;
4. compare win rate, own coins, and the operational diagnostics above;
5. retain changes only when the gain survives held-out seeds and opponents.

Useful initial ablations are:

- season-tail fix only;
- exact provisioning only;
- cadence plus batching only;
- locality-aware routing only;
- capacity management only;
- DROP/same-day liquidation only;
- the combined redesigned executor.

## Documentation drift found during review

The project documents should be reconciled with the implementation:

- `Macro` currently has 14 fields, not 15.
- The current policy has 4,386 parameters, while `README.md` still says 3,892
  and `GOAL.md` describes an older 3,827-parameter architecture.
- `docs/DESIGN.md` says `MAX_HANDS = 16`; `spec.py` uses 10.
- Day 29 executes 23 turns, not all 24 compiled turns.
- Empty structures are not engine-irreversible: DIG can remove them. The current
  planner simply never schedules that operation.
- The training gradient objective is now shaped margin plus an absolute anchor,
  rather than the pure win-rate objective described in `GOAL.md`.
- `docs/DESIGN.md` says there are no hand-written strategy opponents, while
  `es/archetypes.py` supplies fixed strategy archetypes.

These discrepancies do not invalidate the simulator, but they make architectural
review and experiment comparison unnecessarily difficult.

## Bottom line

The once-daily deterministic compiler is the right architecture for the project
constraints. The current macro vocabulary, provisioning model, cadence rules,
storage handling, and routing executor impose a substantial structural ceiling.
Longer ES runs or a larger network will not remove that ceiling.

The highest-value changes are exact provisioning, correct season-tail behavior,
value- and locality-aware labour allocation, shed-capacity control, and same-day
DROP/SELL routing.
