# -*- coding: utf-8 -*-
"""R23 测试面：build_r40（构建组/audit 两类/pack 组）。

audit 组（audit_diff_r40_vs_r37 两类白名单）：①两类归因正路（尾块 sha 对真
块+磁带区 sell_lots sha 对变更表 canonical）②sell_lots diff 归类（真
retape_sell_lots 输出对账：同拍并单重复步+跨拍批量化重放终态双向恒等/纯
sell_lots 无块/零差异空表）③白名单外即抛（未登记差异/虚报登记/前缀破坏/
注释与 change_table 不符/篡改卖单/改非卖单动作/change_table=None 越界）
④锚行识别（装饰差异兼容按核心短语/重复/底版在场/分隔畸形/零差异缺块）。
pack 组（pack_r40）：①manifest 字段齐+文案原文+sha 链（a16e0e9b→r34a→
r37=剥块重算→r40=输入）+runtime_block/route_library_sha256/sell_lots_
change_sha256 三 sha 自证②确定性双跑（manifest 全同/tar 逐字节）③tar 内
条目形态（单 main.py、mode644/mtime0/uid0/gid0、gzip MTIME=0）④缺件 null
不造假（缺块/缺注释→complete=False）+区分度 ⑤坏输入即抛 ⑥双跑不等即抛。
build 组（build_r40 编排）：①集成（卖单手术→变更表注释→建库桩→注入→审计→
打包，产物三件+返回八键+三 sha 对账）②输入字节不变 ③确定性双跑
④异常不落盘（审计红/缺文件→out 零产物）。
真跑：真 r37+真库（kagr23+kagr22+analysis24 败局 12 局=77 局 49 族）→
orderbook_r40/build/ 三件产物+evidence/build_r40_realrun.json（sha 摘要/
归因/双跑）。
"""
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
    from orderbook_r40 import build_r40 as B
    from orderbook_r40 import inject_r40 as IJ
    from orderbook_r40 import retape_lots as rl
except ImportError:  # 兜底：直接以 orderbook_r40/ 为 sys.path 根跑测
    import build_r40 as B
    import inject_r40 as IJ
    import retape_lots as rl

try:
    from orderbook_r37 import retape_sheep as rs
except ImportError:
    sys.path.insert(0, str(_KSIM / "orderbook_r37"))
    import retape_sheep as rs  # type: ignore

_CORE = "r40 运行时尾块"
_LOT_MARKER = B._LOT_MARKER
_DESC = ("public derivative with route library and "
         "late-season sell execution")
_A16 = ("a16e0e9b40c489972630a0b9d04f30e9c1cab031"
        "59fa78676db74277d84d82ab")
_R34A = ("51fc19dba2d0bcbf2d0a3720c26ff318541a0e6c"
         "e5800873bc863f612451aa5b")
_REAL_LIB_SHA = ("0236c30e4e728166c8a8751535517a75c5c13309"
                 "2f2e8f14f2b197baa193ed68")


# ------------------------------ 夹具 ------------------------------

def _canon_sha(obj):
    """canonical json sha256（audit/pack/route_library 同口径）。"""
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"),
                   ensure_ascii=False).encode("utf-8")).hexdigest()


def _mini_lib():
    """合成迷你续段库核心（route_library lib_core 形态；None/bool 实测面）。"""
    return {
        "version": "routelib/1.0",
        "families": {"2|1|WHEAT:5|BAKERY+FARMERS_MARKET": {
            "n_games": 2, "win_rate": 1.0, "margin_mean": 800.0,
            "best_route": 5, "segments": {}}},
        "default": {"n_games": 2, "win_rate": 1.0, "margin_mean": 800.0,
                    "best_route": 5, "segments": {}},
        "defeat_worlds": {"milk_flow": {"families": [], "covered": False}},
    }


def _comment(rows):
    """变更表注释单行（canonical json 单行，build_r40 同口径）。"""
    return (_LOT_MARKER + " " + json.dumps(
        rows, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False) + "\n")


