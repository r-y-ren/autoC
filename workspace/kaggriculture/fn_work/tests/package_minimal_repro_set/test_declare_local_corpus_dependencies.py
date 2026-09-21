"""declare_local_corpus_dependencies 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from package_minimal_repro_set.declare_local_corpus_dependencies import declare_local_corpus_dependencies


def test_declare_local_corpus_dependencies_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:declare_local_corpus_dependencies"):
        declare_local_corpus_dependencies(None)
