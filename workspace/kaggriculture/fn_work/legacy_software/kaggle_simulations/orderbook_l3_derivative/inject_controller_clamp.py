"""inject_controller_clamp（R13 L1）：基座中部受控手术——CARROT2 §3b 目标项钳制（fine/coarse）。

手术面（基座 fn_work/legacy_software/kaggle_simulations/orderbook_derivative/main.py，只读；
sha a16e0e9b…，与 L1 构建链同源三方核对）：
  ① AST 定位 CARROT2 层函数（模块级 def agent 且体内 action=_CA_PARENT(...)，实读唯一，
     基座 4589-4719）与 §3b 买入段 q 赋值（Assign q = _CA_BUFFER - have - buying，实读
     唯一，基座 4695 单行）；
  ② 目标项 `_CA_BUFFER`（Name 子节点，col 16-26）文本段替换——
     fine:   min(_CA_BUFFER, _ca_clamped_target(day, seat, step))
             【需求相对激活（2026-09-24 修订一轮）】目标项**无条件**走 min()：
             需求+2≥8 时 min 自然=原目标=零足迹，需求走低的天（含 day24-26
             收敛期）即按需求收敛囤积（S6 实证 day27 硬窗激活只停新买、
             减不掉已囤 8 颗）；None→_CA_BUFFER 回退收在 helper 内，表达式
             侧不写 try；day<24 也调 _ca_future_plant_demand（磁带扫描），
             实测最坏 0.5ms/步（day6 后缀全长扫描），远低于 10ms 预算——
             不加廉价门。
     coarse: (2 if day >= 27 else _CA_BUFFER)
             【R13-b 降级预案】day≥27 硬窗不变（day=step//24，step>=648；
             responsibility.md【R13 增补】措辞；只改 fine 不动 coarse）；
  ③ CLAMP_HELPER_SRC（_ca_future_plant_demand + 薄包装 _ca_clamped_target）插入层函数
     定义之前（`del agent` 与 `def agent(...)` 之间的模块级，能访问 _ca_tape/_CA_BUFFER/
     _CA_TO——均定义于插入点之前）；day/seat/step 经表达式显式传参（responsibility.md
     `_ca_future_plant_demand(<上下文>)` 占位的落地形态：仅 day 单参取不到"≥当前步"后缀
     与 seat 上下文）；
  ④ fail-safe：需求读不到/任何异常 → _CA_BUFFER（回退原目标=q 原公式行为，requirements
     R13 铁律）；helper 永不抛（异常不外溢到层函数 try 块）。

校验（任一红即抛，不落盘坏产物）：AST 可解析 / difflib 变更集恰{一 def 块插入+一 Assign
值替换}（前缀-中缀-后缀逐字节恒等证明）/ 替换行 AST 形态（IfExp 分支）/ 五区零改动
（diff 全落 CARROT2 区段[4469,4734] + 区域内外代表性函数源段恒等；授权行区间回退制，
见 _ZONE_FUNC_NAMES 注）/ 隔离 ns 真 exec 后末 callable 仍 _cxd_agent（此时尚未追加
layer S）/ py_compile。产物=本目录 main_clamped.py（中间产物，供 build_l13_candidate
在其上追加 layer S 尾块）。"""

import ast
import difflib
import hashlib
import os
import py_compile
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_BASE_MAIN = _HERE.parent / "orderbook_derivative" / "main.py"  # 基座原件（只读，零改动）

# round-30 基座身份链（与 L1 build_layer_s_candidate._BASE_MAIN_SHA256 同源；漂移即抛）
_BASE_MAIN_SHA256 = "a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab"

# 手术授权区段（基座行号 1-based 含端）：CARROT2 层头 4469 至下一层（ORDERPRI2）头前 4734。
# 五区零改动的授权回退口径：非本区段逐字节恒等（任务契约：清单源缺位时的行区间断言）。
_CARROT2_REGION = (4469, 4734)

# 判重 sentinel：本注射器产物必含的 helper def 行
_HELPER_SENTINEL = "def _ca_clamped_target(day, seat, step):"