def _mk_pkg(sells=(), others=(), n_steps=719):
    """迷你磁带路由包（test_retape_lots 同款构造件）：sells=[(step,slot,item,
    qty)]，others=[(step,slot,order)]；路由 0 走满 719 步（池件全被引用）。"""
    markets = {}

    def _put(step, slot, order):
        m = markets.setdefault(step, {})
        assert slot not in m, "测试构造槽位重复: (%d,%d)" % (step, slot)
        m[slot] = order

    for (s, slot, item, qty) in sells:
        _put(s, slot, ["SELL", item, qty])
    for (s, slot, order) in others:
        _put(s, slot, list(order))
    actions = []
    for s in range(n_steps):
        m = markets.get(s, {})
        width = (max(m) + 1) if m else 0
        actions.append({"farmer": ["PASS"], "hands": [],
                        "market": [m.get(j, []) for j in range(width)]})
    return {"actions": actions, "routes": {"0": list(range(n_steps))},
            "shops": []}


_TPL = ("import base64, json, zlib\n"
        "_R108_DATA=json.loads(zlib.decompress(base64.b85decode('x')))\n"
        "X = 1\n"
        "def _base_agent(observation):\n"
        "    return {'farmer': ['PASS'], 'hands': [], 'market': []}\n")


def _blob_text(pkg):
    """磁带 blob 底版文本（_encode_routes 真链填充 blob 字面量）。"""
    return rs._encode_routes(_TPL, pkg)


def _lot_pkg():
    """卖单手术测试磁带：WOOL 同拍 2 单+跨拍 2 单、MILK 跨拍 2 单、1 非卖单。"""
    return _mk_pkg(sells=[(505, 0, "WOOL", 2), (505, 2, "WOOL", 1),
                          (520, 1, "WOOL", 3), (540, 0, "WOOL", 4),
                          (510, 0, "MILK", 5), (511, 1, "MILK", 1)],
                   others=[(530, 0, ["HIRE", "HAND"])])


def _lot_pair():
    """(r37 文本, sell_lots 后 base 文本, 变更表)——真手术+真编解码（批量化
    目标=1：同拍并单+跨拍批量化两式齐出，行序=①WOOL ②MILK ②WOOL）。"""
    pkg = _lot_pkg()
    out = rl.retape_sell_lots(pkg, {"max_orders_target": 1})
    return _blob_text(pkg), _blob_text(out["routes"]), out["change_table"]


def _base_with(tape_text):
    """手术后磁带文本→base 文本（保尾换行）。"""
    return tape_text if tape_text.endswith("\n") else tape_text + "\n"


def _injected_pair():
    """(r37 文本, base 文本, 变更表, r40 main 文本, inject 返回)。"""
    t37, t40, rows = _lot_pair()
    base_text = _base_with(t40) + _comment(rows)
    inj = IJ.inject_r40_block(base_text, _mini_lib())
    return t37, base_text, rows, inj["main_text"], inj


def _w(tmp_path, name, text):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8", newline="\n")
    return str(p)


def _audit_files(tmp_path, text40, text37, rows):
    return B.audit_diff_r40_vs_r37(_w(tmp_path, "r40.py", text40),
                                   _w(tmp_path, "r37.py", text37), rows)


def _patch_lib(monkeypatch, lib):
    """钉建库组件为合成迷你库（包件与脚本态别名同钉）。"""
    core_sha = _canon_sha(lib)

    def _fake_builder(game_dir, family_cfg=None):
        return {"library": dict(lib, build_audit={"library_sha": core_sha}),
                "build_audit": {"library_sha": core_sha, "n_games": 2,
                                "n_families": 1, "coverage": 1.0,
                                "uncovered_families": []}}

    try:
        from orderbook_r40 import route_library as _rlo
    except ImportError:
        import route_library as _rlo
    targets = [_rlo]
    _alt = sys.modules.get("route_library")
    if _alt is not None and _alt is not _rlo:
        targets.append(_alt)
    for m in targets:
        monkeypatch.setattr(m, "build_route_library", _fake_builder)


