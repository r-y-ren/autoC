"""Kaggriculture submission agent -- "rotation ranch" strategy (r3, v4).

Self-contained: standard library only, no imports from the local kgenv
package, so the file uploads as-is to
    kaggle competitions submit kaggriculture -f main.py
and lives at /kaggle_simulations/agent/main.py (official kit convention).
The last callable defined in this file is the entry point (that is how
kaggle_environments picks the agent from a file).

r3 timing redesign (campaign III round 3, sub-wave r3-2).  The round-2
online replays (3 winners, 6 episodes, .tmp-online/round2/) crossed with
the m1 top-20 corpus (58 episodes / 116 seat profiles) pinned the OPENING
AND MID-GAME TIMING as the next-tier ticket, not the ranch structure the
m3 engine already had (deep dive: exports/online/round2_winner_deep_dive.md).
Four phase changes, each with >=3-game profile evidence:

  R3-1 d0 capital allocation: 116/116 top-20 seats and 3/3 round-2 winners
      put 1800-2200 of the 3000 start into 4-5 head ON DAY 0 (2C+2S here,
      1800; arminhej96 5C/2000, 朝闻夕死 + Danila 3C+2S/2200), seeds from
      the leftovers.  First milk lands d8-9 instead of d10+ (measured m3:
      1 sheep on d0, first milk d10, d12 money ~0.4k vs winner band 1.5-8k).
  R3-2 herd deadline: >=12 head by d11 with a 14 ceiling (8C+6S -- winners
      peak 13-17; top-20 med 12 / p75 15).  The m3 plan (11 head, done
      d13-15) never reached 12 at all.  Counter-example checked: Anthaus
      hit 18 head but built d10-12 and lost -- timing, not size, is the
      ticket, so the cap stays 14 and the deadline does the work.
  R3-3 strawberry cadence: plant from day 5 (not day 0 -- the d0 cash
      belongs to the herd burst), 15-20 tiles by d11-13 (cap 6/quad on 3
      quadrants = 18; winners 16-23; top-20 peak med 36 starves the
      feed/care labour budget, so ~20 is the ceiling, not the target).
  R3-4 crew 12: winners hold 12 hands from d7-11 (Danila crew 12 @ d7;
      top-20 9.4-9.9 hires/day).  The m3 ramp peaked at 10.  _crew_target
      follows the herd (CARE/FEED/COLLECT_FERTILIZER scale with head):
      12 once the herd plan is >=12, the pinned m3 ramp as the floor.
      CARE discipline is unchanged full coverage (issue = head/day, no
      oversending -- CARE on a cared animal is an engine no-op).
  Kept from the winners' table deliberately: feed guardrail (gap-fill at
      <=36, ~15u/day cadence; winners 102-462u @ 33-34), 3 quadrants (NE
      d4 / SW d7 -- the m3 plan already sits inside the winner d5-11 band),
      d28+ stop-feed/stop-plant liquidation, milk clear-through gate 105
      and wool gate 150 (the milk/wool hoard-split is a low-confidence
      style item -- 3 winners, 3 different splits -- and the m2
      clear-through discipline measurably dominates the joint-dairy meta),
      daily fertilizer collection sold promptly (61-85 realised; winners
      9.8-18.5k/season -- an income line the m2 engine left on the table).

Online-feedback redesign (campaign III m3).  The m2b dairy engine won the
legacy pool 31W-1L but dropped the m2 online-style pool (dev eval seed 101:
template_wheat 0-2, self_feed_ranch 0-2, crop_rotator 1-1; evidence
exports/eval_results.dev.json).  The m1 replay profiles of 60 official
episodes (120 seat profiles, exports/replay_profiles/, captured 2026-08-29)
pin four structural gaps, addressed as FM-O1..O4:

  FM-O1 (crop revenue share 21% vs top-20 median 54%) -> the field engine
      is a PRICE-KEYED ROTATION over wheat/strawberry/melon/carrot.
      Every non-wheat tile decision is gated by a live price floor
      (CROP_FLOOR) and a calendar phase (CROP_PHASE) copied from the
      ladder #1 "Crop Dusta" frame (26 consistent games: melon early /
      strawberry days 0-14 / filler afterwards; each with a price trigger).
      Wheat is no longer the whole field: it is the crash-proof FEED FLOOR
      (log glut curve -- it cannot be strategically crashed) sized by
      _wheat_cap, and everything the floor does not need goes to the
      highest-priced rotation crop that passes its floor.  Wheat itself
      joins the rotation as a money crop at 30+ (the rank-1 adaptive
      ladder runs a 0.45-0.62 wheat share at 36-42+; measured: the
      volume-farming archetypes monetize 400-520u/season).
  FM-O2 (labour 4.07 hires/day vs top-20 median 9.4, leader 9.7-9.9;
      herd all-cow vs the ladder's mixed ranches) -> labour plan ramps to
      10 hands/day (top-20 100/101 games sit at 9.1-10.2; a flat crew
      from day 1 measured BETTER than the rank-1's quadrant-scaled crew
      because our rotation opening needs tending before quadrant two
      exists), the herd becomes a SMALL MIXED RANCH with sheep primary
      (6 sheep + 5 cows = 11 -- between Milan's 6c+6s and Crop Dusta's
      7c+4s+1g; a 12-head plan measurably crowded out tending and the
      day-8 cash floor), bought INTERLEAVED by relative deficit so cows
      reach the day-8+ premium-milk window on time; the quadrant plan
      buys the third quadrant (NE day 4+, SW day 7+ -- the leader's land
      series; top-20 consensus 3 quadrants, 4th almost nobody) with the
      purchase fund protected from herd buys while it is pending.
  FM-O3 (feed autarky burned half the field on wheat the ladder buys
      externally: top-20 feed purchases 414-2732u/season at avg 26-32) ->
      wheat is a floor, not the field; the herd's gap is filled by
      GUARDRAILED external buying (FEED_BUY_MAX_PRICE, starvation cap 85
      preserved) and the m2 autarky bound on the herd target is released
      (money gate + pace + HERD_CAP bound it instead).  The wheat surplus
      sells from WHEAT_SELL_GATE with a cash-flow fallback -- the gate
      must never starve the land/animal capex plan (measured: 42 wheat
      hoarded at $516 while the NE purchase window lapsed).
  FM-O4 (endgame gain +7.2% of final money vs top-20 median +13.0%) -> a
      48h endgame window: from day 26 wool and from ENDGAME_DAY (28) every
      other premium hoard dumps in per-turn tranches (banking at the
      recovered price beats the day-29 joint liquidation floor), and
      FEEDING STOPS for animals that can no longer repay their wheat
      (unfed animals still produce their base unit; only the care bonus
      needs feed -- measured engine rule), freeing both the wheat (sold)
      and the labour (dump logistics).

  RED LINE (dead-price curves, generalized from the m2b demand-drought
  freeze): production never scales into a dead price.  Sheep buys freeze
  when WOOL < 90, cow buys when MILK < 90 (the m2b rule), and each
  rotation crop's planting freezes under its CROP_FLOOR.  The hoard side
  of the same red line: wool follows its curve (sq glut, T=105 -- the
  fastest crasher) and CUTS LOSSES at WOOL_CUT_LOSS once the curve turns
  (no yarn-store draws), never riding a dead curve into the day-29 floor;
  fertilizer sacks bid 70+ are SOLD rather than spent on wheat/carrot
  boosts worth ~60-70 (only the ~200-230/unit strawberry/melon boosts
  keep the sack -- the self-feed archetype sells 158u for +12.8k).

m2b fixes preserved (tests/test_strategy_m2.py, 26 checks, must not
regress):
  FM-1 ring pastures / feed-pipeline-first  -> kept; herd composition is
      new but pastures still hug the shed ring in every unlocked quadrant.
  FM-2 glut-tolerance discipline -> melon/strawberry return UNDER price
      floors + phase windows + small tranches; wheat stays the feed floor.
  FM-3 capital staging -> wheat-first opening kept (day-0 wheat before any
      animal), money-gated buys with cash reserves; rotation seeds are
      additionally staged behind the pending land fund.
  FM-4 fertilizer -> generalized: animal fertilizer self-consumes on the
      premium rotation crops (strawberry before each production day,
      melon at age 2; wheat/carrot only when the sack is cheap), bounded
      hoard (FERT_STOCK_CAP), gated release.
  Behavioural fixes kept verbatim: last day is liquidation-only (no
      capex, carried goods returned and sold first, infeasible harvests
      skipped); animal purchases confirmed by observed herd deltas
      (_buy_pace/_note_buy_order, per-seat per-episode state); shed
      inventory reserved across carriers; every quantity order positive;
      dawn hire burst within hour <= 2.

Selective-intervention sell gates (decide explicitly WHEN to hoard, WHEN
to release, WHEN to defend -- see _market_gates; every rule commented with
its official MARKET_PARAMS curve rationale).

An OPTIONAL pluggable LLM consultant hook (LLM_PROVIDER, default None) is
provided for local A/B experiments only (scripts/run_llm_ab.py); disabled
by default, never blocks, falls back to the heuristic gate.
"""