# 两模式目标项替换文本（fine=需求相对激活·无条件 min；coarse=R13-b 降级预案 day≥27
# 硬窗不变；表达式侧不写 try——None/异常回退收在 helper 侧）。
# R13 第二次调参变体（2026-09-24）：tuned/lean 与 fine 同一表达式（需求相对 min），
# 差异仅在 helper 源的需求口径——小麦槽计数乘 _CA_WHEAT_SLOT_WEIGHT 权重常数
# （tuned=0.5 半口径；lean=0.0 纯胡萝卜口径），常数行由 mode 参数派生注入；
# fine/coarse 保持 CLAMP_HELPER_SRC 逐字节零漂移（发射态产物身份不动）。
_MODE_EXPRS = {
    "fine": "min(_CA_BUFFER, _ca_clamped_target(day, seat, step))",
    "coarse": "(2 if day >= 27 else _CA_BUFFER)",
    "tuned": "min(_CA_BUFFER, _ca_clamped_target(day, seat, step))",
    "lean": "min(_CA_BUFFER, _ca_clamped_target(day, seat, step))",
}

# 变体需求口径：小麦槽计数权重（None=CLAMP_HELPER_SRC 原口径逐字节不变）。
_WHEAT_SLOT_WEIGHTS = {"fine": None, "coarse": None, "tuned": 0.5, "lean": 0.0}

# 变更集审计的激活语义登记（manifest provenance 消费）
_ACTIVATION_WINDOW = {
    "fine": ("unconditional demand-relative（min 恒走；需求+2>=8 时 min=原目标="
             "零足迹，day24-26 即按需求收敛囤积）"),
    "coarse": "day >= 27 (== step >= 648)",
    "tuned": ("unconditional demand-relative ×wheat-slot weight 0.5（R13 第二次"
              "调参变体：需求=胡萝卜全计+day≤28 小麦槽×0.5，int 截断；clamp 口径"
              "更早咬合，starve 零容忍门为硬绊网）"),
    "lean": ("unconditional demand-relative ×wheat-slot weight 0.0（R13 第二次"
             "调参变体：纯胡萝卜口径，小麦槽不计入需求；最激进早咬合，starve"
             " 零容忍门为硬绊网）"),
}

# 五区零改动断言的函数名清单。来源说明（audit 同款登记）：授权首选=../orderbook_l1_derivative/
# 尾块 docstring 或逆向 digest 的函数名清单——实查两者均无函数名清单，故按授权回退=行区间
# [非 4469-4734] 恒等断言为主；本清单为按基座结构另行取的代表性锚（belt）：
#   磁带/磁带访问域（区段内，注射点邻域）：_ca_tape（route2 后缀访问仿真）、_ca_visits；
#   终局清仓域（区段外尾部）：final_price_guard、_cxtb_agent；
#   槽位重排/反克隆域（区段外尾部，layer D）：_cxd_candidates、_cxd_reorder、_cxd_agent；
#   路由域（区段外 chassis）：Chassis（类）。
_ZONE_FUNC_NAMES = ("_ca_tape", "_ca_visits", "final_price_guard", "_cxtb_agent",
                    "_cxd_candidates", "_cxd_reorder", "_cxd_agent", "Chassis")

