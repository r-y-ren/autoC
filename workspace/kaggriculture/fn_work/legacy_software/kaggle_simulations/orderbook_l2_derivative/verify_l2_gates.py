"""verify_l2_gates（R12 L0）：两窗各全套四门，取全绿最宽窗；fail-closed。"""
import sys


def verify(pkg_root) -> dict:
    raise NotImplementedError("unimplemented:fn:verify_l2_gates")


if __name__ == "__main__":
    sys.exit(verify(sys.argv[1] if len(sys.argv) > 1 else None))
