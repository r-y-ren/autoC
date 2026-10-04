# -*- coding: utf-8 -*-
"""R21 测试面：inject_predict（注入校验四条+库 sha 对账）。

test_inject_predict_block 真测试拆七组（责任契约 fn_docs/hybrid/
responsibility.md【R21 增补】inject_predict_block 行）：
①尾部追加不变量——原 main_text 逐字节前缀恒等（utf-8 字节级）、注入全文
  恰=原文+块文本、块文本以两空行分隔起（含无换行收尾/纯注释/中文底版）；
②四条校验全过（正路）——对返回物独立复跑 compile/ast/exec-末 callable/
  尾部追加 diff，防"跳校验假实现"；另验五函数源与 predict_block.py 单一
  真源逐段同步（ast.get_source_segment 整段在块内）+捕获行先于 def+库行
  恰一行且=参数库 JSON；
③末 callable=_predict_agent 单参冒烟——假父层预置（无 callable 底版供捕获）
  +合成 obs 返回 dict 动作、父层单参同对象送达、_PREDICT_LIBRARY 深等参数库；
④block_sha 确定性——同输入两次同结果、块文本与 main_text 无关（跨输入同
  sha）、sha=块文本 utf-8 字节 sha256、库变则块 sha 变；
⑤失败即抛——非 str→TypeError、空/纯空白→ValueError、撞名→ValueError、
  坏库（非 dict→TypeError；不可 JSON 内嵌/非 Python 字面量形→ValueError）、
  校验①红（语法坏文本）/③红（exec 即抛）→RuntimeError 带定罪位；
⑥库 sha 对账——块内 _PREDICT_LIBRARY canonical sha==参数库 sha==建库记录
  sha（sellflow 建库件口径）；改库一字节（记录 sha 不动）→抛、内嵌字面量
  被改一字节（块侧≠参数侧）→抛；同型未改库确会通过（防"一律抛"）；
⑦真 r37 文本实跑——orderbook_r37/build/main.py 全文注入+四条独立复跑全过
  （真链捕获：_PREDICT_PARENT is _r37_agent），evidence/inject_r38_smoke.json
  记字节/sha（r37/injected/block 字节、injected/block/library sha）。
⑧v2 块形态（B26c）——_BLOCK_FUNCS 六件序钉死（_predict_agent 钉尾）+块内
  v2 注释+锚行核心短语沿 v1 不动+六件源段按序在块内+块 sha 口径。
"""
import ast
import copy
import hashlib
import json
import re
from pathlib import Path

import pytest  # noqa: F401

try:
    from orderbook_predict import inject_predict
except ImportError:  # 兜底：直接以 orderbook_predict/ 为 sys.path 根跑测
    import inject_predict


def test_inject_tail_append_invariant():
    # ①尾部追加不变量：原前缀逐字节一致（含无换行收尾/纯注释/中文底版）。
    lib = _lib()
    for main in (_base_main(), "X = 1", "X = 1\n\n\n", "# comment-only\n",
                 "V = '中文尾版'\n"):
        out = inject_predict.inject_predict_block(main, lib)
        injected = out["main_text"]
        payload = injected[len(main):]
        assert injected.startswith(main)
        assert injected == main + payload
        raw_main = main.encode("utf-8")
        raw_injected = injected.encode("utf-8")
        assert raw_injected[:len(raw_main)] == raw_main   # 逐字节前缀，零既有行改动
        assert raw_injected[len(raw_main):] == payload.encode("utf-8")
        assert payload.startswith("\n\n")                  # 两空行分隔形态
        assert payload.startswith(
            "\n\n# ============ r38 对手预测尾块（自动生成，勿手改） ============\n")
        assert "def _predict_agent(" in payload


