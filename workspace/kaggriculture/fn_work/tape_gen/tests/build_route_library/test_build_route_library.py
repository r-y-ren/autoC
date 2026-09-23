import pytest
from build_route_library.build_route_library import build_route_library

def test_build_route_library_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:build_route_library"):
        build_route_library(None)
