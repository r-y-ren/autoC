"""build_l13_candidate（R13 L0）：双注入构建（中部钳制+layer S 尾块）→打包→manifest。

编排（任一步不确定即抛，fail-closed；沿 R10/R11/R12 先例 build_layer_s_candidate/
build_l11_candidate/build_l2_candidate 配方）：
  ① 基座身份三方核对（盘上真值 == round-30 manifest == a16e0e9b/2838cc66 期望链）；
  ② 中部钳制手术 inject_controller_clamp.inject(mode)（内部六校验全跑）→ 中间产物
     out_dir/main_clamped.py（mode=fine|coarse；默认 out_dir=本目录时即链上既有
     main_clamped.py，幂等覆盖写同款产物）；
  ③ 复制 main_clamped.py 为 out_dir/main.py——已存在旧产物时仅当其 sha 等于本次
     钳制中间产物或上次构建产物（旧 build_manifest.json 的 main_sha256）才允许
     覆盖，防误覆盖他物（沿 L1/L1.1/L2 白名单策略）；
  ④ 追加 layer S 尾块（本文件 _inject_layer_s：L1.1 _inject_v2 的 L3 版，块源=
     orderbook_l1_derivative/layer_s_block.py 逐字节继承（链输入 sha 2f3553fe…），
     sentinel 用 L1 的模块 docstring 首行；四校验+三道写入前防线语义逐条复刻不
     放松，防线三前置态=L3 特有——目标须为本次钳制中间产物的逐字节副本；
     末 callable=_cxs_agent）；
  ⑤ 确定性打包 submission.tar.gz（round-30 v48_derivative 配方逐参复刻，先例
     agent/build.py::build_bytes）：双跑各落一个临时路径，回读逐字节+sha 比对
     一致才发布；
  ⑥ tar 成员清单与基座包核对（恰 ["main.py"]，Kaggle 提交布局）；
  ⑦ 写 build_manifest.json（orderbook_l3_derivative_manifest/1.0；provenance=
     基座链→钳制变更集审计[mode/sha]→layer S 块 sha→双跑声明；four_gates/h2h
     占位 pending S6=verify_l13_gates）并返回 dict。

CLI：python build_l13_candidate.py [--mode {fine,coarse}] [--out DIR]（默认本目录）。
产物三件：main.py、submission.tar.gz、build_manifest.json（另中间产物 main_clamped.py）。
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

import inject_controller_clamp

_HERE = Path(__file__).resolve().parent
_BASE_DIR = _HERE.parent / "orderbook_derivative"  # round-30 基座目录（只读，零改动）
_BASE_MAIN = _BASE_DIR / "main.py"
_BASE_TAR = _BASE_DIR / "submission.tar.gz"
_BASE_MANIFEST = _BASE_DIR / "build_manifest.json"
_L1_BLOCK = _HERE.parent / "orderbook_l1_derivative" / "layer_s_block.py"  # layer S 块源（只读）

# round-30 身份链（构建期三方核对，漂移即抛）：
_BASE_MAIN_SHA256 = "a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab"
_BASE_TAR_SHA256 = "2838cc66e5d3f719569108fa553c9cf9acf8190d0662f8d991856560e6e9641c"

# layer S 块链输入身份（L1.1/L2 同款 L1 块期望；漂移即抛）：
_L1_BLOCK_SHA256 = "2f3553fe4b2df6213cdc1377b2fa9299ece92506291f4ed8f547640c4e2bbfcd"

_SCHEMA = "orderbook_l3_derivative_manifest/1.0"
_DESCRIPTION = "public derivative with seed-truncation layer + late-window carrot demand clamp"  # R13 目标描述文案

_TAR_MEMBER = "main.py"  # 成员布局对照基座 tar 清单（tar -tzf：恰 main.py）

# 尾部追加分隔：钳制件与块文本各以单个换行收尾，再补两个换行恰成"两空行"（L1/L1.1/
# L2 同款形态：钳制件尾行与新块首行之间恰两个空行）。
_SEPARATOR = b"\n\n"

# 判重 sentinel（L1 的）：layer_s_block.py 模块 docstring 首行——注入过的副本必含此串
# （L1.1 _inject_v2 的 v2 专属 sentinel 在此换回 L1 块自身的 sentinel）。
_BLOCK_SENTINEL_BYTES = '"""layer S 尾块模板'.encode("utf-8")

