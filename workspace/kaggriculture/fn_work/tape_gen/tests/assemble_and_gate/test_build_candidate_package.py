import pytest
from assemble_and_gate.build_candidate_package import build_candidate_package

def test_build_candidate_package_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:build_candidate_package"):
        build_candidate_package(None)
