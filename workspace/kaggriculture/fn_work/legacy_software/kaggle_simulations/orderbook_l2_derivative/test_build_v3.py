"""test_build_v3：受控变更集白名单审计与双窗产物（R12 make 面）。

单测面（S5）：
- 白名单恰合：change_set_audit 的删/增/改集合逐一等于白名单，其余顶层语句
  逐字节恒等（确定性重建等值 + 区间剥离对照双验），末顶层 def 仍 _cxs_agent；
- 窗口注入双值：window=648（字节恒等注入）与 window=600（_CXS_FROM 行改写、
  常数值 648→600、两窗 sha 互异、运行时窗口界生效）；
- 幂等与 sha 稳定：破坏产物重跑同 sha 同内容；跨目标路径产物逐字节一致；
- 白名单外篡改检测：_audit_change_set 对 _cxs_plan_view/其余常数/其余函数/
  注释/增删函数/语法坏等篡改面全数抛 ValueError，合法重建不抛；
- fail-closed：L1 结构漂移（目标函数改名）→ make 抛且零产物。

build 收口组（R12 追加，不动上方 make 组）：
- test_build_v3_full_chain_both_windows：build()（缺省 both+本目录）全链真跑一次
  （两窗三产物落盘留档=候选包本体）；manifest 字段/身份链/窗口互异/双跑/tar
  成员/注入 diff 仅尾部逐项断言；
- test_build_v3_inject_prewrite_guards：注入三道写入前防线（写入前即抛，零 exec，
  含跨窗判重）；
- test_build_v3_single_window_and_overwrite_paths：单窗构建参数路径（隔离 out_dir
  真跑）+旧产物白名单覆盖+非法 window 参数拒绝。"""

import ast
import hashlib
import sys
from pathlib import Path

import pytest

import make_layer_s_v3_block as maker

_THIS_DIR = Path(__file__).resolve().parent
_L1_DIR = _THIS_DIR.parent / "orderbook_l1_derivative"
_L1_BLOCK = _L1_DIR / "layer_s_block.py"
_L1_BLOCK_SHA256 = "2f3553fe4b2df6213cdc1377b2fa9299ece92506291f4ed8f547640c4e2bbfcd"


def _line_span(text, lineno, end_lineno):
    """1-based 闭行区间的逐字节片段（含行尾换行）。"""
    return "".join(text.splitlines(keepends=True)[lineno - 1:end_lineno])


def _top_keys(text):
    """(kind, key, node) 顶层语句清单（与 maker._top_statements 同款分类）。"""
    out, others = [], 0
    for node in ast.parse(text).body:
        if isinstance(node, ast.FunctionDef):
            out.append(("def", node.name, node))
        elif (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)):
            out.append(("const", node.targets[0].id, node))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            out.append(("const", node.target.id, node))
        else:
            out.append(("other", others, node))
            others += 1
    return out


def _find(text, kind, name):
    matches = [node for k, n, node in _top_keys(text) if (k, n) == (kind, name)]
    assert len(matches) == 1, (kind, name, len(matches))
    return matches[0]


def _strip_spans(text, spans):
    """剥离 1-based 闭行区间后的行列表（区间剥离对照：白名单外零字节漂移）。"""
    skip = set()
    for lo, hi in spans:
        skip.update(range(lo, hi + 1))
    return [line for i, line in enumerate(text.splitlines(keepends=True), 1) if i not in skip]


