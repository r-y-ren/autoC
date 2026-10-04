# `ROUTE_EARLY_ON` — why it costs −159k a board (code look, no legs)

2026-09-11T13:23Z. Read-only analysis of `src/kagg3/core/plan.py` @ `b906407` (branch
`fitness-shaping`), cross-checked against the judge worktree
`.claude/worktrees/arms-next/src/kagg3/core/plan.py` (identical line numbers for every switch
cited here). No engine games were run.

Verdict: **`ROUTE_EARLY_ON=True` is not a strategy read and not a crash — it is one turn-shift
applied twice.** The shipped tree runs `ROUTE_SPLIT_ON=True`
(`plan.py:2226`, worktree `:2226`), and `build_day` subtracts the *same* `early` vector once under
each switch. Every early unit therefore starts **two** turns before `route_base` instead of one,
which breaks the two hire/spawn laws the planner is built on.

---

## Mechanism

### 1. `_routes` returns one `early`; the caller applies it twice

`_routes` computes the per-unit early flag once. When both switches are passed, the
`ROUTE_SPLIT` branch **supersedes** `route_early` — the `route_early` argument is then never read:

* `plan.py:7037-7070` — `if route_early is None and route_split is None: early_u = 0` … `else:` the
  trial cut at `bud + 1`, then `if route_split is None:` (`:7054`, ROUTE_EARLY's rule) `else:`
  (`:7056-7069`, ROUTE_SPLIT's rule). With both on, only the `else` runs.
* `plan.py:6837-6838` (docstring) states it: *"`route_split` … supersedes `route_early` where both
  are on."*
* `early_u` is a 0/1 flag (`:7068 .astype(i32)`), accumulated at `:7525` and returned as one
  `[MU]` vector at `:7556`.

The caller then shifts the schedule **twice** with that one vector:

```
plan.py:6399    if ROUTE_EARLY_ON:
plan.py:6404        start_u = (start_u - early).astype(i32)
plan.py:6405        walk_u  = (walk_u  + early).astype(i32)
plan.py:6406    if ROUTE_SPLIT_ON:
plan.py:6412        start_u = (start_u - early).astype(i32)
plan.py:6413        walk_u  = (walk_u  + early).astype(i32)
```

Both blocks are guarded by *Python constants*, not by the day-level masks, so the second
subtraction fires on every day and every unit the ROUTE_SPLIT rule flagged — including days
`route_early`'s own gate (`:6066-6078`: `(~wide) & (land_lead == 0) & (route_base == O.ROUTE_BASE)`)
explicitly forbids, i.e. wide days. `start_u` is then `route_base + lead − 2`.

### 2. What the extra turn breaks — narrow day (the common case)

`route_base = O.ROUTE_BASE = 2` (`ops.py:217`), and a narrow early block has `lead = 0` by
construction (`route_split` requires `land_lead == 0` at `:6088` and `d_pick[e1] == 0` at `:7063`,
and `d_lead = max(d_pick, land_lead)` at `:7035`). So **`start_u = 0`**:

* The farmer (unit 0) emits its first route op **at turn 0**, i.e. it steps off its shed-access
  tile *before* turn 0's HIRE market phase. That is the one thing every base constant in the file
  is written to prevent: `ops.py:205-219` — *"`_spawn_hand` puts a new hand on the least occupied
  shed-access tile, so `plan.SPAWN_SLOT`'s 'hand h lands on access tile (h+1) % 4' only holds while
  every unit is still standing on its spawn tile when the hire resolves. One unit that walked …
  moves every later hand's spawn, **and a route laid out from the wrong start tile works the wrong
  tiles for the rest of the day**."* Same law restated at `ops.py:236-239` (`ROUTE_BASE_PACK`:
  *"Turn 0 stays idle for everyone whatever the packing"*) and at `plan.py:3356-3364` (`SPAWN_SLOT`).
  The planner's `SPAWN_X/SPAWN_Y` (`plan.py:3363-3364`) then describe nobody, and every hand's
  block — laid out from `sx, sy` at `:7031` — walks from the wrong tile all season.
* Every hand hired in turn 0 does not exist at turn 0 (`ops.py:205-208`: a hand hired in turn *t*
  first acts in *t+1*), so each hand's **first route op is silently dropped**, and the rest of its
  route is off by one step — every subsequent op targets a tile the unit is not standing on.

### 3. What it breaks — wide day

`route_base = 3`, and the wide branch requires `d_pick[e1] > 0` (`:7065`), so `lead ≥ 1` and
`start_u = 1 + lead`. But `pk_base` is shifted **once only** — the PICKUP rows are adjusted inside
the `ROUTE_SPLIT` block alone (`plan.py:6427-6441`, `pk_base = route_base - where(wide, early, 0)`),
and there is no `ROUTE_EARLY` counterpart. Route rows and pickup rows therefore desynchronise: the
pickup row at `pk_turn` (`:6443`) overwrites the route op sitting on that same turn
(`:6449-6452`, `unit_op = where(hit, O.OP_PICKUP, unit_op)`), so the block loses its opening op and
is one tile out for the rest of the day — on exactly the blocks that carry wheat, fertilizer and
animals.

### 4. Secondary: the admit stage double-credits the labour too

```
plan.py:6312    if ROUTE_EARLY_ON:  labour = labour + xp.where(route_early, n_units, 0)   (:6320)
plan.py:6321    if ROUTE_SPLIT_ON:  labour = labour + xp.where(route_split, n_units, 0)   (:6326)
```

Two turns per unit of admission credit for one turn of work. `ADMIT_ROUNDS` (`:6329`) repairs
over-admission only by dropping tiles, so this compounds the loss rather than causing it.

### 5. The evidence matches, and it is not the sibling asserts

* `S/topb/scr_route_early.log:5-7` — the screen ran in `.claude/worktrees/arms-next` with
  `'ROUTE_SPLIT_ON': True` printed in its own switch dump, i.e. the double shift was live.
* `S/topb/screen_summary.txt:22` — `ROUTE_EARLY_ON` −142,588, t −23.6, **0.0 %** of boards
  identical, 0 % wins; our seat finishes on 4,230-16,319 coins a game
  (`scr_route_early.log:8-25`) against a normal ~150k — the crew works the wrong tiles all season.
* This is a **different** failure from `PRESTOCK`/`MARKET_PACK`, whose screen lines are byte-for-byte
  identical to each other (−154,871, sd 25,389, t −27.00 both, `screen_summary.txt:15,18`) because
  `assert not (EARLY_SELL_ON and (MARKET_PACK_ON or PRESTOCK_ON))` (`plan.py:2478-2479`) raises at
  import and the seat idles on its 3,000 starting coins
  (`docs/strategy/2026-09-10-verdicts.txt:31`). `ROUTE_EARLY_ON` trips no assert: `:2481-2482` only
  forbids it beside `EARLY_SELL_MODE in ("Z","Z1")`, and the shipped mode is `"A"` (`:2466`).
* Why no test caught it: `tests/test_route_early.py:43-48` pins `ROUTE_SPLIT_ON` **off** in both
  fixtures on purpose (*"`ROUTE_SPLIT_ON` … supersedes this switch inside `_routes`, so the ON half
  below only has a subject with the newer switch out of the way"*, fixtures at `:53-54` and
  `:62-63`); `tests/test_route_split.py:52-53, 61-62, 139-140, 274-275` likewise never sets both on.
  **The both-on composition — the only one the shipped tree can produce — is untested.**

---

## Proposed fix (exact diff — NOT applied)

Two hunks, both in `build_day`. They make the caller obey what `_routes` already documents: one
`early` vector, applied once, under whichever rule produced it.

```diff
--- a/src/kagg3/core/plan.py
+++ b/src/kagg3/core/plan.py
@@ -6312,6 +6312,6 @@
-    if ROUTE_EARLY_ON:
-        # [SWITCH] The turn the early start buys, credited to the admit stage
-        # optimistically -- for every unit, on every day the flag allows any of
-        # them. Which units actually come out early is a property of the block
-        # cut and does not exist here; and of the two errors only one is
-        # repairable, since `ADMIT_ROUNDS` drops what the exact route cannot
-        # reach and nothing ever adds a tile back. Without this the new turn has
-        # nothing admitted to spend itself on.
-        labour = labour + xp.where(route_early, n_units, 0)
-    if ROUTE_SPLIT_ON:
-        # [SWITCH] The same optimistic credit `ROUTE_EARLY_ON` takes, for the
-        # same reason: which units come out early is a property of the block
-        # cut and does not exist here, and of the two errors only over-admission
-        # is repairable (`ADMIT_ROUNDS` drops what the exact route cannot
-        # reach; nothing ever adds a tile back).
-        labour = labour + xp.where(route_split, n_units, 0)
+    # [SWITCH] The turn the early start buys, credited to the admit stage
+    # optimistically -- for every unit, on every day the flag allows any of
+    # them. Which units actually come out early is a property of the block cut
+    # and does not exist here; of the two errors only over-admission is
+    # repairable (`ADMIT_ROUNDS` drops what the exact route cannot reach;
+    # nothing ever adds a tile back). ONE credit, from whichever switch owns
+    # the turn: `_routes` reads `route_split` and ignores `route_early` where
+    # both are on (:6837, :7056-7069), so crediting both would buy two turns
+    # of admission for one turn of work.
+    if ROUTE_SPLIT_ON:
+        labour = labour + xp.where(route_split, n_units, 0)
+    elif ROUTE_EARLY_ON:
+        labour = labour + xp.where(route_early, n_units, 0)
@@ -6399,15 +6399,13 @@
-    if ROUTE_EARLY_ON:
-        # [SWITCH] One turn earlier and one turn longer, for the units
-        # `_routes` found nothing in the BUY row to wait for. `lead` is 0 for
-        # every one of them by construction (no pickup, and the flag is off on
-        # a land day), so this is the whole of the per-unit start.
-        start_u = (start_u - early).astype(i32)
-        walk_u = (walk_u + early).astype(i32)
-    if ROUTE_SPLIT_ON:
-        # [SWITCH] One turn earlier and one turn longer, for the units
-        # `_routes` found a turn for -- a narrow-day block the BUY row does not
-        # feed, or a wide-day block whose first turn is a stationary PICKUP.
-        # `lead` already holds the pickup turns, so this shifts the whole
-        # schedule and the pickup rows below go with it.
-        start_u = (start_u - early).astype(i32)
-        walk_u = (walk_u + early).astype(i32)
+    if ROUTE_EARLY_ON or ROUTE_SPLIT_ON:
+        # [SWITCH] One turn earlier and one turn longer, for the units
+        # `_routes` found a turn for -- a narrow-day block the BUY row does not
+        # feed, or (ROUTE_SPLIT) a wide-day block whose first turn is a
+        # stationary PICKUP. `early` is ONE vector however many of the two
+        # switches are on: `_routes` computes it under ROUTE_SPLIT's rule and
+        # ignores `route_early` where both are (:6837, :7056-7069). Applied
+        # twice it puts the crew a turn before `O.ROUTE_BASE` -- turn 0 on a
+        # narrow day -- which re-scatters every hand `_spawn_hand` places
+        # [LAW, ops.ROUTE_BASE, ops.ROUTE_BASE_WIDE] and desynchronises the
+        # pickup rows below, which shift once (`pk_base`) whatever happens here.
+        start_u = (start_u - early).astype(i32)
+        walk_u = (walk_u + early).astype(i32)
```

**Do not add a module-level `assert not (ROUTE_EARLY_ON and ROUTE_SPLIT_ON)`.** It is tempting and
it is the trap that produced the two other void lines: an import-time assert turns a screen rung
into a silently idle agent (`plan.py:2478` → `2026-09-10-verdicts.txt:31`, our seat on exactly
3,000 coins for 40 games, recorded as a −154,871 "read"). With the diff above the combination is
merely **inert** — `ROUTE_EARLY_ON` becomes a no-op whenever `ROUTE_SPLIT_ON` is on, which is what
`_routes` has always meant — and nothing crashes.

### Is the intended behaviour recoverable? Yes, but it is not worth a lever

The fix restores correctness, not an opportunity. `ROUTE_SPLIT_ON` **is** the repaired, promoted
version of exactly this idea: same trial cut, wider gate (`plan.py:2161-2199`), and it is pinned to
fire on *strictly more* boards than `ROUTE_EARLY_ON` (`tests/test_route_split.py:266`), with a real
paired engine read behind it (+1,896 and +3,393 coins/game over two 384-game seed bases,
`plan.py:2207-2216`). `ROUTE_EARLY_ON`'s own smoke was 6 simulator seasons with no margin in it
(`plan.py:2137-2150`). After the fix, running `ROUTE_EARLY_ON=True` on the shipped tree changes
nothing; running it as a lever would require `ROUTE_SPLIT_ON=False`, i.e. trading a promoted switch
for its own weaker ancestor. **Fix the code, close the lever.**

---

## Risk to `PRESTOCK_ON` and `MARKET_PACK_ON`

**The double-application class does not reach them.** Both move `route_base` itself — the single
scalar the whole day's schedule derives from (`turn_budget` `:6280`, `land_lead` `:6064`, `pk_base`
`:6428`) — rather than adding a second delta on top:

