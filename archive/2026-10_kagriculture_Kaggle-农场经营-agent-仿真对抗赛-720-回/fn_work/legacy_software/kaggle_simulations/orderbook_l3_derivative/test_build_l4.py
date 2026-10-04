"""test_build_l4：中部手术变更集审计（恰一 def+一表达式/五区恒定/双模式）。

① test_clamp_change_set_audit：两模式（fine/coarse）变更集审计——difflib 独立重算：
   opcode 恰 [equal, insert, equal, replace, equal]（一 helper 块插入+恰一 Assign 值替换，
   其余前缀/中缀/后缀逐字节恒等）；diff 行数断言（新增=helper 行+分隔 2+替换 1，删除=1）；
   替换行=基座行 16..26 列的目标项原位替换（尾部 - have - buying 保留）；返回契约字段齐。
② test_fine_helper_semantics_pseudo_tape + test_fine_helper_fallbacks：
   CLAMP_HELPER_SRC 独立 exec（伪上下文注入 _ca_tape/_CA_BUFFER/_CA_TO）：
   route2 后缀 k 个 PLANT,CARROT + day≤28 小麦槽 m → min(8, k+m+2)；磁带读不到/异常 → 8；
   后缀边界（≥step）与天窗边界（小麦限 day≤28、胡萝卜不限天）；
   test_fine_expression_wiring：fine 产物真替换行 exec——目标项**无条件** min
   （day27/day26 都调 helper，实参直传；helper=8 时 q 与基座行恒等=零足迹）。
③ test_coarse_targets_day26_27：coarse 产物真替换行 exec：day26→q=8-have-buying、
   day27→q=2-have-buying（目标 8/2）。
④ test_five_zones_constant：两模式 diff 全落授权区段 [4469,4734]；区锚函数源段恒等；
   基座原件零改动。
⑤ test_q_target_ast_shape_per_mode：AST 断言——fine 目标项=无条件 Call
   min(_CA_BUFFER,_ca_clamped_target(day,seat,step))（无 IfExp；需求相对激活）；
   coarse 目标项=IfExp(day>=27, 2, Name _CA_BUFFER)（R13-b 硬窗不变）；全卷 q
   赋值计数与基座一致（仅一处在形态上变为 mode 分形目标项）。
⑤b test_demand_scan_runtime_budget：无条件 min 的 day<24 磁带扫描实测耗时
   （真产物 exec + 生产态 _ca_tape，最坏 step=144）<10ms/步——不加廉价门的
   取舍留档（实测 ~0.5ms 级）。
⑥ test_build_fine_full_chain_products + test_build_fine_dual_injection_diff_audit：
   build("fine") 全链真跑一次（隔离 out_dir；inject 六校验+append 四校验+双跑打包全在
   链内）——三产物+中间产物+manifest 契约（schema/描述文案/mode/占位 pending S6）与盘上
   真值逐项一致；双注入 diff 审计（独立 difflib 重算）：opcode 恰 [equal,insert,equal,
   replace,equal,insert]——中部恰 45 行级变更（helper 42+分隔 2+替换 1，删除恰 1）+尾部
   恰 layer S 块（两空行+块全文 385 行，锚=基座 EOF）；前缀/中缀/后缀逐字节恒等。
⑦ test_build_coarse_isolated_mode_diff：coarse 隔离 out_dir 构建真跑——产物齐、
   manifest mode=coarse；两模式终产物 diff 恰一 replace 单行（q 目标项原位差异）。
⑧ test_build_identity_chain_base_zero_change：身份链（基座 main/tar、L1 块、盘上
   产物 sha 全数钉住）与基座零改动。
⑨ 变体组（R13 第二次调参）：tuned/lean=小麦槽权重 0.5/0.0——helper 源加权语义
   矩阵（demand=k+m×weight）/fail-safe 与天窗不变/变更集同构+audit 权重/build
   全链产物+manifest wheat_slot_weight+q 行无条件 min AST+主产物发射态 sha 绊网。"""

import ast
import difflib
import hashlib
import json
import tarfile
import textwrap
import time
from pathlib import Path

import pytest

import build_l13_candidate
import inject_controller_clamp

_HERE = Path(__file__).resolve().parent
_BASE = _HERE.parent / "orderbook_derivative" / "main.py"
_BASE_SHA256 = "a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab"
_REGION = (4469, 4734)  # 与 inject_controller_clamp._CARROT2_REGION 同值（测试侧独立字面量）
_HELPER_LINES = inject_controller_clamp.CLAMP_HELPER_SRC.splitlines(keepends=True)
_L3_BLOCK = _HERE.parent / "orderbook_l1_derivative" / "layer_s_block.py"
_L3_BLOCK_SHA256 = "2f3553fe4b2df6213cdc1377b2fa9299ece92506291f4ed8f547640c4e2bbfcd"
_BASE_TAR_SHA256 = "2838cc66e5d3f719569108fa553c9cf9acf8190d0662f8d991856560e6e9641c"
# 发射态主产物指纹（R13 第二次调参变体构建的零改动绊网；build_manifest.json 同源）
_MAIN_SHA256 = "88f9a82fb2ff37b9d6e56d1504515d71e97a4bb37c558c35052ffde133ca036b"
_TAR_SHA256 = "e072a87723d83220aa3f8c40442ef7aac4f8c8203f9604a35238bd95b591ff58"


