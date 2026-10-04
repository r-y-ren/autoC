"""Deterministic offline forensics over source-attested 30-locus DNA barcodes."""

from __future__ import annotations

import csv
import hashlib
import math
import re
from collections import Counter, defaultdict
from datetime import date
from typing import Any, Iterable, Mapping, Sequence

LOCUS_COUNT = 30
BAND_PATTERN = re.compile(r"^[0-9a-f]{10}$")
GENOME_PATTERN = re.compile(r"^[0-9a-f]{8}$")
GROUPING_POLICY = "submission_all_input_episodes_both_seats"
SCHEMA_VERSION = "replay-dna/1.1"
VERDICT_IDENTICAL = "IDENTICAL / SAME SOURCE"
VERDICT_RELATED = "RELATED"
VERDICT_WEAK = "WEAK SIGNAL"
VERDICT_UNRELATED = "UNRELATED"
VERDICT_OUT_OF_RANGE = "OUT OF RANGE"


class ForensicsError(ValueError):
    """The supplied DNA evidence cannot be interpreted without guessing."""


def _finite(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ForensicsError(f"{field} must be a finite number")
    number = float(value)
    if not math.isfinite(number):
        raise ForensicsError(f"{field} must be a finite number")
    return number


def parse_bands(value: str | Sequence[str]) -> tuple[str, ...]:
    """Parse exactly 30 ordered lowercase ten-hex loci without zip truncation."""
    if isinstance(value, str):
        bands = value.split("-")
    elif isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        bands = list(value)
    else:
        raise ForensicsError("DNA bands must be a hyphen-delimited string or sequence")
    if len(bands) != LOCUS_COUNT:
        raise ForensicsError(f"DNA barcode must contain exactly {LOCUS_COUNT} loci")
    for index, band in enumerate(bands):
        if not isinstance(band, str) or BAND_PATTERN.fullmatch(band) is None:
            raise ForensicsError(
                f"DNA locus {index} must be a lowercase 10-character hexadecimal string")
    return tuple(bands)


def genome_id(bands: str | Sequence[str]) -> str:
    parsed = parse_bands(bands)
    return hashlib.sha1("".join(parsed).encode()).hexdigest()[:8]


def validate_genome_id(bands: str | Sequence[str], declared: Any, field: str = "genome_id") -> str:
    if not isinstance(declared, str) or GENOME_PATTERN.fullmatch(declared) is None:
        raise ForensicsError(f"{field} must be an 8-character lowercase hexadecimal SHA-1 prefix")
    expected = genome_id(bands)
    if declared != expected:
        raise ForensicsError(f"{field} mismatch: declared {declared}, expected {expected}")
    return declared


def modal_consensus(samples: Iterable[str | Sequence[str]]) -> tuple[tuple[str, ...], float, tuple[float, ...]]:
    """Return deterministic per-locus modes and mean modal agreement."""
    parsed = [parse_bands(sample) for sample in samples]
    if not parsed:
        raise ForensicsError("at least one DNA sample is required for stability")
    consensus: list[str] = []
    agreements: list[float] = []
    for locus in range(LOCUS_COUNT):
        counts = Counter(sample[locus] for sample in parsed)
        modal_count = max(counts.values())
        consensus.append(next(band for band in (sample[locus] for sample in parsed)
                              if counts[band] == modal_count))
        agreements.append(modal_count / len(parsed))
    return tuple(consensus), sum(agreements) / LOCUS_COUNT, tuple(agreements)


def validate_field_validation(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ForensicsError("field validation must be a JSON object")
    required = {
        "teams", "streams", "within_pairs", "cross_pairs", "cardinality_by_day",
        "top_share_by_day", "allele_freqs", "floor",
    }
    if set(payload) != required:
        missing = sorted(required - set(payload))
        extra = sorted(set(payload) - required)
        raise ForensicsError(f"field validation keys mismatch; missing={missing}, extra={extra}")
    for field in ("teams", "streams"):
        value = payload[field]
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ForensicsError(f"field validation {field} must be a positive integer")
    floor = _finite(payload["floor"], "field validation floor")
    if not 0.0 < floor <= 1.0:
        raise ForensicsError("field validation floor must be in (0, 1]")
    frequencies = payload["allele_freqs"]
    if not isinstance(frequencies, list) or len(frequencies) != LOCUS_COUNT:
        raise ForensicsError("field validation requires exactly 30 locus frequency tables")
    for locus, table in enumerate(frequencies):
        if not isinstance(table, dict) or not table:
            raise ForensicsError(f"field validation locus {locus} frequency table is required")
        total = 0.0
        for band, value in table.items():
            if BAND_PATTERN.fullmatch(band) is None:
                raise ForensicsError(f"field validation locus {locus} has an invalid allele")
            frequency = _finite(value, f"field validation locus {locus} frequency")
            if not 0.0 < frequency <= 1.0:
                raise ForensicsError(
                    f"field validation locus {locus} frequency must be in (0, 1]")
            total += frequency
        if not math.isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-9):
            raise ForensicsError(f"field validation locus {locus} frequencies must sum to 1")
    day_keys = {str(index) for index in range(LOCUS_COUNT)}
    for field in ("cardinality_by_day", "top_share_by_day"):
        values = payload[field]
        if not isinstance(values, dict) or set(values) != day_keys:
            raise ForensicsError(f"field validation {field} must cover loci 0 through 29")
        for key, value in values.items():
            number = _finite(value, f"field validation {field}[{key}]")
            if field == "cardinality_by_day":
                if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                    raise ForensicsError(f"field validation {field}[{key}] must be a positive integer")
            elif number < 0 or number > 1:
                raise ForensicsError(f"field validation {field}[{key}] is out of range")
    for field in ("within_pairs", "cross_pairs"):
        values = payload[field]
        if not isinstance(values, list):
            raise ForensicsError(f"field validation {field} must be an array")
        for index, value in enumerate(values):
            number = _finite(value, f"field validation {field}[{index}]")
            if not 0.0 <= number <= 1.0:
                raise ForensicsError(f"field validation {field}[{index}] is out of range")
    return payload


def _stability(value: float | None, field: str) -> float | None:
    if value is None:
        return None
    number = _finite(value, field)
    if not 0.0 <= number <= 1.0:
        raise ForensicsError(f"{field} must be in [0, 1]")
    return number


def compare_barcodes(
    bands_a: str | Sequence[str],
    bands_b: str | Sequence[str],
    field_validation: Mapping[str, Any],
    *,
    stability_a: float | None = None,
    stability_b: float | None = None,
) -> dict[str, Any]:
    """Apply the notebook's exact field-specific RMP and verdict ordering."""
    a, b = parse_bands(bands_a), parse_bands(bands_b)
    field = validate_field_validation(dict(field_validation))
    stability_a = _stability(stability_a, "stability_a")
    stability_b = _stability(stability_b, "stability_b")
    matches = tuple(left == right for left, right in zip(a, b, strict=True))
    matched = sum(matches)
    log10_rmp = 0.0
    matched_frequencies: list[float] = []
    for locus, is_match in enumerate(matches):
        if is_match:
            frequency = max(field["floor"], field["allele_freqs"][locus].get(a[locus], field["floor"]))
            matched_frequencies.append(float(frequency))
            log10_rmp += math.log10(frequency)
    rmp = 10 ** log10_rmp if matched else 1.0
    fork_day = next((locus for locus, is_match in enumerate(matches) if not is_match), None)
    if matched == LOCUS_COUNT:
        base_verdict = VERDICT_IDENTICAL
    elif matched >= 2 and rmp < 1e-4:
        base_verdict = VERDICT_RELATED
    elif rmp < 1e-2:
        base_verdict = VERDICT_WEAK
    else:
        base_verdict = VERDICT_UNRELATED
    available = [value for value in (stability_a, stability_b) if value is not None]
    if not available:
        assessment = "stability_unassessed"
    elif len(available) == 1:
        assessment = "stability_partially_assessed"
    else:
        assessment = "stability_assessed"
    minimum_stability = min(available) if available else None
    verdict = (VERDICT_OUT_OF_RANGE
               if base_verdict == VERDICT_UNRELATED and
               minimum_stability is not None and minimum_stability < 0.6
               else base_verdict)
    return {
        "matched_loci": matched,
        "match_ratio": matched / LOCUS_COUNT,
        "fork_day": fork_day,
        "log10_rmp": log10_rmp,
        "rmp": rmp,
        "base_verdict": base_verdict,
        "verdict": verdict,
        "stability_a": stability_a,
        "stability_b": stability_b,
        "minimum_assessed_stability": minimum_stability,
        "stability_assessment": assessment,
        "field_frequency_floor": float(field["floor"]),
        "matched_frequencies": matched_frequencies,
    }


def _read_csv(path: Path, required: set[str], allowed: set[str]) -> list[dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            headers = reader.fieldnames
            if headers is None:
                raise ForensicsError(f"{path.name} has no CSV header")
            if len(headers) != len(set(headers)):
                raise ForensicsError(f"{path.name} has duplicate CSV headers")
            missing, extra = required - set(headers), set(headers) - allowed
            if missing or extra:
                raise ForensicsError(
                    f"{path.name} columns mismatch; missing={sorted(missing)}, extra={sorted(extra)}")
            rows = list(reader)
    except OSError as exc:
        raise ForensicsError(f"cannot read {path}: {exc}") from exc
    if not rows:
        raise ForensicsError(f"{path.name} must contain at least one record")
    if any(None in row for row in rows):
        raise ForensicsError(f"{path.name} contains a malformed CSV row")
    return rows


def load_authoritative_sources(
    barcodes_path: Path,
    consensus_path: Path,
    references_path: Path,
    field_validation_path: Path,
) -> dict[str, Any]:
    barcode_required = {
        "capture_batch", "submission", "team", "seat", "episode_id", "genome_id", "dna_bands",
    }
    barcode_allowed = barcode_required | {
        "opponent", "bank", "opponent_bank", "sem_bands", "lineage_d5", "lineage_d10", "lineage_d20",
    }
    consensus_required = {
        "capture_batch", "submission", "team", "episodes", "genome_id", "self_agreement", "dna_bands",
    }
    consensus_allowed = consensus_required | {"sem_bands", "lineage_d5", "lineage_d10", "lineage_d20"}
    reference_required = {"label", "kind", "genome_id", "dna_bands"}
    barcode_rows = _read_csv(barcodes_path, barcode_required, barcode_allowed)
    consensus_rows = _read_csv(consensus_path, consensus_required, consensus_allowed)
    reference_rows = _read_csv(references_path, reference_required, reference_required)
    try:
        import json
        field = json.loads(field_validation_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ForensicsError(f"cannot read field_validation.json: {exc}") from exc
    validate_field_validation(field)

    samples: list[dict[str, Any]] = []
    seen_samples: set[tuple[str, str, int, str]] = set()
    for row_number, row in enumerate(barcode_rows, 2):
        try:
            seat = int(row["seat"])
        except ValueError as exc:
            raise ForensicsError(f"barcodes.csv row {row_number} seat must be 0 or 1") from exc
        if seat not in (0, 1):
            raise ForensicsError(f"barcodes.csv row {row_number} seat must be 0 or 1")
        if not all(row[field_name] for field_name in (
                "capture_batch", "submission", "team", "episode_id", "genome_id", "dna_bands")):
            raise ForensicsError(f"barcodes.csv row {row_number} has an empty identity field")
        try:
            date.fromisoformat(row["capture_batch"])
        except ValueError as exc:
            raise ForensicsError(f"barcodes.csv row {row_number} capture_batch must be ISO date") from exc
        bands = parse_bands(row["dna_bands"])
        validate_genome_id(bands, row["genome_id"], f"barcodes.csv row {row_number} genome_id")
        identity = (row["submission"], row["team"], seat, row["episode_id"])
        if identity in seen_samples:
            raise ForensicsError(f"barcodes.csv has duplicate submission/team/seat/episode identity {identity}")
        seen_samples.add(identity)
        samples.append({
            "capture_date": row["capture_batch"], "submission": row["submission"],
            "team": row["team"], "seat": seat, "episode_id": row["episode_id"],
            "bands": list(bands), "genome_id": row["genome_id"],
        })

    supplied_consensus: list[dict[str, Any]] = []
    seen_consensus: set[tuple[str, str, str]] = set()
    for row_number, row in enumerate(consensus_rows, 2):
        if not row["capture_batch"] or not row["submission"] or not row["team"]:
            raise ForensicsError(f"consensus.csv row {row_number} has an empty identity field")
        try:
            date.fromisoformat(row["capture_batch"])
        except ValueError as exc:
            raise ForensicsError(f"consensus.csv row {row_number} capture_batch must be ISO date") from exc
        key = (row["capture_batch"], row["submission"], row["team"])
        if key in seen_consensus:
            raise ForensicsError(f"consensus.csv has duplicate capture/submission/team identity {key}")
        seen_consensus.add(key)
        try:
            episodes = int(row["episodes"])
            agreement = float(row["self_agreement"])
        except ValueError as exc:
            raise ForensicsError(f"consensus.csv row {row_number} has invalid numeric data") from exc
        if episodes <= 0:
            raise ForensicsError(f"consensus.csv row {row_number} episodes must be positive")
        agreement = _stability(agreement, f"consensus.csv row {row_number} self_agreement")
        bands = parse_bands(row["dna_bands"])
        validate_genome_id(bands, row["genome_id"], f"consensus.csv row {row_number} genome_id")
        supplied_consensus.append({
            "capture_date": row["capture_batch"], "submission": row["submission"],
            "team": row["team"], "episodes": episodes, "genome_id": row["genome_id"],
            "bands": list(bands), "producer_self_agreement": agreement,
            "authority": "producer_attested_unseated_not_stability_authority",
        })

    references: list[dict[str, Any]] = []
    seen_labels: set[str] = set()
    for row_number, row in enumerate(reference_rows, 2):
        if not row["label"] or row["label"] in seen_labels:
            raise ForensicsError(f"reference_barcodes.csv row {row_number} label must be unique and non-empty")
        seen_labels.add(row["label"])
        bands = parse_bands(row["dna_bands"])
        validate_genome_id(bands, row["genome_id"],
                           f"reference_barcodes.csv row {row_number} genome_id")
        references.append({"label": row["label"], "kind": row["kind"] or "unspecified",
                           "genome_id": row["genome_id"], "bands": list(bands)})
    return {"samples": samples, "supplied_consensus": supplied_consensus,
            "references": references, "field_validation": field}


def derive_forensics(source_data: Mapping[str, Any]) -> dict[str, Any]:
    samples = list(source_data["samples"])
    references = list(source_data["references"])
    field = source_data["field_validation"]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for sample in samples:
        grouped[sample["submission"]].append(sample)
    groups: list[dict[str, Any]] = []
    for submission in sorted(grouped):
        rows = grouped[submission]
        teams = {row["team"] for row in rows}
        if len(teams) != 1:
            raise ForensicsError(f"submission {submission} maps to multiple teams")
        team = next(iter(teams))
        # The source notebook computes one submission-wide consensus across both seats;
        # retain seat only in the underlying samples, never as a consensus partition.
        consensus, stability, locus_agreements = modal_consensus(row["bands"] for row in rows)
        groups.append({
            "group_id": f"submission={submission}",
            "grouping": GROUPING_POLICY,
            "submission": submission,
            "team": team,
            "episode_count": len(rows),
            "episode_ids": [row["episode_id"] for row in rows],
            "capture_dates": sorted({row["capture_date"] for row in rows}),
            "consensus_bands": list(consensus),
            "consensus_genome_id": genome_id(consensus),
            "stability": stability,
            "locus_agreements": list(locus_agreements),
            "liveness_scope": "dna_sample_stability_only",
            "engine_activity_evidence": False,
        })
    comparisons: list[dict[str, Any]] = []
    for group in groups:
        for reference in sorted(references, key=lambda row: row["label"]):
            result = compare_barcodes(
                group["consensus_bands"], reference["bands"], field,
                stability_a=group["stability"], stability_b=None)
            comparisons.append({
                "group_id": group["group_id"], "group_genome_id": group["consensus_genome_id"],
                "reference_label": reference["label"], "reference_genome_id": reference["genome_id"],
                **result,
            })
    verdict_counts = Counter(row["verdict"] for row in comparisons)
    return {
        "samples": samples,
        "groups": groups,
        "supplied_consensus": list(source_data["supplied_consensus"]),
        "references": references,
        "comparisons": comparisons,
        "summary": {
            "sample_count": len(samples), "group_count": len(groups),
            "supplied_consensus_count": len(source_data["supplied_consensus"]),
            "reference_count": len(references), "comparison_count": len(comparisons),
            "verdict_counts": {key: verdict_counts.get(key, 0) for key in (
                VERDICT_IDENTICAL, VERDICT_RELATED, VERDICT_WEAK,
                VERDICT_UNRELATED, VERDICT_OUT_OF_RANGE)},
            "stability_below_0_6_groups": sum(group["stability"] < 0.6 for group in groups),
            "stability_unassessed_comparisons": sum(
                row["stability_assessment"] == "stability_unassessed" for row in comparisons),
        },
    }
