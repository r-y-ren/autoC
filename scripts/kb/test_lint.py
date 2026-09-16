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
directions: [测试方向]
competition_fit:
  - {track: 黑客松-数据与算法, edge: "快速原型", reuse_cost: 低}
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

# 2026-09-16 升级票02：vault-distill 溯源形态（paper-distill sources + 4 个可选枚举）
TECH_DISTILL_OK = """---
id: arxiv-2603-00001
name: Distill Tech
field: [test]
published: 2026-03-01
maturity: paper
directions: [测试方向]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: low
competition_fit:
  - {track: 黑客松-数据与算法, edge: "快速原型", reuse_cost: 低}
sources:
  - {paper_title: "Joint Task Scheduling for UAV-assisted MEC", doi: "10.0000/test.2026", distilled_from: my_LLM_valut, distilled_date: 2026-09-16}
---
正文
"""

TECH_DISTILL_NO_TITLE = TECH_DISTILL_OK.replace(
    'paper_title: "Joint Task Scheduling for UAV-assisted MEC", ', "")

TECH_DISTILL_WITH_URL = TECH_DISTILL_OK.replace(
    "distilled_date: 2026-09-16}",
    'distilled_date: 2026-09-16, url: "https://ieeexplore.example", accessed: 2026-09-16}')

TECH_BAD_VENUE = TECH_OK.replace("maturity: demo", "maturity: demo\nvenue_tier: SCI-Q1")

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
compliance: {ai_policy_reviewed: true, mode: prep}
---
正文
"""

# 升级票08：workflow.auto_chain 可选开关（缺省合法，false 亦合法，非布尔应拒）
BLUEPRINT_CHAIN_OFF = BLUEPRINT_OK.replace(
    "compliance: {ai_policy_reviewed: true, mode: prep}",
    "compliance: {ai_policy_reviewed: true, mode: prep}\nworkflow: {auto_chain: false}")
BLUEPRINT_CHAIN_BAD = BLUEPRINT_OK.replace(
    "compliance: {ai_policy_reviewed: true, mode: prep}",
    "compliance: {ai_policy_reviewed: true, mode: prep}\nworkflow: {auto_chain: 'yes'}")

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
    ("kb/tech/arxiv-distill-ok.md", TECH_DISTILL_OK, True, "paper-distill 溯源+4 可选枚举合法"),
    ("kb/tech/arxiv-distill-notitle.md", TECH_DISTILL_NO_TITLE, False, "paper-distill 缺 paper_title 应 FAIL"),
    ("kb/tech/arxiv-distill-withurl.md", TECH_DISTILL_WITH_URL, True,
     "paper-distill 携回填 url+accessed 仍合法（not-guard 消除 oneOf 双命中陷阱）"),
    ("kb/tech/arxiv-badvenue.md", TECH_BAD_VENUE, False, "venue_tier 非法枚举应 FAIL"),
    ("kb/tech/README.md", "说明文件", None, "README 应跳过"),
    ("kb/raw/notice.html", "<html>快照</html>", None, "raw 快照应跳过"),
    ("workspace/blueprint.md", BLUEPRINT_OK, True, "合法蓝图（无 workflow 字段=缺省 auto_chain）"),
    ("workspace/bp-chain-off/blueprint.md", BLUEPRINT_CHAIN_OFF, True, "auto_chain: false 合法"),
    ("workspace/bp-chain-bad/blueprint.md", BLUEPRINT_CHAIN_BAD, False, "auto_chain 非布尔应 FAIL"),
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
