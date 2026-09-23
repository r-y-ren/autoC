import pytest
from select_on_holdout.select_on_holdout import select_on_holdout

def test_select_on_holdout_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:select_on_holdout"):
        select_on_holdout(None)
