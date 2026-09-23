import pytest
from search_reflector_configs.define_config_space import define_config_space

def test_define_config_space_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:define_config_space"):
        define_config_space(None)
