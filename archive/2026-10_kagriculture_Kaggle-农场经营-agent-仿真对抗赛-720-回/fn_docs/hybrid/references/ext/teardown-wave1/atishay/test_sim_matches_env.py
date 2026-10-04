"""Phase 3 validation: replay the exact action sequence a Phase 1/2 agent
produced against the real kaggle_environments engine through sim/engine.py
starting from the same seed, and assert every piece of state matches --
not just money, but tiles, market inventory/prices, shed, seeds, town
shops, farmer/hand positions. This is the actual "does the world model
work" check; everything from Phase 4 onward depends on it being true.

Runnable directly (no pytest dependency): `python tests/test_sim_matches_env.py`
"""
import sys

sys.path.insert(0, ".")
from kaggle_environments import make
from sim import engine as sim_engine
from my_agents.single_crop_loop import make_agent as make_crop_agent
from my_agents.animal_loop import make_agent as make_animal_agent

PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}


def run_and_capture(agent_p0, steps, seed):
    """Run the real env for `steps` turns (player 0 = agent_p0, player 1 =
    always PASS), recording every action player 0 actually returned."""
    config = {"episodeSteps": steps + 10, "seed": seed}
    actions_log = []

    def recorder(obs):
        action = agent_p0(obs)
        actions_log.append(action)
        return action

    env = make("kaggriculture", configuration=config)
    env.run([recorder, "pass"])
    return env, config, actions_log[:steps]


def compare_state(env, at_step, sim_state, label):
    """at_step: turn count already processed (index into env.steps)."""
    errors = []
    real0 = env.steps[at_step][0].observation

    for p in range(2):
        real_farm = real0.farms[p]
        sim_farm = sim_state["farms"][p]
        for key in ("money", "tiles", "farmer", "hands", "unlocked_quadrants", "hires_today"):
            if real_farm[key] != sim_farm[key]:
                errors.append(f"{label}: player{p} farm.{key} MISMATCH\n  real={real_farm[key]}\n  sim ={sim_farm[key]}")

        real_priv = env.steps[at_step][p].observation.private
        sim_priv = sim_state["privates"][p]
        for key in ("shed", "seeds", "inventories"):
            if real_priv[key] != sim_priv[key]:
                errors.append(f"{label}: player{p} private.{key} MISMATCH\n  real={real_priv[key]}\n  sim ={sim_priv[key]}")

    real_market = real0.market
    if real_market["inventory"] != sim_state["market"]["inventory"]:
        errors.append(f"{label}: market.inventory MISMATCH\n  real={real_market['inventory']}\n  sim ={sim_state['market']['inventory']}")
    if real_market["prices"] != sim_state["market"]["prices"]:
        errors.append(f"{label}: market.prices MISMATCH\n  real={real_market['prices']}\n  sim ={sim_state['market']['prices']}")

    real_town = real0.town
    if real_town["unlocked_shops"] != sim_state["town"]["unlocked_shops"]:
        errors.append(f"{label}: town.unlocked_shops MISMATCH real={real_town['unlocked_shops']} sim={sim_state['town']['unlocked_shops']}")

    return errors


def replay_and_compare(agent_p0, steps, seed, label):
    env, config, actions_log = run_and_capture(agent_p0, steps, seed)
    n = len(actions_log)  # may be < steps if the agent's action list ran out

    game_state = sim_engine.new_game(config)
    action_plan = [[a, PASS_ACTION] for a in actions_log]
    states = sim_engine.rollout(game_state, config, action_plan)
    final_sim_state = states[-1]

    errors = compare_state(env, n, final_sim_state, label)
    if errors:
        print(f"FAIL {label} ({n} turns)")
        for e in errors[:5]:
            print(" ", e)
    else:
        print(f"PASS {label} ({n} turns)")
    return errors


def main():
    all_errors = []

    # Crops: exercise PLANT/WATER/HARVEST/decay/weeds/day-boundary refresh/
    # market sell across enough days (5) to cross weed-spawn and shop-unlock
    # RNG boundaries (day % 3 == 0 -> shop unlock).
    for crop in ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"]:
        agent = make_crop_agent(crop)
        all_errors += replay_and_compare(agent, steps=5 * 24, seed=42, label=f"crop[{crop}]")

    # fertilize=True wasn't covered above (BUY_PRODUCT -> PICKUP -> FERTILIZE
    # chain, live market-priced spend tracking) until Phase 8 caught the gap.
    fert_agent = make_crop_agent("STRAWBERRY", fertilize=True)
    all_errors += replay_and_compare(fert_agent, steps=15 * 24, seed=77, label="crop[STRAWBERRY fertilize=True]")

    # Animals: exercise BUILD_COOP/BUILD_PASTURE, BUY_ANIMAL, PICKUP, PLACE,
    # FEED, CARE, COLLECT_FERTILIZER, animal HARVEST.
    for animal in ["GOOSE", "COW", "SHEEP"]:
        agent = make_animal_agent(animal)
        all_errors += replay_and_compare(agent, steps=6 * 24, seed=43, label=f"animal[{animal}]")

    # Land + hiring: BUY_LAND (quadrant unlock), multiple HIRE in one day
    # (fibonacci cost curve), hand movement, hand-clearing at day boundary.
    def land_hire_agent(obs):
        step = obs["step"]
        me = obs["farms"][obs["player"]]
        n_hands = len(me["hands"])
        hands_actions = [["EAST"] for _ in range(n_hands)]
        market = []
        if step == 0:
            market = [["BUY_LAND"]]
        elif step == 1:
            market = [["HIRE"]]
        elif step == 2:
            market = [["HIRE"], ["HIRE"]]
        farmer_op = ["EAST"] if step % 2 == 0 else ["SOUTH"]
        return {"farmer": farmer_op, "hands": hands_actions, "market": market}

    all_errors += replay_and_compare(land_hire_agent, steps=3 * 24, seed=7, label="land_and_hire")

    print()
    if all_errors:
        print(f"{len(all_errors)} mismatches total -- sim does NOT match the real engine yet.")
        sys.exit(1)
    else:
        print("All scenarios match the real engine exactly.")


if __name__ == "__main__":
    main()