# CLAMP_HELPER_SRC：钳制需求 helper 源文本（独立 exec 可测——伪上下文注入 _ca_tape/
# _CA_BUFFER/_CA_TO 即可单测；注入态插到 CARROT2 层函数定义之前的模块级，三者均在其前定义）。
CLAMP_HELPER_SRC = '''\
def _ca_future_plant_demand(seat, step):
    """R13 fine 钳制的未来种植需求估计（保守上界，永不抛）。

    route2 磁带后缀（t>=step 经基座 _ca_tape 读；t>=648 恒 2 号路——基座同款路由换算）：
    PLANT,CARROT 全计数（磁带自己的胡萝卜种植都要在 day<=27 买入段内备种，不限天）＋
    day<=_CA_TO(28) 的 PLANT,WHEAT 槽保守全计数（swap 窗内小麦槽都可能被 CARROT2 §2 换种，
    不筛 pays_now/余种，宁多勿饿）。后缀无任何可读步条目（磁带读不到）或任何异常 -> None，
    由 _ca_clamped_target 回退原目标。磁带静态 BUY_SEED 单不参与（R13 授权面只钳目标项）。"""
    try:
        total, seen = 0, False
        for t in range(int(step), 720):
            act = _ca_tape(seat, t)
            if not isinstance(act, dict) or not act:
                continue
            seen = True
            for c in [act.get("farmer") or ["PASS"]] + list(act.get("hands") or []):
                if isinstance(c, (list, tuple)) and len(c) >= 2 and c[0] == "PLANT":
                    if c[1] == "CARROT":
                        total += 1
                    elif c[1] == "WHEAT" and t // 24 <= _CA_TO:
                        total += 1
        return total if seen else None
    except Exception:
        return None


def _ca_clamped_target(day, seat, step):
    """R13 fine 钳制目标项（无条件替换 _CA_BUFFER 的值，永不抛）。

    需求 None（读不到/异常）-> _CA_BUFFER（回退原目标=q 原公式行为，fail-safe）；
    否则 min(8, 需求+2)（+2 安全边：day28 仍可 swap 的小麦槽保消耗不饿种，
    分析12 耦合清单②）。**需求相对激活（2026-09-24 修订一轮）**：任何 day 都按
    min 取值——需求+2>=8 时 min 自然等于原目标 _CA_BUFFER（零足迹），需求走低的
    天（含 day24-26 收敛期）即早于旧 day>=27 硬窗收敛囤积（旧防御分支已删，
    无条件调用）。day/seat/step 为行内作用域实参（responsibility.md
    `_ca_future_plant_demand(<上下文>)` 占位落地；day 现仅保持注入位契约签名，
    激活不再以 day 键控）。"""
    try:
        demand = _ca_future_plant_demand(seat, step)
        if demand is None:
            return _CA_BUFFER
        return min(8, int(demand) + 2)
    except Exception:
        return _CA_BUFFER
'''

# ---------------------------------------------------------------------------
# R13 第二次调参变体（tuned/lean）：加权 helper 源派生（fine/coarse 零漂移）
# ---------------------------------------------------------------------------
# 权重常数行（module 级，插在 helper 首 def 之前；两空行随 top-level 约定）。
_WHEAT_CONST_PREFIX = "_CA_WHEAT_SLOT_WEIGHT = "
_DEF_ANCHOR = "def _ca_future_plant_demand(seat, step):"
# CLAMP_HELPER_SRC 内小麦槽计数分支（elif 行+计数行整体锚定——CARROT 分支的
# 同缩进 total += 1 不在此形态内，锚唯一）。
_WHEAT_BRANCH_OLD = (
    '                    elif c[1] == "WHEAT" and t // 24 <= _CA_TO:\n'
    '                        total += 1\n'
)
_WHEAT_BRANCH_NEW = (
    '                    elif c[1] == "WHEAT" and t // 24 <= _CA_TO:\n'
    '                        total += _CA_WHEAT_SLOT_WEIGHT\n'
)
# helper docstring 的口径行（加权派生时改写，保产物内文档与行为一致）。
_DOC_LINE_OLD = ("    day<=_CA_TO(28) 的 PLANT,WHEAT 槽保守全计数"
                 "（swap 窗内小麦槽都可能被 CARROT2 §2 换种，\n")


