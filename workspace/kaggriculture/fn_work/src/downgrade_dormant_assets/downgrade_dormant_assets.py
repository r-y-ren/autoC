"""gym_env/llm_provider 移实验区（dormant 标注）、economy/redlines 移测试资产区、主线 import 图断言收口的顶层编排（旧树冻结：本批只落分区注册 fn_work/asset_zones.json+验证，零物理搬移；物理搬移属战后 fn-close 期按注册表逐件 git mv）。

上游: R13, R14（详见 fn_docs/responsibility.md）

实现要点：
- 四件 designation（DESIGNATION_TABLE，模块级唯一事实源）：gym_env（半休眠，
  仅冒烟续命）/bots.llm_provider（实验件默认关，未接入提交链）→ dormant_lab；
  economy/redlines（评估链孤儿，仅测试资产/语义对照消费）→ test_asset。
- 编排四步：①四件在场核验（缺件 fail-closed）；②旧树只读消费面扫描
  （prune_mainline_import_graph.scan_legacy_consumers：direct+transitive，
  作 designation 依据如实入注册表）；③主线断言 fn_work/src import 图不含四件
  （prune_mainline_import_graph；B13 前 fn_work 消费面应零，非零即如实报告
  overall=False）；④注册表 schema 校验+落盘。
- 传递面如实披露不判负：fn_work/src 声明 import kgenv.<非四件模块> 经旧树
  kgenv/__init__.py 的 eager import 一跳触达 economy/redlines/gym_env——属
  旧树事实，战后随 __init__ 剔除消解（postwar_execution 已列步骤），主线
  断言只裁**直接声明面**（R13/R14 验收口径=主线 import 图不含四件）。
- 旧树零写入、零物理移动；注册表即战后搬移执行清单（postwar_dest 逐件）。
  路径全由调用方传入或经 shared.discover_campaign_roots 发现（R20：模块内
  零字面战役路径）。
- 注册表可移植性：落盘前把 build_import_graph 产出的 mainline root 绝对
  路径（str(root.resolve())）对战役根相对化（如 "fn_work/src"），注册表
  全文零机器绝对路径（跨机可 commit、diff 可复现）。
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from downgrade_dormant_assets.prune_mainline_import_graph import (
    ZONE_DORMANT_LAB,
    ZONE_TEST_ASSET,
    build_import_graph,
    prune_mainline_import_graph,
    scan_legacy_consumers,
    transitive_member_exposure,
)
from shared.discover_campaign_roots import discover_campaign_roots

__all__ = ["downgrade_dormant_assets", "DESIGNATION_TABLE",
           "REQUIRED_ENTRY_KEYS", "DORMANT_LAB_POSTWAR_DIR",
           "TEST_ASSET_POSTWAR_DIR"]

# 战后落位（战役根相对，子树形态保持）；本批只登记，零物理移动
DORMANT_LAB_POSTWAR_DIR = "dormant_lab"
TEST_ASSET_POSTWAR_DIR = "test_assets"

# 注册表条目必备键（schema 完整性校验；module_ids/postwar_dest 为本批附加键）
REQUIRED_ENTRY_KEYS = ("file", "zone", "reason", "current_consumers",
                       "postwar_action")

# R13/R14 四件 designation（file 相对 software 根）——模块级唯一事实源
DESIGNATION_TABLE: dict[str, dict] = {
    "kgenv/gym_env.py": {
        "zone": ZONE_DORMANT_LAB,
        "module_ids": ["kgenv.gym_env"],
        "reason": "半休眠件（R13/G15）：gym 环仅冒烟续命（smoke_boot 一处），"
                  "评估链主线不依赖；降级 dormant 实验区，冒烟路径战后显式引用实验区",
        "postwar_action": "git mv 至 dormant_lab/kgenv/gym_env.py；"
                          "kgenv/__init__.py 剔除 gym_env eager import；"
                          "smoke_boot.py 冒烟改显式引用实验区（R13 验收口径）",
    },
    "kgenv/bots/llm_provider.py": {
        "zone": ZONE_DORMANT_LAB,
        "module_ids": ["kgenv.bots.llm_provider"],
        "reason": "实验件默认关（R13/G15）：NullProvider 默认态、未接入提交链，"
                  "bots/__init__ 不 eager import；仅 run_llm_ab 实验脚本与"
                  " eval_hardening 测试引用；降级 dormant 实验区",
        "postwar_action": "git mv 至 dormant_lab/kgenv/bots/llm_provider.py；"
                          "run_llm_ab.py/test_eval_hardening.py 引用面随迁改道"
                          "（实验件默认关语义不变）",
    },
    "kgenv/economy.py": {
        "zone": ZONE_TEST_ASSET,
        "module_ids": ["kgenv.economy"],
        "reason": "评估链孤儿（R14/G16）：量化收益模型仅测试资产消费"
                  "（test_economy）+redlines 语义对照；评估链主线不依赖；"
                  "降级纯测试资产区",
        "postwar_action": "git mv 至 test_assets/kgenv/economy.py；"
                          "kgenv/__init__.py 剔除 economy eager import；"
                          "test_economy.py 引用改道；与 redlines 同批搬迁保成员内边",
    },
    "kgenv/redlines.py": {
        "zone": ZONE_TEST_ASSET,
        "module_ids": ["kgenv.redlines"],
        "reason": "评估链孤儿（R14/G16）：红线清单仅测试消费（test_redlines），"
                  "语义对照面；依赖 economy（成员内边）；降级纯测试资产区",
        "postwar_action": "git mv 至 test_assets/kgenv/redlines.py；"
                          "kgenv/__init__.py 剔除 redlines eager import；"
                          "test_redlines.py 引用改道",
    },
}

_REGISTRY_CONTRACT = "R13+R14 downgrade_dormant_assets（fn_docs/responsibility.md）"


def _campaign_rel_posix(path, campaign_root: Path) -> str:
    """绝对路径 → 战役根相对 posix（注册表可移植：零机器绝对路径）。

    build_import_graph 的 root 为 str(root.resolve()) 机器绝对路径，落盘前
    对战役根相对化（如 "fn_work/src"）；路径不在战役根内时以 relpath 兜底
    （可能含 ".."，但仍为相对形态，不落绝对路径）。
    """
    resolved = Path(path).resolve()
    base = campaign_root.resolve()
    try:
        return resolved.relative_to(base).as_posix()
    except ValueError:
        return Path(os.path.relpath(resolved, base)).as_posix()


def _postwar_execution(zone_counts: dict) -> dict:
    return {
        "when": "fn-close 期（战后收口，旧树冻结解除后）",
        "registry_only": True,
        "steps": [
            f"dormant_lab {zone_counts[ZONE_DORMANT_LAB]} 件按 postwar_dest "
            f"逐件 git mv 至 {DORMANT_LAB_POSTWAR_DIR}/（保持 kgenv 子树形态）",
            f"test_asset {zone_counts[ZONE_TEST_ASSET]} 件按 postwar_dest "
            f"逐件 git mv 至 {TEST_ASSET_POSTWAR_DIR}/（economy/redlines 同批）",
            "kgenv/__init__.py 剔除 economy/redlines/gym_env eager import"
            "（消除 `import kgenv.*` 对四件中三件的传递触达面）",
            "消费面改道：smoke_boot 冒烟显式引用实验区（R13 验收）；"
            "test_economy/test_redlines/run_llm_ab/test_eval_hardening 改道新位",
            "验收复跑：主线 import 图不含四件（R13/R14）+ 全量测试绿",
        ],
        "note": "本批零物理移动（旧树冻结）；本注册表即战后搬移执行清单。",
    }


def _validate_schema(entries: list[dict], software_root: Path) -> list[str]:
    """注册表条目 schema 校验（返回错误清单；空清单=完整）。"""
    errors: list[str] = []
    zones = (ZONE_DORMANT_LAB, ZONE_TEST_ASSET)
    for entry in entries:
        file = entry.get("file", "<missing>")
        for key in REQUIRED_ENTRY_KEYS:
            if key not in entry:
                errors.append(f"{file}: 缺必备键 {key}")
        if entry.get("zone") not in zones:
            errors.append(f"{file}: zone 非法 {entry.get('zone')!r} "
                          f"（合法: {zones}）")
        for key in ("reason", "postwar_action"):
            if not str(entry.get(key, "")).strip():
                errors.append(f"{file}: {key} 为空")
        consumers = entry.get("current_consumers")
        if not isinstance(consumers, dict) or \
                not isinstance(consumers.get("direct"), list):
            errors.append(f"{file}: current_consumers 须为 "
                          f"{{direct: [...]}} dict")
        if not entry.get("module_ids"):
            errors.append(f"{file}: module_ids 为空")
        if not str(entry.get("postwar_dest", "")).strip():
            errors.append(f"{file}: postwar_dest 为空")
        if not (software_root / str(entry.get("file", ""))).is_file():
            errors.append(f"{file}: 旧树缺件（在场核验已先行，此处为冗余闸）")
    return errors


def downgrade_dormant_assets(*, software_root=None, mainline_root=None,
                             registry_path=None) -> dict:
    """四件分区 designation+旧树消费面登记+主线 import 图断言+注册表落盘，返回裁决 dict。

    Args:
        software_root: 旧树根（<战役根>/software，只读）；None=按
            discover_campaign_roots 发现。
        mainline_root: 主线布局根（断言对象）；None=战役根/fn_work/src。
        registry_path: 注册表落盘路径；None=战役根/fn_work/asset_zones.json。

    Returns:
        裁决 dict：{overall, designated_files, zone_counts, missing_designated,
        legacy_consumers, mainline: {root, files, declared_imports, violations,
        transitive_exposure}, schema_valid, schema_errors, registry_path,
        frozen_tree, summary}
        mainline.root 为战役根相对 posix（如 "fn_work/src"，注册表零绝对路径）；
        registry_path 为落盘绝对路径（仅进程内返回，不入注册表）。
        overall ⇔ 四件全在场 + fn_work/src 主线 import 图不含四件 + 注册 schema 完整。

    Raises:
        ValueError: 四件任一在旧树缺失（fail-closed，不猜布局）。
    """
    if software_root is None:
        software_root = discover_campaign_roots()["software_root"]
    software = Path(software_root)
    campaign_root = software.parent
    mainline = Path(mainline_root) if mainline_root is not None \
        else campaign_root / "fn_work" / "src"

    # ---- ① 四件在场核验（fail-closed）----
    missing = sorted(f for f in DESIGNATION_TABLE
                     if not (software / f).is_file())
    if missing:
        raise ValueError(
            f"指定四件中 {len(missing)} 件在旧树缺失，fail-closed 拒绝降级登记: "
            f"{missing}\n排查: 确认传入 <战役根>/software（四件清单见 "
            f"DESIGNATION_TABLE，R13/R14 designation 依据）。")

    zone_members = {mid: spec["zone"]
                    for spec in DESIGNATION_TABLE.values()
                    for mid in spec["module_ids"]}

    # ---- ② 旧树只读消费面扫描（designation 依据，如实入注册表）----
    legacy_graph = build_import_graph(software)
    legacy = scan_legacy_consumers(software, zone_members,
                                   graph=legacy_graph)

    # ---- ③ 主线断言：fn_work/src import 图不含四件（B13 前应零，非零如实报告）----
    mainline_graph, violations = prune_mainline_import_graph(
        mainline, zone_members=zone_members)
    mainline_transitive: list[dict] = []
    member_ids = set(zone_members)
    for rel in sorted(mainline_graph["files"]):
        for edge in mainline_graph["files"][rel]["imports"]:
            if edge["target"] in member_ids:
                continue  # direct 违例已裁，不重复入传递面
            for expo in transitive_member_exposure(edge["target"], legacy_graph,
                                                   zone_members):
                mainline_transitive.append(
                    {"importer": rel, "imported": edge["target"],
                     "member": expo["member"], "via": expo["via"]})
    mainline_transitive = sorted(
        {(_t["importer"], _t["imported"], _t["member"]): _t
         for _t in mainline_transitive}.values(),
        key=lambda _t: (_t["importer"], _t["imported"], _t["member"]))

    # ---- ④ 注册表组装 + schema 校验 + 落盘 ----
    postwar_dir = {ZONE_DORMANT_LAB: DORMANT_LAB_POSTWAR_DIR,
                   ZONE_TEST_ASSET: TEST_ASSET_POSTWAR_DIR}
    entries = []
    for file in sorted(DESIGNATION_TABLE):
        spec = DESIGNATION_TABLE[file]
        mids = spec["module_ids"]
        consumers = {"direct": [c for mid in mids
                                for c in legacy[mid]["direct"]],
                     "transitive": [c for mid in mids
                                    for c in legacy[mid]["transitive"]]}
        entries.append({
            "file": file,
            "zone": spec["zone"],
            "module_ids": mids,
            "reason": spec["reason"],
            "current_consumers": consumers,
            "postwar_action": spec["postwar_action"],
            "postwar_dest": f"{postwar_dir[spec['zone']]}/{file}",
        })
    zone_counts = {ZONE_DORMANT_LAB: 0, ZONE_TEST_ASSET: 0}
    for entry in entries:
        zone_counts[entry["zone"]] += 1
    schema_errors = _validate_schema(entries, software)
    schema_valid = not schema_errors

    mainline_block = {
        # 落盘前相对化：graph root 的机器绝对路径 → 战役根相对（如 "fn_work/src"）
        "root": _campaign_rel_posix(mainline_graph["root"], campaign_root),
        "files": mainline_graph["counts"]["files"],
        "declared_imports": mainline_graph["counts"]["declared_imports"],
        "violations": violations,
        "transitive_exposure": mainline_transitive,
    }
    overall = not violations and schema_valid
    legacy_summary = {f: {"direct": len(legacy[m]["direct"]),
                          "transitive": len(legacy[m]["transitive"])}
                      for f, spec in sorted(DESIGNATION_TABLE.items())
                      for m in spec["module_ids"]}
    summary = (
        f"四件登记（dormant_lab {zone_counts[ZONE_DORMANT_LAB]}/"
        f"test_asset {zone_counts[ZONE_TEST_ASSET]}）；旧树 direct 消费面 "
        f"gym_env={legacy_summary['kgenv/gym_env.py']['direct']}/"
        f"llm_provider={legacy_summary['kgenv/bots/llm_provider.py']['direct']}/"
        f"economy={legacy_summary['kgenv/economy.py']['direct']}/"
        f"redlines={legacy_summary['kgenv/redlines.py']['direct']}；"
        f"主线（fn_work/src {mainline_block['files']} 件/"
        f"{mainline_block['declared_imports']} 边）直接消费四件 "
        f"{len(violations)} 处（B13 前预期 0）"
        f"{'，传递面 ' + str(len(mainline_transitive)) + ' 处经 kgenv/__init__（战后随 eager import 剔除消解，不判负）' if mainline_transitive else ''}"
        f"；schema{'完整' if schema_valid else '破损'}"
        f"——{'PASS' if overall else 'FAIL'}")

    verdict = {
        "overall": overall,
        "designated_files": len(entries),
        "zone_counts": zone_counts,
        "missing_designated": missing,
        "legacy_consumers": legacy,
        "mainline": mainline_block,
        "schema_valid": schema_valid,
        "schema_errors": schema_errors,
        "frozen_tree": True,
        "postwar_only": True,
        "summary": summary,
    }

    registry = {
        "contract": _REGISTRY_CONTRACT,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "frozen_tree": True,
        "postwar_execution": _postwar_execution(zone_counts),
        "zone_counts": zone_counts,
        "entries": entries,
        "mainline_check": mainline_block,
        "legacy_consumers": legacy,
        "verdict": verdict,
    }
    reg_path = Path(registry_path) if registry_path is not None \
        else campaign_root / "fn_work" / "asset_zones.json"
    reg_path.parent.mkdir(parents=True, exist_ok=True)
    reg_path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8", newline="\n")
    verdict["registry_path"] = str(reg_path)
    return verdict
