#!/usr/bin/env python3
"""
同步PDF文件与Zotero citekey
从BibTeX文件读取citekey，匹配init目录下的PDF文件，生成重命名映射
"""

import os
import re
import json
from pathlib import Path
import difflib
from typing import Dict, List, Tuple, Optional

def parse_bibtex(bibtex_file: str) -> Dict[str, dict]:
    """解析BibTeX文件，返回{citekey: {title, file_paths}}的字典"""
    print(f"正在解析BibTeX文件: {bibtex_file}")
    
    entries = {}
    current_entry = None
    
    with open(bibtex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 移除注释
    content = re.sub(r'%.*$', '', content, flags=re.MULTILINE)
    
    # 匹配条目
    pattern = r'@(\w+)\s*\{([^,]+),\s*([^@]+)'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        entry_type = match.group(1)
        citekey = match.group(2).strip()
        entry_content = match.group(3)
        
        # 提取标题
        title_match = re.search(r'title\s*=\s*\{([^}]+)\}', entry_content, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else ""
        
        # 清理标题（移除LaTeX命令和多余空格）
        title = clean_title(title)
        
        # 提取文件路径
        file_paths = []
        file_match = re.search(r'file\s*=\s*\{([^}]+)\}', entry_content, re.IGNORECASE)
        if file_match:
            file_str = file_match.group(1)
            # BibTeX中可能有多个文件，用分号分隔
            file_paths = [f.strip() for f in file_str.split(';')]
        
        entries[citekey] = {
            'type': entry_type,
            'title': title,
            'file_paths': file_paths
        }
    
    print(f"成功解析 {len(entries)} 个BibTeX条目")
    return entries

def clean_title(title: str) -> str:
    """清理标题字符串"""
    # 移除LaTeX命令
    title = re.sub(r'\\[a-zA-Z]+\s*\{([^}]*)\}', r'\1', title)
    title = re.sub(r'\{|\}', '', title)
    # 移除多余的空格和特殊字符
    title = re.sub(r'\s+', ' ', title)
    title = title.strip()
    return title

def get_pdf_files(init_dir: str) -> Dict[str, str]:
    """扫描init目录，返回{filename: filepath}的字典"""
    print(f"正在扫描PDF文件: {init_dir}")
    
    pdf_files = {}
    init_path = Path(init_dir)
    
    for pdf_file in init_path.glob('*.pdf'):
        pdf_files[pdf_file.name] = str(pdf_file)
    
    print(f"找到 {len(pdf_files)} 个PDF文件")
    return pdf_files

def match_pdf_to_bibtex(pdf_filename: str, bibtex_entries: Dict[str, dict], 
                         threshold: float = 0.6) -> Optional[Tuple[str, float]]:
    """将PDF文件名与BibTeX条目匹配，返回(citekey, similarity)或None"""
    # 从PDF文件名提取标题（移除.pdf后缀）
    pdf_title = pdf_filename.replace('.pdf', '')
    pdf_title = clean_title(pdf_title)
    
    best_match = None
    best_similarity = 0.0
    
    for citekey, entry in bibtex_entries.items():
        bibtex_title = entry['title']
        
        if not bibtex_title:
            continue
        
        # 使用difflib计算相似度
        similarity = difflib.SequenceMatcher(None, pdf_title.lower(), bibtex_title.lower()).ratio()
        
        if similarity > best_similarity and similarity >= threshold:
            best_similarity = similarity
            best_match = citekey
    
    return (best_match, best_similarity) if best_match else None

def build_mapping(pdf_files: Dict[str, str], 
                bibtex_entries: Dict[str, dict],
                threshold: float = 0.6) -> Dict[str, dict]:
    """构建PDF文件到citekey的映射"""
    print(f"\n开始匹配PDF文件与BibTeX条目（相似度阈值: {threshold}）...")
    
    mapping = {}
    matched_count = 0
    unmatched = []
    
    for pdf_filename, pdf_path in pdf_files.items():
        result = match_pdf_to_bibtex(pdf_filename, bibtex_entries, threshold)
        
        if result:
            citekey, similarity = result
            mapping[pdf_filename] = {
                'citekey': citekey,
                'similarity': similarity,
                'current_path': pdf_path,
                'title': bibtex_entries[citekey]['title']
            }
            matched_count += 1
            print(f"✓ {pdf_filename} -> {citekey} (相似度: {similarity:.2%})")
        else:
            unmatched.append(pdf_filename)
            print(f"✗ {pdf_filename} - 未找到匹配")
    
    print(f"\n匹配结果:")
    print(f"  成功匹配: {matched_count} 个")
    print(f"  未匹配: {len(unmatched)} 个")
    
    return mapping, unmatched

def generate_rename_script(mapping: Dict[str, dict], output_file: str):
    """生成重命名脚本"""
    print(f"\n生成重命名脚本: {output_file}")
    
    script_lines = [
        "#!/bin/bash",
        "# 自动生成的PDF重命名脚本",
        "# 请在执行前检查映射是否正确",
        "#",
        f"# 共 {len(mapping)} 个文件需要重命名",
        "#",
        "# 警告：此脚本会重命名文件，请确保已备份！",
        "",
        "set -e  # 遇遇错误立即退出",
        "",
        "cd /Users/wupengfei/Downloads/raw/init",
        "",
    ]
    
    for old_name, info in mapping.items():
        new_name = f"{info['citekey']}.pdf"
        script_lines.append(f"# {info['title']}")
        script_lines.append(f"# 相似度: {info['similarity']:.2%}")
        script_lines.append(f'if [ -f "{old_name}" ]; then')
        script_lines.append(f'    mv "{old_name}" "{new_name}"')
        script_lines.append(f'    echo "重命名: {old_name} -> {new_name}"')
        script_lines.append(f'else')
        script_lines.append(f'    echo "警告: 文件不存在 - {old_name}"')
        script_lines.append(f'fi')
        script_lines.append("")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(script_lines))
    
    print(f"✓ 重命名脚本已生成: {output_file}")

def save_mapping_report(mapping: Dict[str, dict], unmatched: List[str], 
                       output_file: str):
    """保存映射报告为JSON"""
    print(f"\n保存映射报告: {output_file}")
    
    report = {
        'total_pdfs': len(mapping) + len(unmatched),
        'matched': len(mapping),
        'unmatched': len(unmatched),
        'mapping': mapping,
        'unmatched_files': unmatched
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 映射报告已保存: {output_file}")

def save_unmatched_csv(unmatched: List[str], output_file: str):
    """保存未匹配的文件到CSV"""
    if not unmatched:
        print("\n没有未匹配的文件")
        return
    
    print(f"\n保存未匹配文件列表: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("pdf_filename,status\n")
        for filename in unmatched:
            f.write(f"{filename},unmatched\n")
    
    print(f"✓ 未匹配文件列表已保存: {output_file}")

def main():
    """主函数"""
    print("=" * 80)
    print("PDF文件与Zotero citekey同步工具")
    print("=" * 80)
    
    # 配置
    bibtex_file = '/Users/wupengfei/Downloads/raw/CCFA.bib'
    init_dir = '/Users/wupengfei/Downloads/raw/init'
    output_script = '/Users/wupengfei/Downloads/raw/rename_pdfs.sh'
    output_report = '/Users/wupengfei/Downloads/raw/pdf_citekey_mapping.json'
    output_unmatched = '/Users/wupengfei/Downloads/raw/unmatched_pdfs.csv'
    similarity_threshold = 0.4  # 相似度阈值
    
    # 检查文件是否存在
    if not os.path.exists(bibtex_file):
        print(f"错误: BibTeX文件不存在: {bibtex_file}")
        return
    
    if not os.path.exists(init_dir):
        print(f"错误: init目录不存在: {init_dir}")
        return
    
    # 1. 解析BibTeX文件
    bibtex_entries = parse_bibtex(bibtex_file)
    
    # 2. 扫描PDF文件
    pdf_files = get_pdf_files(init_dir)
    
    # 3. 建立映射
    mapping, unmatched = build_mapping(pdf_files, bibtex_entries, similarity_threshold)
    
    # 4. 生成重命名脚本
    if mapping:
        generate_rename_script(mapping, output_script)
    
    # 5. 保存映射报告
    save_mapping_report(mapping, unmatched, output_report)
    
    # 6. 保存未匹配文件
    save_unmatched_csv(unmatched, output_unmatched)
    
    print("\n" + "=" * 80)
    print("处理完成！")
    print("=" * 80)
    print(f"\n生成的文件:")
    print(f"  1. 重命名脚本: {output_script}")
    print(f"  2. 映射报告: {output_report}")
    if unmatched:
        print(f"  3. 未匹配文件: {output_unmatched}")
    
    print(f"\n下一步:")
    print(f"  1. 检查 {output_report} 确认映射是否正确")
    print(f"  2. 如果需要，调整相似度阈值后重新运行脚本")
    print(f"  3. 确认无误后，执行重命名脚本:")
    print(f"     chmod +x {output_script}")
    print(f"     ./{output_script}")

if __name__ == '__main__':
    main()