# --------------------------------------------------------------------------
# Embedded game constants (mirror of kaggle-environments 1.32.7 kaggriculture)
# --------------------------------------------------------------------------
CROPS = {
    "WHEAT":      {"seed": 10, "first_yield_day": 2, "max_yield_day": 4, "interval": 0, "max_yield": 6, "ongoing": False},
    "CARROT":     {"seed": 20, "first_yield_day": 2, "max_yield_day": 3, "interval": 0, "max_yield": 4, "ongoing": False},
    "TOMATO":     {"seed": 50, "first_yield_day": 8, "max_yield_day": 8, "interval": 1, "max_yield": 4, "ongoing": True},
    "STRAWBERRY": {"seed": 100, "first_yield_day": 10, "max_yield_day": 10, "interval": 2, "max_yield": 4, "ongoing": True},
    "MELON":      {"seed": 80, "first_yield_day": 10, "max_yield_day": 12, "interval": 0, "max_yield": 6, "ongoing": False},
}
ANIMALS = {
    "GOOSE": {"cost": 300, "structure": "COOP", "first_yield_day": 4, "interval": 1, "max_held": 4, "product": "EGG"},
    "COW":   {"cost": 400, "structure": "PASTURE", "first_yield_day": 8, "interval": 2, "max_held": 6, "product": "MILK"},
    "SHEEP": {"cost": 500, "structure": "PASTURE", "first_yield_day": 6, "interval": 3, "max_held": 6, "product": "WOOL"},
}
BASE_PRICE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
              "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}

MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
SEASON_DAYS = 30

# ---- strategy knobs (every value carries its evidence in the comment;
# tuning changes are logged in exports/logs/iteration_gate_log.jsonl) ----

# FM-O2 labour: top-20 median 9.4 hires/day (282-295/season), leader 9.7-9.9
# (Crop Dusta land/labour series); 24 turns/day per unit, fib cost per day.
# R3-4: _crew_target tops this ramp up to HANDS_CAP_R3 following the herd
# (round-2 winners hold 12 hands from d7-11; top-20 9.4-9.9/day).
HANDS_RAMP = ((0, 5), (1, 6), (3, 8), (6, 9), (12, 10))
HANDS_CAP_R3 = 12        # r3: crew 12 once the herd plan reaches 12 head
HIRE_BURST = 5           # HIRE orders per dawn turn (burst, m2b fix)
HIRE_HOUR_MAX = 2        # dawn window (m2b fix: burst must fit hour <= 2)

# FM-O2 land: leader NE day 4+ / SW day 7+; top-20 3-quadrant consensus
# (100/101 seats); the 4th quadrant is almost never bought (skip SE).
# LAND_PLAN[quads_now] = (due_day, protected_fund); fund = price + reserve.
LAND_PLAN = {1: (4, 1700), 2: (7, 2700)}
LAND_PEND_WINDOW = 4     # herd unblocks if land is this many days overdue

# R3-1/R3-2 herd: the r3 opening.  Day 0 buys the mixed burst below outright
# (1800 of the 3000 start; 116/116 top-20 seats hold 4-5 head on d0, 3/3
# round-2 winners; the m3 engine's 1-sheep d0 is the fork the round-2
# losses traced to).  Ceiling 14 = 8C+6S (winners peak 13-17; top-20 med
# 12 / p75 15); with the 4+day target ramp the 12-head deadline lands
# d8-9 (< d11).  Cows interleave in early so they reach the day-8+
# premium-milk window on time; goose dropped (egg log-curve pays ~2.1k
# vs a cow's ~5k in the observed premium-milk meta).
OPENING_HERD = {"COW": 2, "SHEEP": 2}
OPENING_RESERVE = 800    # cash kept besides the day-0 burst (m2b cushion)
HERD_CAP = 14            # total herd ceiling; m2b tests pin _herd_target
                         # to the constant, not a literal
HERD_COMPOSITION = {"SHEEP": 6, "COW": 8, "GOOSE": 0}
ANIMAL_BUY_LAST_DAY = {"SHEEP": 20, "COW": 20, "GOOSE": 24}
COW_BUY_RESERVE = 380    # cash kept besides an animal purchase (m2b)
ANIMAL_PACE = ((8, 3), (4, 2))   # head/day from day: 1 before day 4, 2 to 7, 3 after
PASTURE_RING = 2         # structures within manhattan dist <= 2 of shed access

# RED LINE dead-price freeze (generalized m2b demand-drought rule): no
# species scale-up when ITS product curve is dead (milk-crash leader does
# not expand cows -> applied per species/crop by glut shape).
DEAD_PRICE_FLOOR = {"MILK": 90, "WOOL": 90, "EGG": 30}
DEAD_PRICE_FROM_DAY = 10  # m2b gate: freezes apply once curves can be read

# FM-O1 rotation: phase windows from the rank-1 frame (melon early /
# strawberry mid / late filler), price floors from the m2 online-pool
# archetypes (crop_rotator min_price 55/150, carrot base 35 minus margin).
# R3-3: strawberry phase opens day 5 (the d0-4 cash belongs to the herd
# burst; winners plant d7-11 and top-20 d4-7) and the per-quad cap rises
# to 6 (3 quads = 18 tiles by d11-13; winners 16-23, top-20 peak med 36
# starves the feed/care labour budget -- do not chase it).
FERT_VALUE_GATE = 70     # fert sack sold at 70+ beats a wheat/carrot boost
                         # (~60-70/unit); strawberry/melon boosts (~200-230)
                         # are always worth the sack (self_feed ledger: they
                         # never fertilize and sold 158u for +12.8k)
WHEAT_MONEY_GATE = 30   # wheat joins the rotation as a money crop at 30+
WHEAT_MONEY_CAP_PER_QUAD = 3
CROP_PHASE = {"MELON": (0, 17), "STRAWBERRY": (5, 14), "CARROT": (15, 26)}
CROP_FLOOR = {"MELON": 150, "STRAWBERRY": 55, "CARROT": 28}
CROP_CAP_PER_QUAD = {"MELON": 3, "STRAWBERRY": 6, "CARROT": 4}
PLANT_LAST_DAY = {"WHEAT": 24, "CARROT": 26, "MELON": 17, "STRAWBERRY": 14}

# FM-O3 feed: guardrailed external buying (profiles: avg buy price 26-32,
# 414-2732u/season across top-20); 85 = starvation cap (dear wheat is still
# cheaper than a lost animal -- m2b).
FEED_BUY_MAX_PRICE = 36
WHEAT_FEED_RESERVE = 8   # feed days kept before selling wheat (measured: a
                         # 4-day buffer forced sell-at-33 / rebuy-at-37 churn)
WHEAT_SELL_GATE = 26     # log glut curve; hold for a real bid, but never
                         # starve capex (money-fallback below)

