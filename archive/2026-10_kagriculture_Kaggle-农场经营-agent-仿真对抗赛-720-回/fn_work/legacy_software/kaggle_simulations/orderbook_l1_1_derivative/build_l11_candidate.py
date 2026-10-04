"""build_l11_candidate（R11 L0）：make v2 块→复制基座→注入 v2 尾块→确定性打包→manifest。

编排（任一步不确定即抛，fail-closed；沿 R10 L1 先例 build_layer_s_candidate 配方）：
  ① make_layer_s_v2_block.make()：v2 块再生成+校验（幂等覆盖写；内部 diff 恰一
     函数体审计全跑），并核对 L1 块链输入 sha == 2f3553fe…（漂移即抛）；
  ② 基座身份三方核对（盘上真值 == round-30 manifest == a16e0e9b/2838cc66 期望链）；
  ③ 复制基座 main.py 为 out_dir/main.py——已存在旧产物时仅当其 sha 等于基座原件
     或等于上次注入产物（旧 build_manifest.json 的 main_sha256）才允许覆盖，
     防误覆盖他物（沿 L1 白名单策略）；
  ④ 注入 v2 尾块（本文件 _inject_v2：L1 append_layer_s_block.inject 的 v2 版，
     块源=layer_s_block_v2.py；四校验+三道写入前防线语义逐条复刻，不放松）；
  ⑤ 确定性打包 submission.tar.gz（round-30 v48_derivative 配方逐参复刻，先例
     agent/build.py::build_bytes）：双跑各落一个临时路径，回读逐字节+sha 比对
     一致才发布；
  ⑥ tar 成员清单与基座包核对（恰 ["main.py"]，Kaggle 提交布局）；
  ⑦ 写 build_manifest.json（orderbook_l1_1_derivative_manifest/1.0）并返回 dict。

CLI：python build_l11_candidate.py [--out DIR]（默认本目录）。
产物三件：main.py、submission.tar.gz、build_manifest.json。
"""

import argparse
import ast
import gzip
import hashlib
import io
import json
import os
import py_compile
import sys
import tarfile
import time
from datetime import date
from pathlib import Path

import make_layer_s_v2_block

_HERE = Path(__file__).resolve().parent
_BASE_DIR = _HERE.parent / "orderbook_derivative"  # round-30 基座目录（只读，零改动）
_BASE_MAIN = _BASE_DIR / "main.py"
_BASE_TAR = _BASE_DIR / "submission.tar.gz"
_BASE_MANIFEST = _BASE_DIR / "build_manifest.json"
_L1_BLOCK = _HERE.parent / "orderbook_l1_derivative" / "layer_s_block.py"  # v2 链输入（只读）

# round-30 身份链（构建期三方核对，漂移即抛）：
_BASE_MAIN_SHA256 = "a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab"
_BASE_TAR_SHA256 = "2838cc66e5d3f719569108fa553c9cf9acf8190d0662f8d991856560e6e9641c"

# v2 块的 L1 链输入身份（make_layer_s_v2_block 的源级替换输入；漂移即抛）：
_L1_BLOCK_SHA256 = "2f3553fe4b2df6213cdc1377b2fa9299ece92506291f4ed8f547640c4e2bbfcd"

_V2_BLOCK = _HERE / "layer_s_block_v2.py"  # 注入块源（make 的管线产物位）

_SCHEMA = "orderbook_l1_1_derivative_manifest/1.0"
_DESCRIPTION = "public derivative with seed-truncation layer v2 (net-demand coverage)"  # R11 目标描述文案

_TAR_MEMBER = "main.py"  # 成员布局对照基座 tar 清单（tar -tzf：恰 main.py）

# 尾部追加分隔：基座与块文本各以单个换行收尾，再补两个换行恰成"两空行"（L1 同款形态：
# 基座尾行与新块首行之间恰两个空行）。
_SEPARATOR = b"\n\n"

