from __future__ import annotations

import os
import sys

import _pin

_pin.bootstrap()

import numpy as np
from test_budget_order import _macro, _view

from kagg3 import spec
from kagg3.core import plan as P

if "--digests" not in sys.argv:
    from kagg3.agent.runtime import ProgramEngineState, ProgramIntent, Runtime

BASE = "6ad32400"
PIN_BOARDS = (("d0", 0, 3_000), ("d9", 9, 8_000), ("d15", 15, 20_000))


def _digests():
    return {name: _pin.digest(P.build_day(
        np, _view(money)._replace(day=np.int32(day)), _macro()))
            for name, day, money in PIN_BOARDS}


def test_off_is_master_byte_identical_on_three_boards(monkeypatch):
    monkeypatch.setattr(P, "PROGRAM_ENGINE_ON", False)
    assert _digests() == _pin.tree_digests(__file__, BASE)


def test_ledger_conservation_and_common_reserve():
    state = ProgramEngineState()
    view = _view(7_000)._replace(day=np.int32(9))
    intent = state.reconcile(view)
    ledger = state.last_budget
    assert ledger["reserve"] + ledger["deployable"] == ledger["purse"]
    assert ledger["reserve"] >= ledger["crew"]
    assert intent.reserve == ledger["reserve"]


def test_deadlines_and_carry_forward():
    state = ProgramEngineState()
    d0 = state.reconcile(_view(20_000)._replace(day=np.int32(0)))
    assert int(d0.plant_target[spec.I_WHEAT]) == 10
    assert int(d0.plant_target[spec.I_MELON]) == P.PROGRAM_MELON_D0
    d2 = state.reconcile(_view(20_000)._replace(day=np.int32(2)))
    assert int(d2.plant_target[spec.I_MELON]) >= 1
    assert d2.animal_target.tolist() == ([0, 3, 2] if P.PROGRAM_HERD_REAL else [0, 3, 3])
    assert int(d2.plant_target[spec.I_STRAWBERRY]) == 1
    d6 = state.reconcile(_view(20_000)._replace(day=np.int32(6)))
    d9 = state.reconcile(_view(20_000)._replace(day=np.int32(9)))
    assert d6.land_target == 2 and d9.land_target == 3
    assert d9.hands_target == 10
    d29 = state.reconcile(_view(20_000)._replace(day=np.int32(29)))
    assert not np.any(d29.plant_target)

    # Unexecuted phase work remains owed, and the final phase becomes due on
    # each crop's last viable planting day rather than expiring on day 29.
    debt = ProgramEngineState()
    d10 = debt.reconcile(_view(20_000)._replace(day=np.int32(10)))
    assert int(d10.plant_target[spec.I_WHEAT]) >= 34 + 7
    d27 = debt.reconcile(_view(20_000)._replace(day=np.int32(27)))
    assert d27.plant_target[:2].tolist() == [34 + 54 + 63, 1 + 11 + 32]


def test_animal_target_excludes_standing_herd():
    view = _view(20_000)._replace(day=np.int32(6), kind=np.full(spec.N_TILES, spec.KIND_PASTURE),
                                 occ=np.full(spec.N_TILES, spec.ANIMALS.index("SHEEP")))
    assert ProgramEngineState().reconcile(view).animal_target.tolist() == [1, 6, 0]


def test_executed_phase_priors_conserve_targets_and_start_omitted_crops_early():
    from kagg3.agent.runtime import PROGRAM_PHASES
    state = ProgramEngineState()
    for day in range(30):
        intent = state.reconcile(_view(20_000)._replace(day=np.int32(day)))
        state.planted[day] = intent.plant_target
        if day == 10:
            assert intent.plant_target[spec.I_TOMATO] > 0
            assert intent.plant_target[spec.I_STRAWBERRY] > 0
    for start, end, goals in PROGRAM_PHASES:
        assert state.planted[start:end + 1].sum(axis=0).tolist() == list(goals)



