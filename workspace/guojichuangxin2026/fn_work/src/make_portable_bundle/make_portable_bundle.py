"""免 root 便携包（venv+源码+数据+手册+SHA256）（make_portable_bundle 块）。"""
from __future__ import annotations


class BundleError(Exception):
    """环境不可复制。"""


def make_portable_bundle(out_dir: str = "dist", lite: bool = False) -> dict:
    """tar.gz 布局：src+fixtures+requirements+手册+portable_demo.sh（+venv 非 lite 模式）。

    目标机 Linux x86_64 解压→bash portable_demo.sh（自动重建 venv 或复用携带 venv）。
    """
    import hashlib
    import tarfile
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    from build_package.write_user_manual import write_user_manual
    manual = write_user_manual(str(out / "用户手册.md"))

    staging = out / "ahyd_portable"
    if staging.exists():
        import shutil
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    inc = [(root / "src", "src"), (root / "tests", "tests"),
           (root / "requirements.txt", "requirements.txt"),
           (Path(manual), "用户手册.md")]
    for f in ("smoke_boot.py", "eval.py", "replay_check.py", "sdr_check.py",
              "train.py", "materials.py", "server.py", "demo.sh",
              "batch_eval.py", "pytest.ini"):
        if (root / f).exists():
            inc.append((root / f, f))
    fx = root / "fixtures"
    if fx.exists():
        inc.append((fx, "fixtures"))
    for src, rel in inc:
        dst = staging / rel
        if src.is_dir():
            import shutil
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            import shutil
            shutil.copy2(src, dst)
    if not lite and (root / ".venv").exists():
        import shutil
        shutil.copytree(root / ".venv", staging / ".venv",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    (staging / "portable_demo.sh").write_text(
        "#!/usr/bin/env bash\n# 解压即跑（Linux x86_64）：优先复用携带 venv，缺则现场重建\n"
        "set -euo pipefail\ncd \"$(dirname \"$0\")\"\n"
        "if [ -x .venv/bin/python ]; then PY=.venv/bin/python; else\n"
        "  python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt "
        "torch --index-url https://download.pytorch.org/whl/cpu || "
        ".venv/bin/pip install -q -r requirements.txt\n  PY=.venv/bin/python; fi\n"
        "$PY smoke_boot.py && exec $PY server.py \"$@\"\n", encoding="utf-8")
    (staging / "portable_demo.sh").chmod(0o755)
    tgz = out / "ahyd_portable.tar.gz"
    with tarfile.open(tgz, "w:gz") as tar:
        for item in staging.iterdir():
            tar.add(item, arcname=f"ahyd_portable/{item.name}")
    sha = hashlib.sha256(tgz.read_bytes()).hexdigest()
    (out / "ahyd_portable.tar.gz.sha256").write_text(f"{sha}  ahyd_portable.tar.gz\n",
                                                     encoding="utf-8")
    return {"bundle": str(tgz), "sha256": sha[:16] + "…", "manual": manual,
            "mode": "lite" if lite else "full",
            "note": "目标机解压→bash ahyd_portable/portable_demo.sh（解压即跑属 manual 验证项）"}
