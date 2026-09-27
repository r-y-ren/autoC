# -*- coding: utf-8 -*-
"""R22 测试面：build_r39（audit 组/pack 组/build 组/真跑）。

audit 组（B26c，audit_diff_vs_r37 两类白名单）：①两类归因正路（尾块 v2+
磁带区 shear_phase，块 sha 对真块、shear sha 对变更表 canonical）②shear
diff 归类（真 retape_shear_phase 输出对账/纯 shear 无块/全 no-op 注释形态）
③白名单外即抛（前缀破坏/market 改单写时复制形态/未登记差异/虚报登记/注释
与 change_table 不符）④锚行识别（装饰差异兼容按核心短语/重复/底版在场/
分隔畸形/零差异缺块）。
pack 组（B26c，pack_r39）：①manifest 字段齐+文案原文+sha 链（a16e0e9b→
51fc19db(r34a)→r37=剥块重算→r39=输入）+predict_block/library_sha256（AST
主链）/shear_change_sha256（注释主链）②确定性双跑（manifest 全同/tar 逐字
节）③tar 内条目形态（单 main.py、mode644/mtime0/uid0/gid0、gzip MTIME=0）
④缺件 null 不造假（缺块/缺注释→complete=False）+区分度 ⑤坏输入即抛。
build 组（B26c，build_r39 编排）：①集成（毛期手术→变更表注释→建库桩→注入
→审计→打包，产物三件+返回八键+三 sha 对账）②输入字节不变 ③确定性双跑
④异常不落盘（审计红/缺文件→out 零产物）。
真跑：真 r37+真库（/tmp/kagr23 top-30 新鲜 + /tmp/r33audit 辅助）→
orderbook_predict/build/ 三件产物+evidence/build_r39_realrun.json（sha 摘要/
归因/双跑）。
"""
import copy
import hashlib
import io
import json
import sys
import tarfile
import time
from pathlib import Path

import pytest  # noqa: F401

_HERE = Path(__file__).resolve().parent
_KSIM = _HERE.parent
if str(_KSIM) not in sys.path:
    sys.path.insert(0, str(_KSIM))

try:
    from orderbook_predict import build_r38 as B
    from orderbook_predict import build_r39 as R
    from orderbook_predict import inject_predict
    from orderbook_predict import retape_shear_phase as sp
except ImportError:  # 兜底：直接以 orderbook_predict/ 为 sys.path 根跑测
    import build_r38 as B
    import build_r39 as R
    import inject_predict
    import retape_shear_phase as sp

try:
    from orderbook_r37 import retape_sheep as rs
except ImportError:
    sys.path.insert(0, str(_KSIM / "orderbook_r37"))
    import retape_sheep as rs

_CORE = "r38 对手预测尾块"
_SHEAR_MARKER = "# R39_SHEAR_CHANGE_TABLE: "
_DESC = ("public derivative with throttled opponent sell prediction "
         "(v2) and anti-counter schedule")
_A16 = ("a16e0e9b40c489972630a0b9d04f30e9c1cab031"
        "59fa78676db74277d84d82ab")
_R34A = ("51fc19dba2d0bcbf2d0a3720c26ff318541a0e6c"
         "e5800873bc863f612451aa5b")


# ------------------------------ 夹具 ------------------------------

def _canon_sha(obj):
    """canonical json sha256（sellflow/pack/audit 同口径：ensure_ascii=False）。"""
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, ensure_ascii=False,
                   separators=(",", ":")).encode("utf-8")).hexdigest()


def _mini_lib():
    """合成迷你卖流库（sellflow 建库件形态；ASCII 安全→三 sha 口径恒等）。"""
    return {
        "version": "sellflow/2.0",
        "keys": {"BAKERY|YARN_STORE||m229_w9989": {"n_episodes": 2, "hist": {
            "1": {"MILK": {"qty_sum": 9, "count": 3, "qty_max": 4}}}}},
        "global": {"n_episodes": 2, "hist": {
            "1": {"MILK": {"qty_sum": 9, "count": 3, "qty_max": 4}}}},
    }


def _comment(rows):
    """变更表注释单行（canonical json 单行，build_r39 同口径）。"""
    return (_SHEAR_MARKER + json.dumps(rows, sort_keys=True,
                                       separators=(",", ":"),
                                       ensure_ascii=False) + "\n")


