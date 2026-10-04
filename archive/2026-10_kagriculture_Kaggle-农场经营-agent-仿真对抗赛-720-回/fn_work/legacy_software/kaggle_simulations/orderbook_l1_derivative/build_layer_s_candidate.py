"""build_layer_s_candidate（R10 L0）：复制 orderbook 原件→注入 layer S→确定性打包→manifest。

编排（任一步不确定即抛，fail-closed）：
  ① 基座身份三方核对（盘上真值 == round-30 manifest 记录 == a16e0e9b/2838cc66 期望链）；
  ② 复制基座 main.py 为 out_dir/main.py——已存在旧产物时仅当其 sha 等于基座原件
     或等于上次注入产物（旧 build_manifest.json 的 main_sha256）才允许覆盖，防误覆盖他物；
  ③ append_layer_s_block.inject 注入 layer S 尾块（四校验全跑）；
  ④ 确定性打包 submission.tar.gz（round-30 v48_derivative 配方逐参复刻，先例
     agent/build.py::build_bytes）：双跑各落一个临时路径，回读逐字节+sha 比对
     一致才发布；该配方对 round-30 基座重打包实测逐字节复现 2838cc66…；
  ⑤ tar 成员清单与 round-30 包核对（恰 ["main.py"]，Kaggle 提交布局）；
  ⑥ 写 build_manifest.json（orderbook_l1_derivative_manifest/1.0）并返回 dict。

CLI：python build_layer_s_candidate.py [--out DIR]（默认本目录）。
产物三件：main.py、submission.tar.gz、build_manifest.json。
"""

import argparse
import gzip
import hashlib
import io
import json
import os
import sys
import tarfile
from datetime import date
from pathlib import Path

import append_layer_s_block

_HERE = Path(__file__).resolve().parent
_BASE_DIR = _HERE.parent / "orderbook_derivative"  # round-30 基座目录（只读，零改动）
_BASE_MAIN = _BASE_DIR / "main.py"
_BASE_TAR = _BASE_DIR / "submission.tar.gz"
_BASE_MANIFEST = _BASE_DIR / "build_manifest.json"

# round-30 身份链（构建期三方核对，漂移即抛）：
_BASE_MAIN_SHA256 = "a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab"
_BASE_TAR_SHA256 = "2838cc66e5d3f719569108fa553c9cf9acf8190d0662f8d991856560e6e9641c"

_SCHEMA = "orderbook_l1_derivative_manifest/1.0"
_DESCRIPTION = "public derivative with seed-truncation layer"  # R10 目标描述文案

_TAR_MEMBER = "main.py"  # 成员布局对照 round-30 tar 清单（tar -tzf：恰 main.py）


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


def build(out_dir=None) -> dict:
    """编排：copy→append_layer_s_block→打包（round-30 配方双跑逐字节）→manifest；任一步不确定即抛。"""
    out_dir = Path(out_dir).resolve() if out_dir is not None else _HERE
    out_dir.mkdir(parents=True, exist_ok=True)

    facts = _base_facts()  # ① 基座身份三方核对

    # ② 复制基座为 out_dir/main.py（旧产物 sha 白名单：基座原件 或 上次注入产物）
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

    # ③ 注入 layer S 尾块（inject 内部四校验全跑，任一红即抛）
    report = append_layer_s_block.inject(main_dst)
    main_bytes = main_dst.read_bytes()
    main_sha = _sha256(main_bytes)
    if main_sha != report["injected_main_sha256"]:
        raise RuntimeError("注入后文件盘上 sha 与 inject 报告不一致（fail-closed）")

    # ④ 双跑确定性打包：两次独立构建各落临时路径，回读逐字节+sha 比对一致才发布
    tmp_a = out_dir / ".build_layer_s_candidate.a.tar.gz"
    tmp_b = out_dir / ".build_layer_s_candidate.b.tar.gz"
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

    # ⑤ 成员清单核对：本包与 round-30 包成员名逐项相同，且恰为 ["main.py"]
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tf:
        names = tf.getnames()
    with tarfile.open(_BASE_TAR) as tf:
        base_names = tf.getnames()
    if names != base_names or names != [_TAR_MEMBER]:
        raise RuntimeError(f"tar 成员清单 {names} != round-30 同款 {base_names}（fail-closed）")

    # ⑥ manifest（键名沿 round-30 先例；schema 为本件专属 orderbook_l1_derivative_manifest/1.0）
    manifest = {
        "schema": _SCHEMA,
        "candidate": (
            "shiiin9/your-market-list-is-an-order-book + layer S "
            "(public derivative with seed-truncation layer, Apache-2.0)"
        ),
        "generated": date.today().isoformat(),
        "description": _DESCRIPTION,
        "main_sha256": main_sha,
        "main_bytes": len(main_bytes),
        "tar_sha256": tar_sha,
        "tar_bytes": len(tar_bytes),
        "block_sha256": report["block_sha256"],
        "block_bytes": report["block_bytes"],
        "provenance_chain": [
            f"base main.py sha256 {facts['main_sha256']} == round-30 "
            "orderbook_derivative/build_manifest.json main_sha256（盘上真值三方核对）",
            f"base submission.tar.gz sha256 {facts['tar_sha256']} == round-30 tar_sha256"
            f"（member set {base_names}）",
            f"layer S block = layer_s_block.py sha256 {report['block_sha256']} 注入"
            "（append-only：基座全文+两空行分隔+块文本；inject 四校验全绿）",
            "tar built deterministically (v48_derivative recipe: tarfile mtime0 "
            "uid/gid0 mode644, gzip mtime0), double-build byte-identical",
        ],
        "four_gates": "pending S3 (verify_layer_s_gates)",
        "h2h_2026_09_23": "pending S3 (gate_h2h_vs_verbatim)",
    }
    (out_dir / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    return manifest


if __name__ == "__main__":  # CLI：python build_layer_s_candidate.py [--out DIR]
    _ap = argparse.ArgumentParser(description="构建 layer S 候选包（main.py+submission.tar.gz+manifest）")
    _ap.add_argument("--out", default=None, help="输出目录（默认：脚本所在目录）")
    _manifest = build(_ap.parse_args().out)
    print(
        f"built main.py {_manifest['main_bytes']}B sha {_manifest['main_sha256'][:12]}…, "
        f"submission.tar.gz {_manifest['tar_bytes']}B sha {_manifest['tar_sha256'][:12]}…, "
        f"manifest {_manifest['schema']}"
    )
    sys.exit(0)
