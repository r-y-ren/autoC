from src.seed_agent.seed_agent import seed_agent


def test_seed_agent_exists():
    assert callable(seed_agent)
