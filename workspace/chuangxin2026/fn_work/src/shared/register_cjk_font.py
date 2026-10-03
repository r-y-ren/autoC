# 内置 OFL 中文字体注册进 matplotlib（幂等）；缺字体文件→异常立即暴露（责任文档演进轮一：shared/register_cjk_font）
from __future__ import annotations


def register_cjk_font():
    # 桩——签名意图详见 responsibility.md 演进轮一增量块
    raise NotImplementedError('unimplemented:fn:register_cjk_font')