# v2 块专属 sentinel（判重）：净需求覆盖版 _cxs_seed_surplus docstring 标记——该串
# 在基座 main.py 与 L1 layer_s_block.py 中均 0 次出现（grep 验证），仅 v2 注入产物
# 含它（比 L1 的模块 docstring sentinel 更进一步：可区分 v2 与 L1 注入产物）。
_V2_SENTINEL_BYTES = "净需求覆盖".encode("utf-8")


def _sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def _pack_tar_gz(main_bytes: bytes) -> bytes:
    """确定性打包单成员 tar.gz（round-30 v48_derivative 配方逐参复刻）。

    先例 agent/build.py::build_bytes：plain tar（mode="w"）成员 TarInfo
    mtime=0 uid=gid=0 mode=0o644 uname=gname=""，再 gzip.GzipFile(mtime=0)
    收口（fileobj 用 BytesIO，gzip 头不落文件名）。
    """
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tar:
        info = tarfile.TarInfo(_TAR_MEMBER)
        info.size = len(main_bytes)
        info.mtime = 0
        info.mode = 0o644
        info.uid = info.gid = 0
        info.uname = info.gname = ""
        tar.addfile(info, io.BytesIO(main_bytes))
    gz = io.BytesIO()
    with gzip.GzipFile(fileobj=gz, mode="wb", mtime=0) as z:
        z.write(buf.getvalue())
    return gz.getvalue()


def _base_facts() -> dict:
    """基座身份三方核对：盘上 main.py/tar 真值 ↔ round-30 manifest ↔ 期望链。"""
    base_bytes = _BASE_MAIN.read_bytes()
    base_tar_bytes = _BASE_TAR.read_bytes()
    round30 = json.loads(_BASE_MANIFEST.read_text(encoding="utf-8"))
    main_sha = _sha256(base_bytes)
    tar_sha = _sha256(base_tar_bytes)
    problems = []
    if round30.get("schema") != "orderbook_derivative_manifest/1.0":
        problems.append(f"round-30 manifest schema 漂移: {round30.get('schema')!r}")
    if main_sha != _BASE_MAIN_SHA256:
        problems.append(f"基座 main.py sha {main_sha} != 期望 {_BASE_MAIN_SHA256}")
    if round30.get("main_sha256") != main_sha:
        problems.append("round-30 manifest main_sha256 与盘上真值不符")
    if tar_sha != _BASE_TAR_SHA256:
        problems.append(f"基座 submission.tar.gz sha {tar_sha} != 期望 {_BASE_TAR_SHA256}")
    if round30.get("tar_sha256") != tar_sha:
        problems.append("round-30 manifest tar_sha256 与盘上真值不符")
    if problems:
        raise ValueError("基座身份核对失败（fail-closed）: " + "; ".join(problems))
    return {"bytes": base_bytes, "main_sha256": main_sha, "tar_sha256": tar_sha}


def _inject_v2(main_path) -> dict:
    """追加 v2 尾块并校验：py_compile/AST 可解析/末 callable=_cxs_agent/diff 仅尾部追加。

    L1 append_layer_s_block.inject 的 v2 版（其块源硬编码 L1 layer_s_block.py，
    不能直接复用）：内部逻辑为模板逐条复刻，块源换 layer_s_block_v2.py，四校验
    与三道写入前防线语义不放松；任一红即抛。
    """
    main_path = Path(main_path)
    base_bytes = _BASE_MAIN.read_bytes()  # 基座原件只读打开
    block_bytes = _V2_BLOCK.read_bytes()
    if not base_bytes.endswith(b"\n") or not block_bytes.endswith(b"\n"):
        raise ValueError("base/block 源不以换行收尾，两空行分隔约定不成立（fail-closed）")

    # 写入前防线一：目标不得指向基座原件（orderbook_derivative/main.py 只读）
    if main_path.resolve() == _BASE_MAIN.resolve():
        raise ValueError("refusing to inject: main_path 指向基座原件（orderbook_derivative/main.py 只读）")

    current = main_path.read_bytes()  # 副本须已存在（由调用方从基座复制）
    # 写入前防线二：判重——已含 v2 块（v2 专属 sentinel/块字节）拒绝二次追加
    if _V2_SENTINEL_BYTES in current or block_bytes in current:
        raise ValueError("already injected: 目标副本已含 layer S v2 块（sentinel/块字节判重），拒绝二次追加")
    # 写入前防线三：前置态——目标必须是基座原件的逐字节副本
    if current != base_bytes:
        raise ValueError("main_path 不是基座原件的逐字节副本（前置态漂移），拒绝注入（fail-closed）")

    main_path.write_bytes(current + _SEPARATOR + block_bytes)

    validations = []

    # ① py_compile 通过（注入后文件；临时 pyc 落目标同目录，finally 删除不留痕）
    cfile = main_path.parent / f".build_l11_candidate.{os.getpid()}.pyc"
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
        exec(compile(main_path.read_bytes(), str(main_path), "exec"), ns)  # noqa: S102 - 验收装载门（L1 同款）
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


