import pytest
from select_on_holdout.rank_candidates_seated import rank_candidates_seated

def test_rank_candidates_seated_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:rank_candidates_seated"):
        rank_candidates_seated(None)
