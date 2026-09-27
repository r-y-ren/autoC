# -*- coding: utf-8 -*-
"""R23 测试面：inject_r40（校验四条+库 sha 对账）。

test_inject_r40_block 真测试拆八组：
①尾部追加不变量——原 main_text 逐字节前缀恒等（utf-8 字节级）、块以两空行
  分隔起、锚行核心短语恰一次（含无换行收尾/纯注释/中文底版）；
②三件抽取——runtime_r40.py 三件源 ast 整段在块内（抽取序=_BLOCK_FUNCS，
  _route40_agent 单参包装钉尾）+捕获行先于 def+库行恰一行且=参数库核心 repr；
③校验四条——正路独立复跑 compile/ast/exec-末 callable/尾部逐字节追加；
④末 callable=_route40_agent 单参冒烟——假父层预置+三件链转调实证（竞速
  前移卖单/续段选择 _last_select）+无 callable 底版 PASS 兜底；
⑤block_sha 确定性——同输入同结果、块文本与 main_text 无关、库变则块 sha 变；
⑥失败即抛——坏输入/撞名预检/坏库/校验①③红；
⑦库 sha 对账——块内 canonical==参数==建库记录（route_library.build_audit.
  library_sha 口径）；改库一字节/内嵌字面量被篡→抛；
⑧真 r37 文本实跑——orderbook_r37/build/main.py 全文注入四条全过
  （真链捕获：_R40_PARENT is _r37_agent）。
"""
import ast
import copy
import hashlib
import json
import re
from pathlib import Path

import pytest  # noqa: F401

try:
    from orderbook_r40 import inject_r40
except ImportError:  # 兜底：直接以 orderbook_r40/ 为 sys.path 根跑测
    import inject_r40


def test_inject_tail_append_invariant():
    # ①尾部追加不变量：原前缀逐字节一致（含无换行收尾/纯注释/中文底版）。
    lib = _lib()
    for main in (_base_main(), "X = 1", "X = 1\n\n\n", "# comment-only\n",
                 "V = '中文尾版'\n"):
        out = inject_r40.inject_r40_block(main, lib)
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
            "\n\n# ============ r40 运行时尾块（自动生成，勿手改） ============\n")
        assert "def _route40_agent(" in payload
        assert payload.count("r40 运行时尾块") == 1        # 锚行核心短语恰一次


def test_inject_three_funcs_extraction_and_library_embed():
    # ②三件抽取：runtime_r40.py 三件源 ast 整段按 _BLOCK_FUNCS 序在块内、
    # _route40_agent 单参包装钉尾、捕获行先于一切 def；库行恰一行=参数核心。
    assert inject_r40._BLOCK_FUNCS == (
        "_route40_select", "apply_race_slots", "apply_slot_hygiene")
    assert {"_route40_select", "apply_race_slots", "apply_slot_hygiene",
            "_route40_agent", "_R40_CALLABLES", "_R40_PARENT",
            "_R40_LIBRARY"} <= inject_r40._BLOCK_BOUND    # 撞名预检含全集
    main, lib = _base_main(), _lib()
    out = inject_r40.inject_r40_block(main, lib)
    assert set(out) == {"main_text", "block_sha"}
    assert re.fullmatch(r"[0-9a-f]{64}", out["block_sha"])
    payload = out["main_text"][len(main):]
    src_path = Path(inject_r40.__file__).resolve().with_name("runtime_r40.py")
    src = src_path.read_text(encoding="utf-8")
    segs = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.FunctionDef):
            segs[node.name] = ast.get_source_segment(src, node)
    assert set(segs) == set(inject_r40._BLOCK_FUNCS)   # runtime_r40=三件真源
    for name in inject_r40._BLOCK_FUNCS:
        assert segs[name] in payload
    pos = [payload.index(segs[n]) for n in inject_r40._BLOCK_FUNCS]
    assert pos == sorted(pos)                              # 三件按抽取序
    assert inject_r40._AGENT_SRC in payload
    assert payload.index(inject_r40._AGENT_SRC) > pos[-1]  # 包装钉尾
    assert payload.rstrip().endswith("return action")
    # 捕获行先于一切 def；库行恰一行=参数库核心 repr 字面量
    assert "_R40_CALLABLES = [v for k, v in list(globals().items())" \
           " if callable(v) and not k.startswith(\"__\")]" in payload
    assert "_R40_PARENT = _R40_CALLABLES[-1] if _R40_CALLABLES else None" \
        in payload
    assert payload.index("_R40_PARENT = ") < payload.index("def _route40_select(")
    assert payload.index("_R40_LIBRARY = ") < payload.index("def _route40_select(")
    assert payload.index("def apply_race_slots(") \
        < payload.index("def _route40_agent(")
    lib_lines = [ln for ln in payload.splitlines()
                 if ln.startswith("_R40_LIBRARY = ")]
    assert len(lib_lines) == 1
    assert lib_lines[0] == "_R40_LIBRARY = " + repr(lib)
    assert _extract_lib(payload) == lib                      # 库内嵌深等参数