def test_program_grant_funds_service_then_herd_before_cheap_seeds():
    from kagg3.core import budget as BUD, projector as PJ
    costs = np.broadcast_to(np.asarray(
        [40, 100, *spec.CROP_SEED_COST, *spec.ANIMAL_COST], np.int32)[:, None],
        (BUD.N_LISTS, PJ.K))
    wants = np.asarray([1, 0, 20, 0, 0, 0, 0, 1, 1, 1], np.int32)
    bought = BUD.grant(np, P._program_values(np, costs, 3), costs,
                      wants, np.int32(600), np.int32(100))
    assert bought[BUD.L_WHEAT] == 1
    assert bought[BUD.L_ANIMAL0 + spec.ANIMALS.index('SHEEP')] == 1
    assert bought[BUD.L_ANIMAL0:BUD.L_ANIMAL0 + 2].tolist() == [0, 0]
    assert BUD.spend(np, costs, bought) <= 600


def test_scarce_seed_cells_do_not_starve_later_crop_obligations():
    want = np.asarray([20, 10, 0, 10, 0], np.int32)
    assert P._program_seed_room(np, want, 8).tolist() == [4, 2, 0, 2, 0]
    for cap in range(45):
        got = P._program_seed_room(np, want, cap)
        assert got.sum() == min(cap, want.sum())
        assert np.all((0 <= got) & (got <= want))


def test_unfunded_herd_does_not_reserve_empty_planting_cells(monkeypatch):
    monkeypatch.setattr(P, 'PROGRAM_ENGINE_ON', True)
    view = _view(300)._replace(day=np.int32(3),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(len(spec.SHOP_CONSUME), np.int32))
    kind = np.full(100, spec.KIND_LOCKED, np.int32)
    kind[:2] = spec.KIND_EMPTY
    view = view._replace(kind=kind)
    macro = _macro(plant_target=np.asarray([0, 0, 0, 2, 0], np.int32),
                   animal_want=np.asarray([0, 2, 0], np.int32))
    derived = P._derive(np, view, macro, spec.build_price_table(), np.int32(0),
                        False, np.int32(0), program_engine={'land_target': 1})
    assert derived.a_buy.sum() == 0
    assert derived.seed_buy[spec.I_STRAWBERRY] == 2
    assert derived.purse_left >= 0


def test_unreachable_delivery_falls_back_to_service_without_blocking_queue():
    from kagg3.core import ops as O
    far = int(np.flatnonzero(P.SERP == 0)[0])
    near = int(np.flatnonzero(P.SERP == 44)[0])
    order = np.asarray([far, near] + [i for i in range(100) if i not in (far, near)], np.int32)
    chain = np.full((100, P.CHAIN_MAX), O.OP_PASS, np.int32)
    chain[far, 0], chain[near, 0] = O.OP_FEED, O.OP_WATER
    count = np.zeros(100, np.int32)
    count[[far, near]] = 1
    zero = np.zeros_like(chain)
    picks = np.zeros((P.N_PICK, 100), bool)
    picks[0, far] = True
    delivery = np.zeros(100, bool)
    delivery[far] = True
    result = P._routes(np, chain, zero, zero, count, order, np.int32(2),
                       picks, np.int32(1), np.int32(22), np.int32(0),
                       program_return=(delivery, np.int32(2), np.int32(8)))
    assert result[4][[far, near]].all()
    assert O.OP_FEED in result[0][0] and O.OP_WATER in result[0][0]
    assert not result[8][1].any()


def test_late_land_repair_uses_observed_cash_and_preserves_reserved_orders():
    from kagg3.core import ops as O
    state = ProgramEngineState()
    action = {'farmer': ['PASS'], 'hands': [], 'market': []}
    market = np.zeros((24, spec.MAX_MARKET_ORDERS), np.int32)
    plan = (None, None, None, market, None, None)
    reserve = int(P.HIRE_BILLS[8]) + 31
    farm = {'money': 1000 + reserve, 'unlocked_quadrants': ['NW'],
            'tiles': [[{'animal': 'SHEEP'}]]}
    obs = {'day': 6, 'hour': 19, 'player': 0, 'farms': [farm],
           'private': {'shed': {}}, 'market': {'prices': {'WHEAT': 31}}}
    assert state.repair_land(obs, action, plan)['market'] == [['BUY_LAND']]
    assert action['market'] == []
    farm['money'] -= 1
    assert state.repair_land(obs, action, plan) is action
    farm['money'] += 10_000
    market[20, 0] = O.MO_BUY_SEED
    assert state.repair_land(obs, action, plan) is action


