#!/usr/bin/env python3
"""
从已存在的Markdown文件中提取标题信息并创建CSV记录
"""

import os
import csv
from pathlib import Path


def extract_title_from_markdown(md_path):
    """
    从Markdown文件中提取标题
    
    参数:
        md_path: Markdown文件路径
    
    返回:
        标题字符串
    """
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        for line in lines[:50]:  # 检查前50行
            line = line.strip()
            if line.startswith('# '):
                title = line[2:].strip()
                # 清理特殊字符
                title = title.replace('â', "'").replace('€', "'")
                return title
            elif line.startswith('## '):
                return line[3:].strip()
        
        return "No title found"
    except Exception as e:
        print(f"  警告: 读取文件失败 {os.path.basename(md_path)}: {e}")
        return "Error reading file"


def create_csv_from_markdown(markdown_dir, csv_file):
    """
    从Markdown目录创建CSV记录
    
    参数:
        markdown_dir: Markdown文件目录
        csv_file: 输出CSV文件路径
    """
    if not os.path.exists(markdown_dir):
        print(f"错误: 目录不存在 - {markdown_dir}")
        return
    
    # 获取所有Markdown文件
    md_files = [f for f in os.listdir(markdown_dir) if f.endswith('.md')]
    md_files.sort()
    
    if not md_files:
        print("未找到任何Markdown文件")
        return
    
    print(f"找到 {len(md_files)} 个Markdown文件")
    print()
    
    # 创建CSV记录
    records = []
    for md_filename in md_files:
        md_path = os.path.join(markdown_dir, md_filename)
        title = extract_title_from_markdown(md_path)
        file_size = os.path.getsize(md_path)
        
        record = {
            'pdf_file': md_filename.replace('.md', '.pdf'),
            'title': title,
            'markdown_file': md_filename,
            'file_size_bytes': file_size,
            'file_size_kb': f"{file_size/1024:.2f}"
        }
        records.append(record)
        print(f"处理: {md_filename}")
        print(f"  标题: {title}")
        print()
    
    # 写入CSV
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['pdf_file', 'title', 'markdown_file', 'file_size_bytes', 'file_size_kb']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    
    print(f"✓ CSV文件创建成功: {csv_file}")
    print(f"  记录数: {len(records)}")


def main():
    # 配置路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    markdown_dir = os.path.join(current_dir, 'markdown')
    csv_file = os.path.join(markdown_dir, 'processed_papers.csv')
    
    print("=" * 80)
    print("从Markdown文件创建CSV记录")
    print("=" * 80)
    print()
    
    create_csv_from_markdown(markdown_dir, csv_file)
    
    print("=" * 80)
    print("完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()