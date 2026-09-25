# -*- coding: utf-8 -*-
"""R19/R20 测试面：build_r37（构建组/audit 组/pack 组）。

pack 组（B18，pack_r37 真测试拆八件——三件 sha 方案留档见
build_r37.pack_r37 docstring）：
①确定性双跑——同 main 两次 pack→tar 逐字节同、双跑哈希恒等、manifest 全同
  （generated 日期除外）；
②manifest 字段齐——R16 惯例键+base_sha_chain（a16e0e9b→r34a→r37，链节点对
  盘上真值核对）+whitelist_shas 三件+double_run_sha256+描述文案原文断言，
  且嵌入变更表 JSON 空白/键序不敏感（canonical sha）；
③tar 内条目形态（解包断言）——单 main.py、mode644/mtime0/uid0/gid0/size、
  内层字节同输入、gzip 头 MTIME=0/FLG=0；
④区分度——不同 main→不同 main_sha256/tar_sha256；
⑤坏输入即抛——非 str（含 pathlib.Path）→TypeError、空/纯空白路径→
  ValueError、空文件/重复变更表标记/坏 JSON/锚畸形→ValueError、缺文件→
  FileNotFoundError；
⑥错误契约——双跑不一致→RuntimeError（monkeypatch 配方源）且产物不落盘；
⑦三件 sha 尽力自证——缺件→null 不造假（whitelist_shas_complete=False），
  仅守卫块在场→半填；
⑧签名微调登记钉——首参 r37_main、out_dir 可选默认 None。
build/audit 组属 B18 其余子任务，本文件不动。
"""
import hashlib
import io
import json
import re
import tarfile

import pytest

try:
    from orderbook_r37 import build_r37 as B
except ImportError:  # 兜底：直接以 orderbook_r37/ 为 sys.path 根跑测
    import build_r37 as B

try:
    from orderbook_r37 import inject_guard
except ImportError:
    import inject_guard