def test_inject_four_checks_independent_rerun():
    # ③校验四条正路：返回物形态+独立复跑四条（防"跳校验假实现"）。
    main, lib = _base_main(), _lib()
    out = inject_r40.inject_r40_block(main, lib)
    injected = out["main_text"]
    payload = injected[len(main):]
    compile(injected, "<verify1>", "exec")                   # ①
    ast.parse(injected)                                      # ②
    ns = {"_r40_check3_stub_base": _stub_parent()}           # ③
    exec(compile(injected, "<verify3>", "exec"), ns)
    loaded = [(k, v) for k, v in ns.items()
              if callable(v) and not k.startswith("__")]
    name, fn = loaded[-1]
    assert name == "_route40_agent" and fn.__name__ == "_route40_agent"
    assert isinstance(fn(_obs()), dict)
    assert injected.startswith(main) and injected == main + payload   # ④
    raw_main, raw_injected = main.encode("utf-8"), injected.encode("utf-8")
    assert raw_injected[:len(raw_main)] == raw_main
    assert out["block_sha"] == hashlib.sha256(payload.encode("utf-8")).hexdigest()


def test_inject_last_callable_single_arg_smoke():
    # ④末 callable=_route40_agent 单参冒烟：假父层委托+三件链转调实证。
    main, lib = "X = 1\n", _lib()     # 无 callable 底版→捕获行取到测试预置假父层
    out = inject_r40.inject_r40_block(main, lib)
    observed = []

    def _fake_parent(observation):
        observed.append(observation)
        return {"farmer": ["PASS"], "hands": [],
                "market": [[], ["SELL", "MILK", 3]]}

    ns = {"fake_parent": _fake_parent}
    exec(compile(out["main_text"], "<smoke>", "exec"), ns)
    loaded = [(k, v) for k, v in ns.items()
              if callable(v) and not k.startswith("__")]
    assert loaded[-1][0] == "_route40_agent"              # 恰为最后 callable
    entry = loaded[-1][1]
    assert ns["_R40_PARENT"] is _fake_parent              # 捕获行取到假父层
    assert ns["_R40_LIBRARY"] == lib                      # 库内嵌深等参数库

    obs = _obs()
    result = entry(obs)                                   # 单参形态：fn(observation)
    assert isinstance(result, dict) and set(result) >= {"farmer", "hands", "market"}
    assert len(observed) == 1 and observed[0] is obs       # 父层单参同对象送达
    # apply_race_slots 链实证：SELL 单前移进空槽（总槽数/单量不变）
    assert result["market"] == [["SELL", "MILK", 3], []]
    # _route40_select 链实证：结果落 _last_select（step=5<144 → 回退形）
    sel = entry._last_select
    assert set(sel) == {"route", "family", "confidence"}
    assert sel["route"] is None and sel["confidence"] == 0.0
    # 无 callable 底版：捕获 _R40_PARENT=None → PASS 兜底
    ns2 = {}
    exec(compile(inject_r40.inject_r40_block("Y = 2\n", lib)["main_text"],
                 "<smoke2>", "exec"), ns2)
    assert ns2["_R40_PARENT"] is None
    assert ns2["_route40_agent"](obs) == {"farmer": ["PASS"], "hands": [],
                                          "market": []}


def test_inject_block_sha_determinism():
    # ⑤block_sha 确定性：同输入两次同结果；块文本与 main_text 无关；库变则块变。
    main, lib = _base_main(), _lib()
    out1 = inject_r40.inject_r40_block(main, lib)
    out2 = inject_r40.inject_r40_block(main, lib)
    assert out1 == out2
    out3 = inject_r40.inject_r40_block("Y = 2\n", lib)
    assert out1["block_sha"] == out3["block_sha"]
    payload = out1["main_text"][len(main):]
    assert payload == out3["main_text"][len("Y = 2\n"):]
    assert out1["block_sha"] == hashlib.sha256(payload.encode("utf-8")).hexdigest()
    out4 = inject_r40.inject_r40_block(main, _tampered_lib())
    assert out4["block_sha"] != out1["block_sha"]          # 库变则块 sha 变


