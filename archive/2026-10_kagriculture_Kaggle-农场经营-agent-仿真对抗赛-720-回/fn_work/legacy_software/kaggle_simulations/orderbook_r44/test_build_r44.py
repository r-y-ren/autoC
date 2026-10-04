# -*- coding: utf-8 -*-
"""R27 构建面测试（B45）：三形态产物/AB 链序（gate 外层）/三道写入前防线
（拒原件/判重/纯净副本）/审计白名单外即抛/确定性双跑逐字节/sha 链登记。

单测用合成基座（小脚本、末函数可捕获）；另含对真实 r40 main 的构建冒烟
（产物落 /tmp/r44_smoke/orderbook_r44_{a,b,ab}）。
"""
from __future__ import annotations

import glob
import hashlib
import importlib
import json
from pathlib import Path

import pytest

from orderbook_r44 import build_r44 as b44

_THIS = Path(__file__).resolve().parent

# 合成基座（单测口径：末函数可捕获、恰一换行收尾、末行非注释）
SYNTH_BASE = (
    "# 合成基座（test_build_r44 单测用）\n"
    "def synth_entry(observation, configuration=None):\n"
    "    return {'farmer': [], 'hands': [], 'market': []}\n"
)


def _sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def _exec_main(src: str):
    """装载注入后源码：返回 (ns, 末 callable 名)（双下划线样板名排除）。"""
    ns = {}
    exec(compile(src, "<test-build-r44>", "exec"), ns)  # noqa: S102
    loaded = [v for k, v in ns.items()
              if callable(v) and not (k.startswith("__") and k.endswith("__"))]
    return ns, (loaded[-1].__name__ if loaded else None)


def _r40_main() -> Path:
    """glob 定位真实 r40 构建底（战役根下 orderbook_r40/build/main.py）。"""
    pat = str(_THIS.parent / "orderbook_r40" / "build" / "main.py")
    hits = sorted(glob.glob(pat))
    return Path(hits[0]) if hits else Path(pat)


@pytest.fixture()
def synth_base(tmp_path):
    p = tmp_path / "synth_main.py"
    p.write_text(SYNTH_BASE, encoding="utf-8")
    return p


# ---------------------------------------------------------------- 构建编排 --

def test_build_r44_variant(synth_base, tmp_path):
    """三形态各产出 main+submission.tar.gz+build_manifest.json（合成基座）。
    描述文案按形态原文；tar 成员恰 ["main.py"]；基座原件零改动。"""
    base_before = synth_base.read_bytes()
    for form, desc in (("A", "public derivative with day-high realization"),
                       ("B", "public derivative with glut gate"),
                       ("AB", "public derivative with day-high realization "
                              "/ glut gate")):
        out = tmp_path / ("out_" + form)
        res = b44.build_r44_variant(str(synth_base), form, out)
        main_p = out / "main.py"
        tar_p = out / "submission.tar.gz"
        man_p = out / "build_manifest.json"
        assert main_p.is_file() and tar_p.is_file() and man_p.is_file()
        m = json.loads(man_p.read_text(encoding="utf-8"))
        assert m["schema"] == b44.SCHEMA
        assert m["form"] == form
        assert m["variant"] == "r44_" + form.lower()
        assert m["description"] == desc
        assert m["complete"] is True
        assert m["main_sha256"] == _sha(main_p.read_bytes()) == res["main_sha256"]
        assert m["tar_members"] == ["main.py"]
        assert m["tar_sha256"] == _sha(tar_p.read_bytes())
        # 磁带五区零改动登记（合成基座无 blob 记 null 不造假）
        assert m["audit"]["whitelist"] == ["tail_block_injection"]
        assert m["audit"]["tape_five_zones_unchanged"] is True
    # 拒原件侧面：全链后基座原件逐字节零改动
    assert synth_base.read_bytes() == base_before


def test_build_r44_variant_ab_chain_gate_outer(synth_base, tmp_path):
    """AB 链序：dayhigh 内层、glutgate 外层——_GG_HOST 捕获 _dayhigh_agent
    （门作用于含追加单的最终列表）；末 callable=_glutgate_agent。"""
    res = b44.build_r44_variant(str(synth_base), "AB", tmp_path / "ab")
    src = Path(res["main_path"]).read_text(encoding="utf-8")
    assert src.index(b44._DH_MARKER) < src.index(b44._GG_MARKER)  # 块序
    ns, last = _exec_main(src)
    assert last == "_glutgate_agent"
    assert ns["_GG_HOST"] is ns["_dayhigh_agent"]      # gate 包 dayhigh（外层）
    assert ns["_DH_HOST"] is ns["synth_entry"]        # dayhigh 捕获宿主末函数
    # 单层形态：各捕获宿主、末 callable 为本层入口
    ra = b44.build_r44_variant(str(synth_base), "A", tmp_path / "a")
    nsa, lasta = _exec_main(Path(ra["main_path"]).read_text(encoding="utf-8"))
    assert lasta == "_dayhigh_agent"
    assert nsa["_DH_HOST"] is nsa["synth_entry"]
    rb = b44.build_r44_variant(str(synth_base), "B", tmp_path / "b")
    nsb, lastb = _exec_main(Path(rb["main_path"]).read_text(encoding="utf-8"))
    assert lastb == "_glutgate_agent"
    assert nsb["_GG_HOST"] is nsb["synth_entry"]


