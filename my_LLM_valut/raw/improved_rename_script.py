#!/usr/bin/env python3
"""
改进的文件重命名脚本 - 同时处理PDF和Markdown文件
基于CCFA.bib和现有文件映射关系
"""

import os
import re
import json
from pathlib import Path
from difflib import SequenceMatcher

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

def calculate_similarity(str1, str2):
    """计算字符串相似度"""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def find_best_matching_file(citation_key, title, directory, extension):
    """在目录中查找最佳匹配的文件"""
    best_match = None
    best_similarity = 0.0
    
    if not os.path.exists(directory):
        return None, 0.0
    
    for filename in os.listdir(directory):
        if filename.lower().endswith(extension):
            name_without_ext = filename[:-len(extension)]
            
            # 1. 精确匹配
            if name_without_ext.lower() == citation_key.lower():
                return filename, 1.0
            
            # 2. 部分匹配
            if citation_key.lower() in name_without_ext.lower():
                return filename, 0.9
            
            # 3. 基于标题相似度匹配
            if title:
                similarity = calculate_similarity(title, name_without_ext)
                if similarity > best_similarity and similarity > 0.6:
                    best_match = filename
                    best_similarity = similarity
    
    return best_match, best_similarity

def generate_improved_rename_script(citations, pdf_dir, markdown_dir):
    """生成改进的重命名脚本"""
    script_lines = [
        '#!/bin/bash',
        '# 改进的重命名脚本 - 同时处理PDF和Markdown文件',
        '# 基于CCFA.bib中的citation key',
        '#',
        f'# 共处理 {len(citations)} 个文献条目',
        '#',
        'set -e  # 遇到错误立即退出',
        '',
        'cd /Users/wupengfei/Downloads/my_LLM_valut/raw',
        '',
        'echo "开始文件重命名..."',
        ''
    ]
    
    # 跟踪已使用的文件
    used_pdfs = set()
    used_mds = set()
    matched_count = 0
    high_quality_matches = 0
    
    # 按相似度排序的匹配结果
    all_matches = []
    
    for key, citation in citations.items():
        title = citation['title']
        authors = citation['authors']
        year = citation['year']
        
        # 生成Zotero格式的citation key
        zotero_key = generate_citation_key(authors, year, title)
        
        if not zotero_key:
            continue
        
        # 查找匹配的文件
        pdf_file, pdf_similarity = find_best_matching_file(zotero_key, title, pdf_dir, '.pdf')
        md_file, md_similarity = find_best_matching_file(zotero_key, title, markdown_dir, '.md')
        
        # 如果没有找到Zotero key匹配，尝试原始key
        if not pdf_file or pdf_similarity < 0.8:
            pdf_file_alt, pdf_similarity_alt = find_best_matching_file(key, title, pdf_dir, '.pdf')
            if pdf_similarity_alt > pdf_similarity:
                pdf_file = pdf_file_alt
                pdf_similarity = pdf_similarity_alt
        
        if not md_file or md_similarity < 0.8:
            md_file_alt, md_similarity_alt = find_best_matching_file(key, title, markdown_dir, '.md')
            if md_similarity_alt > md_similarity:
                md_file = md_file_alt
                md_similarity = md_similarity
        
        # 只保留高质量匹配（相似度>0.6）
        if (pdf_file and pdf_similarity > 0.6) or (md_file and md_similarity > 0.6):
            all_matches.append({
                'key': key,
                'zotero_key': zotero_key,
                'title': title,
                'pdf_file': pdf_file,
                'pdf_similarity': pdf_similarity,
                'md_file': md_file,
                'md_similarity': md_similarity
            })
    
    # 按相似度排序，从高到低
    all_matches.sort(key=lambda x: max(
        x['pdf_similarity'] if x['pdf_file'] else 0,
        x['md_similarity'] if x['md_file'] else 0
    ), reverse=True)
    
    # 生成重命名脚本
    for match in all_matches:
        key = match['key']
        zotero_key = match['zotero_key']
        title = match['title']
        pdf_file = match['pdf_file']
        pdf_similarity = match['pdf_similarity']
        md_file = match['md_file']
        md_similarity = match['md_similarity']
        
        # 跳过已使用的文件
        if pdf_file and pdf_file in used_pdfs:
            pdf_file = None
        if md_file and md_file in used_mds:
            md_file = None
        
        # 如果两个都没有可用的，跳过
        if not pdf_file and not md_file:
            continue
        
        matched_count += 1
        
        script_lines.extend([
            f'# {zotero_key}',
            f'# {title[:80]}...' if len(title) > 80 else f'# {title}',
            f'# PDF相似度: {pdf_similarity:.2%}, Markdown相似度: {md_similarity:.2%}',
        ])
        
        # PDF重命名
        if pdf_file:
            target_name = f'{zotero_key}.pdf'
            if pdf_similarity > 0.8:
                high_quality_matches += 1
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
                script_lines.append(f"# PDF跳过（相似度较低）: {pdf_file} -> {target_name}\n")
        
        # Markdown重命名
        if md_file:
            target_name = f'{zotero_key}.md'
            if md_similarity > 0.8:
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
                script_lines.append(f"# Markdown跳过（相似度较低）: {md_file} -> {target_name}\n")
    
    script_lines.extend([
        '',
        'echo "=================================================="',
        f'echo "文件重命名完成！共处理 {matched_count} 个文献"',
        f'echo "高质量匹配: {high_quality_matches} 个"',
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
    
    print("正在解析bib文件...")
    citations = parse_bib_file(bib_path)
    
    print(f"解析完成，共找到 {len(citations)} 个文献条目")
    
    print("正在扫描PDF文件...")
    if os.path.exists(pdf_dir):
        pdf_count = len([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
        print(f"找到 {pdf_count} 个PDF文件")
    
    print("正在扫描Markdown文件...")
    if os.path.exists(markdown_dir):
        md_count = len([f for f in os.listdir(markdown_dir) if f.endswith('.md')])
        print(f"找到 {md_count} 个Markdown文件")
    
    print("正在生成改进的重命名脚本...")
    script_content = generate_improved_rename_script(citations, pdf_dir, markdown_dir)
    
    # 保存脚本
    script_path = '/Users/wupengfei/Downloads/my_LLM_valut/raw/improved_rename.sh'
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"✓ 改进的重命名脚本已生成: {script_path}")
    print(f"  共处理 {len(citations)} 个文献条目")
    print("执行命令:")
    print(f"  chmod +x {script_path}")
    print(f"  {script_path}")

if __name__ == '__main__':
    main()