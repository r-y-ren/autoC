"""Track-B P2.5 惰性旋钮旗关等价测试（PLANNER_ENABLED=False 黄金动作哈希）。

硬约束（蓝图 m7 修订，2026-09-19 用户授权）：src/ 惰性旋钮扩展落地的
同时，PLANNER_ENABLED=False 的行为必须与现役 v13.8 **逐字节等价**——
6 种子全季双席自博弈动作流的 sha256 与预改动捕获的黄金基线
（exports/probes/planner_flagoff/golden_v138.json，含引擎指纹链与捕获
口径）逐种子一致。基线经 PYTHONHASHSEED=12345/999 双进程复跑稳定。
另验证通道活性：旗开+覆盖跑同种子，动作流哈希必异。

机内预算：7 个整季孪生 rollout（旗关 6 + 旗开 1，复用引擎装载缓存），
实测 <30s；超时时长上限 300s。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

SOFTWARE = Path(__file__).resolve().parents[1]
if str(SOFTWARE) not in sys.path:
    sys.path.insert(0, str(SOFTWARE))

SCRIPTS = SOFTWARE / "scripts"
GOLDEN_PATH = SOFTWARE / "exports" / "probes" / "planner_flagoff" \
    / "golden_v138.json"
SEEDS = (11, 22, 33, 47, 58, 69)


def _load_golden_module():
    """按路径装载 scripts/planner_flagoff_golden.py（提供合成季与哈希）。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "planner_flagoff_golden_test",
        str(SCRIPTS / "planner_flagoff_golden.py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("planner_flagoff_golden_test", module)
    spec.loader.exec_module(module)
    return module


def _golden_ready():
    return GOLDEN_PATH.is_file() and \
        (SOFTWARE / "kaggle_simulations" / "agent" / "src" /
         "constants.py").is_file()


@pytest.mark.skipif(not _golden_ready(),
                    reason="黄金基线或现役 src/ 不在位（gitignored 数据）")
class TestFlagOffEquivalence:

    def test_flag_off_action_stream_matches_v138_golden(self):
        """6 种子全季：旗关动作流 sha256 与 v13.8 黄金基线逐种子一致。"""
        golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
        expected = {row["seed"]: row["sha256"] for row in golden["seeds"]}
        assert tuple(sorted(expected)) == SEEDS     # 基线种子面不被偷换
        mod = _load_golden_module()
        rows = mod.hashes_for_seeds(SEEDS)
        mismatch = [r for r in rows if r["sha256"] != expected[r["seed"]]]
        assert not mismatch, (
            "PLANNER_ENABLED=False 旗关等价破坏（种子/实测/期望）："
            + "; ".join(f"{r['seed']}/{r['sha256'][:12]}/"
                        f"{expected[r['seed']][:12]}" for r in mismatch))

    def test_flag_on_overrides_change_action_stream(self):
        """通道活性：同种子旗开+激进覆盖后动作流哈希必异（旋钮真的
        咬合执行器，不是装饰性键面）。"""
        mod = _load_golden_module()
        baseline = mod.hashes_for_seeds(SEEDS[:1])[0]
        ns = mod.build_v138_namespace()
        assert ns["PLANNER_ENABLED"] is False       # 缺省必须关旗
        ns["PLANNER_ENABLED"] = True
        ns["PLANNER_OVERRIDES"] = {
            "mode_volume_day_start": -99, "mode_volume_day_end": 99,
            "herd_day_shift": 2, "sell_price_discount": 0.75}
        flag_on = mod.season_action_hash(ns["agent"], SEEDS[0])
        assert flag_on["sha256"] != baseline["sha256"]