def clamp_helper_src(mode):
    """按 mode 返回钳制 helper 源文本。

    fine/coarse：CLAMP_HELPER_SRC 逐字节返回（发射态口径零漂移）。
    tuned/lean：三处受控派生——①权重常数行 `_CA_WHEAT_SLOT_WEIGHT = 0.5|0.0`
    插在首 def 之前（module 级常数，mode 参数注入常数行）；②小麦槽计数分支
    `total += 1` → `total += _CA_WHEAT_SLOT_WEIGHT`（胡萝卜分支不动）；③helper
    docstring 口径行改写为加权口径。任一锚不唯一即抛（fail-closed，防
    CLAMP_HELPER_SRC 漂移后静默派生错件）。"""
    weight = _WHEAT_SLOT_WEIGHTS[mode]
    if weight is None:
        return CLAMP_HELPER_SRC
    for anchor, count in ((_DEF_ANCHOR, CLAMP_HELPER_SRC.count(_DEF_ANCHOR)),
                          (_WHEAT_BRANCH_OLD, CLAMP_HELPER_SRC.count(_WHEAT_BRANCH_OLD)),
                          (_DOC_LINE_OLD, CLAMP_HELPER_SRC.count(_DOC_LINE_OLD))):
        if count != 1:
            raise ValueError(
                f"加权 helper 派生锚不唯一（{anchor[:40]!r}… 命中 {count} 次，"
                "CLAMP_HELPER_SRC 漂移，fail-closed）")
    weight_repr = repr(weight)  # '0.5' / '0.0'
    const_block = (f"{_WHEAT_CONST_PREFIX}{weight_repr}"
                   f"  # R13 第二次调参变体（mode={mode}）：小麦槽计数权重\n\n\n")
    doc_line_new = (f"    day<=_CA_TO(28) 的 PLANT,WHEAT 槽按 "
                    f"_CA_WHEAT_SLOT_WEIGHT={weight_repr} 加权计数"
                    "（swap 窗内小麦槽都可能被 CARROT2 §2 换种，\n")
    out = CLAMP_HELPER_SRC.replace(_DEF_ANCHOR, const_block + _DEF_ANCHOR, 1)
    out = out.replace(_WHEAT_BRANCH_OLD, _WHEAT_BRANCH_NEW, 1)
    out = out.replace(_DOC_LINE_OLD, doc_line_new, 1)
    # 派生输出面结构自检：常数行恰一、旧全计分支清零、新加权分支恰一、
    # 原 docstring 口径行清零、fine 原文不含权重名（零漂移证明）。
    if (out.count(_WHEAT_CONST_PREFIX + weight_repr) != 1
            or _WHEAT_BRANCH_OLD in out
            or out.count(_WHEAT_BRANCH_NEW) != 1
            or _DOC_LINE_OLD in out):
        raise RuntimeError("加权 helper 派生输出面结构异常（fail-closed）")
    if "_CA_WHEAT_SLOT_WEIGHT" in CLAMP_HELPER_SRC:
        raise RuntimeError("CLAMP_HELPER_SRC 已含权重名（发射态口径漂移，fail-closed）")
    return out


def _leftmost_name(node):
    """BinOp 链最左操作数（须为 Name，否则 None）。"""
    while isinstance(node, ast.BinOp):
        node = node.left
    return node if isinstance(node, ast.Name) else None


def _find_carrot2_layer(tree):
    """CARROT2 层函数=模块级 def agent 且体内首段有 action=_CA_PARENT(...) 赋值；恰一。"""
    hits = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "agent":
            for stmt in node.body:
                if (isinstance(stmt, ast.Assign) and len(stmt.targets) == 1
                        and isinstance(stmt.targets[0], ast.Name) and stmt.targets[0].id == "action"
                        and isinstance(stmt.value, ast.Call) and isinstance(stmt.value.func, ast.Name)
                        and stmt.value.func.id == "_CA_PARENT"):
                    hits.append(node)
                    break
    if len(hits) != 1:
        raise ValueError(f"CARROT2 层函数定位失败：期望恰 1 个（action=_CA_PARENT），实得 {len(hits)}")
    return hits[0]


def _find_q_assign(layer):
    """§3b 买入段 q 赋值：Assign q = BinOp(-, BinOp(-, _CA_BUFFER, have), buying)；恰一且单行。"""
    hits = []
    for node in ast.walk(layer):
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "q"
                and isinstance(node.value, ast.BinOp) and isinstance(node.value.op, ast.Sub)):
            value = node.value
            names = {n.id for n in ast.walk(value) if isinstance(n, ast.Name)}
            leftmost = _leftmost_name(value)
            if (leftmost is not None and leftmost.id == "_CA_BUFFER"
                    and names == {"_CA_BUFFER", "have", "buying"}):
                hits.append((node, leftmost))
    if len(hits) != 1:
        raise ValueError(f"q 赋值定位失败：期望层内恰 1 个（_CA_BUFFER-have-buying 形态），实得 {len(hits)}")
    node, leftmost = hits[0]
    if node.end_lineno != node.lineno:
        raise ValueError(f"q 赋值须单行（实读 {node.lineno}-{node.end_lineno}），切片证明不成立")
    return node, leftmost