def test_reinvestment_buys_only_funded_debt_then_plants_and_waters():
    from kagg3.core import ops as O
    state = ProgramEngineState()
    state.intent = ProgramIntent(np.asarray([2, 0, 0, 0, 0]), np.zeros(3), 1, 1, 100)
    state.last_budget = {'reserve': 100}
    unit = np.full((spec.MAX_HANDS + 1, 24), O.OP_PASS, np.int32)
    market = np.zeros((24, spec.MAX_MARKET_ORDERS), np.int32)
    plan = (unit, unit.copy(), unit.copy(), market, market.copy(), market.copy())
    tiles = [['LOCKED'] * 10 for _ in range(10)]
    tiles[4][4] = tiles[4][5] = None
    farm = {'money': 120, 'farmer': [4, 4], 'hands': [[5, 4]], 'tiles': tiles}
    obs = {'day': 6, 'hour': 6, 'player': 0, 'farms': [farm],
           'private': {'seeds': {}, 'inventories': [{}, {}]},
           'market': {'prices': dict.fromkeys(spec.CROPS, 30)}}
    action = {'farmer': ['PASS'], 'hands': [['PASS']], 'market': []}
    first = state.repair_work(obs, action, plan)
    assert first['market'] == [['BUY_SEED', 'WHEAT', 1]] * 2
    assert len(state.repair_jobs) == 2
    farm['money'] = 100
    obs['hour'] += 1
    obs['private']['seeds'] = {'WHEAT': 2}
    second = state.repair_work(obs, action, plan)
    assert second['market'] == []
    assert second['farmer'] == second['hands'][0] == ['PLANT', 'WHEAT']
    obs['private']['seeds'] = {}
    for x in (4, 5):
        tiles[4][x] = {'kind': 'PLANT', 'crop': 'WHEAT', 'planted_day': 6,
                       'watered_today': False}
    obs['hour'] += 1
    third = state.repair_work(obs, action, plan)
    assert third['farmer'] == third['hands'][0] == ['WATER']
    assert third['market'] == []


def test_carried_stock_reserve_and_conditional_midday_hire():
    from kagg3.core import ops as O
    state = ProgramEngineState()
    state.intent = ProgramIntent(np.asarray([2, 0, 0, 0, 0]), np.zeros(3), 2, 1, 0)
    unit = np.full((spec.MAX_HANDS + 1, 24), O.OP_PASS, np.int32)
    market = np.zeros((24, spec.MAX_MARKET_ORDERS), np.int32)
    plan = (unit, unit.copy(), unit.copy(), market, market.copy(), market.copy())
    farm = {'money': 0, 'farmer': [4, 4], 'hands': [], 'tiles': [[None] * 10 for _ in range(10)]}
    obs = {'day': 1, 'hour': 10, 'player': 0, 'farms': [farm],
           'private': {'shed': {}, 'inventories': [{'COW': 1}]},
           'market': {'prices': dict.fromkeys(spec.CROPS, 30)}}
    reserve = int(P.HIRE_BILLS[6]) + 30
    assert state.owned_reserve(obs) == reserve
    action = {'farmer': ['PASS'], 'hands': [], 'market': []}
    farm['money'] = reserve + 11
    assert state.repair_hire(obs, action, plan)['market'] == [['HIRE']]
    farm['money'] -= 1
    assert state.repair_hire(obs, action, plan) is action
    farm['money'] += 100
    unit[1, 20] = O.OP_WATER
    assert state.repair_hire(obs, action, plan) is action


