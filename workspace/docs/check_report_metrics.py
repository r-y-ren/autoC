#!/usr/bin/env python3
"""Read-only consistency checks for the m5-redocument Typst report (campaign III final)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = REPO_ROOT / "workspace" / "docs" / "report.typ"
METRICS_PATH = REPO_ROOT / "workspace" / "metrics.json"

REQUIRED_SOFTWARE_KEYS = (
    "frozen_candidate_identity",
    "development_gate_summary",
    "strategy_repair_test_summary",
    "holdout_run_status",
    "holdout_seed_manifest",
    "holdout_candidate_hash_match",
    "holdout_schedule",
    "holdout_seat_split",
    "holdout_abnormal_summary",
    "holdout_integrity_pass",
    "confirmatory_overall_record",
    "confirmatory_pair_records",
    "confirmatory_seat_records",
    "confirmatory_wilson_intervals",
    "confirmatory_order_independent_statistics",
    "confirmatory_elo_appendix",
    "confirmatory_export_traceability",
)

# Campaign III (m1-m4) keys that the m5 final report must consume. Names were
# verified against workspace/metrics.json before being listed here.
REQUIRED_SOFTWARE_R3_KEYS = (
    "m1_corpus_episodes_total",
    "m1_corpus_by_band",
    "m1_corpus_abnormal_excluded",
    "m1_profiles_generated",
    "m1_download_bytes",
    "m1_corpus_runtime_seconds",
    "m2_online_style_opponents",
    "m2_opponent_pool_certification",
    "m2_gate_required_opponents",
    "m2_gate_contract_check_pass",
    "m2_opponent_unit_tests_summary",
    "m3_strategy_capability_checks",
    "m3_strategy_regression_summary",
    "m3_development_gate_summary",
    "m3_frozen_candidate_identity",
    "m4_holdout_protocol",
    "m4_holdout_seed_manifest",
    "m4_holdout_candidate_hash_match",
    "m4_holdout_seed_domain_isolation",
    "m4_holdout_run_status",
    "m4_holdout_schedule",
    "m4_holdout_seat_split",
    "m4_holdout_abnormal_summary",
    "m4_holdout_integrity_pass",
    "m4_confirmatory_overall_record",
    "m4_confirmatory_pair_records",
    "m4_confirmatory_seat_records",
    "m4_confirmatory_wilson_intervals",
    "m4_confirmatory_order_independent_statistics",
    "m4_confirmatory_elo_appendix",
    "m4_confirmatory_export_traceability",
)

REQUIRED_UNMEASURED_KEYS = (
    "online_ladder_games",
    "online_skill_rating",
    "online_feedback_calibration",
    "final_submission_commits",
)

# Rewrite targets. The first twelve are the campaign-II targets retained from
# the m3 checker; the R3_* markers lock the m5 placeholder->key rewrite map.
# A completed target is marked by one exact, standalone Typst comment:
# // CHECK:<marker>.
REWRITE_MARKERS = (
    "METHOD_IDENTITY",
    "METHOD_SEEDS",
    "METHOD_ABBA",
    "METHOD_FAIL_CLOSED",
    "METHOD_ATOMIC",
    "RESULT_OVERALL",
    "RESULT_PAIRS",
    "RESULT_SEATS",
    "RESULT_INTERVALS",
    "LIMITATIONS",
    "HUMAN_AI",
    "TRACEABILITY",
    "R3_ROUND1",
    "R3_M1_CORPUS",
    "R3_M2_POOL",
    "R3_M3_CANDIDATE",
    "R3_M4_PROTOCOL",
    "R3_RESULT_OVERALL",
    "R3_RESULT_PAIRS",
    "R3_RESULT_SEATS",
    "R3_RESULT_INTERVALS",
    "R3_BOUNDARY",
)

HISTORICAL_LITERALS = ("1500.8", "36-0")
HISTORICAL_DISCLOSURE_TOKENS = (
    "固定 p0",
    "复用开发种子",
    "顺序敏感 Elo",
    "非确认性",
    "不可外推线上",
)
# A disclosure is adjacent when every required token falls in the same
# blank-line-delimited paragraph as the historical literal.
PARAGRAPH_SPLIT_RE = re.compile(r"(?:\r?\n)[ \t]*(?:\r?\n)+")

METRIC_REFERENCE_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?P<kind>um|m)\s*\(\s*\"(?P<key>[A-Za-z0-9_.-]+)\"\s*\)"
)

# These are the current holdout/development performance spellings that must
# be rendered from m() data rather than duplicated as static report text.
# Campaign II spellings first, then campaign III (m1-m4) spellings.
UNKEYED_PERFORMANCE_PATTERNS = (
    ("119W-9L", re.compile(r"(?<!\w)119\s*W\s*[-/]\s*9\s*L(?!\w)", re.IGNORECASE)),
    ("0.929688", re.compile(r"(?<![\d.])0\.929688(?!\d)")),
    ("576 games", re.compile(r"(?<!\d)576\s*(?:games?|局|场|对局)(?!\w)", re.IGNORECASE)),
    ("288/288", re.compile(r"(?<!\d)288\s*/\s*288(?!\d)")),
    ("Wilson lower bound 0.8718", re.compile(r"(?<![\d.])0\.8718(?!\d)")),
    ("Wilson upper bound 0.9626", re.compile(r"(?<![\d.])0\.9626(?!\d)")),
    ("paired lower bound 0.867281", re.compile(r"(?<![\d.])0\.867281(?!\d)")),
    ("paired upper bound 0.992094", re.compile(r"(?<![\d.])0\.992094(?!\d)")),
    ("31W-1L", re.compile(r"(?<!\w)31\s*W\s*[-/]\s*1\s*L(?!\w)", re.IGNORECASE)),
    ("35/35", re.compile(r"(?<!\d)35\s*/\s*35(?!\d)")),
    ("m4 overall 108W-20L", re.compile(r"(?<!\w)108\s*W\s*[-/]\s*20\s*L(?!\w)", re.IGNORECASE)),
    ("m4 score 0.84375", re.compile(r"(?<![\d.])0\.84375(?!\d)")),
    ("m4 score 84.4 percent", re.compile(r"(?<![\d.])84\.4(?![\d])")),
    ("m4 Wilson lower 0.771", re.compile(r"(?<![\d.])0\.771(?!\d)")),
    ("m4 Wilson upper 0.8965", re.compile(r"(?<![\d.])0\.8965(?!\d)")),
    ("m4 paired lower 0.7551", re.compile(r"(?<![\d.])0\.7551(?!\d)")),
    ("m4 paired upper 0.9324", re.compile(r"(?<![\d.])0\.9324(?!\d)")),
    ("m4 holdout 128 games", re.compile(r"(?<!\d)128\s*(?:games?|局|场|对局)(?!\w)", re.IGNORECASE)),
    ("m4 pair sweep 16-0", re.compile(r"(?<!\w)16\s*[-/]\s*0(?![\d])")),
    ("m4 crop_rotator 12-4", re.compile(r"(?<!\w)12\s*[-/]\s*4(?![\d])")),
    ("m4 template_wheat 10-6", re.compile(r"(?<!\w)10\s*[-/]\s*6(?![\d])")),
    ("m4 self_feed 14-2", re.compile(r"(?<!\w)14\s*[-/]\s*2(?![\d])")),
    ("m4 near_band 8-8", re.compile(r"(?<!\w)8\s*[-/]\s*8(?![\d])")),
    ("m3 gate 57W-7L", re.compile(r"(?<!\w)57\s*W\s*[-/]\s*7\s*L(?!\w)", re.IGNORECASE)),
    ("m3 gate 64 games", re.compile(r"(?<!\d)64\s*(?:games?|局|场|对局)(?!\w)", re.IGNORECASE)),
    ("m2 certification 12W-0L", re.compile(r"(?<!\w)12\s*W\s*[-/]\s*0\s*L(?!\w)", re.IGNORECASE)),
    ("m2 certification 84 games", re.compile(r"(?<!\d)84\s*(?:games?|局|场|对局)(?!\w)", re.IGNORECASE)),
    ("m2 suite 246", re.compile(r"(?<![\d.])246(?![\d.])")),
    ("m2 opponent tests 42", re.compile(r"(?<![\d.])42(?![\d.])")),
    ("m3 suite 269", re.compile(r"(?<![\d.])269(?![\d.])")),
    ("m1 corpus 60 games", re.compile(r"(?<!\d)60\s*(?:games?|局|场|对局)(?!\w)", re.IGNORECASE)),
    ("m1 corpus 1.9GB", re.compile(r"(?<![\d.])1\.9\s*GB(?!\w)", re.IGNORECASE)),
)

# The detector intentionally operates sentence by sentence. A hit needs a
# positive-claim pattern and no explicit negation or boundary phrase in that
# sentence. This keeps the policy reviewable instead of relying on sentiment.
PROHIBITED_CLAIM_PATTERNS = (
    (
        "online/ladder performance assertion",
        re.compile(
            r"(?:天梯|线上)[^。！？\n]{0,40}"
            r"(?:胜率|实力|评级|rating|Elo|排名|名次|榜首|冠军|获奖)",
            re.IGNORECASE,
        ),
    ),
    (
        "rank assertion",
        re.compile(
            r"(?:排名|名次|位列|跻身|进入)[^。！？\n]{0,20}"
            r"(?:第一|第\s*\d+|前\s*\d+|榜首|提升|达到)",
        ),
    ),
    (
        "prize prediction",
        re.compile(
            r"(?:将|会|能|可|预计|预测|有望|大概率|必|稳|确保|保证)"
            r"[^。！？\n]{0,24}(?:获奖|夺奖|拿奖|冠军|登顶)",
        ),
    ),
    (
        "prize result assertion",
        re.compile(
            r"(?:获得|赢得|斩获|拿下|夺得)[^。！？\n]{0,16}"
            r"(?:奖项|获奖|一等奖|二等奖|三等奖|冠军|奖金)",
        ),
    ),
    (
        "guarantee assertion",
        re.compile(
            r"(?:保证|确保|承诺|必然|一定|稳赢|稳胜)"
            r"[^。！？\n]{0,24}(?:胜率|获奖|夺奖|冠军|排名|名次|天梯|线上)",
        ),
    ),
)

EXPLICIT_BOUNDARY_RE = re.compile(
    r"(?:不外推|不可外推|不得外推|不能外推|不代表|不等于|不把|不对|不由|"
    r"没有|并非|无法|不会|未获|未得|未发生|尚未|未标定|未经标定|不承诺|禁止|不可用于|"
    r"仅为本地|只限本地|范围外|待人工|依赖真实线上|如实\s*null|非确认性)",
    re.IGNORECASE,
)

SENTENCE_RE = re.compile(r"[^。！？\n]+[。！？]?", re.MULTILINE)
LEVEL_ONE_HEADING_RE = re.compile(r"(?m)^\s*=\s+(?!=)(?P<title>[^\r\n]+)$")


class CheckFailure(Exception):
    """An input/loading failure that prevents consistency checks."""


def read_utf8(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise CheckFailure(f"required file is missing: {path}") from exc
    except UnicodeDecodeError as exc:
        raise CheckFailure(f"file is not valid UTF-8: {path}: {exc}") from exc
    except OSError as exc:
        raise CheckFailure(f"cannot read {path}: {exc}") from exc


def load_metrics(path: Path) -> dict[str, Any]:
    raw = read_utf8(path)
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CheckFailure(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(value, dict):
        raise CheckFailure(f"metrics root must be a JSON object: {path}")
    return value


def strip_typst_comments(text: str) -> str:
    """Replace Typst comments with spaces while preserving newlines/offsets."""
    chars = list(text)
    index = 0
    quote: str | None = None
    escaped = False
    block_depth = 0

    while index < len(chars):
        current = chars[index]
        following = chars[index + 1] if index + 1 < len(chars) else ""

        if block_depth:
            if current == "/" and following == "*":
                chars[index] = chars[index + 1] = " "
                block_depth += 1
                index += 2
            elif current == "*" and following == "/":
                chars[index] = chars[index + 1] = " "
                block_depth -= 1
                index += 2
            else:
                if current not in "\r\n":
                    chars[index] = " "
                index += 1
            continue

        if quote is not None:
            if escaped:
                escaped = False
            elif current == "\\":
                escaped = True
            elif current == quote:
                quote = None
            index += 1
            continue

        if current in ('"', "'"):
            quote = current
            index += 1
        elif current == "/" and following == "/":
            while index < len(chars) and chars[index] not in "\r\n":
                chars[index] = " "
                index += 1
        elif current == "/" and following == "*":
            chars[index] = chars[index + 1] = " "
            block_depth = 1
            index += 2
        else:
            index += 1

    return "".join(chars)


def _mask_range(chars: list[str], start: int, end: int) -> None:
    for index in range(start, min(end, len(chars))):
        if chars[index] not in "\r\n":
            chars[index] = " "


def mask_typst_dynamic_expressions(text: str) -> str:
    """Mask code-only expressions without hiding markup inside tables/blocks."""
    chars = list(text)
    index = 0
    inline_render_functions = {"fmt", "raw", "repr", "str"}
    while index < len(chars):
        if chars[index] != "#":
            index += 1
            continue

        start = index
        cursor = index + 1
        while cursor < len(chars) and chars[cursor].isspace() and chars[cursor] not in "\r\n":
            cursor += 1

        name_match = re.match(r"[A-Za-z_][A-Za-z0-9_-]*", "".join(chars[cursor:]))
        name: str | None = None
        if name_match:
            name = name_match.group(0)
            cursor += len(name)
            if name in {"let", "set", "show", "import", "include"}:
                end = cursor
                while end < len(chars) and chars[end] not in "\r\n":
                    end += 1
                _mask_range(chars, start, end)
                index = end
                continue
            while cursor < len(chars) and chars[cursor].isspace() and chars[cursor] not in "\r\n":
                cursor += 1

        if cursor >= len(chars) or chars[cursor] not in "({":
            index += 1
            continue
        if name is not None and name not in inline_render_functions:
            index += 1
            continue

        opening = chars[cursor]
        closing = ")" if opening == "(" else "}"
        depth = 0
        quote: str | None = None
        escaped = False
        end = cursor
        while end < len(chars):
            current = chars[end]
            if quote is not None:
                if escaped:
                    escaped = False
                elif current == "\\":
                    escaped = True
                elif current == quote:
                    quote = None
            elif current in ('"', "'"):
                quote = current
            elif current == opening:
                depth += 1
            elif current == closing:
                depth -= 1
                if depth == 0:
                    end += 1
                    break
            end += 1
        _mask_range(chars, start, end)
        index = max(end, index + 1)

    return "".join(chars)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def metric_containers(metrics: dict[str, Any], errors: list[str]) -> tuple[dict[str, Any], dict[str, Any]]:
    software = metrics.get("software")
    if not isinstance(software, dict):
        errors.append("workspace/metrics.json: missing object at software")
        return {}, {}

    measured = software.get("metrics")
    unmeasured = software.get("unmeasured")
    if not isinstance(measured, dict):
        errors.append("workspace/metrics.json: missing object at software.metrics")
        measured = {}
    if not isinstance(unmeasured, dict):
        errors.append("workspace/metrics.json: missing object at software.unmeasured")
        unmeasured = {}
    return measured, unmeasured


def check_metric_references(
    report: str,
    measured: dict[str, Any],
    unmeasured: dict[str, Any],
    errors: list[str],
) -> tuple[set[tuple[str, str]], int]:
    references = {
        (match.group("kind"), match.group("key"))
        for match in METRIC_REFERENCE_RE.finditer(report)
    }
    dangling = 0
    for kind, key in sorted(references):
        namespace = measured if kind == "m" else unmeasured
        resolved = namespace.get(key)
        qualified = f"software.{'metrics' if kind == 'm' else 'unmeasured'}.{key}"
        if not isinstance(resolved, dict) or "value" not in resolved:
            dangling += 1
            errors.append(
                f'dangling {kind}("{key}"): {qualified} must resolve to an object containing "value"'
            )

    required_references = {
        *(("m", key) for key in REQUIRED_SOFTWARE_KEYS),
        *(("m", key) for key in REQUIRED_SOFTWARE_R3_KEYS),
        *(("um", key) for key in REQUIRED_UNMEASURED_KEYS),
    }
    for kind, key in sorted(required_references - references):
        errors.append(f'report is missing required reference {kind}("{key}")')

    for kind, key in sorted(required_references):
        namespace = measured if kind == "m" else unmeasured
        resolved = namespace.get(key)
        qualified = f"software.{'metrics' if kind == 'm' else 'unmeasured'}.{key}"
        if not isinstance(resolved, dict) or "value" not in resolved:
            errors.append(f'required metric {qualified} is not an object containing "value"')

    return references, dangling


def check_rewrite_markers(source: str, errors: list[str]) -> list[str]:
    missing: list[str] = []
    for marker in REWRITE_MARKERS:
        marker_re = re.compile(rf"(?m)^\s*// CHECK:{re.escape(marker)}\s*$")
        count = len(marker_re.findall(source))
        if count == 0:
            missing.append(marker)
            errors.append(f"missing exact rewrite marker line: // CHECK:{marker}")
        elif count > 1:
            errors.append(
                f"rewrite marker must occur exactly once: // CHECK:{marker} (found {count})"
            )
    return missing


def check_historical_disclosures(report_text: str, errors: list[str]) -> int:
    occurrence_count = 0
    for literal in HISTORICAL_LITERALS:
        matches = list(re.finditer(re.escape(literal), report_text))
        occurrence_count += len(matches)
        if len(matches) > 1:
            lines = [line_number(report_text, match.start()) for match in matches]
            errors.append(
                f"historical literal {literal!r} may appear at most once; found on lines {lines}"
            )

    for paragraph in PARAGRAPH_SPLIT_RE.split(report_text):
        for literal in HISTORICAL_LITERALS:
            if literal not in paragraph:
                continue
            missing_tokens = [
                token for token in HISTORICAL_DISCLOSURE_TOKENS if token not in paragraph
            ]
            if missing_tokens:
                errors.append(
                    f"historical literal {literal!r} lacks adjacent disclosure tokens in its "
                    f"paragraph: {', '.join(missing_tokens)}"
                )
    return occurrence_count


def check_unkeyed_performance(report_text: str, errors: list[str]) -> int:
    hits = 0
    for label, pattern in UNKEYED_PERFORMANCE_PATTERNS:
        for match in pattern.finditer(report_text):
            hits += 1
            errors.append(
                f"unkeyed current-performance literal {match.group(0)!r} ({label}) "
                f"on report.typ line {line_number(report_text, match.start())}; render it via m()"
            )
    return hits


def _compact(value: str, limit: int = 140) -> str:
    compacted = " ".join(value.split())
    return compacted if len(compacted) <= limit else compacted[: limit - 3] + "..."


def check_prohibited_extrapolation(report_text: str, errors: list[str]) -> int:
    hits = 0
    for sentence_match in SENTENCE_RE.finditer(report_text):
        sentence = sentence_match.group(0).strip()
        if not sentence or EXPLICIT_BOUNDARY_RE.search(sentence):
            continue
        for label, pattern in PROHIBITED_CLAIM_PATTERNS:
            if pattern.search(sentence):
                hits += 1
                errors.append(
                    f"prohibited {label} on report.typ line "
                    f"{line_number(report_text, sentence_match.start())}: {_compact(sentence)!r}; "
                    "rewrite as an explicit negation or local-only boundary"
                )
                break
    return hits


def appendix_sections(report_text: str) -> dict[str, tuple[str, str]]:
    headings = list(LEVEL_ONE_HEADING_RE.finditer(report_text))
    sections: dict[str, tuple[str, str]] = {}
    for index, heading in enumerate(headings):
        title = heading.group("title").strip()
        appendix_match = re.match(r"附录\s*([AB])(?:\s*[:：-]\s*|\s+)(.*)", title, re.IGNORECASE)
        if not appendix_match:
            continue
        end = headings[index + 1].start() if index + 1 < len(headings) else len(report_text)
        sections[appendix_match.group(1).upper()] = (
            appendix_match.group(2).strip(),
            report_text[heading.end() : end].strip(),
        )
    return sections


def check_appendices(report_text: str, errors: list[str]) -> bool:
    sections = appendix_sections(report_text)
    appendix_a = sections.get("A")
    human_ai_present = bool(
        appendix_a
        and appendix_a[1]
        and re.search(r"(?:人机分工|人工[^。\n]{0,30}AI|AI[^。\n]{0,30}人工)", " ".join(appendix_a))
    )
    if not human_ai_present:
        errors.append("Appendix A must be non-empty and explicitly document human/AI responsibilities")

    appendix_b = sections.get("B")
    traceability_present = bool(
        appendix_b
        and appendix_b[1]
        and (
            re.search(r"(?:可追溯|追溯|证据索引|traceability)", " ".join(appendix_b), re.IGNORECASE)
            or 'm("confirmatory_export_traceability")' in appendix_b[1]
        )
    )
    if not traceability_present:
        errors.append(
            "Appendix B must be non-empty traceability evidence (title/body should say "
            "可追溯, 追溯, 证据索引, or reference m(\"confirmatory_export_traceability\"))"
        )
    return human_ai_present


def deduplicate(items: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(items))


def main() -> int:
    try:
        source = read_utf8(REPORT_PATH)
        metrics = load_metrics(METRICS_PATH)
    except CheckFailure as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors: list[str] = []
    uncommented = strip_typst_comments(source)
    measured, unmeasured = metric_containers(metrics, errors)
    references, dangling_count = check_metric_references(
        uncommented, measured, unmeasured, errors
    )
    missing_markers = check_rewrite_markers(source, errors)

    static_report_text = mask_typst_dynamic_expressions(uncommented)
    historical_count = check_historical_disclosures(static_report_text, errors)
    unkeyed_count = check_unkeyed_performance(static_report_text, errors)
    prohibited_count = check_prohibited_extrapolation(static_report_text, errors)
    human_ai_present = check_appendices(uncommented, errors)

    errors = deduplicate(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAILED: {len(errors)} report consistency error(s)", file=sys.stderr)
        return 1

    result = {
        "report_metric_key_references": len(references),
        "report_dangling_metric_keys": dangling_count,
        "report_unkeyed_performance_numbers": unkeyed_count,
        "report_historical_baseline_disclosures": {
            "count": historical_count,
            "status": "pass",
        },
        "report_prohibited_extrapolation_hits": prohibited_count,
        "report_human_ai_appendix_present": human_ai_present,
        "report_rewrite_mapping_coverage": {
            "required": len(REWRITE_MARKERS),
            "present": len(REWRITE_MARKERS) - len(missing_markers),
            "missing": missing_markers,
            "status": "pass",
        },
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
