# -*- coding: utf-8 -*-
"""R19/R20 测试面：inject_guard（注入校验四条）。

test_inject_cash_guard_block 真测试拆六组（责任契约 fn_docs/hybrid/
responsibility.md【R19/R20 增补】inject_cash_guard_block 行）：
①尾部追加不变量——原 main_text 逐字节前缀恒等（utf-8 字节级）、注入全文
  恰=原文+块文本、块文本以两空行分隔起（含无换行收尾的底版）；
②四条校验全过（正路）——对返回物独立复跑 compile/ast/exec-最后-callable/
  尾部追加 diff，防"跳校验假实现"；
③最后 callable=_r37_agent 单参可调+委托行为冒烟——假基座返回可观察（同
  dict 对象零干预透传、obs 同对象送达、触线时守卫真链路生效置 []）；
④block_sha 确定性——同文本两次同结果、块文本与 main_text 无关（跨输入同
  sha）、sha=块文本 utf-8 字节 sha256；
⑤校验失败即抛——非 str→TypeError、空/纯空白→ValueError、撞名→ValueError、
  校验①红（语法坏文本）/③红（exec 即抛、基座调用即抛、返回非 dict 动作）→
  RuntimeError，异常消息带「校验N红」定罪位；
⑥三函数与 cash_guard_block.py 源同步性——生成块包含三函数定义整段（纯核
  _r37_agent 受控改名 _r37_guard_core 后在块内，源文件不改名）+块尾单参数
  入口 def _r37_agent(observation)。
"""
import ast
import hashlib
import re
from pathlib import Path

import pytest  # noqa: F401

try:
    from orderbook_r37 import inject_guard
except ImportError:  # 兜底：直接以 orderbook_r37/ 为 sys.path 根跑测
    import inject_guard


def test_inject_cash_guard_block():
    # ②四条校验全过（正路）：返回物形态+独立复跑四条（防跳校验假实现）。
    main = _base_main()
    out = inject_guard.inject_cash_guard_block(main)
    assert set(out) == {"main_text", "block_sha"}
    injected = out["main_text"]
    assert isinstance(injected, str) and isinstance(out["block_sha"], str)
    assert re.fullmatch(r"[0-9a-f]{64}", out["block_sha"])
    payload = injected[len(main):]
    # ①compile() 内存编译注入全文
    compile(injected, "<verify1>", "exec")
    # ②ast.parse 注入全文
    ast.parse(injected)
    # ③exec 装载→globals 最后 callable=_r37_agent→单参冒烟
    ns = {"stub": _stub_base()}
    exec(compile(injected, "<verify3>", "exec"), ns)
    loaded = [(k, v) for k, v in ns.items()
              if callable(v) and not (k.startswith("__") and k.endswith("__"))]
    name, fn = loaded[-1]
    assert name == "_r37_agent" and fn.__name__ == "_r37_agent"
    assert isinstance(fn(_obs(step=5, money=1000.0)), dict)
    # ④diff 仅尾部追加
    assert injected.startswith(main)
    assert injected == main + payload
    assert out["block_sha"] == hashlib.sha256(payload.encode("utf-8")).hexdigest()


def test_inject_tail_append_invariant():
    # ①尾部追加不变量：原前缀逐字节一致（含无换行收尾/纯注释底版）。
    for main in (_base_main(), "X = 1", "X = 1\n\n\n", "# comment-only\n"):
        out = inject_guard.inject_cash_guard_block(main)
        injected = out["main_text"]
        payload = injected[len(main):]
        assert injected.startswith(main)
        assert injected == main + payload
        raw_main = main.encode("utf-8")
        raw_injected = injected.encode("utf-8")
        assert raw_injected[:len(raw_main)] == raw_main   # 逐字节前缀，零既有行改动
        assert raw_injected[len(raw_main):] == payload.encode("utf-8")
        assert payload.startswith("\n\n")                  # 两空行分隔形态
        assert "def _r37_agent(observation):" in payload


