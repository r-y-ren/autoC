# -*- coding: utf-8 -*-
"""build_r37（R19/R20 L1）+ 审计/打包子函数。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】）：
以 orderbook_2965_adopt/a/main.py（r34a 在飞件字节）为底复制 →
inject_cash_guard_block + retape_sheep_timing + retape_tail_savings
三白名单改造 → audit_diff_vs_r34a → pack_r37；产物落 orderbook_r37/，
r34a/在飞件零改动。
"""
from __future__ import annotations

from typing import Any, Dict


def build_r37(r34a_main_path: str) -> Dict[str, Any]:
    """构建编排：三白名单改造→diff 审计恰=三件→确定性打包+manifest。

    签名意图：输入: r34a main 路径 / 输出: r37 main+manifest+变更集审计 /
    错误: 超白名单即抛。
    """
    raise NotImplementedError("unimplemented:fn:build_r37")


def audit_diff_vs_r34a(r37_main: str, r34a_main: str) -> Dict[str, Any]:
    """对底版逐字节 diff 审计——差异恰=白名单三件（尾部追加守卫块/羊步点
    变更表/尾盘删除清单），出现白名单外差异即红；输出差异归因表。

    签名意图：输入: r37 main+r34a main / 输出: 归因表 /
    错误: 白名单外差异即抛。
    """
    raise NotImplementedError("unimplemented:fn:audit_diff_vs_r34a")


def pack_r37(r37_main: str) -> Dict[str, Any]:
    """确定性打包+manifest——沿 R16 配方（tarfile mtime0/uid0/gid0/mode644、
    gzip mtime0、双跑逐字节一致）；manifest=基底 sha 链（a16e0e9b→r34a→r37）、
    三白名单件 sha、双跑哈希、描述文案
    "public derivative with cash-floor guard and earlier flock schedule"。

    签名意图：输入: r37 main / 输出: submission.tar.gz+manifest /
    错误: 双跑不一致即抛。
    """
    raise NotImplementedError("unimplemented:fn:pack_r37")
