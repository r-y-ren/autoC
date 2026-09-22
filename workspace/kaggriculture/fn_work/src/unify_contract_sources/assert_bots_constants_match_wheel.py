"""bots 五文件 CROPS_INFO/ANIMALS_INFO 与 vendored wheel 常量交叉断言（篡改即红）。

上游: R8, R9（详见 fn_docs/responsibility.md）

实现要点（[新增]件，B4 先例=fingerprint_engine_constants.cross_check_against_wheel）：
- 钉护对象 = 旧树 kgenv/bots/ 五文件（baseline / cow_baron /
  melon_hoarder / expansionist / online_pool）各自手抄的 CROPS_INFO /
  ANIMALS_INFO 子集表——bots 逻辑（成本估算/交期/喂养计划）全部建立在这份
  手抄镜像之上，此前零 wheel 对照（R9 缺陷本体）。
- wheel 侧真值通道（B4 同款）：直接 import
  kaggle_environments.envs.kaggriculture.kaggriculture——kgenv/engine.py
  装载的同一安装副本；与 software/vendor/ wheel 逐文件一致由旧树 twin P1
  指纹链背书（WHEEL_PROVENANCE.md 留痕）。真值键：CROPS / ANIMALS。
- 断言语义（逐条目精确等值，子集方向）：bots 侧每个条目必须在 wheel 同名
  表中存在且 dict 完全相等；bots 侧刻意只抄子集（各 bot 只抄自己用到的
  作物/牲畜——melon_hoarder 无动物面、连 ANIMALS_INFO 属性都不定义，
  按"未手抄=不使用"口径视同空表），不要求覆盖全表——但报告 coverage
  字段登记并集覆盖面。
- fail-closed：wheel 不可 import 即抛（本函数本身就是主门，无登记指纹可
  兜底——这点与 B4 不同，B4 主门是登记指纹故可 skip）；任一条目漂移抛
  BotsConstantsMismatch（AssertionError 子类，篡改 monkeypatch 即红）。
- 源装载（旧树只读）：sys.modules 已缓存实例优先（monkeypatch 对同一实例
  可见——篡改测试依赖此），否则战役根发现（blueprint.md+software+fn_docs
  三特征）后常规包 import，包初始化链不可用时回退按文件路径装载
  （bots 五文件本体纯 stdlib）。不 import 旧 scripts/；不写任何旧树文件。

适配说明（旧树冻结——物理改线属战后，登记于此）：
- 战后五文件的 CROPS_INFO/ANIMALS_INFO 改为从本包真值投影
  （`dict((k, CROPS[k]) for k in (...))` 子集视图），本断言随之转为
  防御性回归；改线前旧树字面以本交叉断言看护。
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path

__all__ = [
    "BOTS_CONSTANT_MODULES",
    "BotsConstantsMismatch",
    "WheelChannelUnavailable",
    "load_bots_constants_module",
    "load_wheel_constants",
    "assert_bots_constants_match_wheel",
]

# 钉护的五份旧树 bots 文件（模块名后缀；均含 CROPS_INFO/ANIMALS_INFO）
BOTS_CONSTANT_MODULES: tuple[str, ...] = (
    "baseline", "cow_baron", "melon_hoarder", "expansionist", "online_pool",
)

# 战役根目录特征（与仓库布局约定一致，不写字面战役路径）：新布局=fn_docs+
# fn_work 两件齐备（2026-09-23 大整合后唯一形态）；兼容旧布局三特征。
# software 锚=战役根/software（旧）或 fn_work/legacy_software（新）。
_CAMPAIGN_FEATURES = ("fn_docs", "fn_work")
_CAMPAIGN_FEATURES_LEGACY = ("blueprint.md", "software", "fn_docs")

_BOTS_TABLES = (("CROPS_INFO", "CROPS"), ("ANIMALS_INFO", "ANIMALS"))


class BotsConstantsMismatch(AssertionError):
    """bots 手抄常量与 wheel 真值漂移——篡改即红（fail-closed）。"""


class WheelChannelUnavailable(RuntimeError):
    """wheel 真值通道不可 import——本函数即主门，无兜底，fail-closed。"""


def _campaign_software_root() -> Path:
    """自本模块 __file__ 上溯发现战役根（新布局 fn_docs+fn_work 或旧布局三特征），
    返回其 software/（旧）或 fn_work/legacy_software（新）。fail-closed。"""
    here = Path(__file__).resolve()
    for candidate in (here, *here.parents):
        new = all((candidate / name).exists() for name in _CAMPAIGN_FEATURES)
        legacy = all((candidate / name).exists() for name in _CAMPAIGN_FEATURES_LEGACY)
        if new or legacy:
            sw = candidate / "software"
            return sw if sw.is_dir() else candidate / "fn_work" / "legacy_software"
    raise RuntimeError(
        "未找到战役根（特征=" + "+".join(_CAMPAIGN_FEATURES) + " 或 "
        + "+".join(_CAMPAIGN_FEATURES_LEGACY) + "），上溯起点: " + str(here))


def load_bots_constants_module(short_name: str):
    """装载旧树 kgenv/bots/<short_name>（只读；进程内缓存同一实例）。

    sys.modules 已缓存实例优先（守卫与测试对同一实例的 monkeypatch 可见）；
    其次常规包 import；包初始化链失败时回退按文件路径装载（bots 文件
    本体纯 stdlib）。
    """
    module_name = f"kgenv.bots.{short_name}"
    cached = sys.modules.get(module_name)
    if cached is not None:
        return cached
    software = _campaign_software_root()
    if str(software) not in sys.path:
        sys.path.insert(0, str(software))
    try:
        return importlib.import_module(module_name)
    except Exception:
        path = software / "kgenv" / "bots" / f"{short_name}.py"
        if not path.is_file():
            raise RuntimeError(
                f"bots 源文件不存在且包 import 失败: {path}") from None
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"无法构造装载 spec: {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module  # 缓存，后续调用同一实例
        spec.loader.exec_module(module)
        return module


def load_wheel_constants():
    """装载 wheel 侧经济常量模块（B4 同款通道），返回模块对象。

    Raises:
        WheelChannelUnavailable: kaggle_environments 不可 import（主门
            fail-closed，不 skip）。
    """
    try:
        from kaggle_environments.envs.kaggriculture import (
            kaggriculture as wheel_mod)
    except ImportError as exc:
        raise WheelChannelUnavailable(
            f"kaggle_environments 不可 import（本断言即主门，fail-closed）: "
            f"{exc}") from exc
    return wheel_mod


def assert_bots_constants_match_wheel(bots_sources: dict | None = None,
                                      wheel_source=None) -> dict:
    """bots 五文件手抄常量 vs wheel 真值逐条目交叉断言（不一致即抛）。

    Args:
        bots_sources: {模块短名: 含 CROPS_INFO/ANIMALS_INFO 属性的对象}；
            None=装载旧树真实五文件（测试注入用）。
        wheel_source: 含 CROPS/ANIMALS 属性的对象；None=装载 wheel 真值。

    Returns:
        dict：ok（全等 True）/ checked_modules / crops_entries /
            animals_entries（逐模块条目数）/ coverage（五文件并集覆盖的
            wheel 条目面）/ mismatches（空表——非空即已抛）/
            wheel_source（provenance 留痕）。

    Raises:
        WheelChannelUnavailable: wheel 通道不可用（fail-closed）。
        BotsConstantsMismatch: 任一条目缺失或值漂移。
    """
    if bots_sources is None:
        bots_sources = {name: load_bots_constants_module(name)
                        for name in BOTS_CONSTANT_MODULES}
    if wheel_source is None:
        wheel_source = load_wheel_constants()

    mismatches = []
    entry_counts: dict[str, dict[str, int]] = {}
    coverage: dict[str, set] = {w_name: set() for _, w_name in _BOTS_TABLES}
    for name in BOTS_CONSTANT_MODULES:
        source = bots_sources.get(name)
        if source is None:
            mismatches.append({"module": name, "table": "-", "item": "-",
                               "bots": "module missing from bots_sources",
                               "wheel": "-"})
            continue
        counts: dict[str, int] = {}
        for bots_attr, wheel_attr in _BOTS_TABLES:
            bots_table = getattr(source, bots_attr, None)
            wheel_table = getattr(wheel_source, wheel_attr, None)
            if not isinstance(wheel_table, dict):
                mismatches.append({"module": name, "table": bots_attr,
                                   "item": "-", "bots": repr(bots_table),
                                   "wheel": "wheel table unavailable"})
                counts[bots_attr] = -1
                continue
            if bots_table is None:
                # 未手抄=不使用（如 melon_hoarder 无动物面）：视同空表。
                bots_table = {}
            if not isinstance(bots_table, dict):
                mismatches.append({"module": name, "table": bots_attr,
                                   "item": "-", "bots": repr(bots_table),
                                   "wheel": "not a table"})
                counts[bots_attr] = -1
                continue
            counts[bots_attr] = len(bots_table)
            for item, bots_value in bots_table.items():
                coverage[wheel_attr].add(item)
                if item not in wheel_table:
                    mismatches.append({"module": name, "table": bots_attr,
                                       "item": item, "bots": repr(bots_value),
                                       "wheel": "<absent from wheel>"})
                elif dict(bots_value) != dict(wheel_table[item]):
                    mismatches.append({"module": name, "table": bots_attr,
                                       "item": item,
                                       "bots": repr(dict(bots_value)),
                                       "wheel": repr(dict(wheel_table[item]))})
        entry_counts[name] = counts

    report = {
        "ok": not mismatches,
        "checked_modules": list(BOTS_CONSTANT_MODULES),
        "crops_entries": {n: entry_counts.get(n, {}).get("CROPS_INFO", 0)
                          for n in BOTS_CONSTANT_MODULES},
        "animals_entries": {n: entry_counts.get(n, {}).get("ANIMALS_INFO", 0)
                            for n in BOTS_CONSTANT_MODULES},
        "coverage": {w_attr: sorted(items)
                     for w_attr, items in coverage.items()},
        "mismatches": mismatches,
        "wheel_source": str(Path(getattr(wheel_source, "__file__",
                                         "<?>")).resolve()),
    }
    if mismatches:
        detail = "; ".join(
            f"{m['module']}.{m['table']}[{m['item']}]: bots={m['bots']} "
            f"wheel={m['wheel']}" for m in mismatches[:8])
        raise BotsConstantsMismatch(
            f"bots 手抄常量与 wheel 真值漂移（{len(mismatches)} 处）: {detail}")
    return report
