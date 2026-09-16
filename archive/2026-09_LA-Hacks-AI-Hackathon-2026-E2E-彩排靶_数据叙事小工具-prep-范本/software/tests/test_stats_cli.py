"""stats_cli 外部行为测试（票 01，TDD 先行）。

接缝（见 specs/spec.md Testing Decisions）：
- 最高接缝 = CLI 进程边界（a1 的 exec cmd 形态），subprocess 覆盖；
- 第二接缝 = 公共函数 compute_stats / sanity_problems 直接调用。
只测外部行为：进什么 CSV、出什么 JSON、什么退出码；不测内部实现细节。
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

import stats_cli  # noqa: E402

SCRIPT = SOFTWARE_DIR / "stats_cli.py"
SAMPLE_CSV = CAMPAIGN_ROOT / "references" / "data" / "sample.csv"

EXPECTED_SAMPLE_STATS = {
    "source": "sample.csv",
    "rows": 6,
    "cols": 3,
    "columns": ["name", "score", "hours"],
    "numeric_columns": ["score", "hours"],
    "numeric": {
        "score": {"count": 6, "mean": 88.0, "max": 95.0},
        "hours": {"count": 6, "mean": 5.5, "max": 8.0},
    },
}


def write_csv(text: str) -> Path:
    tmp = tempfile.NamedTemporaryFile(
        "w", suffix=".csv", delete=False, encoding="utf-8"
    )
    tmp.write(text)
    tmp.close()
    return Path(tmp.name)


class TestComputeStats(unittest.TestCase):
    """函数接缝：compute_stats 的外部可见契约。"""

    def test_sample_csv_full_shape_and_values(self):
        stats = stats_cli.compute_stats(SAMPLE_CSV)
        self.assertEqual(stats, EXPECTED_SAMPLE_STATS)

    def test_non_numeric_column_excluded_from_numeric(self):
        path = write_csv("city,temp\nFairbanks,-3.5\nNairobi,24\n")
        try:
            stats = stats_cli.compute_stats(path)
            self.assertEqual(stats["columns"], ["city", "temp"])
            self.assertEqual(stats["numeric_columns"], ["temp"])
            self.assertEqual(stats["numeric"]["temp"]["mean"], 10.25)
            self.assertEqual(stats["numeric"]["temp"]["max"], 24.0)
            self.assertEqual(stats["numeric"]["temp"]["count"], 2)
        finally:
            path.unlink()

    def test_all_text_columns_yield_empty_numeric(self):
        path = write_csv("a,b\nfoo,bar\nbaz,qux\n")
        try:
            stats = stats_cli.compute_stats(path)
            self.assertEqual(stats["numeric_columns"], [])
            self.assertEqual(stats["numeric"], {})
            self.assertEqual(stats["rows"], 2)
        finally:
            path.unlink()

    def test_missing_cells_are_ignored_not_parsed(self):
        path = write_csv("name,score\nalice,80\nbob,\ncarol,90\n")
        try:
            stats = stats_cli.compute_stats(path)
            self.assertEqual(stats["numeric"]["score"], {"count": 2, "mean": 85.0, "max": 90.0})
        finally:
            path.unlink()

    def test_missing_file_raises_stats_error(self):
        with self.assertRaises(stats_cli.StatsError):
            stats_cli.compute_stats(Path("/nonexistent/nope.csv"))

    def test_empty_file_raises_stats_error(self):
        path = write_csv("")
        try:
            with self.assertRaises(stats_cli.StatsError):
                stats_cli.compute_stats(path)
        finally:
            path.unlink()

    def test_header_only_raises_stats_error(self):
        path = write_csv("name,score\n")
        try:
            with self.assertRaises(stats_cli.StatsError):
                stats_cli.compute_stats(path)
        finally:
            path.unlink()

    def test_ragged_row_raises_stats_error(self):
        path = write_csv("name,score\nalice,80\nbob\n")
        try:
            with self.assertRaises(stats_cli.StatsError):
                stats_cli.compute_stats(path)
        finally:
            path.unlink()


class TestSanityCheck(unittest.TestCase):
    """函数接缝：sanity_problems 的外部可见契约（--check 语义的判定核）。"""

    def test_sample_stats_have_no_problems(self):
        self.assertEqual(stats_cli.sanity_problems(EXPECTED_SAMPLE_STATS), [])

    def test_no_numeric_columns_is_a_problem(self):
        stats = dict(EXPECTED_SAMPLE_STATS, numeric_columns=[], numeric={})
        self.assertTrue(stats_cli.sanity_problems(stats))


class TestCliProcess(unittest.TestCase):
    """进程接缝：a1 的 exec cmd 形态（--csv <样例> --check）。"""

    def run_cli(self, *argv):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *argv],
            capture_output=True,
            text=True,
        )

    def test_a1_check_mode_exit_zero_with_stats_json(self):
        proc = self.run_cli("--csv", str(SAMPLE_CSV), "--check")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), EXPECTED_SAMPLE_STATS)

    def test_plain_mode_outputs_same_json(self):
        proc = self.run_cli("--csv", str(SAMPLE_CSV))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), EXPECTED_SAMPLE_STATS)

    def test_missing_file_exits_nonzero_with_stderr(self):
        proc = self.run_cli("--csv", "/nonexistent/nope.csv", "--check")
        self.assertNotEqual(proc.returncode, 0)
        self.assertTrue(proc.stderr.strip())

    def test_check_mode_all_text_columns_exits_nonzero(self):
        path = write_csv("a,b\nfoo,bar\n")
        try:
            proc = self.run_cli("--csv", str(path), "--check")
            self.assertNotEqual(proc.returncode, 0)
            self.assertTrue(proc.stderr.strip())
        finally:
            path.unlink()

    def test_plain_mode_all_text_columns_still_outputs_json(self):
        path = write_csv("a,b\nfoo,bar\n")
        try:
            proc = self.run_cli("--csv", str(path))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(proc.stdout)["numeric_columns"], [])
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
