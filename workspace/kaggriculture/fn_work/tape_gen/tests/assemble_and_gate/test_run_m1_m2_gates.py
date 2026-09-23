import pytest
from assemble_and_gate.run_m1_m2_gates import run_m1_m2_gates

def test_run_m1_m2_gates_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:run_m1_m2_gates"):
        run_m1_m2_gates(None)