def _patch_audit(monkeypatch, fn):
    """钉 audit（build_r40 同模块全局；包件与脚本态别名同钉）。"""
    targets = [B]
    _alt = sys.modules.get("build_r40")
    if _alt is not None and _alt is not B:
        targets.append(_alt)
    for m in targets:
        monkeypatch.setattr(m, "audit_diff_r40_vs_r37", fn)


# --------------------- audit 组（两类白名单真测试） ---------------------

def test_audit_two_class_attributed(tmp_path):
    # ①两类归因正路：尾块（sha 对真块字节）+磁带区 sell_lots（sha 对变更表
    # canonical json），归因表三键/whitelist 两键钉死。
    t37, base_text, rows, main_text, inj = _injected_pair()
    assert len(rows) == 3
    assert rows[0]["from_steps"] == [505, 505]     # 同拍并单重复步
    assert rows[2]["from_steps"] == [505, 520, 540]
    assert all(r["kind"] == "sell_lots" for r in rows)
    m = _audit_files(tmp_path, main_text, t37, rows)
    assert set(m) == {"ok", "whitelist", "unattributed"}
    assert m["ok"] is True and m["unattributed"] == []
    assert set(m["whitelist"]) == {"runtime_block", "sell_lots"}
    rb = m["whitelist"]["runtime_block"]
    assert rb["present"] is True and rb["sha256"] == inj["block_sha"]
    assert rb["bytes"] == len(main_text.encode("utf-8")) \
        - len(base_text.encode("utf-8")) > 0
    sl = m["whitelist"]["sell_lots"]
    assert sl["present"] is True and sl["rows"] == len(rows)
    assert sl["changed_routes"] == ["0"]
    assert sl["sha256"] == _canon_sha(rows)
    assert json.loads(json.dumps(m, ensure_ascii=False)) == m   # JSON 可序列化


def test_audit_sell_lots_classification(tmp_path):
    # ②sell_lots diff 归类：纯 sell_lots 无块（rb 不在场/sl 在场）；零差异+
    # 空表→ok（sl present False）；批量化重放终态双向恒等（同拍并单+跨拍
    # 批量化两式）由 ① 钉住，此处补非卖单不动反例（手术零触碰 HIRE 单）。
    t37, t40, rows = _lot_pair()
    m = _audit_files(tmp_path, _base_with(t40) + _comment(rows), t37, rows)
    assert m["ok"] is True
    rb, sl = m["whitelist"]["runtime_block"], m["whitelist"]["sell_lots"]
    assert rb["present"] is False and rb["sha256"] is None
    assert sl["present"] is True and sl["changed_routes"] == ["0"]
    pkg40 = rs._decode_routes(t40)
    assert pkg40["actions"][pkg40["routes"]["0"][530]] == \
        {"farmer": ["PASS"], "hands": [], "market": [["HIRE", "HAND"]]}
    # 零差异+空表
    m2 = _audit_files(tmp_path, t37 + _comment([]), t37, [])
    assert m2["ok"] is True and m2["whitelist"]["sell_lots"] == {
        "present": True, "rows": 0, "changed_routes": [],
        "sha256": _canon_sha([])}
    # 零差异无注释无表
    m3 = _audit_files(tmp_path, t37, t37, None)
    assert m3["ok"] is True and m3["whitelist"]["runtime_block"] == {
        "present": False, "bytes": 0, "sha256": None}
    assert m3["whitelist"]["sell_lots"]["present"] is False


