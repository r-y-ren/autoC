"""Online-style opponents (campaign III m2-online-pool + r3-1 scale_ranch):
five parameterised reconstructions of the ladder archetypes extracted in m1
from 60 official episode replays (120 seat profiles; exports/replay_profiles/)
plus, for scale_ranch, the three round-2 winner replays
(exports/online/round2_winner_deep_dive.md).

Parameter discipline (blueprint m2): every knob of the flagship bots is
backed by a SAME-PLAYER >=3-game consistent finding from the cross-game review
(band_summary.md "Cross-game consistency review").  The near_band bot is marked
``exploratory_params = True``: it draws on the 500-900 rating band where only
2 games exist, but the two seats belong to two INDEPENDENT players whose
structures converge (strawberry-led diversified portfolio + late 4th quadrant
+ heavy endgame dumping), which is the documented justification for including
it in the pool anyway -- it represents the real online distribution around
our own ladder position.  scale_ranch is NOT exploratory: each knob cites a
>=3-game top-20 finding that cross-validates the round-2 winners' single-game
trajectories (the winners are 1 game each, so winner-only numbers are treated
as style, not structure).

Archetypes (see PARAM provenance fields for the exact games):

crop_rotator         -- ladder #1 "Crop Dusta" framework (26 consistent games):
                        constant labour/quadrant frame (4 hires per unlocked
                        quadrant, cap 12 -> 9.7-9.9 hires/day; 3 quadrants),
                        7-cow + 4-sheep + 1-goose herd, price-adaptive wheat
                        share (20-69%) and crop rotation (melon early ->
                        strawberry mid -> tomato late), external feed buying
                        under a price guardrail, endgame hoard-dump.
template_wheat       -- rank 6-28 template cluster (NIklitaCheporev 8 g,
                        Multi-Head Farmers 6 g, Aashka Kapadia 3 g, Gaddam
                        Shiva Teja 3 g, Levin 3 g, heralces 3 g -- identical
                        template): locked 42% wheat share, 414-436u external
                        feed, 9.4 hires/day ramp, 8-cow + 4-sheep herd,
                        dump-priced sell gates (milk/wool/strawberry medians
                        1-69).
self_feed_ranch      -- ladder #2 "Milan Leonard" (12 consistent games):
                        near self-sufficient feed (119-147u external wheat
                        total), 43-50% wheat field, mixed 6-cow + 6-sheep
                        herd, premium sell gates (milk median 200, wool 220),
                        strawberry + melon side business, small external
                        fertilizer top-up.
near_band_diversified -- 500-900 band (Sooriya Senthilkumar ep 102194478,
                        Chirag Bhatnagar ep 102196708; exploratory_params):
                        strawberry-led rotation (51.8%/33.7% shares) + melon,
                        8-cow/3-sheep/2-goose herd, 4th quadrant late,
                        8.5-8.6 hires/day, heavy endgame liquidation
                        (Chirag endgame sell share 17.7%).
scale_ranch            -- round-2 winner archetype (campaign III r3-1, next
                        band above our ladder position): cross-profile of the
                        three round-2 winners (arminhej96 ep102399852 100559,
                        朝闻夕死 ep102402115 95087, Danila Galkin ep102406576
                        98770) validated against the top-20 corpus (58
                        episodes / 116 seats).  Structure: day-0 herd burst
                        (5 animals, ~2000 of the 3000 start), 8-cow + 6-sheep
                        herd complete by day ~9-11, strawberry ramped early
                        (cap 20 tiles), full-coverage CARE, crew 12 from day
                        7, premium milk/strawberry/melon gates, endgame dump
                        day 28.  Every knob cites the >=3-game top-20 finding
                        it cross-validates; single-game winner quirks (4th
                        quadrant, over-issued CARE no-ops) are excluded --
                        see exports/online/round2_winner_deep_dive.md.

All four share one claim-based labour scheduler (same contract as the other
local bots) and are purely functions of the observation: stateless,
deterministic per call.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

CROPS_INFO = {
    "WHEAT":      {"seed": 10,  "first_yield_day": 2,  "max_yield_day": 4,  "interval": 0, "max_yield": 6, "ongoing": False},
    "CARROT":     {"seed": 20,  "first_yield_day": 2,  "max_yield_day": 3,  "interval": 0, "max_yield": 4, "ongoing": False},
    "TOMATO":     {"seed": 50,  "first_yield_day": 8,  "max_yield_day": 8,  "interval": 1, "max_yield": 4, "ongoing": True},
    "STRAWBERRY": {"seed": 100, "first_yield_day": 10, "max_yield_day": 10, "interval": 2, "max_yield": 4, "ongoing": True},
    "MELON":      {"seed": 80,  "first_yield_day": 10, "max_yield_day": 12, "interval": 0, "max_yield": 6, "ongoing": False},
}
ANIMALS_INFO = {
    "GOOSE": {"cost": 300, "structure": "COOP",    "first_yield_day": 4, "interval": 1, "max_held": 4, "product": "EGG"},
    "COW":   {"cost": 400, "structure": "PASTURE", "first_yield_day": 8, "interval": 2, "max_held": 6, "product": "MILK"},
    "SHEEP": {"cost": 500, "structure": "PASTURE", "first_yield_day": 6, "interval": 3, "max_held": 6, "product": "WOOL"},
}
LAND_COSTS = [1000, 2000, 4000]          # NE, SW, SE
SEASON_DAYS = 30
PLANT_DEADLINE = {                        # last day a crop can still pay for itself
    "WHEAT": 25, "CARROT": 26, "MELON": 17,
    "STRAWBERRY": 14, "TOMATO": 21,
}
HARVEST_AGE = {"WHEAT": 4, "CARROT": 3, "MELON": 12}

CROP_ROTATOR_PARAMS: Dict = {
    "name": "crop_rotator",
    "provenance": "Crop Dusta (rank 1), 26 consistent games, e.g. ep101270384/101270420/101370699",
    "exploratory_params": False,
    # labour: 4 hires per unlocked quadrant, cap 12 (observed ramp 4/8/12 at
    # quadrant unlocks -> 9.7-9.9 hires/day, 292-295 total)
    "hire_mode": "quad_scaled",
    "hires_per_quadrant": 4,
    "hire_cap": 12,
    "hire_until_hour": 6,
    # land: 3 quadrants, NE ~day 5, SW ~day 8 (Crop Dusta land series)
    "target_quads": 3,
    "quad_min_day": (4, 7, 10),
    "quad_reserve": (350, 500, 800),
    # herd: 7 cows + 4 sheep + 1 goose stable from ~day 12
    "herd": {"COW": 7, "SHEEP": 4, "GOOSE": 1},
    "animal_reserve": 350,
    # field: price-adaptive wheat share 0.20 (wheat cheap) .. 0.62 (wheat dear)
    "wheat_share_mode": "adaptive",
    "wheat_share": None,
    "wheat_share_ladder": ((42, 0.62), (36, 0.45), (30, 0.32), (0, 0.22)),
    "tiles_per_quad": 22,
    "tiles_per_unit": 5.5,
    "money_crop_caps": {"STRAWBERRY": 28, "MELON": 15, "TOMATO": 22},
    "money_crop_min_price": {"STRAWBERRY": 55, "MELON": 150, "TOMATO": 40},
    "crop_phase": {"MELON": (0, 17), "STRAWBERRY": (0, 14), "TOMATO": (15, 21)},
    # feed: guardrailed external buying (Crop Dusta 506-2732u @ avg 34-39)
    "feed_mode": "adaptive",
    "feed_gate": 45,
    "feed_cheap_at": 34,
    "feed_daily_base": 12,
    "feed_cheap_extra": 40,
    "feed_cover_days": 1.5,
    "wheat_sell_keep": 6,
    # selling: hoard-dump gates + tranche bounds, endgame liquidation day 28
    "sell_gates": {"MILK": 100, "WOOL": 130, "STRAWBERRY": 90, "MELON": 160,
                   "WHEAT": 30, "EGG": 40},
    "sell_tranches": {"MILK": 10, "WOOL": 8, "STRAWBERRY": 8, "MELON": 10,
                      "WHEAT": 40, "EGG": 10},
    "fert_gate": 40,
    "endgame_start": 28,
}

TEMPLATE_WHEAT_PARAMS: Dict = {
    "name": "template_wheat",
    "provenance": "rank 6-28 template cluster: NIklitaCheporev (8 g), Multi-Head Farmers (6 g), "
                  "Aashka Kapadia (3 g), Gaddam Shiva Teja (3 g), Levin (3 g), heralces (3 g)",
    "exploratory_params": False,
    # labour: day-ramped crew -> 282-284 hires/season = 9.4/day (template ramp)
    "hire_mode": "ramp",
    "hire_ramp": ((0, 5), (6, 9), (11, 11)),
    "hire_cap": 12,
    "hire_until_hour": 6,
    "target_quads": 3,
    "quad_min_day": (4, 9, 12),
    "quad_reserve": (400, 600, 900),
    # herd: 8 cows + 4 sheep (template final herds)
    "herd": {"COW": 8, "SHEEP": 4, "GOOSE": 0},
    "animal_reserve": 350,
    # field: locked 42% wheat share (all template games exactly 42%)
    "wheat_share_mode": "fixed",
    "wheat_share": 0.42,
    "wheat_share_ladder": None,
    "tiles_per_quad": 21,
    "tiles_per_unit": 5.5,
    "money_crop_caps": {"STRAWBERRY": 24, "MELON": 11},
    "money_crop_min_price": {"STRAWBERRY": 25, "MELON": 130},
    "crop_phase": {"MELON": (0, 17), "STRAWBERRY": (0, 14)},
    # feed: fixed ~15/day cadence -> 436u/season @ avg 36.6 (template constant)
    "feed_mode": "fixed",
    "feed_gate": 38,
    "feed_cheap_at": 30,
    "feed_daily_base": 15,
    "feed_cheap_extra": 0,
    "feed_cover_days": 1.2,
    "wheat_sell_keep": 4,
    # dump-priced template gates (their sell medians: milk 68, wool 1, straw 19, wheat 36)
    "sell_gates": {"MILK": 60, "WOOL": 45, "STRAWBERRY": 22, "MELON": 140,
                   "WHEAT": 22, "EGG": 30},
    "sell_tranches": {"MILK": 25, "WOOL": 25, "STRAWBERRY": 25, "MELON": 15,
                      "WHEAT": 50, "EGG": 15},
    "fert_gate": 30,
    "endgame_start": 28,
}

SELF_FEED_RANCH_PARAMS: Dict = {
    "name": "self_feed_ranch",
    "provenance": "Milan Leonard (rank 2), 12 consistent games, e.g. ep102000368/102002591/102020456",
    "exploratory_params": False,
    "hire_mode": "ramp",
    "hire_ramp": ((0, 5), (6, 9), (11, 11)),          # -> 274 hires = 9.1/day
    "hire_cap": 12,
    "hire_until_hour": 6,
    "target_quads": 3,
    "quad_min_day": (5, 10, 13),                        # Milan NE day 6, SW day 11
    "quad_reserve": (400, 600, 900),
    # herd: mixed 6 cows + 6 sheep (task-level Milan archetype)
    "herd": {"COW": 6, "SHEEP": 6, "GOOSE": 0},
    "animal_reserve": 350,
    # field: 43-50% wheat (midpoint 0.46), own wheat is the feed base
    "wheat_share_mode": "fixed",
    "wheat_share": 0.46,
    "wheat_share_ladder": None,
    "tiles_per_quad": 20,
    "tiles_per_unit": 5.0,
    "money_crop_caps": {"STRAWBERRY": 26, "MELON": 12},
    "money_crop_min_price": {"STRAWBERRY": 60, "MELON": 150},
    "crop_phase": {"MELON": (0, 17), "STRAWBERRY": (0, 14)},
    # feed: gap-fill only (Milan bought just 119-147u all season @ 33.9)
    "feed_mode": "gap",
    "feed_gate": 40,
    "feed_cheap_at": 32,
    "feed_daily_base": 5,
    "feed_cheap_extra": 0,
    "feed_cover_days": 1.5,
    "wheat_sell_keep": 12,
    "fert_buy_gate": 55,                               # Milan bought 31u fertilizer
    "fert_buy_daily": 1,
    # premium gates: Milan's sell medians milk 200 / wool 220
    "sell_gates": {"MILK": 190, "WOOL": 200, "STRAWBERRY": 90, "MELON": 170,
                   "WHEAT": 26, "EGG": 40},
    "sell_tranches": {"MILK": 8, "WOOL": 8, "STRAWBERRY": 8, "MELON": 10,
                      "WHEAT": 30, "EGG": 10},
    "fert_gate": 45,
    "endgame_start": 28,
}

NEAR_BAND_PARAMS: Dict = {
    "name": "near_band_diversified",
    "provenance": "500-900 band, 2 games / 2 independent players: Sooriya Senthilkumar "
                  "(ep 102194478), Chirag Bhatnagar (ep 102196708)",
    "exploratory_params": True,
    "exploratory_note": "only 2 profiled games (1 per player), but both independent "
                        "players converge on the same strawberry-led diversified "
                        "structure -- included because it represents the real online "
                        "distribution near our ladder position, per blueprint m2",
    "hire_mode": "ramp",
    "hire_ramp": ((0, 4), (6, 8), (12, 10)),           # -> ~262 hires = 8.7/day
    "hire_cap": 11,
    "hire_until_hour": 6,
    "target_quads": 4,                                  # Sooriya unlocked all 4
    "quad_min_day": (7, 10, 12),
    "quad_reserve": (450, 650, 900),
    "herd": {"COW": 8, "SHEEP": 3, "GOOSE": 2},
    "animal_reserve": 350,
    # strawberry-led rotation: Sooriya straw 51.8%/melon 28.4%, Chirag straw 33.7%
    "wheat_share_mode": "fixed",
    "wheat_share": 0.35,
    "wheat_share_ladder": None,
    "tiles_per_quad": 22,
    "tiles_per_unit": 5.5,
    "money_crop_caps": {"STRAWBERRY": 30, "MELON": 14, "TOMATO": 10},
    "money_crop_min_price": {"STRAWBERRY": 70, "MELON": 150, "TOMATO": 45},
    "crop_phase": {"MELON": (0, 17), "STRAWBERRY": (0, 14), "TOMATO": (16, 21)},
    "feed_mode": "gap",
    "feed_gate": 40,
    "feed_cheap_at": 33,
    "feed_daily_base": 12,
    "feed_cheap_extra": 0,
    "feed_cover_days": 1.3,
    "wheat_sell_keep": 6,
    # premium strawberry gate (their medians 221-250) + heavy endgame dumping
    "sell_gates": {"MILK": 120, "WOOL": 130, "STRAWBERRY": 150, "MELON": 180,
                   "WHEAT": 24, "EGG": 45},
    "sell_tranches": {"MILK": 12, "WOOL": 10, "STRAWBERRY": 10, "MELON": 10,
                      "WHEAT": 40, "EGG": 12},
    "fert_gate": 45,
    "endgame_start": 27,                                # Chirag endgame share 17.7%
}

SCALE_RANCH_PARAMS: Dict = {
    "name": "scale_ranch",
    "provenance": "round-2 winners cross-profile (arminhej96 ep102399852 100559, "
                  "朝闻夕死 ep102402115 95087, Danila Galkin ep102406576 98770; "
                  "replays .tmp-online/round2/) validated against the top-20 corpus "
                  "(58 episodes / 116 seats: Crop Dusta 26 g, Milan Leonard 12 g, "
                  "Ryo Hasegawa 16 g) -- r3-1 deep dive, "
                  "exports/online/round2_winner_deep_dive.md",
    "exploratory_params": False,
    # labour: crew 12 from day 7 (all three winners hold 12 hands from d7-11;
    # top-20 hires 282-295 = 9.4-9.9/day).  Day 0 runs a lean 6-hand crew so
    # the herd burst keeps ~2000 of the 3000 start (arminhej96 d0: 4 hands,
    # 5 cows, 340 money left).
    "hire_mode": "ramp",
    "hire_ramp": ((0, 6), (7, 12)),
    "hire_cap": 12,
    "hire_until_hour": 6,
    # land: 3 quadrants, NE ~d5-7 / SW ~d8-11 (winners NE d6-9 / SW d8-11;
    # Crop Dusta NE ~5 / SW ~8 across 26 games; Milan NE 6 / SW 11 across 12).
    # The 4th quadrant is arminhej96's single-game quirk: 115/116 top-20
    # seats stay at 3 quadrants, so it is NOT modelled.
    "target_quads": 3,
    "quad_min_day": (4, 7, 10),
    "quad_reserve": (350, 500, 800),
    # herd: 8 cows + 6 sheep = 14 head (winners peak 13-17: 5C+9S, 9C+4S,
    # 8C+9S; top-20 median 12 / p75 15, Crop Dusta median 16, Subramanya 16).
    # animal_reserve 600 leaves exactly the observed day-0 burst budget:
    # after the 6-hand morning crew (fib cost 20) the 3000 start buys 5 cows
    # at the 1000 buy gate (2000 spent, ~500 for seeds) -- all 116 top-20
    # seats hold 4-5 animals on day 0 (Crop Dusta 5 head in 25/26 games) and
    # reach 12+ by day 4-7; all three winners buy 5 head on day 0 and
    # complete the herd by day 8-11.  Sheep follow at the 1100 gate once the
    # cows' milk + fertilizer income arrives (arminhej96: 9 sheep on day 8).
    "herd": {"COW": 8, "SHEEP": 6, "GOOSE": 0},
    "animal_reserve": 600,
    # field: wheat base 32% (winners 8-19 live wheat tiles / 35-50% share --
    # the low end, because the herd's feed comes from the market too; top-20
    # 42-50% with self-feeding herds)
    "wheat_share_mode": "fixed",
    "wheat_share": 0.32,
    "wheat_share_ladder": None,
    "tiles_per_quad": 22,
    "tiles_per_unit": 5.5,
    # strawberry is the mid-game money engine: winners plant 6-8 tiles on
    # d7-d11 (arminhej d11, 朝闻夕死 d7, Danila d7) and ramp to 16-23 by
    # d11-13, realising 208-246/unit; top-20 reach 6+ tiles by d4-7 and peak
    # 33-37.  Cap 16 sits at the winner floor, one notch below the top-20
    # field share (a bigger field starves the feed/care crews); the day-5
    # phase keeps the day-0 cash on the herd burst.  Melon 8-10 tiles d0-17
    # (winners 8/8/17-19, top-20 median 13).
    "money_crop_caps": {"STRAWBERRY": 16, "MELON": 8},
    "money_crop_min_price": {"STRAWBERRY": 60, "MELON": 130},
    "crop_phase": {"MELON": (0, 17), "STRAWBERRY": (5, 14)},
    # feed: guardrailed gap-fill (winners 102-462u external @ avg 33-34,
    # i.e. a 15u/day cadence at the Danila end; Danila stockpiled 256u on
    # d1-2 while wheat was cheap -- the cheap_extra stock-up reproduces
    # this; top-20 spans 60-2732u, so the magnitude itself is a style knob,
    # only the guardrail is a ticket)
    "feed_mode": "gap",
    "feed_gate": 38,
    "feed_cheap_at": 30,
    "feed_daily_base": 15,
    "feed_cheap_extra": 40,
    "feed_cover_days": 1.3,
    "wheat_sell_keep": 10,
    # care: full-coverage discipline -- winners issue CARE for every animal
    # every day from day 0 (arminhej96 23-32 issued/day at 14 head, executed
    # cares are capped at head by the engine), top-20 CARE p25 268.  Weight
    # above routine water/plant, below urgent water and harvest.
    "care_weight": 70,
    # seeds keep the next animal buy liquid while the herd builds (the
    # winners' day-0 split: 5 cows first, wheat from the leftovers,
    # strawberry only once the fertilizer/wheat income arrives)
    "seed_cash_floor": 1100,
    # sells: premium milk like 朝闻夕死/Danila (realised 207-212) and a mid
    # wool gate (arminhej 241 hoarded / Danila 116); strawberry 208-246 and
    # melon 199-231 are always premium; fertilizer streams daily (winners
    # 61-85 realised, 9.8-18.5k revenue).
    "sell_gates": {"MILK": 190, "WOOL": 110, "STRAWBERRY": 150, "MELON": 170,
                   "WHEAT": 30, "EGG": 40},
    "sell_tranches": {"MILK": 12, "WOOL": 10, "STRAWBERRY": 10, "MELON": 10,
                      "WHEAT": 40, "EGG": 10},
    "fert_gate": 45,
    "endgame_start": 28,    # winners stop feeding/planting and liquidate d28-29
}

WHEAT_STRAW_MONSTER_PARAMS: Dict = {
    "name": "wheat_straw_monster",
    "provenance": "round-3 public-ladder winners that beat the r4 candidate "
                  "by 20-34k (Renji Starfall ep102549493 109695: crew 10 from "
                  "d0 / 12 from d12, NE+SW both on d10, strawberry burst 28+4 "
                  "tiles d11-12 to a 42-tile peak, wheat money crop replanted "
                  "all season 1508u sold @ avg 37.7, external feed 1501u, "
                  "d12=6052 d24=56055; DevilQ ep102558469 96629: 14 cows, "
                  "strawberry 33 peak d8-14, melon 21, wheat 429u sold, feed "
                  "532u; replays .tmp-online/round3/, deep stats "
                  ".tmp-online/round3/monster_deep_stats.json)",
    "exploratory_params": False,
    # labour: crew 10 from day 0 (Renji hires 10 on d0 itself -- the field
    # economy needs the hands before the land does), 12 from d12 (Renji's
    # step-up when the 42-tile field lands; DevilQ ramps 5->9->12)
    "hire_mode": "ramp",
    "hire_ramp": ((0, 10), (12, 12)),
    "hire_cap": 12,
    "hire_until_hour": 6,
    # land: both extra quadrants on day 10 (Renji bought NE and SW the same
    # day -- the strawberry burst needs the tiles, not an early quadrant;
    # DevilQ NE d8 / SW d18 brackets it)
    "target_quads": 3,
    "quad_min_day": (8, 10, 12),
    "quad_reserve": (400, 550, 800),
    # herd: cow-led, 12 head (Renji 6C+2S mild, DevilQ 14 cows -- the
    # monster band treats animals as the cash floor, not the ceiling)
    "herd": {"COW": 10, "SHEEP": 2, "GOOSE": 0},
    "animal_reserve": 500,
    # field: wheat money crop base 25% of a near-fully-farmed 3-quad field
    # (Renji replants wheat continuously -- 52u/day sold; DevilQ peak 24
    # tiles; the log curve absorbs the volume)
    "wheat_share_mode": "fixed",
    "wheat_share": 0.25,
    "wheat_share_ladder": None,
    "tiles_per_quad": 24,
    "tiles_per_unit": 5.5,
    # the strawberry BURST: 42-tile ceiling planted in the d9-14 window
    # after the second quadrant lands (Renji 7 probe tiles d1 then 32 in
    # d10-12; DevilQ 33 across d8-14); melon 10-21 alongside
    "money_crop_caps": {"STRAWBERRY": 42, "MELON": 12},
    "money_crop_min_price": {"STRAWBERRY": 60, "MELON": 140},
    "crop_phase": {"MELON": (0, 17), "STRAWBERRY": (9, 14)},
    # feed: heavy external buying at a wide guardrail (Renji 1501u @ 37.7
    # avg / 56.5k spend; DevilQ 532u @ 40.4 -- the wheat field sells, the
    # herd eats from the market)
    "feed_mode": "gap",
    "feed_gate": 45,
    "feed_cheap_at": 32,
    "feed_daily_base": 30,
    "feed_cheap_extra": 60,
    "feed_cover_days": 1.5,
    "wheat_sell_keep": 8,
    # care: full coverage (DevilQ 423 issued ~= head x days; Renji keeps
    # CARE lean because the herd is small -- the weight stays high so the
    # cash floor never starves)
    "care_weight": 70,
    # seeds stay liquid behind the herd/land burst (Renji d1: 7 straw +
    # 4 wheat + 1 cow from the 3000 start)
    "seed_cash_floor": 900,
    # sells: wheat is the volume line (52u/day), strawberry/melon premium
    # tranches, milk cleared through (Renji 126 milk / DevilQ 286)
    "sell_gates": {"MILK": 150, "WOOL": 110, "STRAWBERRY": 100, "MELON": 160,
                   "WHEAT": 28, "EGG": 40},
    "sell_tranches": {"MILK": 14, "WOOL": 10, "STRAWBERRY": 12, "MELON": 10,
                      "WHEAT": 44, "EGG": 10},
    "fert_gate": 45,
    "endgame_start": 27,    # DevilQ still replants wheat d23-26; dump d27+
}


TWO_QUAD_DENSER_PARAMS = {
    "name": "two_quad_denser",
    "provenance": "round-4 public-ladder winner that beat the v6 candidate "
                  "by 5.2k with the BEST fundamentals seen online (Sam Scott "
                  "ep102685729 97616 vs our 92465: exactly 2 quadrants "
                  "(NE on d8, SW/SE never), 9C+6S+2G=17 head, wheat field "
                  "steady at 17-23 tiles ALL season, strawberries only 6-8 "
                  "tiles, weeds 0-4 vs our 6-48, d0 hands 8 -> 12 from d8, "
                  "d12 money 4492 vs our 50, external feed 322u, fertilizer "
                  "334u sold as an income line, endgame d24->d29 +38.8k; "
                  "replay .tmp-online/round4/episode-102685729-replay.json)",
    "exploratory_params": False,
    # labour: 8 hands from day 0 (Sam d0 end: hands 8, money 348 -- the
    # wheat field needs the crew before the second quadrant exists), 12
    # hands from the d8 NE step-up
    "hire_mode": "ramp",
    "hire_ramp": ((0, 8), (8, 12)),
    "hire_cap": 12,
    "hire_until_hour": 6,
    # land: exactly TWO quadrants -- NE on day 8 once the cow ramp lands
    # (d7 money 4792 funds it); SW/SE never: the land money feeds the herd
    # and the wheat field density instead
    "target_quads": 2,
    "quad_min_day": (8, 99, 99),
    "quad_reserve": (600, 0, 0),
    # herd: 9C+6S+2G = 17 head (d0 opens sheep-led 3S+1C/1200; cows ramp
    # d5-8 to 9; +3 sheep on d16 close it at 17 -- the egg line rides on
    # 2 geese and sheep wool scales with the wheat-feed capacity)
    "herd": {"COW": 9, "SHEEP": 6, "GOOSE": 2},
    "animal_reserve": 450,
    # field: the wheat line IS the economy -- 17-23 tiles steady on a
    # 2-quad field (~40% share; feed floor + cash volume at the log curve)
    "wheat_share_mode": "fixed",
    "wheat_share": 0.40,
    "wheat_share_ladder": None,
    "tiles_per_quad": 24,
    "tiles_per_unit": 5.5,
    # money crops stay SMALL: strawberry 6-8 tiles from d8 (NE lands d8,
    # first straw production d17-18), early carrot probe d4-7 (7 tiles);
    # NO melon (Sam planted zero)
    "money_crop_caps": {"STRAWBERRY": 8, "MELON": 0, "CARROT": 7},
    "money_crop_min_price": {"STRAWBERRY": 60, "MELON": 140, "CARROT": 20},
    "crop_phase": {"STRAWBERRY": (8, 16), "MELON": (0, 17), "CARROT": (3, 8)},
    # feed: external wheat at a tight guardrail (322u over 121 orders,
    # avg ~2.7u -- a constant drip, not the monster's bulk buying)
    "feed_mode": "gap",
    "feed_gate": 40,
    "feed_cheap_at": 30,
    "feed_daily_base": 12,
    "feed_cheap_extra": 24,
    "feed_cover_days": 1.5,
    "wheat_sell_keep": 8,
    # care: full coverage (CARE 314 ~= head x days; weeds 0-4 all season --
    # the discipline line this archetype pins)
    "care_weight": 70,
    # cash-tracked from a lean opening (d0 end money 348)
    "seed_cash_floor": 400,
    # sells: milk/wool/egg cleared through in small tranches (20/19/16
    # orders), fertilizer is an income line (334u sold, gate 40), wheat
    # sold at 28+ in 16u tranches, strawberry premium (only 19u -- the
    # 6-8 tile field is a side line, not the engine)
    "sell_gates": {"MILK": 140, "WOOL": 120, "STRAWBERRY": 100, "MELON": 160,
                   "WHEAT": 28, "EGG": 35, "FERTILIZER": 40},
    "sell_tranches": {"MILK": 12, "WOOL": 8, "STRAWBERRY": 8, "MELON": 10,
                      "WHEAT": 16, "EGG": 6, "FERTILIZER": 12},
    "fert_gate": 40,
    "endgame_start": 25,    # straw cleared by d26, wheat harvest-only d28-29
}


def _dist(ax: int, ay: int, bx: int, by: int) -> int:
    return abs(ax - bx) + abs(ay - by)


def _step_towards(fx: int, fy: int, tx: int, ty: int) -> List[str]:
    dx, dy = tx - fx, ty - fy
    if dx == 0 and dy == 0:
        return ["PASS"]
    if abs(dx) >= abs(dy) and dx != 0:
        return ["EAST"] if dx > 0 else ["WEST"]
    return ["SOUTH"] if dy > 0 else ["NORTH"]


def _shed_tiles(board: int) -> Tuple[Tuple[int, int], ...]:
    h = board // 2
    return ((h - 1, h - 1), (h, h - 1), (h - 1, h), (h, h))


def _shed_adjacent(x: int, y: int, board: int) -> bool:
    return (x, y) in _shed_tiles(board)


def _hire_cost(already_hired_today: int) -> int:
    """Engine fib schedule: 1, 1, 2, 3, 5, 8, 13, ... per hire that day."""
    a, b = 1, 1
    for _ in range(max(0, already_hired_today)):
        a, b = b, a + b
    return a


def _hire_target(day: int, quads: int, p: Dict) -> int:
    if p["hire_mode"] == "quad_scaled":
        return min(p["hire_cap"], p["hires_per_quadrant"] * max(1, quads))
    target = p["hire_cap"]
    for from_day, hands in p["hire_ramp"]:
        if day >= from_day:
            target = hands
    return min(p["hire_cap"], target)


def _wheat_share(p: Dict, wheat_price: float) -> float:
    if p["wheat_share_mode"] == "fixed":
        return p["wheat_share"]
    for threshold, share in p["wheat_share_ladder"]:
        if wheat_price >= threshold:
            return share
    return p["wheat_share_ladder"][-1][1]


def _market_orders(state: Dict, p: Dict) -> List[list]:
    """Build the <=10 market orders for this turn.

    Priority: labour > land > herd > feed > seeds > gated sells.  Buys come
    first because a dropped sell tranche simply repeats next turn, while a
    dropped HIRE/BUY_LAND loses a whole day of the plan.
    """
    day, hour = state["day"], state["hour"]
    money, shed, seeds = state["money"], state["shed"], state["seeds"]
    prices = state["prices"]
    endgame = day >= p["endgame_start"]
    last_day = day >= SEASON_DAYS - 1
    orders: List[list] = []

    if endgame:
        # endgame hoard-dump window: liquidate the shed, buy nothing
        for item in ("STRAWBERRY", "MELON", "MILK", "WOOL", "WHEAT", "TOMATO",
                     "EGG", "FERTILIZER", "CARROT"):
            if shed.get(item, 0) > 0:
                orders.append(["SELL", item, shed[item]])
        return orders[:10]

    # ---- buys: labour, land, herd, feed, seeds ------------------------------
    # cash_tracked (opt-in via seed_cash_floor, scale_ranch): approximate the
    # engine's intra-turn sequential commits so later orders in the SAME turn
    # see the cash the earlier ones already spent -- the default bots keep
    # the historical turn-start-money behaviour byte-for-byte.
    cash_tracked = p.get("seed_cash_floor") is not None
    cash = money
    hire_target = _hire_target(day, state["quads"], p)
    # hiring takes one turn per hand: keep the morning window open long
    # enough for the full daily crew (the profiles' 9.4-9.9 hires/day); the
    # money gate uses the exact fib cost so a lean day still hires the
    # cheap early hands
    if hour <= max(p["hire_until_hour"], hire_target + 2) \
            and len(state["hands"]) < hire_target \
            and money >= _hire_cost(len(state["hands"])):
        orders.append(["HIRE"])

    # land plan: while a quadrant purchase is due, protect its cash from the
    # herd buys below (working capital -- seeds/feed -- is never blocked: it
    # is what pays for the land; the top-20 series unlock NE/SW on schedule)
    quads = state["quads"]
    land_pending = False
    land_fund = 0
    if quads < p["target_quads"]:
        idx = quads - 1                                # next land cost index
        cost = LAND_COSTS[idx] if idx < len(LAND_COSTS) else None
        if cost is not None and day >= p["quad_min_day"][idx]:
            land_fund = cost + p["quad_reserve"][idx]
            land_pending = True
            if money >= land_fund:
                orders.append(["BUY_LAND"])

    # herd growth is subordinated to the quadrant plan; animals may wait in
    # the shed until a pen is built and placed (the owned count includes the
    # shed, so the buy gate self-limits)
    if day <= SEASON_DAYS - 3:
        for animal, target in sorted(p["herd"].items()):
            if target <= 0 or len(orders) >= 8:
                continue
            owned = state["animals_alive"].get(animal, 0) + shed.get(animal, 0) \
                + sum((inv or {}).get(animal, 0) for inv in state["inventories"])
            if owned >= target:
                continue
            budget = land_fund + ANIMALS_INFO[animal]["cost"] + p["animal_reserve"]
            if cash_tracked:
                if cash >= budget:
                    orders.append(["BUY_ANIMAL", animal, 1])
                    cash -= ANIMALS_INFO[animal]["cost"]
            elif money >= budget:
                orders.append(["BUY_ANIMAL", animal, 1])

    # external feed wheat under the price guardrail: buy the herd's gap only,
    # plus a bounded stock-up while the price is cheap (per-day cadence from
    # the profile the bot models; magnitude capped by the live herd size)
    if not last_day:
        wheat_price = prices.get("WHEAT", 25)
        if wheat_price <= p["feed_gate"]:
            stock = shed.get("WHEAT", 0) + sum((inv or {}).get("WHEAT", 0)
                                               for inv in state["inventories"])
            if p.get("feed_mode") == "fixed":
                # fixed per-day ration, ordered once in the morning: the
                # template cluster's constant 414-436u/season cadence
                if hour <= 1 and stock < state["animals_alive_total"] + 10:
                    qty = p["feed_daily_base"]
                else:
                    qty = 0
            else:
                cover = round(state["animals_alive_total"] * p["feed_cover_days"]) + 2
                qty = min(p["feed_daily_base"], max(0, cover - stock))
                if wheat_price <= p["feed_cheap_at"]:
                    qty = max(qty, min(p["feed_cheap_extra"],
                                       max(0, state["animals_alive_total"] * 2 - stock)))
            qty = max(0, min(qty, max(0, 90 - sum(v for v in shed.values()
                                                  if isinstance(v, (int, float))))))
            if qty > 0 and money >= wheat_price * min(qty, 4):
                orders.append(["BUY_PRODUCT", "WHEAT", qty])
        fert_gate = p.get("fert_buy_gate")
        if fert_gate is not None and prices.get("FERTILIZER", 100) <= fert_gate \
                and state["wheat_alive"] > 0 and day <= SEASON_DAYS - 6:
            orders.append(["BUY_PRODUCT", "FERTILIZER", p["fert_buy_daily"]])

    # seeds: the feed base first, then the largest deficits (orders are
    # scarce and money crops must not crowd out the wheat field).
    # seed_cash_floor (opt-in, scale_ranch): while the herd is incomplete,
    # cap seed quantities so the turn keeps `floor` cash for the next animal
    # buy -- reproduces the winners' "cows first, seeds from the leftovers"
    # day-0 split (arminhej96: 5 cows + 12 wheat tiles, 340 money left).
    herd_pending = sum(state["animals_alive"].get(a, 0) + shed.get(a, 0)
                       + sum((inv or {}).get(a, 0)
                             for inv in state["inventories"])
                       for a, target in p["herd"].items()
                       if target > 0) < sum(n for n in p["herd"].values())
    seed_floor = p.get("seed_cash_floor", 0) if herd_pending else 0
    deficits = []
    for crop, target in state["plan"]:
        want = target - state["crops_alive"].get(crop, 0) - seeds.get(crop, 0)
        seed_cost = CROPS_INFO[crop]["seed"]
        if want > 0 and money >= seed_cost * 2:
            deficits.append({"crop": crop, "want": want})
    deficits.sort(key=lambda d: (d["crop"] != "WHEAT", -d["want"]))
    for d in deficits[:3]:
        seed_cost = CROPS_INFO[d["crop"]]["seed"]
        qty = min(d["want"], 12)
        if seed_floor:
            qty = min(qty, max(0, int((cash - seed_floor) // seed_cost)))
        if qty > 0:
            orders.append(["BUY_SEED", d["crop"], qty])
            if cash_tracked:
                cash -= qty * seed_cost

    # ---- sells: gated tranches with shed-pressure fallback ------------------
    shed_count = sum(v for v in shed.values() if isinstance(v, (int, float)))
    feed_keep = p.get("wheat_sell_keep", 6) if not last_day else 0
    for item, gate in p["sell_gates"].items():
        if len(orders) >= 10:
            break
        held = shed.get(item, 0)
        if held <= 0:
            continue
        eff_gate = gate
        tranche = p["sell_tranches"].get(item, 10)
        if item == "WHEAT":
            # the online signature: sell the own wheat crop down to a small
            # feed buffer and buy feed on the market instead
            held = max(0, held - feed_keep)
            if held <= 0:
                continue
        if shed_count >= 80:
            eff_gate = 1                             # shed-cap protection
        if prices.get(item, 0) >= eff_gate:
            orders.append(["SELL", item, min(held, tranche)])
    if len(orders) < 10 and shed.get("FERTILIZER", 0) > 0 \
            and prices.get("FERTILIZER", 0) >= p["fert_gate"]:
        orders.append(["SELL", "FERTILIZER", shed["FERTILIZER"]])
    return orders[:10]


def _field_plan(state: Dict, p: Dict) -> List[Tuple[str, int]]:
    """Target concurrent tile counts per crop (wheat floor + money crops)."""
    day = state["day"]
    prices = state["prices"]
    units = 1 + len(state["hands"])
    quads = state["quads"]
    max_tiles = min(int(p["tiles_per_quad"] * quads),
                    max(8, int(p["tiles_per_unit"] * units)))
    if day >= p["endgame_start"]:
        return []
    share = _wheat_share(p, prices.get("WHEAT", 25))
    wheat_target = round(max_tiles * share)
    plan: List[Tuple[str, int]] = [("WHEAT", wheat_target)]
    for crop, cap in sorted(p["money_crop_caps"].items()):
        phase = p["crop_phase"].get(crop, (0, PLANT_DEADLINE.get(crop, 20)))
        if not (phase[0] <= day <= min(phase[1], PLANT_DEADLINE.get(crop, 20))):
            continue
        if prices.get(crop, 0) < p["money_crop_min_price"].get(crop, 1):
            continue
        scaled = round(cap * min(1.0, quads / max(1, p["target_quads"] - 1)))
        plan.append((crop, max(0, min(cap, scaled))))
    return plan


def online_style_agent(obs: Dict, p: Dict) -> Dict:
    player = obs.get("player", 0)
    farms = obs.get("farms", []) or []
    private = obs.get("private", {}) or {}
    if not farms or player >= len(farms):
        return {"farmer": ["PASS"], "hands": [], "market": []}
    farm = farms[player]
    tiles = farm.get("tiles", []) or []
    board = len(tiles)
    if not board:
        return {"farmer": ["PASS"], "hands": [], "market": []}

    day = obs.get("day", 0)
    hour = obs.get("hour", 0)
    money = farm.get("money", 0.0)
    seeds = private.get("seeds", {}) or {}
    shed = private.get("shed", {}) or {}
    inventories = [inv or {} for inv in (private.get("inventories") or [])]
    prices = ((obs.get("market", {}) or {}).get("prices", {}) or {})
    fx, fy = farm.get("farmer", [board // 2 - 1, board // 2 - 1])
    hands = [tuple(h) for h in (farm.get("hands", []) or [])]
    quads = len(farm.get("unlocked_quadrants", []) or ["NW"])
    endgame = day >= p["endgame_start"]
    last_day = day >= SEASON_DAYS - 1
    sx, sy = board // 2 - 1, board // 2 - 1

    # ---- read the ground ---------------------------------------------------
    empty: List[Tuple[int, int]] = []
    structures: Dict[str, List[Tuple[int, int]]] = {"PASTURE": [], "COOP": []}
    empty_structures: List[Tuple[int, int]] = []
    crops_alive: Dict[str, int] = {}
    animals_alive: Dict[str, int] = {}
    animals_to_feed = 0
    wheat_alive = 0
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile == "LOCKED" or tile is None:
                if tile is None:
                    empty.append((x, y))
                continue
            if not isinstance(tile, dict):
                continue
            kind = tile.get("kind")
            if kind == "WEED":
                continue
            if kind == "PLANT":
                crop = tile.get("crop", "")
                crops_alive[crop] = crops_alive.get(crop, 0) + 1
                if crop == "WHEAT":
                    wheat_alive += 1
            elif kind in structures:
                structures[kind].append((x, y))
                if "animal" not in tile:
                    empty_structures.append((x, y))
                else:
                    animals_alive[tile["animal"]] = animals_alive.get(tile["animal"], 0) + 1
                    if not tile.get("fed_today", False):
                        animals_to_feed += 1
    animals_total = sum(animals_alive.values())
    empty.sort(key=lambda pos: (_dist(sx, sy, pos[0], pos[1]), pos[1], pos[0]))

    state = {
        "day": day, "hour": hour, "money": money, "shed": shed, "seeds": seeds,
        "prices": prices, "hands": hands, "quads": quads,
        "inventories": inventories, "animals_alive": animals_alive,
        "animals_alive_total": animals_total, "crops_alive": crops_alive,
        "wheat_alive": wheat_alive, "structures_total": {
            kind: len(positions) for kind, positions in structures.items()},
    }
    state["plan"] = _field_plan(state, p)
    cash_tracked = p.get("seed_cash_floor") is not None

    # ---- task list ----------------------------------------------------------
    tasks: List[Dict] = []

    def add(w, x, y, act, key, need=None):
        tasks.append({"w": w, "x": x, "y": y, "act": act, "key": key, "need": need})

    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict):
                continue
            kind = tile.get("kind")
            if kind == "WEED":
                add(20, x, y, ["DIG"], ("dig", x, y))
                continue
            if kind == "PLANT":
                crop = tile.get("crop", "")
                cd = CROPS_INFO.get(crop)
                if cd is None:
                    continue
                age = day - tile.get("planted_day", day)
                if not endgame and not tile.get("watered_today", False):
                    window_lo = (cd["max_yield_day"] + 1) // 2
                    if tile.get("consecutive_unwatered", 0) >= 1:
                        add(98, x, y, ["WATER"], ("water", x, y))
                    elif cd["ongoing"] or window_lo <= age <= cd["max_yield_day"]:
                        add(42, x, y, ["WATER"], ("water", x, y))
                yu = tile.get("yield_units", 0)
                if yu > 0:
                    if cd["ongoing"]:
                        if yu >= 3 or endgame:
                            add(70, x, y, ["HARVEST"], ("harv", x, y))
                    else:
                        ready = age >= HARVEST_AGE.get(crop, 4) or endgame
                        if ready:
                            add(74 if crop == "MELON" else 72, x, y,
                                ["HARVEST"], ("harv", x, y))
            elif "animal" in tile:
                if not last_day:
                    if not tile.get("fed_today", False):
                        if tile.get("consecutive_unfed", 0) >= 1:
                            w = 110 if cash_tracked else 100
                        else:
                            w = 96 if cash_tracked else 90
                        add(w, x, y, ["FEED"], ("feed", x, y), need="WHEAT")
                    if not tile.get("cared_today", False) and tile.get("fed_today", False):
                        add(p.get("care_weight", 30), x, y, ["CARE"], ("care", x, y))
                yu = tile.get("yield_units", 0)
                if yu >= 3 or (yu > 0 and endgame):
                    add(66, x, y, ["HARVEST"], ("harva", x, y))
                if tile.get("fertilizer_available", False) and not last_day:
                    add(38, x, y, ["COLLECT_FERTILIZER"], ("cfert", x, y))

    # structures: build toward herd targets on the empties nearest the shed
    if not endgame and day <= SEASON_DAYS - 4:
        want = {"PASTURE": p["herd"].get("COW", 0) + p["herd"].get("SHEEP", 0),
                "COOP": p["herd"].get("GOOSE", 0)}
        for kind, target_n in want.items():
            room = target_n - len(structures[kind])
            if room <= 0:
                continue
            op = "BUILD_PASTURE" if kind == "PASTURE" else "BUILD_COOP"
            for x, y in empty[:room]:
                add(62, x, y, [op], ("build", x, y))
                empty = [e for e in empty if e != (x, y)]

    # place animals from the shed onto built-but-empty structures
    shed_animals = {a: shed.get(a, 0) + sum(inv.get(a, 0) for inv in inventories)
                    for a in p["herd"] if p["herd"][a] > 0}
    if any(n > 0 for n in shed_animals.values()) and empty_structures:
        for x, y in empty_structures:
            tile = tiles[y][x]
            for animal, n in shed_animals.items():
                if n <= 0:
                    continue
                if ANIMALS_INFO[animal]["structure"] == tile.get("kind"):
                    add(82, x, y, ["PLACE", animal], ("place", x, y), need=animal)
                    break

    # planting: fill toward the plan on the empties nearest the shed
    if not endgame:
        slots = list(empty)
        for crop, target in state["plan"]:
            deficit = target - crops_alive.get(crop, 0)
            if deficit <= 0 or seeds.get(crop, 0) <= 0:
                continue
            for x, y in slots[:deficit]:
                add(28 if crop == "WHEAT" else 32, x, y,
                    ["PLANT", crop], ("plant", x, y, crop))
                slots = [s for s in slots if s != (x, y)]

    # ---- logistics (shed pickups) -------------------------------------------
    wheat_carried = sum(inv.get("WHEAT", 0) for inv in inventories)
    if animals_to_feed > 0 and shed.get("WHEAT", 0) > 0 \
            and wheat_carried < animals_to_feed:
        div = 2 if cash_tracked else 4
        carriers = max(1, (animals_to_feed + div - 1) // div)
        remaining = min(shed["WHEAT"], animals_to_feed + 2)
        for i in range(carriers):
            n = min(4, remaining)
            if n <= 0:
                break
            remaining -= n
            add(95, sx, sy, ["PICKUP", "WHEAT", n], ("pickup_w", i))
    animal_carried = {a: sum(inv.get(a, 0) for inv in inventories)
                      for a in p["herd"] if p["herd"][a] > 0}
    if any(t["act"][0] == "PLACE" for t in tasks):
        if cash_tracked:
            # scale_ranch: a bought-but-unplaced animal produces nothing and
            # blocks the next buy (owned includes the shed), so every animal
            # type gets its own high-priority pickup each turn
            for animal, carried in animal_carried.items():
                if carried == 0 and shed.get(animal, 0) > 0:
                    add(96, sx, sy, ["PICKUP", animal, min(2, shed[animal])],
                        ("pickup_a", animal))
        else:
            for animal, carried in animal_carried.items():
                if carried == 0 and shed.get(animal, 0) > 0:
                    add(93, sx, sy, ["PICKUP", animal, min(2, shed[animal])],
                        ("pickup_a", animal))
                    break

    # ---- schedule units (claim-based, act-here-first) ------------------------
    claimed: set = set()
    units = [(fx, fy)] + hands
    carried_feed_units = wheat_carried

    def unit_inv(i: int) -> Dict:
        while len(inventories) <= i:
            inventories.append({})
        return inventories[i]

    def executable(t: Dict, ui: int) -> bool:
        need = t.get("need")
        if need and unit_inv(ui).get(need, 0) <= 0:
            return False
        x, y = t["x"], t["y"]
        tile = tiles[y][x] if 0 <= y < board and 0 <= x < board else None
        kind = tile.get("kind", "") if isinstance(tile, dict) else None
        op = t["act"][0]
        if op == "WATER":
            return kind == "PLANT" and not tile.get("watered_today", False)
        if op == "HARVEST":
            if kind == "PLANT":
                return tile.get("yield_units", 0) > 0
            return isinstance(tile, dict) and "animal" in tile \
                and tile.get("yield_units", 0) > 0
        if op == "FEED":
            return isinstance(tile, dict) and "animal" in tile \
                and not tile.get("fed_today", False)
        if op == "CARE":
            return isinstance(tile, dict) and "animal" in tile \
                and not tile.get("cared_today", False)
        if op == "COLLECT_FERTILIZER":
            return isinstance(tile, dict) and "animal" in tile \
                and tile.get("fertilizer_available", False)
        if op == "PLANT":
            return tile is None
        if op == "DIG":
            return kind == "WEED"
        if op in ("BUILD_PASTURE", "BUILD_COOP"):
            return tile is None
        if op == "PLACE":
            return isinstance(tile, dict) and kind in ("PASTURE", "COOP") \
                and "animal" not in tile
        if op == "PICKUP":
            return shed.get(t["act"][1], 0) >= 1 \
                and _shed_adjacent(units[ui][0], units[ui][1], board)
        return True

    actions: List[List[str]] = []
    for ui, (ux, uy) in enumerate(units):
        chosen = None
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
            best = None
            for t in tasks:
                if t["key"] in claimed:
                    continue
                if t.get("need") and unit_inv(ui).get(t["need"], 0) <= 0:
                    continue
                score = t["w"] / (1.0 + _dist(ux, uy, t["x"], t["y"]))
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
                actions.append(_step_towards(ux, uy, sx, sy))
        else:
            actions.append(_step_towards(ux, uy, cx, cy))

    # seed-demote guard (engine blocks ALL plants of a crop on over-demand)
    demand: Dict[str, int] = {}
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

    orders = _market_orders(state, p)
    farmer = actions[0] if actions else ["PASS"]
    return {"farmer": farmer, "hands": actions[1:], "market": orders}


def crop_rotator_agent(obs: Dict) -> Dict:
    """Ladder #1 archetype: constant frame, market-adaptive rotation."""
    return online_style_agent(obs, CROP_ROTATOR_PARAMS)


