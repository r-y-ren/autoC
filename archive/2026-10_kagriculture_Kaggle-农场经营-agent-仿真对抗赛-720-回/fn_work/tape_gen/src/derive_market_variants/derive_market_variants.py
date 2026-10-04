"""derive_market_variants（L0，R3）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

顶层编排：骨干路由 + 文档化市场单编辑算子集 → 变体集 + 差分账本。
骨干 farmer+hands 流逐字节保留（assert_farmer_stream_identity 逐变体
断言；失配变体剔除并留痕——"算子异常跳过留痕"）。

变体计划（确定性、数量受控：每骨干 ≤ MAX_VARIANTS=8，稀疏纪律——
v48 先例 farm_fast=±1-3 天卖单时移、消融树上最稀疏的枝是赢家配置）：

| 变体名 | 算子 | 参数 |
|---|---|---|
| shift_dp1 / dm1 / dp2 / dm2 | shift_sells_by_days | days=±1/±2 |
| scale_r0p75 / r1p25 | scale_sell_quantities | ratio=0.75/1.25 |
| cap_c120 / c240 | daily_sell_cap | cap=120/240 |

产物（fn_work/tape_gen/library/）：
* ``market_variants.json``——{变体名: [719 步]}，与 routes.json 同基
  格式（v48 载入路径兼容形态，每变体即一条完整路由磁带）；
* ``variants_ledger.json``——差分账本（逐变体算子/参数/守恒账/恒等
  断言/市场差分摘要/哈希）。

错误：算子异常（fail-closed 输入级）抛出；变体级失配剔除留痕不熔断。
确定性：同输入同输出（全排序、规范 JSON、无墙钟）。
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from derive_market_variants.apply_market_edit_operators import \
    apply_market_edit_operators
from derive_market_variants.assert_farmer_stream_identity import \
    assert_farmer_stream_identity

_CAMPAIGN_ROOT = Path(__file__).resolve().parents[4]
_TAPE_GEN_ROOT = _CAMPAIGN_ROOT / "fn_work" / "tape_gen"
DEFAULT_LIBRARY_DIR = _TAPE_GEN_ROOT / "library"

#: 每骨干变体上限（数量受控，稀疏纪律）。
MAX_VARIANTS = 8

#: 默认变体计划（顺序即输出序；name 确定性命名）。
DEFAULT_VARIANT_PLAN = (
    {"name": "shift_dp1", "operator": "shift_sells_by_days",
     "params": {"days": 1}},
    {"name": "shift_dm1", "operator": "shift_sells_by_days",
     "params": {"days": -1}},
    {"name": "shift_dp2", "operator": "shift_sells_by_days",
     "params": {"days": 2}},
    {"name": "shift_dm2", "operator": "shift_sells_by_days",
     "params": {"days": -2}},
    {"name": "scale_r0p75", "operator": "scale_sell_quantities",
     "params": {"ratio": 0.75}},
    {"name": "scale_r1p25", "operator": "scale_sell_quantities",
     "params": {"ratio": 1.25}},
    {"name": "cap_c120", "operator": "daily_sell_cap",
     "params": {"cap": 120}},
    {"name": "cap_c240", "operator": "daily_sell_cap",
     "params": {"cap": 240}},
)


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _dump(route) -> str:
    return json.dumps(route, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def derive_market_variants(payload=None):
    """意图级签名；真值在责任文档。

    payload 可覆盖：backbone_route（缺省读 library/routes.json 的
    default 路由）/ library_dir / output_dir / plan / max_variants /
    band。返回 {variants, rejected, ledger, paths, backbone_sha256}。
    """
    payload = dict(payload or {})
    library_dir = Path(payload.get("library_dir") or DEFAULT_LIBRARY_DIR)
    output_dir = Path(payload.get("output_dir") or library_dir)

    backbone = payload.get("backbone_route") \
        if "backbone_route" in payload else None
    if backbone is None:
        routes_path = library_dir / "routes.json"
        if not routes_path.is_file():
            raise ValueError(f"backbone route missing (fail-closed): pass "
                             f"backbone_route or ensure {routes_path}")
        backbone = json.loads(routes_path.read_text(
            encoding="utf-8"))["default"]
    if not isinstance(backbone, list) or not backbone:
        raise ValueError("backbone route must be a non-empty step list "
                         "(fail-closed)")

    plan = payload.get("plan") or DEFAULT_VARIANT_PLAN
    max_variants = int(payload.get("max_variants") or MAX_VARIANTS)
    band = payload.get("band")

    variants = {}
    ledger = []
    rejected = []
    for spec in plan[:max_variants]:
        name = spec["name"]
        entry = {"name": name, "operator": spec["operator"],
                 "params": spec["params"]}
        try:
            applied = apply_market_edit_operators({
                "route": backbone, "operator": spec["operator"],
                "params": spec["params"], "band": band})
        except ValueError as exc:
            entry["status"] = "rejected_operator_error"
            entry["reason"] = str(exc)
            rejected.append(entry)
            continue

        identity = assert_farmer_stream_identity({
            "route": applied["route"], "backbone": backbone})
        entry["status"] = "ok" if identity["ok"] else \
            "rejected_identity_violation"
        entry["farmer_identity"] = {
            "ok": identity["ok"],
            "checked_steps": identity["checked_steps"],
            "first_divergence": identity["first_divergence"],
            "farmer_sha256": identity["farmer_sha256"],
        }
        entry["changes"] = applied["changes"]
        entry["market_changed_steps"] = identity.get("market_changed_steps")
        entry["route_sha256"] = _sha256_text(_dump(applied["route"]))
        if not identity["ok"]:
            rejected.append(entry)
            continue
        variants[name] = applied["route"]
        ledger.append(entry)

    variants_text = json.dumps(variants, ensure_ascii=False, sort_keys=True,
                               separators=(",", ":"))
    doc = {
        "backbone_sha256": _sha256_text(_dump(backbone)),
        "max_variants": max_variants,
        "plan": [dict(spec) for spec in plan[:max_variants]],
        "n_variants": len(variants),
        "n_rejected": len(rejected),
        "variants_sha256": _sha256_text(variants_text),
        "ledger": ledger,
        "rejected": rejected,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    variants_path = output_dir / "market_variants.json"
    variants_path.write_text(variants_text + "\n", encoding="utf-8")
    ledger_path = output_dir / "variants_ledger.json"
    ledger_text = json.dumps(doc, ensure_ascii=False, indent=2,
                             sort_keys=True)
    ledger_path.write_text(ledger_text + "\n", encoding="utf-8")

    result = dict(doc)
    result["variants"] = variants
    result["paths"] = {"variants": str(variants_path),
                       "ledger": str(ledger_path)}
    return result