@pytest.fixture(scope="module")
def products(tmp_path_factory):
    """一次性两模式真注入（inject 内部六校验全跑，含整卷 exec）。"""
    out = {}
    for mode in ("fine", "coarse"):
        path = tmp_path_factory.mktemp(f"l4_{mode}") / "main_clamped.py"
        out[mode] = (path, inject_controller_clamp.inject(_BASE, mode, out_path=path))
    return out


def _lines(path):
    return path.read_text(encoding="utf-8").splitlines(keepends=True)


def _opcodes(base_lines, out_lines):
    return list(difflib.SequenceMatcher(None, base_lines, out_lines, autojunk=False).get_opcodes())


def _q_assigns(tree):
    return [n for n in ast.walk(tree)
            if isinstance(n, ast.Assign) and len(n.targets) == 1
            and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "q"]


def test_clamp_change_set_audit(products):
    # ① 两模式变更集审计：恰一替换+helper 插入；diff 行数断言。
    base_lines = _lines(_BASE)
    assert hashlib.sha256(_BASE.read_bytes()).hexdigest() == _BASE_SHA256  # 基座指纹前置断言
    for mode, (path, report) in products.items():
        out_lines = _lines(path)
        ops = _opcodes(base_lines, out_lines)
        assert [op[0] for op in ops] == ["equal", "insert", "equal", "replace", "equal"]
        _, pi1, pi2, pj1, pj2 = ops[1]
        _, ri1, ri2, rj1, rj2 = ops[3]
        # 插入块==helper 源文本+两分隔空行，恰在层 def 行（基座 4589）之前
        assert (pi1, pi2) == (4588, 4588)
        assert out_lines[pj1:pj2] == _HELPER_LINES + ["\n", "\n"]
        # 恰一 Assign 值替换：基座 4695 行（q = _CA_BUFFER - have - buying）单行
        assert (ri1, ri2) == (4694, 4695)
        assert len(out_lines[rj1:rj2]) == 1
        base_q = base_lines[4694]
        new_q = out_lines[rj1]
        expr = inject_controller_clamp._MODE_EXPRS[mode]
        assert new_q == base_q[:16] + expr + base_q[26:]  # 目标项原位替换（col 16-26）
        assert new_q.rstrip("\n").endswith("- have - buying")  # q 公式尾部保留
        # diff 行数：新增=helper+分隔2+替换1；删除=1（被替换原行）
        added = sum(j2 - j1 for t, i1, i2, j1, j2 in ops if t in ("insert", "replace"))
        removed = sum(i2 - i1 for t, i1, i2, j1, j2 in ops if t in ("delete", "replace"))
        assert (added, removed) == (len(_HELPER_LINES) + 2 + 1, 1)
        # 返回契约：{injected_sha, change_set:{mode, replaced_line_span, helper_span, audit}, out_path}
        assert set(report) == {"injected_sha", "change_set", "out_path"}
        assert set(report["change_set"]) == {"mode", "replaced_line_span", "helper_span", "audit"}
        assert report["change_set"]["mode"] == mode
        assert report["change_set"]["replaced_line_span"] == [4695, 4695]  # 基座行号
        assert report["change_set"]["helper_span"] == [4589, 4589 + len(_HELPER_LINES) - 1]
        assert report["injected_sha"] == hashlib.sha256(path.read_bytes()).hexdigest()
        assert Path(report["out_path"]) == path.resolve()
        out_text = path.read_text(encoding="utf-8")
        assert out_text.count(inject_controller_clamp.CLAMP_HELPER_SRC) == 1  # helper 恰注入一次
    # 两模式产物互异且均异于基座
    sha_fine = products["fine"][1]["injected_sha"]
    sha_coarse = products["coarse"][1]["injected_sha"]
    assert sha_fine != sha_coarse and sha_fine != _BASE_SHA256 and sha_coarse != _BASE_SHA256


def _pseudo_ns(tape_map, ca_buffer=8, ca_to=28):
    """伪上下文注入：_ca_tape/_CA_BUFFER/_CA_TO 供 CLAMP_HELPER_SRC 独立 exec。"""
    ns = {"_CA_BUFFER": ca_buffer, "_CA_TO": ca_to,
          "_ca_tape": lambda seat, t: tape_map.get(t, {})}
    exec(compile(inject_controller_clamp.CLAMP_HELPER_SRC, "<clamp_helper>", "exec"), ns)
    return ns


