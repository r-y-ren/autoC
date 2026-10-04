"""四类最小集文件（flagoff golden/round23 灾难局/孪生 manifest+样例/对手池种子定义）
清单驱动收集到 fn_work/minimal_repro_set/，逐件登记 {category, source_path, sha256,
size, status}；缺失件登记 status=missing+回填办法，不因缺失中断（本机无 gitignored
语料时仍完成登记，主力机重跑本函数即补齐）。

上游: R19（详见 fn_docs/responsibility.md）

实现要点：
- 四类清单（R19 定桩）以 source_path 相对战役根声明，路径取自旧树脚本的真实
  常量（planner_flagoff_golden.py GOLDEN_PATH / round23_disaster_dtsp_probe.py
  REPLAY / twin_fidelity.py SUMMARY_PATH / kgenv 契约模块），不发明新路径。
- 逐件判定：文件在机 → sha256+size 并物理复制到
  <战役根>/fn_work/minimal_repro_set/<category>/<去 software|references 前缀子路径>；
  不在机 → status=missing + backfill（主力机补齐通道），登记不中断。
- 类别白名单 fail-closed：未知类别名抛 ValueError（清单驱动，不静默忽略）。
- 确定性：类别与条目按声明序（tuple 固定序）处理，无集合迭代序依赖；收集
  产物 manifest 双次构建逐字节一致（不含时钟字段，时间由 JOURNAL/git 记账）。
"""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

__all__ = ["CATEGORY_ORDER", "CATEGORY_SPEC", "collect_gate_golden_files"]

# R19 四类最小集清单（source_path 相对战役根；backfill=主力机补齐通道）。
# 顺序即 manifest 登记序（确定性），不得用集合迭代。
CATEGORY_ORDER = (
    "flagoff_golden",
    "disaster_replay",
    "twin_fidelity_manifest",
    "opponent_seed_definitions",
)

CATEGORY_SPEC: dict[str, dict] = {
    "flagoff_golden": {
        "label": "旗关等价黄金 JSON（DTSP 旗关 --check 基线）",
        "entries": (
            {
                "source_path": "software/exports/probes/planner_flagoff/golden_v138.json",
                "note": "含引擎指纹链与种子表（scripts/planner_flagoff_golden.py 定桩路径）",
                "backfill": "主力机重跑 python software/scripts/planner_flagoff_golden.py "
                            "--emit 捕获基线写入该路径后，重跑本收集函数（README 旗关等价节）",
            },
        ),
    },
    "disaster_replay": {
        "label": "round23 灾难局回放（ep110634204）",
        "entries": (
            {
                "source_path":
                    "references/data/online-replays/round23/episode-110634204-replay.json",
                "note": "灾难局接合证明数据源（scripts/round23_disaster_dtsp_probe.py 同路径）",
                "backfill": "主力机自线上 episode 拉取通道重新下载 round23 ep110634204 回放"
                            "至该路径后，重跑本收集函数",
            },
        ),
    },
    "twin_fidelity_manifest": {
        "label": "孪生保真抽样语料 manifest+样例",
        "entries": (
            {
                "source_path": "software/exports/twin/p1_fidelity_summary.md",
                "note": "P1 结论单源：指纹链（wheel/双文件 sha）+抽样种子 20260919+三窗",
                "backfill": "库内件（git 跟踪）；缺失属异常，自 git 历史回捞",
            },
            {
                "source_path": "software/exports/probes/twin_fidelity/fidelity_report.json",
                "note": "抽样逐局明细（数据中间物，R18 策略 gitignored）",
                "backfill": "主力机重跑 python software/scripts/twin_fidelity.py 生成后，"
                            "重跑本收集函数",
            },
            {
                "source_path": "software/exports/replay_profiles/index.json",
                "note": "m1 回放语料画像 manifest（在线池对手重构的语料侧台账）",
                "backfill": "库内件（git 跟踪）；缺失属异常，自 git 历史回捞",
            },
            {
                "source_path": "software/exports/replay_profiles/exclusions.json",
                "note": "画像语料排除清单（与 index.json 同源）",
                "backfill": "库内件（git 跟踪）；缺失属异常，自 git 历史回捞",
            },
            {
                "source_path": "references/data/replay-corpus/manifest.json",
                "note": "回放语料冻结核台账（corpus_integrity 蓝图验收 cmd 依赖，G23）",
                "backfill": "主力机 python software/scripts/corpus_fetch.py --stage 重建"
                            "台账后，重跑本收集函数",
            },
        ),
    },
    "opponent_seed_definitions": {
        "label": "对手池种子/roster 定义",
        "entries": (
            {
                "source_path": "software/kgenv/bots/__init__.py",
                "note": "对手名册（STRONG_OPPONENTS/ONLINE_STYLE_OPPONENTS+agents）",
                "backfill": "库内件（git 跟踪）；缺失属异常，自 git 历史回捞",
            },
            {
                "source_path": "software/kgenv/eval_contract.py",
                "note": "种子域单源（DEVELOPMENT_SEEDS 101-104/REGRESSION_SEEDS 201-208）",
                "backfill": "库内件（git 跟踪）；缺失属异常，自 git 历史回捞",
            },
            {
                "source_path": "software/kgenv/holdout_contract.py",
                "note": "holdout 种子域+历史种子冻结（38 枚单源）",
                "backfill": "库内件（git 跟踪）；缺失属异常，自 git 历史回捞",
            },
        ),
    },
}