def test_audit_unattributed_raises(tmp_path):
    # ③白名单外即抛：未登记差异/虚报登记/前缀破坏/注释不符/篡改卖单/改
    # 非卖单动作/change_table=None 越界。
    t37, t40, rows = _lot_pair()
    comment = _comment(rows)
    base40 = _base_with(t40)
    # ③a 未登记差异（真手术输出但变更表空+注释对空表）
    with pytest.raises(ValueError, match="lot_state"):
        _audit_files(tmp_path, base40 + _comment([]), t37, [])
    # ③b 虚报登记（变更表真条目但磁带零差异，注释在场）
    with pytest.raises(ValueError, match="lot_state"):
        _audit_files(tmp_path, t37 + comment, t37, rows)
    # ③c 前缀破坏（blob 前字节变）
    bad = (base40 + comment).replace("import base64, json, zlib\n",
                                     "import base64, json\nimport zlib\n", 1)
    with pytest.raises(ValueError, match="prefix_broken"):
        _audit_files(tmp_path, bad, t37, rows)
    # ③d 变更表注释与 change_table 参数不符
    with pytest.raises(ValueError, match="lot_comment"):
        _audit_files(tmp_path, base40 + _comment([]), t37, rows)
    # ③e 篡改卖单（合并单 qty+1 走写时复制指针）→ 重放终态不恒等
    tampered = rl.retape_sell_lots(_lot_pkg(), {"max_orders_target": 1})["routes"]
    tampered["actions"][tampered["routes"]["0"][505]]["market"][0][2] += 1
    t40c = _blob_text(tampered)
    with pytest.raises(ValueError, match="lot_state"):
        _audit_files(tmp_path, _base_with(t40c) + comment, t37, rows)
    # ③f 改非卖单动作（farmer 单元指令，走写时复制指针形态）→ lot_action
    import copy as _copy
    tampered2 = rl.retape_sell_lots(_lot_pkg(), {"max_orders_target": 1})["routes"]
    act = _copy.deepcopy(tampered2["actions"][tampered2["routes"]["0"][530]])
    act["farmer"] = ["HARVEST"]
    tampered2["actions"].append(act)
    tampered2["routes"]["0"][530] = len(tampered2["actions"]) - 1
    t40d = _blob_text(tampered2)
    with pytest.raises(ValueError, match="lot_action"):
        _audit_files(tmp_path, _base_with(t40d) + comment, t37, rows)
    # ③f' 就地改被引用池件（非写时复制形态）→ lot_pool
    tampered3 = rl.retape_sell_lots(_lot_pkg(), {"max_orders_target": 1})["routes"]
    tampered3["actions"][tampered3["routes"]["0"][530]]["farmer"] = ["HARVEST"]
    t40e = _blob_text(tampered3)
    with pytest.raises(ValueError, match="lot_pool"):
        _audit_files(tmp_path, _base_with(t40e) + comment, t37, rows)
    # ③g change_table=None 不许磁带差异（零登记口径）
    with pytest.raises(ValueError):
        _audit_files(tmp_path, base40, t37, None)


def test_audit_anchor_recognition(tmp_path):
    # ④锚行识别同 B26：装饰差异按核心短语识别；重复/底版在场/分隔畸形即抛；
    # 零差异缺块→present False。
    base = "# anchor 形态测试底版\nX = 1\n"
    deco = ("\n\n# ====== " + _CORE + "（自动生成，勿手改） ==\n"
            "_R40_LIBRARY = {}\n")
    m = _audit_files(tmp_path, base + deco, base, [])
    assert m["ok"] is True
    rb = m["whitelist"]["runtime_block"]
    assert rb["present"] is True
    assert rb["sha256"] == hashlib.sha256(deco.encode("utf-8")).hexdigest()
    assert rb["bytes"] == len(deco.encode("utf-8"))
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
    assert m2["whitelist"]["runtime_block"] == {"present": False, "bytes": 0,
                                                "sha256": None}
    assert m2["whitelist"]["sell_lots"]["present"] is False


# ------------------------- pack 组（pack_r40） -------------------------

