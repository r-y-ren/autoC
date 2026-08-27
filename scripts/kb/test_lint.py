#!/usr/bin/env python3
"""S-08 lint_kb 回归测试：目标识别（四类契约文件精确匹配、正文/原料跳过）与日期格式校验。"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lint_kb import validate_path  # noqa: E402

META_OK = """---
id: demo-cup
name: Demo Cup
tier: 学科竞赛
directions: [test]
status: active
ai_policy: {summary: "无限制", checked: "2026-08-27"}
last_verified: "2026-08-27"
sources:
  - {url: "https://example.com", accessed: "2026-08-27"}
---
正文
"""

META_BAD_DATE = META_OK.replace('accessed: "2026-08-27"', 'accessed: "2026/08/27"')

TECH_OK = """---
id: arxiv-2501-00001
name: Test Tech
field: [test]
published: 2026-08-01
maturity: demo
competition_fit:
  - {track: hackathon, edge: "快速原型", reuse_cost: 低}
sources:
  - {url: "https://example.com", accessed: 2026-08-27}
---
正文
"""

TECH_NO_FIT = """---
id: arxiv-2501-00002
name: Bad Tech
field: [test]
published: 2026-08-01
maturity: paper
sources:
  - {url: "https://example.com", accessed: 2026-08-27 }
---
正文
"""

TECH_BAD_PUB = TECH_OK.replace("published: 2026-08-01", 'published: "2026-13-01"')

BLUEPRINT_OK = """---
campaign: {competition_id: demo-cup, name: Demo Cup, theme: t}
scope: {deliverables: [demo], out_of_scope: []}
tech_stack:
  - {name: tech-a, kb_tech_ids: [arxiv-2501-00001], rationale: diff}
interface_contracts:
  - {between: [software, hardware], contract_file: if.md}
milestones:
  - {id: m1, task: build, owner_role: software}
acceptance:
  checklist:
    - {id: a1, category: software, item: runs, method: exec}
compliance: {ai_policy_reviewed: true}
---
正文
"""

ACCEPT_OK = """{
  "campaign": {"competition_id": "demo-cup"},
  "checklist": [{"id": "a1", "category": "software", "status": "pass", "evidence": "log"}],
  "result": "pass",
  "generated_at": "2026-08-27T12:00:00"
}
"""

# (相对路径, 内容, 期望: True=PASS / False=FAIL / None=SKIP)
CASES = [
    ("kb/competitions/cup-ok/meta.md", META_OK, True, "合法赛事条目"),
    ("kb/competitions/cup-bad/meta.md", META_BAD_DATE, False, "accessed 非法日期（format:date 应拦截）"),
    ("kb/competitions/cup-ok/winners/2025-国一-某队.md", "获奖分析正文（无 frontmatter）", None, "winners 正文应跳过"),
    ("kb/competitions/cup-ok/patterns.md", "模式库正文", None, "patterns 应跳过"),
    ("kb/tech/arxiv-2501-00001.md", TECH_OK, True, "合法技术卡片（YAML 日期自动规范化）"),
    ("kb/tech/arxiv-badfit.md", TECH_NO_FIT, False, "缺 competition_fit 应 FAIL"),
    ("kb/tech/arxiv-badpub.md", TECH_BAD_PUB, False, "published 2026-13-01 应被 format 拦截"),
    ("kb/tech/README.md", "说明文件", None, "README 应跳过"),
    ("kb/raw/notice.html", "<html>快照</html>", None, "raw 快照应跳过"),
    ("workspace/blueprint.md", BLUEPRINT_OK, True, "合法蓝图"),
    ("workspace/acceptance/run-1.json", ACCEPT_OK, True, "合法验收记录"),
    ("workspace/acceptance/note.md", "随手笔记", None, "acceptance 下非 json 应跳过"),
]


def main() -> int:
    passed = 0
    with tempfile.TemporaryDirectory(prefix="autoc_lint_test_") as td:
        base = Path(td)
        for rel, content, expect, note in CASES:
            f = base / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(content, encoding="utf-8")
            ok, msg = validate_path(f)
            if expect is None:
                got = "SKIP" if msg.startswith("skip") else ("PASS" if ok else "FAIL")
                good = got == "SKIP"
            else:
                got = "PASS" if ok else "FAIL"
                good = ok == expect
            passed += good
            mark = "PASS" if good else "FAIL"
            print(f"{mark} {rel:52s} 期望{expect if expect is not None else 'SKIP'} 实际{got:4s} [{msg[:40]}] # {note}")
    print(f"[test_lint] {passed}/{len(CASES)} 通过")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
