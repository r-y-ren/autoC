import pytest
from select_on_holdout.split_train_holdout import split_train_holdout

def test_split_train_holdout_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:split_train_holdout"):
        split_train_holdout(None)