def test_inject_last_callable_delegation():
    # ③最后 callable=_r37_agent 单参可调+委托行为冒烟（假基座返回可观察）。
    main = "X = 1\n"          # 无 callable 底版→捕获行取到测试预置假基座
    out = inject_guard.inject_cash_guard_block(main)
    observed = []

    def _fake_parent(observation):
        observed.append(observation)
        return {"market": [["BUY_ANIMAL", "SHEEP", 1]],
                "farmer": ["PASS"], "hands": []}

    ns = {"fake_parent": _fake_parent}
    exec(compile(out["main_text"], "<delegation>", "exec"), ns)
    loaded = [(k, v) for k, v in ns.items()
              if callable(v) and not (k.startswith("__") and k.endswith("__"))]
    assert loaded[-1][0] == "_r37_agent"                  # 恰为最后 callable
    entry = loaded[-1][1]

    # 委托冒烟（触线路径）：假基座被单参调用一次、obs 同对象送达，
    # BUY_ANIMAL 执行点现金 100<500 触线→守卫真链路顺延置 []。
    obs = _obs(step=10, money=100.0)
    result = entry(obs)
    assert len(observed) == 1 and observed[0] is obs
    assert result == {"market": [[]], "farmer": ["PASS"], "hands": []}
    assert result is not None

    # 零干预透传：未触线→假基座动作原对象返回（纯核零足迹，同对象身份钉住）。
    observed.clear()
    safe_holder = []

    def _safe_parent(observation):
        observed.append(observation)
        action = {"market": [["SELL", "WOOL", 1]], "farmer": ["PASS"], "hands": []}
        safe_holder.append(action)
        return action

    ns2 = {"fake_parent": _safe_parent}
    exec(compile(out["main_text"], "<delegation2>", "exec"), ns2)
    entry2 = [v for k, v in ns2.items() if callable(v)
              and not (k.startswith("__") and k.endswith("__"))][-1]
    obs2 = _obs(step=10, money=1000.0)
    result2 = entry2(obs2)
    assert len(observed) == 1 and observed[0] is obs2
    assert result2 is safe_holder[0]      # 零干预：基座动作原对象透传


def test_inject_block_sha_determinism():
    # ④block_sha 确定性：同输入两次同结果；块文本与 main_text 无关（跨输入同 sha）。
    main = _base_main()
    out1 = inject_guard.inject_cash_guard_block(main)
    out2 = inject_guard.inject_cash_guard_block(main)
    assert out1 == out2
    out3 = inject_guard.inject_cash_guard_block("Y = 2\n")
    assert out1["block_sha"] == out3["block_sha"]
    payload = out1["main_text"][len(main):]
    assert out1["block_sha"] == hashlib.sha256(payload.encode("utf-8")).hexdigest()
    assert payload == out3["main_text"][len("Y = 2\n"):]
    # 跨多次独立抽取生成的块文本逐字节同（生成确定性）
    assert payload == inject_guard.inject_cash_guard_block("Z = 3\n")["main_text"][len("Z = 3\n"):]


