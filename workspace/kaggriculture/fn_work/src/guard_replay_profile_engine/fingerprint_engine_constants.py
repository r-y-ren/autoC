"""replay_profile 引擎常量集提取与 sha256 指纹计算+登记值维护（升版 wheel 时显式重登记流程）。

上游: R5（详见 fn_docs/responsibility.md）

实现要点：
- 钉护对象 = 旧树 kgenv/replay_profile.py :564-626 的手写引擎镜像常量块——其后
  ~1050 行复算（价格公式/棚容/城镇需求等）全部建立在这份常量手抄镜像之上，而此前
  零指纹看护（R5 缺陷本体）。选定应钉常量键集（登记清单，五类共 16 键）：
    * 价格参数类: S_MARKET_PARAMS / S_MARKET_I0 / S_PRICE_FLOOR / S_HINGE_GAIN
    * 经济表类:   S_CROPS / S_ANIMALS / S_PRODUCTS / S_LAND_ORDER / S_LAND_PRICES
    * 容量类:     S_DEFAULT_CONFIG（含 shedCapacity/boardSize/episodeSteps 等 11 键）
    * 城镇需求类: S_SHOPS / S_TOWN_CENTER_PRODUCTS / S_MAX_SHOP_INSTANCES
    * 几何与操作语义类: S_FARMER_MOVES / S_FAILS / S_UNIT_OPS_TRACKED
  SUCCESS_PROTOCOL 是协议版本标记而非引擎常量，刻意不钉。
- 指纹 = 键集值经规范化序列化（递归 tuple->list，键排序，JSON 紧凑分隔）后的
  sha256；任何键值/键集漂移必然改变指纹（fail-closed 语义的根基）。
- wheel 侧真值交叉比对通道（kgenv/economy.py 的 re-export 先例）：直接 import
  kaggle_environments.envs.kaggriculture.kaggriculture——kgenv/engine.py 装载的
  同一安装副本；其与 software/vendor/ wheel 逐文件一致由旧树 twin P1 指纹链背书
  （WHEEL_PROVENANCE.md 留痕）。可比对键集 = 除 S_FAILS / S_UNIT_OPS_TRACKED
  （镜像自有的归因口径表，wheel 无对应物）外的 14 键；S_DEFAULT_CONFIG 的 wheel
  侧真值取场景 kaggriculture.json 的 configuration defaults（按镜像所引键子集）。
  wheel 不可 import 时交叉比对记 skip+原因（主门仍是登记指纹），不冒进抛错。
- 登记值维护：REGISTERED_FINGERPRINT 为源码默认登记值（建立时点已用
  cross_check_against_wheel 全绿锚定于 wheel 真值）；set_registered_fingerprint
  为运行期显式重登记接口（测试注入用）；升版 wheel 正式流程 =
  ①更新 replay_profile 镜像常量 -> ②cross_check_against_wheel 全绿 ->
  ③fingerprint_engine_constants 取新指纹 -> ④重登记并把新值固化回本模块源码
  默认登记值，随 commit 留痕。绕过 ②③ 的任何常量改动都会被守卫打红。
- 旧树只读消费：默认源经 __file__ 上溯发现战役根（blueprint.md+software+
  fn_docs 三特征齐备）后 import 旧树 kgenv.replay_profile（只读；包初始化依赖
  缺失时回退按文件路径装载——replay_profile 本体纯 stdlib）。不 import 旧树
  scripts/；不写任何旧树文件。
"""

from __future__ import annotations

import hashlib
import importlib
import importlib.util
import json
import sys
from pathlib import Path

__all__ = [
    "PINNED_CONSTANT_KEYS",
    "WHEEL_COMPARABLE_KEYS",
    "ConstantExtractionError",
    "EngineFingerprintError",
    "extract_engine_constants",
    "fingerprint_engine_constants",
    "get_registered_fingerprint",
    "set_registered_fingerprint",
    "reset_registered_fingerprint",
    "cross_check_against_wheel",
]