def _tape_with(k_carrot=0, m_wheat=0, wheat_start=673, carrot_start=650, pass_at=660):
    """route2 后缀伪磁带：k 个 PLANT,CARROT（day27 起）+ m 个 PLANT,WHEAT（默认 day28 窗内）。

    每步条目恰 1 个种植单元（farmer）；pass_at=可读性锚（后缀至少一个非空步条目，
    使 k=m=0 表示"磁带可读但零未来种植"而非"磁带读不到"——两语义 helper 侧可分）。"""
    tape = {}
    if pass_at is not None:
        tape[pass_at] = {"farmer": ["PASS"], "hands": []}
    for i in range(k_carrot):
        tape[carrot_start + i] = {"farmer": ["PLANT", "CARROT"], "hands": []}
    for i in range(m_wheat):
        tape[wheat_start + i] = {"farmer": ["PLANT", "WHEAT"], "hands": []}
    return tape


@pytest.mark.parametrize("k,m,expected", [
    (0, 0, 2), (1, 0, 3), (3, 2, 7), (6, 3, 8), (10, 0, 8), (2, 7, 8),  # min(8, k+m+2) 封顶
])
def test_fine_helper_semantics_pseudo_tape(k, m, expected):
    # ② route2 后缀含 k 个 PLANT,CARROT + day≤28 小麦槽 m → _ca_clamped_target = min(8, k+m+2)。
    ns = _pseudo_ns(_tape_with(k, m))
    assert ns["_ca_future_plant_demand"](0, 650) == k + m
    assert ns["_ca_clamped_target"](27, 0, 650) == expected


def test_fine_helper_fallbacks():
    # ② 磁带读不到→8（回退原目标）；异常→8；后缀/天窗边界；day<27 需求相对取值
    # （修订一轮：防御分支已删，任何 day 都走 min(8, 需求+2)）。
    empty = _pseudo_ns({})
    assert empty["_ca_future_plant_demand"](0, 650) is None  # 后缀无可读步条目
    assert empty["_ca_clamped_target"](27, 0, 650) == 8
    raising = {"_CA_BUFFER": 8, "_CA_TO": 28,
               "_ca_tape": lambda seat, t: (_ for _ in ()).throw(RuntimeError("tape down"))}
    exec(compile(inject_controller_clamp.CLAMP_HELPER_SRC, "<clamp_helper>", "exec"), raising)
    assert raising["_ca_clamped_target"](27, 0, 650) == 8  # 任何异常→原目标
    # 后缀边界：PLANT,CARROT@t<step 不计、@t=step 计（≥当前步）；可读性锚保后缀可读
    ns = _pseudo_ns({649: {"farmer": ["PLANT", "CARROT"], "hands": []},
                     655: {"farmer": ["PASS"], "hands": []}})
    assert ns["_ca_clamped_target"](27, 0, 650) == 2
    ns = _pseudo_ns({650: {"farmer": ["PLANT", "CARROT"], "hands": []}})
    assert ns["_ca_clamped_target"](27, 0, 650) == 3
    # 天窗边界：PLANT,WHEAT@day29（t=700）不计；PLANT,CARROT@day29 仍计（备种不限天）
    ns = _pseudo_ns({700: {"farmer": ["PLANT", "WHEAT"], "hands": []}})
    assert ns["_ca_clamped_target"](27, 0, 650) == 2
    ns = _pseudo_ns({700: {"farmer": ["PLANT", "CARROT"], "hands": []}})
    assert ns["_ca_clamped_target"](27, 0, 650) == 3
    # day<27：需求相对取值（min 恒走，无 day 键控）——k=5 → min(8,7)=7；
    # 需求充足（k≥6）→ 8=原目标（零足迹）
    ns = _pseudo_ns(_tape_with(k_carrot=5))
    assert ns["_ca_clamped_target"](26, 0, 648) == 7
    assert ns["_ca_clamped_target"](6, 0, 144) == 7
    ns = _pseudo_ns(_tape_with(k_carrot=6))
    assert ns["_ca_clamped_target"](24, 0, 576) == 8


def test_fine_expression_wiring(products):
    # ②b fine 产物真替换行 exec：目标项**无条件** min（day27/day26 都走 helper）；
    # helper 回 8（需求充足）时 q 与基座行恒等（零足迹）。
    path, report = products["fine"]
    out_lines = _lines(path)
    new_q = out_lines[report["change_set"]["audit"]["replaced_line_span_out"][0] - 1]
    assert "- have - buying" in new_q
    called = []

    def fake_target(day, seat, step):
        called.append((day, seat, step))
        return 5

    # day27：目标=min(8, helper=5)=5 → q = 5 - have(2) - buying(1) = 2；实参 (27,3,660) 直传
    g = {"day": 27, "seat": 3, "step": 660, "have": 2, "buying": 1,
         "_CA_BUFFER": 8, "_ca_clamped_target": fake_target}
    exec(compile(textwrap.dedent(new_q), "<fine_q>", "exec"), g)
    assert called == [(27, 3, 660)]
    assert g["q"] == 2
    # day26：需求相对激活（修订一轮）——helper 同样被调用 → q = 5 - 2 - 1 = 2
    called.clear()
    g = {"day": 26, "seat": 3, "step": 26 * 24 + 12, "have": 2, "buying": 1,
         "_CA_BUFFER": 8, "_ca_clamped_target": fake_target}
    exec(compile(textwrap.dedent(new_q), "<fine_q>", "exec"), g)
    assert called == [(26, 3, 26 * 24 + 12)]
    assert g["q"] == 2
    # 需求充足（helper=8）：min(8,8)=8 → q 与基座行为恒等（零足迹），helper 仍被调用
    called.clear()
    g = {"day": 24, "seat": 0, "step": 576, "have": 3, "buying": 1,
         "_CA_BUFFER": 8, "_ca_clamped_target": lambda *a: called.append(a) or 8}
    exec(compile(textwrap.dedent(new_q), "<fine_q>", "exec"), g)
    assert g["q"] == 4 and called  # 8-3-1=4；表达式仍写但行为同原式