def test_build_r37(tmp_path, monkeypatch):
    # build 组真测试（①-⑥）：合成 mini-main 真跑五组件编排；r34a 输入零改动；
    # 变更表注释 pack 自证；审计归因三类零 UNATTRIBUTED；确定性双跑；
    # 异常路径（缺文件/审计红）不落半成品。
    import copy

    try:
        from orderbook_r37 import retape_sheep as _rs
        from orderbook_r37 import retape_tail as _rt
    except ImportError:  # 兜底：直接以 orderbook_r37/ 为 sys.path 根跑测
        import retape_sheep as _rs
        import retape_tail as _rt

    marker_sheep = "# R37_SHEEP_CHANGE_TABLE:"
    marker_tail = "# R37_TAIL_REMOVAL_LIST:"

    def _mk_tape():
        # 迷你磁带（719 步单路由）：羊批 264 达标 no-op + 288 晚批前移 288→200
        # （供资卖单 200）；剪毛五轮 d6/9/12/15/18 过②核算；尾盘 CARE@672、
        # FEED@696、闲置 HIRE@700 三类删除素材。
        steps = 719
        mk = {s: [] for s in range(steps)}
        mk[200].append(["SELL", "WOOL", 3])
        mk[264].append(["BUY_ANIMAL", "SHEEP", 1])
        mk[288].append(["BUY_ANIMAL", "SHEEP", 2])
        mk[700].append(["HIRE"])
        fm = {s: ["PASS"] for s in range(steps)}
        for d in (6, 9, 12, 15, 18):
            fm[d * 24] = ["HARVEST"]
            fm[d * 24 + 1] = ["PLACE", "WOOL", 1]
        fm[672] = ["CARE"]
        fm[696] = ["FEED"]
        actions = [{"farmer": fm[s], "hands": [], "market": mk[s]}
                   for s in range(steps)]
        return {"actions": actions, "routes": {"0": list(range(steps))},
                "shops": []}

    base_text = ("import base64, json, zlib\nX = 1\n"
                 "_R108_DATA=json.loads(zlib.decompress("
                 "base64.b85decode('PLACEHOLDER')))\nY = 2\n")
    r34_text = _rs._encode_routes(base_text, _mk_tape())
    r34 = tmp_path / "r34a_main.py"
    r34.write_text(r34_text, encoding="utf-8", newline="\n")
    r34_before = r34.read_bytes()

    def _assert_clean(out):
        assert not (out / "main.py").exists()
        assert not (out / "submission.tar.gz").exists()
        assert not (out / "build_manifest.json").exists()

    # ---- ① 编排全流程集成：五组件真跑，产物三件齐全 ----
    out = tmp_path / "build"
    res = B.build_r37(str(r34), out_dir=str(out))
    for name in ("main.py", "submission.tar.gz", "build_manifest.json"):
        assert (out / name).is_file()
    assert set(res) == {"main_path", "main_sha256", "tar_sha256", "manifest",
                        "diff_attribution", "block_sha", "sheep_change_table",
                        "tail_removal_list", "r34a_main_path", "r34a_sha256"}
    assert res["main_path"] == str(out / "main.py")
    assert res["main_sha256"] == hashlib.sha256(
        (out / "main.py").read_bytes()).hexdigest()
    assert res["tar_sha256"] == hashlib.sha256(
        (out / "submission.tar.gz").read_bytes()).hexdigest()
    main_text = (out / "main.py").read_text(encoding="utf-8")
    assert main_text.count(_GUARD_TITLE) == 1          # 锚行形态与 inject 同款
    assert "def _r37_agent(observation):" in main_text

    # ---- ② r34a 输入字节不变 ----
    assert r34.read_bytes() == r34_before
    assert res["r34a_sha256"] == hashlib.sha256(r34_before).hexdigest()

    # ---- ③ 变更表注释可被 pack 自证（canonical sha 对账） ----
    manifest = res["manifest"]
    assert manifest["whitelist_shas_complete"] is True
    assert all(v is not None for v in manifest["whitelist_shas"].values())
    assert manifest["whitelist_shas"]["guard_block"] == res["block_sha"]
    lines_s = [ln for ln in main_text.splitlines()
               if ln.startswith(marker_sheep)]
    lines_t = [ln for ln in main_text.splitlines() if ln.startswith(marker_tail)]
    assert len(lines_s) == 1 and len(lines_t) == 1     # 恰一行单行 JSON 注释
    sheep_rows = json.loads(lines_s[0][len(marker_sheep):])
    tail_rows = json.loads(lines_t[0][len(marker_tail):])
    assert sheep_rows == res["sheep_change_table"]
    assert tail_rows == res["tail_removal_list"]
    assert lines_s[0][len(marker_sheep):].strip() == _canon(sheep_rows)
    assert lines_t[0][len(marker_tail):].strip() == _canon(tail_rows)
    assert manifest["whitelist_shas"]["sheep_change_table"] == _table_sha(
        sheep_rows)
    assert manifest["whitelist_shas"]["tail_removal_list"] == _table_sha(
        tail_rows)
    # 五组件真跑语义钉：羊批 264 no-op + 288→200 前移；尾盘 CARE/FEED/HIRE 删
    assert [(r["route"], r["kind"], r["from_step"], r["to_step"])
            for r in sheep_rows] \
        == [("0", "no-op", 264, 264), ("0", "buy_move", 288, 200)]
    assert [(e["step"], e["kind"], e["unit"], e["slot"]) for e in tail_rows] \
        == [(672, "CARE", "F", None), (696, "FEED", "F", None),
            (700, "HIRE", None, 0)]

    # ---- ④ 审计归因三类零 UNATTRIBUTED ----
    att = res["diff_attribution"]
    assert att["ok"] is True and att["unattributed"] == []
    wl = att["whitelist"]
    assert wl["tail_guard_block"]["present"] is True \
        and wl["tail_guard_block"]["bytes"] > 0
    assert wl["sheep_retiming"]["present"] is True \
        and wl["sheep_retiming"]["n_moves"] == 1
    assert wl["tail_savings"]["present"] is True \
        and wl["tail_savings"]["n_removed"] == 3
    assert json.loads(json.dumps(att, ensure_ascii=False)) == att

    # ---- ⑤ 确定性：两次 build 同 main sha + 同 tar sha（逐字节同） ----
    out_b = tmp_path / "build_b"
    res_b = B.build_r37(str(r34), out_dir=str(out_b))
    assert res_b["main_sha256"] == res["main_sha256"]
    assert res_b["tar_sha256"] == res["tar_sha256"]
    assert (out_b / "main.py").read_bytes() == (out / "main.py").read_bytes()
    assert (out_b / "submission.tar.gz").read_bytes() \
        == (out / "submission.tar.gz").read_bytes()

    # ---- ⑥ 异常路径（缺文件/审计红）不落半成品 ----
    out_missing = tmp_path / "build_missing"
    with pytest.raises(FileNotFoundError):
        B.build_r37(str(tmp_path / "nope.py"), out_dir=str(out_missing))
    _assert_clean(out_missing)

    # 审计红（白名单外 diff）：手术件夹带 SELL 量私货→超白名单即抛
    orig_tail = _rt.retape_tail_savings

    def _rogue_tail(tape_routes):
        outp = orig_tail(copy.deepcopy(tape_routes))
        live = outp["routes"]["actions"][outp["routes"]["routes"]["0"][200]]
        live["market"][0][2] = 99        # SELL WOOL 3→99：白名单外改动
        return outp

    monkeypatch.setattr(_rt, "retape_tail_savings", _rogue_tail)
    out_red = tmp_path / "build_red"
    with pytest.raises(ValueError, match="白名单外差异"):
        B.build_r37(str(r34), out_dir=str(out_red))
    _assert_clean(out_red)