def _mk_pkg(steps=720, places=(), shear_days=(), n_hands=2):
    """迷你磁带路由包（test_shear_phase 同款构造件：2 羊格 5 产毛窗）。"""
    farmers = {s: ["PASS"] for s in range(steps)}
    hands = {s: [["PASS"] for _ in range(n_hands)] for s in range(steps)}
    markets = {s: [] for s in range(steps)}
    for s, ui in places:
        hands[s][ui] = ["PLACE", "SHEEP", 1]
    for d, ui in shear_days:
        hands[d * 24][ui] = ["HARVEST"]
    actions = [{"farmer": farmers[s], "hands": hands[s], "market": markets[s]}
               for s in range(steps)]
    return {"actions": actions, "routes": {"0": list(range(steps))},
            "shops": []}


def _shear_pkg():
    """真 retape_shear_phase 手术输出（2 格错峰 from 15→to 17）。"""
    pkg = _mk_pkg(places=[(9 * 24 + 1, 0), (9 * 24 + 1, 1)],
                  shear_days=[(d, 0) for d in (15, 18, 21, 24, 27)]
                  + [(d, 1) for d in (15, 18, 21, 24, 27)])
    return pkg, sp.retape_shear_phase(pkg)


_TPL = ("import base64, json, zlib\n"
        "_R108_DATA=json.loads(zlib.decompress(base64.b85decode('x')))\n"
        "X = 1\n"
        "def _base_agent(observation):\n"
        "    return {'farmer': ['PASS'], 'hands': [], 'market': []}\n")


def _blob_text(pkg):
    """磁带 blob 底版文本（_encode_routes 真链填充 blob 字面量）。"""
    return rs._encode_routes(_TPL, pkg)


def _shear_pair():
    """(r37 文本, shear 后文本, 变更表)——真手术+真编解码。"""
    pkg, out = _shear_pkg()
    return _blob_text(pkg), _blob_text(out["routes"]), out["change_table"]


def _w(tmp_path, name, text):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8", newline="\n")
    return str(p)


def _audit_files(tmp_path, text39, text37, rows):
    return B.audit_diff_vs_r37(_w(tmp_path, "r39.py", text39),
                               _w(tmp_path, "r37.py", text37), rows)


def _patch_lib(monkeypatch, lib):
    """钉建库组件为合成迷你库（orderbook_predict.sellflow 与脚本态别名同钉）。"""
    def _fake_builder(replay_dir, labels=None):
        return {"library": lib,
                "build_audit": {"replay_dir": replay_dir, "n_files": 1,
                                "n_used": 1, "n_skipped": 0,
                                "total_events": 3,
                                "sha256_of_library": _canon_sha(lib)}}

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


# --------------------- audit 组（两类白名单真测试） ---------------------

def test_audit_two_class_attributed(tmp_path):
    # ①两类归因正路：尾块 v2（sha 对真块字节）+磁带区 shear_phase（sha 对
    # 变更表 canonical json），归因表三键/whitelist 两键钉死。
    t37, t39, rows = _shear_pair()
    assert len(rows) == 2 and all(not r["reason"].startswith("no-op")
                                  for r in rows)
    base_text = t39 + _comment(rows)
    inj = inject_predict.inject_predict_block(base_text, _mini_lib())
    main_text = inj["main_text"]
    m = _audit_files(tmp_path, main_text, t37, rows)
    assert set(m) == {"ok", "whitelist", "unattributed"}
    assert m["ok"] is True and m["unattributed"] == []
    assert set(m["whitelist"]) == {"predict_block", "shear_phase"}
    pb = m["whitelist"]["predict_block"]
    assert pb["present"] is True and pb["sha256"] == inj["block_sha"]
    assert pb["bytes"] == len(main_text.encode("utf-8")) \
        - len(base_text.encode("utf-8")) > 0
    sh = m["whitelist"]["shear_phase"]
    assert sh["present"] is True and sh["rows"] == len(rows)
    assert sh["changed_routes"] == ["0"]
    assert sh["sha256"] == _canon_sha(rows)
    assert json.loads(json.dumps(m, ensure_ascii=False)) == m   # JSON 可序列化