def test_inject_bad_input_raises():
    # ⑤校验失败即抛（不许静默）：坏输入/预检红/校验①③红。
    with pytest.raises(TypeError):
        inject_guard.inject_cash_guard_block(None)
    with pytest.raises(TypeError):
        inject_guard.inject_cash_guard_block(b"X = 1\n")
    with pytest.raises(TypeError):
        inject_guard.inject_cash_guard_block(42)
    with pytest.raises(ValueError):
        inject_guard.inject_cash_guard_block("")
    with pytest.raises(ValueError):
        inject_guard.inject_cash_guard_block("   \n\t")
    # 撞名预检：底版早绑 _r37_agent（dict 重绑序陷阱会致最后 callable 漂移）
    with pytest.raises(ValueError):
        inject_guard.inject_cash_guard_block(
            "def _r37_agent(observation):\n    return {}\n"
            "def base(observation):\n    return {}\n")
    # 校验①红：语法坏文本（预检让位，compile 定罪）
    with pytest.raises(RuntimeError, match="校验①红"):
        inject_guard.inject_cash_guard_block("if True:\n")
    # 校验③红：exec 装载即抛
    with pytest.raises(RuntimeError, match="校验③红"):
        inject_guard.inject_cash_guard_block("raise RuntimeError('dead at import')\n")
    # 校验③红：基座单参调用即抛（冒烟走不过）
    with pytest.raises(RuntimeError, match="校验③红"):
        inject_guard.inject_cash_guard_block(
            "def base(observation):\n    raise ValueError('dead base')\n")
    # 校验③红：基座单参返回非 dict 动作（冒烟判据不过）
    with pytest.raises(RuntimeError, match="校验③红"):
        inject_guard.inject_cash_guard_block(
            "def base(observation):\n    return 'not-an-action'\n")
    # 同型正常态确会通过（防"一律抛"假实现）
    ok = inject_guard.inject_cash_guard_block(_base_main())
    assert ok["main_text"].startswith("# synthetic")


def test_inject_block_source_sync():
    # ⑥三函数与 cash_guard_block.py 源同步性：生成块包含三函数定义整段。
    main = "X = 1\n"
    out = inject_guard.inject_cash_guard_block(main)
    block = out["main_text"][len(main):]
    src_path = Path(inject_guard.__file__).resolve().with_name("cash_guard_block.py")
    src = src_path.read_text(encoding="utf-8")
    segs = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.FunctionDef):
            segs[node.name] = ast.get_source_segment(src, node)
    assert set(segs) == {"_r37_agent", "_r37_cash_guard", "_r37_defer_low_priority"}
    # 唯一受控改名：纯核 _r37_agent → _r37_guard_core（词边界，含函数属性账自引用）
    renamed = re.sub(r"\b_r37_agent\b", "_r37_guard_core", segs["_r37_agent"])
    assert renamed in block
    assert segs["_r37_agent"] not in block
    assert segs["_r37_cash_guard"] in block
    assert segs["_r37_defer_low_priority"] in block
    # 块内函数面：三函数定义+块尾单参数入口（入口必须最后定义）
    for name in ("def _r37_guard_core(", "def _r37_cash_guard(",
                 "def _r37_defer_low_priority("):
        assert name in block
    assert "def _r37_agent(observation):" in block
    assert block.index("def _r37_guard_core(") < block.index("def _r37_agent(observation):")
    assert block.rstrip().endswith(
        "return _r37_guard_core(observation, base_action)")
    # 捕获行机制在位：先于三函数定义执行
    assert "_R37_GUARD_PARENT = _R37_GUARD_CALLABLES[-1]" in block
    assert block.index("_R37_GUARD_PARENT = ") < block.index("def _r37_guard_core(")


def _base_main():
    """合成底版：形态贴近 r34a（尾部可 callable，last-callable 链）。"""
    return (
        "# synthetic r34a-like base\n"
        "def _base_agent(observation, configuration=None):\n"
        "    return {'farmer': ['PASS'], 'hands': [], 'market': []}\n"
        "def agent(observation, configuration=None):\n"
        "    return _base_agent(observation, configuration)\n"
    )


def _stub_base():
    """校验③式假基座（独立复跑用）。"""
    def _stub(observation):
        return {"farmer": ["PASS"], "hands": [], "market": []}
    return _stub


def _obs(step=5, money=1000.0, hires_today=0):
    """合成 kaggriculture 观测（cash_guard 读法：step/player/farms[seat]）。"""
    return {
        "step": step,
        "player": 0,
        "farms": {
            0: {"money": money, "hires_today": hires_today},
            1: {"money": 1000.0, "hires_today": 0},
        },
    }