# FM-4 fertilizer (m2b, generalized to rotation crops)
FERT_GATE = 50           # fertilizer: hold below, release above
FERT_STOCK_CAP = 6       # hoard bound: shed slots belong to the products
FERT_FIELD_RESERVE = 4   # keep some fertilizer for the fields

# FM-O4 endgame 48h window (top-20 median endgame gain +13.0% of final)
ENDGAME_DAY = 28         # dump tranches + stop feeding from here

# premium sell gates / tranches (curve shapes: wool/melon sq, milk/straw
# linear, wheat/egg log -- tranche size inversely follows crash speed)
WOOL_GATE = 150
WOOL_HOARD_FLOOR = 8
WOOL_HOARD_CAP = 34
WOOL_CUT_LOSS = 45      # curve dying (no yarn store drawn): realize fast
STRAWBERRY_GATE = 105
STRAWBERRY_HOARD_FLOOR = 8
MELON_GATE = 180
MELON_HOARD_FLOOR = 4
CARROT_GATE = 28
CARROT_HOARD_FLOOR = 6
EGG_GATE = 40
EGG_HOARD_FLOOR = 4

LLM_PROVIDER = None      # optional consultant, default off; local A/B only

# Module-level state keyed by player id (the framework may exec one copy of
# this file for both seats in self-play validation episodes).  Tracks the
# per-day animal purchase pace by confirming actual herd-count changes in
# the next observation; orders themselves never consume pace.
_STATE = {}


def _buy_pace(player, day, hour, herd_total):
    """Return confirmed animal purchases for this day.

    A BUY_ANIMAL order is only a request.  The market may reject it for lack
    of cash or shed capacity, so pace is advanced only by a positive
    herd-count delta observed on a later turn.  A backwards clock denotes a
    new episode.
    """
    st = _STATE.get(player)
    if st is None or st["day"] != day or hour <= st.get("hour", -1):
        _STATE[player] = {"day": day, "hour": hour,
                          "last_herd": herd_total, "confirmed": 0,
                          "pending": 0}
        return 0
    delta = max(0, int(herd_total) - int(st.get("last_herd", herd_total)))
    if delta:
        st["confirmed"] = st.get("confirmed", 0) + delta
        st["pending"] = max(0, st.get("pending", 0) - delta)
    st["hour"] = hour
    st["last_herd"] = herd_total
    return st.get("confirmed", 0)


def _note_buy_order(player, day, hour, n):
    """Record an unconfirmed request without consuming the daily pace."""
    st = _STATE.get(player)
    if st is None or st["day"] != day or hour < st.get("hour", -1):
        st = {"day": day, "hour": hour, "last_herd": 0,
              "confirmed": 0, "pending": 0}
        _STATE[player] = st
    st["hour"] = hour
    st["pending"] = st.get("pending", 0) + max(0, int(n))


def _note_buys(player, day, hour, n):
    """Compatibility shim for callers from the pre-confirmation strategy."""
    _note_buy_order(player, day, hour, n)


def _get(obj, key, default):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _dist(ax, ay, bx, by):
    return abs(ax - bx) + abs(ay - by)


def _step_towards(fx, fy, tx, ty):
    dx, dy = tx - fx, ty - fy
    if dx == 0 and dy == 0:
        return ["PASS"]
    if abs(dx) >= abs(dy) and dx != 0:
        return ["EAST"] if dx > 0 else ["WEST"]
    return ["SOUTH"] if dy > 0 else ["NORTH"]


def _shed_access(board_size):
    half = board_size // 2
    return ((half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half))


def _shed_adjacent(x, y, board_size):
    return (x, y) in _shed_access(board_size)


def _quadrant_shed_tile(x, y, board_size):
    """The shed-access tile of the quadrant (x, y) sits in."""
    half = board_size // 2
    qx = half - 1 if x < half else half
    qy = half - 1 if y < half else half
    return (qx, qy)


def _quadrant_of(x, y, board_size):
    half = board_size // 2
    return ("N" if y < half else "S") + ("W" if x < half else "E")


def _window(crop):
    cd = CROPS[crop]
    return (cd["max_yield_day"] + 1) // 2, cd["max_yield_day"]


def _hire_cost(n_already_today):
    """Engine fib schedule: 1, 1, 2, 3, 5, 8, ... for the (n+1)-th hire."""
    a, b = 1, 1
    for _ in range(max(0, n_already_today)):
        a, b = b, a + b
    return a


def _wheat_cap(day, wheat_price=25):
    """Wheat FEED-FLOOR size (m2b base values, test-pinned at 25/40): 16
    tiles fund the opening, 18 the full herd (18 fertilized tiles =
    21.6 wheat/day vs 10 animals eating 10).  Dear-wheat bands follow the
    rank-1 adaptive share (crop_rotator ladder 0.32/0.45/0.62 of a 3-quad
    field at 30/36/42 coins -- measured seed-102 economy: five wheat shops,
    wheat 33-45 all season, log curve = no crash risk): at 42+ wheat IS
    the money crop.  With FM-O3 the floor never has to cover the whole
    field: rotation crops take the remaining tiles.
    """
    cap = 16 if day <= 2 else 18
    if day > 2 and wheat_price >= 42:
        cap += 12
    elif day > 2 and wheat_price >= 35:
        cap += 4          # dear wheat: farm more of it (feed margin + cash)
    return min(cap, 30)


def _herd_target(day, feed_capacity):
    """Total-animal plan (m2b formula shape, test-pinned at d0/d8/d25):
    4 head on day 0 (the r3 opening burst), the build accelerates from
    day 5 so the 12-head deadline lands by d6-8 and the 14 ceiling by d8
    (R3-2: winners 13-17 by d8-11; top-20 med 12 by d6; the m3 plan never
    reached 12).  Feed capacity caps it as in m2b, though in r3 the
    autarky bound is normally slack (FM-O3 guardrailed external feed
    covers the gap) -- the money gate + daily pace + composition do the
    real limiting.
    """
    return min(HERD_CAP, 4 + day + max(0, day - 4), max(4, feed_capacity))


def _hands_target(day, herd, wheat_tiles, quads=3):
    """Labour plan (FM-O2): top-20 median 9.4 hires/day, leader 9.7-9.9
    (Crop Dusta labour series; our m2 engine ran 4.07 and lost the labour
    race -- fields went untended and weeded at 5 units).  Flat ramp to 10
    by day 12.  (A quadrant-scaled plan was measured WORSE: our rotation
    opening needs the full crew before the second quadrant exists.)
    """
    target = 2
    for from_day, hands in HANDS_RAMP:
        if day >= from_day:
            target = hands
    return max(2, min(target, 10))


def _crew_target(day, herd, wheat_tiles, quads=3):
    """R3-4 crew plan: the m3 ramp above stays the FLOOR, and the crew
    follows the herd up to HANDS_CAP_R3 once the ranch plan needs it
    (round-2 winners hold 12 hands from d7-11 while milking 13-17 head;
    CARE + FEED + COLLECT_FERTILIZER all scale with head count).  A bad
    season (small herd) never overhires: the ramp alone is the target.
    """
    return min(HANDS_CAP_R3, max(_hands_target(day, herd, wheat_tiles, quads),
                                 herd))


def _animal_pace(day):
    """Confirmed-purchase pace: 1/day through the capital-heavy opening,
    2/day while the herds ramp, 3/day later (m2b shape)."""
    for from_day, pace in ANIMAL_PACE:
        if day >= from_day:
            return pace
    return 1


def _milk_gate(day):
    """Milk hold-threshold by day (selective intervention, see _market_gates).

    Base 105: in a joint-dairy market (both players milking ~20+/day vs
    town consumption of ~5/day, measured mirror prices 97-135) holding for
    higher bands just deferred sales into eventual pressure dumps (measured
    realized ~60/unit).  Clearing daily at >= 105 dominates.  Decay
    late-season: the day-29 liquidation floor is coming for everyone, so
    clearing inventory at a lower-but-positive gate beats holding into the
    joint dump.
    """
    if day >= 28:
        return 80
    if day >= 26:
        return 90
    if day >= 24:
        return 100
    return 105


