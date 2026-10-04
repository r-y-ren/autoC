"""make_layer_s_v2_block（R11 L1）：从 L1 块源生成 v2 块——恰一处函数体替换+AST diff 校验。"""

import ast
import hashlib
from pathlib import Path

_TARGET_FUNCTION = "_cxs_seed_surplus"
_LAST_TOP_DEF_EXPECTED = "_cxs_agent"

# 净需求覆盖版 _cxs_seed_surplus（R11 替换文本）：与 L1 版同签名/同 docstring 风格，
# 唯一口径变更=供给删去磁带未来购买路（26 局实证：磁带未来购买计入供给=回买
# 92% 侵蚀的根因，分析 10/11）。作为完整函数源嵌入（def 行起、末行换行止），
# 拼接时前缀/后缀从 L1 源逐字节继承，保证与 L1 的 diff 恰为一处函数体。
V2_SURPLUS_SRC = '''def _cxs_seed_surplus(crop, observation, kept_orders, plan_view, current_plants: int | None = None):
    """零误杀核心（v2 净需求覆盖，R11）：surplus=max(0,库存−当前步PLANT消耗)+保留单−可完成需求；磁带未来购买不计；解析失败→None。

    v2 相对 L1 的唯一口径变更：磁带未来 BUY_SEED 一律不再计入供给（R11 净需求
    覆盖）。删去磁带未来供给后本函数更保守（供给变小→删得更少）——这正确：
    磁带单由各自回合同判定守护，回买单（本回合订单）在同口径下被正确评估。
    demand = _cxs_completable_plant_demand(crop, observation, plan_view)，
    其 None → 本函数 None；v2 需求只调一次 plan_view（供给不再读磁带，无 L1
    的二次调用一致性交叉核对，也不必再读 observation["step"]）。供给两路相加
    （held_effective = max(0, 库存 − current_plants)，超扣钳 0 不为负）：
      1) 有效库存种子 observation["private"]["seeds"].get(crop, 0) 减当前步
         PLANT 消耗。字段路径取基座同款（orderbook_derivative/main.py：
         tomato 门 L6775 obs['private']['seeds'].get('TOMATO', 0)；CARROT2
         层 L4607/L4693 int(priv["seeds"].get("CARROT", 0))）；基座的 int()
         宽 coercion 收紧为严格数型（bool/字符串数字/半值 float 均视为类型
         异常）；字段缺失/类型异常 → None。current_plants：None=未知 →
         直接返回 None（引擎结算序同 step 单位动作 PLANT 消耗 private.seeds
         先于市场买单入账，当前步种植消耗不属于未来供给，消耗未知即供给
         不确定）；0=确证当前步无该品种植；非负整数校验（bool/str/半值
         float/负数 → None）。
      2) kept_orders 中 ["BUY_SEED", crop, qty] 之和（本回合保留单），订单
         匹配对齐基座式 len(o)>=3 and o[:2]==["BUY_SEED", crop]（main.py
         L4680/L4694）。kept_orders 非 list/tuple，或任一订单非 list/tuple、
         长度<3（无论操作类型——无法确认该单不是本品项）、本品项 BUY_SEED
         的 qty 非整数（bool/str/None/半值 float 同拒）→ None：解析不完整=
         不确定=零截断。
    返回 int=允许删除的本品项 BUY_SEED 数量 = min(max(0, 供给−需求),
    kept_orders 本品项购买量)（删除对象只可能是本回合订单）；None=不确定=
    上游对该品项零截断；0=确证无剩余（与 None 异义）。其余任何读取/解析
    异常 → None（零误杀：一切不确定→None→上游零截断）。
    """
    if current_plants is None:
        return None  # 当前步 PLANT 消耗未知=供给不确定=零误杀纪律→None

    def _strict_count(value):
        # 数量解析纪律（同 _cxs_completable_plant_demand）：int（非 bool）原样，
        # 整值 float 折 int；bool/str/None/半值 float 抛异常 → 外层定向 None。
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("count not numeric")
        if isinstance(value, float):
            if not value.is_integer():
                raise TypeError("count fractional")
            value = int(value)
        return value

    try:
        # 当前步 PLANT 消耗：非负整数（bool/str/半值 float → _strict_count 抛；
        # 负数 → 显式 None）
        plants_now = _strict_count(current_plants)
        if plants_now < 0:
            return None

        # 需求（v2 唯一一次 plan_view 消费点：可完成 PLANT 种子需求）
        demand = _cxs_completable_plant_demand(crop, observation, plan_view)
        if demand is None:
            return None

        # 库存（observation 非 dict / 字段缺失 / 类型异常 → None）
        if not isinstance(observation, dict):
            return None
        priv = observation.get("private")
        if not isinstance(priv, dict):
            return None
        seeds = priv.get("seeds")
        if not isinstance(seeds, dict):
            return None
        held = _strict_count(seeds.get(crop, 0))

        # 保留单：畸形订单一律 None（宁可保守：无法解析的订单集合不能作截断依据）
        if not isinstance(kept_orders, (list, tuple)):
            return None
        kept_buy = 0
        for order in kept_orders:
            if not isinstance(order, (list, tuple)) or len(order) < 3:
                return None
            if order[0] == "BUY_SEED" and order[1] == crop:
                kept_buy += _strict_count(order[2])

        held_effective = held - plants_now  # 当前步 PLANT 先于买单入账：扣减
        if held_effective < 0:
            held_effective = 0  # 超扣钳 0（plants>held 不得产生负供给）
        supply = held_effective + kept_buy  # v2 净口径：磁带未来购买一律不计
        allow = supply - demand
        if allow < 0:
            allow = 0
        if allow > kept_buy:
            allow = kept_buy
        return allow
    except Exception:
        return None
'''


