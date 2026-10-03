"""回放模式：回放文件→帧格式等价功率谱帧（source=replay）（run_spectrum_monitor 块）。"""
from __future__ import annotations


class ReplayError(Exception):
    """文件缺失/格式不符。"""


def replay_spectrum_source(replay_file: str, params: dict | None = None):
    """.npz（freqs_hz + frames_dbm[T,F]）→ 逐帧生成器；支持循环（loop=True）。"""
    from pathlib import Path
    import numpy as np
    p = Path(replay_file)
    if not p.exists():
        raise ReplayError(f"回放文件不存在: {replay_file}（先录制或用 make_replay_fixture）")
    try:
        z = np.load(p)
        freqs, frames = z["freqs_hz"], z["frames_dbm"]
    except Exception as exc:
        raise ReplayError(f"回放文件格式不符: {exc}") from exc
    loop = bool((params or {}).get("loop", True))
    i = 0
    while True:
        yield {"topic": "spectrum", "source": "replay", "freqs_hz": freqs,
               "power_dbm": frames[i % len(frames)], "frame_idx": i}
        i += 1
        if not loop and i >= len(frames):
            return
