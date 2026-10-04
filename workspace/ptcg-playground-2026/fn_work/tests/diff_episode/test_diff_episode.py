from src.diff_episode.diff_episode import diff_episode


def test_diff_episode_exists():
    assert callable(diff_episode)