def test_coarse_targets_day26_27(products):
    # ③ coarse：day26/27 目标 8/2（真替换行 exec；q=目标-have-buying）。
    path, report = products["coarse"]
    out_lines = _lines(path)
    new_q = out_lines[report["change_set"]["audit"]["replaced_line_span_out"][0] - 1]
    for day, have, buying, expected_q in [(26, 0, 0, 8), (27, 0, 0, 2), (27, 1, 2, -1), (26, 3, 4, 1)]:
        g = {"day": day, "seat": 0, "step": day * 24 + 5, "have": have, "buying": buying,
             "_CA_BUFFER": 8, "_ca_clamped_target": lambda *a: 5}
        exec(compile(textwrap.dedent(new_q), "<coarse_q>", "exec"), g)
        assert g["q"] == expected_q, (day, have, buying)


def test_five_zones_constant(products):
    # ④ 五区恒定：两模式 diff 全落授权区段；区锚函数源段恒等；基座零改动。
    base_lines = _lines(_BASE)
    base_tree = ast.parse("".join(base_lines))
    for mode, (path, _report) in products.items():
        out_lines = _lines(path)
        for tag, i1, i2, j1, j2 in _opcodes(base_lines, out_lines):
            if tag == "equal":
                continue
            pos = i1 + 1 if tag != "insert" else i1  # insert 以基座插入锚位计
            assert _REGION[0] - (1 if tag == "insert" else 0) <= pos <= _REGION[1], (mode, tag, pos)
        out_tree = ast.parse("".join(out_lines))
        spans = {}
        for tree, ls in ((base_tree, base_lines), (out_tree, out_lines)):
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in inject_controller_clamp._ZONE_FUNC_NAMES:
                    spans.setdefault(node.name, []).append("".join(ls[node.lineno - 1:node.end_lineno]))
        for name, texts in spans.items():
            assert len(texts) == 2 and texts[0] == texts[1], name  # 基座==产物，源段恒等
    assert hashlib.sha256(_BASE.read_bytes()).hexdigest() == _BASE_SHA256  # 基座原件零改动


def test_q_target_ast_shape_per_mode(products):
    # ⑤ 目标项 AST 分形（修订一轮）：fine=无条件 Call min(_CA_BUFFER,
    # _ca_clamped_target(day, seat, step))（无 IfExp 门控）；coarse=IfExp(day>=27,
    # 2, Name _CA_BUFFER)（R13-b 硬窗不变）。
    for mode, (path, _report) in products.items():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        hits = []
        for node in _q_assigns(tree):
            v = node.value
            if (isinstance(v, ast.BinOp) and isinstance(v.op, ast.Sub)
                    and isinstance(v.left, ast.BinOp) and isinstance(v.left.op, ast.Sub)
                    and isinstance(v.left.right, ast.Name) and v.left.right.id == "have"
                    and isinstance(v.right, ast.Name) and v.right.id == "buying"):
                hits.append((node, v))
        assert len(hits) == 1  # 全卷恰一处 <目标项> - have - buying
        node, v = hits[0]
        assert node.lineno == 4695 + len(_HELPER_LINES) + 2  # 替换行产物行号（4695+插入块位移）
        target = v.left.left
        if mode == "fine":
            # 无条件 min：Call(min, [_CA_BUFFER, _ca_clamped_target(day, seat, step)])
            assert (isinstance(target, ast.Call) and target.func.id == "min"
                    and len(target.args) == 2
                    and isinstance(target.args[0], ast.Name)
                    and target.args[0].id == "_CA_BUFFER"
                    and isinstance(target.args[1], ast.Call)
                    and target.args[1].func.id == "_ca_clamped_target"
                    and [a.id for a in target.args[1].args] == ["day", "seat", "step"])
            assert not any(isinstance(n, ast.IfExp) for n in ast.walk(v)), \
                "fine 目标项不应再含 IfExp 门控（需求相对激活）"
        else:
            # coarse：IfExp(day>=27, 2, _CA_BUFFER)——硬窗不变
            assert (isinstance(target, ast.IfExp)
                    and isinstance(target.test, ast.Compare)
                    and target.test.left.id == "day"
                    and isinstance(target.test.ops[0], ast.GtE)
                    and target.test.comparators[0].value == 27
                    and isinstance(target.body, ast.Constant) and target.body.value == 2
                    and isinstance(target.orelse, ast.Name)
                    and target.orelse.id == "_CA_BUFFER")
        # 全卷 q 赋值计数与基座一致：手术只改形态，不增删语句
        assert len(_q_assigns(tree)) == len(_q_assigns(ast.parse(_BASE.read_text(encoding="utf-8"))))


