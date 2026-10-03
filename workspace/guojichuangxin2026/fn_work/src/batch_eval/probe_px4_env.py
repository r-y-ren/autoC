"""PX4 工具链与源码树就绪探测（不安装，只报告）（batch_eval 块）。"""
from __future__ import annotations

_REQUIRED_CMDS = ("make", "cmake", "git")
_ARM_HINTS = ("arm-none-eabi-gcc", "aarch64-linux-gnu-gcc")


def probe_px4_env(config: dict) -> dict:
    """config: sitl 节（px4_dir/airframe）。输出 {ready, missing, px4_dir, note}。"""
    import shutil
    from pathlib import Path
    missing = [c for c in _REQUIRED_CMDS if shutil.which(c) is None]
    if not any(shutil.which(a) for a in _ARM_HINTS):
        missing.append("arm-none-eabi-gcc（交叉工具链）")
    px4_dir = (config or {}).get("px4_dir", "")
    if not px4_dir or not (Path(px4_dir) / "Makefile").exists():
        missing.append("sitl.px4_dir 源码树（克隆 PX4-Autopilot 后配置）")
    ready = not missing
    return {"ready": ready, "missing": missing, "px4_dir": px4_dir,
            "note": "" if ready else "缺项见 missing；安装属用户 sudo 动作（pacman 包单见批报告）"}