# 收集落点相对战役根（fn_work 内新建许可由本批次授予）
DEFAULT_DEST_SUBDIR = "fn_work/minimal_repro_set"
# 复制子路径的前缀剥离规则：software/references 下的文件保其余子路径（防同名碰撞）
_STRIP_PREFIXES = ("software/", "references/")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _dest_relative_path(source_rel: str) -> Path:
    """源相对路径 → 类别目录内子路径（剥 software|references 前缀，其余 /→__）。"""
    rest = source_rel
    for prefix in _STRIP_PREFIXES:
        if rest.startswith(prefix):
            return Path(rest[len(prefix):])
    return Path(rest.replace("/", "__"))


def collect_gate_golden_files(category_list=None, *, campaign_root=None,
                               dest_dir=None) -> tuple:
    """按四类清单收集最小集文件到 fn_work/minimal_repro_set/，逐件登记。

    Args:
        category_list: 待收集类别名列表；None=全部四类（R19），[] =显式空集。
            未知类别名抛 ValueError（fail-closed，不静默忽略）。
        campaign_root: 战役根；None=shared.discover_campaign_roots 发现。
        dest_dir: 收集落点目录；None=<战役根>/fn_work/minimal_repro_set。

    Returns:
        (file_set, registry) 二元组：
        - file_set: collected 件登记列表（含 dest_path，供预算断言消费）；
        - registry: 全部条目登记（collected+missing，含 backfill 说明），
          每件 {category, source_path, dest_path, sha256, size, status, note, backfill}。
        missing 件不中断（本机缺 gitignored 语料为常态，登记回填通道）。
    """
    if category_list is None:
        category_list = list(CATEGORY_ORDER)
    unknown = [c for c in category_list if c not in CATEGORY_SPEC]
    if unknown:
        raise ValueError(
            f"未知最小集类别: {unknown}（合法类别={list(CATEGORY_ORDER)}）")

    if campaign_root is None:
        campaign_root = discover_campaign_roots()["campaign_root"]
    campaign_root = Path(campaign_root)
    if dest_dir is None:
        dest_dir = campaign_root / DEFAULT_DEST_SUBDIR
    dest_dir = Path(dest_dir)

    file_set: list[dict] = []
    registry: list[dict] = []
    for category in category_list:
        spec = CATEGORY_SPEC[category]
        for entry in spec["entries"]:
            source = campaign_root / entry["source_path"]
            record = {
                "category": category,
                "category_label": spec["label"],
                "source_path": entry["source_path"],
                "dest_path": None,
                "sha256": None,
                "size": None,
                "status": "missing",
                "note": entry["note"],
                "backfill": entry["backfill"],
            }
            if source.is_file():
                dest = (dest_dir / category / _dest_relative_path(entry["source_path"]))
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, dest)
                record.update(
                    status="collected",
                    dest_path=str(dest.relative_to(campaign_root)),
                    sha256=_sha256_file(source),
                    size=source.stat().st_size,
                )
                file_set.append(record)
            registry.append(record)
    return file_set, registry
