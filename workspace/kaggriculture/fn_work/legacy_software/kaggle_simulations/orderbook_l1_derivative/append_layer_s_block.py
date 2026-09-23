"""append_layer_s_block（R10 L1）：把 layer_s_block 源码注入 L1 副本尾部并过四条校验。"""

import ast
import hashlib
import os
import py_compile
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_BASE_MAIN = _HERE.parent / "orderbook_derivative" / "main.py"  # 基座原件（只读，零改动）
_BLOCK_FILE = _HERE / "layer_s_block.py"  # 待注入块=同目录层文件整体文本

# 块首 sentinel（判重）：layer_s_block.py 模块 docstring 首行——注入过的副本必含此串。
_BLOCK_SENTINEL_BYTES = '"""layer S 尾块模板'.encode("utf-8")

# 尾部追加分隔：基座与块文本各以单个换行收尾，再补两个换行恰成"两空行"（层 D/counter
# T-B 尾块同款形态：基座尾行与新块首行之间恰两个空行）。
_SEPARATOR = b"\n\n"


def inject(main_path) -> dict:
    """追加尾块并校验：py_compile/AST 可解析/末 callable=_cxs_agent/diff 仅尾部追加；任一红即抛。"""
    main_path = Path(main_path)
    base_bytes = _BASE_MAIN.read_bytes()  # 基座原件只读打开
    block_bytes = _BLOCK_FILE.read_bytes()
    if not base_bytes.endswith(b"\n") or not block_bytes.endswith(b"\n"):
        raise ValueError("base/block 源不以换行收尾，两空行分隔约定不成立（fail-closed）")
    if main_path.resolve() == _BASE_MAIN.resolve():
        raise ValueError("refusing to inject: main_path 指向基座原件（orderbook_derivative/main.py 只读）")

    current = main_path.read_bytes()  # L1 main.py 副本须已存在（由调用方从基座复制）
    if _BLOCK_SENTINEL_BYTES in current or block_bytes in current:
        raise ValueError("already injected: 目标副本已含 layer S 块（sentinel/块字节判重），拒绝二次追加")
    if current != base_bytes:
        raise ValueError("main_path 不是基座原件的逐字节副本（前置态漂移），拒绝注入（fail-closed）")

    main_path.write_bytes(current + _SEPARATOR + block_bytes)

    validations = []

    # ① py_compile 通过（注入后文件；临时 pyc 落目标同目录，finally 删除不留痕）
    cfile = main_path.parent / f".append_layer_s_block.{os.getpid()}.pyc"
    try:
        py_compile.compile(str(main_path), cfile=str(cfile), doraise=True)
    except Exception as exc:
        raise RuntimeError(f"校验①红：py_compile 未通过: {exc!r}") from exc
    finally:
        cfile.unlink(missing_ok=True)
    validations.append({
        "check": "py_compile", "ok": True,
        "detail": f"py_compile.compile(doraise=True) passed: {main_path}",
    })

    # ② AST 可解析（注入后文件全文）
    try:
        ast.parse(main_path.read_bytes(), filename=str(main_path))
    except SyntaxError as exc:
        raise RuntimeError(f"校验②红：ast.parse 未通过: {exc!r}") from exc
    validations.append({
        "check": "ast_parse", "ok": True,
        "detail": f"ast.parse passed ({main_path.stat().st_size} bytes)",
    })

    # ③ 装载后 globals 最后 callable = _cxs_agent：隔离命名空间 exec 注入后源码——基座
    #    import 期解码磁带构建 _IMPL（纯 stdlib），exec 全量执行（四条校验必须全跑，不跳过）。
    ns: dict = {}
    t0 = time.perf_counter()
    try:
        exec(compile(main_path.read_bytes(), str(main_path), "exec"), ns)
    except Exception as exc:
        raise RuntimeError(f"校验③红：注入后源码 exec 失败: {exc!r}") from exc
    exec_seconds = time.perf_counter() - t0
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded:
        raise RuntimeError("校验③红：exec 后命名空间无任何 callable")
    if loaded[-1].__name__ != "_cxs_agent":
        raise RuntimeError(f"校验③红：装载后最后 callable={loaded[-1].__name__!r}，应为 '_cxs_agent'")
    validations.append({
        "check": "last_callable", "ok": True,
        "detail": f"exec {exec_seconds:.2f}s；globals 最后 callable = _cxs_agent",
    })

    # ④ diff 仅尾部追加：注入后文件==基座全文+分隔+注入块（逐字节前缀恒等），基座原件零改动
    written = main_path.read_bytes()
    if not written.startswith(base_bytes):
        raise RuntimeError("校验④红：注入后文件不以基座全文为逐字节前缀（既有行被改动）")
    if written != base_bytes + _SEPARATOR + block_bytes:
        raise RuntimeError("校验④红：注入后文件 != 基座全文+分隔+注入块（逐字节不等）")
    if _BASE_MAIN.read_bytes() != base_bytes:
        raise RuntimeError("校验④红：基座原件内容发生变化（须零改动）")
    validations.append({
        "check": "append_only_diff", "ok": True,
        "detail": (
            f"prefix {len(base_bytes)}B 逐字节恒等；+sep {len(_SEPARATOR)}B +block {len(block_bytes)}B；"
            "基座原件注入前后逐字节未变"
        ),
    })

    return {
        "injected_main_sha256": hashlib.sha256(written).hexdigest(),
        "block_sha256": hashlib.sha256(block_bytes).hexdigest(),
        "block_bytes": len(block_bytes),
        "validations": validations,
    }