def template_wheat_agent(obs: Dict) -> Dict:
    """Rank 6-28 template archetype: locked 42% wheat + fixed feed cadence."""
    return online_style_agent(obs, TEMPLATE_WHEAT_PARAMS)


def self_feed_ranch_agent(obs: Dict) -> Dict:
    """Ladder #2 archetype: self-fed mixed herd + premium sell gates."""
    return online_style_agent(obs, SELF_FEED_RANCH_PARAMS)


def near_band_diversified_agent(obs: Dict) -> Dict:
    """500-900 band archetype (exploratory params -- see module docstring)."""
    return online_style_agent(obs, NEAR_BAND_PARAMS)


def scale_ranch_agent(obs: Dict) -> Dict:
    """Round-2 winner archetype (r3-1): day-0 herd burst + early strawberry
    + full-coverage CARE + premium gates; the next band above our ladder."""
    return online_style_agent(obs, SCALE_RANCH_PARAMS)


def wheat_straw_monster_agent(obs: Dict) -> Dict:
    """Round-3 winner archetype (r5-P6): crew-10 opening, day-10 double
    quadrant + 42-tile strawberry burst, continuous wheat money crop at
    log-curve volume, market-fed herd -- the 96-110k band that beat the
    r4 candidate online."""
    return online_style_agent(obs, WHEAT_STRAW_MONSTER_PARAMS)


