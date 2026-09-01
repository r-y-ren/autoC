"""Offline DNA forensics and integrity contract regressions."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path

import pytest

from kgenv.dna_forensics import (
    ForensicsError,
    compare_barcodes,
    genome_id,
    modal_consensus,
    parse_bands,
    validate_field_validation,
)
from kgenv.dna_integrity import (
    IntegrityError,
    assert_finite_numbers,
    assert_no_forbidden_fields,
    canonical_artifact_digest,
    validate_artifacts,
    validate_input_path,
    validate_output_dir,
)


def _bands(prefix: str = "a", *, count: int = 30) -> list[str]:
    return [f"{prefix}{index:09x}" for index in range(count)]


def _field(*, floor: float = 0.01) -> dict:
    teams = round(1 / floor)
    return {
        "teams": teams,
        "streams": 110,
        "within_pairs": [1.0],
        "cross_pairs": [0.0],
        "cardinality_by_day": {str(i): 1 for i in range(30)},
        "top_share_by_day": {str(i): 1.0 for i in range(30)},
        "allele_freqs": [
            {**{f"{j:010x}": floor for j in range(teams - 1)},
             f"{teams - 1:010x}": 1.0 - floor * (teams - 1)}
            for _ in range(30)
        ],
        "floor": floor,
    }


def test_strict_bands_and_sha1_genome_id():
    bands = _bands()
    assert parse_bands("-".join(bands)) == tuple(bands)
    expected = hashlib.sha1("".join(bands).encode()).hexdigest()[:8]
    assert genome_id(bands) == expected
    assert genome_id(parse_bands("-".join(bands))) == expected
    repeated_locus = [*bands[:-1], bands[-2]]
    assert parse_bands(repeated_locus) == tuple(repeated_locus)
    for invalid in (_bands(count=29), _bands(count=31), [*bands[:-1], "ABCDEF1234"],
                    [*bands[:-1], "abc"]):
        with pytest.raises(ForensicsError, match="30|lowercase"):
            parse_bands(invalid)


def test_modal_stability_uses_all_rows_and_deterministic_tie_break():
    low, high = _bands("a"), _bands("b")
    low[0], high[0] = "0000000001", "0000000002"
    consensus, stability, agreements = modal_consensus([high, low])
    assert consensus[0] == "0000000002"
    assert agreements[0] == 0.5
    assert stability == 0.5
    one, one_stability, _ = modal_consensus([low])
    assert one == tuple(low) and one_stability == 1.0
    with pytest.raises(ForensicsError, match="sample"):
        modal_consensus([])


def test_exact_rmp_verdict_thresholds_and_out_of_range():
    a = _bands()
    unrelated = _bands("b")
    field = _field(floor=0.01)

    identical = compare_barcodes(a, a, field, stability_a=1.0, stability_b=1.0)
    assert identical["verdict"] == "IDENTICAL / SAME SOURCE"
    assert identical["matched_loci"] == 30 and identical["fork_day"] is None

    related_field = _field(floor=0.009)
    two = unrelated.copy()
    two[:2] = a[:2]
    related = compare_barcodes(a, two, related_field)
    assert related["rmp"] < 1e-4 and related["verdict"] == "RELATED"

    equality_field = _field(floor=0.01)
    equality = compare_barcodes(a, two, equality_field)
    assert equality["rmp"] == pytest.approx(1e-4)
    assert equality["verdict"] == "WEAK SIGNAL"

    one = unrelated.copy()
    one[0] = a[0]
    weak = compare_barcodes(a, one, _field(floor=0.009))
    assert weak["verdict"] == "WEAK SIGNAL"
    equal_weak = compare_barcodes(a, one, _field(floor=0.01))
    assert equal_weak["verdict"] == "UNRELATED"

    refused = compare_barcodes(a, unrelated, field, stability_a=0.599, stability_b=1.0)
    assert refused["base_verdict"] == "UNRELATED"
    assert refused["verdict"] == "OUT OF RANGE"
    boundary = compare_barcodes(a, unrelated, field, stability_a=0.6, stability_b=1.0)
    assert boundary["verdict"] == "UNRELATED"
    unassessed = compare_barcodes(a, unrelated, field)
    assert unassessed["verdict"] == "UNRELATED"
    assert unassessed["stability_assessment"] == "stability_unassessed"


@pytest.mark.parametrize("mutate", [
    lambda f: f.update(floor=0.0),
    lambda f: f.update(floor=float("nan")),
    lambda f: f.update(allele_freqs=f["allele_freqs"][:-1]),
    lambda f: f["allele_freqs"][0].update({"a000000000": float("inf")}),
    lambda f: f["allele_freqs"].__setitem__(0, None),
])
def test_field_validation_fails_closed(mutate):
    field = _field()
    mutate(field)
    with pytest.raises(ForensicsError, match="floor|frequency|30|locus"):
        validate_field_validation(field)


def test_forbidden_fields_and_nonfinite_numbers_fail_closed():
    assert_no_forbidden_fields({"groups": [{"stability": 0.9}], "evidence_scope": {
        "dna_liveness_only": True, "engine_activity_evidence": False,
        "strength_claim": False,
    }})
    for payload in ({"nested": {"action": "PASS"}}, {"rows": [{"inventory": {}}]},
                    {"raw_trace": []}, {"steps": 720}, {"price": 1},
                    {"market_state": {}}, {"action_log": []}):
        with pytest.raises(IntegrityError, match="forbidden"):
            assert_no_forbidden_fields(payload)
    for value in (float("nan"), float("inf"), float("-inf")):
        with pytest.raises(IntegrityError, match="non-finite"):
            assert_finite_numbers({"nested": [value]})


def test_input_and_output_path_guards(tmp_path):
    dna = tmp_path / ".tmp-dna"
    dna.mkdir()
    allowed = dna / "barcodes.csv"
    allowed.write_text("submission,team,seat,episode_id,genome_id,dna_bands\n", encoding="utf-8")
    assert validate_input_path(allowed, "barcodes.csv") == allowed.resolve()
    for invalid in ("https://example.com/barcodes.csv", tmp_path / "barcodes.csv",
                    dna / "eval_results.json", tmp_path / "holdout" / "barcodes.csv"):
        with pytest.raises(IntegrityError, match=r"local|\.tmp-dna|basename|holdout|input"):
            validate_input_path(invalid, "barcodes.csv")

    software = tmp_path / "workspace" / "software"
    output = software / "exports" / "replay_dna"
    output.mkdir(parents=True)
    assert validate_output_dir(output, software) == output.resolve()
    with pytest.raises(IntegrityError, match="replay_dna"):
        validate_output_dir(software / "exports" / "holdout", software)


def _write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _source_fixture(root: Path) -> dict[str, Path]:
    dna = root / ".tmp-dna"
    dna.mkdir()
    b0, b1 = _bands(), _bands()
    b1[-1] = "b00000001d"
    barcode_rows = []
    for episode, seat, bands in (("10", 0, b0), ("10", 1, b1), ("12", 1, b0)):
        barcode_rows.append({
            "capture_batch": "2026-08-31", "submission": "42", "team": "team-a",
            "seat": seat, "episode_id": episode, "opponent": "other", "bank": "1",
            "opponent_bank": "2", "genome_id": genome_id(bands),
            "dna_bands": "-".join(bands), "sem_bands": "x", "lineage_d5": "x",
            "lineage_d10": "x", "lineage_d20": "x",
        })
    _write_csv(dna / "barcodes.csv", list(barcode_rows[0]), barcode_rows)
    consensus = [{"capture_batch": "2026-08-31", "submission": "42", "team": "team-a",
                  "episodes": "3", "genome_id": genome_id(b0), "self_agreement": "0.9",
                  "dna_bands": "-".join(b0), "sem_bands": "x", "lineage_d5": "x",
                  "lineage_d10": "x", "lineage_d20": "x"}]
    _write_csv(dna / "consensus.csv", list(consensus[0]), consensus)
    refs = [{"label": "ref-a", "kind": "route", "genome_id": genome_id(b0),
             "dna_bands": "-".join(b0)}]
    _write_csv(dna / "reference_barcodes.csv", list(refs[0]), refs)
    (dna / "field_validation.json").write_text(json.dumps(_field()), encoding="utf-8")
    return {name: dna / name for name in (
        "barcodes.csv", "consensus.csv", "reference_barcodes.csv", "field_validation.json")}


def test_cli_generation_and_verify_detect_source_and_digest_drift(tmp_path):
    from scripts import analyze_dna_forensics

    sources = _source_fixture(tmp_path)
    software = tmp_path / "workspace" / "software"
    output = software / "exports" / "replay_dna"
    output.mkdir(parents=True)
    repo_schema = Path(__file__).parents[1] / "exports" / "replay_dna" / "dna_schema.json"
    schema = output / "dna_schema.json"
    schema.write_bytes(repo_schema.read_bytes())

    args = []
    for flag, name in (("--barcodes", "barcodes.csv"), ("--consensus", "consensus.csv"),
                       ("--references", "reference_barcodes.csv"),
                       ("--field-validation", "field_validation.json")):
        args.extend([flag, str(sources[name])])
    args.extend(["--output-dir", str(output)])
    assert analyze_dna_forensics.main(args, software_root=software) == 0
    result = validate_artifacts(output / "index.json", output / "report.json", schema,
                                software_root=software)
    assert result["samples"] == 3 and result["groups"] == 1
    report = json.loads((output / "report.json").read_text(encoding="utf-8"))
    assert all(group["grouping"] == "submission_all_input_episodes_both_seats"
               for group in report["groups"])
    assert all("seat" not in group for group in report["groups"])
    assert report["evidence_scope"]["extractor_status"] == "source_extractor_not_published"
    assert report["evidence_scope"]["engine_activity_evidence"] is False

    index_path = output / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    index["counts"]["samples"] += 1
    index_path.write_text(json.dumps(index), encoding="utf-8")
    with pytest.raises(IntegrityError, match="index canonical digest"):
        validate_artifacts(index_path, output / "report.json", schema, software_root=software)

    index["digests"]["canonical_payload_sha256"] = canonical_artifact_digest(index)
    index_path.write_text(json.dumps(index), encoding="utf-8")
    with pytest.raises(IntegrityError, match="counts mismatch"):
        validate_artifacts(index_path, output / "report.json", schema, software_root=software)

    assert analyze_dna_forensics.main(args, software_root=software) == 0
    report = json.loads((output / "report.json").read_text(encoding="utf-8"))
    forged = copy.deepcopy(report)
    forged["groups"][0]["stability"] = 1.0
    forged["digests"]["canonical_payload_sha256"] = canonical_artifact_digest(forged)
    (output / "report.json").write_text(json.dumps(forged), encoding="utf-8")
    with pytest.raises(IntegrityError, match="stability|report SHA"):
        validate_artifacts(output / "index.json", output / "report.json", schema,
                           software_root=software)

    assert analyze_dna_forensics.main(args, software_root=software) == 0
    report_path = output / "report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    index = json.loads(index_path.read_text(encoding="utf-8"))
    report["source_manifest"][0]["role"] = "forged_role"
    report["digests"]["canonical_payload_sha256"] = canonical_artifact_digest(report)
    report_data = (json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    report_path.write_bytes(report_data)
    index["source_manifest"] = copy.deepcopy(report["source_manifest"])
    index["report_sha256"] = hashlib.sha256(report_data).hexdigest()
    index["digests"]["canonical_payload_sha256"] = canonical_artifact_digest(index)
    index_path.write_text(json.dumps(index), encoding="utf-8")
    with pytest.raises(IntegrityError, match="manifest metadata"):
        validate_artifacts(index_path, report_path, schema, software_root=software)

    assert analyze_dna_forensics.main(args, software_root=software) == 0
    sources["barcodes.csv"].write_text(
        sources["barcodes.csv"].read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(IntegrityError, match="source SHA"):
        validate_artifacts(output / "index.json", output / "report.json", schema,
                           software_root=software)


def test_source_dates_fail_closed_before_artifact_write(tmp_path):
    from scripts import analyze_dna_forensics

    sources = _source_fixture(tmp_path)
    sources["barcodes.csv"].write_text(
        sources["barcodes.csv"].read_text(encoding="utf-8").replace("2026-08-31", "2026-02-30"),
        encoding="utf-8")
    software = tmp_path / "workspace" / "software"
    output = software / "exports" / "replay_dna"
    output.mkdir(parents=True)
    schema = Path(__file__).parents[1] / "exports" / "replay_dna" / "dna_schema.json"
    (output / "dna_schema.json").write_bytes(schema.read_bytes())
    args = ["--barcodes", str(sources["barcodes.csv"]),
            "--consensus", str(sources["consensus.csv"]),
            "--references", str(sources["reference_barcodes.csv"]),
            "--field-validation", str(sources["field_validation.json"]),
            "--output-dir", str(output)]
    assert analyze_dna_forensics.main(args, software_root=software) == 1
    assert not (output / "report.json").exists()


def test_cli_rejects_software_root_override():
    from scripts import analyze_dna_forensics, check_dna_forensics

    with pytest.raises(SystemExit):
        analyze_dna_forensics.build_parser().parse_args(["--software-root", "elsewhere"])
    with pytest.raises(SystemExit):
        check_dna_forensics.build_parser().parse_args(["--software-root", "elsewhere"])


def test_cli_rejects_raw_replay_columns_before_writing(tmp_path):
    from scripts import analyze_dna_forensics

    sources = _source_fixture(tmp_path)
    text = sources["barcodes.csv"].read_text(encoding="utf-8")
    sources["barcodes.csv"].write_text(text.replace("opponent,", "action,"), encoding="utf-8")
    software = tmp_path / "workspace" / "software"
    output = software / "exports" / "replay_dna"
    output.mkdir(parents=True)
    args = ["--barcodes", str(sources["barcodes.csv"]), "--consensus", str(sources["consensus.csv"]),
            "--references", str(sources["reference_barcodes.csv"]),
            "--field-validation", str(sources["field_validation.json"]),
            "--output-dir", str(output)]
    assert analyze_dna_forensics.main(args, software_root=software) == 1
    assert not (output / "report.json").exists()
