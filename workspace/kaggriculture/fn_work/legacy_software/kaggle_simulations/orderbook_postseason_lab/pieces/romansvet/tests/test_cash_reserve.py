"""The purse keeps tomorrow's crew back from today's shopping.

`_derive` used to hand the whole of `view.money - hire_bill` to the land
comparison and then to `budget.grant`, which spends by value per coin until
nothing fits. A day whose candidate list outruns the purse therefore ended on
zero coins -- and a farm on zero coins cannot hire. The fib bill is trivial
(143 coins for ten hands, 2,583 for sixteen) but it is not free, so an agent
that spends itself out every morning fields the farmer alone for the rest of
the season, produces almost nothing, and never earns its way back.

The floor is structural, not a gene: `HIRE_BILLS[n_hire + 1]`, the fib bill of
the crew the day's own enumeration chose, one hand wider. Tomorrow can
therefore always re-field today's crew out of coins already in the bank,
whatever the market does, and can grow it by one. It is void from
`valuation.pay_day()` on, the last day that can still hire, where there is no
tomorrow to hire for and a held coin is a lost one. That day was
`O.LAST_SHED_DAY` while day 29 hired nobody by law and is 29 under the shipped
`plan.DROP_ON` / `plan.HORIZON_DROP_ON` (5b0fcc4; the HORIZON block in
`plan.py` and `cash_reserve`'s own docstring), so the two tests below that name
the boundary read it off `pay_day()` rather than off the constant that used to
equal it.

It binds the hire enumeration as well as the buy side [LAW]. A hand count is a
candidate only if its bill *and* the reserve it implies fit `view.money`;
without that the enumeration spends the reserve on the crew itself, which is
not a hypothetical -- with M1's larger opening development the replay below put
a farm on 7 coins on day 2, where it hired the four hands 7 coins exactly pays
for and never had a coin again.

What the floor does and does not buy, measured against `starter` in the engine
over sixteen games (8 seeds x 2 seats):

* A policy that develops every tile and holds every product -- so it spends the
  purse and earns nothing back -- ran the whole season on **zero coins**: the
  purse hit 0 on day 4 and never moved. With the floor it never reaches zero at
  all. That is `test_a_spend_everything_theta_never_reaches_zero_coins`.
* Crew continuity -- dawn money never below the fib bill of yesterday's crew --
  was violated once in sixteen games and is now violated never.

It does **not** make "at least one hand every day" true, and no reserve could:
a day with coins in the bank and no work worth a hand hires nobody on purpose
[1.5], and a farm whose policy refuses to sell has no coins to hire with
whatever is held back. Bare days are therefore not what these tests count.

**Measured change from M1 (2026-08-25), stated rather than hidden.** Counting a
freshly bought quadrant's tiles as developable doubles what this theta asks for
on day 0: it hires seven hands and orders seeds for fifty tiles instead of
twenty-five, and the opening purse is gone by day 2 either way. Before M1 the
same theta recovered on day 14, when its own shed finally overflowed and forced
a sale; with M1 the early crew is spent on the opening order instead, few
enough tiles are worked that the shed never overflows, and the farm runs the
rest of the season on the farmer alone at a floor of 2 coins. The reserve is
doing its job -- the purse never empties and yesterday's crew is always
re-fieldable -- but it cannot manufacture income for a policy that will not
sell, so what is asserted below is the floor and the continuity, not a hand
count.
"""
from __future__ import annotations

import os
import sys

import _pin

# `kagg3` FIRST, out of the tree this process is meant to measure: the
# shared fixtures below do their own `sys.path.insert(0, "src")` and import
# `kagg3` on the way in, so a module that imported one of them first loaded
# THIS tree into a `--digests` subprocess and pinned the tree against itself
# (`tests/_pin.py`).
_pin.bootstrap()

import numpy as np
import pytest
from test_budget_order import _macro, _view, geese
from test_hire_bill import _buy_bill, _hire_bill

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import policy as PO
from kagg3.core import valuation as VAL

