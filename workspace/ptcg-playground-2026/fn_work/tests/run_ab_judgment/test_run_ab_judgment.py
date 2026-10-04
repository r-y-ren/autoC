from src.run_ab_judgment.run_ab_judgment import run_ab_judgment


def test_run_ab_judgment_exists():
    assert callable(run_ab_judgment)
