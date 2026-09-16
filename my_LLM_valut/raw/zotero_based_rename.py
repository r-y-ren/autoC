#!/usr/bin/env python3
"""
基于Zotero citation key规则的重命名脚本
规则：auth.lower + year + shorttitle(3,3)
例如：wu2026ServiceorientedSegmentedTrajectory
"""

import os
import re
import json
from pathlib import Path

def parse_bib_file(bib_path):
    """解析.bib文件，提取完整的citation信息"""
    citations = {}
    
    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式匹配@entry{key, ...}模式
    pattern = r'@(\w+)\{\s*([^,]+)\s*,'
    matches = re.findall(pattern, content)
    
    for match in matches:
        entry_type, key = match[0], match[1].strip()
        if not key:  # 忽略空key
            continue
            
        # 提取条目内容
        search_str = '@' + entry_type + '{' + key + ','
        start = content.find(search_str)
        if start == -1:
            continue
            
        # 找到条目结束位置
        end = start + len(search_str)
        brace_count = 1
        i = end
        while i < len(content) and brace_count > 0:
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
            i += 1
        
        entry_content = content[start:i]
        
        # 提取标题和作者
        title = extract_title(entry_content)
        authors = extract_authors(entry_content)
        year = extract_year(entry_content)
        
        citations[key] = {
            'type': entry_type,
            'title': title,
            'authors': authors,
            'year': year
        }
    
    return citations

def extract_title(content):
    """从条目内容中提取标题"""
    patterns = [
        r'title\s*=\s*\{([^}]+)\}',
        r'title\s*=\s*"([^"]+)"',
    ]
    
    for pattern in patterns:
        title_match = re.search(pattern, content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1)
            # 清理标题
            title = re.sub(r'\{\{|\}\}', '', title)
            title = re.sub(r'\s+', ' ', title)
            title = title.strip()
            return title
    
    return None

def extract_authors(content):
    """从条目内容中提取作者"""
    author_match = re.search(r'author\s*=\s*\{([^}]+)\}', content, re.IGNORECASE)
    if author_match:
        authors_str = author_match.group(1)
        # 分割作者
        authors = [a.strip() for a in authors_str.split(' and ')]
        return authors
    return []

def extract_year(content):
    """从条目内容中提取年份"""
    year_match = re.search(r'year\s*=\s*(\d{4})', content, re.IGNORECASE)
    if year_match:
        return year_match.group(1)
    return None

def generate_citation_key(authors, year, title):
    """生成Zotero格式的citation key"""
    if not authors or not year:
        return None
    
    # 提取第一作者的姓氏（小写）
    first_author = authors[0]
    if ',' in first_author:
        # 格式：Last, First
        last_name = first_author.split(',')[0].strip()
    else:
        # 格式：First Last
        last_name = first_author.split()[-1].strip()
    
    author_part = last_name.lower()
    
    # 生成shorttitle（3,3格式：前3个词，每个词取前3个字符）
    if title:
        # 清理标题
        title_clean = re.sub(r'[^\w\s]', '', title.lower())
        words = title_clean.split()
        
        # 取前3个词，每个词取前3个字符
        shorttitle_parts = []
        for word in words[:3]:
            if len(word) >= 3:
                shorttitle_parts.append(word[:3].capitalize())
            else:
                shorttitle_parts.append(word.capitalize())
        
        shorttitle = ''.join(shorttitle_parts)
    else:
        shorttitle = 'Unknown'
    
    # 组合：author + year + shorttitle
    citation_key = f"{author_part}{year}{shorttitle}"
    
    return citation_key

def find_matching_files_by_citation_key(citation_key, directory, extension):
    """在目录中查找匹配citation key的文件"""
    key_lower = citation_key.lower()
    
    # 精确匹配
    for filename in os.listdir(directory):
        if filename.lower().endswith(extension):
            name_without_ext = filename[:-len(extension)].lower()
            if name_without_ext == key_lower:
                return filename
    
    # 尝试部分匹配（忽略大小写）
    for filename in os.listdir(directory):
        if filename.lower().endswith(extension):
            name_without_ext = filename[:-len(extension)].lower()
            if key_lower in name_without_ext or name_without_ext in key_lower:
                return filename
    
    return None