#: The `_with_free_coops` shape from `test_hire_bill`: land plus geese, the
#: cheapest of which costs 300, so "the greedy spent everything it was given"
#: is `leftover < 300`.
CHEAPEST_CANDIDATE = int(spec.ANIMAL_COST[0])


def _hires(op):
    return int((op == O.MO_HIRE).sum())


def _board(money, n_coops=5, n_ripe=0, day=13):
    z = np.zeros(spec.N_TILES, np.int32)
    view = _view(money, nquad=1)._replace(day=np.int32(day))
    kind, occ, t_yield, t_fert = (view.kind.copy(), view.occ.copy(),
                                  view.t_yield.copy(), view.t_fert.copy())
    kind[:n_coops] = spec.KIND_COOP
    if n_ripe:
        s = slice(n_coops, n_coops + n_ripe)
        kind[s], occ[s], t_yield[s], t_fert[s] = spec.KIND_PLANT, spec.I_TOMATO, 1, day
    return view._replace(kind=kind, occ=occ, t_yield=t_yield, t_fert=t_fert,
                         t_day=z.copy())


def test_a_hand_count_the_reserve_cannot_cover_is_not_a_candidate():
    """The enumeration will not spend the reserve on the crew [LAW].

    Seven coins buys four hands outright (`HIRE_BILLS[4] == 7`) and nothing
    else; with the reserve it buys two, because three hands plus the reserve
    the third implies is 4 + 7 = 11. Measured on the engine replay below as the
    difference between a farm that ends the season on 2 coins and one that ends
    it on none."""
    view = _board(7, n_coops=0, n_ripe=20, day=13)
    macro = _macro()
    n = _hires(P.build_day(np, view, macro)[3])
    assert int(P.HIRE_BILLS[n]) + int(P.cash_reserve(np, np.int32(n), view.day)) <= 7
    assert n < 4, "the enumeration hired a crew it cannot re-field tomorrow"


def test_the_reserve_covers_tomorrows_crew_and_one_more_hand():
    for n in range(spec.MAX_HANDS + 1):
        r = int(P.cash_reserve(np, np.int32(n), np.int32(0)))
        assert r >= int(P.HIRE_BILLS[n]), "tomorrow cannot re-field today's crew"
        assert r == int(P.HIRE_BILLS[min(n + 1, spec.MAX_HANDS)])
    # monotone in the crew size, so a bigger crew is a bigger commitment
    rs = [int(P.cash_reserve(np, np.int32(n), np.int32(0))) for n in range(spec.MAX_HANDS + 1)]
    assert rs == sorted(rs)


def test_the_reserve_is_void_once_there_is_no_tomorrow_to_hire_for():
    """The last day that can hire has nothing to reserve for, and that day is
    `valuation.pay_day()`.

    It used to be `O.LAST_SHED_DAY` = 28, because day 29 banked nothing and so
    hired nobody by law [LAW, 0.4]. `plan.DROP_ON` gave day 29 a crew again --
    HARVEST -> walk home -> DROP -> `SELL_TURNS[-1]` closes inside the day --
    and `plan.HORIZON_DROP_ON` (761c196, shipped on by 5b0fcc4; the HORIZON
    block in `plan.py`) moved the horizon with it: every `HIRE_TURNS` row
    resolves before `SELL_TURNS[0]`, so day 29's crew is paid out of coins day
    28 carried overnight and day 28 holds the bill back like any other day.

    The property is untouched -- a coin held past the last day that can hire is
    a coin thrown away -- so it is asserted against `pay_day()` instead of the
    constant that used to equal it. `tests/test_horizon_drop.py` pins the flip
    day itself under both settings of the switch.
    """
    pay = int(VAL.pay_day())
    for day in (pay, pay + 1):
        assert int(P.cash_reserve(np, np.int32(spec.MAX_HANDS), np.int32(day))) == 0
    assert int(P.cash_reserve(np, np.int32(0), np.int32(pay - 1))) > 0


