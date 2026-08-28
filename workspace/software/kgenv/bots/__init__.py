"""Local bots: baselines, opponents, and the pluggable LLM provider."""

from .baseline import baseline_wheat_agent, greedy_carrot_agent  # noqa: F401
from .cow_baron import cow_baron_agent  # noqa: F401
from .melon_hoarder import melon_hoarder_agent  # noqa: F401
from .expansionist import expansionist_agent  # noqa: F401

# m1 wave-2 strong opponents (must each hold >=50% win rate vs the frozen
# weak pool, greedy_carrot and below -- see scripts/check_opponent_strength.py)
STRONG_OPPONENTS = ("cow_baron", "melon_hoarder", "expansionist")
