# 纯函数：读 steps.jsonl 进度→(起跑索引,已完成记录,finished)；损坏→从 0 重跑记事件（责任文档演进轮一：execute_scenario/resume_from）
from __future__ import annotations


def resume_from(run_dir, plan):
    # 桩——签名意图详见 responsibility.md 演进轮一增量块
    raise NotImplementedError('unimplemented:fn:resume_from')