def _accounting(view, macro):
    op = P.build_day(np, view, macro)[3]
    n = _hires(op)
    reserve = int(P.cash_reserve(np, np.int32(n), view.day))
    return n, reserve, _buy_bill(view, macro)


def _assert_cliff(board, macro, want_cost, day):
    """The purse handed to the buy side is exactly `money - hire_bill - reserve`.

    Asserted as a one-coin cliff rather than as "the greedy spent everything":
    the greedy stops at the day's *wants* as often as at the purse, so a
    leftover proves nothing either way. `want_cost` is what this board actually
    wants to buy, so at `want_cost + hire_bill + reserve` coins the whole want
    is granted and one coin less drops the last item. That pins the reserve to
    the coin -- a reserve of zero, or of anything else, moves the cliff.
    """
    probe = board(want_cost + 100_000, day)
    n, reserve, full = _accounting(probe, macro)
    assert full == want_cost, f"fixture does not want {want_cost}, it wants {full}"
    exact = board(want_cost + _hire_bill(n) + reserve, day)
    short = board(want_cost + _hire_bill(n) + reserve - 1, day)
    for v in (exact, short):
        assert _hires(P.build_day(np, v, macro)[3]) == n, \
            "the fixture's hire count moved with the purse; the cliff is not the reserve's"
    assert _buy_bill(exact, macro) == want_cost
    assert _buy_bill(short, macro) < want_cost
    return reserve


def test_the_purse_is_the_money_less_the_bill_and_the_reserve():
    """On a working day the cliff sits a whole reserve above the bill."""
    macro = _macro(land_bias=np.int32(spec.LAND_PRICES[0]), animal_want=geese(5))
    land_and_geese = int(spec.LAND_PRICES[0]) + 5 * CHEAPEST_CANDIDATE
    for n_ripe in (0, 20):
        board = lambda money, day, r=n_ripe: _board(money, n_ripe=r, day=day)
        assert _assert_cliff(board, macro, land_and_geese, 13) > 0


def test_the_floor_does_not_leak_past_the_last_working_day():
    """The last day that shops still holds a whole reserve; the day the reserve
    is void has no purse for it to leak into.

    This used to be one board and one number: `LAST_SHED_DAY` had no tomorrow
    to hire for, so its cliff sat at the bill with no reserve above it. Under
    the shipped switches (`plan.HORIZON_DROP_ON`, 761c196/5b0fcc4) day 29 hires
    through the DROP enumeration out of coins day 28 carried, so
    `valuation.pay_day()` is 29 and **day 28 reserves like any other day**.

    The two facts the old assertion tied together have come apart, and there is
    no board left that has both halves: `pay_day()` is now also `terminal`
    (`day > LAST_SHED_DAY`), and `build_day` zeroes a terminal day's purse
    outright, so "a live buy side with no floor under it" is not a reachable
    day. What replaces it is the pair that is now true -- the last day that
    shops keeps tomorrow's bill back, and the day the floor lapses buys nothing
    at all, which is the same guarantee that no coin is held past its use and
    none leaks into a purchase.

    Land only: `acquire_ok` [0.2] already refuses a new animal this late, so
    geese are not part of what this board wants and pinning them would be
    testing the horizon rule twice."""
    macro = _macro(land_bias=np.int32(spec.LAND_PRICES[0]))
    board = lambda money, day: _board(money, n_coops=0, day=day)
    reserve = _assert_cliff(board, macro, int(spec.LAND_PRICES[0]), O.LAST_SHED_DAY)
    n = _hires(P.build_day(np, board(100_000, O.LAST_SHED_DAY), macro)[3])
    assert reserve == int(P.cash_reserve(np, np.int32(n), np.int32(O.LAST_SHED_DAY))) > 0

    pay = int(VAL.pay_day())                       # 29: void, and terminal too
    assert int(P.cash_reserve(np, np.int32(spec.MAX_HANDS), np.int32(pay))) == 0
    assert _buy_bill(board(100_000, pay), macro) == 0, "a terminal day went shopping"


