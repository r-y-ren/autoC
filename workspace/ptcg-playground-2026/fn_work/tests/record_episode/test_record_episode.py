from src.record_episode.record_episode import record_episode


def test_record_episode_exists():
    assert callable(record_episode)