def test_inject_bad_input_raises():
    # ⑥失败即抛（不许静默）：坏输入/预检红/坏库/校验①③红。
    main, lib = _base_main(), _lib()
    with pytest.raises(TypeError):
        inject_r40.inject_r40_block(None, lib)
    with pytest.raises(TypeError):
        inject_r40.inject_r40_block(b"X = 1\n", lib)
    with pytest.raises(TypeError):
        inject_r40.inject_r40_block(42, lib)
    with pytest.raises(ValueError):
        inject_r40.inject_r40_block("", lib)
    with pytest.raises(ValueError):
        inject_r40.inject_r40_block("   \n\t", lib)
    # 撞名预检：底版早绑块名（dict 重绑序陷阱会致末 callable 漂移/静默覆写）
    for colliding in ("def _route40_agent(observation):\n    return {}\n",
                      "_R40_PARENT = 1\n",
                      "_R40_LIBRARY = {}\n",
                      "_R40_CALLABLES = []\n",
                      "def apply_slot_hygiene(observation, action):\n    return {}\n",
                      "def apply_race_slots(observation, action):\n    return {}\n",
                      "def _route40_select(observation, library=None):\n    return {}\n"):
        with pytest.raises(ValueError, match="撞名"):
            inject_r40.inject_r40_block(colliding, lib)
    # 坏库：非 dict→TypeError；不可作 Python 字面量内嵌/不可 canonical sha→ValueError
    with pytest.raises(TypeError):
        inject_r40.inject_r40_block(main, None)
    with pytest.raises(TypeError):
        inject_r40.inject_r40_block(main, ["not-a-dict"])
    with pytest.raises(TypeError):
        inject_r40.inject_r40_block(main, 42)
    with pytest.raises(ValueError):
        inject_r40.inject_r40_block(main, {"k": {1, 2}})      # set 不可 canonical sha
    with pytest.raises(ValueError):
        inject_r40.inject_r40_block(main, {"k": object()})    # repr 非 Python 字面量
    # 校验①红：语法坏文本（预检让位，compile 定罪）
    with pytest.raises(RuntimeError, match="校验①红"):
        inject_r40.inject_r40_block("if True:\n", lib)
    # 校验③红：exec 装载即抛
    with pytest.raises(RuntimeError, match="校验③红"):
        inject_r40.inject_r40_block(
            "raise RuntimeError('dead at import')\n", lib)
    # 同型正常态确会通过（防"一律抛"假实现）
    ok = inject_r40.inject_r40_block(main, lib)
    assert ok["main_text"].startswith("# synthetic")


def test_inject_library_sha_reconcile(monkeypatch):
    # ⑦库 sha 对账：块内 == 参数 == 建库记录（route_library 记录 sha 口径）；
    # 改库一字节（记录 sha 不动）→抛；内嵌字面量被篡→抛。
    main, lib = _base_main(), _lib()
    out = inject_r40.inject_r40_block(main, lib)
    emb = _extract_lib(out["main_text"][len(main):])
    assert _sha_of(emb) == _sha_of(lib)                       # 块内 canonical==参数
    # 建库件返回形正路：内嵌=库核心（壳/构建账不入块），记录 sha 对账过
    audit = {"library_sha": _sha_of(lib), "n_games": 3}
    wrapper = {"library": dict(lib, build_audit=dict(audit)),
               "build_audit": dict(audit)}
    outw = inject_r40.inject_r40_block(main, wrapper)
    assert _extract_lib(outw["main_text"][len(main):]) == lib  # build_audit 剥离
    assert outw["block_sha"] == out["block_sha"]              # 同库同块（壳不入块）
    # ⑦a 改库一字节（win_rate）而建库记录 sha 不动 → 完整性不符即抛
    with pytest.raises(RuntimeError, match="库sha对账红"):
        inject_r40.inject_r40_block(
            main, {"library": _tampered_lib(),
                   "build_audit": {"library_sha": _sha_of(lib)}})
    # ⑦b 块侧内嵌字面量被篡（生成链路被改）→ 块侧≠参数侧即抛
    real_literal = inject_r40._library_literal

    def _corrupt_literal(obj):
        return real_literal(obj).replace("'n_games'", "'n_game5'", 1)

    monkeypatch.setattr(inject_r40, "_library_literal", _corrupt_literal)
    with pytest.raises(RuntimeError, match="库sha对账红"):
        inject_r40.inject_r40_block(main, lib)


