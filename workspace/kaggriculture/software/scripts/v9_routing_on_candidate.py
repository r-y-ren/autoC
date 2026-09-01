"""Development candidate wrapper: agent_v9 with the router ACTIVE.

Turns the sector router on (V9_SHADOW_ROUTING=False) while keeping the
rejected WHEAT_FARM mode off, so ablate.py can gate the scheduler change
on its own.  Never submit this file: the production entry stays
agent/main.py (v7.2).
"""
import importlib.util
import os

_CORE_PATH = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..",
    "kaggle_simulations", "agent_v9", "main.py"))

_spec = importlib.util.spec_from_file_location("agent_v9_routing_on", _CORE_PATH)
_core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_core)
_core.V9_WHEAT_FARM_ENABLED = False
_core.V9_SHADOW_ROUTING = False


def agent(obs):
    return _core.agent(obs)