def generate_rename_script(citations, pdf_dir, markdown_dir):
    """生成重命名脚本"""
    script_lines = [
        '#!/bin/bash',
        '# 基于Zotero citation key规则的重命名脚本',
        '# 规则：auth.lower + year + shorttitle(3,3)',
        '# 例如：wu2026ServiceorientedSegmentedTrajectory',
        '#',
        f'# 共处理 {len(citations)} 个文献条目',
        '#',
        'set -e  # 遇到错误立即退出',
        '',
        'cd /Users/wupengfei/Downloads/my_LLM_valut/raw',
        ''
    ]
    
    # 跟踪已使用的文件
    used_pdfs = set()
    used_mds = set()
    matched_count = 0
    
    for key, citation in citations.items():
        title = citation['title']
        authors = citation['authors']
        year = citation['year']
        
        # 生成Zotero格式的citation key
        zotero_key = generate_citation_key(authors, year, title)
        
        if not zotero_key:
            continue
        
        # 查找匹配的文件
        pdf_file = find_matching_files_by_citation_key(zotero_key, pdf_dir, '.pdf')
        md_file = find_matching_files_by_citation_key(zotero_key, markdown_dir, '.md')
        
        # 如果没有找到，尝试在原始key中查找
        if not pdf_file:
            pdf_file = find_matching_files_by_citation_key(key, pdf_dir, '.pdf')
        if not md_file:
            md_file = find_matching_files_by_citation_key(key, markdown_dir, '.md')
        
        if pdf_file or md_file:
            matched_count += 1
            
            # 标记已使用的文件
            if pdf_file and pdf_file not in used_pdfs:
                used_pdfs.add(pdf_file)
            if md_file and md_file not in used_mds:
                used_mds.add(md_file)
            
            script_lines.append(f'# {zotero_key}')
            if title:
                script_lines.append(f'# {title[:80]}...' if len(title) > 80 else f'# {title}')
            script_lines.append('')
            
            # PDF重命名
            if pdf_file and pdf_file not in used_pdfs:
                target_name = f'{zotero_key}.pdf'
                if pdf_file != target_name:
                    script_lines.extend([
                        f'if [ -f "pdfs/{pdf_file}" ]; then',
                        f'    mv "pdfs/{pdf_file}" "pdfs/{target_name}"',
                        f'    echo "✓ PDF重命名: {pdf_file[:60]}... -> {target_name}"' if len(pdf_file) > 60 else f'    echo "✓ PDF重命名: {pdf_file} -> {target_name}"',
                        'else',
                        f'    echo "⚠ PDF文件不存在: pdfs/{pdf_file}"',
                        'fi',
                        ''
                    ])
                    used_pdfs.add(pdf_file)
                else:
                    script_lines.append(f'# PDF已正确命名: {target_name}\n')
            
            # Markdown重命名
            if md_file and md_file not in used_mds:
                target_name = f'{zotero_key}.md'
                if md_file != target_name:
                    script_lines.extend([
                        f'if [ -f "markdown/{md_file}" ]; then',
                        f'    mv "markdown/{md_file}" "markdown/{target_name}"',
                        f'    echo "✓ Markdown重命名: {md_file[:60]}... -> {target_name}"' if len(md_file) > 60 else f'    echo "✓ Markdown重命名: {md_file} -> {target_name}"',
                        'else',
                        f'    echo "⚠ Markdown文件不存在: markdown/{md_file}"',
                        'fi',
                        ''
                    ])
                    used_mds.add(md_file)
                else:
                    script_lines.append(f'# Markdown已正确命名: {target_name}\n')
    
    script_lines.extend([
        '',
        'echo "=================================================="',
        f'echo "文件重命名完成！共处理 {matched_count} 个文献"',
        'echo "=================================================="',
        'echo "PDF文件在: pdfs/"',
        'echo "Markdown文件在: markdown/"',
        'echo "请检查重命名结果。"'
    ])
    
    return '\n'.join(script_lines)

def main():
    """主函数"""
    bib_path = '/Users/wupengfei/Downloads/my_LLM_valut/raw/CCFA.bib'
    pdf_dir = '/Users/wupengfei/Downloads/my_LLM_valut/raw/pdfs'
    markdown_dir = '/Users/wupengfei/Downloads/my_LLM_valut/raw/markdown'
    
    if not os.path.exists(bib_path):
        print(f"错误: 找不到bib文件 {bib_path}")
        return
    
    if not os.path.exists(pdf_dir):
        print(f"错误: 找不到PDF目录 {pdf_dir}")
        return
    
    if not os.path.exists(markdown_dir):
        print(f"错误: 找不到Markdown目录 {markdown_dir}")
        return
    
    print("正在解析bib文件...")
    citations = parse_bib_file(bib_path)
    
    print(f"解析完成，共找到 {len(citations)} 个文献条目")
    
    print("正在生成基于Zotero规则的重命名脚本...")
    script_content = generate_rename_script(citations, pdf_dir, markdown_dir)
    
    # 保存脚本
    script_path = '/Users/wupengfei/Downloads/my_LLM_valut/raw/rename_zotero_style.sh'
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"✓ 重命名脚本已生成: {script_path}")
    print(f"  共处理 {len(citations)} 个文献条目")
    print("执行命令:")
    print(f"  chmod +x {script_path}")
    print(f"  {script_path}")

if __name__ == '__main__':
    main()