def _llm_sell_gate(item, price, base_gate, context):
    """Optional LLM consultation for premium sell timing; default heuristic.

    The provider (if any) must answer with {"gate": int}. Any failure or
    absurd answer falls back to the heuristic gate. Never blocks the turn:
    providers are expected to enforce their own call budget/timeout
    (Reasonableness Standard).
    """
    if LLM_PROVIDER is None:
        return base_gate
    try:
        ans = LLM_PROVIDER.suggest(
            f"Item {item} trades at {price} (base {BASE_PRICE[item]}). "
            f"Return the minimum price we should accept for selling into a "
            f"glut-crashing market, as JSON {{\"gate\": int}}.", context)
        gate = int(_get(ans or {}, "gate", base_gate))
        if 1 <= gate <= BASE_PRICE[item] * 2:
            return gate
    except Exception:
        pass
    return base_gate


def _field_alloc(farm, day, prices):
    """Deterministic structure + rotation plan (FM-O1/FM-O2).

    Structures: pastures (and one coop) on the manhattan ring
    (dist <= PASTURE_RING) around the shed-access tile of every unlocked
    quadrant, built at most 2 ahead of the herd plan (m2b FM-1).

    Field: money crops claim the empties nearest the shed while their
    (phase, price floor, cap) gates are open -- each gate is the red-line
    freeze for that crop; wheat fills the rest up to the _wheat_cap feed
    floor; surplus tiles stay fallow (labour is the binding resource).

    Returns (builds, crop_map, n_animals, wheat_capacity) where
      builds: {(x, y): "PASTURE"|"COOP"} to build,
      crop_map: {crop: set(positions)} planned tiles (alive + to-plant),
      n_animals: animals currently placed,
      wheat_capacity: wheat tiles * 1.2 (fertilized units/day).
    """
    tiles = _get(farm, "tiles", [])
    board = len(tiles)
    quads = _get(farm, "unlocked_quadrants", ["NW"]) or ["NW"]

    existing = {crop: set() for crop in CROPS}
    n_animals = 0
    n_pasture = 0
    n_coop = 0
    empty_ring, empty_field = [], []
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile == "LOCKED":
                continue
            pos = (x, y)
            if tile is None:
                if _quadrant_of(x, y, board) in quads and \
                        any(_dist(x, y, qx, qy) <= PASTURE_RING
                            for qx, qy in _shed_access(board)) and \
                        not _shed_adjacent(x, y, board):
                    empty_ring.append(pos)
                elif _quadrant_of(x, y, board) in quads:
                    empty_field.append(pos)
                continue
            if not isinstance(tile, dict):
                continue
            kind = _get(tile, "kind", "")
            if kind == "WEED":
                continue
            if kind == "PASTURE":
                n_pasture += 1
                if "animal" in tile:
                    n_animals += 1
                continue
            if kind == "COOP":
                n_coop += 1
                if "animal" in tile:
                    n_animals += 1
                continue
            if kind == "PLANT":
                crop = _get(tile, "crop", "WHEAT")
                if crop in existing:
                    existing[crop].add(pos)

    empty_ring.sort(key=lambda p: (min(_dist(p[0], p[1], *q) for q in _shed_access(board)), p[1], p[0]))
    builds = {}
    field_extra = []
    herd_t = _herd_target(day, 99)
    pasture_want = min(HERD_CAP + 1, herd_t + 2)
    for pos in empty_ring:
        if n_coop < min(HERD_COMPOSITION["GOOSE"], herd_t) and \
                n_coop + n_pasture < pasture_want + 1:
            builds[pos] = "COOP"
            n_coop += 1
        elif n_pasture < pasture_want:
            builds[pos] = "PASTURE"
            n_pasture += 1
        else:
            field_extra.append(pos)

    empties = field_extra + empty_field
    empties.sort(key=lambda p: (min(_dist(p[0], p[1], *q) for q in _shed_access(board)), p[1], p[0]))
    crop_map = {crop: set(existing[crop]) for crop in CROPS}
    for crop in ("STRAWBERRY", "MELON", "CARROT"):
        lo, hi = CROP_PHASE[crop]
        if not (lo <= day <= hi):
            continue
        if _get(prices, crop, BASE_PRICE[crop]) < CROP_FLOOR[crop]:
            continue  # red line: dead-price freeze for this crop
        room = CROP_CAP_PER_QUAD[crop] * len(quads) - len(crop_map[crop])
        taken = 0
        for pos in empties:
            if taken >= room:
                break
            crop_map[crop].add(pos)
            taken += 1
        empties = empties[taken:]
    wheat_room = _wheat_cap(day, _get(prices, "WHEAT", 25)) - len(crop_map["WHEAT"])
    if _get(prices, "WHEAT", 25) >= WHEAT_MONEY_GATE:
        # log-curve wheat as a rotation money crop (rank-1 adaptive share:
        # 0.45-0.62 of the field when wheat trades 36-42+); the extra tiles
        # also soften the wheat price against volume-farming opponents
        wheat_room += WHEAT_MONEY_CAP_PER_QUAD * len(quads)
    taken = 0
    for pos in empties:
        if taken >= wheat_room:
            break
        crop_map["WHEAT"].add(pos)
        taken += 1

    capacity = int(len(crop_map["WHEAT"]) * 1.2)
    return builds, crop_map, n_animals, capacity


def _count_crops(farm):
    """Alive PLANT tiles per crop (for seed deficits)."""
    counts = {crop: 0 for crop in CROPS}
    for row in _get(farm, "tiles", []) or []:
        for tile in row:
            if isinstance(tile, dict) and _get(tile, "kind", "") == "PLANT":
                crop = _get(tile, "crop", "")
                if crop in counts:
                    counts[crop] += 1
    return counts


def _species_counts(farm, private, herd_total):
    """Placed + shed + carried animals per species.  Herd totals handed in
    by abstract callers that carry no observable composition are attributed
    to the primary species (sheep) -- real observations never need this.
    """
    counts = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    for row in _get(farm, "tiles", []) or []:
        for tile in row:
            if isinstance(tile, dict) and "animal" in tile:
                animal = _get(tile, "animal", "")
                if animal in counts:
                    counts[animal] += 1
    shed = _get(private, "shed", {}) or {}
    for animal in counts:
        counts[animal] += _get(shed, animal, 0)
        for inv in (_get(private, "inventories", []) or []):
            if inv:
                counts[animal] += _get(inv, animal, 0)
    extra = int(herd_total) - sum(counts.values())
    if extra > 0:
        counts["SHEEP"] += extra
    return counts


