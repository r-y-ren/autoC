import pytest
from derive_market_variants.apply_market_edit_operators import apply_market_edit_operators

def test_apply_market_edit_operators_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:apply_market_edit_operators"):
        apply_market_edit_operators(None)