# --------------------------------------------------------------- engine replay

def _theta(kind):
    """The three seats these replays use.

    `zero` is `artifacts/zero_theta.npy` -- all zeros, the shipped fallback,
    and rebuilt here rather than loaded so the test does not depend on an
    artifact that `.gitignore` keeps out of the tree. Every head output is then
    its bias, which is zero, so every decode is the neutral one.

    `broke` forces the two decodes that spend a farm to nothing: every free
    tile developed (`dev_frac -> 1`), every developed tile an animal
    (`animal_share -> 1`), and the land bias saturated positive, so a quadrant
    is bought whenever it is affordable and not worth less than its price.

    `hoard` is the same spend-everything front end with the *income* switched
    off -- a high sell score puts the reservation value above every quote, so
    nothing is ever sold and the only coins the farm will ever see are the
    3,000 it starts with. That is the pure form of the failure: the day's
    candidate list always outruns the purse, so before the floor the purse hit
    zero on day 4 and stayed there.
    """
    t = np.zeros(PO.N_PARAMS, np.float32)
    o = PO.offset("gb2")
    if kind in ("broke", "hoard"):
        t[o + 1] = 8.0          # land bias saturated positive
        t[o + 5] = 8.0          # dev_frac -> 1
    if kind == "broke":
        t[o + 6] = 8.0          # animal_share -> 1
    if kind == "hoard":
        t[o + 6] = -8.0         # animal_share -> 0: crops, which are cheap to over-buy
        t[PO.offset("b2") + 1] = 6.0     # sell score high -> hold everything, sell nothing
    return t


def _agent(theta):
    from kagg3.agent import parse, runtime

    def macro(obs, player, view):
        opp = obs["farms"][1 - player]
        vo = parse.parse_view({**obs, "private": {"shed": {}, "seeds": {}}}, 1 - player)
        return brain.decide(np, theta, brain.PolicyObs(
            day=np.int32(view.day), money=view.money, opp_money=np.int32(opp["money"]),
            kind=view.kind, occ=view.occ, opp_kind=vo.kind, opp_occ=vo.occ,
            t_day=view.t_day, t_yield=view.t_yield, shed=view.shed, seeds=view.seeds,
            nquad=view.nquad, opp_nquad=np.int32(len(opp["unlocked_quadrants"])),
            mkt_inv=parse.parse_market(obs)[0], price=view.price,
            shops=parse.parse_town(obs)))
    return runtime.make_agent(macro)


def _season(theta, seed, seat):
    """(hands, dawn money) per day, played against `starter` in the engine.

    Hands are read at hour 4: both hire turns (0 and 2) have resolved by then
    and nothing has escaped yet. Money is read at hour 0, before the day has
    spent anything."""
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": int(seed)})
    me = _agent(theta)
    env.run([me, "starter"] if seat == 0 else ["starter", me])

    def at(step, key):
        farm = env.steps[min(step, len(env.steps) - 1)][0].observation["farms"][seat]
        return len(farm["hands"]) if key == "hands" else int(farm["money"])

    return ([at(d * 24 + 4, "hands") for d in range(spec.N_DAYS)],
            [at(d * 24, "money") for d in range(spec.N_DAYS)])


@pytest.mark.parametrize("seed,seat", [(2104521678, 0), (1164543749, 1)])
def test_a_spend_everything_theta_never_reaches_zero_coins(seed, seat):
    """The bankruptcy itself, replayed in the real engine against `starter`.

    The `hoard` seat spends its purse every morning and sells nothing, so the
    3,000 it starts with is every coin it will ever have unless its own shed
    overflows. Before the floor that purse hit **zero** on day 4 and stayed
    there for the rest of the season, on every one of sixteen measured games:
    zero coins is not a bad day, it is a farm that cannot hire, cannot buy a
    seed and cannot buy the wheat its animals eat, and it is absorbing rather
    than recoverable.

    The floor is what makes that unreachable, and it is asserted as exactly
    that -- the purse is never empty -- rather than as a hand count. A day with
    coins and no work worth a hand hires nobody on purpose [1.5], and no
    reserve can buy a hand for a policy that refuses to earn; the module
    docstring records what this theta's season looks like now.
    """
    _, money = _season(_theta("hoard"), seed, seat)
    broke = [(d, m) for d, m in enumerate(money) if m <= 0]
    assert not broke, f"purse empty on (day, money) {broke}"


