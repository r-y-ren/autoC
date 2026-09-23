import pytest
from build_route_library.elect_backbone import elect_backbone

def test_elect_backbone_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:elect_backbone"):
        elect_backbone(None)