def test_audit_shear_only_and_noop(tmp_path):
    # ②shear diff 归类：纯 shear 无块（pb 不在场/shear 在场）；全 no-op 变更表
    # +注释在场+磁带零差异→ok（shear present=True 但 changed_routes 空）。
    t37, t39, rows = _shear_pair()
    m = _audit_files(tmp_path, t39 + _comment(rows), t37, rows)
    assert m["ok"] is True
    pb, sh = m["whitelist"]["predict_block"], m["whitelist"]["shear_phase"]
    assert pb["present"] is False and pb["sha256"] is None
    assert sh["present"] is True and sh["changed_routes"] == ["0"]
    # ②b 全 no-op（offset=3 越季丢弃→4 刀不可挪）：零差异+注释在场
    out3 = sp.retape_shear_phase(rs._decode_routes(t37), offset=3)
    rows3 = out3["change_table"]
    assert rows3 and all(r["reason"].startswith("no-op") for r in rows3)
    m2 = _audit_files(tmp_path, t37 + _comment(rows3), t37, rows3)
    assert m2["ok"] is True and m2["unattributed"] == []
    sh2 = m2["whitelist"]["shear_phase"]
    assert sh2["rows"] == len(rows3) and sh2["changed_routes"] == []
    assert sh2["present"] is True
    assert sh2["sha256"] == _canon_sha(rows3)


def test_audit_unattributed_raises(tmp_path):
    # ③白名单外即抛：前缀破坏/market 改单（写时复制形态）/未登记差异/虚报
    # 登记/注释与 change_table 参数不符。
    t37, t39, rows = _shear_pair()
    comment = _comment(rows)
    # ③a 前缀破坏（blob 前字节变）
    bad = (t39 + comment).replace("import base64, json, zlib\n",
                                  "import base64, json\nimport zlib\n", 1)
    with pytest.raises(ValueError, match="首条未归因：前缀"):
        _audit_files(tmp_path, bad, t37, rows)
    # ③b 非 shear 形 blob 差异（market 改单走写时复制指针）→ unattributed
    tampered = copy.deepcopy(rs._decode_routes(t37))
    act = copy.deepcopy(tampered["actions"][5])
    act["market"] = [["SELL", "MILK", 1]]
    tampered["actions"].append(act)
    tampered["routes"]["0"][5] = len(tampered["actions"]) - 1
    with pytest.raises(ValueError, match="shear_action"):
        _audit_files(tmp_path, _blob_text(tampered) + comment, t37, rows)
    # ③c 未登记差异（真 shear 输出但变更表空）
    with pytest.raises(ValueError, match="shear_unregistered"):
        _audit_files(tmp_path, t39 + _comment([]), t37, [])
    # ③d 虚报登记（变更表有真条目但磁带零差异）
    with pytest.raises(ValueError, match="shear_no_diff"):
        _audit_files(tmp_path, t37 + comment, t37, rows)
    # ③e 变更表注释与 change_table 参数不符
    with pytest.raises(ValueError, match="shear_comment"):
        _audit_files(tmp_path, t39 + _comment([]), t37, rows)


def test_audit_anchor_recognition(tmp_path):
    # ④锚行识别同 v1：装饰差异按核心短语识别；重复/底版在场/分隔畸形即抛；
    # 零差异缺块→present False。
    base = "# anchor 形态测试底版\nX = 1\n"
    deco = ("\n\n# ====== " + _CORE + "（自动生成，勿手改） ==\n"
            "_PREDICT_LIBRARY = {}\n")
    m = _audit_files(tmp_path, base + deco, base, [])
    assert m["ok"] is True
    pb = m["whitelist"]["predict_block"]
    assert pb["present"] is True
    assert pb["sha256"] == hashlib.sha256(deco.encode("utf-8")).hexdigest()
    assert pb["bytes"] == len(deco.encode("utf-8"))
    with pytest.raises(ValueError, match="anchor_duplicate"):
        _audit_files(tmp_path, base + deco + deco, base, [])
    with pytest.raises(ValueError, match="anchor_in_base"):
        _audit_files(tmp_path, base + deco, base + "# " + _CORE + " 底版注\n", [])
    bad_gap = base.rstrip("\n") + "\n# ============ " + _CORE \
        + "（自动生成，勿手改） ============\n"
    with pytest.raises(ValueError, match="block_separator"):
        _audit_files(tmp_path, bad_gap, base, [])
    m2 = _audit_files(tmp_path, base, base, [])
    assert m2["ok"] is True
    assert m2["whitelist"]["predict_block"] == {"present": False, "bytes": 0,
                                                "sha256": None}
    assert m2["whitelist"]["shear_phase"]["present"] is False