def test_build_r44_variant_audit_whitelist_raises(synth_base, tmp_path, monkeypatch):
    """审计白名单外即抛：注入块外被塞入改动→RuntimeError 且不产出。"""
    orig = b44.append_dayhigh_block
    monkeypatch.setattr(b44, "append_dayhigh_block",
                        lambda s: orig(s) + "\nX = 1\n")
    out = tmp_path / "out"
    with pytest.raises(RuntimeError, match="白名单"):
        b44.build_r44_variant(str(synth_base), "A", out)
    assert not out.exists()  # 失败路径不产出


def test_build_r44_variant_double_run_deterministic(synth_base, tmp_path):
    """双跑逐字节一致：两次独立构建的 main/tar 逐字节相同（确定性双跑）。"""
    r1 = b44.build_r44_variant(str(synth_base), "AB", tmp_path / "d1")
    r2 = b44.build_r44_variant(str(synth_base), "AB", tmp_path / "d2")
    assert Path(r1["main_path"]).read_bytes() == Path(r2["main_path"]).read_bytes()
    assert Path(r1["tar_path"]).read_bytes() == Path(r2["tar_path"]).read_bytes()
    assert r1["main_sha256"] == r2["main_sha256"]
    assert r1["tar_sha256"] == r2["tar_sha256"]
    m = r1["manifest"]
    assert m["double_run_sha256"]["run1"] == m["double_run_sha256"]["run2"] \
        == m["tar_sha256"]


def test_build_r44_variant_double_run_mismatch_raises(synth_base, tmp_path,
                                                      monkeypatch):
    """双跑不一致即抛（monkeypatch 打包配方源）且不产出。"""
    ba = importlib.import_module("orderbook_2965_adopt.build_adopt")

    def _rogue(main_bytes):
        _rogue.n += 1
        return b"tar-run-%d" % _rogue.n

    _rogue.n = 0
    monkeypatch.setattr(ba, "build_tar_bytes", _rogue)
    out = tmp_path / "out"
    with pytest.raises(RuntimeError, match="双跑"):
        b44.build_r44_variant(str(synth_base), "A", out)
    assert not out.exists()


def test_build_r44_variant_sha_chain_registered(synth_base, tmp_path):
    """sha 链登记（…→r34a→r40→r44_*）字段在：链节点/双跑哈希/块 sha 齐。"""
    res = b44.build_r44_variant(str(synth_base), "A", tmp_path / "out")
    m = res["manifest"]
    chain = m["base_sha_chain"]
    base_sha = _sha(synth_base.read_bytes())
    assert chain["r34a"] == b44.UPSTREAM_CHAIN["r34a"]
    assert chain["a16e0e9b"] == b44.UPSTREAM_CHAIN["a16e0e9b"]
    assert chain["r40"] == base_sha == m["base_main_sha256"]
    assert chain["r44_a"] == m["main_sha256"]
    assert m["base_matches_flying_r40"] is (base_sha == b44.FLYING_R40_SHA256)
    assert set(m["double_run_sha256"]) == {"run1", "run2"}
    assert m["blocks"]["dayhigh"]["sha256"] and m["blocks"]["dayhigh"]["bytes"] > 0
    assert "glutgate" not in m["blocks"]


# ------------------------------------------------------------- 注入（append） --

def test_append_dayhigh_block(synth_base):
    """dayhigh 尾块形态：quote_context 源+dayhigh 层源按序拼接；块首捕获
    _DH_HOST=宿主末函数；块尾封口 _dayhigh_agent 成新末 callable；append-only。"""
    out = b44.append_dayhigh_block(SYNTH_BASE)
    assert out.startswith(SYNTH_BASE)                       # append-only 前缀
    assert out.endswith(b44._DH_SEAL)                       # 块尾封口收尾
    q_src = (_THIS / "quote_context.py").read_text(encoding="utf-8")
    day_src = (_THIS / "dayhigh_layer.py").read_text(encoding="utf-8")
    i_head = out.index(b44._DH_HEAD)
    i_q = out.index(q_src)
    i_day = out.index(day_src)
    assert i_head < i_q < i_day                              # 按序拼接
    ns, last = _exec_main(out)
    assert last == "_dayhigh_agent"
    assert ns["_DH_HOST"] is ns["synth_entry"]               # 捕获原末函数