@pytest.mark.parametrize("case", [
    "all_attributed",       # ①三类全归因正路
    "outside_blob_line",    # ②白名单外差异（blob 区外一行）即抛
    "broken_prefix",        # ③前缀破坏（改原文字节）即抛
    "identical",            # ④同文本=零归因 ok
    "keys_stable",          # ⑤归因表键稳定
    "in_blob_unclassified", # 白名单外差异（blob 内非白名单改动）即抛
    "decode_failure",       # blob 解码失败按无法归因红
])
def test_audit_diff_vs_r34a(case, tmp_path):
    # 真测试：构造文本+真编解码（retape_sheep._encode_routes）+真守卫块
    # （inject_guard）；audit 只抛不改，归因表可直接进 manifest。
    from pathlib import Path

    def _w(name, text):
        p = tmp_path / name
        p.write_text(text, encoding="utf-8", newline="\n")
        return str(p)

    base34, r37, block_sha = _mk_audit_pair()

    if case == "all_attributed":
        m = B.audit_diff_vs_r34a(_w("r37.py", r37), _w("r34a.py", base34))
        assert m["ok"] is True and m["unattributed"] == []
        tb = m["whitelist"]["tail_guard_block"]
        assert tb["present"] is True and tb["sha256"] == block_sha \
            and tb["bytes"] > 0
        sh = m["whitelist"]["sheep_retiming"]
        assert sh["present"] is True and sh["n_moves"] == 1
        assert sh["moves"] == [{"order": ["BUY_ANIMAL", "SHEEP", 2],
                                "from": [["0", 1, 1]], "to": [["0", 2, 1]]}]
        ts = m["whitelist"]["tail_savings"]
        assert ts["present"] is True and ts["n_removed"] == 3
        assert {r["kind"] for r in ts["removed"]} == {"CARE", "FEED", "HIRE"}
    elif case == "outside_blob_line":
        bad = r37.replace("Y = 2", "Y = 3")
        assert bad != r37
        with pytest.raises(ValueError, match="首条未归因：行文本"):
            B.audit_diff_vs_r34a(_w("bad.py", bad), _w("r34a.py", base34))
    elif case == "broken_prefix":
        bad = r37.replace("X = 1", "X = 0")
        assert bad != r37
        with pytest.raises(ValueError, match="首条未归因：行文本"):
            B.audit_diff_vs_r34a(_w("bad.py", bad), _w("r34a.py", base34))
    elif case == "identical":
        m = B.audit_diff_vs_r34a(_w("same.py", base34), _w("r34a.py", base34))
        assert m["ok"] is True and m["unattributed"] == []
        assert all(not v["present"] for v in m["whitelist"].values())
    elif case == "keys_stable":
        m = B.audit_diff_vs_r34a(_w("r37.py", r37), _w("r34a.py", base34))
        assert set(m) == {"ok", "whitelist", "unattributed"}
        assert set(m["whitelist"]) == {"tail_guard_block", "sheep_retiming",
                                       "tail_savings"}
        assert set(m["whitelist"]["tail_guard_block"]) == {
            "present", "bytes", "sha256"}
        assert set(m["whitelist"]["sheep_retiming"]) == {
            "present", "n_moves", "moves"}
        assert set(m["whitelist"]["tail_savings"]) == {
            "present", "n_removed", "removed"}
        assert json.loads(json.dumps(m, ensure_ascii=False)) == m
    elif case == "in_blob_unclassified":
        try:
            from orderbook_r37 import retape_sheep
        except ImportError:
            import retape_sheep
        pkg = retape_sheep._decode_routes(base34)
        pkg["actions"][1]["market"][0][2] = 99     # 改 SELL 量：非白名单
        bad = retape_sheep._encode_routes(base34, pkg)
        with pytest.raises(ValueError, match="action_delta_unclassified"):
            B.audit_diff_vs_r34a(_w("bad.py", bad), _w("r34a.py", base34))
    elif case == "decode_failure":
        try:
            from orderbook_r37 import retape_sheep
        except ImportError:
            import retape_sheep
        bad = retape_sheep._BLOB_RE.sub(
            lambda mo: mo.group(0).replace(mo.group(1), "AAAA"), base34)
        assert bad != base34
        with pytest.raises(ValueError, match="blob_decode_failure"):
            B.audit_diff_vs_r34a(_w("bad.py", bad), _w("r34a.py", base34))