# 战役根目录特征（三件齐备才算；与仓库布局约定一致，不写字面战役路径）
_CAMPAIGN_FEATURES = ("blueprint.md", "software", "fn_docs")
# 旧树镜像模块（只读消费）
_MODULE_NAME = "kgenv.replay_profile"

# --------------------------------------------------------------------------- #
# 选定应钉常量键集（登记清单；顺序固定，指纹不受传入序影响）
# --------------------------------------------------------------------------- #
PINNED_CONSTANT_KEYS: tuple[str, ...] = (
    # 价格参数类
    "S_MARKET_PARAMS", "S_MARKET_I0", "S_PRICE_FLOOR", "S_HINGE_GAIN",
    # 经济表类
    "S_CROPS", "S_ANIMALS", "S_PRODUCTS", "S_LAND_ORDER", "S_LAND_PRICES",
    # 容量类
    "S_DEFAULT_CONFIG",
    # 城镇需求类
    "S_SHOPS", "S_TOWN_CENTER_PRODUCTS", "S_MAX_SHOP_INSTANCES",
    # 几何与操作语义类
    "S_FARMER_MOVES", "S_FAILS", "S_UNIT_OPS_TRACKED",
)

# wheel 侧模块常量名映射（economy.py re-export 先例；13 个模块级常量 +
# S_DEFAULT_CONFIG 经场景 json defaults 通道，共 14 个可比对键）
_WHEEL_NAME_MAP: dict[str, str] = {
    "S_CROPS": "CROPS",
    "S_ANIMALS": "ANIMALS",
    "S_PRODUCTS": "PRODUCTS",
    "S_PRICE_FLOOR": "PRICE_FLOOR",
    "S_HINGE_GAIN": "HINGE_GAIN",
    "S_MARKET_PARAMS": "MARKET_PARAMS",
    "S_MARKET_I0": "MARKET_I0",
    "S_FARMER_MOVES": "FARMER_MOVES",
    "S_LAND_ORDER": "LAND_ORDER",
    "S_LAND_PRICES": "LAND_PRICES",
    "S_SHOPS": "SHOPS",
    "S_TOWN_CENTER_PRODUCTS": "TOWN_CENTER_PRODUCTS",
    "S_MAX_SHOP_INSTANCES": "MAX_SHOP_INSTANCES",
}
# S_DEFAULT_CONFIG 的 wheel 侧真值来源：场景 json 的 configuration defaults
_CONFIG_KEY = "S_DEFAULT_CONFIG"
_WHEEL_COMPARABLE_EXTRA = (_CONFIG_KEY,)
WHEEL_COMPARABLE_KEYS: tuple[str, ...] = (
    *tuple(sorted(_WHEEL_NAME_MAP)), *_WHEEL_COMPARABLE_EXTRA)

# 登记指纹（建立时点锚定于 wheel 真值；升版 wheel 须经显式重登记流程更新）
REGISTERED_FINGERPRINT = "69fd142e443f6d14fd889b5f1175fe94bd415b574ca1ddf3d16bd80fe8d1146f"


class ConstantExtractionError(RuntimeError):
    """常量集提取失败（键缺失/源不可装载/值不可规范化）——fail-closed。"""


class EngineFingerprintError(RuntimeError):
    """引擎指纹不符（镜像常量与登记值或 wheel 真值漂移）——fail-closed。"""


# 运行期登记表（显式重登记接口维护；默认=源码登记值）
_registry: dict[str, str] = {"registered_fingerprint": REGISTERED_FINGERPRINT}


# --------------------------------------------------------------------------- #
# 源装载（旧树只读）
# --------------------------------------------------------------------------- #
def _campaign_software_root() -> Path:
    """自本模块 __file__ 上溯发现战役根，返回其 software/ 子目录（fail-closed）。"""
    here = Path(__file__).resolve()
    for candidate in (here, *here.parents):
        if all((candidate / name).exists() for name in _CAMPAIGN_FEATURES):
            return candidate / "software"
    raise ConstantExtractionError(
        "未找到战役根（特征=" + "+".join(_CAMPAIGN_FEATURES) + "），"
        f"上溯起点: {here}")


