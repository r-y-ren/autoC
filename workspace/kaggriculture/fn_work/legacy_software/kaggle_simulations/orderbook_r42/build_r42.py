# -*- coding: utf-8 -*-
"""build_r42 及构建面三子件（R25）。

责任契约（fn_docs/hybrid/responsibility.md【R25 增补】）：r40 字节为底 →
inject_r42_block → audit_diff_r42_vs_r40 → pack_r42；r40 已发射件零改动。
"""
from __future__ import annotations

from typing import Any, Dict


def build_r42(r40_main: Any, out_dir: Any = None,
              config: Any = None) -> Dict[str, Any]:
    """构建编排。签名意图：输入: r40 main 路径+常量配置 / 输出: r42 main+
    manifest+变更集审计 / 错误: 超白名单即抛。"""
    raise NotImplementedError("unimplemented:fn:build_r42")


def audit_diff_r42_vs_r40(r42_main: str, r40_main: str,
                          change_table: Any = None) -> Dict[str, Any]:
    """变更归因审计（白名单一类=尾部运行时块）。签名意图：输入: r42 main+
    r40 main+变更表 / 输出: 归因表 / 错误: 白名单外即抛。"""
    raise NotImplementedError("unimplemented:fn:audit_diff_r42_vs_r40")


def pack_r42(r42_main: str, out_dir: Any = None) -> Dict[str, Any]:
    """确定性打包+manifest（sha 链 …→r37→r40→r42）。签名意图：输入: r42
    main / 输出: submission.tar.gz+manifest / 错误: 双跑不一致即抛。"""
    raise NotImplementedError("unimplemented:fn:pack_r42")