def test_drop_sale_reserves_inputs_and_walks_can_cross_locked_land():
    from kagg3.core import ops as O
    state = ProgramEngineState()
    unit = np.full((spec.MAX_HANDS + 1, 24), O.OP_PASS, np.int32)
    market = np.zeros((24, spec.MAX_MARKET_ORDERS), np.int32)
    plan = (unit, unit.copy(), unit.copy(), market, market.copy(), market.copy())
    tiles = [['LOCKED'] * 10 for _ in range(10)]
    tiles[4][4] = None
    farm = {'money': 0, 'farmer': [5, 5], 'hands': [], 'tiles': tiles}
    obs = {'day': 1, 'hour': 10, 'player': 0, 'farms': [farm],
           'private': {'shed': {}, 'seeds': {'WHEAT': 1},
                       'inventories': [{'FERTILIZER': 2}]},
           'market': {'prices': dict.fromkeys(spec.CROPS, 30)}}
    dropping = {'farmer': ['DROP'], 'hands': [], 'market': []}
    assert state.repair_sales(obs, dropping, plan)['market'] == [['SELL', 'FERTILIZER', 2]]
    obs['private']['shed'] = {'WHEAT': 98}
    obs['private']['inventories'] = [{'WOOL': 2, 'MELON': 3}]
    assert state.repair_sales(obs, dropping, plan)['market'] == [['SELL', 'WOOL', 2]]
    obs['private']['shed'] = {}
    obs['private']['inventories'] = [{'FERTILIZER': 2}]
    unit[0, 15] = O.OP_PICKUP
    plan[1][0, 15], plan[2][0, 15] = spec.I_FERT, 2
    assert state.repair_sales(obs, dropping, plan) is dropping
    unit[0, 15] = O.OP_PASS
    state.intent = ProgramIntent(np.asarray([1, 0, 0, 0, 0]), np.zeros(3), 0, 1, 0)
    state.repair_jobs[0] = (4, 4, spec.I_WHEAT)
    action = {'farmer': ['PASS'], 'hands': [], 'market': []}
    assert state.repair_work(obs, action, plan)['farmer'] == ['WEST']


def test_crew_budget_protects_today_feed_before_hiring(monkeypatch):
    from kagg3.core import ops as O
    monkeypatch.setattr(P, 'PROGRAM_ENGINE_ON', True)
    view = _view(200)._replace(day=np.int32(1))
    kind, occ, cons = view.kind.copy(), view.occ.copy(), view.t_cons.copy()
    near = np.argsort(P.DIST_SHED)[:5]
    kind[near], occ[near], cons[near] = spec.KIND_PASTURE, 1, 1
    view = view._replace(kind=kind, occ=occ, t_cons=cons)
    intent = ProgramIntent(np.zeros(5, np.int32), np.zeros(3, np.int32), 10, 1, 20)
    plan = P.build_day(np, view, _macro(hire_bias=np.int32(10000)), program_engine=intent)
    food = (plan[3] == O.MO_BUY_PRODUCT) & (plan[4] == spec.I_WHEAT)
    assert plan[5][food].sum() == 5
    assert np.sum(plan[0] == O.OP_FEED) == 5


def test_observed_decay_repairs_only_a_funded_replant_chain():
    from kagg3.core import ops as O
    unit = np.full((spec.MAX_HANDS + 1, 24), O.OP_PASS, np.int32)
    unit[0, 11] = O.OP_PLANT
    plan = (unit, None, None, None, None, None)
    farm = {'farmer': [0, 0], 'hands': [], 'tiles': [[{'kind': 'WEED'}]]}
    obs = {'hour': 10, 'player': 0, 'farms': [farm]}
    action = {'farmer': ['HARVEST'], 'hands': [], 'market': [['BUY_SEED', 'WHEAT', 1]]}
    repaired = ProgramEngineState.repair_decay(obs, action, plan)
    assert repaired['farmer'] == ['DIG']
    assert repaired['market'] == action['market']
    assert action['farmer'] == ['HARVEST']
    unit[0, 11] = O.OP_PASS
    assert ProgramEngineState.repair_decay(obs, action, plan) is action
    unit[0, 11] = O.OP_PLANT
    farm['tiles'][0][0] = {'kind': 'PLANT'}
    assert ProgramEngineState.repair_decay(obs, action, plan) is action