def test_pack_r40(tmp_path):
    # ①manifest 字段齐+文案原文+sha 链+三 sha 自证（runtime_block/
    # route_library/sell_lots）；返回=盘上 manifest。
    t37, base_text, rows, main_text, inj = _injected_pair()
    p = _w(tmp_path, "main.py", main_text)
    out = tmp_path / "out"
    m = B.pack_r40(p, out_dir=str(out))
    assert set(m) == {"schema", "generated", "variant", "description",
                      "main_sha256", "main_bytes", "tar_sha256", "tar_bytes",
                      "tar_members", "double_run_sha256", "base_sha_chain",
                      "runtime_block", "route_library_sha256",
                      "sell_lots_change_sha256", "complete"}
    assert m["schema"] == "orderbook_r40_manifest/1.0"
    assert m["variant"] == "r40"
    assert m["description"] == _DESC
    raw = main_text.encode("utf-8")
    assert m["main_sha256"] == hashlib.sha256(raw).hexdigest()
    assert m["main_bytes"] == len(raw)
    assert m["tar_members"] == ["main.py"]
    assert set(m["base_sha_chain"]) == {"a16e0e9b", "r34a", "r37", "r40"}
    assert m["base_sha_chain"]["a16e0e9b"] == _A16
    assert m["base_sha_chain"]["r34a"] == _R34A
    assert m["base_sha_chain"]["r37"] == hashlib.sha256(
        base_text.encode("utf-8")).hexdigest()
    assert m["base_sha_chain"]["r40"] == m["main_sha256"]
    assert m["runtime_block"] == {
        "present": True,
        "bytes": len(main_text.encode("utf-8"))
        - len(base_text.encode("utf-8")),
        "sha256": inj["block_sha"]}
    assert m["route_library_sha256"] == _canon_sha(_mini_lib())
    assert m["sell_lots_change_sha256"] == _canon_sha(rows)
    assert m["complete"] is True
    assert m == json.loads((out / "build_manifest.json").read_text(
        encoding="utf-8"))
    assert (out / "submission.tar.gz").is_file()


def test_pack_r40_deterministic_double_run(tmp_path):
    # ②确定性双跑：同 main 两次 pack→manifest 全同、tar 逐字节同、双跑哈希恒等。
    t37, base_text, rows, main_text, inj = _injected_pair()
    p = _w(tmp_path, "main.py", main_text)
    m1 = B.pack_r40(p, out_dir=str(tmp_path / "o1"))
    tar1 = (tmp_path / "o1" / "submission.tar.gz").read_bytes()
    m2 = B.pack_r40(p, out_dir=str(tmp_path / "o2"))
    tar2 = (tmp_path / "o2" / "submission.tar.gz").read_bytes()
    assert m1 == m2
    assert tar1 == tar2
    assert m1["double_run_sha256"] == {"run1": m1["tar_sha256"],
                                       "run2": m1["tar_sha256"]}
    # 区分度：不同 main→不同 sha
    p2 = _w(tmp_path, "main2.py", main_text + "Y = 2\n")
    m3 = B.pack_r40(p2, out_dir=str(tmp_path / "o3"))
    assert m3["main_sha256"] != m1["main_sha256"]
    assert m3["tar_sha256"] != m1["tar_sha256"]


def test_pack_r40_tar_shape(tmp_path):
    # ③tar 内条目形态：单 main.py、mode644/mtime0/uid0/gid0/size、内层字节
    # 同输入、gzip 头 FLG=0/MTIME=0。
    t37, base_text, rows, main_text, inj = _injected_pair()
    p = _w(tmp_path, "main.py", main_text)
    out = tmp_path / "out"
    m = B.pack_r40(p, out_dir=str(out))
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


def test_pack_r40_missing_pieces_null(tmp_path):
    # ④缺件 null 不造假：缺块/缺注释→对应 sha null+complete=False。
    t37, t40, rows = _lot_pair()
    block = "\n\n# ============ " + _CORE \
        + "（自动生成，勿手改） ============\n" \
        + "def _route40_agent(observation):\n    return {}\n"
    # 全缺（无块无注释）
    m0 = B.pack_r40(_w(tmp_path, "a.py", t37), out_dir=str(tmp_path / "oa"))
    assert m0["runtime_block"] == {"present": False, "bytes": 0, "sha256": None}
    assert m0["route_library_sha256"] is None
    assert m0["sell_lots_change_sha256"] is None
    assert m0["base_sha_chain"]["r37"] is None
    assert m0["complete"] is False
    # 有块缺库行缺注释（库 sha/变更表 sha null；r37 剥块节点在场）
    m1 = B.pack_r40(_w(tmp_path, "b.py", t40 + block),
                    out_dir=str(tmp_path / "ob"))
    assert m1["runtime_block"]["present"] is True
    assert m1["route_library_sha256"] is None      # 块内无 _R40_LIBRARY→null
    assert m1["sell_lots_change_sha256"] is None
    assert m1["base_sha_chain"]["r37"] is not None
    assert m1["complete"] is False
    # 有注释缺块（块/库/r37 节点 null，变更表 sha 在场）
    m2 = B.pack_r40(_w(tmp_path, "c.py", t40 + _comment(rows)),
                    out_dir=str(tmp_path / "oc"))
    assert m2["runtime_block"]["present"] is False
    assert m2["route_library_sha256"] is None and m2["base_sha_chain"]["r37"] \
        is None
    assert m2["sell_lots_change_sha256"] == _canon_sha(rows)
    assert m2["complete"] is False


