#!/usr/bin/env python3
"""
Establish bidirectional links between a paper markdown file and its image assets.

Workflow:
1. Parse a Zotero-style annotation markdown file in raw/assets/.
2. Extract image file keys, page labels, and figure/table captions.
3. Update the paper markdown with:
   - a top-level "图像索引" section
   - anchor links for figures/tables
   - corrected image references before figure captions
4. Update raw/assets/<paper>/README.md with links back to the paper anchors.

Example:
    python3 establish_image_links.py \
      --markdown ../markdown/chen2025JointTrajectoryOptimization.md \
      --annotation "../assets/注释-(2026-4-7-08-49-50)-BSPCU9EX.md"
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


IMAGE_LINK_RE = re.compile(r"!\[[^\]]*\]\((?P<path>[^)]+)\)")
FIGURE_CAPTION_RE = re.compile(
    r"^(?:Fig\.\s*(?P<fig_num_short>\d+)\.\s*|Figure\s+(?P<fig_num_long>\d+)\s*)"
    r"(?:(?:\([^)]*\))\s*)?(?P<desc>.+?)\s*$",
    re.IGNORECASE,
)
TABLE_CAPTION_RE = re.compile(
    r"^Table\s+(?P<table_num>(?:[IVXLCDM]+|\d+))\.?\s*(?P<desc>.*)$",
    re.IGNORECASE,
)
PAGE_RE = re.compile(r"p\.\s*(\d+)")
PAGE_LABEL_RE = re.compile(r"pageLabel%22%3A%22([^%]+)%22")
LOCATOR_RE = re.compile(r"locator%22%3A%22([^%]+)%22")


@dataclass
class AssetEntry:
    kind: str
    number: str
    anchor_id: str
    page_label: str
    image_file: str
    caption: str
    description: str
    paper_label: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build bidirectional links between a paper markdown file and its image assets."
    )
    parser.add_argument(
        "--markdown",
        required=True,
        type=Path,
        help="Path to the paper markdown file, e.g. raw/markdown/chen2025JointTrajectoryOptimization.md",
    )
    parser.add_argument(
        "--annotation",
        required=True,
        type=Path,
        help="Path to the Zotero annotation markdown file in raw/assets/",
    )
    parser.add_argument(
        "--assets-dir",
        type=Path,
        help="Path to the asset folder. Defaults to raw/assets/<markdown stem>/",
    )
    parser.add_argument(
        "--delete-annotation",
        action="store_true",
        help="Delete the annotation markdown after successful generation. Use only after verifying output.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    markdown_path = args.markdown.resolve()
    annotation_path = args.annotation.resolve()
    assets_dir = (
        args.assets_dir.resolve()
        if args.assets_dir
        else markdown_path.parent.parent / "assets" / markdown_path.stem
    )

    validate_paths(markdown_path, annotation_path, assets_dir)
    entries = parse_annotation(annotation_path, assets_dir)
    if not entries:
        raise SystemExit(f"No figure or table mappings were parsed from: {annotation_path}")

    markdown_content = markdown_path.read_text(encoding="utf-8")
    markdown_content, warnings = update_markdown(markdown_content, markdown_path, assets_dir, entries)
    markdown_path.write_text(markdown_content, encoding="utf-8")

    readme_path = assets_dir / "README.md"
    readme_path.write_text(build_assets_readme(markdown_path, assets_dir, entries), encoding="utf-8")

    print(f"Updated markdown: {markdown_path}")
    print(f"Updated assets index: {readme_path}")
    print(f"Parsed {len(entries)} image mappings from: {annotation_path.name}")
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  - {warning}")

    if args.delete_annotation:
        annotation_path.unlink()
        print(f"\nDeleted annotation source: {annotation_path}")


def validate_paths(markdown_path: Path, annotation_path: Path, assets_dir: Path) -> None:
    if not markdown_path.is_file():
        raise SystemExit(f"Markdown file not found: {markdown_path}")
    if not annotation_path.is_file():
        raise SystemExit(f"Annotation file not found: {annotation_path}")
    if not assets_dir.is_dir():
        raise SystemExit(f"Assets directory not found: {assets_dir}")


def parse_annotation(annotation_path: Path, assets_dir: Path) -> list[AssetEntry]:
    lines = annotation_path.read_text(encoding="utf-8").splitlines()
    entries: list[AssetEntry] = []

    for index, line in enumerate(lines):
        image_match = re.search(r"attachments/([A-Za-z0-9]+\.png)", line)
        if not image_match:
            continue

        image_file = image_match.group(1)
        if not (assets_dir / image_file).exists():
            continue

        caption_line = next_nonempty_line(lines, index + 1)
        if caption_line is None:
            continue

        caption = extract_caption(caption_line)
        if not caption:
            continue

        page_label = extract_page_label(line, caption_line)
        entry = build_entry(image_file, page_label, caption)
        if entry is None:
            continue

        entries.append(entry)

    deduped: list[AssetEntry] = []
    seen = set()
    for entry in entries:
        key = (entry.kind, entry.number, entry.image_file)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(entry)
    return deduped


def next_nonempty_line(lines: list[str], start: int) -> str | None:
    for idx in range(start, len(lines)):
        if lines[idx].strip():
            return lines[idx].strip()
    return None


def extract_caption(raw_line: str) -> str:
    line = raw_line
    if "</span>" in line:
        line = line.split("</span>")[-1]
    line = re.sub(r"<[^>]+>", "", line)
    line = line.replace("\\", "").strip()
    line = re.sub(r"\s+", " ", line)
    line = re.sub(r"\s+([.,;:])", r"\1", line)
    if not line:
        return ""
    return line


def extract_page_label(image_line: str, caption_line: str) -> str:
    for pattern in (PAGE_RE, PAGE_LABEL_RE, LOCATOR_RE):
        for source in (caption_line, image_line):
            match = pattern.search(source)
            if match:
                return match.group(1)
    return "-"


def build_entry(image_file: str, page_label: str, caption: str) -> AssetEntry | None:
    figure_match = FIGURE_CAPTION_RE.match(caption)
    if figure_match:
        number = figure_match.group("fig_num_short") or figure_match.group("fig_num_long")
        description = normalize_text(figure_match.group("desc"))
        return AssetEntry(
            kind="figure",
            number=number,
            anchor_id=f"fig-{number}",
            page_label=page_label,
            image_file=image_file,
            caption=f"Fig. {number}. {description}",
            description=description,
            paper_label=f"Fig. {number}",
        )

    table_match = TABLE_CAPTION_RE.match(caption)
    if table_match:
        table_number = table_match.group("table_num").upper()
        description = sentence_case_if_upper(normalize_text(table_match.group("desc")))
        anchor_suffix = roman_to_int(table_number) or table_number.lower()
        anchor_id = f"table-{anchor_suffix}"
        caption_text = f"Table {table_number}" if not description else f"Table {table_number}. {description}"
        return AssetEntry(
            kind="table",
            number=table_number,
            anchor_id=anchor_id,
            page_label=page_label,
            image_file=image_file,
            caption=caption_text,
            description=description,
            paper_label=f"Table {table_number}",
        )

    return None


def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([.,;:])", r"\1", text)
    return text


def sentence_case_if_upper(text: str) -> str:
    if not text:
        return text
    if text.isupper():
        return text[:1] + text[1:].lower()
    return text


def roman_to_int(value: str) -> int | None:
    numerals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    prev = 0
    try:
        for char in reversed(value.upper()):
            current = numerals[char]
            if current < prev:
                total -= current
            else:
                total += current
                prev = current
    except KeyError:
        return None
    return total


def update_markdown(
    content: str,
    markdown_path: Path,
    assets_dir: Path,
    entries: list[AssetEntry],
) -> tuple[str, list[str]]:
    content = upsert_image_index_section(content, assets_dir, entries)
    lines = content.splitlines()
    warnings: list[str] = []

    for entry in entries:
        lines, warning = upsert_body_reference(lines, assets_dir.name, entry)
        if warning:
            warnings.append(warning)

    output = "\n".join(lines)
    if content.endswith("\n"):
        output += "\n"
    return output, warnings


def upsert_image_index_section(content: str, assets_dir: Path, entries: list[AssetEntry]) -> str:
    section = build_image_index_section(assets_dir, entries)
    section_re = re.compile(r'\n?<a id="image-index"></a>\n## 图像索引\n.*?(?=\n## |\Z)', re.DOTALL)
    if section_re.search(content):
        content = section_re.sub("\n" + section.rstrip() + "\n", content, count=1)
        return content

    insert_after = re.search(r"(?m)^Index Terms.*$", content)
    if insert_after:
        insertion_point = insert_after.end()
        return content[:insertion_point] + "\n\n" + section + content[insertion_point:]

    first_heading = re.search(r"(?m)^## ", content)
    if first_heading:
        return content[: first_heading.start()] + section + "\n" + content[first_heading.start() :]

    return content.rstrip() + "\n\n" + section


def build_image_index_section(assets_dir: Path, entries: Iterable[AssetEntry]) -> str:
    lines = [
        '<a id="image-index"></a>',
        "## 图像索引",
        "",
        "本索引由 `raw/scripts/establish_image_links.py` 根据注释导出的图片标注解析生成。图片目录总览见 "
        f"[{assets_dir.name}/README.md](../assets/{assets_dir.name}/README.md#asset-index)。",
        "",
        "| 图号/表号 | 论文定位 | 资源文件 | 说明 |",
        "| --- | --- | --- | --- |",
    ]
    for entry in entries:
        page_display = f"p. {entry.page_label}" if entry.page_label != "-" else "-"
        resource_link = f"[{entry.image_file}](../assets/{assets_dir.name}/{entry.image_file})"
        description = entry.description or entry.caption
        lines.append(f"| [{entry.paper_label}](#{entry.anchor_id}) | {page_display} | {resource_link} | {description} |")
    lines.append("")
    return "\n".join(lines)


def upsert_body_reference(
    lines: list[str],
    assets_dir_name: str,
    entry: AssetEntry,
) -> tuple[list[str], str | None]:
    caption_index = find_caption_index(lines, entry)
    if caption_index is None:
        return lines, f"Could not find caption in markdown for {entry.paper_label}."

    if entry.kind == "figure":
        lines, caption_index = ensure_figure_image(lines, caption_index, assets_dir_name, entry.image_file)

    lines, _ = ensure_anchor(lines, caption_index, entry.anchor_id)
    return lines, None


def find_caption_index(lines: list[str], entry: AssetEntry) -> int | None:
    if entry.kind == "figure":
        pattern = re.compile(
            rf"^\s*(?:Fig\.\s*{re.escape(entry.number)}\.|Figure\s+{re.escape(entry.number)}\b)",
            re.IGNORECASE,
        )
    else:
        pattern = re.compile(rf"^\s*Table\s+{re.escape(entry.number)}\b", re.IGNORECASE)

    for idx, line in enumerate(lines):
        if pattern.match(line.strip()):
            return idx
    return None


def ensure_figure_image(
    lines: list[str],
    caption_index: int,
    assets_dir_name: str,
    image_file: str,
) -> tuple[list[str], int]:
    image_line = f"![](../assets/{assets_dir_name}/{image_file})"
    image_index = find_nearby_image_line(lines, caption_index)

    if image_index is not None:
        lines[image_index] = image_line
        return lines, caption_index

    lines.insert(caption_index, image_line)
    lines.insert(caption_index + 1, "")
    return lines, caption_index + 2


def find_nearby_image_line(lines: list[str], caption_index: int) -> int | None:
    lower_bound = max(0, caption_index - 8)
    for idx in range(caption_index - 1, lower_bound - 1, -1):
        stripped = lines[idx].strip()
        if not stripped:
            continue
        if stripped.startswith("<a id="):
            continue
        if IMAGE_LINK_RE.fullmatch(stripped):
            return idx
    return None


def ensure_anchor(lines: list[str], caption_index: int, anchor_id: str) -> tuple[list[str], int]:
    anchor_line = f'<a id="{anchor_id}"></a>'
    window_start = max(0, caption_index - 3)
    duplicates = [idx for idx in range(window_start, caption_index + 1) if lines[idx].strip() == anchor_line]

    for idx in reversed(duplicates):
        if idx != caption_index - 1:
            lines.pop(idx)
            if idx < caption_index:
                caption_index -= 1

    if caption_index > 0 and lines[caption_index - 1].strip() == anchor_line:
        return lines, caption_index

    lines.insert(caption_index, anchor_line)
    return lines, caption_index + 1


def build_assets_readme(markdown_path: Path, assets_dir: Path, entries: Iterable[AssetEntry]) -> str:
    relative_markdown = Path("..") / ".." / "markdown" / markdown_path.name
    lines = [
        '<a id="asset-index"></a>',
        f"# Image Assets for {assets_dir.name}",
        "",
        f"This directory contains images referenced in [{markdown_path.name}]({relative_markdown.as_posix()}#image-index).",
        "",
        "The figure mapping below is generated by `raw/scripts/establish_image_links.py`, so each asset can link back to the corresponding figure/table anchor in the paper markdown.",
        "",
        "## Image Index",
        "",
        "| Image File | Figure Reference | Paper Link |",
        "|------------|------------------|------------|",
    ]
    for entry in entries:
        paper_link = f"[{entry.paper_label}]({relative_markdown.as_posix()}#{entry.anchor_id})"
        lines.append(f"| [{entry.image_file}]({entry.image_file}) | {entry.caption} | {paper_link} |")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