def test_repair_does_not_count_a_planted_job_twice():
    from kagg3.core import ops as O
    state = ProgramEngineState()
    state.intent = ProgramIntent(np.asarray([2, 0, 0, 0, 0]), np.zeros(3), 1, 1, 0)
    unit = np.full((spec.MAX_HANDS + 1, 24), O.OP_PASS, np.int32)
    market = np.zeros((24, spec.MAX_MARKET_ORDERS), np.int32)
    plan = (unit, unit.copy(), unit.copy(), market, market.copy(), market.copy())
    tiles = [['LOCKED'] * 10 for _ in range(10)]
    tiles[4][4] = {'kind': 'PLANT', 'crop': 'WHEAT', 'planted_day': 6,
                   'watered_today': False}
    tiles[4][5] = None
    farm = {'money': 100, 'farmer': [4, 4], 'hands': [[5, 4]], 'tiles': tiles}
    obs = {'day': 6, 'hour': 10, 'player': 0, 'farms': [farm],
           'private': {'seeds': {'WHEAT': 1}, 'inventories': [{}, {}]},
           'market': {'prices': dict.fromkeys(spec.CROPS, 30)}}
    state.repair_jobs[0] = (4, 4, spec.I_WHEAT)
    action = {'farmer': ['PASS'], 'hands': [['PASS']], 'market': []}
    repaired = state.repair_work(obs, action, plan)
    assert repaired['farmer'] == ['WATER']
    assert repaired['hands'] == [['PLANT', 'WHEAT']]


def test_final_owner_is_after_veto_and_uses_one_intent(monkeypatch):
    monkeypatch.setattr(P, "PROGRAM_ENGINE_ON", True)
    macro = _macro(plant_target=np.zeros(5, np.int32),
                   animal_want=np.zeros(3, np.int32))
    intent = ProgramIntent(np.asarray([1, 2, 3, 4, 5], np.int32),
                           np.asarray([2, 4, 3], np.int32), 6, 2, 100)
    moved = P._program_macro(np, macro, intent)
    np.testing.assert_array_equal(moved.plant_target, intent.plant_target)
    np.testing.assert_array_equal(moved.animal_want, intent.animal_target)


def test_per_seat_and_per_game_reset(monkeypatch):
    a, b = ProgramEngineState(), ProgramEngineState()
    a.melon_sell_requested[10] = 9
    assert b.melon_sell_requested[10] == 0
    a.last_day = 20
    a.reconcile(_view(3_000)._replace(day=np.int32(0)))
    assert a.last_day == 0 and a.melon_sell_requested[10] == 0
    monkeypatch.setattr(P, "PROGRAM_ENGINE_ON", True)
    r0, r1 = Runtime(lambda *_: _macro()), Runtime(lambda *_: _macro())
    assert r0.program_engine is not r1.program_engine


if __name__ == "__main__":
    want = os.path.abspath(sys.argv[sys.argv.index("--digests") + 1])
    import kagg3
    assert os.path.abspath(kagg3.__file__).startswith(want + os.sep)
    for key, value in _digests().items():
        print(key, value)


def test_melon_opening_lot_on_d0_carries_unfunded_rest(monkeypatch):
    monkeypatch.setattr(P, "PROGRAM_MELON_D0", 11)
    state = ProgramEngineState()
    assert int(state.reconcile(_view(3_000)._replace(day=np.int32(0)))
               .plant_target[spec.I_MELON]) == 11
    state.planted[0, spec.I_MELON] = 8          # only 8 were fundable on d0
    assert int(state.reconcile(_view(3_000)._replace(day=np.int32(1)))
               .plant_target[spec.I_MELON]) == 3
    monkeypatch.setattr(P, "PROGRAM_MELON_D0", 6)   # astra14 6/4/1 opening
    old = ProgramEngineState()
    got = []
    for d, n in enumerate((6, 4, 1)):
        got.append(int(old.reconcile(_view(3_000)._replace(day=np.int32(d)))
                       .plant_target[spec.I_MELON]))
        old.planted[d, spec.I_MELON] = n
    assert got == [6, 4, 1]


def test_herd_first_funds_scheduled_herd_past_repay_gate(monkeypatch):
    monkeypatch.setattr(P, 'PROGRAM_ENGINE_ON', True)
    view = _view(20_000)._replace(day=np.int32(16),
        mkt_inv=np.full(spec.N_PRODUCTS, 80_000, np.int32),
        shops=np.zeros(len(spec.SHOP_CONSUME), np.int32),
        price=np.ones(spec.N_PRODUCTS, np.int32))
    kind = np.full(100, spec.KIND_LOCKED, np.int32)
    kind[:10] = spec.KIND_EMPTY
    view = view._replace(kind=kind)
    macro = _macro(plant_target=np.zeros(spec.N_CROPS, np.int32),
                   animal_want=np.asarray([0, 0, 1], np.int32))
    def buy(flag):
        monkeypatch.setattr(P, 'PROGRAM_HERD_FIRST', flag)
        return P._derive(np, view, macro, spec.build_price_table(), np.int32(0),
                         False, np.int32(0), program_engine={'land_target': 1}).a_buy
    assert int(buy(False).sum()) == 0          # wool at 1 coin never repays
    assert int(buy(True)[spec.ANIMALS.index('SHEEP')]) == 1


