"""build_l2_candidate（R12 L0）：v3 双窗构建编排（648/600），确定性打包+manifest。

编排（任一步不确定即抛，fail-closed；沿 R11 L1.1 先例 build_l11_candidate 配方，
单窗流程逐条同构、块源参数化为 make 生成的 v3 窗块）：
  ① make_layer_s_v3_block.make(_L1_BLOCK, layer_s_block_v3_w{window}.py, window)：
     v3 窗块再生成+校验（幂等覆盖写；受控变更集+路由解耦审计在 make 内部全跑），
     并核对 L1 块链输入 sha == 2f3553fe…（漂移即抛）；块落本目录 make 管线产物位
     （gate_equivalence_v3 的注入源预期位）；
  ② 基座身份三方核对（盘上真值 == round-30 manifest == a16e0e9b/2838cc66 期望链）；
  ③ 复制基座 main.py 为 out_dir/w{window}/main.py——已存在旧产物时仅当其 sha 等于
     基座原件或等于上次注入产物（旧 build_manifest.json 的 main_sha256）才允许
     覆盖，防误覆盖他物（沿 L1/L1.1 白名单策略，逐窗独立）；
  ④ 注入 v3 窗块（本文件 _inject_v3：L1.1 _inject_v2 的 v3 版，块源=
     layer_s_block_v3_w{window}.py；四校验+三道写入前防线语义逐条复刻，不放松）；
  ⑤ 确定性打包 submission.tar.gz（round-30 v48_derivative 配方逐参复刻）：双跑各落
     一个临时路径，回读逐字节+sha 比对一致才发布；
  ⑥ tar 成员清单与基座包核对（恰 ["main.py"]，Kaggle 提交布局）；
  ⑦ 写 out_dir/w{window}/build_manifest.json（orderbook_l2_derivative_manifest/
     1.0：含 window/route_boundary:648/change_set_audit/描述文案/身份链）并收集返回。

window 参数：'648'/'600'/'both'（缺省 both=两窗各建）；返回 {'windows': {window: manifest}}。
CLI：python build_l2_candidate.py [--window {648,600,both}] [--out DIR]（缺省本目录）。
产物每窗三件：w{window}/{main.py, submission.tar.gz, build_manifest.json}。
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

import make_layer_s_v3_block

_HERE = Path(__file__).resolve().parent
_BASE_DIR = _HERE.parent / "orderbook_derivative"  # round-30 基座目录（只读，零改动）
_BASE_MAIN = _BASE_DIR / "main.py"
_BASE_TAR = _BASE_DIR / "submission.tar.gz"
_BASE_MANIFEST = _BASE_DIR / "build_manifest.json"
_L1_BLOCK = _HERE.parent / "orderbook_l1_derivative" / "layer_s_block.py"  # v3 链输入（只读）

# round-30 身份链（构建期三方核对，漂移即抛）：
_BASE_MAIN_SHA256 = "a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab"
_BASE_TAR_SHA256 = "2838cc66e5d3f719569108fa553c9cf9acf8190d0662f8d991856560e6e9641c"

# v3 块的 L1 链输入身份（make_layer_s_v3_block 的受控变更集输入；漂移即抛）：
_L1_BLOCK_SHA256 = "2f3553fe4b2df6213cdc1377b2fa9299ece92506291f4ed8f547640c4e2bbfcd"

# v3 窗块产物位（make 管线产物位=gate_equivalence_v3 的注入源预期位）：
_V3_BLOCK_TEMPLATE = "layer_s_block_v3_w{window}.py"

_WINDOWS = ("648", "600")  # w648 主跑 / w600 附加跑（verify_l2_gates 双窗产物位同名）

_SCHEMA = "orderbook_l2_derivative_manifest/1.0"
_DESCRIPTION = "public derivative with seed-truncation layer v3 (quantity-balanced)"  # R12 目标描述文案

_TAR_MEMBER = "main.py"  # 成员布局对照基座 tar 清单（tar -tzf：恰 main.py）

# 尾部追加分隔：基座与块文本各以单个换行收尾，再补两个换行恰成"两空行"（L1/L1.1
# 同款形态：基座尾行与新块首行之间恰两个空行）。
_SEPARATOR = b"\n\n"

# v3 块专属 sentinel（判重）：_cxs_seed_balance 函数名——该串在基座 main.py、L1
# layer_s_block.py、L1.1 layer_s_block_v2.py 中均 0 次出现（grep 验证），仅 v3 注入
# 产物含它（两窗块同含：跨窗误注入亦被此判重拦下）。
_V3_SENTINEL_BYTES = b"_cxs_seed_balance"

_ROUTE_BOUNDARY_EXPECTED = 648  # 路由边界硬事实（基座 day-27 强制 2 号路），两窗恒 648


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


def _inject_v3(main_path, window) -> dict:
    """追加 v3 窗块并校验：py_compile/AST 可解析/末 callable=_cxs_agent/diff 仅尾部追加。

    L1.1 _inject_v2 的 v3 版（其块源硬编码 layer_s_block_v2.py，不能直接复用）：
    内部逻辑为模板逐条复刻，块源换 layer_s_block_v3_w{window}.py，四校验与三道
    写入前防线语义不放松；任一红即抛。
    """
    main_path = Path(main_path)
    v3_block = _HERE / _V3_BLOCK_TEMPLATE.format(window=window)
    base_bytes = _BASE_MAIN.read_bytes()  # 基座原件只读打开
    block_bytes = v3_block.read_bytes()
    if not base_bytes.endswith(b"\n") or not block_bytes.endswith(b"\n"):
        raise ValueError("base/block 源不以换行收尾，两空行分隔约定不成立（fail-closed）")

    # 写入前防线一：目标不得指向基座原件（orderbook_derivative/main.py 只读）
    if main_path.resolve() == _BASE_MAIN.resolve():
        raise ValueError("refusing to inject: main_path 指向基座原件（orderbook_derivative/main.py 只读）")

    current = main_path.read_bytes()  # 副本须已存在（由调用方从基座复制）
    # 写入前防线二：判重——已含 v3 块（v3 专属 sentinel/该窗块字节）拒绝二次追加
    # （sentinel 两窗同串：跨窗误注入在此一并拦截）。
    if _V3_SENTINEL_BYTES in current or block_bytes in current:
        raise ValueError("already injected: 目标副本已含 layer S v3 块（sentinel/块字节判重），拒绝二次追加")
    # 写入前防线三：前置态——目标必须是基座原件的逐字节副本
    if current != base_bytes:
        raise ValueError("main_path 不是基座原件的逐字节副本（前置态漂移），拒绝注入（fail-closed）")

    main_path.write_bytes(current + _SEPARATOR + block_bytes)

    validations = []

    # ① py_compile 通过（注入后文件；临时 pyc 落目标同目录，finally 删除不留痕）
    cfile = main_path.parent / f".build_l2_candidate.{os.getpid()}.pyc"
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
        exec(compile(main_path.read_bytes(), str(main_path), "exec"), ns)  # noqa: S102 - 验收装载门（L1/L1.1 同款）
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
        "detail": f"exec {exec_seconds:.2f}s；globals 最后 callable = _cxs_agent（window={window}）",
    })

    # ④ diff 仅尾部追加：注入后文件==基座全文+分隔+该窗块（逐字节前缀恒等），基座原件零改动
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
            f"prefix {len(base_bytes)}B 逐字节恒等；+sep {len(_SEPARATOR)}B "
            f"+block(w{window}) {len(block_bytes)}B；基座原件注入前后逐字节未变"
        ),
    })

    return {
        "injected_main_sha256": hashlib.sha256(written).hexdigest(),
        "block_sha256": hashlib.sha256(block_bytes).hexdigest(),
        "block_bytes": len(block_bytes),
        "validations": validations,
    }


def _build_window(window, out_dir, facts) -> dict:
    """单窗七步编排（make→copy→inject→双跑打包→成员核对→manifest）；任一步不确定即抛。"""
    window_int = int(window)
    window_dir = out_dir / f"w{window}"
    window_dir.mkdir(parents=True, exist_ok=True)

    # ① v3 窗块再生成+校验（幂等）：先核对 L1 链输入身份，make 内部受控变更集
    #    +路由解耦审计全跑（白名单外差异即抛，写入前 fail-closed）
    l1_sha = _sha256(_L1_BLOCK.read_bytes())
    if l1_sha != _L1_BLOCK_SHA256:
        raise ValueError(f"L1 块链输入 sha {l1_sha} != 期望 {_L1_BLOCK_SHA256}（fail-closed）")
    v3_block = _HERE / _V3_BLOCK_TEMPLATE.format(window=window)
    block_info = make_layer_s_v3_block.make(_L1_BLOCK, v3_block, window=window_int)
    if Path(block_info["v3_path"]) != v3_block:
        raise RuntimeError(f"make 产物不在管线产物位 {v3_block}（fail-closed）")
    block_bytes = v3_block.read_bytes()
    if _sha256(block_bytes) != block_info["v3_sha256"]:
        raise RuntimeError("make 报告 sha 与盘上 v3 块真值不一致（fail-closed）")
    audit = block_info["change_set_audit"]
    if audit.get("window") != window_int:
        raise RuntimeError(f"change_set_audit window {audit.get('window')!r} != {window_int}（fail-closed）")
    if audit.get("route_boundary") != _ROUTE_BOUNDARY_EXPECTED:
        raise RuntimeError(
            f"change_set_audit route_boundary {audit.get('route_boundary')!r} != "
            f"{_ROUTE_BOUNDARY_EXPECTED}（路由边界硬事实漂移，fail-closed）")

    # ② 基座身份（build() 已三方核对，此处取字节）
    base_bytes = facts["bytes"]

    # ③ 复制基座为 window_dir/main.py（旧产物 sha 白名单：基座原件 或 上次注入产物）
    main_dst = window_dir / "main.py"
    if main_dst.exists():
        existing_sha = _sha256(main_dst.read_bytes())
        allowed = {facts["main_sha256"]}
        prev_manifest_path = window_dir / "build_manifest.json"
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
    main_dst.write_bytes(base_bytes)

    # ④ 注入 v3 窗块（_inject_v3 内部四校验+三防线全跑，任一红即抛）
    report = _inject_v3(main_dst, window)
    main_bytes = main_dst.read_bytes()
    main_sha = _sha256(main_bytes)
    if main_sha != report["injected_main_sha256"]:
        raise RuntimeError("注入后文件盘上 sha 与 inject 报告不一致（fail-closed）")
    if report["block_sha256"] != block_info["v3_sha256"]:
        raise RuntimeError("inject 块 sha 与 make 产物 sha 不一致（管线内身份断裂，fail-closed）")

    # ⑤ 双跑确定性打包：两次独立构建各落临时路径，回读逐字节+sha 比对一致才发布
    tmp_a = window_dir / f".build_l2_candidate.w{window}.a.tar.gz"
    tmp_b = window_dir / f".build_l2_candidate.w{window}.b.tar.gz"
    tar_dst = window_dir / "submission.tar.gz"
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

    # ⑦ manifest（键名沿 L1.1 先例+window/route_boundary/change_set_audit 收口键）
    manifest = {
        "schema": _SCHEMA,
        "candidate": (
            "shiiin9/your-market-list-is-an-order-book + layer S v3 "
            f"(public derivative with seed-truncation layer v3 w{window}, Apache-2.0)"
        ),
        "generated": date.today().isoformat(),
        "description": _DESCRIPTION,
        "window": window_int,
        "route_boundary": audit["route_boundary"],
        "main_sha256": main_sha,
        "main_bytes": len(main_bytes),
        "tar_sha256": tar_sha,
        "tar_bytes": len(tar_bytes),
        "block_sha256": report["block_sha256"],
        "block_bytes": report["block_bytes"],
        "l1_block_sha256": l1_sha,
        "change_set_audit": audit,
        "provenance_chain": [
            f"base main.py sha256 {facts['main_sha256']} == round-30 "
            "orderbook_derivative/build_manifest.json main_sha256（盘上真值三方核对）",
            f"base submission.tar.gz sha256 {facts['tar_sha256']} == round-30 tar_sha256"
            f"（member set {base_names}）",
            f"L1 layer_s_block.py sha256 {l1_sha} → make_layer_s_v3_block.make("
            f"window={window_int}) 受控变更集（删 truncate/surplus；增 reduce_orders/"
            "seed_balance/observed_plant_rate+安全边常数组+_CXS_ROUTE_BOUNDARY=648；"
            "改 agent/plan_view/_CXS_FROM 648→窗口值）→ "
            f"{_V3_BLOCK_TEMPLATE.format(window=window)} sha256 {report['block_sha256']}"
            "（change-set audit 全绿；路由边界 648 与窗口解耦）",
            f"layer S v3 block = {_V3_BLOCK_TEMPLATE.format(window=window)} "
            f"sha256 {report['block_sha256']} 注入（window={window_int}；append-only："
            "基座全文+两空行分隔+块文本；inject 四校验全绿）",
            "tar built deterministically (v48_derivative recipe: tarfile mtime0 "
            "uid/gid0 mode644, gzip mtime0), double-build byte-identical",
        ],
        "four_gates": "pending S4 (verify_l2_gates)",
        "h2h_vs_l1": "pending S4 (verify_l2_gates)",
    }
    (window_dir / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    return manifest


def build(window="both", out_dir=None) -> dict:
    """双窗构建编排：每窗 make→copy→_inject_v3→打包（双跑）→manifest；返回 {'windows': {…}}。

    window ∈ {'648', '600', 'both'}（缺省 both=两窗各建）；out_dir 为包根（缺省本
    目录），产物落 out_dir/w{window}/ 三件。任一步不确定即抛（fail-closed）。
    """
    if not isinstance(window, str) or window not in _WINDOWS + ("both",):
        raise ValueError(f"window must be one of {_WINDOWS + ('both',)!r}, got {window!r}")
    out_dir = Path(out_dir).resolve() if out_dir is not None else _HERE
    out_dir.mkdir(parents=True, exist_ok=True)

    facts = _base_facts()  # 基座身份三方核对（漂移即抛）
    windows = _WINDOWS if window == "both" else (window,)
    return {"windows": {w: _build_window(w, out_dir, facts) for w in windows}}


if __name__ == "__main__":  # CLI：python build_l2_candidate.py [--window …] [--out DIR]
    _ap = argparse.ArgumentParser(
        description="构建 layer S v3 双窗候选包（w648/w600 各 main.py+submission.tar.gz+manifest）")
    _ap.add_argument("--window", default="both", choices=list(_WINDOWS) + ["both"],
                     help="构建窗口（默认：both=两窗各建）")
    _ap.add_argument("--out", default=None, help="输出包根目录（默认：脚本所在目录；产物落 w{window}/ 子目录）")
    _args = _ap.parse_args()
    _result = build(_args.window, _args.out)
    for _w, _m in _result["windows"].items():
        print(
            f"w{_w}: main.py {_m['main_bytes']}B sha {_m['main_sha256'][:12]}…, "
            f"submission.tar.gz {_m['tar_bytes']}B sha {_m['tar_sha256'][:12]}…, "
            f"manifest {_m['schema']}"
        )
    sys.exit(0)
