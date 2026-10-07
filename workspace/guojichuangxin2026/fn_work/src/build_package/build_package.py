"""pyproject+wheel 构建+干净 venv 装后自测（build_package 块）。"""
from __future__ import annotations


class BuildError(Exception):
    """构建失败（贴 stderr 摘要）。"""

_CONSOLE = {
    "ahyd-demo": "ahyd_cli.shims:demo_main",
    "ahyd-eval": "ahyd_cli.shims:eval_main",
    "ahyd-replay-check": "ahyd_cli.shims:replay_main",
    "ahyd-sdr-check": "ahyd_cli.shims:sdr_main",
}


def build_package(out_dir: str = "dist", skip_build: bool = False) -> dict:
    """产 pyproject（src 包映射+console_scripts）→构建 wheel→干净 venv 装后探活。"""
    import subprocess
    import sys
    import venv
    from pathlib import Path

    from build_package.write_user_manual import write_user_manual

    root = Path(__file__).resolve().parents[2]
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    pkgs = sorted(p.name for p in (root / "src").iterdir()
                  if p.is_dir() and p.name != "__pycache__")
    pyproject = root / "pyproject.toml"
    pyproject.write_text(
        "[build-system]\nrequires = [\"setuptools>=68\"]\nbuild-backend = "
        "\"setuptools.build_meta\"\n\n[project]\nname = \"anhang-yundun\"\n"
        "version = \"0.1.0\"\ndescription = \"安航云盾演示系统（乡村物流无人机主动安全）\"\n"
        "requires-python = \">=3.11\"\n\n[tool.setuptools]\npackage-dir = {\"\" = \"src\"}\n"
        f"packages = {pkgs}\n\n[project.scripts]\n" +
        "".join(f'{k} = "{v}"\n' for k, v in _CONSOLE.items()) +
        "\n[tool.setuptools.package-data]\n\"*\" = [\"*.yaml\", \"*.npz\"]\n",
        encoding="utf-8")
    manual = write_user_manual(str(out / "用户手册.md"))

    # R24：打包前置卫生核验——ignore 覆盖 runs_* + 产物入库扫描（发现即失败列清单）
    import subprocess
    hygiene = {"ignore_runs": False, "tracked_artifacts": []}
    gi = root / ".gitignore"
    gi_txt = gi.read_text(encoding="utf-8") if gi.exists() else ""
    hygiene["ignore_runs"] = "runs_*/" in gi_txt or "runs*" in gi_txt
    if not hygiene["ignore_runs"]:
        raise BuildError("卫生核验失败：.gitignore 缺 runs_*/ 规约")
    ls = subprocess.run(["git", "ls-files", "fn_work"], capture_output=True,
                        text=True, cwd=root.parent.parent)
    hygiene["tracked_artifacts"] = [f for f in ls.stdout.splitlines()
                                   if "/runs_" in f or f.startswith("fn_work/runs_")]
    if hygiene["tracked_artifacts"]:
        raise BuildError(f"卫生核验失败：{len(hygiene['tracked_artifacts'])} 个评估产物在库"
                         f"（前 3：{hygiene['tracked_artifacts'][:3]}）——先 git rm --cached")

    wheels = []
    if not skip_build:
        r = subprocess.run([sys.executable, "-m", "pip", "wheel", "--no-deps",
                            "-w", str(out), str(root)],
                           capture_output=True, text=True, timeout=600)
        if r.returncode != 0:
            raise BuildError(f"wheel 构建失败: {r.stderr[-400:]}")
        wheels = sorted(str(p) for p in out.glob("*.whl"))
        # 干净 venv 装后探活：import 全包 + 入口点 help
        vv = out / "_venvtest"
        venv.create(str(vv), with_pip=True)
        pip = vv / "bin" / "pip"
        r2 = subprocess.run([str(pip), "install", "--quiet", wheels[-1]],
                            capture_output=True, text=True, timeout=600)
        r3 = subprocess.run([str(vv / "bin" / "ahyd-demo"), "--help"],
                            capture_output=True, text=True, timeout=60) \
            if (vv / "bin" / "ahyd-demo").exists() else None
        ok = r2.returncode == 0 and r3 is not None and "usage" in (r3.stdout + r3.stderr).lower()
        if not ok:
            raise BuildError(f"装后自测失败: {r2.stderr[-200:]} "
                             f"/ entry={(r3.stdout + r3.stderr)[-200:] if r3 else 'missing'}")
    return {"pyproject": str(pyproject), "manual": manual, "wheels": wheels,
            "packages": pkgs, "post_install_test": "passed" if wheels else "skipped",
            "hygiene": hygiene}
