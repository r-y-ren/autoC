"""downgrade_dormant_assets 顶层镜像测试（tmp 假战役树全链编排）：四件登记
分区/schema 完整/旧树消费面入注册表/主线断言（零违例 PASS、违例如实报告
FAIL）/传递面披露不判负/缺件 fail-closed/零物理移动/注册表默认路径推导。"""

import json
from pathlib import Path

import pytest

from downgrade_dormant_assets.downgrade_dormant_assets import (
    DESIGNATION_TABLE,
    DORMANT_LAB_POSTWAR_DIR,
    REQUIRED_ENTRY_KEYS,
    TEST_ASSET_POSTWAR_DIR,
    downgrade_dormant_assets,
)


def _mk(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


@pytest.fixture()
def fake_campaign(tmp_path):
    """tmp 假战役树：software 镜像旧树关键 import 形态 + fn_work/src 干净主线。"""
    sw = tmp_path / "software"
    _mk(sw, "kgenv/__init__.py",
        "from . import economy, redlines, engine, gym_env, elo, arena\n")
    _mk(sw, "kgenv/economy.py",
        "from kaggle_environments.envs.kaggriculture.kaggriculture "
        "import CROPS\n")
    _mk(sw, "kgenv/redlines.py", "from .economy import CROPS, ANIMALS\n")
    _mk(sw, "kgenv/gym_env.py", "from .engine import FULL_EPISODE_STEPS\n")
    _mk(sw, "kgenv/engine.py", "FULL_EPISODE_STEPS = 720\n")
    _mk(sw, "kgenv/bots/__init__.py", "from .baseline import b\n")
    _mk(sw, "kgenv/bots/baseline.py", "b = 1\n")
    _mk(sw, "kgenv/bots/llm_provider.py", "class NullProvider:\n    pass\n")
    _mk(sw, "smoke_boot.py", "from kgenv.gym_env import KaggricultureGym\n")
    _mk(sw, "scripts/run_llm_ab.py",
        "from kgenv.bots.llm_provider import provider_from_env\n")
    _mk(sw, "tests/test_economy.py", "from kgenv.economy import CROPS\n")
    _mk(sw, "tests/test_redlines.py",
        "from kgenv.redlines import check_farm, summary\n")
    mainline = tmp_path / "fn_work" / "src"
    _mk(mainline, "clean_mod.py", "import json\nimport kgenv.arena\n")
    return {"campaign": tmp_path, "software": sw, "mainline": mainline}


def test_orchestration_pass_registry_schema_and_no_move(fake_campaign):
    verdict = downgrade_dormant_assets(
        software_root=fake_campaign["software"])  # 主线/注册表默认路径推导

    assert verdict["overall"] is True
    assert verdict["zone_counts"] == {"dormant_lab": 2, "test_asset": 2}
    assert verdict["missing_designated"] == []
    assert verdict["mainline"]["violations"] == []  # fn_work 消费四件 = 0（B13 前）
    assert verdict["schema_valid"] is True and verdict["schema_errors"] == []
    assert verdict["frozen_tree"] is True and verdict["postwar_only"] is True

    # 注册表落默认路径（战役根/fn_work/asset_zones.json）且 schema 完整
    registry_path = Path(verdict["registry_path"])
    assert registry_path == fake_campaign["campaign"] / "fn_work" \
        / "asset_zones.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    for key in ("contract", "generated_at", "frozen_tree", "postwar_execution",
                "zone_counts", "entries", "mainline_check",
                "legacy_consumers", "verdict"):
        assert key in registry
    assert registry["frozen_tree"] is True
    assert registry["postwar_execution"]["registry_only"] is True
    assert len(registry["entries"]) == 4

    # 注册表零绝对路径（可移植，跨机可 commit）：root 相对战役根
    assert registry["mainline_check"]["root"] == "fn_work/src"
    assert registry["verdict"]["mainline"]["root"] == "fn_work/src"

    def _strings(obj):
        if isinstance(obj, str):
            yield obj
        elif isinstance(obj, dict):
            for v in obj.values():
                yield from _strings(v)
        elif isinstance(obj, list):
            for v in obj:
                yield from _strings(v)

    assert not [s for s in _strings(registry) if s.startswith("/")], \
        "注册表全文不得含绝对路径（root 等须为战役根相对形态）"

    by_file = {e["file"]: e for e in registry["entries"]}
    assert set(by_file) == set(DESIGNATION_TABLE)
    for entry in registry["entries"]:
        assert all(k in entry for k in REQUIRED_ENTRY_KEYS)  # 五必备键
        assert entry["zone"] in ("dormant_lab", "test_asset")
        assert entry["module_ids"] and entry["postwar_dest"]
        assert entry["reason"] and entry["postwar_action"]
    zone = {"kgenv/gym_env.py": "dormant_lab",
            "kgenv/bots/llm_provider.py": "dormant_lab",
            "kgenv/economy.py": "test_asset",
            "kgenv/redlines.py": "test_asset"}
    for file, z in zone.items():
        assert by_file[file]["zone"] == z
        prefix = DORMANT_LAB_POSTWAR_DIR if z == "dormant_lab" \
            else TEST_ASSET_POSTWAR_DIR
        assert by_file[file]["postwar_dest"] == f"{prefix}/{file}"

    # 旧树消费面如实入注册表（direct 计数与假树 import 形态一致）
    def direct(file):
        return len(by_file[file]["current_consumers"]["direct"])
    assert direct("kgenv/economy.py") == 3      # init+redlines+test_economy
    assert direct("kgenv/redlines.py") == 2     # init+test_redlines
    assert direct("kgenv/gym_env.py") == 2      # init+smoke_boot
    assert direct("kgenv/bots/llm_provider.py") == 1  # 仅 run_llm_ab（默认关）

    # 零物理移动：四件仍原位、战后分区目录未建
    assert all((fake_campaign["software"] / f).is_file()
               for f in DESIGNATION_TABLE)
    assert not (fake_campaign["campaign"] / DORMANT_LAB_POSTWAR_DIR).exists()
    assert not (fake_campaign["campaign"] / TEST_ASSET_POSTWAR_DIR).exists()


