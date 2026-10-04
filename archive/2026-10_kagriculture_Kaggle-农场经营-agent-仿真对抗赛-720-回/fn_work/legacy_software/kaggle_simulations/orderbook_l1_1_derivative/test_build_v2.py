"""test_build_v2：make 的源级替换与 diff 恰一函数体校验 + build 收口组（R11）。

build 收口组（追加，不动上方 make 组）：
- test_build_v2_full_chain_produces_artifacts：build() 全链真跑一次（out_dir 默
  认=本目录），三件产物落盘留档=候选包本体；manifest 字段齐且与盘上真值逐项
  一致（注入 append-only 形态复核+身份链断言：基座 a16e0e9b/2838cc66 → L1 块
  2f3553fe → v2 块 sha → 双跑声明；双跑一致性在 build 函数内已断言）；
- test_build_v2_tar_rebuild_matches_disk：独立复核确定性（配方函数直调重建 tar，
  不重跑 build）；
- test_build_v2_tar_members_match_base：tar 成员==基座包同款（恰 ["main.py"]）；
- test_build_v2_inject_prewrite_guards：注入三道写入前防线（写入前即抛，零 exec）；
- test_build_v2_whitelist_overwrite：旧产物 sha 白名单覆盖路径（隔离 out_dir 真跑）。"""

import ast
import difflib
import hashlib
import json
import re
import tarfile
import time
from pathlib import Path

import pytest

import build_l11_candidate
import make_layer_s_v2_block as maker

_THIS_DIR = Path(__file__).resolve().parent
_L1_DIR = _THIS_DIR.parent / "orderbook_l1_derivative"
_L1_BLOCK = _L1_DIR / "layer_s_block.py"


def _line_span(text, lineno, end_lineno):
    """1-based 闭行区间的逐字节片段（含行尾换行）。"""
    return "".join(text.splitlines(keepends=True)[lineno - 1:end_lineno])


def test_v2_block_diff_single_function(tmp_path):
    # make() 真跑（显式 L1 路径 → tmp 产物）：v2 文件生成 + 返回契约三键。
    out = tmp_path / "layer_s_block_v2.py"
    info = maker.make(_L1_BLOCK, out)
    v2_text = out.read_text(encoding="utf-8")
    l1_text = _L1_BLOCK.read_text(encoding="utf-8")

    assert Path(info["v2_path"]) == out
    assert info["v2_sha256"] == hashlib.sha256(out.read_bytes()).hexdigest()
    audit = info["diff_audit"]
    assert audit["only_function"] == "_cxs_seed_surplus"
    l1a, l1b = audit["l1_lines"]
    v2a, v2b = audit["v2_lines"]

    # AST 校验：v2 可解析；审计行区间恰指向两版唯一的同名目标函数。
    l1_tree = ast.parse(l1_text)
    v2_tree = ast.parse(v2_text)
    l1_fns = [n for n in l1_tree.body if isinstance(n, ast.FunctionDef) and n.name == "_cxs_seed_surplus"]
    v2_fns = [n for n in v2_tree.body if isinstance(n, ast.FunctionDef) and n.name == "_cxs_seed_surplus"]
    assert len(l1_fns) == len(v2_fns) == 1
    assert (l1_fns[0].lineno, l1_fns[0].end_lineno) == (l1a, l1b)
    assert (v2_fns[0].lineno, v2_fns[0].end_lineno) == (v2a, v2b)
    # 中段恰为嵌入的替换文本（逐字节，含行尾换行）。
    assert _line_span(v2_text, v2a, v2b) == maker.V2_SURPLUS_SRC

    # 逐字节前缀/后缀恒等：目标函数区间外一切字节相同（其余函数+常数+docstring）。
    l1_lines = l1_text.splitlines(keepends=True)
    prefix = "".join(l1_lines[:l1a - 1])
    suffix = "".join(l1_lines[l1b:])
    assert v2_text.startswith(prefix)
    assert v2_text.endswith(suffix)

    # AST 级佐证：其余顶层语句逐一类型相同且源片段逐字节相同。
    def _rest(tree):
        return [n for n in tree.body
                if not (isinstance(n, ast.FunctionDef) and n.name == "_cxs_seed_surplus")]

    l1_rest, v2_rest = _rest(l1_tree), _rest(v2_tree)
    assert len(l1_rest) == len(v2_rest)
    for a, b in zip(l1_rest, v2_rest):
        assert type(a) is type(b)
        assert _line_span(l1_text, a.lineno, a.end_lineno) == _line_span(v2_text, b.lineno, b.end_lineno)

    # 逐行 diff 佐证：一切非 equal 变更行对都落在两函数行区间内（恰一处函数体）。
    sm = difflib.SequenceMatcher(None, l1_text.splitlines(), v2_text.splitlines(), autojunk=False)
    changed = [op for op in sm.get_opcodes() if op[0] != "equal"]
    assert changed, "diff 为空=替换未发生"
    for tag, i1, i2, j1, j2 in changed:
        assert l1a <= i1 + 1 and i2 <= l1b, (tag, i1, i2)
        assert v2a <= j1 + 1 and j2 <= v2b, (tag, j1, j2)

    # v2 末顶层 def 仍 _cxs_agent（AST：最后顶层 def 名）。
    top_defs = [n for n in v2_tree.body if isinstance(n, ast.FunctionDef)]
    assert top_defs[-1].name == "_cxs_agent"

    # sha 稳定 + 幂等重生成（覆盖写）：破坏产物后重跑同 sha、同内容。
    out.write_text("stale", encoding="utf-8")
    info2 = maker.make(_L1_BLOCK, out)
    assert info2["v2_sha256"] == info["v2_sha256"]
    assert out.read_text(encoding="utf-8") == v2_text

    # 缺省路径真跑：out 缺省=本目录 layer_s_block_v2.py（管线产物位），缺省 L1
    # 源定位同级 orderbook_l1_derivative/layer_s_block.py；内容与 tmp 版逐字节同。
    info3 = maker.make()
    default_out = _THIS_DIR / "layer_s_block_v2.py"
    assert Path(info3["v2_path"]) == default_out
    assert default_out.read_bytes() == out.read_bytes()
    assert info3["v2_sha256"] == info["v2_sha256"]