def test_v3_block_change_set_audit(tmp_path):
    l1_text = _L1_BLOCK.read_text(encoding="utf-8")
    assert hashlib.sha256(_L1_BLOCK.read_bytes()).hexdigest() == _L1_BLOCK_SHA256  # 基底契约钉

    # ---- make 真跑（双窗）：返回契约三键 + sha 与盘上真值一致 ----
    out648 = tmp_path / "layer_s_block_v3_w648.py"
    info = maker.make(_L1_BLOCK, out648, window=648)
    assert Path(info["v3_path"]) == out648
    v3_text = out648.read_text(encoding="utf-8")
    assert info["v3_sha256"] == hashlib.sha256(out648.read_bytes()).hexdigest()
    out600 = tmp_path / "layer_s_block_v3_w600.py"
    info600 = maker.make(_L1_BLOCK, out600, window=600)
    v3_600 = out600.read_text(encoding="utf-8")
    assert info600["v3_sha256"] == hashlib.sha256(out600.read_bytes()).hexdigest()
    assert info["v3_sha256"] != info600["v3_sha256"]  # 双窗产物互异

    # ---- 白名单恰合（语义层）：删/增/改集合逐一等于白名单 ----
    audit = info["change_set_audit"]
    assert audit["deleted_functions"] == sorted(["_cxs_seed_truncate", "_cxs_seed_surplus"])
    assert audit["added_functions"] == sorted(
        ["_cxs_reduce_orders", "_cxs_seed_balance", "_cxs_observed_plant_rate"])
    assert audit["added_constants"] == sorted(
        ["_CXS_SAFETY_LOOKBACK_STEPS", "_CXS_SAFETY_MIN_MARGIN", "_CXS_ROUTE_BOUNDARY"])
    assert audit["modified_functions"] == ["_cxs_agent", "_cxs_plan_view"]  # plan_view=路由行解耦
    assert audit["modified_constants"] == {"_CXS_FROM": [648, 648]}
    assert audit["route_boundary"] == 648
    assert audit["unchanged_top_level"] == 9  # 13 顶层语句 −2 删 −2 改（agent+plan_view）
    assert audit["last_def"] == "_cxs_agent"
    audit600 = info600["change_set_audit"]
    assert audit600["deleted_functions"] == audit["deleted_functions"]
    assert audit600["added_functions"] == audit["added_functions"]
    assert audit600["added_constants"] == audit["added_constants"]
    assert audit600["modified_functions"] == ["_cxs_agent", "_cxs_plan_view"]
    assert audit600["modified_constants"] == {"_CXS_FROM": [648, 600]}
    assert audit600["route_boundary"] == 648
    assert audit600["unchanged_top_level"] == 8  # w600 的 _CXS_FROM 行亦属改写

    # ---- AST 结构：旧函数删尽、新函数恰一、末 def 仍 _cxs_agent、常数注入 ----
    v3_tree = ast.parse(v3_text)
    v3_defs = [n.name for n in v3_tree.body if isinstance(n, ast.FunctionDef)]
    assert "_cxs_seed_truncate" not in v3_defs and "_cxs_seed_surplus" not in v3_defs
    for name in ("_cxs_plan_view", "_cxs_reduce_orders", "_cxs_seed_balance",
                 "_cxs_observed_plant_rate", "_cxs_completable_plant_demand",
                 "_cxs_harvest_completable", "_cxs_agent"):
        assert v3_defs.count(name) == 1, name
    assert v3_defs[-1] == "_cxs_agent"
    from_line_648 = _line_span(v3_text, *_span_of(v3_text, "const", "_CXS_FROM"))
    assert from_line_648 == "_CXS_FROM = 648\n"  # 648 注入=字节恒等（白名单允许、不强制）
    from_line_600 = _line_span(v3_600, *_span_of(v3_600, "const", "_CXS_FROM"))
    assert from_line_600 == "_CXS_FROM = 600\n"
    safety_a = _find(v3_text, "const", "_CXS_SAFETY_LOOKBACK_STEPS")
    safety_b = _find(v3_text, "const", "_CXS_SAFETY_MIN_MARGIN")
    assert safety_a.value.value == 24 and safety_b.value.value == 2
    # ---- 路由解耦（2026-09-24 修正）：两窗产物 _CXS_ROUTE_BOUNDARY 恒 648（基座硬事实，
    #      非 window 参数）；plan_view 体内比较节点改引 _CXS_ROUTE_BOUNDARY、无 _CXS_FROM。----
    for text in (v3_text, v3_600):
        boundary = _find(text, "const", "_CXS_ROUTE_BOUNDARY")
        assert type(boundary.value) is ast.Constant and boundary.value.value == 648
        pv = _find(text, "def", "_cxs_plan_view")
        pv_span = _line_span(text, pv.lineno, pv.end_lineno)
        assert maker._ROUTE_LINE_NEW in pv_span and "_CXS_FROM" not in pv_span
        # AST 断言：plan_view 路由行的比较对象是 _CXS_ROUTE_BOUNDARY（非 _CXS_FROM）
        names_used = {n.id for n in ast.walk(pv) if isinstance(n, ast.Name)}
        assert "_CXS_ROUTE_BOUNDARY" in names_used and "_CXS_FROM" not in names_used

    # ---- 改写区逐字节等于嵌入源（拼接面防漂移）----
    for name, src in (("_cxs_reduce_orders", maker.V3_REDUCE_SRC),
                      ("_cxs_seed_balance", maker.V3_BALANCE_SRC),
                      ("_cxs_observed_plant_rate", maker.V3_PLANT_RATE_SRC),
                      ("_cxs_agent", maker.V3_AGENT_SRC)):
        node = _find(v3_text, "def", name)
        assert _line_span(v3_text, node.lineno, node.end_lineno) == src, name

    # ---- 白名单外零字节漂移（区间剥离对照）：两侧各剥离白名单区间后行列表恒等 ----
    l1_spans = [_span_of(l1_text, "const", "_CXS_FROM"),
                _span_of(l1_text, "def", "_cxs_plan_view"),
                _span_of(l1_text, "def", "_cxs_seed_truncate"),
                _span_of(l1_text, "def", "_cxs_seed_surplus"),
                _span_of(l1_text, "def", "_cxs_agent")]
    v3_spans = [_span_of(v3_text, "const", "_CXS_FROM"),
                _span_of(v3_text, "const", "_CXS_ROUTE_BOUNDARY"),
                _span_of(v3_text, "const", "_CXS_SAFETY_LOOKBACK_STEPS"),
                _span_of(v3_text, "const", "_CXS_SAFETY_MIN_MARGIN"),
                _span_of(v3_text, "def", "_cxs_plan_view"),
                _span_of(v3_text, "def", "_cxs_reduce_orders"),
                # balance..rate 整段（含区间内分隔空行——属改写区胶水）
                (_find(v3_text, "def", "_cxs_seed_balance").lineno,
                 _find(v3_text, "def", "_cxs_observed_plant_rate").end_lineno),
                _span_of(v3_text, "def", "_cxs_agent")]
    assert _strip_spans(l1_text, l1_spans) == _strip_spans(v3_text, v3_spans)

    # ---- 幂等 + sha 稳定：破坏产物重跑同 sha 同内容；跨路径产物逐字节一致 ----
    out648.write_text("stale", encoding="utf-8")
    info2 = maker.make(_L1_BLOCK, out648, window=648)
    assert info2["v3_sha256"] == info["v3_sha256"]
    assert out648.read_text(encoding="utf-8") == v3_text
    other = tmp_path / "elsewhere" / "layer_s_block_v3.py"
    other.parent.mkdir()
    assert maker.make(_L1_BLOCK, other, window=648)["v3_sha256"] == info["v3_sha256"]
    assert other.read_bytes() == out648.read_bytes()

    # ---- 白名单外篡改检测：_audit_change_set 全数抛 ValueError ----
    def _audit_raises(tampered):
        with pytest.raises(ValueError):
            maker._audit_change_set(l1_text, tampered, 648)

    _audit_raises(v3_text.replace(  # 白名单函数体越权篡改（plan_view 折叠行——超"单点
        'out[t] = {"plants": plants, "buy_seed": buys}',        # 常数替换"范围，字节层捕获）
        'out[t] = {"plants": plants, "buy_seed": buys, "x": 1}', 1))
    _audit_raises(v3_text.replace(  # 路由解耦回退（重引 _CXS_FROM——解耦不变式捕获）
        maker._ROUTE_LINE_NEW, maker._ROUTE_LINE_OLD, 1))
    _audit_raises(v3_text.replace("_CXS_ROUTE_BOUNDARY = 648", "_CXS_ROUTE_BOUNDARY = 600", 1))
    _audit_raises(v3_text.replace("_CXS_SEASON_END = 718", "_CXS_SEASON_END = 717", 1))
    _audit_raises(v3_text.replace('"WHEAT": 48,', '"WHEAT": 47,', 1))
    _audit_raises(v3_text.replace(  # 非白名单函数体篡改（harvest）
        "return step + table[crop] <= _CXS_PLANT_DEADLINE_SUM",
        "return step + table[crop] <= _CXS_PLANT_DEADLINE_SUM - 1", 1))
    _audit_raises(v3_text.replace("# 契约级常数（requirements R10：step≥648=d27 起；季末=step 718）",
                                  "# 篡改注释", 1))  # 区间外注释漂移
    _audit_raises(v3_text + "\n\ndef _extra_tamper():\n    return 1\n")  # 白名单外新增 def
    _audit_raises("\n".join(v3_text.splitlines()[:-1]) + "\n")  # 删末行（agent 体残缺→重建不等）
    _audit_raises(v3_text.replace("def _cxs_agent(", "def _cxs_agent_v3(", 1))  # 末 def 改名
    _audit_raises(v3_text.replace("return deficit + margin", "return deficit + margin + 1", 1))
    _audit_raises("def broken(:\n")  # 语法坏 → SyntaxError 定向收编为 ValueError
    # 合法重建不抛（对照组；w600 亦然）
    assert maker._audit_change_set(l1_text, v3_text, 648)["last_def"] == "_cxs_agent"
    maker._audit_change_set(l1_text, v3_600, 600)

    # 窗口注入越界/类型面：bool/str/0/719 全数拒绝且零产物。
    for bad_window in (True, "600", 0, 719, 648.0):
        with pytest.raises(ValueError):
            maker.make(_L1_BLOCK, tmp_path / f"bad_{bad_window!r}.py", window=bad_window)

    # ---- fail-closed：L1 结构漂移（目标函数改名）→ make 抛且零产物 ----
    tampered_l1 = tmp_path / "tampered_l1.py"
    tampered_l1.write_text(
        l1_text.replace("def _cxs_seed_truncate(", "def _cxs_seed_truncate_renamed("),
        encoding="utf-8")
    refused = tmp_path / "should_not_exist.py"
    with pytest.raises(ValueError):
        maker.make(tampered_l1, refused)
    assert not refused.exists()