def test_mainline_violation_reported_honestly_as_fail(fake_campaign):
    rogue = _mk(fake_campaign["mainline"], "rogue.py",
                "import kgenv.economy\n")
    verdict = downgrade_dormant_assets(
        software_root=fake_campaign["software"],
        mainline_root=fake_campaign["mainline"])
    assert rogue.is_file()

    assert verdict["overall"] is False
    violations = verdict["mainline"]["violations"]
    assert len(violations) == 1
    assert violations[0]["importer"] == "rogue.py"
    assert violations[0]["member"] == "kgenv.economy"
    assert violations[0]["zone"] == "test_asset"
    assert "FAIL" in verdict["summary"]
    registry = json.loads(
        Path(verdict["registry_path"]).read_text(encoding="utf-8"))
    assert registry["verdict"]["overall"] is False  # 注册表留痕如实


def test_transitive_exposure_disclosed_but_not_failing(fake_campaign):
    """主线 import kgenv.arena 经旧树 kgenv/__init__ 一跳触达三件：披露不判负。"""
    verdict = downgrade_dormant_assets(
        software_root=fake_campaign["software"])
    exposure = verdict["mainline"]["transitive_exposure"]
    assert exposure, "干净主线声明 kgenv.arena 应有一跳传递披露"
    assert all(e["imported"] == "kgenv.arena" for e in exposure)
    assert {e["member"] for e in exposure} == {
        "kgenv.economy", "kgenv.redlines", "kgenv.gym_env"}
    assert all(e["via"] == "kgenv/__init__.py" for e in exposure)
    assert verdict["overall"] is True  # 传递面属旧树事实，战后消解，不判负
    registry = json.loads(
        Path(verdict["registry_path"]).read_text(encoding="utf-8"))
    assert any("eager import" in step
               for step in registry["postwar_execution"]["steps"])


def test_missing_designated_fail_closed(fake_campaign):
    (fake_campaign["software"] / "kgenv" / "redlines.py").unlink()
    with pytest.raises(ValueError, match="旧树缺失"):
        downgrade_dormant_assets(
            software_root=fake_campaign["software"])


def test_custom_registry_path_and_zone_enum(fake_campaign, tmp_path):
    reg = tmp_path / "sub" / "zones.json"
    verdict = downgrade_dormant_assets(
        software_root=fake_campaign["software"],
        mainline_root=fake_campaign["mainline"], registry_path=reg)
    assert verdict["registry_path"] == str(reg)
    assert reg.is_file()
    registry = json.loads(reg.read_text(encoding="utf-8"))
    assert {e["zone"] for e in registry["entries"]} == {"dormant_lab",
                                                        "test_asset"}
    assert registry["verdict"]["summary"] == verdict["summary"]