# ------------------------- pack 组（pack_r39） -------------------------

def test_pack_r39(tmp_path):
    # ①manifest 字段齐+文案原文+sha 链+三 sha 自证（predict_block/library/
    # shear）；返回=盘上 manifest。
    t37, t39, rows = _shear_pair()
    base_text = t39 + _comment(rows)
    inj = inject_predict.inject_predict_block(base_text, _mini_lib())
    main_text = inj["main_text"]
    p = _w(tmp_path, "main.py", main_text)
    out = tmp_path / "out"
    m = R.pack_r39(p, out_dir=str(out))
    assert set(m) == {"schema", "generated", "variant", "description",
                      "main_sha256", "main_bytes", "tar_sha256", "tar_bytes",
                      "tar_members", "double_run_sha256", "base_sha_chain",
                      "predict_block", "library_sha256",
                      "shear_change_sha256", "complete"}
    assert m["schema"] == "orderbook_r39_manifest/1.0"
    assert m["variant"] == "r39"
    assert m["description"] == _DESC
    raw = main_text.encode("utf-8")
    assert m["main_sha256"] == hashlib.sha256(raw).hexdigest()
    assert m["main_bytes"] == len(raw)
    assert m["tar_members"] == ["main.py"]
    assert set(m["base_sha_chain"]) == {"a16e0e9b", "r34a", "r37", "r39"}
    assert m["base_sha_chain"]["a16e0e9b"] == _A16
    assert m["base_sha_chain"]["r34a"] == _R34A
    assert m["base_sha_chain"]["r37"] == hashlib.sha256(
        base_text.encode("utf-8")).hexdigest()
    assert m["base_sha_chain"]["r39"] == m["main_sha256"]
    assert m["predict_block"] == {
        "present": True,
        "bytes": len(main_text.encode("utf-8"))
        - len(base_text.encode("utf-8")),
        "sha256": inj["block_sha"]}
    assert m["library_sha256"] == _canon_sha(_mini_lib())
    assert m["shear_change_sha256"] == _canon_sha(rows)
    assert m["complete"] is True
    assert m == json.loads((out / "build_manifest.json").read_text(
        encoding="utf-8"))
    assert (out / "submission.tar.gz").is_file()


def test_pack_r39_deterministic_double_run(tmp_path):
    # ②确定性双跑：同 main 两次 pack→manifest 全同（generated 日期同日）、
    # tar 逐字节同、双跑哈希恒等。
    t37, t39, rows = _shear_pair()
    base_text = t39 + _comment(rows)
    main_text = inject_predict.inject_predict_block(base_text,
                                                    _mini_lib())["main_text"]
    p = _w(tmp_path, "main.py", main_text)
    m1 = R.pack_r39(p, out_dir=str(tmp_path / "o1"))
    tar1 = (tmp_path / "o1" / "submission.tar.gz").read_bytes()
    m2 = R.pack_r39(p, out_dir=str(tmp_path / "o2"))
    tar2 = (tmp_path / "o2" / "submission.tar.gz").read_bytes()
    assert m1 == m2
    assert tar1 == tar2
    assert m1["double_run_sha256"] == {"run1": m1["tar_sha256"],
                                       "run2": m1["tar_sha256"]}
    # 区分度：不同 main→不同 sha
    p2 = _w(tmp_path, "main2.py", main_text + "Y = 2\n")
    m3 = R.pack_r39(p2, out_dir=str(tmp_path / "o3"))
    assert m3["main_sha256"] != m1["main_sha256"]
    assert m3["tar_sha256"] != m1["tar_sha256"]