def _span_of(text, kind, name):
    """1-based 闭行区间（kind, name）定位（唯一性由调用方语义保证）。"""
    node = _find(text, kind, name)
    return (node.lineno, node.end_lineno)


# ---------------------------------------------------------------------------
# build 收口组（R12）：真跑一次 build_l2_candidate.build()（缺省 out_dir=本目录、
# window='both'），两窗三产物落盘留档（它就是候选包本体）；全默认 build 恰跑一次
# （耗时纪律，两窗各含一次 ~1MB 整卷 exec，实测秒级）。

import json
import re
import tarfile
import time

import build_l2_candidate

_BASE = _THIS_DIR.parent / "orderbook_derivative" / "main.py"
_BASE_TAR = _THIS_DIR.parent / "orderbook_derivative" / "submission.tar.gz"
_BASE_SHA256 = "a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab"
_BASE_TAR_SHA256 = "2838cc66e5d3f719569108fa553c9cf9acf8190d0662f8d991856560e6e9641c"

# v3 窗块产物位（make 管线产物位=build 注入源=gate_equivalence_v3 预期位）。
_V3_BLOCK_FILES = {w: _THIS_DIR / f"layer_s_block_v3_w{w}.py" for w in ("648", "600")}
# 两窗块身份钉（R12 管线实测；make 幂等确定性→重生成恒等）：
_V3_BLOCK_SHA256 = {
    "648": "5fc4c53ce2d4dc4dad0f533efb0a95198ea98f9385146251e1946b1d8997feff",
    "600": "c308ff2630ffd9f14ba14c268a21e1ef3b1c3ce86f4c5628050006b0f771c48c",
}