def test_demand_scan_runtime_budget(products):
    # 修订一轮取舍实测：无条件 min 使 day<24 也调 _ca_future_plant_demand（磁带
    # 扫描）——对真产物整卷 exec 后用生产态 _ca_tape/_IMPL 实测最坏长度扫描
    # （step=144，576 步后缀）耗时，须 <10ms/步（廉价门阈值）；实测 ~0.5ms 级
    # → 不加 day 门（报告见 evidence/verify_summary.json 环境）。
    path, _report = products["fine"]
    ns = {}
    exec(compile(path.read_bytes(), str(path), "exec"), ns)
    # 生产态：chassis 已在 import 期解码；players 填一个席位使 _ca_tape 走真路径
    ns["_IMPL"].chassis.players.setdefault(0, {"route": 0})
    fpd = ns["_ca_future_plant_demand"]
    best = None
    for _ in range(7):
        t0 = time.perf_counter()
        for _ in range(20):
            fpd(0, 144)          # 最坏：day6 起后缀全长 576 步
        dt = (time.perf_counter() - t0) / 20
        best = dt if best is None or dt < best else best
    assert best < 0.010, f"磁带扫描 {best * 1000:.3f} ms/步 ≥ 10ms 预算（需加廉价门）"


# ---------------- ⑥⑦⑧ build_l13_candidate 双注入构建全链（R13 L0；不动上方既有组） ----------------


@pytest.fixture(scope="module")
def l3_built(tmp_path_factory):
    """一次性 build("fine") 全链真跑（inject 六校验+append 四校验+双跑打包全在链内）。"""
    out_dir = tmp_path_factory.mktemp("l3_build_fine")
    manifest = build_l13_candidate.build("fine", out_dir=out_dir)
    return out_dir, manifest


def test_build_fine_full_chain_products(l3_built, products):
    # ⑥ 三产物+中间产物+manifest：字段契约与盘上真值逐项一致；钳制件与独立注入逐字节一致。
    out_dir, manifest = l3_built
    main_path = out_dir / "main.py"
    tar_path = out_dir / "submission.tar.gz"
    clamped_path = out_dir / "main_clamped.py"
    for p in (clamped_path, main_path, tar_path, out_dir / "build_manifest.json"):
        assert p.is_file(), p
    # manifest 盘上件 == 返回值（JSON round-trip）；契约字段
    assert json.loads((out_dir / "build_manifest.json").read_text(encoding="utf-8")) == manifest
    assert manifest["schema"] == "orderbook_l3_derivative_manifest/1.0"
    assert manifest["description"] == (
        "public derivative with seed-truncation layer + late-window carrot demand clamp")
    assert manifest["mode"] == "fine"
    assert manifest["four_gates"] == "pending S6 (verify_l13_gates)"
    assert manifest["h2h_vs_l1"] == "pending S6 (verify_l13_gates)"
    # 盘上真值 == manifest 声明
    main_bytes = main_path.read_bytes()
    clamped_bytes = clamped_path.read_bytes()
    assert manifest["main_sha256"] == hashlib.sha256(main_bytes).hexdigest()
    assert manifest["main_bytes"] == len(main_bytes)
    assert manifest["tar_sha256"] == hashlib.sha256(tar_path.read_bytes()).hexdigest()
    assert manifest["tar_bytes"] == len(tar_path.read_bytes())
    # 中间产物=独立注入（products 夹具）同款逐字节（管线确定性）；块链身份钉住
    assert manifest["clamped_sha256"] == products["fine"][1]["injected_sha"]
    assert hashlib.sha256(clamped_bytes).hexdigest() == manifest["clamped_sha256"]
    assert manifest["clamp_change_set"]["mode"] == "fine"
    block_bytes = _L3_BLOCK.read_bytes()
    assert hashlib.sha256(block_bytes).hexdigest() == _L3_BLOCK_SHA256
    assert manifest["block_sha256"] == _L3_BLOCK_SHA256 == manifest["l1_block_sha256"]
    # 终产物逐字节等式：钳制件全文+两空行+layer S 块
    assert main_bytes == clamped_bytes + b"\n\n" + block_bytes
    # tar 成员恰 ["main.py"] 且成员字节 == main.py（提交布局+内容一致）
    with tarfile.open(tar_path, "r:gz") as tf:
        assert tf.getnames() == ["main.py"]
        assert tf.extractfile("main.py").read() == main_bytes
    # provenance=基座链→钳制变更集审计[mode/sha]→layer S 块 sha→双跑声明
    prov = manifest["provenance_chain"]
    assert len(prov) == 5
    assert _BASE_SHA256 in prov[0] and "三方核对" in prov[0]
    assert _BASE_TAR_SHA256 in prov[1]
    assert "mode=fine" in prov[2] and manifest["clamped_sha256"] in prov[2]
    assert _L3_BLOCK_SHA256 in prov[3] and "append-only" in prov[3]
    assert "double-build byte-identical" in prov[4]