def test_make_fail_closed_when_target_missing(tmp_path):
    # fail-closed（契约：定位失败即抛）：L1 源定位不到目标函数 → ValueError，
    # 且不产出任何文件。
    tampered = tmp_path / "tampered_l1.py"
    tampered.write_text(
        _L1_BLOCK.read_text(encoding="utf-8").replace(
            "def _cxs_seed_surplus(", "def _cxs_seed_surplus_renamed("),
        encoding="utf-8")
    out = tmp_path / "should_not_exist.py"
    with pytest.raises(ValueError):
        maker.make(tampered, out)
    assert not out.exists()


# ---------------------------------------------------------------------------
# build 收口组（R11）：真跑一次 build_l11_candidate.build()（out_dir 默认=本目录），
# 三件产物落盘并保留（它就是候选包本体）；全文件默认目录 build 恰跑一次（耗时纪律）。

_BASE = _THIS_DIR.parent / "orderbook_derivative" / "main.py"
_BASE_TAR = _THIS_DIR.parent / "orderbook_derivative" / "submission.tar.gz"
_BASE_SHA256 = "a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab"
_BASE_TAR_SHA256 = "2838cc66e5d3f719569108fa553c9cf9acf8190d0662f8d991856560e6e9641c"
_L1_BLOCK_SHA256 = "2f3553fe4b2df6213cdc1377b2fa9299ece92506291f4ed8f547640c4e2bbfcd"
_V2_BLOCK_FILE = _THIS_DIR / "layer_s_block_v2.py"

# build 全链预算：make（AST 级）+复制+注入（含 ~1MB 整卷 exec，L1 实测亚秒级）
# +双跑打包，预算 180s。
_BUILD_BUDGET_SECONDS = 180.0

# manifest 必备键（R11 收口契约：schema/身份链输入/占位门/描述文案）。
_REQUIRED_MANIFEST_KEYS = {
    "schema", "candidate", "generated", "description",
    "main_sha256", "main_bytes", "tar_sha256", "tar_bytes",
    "block_sha256", "block_bytes", "l1_block_sha256",
    "provenance_chain", "four_gates", "h2h_vs_l1",
}


@pytest.fixture(scope="module")
def built():
    """一次性真跑 build()：返回 (manifest, elapsed_seconds)；产物留盘。"""
    t0 = time.perf_counter()
    manifest = build_l11_candidate.build()
    elapsed = time.perf_counter() - t0
    return manifest, elapsed


def test_build_v2_full_chain_produces_artifacts(built):
    # 全链实跑：三件产物落盘；manifest 字段齐且与盘上真值逐项一致；身份链完整。
    manifest, elapsed = built
    assert elapsed < _BUILD_BUDGET_SECONDS, f"build 全链超预算: {elapsed:.1f}s >= 180s"
    main_p = _THIS_DIR / "main.py"
    tar_p = _THIS_DIR / "submission.tar.gz"
    mf_p = _THIS_DIR / "build_manifest.json"
    assert main_p.is_file() and tar_p.is_file() and mf_p.is_file()
    main_bytes = main_p.read_bytes()
    assert manifest["schema"] == "orderbook_l1_1_derivative_manifest/1.0"
    assert _REQUIRED_MANIFEST_KEYS <= set(manifest)
    assert manifest["description"] == "public derivative with seed-truncation layer v2 (net-demand coverage)"
    assert manifest["main_sha256"] == hashlib.sha256(main_bytes).hexdigest()
    assert manifest["main_bytes"] == len(main_bytes)
    assert manifest["tar_sha256"] == hashlib.sha256(tar_p.read_bytes()).hexdigest()
    assert manifest["tar_bytes"] == tar_p.stat().st_size
    assert manifest["block_sha256"] == hashlib.sha256(_V2_BLOCK_FILE.read_bytes()).hexdigest()
    assert manifest["block_bytes"] == _V2_BLOCK_FILE.stat().st_size
    assert manifest["l1_block_sha256"] == _L1_BLOCK_SHA256
    # 注入形态复核：main.py == 基座全文+两空行分隔+v2 块全文（append-only）
    base_bytes = _BASE.read_bytes()
    v2_block_bytes = _V2_BLOCK_FILE.read_bytes()
    assert main_bytes == base_bytes + build_l11_candidate._SEPARATOR + v2_block_bytes
    # 盘上 manifest 文件与 build() 返回 dict 逐项一致
    assert json.loads(mf_p.read_text(encoding="utf-8")) == manifest
    # 身份链：基座 a16e0e9b/2838cc66 → L1 块 2f3553fe → v2 块 sha → 双跑声明
    # （双跑逐字节一致性已由 build 函数内断言，此处断言链文在档）+ S4 占位门。
    chain = "\n".join(manifest["provenance_chain"])
    assert _BASE_SHA256 in chain
    assert _BASE_TAR_SHA256 in chain
    assert _L1_BLOCK_SHA256 in chain
    assert manifest["block_sha256"] in chain
    assert "double-build byte-identical" in chain
    assert "pending S4" in manifest["four_gates"]
    assert "pending S4" in manifest["h2h_vs_l1"]
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", manifest["generated"])
    # 基座原件在 build 全链后仍逐字节未动（零改动纪律）
    assert hashlib.sha256(base_bytes).hexdigest() == _BASE_SHA256
    assert hashlib.sha256(_BASE_TAR.read_bytes()).hexdigest() == _BASE_TAR_SHA256


