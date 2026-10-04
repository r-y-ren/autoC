"""程序化发现战役根/仓根/软件根（目录特征过滤：含 blueprint.md+software+fn_docs 者=战役根），返回 campaign_root/repo_root/software_root 具名结构，取代一切字面战役路径与"仓根 CWD 假设"，找不到特征目录即抛 RootDiscoveryError（fail-closed，不猜）。

上游: R20（详见 fn_docs/responsibility.md）

实现要点：
- 仓根特征 = .git 与 AGENTS.md 并存（.git 文件形态——worktree——亦认）；战役根特征 =
  新布局=fn_docs+fn_work 两件齐备（2026-09-23 大整合后唯一形态）；兼容旧布局 blueprint.md+software+fn_docs；software_root=战役根/software（旧）或 fn_work/legacy_software（新）。
- 默认起点按本模块 __file__ 上溯，与进程 CWD 完全无关（取代"仓根 CWD 假设"）。
- 起点位于战役树外（如仓根）时，回落扫描仓内标准多战役容器（布局约定 workspace/<cid>/，
  AGENTS.md）的直接子目录：特征完备者恰一个才采纳；多个=歧义、零个=未找到，均 fail-closed。
- 本模块零字面战役路径/战役名（R20）；调用点亦不得拼接字面战役名。
"""

from pathlib import Path

__all__ = ["RootDiscoveryError", "discover_campaign_roots"]

# 战役根目录特征（三者齐备才算；缺任一即不算，宁缺毋滥）
_CAMPAIGN_FEATURES = ("fn_docs", "fn_work")
_REPO_FEATURES = (".git", "AGENTS.md")
# 仓内标准多战役容器名（仓库布局约定，非战役名）；仅作战役树外起点的回落扫描范围
_WORKSPACE_DIRNAME = "workspace"

_LEGACY_CAMPAIGN_FEATURES = ("blueprint.md", "software", "fn_docs")
_FEATURE_LIST_TEXT = "+".join(_CAMPAIGN_FEATURES)
_REPO_FEATURE_LIST_TEXT = "+".join(_REPO_FEATURES)


class RootDiscoveryError(RuntimeError):
    """特征目录定位失败（fail-closed）：不猜路径、不回退默认、不带 CWD 假设。"""


def _has_features(base: Path, features: tuple[str, ...]) -> bool:
    return all((base / name).exists() for name in features)


def _walk_up(start: Path, features: tuple[str, ...]) -> Path | None:
    """自 start（含自身）逐级上溯，返回首个特征齐备的祖先目录；无则 None。"""
    for candidate in (start, *start.parents):
        if _has_features(candidate, features):
            return candidate
    return None


def _campaign_candidates(repo_root: Path) -> list[Path]:
    """仓内标准容器下特征完备的战役目录（仅直接子目录一层；排序保确定性）。"""
    container = repo_root / _WORKSPACE_DIRNAME
    if not container.is_dir():
        return []
    return sorted(
        p for p in container.iterdir()
        if p.is_dir() and ((_has_features(p, _CAMPAIGN_FEATURES) or _has_features(p, _LEGACY_CAMPAIGN_FEATURES)) or _has_features(p, _LEGACY_CAMPAIGN_FEATURES))
    )


def discover_campaign_roots(start_path=None) -> dict:
    """以目录特征发现三根（仓根/战役根/软件根），结果与进程 CWD 无关。

    Args:
        start_path: 发现起点，文件或目录均可；None=按本模块 __file__ 上溯。
            起点在战役树内时直接上溯命中；在仓内但战役树外（如仓根）时回落
            扫描标准容器 workspace/ 的直接子目录。

    Returns:
        dict，三键均为绝对 Path（已 resolve）：
        {"campaign_root": …, "repo_root": …, "software_root": …}

    Raises:
        RootDiscoveryError: 起点不存在 / 战役根不可定位 / 仓根不可定位 /
            多战役歧义 / 战役根不在仓根之内——一律 fail-closed，消息附排查提示。
    """
    if start_path is None:
        search = Path(__file__).resolve()
    else:
        search = Path(start_path).expanduser()
        if not search.exists():
            raise RootDiscoveryError(
                f"起点路径不存在: {search}\n"
                f"排查: 传入实际存在的文件/目录（战役树内任意路径均可），"
                f"或留空让起点默认取本模块 __file__ 上溯。"
            )
        search = search.resolve()

    repo_root = _walk_up(search, _REPO_FEATURES)
    campaign_root = _walk_up(search, _CAMPAIGN_FEATURES) or _walk_up(
        search, _LEGACY_CAMPAIGN_FEATURES
    )

    if campaign_root is None and repo_root is not None:
        # 起点在战役树外（如仓根本身）：回落扫描标准容器，恰一命中才采纳
        candidates = _campaign_candidates(repo_root)
        if len(candidates) == 1:
            campaign_root = candidates[0]
        elif len(candidates) > 1:
            listed = ", ".join(str(p.relative_to(repo_root)) for p in candidates)
            raise RootDiscoveryError(
                f"仓内发现多个特征完备的战役目录，拒绝猜测: {listed}\n"
                f"排查: 以目标战役树内路径作为 start_path 传入以消歧"
                f"（战役根特征={_FEATURE_LIST_TEXT}）。"
            )

    if campaign_root is None:
        raise RootDiscoveryError(
            f"未找到战役根（特征={_FEATURE_LIST_TEXT}），上溯起点: {search}\n"
            f"排查: ①确认起点位于战役树内（战役根=fn_docs+fn_work（新布局）或 blueprint.md+software+fn_docs（旧布局））；"
            f"②自仓内战役树外调用时仅回落扫描 {_WORKSPACE_DIRNAME}/ 直接子目录，"
            f"确认容器下存在特征完备目录；③三特征件缺一不可，检查是否被改名或移动。"
        )

    if repo_root is None:
        raise RootDiscoveryError(
            f"找到战役根 {campaign_root}，但其上无仓根"
            f"（特征={_REPO_FEATURE_LIST_TEXT} 并存）\n"
            f"排查: ①确认该战役位于本仓库内而非孤立/外部副本；"
            f"②仓根特征件缺失时先补齐（.git 目录或 worktree .git 文件 + AGENTS.md）。"
        )

    if repo_root not in campaign_root.parents:
        raise RootDiscoveryError(
            f"战役根不在仓根之内（campaign_root={campaign_root}, "
            f"repo_root={repo_root}），布局不合约定（仓根应包含战役根）\n"
            f"排查: 确认起点指向仓库内的战役树，而非特征巧合的外部同名目录。"
        )

    return {
        "campaign_root": campaign_root,
        "repo_root": repo_root,
        "software_root": (campaign_root / "software") if (campaign_root / "software").is_dir() else (campaign_root / "fn_work" / "legacy_software"),
    }
