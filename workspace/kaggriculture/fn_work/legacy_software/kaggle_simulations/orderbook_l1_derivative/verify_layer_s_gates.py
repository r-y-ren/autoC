"""verify_layer_s_gates（R10 L0）：四门编排与台账（evidence 四件套），fail-closed。"""
import sys


def verify(pkg_path, episodes_manifest) -> dict:
    """顺序跑门①②③④→{overall,h2h,lineage,equivalence,launch}；任一门不可执行=整体 fail。"""
    raise NotImplementedError("unimplemented:fn:verify_layer_s_gates")


if __name__ == "__main__":  # CLI：python verify_layer_s_gates.py <pkg> <episodes.json>
    sys.exit(verify(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