def test_pack_r40_bad_input_raises(tmp_path):
    # ⑤坏输入即抛：非 str→TypeError、空/纯空白→ValueError、空文件→ValueError、
    # 锚两次/分隔畸形/伴生行重复或坏值→ValueError、缺文件→FileNotFoundError。
    t37, t40, rows = _lot_pair()
    with pytest.raises(TypeError):
        B.pack_r40(Path(tmp_path) / "main.py", out_dir=str(tmp_path))
    with pytest.raises(TypeError):
        B.pack_r40("x.py", out_dir=3)
    with pytest.raises(ValueError):
        B.pack_r40("   ")
    with pytest.raises(ValueError):
        B.pack_r40("")
    empty = _w(tmp_path, "empty.py", "")
    with pytest.raises(ValueError):
        B.pack_r40(empty, out_dir=str(tmp_path / "o1"))
    block = "\n\n# ============ " + _CORE \
        + "（自动生成，勿手改） ============\n_R40_LIBRARY = {}\n"
    with pytest.raises(ValueError, match="锚行核心短语出现 2 次"):
        B.pack_r40(_w(tmp_path, "twice.py", t37 + block + block),
                   out_dir=str(tmp_path / "o2"))
    with pytest.raises(ValueError, match="锚行前分隔畸形"):
        B.pack_r40(_w(tmp_path, "gap.py", t37 + block.lstrip("\n")),
                   out_dir=str(tmp_path / "o3"))
    with pytest.raises(ValueError, match="R40_LOT_CHANGE_TABLE"):
        B.pack_r40(_w(tmp_path, "badc.py",
                      t40 + _comment(rows) + _comment(rows)),
                   out_dir=str(tmp_path / "o4"))
    with pytest.raises(ValueError, match="R40_LOT_CHANGE_TABLE"):
        B.pack_r40(_w(tmp_path, "badj.py",
                      t40 + _LOT_MARKER + " {not json\n"),
                   out_dir=str(tmp_path / "o5"))
    with pytest.raises(FileNotFoundError):
        B.pack_r40(str(tmp_path / "missing.py"), out_dir=str(tmp_path / "o6"))


def test_pack_r40_double_run_mismatch_raises(monkeypatch):
    # ⑥负向钉：双跑不等即抛 RuntimeError 且不落盘。
    import orderbook_2965_adopt.build_adopt as _ba
    orig = _ba.build_tar_bytes
    state = {"n": 0}

    def fake_tar(text):
        state["n"] += 1
        return orig(text) + b"\x00" * state["n"]   # 第二次多一字节

    monkeypatch.setattr(_ba, "build_tar_bytes", fake_tar)
    t37, base_text, rows, main_text, inj = _injected_pair()
    import os as _os
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        main = _os.path.join(td, "main.py")
        with open(main, "w", encoding="utf-8") as fh:
            fh.write(main_text)
        with pytest.raises(RuntimeError, match="双跑不一致"):
            B.pack_r40(main, out_dir=td)
        assert not _os.path.exists(_os.path.join(td, "submission.tar.gz"))


# ------------------------- build 组（build_r40） -------------------------