def _market_gates(day, prices, shed, herd):
    """Selective-intervention sell decisions: what to SELL this turn, with
    the hoard / release / defend rule per item made explicit.

    Curve rationale (official MARKET_PARAMS):
      * MILK base 160, LINEAR glut (T=122): hoard below _milk_gate, clear
        through at the band, big tranche at peaks, halve inside the band,
        drain before the 100-slot discard cliff (m2b logic, kept verbatim).
      * WOOL base 200, SQ glut (T=105: ~56 units above equilibrium reach
        the $1 floor -- the fastest crasher): realize in size at real bids
        (12 at 200+, 8 at the gate, 6 at 100+), CUT LOSSES down to a small
        buffer at WOOL_CUT_LOSS once the curve is dying (measured: yarn-
        store draws decide the whole wool market), dump tranches from
        day 26 (FM-O4).
      * STRAWBERRY base 120, LINEAR glut (T=100): gate 105, tranche 8,
        bounded hoard, endgame dump (the near-band premium: their held
        medians 221-250 come from hoarding, not from dumping daily).
      * MELON base 250, SQ glut (T=300): gate 180, tranche 8 -- realize
        BEFORE the volume farmers' 100+ unit flow floors the curve (the
        m1 engine's melon branch died holding for 250; cap stays 9 tiles
        because a 12-tile plan measurably crashed our own price).
      * CARROT base 35, SQRT glut (T=450, hinge below -- town spikes it
        when scarce): gate 28, generous tranche 15.
      * EGG base 50, LOG glut (crash-tolerant like wheat): gate 40,
        tranche 10.
      * FERTILIZER base 100, linear both sides, no town consumption (m2b):
        bounded hoard, gated release, unconditional from day 25.
      * WHEAT base 25, LOG glut: sell the surplus above the feed reserve
        from WHEAT_SELL_GATE (a real bid, not the floor).
    Returns a list of ["SELL", item, qty] market orders.
    """
    orders = []
    last_day = day >= SEASON_DAYS - 1
    endgame = day >= ENDGAME_DAY
    shed_count = sum(v for v in shed.values() if isinstance(v, (int, float)))

    if last_day:
        # day 29: only bank money counts; liquidate every tradable shed item
        for item in BASE_PRICE:
            n = shed.get(item, 0)
            if isinstance(n, (int, float)) and n > 0:
                orders.append(["SELL", item, n])
        return orders

    # ---- MILK: hoard / release / defend (m2b, verbatim) ------------------
    milk = shed.get("MILK", 0)
    if milk > 0:
        gate = _llm_sell_gate("MILK", prices.get("MILK", BASE_PRICE["MILK"]),
                              _milk_gate(day), {"day": day, "shed": milk,
                                                "herd": herd})
        p = prices.get("MILK", BASE_PRICE["MILK"])
        if shed_count >= 70 and p >= 30:
            sell = max(0, milk - 15)
            if sell > 0:
                orders.append(["SELL", "MILK", sell])
        elif p >= 145:
            orders.append(["SELL", "MILK", min(milk, 24)])
        elif p >= gate:
            orders.append(["SELL", "MILK", min(milk, 20)])

    # ---- WOOL: sq glut (T=105) -- follow the curve, never ride it down ---
    # Sheep flow (ours + the opponent's, 9-12 head across the pool) exceeds
    # base town consumption in most draws: wool either stays scarce (yarn
    # stores drawn -- observed 240+ all season) or floors (+56 units above
    # equilibrium is already $5).  So: realize in size at real bids, cut the
    # hoard fast once the curve turns (WOOL_CUT_LOSS), dump in the endgame
    # window -- never ride a dead curve into the day-29 joint floor.
    wool = shed.get("WOOL", 0)
    if isinstance(wool, (int, float)) and wool > 0:
        p = prices.get("WOOL", BASE_PRICE["WOOL"])
        if endgame or day >= 26:
            orders.append(["SELL", "WOOL", min(wool, 12)])
        elif shed_count >= 78 and p >= 5:
            orders.append(["SELL", "WOOL", max(0, wool - 10)])
        elif wool > WOOL_HOARD_FLOOR:
            if p >= 200:
                orders.append(["SELL", "WOOL", min(wool - WOOL_HOARD_FLOOR, 12)])
            elif p >= WOOL_GATE:
                orders.append(["SELL", "WOOL", min(wool - WOOL_HOARD_FLOOR, 8)])
            elif p >= 100:
                orders.append(["SELL", "WOOL", min(wool - WOOL_HOARD_FLOOR, 6)])
            elif p >= WOOL_CUT_LOSS and (day >= 18 or wool > WOOL_HOARD_CAP):
                orders.append(["SELL", "WOOL", min(wool - 4, 8)])

    # ---- premium rotation/herd goods: gated tranches + hoard bounds ------
    def premium(item, gate, tranche, hoard_floor, hoard_cap, low_gate,
                endgame_tranche):
        held = shed.get(item, 0)
        if not isinstance(held, (int, float)) or held <= hoard_floor:
            return
        p = prices.get(item, BASE_PRICE[item])
        if endgame:
            orders.append(["SELL", item, min(held, endgame_tranche)])
        elif shed_count >= 78 and p >= 5:
            # discard-cliff guard shared with milk
            orders.append(["SELL", item, max(0, held - 10)])
        elif p >= gate + 30:
            orders.append(["SELL", item, min(held - hoard_floor, tranche * 2)])
        elif p >= gate:
            orders.append(["SELL", item, min(held - hoard_floor, tranche)])
        elif held > hoard_cap and p >= low_gate:
            orders.append(["SELL", item, min(held - hoard_cap, tranche)])

    premium("STRAWBERRY", STRAWBERRY_GATE, 8, STRAWBERRY_HOARD_FLOOR, 26, 70, 12)
    premium("MELON", MELON_GATE, 8, MELON_HOARD_FLOOR, 14, 120, 8)
    premium("CARROT", CARROT_GATE, 15, CARROT_HOARD_FLOOR, 30, 22, 20)
    premium("EGG", EGG_GATE, 10, EGG_HOARD_FLOOR, 16, 30, 12)

    # ---- FERTILIZER: bounded hoard, gated release (m2b) ------------------
    fert = shed.get("FERTILIZER", 0)
    if fert > 0:
        if day >= 25:
            orders.append(["SELL", "FERTILIZER", fert])
        elif fert > FERT_STOCK_CAP:
            orders.append(["SELL", "FERTILIZER", max(0, fert - FERT_FIELD_RESERVE)])
        elif prices.get("FERTILIZER", BASE_PRICE["FERTILIZER"]) >= FERT_GATE:
            sell = max(0, fert - FERT_FIELD_RESERVE)
            if sell > 0:
                orders.append(["SELL", "FERTILIZER", sell])
    return orders