def test_pack_r37(tmp_path):
    # ②manifest 字段齐（核心正路）：R16 惯例键+sha 链+三件 sha+双跑哈希+文案原文。
    from pathlib import Path

    main = _write_main(tmp_path)
    out = tmp_path / "out"
    m = B.pack_r37(str(main), out_dir=str(out))
    assert m == json.loads((out / "build_manifest.json").read_text(encoding="utf-8"))
    assert set(m) == {
        "schema", "generated", "variant", "description", "main_sha256",
        "main_bytes", "tar_sha256", "tar_bytes", "tar_members",
        "tar_rebuild_reproducible", "tar_size_ok", "base_sha_chain",
        "whitelist_shas", "whitelist_shas_complete", "double_run_sha256"}
    assert m["schema"] == "orderbook_r37_manifest/1.0"
    assert m["variant"] == "r37"
    assert m["description"] == ("public derivative with cash-floor guard "
                                "and earlier flock schedule")
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", m["generated"])
    main_bytes = main.read_bytes()
    assert m["main_sha256"] == hashlib.sha256(main_bytes).hexdigest()
    assert m["main_bytes"] == len(main_bytes)
    assert m["tar_members"] == ["main.py"]
    assert m["tar_rebuild_reproducible"] is True
    assert m["tar_size_ok"] is True
    assert m["tar_bytes"] == (out / "submission.tar.gz").stat().st_size
    assert m["tar_sha256"] == hashlib.sha256(
        (out / "submission.tar.gz").read_bytes()).hexdigest()
    # 双跑哈希：run1==run2==tar_sha256
    assert m["double_run_sha256"] == {"run1": m["tar_sha256"],
                                      "run2": m["tar_sha256"]}
    # base_sha_chain：钉死值+盘上真值三方核对（a16e0e9b→r34a→r37）
    chain = m["base_sha_chain"]
    assert set(chain) == {"a16e0e9b", "r34a", "r37"}
    assert chain["a16e0e9b"] == ("a16e0e9b40c489972630a0b9d04f30e9c1cab031"
                                 "59fa78676db74277d84d82ab")
    r34a_path = (Path(__file__).resolve().parent.parent
                 / "orderbook_2965_adopt" / "a" / "main.py")
    assert chain["r34a"] == hashlib.sha256(r34a_path.read_bytes()).hexdigest()
    assert chain["r37"] == m["main_sha256"]
    # 三白名单件 sha：块 sha 与 inject block_sha 同口径+变更表 canonical sha
    assert m["whitelist_shas"] == {
        "guard_block": inject_guard.inject_cash_guard_block("X = 1\n")["block_sha"],
        "sheep_change_table": _table_sha(_SHEEP_TABLE),
        "tail_removal_list": _table_sha(_TAIL_TABLE)}
    assert m["whitelist_shas_complete"] is True
    # 嵌入变更表 JSON 空白/键序不敏感（canonical sha 同）
    sloppy_text = (
        _BASE
        + '# R37_SHEEP_CHANGE_TABLE:  [{"count": 11, "animal": "SHEEP", '
          '"buy_step_new": 264, "buy_step_old": 456, "route": 9}]\n'
        + '# R37_TAIL_REMOVAL_LIST: [ {"step": 672, "removed": "CARE"},'
          '{"removed": "FEED", "step": 696} ]\n')
    sloppy_text = inject_guard.inject_cash_guard_block(sloppy_text)["main_text"]
    sloppy = tmp_path / "sloppy.py"
    sloppy.write_text(sloppy_text, encoding="utf-8", newline="\n")
    ms = B.pack_r37(str(sloppy), out_dir=str(tmp_path / "out_sloppy"))
    assert ms["whitelist_shas"] == m["whitelist_shas"]


