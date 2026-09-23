import pytest
from build_route_library.fork_routes_on_events import fork_routes_on_events

def test_fork_routes_on_events_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:fork_routes_on_events"):
        fork_routes_on_events(None)
