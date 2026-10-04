from src.pack_submission.pack_submission import pack_submission


def test_pack_submission_exists():
    assert callable(pack_submission)
