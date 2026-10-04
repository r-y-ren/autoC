"""run_pipeline（L0，R7）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

全管线确定性编排 + 账本：

* 七段编排（T1→T4）：mine_trajectories → build_route_library →
  derive_market_variants → search_reflector_configs（内含 R5 分离+留出
  裁决）→ assemble_and_gate（打包+M1/M2 门禁）。各段缺省=真函数，
  payload["stages"] 可按名注入替身（测试用假件）。
* **账本（链哈希）**：逐段一行 {stage, 产物 sha256 摘要, line_sha256,
  prev_sha256}——line_sha256 = sha256(canonical 行 ∥ prev_sha256)，
  尾部 chain_sha256 汇总；跨段对账（语料 corpus_hash / 库
  routes_sha256 / 选择 selection_sha256 / 候选包 main sha）进哈希链，
  T1-T4 任何一段变动都会改变链尾。
* **双跑一致**：payload["double_run"]=true 时整段编排跑两遍，比较
  canonical 账本与关键产物字节；结果入 runtime（实测侧件），不进账本
  （账本保持确定性）。
* 错误：任一段异常 fail-closed 上抛（管线不成即停，不产出半截账本）；
  门禁 FAIL **不是**管线错误——grading 如实透传（R6 分档）。

产物：fn_work/tape_gen/pipeline/{ledger.jsonl, ledger_head.json,
runtime_stats.json}。账本无墙钟/无时间戳——同输入双跑逐字节一致。
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

_SRC_ROOT = str(Path(__file__).resolve().parents[1])
if _SRC_ROOT not in sys.path:            # 脚本直跑（pytest 经 conftest 已加）
    sys.path.insert(0, _SRC_ROOT)

from assemble_and_gate.assemble_and_gate import assemble_and_gate
from derive_market_variants.derive_market_variants import (
    derive_market_variants,
)
from mine_trajectories.mine_trajectories import mine_trajectories
from build_route_library.build_route_library import build_route_library
from search_reflector_configs.search_reflector_configs import (
    search_reflector_configs,
)

_CAMPAIGN_ROOT = Path(__file__).resolve().parents[4]
_TAPE_GEN_ROOT = _CAMPAIGN_ROOT / "fn_work" / "tape_gen"
DEFAULT_OUTPUT_DIR = _TAPE_GEN_ROOT / "pipeline"

STAGE_ORDER = ("mine_trajectories", "build_route_library",
               "derive_market_variants", "search_reflector_configs",
               "assemble_and_gate")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _canonical(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def _file_sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class _Ledger:
    """链式账本：行哈希逐行咬合（prev_sha256 → line_sha256）。"""

    def __init__(self):
        self.lines = []
        self.prev = _sha256_text("tape_gen:genesis")

    def add(self, stage: str, digest: dict) -> dict:
        line = {"stage": stage, "prev_sha256": self.prev,
                "digest": digest}
        line["line_sha256"] = _sha256_text(_canonical(
            {"stage": stage, "digest": digest,
             "prev_sha256": self.prev}))
        self.lines.append(line)
        self.prev = line["line_sha256"]
        return line

    @property
    def chain_sha256(self):
        return self.prev

    def dumps(self) -> str:
        return "".join(_canonical(line) + "\n" for line in self.lines)


def _compose(payload, ledger: _Ledger) -> dict:
    """单遍全管线（真函数缺省；payload['stages'][name] 可注入替身）。"""
    stages = payload.get("stages") or {}

    def _stage(name, default_fn, stage_payload):
        fn = stages.get(name) or default_fn
        return fn(stage_payload)

    # ---- T1：挖掘 ----
    t1_payload = dict(payload.get("mine") or {})
    for key in ("corpus_dirs", "clone_reference", "own_team", "audit_games"):
        if key in payload:
            t1_payload.setdefault(key, payload[key])
    mine = _stage("mine_trajectories", mine_trajectories, t1_payload)
    ledger.add("mine_trajectories", {
        "corpus_hash": mine["corpus_hash"],
        "store_sha256": mine["store_sha256"],
        "kept_trajectories": mine["summary"]["kept"],
        "games": mine["summary"]["games"]})

    # ---- T2a：路由库 ----
    lib_payload = {"store_path": mine["paths"]["store"]}
    lib_payload.update(payload.get("library") or {})
    library = _stage("build_route_library", build_route_library, lib_payload)
    ledger.add("build_route_library", {
        "n_routes": library["n_routes"],
        "routes_sha256": library["routes_sha256"],
        "fidelity_all_ok": library["fidelity"]["all_ok"],
        "shared_prefix": library["fork_events"]["shared_prefix"],
        "store_sha256": library["store"]["sha256"]})

    # ---- T2b：市场变体 ----
    var_payload = {"library_dir": Path(
        library["paths"]["routes"]).parent}
    var_payload.update(payload.get("variants") or {})
    variants = _stage("derive_market_variants", derive_market_variants,
                      var_payload)
    ledger.add("derive_market_variants", {
        "n_variants": variants["n_variants"],
        "n_rejected": variants["n_rejected"],
        "variants_sha256": variants["variants_sha256"],
        "backbone_sha256": variants["backbone_sha256"]})

    # ---- T3：搜索+选择（内含 R5 分离与留出裁决）----
    search_payload = {"library_dir": var_payload["library_dir"],
                      "store_path": lib_payload["store_path"]}
    search_payload.update(payload.get("search") or {})
    search = _stage("search_reflector_configs", search_reflector_configs,
                    search_payload)
    ledger.add("search_reflector_configs", {
        "base_space_size": search["space"]["base_space_size"],
        "split_sha256": search["split"]["split_sha256"],
        "finalists": len(search["evaluation"]["finalists"]),
        "final_candidate_id":
            search["selection"]["final"]["candidate_id"],
        "selection_sha256":
            search["selection"]["final"]["selection_sha256"],
        "holdout_winrate":
            search["selection"]["final"]["holdout"]["winrate"]})

    # ---- T4：组装+门禁 ----
    asm_payload = {
        "library_dir": var_payload["library_dir"],
        "selection_path": (Path(search["paths"]["output_dir"])
                           / "final_selection.json"),
    }
    asm_payload.update(payload.get("assemble") or {})
    assembled = _stage("assemble_and_gate", assemble_and_gate, asm_payload)
    pkg = assembled["package"]
    ledger.add("assemble_and_gate", {
        "package_main_sha256": pkg["products"]["main_py"]["sha256"],
        "package_main_bytes": pkg["products"]["main_py"]["bytes"],
        "package_tar_sha256":
            pkg["products"]["submission_tar_gz"]["sha256"],
        "selection_sha256": pkg["selection"]["selection_sha256"],
        "grading": assembled["grading"]["overall"],
        "gate_report_sha256": _file_sha(
            assembled["gates"]["paths"]["report"])
        if assembled["gates"] and assembled["gates"].get("paths")
        else None})

    return {
        "mine": mine,
        "library": library,
        "variants": variants,
        "search": search,
        "assembled": assembled,
        "ledger": ledger,
    }


def run_pipeline(payload=None):
    """意图级签名；真值在责任文档。

    payload：各段覆盖键（mine/library/variants/search/assemble）+
    stages（按名注入替身）+ output_dir + double_run。
    返回 {ledger（行列表）, chain_sha256, grading, stages 摘要,
    runtime, paths}。
    """
    payload = dict(payload or {})
    output_dir = Path(payload.get("output_dir") or DEFAULT_OUTPUT_DIR)
    started = time.monotonic()

    first = _compose(payload, _Ledger())
    ledger = first["ledger"]
    runtime = {"wall_clock_s": round(time.monotonic() - started, 3)}
    double = {"double_run": False, "double_run_identical": None}
    if payload.get("double_run"):
        t1 = time.monotonic()
        second = _compose(payload, _Ledger())
        double = {
            "double_run": True,
            "double_run_identical": bool(
                second["ledger"].dumps() == ledger.dumps()),
            "second_chain_sha256": second["ledger"].chain_sha256,
        }
        double["double_run_wall_s"] = round(time.monotonic() - t1, 3)
        if not double["double_run_identical"]:
            raise RuntimeError("pipeline double-run ledger mismatch "
                               "(fail-closed)")

    output_dir.mkdir(parents=True, exist_ok=True)
    ledger_path = output_dir / "ledger.jsonl"
    ledger_path.write_text(ledger.dumps(), encoding="utf-8")
    head = {
        "protocol": "tape_gen-pipeline-ledger/1.0",
        "stage_order": list(STAGE_ORDER),
        "n_lines": len(ledger.lines),
        "chain_sha256": ledger.chain_sha256,
        "grading": first["assembled"]["grading"]["overall"],
    }
    (output_dir / "ledger_head.json").write_text(
        json.dumps(head, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n", encoding="utf-8")
    runtime.update(double)
    (output_dir / "runtime_stats.json").write_text(
        json.dumps(runtime, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n", encoding="utf-8")

    return {
        "ledger": ledger.lines,
        "chain_sha256": ledger.chain_sha256,
        "grading": first["assembled"]["grading"]["overall"],
        "gates": first["assembled"]["gates"],
        "package": first["assembled"]["package"],
        "stage_digests": [line["digest"] for line in ledger.lines],
        "runtime": runtime,
        "paths": {"output_dir": str(output_dir),
                  "ledger": str(ledger_path),
                  "ledger_head": str(output_dir / "ledger_head.json"),
                  "runtime_stats": str(output_dir
                                       / "runtime_stats.json")},
    }


def _cli() -> int:
    import sys
    result = run_pipeline({"double_run": "--no-double-run"
                           not in sys.argv})
    print(json.dumps({
        "chain_sha256": result["chain_sha256"],
        "grading": result["grading"],
        "stage_digests": result["stage_digests"],
        "runtime": result["runtime"]},
        ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
