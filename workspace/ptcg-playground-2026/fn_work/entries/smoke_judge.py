"""R1 判决池冒烟入口（蓝图 sw-boot 等价）"""
import sys

from src.run_judge_pool.run_judge_pool import run_judge_pool

if __name__ == "__main__":
    run_judge_pool({})
