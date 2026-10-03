"""Stable planner specifications used by the local research ladder.

V2 is the validated 50-seed champion. Its candidate list is explicit so
future edits to planner.candidates.default_candidates do not silently alter
the benchmark. Shared engine bug fixes still apply to every version.
"""
from my_agents.animal_loop import ANIMAL_INFO, make_agent as make_animal_agent
from my_agents.barathan_melon_wheat import make_agent as make_barathan_agent
from my_agents.bugmaker_melon_recycle import make_agent as make_bugmaker_agent
from my_agents.dual_worker_animal import make_agent as make_herd_agent
from my_agents.hybrid_crop_animal import make_agent as make_hybrid_agent
from my_agents.multi_worker_crop import make_agent as make_multi_agent
from my_agents.quadrant_crop import QUADRANT_TILES, make_agent as make_quadrant_agent
from my_agents.single_crop_loop import CROP_INFO, make_agent as make_crop_agent
from my_agents.v7_melon_dynamic import make_agent as make_v7_agent
from my_agents.v8_melon_crop_engine import make_agent as make_v8_agent
from my_agents.v9_adaptive_crop_engine import make_agent as make_v9_agent
from planner.executor import make_planner_agent


def _dual_candidates():
    return {
        "dual_COW_COW": lambda: make_herd_agent("COW", animal_b="COW"),
        "dual_COW_SHEEP": lambda: make_herd_agent("COW", animal_b="SHEEP"),
    }


def v1_candidates():
    """The candidate pool immediately before the validated labor expansion."""
    candidates = {}
    for crop, info in CROP_INFO.items():
        wait = info["max_yield_day"]
        candidates[f"single_{crop}"] = lambda crop=crop, wait=wait: make_crop_agent(
            crop, wait_days=wait
        )
        candidates[f"quadrant_{crop}"] = lambda crop=crop, wait=wait: make_quadrant_agent(
            crop, wait_days=wait, tiles=QUADRANT_TILES
        )
    candidates["multi_worker_MELON"] = lambda: make_multi_agent(
        "MELON", wait_days=CROP_INFO["MELON"]["max_yield_day"], target_quadrants=2
    )
    for animal in ANIMAL_INFO:
        candidates[f"animal_{animal}"] = lambda animal=animal: make_animal_agent(animal)
    candidates.update(_dual_candidates())
    return candidates


def v2_candidates():
    """Frozen candidate specification for the 2026-08-07 champion."""
    candidates = {}
    for quadrants in (2, 3, 4):
        candidates[f"multi_worker_MELON_{quadrants}q"] = (
            lambda quadrants=quadrants: make_multi_agent(
                "MELON",
                wait_days=CROP_INFO["MELON"]["max_yield_day"],
                target_quadrants=quadrants,
            )
        )
    candidates.update(_dual_candidates())
    candidates.update({
        "triple_COW_SHEEP_GOOSE": lambda: make_herd_agent(
            "COW", animal_b="SHEEP", extra_animals=["GOOSE"]
        ),
        "triple_COW_COW_SHEEP": lambda: make_herd_agent(
            "COW", animal_b="COW", extra_animals=["SHEEP"]
        ),
        "quad_COW_COW_COW_SHEEP": lambda: make_herd_agent(
            "COW", animal_b="COW", extra_animals=["COW", "SHEEP"]
        ),
        "quad_COW_COW_SHEEP_SHEEP": lambda: make_herd_agent(
            "COW", animal_b="COW", extra_animals=["SHEEP", "SHEEP"]
        ),
    })
    return candidates


def v3_candidates():
    """Sweep-informed candidate specification added on August 7, 2026."""
    candidates = v2_candidates()
    for crop in ("WHEAT", "CARROT"):
        candidates[f"multi_worker_{crop}_2q"] = (
            lambda crop=crop: make_multi_agent(
                crop,
                wait_days=CROP_INFO[crop]["max_yield_day"],
                target_quadrants=2,
            )
        )
    for transition_day in (6, 8):
        candidates[f"hybrid_MELON_2q_COW_d{transition_day}"] = (
            lambda transition_day=transition_day: make_hybrid_agent(
                "MELON",
                farmer_animal="COW",
                wait_days=CROP_INFO["MELON"]["max_yield_day"],
                target_quadrants=2,
                transition_day=transition_day,
            )
        )
        candidates[f"hybrid_MELON_2q_SHEEP_d{transition_day}"] = (
            lambda transition_day=transition_day: make_hybrid_agent(
                "MELON",
                farmer_animal="SHEEP",
                wait_days=CROP_INFO["MELON"]["max_yield_day"],
                target_quadrants=2,
                transition_day=transition_day,
            )
        )
    candidates["hybrid_MELON_3q_COW_d6"] = (
        lambda: make_hybrid_agent(
            "MELON",
            farmer_animal="COW",
            wait_days=CROP_INFO["MELON"]["max_yield_day"],
            target_quadrants=3,
            transition_day=6,
            operating_reserve=1200,
        )
    )
    candidates.update({
        "dual_COW_COW": lambda: make_herd_agent("COW", animal_b="COW"),
        "dual_COW_SHEEP": lambda: make_herd_agent("COW", animal_b="SHEEP"),
        "dual_GOOSE_GOOSE": lambda: make_herd_agent("GOOSE", animal_b="GOOSE"),
        "triple_COW_COW_COW": lambda: make_herd_agent(
            "COW", animal_b="COW", extra_animals=["COW"]
        ),
        "triple_COW_SHEEP_SHEEP": lambda: make_herd_agent(
            "COW", animal_b="SHEEP", extra_animals=["SHEEP"]
        ),
        "triple_SHEEP_SHEEP_SHEEP": lambda: make_herd_agent(
            "SHEEP", animal_b="SHEEP", extra_animals=["SHEEP"]
        ),
    })
    return candidates