def build(out_dir=None) -> dict:
    """编排：make v2 块→copy 基座→_inject_v2→打包（双跑逐字节）→manifest；任一步不确定即抛。"""
    out_dir = Path(out_dir).resolve() if out_dir is not None else _HERE
    out_dir.mkdir(parents=True, exist_ok=True)

    # ① v2 块再生成+校验（幂等）：先核对 L1 链输入身份，make 内部 diff 恰一函数体审计全跑
    l1_sha = _sha256(_L1_BLOCK.read_bytes())
    if l1_sha != _L1_BLOCK_SHA256:
        raise ValueError(f"L1 块链输入 sha {l1_sha} != 期望 {_L1_BLOCK_SHA256}（fail-closed）")
    block_info = make_layer_s_v2_block.make()
    if Path(block_info["v2_path"]) != _V2_BLOCK:
        raise RuntimeError("make 产物不在本目录 layer_s_block_v2.py（管线产物位漂移，fail-closed）")
    block_bytes = _V2_BLOCK.read_bytes()
    if _sha256(block_bytes) != block_info["v2_sha256"]:
        raise RuntimeError("make 报告 sha 与盘上 v2 块真值不一致（fail-closed）")

    # ② 基座身份三方核对
    facts = _base_facts()

    # ③ 复制基座为 out_dir/main.py（旧产物 sha 白名单：基座原件 或 上次注入产物）
    main_dst = out_dir / "main.py"
    if main_dst.exists():
        existing_sha = _sha256(main_dst.read_bytes())
        allowed = {facts["main_sha256"]}
        prev_manifest_path = out_dir / "build_manifest.json"
        if prev_manifest_path.is_file():
            try:
                prev = json.loads(prev_manifest_path.read_text(encoding="utf-8"))
                allowed.add(prev.get("main_sha256"))
            except (OSError, ValueError):
                pass  # 旧 manifest 不可读→不放宽白名单（fail-closed）
        if existing_sha not in allowed:
            raise ValueError(
                f"refusing to overwrite {main_dst}: 现存 sha {existing_sha} 既不等于基座"
                f" {facts['main_sha256']} 也不等于上次注入产物（防误覆盖他物，fail-closed）"
            )
    main_dst.write_bytes(facts["bytes"])

    # ④ 注入 v2 尾块（_inject_v2 内部四校验+三防线全跑，任一红即抛）
    report = _inject_v2(main_dst)
    main_bytes = main_dst.read_bytes()
    main_sha = _sha256(main_bytes)
    if main_sha != report["injected_main_sha256"]:
        raise RuntimeError("注入后文件盘上 sha 与 inject 报告不一致（fail-closed）")
    if report["block_sha256"] != block_info["v2_sha256"]:
        raise RuntimeError("inject 块 sha 与 make 产物 sha 不一致（管线内身份断裂，fail-closed）")

    # ⑤ 双跑确定性打包：两次独立构建各落临时路径，回读逐字节+sha 比对一致才发布
    tmp_a = out_dir / ".build_l11_candidate.a.tar.gz"
    tmp_b = out_dir / ".build_l11_candidate.b.tar.gz"
    tar_dst = out_dir / "submission.tar.gz"
    try:
        tmp_a.write_bytes(_pack_tar_gz(main_bytes))
        tmp_b.write_bytes(_pack_tar_gz(main_bytes))
        built_a = tmp_a.read_bytes()
        built_b = tmp_b.read_bytes()
        if built_a != built_b or _sha256(built_a) != _sha256(built_b):
            raise RuntimeError("双跑打包不一致（确定性破坏），拒绝发布产物（fail-closed）")
        os.replace(tmp_a, tar_dst)
    finally:
        tmp_a.unlink(missing_ok=True)
        tmp_b.unlink(missing_ok=True)
    tar_bytes = tar_dst.read_bytes()
    if tar_bytes != built_a:
        raise RuntimeError("发布产物与双跑比对样本不一致（fail-closed）")
    tar_sha = _sha256(tar_bytes)

    # ⑥ 成员清单核对：本包与基座包成员名逐项相同，且恰为 ["main.py"]
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tf:
        names = tf.getnames()
    with tarfile.open(_BASE_TAR) as tf:
        base_names = tf.getnames()
    if names != base_names or names != [_TAR_MEMBER]:
        raise RuntimeError(f"tar 成员清单 {names} != 基座同款 {base_names}（fail-closed）")

    # ⑦ manifest（键名沿 L1 先例+l1_block_sha256 链输入键；schema 为本件专属）
    manifest = {
        "schema": _SCHEMA,
        "candidate": (
            "shiiin9/your-market-list-is-an-order-book + layer S v2 "
            "(public derivative with seed-truncation layer v2, Apache-2.0)"
        ),
        "generated": date.today().isoformat(),
        "description": _DESCRIPTION,
        "main_sha256": main_sha,
        "main_bytes": len(main_bytes),
        "tar_sha256": tar_sha,
        "tar_bytes": len(tar_bytes),
        "block_sha256": report["block_sha256"],
        "block_bytes": report["block_bytes"],
        "l1_block_sha256": l1_sha,
        "provenance_chain": [
            f"base main.py sha256 {facts['main_sha256']} == round-30 "
            "orderbook_derivative/build_manifest.json main_sha256（盘上真值三方核对）",
            f"base submission.tar.gz sha256 {facts['tar_sha256']} == round-30 tar_sha256"
            f"（member set {base_names}）",
            f"L1 layer_s_block.py sha256 {l1_sha} → make_layer_s_v2_block.make 恰一"
            f"函数体替换（_cxs_seed_surplus → 净需求覆盖版）→ layer_s_block_v2.py "
            f"sha256 {report['block_sha256']}（diff 审计全绿）",
            f"layer S v2 block = layer_s_block_v2.py sha256 {report['block_sha256']} 注入"
            "（append-only：基座全文+两空行分隔+块文本；inject 四校验全绿）",
            "tar built deterministically (v48_derivative recipe: tarfile mtime0 "
            "uid/gid0 mode644, gzip mtime0), double-build byte-identical",
        ],
        "four_gates": "pending S4 (verify_l11_gates)",
        "h2h_vs_l1": "pending S4 (gate_h2h_vs_l1)",
    }
    (out_dir / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    return manifest


if __name__ == "__main__":  # CLI：python build_l11_candidate.py [--out DIR]
    _ap = argparse.ArgumentParser(description="构建 layer S v2 候选包（main.py+submission.tar.gz+manifest）")
    _ap.add_argument("--out", default=None, help="输出目录（默认：脚本所在目录）")
    _manifest = build(_ap.parse_args().out)
    print(
        f"built main.py {_manifest['main_bytes']}B sha {_manifest['main_sha256'][:12]}…, "
        f"submission.tar.gz {_manifest['tar_bytes']}B sha {_manifest['tar_sha256'][:12]}…, "
        f"manifest {_manifest['schema']}"
    )
    sys.exit(0)