def test_inject_four_checks_and_source_sync():
    # ②四条校验全过（正路）：返回物形态+独立复跑四条（防跳校验假实现）。
    main, lib = _base_main(), _lib()
    out = inject_predict.inject_predict_block(main, lib)
    assert set(out) == {"main_text", "block_sha"}
    injected = out["main_text"]
    assert isinstance(injected, str) and isinstance(out["block_sha"], str)
    assert re.fullmatch(r"[0-9a-f]{64}", out["block_sha"])
    payload = injected[len(main):]
    # ①compile() 内存编译注入全文
    compile(injected, "<verify1>", "exec")
    # ②ast.parse 注入全文
    ast.parse(injected)
    # ③exec 装载→globals 最后 callable=_predict_agent→单参冒烟
    ns = {"_predict_check3_stub_base": _stub_parent()}
    exec(compile(injected, "<verify3>", "exec"), ns)
    loaded = [(k, v) for k, v in ns.items() if callable(v) and not k.startswith("__")]
    name, fn = loaded[-1]
    assert name == "_predict_agent" and fn.__name__ == "_predict_agent"
    assert isinstance(fn(_obs()), dict)
    # ④diff 仅尾部追加
    assert injected.startswith(main)
    assert injected == main + payload
    assert out["block_sha"] == hashlib.sha256(payload.encode("utf-8")).hexdigest()
    # ---- 单一真源同步：五函数源文本= predict_block.py ast 整段（零手抄） ----
    src_path = Path(inject_predict.__file__).resolve().with_name("predict_block.py")
    src = src_path.read_text(encoding="utf-8")
    segs = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.FunctionDef):
            segs[node.name] = ast.get_source_segment(src, node)
    assert set(segs) == {"detect_clone", "infer_rival_sells", "match_sellflow",
                         "extrapolate_sells", "apply_dodge", "_predict_agent"}
    for seg in segs.values():
        assert seg in payload
    # ---- 块结构：捕获行先于一切 def；_predict_agent 钉尾；库行恰一行 ----
    assert "_PREDICT_CALLABLES = [v for k, v in list(globals().items())" \
           " if callable(v) and not k.startswith(\"__\")]" in payload
    assert "_PREDICT_PARENT = _PREDICT_CALLABLES[-1] if _PREDICT_CALLABLES else None" in payload
    assert payload.index("_PREDICT_PARENT = ") < payload.index("def infer_rival_sells(")
    assert payload.index("_PREDICT_LIBRARY = ") < payload.index("def infer_rival_sells(")
    assert payload.index("def apply_dodge(") < payload.index("def _predict_agent(")
    lib_lines = [ln for ln in payload.splitlines() if ln.startswith("_PREDICT_LIBRARY = ")]
    assert len(lib_lines) == 1
    assert lib_lines[0] == "_PREDICT_LIBRARY = " + _lib_json(lib)
    assert _extract_lib(payload) == lib


def test_inject_last_callable_smoke():
    # ③末 callable=_predict_agent 单参可调+假父层委托冒烟（合成 obs 返回 dict）。
    main, lib = "X = 1\n", _lib()     # 无 callable 底版→捕获行取到测试预置假父层
    out = inject_predict.inject_predict_block(main, lib)
    observed = []
    parent_action = {"farmer": ["PASS"], "hands": [], "market": [["SELL", "MILK", 3]]}

    def _fake_parent(observation):
        observed.append(observation)
        return parent_action

    ns = {"fake_parent": _fake_parent}
    exec(compile(out["main_text"], "<smoke>", "exec"), ns)
    loaded = [(k, v) for k, v in ns.items() if callable(v) and not k.startswith("__")]
    assert loaded[-1][0] == "_predict_agent"              # 恰为最后 callable
    entry = loaded[-1][1]
    assert ns["_PREDICT_PARENT"] is _fake_parent           # 捕获行取到假父层
    assert ns["_PREDICT_LIBRARY"] == lib                   # 库内嵌深等参数库

    obs = _obs()
    result = entry(obs)                                    # 单参形态：fn(observation)
    assert isinstance(result, dict)
    assert len(observed) == 1 and observed[0] is obs        # 父层单参同对象送达
    assert result["market"] == [["SELL", "MILK", 3]]        # 置信不足→零动作不动卖单
    assert set(result) >= {"farmer", "hands", "market"}


