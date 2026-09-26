# -*- coding: utf-8 -*-
"""R21 测试面：build_r38（构建组/audit 组/pack 组）。

audit 组（B23，audit_diff_vs_r37 真测试）：①正路（base+尾块→归因对，块
sha/字节数对真块）+兼容装饰差异按核心短语识别 ②白名单外差异（改前缀一行/
块外多字节）即抛 ③锚行缺失/两次出现即抛 ④同文本零差异（present=False）
⑤归因表键稳定（JSON 可序列化）。build 组（B23 构建编排）真测试五件
（集成/输入不变/审计三件套/确定性/异常面）见文件首段。

pack 组（B23，pack_r38 真测试拆六件——实现方案留档见 build_r38.pack_r38
docstring）：
①manifest 字段齐+文案原文——R16 惯例键+base_sha_chain（a16e0e9b→51fc19db
  →r37=剥块重算→r38=输入重算）+predict_block（块 sha 对真块）+
  library_sha256（canonical json sha）+complete，且返回=盘上 manifest；
②确定性双跑——同 main 两次 pack→tar 逐字节同、双跑哈希恒等、manifest 全同
  （generated 日期除外）；
③tar 内条目形态（解包断言）——单 main.py、mode644/mtime0/uid0/gid0/size、
  内层字节同输入、gzip 头 MTIME=0/FLG=0；
④区分度——不同 main→不同 main_sha256/tar_sha256；
⑤坏输入即抛——非 str（含 pathlib.Path）→TypeError、空/纯空白路径→
  ValueError、空文件/锚两次/锚前分隔畸形（非恰两换行）→ValueError、缺文件→
  FileNotFoundError；
⑥predict_block 缺件→null+complete=False（不造假）——缺锚→predict_block
  {"present": False, "bytes": 0, "sha256": None}+库 sha null+r37 链节点 null；
  块在场库解析不出→库 sha null/complete False 不造假；伴生行兜底认账。
"""
import hashlib
import io
import json
import re
import tarfile

import pytest

try:
    from orderbook_predict import build_r38 as B
except ImportError:  # 兜底：直接以 orderbook_predict/ 为 sys.path 根跑测
    import build_r38 as B


# ------------------------- build 组（B23 构建编排真测试） -------------------------
# ①编排全流程集成 ②r37 输入字节不变 ③审计三件套过（零 UNATTRIBUTED）
# ④确定性（两次 build 同 main/tar sha）⑤异常路径（缺文件/审计红不落盘）。
# 建库组件以合成迷你库桩钉（卖流库构建归 sellflow 组真测试），注入/审计/打包
# 全链真件跑。


def _mini_lib():
    """合成迷你卖流库（sellflow 建库件形态；ASCII 安全→三 sha 口径恒等）。"""
    return {
        "version": "sellflow/1.0",
        "keys": {"BAKERY|YARN_STORE||m229_w9989": {"n_episodes": 2, "hist": {
            "1": {"MILK": {"qty_sum": 9, "count": 3, "qty_max": 4}}}}},
        "global": {"n_episodes": 2, "hist": {
            "1": {"MILK": {"qty_sum": 9, "count": 3, "qty_max": 4}}}},
    }


