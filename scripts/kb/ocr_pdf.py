#!/usr/bin/env python3
"""S-13 PDF 解析（ocr_pdf）：有文本层直取；无文本层逐页渲染 → tesseract OCR。

紧循环边界：只做确定性"PDF → 文本 + 置信度报告"；"这页写的是什么意思"归 Scraper 判断。
输出：与 PDF 同名 .txt（文本）+ .ocr.json（逐页报告：模式/字符数/OCR 平均置信度），
      低置信页（mean_conf < 70）列于报告 low_conf_pages 并在 stderr 告警。

用法：python scripts/kb/ocr_pdf.py <pdf路径> [--lang chi_sim+eng] [--dpi 200]
依赖：pypdfium2、pillow（渲染）；tesseract（OCR，无文本层时才需要）
退出码：0=成功；2=环境/参数错误；3=全部页面无法解析
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TEXT_MIN_CHARS = 50     # 单页文本层低于此字符数视为扫描页
LOW_CONF = 70           # OCR 平均置信度低于此告警


def find_tesseract() -> str | None:
    exe = shutil.which("tesseract")
    if exe:
        return exe
    for p in (r"C:\Program Files\Tesseract-OCR\tesseract.exe",
              r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"):
        if Path(p).is_file():
            return p
    return None


def ensure_lang(tess: str, lang: str) -> None:
    """默认 tessdata 缺语言包时，自动指向用户级 ~/.tessdata。

    注意 TESSDATA_PREFIX 是整体替换而非叠加：用户目录必须自带
    ①缺失语言的 traineddata ②默认目录已有的语言包（eng/osd，避免遮蔽）
    ③configs/ 目录（tsv 等输出格式定义）。缺一不可，否则 tesseract 静默失败。
    """
    import os
    listed = subprocess.run([tess, "--list-langs"], capture_output=True, text=True).stdout
    have = {l.strip() for l in listed.splitlines()[1:]}
    missing = [l for l in lang.split("+") if l and l not in have]
    if not missing:
        return
    user_data = Path.home() / ".tessdata"
    if not all((user_data / f"{l}.traineddata").is_file() for l in missing):
        print(f"[ocr_pdf] 用户级 tessdata 缺 {missing} 的 traineddata，请先放置", file=sys.stderr)
        sys.exit(2)
    src = Path(tess).resolve().parent / "tessdata"
    for f in src.glob("*.traineddata"):  # 补齐默认语言包，避免遮蔽
        dst = user_data / f.name
        if not dst.is_file():
            try:
                shutil.copy2(f, dst)
            except OSError:
                pass
    cfg_src, cfg_dst = src / "configs", user_data / "configs"
    if cfg_src.is_dir() and not cfg_dst.is_dir():  # 补齐输出格式定义
        shutil.copytree(cfg_src, cfg_dst)
    os.environ["TESSDATA_PREFIX"] = str(user_data)
    print(f"[ocr_pdf] 语言包 {missing} → 用户级 {user_data}（已补齐默认包与 configs）", file=sys.stderr)


def ocr_image(tess: str, img: Path, lang: str) -> tuple[str, float | None]:
    """tesseract tsv 输出 → (文本, 词级平均置信度)。"""
    proc = subprocess.run([tess, str(img), "stdout", "-l", lang, "tsv"],
                          capture_output=True, text=True, timeout=120)
    lines, words, confs = [], [], []
    for row in proc.stdout.splitlines()[1:]:
        cols = row.split("\t")
        if len(cols) < 12:
            continue
        text = cols[11].strip()
        conf = float(cols[10])
        if text:
            words.append(text)
            if conf >= 0:
                confs.append(conf)
        if cols[0].isdigit() and text == "" and cols[4] not in ("", "0"):
            lines.append("\n")
    # 按换行提示重组太脆弱，直接以空格连接 + 段落按 tsv 的 block_num 分组
    mean_conf = round(sum(confs) / len(confs), 1) if confs else None
    return " ".join(words), mean_conf


def main() -> int:
    ap = argparse.ArgumentParser(description="PDF → 文本（文本层直取 / 逐页 OCR）")
    ap.add_argument("pdf", type=str)
    ap.add_argument("--lang", default="chi_sim+eng")
    ap.add_argument("--dpi", type=int, default=200)
    args = ap.parse_args()

    pdf = Path(args.pdf)
    if not pdf.is_file():
        print(f"[ocr_pdf] 文件不存在：{pdf}", file=sys.stderr)
        return 2

    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(str(pdf))
    tess = find_tesseract()
    if tess:
        ensure_lang(tess, args.lang)
    pages_report, texts = [], []
    ocr_pages = 0

    with tempfile.TemporaryDirectory(prefix="autoc_ocr_") as td:
        for i in range(len(doc)):
            page = doc[i]
            tp = page.get_textpage()
            n_chars = tp.count_chars()
            if n_chars >= TEXT_MIN_CHARS:
                text = tp.get_text_range()
                pages_report.append({"page": i + 1, "mode": "text", "chars": n_chars, "conf": None})
                texts.append(text)
                continue
            if not tess:
                pages_report.append({"page": i + 1, "mode": "no-text-layer", "chars": n_chars,
                                     "conf": None, "error": "tesseract 不可用"})
                texts.append("")
                continue
            bitmap = page.render(scale=args.dpi / 72)
            img = Path(td) / f"p{i + 1}.png"
            bitmap.to_pil().save(img)
            try:
                text, conf = ocr_image(tess, img, args.lang)
            except Exception as e:  # noqa: BLE001
                pages_report.append({"page": i + 1, "mode": "ocr", "chars": 0,
                                     "conf": None, "error": str(e)[:80]})
                texts.append("")
                continue
            ocr_pages += 1
            pages_report.append({"page": i + 1, "mode": "ocr", "chars": len(text), "conf": conf})
            texts.append(text)

    out_txt = pdf.with_suffix(".txt")
    out_json = pdf.with_suffix(".ocr.json")
    full_text = "\n\n".join(f"===== 第 {r['page']} 页（{r['mode']}）=====\n{t}"
                            for r, t in zip(pages_report, texts))
    out_txt.write_text(full_text, encoding="utf-8")
    low = [r["page"] for r in pages_report
           if r["mode"] == "ocr" and (r["conf"] is None or r["conf"] < LOW_CONF)]
    out_json.write_text(json.dumps({
        "pdf": str(pdf), "pages": len(pages_report),
        "text_pages": sum(1 for r in pages_report if r["mode"] == "text"),
        "ocr_pages": ocr_pages, "low_conf_pages": low,
        "report": pages_report,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[ocr_pdf] {pdf.name}：{len(pages_report)} 页 | 文本层 {sum(1 for r in pages_report if r['mode']=='text')} | "
          f"OCR {ocr_pages} | 低置信页 {low or '无'}")
    print(f"[ocr_pdf] 输出 → {out_txt.name} / {out_json.name}")
    if low:
        print(f"[ocr_pdf] 低置信页需人工复核（conf<{LOW_CONF}）", file=sys.stderr)
    if all(r["mode"] == "no-text-layer" for r in pages_report):
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