* `PRESTOCK`: `plan.py:6002-6014` sets `route_base` to `O.ROUTE_BASE_PRE`/`ROUTE_BASE_WIDE_PRE`
  (`ops.py:226-227`) on a buy-row-empty day.
* `MARKET_PACK`: `plan.py:6026-6031` sets it to `O.ROUTE_BASE_PACK` (`ops.py:239`).

And both **switch `route_split` off by construction** on the days they fire: the `route_split` gate
requires `route_base == where(wide, O.ROUTE_BASE_WIDE, O.ROUTE_BASE)` (`plan.py:6088-6090`), which
is false once either switch has moved the base — stated in as many words at `plan.py:6029-6031`
(*"`route_base` moving off the law's own value is what switches `route_split` off below, which is
the rule that keeps turn 0 idle for everyone"*). `route_early`'s gate (`:6077-6078`) has the same
clause. So no second shift, and no turn-0 step.

**They have a different blocker, and it will void the queued P3 re-screen unless it is handled.**
Clearing `EARLY_SELL_ON=False` gets them past the import assert at `:2478`, but they then hit
*trace-time* asserts inside `_market`:

```
plan.py:7625    if pump is not None:
plan.py:7631        assert pack is None, "OPEN_PUMP owns turn 1; MARKET_PACK empties it"
plan.py:7632        assert hire_wide_early is None, \
plan.py:7633            "OPEN_PUMP owns turn 1; PRESTOCK's overflow hire row takes it"
```

`pump` is not `None` whenever `OPEN_PUMP_ON` is on — it is set unconditionally at
`plan.py:6745-6749`, zero-valued on days the pump declines but never `None` — and
`hire_wide_early` is `buy_row_empty if PRESTOCK_ON else None` (`:6753`), likewise not `None` on
days the row is not empty. The shipped tree runs `OPEN_PUMP_ON = True` (`plan.py:1173`, worktree
`:1173`) and the TOPB harness passes it explicitly (`S/topb/screen2.sh:4`,
`PAIR="OPEN_PUMP_ON=True,…"`). **`PRESTOCK_ON=True` or `MARKET_PACK_ON=True` beside the shipped
pump raises on day 0 and reproduces the exact 3,000-coin idle line again.** The plan recorded at
`docs/strategy/2026-09-11-lever-ranking.md:130-135` ("B + `EARLY_SELL_ON=False`, then
+ `PRESTOCK_ON=True`") is therefore incomplete as written: it also needs `OPEN_PUMP_ON=False`.

Second-order confound, not a bug: on the days `PRESTOCK`/`MARKET_PACK` fire they hand back
`ROUTE_SPLIT`'s promoted turn (the gate above), so a rung that flips them measures
`switch − ROUTE_SPLIT-on-those-days`. Price it, do not "fix" it — the base really is the law there.

---

## Recommended measurement (≤ 1 h)

1. **Zero games, minutes — the falsifier for this report.** Add one case to
   `tests/test_route_early.py` (whose fixtures at `:53-54`/`:62-63` currently pin `ROUTE_SPLIT_ON`
   off): with `ROUTE_SPLIT_ON=True`, the day rows under `ROUTE_EARLY_ON=True` must be **byte-identical**
   to `ROUTE_EARLY_ON=False`. It fails today (`start_u` two turns early, `start_u = 0` on a narrow
   day) and passes with the diff above. Assert on `start_u`/`unit_op` directly rather than on coins.
2. **Do not spend engine legs on `ROUTE_EARLY_ON`** — after the fix it is inert on the shipped tree
   and strictly dominated by `ROUTE_SPLIT_ON` off it (`tests/test_route_split.py:266`).
3. **Spend the hour on the P3 family instead, in the only legal composition** — TOPB2's 20 boards
   × 2 seats = 40 games a rung, ~80 s a rung at `WORKERS=8` (`S/topb/scr_route_early.log:8`,
   "40 games in 78s"), so three rungs cost ~5 min of the hour and leave room for the hold-out:
   * rung 0 (baseline): B theta, `EARLY_SELL_ON=False,OPEN_PUMP_ON=False` + the rest of `PAIR`
   * rung 1: rung 0 `+ PRESTOCK_ON=True`
   * rung 2: rung 0 `+ MARKET_PACK_ON=True`
   Judge each against **rung 0**, not against shipped B — the pump and the early sell are both out,
   so a comparison to B measures those two, not the switch. Winner (if any) then goes to the
   LIVE-C 73-102 hold-out (30 boards) inside the same hour.
4. **Add a void detector to the screen harness** (`S/topb/run.sh` / `screen*.sh`): fail the line
   when our seat's mean coins are below ~5,000 instead of printing a margin. That one check would
   have labelled all three of the 2026-09-10 void lines (`screen_summary.txt:15,18,22`) as crashes
   rather than recording two of them as −154,871 "reads" and one as a −142,588 strategy verdict.