def test_pack_r39_tar_shape(tmp_path):
    # ③tar 内条目形态：单 main.py、mode644/mtime0/uid0/gid0/size、内层字节
    # 同输入、gzip 头 FLG=0/MTIME=0。
    t37, t39, rows = _shear_pair()
    main_text = inject_predict.inject_predict_block(
        t39 + _comment(rows), _mini_lib())["main_text"]
    p = _w(tmp_path, "main.py", main_text)
    out = tmp_path / "out"
    m = R.pack_r39(p, out_dir=str(out))
    raw = (out / "submission.tar.gz").read_bytes()
    assert raw[:2] == b"\x1f\x8b" and raw[3] == 0      # FLG=0
    assert raw[4:8] == b"\x00\x00\x00\x00"             # gzip MTIME=0
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        members = tar.getmembers()
        inner = tar.extractfile("main.py").read()
    assert [mm.name for mm in members] == ["main.py"]
    mm = members[0]
    assert (mm.mode, mm.mtime, mm.uid, mm.gid) == (0o644, 0, 0, 0)
    assert mm.size == len(main_text.encode("utf-8"))
    assert inner == main_text.encode("utf-8")
    assert m["tar_bytes"] == len(raw)


def test_pack_r39_missing_pieces_null(tmp_path):
    # ④缺件 null 不造假：缺块/缺注释→对应 sha null+complete=False。
    t37, t39, rows = _shear_pair()
    block = "\n\n# ============ " + _CORE \
        + "（自动生成，勿手改） ============\n" \
        + "def _predict_agent(observation):\n    return {}\n"
    # 全缺（无块无注释）
    m0 = R.pack_r39(_w(tmp_path, "a.py", t37), out_dir=str(tmp_path / "oa"))
    assert m0["predict_block"] == {"present": False, "bytes": 0, "sha256": None}
    assert m0["library_sha256"] is None and m0["shear_change_sha256"] is None
    assert m0["base_sha_chain"]["r37"] is None
    assert m0["complete"] is False
    # 有块缺库行缺注释（库 sha/shear sha null；r37 剥块节点在场）
    m1 = R.pack_r39(_w(tmp_path, "b.py", t39 + block), out_dir=str(tmp_path / "ob"))
    assert m1["predict_block"]["present"] is True
    assert m1["library_sha256"] is None      # 块内无 _PREDICT_LIBRARY→null 不造假
    assert m1["shear_change_sha256"] is None
    assert m1["base_sha_chain"]["r37"] is not None
    assert m1["complete"] is False
    # 有注释缺块（块/库/r37 节点 null，shear sha 在场）
    m2 = R.pack_r39(_w(tmp_path, "c.py", t39 + _comment(rows)),
                    out_dir=str(tmp_path / "oc"))
    assert m2["predict_block"]["present"] is False
    assert m2["library_sha256"] is None and m2["base_sha_chain"]["r37"] is None
    assert m2["shear_change_sha256"] == _canon_sha(rows)
    assert m2["complete"] is False


def test_pack_r39_bad_input_raises(tmp_path):
    # ⑤坏输入即抛：非 str→TypeError、空/纯空白→ValueError、空文件→ValueError、
    # 锚两次/分隔畸形/伴生行重复或坏值→ValueError、缺文件→FileNotFoundError。
    t37, t39, rows = _shear_pair()
    with pytest.raises(TypeError):
        R.pack_r39(Path(tmp_path) / "main.py", out_dir=str(tmp_path))
    with pytest.raises(TypeError):
        R.pack_r39("x.py", out_dir=3)
    with pytest.raises(ValueError):
        R.pack_r39("   ")
    with pytest.raises(ValueError):
        R.pack_r39("")
    empty = _w(tmp_path, "empty.py", "")
    with pytest.raises(ValueError):
        R.pack_r39(empty, out_dir=str(tmp_path / "o1"))
    block = "\n\n# ============ " + _CORE \
        + "（自动生成，勿手改） ============\n_PREDICT_LIBRARY = {}\n"
    with pytest.raises(ValueError, match="预测块锚行核心短语出现 2 次"):
        R.pack_r39(_w(tmp_path, "twice.py", t37 + block + block),
                   out_dir=str(tmp_path / "o2"))
    with pytest.raises(ValueError, match="锚行前分隔畸形"):
        R.pack_r39(_w(tmp_path, "gap.py", t37 + block.lstrip("\n")),
                   out_dir=str(tmp_path / "o3"))
    with pytest.raises(ValueError, match="R39_SHEAR_CHANGE_TABLE"):
        R.pack_r39(_w(tmp_path, "badc.py",
                      t39 + _comment(rows) + _comment(rows)),
                   out_dir=str(tmp_path / "o4"))
    with pytest.raises(ValueError, match="R39_SHEAR_CHANGE_TABLE"):
        R.pack_r39(_w(tmp_path, "badj.py",
                      t39 + _SHEAR_MARKER + "{not json\n"),
                   out_dir=str(tmp_path / "o5"))
    with pytest.raises(FileNotFoundError):
        R.pack_r39(str(tmp_path / "missing.py"), out_dir=str(tmp_path / "o6"))


