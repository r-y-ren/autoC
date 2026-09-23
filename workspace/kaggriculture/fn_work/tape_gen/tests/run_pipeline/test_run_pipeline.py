import pytest
from run_pipeline.run_pipeline import run_pipeline

def test_run_pipeline_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:run_pipeline"):
        run_pipeline(None)
