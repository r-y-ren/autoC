#!/usr/bin/env python3
"""
直接扫描Markdown文件，按照 auth.lower + year + shorttitle(3,3) 规则重命名
完全不依赖bib文件
"""

import os
import re
from pathlib import Path
from difflib import SequenceMatcher

def extract_info_from_filename(filename):
    """从文件名中提取作者、年份、标题信息"""
    # 移除.md扩展名
    name = filename[:-3] if filename.endswith('.md') else filename
    
    # 提取年份（4位数字）
    year_match = re.search(r'\b(20[12][0-9])\b', name)
    year = year_match.group(1) if year_match else 'Unknown'
    
    # 提取作者信息
    authors = []
    # 匹配中文作者模式：XXX 等 - 2024
    chinese_author_match = re.match(r'^([^等]+)\s+等\s*-\s*\d{4}', name)
    if chinese_author_match:
        authors = [chinese_author_match.group(1).strip()]
    else:
        # 匹配英文作者模式：Xingxia Gao, ...
        english_author_match = re.match(r'^([A-Z][a-z]+\s+[A-Z][a-z]+)', name)
        if english_author_match:
            authors = [english_author_match.group(1).strip()]
        # 匹配其他模式：Gao-2025-
        simple_author_match = re.match(r'^([A-Z][a-z]+)-\d{4}', name)
        if simple_author_match:
            authors = [simple_author_match.group(1).strip()]
    
    # 提取标题（去掉作者和年份后剩余的部分）
    title = name
    if chinese_author_match:
        # XXX 等 - 2024 - Title
        title = re.sub(r'^[^等]+\s+等\s*-\s*\d{4}\s*-\s*', '', title)
    elif english_author_match or simple_author_match:
        # Author-2024-Title 或 Author 等 - 2024 - Title
        title = re.sub(r'^[A-Z][a-z]+[\s,-]+\d{4}[\s,-]*', '', title)
        # 移除常见的前缀
        title = re.sub(r'^[-\s]+', '', title)
    
    # 清理标题
    title = title.replace('_', ' ').replace('-', ' ')
    title = re.sub(r'\s+', ' ', title).strip()
    
    return {
        'year': year,
        'authors': authors,
        'title': title
    }