def _build_tasks(obs, farm, private, day):
    """Return (tasks, animals_to_feed, herd_total, wheat_tiles, capacity)."""
    tiles = _get(farm, "tiles", [])
    board = len(tiles)
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    builds, crop_map, n_animals, capacity = _field_alloc(farm, day, prices)
    seeds = _get(private, "seeds", {}) or {}
    shed = _get(private, "shed", {}) or {}
    inventories = _get(private, "inventories", []) or []
    wheat_on_units = sum(_get(inv, "WHEAT", 0) for inv in inventories if inv)
    species_on_units = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    fert_on_units = 0
    for inv in inventories:
        if not inv:
            continue
        for animal in species_on_units:
            species_on_units[animal] += _get(inv, animal, 0)
        fert_on_units += _get(inv, "FERTILIZER", 0)
    animals_to_feed = 0

    tasks = []

    def add(w, x, y, act, key, need=None, units=None):
        tasks.append({"w": w, "x": x, "y": y, "act": act, "key": key,
                      "need": need, "units": units})

    last_day = day >= SEASON_DAYS - 1
    stop_feed = day >= ENDGAME_DAY        # FM-O4: doomsday stop-feeding
    if last_day:
        hour = _get(obs, "hour", 0)
        positions = [tuple(_get(farm, "farmer", [board // 2 - 1, board // 2 - 1]))]
        positions.extend(tuple(hand) for hand in (_get(farm, "hands", []) or []))
        accesses = _shed_access(board)

        for ui, (ux, uy) in enumerate(positions):
            inv = inventories[ui] if ui < len(inventories) else {}
            if sum(n for n in inv.values() if isinstance(n, (int, float)) and n > 0) <= 0:
                continue
            sx, sy = min(accesses, key=lambda pos: (_dist(ux, uy, *pos), pos[1], pos[0]))
            add(120, sx, sy, ["DROP"], ("return", ui), units={ui})

        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if not isinstance(tile, dict) or _get(tile, "yield_units", 0) <= 0:
                    continue
                if _get(tile, "kind", "") != "PLANT" and "animal" not in tile:
                    continue
                eligible = set()
                return_distance = min(_dist(x, y, *pos) for pos in accesses)
                for ui, (ux, uy) in enumerate(positions):
                    inv = inventories[ui] if ui < len(inventories) else {}
                    if any(n > 0 for n in inv.values() if isinstance(n, (int, float))):
                        continue
                    turns_needed = _dist(ux, uy, x, y) + 1 + return_distance + 1
                    if turns_needed <= 23 - hour:
                        eligible.add(ui)
                if eligible:
                    add(110, x, y, ["HARVEST"], ("harvest", x, y),
                        units=eligible)

        herd_total = n_animals + sum(_get(shed, a, 0) for a in ANIMALS) \
            + sum(species_on_units.values())
        return tasks, 0, herd_total, len(crop_map["WHEAT"]), capacity

    # species still waiting in the shed (place tasks need carriers)
    placeable = {"SHEEP": _get(shed, "SHEEP", 0) + species_on_units["SHEEP"],
                 "COW": _get(shed, "COW", 0) + species_on_units["COW"],
                 "GOOSE": _get(shed, "GOOSE", 0) + species_on_units["GOOSE"]}

    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile == "LOCKED":
                continue
            pos = (x, y)
            if tile is None:
                if pos in builds:
                    op = "BUILD_COOP" if builds[pos] == "COOP" else "BUILD_PASTURE"
                    add(46, x, y, [op], ("build", x, y))
                    continue
                crop = None
                for c, positions in crop_map.items():
                    if pos in positions:
                        crop = c
                        break
                if crop is not None and seeds.get(crop, 0) > 0 \
                        and day <= PLANT_LAST_DAY.get(crop, 24):
                    add(30 if crop == "WHEAT" else 32, x, y,
                        ["PLANT", crop], ("plant", x, y))
                continue
            if not isinstance(tile, dict):
                continue
            kind = _get(tile, "kind", "")
            if kind == "WEED":
                if pos in builds or any(pos in s for s in crop_map.values()):
                    add(22, x, y, ["DIG"], ("dig", x, y))
                continue
            if kind == "PLANT":
                crop = _get(tile, "crop", "WHEAT")
                cd = CROPS.get(crop)
                if not cd:
                    continue
                planned = pos in crop_map.get(crop, ())
                age = day - _get(tile, "planted_day", day)
                yu = _get(tile, "yield_units", 0)
                ws, we = _window(crop)
                in_window = ws <= age <= we
                if not _get(tile, "watered_today", False):
                    if _get(tile, "consecutive_unwatered", 0) >= 1:
                        add(98, x, y, ["WATER"], ("water", x, y))   # dies tonight
                    elif planned and cd["ongoing"]:
                        # ongoing crops: watering doubles fertilized output
                        # and keeps the 2-day survival streak clear
                        add(40, x, y, ["WATER"], ("water", x, y))
                    elif in_window and planned:
                        add(42, x, y, ["WATER"], ("water", x, y))
                    elif age % 2 == 1:
                        add(24, x, y, ["WATER"], ("water", x, y))   # survival
                # FM-4 generalized: animal fertilizer feeds the rotation.
                # One-time crops at age 2 (the +2 window then lands inside
                # the 3-day fertilizer window); strawberry refreshed
                # whenever the 3-day window lapses (each production day
                # pays +2 instead of +1 while watered).
                if planned and _get(tile, "fertilized_until_day", -1) < day:
                    if cd["ongoing"] or age == 2:
                        premium_boost = crop in ("STRAWBERRY", "MELON")
                        fert_dear = _get(prices, "FERTILIZER",
                                         BASE_PRICE["FERTILIZER"]) >= FERT_VALUE_GATE
                        if premium_boost or not fert_dear:
                            add(36 if cd["ongoing"] else 34, x, y, ["FERTILIZE"],
                                ("fert", x, y), need="FERTILIZER")
                if yu > 0:
                    if cd["ongoing"]:
                        if yu >= 3:
                            add(70, x, y, ["HARVEST"], ("harvest", x, y))
                    elif age >= cd["max_yield_day"] + 1 or last_day:
                        # rot emergency: one-time crops decay to a weed from
                        # hour 0 of this day, ~1 unit per 2 turns
                        add(95, x, y, ["HARVEST"], ("harvest", x, y))
                    elif age >= cd["max_yield_day"] and (
                            _get(tile, "watered_today", False) or
                            _get(obs, "hour", 0) >= 18):
                        add(80, x, y, ["HARVEST"], ("harvest", x, y))
            elif "animal" in tile:
                if not stop_feed:
                    if not _get(tile, "fed_today", False):
                        animals_to_feed += 1
                        # escape risk outranks everything: escalate by streak/hour
                        if _get(tile, "consecutive_unfed", 0) >= 1 or \
                                _get(obs, "hour", 0) >= 16:
                            w = 100
                        else:
                            w = 88
                        add(w, x, y, ["FEED"], ("feed", x, y), need="WHEAT")
                    if day <= SEASON_DAYS - 3 and not _get(tile, "cared_today", False) \
                            and _get(tile, "fed_today", False):
                        add(56, x, y, ["CARE"], ("care", x, y))
                yu = _get(tile, "yield_units", 0)
                if yu >= 5:
                    add(92, x, y, ["HARVEST"], ("harvest", x, y))   # about to cap
                elif yu >= 3 or (yu > 0 and (last_day or stop_feed)):
                    add(70, x, y, ["HARVEST"], ("harvest", x, y))
                if _get(tile, "fertilizer_available", False):
                    add(44, x, y, ["COLLECT_FERTILIZER"], ("cfert", x, y))
            elif kind in ("PASTURE", "COOP") and "animal" not in tile:
                animal = None
                if kind == "COOP" and placeable["GOOSE"] > 0:
                    animal = "GOOSE"
                elif kind == "PASTURE":
                    for candidate in ("SHEEP", "COW"):
                        if placeable[candidate] > 0:
                            animal = candidate
                            break
                if animal is not None and _get(obs, "hour", 0) <= 18:
                    # urgent: an unplaced animal produces nothing and squats
                    # in the shed (a 100-slot shared resource)
                    placeable[animal] -= 1
                    add(82, x, y, ["PLACE", animal], ("place", x, y),
                        need=animal)

    board_half = board // 2
    shed_tile = (board_half - 1, board_half - 1)
    shed_available = {item: max(0, int(n)) for item, n in shed.items()}
    # ---- feed logistics: distribute the wheat across several carriers ----
    # (one carrier cannot FEED a 10-animal ring within 24 turns; chunks of 5
    # are grabbed by different units because a loaded carrier is barred
    # from picking up another chunk -- see executable() below.  Chunks are
    # raised whenever carried wheat falls short of the mouths, so multiple
    # carriers restock throughout the day.)
    if animals_to_feed > 0 and shed_available.get("WHEAT", 0) > 0:
        shortfall = animals_to_feed + 2 - wheat_on_units
        i = 0
        while shortfall > 0 and i < 4 and shed_available.get("WHEAT", 0) > 0:
            n = min(5, shortfall, shed_available["WHEAT"])
            if n <= 0:
                break
            add(96 - 8 * i, shed_tile[0], shed_tile[1], ["PICKUP", "WHEAT", n],
                ("pickup_w", i))
            shortfall -= n
            shed_available["WHEAT"] -= n
            i += 1
    # ---- animal logistics: carry bought animals onto empty structures ----
    for animal in ("SHEEP", "COW", "GOOSE"):
        if shed_available.get(animal, 0) > 0 and species_on_units[animal] < 2 \
                and any(t["key"][0] == "place" and t["act"][1] == animal
                        for t in tasks):
            n = min(2, shed_available[animal])
            add(94, shed_tile[0], shed_tile[1], ["PICKUP", animal, n],
                ("pickup_a", animal))
            shed_available[animal] -= n
    # ---- fertilizer logistics for the rotation's fertilize tasks --------
    if any(t["key"][0] == "fert" for t in tasks) and \
            shed_available.get("FERTILIZER", 0) > 0 and fert_on_units < 3:
        n = min(4, shed_available["FERTILIZER"])
        add(40, shed_tile[0], shed_tile[1], ["PICKUP", "FERTILIZER", n],
            ("pickup_f", 0))
        shed_available["FERTILIZER"] -= n
    herd_total = n_animals + sum(_get(shed, a, 0) for a in ANIMALS) \
        + sum(species_on_units.values())
    return tasks, animals_to_feed, herd_total, len(crop_map["WHEAT"]), capacity


def _market_orders(obs, farm, private, day, animals_to_feed, herd_total):
    money = _get(farm, "money", 0.0)
    shed = _get(private, "shed", {}) or {}
    seeds = _get(private, "seeds", {}) or {}
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    quads = len(_get(farm, "unlocked_quadrants", ["NW"]) or ["NW"])
    shed_count = sum(v for v in shed.values() if isinstance(v, (int, float)))
    last_day = day >= SEASON_DAYS - 1
    builds, crop_map, _placed, capacity = _field_alloc(farm, day, prices)

    orders = []

    # ---- land plan (FM-O2): NE day 4+, SW day 7+; the fund is protected --
    # (working capital -- seeds/feed -- is never blocked: it pays for the
    # land; herd buys wait for the fund while it is pending).  The purchase
    # itself stays eligible every day after the due day -- the block on the
    # herd simply lapses so a slow season cannot deadlock the ranch.
    land_fund = 0
    land_pending = False
    if quads in LAND_PLAN:
        due_day, fund = LAND_PLAN[quads]
        if day >= due_day:
            land_fund = fund
            if money >= fund:
                orders.append(["BUY_LAND"])
            elif day < due_day + LAND_PEND_WINDOW:
                land_pending = True

    # ---- feed security (FM-O3 + m2b phantom guard): never let the herd
    # run short of wheat, counting what carriers already hold (a shed-only
    # check sees the morning pickup as a shortfall and re-buys what we just
    # sold -- measured -8k/season).  Guardrail: normal-state buys stop at
    # FEED_BUY_MAX_PRICE (profile avg 26-32); starvation cap 85 kept (dear
    # wheat is still cheaper than a lost animal).
    wheat_carried = sum(_get(inv, "WHEAT", 0)
                        for inv in (_get(private, "inventories", []) or []) if inv)
    sys_wheat = shed.get("WHEAT", 0) + wheat_carried
    if animals_to_feed > 0 and not last_day \
            and sys_wheat < animals_to_feed + 3:
        cap = 85 if sys_wheat < animals_to_feed else FEED_BUY_MAX_PRICE
        if prices.get("WHEAT", 25) <= cap:
            want = min(16, animals_to_feed + 8 - sys_wheat)
            if want > 0:
                orders.append(["BUY_PRODUCT", "WHEAT", want])

    # ---- seeds: the wheat feed floor first (m2b), then rotation crops
    # staged behind the pending land fund (FM-3 staging).  R3-3 exception:
    # strawberry is NOT staged behind the land fund once its phase opens --
    # the winners plant 6+ tiles on d5-11 while the NE/SW purchases proceed
    # on their own fund-gated schedule (planting d5 pays from d15 at
    # ~200/u; the one-day land delay it can cost repays many times over).
    if seeds.get("WHEAT", 0) < 6 and day <= SEASON_DAYS - 7 and money >= 150:
        orders.append(["BUY_SEED", "WHEAT", 12])
    if not last_day:
        alive = _count_crops(farm)
        for crop in ("STRAWBERRY", "MELON", "CARROT"):
            lo, hi = CROP_PHASE[crop]
            if not (lo <= day <= hi):
                continue
            if prices.get(crop, BASE_PRICE[crop]) < CROP_FLOOR[crop]:
                continue  # red line: dead-price freeze
            want = CROP_CAP_PER_QUAD[crop] * quads - alive[crop] - seeds.get(crop, 0)
            batch = min(6, max(0, want))
            seed_gate = 250 if crop == "STRAWBERRY" else land_fund + 250
            if batch > 0 and money >= seed_gate + CROPS[crop]["seed"] * batch:
                orders.append(["BUY_SEED", crop, batch])

    # ---- herd (FM-O2 + R3-1/R3-2): mixed 14-head ranch, money-gated,
    # paced by CONFIRMED purchases (m2b), species-level dead-price freeze
    # (red line).  Day 0 is the r3 opening: the burst buys OPENING_HERD
    # outright (2C+2S = 1800 of the 3000 start; 116/116 top-20 seats and
    # 3/3 round-2 winners put 4-5 head on d0 -- the m3 1-sheep opening is
    # the fork the round-2 losses traced to), both species in one turn so
    # cows reach the day-8 milk window AND sheep the day-6 wool window.
    reserve = 800 if day <= 3 else (550 if day <= 7 else COW_BUY_RESERVE)
    if land_pending:
        reserve += land_fund
    pace = _animal_pace(day)
    target = _herd_target(day, 99)   # FM-O3: external feed releases autarky
    bought = _buy_pace(_get(obs, "player", 0), day, _get(obs, "hour", 0),
                       herd_total)
    opening_bought = False
    if not last_day and day == 0 and herd_total == 0:
        spend = 0
        for animal in ("COW", "SHEEP"):
            want = OPENING_HERD.get(animal, 0)
            cost = ANIMALS[animal]["cost"]
            n = min(want, int((money - spend - OPENING_RESERVE) // cost)) \
                if money - spend > OPENING_RESERVE else 0
            if n > 0:
                orders.append(["BUY_ANIMAL", animal, n])
                _note_buy_order(_get(obs, "player", 0), day,
                                _get(obs, "hour", 0), n)
                spend += n * cost
                opening_bought = True
    if not opening_bought and not last_day and herd_total < target \
            and shed_count < 88 and bought < pace:
        species = _species_counts(farm, private, herd_total)
        # interleave species by relative deficit so cows reach their day-8+
        # premium-milk window on time instead of queueing behind the sheep
        candidates = sorted((a for a in HERD_COMPOSITION if HERD_COMPOSITION[a] > 0),
                            key=lambda a: species[a] / float(HERD_COMPOSITION[a]))
        for animal in candidates:
            if species[animal] >= HERD_COMPOSITION[animal]:
                continue
            if day > ANIMAL_BUY_LAST_DAY[animal]:
                continue
            product = ANIMALS[animal]["product"]
            if day >= DEAD_PRICE_FROM_DAY and \
                    prices.get(product, BASE_PRICE[product]) < DEAD_PRICE_FLOOR[product]:
                continue  # dead-price freeze (m2b demand-drought generalized)
            cost = ANIMALS[animal]["cost"]
            if money < cost + reserve:
                continue
            n = min(pace - bought, target - herd_total,
                    HERD_COMPOSITION[animal] - species[animal],
                    int((money - reserve) // cost))
            if n > 0:
                orders.append(["BUY_ANIMAL", animal, n])
                _note_buy_order(_get(obs, "player", 0), day,
                                _get(obs, "hour", 0), n)
            break   # one species per turn

    # ---- selling: selective-intervention gates --------------------------
    orders.extend(_market_gates(day, prices, shed, herd_total))
    if last_day:
        # Goods already carried can DROP before market processing in this turn,
        # so include them in liquidation. Failed/partial quantities remain legal
        # positive orders and simply commit up to actual shed availability.
        carried = {}
        for inv in (_get(private, "inventories", []) or []):
            for item, n in (inv or {}).items():
                if isinstance(n, (int, float)) and n > 0:
                    carried[item] = carried.get(item, 0) + n
        indexed = {order[1]: order for order in orders if order[0] == "SELL"}
        for item, n in carried.items():
            if item not in BASE_PRICE:
                continue
            if item in indexed:
                indexed[item][2] += n
            else:
                order = ["SELL", item, n]
                orders.append(order)
                indexed[item] = order
    # wheat: log glut curve; sell the surplus above the feed reserve at a
    # real bid (WHEAT_SELL_GATE), under the m2b pressure/late fallbacks
    if not last_day:
        reserve_w = animals_to_feed + WHEAT_FEED_RESERVE
        surplus = shed.get("WHEAT", 0) - reserve_w
        wheat_px = prices.get("WHEAT", 25)
        if surplus > 0 and (wheat_px >= WHEAT_SELL_GATE
                            or shed_count >= 70 or day >= 26
                            or (money < 1000 and wheat_px >= 20)):
            # money < 1000: cash-flow fallback -- the gate must never starve
            # the land/animal capex plan (measured: 42 wheat hoarded at $516
            # while the NE purchase window lapsed)
            orders.append(["SELL", "WHEAT", surplus])
    return orders


def _schedule_units(obs, farm, private, day, tasks):
    tiles = _get(farm, "tiles", [])
    board = len(tiles)
    units = [tuple(_get(farm, "farmer", [board // 2 - 1, board // 2 - 1]))]
    for h in _get(farm, "hands", []) or []:
        units.append(tuple(h))
    inventories = _get(private, "inventories", []) or []

    def unit_inv(i):
        while len(inventories) <= i:
            inventories.append({})
        return inventories[i]

    claimed = set()
    actions = []

    def executable(task, ui):
        eligible = task.get("units")
        if eligible is not None and ui not in eligible:
            return False
        need = task.get("need")
        if need and _get(unit_inv(ui), need, 0) <= 0:
            return False
        x, y = task["x"], task["y"]
        tile = tiles[y][x]
        kind = _get(tile, "kind", "") if isinstance(tile, dict) else None
        op = task["act"][0]
        if op in ("WATER", "FERTILIZE"):
            return kind == "PLANT"
        if op == "HARVEST":
            return kind == "PLANT" or (isinstance(tile, dict) and "animal" in tile)
        if op in ("FEED", "CARE", "COLLECT_FERTILIZER"):
            return isinstance(tile, dict) and "animal" in tile
        if op == "PLANT":
            return tile is None
        if op == "DIG":
            return kind == "WEED"
        if op in ("BUILD_PASTURE", "BUILD_COOP"):
            return tile is None
        if op == "PLACE":
            structure = ANIMALS.get(task["act"][1], {}).get("structure")
            return isinstance(tile, dict) and _get(tile, "kind", "") == structure \
                and "animal" not in tile
        if op == "PICKUP":
            if not _shed_adjacent(units[ui][0], units[ui][1], board):
                return False
            # a carrier holding a full chunk moves out to feed instead of
            # chain-grabbing every chunk at the shed (multi-carrier FEED)
            if task["act"][1:2] == ["WHEAT"] and _get(unit_inv(ui), "WHEAT", 0) >= 5:
                return False
            return True
        if op == "DROP":
            return _shed_adjacent(units[ui][0], units[ui][1], board) and any(
                n > 0 for n in unit_inv(ui).values()
                if isinstance(n, (int, float)))
        return True

    for ui, (ux, uy) in enumerate(units):
        chosen = None
        # 1) act on the current tile (highest weight executable here)
        best_here = None
        for t in tasks:
            if t["key"] in claimed or (t["x"], t["y"]) != (ux, uy):
                continue
            if not executable(t, ui):
                continue
            if best_here is None or t["w"] > best_here["w"]:
                best_here = t
        if best_here is not None:
            chosen = best_here
        else:
            # 2) walk toward the best unclaimed task; prefer tasks whose
            # carried-item requirement this unit already satisfies
            best = None
            for t in tasks:
                if t["key"] in claimed or (t.get("units") is not None and
                                             ui not in t["units"]):
                    continue
                score = t["w"] / (1.0 + _dist(ux, uy, t["x"], t["y"]))
                need = t.get("need")
                if need:
                    if _get(unit_inv(ui), need, 0) > 0:
                        score *= 1.8   # carriers converge on consumer tasks
                    else:
                        score *= 0.35  # wheatless units do not chase FEED tasks
                if t["act"][0] == "PICKUP" and t["act"][1:2] == ["WHEAT"] \
                        and _get(unit_inv(ui), "WHEAT", 0) >= 5:
                    score *= 0.35     # loaded carriers leave the shed to feed
                if best is None or score > best[0]:
                    best = (score, t)
            chosen = best[1] if best else None

        if chosen is None:
            actions.append(["PASS"])
            continue
        claimed.add(chosen["key"])
        cx, cy = chosen["x"], chosen["y"]
        if (ux, uy) == (cx, cy):
            if executable(chosen, ui):
                actions.append(list(chosen["act"]))
            else:
                # standing on it but missing the carried item -> fetch at shed
                half = board // 2
                sx, sy = half - 1, half - 1
                actions.append(_step_towards(ux, uy, sx, sy))
        else:
            actions.append(_step_towards(ux, uy, cx, cy))

    # R6 guard: never request more PLANTs of a crop than seeds held
    seeds = _get(private, "seeds", {}) or {}
    demand = {}
    for a in actions:
        if a and a[0] == "PLANT":
            demand[a[1]] = demand.get(a[1], 0) + 1
    for crop, n in demand.items():
        if n > seeds.get(crop, 0):
            keep = seeds.get(crop, 0)
            for i, a in enumerate(actions):
                if a and a[0] == "PLANT" and a[1] == crop:
                    if keep > 0:
                        keep -= 1
                    else:
                        actions[i] = ["PASS"]
    return actions


def agent(obs):
    """Entry point: one action dict per turn (official Quick-Start signature)."""
    try:
        player = _get(obs, "player", 0)
        farms = _get(obs, "farms", [])
        if not farms or player >= len(farms):
            return {"farmer": ["PASS"], "hands": [], "market": []}
        farm = farms[player]
        day = _get(obs, "day", 0)
        hour = _get(obs, "hour", 0)
        tiles = _get(farm, "tiles", [])
        if not tiles:
            return {"farmer": ["PASS"], "hands": [], "market": []}

        tasks, animals_to_feed, herd_total, wheat_tiles, capacity = \
            _build_tasks(obs, farm, private=_get(obs, "private", {}) or {}, day=day)
        actions = _schedule_units(obs, farm, _get(obs, "private", {}) or {},
                                  day, tasks)
        orders = _market_orders(obs, farm, _get(obs, "private", {}) or {},
                                day, animals_to_feed, herd_total)

        # FM-O2/R3-4 labour: hire up to the plan in a dawn burst (hands reset
        # every morning; one HIRE per order; only hour <= 2 can hire -- m2b
        # fix).  Each emitted HIRE is affordable at its exact fib price.
        hires = []
        if day < SEASON_DAYS - 1 and hour <= HIRE_HOUR_MAX:
            quads = len(_get(farm, "unlocked_quadrants", ["NW"]) or ["NW"])
            hands_t = _crew_target(day, herd_total, wheat_tiles, quads)
            hands = len(_get(farm, "hands", []) or [])
            money = _get(farm, "money", 0.0)
            spend = 0
            for i in range(hands, hands_t):
                cost = _hire_cost(i)
                # keep a working-cash cushion: a broke dawn cannot hire the
                # crew that would earn it back (measured day-8 stall)
                if spend + cost > money - 60 or len(hires) >= HIRE_BURST:
                    break
                spend += cost
                hires.append(["HIRE"])

        # buys before sells (a dropped sell tranche simply repeats next
        # turn, while a dropped HIRE/BUY loses a whole day of the plan);
        # dawn hires lead the queue.
        buys = [o for o in orders if o[0] != "SELL"]
        sells = [o for o in orders if o[0] == "SELL"]
        orders = hires + buys + sells

        # Final defense: every quantity-bearing market order must be positive,
        # and the terminal day is liquidation-only.
        orders = [o for o in orders
                  if len(o) < 3 or (isinstance(o[2], (int, float)) and o[2] > 0)]
        if day >= SEASON_DAYS - 1:
            orders = [o for o in orders if o[0] == "SELL"]

        farmer = actions[0] if actions else ["PASS"]
        hands_actions = actions[1:]
        return {"farmer": farmer, "hands": hands_actions, "market": orders[:10]}
    except Exception:
        # a submission must never crash: fall back to a safe legal action
        return {"farmer": ["PASS"], "hands": [], "market": []}
