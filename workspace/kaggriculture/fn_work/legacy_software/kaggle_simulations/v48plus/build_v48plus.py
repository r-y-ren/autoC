# 【中文】build_v48plus.py —— v48plus/main.py 确定性构建器
# ===========================================================================
# 产物 = v48 解码真源码（references/data/intel-notebooks/v48build/main.py，
#   sha256 dadee25a…2664a，与在跑 v48_derivative/main.py 逐字节一致）逐字
#   保留 + 追加 v48plus_layers.py（V50 经济层手工移植：COURIER/CAPHARV/
#   SHEDROOM）。不修改 base 任何一行；追加块见 layers 文件头注释（含未移植
#   层与理由）。
# 确定性：纯拼接构建，无时间戳/随机源；双次构建字节一致由本脚本自证。
# 包体：submission.tar.gz 单 main.py，确定性 tar（mtime=0/uid=gid=0/mode
#   0644，gzip mtime=0，与 v48_derivative 打包同口径）。
# CLI：python build_v48plus.py [--check-only]
# 输出：本目录 main.py + submission.tar.gz + build_manifest.json
# ===========================================================================
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import py_compile
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
BASE_MAIN = os.path.join(ROOT, "references", "data", "intel-notebooks",
                         "v48build", "main.py")
LAYERS = os.path.join(HERE, "v48plus_layers.py")
OUT_MAIN = os.path.join(HERE, "main.py")
OUT_TAR = os.path.join(HERE, "submission.tar.gz")
OUT_MANIFEST = os.path.join(HERE, "build_manifest.json")

# dadee25a9840313218384208c53b2c4752f82c3209cc654632e0b96c65e2664a 的前 16 位
BASE_SHA16 = "dadee25a98403132"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_once() -> bytes:
    base = open(BASE_MAIN, "rb").read()
    if sha256_bytes(base)[:16] != BASE_SHA16:
        raise SystemExit(f"base sha mismatch: {sha256_bytes(base)[:16]}")
    layers = open(LAYERS, "rb").read()
    if not base.endswith(b"\n"):
        base += b"\n"
    return base + layers


def pack_tar(source: bytes) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as tar:
        info = tarfile.TarInfo("main.py")
        info.size = len(source)
        info.mtime = 0
        info.mode = 0o644
        info.uid = 0
        info.gid = 0
        info.uname = ""
        info.gname = ""
        tar.addfile(info, io.BytesIO(source))
    gz = io.BytesIO()
    with gzip.GzipFile(fileobj=gz, mode="wb", mtime=0, filename="") as z:
        z.write(buffer.getvalue())
    return gz.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true",
                        help="只构建并比对，不落盘")
    args = parser.parse_args()

    first = build_once()
    second = build_once()
    if first != second:
        raise SystemExit("build is not deterministic")
    compile(first, "main.py", "exec")

    manifest = {
        "base": {
            "path": os.path.relpath(BASE_MAIN, ROOT).replace("\\", "/"),
            "sha256": sha256_bytes(open(BASE_MAIN, "rb").read()),
        },
        "layers": {
            "path": "software/kaggle_simulations/v48plus/v48plus_layers.py",
            "sha256": sha256_bytes(open(LAYERS, "rb").read()),
        },
        "main_py": {
            "bytes": len(first),
            "sha256": sha256_bytes(first),
        },
        "deterministic_double_build": True,
        "stdlib_only": True,
    }

    if args.check_only:
        print(json.dumps(manifest, indent=2))
        return

    with open(OUT_MAIN, "wb") as handle:
        handle.write(first)
    py_compile.compile(OUT_MAIN, doraise=True)
    tar_bytes = pack_tar(first)
    with open(OUT_TAR, "wb") as handle:
        handle.write(tar_bytes)
    tar_again = pack_tar(build_once())
    if tar_again != tar_bytes:
        raise SystemExit("tar packing is not deterministic")
    manifest["submission_tar_gz"] = {
        "bytes": len(tar_bytes),
        "sha256": sha256_bytes(tar_bytes),
        "deterministic_double_pack": True,
    }
    with open(OUT_MANIFEST, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