def test_pack_r37_deterministic_double_run(tmp_path):
    # ①确定性双跑：同 main 两次 pack→同 tar 字节/同 sha；manifest 全同（generated 除外）。
    main = _write_main(tmp_path)
    out_a, out_b = tmp_path / "out_a", tmp_path / "out_b"
    m1 = B.pack_r37(str(main), out_dir=str(out_a))
    m2 = B.pack_r37(str(main), out_dir=str(out_b))
    tar_a = (out_a / "submission.tar.gz").read_bytes()
    tar_b = (out_b / "submission.tar.gz").read_bytes()
    assert tar_a == tar_b
    assert m1["tar_sha256"] == m2["tar_sha256"] == hashlib.sha256(tar_a).hexdigest()
    assert m1["double_run_sha256"]["run1"] == m1["double_run_sha256"]["run2"]
    g1, g2 = dict(m1), dict(m2)
    g1.pop("generated")
    g2.pop("generated")
    assert g1 == g2


def test_pack_r37_tar_shape(tmp_path):
    # ③tar 内条目形态（解包断言）：单 main.py、mode644/mtime0/uid0/gid0、内层同输入、gzip 头 mtime0。
    main = _write_main(tmp_path)
    out = tmp_path / "out"
    B.pack_r37(str(main), out_dir=str(out))
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


def test_pack_r37_distinct_mains_distinct_sha(tmp_path):
    # ④区分度：不同 main→不同 main_sha256/tar_sha256。
    main_a = _write_main(tmp_path, name="a.py")
    main_b = _write_main(tmp_path, name="b.py", base=_BASE + "X = 1\n")
    m1 = B.pack_r37(str(main_a), out_dir=str(tmp_path / "o1"))
    m2 = B.pack_r37(str(main_b), out_dir=str(tmp_path / "o2"))
    assert m1["main_sha256"] != m2["main_sha256"]
    assert m1["tar_sha256"] != m2["tar_sha256"]


