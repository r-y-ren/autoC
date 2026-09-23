import pytest
from derive_market_variants.assert_farmer_stream_identity import assert_farmer_stream_identity

def test_assert_farmer_stream_identity_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:assert_farmer_stream_identity"):
        assert_farmer_stream_identity(None)