# build 全链预算（两窗各：make AST 级+复制+注入含 ~1MB 整卷 exec（实测亚秒级）
# +双跑打包），预算 180s。
_BUILD_BUDGET_SECONDS = 180.0

# manifest 必备键（R12 收口契约：schema/窗口面/身份链输入/审计/占位门/描述文案）。
_REQUIRED_MANIFEST_KEYS = {
    "schema", "candidate", "generated", "description", "window", "route_boundary",
    "main_sha256", "main_bytes", "tar_sha256", "tar_bytes",
    "block_sha256", "block_bytes", "l1_block_sha256", "change_set_audit",
    "provenance_chain", "four_gates", "h2h_vs_l1",
}


@pytest.fixture(scope="module")
def built():
    """一次性真跑 build()：返回 (result, elapsed_seconds)；两窗产物留盘。"""
    t0 = time.perf_counter()
    result = build_l2_candidate.build()
    elapsed = time.perf_counter() - t0
    return result, elapsed


def test_build_v3_full_chain_both_windows(built):
    # 全链实跑（both）：两窗三产物齐落盘；manifest 字段齐且与盘上真值逐项一致；
    # 身份链完整；窗口互异；注入 diff 仅尾部；tar 成员==基座同款；确定性独立复核。
    result, elapsed = built
    assert elapsed < _BUILD_BUDGET_SECONDS, f"build 全链超预算: {elapsed:.1f}s >= 180s"
    assert set(result) == {"windows"}
    assert set(result["windows"]) == {"648", "600"}
    base_bytes = _BASE.read_bytes()
    mains = {}
    for w in ("648", "600"):
        win_dir = _THIS_DIR / f"w{w}"
        main_p = win_dir / "main.py"
        tar_p = win_dir / "submission.tar.gz"
        mf_p = win_dir / "build_manifest.json"
        assert main_p.is_file() and tar_p.is_file() and mf_p.is_file()
        m = result["windows"][w]
        main_bytes = main_p.read_bytes()
        mains[w] = main_bytes

        # manifest 契约面：schema/必备键/描述文案/窗口与路由边界（648 硬事实恒定）
        assert m["schema"] == "orderbook_l2_derivative_manifest/1.0"
        assert _REQUIRED_MANIFEST_KEYS <= set(m)
        assert m["description"] == "public derivative with seed-truncation layer v3 (quantity-balanced)"
        assert m["window"] == int(w)
        assert m["route_boundary"] == 648

        # 与盘上真值逐项一致（main/tar/block 三件 + 身份链输入）
        assert m["main_sha256"] == hashlib.sha256(main_bytes).hexdigest()
        assert m["main_bytes"] == len(main_bytes)
        assert m["tar_sha256"] == hashlib.sha256(tar_p.read_bytes()).hexdigest()
        assert m["tar_bytes"] == tar_p.stat().st_size
        assert m["block_sha256"] == hashlib.sha256(_V3_BLOCK_FILES[w].read_bytes()).hexdigest()
        assert m["block_bytes"] == _V3_BLOCK_FILES[w].stat().st_size
        assert m["block_sha256"] == _V3_BLOCK_SHA256[w]  # 管线身份钉
        assert m["l1_block_sha256"] == _L1_BLOCK_SHA256

        # change_set_audit 原样入档+窗口/路由边界一致
        audit = m["change_set_audit"]
        assert audit["window"] == int(w)
        assert audit["route_boundary"] == 648
        assert audit["modified_constants"] == {"_CXS_FROM": [648, int(w)]}
        assert audit["last_def"] == "_cxs_agent"

        # 注入 diff 仅尾部（append-only 复核）：前缀=基座全文逐字节，形态=基座+两空行+该窗块
        block_bytes = _V3_BLOCK_FILES[w].read_bytes()
        assert main_bytes.startswith(base_bytes)
        assert main_bytes == base_bytes + build_l2_candidate._SEPARATOR + block_bytes

        # 身份链：基座链→L1 块→v3 块[窗 sha]→双跑声明（链文在档）+ S4 占位门
        chain = "\n".join(m["provenance_chain"])
        assert _BASE_SHA256 in chain
        assert _BASE_TAR_SHA256 in chain
        assert _L1_BLOCK_SHA256 in chain
        assert m["block_sha256"] in chain
        assert f"window={w}" in chain
        assert "double-build byte-identical" in chain
        assert "pending S4" in m["four_gates"]
        assert "pending S4" in m["h2h_vs_l1"]
        assert re.match(r"^\d{4}-\d{2}-\d{2}$", m["generated"])

        # 盘上 manifest 文件与 build() 返回 dict 逐项一致
        assert json.loads(mf_p.read_text(encoding="utf-8")) == m

        # tar 成员==基座包同款：恰 ["main.py"]（Kaggle 提交布局）
        with tarfile.open(tar_p) as tf:
            ours = tf.getnames()
        with tarfile.open(_BASE_TAR) as tf:
            base_names = tf.getnames()
        assert ours == base_names == ["main.py"]

        # 独立复核确定性（双跑之外第三方复核：配方函数直调重建，不重跑 build）
        rebuilt = build_l2_candidate._pack_tar_gz(main_bytes)
        assert rebuilt == tar_p.read_bytes()

    # 窗口互异：两窗 main/tar/block sha 两两互异，且差异面恰=块内 _CXS_FROM 常数行
    m648, m600 = result["windows"]["648"], result["windows"]["600"]
    assert m648["block_sha256"] != m600["block_sha256"]
    assert m648["main_sha256"] != m600["main_sha256"]
    assert m648["tar_sha256"] != m600["tar_sha256"]
    b648, b600 = mains["648"], mains["600"]
    i = next(k for k in range(min(len(b648), len(b600))) if b648[k] != b600[k])
    assert b648[:i].endswith(b"_CXS_FROM = 6"), "两窗首个差异不在 _CXS_FROM 常数行"
    assert b648[i:i + 2] == b"48" and b600[i:i + 2] == b"00"
    tail648 = b648[b648.index(b"\n", i):]  # 该常数行行尾之后
    tail600 = b600[b600.index(b"\n", i):]
    assert tail648 == tail600  # 差异行之后两窗逐字节恒等（差异面恰=常数行）

    # 基座原件在 build 全链后仍逐字节未动（零改动纪律）
    assert hashlib.sha256(_BASE.read_bytes()).hexdigest() == _BASE_SHA256
    assert hashlib.sha256(_BASE_TAR.read_bytes()).hexdigest() == _BASE_TAR_SHA256


