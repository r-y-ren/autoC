import pytest
from derive_market_variants.derive_market_variants import derive_market_variants

def test_derive_market_variants_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:derive_market_variants"):
        derive_market_variants(None)