_MODES = ("fine", "coarse")


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


def _inject_layer_s(main_path, clamped_bytes) -> dict:
    """追加 layer S 尾块（L1 块源）并校验：py_compile/AST/末 callable=_cxs_agent/diff 仅尾部追加。

    L1.1 build_l11_candidate._inject_v2 的 L3 版（其块源硬编码 layer_s_block_v2.py，
    不能直接复用）：内部逻辑为模板逐条复刻，块源换 orderbook_l1_derivative/
    layer_s_block.py（L1 逐字节继承），sentinel 用 L1 的；防线三前置态=L3 特有——
    目标须为钳制中间产物（main_clamped.py）的逐字节副本（L1/L1.1/L2 为基座原件
    副本）。四校验与三道写入前防线语义不放松；任一红即抛。
    """
    main_path = Path(main_path)
    base_bytes = _BASE_MAIN.read_bytes()  # 基座原件只读打开（校验④零改动对照）
    block_bytes = _L1_BLOCK.read_bytes()
    if not clamped_bytes.endswith(b"\n") or not block_bytes.endswith(b"\n"):
        raise ValueError("clamped/block 源不以换行收尾，两空行分隔约定不成立（fail-closed）")

    # 写入前防线一：目标不得指向基座原件（orderbook_derivative/main.py 只读）
    if main_path.resolve() == _BASE_MAIN.resolve():
        raise ValueError("refusing to inject: main_path 指向基座原件（orderbook_derivative/main.py 只读）")

    current = main_path.read_bytes()  # 副本须已存在（由调用方从钳制中间产物复制）
    # 写入前防线二：判重——已含 layer S 块（L1 sentinel/块字节）拒绝二次追加
    if _BLOCK_SENTINEL_BYTES in current or block_bytes in current:
        raise ValueError("already injected: 目标副本已含 layer S 块（sentinel/块字节判重），拒绝二次追加")
    # 写入前防线三：前置态——目标必须是本次钳制中间产物的逐字节副本
    if current != clamped_bytes:
        raise ValueError("main_path 不是钳制中间产物（main_clamped.py）的逐字节副本（前置态漂移），拒绝注入（fail-closed）")

    main_path.write_bytes(current + _SEPARATOR + block_bytes)

    validations = []

    # ① py_compile 通过（注入后文件；临时 pyc 落目标同目录，finally 删除不留痕）
    cfile = main_path.parent / f".build_l13_candidate.{os.getpid()}.pyc"
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
    #    import 期解码磁带构建 _IMPL（纯 stdlib），exec 全量执行（四条校验必须全跑，不跳过）；
    #    layer S 宿主捕获取注入态 globals 末 callable=基座尾部 orderbook 版 _cxd_agent。
    ns: dict = {}
    t0 = time.perf_counter()
    try:
        exec(compile(main_path.read_bytes(), str(main_path), "exec"), ns)  # noqa: S102 - 验收装载门（L1/L1.1/L2 同款）
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

    # ④ diff 仅尾部追加：注入后文件==钳制件全文+分隔+注入块（逐字节前缀恒等），基座原件零改动
    written = main_path.read_bytes()
    if not written.startswith(clamped_bytes):
        raise RuntimeError("校验④红：注入后文件不以钳制件全文为逐字节前缀（既有行被改动）")
    if written != clamped_bytes + _SEPARATOR + block_bytes:
        raise RuntimeError("校验④红：注入后文件 != 钳制件全文+分隔+注入块（逐字节不等）")
    if _BASE_MAIN.read_bytes() != base_bytes:
        raise RuntimeError("校验④红：基座原件内容发生变化（须零改动）")
    validations.append({
        "check": "append_only_diff", "ok": True,
        "detail": (
            f"prefix {len(clamped_bytes)}B（=main_clamped.py 钳制件）逐字节恒等；"
            f"+sep {len(_SEPARATOR)}B +block {len(block_bytes)}B；基座原件注入前后逐字节未变"
        ),
    })

    return {
        "injected_main_sha256": hashlib.sha256(written).hexdigest(),
        "block_sha256": hashlib.sha256(block_bytes).hexdigest(),
        "block_bytes": len(block_bytes),
        "validations": validations,
    }