def _top_defs(tree):
    return [n for n in tree.body if isinstance(n, ast.FunctionDef)]


def _find_target(tree, name, label):
    matches = [n for n in _top_defs(tree) if n.name == name]
    if len(matches) != 1:
        raise ValueError(f"{label}: expected exactly one top-level def {name!r}, found {len(matches)}")
    return matches[0]


def _line_span(text, lineno, end_lineno):
    """1-based 闭行区间的逐字节源片段（含行尾换行）。"""
    return "".join(text.splitlines(keepends=True)[lineno - 1:end_lineno])


def _line_offset(text, lineno):
    """行号（1-based）行首的字节偏移；行号超界=文末。"""
    lines = text.splitlines(keepends=True)
    if lineno > len(lines):
        return len(text)
    return sum(len(line) for line in lines[:lineno - 1])


def _audit_diff_single_function(l1_tree, l1_text, v2_tree, v2_text, l1_fn, v2_fn):
    """diff 恰为一处函数体：目标函数同位；其余顶层语句（其余函数+常数+docstring）逐字节相同。"""
    if l1_tree.body.index(l1_fn) != v2_tree.body.index(v2_fn):
        raise ValueError(f"diff audit: {_TARGET_FUNCTION} position drifted")
    l1_rest = [n for n in l1_tree.body if n is not l1_fn]
    v2_rest = [n for n in v2_tree.body if n is not v2_fn]
    if len(l1_rest) != len(v2_rest):
        raise ValueError("diff audit: top-level statement count changed")
    for a, b in zip(l1_rest, v2_rest):
        if type(a) is not type(b):
            raise ValueError(f"diff audit: statement type drift at L1 line {a.lineno}")
        if _line_span(l1_text, a.lineno, a.end_lineno) != _line_span(v2_text, b.lineno, b.end_lineno):
            raise ValueError(f"diff audit: byte drift outside {_TARGET_FUNCTION} at L1 line {a.lineno}")


def make(l1_block_path=None, out_path=None) -> dict:
    """生成 layer_s_block_v2.py：替换 _cxs_seed_surplus 为净需求覆盖版；校验 diff 恰一函数体。"""
    here = Path(__file__).resolve().parent
    l1_path = (Path(l1_block_path) if l1_block_path is not None
               else here.parent / "orderbook_l1_derivative" / "layer_s_block.py")
    out = Path(out_path) if out_path is not None else here / "layer_s_block_v2.py"

    # 替换文本结构守卫：嵌入源自身恰一条顶层 def 且名为目标函数（防拼接面漂移）。
    embedded = ast.parse(V2_SURPLUS_SRC)
    embedded_defs = _top_defs(embedded)
    if len(embedded.body) != 1 or len(embedded_defs) != 1 or embedded_defs[0].name != _TARGET_FUNCTION:
        raise ValueError(f"V2_SURPLUS_SRC: expected exactly one top-level def {_TARGET_FUNCTION!r}")

    # ① AST 定位 L1 目标函数起止行（1-based 闭区间）→ 前缀/后缀字节切分。
    l1_text = l1_path.read_text(encoding="utf-8")
    l1_tree = ast.parse(l1_text)
    l1_fn = _find_target(l1_tree, _TARGET_FUNCTION, "L1 block")
    prefix = l1_text[:_line_offset(l1_text, l1_fn.lineno)]
    suffix = l1_text[_line_offset(l1_text, l1_fn.end_lineno + 1):]

    # ② 拼接：区间外逐字节继承，目标函数体替换为净需求覆盖版。
    v2_text = prefix + V2_SURPLUS_SRC + suffix

    # ③ 校验：v2 源 ast.parse 通过（失败即抛）；diff 恰为一处函数体；末顶层 def 仍 _cxs_agent。
    v2_tree = ast.parse(v2_text)
    v2_fn = _find_target(v2_tree, _TARGET_FUNCTION, "v2 block")
    if _line_span(v2_text, v2_fn.lineno, v2_fn.end_lineno) != V2_SURPLUS_SRC:
        raise ValueError("v2 block: spliced segment drifted from V2_SURPLUS_SRC")
    _audit_diff_single_function(l1_tree, l1_text, v2_tree, v2_text, l1_fn, v2_fn)
    top_defs = _top_defs(v2_tree)
    if not top_defs or top_defs[-1].name != _LAST_TOP_DEF_EXPECTED:
        raise ValueError(f"v2 block: last top-level def is not {_LAST_TOP_DEF_EXPECTED!r}")

    # ④ 写出（幂等覆盖写）→ sha 身份 + diff 审计。
    out.write_text(v2_text, encoding="utf-8")
    return {
        "v2_path": str(out),
        "v2_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        "diff_audit": {
            "only_function": _TARGET_FUNCTION,
            "l1_lines": [l1_fn.lineno, l1_fn.end_lineno],
            "v2_lines": [v2_fn.lineno, v2_fn.end_lineno],
        },
    }