def v4_candidates():
    """Lean past-opponent challenger aligned with the current submission.

    V3 kept every sweep-informed idea in the live pool. The quick validation
    showed that breadth can add runtime/noise without a clear score gain, so
    V4 keeps the validated V2 core and only adds the replay-loss counter
    openers that are also present in submission.py.
    """
    candidates = v2_candidates()
    for crop in ("WHEAT", "CARROT"):
        candidates[f"multi_worker_{crop}_2q"] = (
            lambda crop=crop: make_multi_agent(
                crop,
                wait_days=CROP_INFO[crop]["max_yield_day"],
                target_quadrants=2,
            )
        )
    candidates["dual_GOOSE_GOOSE"] = lambda: make_herd_agent("GOOSE", animal_b="GOOSE")
    return candidates


def v5_candidates():
    """Bugmaker-learning challenger.

    V5 starts from the proven V2 champion and adds one explicit capital-
    recycling melon line learned from Bugmaker's replay: dense day-0 melon,
    harvest spike, land expansion, late fast-crop closeout.
    """
    candidates = v2_candidates()
    candidates["bugmaker_melon_recycle"] = make_bugmaker_agent
    return candidates


def v6_candidates():
    """Forced Barathan Aslan replay copy.

    V5 added a melon-recycle candidate, but the live planner still chose cattle
    in the latest Barathan loss. V6 removes that selector risk and runs the
    replay-backed melon -> land -> wheat line directly.
    """
    return {
        "barathan_melon_wheat": make_barathan_agent,
    }


def v7_candidates():
    """V7 melon opener with tested dynamic-labor hooks.

    The default schedule currently matches the strongest local sweep
    (11 late hands), but the agent exposes the labor schedule for follow-up
    search without changing the proven opening.
    """
    return {
        "v7_melon_dynamic": make_v7_agent,
    }


def v8_candidates():
    """V8 crop-engine challenger.

    Keeps the champion melon opener, day-10 land expansion, and all-11 labor,
    but switches the post-day-10 engine from wheat to strawberry based on the
    first controlled crop sweep.
    """
    return {
        "v8_strawberry_engine": lambda: make_v8_agent(post_day10_crop="STRAWBERRY"),
    }


def v9_candidates():
    """V9 adaptive crop engine.

    Uses the wheat champion line when opponent pressure resembles the
    Barathan replay, otherwise switches to the higher-ceiling strawberry
    engine discovered in the crop sweep.
    """
    return {
        "v9_adaptive_crop_engine": make_v9_agent,
    }


VERSIONS = {
    "v1": v1_candidates,
    "v2": v2_candidates,
    "v3": v3_candidates,
    "v4": v4_candidates,
    "v5": v5_candidates,
    "v6": v6_candidates,
    "v7": v7_candidates,
    "v8": v8_candidates,
    "v9": v9_candidates,
}


def make_version(name, config):
    try:
        candidates = VERSIONS[name]()
    except KeyError as exc:
        raise ValueError(f"Unknown planner version {name!r}; choose from {sorted(VERSIONS)}") from exc
    if name in ("v6", "v7", "v8", "v9"):
        factories = {
            "v6": ("barathan_melon_wheat", make_barathan_agent),
            "v7": ("v7_melon_dynamic", make_v7_agent),
            "v8": ("v8_strawberry_engine", lambda: make_v8_agent(post_day10_crop="STRAWBERRY")),
            "v9": ("v9_adaptive_crop_engine", make_v9_agent),
        }
        label, factory = factories[name]
        base_agent = factory()
        state = {"history": []}

        def agent(obs):
            if not state["history"]:
                state["history"].append((obs["day"], label, []))
            return base_agent(obs)

        agent.track = base_agent.track
        agent.state = state
        return agent
    return make_planner_agent(config, candidates=candidates)
