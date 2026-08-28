"""kgenv -- Kaggriculture local evaluation infrastructure.

Built on the OFFICIAL kaggle-environments engine (kaggriculture scenario,
PyPI kaggle-environments 1.32.7). See README.md for the vendored-wheel note.

Modules
-------
economy   : quantified crop/animal/market revenue models (unit-testable)
redlines  : mechanic red-line checklist (watering/feeding/production caps)
engine    : single-episode runner on the official engine
gym_env   : gym-style single-agent wrapper with pluggable opponent
arena     : match running, replay logs, submission loading
elo       : Elo rating math for the evaluation script
bots      : local baseline/opponent agents + pluggable LLM provider
"""

__version__ = "1.0.0"

from . import economy, redlines, engine, gym_env, elo, arena  # noqa: F401


def official_engine_version() -> str:
    """Version string of the installed kaggle-environments package."""
    import kaggle_environments
    return getattr(kaggle_environments, "__version__", "unknown")