def test_build_v3_inject_prewrite_guards(built, tmp_path):
    # 注入三道写入前防线（全部在写入前抛出，零 exec 成本，文件零改动）。
    # 防线一：目标指向基座原件 → 拒绝（只读纪律）
    with pytest.raises(ValueError, match="refusing to inject"):
        build_l2_candidate._inject_v3(_BASE, "648")
    # 防线二：已注入产物再注入 → 判重拒绝（sentinel/块字节，文件逐字节不变）；
    #         跨窗变体：w648 已注入产物对 w600 块亦拒绝（v3 sentinel 两窗同串）。
    main_p = _THIS_DIR / "w648" / "main.py"
    before = main_p.read_bytes()
    with pytest.raises(ValueError, match="already injected"):
        build_l2_candidate._inject_v3(main_p, "648")
    with pytest.raises(ValueError, match="already injected"):
        build_l2_candidate._inject_v3(main_p, "600")
    assert main_p.read_bytes() == before
    # 防线三：非基座逐字节副本（前置态漂移）→ 拒绝注入
    drifted = tmp_path / "drifted.py"
    drifted.write_bytes(_BASE.read_bytes() + b"# drift\n")
    with pytest.raises(ValueError, match="逐字节副本"):
        build_l2_candidate._inject_v3(drifted, "648")


