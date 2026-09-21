"""discover_campaign_roots 单测。

覆盖契约（fn_docs/responsibility.md 共享函数节 + R20）：
①真实仓库三根发现正确（期望值在测试内独立推导，非复用被测实现）；
②不同 CWD（仓根/深层临时子目录）与不同显式起点下结果一致（取代"仓根 CWD 假设"）；
③tmp_path 假树缺特征 → RootDiscoveryError（fail-closed：缺战役特征/缺仓根/多战役歧义/起点不存在）；
④模块源码无字面战役名（R20：战役名清单自真实仓容器动态枚举，测试自身不写字面战役名）。
"""

from pathlib import Path
import sys

# 防御性自举：仓外 CWD + 绝对路径调用时 pytest rootdir 推断会截掉 fn_work/tests/conftest.py
# （confcutdir），此处按 __file__ 程序化补 src 入 sys.path（幂等；R20：不写字面战役路径）。
_SRC_DIR = Path(__file__).resolve().parents[2] / "src"  # shared→tests→fn_work→src
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

import pytest

import shared.discover_campaign_roots as dcr_module
from shared.discover_campaign_roots import RootDiscoveryError, discover_campaign_roots

MODULE_FILE = Path(dcr_module.__file__).resolve()
TESTS_SHARED_DIR = Path(__file__).resolve().parent
# tests/shared → tests → fn_work → 战役根（独立于被测实现推导期望值）
EXPECTED_CAMPAIGN_ROOT = TESTS_SHARED_DIR.parents[2]
CAMPAIGN_FEATURES = ("blueprint.md", "software", "fn_docs")


def _expected_repo_root() -> Path:
    for candidate in (EXPECTED_CAMPAIGN_ROOT, *EXPECTED_CAMPAIGN_ROOT.parents):
        if (candidate / ".git").exists() and (candidate / "AGENTS.md").is_file():
            return candidate
    raise AssertionError("测试自身无法定位真实仓根（.git+AGENTS.md 并存）——环境异常")


def test_real_repo_three_roots():
    roots = discover_campaign_roots()
    assert set(roots) == {"campaign_root", "repo_root", "software_root"}
    assert roots["campaign_root"] == EXPECTED_CAMPAIGN_ROOT
    assert roots["repo_root"] == _expected_repo_root()
    assert roots["software_root"] == EXPECTED_CAMPAIGN_ROOT / "software"
    # 特征完备性独立复核（非仅信返回值）
    for feat in CAMPAIGN_FEATURES:
        assert (EXPECTED_CAMPAIGN_ROOT / feat).exists(), feat
    # 三根相互关系：仓根包含战役根，软件根真实存在
    assert roots["repo_root"] in roots["campaign_root"].parents
    assert roots["software_root"].is_dir()


def test_cwd_and_start_path_independence(tmp_path, monkeypatch):
    baseline = discover_campaign_roots()
    # 不同 CWD：真实仓根 / 深层临时子目录——默认起点按 __file__，结果必须一致
    monkeypatch.chdir(baseline["repo_root"])
    assert discover_campaign_roots() == baseline
    nested = tmp_path / "deep" / "nested" / "dir"
    nested.mkdir(parents=True)
    monkeypatch.chdir(nested)
    assert discover_campaign_roots() == baseline
    # 显式起点：战役树内（fn_docs/战役根，含字符串形态）与战役树外（仓根，走回落扫描）一致
    assert discover_campaign_roots(start_path=baseline["campaign_root"] / "fn_docs") == baseline
    assert discover_campaign_roots(start_path=str(baseline["campaign_root"])) == baseline
    assert discover_campaign_roots(start_path=baseline["repo_root"]) == baseline


def test_synthetic_full_tree(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    (repo / "AGENTS.md").write_text("# synthetic\n", encoding="utf-8")
    camp = repo / "workspace" / "acamp"
    camp.mkdir(parents=True)
    (camp / "blueprint.md").write_text("# bp\n", encoding="utf-8")
    (camp / "software").mkdir()
    (camp / "fn_docs").mkdir()
    deep = camp / "fn_docs" / "nested"
    deep.mkdir()
    roots = discover_campaign_roots(start_path=deep)
    assert roots["campaign_root"] == camp.resolve()
    assert roots["repo_root"] == repo.resolve()
    assert roots["software_root"] == (camp / "software").resolve()


def test_fail_closed_when_campaign_features_missing(tmp_path):
    # 仓根齐备，但容器内目录缺 fn_docs——特征不齐备，不许当战役根
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    (repo / "AGENTS.md").write_text("# synthetic\n", encoding="utf-8")
    partial = repo / "workspace" / "partial"
    partial.mkdir(parents=True)
    (partial / "blueprint.md").write_text("# bp\n", encoding="utf-8")
    (partial / "software").mkdir()
    with pytest.raises(RootDiscoveryError, match=r"blueprint\.md\+software\+fn_docs"):
        discover_campaign_roots(start_path=repo)


def test_fail_closed_when_repo_root_missing(tmp_path):
    # 特征齐备的战役目录但上方无仓根（孤立副本）——fail-closed
    camp = tmp_path / "orphan"
    camp.mkdir()
    (camp / "blueprint.md").write_text("# bp\n", encoding="utf-8")
    (camp / "software").mkdir()
    (camp / "fn_docs").mkdir()
    with pytest.raises(RootDiscoveryError, match=r"\.git\+AGENTS\.md"):
        discover_campaign_roots(start_path=camp / "fn_docs")


def test_fail_closed_when_ambiguous_campaigns(tmp_path):
    # 容器下两个特征齐备战役：拒绝猜测，消歧责任在调用方
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    (repo / "AGENTS.md").write_text("# synthetic\n", encoding="utf-8")
    for name in ("c_one", "c_two"):
        camp = repo / "workspace" / name
        camp.mkdir(parents=True)
        (camp / "blueprint.md").write_text("# bp\n", encoding="utf-8")
        (camp / "software").mkdir()
        (camp / "fn_docs").mkdir()
    with pytest.raises(RootDiscoveryError, match=r"c_one.*c_two"):
        discover_campaign_roots(start_path=repo)


def test_fail_closed_when_start_missing(tmp_path):
    with pytest.raises(RootDiscoveryError, match="不存在"):
        discover_campaign_roots(start_path=tmp_path / "no_such_path")


def test_module_source_has_no_literal_campaign_names():
    # R20：模块源码零字面战役名；受检名单自真实仓容器动态枚举，测试不写字面战役名
    roots = discover_campaign_roots()
    container = roots["repo_root"] / "workspace"
    campaign_names = sorted(
        p.name for p in container.iterdir() if p.is_dir()
    ) if container.is_dir() else []
    assert campaign_names, "真实仓 workspace 容器应有战役目录可供 R20 检查"
    source = MODULE_FILE.read_text(encoding="utf-8")
    offenders = [name for name in campaign_names if name in source]
    assert offenders == [], f"模块源码出现字面战役名（违反 R20）: {offenders}"