@pytest.mark.parametrize("seed,seat", [(2104521678, 0), (1164543749, 1)])
def test_a_day_never_hires_a_crew_it_cannot_re_field(seed, seat):
    """The enumeration's half of the floor, in the engine.

    `bills[h] + cash_reserve(h)` has to fit `view.money`, so a farm down to its
    reserve cannot spend it on the crew. Read off the replay as "dawn money
    always covers yesterday's bill and the reserve that bill implied"."""
    hands, money = _season(_theta("hoard"), seed, seat)
    bad = [(d, money[d], hands[d - 1]) for d in range(1, O.LAST_SHED_DAY + 1)
           if money[d] < int(P.HIRE_BILLS[hands[d - 1]])]
    assert not bad, f"(day, dawn money, yesterday's crew) {bad}"


@pytest.mark.parametrize("kind,seed,seat", [
    ("broke", 1164543749, 0), ("broke", 2104521678, 0), ("zero", 2104521678, 0)])
def test_the_farm_can_always_re_field_yesterdays_crew(kind, seed, seat):
    """The floor's guarantee, stated as the invariant it actually is.

    Whatever a day hires, the next morning opens with at least that crew's fib
    bill in the bank -- the day held it back before it went shopping. This is
    the property the reserve buys; it is not "a hand every day", which is the
    enumeration's call and not the purse's. `broke` on seed 1164543749 seat 0
    violated it on day 20 before the floor."""
    hands, money = _season(_theta(kind), seed, seat)
    bad = [(d, money[d], int(P.HIRE_BILLS[hands[d - 1]]))
           for d in range(1, O.LAST_SHED_DAY + 1)
           if money[d] < int(P.HIRE_BILLS[hands[d - 1]])]
    assert not bad, f"{kind} seed {seed} seat {seat}: (day, money, yesterday's bill) {bad}"


# ------------------------------------------------- land against the reserve

#: NW owned and empty, the other three quadrants LOCKED, so a purchase really
#: opens 25 tiles and the valuation has something to price [1.3].
LAND_0 = int(spec.LAND_PRICES[0])
WHEAT_50 = np.array([50, 0, 0, 0, 0], np.int32)


def _land_board(money, wool=0, day=6):
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.where(P.SERP_QUAD == 0, spec.KIND_EMPTY, spec.KIND_LOCKED).astype(np.int32)
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WOOL] = wool
    return _view(money)._replace(day=np.int32(day), kind=kind, occ=z - 1, shed=shed)


def _land_macro(**kw):
    kw.setdefault("plant_target", WHEAT_50)
    return _macro(**kw)


def _land_qty(view, macro):
    op, _, qty = P.build_day(np, view, macro)[3:6]
    return int(qty[op == O.MO_BUY_LAND].sum())


def _turn1_cost(view, macro):
    """What the turn-1 row commits, priced at the engine's own curve walk."""
    from kagg3.core import projector as PJ
    op, arg, qty = P.build_day(np, view, macro)[3:6]
    quotes = PJ.buy_quotes(np, P.default_price_table(),
                           PJ.projected_inv(np, view.mkt_inv, view.shops, O.TURN_BUY))
    total = 0
    for s in range(spec.MAX_MARKET_ORDERS):
        o, a, q = int(op[O.TURN_BUY, s]), int(arg[O.TURN_BUY, s]), int(qty[O.TURN_BUY, s])
        if q == 0:
            continue
        if o == O.MO_BUY_PRODUCT:
            total += int(quotes[a, :q].sum())
        elif o == O.MO_BUY_SEED:
            total += q * int(spec.CROP_SEED_COST[a])
        elif o == O.MO_BUY_ANIMAL:
            total += q * int(spec.ANIMAL_COST[a])
    return total


