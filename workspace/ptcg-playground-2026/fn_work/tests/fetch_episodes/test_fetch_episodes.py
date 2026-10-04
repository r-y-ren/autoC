from src.fetch_episodes.fetch_episodes import fetch_episodes


def test_fetch_episodes_exists():
    assert callable(fetch_episodes)
