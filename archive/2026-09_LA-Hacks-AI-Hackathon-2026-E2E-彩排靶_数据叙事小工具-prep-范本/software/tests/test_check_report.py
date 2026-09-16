"""check_report 外部行为测试（票 03，TDD 先行；W1 用夹具验证行为，真跑留待 W2 后）。

接缝（见 specs/spec.md Testing Decisions）：
- a3 的 exec cmd 形态为无参数默认路径；测试用 --pdf/--typ/--metrics 覆盖参数在临时夹具上
  驱动同一进程边界（不把"W1 尚无报告"钉成断言，避免 W2 产物出现后变红）；
- 第二接缝 = 公共函数 extract_metric_refs / run_checks 直接调用。
只测外部行为：存在性、命中/未命中退出码；不测解析器内部。
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SOFTWARE_DIR = Path(__file__).resolve().parents[1]
CAMPAIGN_ROOT = SOFTWARE_DIR.parent
if str(SOFTWARE_DIR) not in sys.path:
    sys.path.insert(0, str(SOFTWARE_DIR))

import check_report  # noqa: E402

SCRIPT = SOFTWARE_DIR / "check_report.py"

METRICS = {
    "_meta": {"method": "fixture"},
    "rows": 6,
    "cols": 3,
    "score_mean": 88.0,
}

GOOD_TYP = """
#let metrics = json("../../software/metrics.json")
= 报告
共 metrics.rows 行、metrics.cols 列；规范形 metrics.software.score_mean。
"""


class Fixture(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def write(self, rel: str, text: str) -> Path:
        p = self.dir / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p

    def build(self, typ_text=GOOD_TYP, with_pdf=True, metrics=METRICS):
        self.write("docs/report.typ", typ_text)
        if with_pdf:
            self.write("docs/report.pdf", "%PDF-1.4 fixture")
        self.write("software/metrics.json", json.dumps(metrics))
        return (
            self.dir / "docs" / "report.pdf",
            self.dir / "docs" / "report.typ",
            self.dir / "software" / "metrics.json",
        )

    def run_cli(self, *argv):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *argv],
            capture_output=True,
            text=True,
        )

    def run_on_fixture(self, typ_text=GOOD_TYP, with_pdf=True, metrics=METRICS):
        pdf, typ, met = self.build(typ_text, with_pdf, metrics)
        return self.run_cli(
            "--pdf", str(pdf), "--typ", str(typ), "--metrics", str(met)
        )


class TestExtractRefs(unittest.TestCase):
    """函数接缝：两种规范引用形都应被识别（interface/contract.md §4）。"""

    def test_both_canonical_forms_extracted_and_deduped(self):
        refs = check_report.extract_metric_refs(
            "metrics.rows 及 metrics.software.cols 与 metrics.rows"
        )
        self.assertEqual(refs, {"rows", "cols"})

    def test_no_refs_gives_empty_set(self):
        self.assertEqual(check_report.extract_metric_refs("纯文本，无引用。"), set())

    def test_dotted_continuation_not_captured_as_key(self):
        # metrics.software.rows 归 pattern1；pattern2 不得把 "software" 当键
        refs = check_report.extract_metric_refs("metrics.software.rows")
        self.assertEqual(refs, {"rows"})


class TestCliProcess(Fixture):
    """进程接缝：a3 核验器在夹具上的命中/未命中两分支。"""

    def test_hit_branch_all_good_exits_zero(self):
        proc = self.run_on_fixture()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("OK", proc.stdout)

    def test_miss_branch_unknown_key_exits_one(self):
        proc = self.run_on_fixture(typ_text="差值 metrics.delta_mean。")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("delta_mean", proc.stderr)

    def test_pdf_missing_exits_one(self):
        proc = self.run_on_fixture(with_pdf=False)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("report.pdf", proc.stderr)

    def test_typ_missing_exits_one(self):
        pdf, _, met = self.build(with_pdf=True)
        proc = self.run_cli("--pdf", str(pdf), "--typ", str(self.dir / "docs" / "nope.typ"), "--metrics", str(met))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("nope.typ", proc.stderr)

    def test_no_metric_refs_exits_one(self):
        proc = self.run_on_fixture(typ_text="= 报告\n全文没有一个引用。\n")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("引用", proc.stderr)

    def test_bare_metrics_dot_software_prefix_is_rejected(self):
        # 契约 §4：metrics. 前缀不得用于其他对象；裸 metrics.software 不是合法引用
        proc = self.run_on_fixture(typ_text="错误用法 metrics.software 结尾。\n")
        self.assertEqual(proc.returncode, 1)

    def test_metrics_file_missing_exits_two(self):
        pdf, typ, _ = self.build()
        proc = self.run_cli("--pdf", str(pdf), "--typ", str(typ), "--metrics", str(self.dir / "gone.json"))
        self.assertEqual(proc.returncode, 2)

    def test_metrics_corrupt_json_exits_two(self):
        pdf, typ, _ = self.build()
        bad = self.write("software/bad.json", "{not json")
        proc = self.run_cli("--pdf", str(pdf), "--typ", str(typ), "--metrics", str(bad))
        self.assertEqual(proc.returncode, 2)


class TestRunChecksFunction(Fixture):
    """函数接缝：run_checks 的判定核（与进程分支等价覆盖）。"""

    def test_run_checks_hit(self):
        pdf, typ, met = self.build()
        problems, hits = check_report.run_checks(pdf, typ, met)
        self.assertEqual(problems, [])
        self.assertEqual(hits, {"rows", "cols", "score_mean"})

    def test_run_checks_unknown_key(self):
        pdf, typ, met = self.build(typ_text="x metrics.rows_y z")
        problems, hits = check_report.run_checks(pdf, typ, met)
        self.assertTrue(problems)
        self.assertEqual(hits, {"rows_y"})


class TestDefaultPaths(unittest.TestCase):
    """默认路径锚定战役根（a3 无参数 cmd 的解析对象），不依赖 W1 是否已有报告。"""

    def test_defaults_point_to_campaign_root(self):
        self.assertEqual(
            check_report.DEFAULT_PDF, CAMPAIGN_ROOT / "docs" / "report.pdf"
        )
        self.assertEqual(
            check_report.DEFAULT_TYP, CAMPAIGN_ROOT / "docs" / "report.typ"
        )
        self.assertEqual(
            check_report.DEFAULT_METRICS, CAMPAIGN_ROOT / "software" / "metrics.json"
        )


if __name__ == "__main__":
    unittest.main()