def _overhead(view, macro):
    op = P.build_day(np, view, macro)[3]
    n = _hires(op)
    return _hire_bill(n) + int(P.cash_reserve(np, np.int32(n), view.day))


def _board_with_purse(purse, macro, **kw):
    """A board whose money is `purse` *plus* the day's own overhead -- the hire
    bill and the reserve -- so the fixture states the number the land decision
    actually sees. Settled rather than assumed: raising the money can raise the
    hire count and so the overhead."""
    view = _land_board(purse, **kw)
    for _ in range(6):
        over = _overhead(view, macro)
        nxt = _land_board(purse + over, **kw)
        if _overhead(nxt, macro) == over:
            return nxt
        view = nxt
    raise AssertionError("the day's overhead does not settle at this purse")


def test_land_never_eats_the_reserve():
    """The coin order is a LAW [1.5]: hire bill, then the reserve, then land,
    then the greedy. So the purse a quadrant is bought out of is `view.money`
    less the first two, and one coin under the price buys nothing -- the
    reserve is not there to be raided for the last coin of a quadrant.

    The gene is saturated here so the *valuation* is not what decides: this is
    the affordability half, and `test_land_value_is_computed_after_the_reserve`
    is the other."""
    macro = _land_macro(land_bias=np.int32(LAND_0))
    exact = _board_with_purse(LAND_0, macro)
    short = _board_with_purse(LAND_0 - 1, macro)
    assert int(P.cash_reserve(np, np.int32(_hires(P.build_day(np, exact, macro)[3])),
                              exact.day)) > 0, "no reserve to eat at this fixture"
    assert _land_qty(exact, macro) == 1
    assert _land_qty(short, macro) == 0


def test_the_reserve_is_not_funded_by_projected_revenue():
    """Projected lot-1 revenue may fund the land *gap* -- a shortfall there
    costs one purchase and no more -- but never the reserve, whose whole point
    is to be certain. So the turn-1 row stays inside hour-0 money less the
    bill and the reserve however much wool is standing in the shed."""
    macro = _land_macro(land_bias=np.int32(LAND_0),
                        hold=np.zeros(spec.N_PRODUCTS, np.int32))
    view = _land_board(3000, wool=40)
    n = _hires(P.build_day(np, view, macro)[3])
    reserve = int(P.cash_reserve(np, np.int32(n), view.day))
    assert reserve > 0
    assert _land_qty(view, macro) == 1, "the fixture did not buy the quadrant"
    assert _turn1_cost(view, macro) <= 3000 - _hire_bill(n) - reserve


def test_land_value_is_computed_after_the_reserve():
    """A quadrant whose tiles the farm could only stock by eating tomorrow's
    crew is worth less, and the valuation has to see that rather than being
    corrected afterwards.

    Swept rather than pinned to one purse, because at zero bias the two sides
    feed back: buying the quadrant adds 25 tiles of work, which hires a hand,
    which raises the reserve, which can un-buy the quadrant. What is asserted
    is the thing that does not oscillate -- the smallest purse that takes the
    quadrant is more than `bill + reserve + price` by at least the price of one
    wheat seed, because the coins `marginal_gain` walks are what those two
    deductions and the land price leave, not `view.money`.
    """
    macro = _land_macro(land_bias=np.int32(0))
    buys = [m for m in range(LAND_0, LAND_0 + 800, 5)
            if _land_qty(_land_board(m), macro)]
    assert buys, "no purse in the sweep buys the quadrant at zero bias"
    first = min(buys)
    n = _hires(P.build_day(np, _land_board(first), macro)[3])
    over = _hire_bill(n) + int(P.cash_reserve(np, np.int32(n), np.int32(6)))
    assert first - over - LAND_0 >= int(spec.CROP_SEED_COST[spec.I_WHEAT]), \
        f"{first} coins bought a quadrant with {first - over - LAND_0} left to stock it"
