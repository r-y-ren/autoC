#!/usr/bin/env python3
"""S-17 my_LLM_valut bib 回填辅助（升级票04，2026-09-16）。

解析 vault 下全部 .bib，产出 citekey → {title, venue, year, doi, url} 映射（yaml），
供 vault-distill 建卡时对 paper-distill sources 尽力回填 doi/url（铁律 1 受控例外：
标题必标，DOI/URL 回填不到就留空，禁止编造）。

  --vault PATH   vault 根目录（默认 my_LLM_valut）
  --out PATH     输出映射（默认 kb/raw/vault-bib-map.yaml——kb/raw/ 不入库，本机使用）
  --selftest     假 bib 回归（不读 vault）
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ENTRY = re.compile(r'@\w+\s*\{\s*([^,\s]+)\s*,')
FIELD = re.compile(r'^\s*(\w+)\s*=\s*(.+?)\s*$', re.M)


def _clean(v: str) -> str:
    v = v.strip().rstrip(',').strip()
    if v[:1] in '"{' and v[-1:] in '"}':
        v = v[1:-1]
    v = re.sub(r'[{}]', '', v)
    v = v.replace('\\\\', '').replace('\\', '')
    return re.sub(r'\s+', ' ', v).strip()


def parse_bib(text: str) -> dict:
    """按 @ 条目切块，逐字段清洗。valut 的 bib 字段均为单行（annotation 多行但不需要）。"""
    out: dict = {}
    blocks = re.split(r'\n(?=@\w+\s*\{)', text)
    for b in blocks:
        m = ENTRY.search(b)
        if not m:
            continue
        key = m.group(1)
        fields = {k.lower(): _clean(v) for k, v in FIELD.findall(b)}
        keep: dict = {}
        for src, dst in (("title", "title"), ("booktitle", "venue"),
                         ("journal", "venue"), ("year", "year"), ("doi", "doi"), ("url", "url")):
            v = fields.get(src, "")
            if v:
                keep.setdefault(dst, v)
        if keep:
            out[key] = keep
    return out


def collect(vault: Path) -> dict:
    merged: dict = {}
    for bib in sorted(vault.rglob("*.bib")):
        try:
            merged.update(parse_bib(bib.read_text(encoding="utf-8", errors="replace")))
        except Exception as e:  # noqa: BLE001
            print(f"[vault_bib] ⚠ 跳过不可读 bib {bib.name}: {e}")
    return merged


def selftest() -> int:
    fake = """@article{fake2026test,
  title = {A {Fake} Title on UAV Offloading},
  journal = {IEEE JSAC},
  year = 2026,
  doi = {10.1109/fake.2026},
  url = {https://example.com/fake}
}

@inproceedings{fake2026b,
  title = "Second Paper",
  booktitle = {INFOCOM},
  year = {2026}
}
"""
    m = parse_bib(fake)
    checks = [
        (m.get("fake2026test", {}).get("title") == "A Fake Title on UAV Offloading", "title 花括号清洗"),
        (m.get("fake2026test", {}).get("doi") == "10.1109/fake.2026", "doi 提取"),
        (m.get("fake2026b", {}).get("venue") == "INFOCOM" and "doi" not in m["fake2026b"], "venue 提取/无 doi 留空"),
    ]
    ok = sum(c for c, _ in checks)
    for c, note in checks:
        print(("PASS " if c else "FAIL ") + note)
    print(f"[vault_bib][selftest] {ok}/{len(checks)} 通过")
    return 0 if ok == len(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="my_LLM_valut bib 回填辅助")
    ap.add_argument("--vault", default="my_LLM_valut")
    ap.add_argument("--out", default=None, help="默认 kb/raw/vault-bib-map.yaml")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    vault = Path(args.vault)
    if not vault.is_dir():
        print(f"[vault_bib] vault 不存在：{vault}")
        return 1
    merged = collect(vault)
    if not merged:
        print("[vault_bib] 未解析到任何条目")
        return 1

    with_doi = sum(1 for v in merged.values() if v.get("doi"))
    with_url = sum(1 for v in merged.values() if v.get("url"))
    out = Path(args.out) if args.out else Path("kb/raw/vault-bib-map.yaml")
    out.parent.mkdir(parents=True, exist_ok=True)
    import yaml
    out.write_text(yaml.safe_dump(merged, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"[vault_bib] {len(merged)} 条目 → {out}（doi 覆盖 {with_doi}，url 覆盖 {with_url}；"
          f"覆盖不到的回填留空，禁止编造）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