def test_build_v2_tar_rebuild_matches_disk(built):
    # 独立复核确定性：以盘上注入版 main.py 重建一次 tar（配方函数直调，不重跑
    # build），与盘上 submission.tar.gz 逐字节一致、sha 等于 manifest 记录值。
    manifest, _ = built
    rebuilt = build_l11_candidate._pack_tar_gz((_THIS_DIR / "main.py").read_bytes())
    assert rebuilt == (_THIS_DIR / "submission.tar.gz").read_bytes()
    assert hashlib.sha256(rebuilt).hexdigest() == manifest["tar_sha256"]


def test_build_v2_tar_members_match_base(built):
    # 成员清单==基座包同款：与本仓 ../orderbook_derivative/submission.tar.gz
    # 成员名逐项相同，且恰为 ["main.py"]（Kaggle 提交布局）。
    with tarfile.open(_THIS_DIR / "submission.tar.gz") as tf:
        ours = tf.getnames()
    with tarfile.open(_BASE_TAR) as tf:
        base = tf.getnames()
    assert ours == base == ["main.py"]


def test_build_v2_inject_prewrite_guards(built, tmp_path):
    # 注入三道写入前防线（全部在写入前抛出，零 exec 成本，文件零改动）。
    main_p = _THIS_DIR / "main.py"
    # 防线一：目标指向基座原件 → 拒绝（只读纪律）
    with pytest.raises(ValueError, match="refusing to inject"):
        build_l11_candidate._inject_v2(_BASE)
    # 防线二：已注入产物再注入 → 判重拒绝（sentinel/块字节，文件逐字节不变）
    before = main_p.read_bytes()
    with pytest.raises(ValueError, match="already injected"):
        build_l11_candidate._inject_v2(main_p)
    assert main_p.read_bytes() == before
    # 防线三：非基座逐字节副本（前置态漂移）→ 拒绝注入
    drifted = tmp_path / "drifted.py"
    drifted.write_bytes(_BASE.read_bytes() + b"# drift\n")
    with pytest.raises(ValueError, match="逐字节副本"):
        build_l11_candidate._inject_v2(drifted)


def test_build_v2_whitelist_overwrite(tmp_path, built):
    # 旧产物 sha 白名单覆盖路径（沿 L1；隔离 out_dir 真跑）：
    # ① 干净目录首建 → 三件产物齐；
    m1 = build_l11_candidate.build(tmp_path)
    main_p = tmp_path / "main.py"
    tar_p = tmp_path / "submission.tar.gz"
    assert main_p.is_file() and tar_p.is_file()
    assert (tmp_path / "build_manifest.json").is_file()
    # ② 旧产物=上次注入产物（其 sha 在 prev manifest → 白名单内）→ 覆盖重建成功，
    #    且跨 build 逐字节确定（main/tar sha 与首建一致、与默认目录产物一致）；
    m2 = build_l11_candidate.build(tmp_path)
    assert m2["main_sha256"] == m1["main_sha256"]
    assert m2["tar_sha256"] == m1["tar_sha256"]
    assert m1["main_sha256"] == built[0]["main_sha256"]
    assert m1["tar_sha256"] == built[0]["tar_sha256"]
    # ③ 白名单外（现存 sha 既非基座也非上次产物）→ 拒绝覆盖，他物不被破坏；
    main_p.write_bytes(b"tampered: not base, not prev product")
    with pytest.raises(ValueError, match="refusing to overwrite"):
        build_l11_candidate.build(tmp_path)
    assert main_p.read_bytes() == b"tampered: not base, not prev product"
    assert hashlib.sha256(tar_p.read_bytes()).hexdigest() == m1["tar_sha256"]