# ------------------------- build 组（build_r39） -------------------------

def test_build_r39(tmp_path, monkeypatch):
    # ①编排全流程集成+②输入字节不变：毛期手术→变更表注释→建库（桩）→注入→
    # 审计→打包真链；产物三件+返回八键+三 sha 对账（inject/audit/pack 互证）。
    _patch_lib(monkeypatch, _mini_lib())
    src = tmp_path / "r37_main.py"
    src.write_text(_blob_text(_shear_pkg()[0]), encoding="utf-8",
                   newline="\n")
    before = src.read_bytes()
    out = tmp_path / "out"
    res = R.build_r39(str(src), out_dir=str(out))
    assert src.read_bytes() == before                        # ②输入字节不变

    for name in ("main.py", "submission.tar.gz", "build_manifest.json"):
        assert (out / name).is_file()
    assert set(res) == {"main_path", "main_sha256", "tar_sha256", "manifest",
                        "diff_attribution", "block_sha", "library_sha256",
                        "shear_change_sha256"}
    raw = (out / "main.py").read_bytes()
    assert res["main_path"] == str(out / "main.py")
    assert res["main_sha256"] == hashlib.sha256(raw).hexdigest()
    assert res["tar_sha256"] == hashlib.sha256(
        (out / "submission.tar.gz").read_bytes()).hexdigest()

    m = res["manifest"]
    assert m == json.loads((out / "build_manifest.json").read_text(
        encoding="utf-8"))
    assert m["schema"] == "orderbook_r39_manifest/1.0" and m["complete"] is True
    assert m["base_sha_chain"]["r39"] == res["main_sha256"]
    assert m["base_sha_chain"]["r37"] == hashlib.sha256(
        raw[:len(raw) - m["predict_block"]["bytes"]]).hexdigest()

    # 变更表注释单行在 base 内（shear sha 对注释 canonical）
    marks = [ln for ln in raw.decode("utf-8").splitlines()
             if ln.startswith(_SHEAR_MARKER)]
    assert len(marks) == 1
    rows = json.loads(marks[0][len(_SHEAR_MARKER):])
    assert len(rows) == 2 and all(r["kind"] == "shear_phase" for r in rows)
    assert res["shear_change_sha256"] == _canon_sha(rows) \
        == m["shear_change_sha256"]

    # 两类归因+三 sha 互证（inject=audit=pack）
    att = res["diff_attribution"]
    assert att["ok"] is True and att["unattributed"] == []
    assert set(att["whitelist"]) == {"predict_block", "shear_phase"}
    assert att["whitelist"]["predict_block"]["sha256"] == res["block_sha"] \
        == m["predict_block"]["sha256"]
    assert att["whitelist"]["shear_phase"]["rows"] == len(rows)
    assert res["library_sha256"] == _canon_sha(_mini_lib()) \
        == m["library_sha256"]
    # r37 零改动语义：shear 变更表只登记 kind=shear_phase、路由级差异对账过
    assert att["whitelist"]["shear_phase"]["changed_routes"] == ["0"]


def test_build_r39_deterministic_two_runs(tmp_path, monkeypatch):
    # ③确定性：同输入两次 build→main/tar/block/library/shear sha 全同。
    _patch_lib(monkeypatch, _mini_lib())
    src = tmp_path / "r37_main.py"
    src.write_text(_blob_text(_shear_pkg()[0]), encoding="utf-8",
                   newline="\n")
    r1 = R.build_r39(str(src), out_dir=str(tmp_path / "o1"))
    r2 = R.build_r39(str(src), out_dir=str(tmp_path / "o2"))
    for k in ("main_sha256", "tar_sha256", "block_sha", "library_sha256",
              "shear_change_sha256"):
        assert r1[k] == r2[k], k
    assert (tmp_path / "o1" / "main.py").read_bytes() \
        == (tmp_path / "o2" / "main.py").read_bytes()


