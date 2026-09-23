"""test_build（继承 R10 验收④装载门）：注入校验组。

① test_inject_only_appends：注入后文件=基座原件+块（前缀逐字节恒等+后缀恰为
   分隔+块文本），基座原件 sha 注入前后不变；
② test_last_callable_is_cxs_agent：真 exec（整个测试文件仅此一次，~1MB 文件；
   120s 超时预算——环境无 pytest-timeout，以耗时断言落实）装载注入后文件，
   globals 最后 callable=_cxs_agent 且宿主捕获=_cxd_agent；
③ test_reinject_rejected：对已含块的文件再 inject → 抛错而非二次追加；
④ test_injected_block_matches_layer_file：防漂移——注入块与盘上 layer_s_block.py
   逐字节一致（注入块 sha == 层文件 sha）。"""

import hashlib
import shutil
import time
from pathlib import Path

import pytest

import append_layer_s_block

_HERE = Path(__file__).resolve().parent
_BASE = _HERE.parent / "orderbook_derivative" / "main.py"
_BLOCK = _HERE / "layer_s_block.py"
_BASE_SHA256 = "a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab"

# 超时预算：注入四校验（py_compile+AST+整卷 exec）对 ~1MB 文件实测亚秒级，预算 120s。
_EXEC_BUDGET_SECONDS = 120.0


@pytest.fixture(scope="module")
def injected(tmp_path_factory):
    """一次性完成真注入（inject 内部四条校验含真 exec）：返回 (main_path, report)。"""
    main_path = tmp_path_factory.mktemp("l1") / "main.py"
    shutil.copyfile(_BASE, main_path)
    report = append_layer_s_block.inject(main_path)
    return main_path, report


def test_inject_only_appends(injected):
    # ① 注入后文件=原件+块：前缀逐字节恒等（既有行零改动），后缀恰为"两空行分隔+块文本"。
    main_path, report = injected
    base_bytes = _BASE.read_bytes()
    block_bytes = _BLOCK.read_bytes()
    assert hashlib.sha256(base_bytes).hexdigest() == _BASE_SHA256  # 基座原件指纹前置断言
    got = main_path.read_bytes()
    assert got.startswith(base_bytes)  # 前缀恒等：diff 无既有行改动
    assert got[len(base_bytes):] == append_layer_s_block._SEPARATOR + block_bytes  # 后缀恰为块
    assert report["injected_main_sha256"] == hashlib.sha256(got).hexdigest()
    # 基座原件注入后仍逐字节未动（不落任何对原文件的改动）
    assert hashlib.sha256(_BASE.read_bytes()).hexdigest() == _BASE_SHA256


def test_last_callable_is_cxs_agent(injected):
    # ② 真 exec（本文件唯一一次）装载注入后文件：globals 最后 callable=_cxs_agent
    #    （官方入口装载门桌面版）；块首 _CXS_HOST 捕获=基座尾部 _cxd_agent（层 D 先例同构）。
    main_path, _ = injected
    src = main_path.read_bytes()
    ns: dict = {}
    t0 = time.perf_counter()
    exec(compile(src, str(main_path), "exec"), ns)  # noqa: S102 - 验收④装载门桌面版
    elapsed = time.perf_counter() - t0
    assert elapsed < _EXEC_BUDGET_SECONDS, f"装载 exec 超预算: {elapsed:.1f}s >= 120s"
    last = [v for v in ns.values() if callable(v)][-1]
    assert last.__name__ == "_cxs_agent"
    assert ns["_CXS_HOST"] is not None and ns["_CXS_HOST"].__name__ == "_cxd_agent"


def test_reinject_rejected(injected):
    # ③ 重复注入幂等拒绝：对已含块的文件再 inject → 抛错（sentinel/块字节判重），
    #    而非二次追加（文件逐字节不变）。
    main_path, _ = injected
    before = main_path.read_bytes()
    with pytest.raises(ValueError, match="already injected"):
        append_layer_s_block.inject(main_path)
    assert main_path.read_bytes() == before  # 未发生二次追加


def test_injected_block_matches_layer_file(injected):
    # ④ 防漂移断言：注入块=layer_s_block.py 当前盘上文本逐字节一致（注入块 sha==层文件 sha），
    #    且 report 的块审计字段与盘上真值一致。
    main_path, report = injected
    base_bytes = _BASE.read_bytes()
    block_bytes = _BLOCK.read_bytes()
    tail = main_path.read_bytes()[len(base_bytes) + len(append_layer_s_block._SEPARATOR):]
    assert tail == block_bytes
    assert hashlib.sha256(tail).hexdigest() == hashlib.sha256(block_bytes).hexdigest()
    assert report["block_sha256"] == hashlib.sha256(block_bytes).hexdigest()
    assert report["block_bytes"] == len(block_bytes)