def test_build_r40(tmp_path, monkeypatch):
    # ①编排全流程集成+②输入字节不变：卖单手术→变更表注释→建库（桩）→注入→
    # 审计→打包真链；产物三件+返回八键+三 sha 对账（inject/audit/pack 互证）。
    _patch_lib(monkeypatch, _mini_lib())
    src = tmp_path / "r37_main.py"
    src.write_text(_blob_text(_lot_pkg()), encoding="utf-8", newline="\n")
    before = src.read_bytes()
    out = tmp_path / "out"
    res = B.build_r40(str(src), out_dir=str(out))
    assert src.read_bytes() == before                        # ②输入字节不变

    for name in ("main.py", "submission.tar.gz", "build_manifest.json"):
        assert (out / name).is_file()
    assert set(res) == {"main_path", "main_sha256", "tar_sha256", "manifest",
                        "diff_attribution", "block_sha", "library_sha256",
                        "sell_lots_change_sha256"}
    raw = (out / "main.py").read_bytes()
    assert res["main_path"] == str(out / "main.py")
    assert res["main_sha256"] == hashlib.sha256(raw).hexdigest()
    assert res["tar_sha256"] == hashlib.sha256(
        (out / "submission.tar.gz").read_bytes()).hexdigest()

    m = res["manifest"]
    assert m == json.loads((out / "build_manifest.json").read_text(
        encoding="utf-8"))
    assert m["schema"] == "orderbook_r40_manifest/1.0" and m["complete"] is True
    assert m["base_sha_chain"]["r40"] == res["main_sha256"]
    assert m["base_sha_chain"]["r37"] == hashlib.sha256(
        raw[:len(raw) - m["runtime_block"]["bytes"]]).hexdigest()

    # 变更表注释单行在 base 内（变更表 sha 对注释 canonical）
    marks = [ln for ln in raw.decode("utf-8").splitlines()
             if ln.startswith(_LOT_MARKER)]
    assert len(marks) == 1
    rows = json.loads(marks[0][len(_LOT_MARKER):])
    # 缺省参数（目标 337）：跨拍批量化不触发，同拍并单恰 1 行（WOOL@505 k=2→1）
    assert len(rows) == 1 and all(r["kind"] == "sell_lots" for r in rows)
    assert rows[0]["item"] == "WOOL" and rows[0]["from_steps"] == [505, 505]
    assert rows[0]["qty"] == 3 and rows[0]["to_step"] == 505
    assert res["sell_lots_change_sha256"] == _canon_sha(rows) \
        == m["sell_lots_change_sha256"]

    # 两类归因+三 sha 互证（inject=audit=pack）
    att = res["diff_attribution"]
    assert att["ok"] is True and att["unattributed"] == []
    assert set(att["whitelist"]) == {"runtime_block", "sell_lots"}
    assert att["whitelist"]["runtime_block"]["sha256"] == res["block_sha"] \
        == m["runtime_block"]["sha256"]
    assert att["whitelist"]["sell_lots"]["rows"] == len(rows)
    assert res["library_sha256"] == _canon_sha(_mini_lib()) \
        == m["route_library_sha256"]
    # r37 零改动语义：sell_lots 变更表只登记 kind=sell_lots、路由级差异对账过
    assert att["whitelist"]["sell_lots"]["changed_routes"] == ["0"]


def test_build_r40_deterministic_two_runs(tmp_path, monkeypatch):
    # ③确定性：同输入两次 build→main/tar/block/library/lot sha 全同。
    _patch_lib(monkeypatch, _mini_lib())
    src = tmp_path / "r37_main.py"
    src.write_text(_blob_text(_lot_pkg()), encoding="utf-8", newline="\n")
    r1 = B.build_r40(str(src), out_dir=str(tmp_path / "o1"))
    r2 = B.build_r40(str(src), out_dir=str(tmp_path / "o2"))
    for k in ("main_sha256", "tar_sha256", "block_sha", "library_sha256",
              "sell_lots_change_sha256"):
        assert r1[k] == r2[k], k
    assert (tmp_path / "o1" / "main.py").read_bytes() \
        == (tmp_path / "o2" / "main.py").read_bytes()