def _sha_of(lib):
    """canonical json sha256（sellflow 建库件口径）。"""
    return hashlib.sha256(
        json.dumps(lib, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _base_main():
    """合成迷你 base（形态贴近 r37：尾部 callable 供 last-callable 捕获）。"""
    return (
        "# synthetic r37-like base（最小底版）\n"
        "X = 1\n"
        "def _base_agent(observation, configuration=None):\n"
        "    return {'farmer': ['PASS'], 'hands': [], 'market': []}\n"
        "def agent(observation, configuration=None):\n"
        "    return _base_agent(observation, configuration)\n"
    )


def _patch_lib(monkeypatch, lib):
    """钉建库组件为合成迷你库（orderbook_predict.sellflow 与脚本态别名同钉）。"""
    import sys

    def _fake_builder(replay_dir, labels=None):
        return {"library": lib,
                "build_audit": {"replay_dir": replay_dir, "n_files": 1,
                                "n_used": 1, "n_skipped": 0,
                                "total_events": 3,
                                "sha256_of_library": _sha_of(lib)}}

    try:
        from orderbook_predict import sellflow as _sf
    except ImportError:
        import sellflow as _sf
    targets = [_sf]
    _alt = sys.modules.get("sellflow")
    if _alt is not None and _alt is not _sf:
        targets.append(_alt)
    for m in targets:
        monkeypatch.setattr(m, "build_sellflow_library", _fake_builder)


def test_build_r38_pipeline(tmp_path, monkeypatch):
    # ①编排全流程集成：合成迷你库+迷你 base 走建库（桩）→注入→审计→打包真链，
    # 产物三件（main.py/submission.tar.gz/build_manifest.json）+返回形态钉死。
    lib = _mini_lib()
    _patch_lib(monkeypatch, lib)
    src = tmp_path / "r37_main.py"
    src.write_text(_base_main(), encoding="utf-8", newline="\n")
    out = tmp_path / "out"
    res = B.build_r38(str(src), out_dir=str(out))

    # 产物三件
    for name in ("main.py", "submission.tar.gz", "build_manifest.json"):
        assert (out / name).is_file()

    # 返回形态
    assert set(res) == {"main_path", "main_sha256", "tar_sha256", "manifest",
                        "diff_attribution", "block_sha", "library_sha256",
                        "build_audit", "r37_main_path", "r37_sha256"}
    raw = (out / "main.py").read_bytes()
    base = src.read_bytes()
    assert res["main_path"] == str(out / "main.py")
    assert res["r37_main_path"] == str(src)
    assert res["r37_sha256"] == hashlib.sha256(base).hexdigest()
    assert res["main_sha256"] == hashlib.sha256(raw).hexdigest()
    assert res["tar_sha256"] == hashlib.sha256(
        (out / "submission.tar.gz").read_bytes()).hexdigest()

    # manifest=盘上文件，sha 链/块 sha 与返回值互证
    m = res["manifest"]
    assert m == json.loads((out / "build_manifest.json").read_text(
        encoding="utf-8"))
    assert m["main_sha256"] == res["main_sha256"]
    assert m["tar_sha256"] == res["tar_sha256"]
    assert m["base_sha_chain"]["r37"] == hashlib.sha256(base).hexdigest()
    assert m["base_sha_chain"]["r38"] == res["main_sha256"]

    # main=base 逐字节前缀+尾部恰一预测块（block_sha 对真块字节）
    assert raw.startswith(base)
    tail = raw[len(base):]
    assert res["block_sha"] == hashlib.sha256(tail).hexdigest()
    assert m["predict_block"] == {"present": True, "bytes": len(tail),
                                  "sha256": res["block_sha"]}
    assert base.decode("utf-8").count(_CORE) == 0
    assert raw.decode("utf-8").count(_CORE) == 1

    # 库 sha 三件套对账（build_audit 记录==pack 自证==canonical 重算）
    assert res["library_sha256"] == _sha_of(lib) == m["library_sha256"]
    assert res["build_audit"]["sha256_of_library"] == res["library_sha256"]
    assert m["complete"] is True


def test_build_r38_input_bytes_unchanged(tmp_path, monkeypatch):
    # ②r37 输入字节不变：编排只读输入、全程零写回（含真跑段）。
    _patch_lib(monkeypatch, _mini_lib())
    src = tmp_path / "r37_main.py"
    src.write_text(_base_main(), encoding="utf-8", newline="\n")
    before = src.read_bytes()
    B.build_r38(str(src), out_dir=str(tmp_path / "out"))
    assert src.read_bytes() == before


def test_build_r38_audit_attribution(tmp_path, monkeypatch):
    # ③审计三件套过：归因表 ok/whitelist/unattributed 三键、零 UNATTRIBUTED，
    # 块 sha 在 inject/audit/pack 三件同口径互证。
    _patch_lib(monkeypatch, _mini_lib())
    src = tmp_path / "r37_main.py"
    src.write_text(_base_main(), encoding="utf-8", newline="\n")
    res = B.build_r38(str(src), out_dir=str(tmp_path / "out"))
    att = res["diff_attribution"]
    assert set(att) == {"ok", "whitelist", "unattributed"}
    assert att["ok"] is True and att["unattributed"] == []
    assert set(att["whitelist"]) == {"predict_block"}
    pb = att["whitelist"]["predict_block"]
    assert pb["present"] is True
    assert pb["sha256"] == res["block_sha"]
    assert pb["sha256"] == res["manifest"]["predict_block"]["sha256"]
    assert pb["bytes"] == res["manifest"]["predict_block"]["bytes"] > 0
    assert json.loads(json.dumps(att, ensure_ascii=False)) == att


def test_build_r38_deterministic_two_runs(tmp_path, monkeypatch):
    # ④确定性：同输入两次 build→同 main/tar sha、tar 逐字节同；manifest 全同
    # （generated 日期除外）。
    _patch_lib(monkeypatch, _mini_lib())
    src = tmp_path / "r37_main.py"
    src.write_text(_base_main(), encoding="utf-8", newline="\n")
    r1 = B.build_r38(str(src), out_dir=str(tmp_path / "o1"))
    r2 = B.build_r38(str(src), out_dir=str(tmp_path / "o2"))
    assert r1["main_sha256"] == r2["main_sha256"]
    assert r1["tar_sha256"] == r2["tar_sha256"]
    assert r1["block_sha"] == r2["block_sha"]
    assert r1["library_sha256"] == r2["library_sha256"]
    t1 = (tmp_path / "o1" / "submission.tar.gz").read_bytes()
    t2 = (tmp_path / "o2" / "submission.tar.gz").read_bytes()
    assert t1 == t2
    assert (tmp_path / "o1" / "main.py").read_bytes() == \
        (tmp_path / "o2" / "main.py").read_bytes()
    g1, g2 = dict(r1["manifest"]), dict(r2["manifest"])
    g1.pop("generated")
    g2.pop("generated")
    assert g1 == g2


def test_build_r38_failure_surfaces(tmp_path, monkeypatch):
    # ⑤异常路径：缺文件/空文件/坏参数即抛且 out 目录零触碰；审计红（底版权含
    # 块锚核心短语→anchor_in_base 超白名单）即抛且不落半成品。
    out = tmp_path / "out"
    with pytest.raises(FileNotFoundError):
        B.build_r38(str(tmp_path / "missing.py"), out_dir=str(out))
    assert not out.exists()
    with pytest.raises(TypeError):
        B.build_r38(None, out_dir=str(out))
    with pytest.raises(TypeError):
        B.build_r38(str(tmp_path / "x.py"), out_dir=tmp_path)   # out_dir 非 str
    with pytest.raises(ValueError):
        B.build_r38("", out_dir=str(out))
    with pytest.raises(ValueError):
        B.build_r38("  \n\t", out_dir=str(out))
    empty = tmp_path / "empty.py"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        B.build_r38(str(empty), out_dir=str(out))
    assert not out.exists()                              # 预检红零触碰 out

    _patch_lib(monkeypatch, _mini_lib())
    poisoned = tmp_path / "poisoned.py"
    poisoned.write_text("# 注释含 " + _CORE + " 占位（模拟白名单外残留）\n"
                        + _base_main(), encoding="utf-8", newline="\n")
    with pytest.raises(ValueError, match="anchor_in_base"):
        B.build_r38(str(poisoned), out_dir=str(out))
    assert not out.exists()                              # 审计红不落盘
    # 注入红（库 sha 对账红）同样不落盘：改库一字节而建库记录 sha 不动
    bad_lib = _mini_lib()
    bad_lib = json.loads(json.dumps(bad_lib))
    bad_lib["keys"]["BAKERY|YARN_STORE||m229_w9989"]["hist"]["1"]["MILK"]["qty_sum"] = 8

    def _lying_builder(replay_dir, labels=None):
        return {"library": bad_lib,
                "build_audit": {"replay_dir": replay_dir,
                                "sha256_of_library": _sha_of(_mini_lib())}}
    try:
        from orderbook_predict import sellflow as _sf
    except ImportError:
        import sellflow as _sf
    monkeypatch.setattr(_sf, "build_sellflow_library", _lying_builder)
    clean = tmp_path / "clean.py"
    clean.write_text(_base_main(), encoding="utf-8", newline="\n")
    with pytest.raises(RuntimeError, match="库sha对账红"):
        B.build_r38(str(clean), out_dir=str(out))
    assert not out.exists()                              # 注入红不落盘


# audit 组共享夹具（最小真实 base+预测尾块文本对：真锚行+内嵌库数据）
_CORE = "r38 对手预测尾块"
_ANCHOR = "# ============ r38 对手预测尾块（自动生成，勿手改） ============"


def _mk_audit_pair():
    """构造 audit 组共享 (base, r38, block, block_sha)：最小真实文本对+真块 sha。

    base=最小底版（含磁带区占位行——前缀性质直接覆盖磁带区零改动）；
    block=预测尾块（B17 追加载荷形态：前置两空行分隔+锚行+内嵌库数据）；
    block_sha=尾部块字节 sha（=audit predict_block.sha256 口径）。
    """
    base = (
        "# base r37 main（最小底版）\n"
        "X = 1\n"
        "TAPE = \"R108_DATA:tape-payload\"\n"
        "def _base_agent(observation):\n"
        "    return {}\n"
    )
    block = (
        "\n\n"
        + _ANCHOR + "\n"
        + "_PREDICT_LIBRARY = {\"k\": [1, 2, 3]}\n"
        + "def _predict_agent(observation):\n"
        + "    return {}\n"
    )
    r38 = base + block
    block_sha = hashlib.sha256(block.encode("utf-8")).hexdigest()
    return base, r38, block, block_sha


@pytest.mark.parametrize("case", [
    "all_attributed",      # ①正路：base+尾块→归因对（sha/bytes 对真块）
    "decorated_anchor",    # ①兼容装饰差异：锚行 === 装饰不同按核心短语识别
    "prefix_line_changed", # ②白名单外差异（改前缀一行）即抛
    "outside_block_bytes", # ②白名单外差异（块外多字节）即抛
    "anchor_missing",      # ③锚行缺失即抛
    "anchor_twice",        # ③锚行两次出现即抛
    "identical",           # ④同文本零差异（present=False）
    "keys_stable",         # ⑤归因表键稳定（JSON 可序列化）
])
def test_audit_diff_vs_r37(case, tmp_path):
    # 真测试：构造 base+预测尾块文本对（真锚行+内嵌库数据）；audit 只抛不改，
    # 归因表可直接进 manifest。

    def _w(name, text):
        p = tmp_path / name
        p.write_text(text, encoding="utf-8", newline="\n")
        return str(p)

    base, r38, block, block_sha = _mk_audit_pair()

    if case == "all_attributed":
        m = B.audit_diff_vs_r37(_w("r38.py", r38), _w("r37.py", base))
        assert m["ok"] is True and m["unattributed"] == []
        pb = m["whitelist"]["predict_block"]
        assert pb["present"] is True and pb["sha256"] == block_sha
        assert pb["bytes"] == len(block.encode("utf-8")) > 0
    elif case == "decorated_anchor":
        # 兼容装饰差异按核心短语识别：锚行 === 装饰不同（含前置单空行分隔）
        # 同样归因 predict_block，sha 对尾部块字节。
        deco_block = (
            "\n"
            + "# ====== " + _CORE + "（自动生成，勿手改） ==\n"
            + "_PREDICT_LIBRARY = {}\n"
        )
        good = base + deco_block
        m = B.audit_diff_vs_r37(_w("r38d.py", good), _w("r37.py", base))
        assert m["ok"] is True and m["unattributed"] == []
        pb = m["whitelist"]["predict_block"]
        assert pb["present"] is True
        assert pb["sha256"] == hashlib.sha256(
            deco_block.encode("utf-8")).hexdigest()
    elif case == "prefix_line_changed":
        bad = r38.replace("X = 1", "X = 0")
        assert bad != r38
        with pytest.raises(ValueError, match="首条未归因：前缀"):
            B.audit_diff_vs_r37(_w("bad.py", bad), _w("r37.py", base))
    elif case == "outside_block_bytes":
        # 块外多字节①：追加区锚行前多出非分隔字节（尾部但不在块内）即抛。
        bad_tail = base + "# stray\n" + block
        assert bad_tail != r38
        with pytest.raises(ValueError, match="首条未归因：尾部追加区"):
            B.audit_diff_vs_r37(_w("bad1.py", bad_tail), _w("r37.py", base))
        # 块外多字节②：前缀区中段插字节（块外任何字节变）即抛。
        k = len(base) // 2
        bad_splice = r38[:k] + "### extra bytes ###\n" + r38[k:]
        assert bad_splice != r38
        with pytest.raises(ValueError, match="首条未归因：前缀"):
            B.audit_diff_vs_r37(_w("bad2.py", bad_splice), _w("r37.py", base))
    elif case == "anchor_missing":
        bad = base + "\n\n# 普通尾注\n_PREDICT_LIBRARY = {}\n"
        assert _CORE not in bad
        with pytest.raises(ValueError, match="anchor_missing"):
            B.audit_diff_vs_r37(_w("bad.py", bad), _w("r37.py", base))
    elif case == "anchor_twice":
        bad = r38 + _ANCHOR + "\n"
        assert bad.count(_CORE) == 2
        with pytest.raises(ValueError, match="anchor_duplicate"):
            B.audit_diff_vs_r37(_w("bad.py", bad), _w("r37.py", base))
    elif case == "identical":
        m = B.audit_diff_vs_r37(_w("same.py", base), _w("r37.py", base))
        assert m["ok"] is True and m["unattributed"] == []
        assert m["whitelist"]["predict_block"] == {"present": False,
                                                   "bytes": 0, "sha256": None}
    elif case == "keys_stable":
        m = B.audit_diff_vs_r37(_w("r38.py", r38), _w("r37.py", base))
        assert set(m) == {"ok", "whitelist", "unattributed"}
        assert set(m["whitelist"]) == {"predict_block"}
        assert set(m["whitelist"]["predict_block"]) == {"present", "bytes",
                                                        "sha256"}
        assert json.loads(json.dumps(m, ensure_ascii=False)) == m


# ---------------------------------------------------------------------------
# pack 组夹具（合成 r38 main：底版+B17 追加载荷形态预测尾块，真锚行+内嵌库）
# ---------------------------------------------------------------------------
_LIB = {"version": "r38lib",
        "keys": {"EARLY||m0_w0": {"n_episodes": 3,
                                  "hist": {"0": {"MILK": {"qty_sum": 6,
                                                          "count": 2,
                                                          "qty_max": 4}}}}},
        "global": {"0": {"WOOL": {"qty_sum": 1, "count": 1, "qty_max": 1}}}}
_BASE = (
    "# base r37 main（最小底版）\n"
    "X = 1\n"
    "def _base_agent(observation):\n"
    "    return {}\n"
)


def _canon_sha(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, ensure_ascii=False,
                   separators=(",", ":")).encode("utf-8")).hexdigest()


def _mk_main(tmp_path, name="main.py", base=_BASE, lib_repr=repr(_LIB),
             marker=None, gap="\n"):
    body = _ANCHOR + "\n"
    if lib_repr is not None:
        body += "_PREDICT_LIBRARY = " + lib_repr + "\n"
    body += "def _predict_agent(observation):\n    return {}\n"
    if marker is not None:
        body += marker + "\n"
    p = tmp_path / name
    p.write_text(base + gap + body, encoding="utf-8", newline="\n")
    return p


def test_pack_r38(tmp_path):
    # ①manifest 字段齐+文案原文：R16 惯例键+sha 链+预测块 sha+库 sha+complete，
    # 返回=盘上 build_manifest.json。
    main = _mk_main(tmp_path)
    out = tmp_path / "out"
    m = B.pack_r38(str(main), out_dir=str(out))
    assert m == json.loads((out / "build_manifest.json").read_text(encoding="utf-8"))
    assert set(m) == {
        "schema", "generated", "variant", "description", "main_sha256",
        "main_bytes", "tar_sha256", "tar_bytes", "tar_members",
        "double_run_sha256", "base_sha_chain", "predict_block",
        "library_sha256", "complete"}
    assert m["schema"] == "orderbook_r38_manifest/1.0"
    assert m["variant"] == "r38"
    assert m["description"] == ("public derivative with opponent sell "
                                "prediction (front-run + dodge)")
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", m["generated"])
    raw = main.read_bytes()
    assert m["main_sha256"] == hashlib.sha256(raw).hexdigest()
    assert m["main_bytes"] == len(raw)
    assert m["tar_members"] == ["main.py"]
    assert m["tar_bytes"] == (out / "submission.tar.gz").stat().st_size
    assert m["tar_sha256"] == hashlib.sha256(
        (out / "submission.tar.gz").read_bytes()).hexdigest()
    assert m["double_run_sha256"] == {"run1": m["tar_sha256"],
                                      "run2": m["tar_sha256"]}
    chain = m["base_sha_chain"]
    assert set(chain) == {"a16e0e9b", "r34a", "r37", "r38"}
    assert chain["a16e0e9b"] == ("a16e0e9b40c489972630a0b9d04f30e9c1cab031"
                                 "59fa78676db74277d84d82ab")
    assert chain["r34a"] == ("51fc19dba2d0bcbf2d0a3720c26ff318541a0e6c"
                             "e5800873bc863f612451aa5b")
    assert chain["r38"] == m["main_sha256"]
    idx = raw.index(_ANCHOR.encode("utf-8")) - 2
    block = raw[idx:]
    assert m["predict_block"] == {"present": True, "bytes": len(block),
                                  "sha256": hashlib.sha256(block).hexdigest()}
    assert chain["r37"] == hashlib.sha256(raw[:idx]).hexdigest()
    assert m["library_sha256"] == _canon_sha(_LIB)
    assert m["complete"] is True


def test_pack_r38_deterministic_double_run(tmp_path):
    # ②确定性双跑：同 main 两次 pack→同 tar 字节/同 sha；manifest 全同（generated 除外）。
    main = _mk_main(tmp_path)
    m1 = B.pack_r38(str(main), out_dir=str(tmp_path / "out_a"))
    m2 = B.pack_r38(str(main), out_dir=str(tmp_path / "out_b"))
    tar_a = (tmp_path / "out_a" / "submission.tar.gz").read_bytes()
    tar_b = (tmp_path / "out_b" / "submission.tar.gz").read_bytes()
    assert tar_a == tar_b
    assert m1["tar_sha256"] == m2["tar_sha256"] == hashlib.sha256(tar_a).hexdigest()
    assert m1["double_run_sha256"]["run1"] == m1["double_run_sha256"]["run2"]
    g1, g2 = dict(m1), dict(m2)
    g1.pop("generated")
    g2.pop("generated")
    assert g1 == g2


def test_pack_r38_tar_shape(tmp_path):
    # ③tar 内条目形态（解包断言）：单 main.py、mode644/mtime0/uid0/gid0、内层同输入、gzip 头 mtime0。
    main = _mk_main(tmp_path)
    out = tmp_path / "out"
    B.pack_r38(str(main), out_dir=str(out))
    raw = (out / "submission.tar.gz").read_bytes()
    assert raw[:2] == b"\x1f\x8b" and raw[3] == 0      # gzip 头 FLG=0（无 FNAME）
    assert raw[4:8] == b"\x00\x00\x00\x00"             # gzip MTIME=0
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        members = tar.getmembers()
        assert [mem.name for mem in members] == ["main.py"]
        info = members[0]
        assert info.isfile() and info.mode == 0o644
        assert info.mtime == 0 and info.uid == 0 and info.gid == 0
        assert info.size == main.stat().st_size
        assert tar.extractfile("main.py").read() == main.read_bytes()


def test_pack_r38_distinct_mains_distinct_sha(tmp_path):
    # ④区分度：不同 main→不同 main_sha256/tar_sha256。
    main_a = _mk_main(tmp_path, name="a.py")
    main_b = _mk_main(tmp_path, name="b.py", base=_BASE + "Y = 2\n")
    m1 = B.pack_r38(str(main_a), out_dir=str(tmp_path / "o1"))
    m2 = B.pack_r38(str(main_b), out_dir=str(tmp_path / "o2"))
    assert m1["main_sha256"] != m2["main_sha256"]
    assert m1["tar_sha256"] != m2["tar_sha256"]


def test_pack_r38_bad_input_raises(tmp_path):
    # ⑤坏输入即抛：非 str→TypeError；空路径/空文件/锚两次/分隔畸形→ValueError；
    # 缺文件→FileNotFoundError。
    with pytest.raises(TypeError):
        B.pack_r38(None, out_dir=str(tmp_path))
    with pytest.raises(TypeError):
        B.pack_r38(b"main.py", out_dir=str(tmp_path))
    with pytest.raises(TypeError):
        B.pack_r38(42, out_dir=str(tmp_path))
    with pytest.raises(TypeError):
        B.pack_r38(tmp_path / "main.py", out_dir=str(tmp_path))  # pathlib.Path 非 str
    with pytest.raises(ValueError):
        B.pack_r38("", out_dir=str(tmp_path))
    with pytest.raises(ValueError):
        B.pack_r38("   \n\t", out_dir=str(tmp_path))
    with pytest.raises(FileNotFoundError):
        B.pack_r38(str(tmp_path / "missing.py"), out_dir=str(tmp_path))
    empty = tmp_path / "empty.py"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        B.pack_r38(str(empty), out_dir=str(tmp_path))
    dup = _mk_main(tmp_path, name="dup.py")
    dup.write_text(dup.read_text(encoding="utf-8") + _ANCHOR + "\n",
                   encoding="utf-8", newline="\n")
    with pytest.raises(ValueError):
        B.pack_r38(str(dup), out_dir=str(tmp_path))
    tight = _mk_main(tmp_path, name="tight.py", gap="")   # 锚前非恰两换行
    with pytest.raises(ValueError):
        B.pack_r38(str(tight), out_dir=str(tmp_path))
    head = _mk_main(tmp_path, name="head.py", base="", gap="")  # 锚行顶文件头
    with pytest.raises(ValueError):
        B.pack_r38(str(head), out_dir=str(tmp_path))


def test_pack_r38_predict_block_missing(tmp_path):
    # ⑥缺件→null+complete=False（不造假）；库解析不出同样记 null；伴生行兜底认账。
    plain = tmp_path / "plain.py"
    plain.write_text(_BASE, encoding="utf-8", newline="\n")
    m0 = B.pack_r38(str(plain), out_dir=str(tmp_path / "o0"))
    assert m0["predict_block"] == {"present": False, "bytes": 0,
                                   "sha256": None}
    assert m0["library_sha256"] is None
    assert m0["base_sha_chain"]["r37"] is None
    assert m0["base_sha_chain"]["r38"] == m0["main_sha256"]
    assert m0["complete"] is False
    assert (tmp_path / "o0" / "submission.tar.gz").exists()   # 缺件不阻断出包
    # 块在场但 _PREDICT_LIBRARY 解析不出→库 sha null、complete False 不造假
    nolib = _mk_main(tmp_path, name="nolib.py", lib_repr="build_library()")
    raw = nolib.read_bytes()
    idx = raw.index(_ANCHOR.encode("utf-8")) - 2
    m1 = B.pack_r38(str(nolib), out_dir=str(tmp_path / "o1"))
    assert m1["predict_block"]["present"] is True
    assert m1["predict_block"]["sha256"] == hashlib.sha256(raw[idx:]).hexdigest()
    assert m1["library_sha256"] is None
    assert m1["base_sha_chain"]["r37"] == hashlib.sha256(raw[:idx]).hexdigest()
    assert m1["complete"] is False
    # 伴生 manifest 行兜底：块文本解析不出→「# R38_LIBRARY_SHA256: <hex>」认账
    mark = "# R38_LIBRARY_SHA256: " + _canon_sha(_LIB)
    m2 = B.pack_r38(str(_mk_main(tmp_path, name="mark.py",
                                 lib_repr="build_library()", marker=mark)),
                    out_dir=str(tmp_path / "o2"))
    assert m2["library_sha256"] == _canon_sha(_LIB)
    assert m2["complete"] is True