def test_build_v3_single_window_and_overwrite_paths(tmp_path, built):
    # 单窗构建参数路径：window='600' 只建 w600（隔离 out_dir 真跑）；与默认双窗
    # 产物逐字节确定；旧产物白名单覆盖；白名单外拒绝；非法 window 参数拒绝。
    out = tmp_path / "single"
    r = build_l2_candidate.build(window="600", out_dir=out)
    assert set(r) == {"windows"} and set(r["windows"]) == {"600"}
    assert (out / "w600" / "main.py").is_file()
    assert (out / "w600" / "submission.tar.gz").is_file()
    assert (out / "w600" / "build_manifest.json").is_file()
    assert not (out / "w648").exists()  # 单窗=只建该窗
    default600 = built[0]["windows"]["600"]
    assert r["windows"]["600"]["main_sha256"] == default600["main_sha256"]
    assert r["windows"]["600"]["tar_sha256"] == default600["tar_sha256"]
    assert r["windows"]["600"]["block_sha256"] == default600["block_sha256"]

    # 旧产物=上次注入产物（其 sha 在 prev manifest → 白名单内）→ 覆盖重建成功，
    # 跨 build 逐字节确定
    r2 = build_l2_candidate.build(window="600", out_dir=out)
    assert r2 == r

    # 白名单外（现存 sha 既非基座也非上次产物）→ 拒绝覆盖，他物不被破坏
    main_p = out / "w600" / "main.py"
    tar_p = out / "w600" / "submission.tar.gz"
    main_p.write_bytes(b"tampered: not base, not prev product")
    with pytest.raises(ValueError, match="refusing to overwrite"):
        build_l2_candidate.build(window="600", out_dir=out)
    assert main_p.read_bytes() == b"tampered: not base, not prev product"
    assert hashlib.sha256(tar_p.read_bytes()).hexdigest() == default600["tar_sha256"]

    # 非法 window 参数（类型/取值面）全数拒绝且零产物
    for bad in (648, "640", "both ", None):
        with pytest.raises(ValueError):
            build_l2_candidate.build(window=bad, out_dir=tmp_path / "nowhere")
    assert not (tmp_path / "nowhere").exists()
