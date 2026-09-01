#!/usr/bin/env python3
"""init_state v2 多战役集成测试：v1→v2 升级、新战役登记（骨架）、保留名校验、--close。

在隔离临时根中执行（ZCODE_PROJECT_DIR 指向），不触碰真实 .flow/state.json。
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "guard" / "init_state.py"
SRC_ROOT = Path(__file__).resolve().parents[2]

V1_STATE = {"schema_version": 1, "phase": "deliver", "campaign": None,
            "extra_allow": [], "retry": {"count": 2, "max": 3, "tripped": False}}


def make_root(with_legacy_bp: bool) -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="autoc_init_test_"))
    shutil.copytree(SRC_ROOT / "config", tmp / "config", dirs_exist_ok=True)
    (tmp / ".flow").mkdir()
    (tmp / "workspace").mkdir()
    if with_legacy_bp:
        (tmp / "workspace" / "blueprint.md").write_text("---\ncampaign: {name: x}\n---\n", encoding="utf-8")
    (tmp / ".flow" / "state.json").write_text(json.dumps(V1_STATE), encoding="utf-8")
    return tmp


def run(root: Path, *args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ, ZCODE_PROJECT_DIR=str(root))
    return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=root,
                          capture_output=True, text=True, env=env, timeout=30)


def read_state(root: Path) -> dict:
    return json.loads((root / ".flow" / "state.json").read_text(encoding="utf-8"))


def main() -> int:
    passed = 0
    total = 5

    # 1. v1→v2 升级（legacy 布局）：顶层阶段+retry 迁入战役条目，全局复位 idle
    root = make_root(with_legacy_bp=True)
    try:
        p = run(root, "--campaign", "kaggriculture", "--phase", "verify", "--by", "test")
        st = read_state(root)
        camp = st.get("campaigns", {}).get("kaggriculture", {})
        ok = (p.returncode == 0 and st.get("schema_version") == 2 and st.get("phase") == "idle"
              and camp.get("root") == "workspace" and camp.get("phase") == "verify"
              and camp.get("retry", {}).get("count") == 2)
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 1 v1→v2 legacy 升级：root={camp.get('root')} "
              f"phase={camp.get('phase')} retry={camp.get('retry', {}).get('count')}（期望 workspace/verify/2）")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 2. 新战役登记：root=workspace/<cid> + 骨架目录
    root = make_root(with_legacy_bp=False)
    try:
        (root / ".flow" / "state.json").unlink()  # 全新引导
        run(root)  # 引导 v1 idle
        p = run(root, "--campaign", "newcup", "--phase", "decide")
        st = read_state(root)
        camp = st.get("campaigns", {}).get("newcup", {})
        skel_ok = all((root / "workspace" / "newcup" / d).is_dir()
                      for d in ("software", "hardware", "docs", "references", "acceptance"))
        ok = (p.returncode == 0 and camp.get("root") == "workspace/newcup"
              and camp.get("phase") == "decide" and skel_ok
              and (root / "workspace" / "newcup" / "JOURNAL.md").is_file())
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 2 新战役登记：root={camp.get('root')} 骨架={skel_ok}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 3. 保留名/非法 id 拒绝
    root = make_root(with_legacy_bp=False)
    try:
        p1 = run(root, "--campaign", "software", "--phase", "decide")
        p2 = run(root, "--campaign", "Bad_ID", "--phase", "decide")
        ok = p1.returncode == 2 and p2.returncode == 2
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 3 非法/保留 id 拒绝：reserved={p1.returncode == 2} bad={p2.returncode == 2}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 4. 全局阶段不再接受战役值（提示 --campaign）
    root = make_root(with_legacy_bp=False)
    try:
        run(root)  # 引导
        p = run(root, "--phase", "deliver")
        ok = p.returncode == 2 and "--campaign" in p.stderr
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 4 全局拒绝战役阶段：exit={p.returncode} 提示含--campaign={'--campaign' in p.stderr}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 5. --close 注销（其余战役保留）
    root = make_root(with_legacy_bp=False)
    try:
        run(root)
        run(root, "--campaign", "a-cup", "--phase", "decide")
        run(root, "--campaign", "b-cup", "--phase", "decide")
        p = run(root, "--campaign", "a-cup", "--close")
        st = read_state(root)
        ok = (p.returncode == 0 and "a-cup" not in st.get("campaigns", {})
              and "b-cup" in st.get("campaigns", {}))
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 5 --close 注销：剩战役={sorted(st.get('campaigns', {}))}（期望 ['b-cup']）")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    print(f"[test_init_state] {passed}/{total} 通过")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
