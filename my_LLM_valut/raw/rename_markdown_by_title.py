#!/usr/bin/env python3
"""
从Markdown文件提取标题，在bib文件中匹配，使用citation key重命名
"""

import os
import re
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
        
        # 提取标题
        title = extract_title_from_bib(entry_content)
        
        if title:
            citations[key] = {
                'type': entry_type,
                'title': title,
                'key': key
            }
    
    return citations

def extract_title_from_bib(content):
    """从bib条目中提取标题"""
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

def extract_title_from_markdown(filepath):
    """从Markdown文件第一行提取标题"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        
        # 清理标题
        title = re.sub(r'[^a-zA-Z0-9\s]', '', first_line)
        title = re.sub(r'\s+', ' ', title).strip()
        
        return title
    except Exception as e:
        return None

def calculate_similarity(str1, str2):
    """计算字符串相似度"""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def find_best_matching_citation(markdown_title, citations, threshold=0.6):
    """在bib条目中找到最佳匹配的citation"""
    best_match = None
    best_similarity = 0.0
    
    for key, citation in citations.items():
        bib_title = citation['title']
        if not bib_title:
            continue
        
        # 清理bib标题
        bib_title_clean = re.sub(r'[^a-zA-Z0-9\s]', '', bib_title)
        bib_title_clean = re.sub(r'\s+', ' ', bib_title_clean).strip()
        
        # 计算相似度
        similarity = calculate_similarity(markdown_title, bib_title_clean)
        
        # 检查是否包含关键词
        if similarity > best_similarity:
            best_similarity = similarity
            best_match = citation
    
    if best_similarity >= threshold:
        return best_match, best_similarity
    else:
        return None, best_similarity

def generate_rename_script(markdown_dir, bib_path):
    """生成重命名脚本"""
    # 解析bib文件
    print("正在解析bib文件...")
    citations = parse_bib_file(bib_path)
    print(f"解析完成，共找到 {len(citations)} 个文献条目")
    
    script_lines = [
        '#!/bin/bash',
        '# 通过标题匹配bib文件，使用citation key重命名Markdown文件',
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
    low_matches = []  # 记录低相似度匹配
    
    # 处理每个Markdown文件
    for filename in sorted(markdown_files):
        filepath = os.path.join(markdown_dir, filename)
        
        # 跳过已经符合格式的文件
        if re.match(r'^[a-z]+\d{4}[A-Z]', filename):
            script_lines.append(f'# 已符合格式，跳过: {filename}')
            script_lines.append('')
            continue
        
        # 从Markdown提取标题
        md_title = extract_title_from_markdown(filepath)
        
        if not md_title:
            script_lines.extend([
                f'# 无法处理: {filename}',
                f'# 原因: 无法从第一行提取标题',
                ''
            ])
            unprocessed_files.append(filename)
            continue
        
        # 在bib中查找最佳匹配
        best_match, similarity = find_best_matching_citation(md_title, citations)
        
        if best_match and best_match['key'] not in used_filenames:
            citation_key = best_match['key']
            new_filename = f"{citation_key}.md"
            
            script_lines.extend([
                f'# 原文件: {filename}',
                f'# Markdown标题: {md_title[:80]}...' if len(md_title) > 80 else f'# Markdown标题: {md_title}',
                f'# 匹配的bib标题: {best_match["title"][:80]}...' if len(best_match["title"]) > 80 else f'# 匹配的bib标题: {best_match["title"]}',
                f'# 相似度: {similarity:.2%}',
                f'# Citation key: {citation_key}',
                f'# 新文件名: {new_filename}',
                f'if [ -f "markdown/{filename}" ]; then',
                f'    mv "markdown/{filename}" "markdown/{new_filename}"',
                f'    echo "✓ 重命名: {filename[:50]}... -> {new_filename}"' if len(filename) > 50 else f'    echo "✓ 重命名: {filename} -> {new_filename}"',
                'else',
                f'    echo "⚠ 文件不存在: markdown/{filename}"',
                'fi',
                ''
            ])
            used_filenames.add(citation_key)
            renamed_count += 1
        elif best_match and best_match['key'] in used_filenames:
            # 文件名冲突
            script_lines.extend([
                f'# 无法处理: {filename}',
                f'# 原因: Citation key {best_match["key"]} 已被使用',
                ''
            ])
            unprocessed_files.append(filename)
        else:
            # 没有找到匹配
            if similarity > 0.3:
                # 相似度较低，但可能有参考价值
                low_matches.append({
                    'filename': filename,
                    'md_title': md_title,
                    'best_match': best_match if best_match else None,
                    'similarity': similarity
                })
            script_lines.extend([
                f'# 无法处理: {filename}',
                f'# 原因: 在bib文件中未找到匹配的标题 (最高相似度: {similarity:.2%})',
                ''
            ])
            unprocessed_files.append(filename)
    
    # 保存低相似度匹配信息
    if low_matches:
        script_lines.extend([
            '',
            '# 低相似度匹配（可能需要手动确认）：',
            '',
        ])
        for item in low_matches:
            script_lines.extend([
                f'# 文件: {item["filename"]}',
                f'# Markdown标题: {item["md_title"][:60]}...' if len(item["md_title"]) > 60 else f'# Markdown标题: {item["md_title"]}',
                f'# 最佳匹配: {item["best_match"]["title"][:60] if item["best_match"] else "无"}...',
                f'# 相似度: {item["similarity"]:.2%}',
                ''
            ])
    
    script_lines.extend([
        '',
        'echo "=================================================="',
        f'echo "Markdown文件重命名完成！共处理 {renamed_count} 个文件"',
        f'echo "无法自动处理: {len(unprocessed_files)} 个文件"',
        f'echo "低相似度匹配: {len(low_matches)} 个"',
        'echo "=================================================="',
        'echo "Markdown文件在: markdown/"',
        'echo "请检查无法处理的文件，手动重命名。"'
    ])
    
    return '\n'.join(script_lines)

def main():
    """主函数"""
    markdown_dir = '/Users/wupengfei/Downloads/my_LLM_valut/raw/markdown'
    bib_path = '/Users/wupengfei/Downloads/my_LLM_valut/raw/CCFA.bib'
    
    if not os.path.exists(markdown_dir):
        print(f"错误: 找不到目录 {markdown_dir}")
        return
    
    if not os.path.exists(bib_path):
        print(f"错误: 找不到bib文件 {bib_path}")
        return
    
    print("正在生成Markdown重命名脚本...")
    script_content = generate_rename_script(markdown_dir, bib_path)
    
    # 保存脚本
    script_path = '/Users/wupengfei/Downloads/my_LLM_valut/raw/rename_markdown_by_title.sh'
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"✓ Markdown重命名脚本已生成: {script_path}")
    print("执行命令:")
    print(f"  chmod +x {script_path}")
    print(f"  {script_path}")

if __name__ == '__main__':
    main()