def test_build_fine_dual_injection_diff_audit(l3_built):
    # ⑥b 双注入 diff 审计（独立 difflib 重算）：中部恰 45 行级变更+尾部恰 layer S 块追加。
    out_dir, _manifest = l3_built
    base_lines = _lines(_BASE)
    out_lines = _lines(out_dir / "main.py")
    block_lines = _L3_BLOCK.read_text(encoding="utf-8").splitlines(keepends=True)
    ops = _opcodes(base_lines, out_lines)
    # 双注入 opcode 恰 [equal,insert,equal,replace,equal,insert]：中部手术+尾部追加
    assert [op[0] for op in ops] == ["equal", "insert", "equal", "replace", "equal", "insert"]
    _, pi1, pi2, pj1, pj2 = ops[1]
    _, ri1, ri2, rj1, rj2 = ops[3]
    _, ti1, ti2, tj1, tj2 = ops[5]
    # 中部插入块==helper 源文本+两分隔空行，恰在层 def 行（基座 4589）之前（与①同款）
    assert (pi1, pi2) == (4588, 4588)
    assert out_lines[pj1:pj2] == _HELPER_LINES + ["\n", "\n"]
    # 中部恰一 Assign 值替换：基座 4695 行单行，目标项原位替换（fine 表达式）
    assert (ri1, ri2) == (4694, 4695)
    assert len(out_lines[rj1:rj2]) == 1
    base_q = base_lines[4694]
    assert out_lines[rj1] == base_q[:16] + inject_controller_clamp._MODE_EXPRS["fine"] + base_q[26:]
    # 尾部恰 layer S 块：末 insert==两空行+块全文，锚=基座 EOF（尾部纯追加零基座行消耗）
    assert (ti1, ti2) == (len(base_lines), len(base_lines))
    assert out_lines[tj1:tj2] == ["\n", "\n"] + block_lines
    assert "".join(base_lines[ti2:]) == "" and "".join(out_lines[tj2:]) == ""
    # 行数总账：中部新增=helper 42+分隔 2+替换 1=45 行级；尾部新增=分隔 2+块 385；删除恰 1
    added = sum(j2 - j1 for t, i1, i2, j1, j2 in ops if t in ("insert", "replace"))
    removed = sum(i2 - i1 for t, i1, i2, j1, j2 in ops if t in ("delete", "replace"))
    assert (added, removed) == (len(_HELPER_LINES) + 2 + 1 + 2 + len(block_lines), 1)
    # 前缀/中缀/后缀与基座逐字节恒等（三段证明；基座指纹前置断言）
    assert hashlib.sha256(_BASE.read_bytes()).hexdigest() == _BASE_SHA256
    assert "".join(base_lines[:pi1]) == "".join(out_lines[:pj1])
    assert "".join(base_lines[pi2:ri1]) == "".join(out_lines[pj2:rj1])
    assert "".join(base_lines[ri2:ti1]) == "".join(out_lines[rj2:tj1])


def test_build_coarse_isolated_mode_diff(tmp_path, l3_built):
    # ⑦ coarse 隔离 out_dir 构建真跑：产物齐、mode=coarse；两模式终产物差异恰 q 目标项一行。
    fine_dir, fine_manifest = l3_built
    coarse_dir = tmp_path / "l3_build_coarse"
    coarse_manifest = build_l13_candidate.build("coarse", out_dir=coarse_dir)
    assert coarse_manifest["mode"] == "coarse"
    assert coarse_manifest["schema"] == "orderbook_l3_derivative_manifest/1.0"
    assert coarse_manifest["four_gates"] == "pending S6 (verify_l13_gates)"
    for name in ("main_clamped.py", "main.py", "submission.tar.gz", "build_manifest.json"):
        assert (coarse_dir / name).is_file(), name
    # 两模式中间产物互异、终产物互异（tar 随 main 内容联动）
    assert coarse_manifest["clamped_sha256"] != fine_manifest["clamped_sha256"]
    assert coarse_manifest["tar_sha256"] != fine_manifest["tar_sha256"]
    # 模式差异行：两模式终产物 diff 恰一 replace 单行（同一位移后的 q 行；目标项原位差异）
    fine_lines = _lines(fine_dir / "main.py")
    coarse_lines = _lines(coarse_dir / "main.py")
    ops = _opcodes(fine_lines, coarse_lines)
    assert [op[0] for op in ops] == ["equal", "replace", "equal"]
    _, i1, i2, j1, j2 = ops[1]
    q_idx_out = 4694 + len(_HELPER_LINES) + 2  # 基座 4695 行+插入块位移（0-based 产物下标）
    assert (i1, i2, j1, j2) == (q_idx_out, q_idx_out + 1, q_idx_out, q_idx_out + 1)
    base_q = _lines(_BASE)[4694]
    assert fine_lines[i1] == base_q[:16] + inject_controller_clamp._MODE_EXPRS["fine"] + base_q[26:]
    assert coarse_lines[j1] == base_q[:16] + inject_controller_clamp._MODE_EXPRS["coarse"] + base_q[26:]
    assert coarse_lines[j1].rstrip("\n").endswith("- have - buying")  # q 公式尾部保留