def _assert_assign_shape(tree, mode):
    """校验③：替换后 q 赋值 AST 形态（mode 分形；q = <目标项> - have - buying）。

    fine 族（fine/tuned/lean——2026-09-24 修订一轮·需求相对激活，tuned/lean 为
    R13 第二次调参变体，表达式同形仅 helper 需求口径加权）：目标项=Call
    min(_CA_BUFFER, _ca_clamped_target(day, seat, step))——BinOp(-, BinOp(-,
    Call, have), buying)，**无条件** min（无 IfExp 门控；helper 内 None→
    _CA_BUFFER 回退；需求+2≥8 时 min=原目标=零足迹）；coarse（R13-b 降级
    预案）：目标项=IfExp(day>=27, 2, Name _CA_BUFFER)——day≥27 硬窗不变
    （day<27 走原目标，行为恒等）。"""
    hits = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "q"):
            continue
        value = node.value
        if not (isinstance(value, ast.BinOp) and isinstance(value.op, ast.Sub)
                and isinstance(value.left, ast.BinOp) and isinstance(value.left.op, ast.Sub)
                and isinstance(value.left.right, ast.Name) and value.left.right.id == "have"
                and isinstance(value.right, ast.Name) and value.right.id == "buying"):
            continue
        target = value.left.left
        if mode in ("fine", "tuned", "lean"):
            if not (isinstance(target, ast.Call) and isinstance(target.func, ast.Name)
                    and target.func.id == "min" and len(target.args) == 2
                    and isinstance(target.args[0], ast.Name)
                    and target.args[0].id == "_CA_BUFFER"
                    and isinstance(target.args[1], ast.Call)
                    and isinstance(target.args[1].func, ast.Name)
                    and target.args[1].func.id == "_ca_clamped_target"
                    and [a.id for a in target.args[1].args if isinstance(a, ast.Name)] == ["day", "seat", "step"]):
                continue
        else:
            if not (isinstance(target, ast.IfExp)
                    and isinstance(target.test, ast.Compare)
                    and isinstance(target.test.left, ast.Name)
                    and target.test.left.id == "day" and len(target.test.ops) == 1
                    and isinstance(target.test.ops[0], ast.GtE) and len(target.test.comparators) == 1
                    and isinstance(target.test.comparators[0], ast.Constant)
                    and target.test.comparators[0].value == 27
                    and isinstance(target.body, ast.Constant) and target.body.value == 2
                    and isinstance(target.orelse, ast.Name) and target.orelse.id == "_CA_BUFFER"):
                continue
        hits.append((node, target))
    if len(hits) != 1:
        raise RuntimeError(f"校验③红：替换后 clamped q 赋值期望恰 1 处（{mode} 形态），实得 {len(hits)}")
    return True


def _zone_segments(tree, lines, names):
    """模块级 def/class 按名取源段文本（行切片，1-based 含端）。"""
    spans = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name in names:
            spans[node.name] = (node.lineno, node.end_lineno,
                                "".join(lines[node.lineno - 1:node.end_lineno]))
    return spans