def test_build_r40_failure_no_artifacts(tmp_path, monkeypatch):
    # ④异常不落盘（B18 同款）：审计红/缺文件→out 目录零产物。

    def _boom(r40_main, r37_main, change_table=None):
        raise RuntimeError("audit 红（测试注入）")

    _patch_lib(monkeypatch, _mini_lib())
    src = tmp_path / "r37_main.py"
    src.write_text(_blob_text(_lot_pkg()), encoding="utf-8", newline="\n")
    _patch_audit(monkeypatch, _boom)
    out = tmp_path / "out"
    with pytest.raises(RuntimeError, match="audit 红"):
        B.build_r40(str(src), out_dir=str(out))
    assert not (out / "main.py").exists()
    assert not (out / "submission.tar.gz").exists()
    assert not (out / "build_manifest.json").exists()
    monkeypatch.undo()
    with pytest.raises(FileNotFoundError):
        B.build_r40(str(tmp_path / "missing.py"), out_dir=str(out))
    assert not (out / "main.py").exists()


# --------------------------- 真跑（真 r37+真库） ---------------------------

def test_build_r40_realrun():
    # 真跑验收：orderbook_r37/build/main.py + kagr23/kagr22/analysis24 败局
    # 12 局真库（77 局 49 族）→ orderbook_r40/build/ 三件产物 +
    # evidence/build_r40_realrun.json（sha 摘要/归因/双跑）。
    if not (Path("/tmp/kagr23").is_dir() and Path("/tmp/kagr22").is_dir()
            and Path("/tmp/kagr24").is_dir()):
        pytest.skip("真跑语料缺失: /tmp/kagr23 /tmp/kagr22 /tmp/kagr24")
    src = _KSIM / "orderbook_r37" / "build" / "main.py"
    before = src.read_bytes()
    res = B.build_r40(str(src))            # out_dir=None → 本包 build/
    assert src.read_bytes() == before                        # r37 零改动
    out = _HERE / "build"
    for name in ("main.py", "submission.tar.gz", "build_manifest.json"):
        assert (out / name).is_file()
    m = res["manifest"]
    assert m["complete"] is True
    att = res["diff_attribution"]
    assert att["ok"] is True and att["unattributed"] == []
    rb = att["whitelist"]["runtime_block"]
    sl = att["whitelist"]["sell_lots"]
    assert rb["present"] is True and rb["sha256"] == res["block_sha"]
    # 真跑数字钉（真库 77 局 49 族 + 卖单手术 529 行——B32 修订
    # cross_step=False 只同拍并单零时序移动[合并合没时机机制修正]）
    assert res["library_sha256"] == _REAL_LIB_SHA
    ev_lib = json.loads((_HERE / "evidence" / "route_library_realrun.json")
                        .read_text(encoding="utf-8"))
    assert res["library_sha256"] == ev_lib["build_audit"]["library_sha"]
    assert sl["present"] is True and sl["rows"] == 529
    assert sl["sha256"] == res["sell_lots_change_sha256"] \
        == m["sell_lots_change_sha256"]
    assert m["double_run_sha256"]["run1"] == m["double_run_sha256"]["run2"] \
        == res["tar_sha256"]

    ev = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "generated_by": "build_r40_realrun",
        "r37_main_path": "orderbook_r37/build/main.py",
        "corpus": {"dirs": list(B.CORPUS_DIRS),
                   "loss_ids": list(B.LOSS_IDS),
                   "loss_search_dirs": list(B.LOSS_SEARCH_DIRS),
                   "n_files": len(B._corpus_files())},
        "sha_summary": {
            "r37_main_sha256": hashlib.sha256(before).hexdigest(),
            "main_sha256": res["main_sha256"],
            "tar_sha256": res["tar_sha256"],
            "block_sha256": res["block_sha"],
            "route_library_sha256": res["library_sha256"],
            "sell_lots_change_sha256": res["sell_lots_change_sha256"],
            "base_node_r37": m["base_sha_chain"]["r37"],
        },
        "diff_attribution": att,
        "double_run_sha256": m["double_run_sha256"],
        "sell_lots_summary": {"rows": sl["rows"],
                              "n_changed": len(sl["changed_routes"]),
                              "changed_routes": sl["changed_routes"]},
        "build": res,
    }
    ev_path = _HERE / "evidence" / "build_r40_realrun.json"
    ev_path.write_text(json.dumps(ev, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8")