def two_quad_denser_agent(obs: Dict) -> Dict:
    """Round-4 winner archetype (v7.1): Sam Scott ep102685729 -- exactly
    two quadrants, 17-head dairy, a 17-23-tile wheat field as THE economy,
    small strawberry side line, near-zero weeds, fertilizer sold as an
    income line and a +38.8k endgame ramp."""
    return online_style_agent(obs, TWO_QUAD_DENSER_PARAMS)


ONLINE_STYLE_OPPONENTS = {
    "crop_rotator": crop_rotator_agent,
    "template_wheat": template_wheat_agent,
    "self_feed_ranch": self_feed_ranch_agent,
    "near_band_diversified": near_band_diversified_agent,
    "scale_ranch": scale_ranch_agent,
    "wheat_straw_monster": wheat_straw_monster_agent,
    "two_quad_denser": two_quad_denser_agent,
}
ONLINE_STYLE_PARAM_SETS = {
    "crop_rotator": CROP_ROTATOR_PARAMS,
    "template_wheat": TEMPLATE_WHEAT_PARAMS,
    "self_feed_ranch": SELF_FEED_RANCH_PARAMS,
    "near_band_diversified": NEAR_BAND_PARAMS,
    "scale_ranch": SCALE_RANCH_PARAMS,
    "wheat_straw_monster": WHEAT_STRAW_MONSTER_PARAMS,
    "two_quad_denser": TWO_QUAD_DENSER_PARAMS,
}