def inject(base_main_path, mode="fine", out_path=None) -> dict:
    """行 4695 目标项替换+helper 插入；变更集恰{一 def 块+一表达式}；五区零改动断言。

    base_main_path：基座原件路径（只读；sha 须等于 round-30 身份链，漂移即抛）。
    mode：fine=需求钳制（无条件 min(8, 磁带需求+2)，None/异常回退 _CA_BUFFER——
    需求相对激活）；coarse=R13-b 粗粒度（day>=27 目标 2，硬窗不变）。
    out_path：产物路径（默认本目录 main_clamped.py 中间产物；测试可指定隔离路径）。
    """
    base_path = Path(base_main_path)
    if mode not in _MODE_EXPRS:
        raise ValueError(f"mode 须为 fine|coarse|tuned|lean，实得 {mode!r}")
    base_bytes = base_path.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != _BASE_MAIN_SHA256:
        raise ValueError(f"基座身份核对失败：sha {base_sha} != round-30 期望 {_BASE_MAIN_SHA256}（fail-closed）")
    out_path = Path(out_path) if out_path is not None else _HERE / "main_clamped.py"
    if out_path.resolve() == base_path.resolve():
        raise ValueError("refusing: out_path 指向基座原件（orderbook_derivative/main.py 只读）")
    if out_path.resolve().parent == base_path.resolve().parent:
        raise ValueError("refusing: out_path 落在基座目录（orderbook_derivative/ 只读）")
    if out_path.exists():
        current = out_path.read_bytes()
        if current != base_bytes and _HELPER_SENTINEL.encode("utf-8") not in current:
            raise ValueError("out_path 已存在且既非基座字节副本、亦非本注射器旧产物（sentinel 判定），拒绝覆盖")

    text = base_bytes.decode("utf-8")
    lines = text.splitlines(keepends=True)
    tree = ast.parse(text)  # 基座可解析（身份 sha 已核对，此处兼作前置断言）
    if _HELPER_SENTINEL in text:
        raise ValueError("基座已含钳制 helper（sentinel 命中），拒绝二次注入")

    layer = _find_carrot2_layer(tree)
    q_node, buffer_name = _find_q_assign(layer)
    expr = _MODE_EXPRS[mode]

    q_idx = q_node.lineno - 1                 # 0-based：4694（基座 4695 行）
    anchor = layer.lineno - 1                 # 0-based：4588（层 def 行前插入点）
    if not anchor < q_idx:
        raise RuntimeError("注入点须在 q 赋值之前（层函数定义之前）")
    if not (_CARROT2_REGION[0] <= anchor + 1 and q_node.lineno <= _CARROT2_REGION[1]):
        raise RuntimeError(f"手术点越出授权区段 {_CARROT2_REGION}（anchor={anchor + 1}, q={q_node.lineno}）")

    q_line = lines[q_idx]
    new_line = q_line[:buffer_name.col_offset] + expr + q_line[buffer_name.end_col_offset:]
    if new_line == q_line:
        raise RuntimeError("替换行为空操作（目标项未变化）")

    helper_src = clamp_helper_src(mode)
    helper_lines = helper_src.splitlines(keepends=True)
    first = helper_lines[0] if helper_lines else ""
    if not (first.startswith("def _ca_future_plant_demand(")
            or first.startswith(_WHEAT_CONST_PREFIX)):
        raise ValueError("helper 源形态异常（须以 _ca_future_plant_demand def 或"
                         " _CA_WHEAT_SLOT_WEIGHT 常数行开头）")
    if not helper_src.endswith("\n"):
        raise ValueError("helper 源须以换行收尾（拼接约定）")
    sep_lines = ["\n", "\n"]  # 与层函数定义之间恰两空行（基座 top-level def 分隔同款）
    inserted_block = helper_lines + sep_lines
    insert_end_base = anchor + len(inserted_block)  # 插入块末（基座行号基线）
    if not (insert_end_base <= _CARROT2_REGION[1]):
        raise RuntimeError("插入块越出授权区段")

    out_lines = (lines[:anchor] + inserted_block + lines[anchor:q_idx]
                 + [new_line] + lines[q_idx + 1:])
    out_text = "".join(out_lines)
    out_bytes = out_text.encode("utf-8")

    validations = []

    # ① AST 可解析（产物全文）
    try:
        out_tree = ast.parse(out_text)
    except SyntaxError as exc:
        raise RuntimeError(f"校验①红：ast.parse 未通过: {exc!r}") from exc
    validations.append({"check": "ast_parse", "ok": True, "detail": f"ast.parse passed ({len(out_bytes)} bytes)"})

    # ② 变更集恰{一 def 块插入+一 Assign 值替换}：difflib 独立审计（非构造自证）——
    #    opcode 序列须恰 [equal, insert, equal, replace, equal]，且插入块/替换行与手术文本
    #    逐字节相等，前缀-中缀-后缀与基座逐字节恒等。
    ops = list(difflib.SequenceMatcher(None, lines, out_lines, autojunk=False).get_opcodes())
    tags = [op[0] for op in ops]
    if tags != ["equal", "insert", "equal", "replace", "equal"] or len(ops) != 5:
        raise RuntimeError(f"校验②红：opcode 序列 {tags} != [equal, insert, equal, replace, equal]")
    _, pi1, pi2, pj1, pj2 = ops[1]
    _, ri1, ri2, rj1, rj2 = ops[3]
    if (pi1, pi2) != (anchor, anchor) or out_lines[pj1:pj2] != inserted_block:
        raise RuntimeError("校验②红：插入块位置/内容与手术文本不符")
    if (ri1, ri2) != (q_idx, q_idx + 1) or out_lines[rj1:rj2] != [new_line]:
        raise RuntimeError("校验②红：替换行位置/内容与手术文本不符")
    if "".join(lines[:pi1]) != "".join(out_lines[:pj1]) or "".join(lines[pi2:ri1]) != "".join(out_lines[pj2:rj1]) \
            or "".join(lines[ri2:]) != "".join(out_lines[rj2:]):
        raise RuntimeError("校验②红：前缀/中缀/后缀与基座非逐字节恒等")
    validations.append({
        "check": "change_set_splice", "ok": True,
        "detail": (f"insert {len(inserted_block)} 行 @基座行 {anchor + 1} 前（helper {len(helper_lines)} 行+分隔 2 行）；"
                   f"replace 1 行 @基座行 {q_node.lineno}；前缀 {pi1} 行/中缀 {ri1 - pi2} 行/后缀 {len(lines) - ri2} 行逐字节恒等"),
    })

    # ③ 替换行 AST 形态（mode 分形：fine 族=无条件 min Call；coarse=IfExp 硬窗）
    _assert_assign_shape(out_tree, mode)
    if mode in ("fine", "tuned", "lean"):
        weight_note = ("" if mode == "fine" else
                       f"；helper 需求口径小麦槽×_CA_WHEAT_SLOT_WEIGHT="
                       f"{_WHEAT_SLOT_WEIGHTS[mode]!r}（R13 第二次调参变体）")
        shape_detail = ("q = min(_CA_BUFFER, _ca_clamped_target(day, seat, step)) - have"
                        " - buying（目标项无条件 min·需求相对激活；None→_CA_BUFFER"
                        " 回退在 helper 内；需求+2≥8 时 min=原目标=零足迹)"
                        + weight_note)
    else:
        shape_detail = ("q = (2 if day >= 27 else _CA_BUFFER) - have - buying"
                        "（R13-b 降级预案硬窗；orelse=Name(_CA_BUFFER)）")
    validations.append({"check": "assign_shape", "ok": True, "detail": shape_detail})

    # ④ 五区零改动：所有 diff opcode 落授权区段内（行区间回退制为主）+ 区域内外代表性函数源段恒等
    for tag, i1, i2, j1, j2 in ops:
        if tag == "equal":
            continue
        base_pos = i1 + 1 if tag != "insert" else i1  # insert 的基座位=插入点前一行锚
        if not (_CARROT2_REGION[0] - (1 if tag == "insert" else 0) <= base_pos and base_pos <= _CARROT2_REGION[1]):
            raise RuntimeError(f"校验④红：diff 变更越出授权区段 {_CARROT2_REGION}（{tag}@基座行 {base_pos}）")
    base_zones = _zone_segments(tree, lines, _ZONE_FUNC_NAMES)
    out_zones = _zone_segments(out_tree, out_lines, _ZONE_FUNC_NAMES)
    zone_report = {}
    for name in _ZONE_FUNC_NAMES:
        if name not in base_zones or name not in out_zones:
            raise RuntimeError(f"校验④红：五区锚函数 {name} 在基座/产物中定位失败")
        if base_zones[name][2] != out_zones[name][2]:
            raise RuntimeError(f"校验④红：五区锚函数 {name} 源段非恒等")
        zone_report[name] = {"base_span": list(base_zones[name][:2]), "identical": True}
    validations.append({
        "check": "five_zones_zero_change", "ok": True,
        "detail": (f"diff 全部落授权区段 {list(_CARROT2_REGION)}（授权行区间回退制：清单源=实查无 L1 尾块"
                   f"docstring 函数清单/逆向 digest，按任务契约回退行区间断言）；另 {len(_ZONE_FUNC_NAMES)} 个"
                   "代表性区锚函数（磁带访问/终局清仓/槽位重排/路由 chassis）源段逐字节恒等"),
    })

    # ⑤ 隔离 ns 真 exec：末 callable 仍 _cxd_agent（此时尚未追加 layer S）；helper 已在装载面
    ns: dict = {}
    t0 = time.perf_counter()
    try:
        exec(compile(out_bytes, str(out_path), "exec"), ns)
    except Exception as exc:
        raise RuntimeError(f"校验⑤红：产物源码 exec 失败: {exc!r}") from exc
    exec_seconds = time.perf_counter() - t0
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != "_cxd_agent":
        last = loaded[-1].__name__ if loaded else "<none>"
        raise RuntimeError(f"校验⑤红：装载后末 callable={last!r}，应为 '_cxd_agent'（layer S 未追加态）")
    for helper_name in ("_ca_future_plant_demand", "_ca_clamped_target"):
        if not callable(ns.get(helper_name)):
            raise RuntimeError(f"校验⑤红：装载面缺 helper {helper_name}")
    validations.append({"check": "last_callable_exec", "ok": True,
                        "detail": f"exec {exec_seconds:.2f}s；globals 末 callable=_cxd_agent；两 helper 已装载"})

    # 全部校验绿后才落盘；⑥ py_compile 落盘件并回读 sha
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(out_bytes)
    cfile = out_path.parent / f".inject_controller_clamp.{os.getpid()}.pyc"
    try:
        py_compile.compile(str(out_path), cfile=str(cfile), doraise=True)
    except Exception as exc:
        raise RuntimeError(f"校验⑥红：py_compile 未通过: {exc!r}") from exc
    finally:
        cfile.unlink(missing_ok=True)
    written = out_path.read_bytes()
    injected_sha = hashlib.sha256(written).hexdigest()
    if written != out_bytes:
        raise RuntimeError("校验⑥红：落盘回读与内存产物非逐字节一致")
    if hashlib.sha256(base_path.read_bytes()).hexdigest() != _BASE_MAIN_SHA256:
        raise RuntimeError("校验⑥红：基座原件内容发生变化（须零改动）")
    validations.append({"check": "py_compile_and_write", "ok": True,
                        "detail": f"py_compile passed；落盘 {out_path}（回读逐字节一致）"})

    shift = len(inserted_block)
    return {
        "injected_sha": injected_sha,
        "change_set": {
            "mode": mode,
            "replaced_line_span": [q_node.lineno, q_node.lineno],  # 基座行号（1-based 含端）
            "helper_span": [anchor + 1, anchor + len(helper_lines)],  # 产物行号（def 行含端；分隔 2 空行不计入）
            "audit": {
                "base_sha256": base_sha,
                "base_main": str(base_path.resolve()),
                "expr": expr,
                "wheat_slot_weight": _WHEAT_SLOT_WEIGHTS[mode],
                "activation_window": _ACTIVATION_WINDOW[mode],
                "replaced_line_span_out": [q_node.lineno + shift, q_node.lineno + shift],
                "inserted_line_count": len(inserted_block),
                "helper_line_count": len(helper_lines),
                "insert_separator_lines": len(sep_lines),
                "region": list(_CARROT2_REGION),
                "zone_anchors": zone_report,
                "zone_list_source": ("行区间回退制为主（授权：清单源实查缺位）；"
                                     "锚函数清单=基座结构另行取（磁带访问/终局清仓/槽位重排/路由）"),
                "last_callable": "_cxd_agent",
                "opcodes": [[t, i1, i2, j1, j2] for t, i1, i2, j1, j2 in ops],
                "validations": validations,
            },
        },
        "out_path": str(out_path.resolve()),
    }
