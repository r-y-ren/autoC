import pytest
from search_reflector_configs.evaluate_ablation_tree import evaluate_ablation_tree

def test_evaluate_ablation_tree_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:evaluate_ablation_tree"):
        evaluate_ablation_tree(None)