def test_build_identity_chain_base_zero_change(l3_built):
    # ⑧ 身份链与基座零改动：全链构建（含⑦ coarse 隔离跑）之后基座/块链/盘上产物 sha 全数钉住。
    out_dir, manifest = l3_built
    assert hashlib.sha256(_BASE.read_bytes()).hexdigest() == _BASE_SHA256  # 基座 main.py 零改动
    assert hashlib.sha256((_HERE.parent / "orderbook_derivative" / "submission.tar.gz")
                          .read_bytes()).hexdigest() == _BASE_TAR_SHA256  # 基座 tar 零改动
    assert hashlib.sha256(_L3_BLOCK.read_bytes()).hexdigest() == _L3_BLOCK_SHA256  # L1 块链恒定
    # 盘上产物身份 == manifest 声明（终产物与中间产物均未被后续步骤触碰）
    assert hashlib.sha256((out_dir / "main.py").read_bytes()).hexdigest() == manifest["main_sha256"]
    assert hashlib.sha256((out_dir / "main_clamped.py").read_bytes()).hexdigest() == manifest["clamped_sha256"]
    # 基座目录无本构建器写痕（构建只写 out_dir；orderbook_derivative/ 只读——目录内
    # 既有 h2h/launch 证据文件为前轮产物，与本构建无关，不在断言面内）
    _leak = [p.name for p in (_HERE.parent / "orderbook_derivative").iterdir()
             if "build_l13" in p.name or "inject_controller_clamp" in p.name
             or p.name == "main_clamped.py"]
    assert _leak == []


# ---------------- ⑨ R13 第二次调参变体（tuned/lean：小麦槽权重 0.5/0.0） ----------------


@pytest.fixture(scope="module")
def variant_products(tmp_path_factory):
    """一次性两变体真注入（inject 内部六校验全跑，含整卷 exec）。"""
    out = {}
    for mode in ("tuned", "lean"):
        path = tmp_path_factory.mktemp(f"l4_{mode}") / "main_clamped.py"
        out[mode] = (path, inject_controller_clamp.inject(_BASE, mode, out_path=path))
    return out


def _variant_ns(mode, tape_map, ca_buffer=8, ca_to=28):
    """伪上下文独立 exec 变体加权 helper 源（clamp_helper_src(mode)）。"""
    ns = {"_CA_BUFFER": ca_buffer, "_CA_TO": ca_to,
          "_ca_tape": lambda seat, t: tape_map.get(t, {})}
    exec(compile(inject_controller_clamp.clamp_helper_src(mode),
                 f"<clamp_helper_{mode}>", "exec"), ns)
    return ns


@pytest.mark.parametrize("mode,weight", [("tuned", 0.5), ("lean", 0.0)])
@pytest.mark.parametrize("k,m", [(0, 0), (2, 4), (5, 6), (6, 4), (10, 0), (1, 9)])
def test_variant_demand_weight_semantics(mode, weight, k, m):
    # ⑨-1 变体需求口径：demand = k 胡萝卜 + m 小麦槽×weight（float 精确）；
    # target=min(8, int(demand)+2)——day24/26/27 同式（表达式与 fine 同形，
    # 需求相对激活在变体同样成立）。
    ns = _variant_ns(mode, _tape_with(k, m))
    want = k + m * weight
    assert ns["_ca_future_plant_demand"](0, 650) == want
    for day, step in ((24, 576), (26, 624), (27, 650)):
        assert ns["_ca_clamped_target"](day, 0, step) == min(8, int(want) + 2)


@pytest.mark.parametrize("mode", ["tuned", "lean"])
def test_variant_fallbacks_and_windows(mode):
    # ⑨-2 fail-safe 与天窗在变体口径下不变：读不到→None→8（回退原目标）；
    # 小麦@day29 不计（无论权重）；胡萝卜@day29 仍计（备种不限天）。
    empty = _variant_ns(mode, {})
    assert empty["_ca_future_plant_demand"](0, 650) is None
    assert empty["_ca_clamped_target"](27, 0, 650) == 8
    ns = _variant_ns(mode, {700: {"farmer": ["PLANT", "WHEAT"], "hands": []}})
    assert ns["_ca_clamped_target"](27, 0, 650) == 2
    ns = _variant_ns(mode, {700: {"farmer": ["PLANT", "CARROT"], "hands": []}})
    assert ns["_ca_clamped_target"](27, 0, 650) == 3