def extract_info_from_content(filepath):
    """从Markdown文件内容中提取作者和标题信息（前2行）"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 获取前2行
        lines = content.split('\n')[:2]
        first_line = lines[0].strip() if lines else ''
        second_line = lines[1].strip() if len(lines) > 1 else ''
        
        # 尝试从第一行提取作者（可能有多个作者）
        authors = []
        # 匹配英文作者：Xingxia Gao, ...
        author_matches = re.findall(r'([A-Z][a-z]+\s+[A-Z][a-z]+)', first_line)
        if author_matches:
            # 取第一个匹配的作者（第一作者）
            authors = [author_matches[0].strip()]
        
        # 从文件名获取年份
        filename = os.path.basename(filepath)[:-3]  # 移除.md
        year_match = re.search(r'\b(20[12][0-9])\b', filename)
        year = year_match.group(1) if year_match else 'Unknown'
        
        # 从文件名获取标题
        title = extract_info_from_filename(filename)['title']
        
        return {
            'authors': authors,
            'title': title,
            'year': year,
            'raw_content': first_line  # 保存原始内容用于调试
        }
    except Exception as e:
        return {
            'authors': [],
            'title': '',
            'year': 'Unknown',
            'raw_content': ''
        }

def generate_new_filename(info, original_filename):
    """按照 auth.lower + year + shorttitle(3,3) 规则生成新文件名"""
    year = info['year']
    authors = info['authors']
    title = info['title']
    
    # 如果没有作者信息，从文件名提取
    if not authors:
        name_info = extract_info_from_filename(original_filename)
        if name_info['authors']:
            authors = name_info['authors']
    
    if not authors or year == 'Unknown':
        return None
    
    # 提取第一作者姓氏（小写）
    first_author = authors[0]
    if ',' in first_author:
        # 格式：Last, First
        last_name = first_author.split(',')[0].strip()
    else:
        # 格式：First Last 或 中文作者
        if any('\u4e00' <= c <= '\u9fff' for c in first_author):
            # 中文作者，直接使用
            last_name = first_author
        else:
            # 英文作者，提取姓氏
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
        
        # 如果shorttitle太短，使用更多词
        if len(shorttitle) < 6 and len(words) > 3:
            for word in words[3:6]:
                shorttitle_parts.append(word[:3].capitalize() if len(word) >= 3 else word.capitalize())
            shorttitle = ''.join(shorttitle_parts)
    else:
        shorttitle = 'Unknown'
    
    # 组合：author + year + shorttitle
    new_filename = f"{author_part}{year}{shorttitle}.md"
    
    return new_filename

def generate_rename_script(markdown_dir):
    """生成重命名脚本"""
    script_lines = [
        '#!/bin/bash',
        '# 直接按照 auth.lower + year + shorttitle(3,3) 规则重命名Markdown文件',
        '# 完全不依赖bib文件',
        '#',
    ]
    
    # 获取所有Markdown文件
    markdown_files = [f for f in os.listdir(markdown_dir) if f.endswith('.md')]
    script_lines.append(f'# 共处理 {len(markdown_files)} 个Markdown文件')
    script_lines.extend([
        '#',
        'set -e  # 遇到错误立即退出',
        '',
        'cd /Users/wupengfei/Downloads/my_LLM_valut/raw',
        '',
        'echo "开始Markdown文件重命名..."',
        ''
    ])
    
    # 已使用的文件名和无法处理的文件列表
    used_filenames = set()
    renamed_count = 0
    unprocessed_files = []  # 记录无法处理的文件
    
    # 处理每个Markdown文件
    for filename in sorted(markdown_files):
        filepath = os.path.join(markdown_dir, filename)
        
        # 跳过已经符合格式的文件
        if re.match(r'^[a-z]+\d{4}[A-Z]', filename):
            script_lines.append(f'# 已符合格式，跳过: {filename}')
            script_lines.append('')
            continue
        
        # 优先从内容提取信息（内容信息更准确）
        content_info = extract_info_from_content(filepath)
        
        # 如果内容中有作者信息，使用内容信息
        if content_info['authors']:
            info = {
                'year': content_info['year'],
                'authors': content_info['authors'],
                'title': extract_info_from_filename(filename)['title']  # 标题仍从文件名提取
            }
        else:
            # 否则从文件名提取
            info = extract_info_from_filename(filename)
            
            # 如果文件名缺少年份信息，尝试从内容提取年份
            if info['year'] == 'Unknown' and content_info['year'] != 'Unknown':
                info['year'] = content_info['year']
        
        # 生成新文件名
        new_filename = generate_new_filename(info, filename)
        
        if new_filename and new_filename not in used_filenames:
            script_lines.extend([
                f'# 原文件: {filename}',
                f'# 作者: {", ".join(info["authors"])}',
                f'# 年份: {info["year"]}',
                f'# 标题: {info["title"][:80]}...' if len(info["title"]) > 80 else f'# 标题: {info["title"]}',
                f'# 新文件名: {new_filename}',
                f'if [ -f "markdown/{filename}" ]; then',
                f'    mv "markdown/{filename}" "markdown/{new_filename}"',
                f'    echo "✓ 重命名: {filename[:50]}... -> {new_filename}"' if len(filename) > 50 else f'    echo "✓ 重命名: {filename} -> {new_filename}"',
                'else',
                f'    echo "⚠ 文件不存在: markdown/{filename}"',
                'fi',
                ''
            ])
            used_filenames.add(new_filename)
            renamed_count += 1
        else:
            script_lines.extend([
                f'# 无法处理: {filename}',
                f'# 原因: {"缺少作者信息" if not info["authors"] else "缺少年份信息" if info["year"] == "Unknown" else "文件名冲突"}',
                ''
            ])
            # 记录到无法处理文件列表
            unprocessed_files.append(filename)
    
    # 保存无法处理的文件列表到本地
    if unprocessed_files:
        script_lines.extend([
            '',
            '# 以下文件无法自动处理，需要手动检查：',
            '',
        ])
        for filename in unprocessed_files:
            filepath = os.path.join(markdown_dir, filename)
            try:
                # 尝试读取文件内容保存到日志
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')[:5]  # 保存前5行
                    content_preview = '\n'.join(lines)
                    script_lines.extend([
                        f'# 文件: {filename}',
                        f'# 前5行预览:',
                        f'# {content_preview[:200]}...' if len(content_preview) > 200 else f'# {content_preview}',
                        ''
                    ])
            except Exception as e:
                script_lines.extend([
                    f'# 文件: {filename}',
                    f'# 错误: 无法读取文件内容 - {e}',
                    ''
                ])
    
    script_lines.extend([
        '',
        'echo "=================================================="',
        f'echo "Markdown文件重命名完成！共处理 {renamed_count} 个文件"',
        f'echo "无法自动处理: {len(unprocessed_files)} 个文件"',
        'echo "=================================================="',
        'echo "Markdown文件在: markdown/"',
        'echo "请检查无法处理的文件，手动重命名。"'
    ])
    
    return '\n'.join(script_lines)

def main():
    """主函数"""
    markdown_dir = '/Users/wupengfei/Downloads/my_LLM_valut/raw/markdown'
    
    if not os.path.exists(markdown_dir):
        print(f"错误: 找不到目录 {markdown_dir}")
        return
    
    print("正在扫描Markdown文件...")
    script_content = generate_rename_script(markdown_dir)
    
    # 保存脚本
    script_path = '/Users/wupengfei/Downloads/my_LLM_valut/raw/rename_markdown_simple.sh'
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"✓ Markdown重命名脚本已生成: {script_path}")
    print("执行命令:")
    print(f"  chmod +x {script_path}")
    print(f"  {script_path}")

if __name__ == '__main__':
    main()