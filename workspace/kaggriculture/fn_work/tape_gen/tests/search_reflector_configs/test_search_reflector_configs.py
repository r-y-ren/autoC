import pytest
from search_reflector_configs.search_reflector_configs import search_reflector_configs

def test_search_reflector_configs_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:search_reflector_configs"):
        search_reflector_configs(None)