def test_inject_block_sha_determinism():
    # ④block_sha 确定性：同输入两次同结果；块文本与 main_text 无关（跨输入同 sha）。
    main, lib = _base_main(), _lib()
    out1 = inject_predict.inject_predict_block(main, lib)
    out2 = inject_predict.inject_predict_block(main, lib)
    assert out1 == out2
    out3 = inject_predict.inject_predict_block("Y = 2\n", lib)
    assert out1["block_sha"] == out3["block_sha"]
    payload = out1["main_text"][len(main):]
    assert payload == out3["main_text"][len("Y = 2\n"):]
    assert out1["block_sha"] == hashlib.sha256(payload.encode("utf-8")).hexdigest()
    # 跨多次独立抽取生成的块文本逐字节同（生成确定性）
    assert payload == inject_predict.inject_predict_block(
        "Z = 3\n", lib)["main_text"][len("Z = 3\n"):]
    # 库内嵌进块：库变→块 sha 变
    out4 = inject_predict.inject_predict_block(main, _tampered_lib())
    assert out4["block_sha"] != out1["block_sha"]


def test_inject_bad_input_raises():
    # ⑤校验失败即抛（不许静默）：坏输入/预检红/坏库/校验①③红。
    main, lib = _base_main(), _lib()
    with pytest.raises(TypeError):
        inject_predict.inject_predict_block(None, lib)
    with pytest.raises(TypeError):
        inject_predict.inject_predict_block(b"X = 1\n", lib)
    with pytest.raises(TypeError):
        inject_predict.inject_predict_block(42, lib)
    with pytest.raises(ValueError):
        inject_predict.inject_predict_block("", lib)
    with pytest.raises(ValueError):
        inject_predict.inject_predict_block("   \n\t", lib)
    # 撞名预检：底版早绑块名（dict 重绑序陷阱会致末 callable 漂移/静默覆写）
    for colliding in ("def _predict_agent(observation):\n    return {}\n",
                      "_PREDICT_PARENT = 1\n",
                      "_PREDICT_LIBRARY = {}\n",
                      "def apply_dodge(observation, action, predictions):\n    return {}\n",
                      "def match_sellflow(observation, library):\n    return {}\n"):
        with pytest.raises(ValueError):
            inject_predict.inject_predict_block(colliding, lib)
    # 坏库：非 dict→TypeError；不可 JSON 内嵌/非 Python 字面量形→ValueError
    with pytest.raises(TypeError):
        inject_predict.inject_predict_block(main, None)
    with pytest.raises(TypeError):
        inject_predict.inject_predict_block(main, ["not-a-dict"])
    with pytest.raises(TypeError):
        inject_predict.inject_predict_block(main, 42)
    with pytest.raises(ValueError):
        inject_predict.inject_predict_block(main, {"k": {1, 2}})   # 不可 JSON 序列化
    with pytest.raises(ValueError):
        inject_predict.inject_predict_block(main, {"v": True})     # true 形非 Python 字面量
    # 校验①红：语法坏文本（预检让位，compile 定罪）
    with pytest.raises(RuntimeError, match="校验①红"):
        inject_predict.inject_predict_block("if True:\n", lib)
    # 校验③红：exec 装载即抛
    with pytest.raises(RuntimeError, match="校验③红"):
        inject_predict.inject_predict_block(
            "raise RuntimeError('dead at import')\n", lib)
    # 同型正常态确会通过（防"一律抛"假实现）
    ok = inject_predict.inject_predict_block(main, lib)
    assert ok["main_text"].startswith("# synthetic")