def build(mode="fine", out_dir=None) -> dict:
    """双注入构建编排：钳制手术→copy→追加 layer S→打包（双跑）→manifest；任一步不确定即抛。

    mode ∈ {'fine','coarse'}（缺省 fine）；out_dir 为产物目录（缺省本目录），产物三件
    main.py/submission.tar.gz/build_manifest.json（另中间产物 main_clamped.py）。
    """
    if mode not in _MODES:
        raise ValueError(f"mode 须为 fine|coarse，实得 {mode!r}")
    out_dir = Path(out_dir).resolve() if out_dir is not None else _HERE
    out_dir.mkdir(parents=True, exist_ok=True)

    # ① 基座身份三方核对（漂移即抛）
    facts = _base_facts()

    # ② 中部钳制手术（inject 内部六校验全跑）→ 中间产物 out_dir/main_clamped.py
    clamped_dst = out_dir / "main_clamped.py"
    clamp_report = inject_controller_clamp.inject(_BASE_MAIN, mode, out_path=clamped_dst)
    clamped_bytes = clamped_dst.read_bytes()
    clamped_sha = _sha256(clamped_bytes)
    if clamped_sha != clamp_report["injected_sha"]:
        raise RuntimeError("钳制中间产物盘上 sha 与 inject 报告不一致（fail-closed）")
    if clamp_report["change_set"]["mode"] != mode:
        raise RuntimeError("inject 变更集 mode 与请求 mode 不一致（fail-closed）")

    # ③ 复制钳制件为 out_dir/main.py（旧产物 sha 白名单：本次钳制中间产物 或 上次构建产物）
    main_dst = out_dir / "main.py"
    if main_dst.exists():
        existing_sha = _sha256(main_dst.read_bytes())
        allowed = {clamped_sha}
        prev_manifest_path = out_dir / "build_manifest.json"
        if prev_manifest_path.is_file():
            try:
                prev = json.loads(prev_manifest_path.read_text(encoding="utf-8"))
                allowed.add(prev.get("main_sha256"))
            except (OSError, ValueError):
                pass  # 旧 manifest 不可读→不放宽白名单（fail-closed）
        if existing_sha not in allowed:
            raise ValueError(
                f"refusing to overwrite {main_dst}: 现存 sha {existing_sha} 既不等于本次钳制"
                f"中间产物 {clamped_sha} 也不等于上次构建产物（防误覆盖他物，fail-closed）"
            )
    main_dst.write_bytes(clamped_bytes)

    # ④ 追加 layer S 尾块（块链输入身份先核对；_inject_layer_s 内部四校验+三防线全跑）
    l1_sha = _sha256(_L1_BLOCK.read_bytes())
    if l1_sha != _L1_BLOCK_SHA256:
        raise ValueError(f"layer S 块链输入 sha {l1_sha} != 期望 {_L1_BLOCK_SHA256}（fail-closed）")
    report = _inject_layer_s(main_dst, clamped_bytes)
    if clamped_dst.read_bytes() != clamped_bytes:
        raise RuntimeError("追加尾块后钳制中间产物内容发生变化（须零改动，fail-closed）")
    main_bytes = main_dst.read_bytes()
    main_sha = _sha256(main_bytes)
    if main_sha != report["injected_main_sha256"]:
        raise RuntimeError("注入后文件盘上 sha 与 inject 报告不一致（fail-closed）")
    if report["block_sha256"] != l1_sha:
        raise RuntimeError("inject 块 sha 与链输入 L1 块 sha 不一致（管线内身份断裂，fail-closed）")

    # ⑤ 双跑确定性打包：两次独立构建各落临时路径，回读逐字节+sha 比对一致才发布
    tmp_a = out_dir / f".build_l13_candidate.{mode}.a.tar.gz"
    tmp_b = out_dir / f".build_l13_candidate.{mode}.b.tar.gz"
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

    # ⑦ manifest（键名沿 L1.1/L2 先例+mode/clamped 链键；provenance=基座链→钳制变更集
    #    审计[mode/sha]→layer S 块 sha→双跑声明；four_gates/h2h 占位 pending S6）
    change_set = clamp_report["change_set"]
    manifest = {
        "schema": _SCHEMA,
        "candidate": (
            "shiiin9/your-market-list-is-an-order-book + layer S + carrot2 clamp "
            f"(public derivative with seed-truncation layer + late-window carrot "
            f"demand clamp [{mode}], Apache-2.0)"
        ),
        "generated": date.today().isoformat(),
        "description": _DESCRIPTION,
        "mode": mode,
        "main_sha256": main_sha,
        "main_bytes": len(main_bytes),
        "tar_sha256": tar_sha,
        "tar_bytes": len(tar_bytes),
        "block_sha256": report["block_sha256"],
        "block_bytes": report["block_bytes"],
        "l1_block_sha256": l1_sha,
        "clamped_sha256": clamped_sha,
        "clamped_bytes": len(clamped_bytes),
        "clamp_change_set": change_set,
        "provenance_chain": [
            f"base main.py sha256 {facts['main_sha256']} == round-30 "
            "orderbook_derivative/build_manifest.json main_sha256（盘上真值三方核对）",
            f"base submission.tar.gz sha256 {facts['tar_sha256']} == round-30 tar_sha256"
            f"（member set {base_names}）",
            f"inject_controller_clamp.inject(mode={mode}) → main_clamped.py sha256 "
            f"{clamped_sha}（中部受控手术：钳制 helper 插入@基座行 {change_set['helper_span'][0]} 前"
            f" + CARROT2 §3b q 目标项替换@基座行 {change_set['replaced_line_span'][0]}"
            f"（激活窗 {change_set['audit']['activation_window']}；表达式 {change_set['audit']['expr']}）；"
            "六校验全绿，变更集审计见 clamp_change_set）",
            f"layer S block = orderbook_l1_derivative/layer_s_block.py sha256 {l1_sha} 注入"
            "（append-only：钳制件全文+两空行分隔+块文本；四校验+三防线全绿，"
            "末 callable=_cxs_agent）",
            "tar built deterministically (v48_derivative recipe: tarfile mtime0 "
            "uid/gid0 mode644, gzip mtime0), double-build byte-identical",
        ],
        "four_gates": "pending S6 (verify_l13_gates)",
        "h2h_vs_l1": "pending S6 (verify_l13_gates)",
    }
    (out_dir / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    return manifest


if __name__ == "__main__":  # CLI：python build_l13_candidate.py [--mode …] [--out DIR]
    _ap = argparse.ArgumentParser(
        description="构建 L3 双注入候选包（中部钳制+layer S 尾块：main.py+submission.tar.gz+manifest）")
    _ap.add_argument("--mode", default="fine", choices=list(_MODES),
                     help="钳制模式（默认 fine=需求钳制 min(8,需求+2)；coarse=day>=27 目标 2）")
    _ap.add_argument("--out", default=None, help="输出目录（默认：脚本所在目录）")
    _args = _ap.parse_args()
    _manifest = build(mode=_args.mode, out_dir=_args.out)
    print(
        f"[{_manifest['mode']}] built main.py {_manifest['main_bytes']}B "
        f"sha {_manifest['main_sha256'][:12]}…, submission.tar.gz {_manifest['tar_bytes']}B "
        f"sha {_manifest['tar_sha256'][:12]}…, manifest {_manifest['schema']}"
    )
    sys.exit(0)
