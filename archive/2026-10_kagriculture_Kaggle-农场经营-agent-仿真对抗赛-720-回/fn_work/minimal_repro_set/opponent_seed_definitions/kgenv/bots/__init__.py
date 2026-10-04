"""Local bots: baselines, opponents, and the pluggable LLM provider."""

from .baseline import baseline_wheat_agent, greedy_carrot_agent  # noqa: F401
from .cow_baron import cow_baron_agent  # noqa: F401
from .melon_hoarder import melon_hoarder_agent  # noqa: F401
from .expansionist import expansionist_agent  # noqa: F401
from .online_pool import (crop_rotator_agent, near_band_diversified_agent,  # noqa: F401
                          scale_ranch_agent, self_feed_ranch_agent,
                          template_wheat_agent, two_quad_denser_agent,
                          wheat_straw_monster_agent)

# m1 wave-2 strong opponents (must each hold >=50% win rate vs the frozen
# weak pool, greedy_carrot and below -- see scripts/check_opponent_strength.py)
STRONG_OPPONENTS = ("cow_baron", "melon_hoarder", "expansionist")

# m2 online-style opponents (campaign III): reconstructions of ladder
# archetypes from the m1 replay-profile corpus; same >=50% certification
# vs the frozen weak pool.  near_band_diversified carries exploratory_params
# (2-game evidence; see kgenv/bots/online_pool.py docstring).  scale_ranch
# (r3-1) reconstructs the round-2 winner archetype cross-validated against
# the top-20 corpus -- NOT exploratory, every knob cites a >=3-game finding.
# wheat_straw_monster (r5-P6) reconstructs the round-3 96-110k winner band
# (Renji/DevilQ replays) -- the first local sparring partner for the online
# ceiling; certified like every other pool member.  two_quad_denser (v7.1)
# reconstructs the round-4 winner archetype (Sam Scott ep102685729): 2
# quadrants, 17-head dairy, all-season 17-23-tile wheat field, near-zero
# weeds -- the best online fundamentals seen against the v6 candidate.
ONLINE_STYLE_OPPONENTS = (
    "crop_rotator",
    "template_wheat",
    "self_feed_ranch",
    "near_band_diversified",
    "scale_ranch",
    "wheat_straw_monster",
    "two_quad_denser",
)