def test_inject_library_sha_reconcile(monkeypatch):
    # ⑥库 sha 对账：块内 == 参数 == 建库记录（sellflow 建库件口径）；改库一字节即抛。
    main, lib = _base_main(), _lib()
    out = inject_predict.inject_predict_block(main, lib)
    emb = _extract_lib(out["main_text"][len(main):])
    assert _sha_of(emb) == _sha_of(lib)                       # 块内 canonical sha==参数
    # 建库件返回形正路：内嵌=库数据本体（非包装壳），记录 sha 对账过
    wrapper = {"library": lib,
               "build_audit": {"sha256_of_library": _sha_of(lib), "n_used": 86}}
    outw = inject_predict.inject_predict_block(main, wrapper)
    assert _extract_lib(outw["main_text"][len(main):]) == lib
    assert outw["block_sha"] == out["block_sha"]              # 同库同块（壳不入块）
    # ⑥a 改库一字节（qty_sum 9→8）而建库记录 sha 不动 → 库数据完整性不符即抛
    with pytest.raises(RuntimeError, match="库sha对账红"):
        inject_predict.inject_predict_block(
            main, {"library": _tampered_lib(),
                   "build_audit": {"sha256_of_library": _sha_of(lib)}})
    # ⑥b 块侧内嵌字面量被改一字节（count→c0unt，模拟生成链路被篡改）→ 块侧≠参数侧即抛
    real_literal = inject_predict._library_literal

    def _corrupt_literal(obj):
        return real_literal(obj).replace('"count"', '"c0unt"', 1)

    monkeypatch.setattr(inject_predict, "_library_literal", _corrupt_literal)
    with pytest.raises(RuntimeError, match="库sha对账红"):
        inject_predict.inject_predict_block(main, lib)


def test_inject_v2_block_shape():
    # ⑧v2 块形态：_BLOCK_FUNCS 六件序（_predict_agent 钉尾）、块内 v2 注释、
    # 锚行核心短语沿 v1、六件源段按 _BLOCK_FUNCS 序在块内、sha 口径。
    assert inject_predict._BLOCK_FUNCS == (
        "detect_clone", "infer_rival_sells", "match_sellflow",
        "extrapolate_sells", "apply_dodge", "_predict_agent")
    assert inject_predict._BLOCK_FUNCS[-1] == "_predict_agent"
    assert "detect_clone" in inject_predict._BLOCK_BOUND   # 撞名预检含六件
    main, lib = _base_main(), _lib()
    out = inject_predict.inject_predict_block(main, lib)
    payload = out["main_text"][len(main):]
    assert payload.startswith(
        "\n\n# ============ r38 对手预测尾块（自动生成，勿手改） ============\n")
    assert "r39 v2 块内容" in payload                      # 块内 v2 注释
    src_path = Path(inject_predict.__file__).resolve().with_name("predict_block.py")
    src = src_path.read_text(encoding="utf-8")
    segs = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.FunctionDef):
            segs[node.name] = ast.get_source_segment(src, node)
    pos = [payload.index(segs[n]) for n in inject_predict._BLOCK_FUNCS]
    assert pos == sorted(pos)                              # 六件按 _BLOCK_FUNCS 序
    assert payload.index(segs["_predict_agent"]) == max(pos)   # _predict_agent 钉尾
    assert out["block_sha"] == hashlib.sha256(
        payload.encode("utf-8")).hexdigest()


