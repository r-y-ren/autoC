"""R4 提交包自检入口（蓝图 sw-pack 等价）"""
import sys

from src.pack_submission.pack_submission import pack_submission

if __name__ == "__main__":
    pack_submission({})
