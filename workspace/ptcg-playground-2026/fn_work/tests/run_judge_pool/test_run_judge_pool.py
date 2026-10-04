from src.run_judge_pool.run_judge_pool import run_judge_pool


def test_run_judge_pool_exists():
    assert callable(run_judge_pool)