def test_pack_r37_bad_input_raises(tmp_path):
    # ⑤坏输入即抛：非 str→TypeError；空路径/空文件/畸形标记锚→ValueError；缺文件→FileNotFoundError。
    with pytest.raises(TypeError):
        B.pack_r37(None, out_dir=str(tmp_path))
    with pytest.raises(TypeError):
        B.pack_r37(b"main.py", out_dir=str(tmp_path))
    with pytest.raises(TypeError):
        B.pack_r37(42, out_dir=str(tmp_path))
    with pytest.raises(TypeError):
        B.pack_r37(tmp_path / "main.py", out_dir=str(tmp_path))  # pathlib.Path 非 str
    with pytest.raises(ValueError):
        B.pack_r37("", out_dir=str(tmp_path))
    with pytest.raises(ValueError):
        B.pack_r37("   \n\t", out_dir=str(tmp_path))
    with pytest.raises(FileNotFoundError):
        B.pack_r37(str(tmp_path / "missing.py"), out_dir=str(tmp_path))
    empty = tmp_path / "empty.py"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        B.pack_r37(str(empty), out_dir=str(tmp_path))
    dup = tmp_path / "dup.py"
    dup.write_text(_BASE + "# R37_SHEEP_CHANGE_TABLE: []\n"
                   "# R37_SHEEP_CHANGE_TABLE: []\n", encoding="utf-8")
    with pytest.raises(ValueError):
        B.pack_r37(str(dup), out_dir=str(tmp_path))
    bad = tmp_path / "bad.py"
    bad.write_text(_BASE + "# R37_SHEEP_CHANGE_TABLE: {not json}\n",
                   encoding="utf-8")
    with pytest.raises(ValueError):
        B.pack_r37(str(bad), out_dir=str(tmp_path))
    anchor_only = tmp_path / "anchor_only.py"
    anchor_only.write_text(_BASE + _GUARD_TITLE + "\n", encoding="utf-8")
    with pytest.raises(ValueError):
        B.pack_r37(str(anchor_only), out_dir=str(tmp_path))


def test_pack_r37_double_run_mismatch_raises(tmp_path, monkeypatch):
    # ⑥错误契约：双跑不一致→RuntimeError 且产物不落盘（monkeypatch 配方源）。
    try:
        from orderbook_2965_adopt import build_adopt as ba
    except ImportError:  # 与 pack_r37 同款兜底导入路径
        import build_adopt as ba
    calls = []

    def _fake_build_tar_bytes(main_bytes):
        calls.append(main_bytes)
        return b"run%d|" % len(calls) + main_bytes

    monkeypatch.setattr(ba, "build_tar_bytes", _fake_build_tar_bytes)
    main = _write_main(tmp_path)
    out = tmp_path / "out"
    with pytest.raises(RuntimeError, match="双跑"):
        B.pack_r37(str(main), out_dir=str(out))
    assert len(calls) == 2
    assert not (out / "submission.tar.gz").exists()
    assert not (out / "build_manifest.json").exists()


def test_pack_r37_whitelist_best_effort(tmp_path):
    # ⑦三件 sha 尽力自证：缺件→null 不造假；仅守卫块在场→半填；complete 随行。
    plain = tmp_path / "plain.py"
    plain.write_text(_BASE, encoding="utf-8")
    m0 = B.pack_r37(str(plain), out_dir=str(tmp_path / "o0"))
    assert m0["whitelist_shas"] == {"guard_block": None,
                                    "sheep_change_table": None,
                                    "tail_removal_list": None}
    assert m0["whitelist_shas_complete"] is False
    assert m0["tar_rebuild_reproducible"] is True

    guard_only = _write_main(tmp_path, name="guard_only.py",
                             sheep=None, tail=None)
    m1 = B.pack_r37(str(guard_only), out_dir=str(tmp_path / "o1"))
    assert m1["whitelist_shas"] == {
        "guard_block": inject_guard.inject_cash_guard_block("X = 1\n")["block_sha"],
        "sheep_change_table": None, "tail_removal_list": None}
    assert m1["whitelist_shas_complete"] is False


def test_pack_r37_signature_intent():
    # ⑧签名微调登记钉：首参 r37_main、out_dir 可选默认 None（批间登记）。
    import inspect

    sig = inspect.signature(B.pack_r37)
    params = list(sig.parameters)
    assert params[0] == "r37_main" and set(params) == {"r37_main", "out_dir"}
    assert sig.parameters["out_dir"].default is None


# ---------------------------------------------------------------------------
# pack 组夹具（合成 r37 main：底版+内嵌变更表注释行+真守卫尾块）
# ---------------------------------------------------------------------------
_SHEEP_TABLE = [{"route": 9, "buy_step_old": 456, "buy_step_new": 264,
                 "animal": "SHEEP", "count": 11}]