def test_inject_real_r37_smoke():
    # ⑦真 r37 文本实跑：orderbook_r37/build/main.py 全文注入+四条独立复跑全过。
    base_path = Path(__file__).resolve().parents[1] / "orderbook_r37" / "build" / "main.py"
    main = base_path.read_text(encoding="utf-8")
    lib = _lib()
    out = inject_predict.inject_predict_block(main, lib)
    injected = out["main_text"]
    payload = injected[len(main):]
    # ①②compile/ast
    compile(injected, "<verify1>", "exec")
    ast.parse(injected)
    # ③exec 装载：真链捕获 _PREDICT_PARENT is _r37_agent、末 callable=_predict_agent、单参冒烟
    ns = {"_predict_check3_stub_base": _stub_parent()}
    exec(compile(injected, "<verify3>", "exec"), ns)
    loaded = [(k, v) for k, v in ns.items() if callable(v) and not k.startswith("__")]
    assert loaded[-1][0] == "_predict_agent" and loaded[-1][1].__name__ == "_predict_agent"
    assert ns["_PREDICT_PARENT"] is ns["_r37_agent"]          # 底版末 callable=守卫链入口
    assert ns["_PREDICT_LIBRARY"] == lib
    assert isinstance(loaded[-1][1](_obs()), dict)
    # ④尾部逐字节追加
    assert injected == main + payload
    raw_main, raw_injected = main.encode("utf-8"), injected.encode("utf-8")
    assert raw_injected[:len(raw_main)] == raw_main
    assert out["block_sha"] == hashlib.sha256(payload.encode("utf-8")).hexdigest()
    # evidence：字节/sha（r37/injected/block 字节、injected/block/library sha）
    ev = {
        "r37_main_path": "orderbook_r37/build/main.py",
        "r37_main_bytes": len(raw_main),
        "injected_bytes": len(raw_injected),
        "block_bytes": len(payload.encode("utf-8")),
        "r37_main_sha256": hashlib.sha256(raw_main).hexdigest(),
        "injected_sha256": hashlib.sha256(raw_injected).hexdigest(),
        "block_sha256": out["block_sha"],
        "library_sha256": _sha_of(lib),
        "last_callable": "_predict_agent",
        "n_block_funcs": 6,
    }
    assert ev["injected_bytes"] == ev["r37_main_bytes"] + ev["block_bytes"]
    ev_path = Path(__file__).resolve().parent / "evidence" / "inject_r38_smoke.json"
    ev_path.parent.mkdir(parents=True, exist_ok=True)
    ev_path.write_text(json.dumps(ev, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                       encoding="utf-8")


# ------------------------------ 夹具 ------------------------------

def _lib():
    """合成卖流库（sellflow 建库件形态：version/keys/global，键=首二店||指纹）。"""
    return {
        "version": "sellflow/1.0",
        "keys": {"BAKERY|YARN_STORE||m229_w9989": {"n_episodes": 5, "hist": {
            "1": {"MILK": {"qty_sum": 9, "count": 3, "qty_max": 4},
                  "WOOL": {"qty_sum": 2, "count": 1, "qty_max": 2}}}}},
        "global": {"n_episodes": 86, "hist": {
            "1": {"MILK": {"qty_sum": 20, "count": 8, "qty_max": 5}}}},
    }


def _tampered_lib():
    """改库一字节（qty_sum 9→8）：canonical sha 必变。"""
    tampered = copy.deepcopy(_lib())
    tampered["keys"]["BAKERY|YARN_STORE||m229_w9989"]["hist"]["1"]["MILK"]["qty_sum"] = 8
    return tampered


def _sha_of(lib):
    """canonical json sha256（sellflow 建库件同口径）。"""
    return hashlib.sha256(
        json.dumps(lib, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _lib_json(lib):
    """内嵌字面量口径（json.dumps ensure_ascii=False 紧凑）。"""
    return json.dumps(lib, ensure_ascii=False, separators=(",", ":"))


def _extract_lib(payload):
    """从块文本解析 _PREDICT_LIBRARY 常量（对账口径）。"""
    for node in ast.parse(payload, filename="<payload>").body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "_PREDICT_LIBRARY" for t in node.targets):
            return ast.literal_eval(ast.get_source_segment(payload, node.value))
    raise AssertionError("payload 内未找到 _PREDICT_LIBRARY")


def _base_main():
    """合成底版：形态贴近 r37（尾部可 callable，last-callable 链）。"""
    return (
        "# synthetic r37-like base\n"
        "def _base_agent(observation, configuration=None):\n"
        "    return {'farmer': ['PASS'], 'hands': [], 'market': []}\n"
        "def agent(observation, configuration=None):\n"
        "    return _base_agent(observation, configuration)\n"
    )


def _stub_parent():
    """校验③式假父层（独立复跑用）。"""
    def _stub(observation):
        return {"farmer": ["PASS"], "hands": [], "market": [["SELL", "MILK", 2]]}
    return _stub


def _obs(step=5):
    """合成 observation（player=0 → 对手=farms[1]；predict_block 读法）。"""
    return {
        "step": step, "day": step // 24, "hour": step % 24, "player": 0,
        "farms": [{"money": 210.0}, {"money": 229.0}],
        "market": {"inventory": {"WHEAT": 9989, "MILK": 500},
                   "prices": {"WHEAT": 25, "MILK": 160}},
        "town": {"unlocked_shops": ["BAKERY", "YARN_STORE"]},
        "private": {"shed": {}, "seeds": {}, "inventories": [{}]},
    }
