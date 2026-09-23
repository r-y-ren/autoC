import pytest
from assemble_and_gate.assemble_and_gate import assemble_and_gate

def test_assemble_and_gate_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:assemble_and_gate"):
        assemble_and_gate(None)
