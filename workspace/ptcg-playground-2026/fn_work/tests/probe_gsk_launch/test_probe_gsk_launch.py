from src.probe_gsk_launch.probe_gsk_launch import probe_gsk_launch


def test_probe_gsk_launch_exists():
    assert callable(probe_gsk_launch)