def test_append_glutgate_block(synth_base):
    """glutgate 尾块形态：B=单独层（_GG_HOST=宿主末函数）；AB=接在 dayhigh 之外
    层（_GG_HOST=_dayhigh_agent）；防线同 dayhigh。"""
    out_b = b44.append_glutgate_block(SYNTH_BASE)
    assert out_b.startswith(SYNTH_BASE) and out_b.endswith(b44._GG_SEAL)
    ns_b, last_b = _exec_main(out_b)
    assert last_b == "_glutgate_agent"
    assert ns_b["_GG_HOST"] is ns_b["synth_entry"]
    # AB 前置态：dayhigh 之后追加→gate 外层
    out_ab = b44.append_glutgate_block(b44.append_dayhigh_block(SYNTH_BASE))
    ns_ab, last_ab = _exec_main(out_ab)
    assert last_ab == "_glutgate_agent"
    assert ns_ab["_GG_HOST"] is ns_ab["_dayhigh_agent"]


def test_inject_prewrite_guards_dayhigh(synth_base):
    """三道写入前防线（dayhigh）：①拒原件（文件/字节指代即拒+原件零写盘）
    ②判重 ③纯净副本（残块/外来块/坏源/收尾漂移即拒）。"""
    before = synth_base.read_bytes()
    # ① 拒原件：原件/文件指代只读（非候选源文本的 Path/bytes/None 一律拒）
    for bad in (synth_base, b"raw bytes", None):
        with pytest.raises(ValueError, match="refusing to inject"):
            b44.append_dayhigh_block(bad)
    assert synth_base.read_bytes() == before                 # 原件零写盘
    # ② 判重：重复注入拒绝
    once = b44.append_dayhigh_block(SYNTH_BASE)
    with pytest.raises(ValueError, match="already injected"):
        b44.append_dayhigh_block(once)
    # ③ 纯净副本：漂移形态各拒
    with pytest.raises(ValueError, match="非纯净副本"):
        b44.append_dayhigh_block(SYNTH_BASE + "# drift\n")   # 先例漂移形态
    with pytest.raises(ValueError, match="非纯净副本"):
        b44.append_dayhigh_block("def broken(:\n")           # 坏源
    with pytest.raises(ValueError, match="非纯净副本"):
        b44.append_dayhigh_block(SYNTH_BASE[:-1])            # 收尾漂移
    with pytest.raises(ValueError, match="非纯净副本"):
        b44.append_dayhigh_block("X = 1\n")                  # 无可捕获末函数
    gg = b44.append_glutgate_block(SYNTH_BASE)
    with pytest.raises(ValueError, match="非纯净副本"):
        b44.append_dayhigh_block(gg)                         # 外来块（链序错）


def test_inject_prewrite_guards_glutgate(synth_base):
    """三道写入前防线（glutgate）：①拒原件 ②判重 ③纯净副本（dayhigh 残块即拒；
    完整 dayhigh 前置态放行）。"""
    before = synth_base.read_bytes()
    for bad in (synth_base, b"raw bytes", None):
        with pytest.raises(ValueError, match="refusing to inject"):
            b44.append_glutgate_block(bad)
    assert synth_base.read_bytes() == before
    once = b44.append_glutgate_block(SYNTH_BASE)
    with pytest.raises(ValueError, match="already injected"):
        b44.append_glutgate_block(once)
    with pytest.raises(ValueError, match="already injected"):
        b44.append_glutgate_block(
            b44.append_glutgate_block(b44.append_dayhigh_block(SYNTH_BASE)))
    # 残块：dayhigh 头在而块不完整→拒
    with pytest.raises(ValueError, match="非纯净副本"):
        b44.append_glutgate_block(SYNTH_BASE + "\n\n" + b44._DH_HEAD)
    with pytest.raises(ValueError, match="非纯净副本"):
        b44.append_glutgate_block(SYNTH_BASE + "# drift\n")
    with pytest.raises(ValueError, match="非纯净副本"):
        b44.append_glutgate_block("X = 1\n")


# ------------------------------------------------------------ 真实 r40 冒烟 --

def test_build_smoke_real_r40(tmp_path):
    """对真实 r40 main 的构建冒烟：三形态落 /tmp/r44_smoke/orderbook_r44_*；
    在飞件身份链=4ce951f0…；A 形态宿主捕获=_route40_agent。"""
    base = _r40_main()
    if not base.is_file():
        pytest.skip("r40 构建底不存在: %s" % base)
    before = base.read_bytes()
    smoke_root = Path("/tmp/r44_smoke")
    for form in ("A", "B", "AB"):
        out = smoke_root / b44.FORM_DIRS[form]
        res = b44.build_r44_variant(str(base), form, out)
        m = res["manifest"]
        assert m["base_matches_flying_r40"] is True
        assert m["base_sha_chain"]["r40"] == b44.FLYING_R40_SHA256
        assert (out / "main.py").is_file()
        assert (out / "submission.tar.gz").is_file()
        assert (out / "build_manifest.json").is_file()
        assert m["main_sha256"] == _sha((out / "main.py").read_bytes())
        assert m["tar_sha256"] == _sha((out / "submission.tar.gz").read_bytes())
    ns, last = _exec_main(
        (smoke_root / b44.FORM_DIRS["A"] / "main.py").read_text(encoding="utf-8"))
    assert last == "_dayhigh_agent"
    assert ns["_DH_HOST"].__name__ == "_route40_agent"   # 真基座末函数捕获
    assert base.read_bytes() == before                   # r40 在飞件零改动