def load_replay_profile_module():
    """装载旧树 kgenv.replay_profile（只读；进程内缓存）。

    优先 sys.modules 已缓存实例（守卫与测试对同一实例的 monkeypatch 可见）；
    其次常规包 import（需 kgenv/__init__ 的依赖齐备）；包初始化失败时回退
    按文件路径装载（replay_profile 本体纯 stdlib，无包外依赖）。
    """
    cached = sys.modules.get(_MODULE_NAME)
    if cached is not None:
        return cached
    software = _campaign_software_root()
    if str(software) not in sys.path:
        sys.path.insert(0, str(software))
    try:
        return importlib.import_module(_MODULE_NAME)
    except Exception:
        # 包初始化链（kgenv/__init__ 拉 kaggle_environments 等）不可用时，
        # 回退按文件直接装载镜像本体——它是纯 stdlib 模块。
        path = software / "kgenv" / "replay_profile.py"
        if not path.is_file():
            raise ConstantExtractionError(
                f"镜像源文件不存在且包 import 失败: {path}") from None
        spec = importlib.util.spec_from_file_location(_MODULE_NAME, path)
        if spec is None or spec.loader is None:
            raise ConstantExtractionError(f"无法构造装载 spec: {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[_MODULE_NAME] = module  # 缓存，后续调用同一实例
        spec.loader.exec_module(module)
        return module


# --------------------------------------------------------------------------- #
# 提取与指纹
# --------------------------------------------------------------------------- #
def _canonicalize(value):
    """递归规范化：tuple->list、dict 键保持原序（外层统一排序）。"""
    if isinstance(value, dict):
        return {str(k): _canonicalize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_canonicalize(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise ConstantExtractionError(
        f"常量值含不可规范化的类型: {type(value).__name__} ({value!r:.80})")


def _canonical_json(values: dict) -> str:
    return json.dumps(
        {key: _canonicalize(values[key]) for key in sorted(values)},
        sort_keys=True, ensure_ascii=True, separators=(",", ":"))


def _sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract_engine_constants(constants_source=None, keys=None) -> dict:
    """从镜像源提取选定键集的常量值（键缺失即抛，fail-closed）。

    Args:
        constants_source: 模块对象/含常量属性的任意对象；None=装载旧树
            kgenv.replay_profile 默认源。
        keys: 键元组；None=PINNED_CONSTANT_KEYS。

    Returns:
        dict {键: 值}（仅选定键集）。

    Raises:
        ConstantExtractionError: 源不可装载 / 任一键缺失 / 值不可规范化。
    """
    if constants_source is None:
        constants_source = load_replay_profile_module()
    selected = tuple(keys) if keys is not None else PINNED_CONSTANT_KEYS
    values: dict = {}
    for key in selected:
        if not hasattr(constants_source, key):
            raise ConstantExtractionError(
                f"常量源缺少应钉键: {key}（选定键集共 {len(selected)} 键，"
                "键集登记清单见 PINNED_CONSTANT_KEYS）")
        values[key] = getattr(constants_source, key)
    _canonical_json(values)  # 预检可规范化（不可规范化在此抛）
    return values


def fingerprint_engine_constants(constants_source=None, *, keys=None) -> str:
    """提取镜像常量集并计算 sha256 指纹（64 位十六进制）。

    Args:
        constants_source: 常量源（模块/任意对象）；None=默认装载旧树
            kgenv.replay_profile。
        keys: 键元组；None=完整选定键集。

    Returns:
        规范化序列化（键排序+tuple->list+紧凑 JSON）后的 sha256 hexdigest。

    Raises:
        ConstantExtractionError: 提取失败（见 extract_engine_constants）。
    """
    values = extract_engine_constants(constants_source, keys)
    return _sha256_hex(_canonical_json(values))


# --------------------------------------------------------------------------- #
# 登记值维护（升版 wheel 显式重登记）
# --------------------------------------------------------------------------- #
def get_registered_fingerprint() -> str:
    """当前登记指纹（默认=源码登记值；set 后=运行期重登记值）。"""
    return _registry["registered_fingerprint"]


def set_registered_fingerprint(value: str) -> None:
    """显式重登记（运行期）。升版 wheel 正式流程见模块 docstring；测试注入用。"""
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError("登记值须为 64 位十六进制 sha256 指纹字符串")
    _registry["registered_fingerprint"] = value


def reset_registered_fingerprint() -> None:
    """恢复源码默认登记值（重登记试验后收尾用）。"""
    _registry["registered_fingerprint"] = REGISTERED_FINGERPRINT


# --------------------------------------------------------------------------- #
# wheel 侧真值交叉比对
# --------------------------------------------------------------------------- #
def _wheel_constant_values(wheel_mod, mirror_config: dict | None) -> dict:
    """从 wheel 侧模块+场景 json 提取可比对键集的真值（S_ 名归一）。"""
    values = {s_key: getattr(wheel_mod, w_name)
              for s_key, w_name in sorted(_WHEEL_NAME_MAP.items())}
    json_path = Path(wheel_mod.__file__).resolve().with_name("kaggriculture.json")
    cfg = json.loads(json_path.read_text(encoding="utf-8"))["configuration"]
    defaults = {name: (spec.get("default") if isinstance(spec, dict) else spec)
                for name, spec in cfg.items()}
    if mirror_config is not None:
        # 按镜像所引键子集取真值（镜像刻意只跟踪其复算依赖的 11 个配置键）
        values[_CONFIG_KEY] = {k: defaults[k] for k in mirror_config}
    else:
        values[_CONFIG_KEY] = defaults
    return values


def cross_check_against_wheel(constants_source=None) -> dict:
    """镜像常量集 vs wheel 侧真值的逐键交叉比对（economy.py re-export 先例通道）。

    Args:
        constants_source: 镜像常量源；None=默认装载旧树 kgenv.replay_profile。

    Returns:
        dict：
          skipped/skip_reason —— wheel 不可 import 时 True+原因（主门仍是
              登记指纹，交叉比对记 skip 不抛）；
          ok —— 未 skip 时，可比对键集逐键相等为 True；
          comparable_keys —— 14 个可比对键；
          mismatches —— [{key, mirror, wheel}]（已规范化值的逐键差异）；
          wheel_fingerprint —— wheel 侧可比对键集（S_ 名归一+配置键子集对齐）
              的同口径指纹，供登记审计比对；
          wheel_source —— wheel 侧模块文件路径（provenance 留痕）。

    Raises:
        ConstantExtractionError: 镜像源提取失败。
    """
    mirror_values = extract_engine_constants(constants_source)
    try:
        from kaggle_environments.envs.kaggriculture import (
            kaggriculture as wheel_mod)
    except ImportError as exc:  # wheel 通道不可用：记 skip+原因，不抛
        return {"skipped": True,
                "skip_reason": f"kaggle_environments 不可 import: {exc}",
                "ok": None, "comparable_keys": list(WHEEL_COMPARABLE_KEYS),
                "mismatches": None, "wheel_fingerprint": None,
                "wheel_source": None}

    wheel_values = _wheel_constant_values(wheel_mod, mirror_values.get(_CONFIG_KEY))
    mismatches = []
    for key in WHEEL_COMPARABLE_KEYS:
        m = _canonicalize(mirror_values[key])
        w = _canonicalize(wheel_values[key])
        if m != w:
            mismatches.append({"key": key, "mirror": m, "wheel": w})
    return {"skipped": False, "skip_reason": None,
            "ok": not mismatches,
            "comparable_keys": list(WHEEL_COMPARABLE_KEYS),
            "mismatches": mismatches,
            "wheel_fingerprint": _sha256_hex(
                _canonical_json({k: wheel_values[k]
                                 for k in WHEEL_COMPARABLE_KEYS})),
            "wheel_source": str(Path(wheel_mod.__file__).resolve())}