# ---- PROGFIX1: port-fidelity fixes (S/progfix1, seat-swap ledgers) ----------

def _pf_view(day, money, n_empty, seeds=(0, 0, 0, 0, 0)):
    view = _view(money)._replace(day=np.int32(day),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(len(spec.SHOP_CONSUME), np.int32),
        seeds=np.asarray(seeds, np.int32))
    kind = np.full(100, spec.KIND_LOCKED, np.int32)
    kind[:n_empty] = spec.KIND_EMPTY
    return view._replace(kind=kind)


def _pf_derive(view, macro):
    return P._derive(np, view, macro, spec.build_price_table(), np.int32(0),
                     False, np.int32(0), program_engine={'land_target': 1})


def _planted(d):
    from kagg3.core import ops as O
    is_p = d.chain_op == O.OP_PLANT
    return [int(np.sum(is_p & (d.chain_a == c))) for c in range(spec.N_CROPS)]


def test_progfix_funded_planting_keeps_full_value(monkeypatch):
    """(1) the theta's dev_weight discount must not price a funded programme
    planting at ~10 coins (it lost every admission and stranded the seed)."""
    monkeypatch.setattr(P, 'PROGRAM_ENGINE_ON', True)
    view = _pf_view(22, 20_000, 4, seeds=(4, 0, 0, 0, 0))
    macro = _macro(plant_target=np.asarray([4, 0, 0, 0, 0], np.int32),
                   dev_weight=np.int32(P.GROW_ONE // 16))
    from kagg3.core import ops as O
    val = {}
    for flag in (False, True):
        monkeypatch.setattr(P, 'PROGRAM_PLANT_FULL', flag)
        d = _pf_derive(view, macro)
        plant = np.any(d.chain_op == O.OP_PLANT, axis=1)
        assert plant.sum() == 4
        val[flag] = int(d.tile_value[plant].min())
    assert val[True] >= 8 * val[False]


def test_progfix_scarce_slots_shared_across_crops_and_no_stranded_buy(monkeypatch):
    """(1b) scarce slots are shared pro rata, not all handed to wheat;
    (1c) held seed claims its tiles before the day buys more."""
    monkeypatch.setattr(P, 'PROGRAM_ENGINE_ON', True)
    macro = _macro(plant_target=np.asarray([6, 6, 0, 0, 0], np.int32))
    view = _pf_view(22, 20_000, 6, seeds=(6, 6, 0, 0, 0))
    monkeypatch.setattr(P, 'PROGRAM_PLANT_SHARE', False)
    d = _pf_derive(view, macro)
    assert _planted(d)[:2] == [6, 0]
    monkeypatch.setattr(P, 'PROGRAM_PLANT_SHARE', True)
    d = _pf_derive(view, macro)
    assert _planted(d)[:2] == [3, 3]
    assert int(d.seed_buy.sum()) == 0            # 12 held seeds, 6 tiles: buy none
    d = _pf_derive(_pf_view(22, 20_000, 6, seeds=(2, 0, 0, 0, 0)), macro)
    assert int(d.seed_buy.sum()) <= 4            # room is 6 tiles less 2 held


def test_progfix_herd_schedule_is_engine_mean(monkeypatch):
    """(2) the herd rows follow the ENGINE's own mean buy schedule."""
    from kagg3.agent.runtime import PROGRAM_ANIMALS_REAL
    monkeypatch.setattr(P, 'PROGRAM_HERD_REAL', True)
    state = ProgramEngineState()
    for day in (0, 6, 9, 12):
        s, c, g = PROGRAM_ANIMALS_REAL[day]
        got = state.reconcile(_view(20_000)._replace(day=np.int32(day))).animal_target
        assert got.tolist() == [g, c, s]
    assert PROGRAM_ANIMALS_REAL[-1] == (8, 8, 4)
    assert all(a <= b for r0, r1 in zip(PROGRAM_ANIMALS_REAL, PROGRAM_ANIMALS_REAL[1:])
               for a, b in zip(r0, r1))


def test_progfix_no_fertilizer_buy_back_d10_19(monkeypatch):
    """(3) d10-19 the programme sells its fertilizer; it never buys it back."""
    monkeypatch.setattr(P, 'PROGRAM_ENGINE_ON', True)
    view = _pf_view(12, 20_000, 0)
    kind = np.asarray(view.kind).copy(); kind[:20] = spec.KIND_PLANT
    occ = np.full(100, -1, np.int32); occ[:20] = spec.I_TOMATO
    t_day = np.zeros(100, np.int32); t_day[:20] = 4
    price = np.full(spec.N_PRODUCTS, 25, np.int32)
    price[spec.I_TOMATO], price[spec.I_FERT] = 200, 5
    view = view._replace(kind=kind, occ=occ, t_day=t_day, price=price)
    macro = _macro()
    got = {}
    for flag in (False, True):
        monkeypatch.setattr(P, 'PROGRAM_FERT_SELL', flag)
        got[flag] = int(_pf_derive(view, macro).fert_bought)
    assert got[True] == 0
    assert got[False] > 0


def test_progfix2_midday_herd_buy_after_sales_and_land(monkeypatch):
    """PROGFIX2 (1): the herd deficit is bought mid-day from observed cash
    onto observed free tiles; owed seed money and cached buys come first."""
    from kagg3.core import ops as O
    from kagg3.agent.runtime import PROGRAM_ANIMALS_REAL
    monkeypatch.setattr(P, 'PROGRAM_HERD_MIDDAY', True)
    monkeypatch.setattr(P, 'PROGRAM_HERD_MIDDAY_SEEDFIRST', True)  # rejected arm, still tested
    monkeypatch.setattr(P, 'PROGRAM_HERD_REAL', True)
    state = ProgramEngineState()
    state.intent = ProgramIntent(np.zeros(spec.N_CROPS, np.int32),
                                 np.zeros(3, np.int32), 6, 2, 0)
    s, c, g = PROGRAM_ANIMALS_REAL[6]
    ops = np.zeros((2, 24), np.int32)
    market = np.zeros((24, spec.MAX_MARKET_ORDERS), np.int32)
    plan = (ops, np.zeros((2, 24), np.int32), None, market, None, None)
    tiles = [[None] * 10 for _ in range(10)]
    tiles[0][0] = {'animal': 'COW'}; tiles[0][1] = {'animal': 'SHEEP'}
    farm = {'money': 0, 'hands': [], 'farmer': [5, 5], 'tiles': tiles}
    obs = {'day': 6, 'hour': 9, 'player': 0, 'farms': [farm],
           'private': {'shed': {}, 'inventories': [{}]},
           'market': {'prices': {'WHEAT': 30}}}
    action = {'farmer': ['PASS'], 'hands': [], 'market': []}
    reserve = ProgramEngineState.owned_reserve(obs)
    farm['money'] = reserve + 530 + 330 - 1            # one sheep; no cow or goose left
    got = state.repair_herd(obs, action, plan)['market']
    assert got == [['BUY_ANIMAL', 'SHEEP', 1]]
    farm['money'] = reserve + 100_000
    got = dict((o[1], o[2]) for o in state.repair_herd(obs, action, plan)['market'])
    assert got == {'SHEEP': s - 1, 'COW': c - 1, 'GOOSE': g}
    assert action['market'] == []
    # owed seed keeps its money
    state.intent = state.intent._replace(
        plant_target=np.asarray([0, 0, 0, 1000, 0], np.int32))
    assert state.repair_herd(obs, action, plan) is action
    state.intent = state.intent._replace(plant_target=np.zeros(spec.N_CROPS, np.int32))
    # before the first sale turn, with a cached purchase, or with the flag off: no buy
    assert state.repair_herd(dict(obs, hour=O.SELL_TURNS[0]), action, plan) is action
    market[20, 0] = O.MO_BUY_SEED
    assert state.repair_herd(obs, action, plan) is action
    market[20, 0] = 0
    monkeypatch.setattr(P, 'PROGRAM_HERD_MIDDAY', False)
    assert state.repair_herd(obs, action, plan) is action