def test_inject_real_r37_smoke():
    # ⑧真 r37 文本实跑：全文注入+四条独立复跑全过；真链捕获 _r37_agent。
    base_path = Path(__file__).resolve().parents[1] / "orderbook_r37" / \
        "build" / "main.py"
    main = base_path.read_text(encoding="utf-8")
    lib = _lib()
    out = inject_r40.inject_r40_block(main, lib)
    injected = out["main_text"]
    payload = injected[len(main):]
    compile(injected, "<verify1>", "exec")
    ast.parse(injected)
    ns = {"_r40_check3_stub_base": _stub_parent()}
    exec(compile(injected, "<verify3>", "exec"), ns)
    loaded = [(k, v) for k, v in ns.items()
              if callable(v) and not k.startswith("__")]
    assert loaded[-1][0] == "_route40_agent"
    assert loaded[-1][1].__name__ == "_route40_agent"
    assert ns["_R40_PARENT"] is ns["_r37_agent"]          # 底版末 callable=守卫链入口
    assert ns["_R40_LIBRARY"] == lib
    assert isinstance(loaded[-1][1](_obs()), dict)
    assert injected == main + payload                     # 尾部逐字节追加
    raw_main, raw_injected = main.encode("utf-8"), injected.encode("utf-8")
    assert raw_injected[:len(raw_main)] == raw_main
    assert out["block_sha"] == hashlib.sha256(payload.encode("utf-8")).hexdigest()
    assert main.count("r40 运行时尾块") == 0               # 底版锚行零在场


# ------------------------------ 夹具 ------------------------------

def _lib():
    """合成续段库核心（route_library lib_core 形态；含 best_route=None/
    covered=bool——repr 字面量口径实测面）。"""
    return {
        "version": "routelib/1.0",
        "families": {
            "2|1|WHEAT:5|BAKERY+FARMERS_MARKET": {
                "n_games": 3, "win_rate": 2 / 3, "margin_mean": 750.0,
                "best_route": 5,
                "segments": {"5": {"n": 3, "win_rate": 2 / 3,
                                   "margin_mean": 500.0}}},
            "1|0|MELON:3|PET_CAFE+YARN_STORE": {
                "n_games": 1, "win_rate": 0.0, "margin_mean": -100.0,
                "best_route": None, "segments": {}},
        },
        "default": {"n_games": 4, "win_rate": 0.75, "margin_mean": 537.5,
                    "best_route": 5, "segments": {}},
        "defeat_worlds": {
            "milk_flow": {"families": ["1|0|MELON:3|PET_CAFE+YARN_STORE"],
                          "covered": False},
            "wool_flow": {"families": [], "covered": True},
        },
    }


def _tampered_lib():
    """改库一字节（win_rate 0.75→0.7）：canonical sha 必变。"""
    tampered = copy.deepcopy(_lib())
    tampered["default"]["win_rate"] = 0.7
    return tampered


def _canon_sha(obj):
    """canonical json sha256（route_library.build_audit.library_sha 同口径）。"""
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"),
                   ensure_ascii=False).encode("utf-8")).hexdigest()


def _sha_of(lib):
    return _canon_sha(lib)


def _extract_lib(payload):
    """从块文本解析 _R40_LIBRARY 常量（对账口径）。"""
    for node in ast.parse(payload, filename="<payload>").body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "_R40_LIBRARY"
                for t in node.targets):
            return ast.literal_eval(ast.get_source_segment(payload, node.value))
    raise AssertionError("payload 内未找到 _R40_LIBRARY")


def _base_main():
    """合成底版：形态贴近 r37（尾部 callable，last-callable 链）。"""
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
    """合成 observation（三件链读法：step/farms/town/market.inventory）。"""
    return {
        "step": step, "day": step // 24, "hour": step % 24, "player": 0,
        "farms": [{"money": 210.0, "hands": [], "unlocked_quadrants": [],
                   "tiles": []},
                  {"money": 229.0, "hands": [], "unlocked_quadrants": [],
                   "tiles": []}],
        "market": {"inventory": {"WHEAT": 9989, "MILK": 500},
                   "prices": {"WHEAT": 25, "MILK": 160}},
        "town": {"unlocked_shops": ["BAKERY", "YARN_STORE"]},
        "private": {"shed": {}, "seeds": {}, "inventories": [{}]},
    }
