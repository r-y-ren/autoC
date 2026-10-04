from src.prepare_metrics_shards.prepare_metrics_shards import prepare_metrics_shards


def test_prepare_metrics_shards_exists():
    assert callable(prepare_metrics_shards)
