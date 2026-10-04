from src.cluster_opponents.cluster_opponents import cluster_opponents


def test_cluster_opponents_exists():
    assert callable(cluster_opponents)