def test_variant_change_set_structure(variant_products, products):
    # ⑨-3 变体变更集：opcode 同构（insert@4588 + replace@4694），插入块=加权
    # helper+两分隔行；diff 全落授权区段；q 表达式与 fine 同形；audit 携带
    # 权重；fine/coarse 产物零权重名（主口径字节零漂移）。
    base_lines = _lines(_BASE)
    for mode, weight in (("tuned", 0.5), ("lean", 0.0)):
        path, report = variant_products[mode]
        out_lines = _lines(path)
        ops = _opcodes(base_lines, out_lines)
        assert [op[0] for op in ops] == ["equal", "insert", "equal", "replace", "equal"]
        _, pi1, pi2, pj1, pj2 = ops[1]
        _, ri1, ri2, _rj1, _rj2 = ops[3]
        assert (pi1, pi2) == (4588, 4588)
        helper_lines = inject_controller_clamp.clamp_helper_src(mode).splitlines(keepends=True)
        assert out_lines[pj1:pj2] == helper_lines + ["\n", "\n"]
        assert (ri1, ri2) == (4694, 4695)
        for tag, i1, i2, j1, j2 in ops:
            if tag == "equal":
                continue
            pos = i1 + 1 if tag != "insert" else i1
            assert _REGION[0] - (1 if tag == "insert" else 0) <= pos <= _REGION[1], (mode, tag, pos)
        assert report["change_set"]["mode"] == mode
        assert report["change_set"]["audit"]["wheat_slot_weight"] == weight
        assert inject_controller_clamp._MODE_EXPRS[mode] == inject_controller_clamp._MODE_EXPRS["fine"]
        text = path.read_text(encoding="utf-8")
        assert text.count(f"_CA_WHEAT_SLOT_WEIGHT = {weight!r}") == 1
        assert "total += _CA_WHEAT_SLOT_WEIGHT" in text
    for mode in ("fine", "coarse"):
        assert "_CA_WHEAT_SLOT_WEIGHT" not in products[mode][0].read_text(encoding="utf-8")


def test_variant_ast_shape_and_build_products(tmp_path):
    # ⑨-4 build 全链真跑（tuned/lean）：manifest mode+wheat_slot_weight+产物件+
    # tar 成员；终产物=钳制件+两空行+layer S 块；q 行 AST=无条件 min（fine 族
    # 同形）；构建后主产物发射态零漂移（sha 绊网）。
    for mode, weight in (("tuned", 0.5), ("lean", 0.0)):
        out_dir = tmp_path / f"l3_build_{mode}"
        manifest = build_l13_candidate.build(mode, out_dir=out_dir)
        assert manifest["mode"] == mode
        assert manifest["wheat_slot_weight"] == weight
        assert manifest["clamp_change_set"]["audit"]["wheat_slot_weight"] == weight
        assert manifest["four_gates"] == "pending S6 (verify_l13_gates)"
        for name in ("main_clamped.py", "main.py", "submission.tar.gz", "build_manifest.json"):
            assert (out_dir / name).is_file(), (mode, name)
        main_bytes = (out_dir / "main.py").read_bytes()
        block_bytes = _L3_BLOCK.read_bytes()
        assert main_bytes == (out_dir / "main_clamped.py").read_bytes() + b"\n\n" + block_bytes
        with tarfile.open(out_dir / "submission.tar.gz", "r:gz") as tf:
            assert tf.getnames() == ["main.py"]
            assert tf.extractfile("main.py").read() == main_bytes
        # AST：全卷恰一处 <目标项>-have-buying，目标项=无条件 min（fine 族同形）
        tree = ast.parse(main_bytes)
        hits = []
        for node in _q_assigns(tree):
            v = node.value
            if (isinstance(v, ast.BinOp) and isinstance(v.op, ast.Sub)
                    and isinstance(v.left, ast.BinOp) and isinstance(v.left.op, ast.Sub)
                    and isinstance(v.left.right, ast.Name) and v.left.right.id == "have"
                    and isinstance(v.right, ast.Name) and v.right.id == "buying"):
                hits.append((node, v))
        assert len(hits) == 1
        target = hits[0][1].left.left
        assert (isinstance(target, ast.Call) and isinstance(target.func, ast.Name)
                and target.func.id == "min" and len(target.args) == 2
                and isinstance(target.args[0], ast.Name)
                and target.args[0].id == "_CA_BUFFER"
                and isinstance(target.args[1], ast.Call)
                and isinstance(target.args[1].func, ast.Name)
                and target.args[1].func.id == "_ca_clamped_target"
                and [a.id for a in target.args[1].args] == ["day", "seat", "step"])
        assert not any(isinstance(n, ast.IfExp) for n in ast.walk(hits[0][1]))
    # 主产物发射态零漂移绊网（变体构建只写隔离目录）
    assert hashlib.sha256((_HERE / "main.py").read_bytes()).hexdigest() == _MAIN_SHA256
    assert hashlib.sha256((_HERE / "submission.tar.gz").read_bytes()).hexdigest() == _TAR_SHA256
