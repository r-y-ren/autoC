"""prune_mainline_import_graph 镜像测试（tmp 假树）：import 图构建/违例检出
（绝对/from-import 名/子模块/动态字面量/相对导入）/strict 抛/传递面披露/
fail-closed/旧树只读消费面扫描（direct+transitive）。"""

import pytest

from downgrade_dormant_assets.prune_mainline_import_graph import (
    DESIGNATED_ZONE_MEMBERS,
    MainlineImportViolationError,
    ZONE_DORMANT_LAB,
    ZONE_TEST_ASSET,
    build_import_graph,
    prune_mainline_import_graph,
    scan_legacy_consumers,
    transitive_member_exposure,
)

_MEMBERS = DESIGNATED_ZONE_MEMBERS  # R13/R14 指定四件


def _mk(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


# ---------------- 主线违例检出 ----------------

def test_violations_absolute_from_import_and_clean_neighbors(tmp_path):
    root = tmp_path / "mainline"
    _mk(root, "app.py", "import kgenv.gym_env\n")
    _mk(root, "mod_from_parent.py", "from kgenv.bots import llm_provider\n")
    _mk(root, "mod_from_import.py", "from kgenv.economy import CROPS\n")
    _mk(root, "clean.py",
        "import os\nimport kgenv.arena\nfrom kgenv import arena\n"
        "from kgenv.arena import run_match\n")

    graph, violations = prune_mainline_import_graph(root, zone_members=_MEMBERS)

    by_member = {v["member"]: v for v in violations}
    assert set(by_member) == {"kgenv.gym_env", "kgenv.bots.llm_provider",
                              "kgenv.economy"}
    v = by_member["kgenv.gym_env"]
    assert (v["importer"], v["line"], v["zone"]) == ("app.py", 1,
                                                     ZONE_DORMANT_LAB)
    assert v["stmt"] == "import kgenv.gym_env"
    assert by_member["kgenv.bots.llm_provider"]["imported"] \
        == "kgenv.bots.llm_provider"  # from P import N 形态解析为模块名导入
    assert by_member["kgenv.economy"]["zone"] == ZONE_TEST_ASSET
    # 干净邻居（kgenv 本体/arena/from-import 函数名）不命中
    assert all(v["importer"] != "clean.py" for v in violations)
    assert graph["counts"]["files"] == 4


def test_dynamic_literal_and_submodule_prefix_violations(tmp_path):
    root = tmp_path / "mainline"
    _mk(root, "dyn.py", "import importlib\n"
        "mod = importlib.import_module('kgenv.redlines')\n")
    _mk(root, "sub.py", "import kgenv.gym_env.helper\n")
    _mk(root, "dunder.py", "m = __import__('kgenv.economy')\n")

    _, violations = prune_mainline_import_graph(root, zone_members=_MEMBERS)
    assert {(v["member"], v["importer"]) for v in violations} == {
        ("kgenv.redlines", "dyn.py"), ("kgenv.gym_env", "sub.py"),
        ("kgenv.economy", "dunder.py")}


def test_clean_mainline_zero_violations_and_graph_shape(tmp_path):
    root = tmp_path / "mainline"
    _mk(root, "pkg/__init__.py", "")
    _mk(root, "pkg/tool.py", "import json\nimport kgenv.arena\n")
    _mk(root, "solo.py", "from kgenv.arena import run_match\n")

    graph, violations = prune_mainline_import_graph(root, zone_members=_MEMBERS)
    assert violations == []
    assert graph["counts"] == {"files": 3, "declared_imports": 3}
    tool = graph["files"]["pkg/tool.py"]
    assert tool["module"] == "pkg.tool"
    assert [(e["target"], e["names"]) for e in tool["imports"]] == [
        ("json", []), ("kgenv.arena", [])]
    solo = graph["files"]["solo.py"]
    assert solo["module"] == "solo"
    # from-import 一条边（target=P）附 from 名单；函数名不展开为伪模块边
    assert [(e["target"], e["names"]) for e in solo["imports"]] == [
        ("kgenv.arena", ["run_match"])]


def test_strict_raises_with_violations_attached(tmp_path):
    root = tmp_path / "mainline"
    _mk(root, "bad.py", "import kgenv.redlines\n")
    _mk(root, "good.py", "import os\n")

    with pytest.raises(MainlineImportViolationError) as exc_info:
        prune_mainline_import_graph(root, zone_members=_MEMBERS, strict=True)
    assert exc_info.value.violations[0]["member"] == "kgenv.redlines"
    assert "kgenv.redlines" in str(exc_info.value)


def test_strict_clean_tree_returns_normally(tmp_path):
    root = tmp_path / "mainline"
    _mk(root, "good.py", "import os\n")
    graph, violations = prune_mainline_import_graph(
        root, zone_members=_MEMBERS, strict=True)
    assert violations == [] and graph["counts"]["files"] == 1


def test_fail_closed_missing_or_empty_root(tmp_path):
    with pytest.raises(ValueError, match="不存在或非目录"):
        prune_mainline_import_graph(tmp_path / "nowhere",
                                    zone_members=_MEMBERS)
    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(ValueError, match="无 .py 文件"):
        prune_mainline_import_graph(empty, zone_members=_MEMBERS)
    bad = tmp_path / "bad"
    _mk(bad, "broken.py", "def (:\n")
    with pytest.raises(ValueError, match="源码解析失败"):
        prune_mainline_import_graph(bad, zone_members=_MEMBERS)
    ok = tmp_path / "ok"
    _mk(ok, "a.py", "import os\n")
    with pytest.raises(ValueError, match="zone_members 为空"):
        prune_mainline_import_graph(ok, zone_members={})


# ---------------- 旧树只读消费面扫描（tmp 假旧树镜像关键形态） ----------------

@pytest.fixture()
def fake_software(tmp_path):
    """假旧树：镜像 kgenv 关键 import 形态（eager init/相对导入/成员内边）。"""
    sw = tmp_path / "software"
    _mk(sw, "kgenv/__init__.py",
        "from . import economy, redlines, engine, gym_env, elo, arena\n")
    _mk(sw, "kgenv/economy.py",
        "from kaggle_environments.envs.kaggriculture.kaggriculture "
        "import CROPS\n")
    _mk(sw, "kgenv/redlines.py", "from .economy import CROPS, ANIMALS\n")
    _mk(sw, "kgenv/gym_env.py", "from .engine import FULL_EPISODE_STEPS\n")
    _mk(sw, "kgenv/engine.py", "FULL_EPISODE_STEPS = 720\n")
    _mk(sw, "kgenv/arena.py", "def run_match():\n    pass\n")
    _mk(sw, "kgenv/bots/__init__.py", "from .baseline import b\n")
    _mk(sw, "kgenv/bots/baseline.py", "b = 1\n")
    _mk(sw, "kgenv/bots/llm_provider.py", "class NullProvider:\n    pass\n")
    _mk(sw, "smoke_boot.py", "from kgenv.gym_env import KaggricultureGym\n")
    _mk(sw, "scripts/run_llm_ab.py",
        "from kgenv.bots.llm_provider import provider_from_env\n")
    _mk(sw, "scripts/arena_user.py", "import kgenv.arena\n")
    _mk(sw, "tests/test_economy.py", "from kgenv.economy import CROPS\n")
    _mk(sw, "tests/test_redlines.py", "from kgenv.redlines import check_farm\n")
    return sw


def test_legacy_scan_direct_consumers(fake_software):
    result = scan_legacy_consumers(fake_software, _MEMBERS)

    def direct(member):
        return sorted(c["consumer"] for c in result[member]["direct"])

    assert direct("kgenv.economy") == ["kgenv/__init__.py",
                                       "kgenv/redlines.py", "tests/test_economy.py"]
    assert direct("kgenv.redlines") == ["kgenv/__init__.py",
                                        "tests/test_redlines.py"]
    assert direct("kgenv.gym_env") == ["kgenv/__init__.py", "smoke_boot.py"]
    # llm_provider：仅实验脚本直连；bots/__init__ 不 eager import（默认关）
    assert direct("kgenv.bots.llm_provider") == ["scripts/run_llm_ab.py"]
    econ = [c for c in result["kgenv.economy"]["direct"]
            if c["consumer"] == "kgenv/redlines.py"][0]
    assert (econ["line"], econ["stmt"]) == (
        1, "from .economy import CROPS, ANIMALS")  # 相对导入解析为 kgenv.economy


def test_legacy_scan_transitive_via_pkg_init_and_member_edge(fake_software):
    result = scan_legacy_consumers(fake_software, _MEMBERS)

    trans = result["kgenv.economy"]["transitive"]
    # import kgenv.arena → 经 kgenv/__init__.py eager import 触达 economy
    assert {"consumer": "scripts/arena_user.py", "via": "kgenv/__init__.py",
            "member": "kgenv.economy"} in trans
    # test_redlines → import kgenv.redlines → 经 redlines 文件成员内边触达 economy
    assert {"consumer": "tests/test_redlines.py", "via": "kgenv/redlines.py",
            "member": "kgenv.economy"} in trans
    gym = result["kgenv.gym_env"]["transitive"]
    assert {"consumer": "scripts/arena_user.py", "via": "kgenv/__init__.py",
            "member": "kgenv.gym_env"} in gym
    # 消费者=披露源文件（kgenv/__init__ 自身）不进传递面
    assert all(t["consumer"] != "kgenv/__init__.py"
               for m in result.values() for t in m["transitive"])


def test_transitive_member_exposure_one_hop_semantics(fake_software):
    graph = build_import_graph(fake_software)
    # 直接声明成员者不算自身的传递消费者；非成员目标经祖先 init 披露
    assert transitive_member_exposure("kgenv.arena", graph, _MEMBERS) == [
        {"member": "kgenv.economy", "via": "kgenv/__init__.py"},
        {"member": "kgenv.gym_env", "via": "kgenv/__init__.py"},
        {"member": "kgenv.redlines", "via": "kgenv/__init__.py"}]
    # 无关目标零披露
    assert transitive_member_exposure("json", graph, _MEMBERS) == []
