"""Development candidate wrapper: agent_v9 with WHEAT_FARM enabled.

ablate.py loads a candidate by file path, so the opt-in flag is turned on
here instead of changing the default-off tree.  The core module keeps its
own state namespaces; this file only forwards the agent callable.  Never
submit this file: the production entry stays agent/main.py (v7.2).
"""
import importlib.util
import os

_CORE_PATH = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..",
    "kaggle_simulations", "agent_v9", "main.py"))

_spec = importlib.util.spec_from_file_location("agent_v9_wheat_on", _CORE_PATH)
_core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_core)
_core.V9_WHEAT_FARM_ENABLED = True


def agent(obs):
    return _core.agent(obs)