def test_build_r39_failure_no_artifacts(tmp_path, monkeypatch):
    # ④异常不落盘（B18 同款）：审计红/缺文件→out 目录零产物。
    _patch_lib(monkeypatch, _mini_lib())
    src = tmp_path / "r37_main.py"
    src.write_text(_blob_text(_shear_pkg()[0]), encoding="utf-8",
                   newline="\n")

    def _boom(r39_main, r37_main, change_table=None):
        raise RuntimeError("audit 红（测试注入）")

    try:
        from orderbook_predict import build_r38 as _br
    except ImportError:
        import build_r38 as _br
    monkeypatch.setattr(_br, "audit_diff_vs_r37", _boom)
    out = tmp_path / "out"
    with pytest.raises(RuntimeError, match="audit 红"):
        R.build_r39(str(src), out_dir=str(out))
    assert not (out / "main.py").exists()
    assert not (out / "submission.tar.gz").exists()
    assert not (out / "build_manifest.json").exists()
    monkeypatch.undo()
    with pytest.raises(FileNotFoundError):
        R.build_r39(str(tmp_path / "missing.py"), out_dir=str(out))
    assert not (out / "main.py").exists()


# --------------------------- 真跑（真 r37+真库） ---------------------------

def test_build_r39_realrun():
    # 真跑验收：orderbook_r37/build/main.py + /tmp/kagr23（top-30 新鲜）+
    # /tmp/r33audit（辅助）→ orderbook_predict/build/ 三件产物 +
    # evidence/build_r39_realrun.json（sha 摘要/归因/双跑）。
    src = _KSIM / "orderbook_r37" / "build" / "main.py"
    res = R.build_r39(str(src))            # out_dir=None → 本包 build/
    out = _HERE / "build"
    for name in ("main.py", "submission.tar.gz", "build_manifest.json"):
        assert (out / name).is_file()
    m = res["manifest"]
    assert m["complete"] is True
    att = res["diff_attribution"]
    assert att["ok"] is True and att["unattributed"] == []
    sh = att["whitelist"]["shear_phase"]
    assert att["whitelist"]["predict_block"]["present"] is True
    assert sh["present"] is True and sh["rows"] == 283
    # 偏移路由与 shear_phase_realrun.json 交叉核对（真跑数字一致性）
    ev_shear = json.loads((_HERE / "evidence" / "shear_phase_realrun.json")
                          .read_text(encoding="utf-8"))
    assert sh["changed_routes"] == ev_shear["shifted_routes"]
    assert sh["sha256"] == res["shear_change_sha256"] == m["shear_change_sha256"]
    assert m["double_run_sha256"]["run1"] == m["double_run_sha256"]["run2"] \
        == res["tar_sha256"]

    ev = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "generated_by": "build_r39_realrun",
        "r37_main_path": "orderbook_r37/build/main.py",
        "corpus": {"replay_dir": "/tmp/kagr23", "aux_replay_dir": "/tmp/r33audit"},
        "sha_summary": {
            "r37_main_sha256": hashlib.sha256(
                src.read_bytes()).hexdigest(),
            "main_sha256": res["main_sha256"],
            "tar_sha256": res["tar_sha256"],
            "block_sha256": res["block_sha"],
            "library_sha256": res["library_sha256"],
            "shear_change_sha256": res["shear_change_sha256"],
            "base_node_r37": m["base_sha_chain"]["r37"],
        },
        "diff_attribution": att,
        "double_run_sha256": m["double_run_sha256"],
        "shear_summary": {"rows": sh["rows"],
                          "n_changed": len(sh["changed_routes"]),
                          "changed_routes": sh["changed_routes"]},
        "build": res,
    }
    ev_path = _HERE / "evidence" / "build_r39_realrun.json"
    ev_path.write_text(json.dumps(ev, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8")