_TAIL_TABLE = [{"step": 672, "removed": "CARE"},
               {"step": 696, "removed": "FEED"}]
_BASE = "def agent(observation):\n    return {'farmer': ['PASS']}\n"
_GUARD_TITLE = "# ============ r37 现金保底守卫尾块（自动生成，勿手改） ============"


def _canon(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"))


def _table_sha(obj):
    return hashlib.sha256(_canon(obj).encode("utf-8")).hexdigest()


def _write_main(tmp_path, name="main.py", sheep=_SHEEP_TABLE, tail=_TAIL_TABLE,
                guard=True, base=_BASE):
    parts = [base]
    if sheep is not None:
        parts.append("# R37_SHEEP_CHANGE_TABLE: " + _canon(sheep) + "\n")
    if tail is not None:
        parts.append("# R37_TAIL_REMOVAL_LIST: " + _canon(tail) + "\n")
    text = "".join(parts)
    if guard:
        text = inject_guard.inject_cash_guard_block(text)["main_text"]
    p = tmp_path / name
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


# ---------------------------------------------------------------------------
# audit 组共享夹具（最小真实 r34a/r37 文本对：真 blob 编解码+真守卫尾块）
# ---------------------------------------------------------------------------
def _mk_audit_pair():
    """构造 audit 组共享 (base34, r37, block_sha)：最小真实文本对+真块 sha。

    base34=底版（X/Y 常量行+stdlib 导入行+真 _R108_DATA blob：actions 6 件、
    路由 2 条微型（4+2 步）、shops 空；retape_sheep._encode_routes 真编解码，
    同输入两次编码逐字节恒等）；r37=同前缀+blob 内三类白名单差异——route "0"
    step1 SHEEP 买单 slot1 换 []（移出）+ step2 market 尾部追加 slot1（移入）、
    step3 CARE/FEED 单元指令删+闲置 HIRE 单删——再尾部追加真守卫块
    （inject_guard.inject_cash_guard_block，含锚行恰一次+单参入口行）。
    block_sha=注入块字节 sha（=audit tail_guard_block.sha256 口径）。
    """
    try:
        from orderbook_r37 import retape_sheep as _rs
    except ImportError:  # 与用例内同款兜底导入路径
        import retape_sheep as _rs

    def _act(market=(), farmer=("PASS",), hands=()):
        return {"farmer": list(farmer),
                "hands": [list(h) for h in hands],
                "market": [list(o) for o in market]}

    text = ("X = 1\nY = 2\nimport base64, json, zlib\n"
            "_R108_DATA=json.loads(zlib.decompress("
            "base64.b85decode('PLACEHOLDER')))\n")
    routes = {"0": [0, 1, 2, 3], "1": [4, 5]}
    a0 = _act([["SELL", "WHEAT", 4]])
    a1 = _act([["SELL", "WOOL", 5], ["BUY_ANIMAL", "SHEEP", 2]])
    a2 = _act([["SELL", "HAY", 3]])
    a3 = _act([["HIRE"], ["SELL", "HAY", 2]], farmer=("CARE",),
              hands=(["FEED"], ["HARVEST"]))
    a4 = _act([["SELL", "MILK", 1]])
    a5 = _act([["BUY_SEED", "MELON", 1]], farmer=("WATER",),
              hands=(["PASS"],))
    base34 = _rs._encode_routes(text, {
        "actions": [a0, a1, a2, a3, a4, a5], "routes": routes, "shops": []})
    b1 = _act([["SELL", "WOOL", 5], []])       # SHEEP 买单移出→[] 占位
    b2 = _act([["SELL", "HAY", 3],
               ["BUY_ANIMAL", "SHEEP", 2]])    # 同单移入→market 尾部追加
    b3 = _act([[], ["SELL", "HAY", 2]], farmer=(), hands=([], ["HARVEST"]))
    mid = _rs._encode_routes(text, {
        "actions": [a0, b1, b2, b3, a4, a5], "routes": routes, "shops": []})
    inj = inject_guard.inject_cash_guard_block(mid)
    return base34, inj["main_text"], inj["block_sha"]
