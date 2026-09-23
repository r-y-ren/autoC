"""build_layer_s_candidate（R10 L0）：复制 orderbook 原件→注入 layer S→确定性打包→manifest。"""
import sys


def build(out_dir=None) -> dict:
    """编排：copy→append_layer_s_block→打包（round-30 配方双跑逐字节）→manifest；任一步不确定即抛。"""
    raise NotImplementedError("unimplemented:fn:build_layer_s_candidate")


if __name__ == "__main__":  # CLI：python build_layer_s_candidate.py [--out DIR]
    sys.exit(build())
