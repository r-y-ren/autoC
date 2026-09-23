import pytest
from build_route_library.verify_replay_fidelity import verify_replay_fidelity

def test_verify_replay_fidelity_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:verify_replay_fidelity"):
        verify_replay_fidelity(None)
